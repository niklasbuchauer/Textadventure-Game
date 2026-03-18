"""
Equipment System
================
Allows players to equip weapons, armor, shields, and accessories
into dedicated slots. Equipped items provide stat bonuses that
stack on top of the player's base stats.

Equipment slots:
  - weapon:    Increases strength / attack damage
  - armor:     Increases defense / damage reduction
  - shield:    Increases defense further
  - helm:      Head protection, various bonuses
  - boots:     Footwear, dexterity/speed bonuses
  - gloves:    Hand protection, strength/dexterity bonuses
  - accessory: Varies (perception, charisma, dexterity, etc.)

Items are moved from inventory into the equipment dict in
player.state["equipment"]. Unequipping returns them to inventory.
"""

# ═════════════════════════════════════════════════════════════════════
# RARITY SYSTEM
# ═════════════════════════════════════════════════════════════════════
# Items have a rarity tier that affects stat scaling.
# Final stats = base_material_stats × rarity_multiplier
# ═════════════════════════════════════════════════════════════════════

RARITY_TIERS = {
    "common":    {"name": "Common",    "icon": "🟢", "multiplier": 1.0,  "color": "#9e9e9e"},
    "uncommon":  {"name": "Uncommon",  "icon": "🔵", "multiplier": 1.3,  "color": "#4caf50"},
    "rare":      {"name": "Rare",      "icon": "🟡", "multiplier": 1.6,  "color": "#2196f3"},
    "epic":      {"name": "Epic",      "icon": "🟠", "multiplier": 2.0,  "color": "#9c27b0"},
    "legendary": {"name": "Legendary", "icon": "🟣", "multiplier": 2.5,  "color": "#ff9800"},
    "mythic":    {"name": "Mythic",    "icon": "⭐", "multiplier": 3.0,  "color": "#f44336"},
}

# ═════════════════════════════════════════════════════════════════════
# MATERIAL TIERS
# ═════════════════════════════════════════════════════════════════════
# Material determines base stat ranges before rarity multiplier
# ═════════════════════════════════════════════════════════════════════

MATERIAL_TIERS = {
    "cloth":       {"name": "Cloth",       "base_range": (1, 2),  "tier": 1},
    "wood":        {"name": "Wood",        "base_range": (1, 2),  "tier": 1},
    "leather":     {"name": "Leather",     "base_range": (2, 3),  "tier": 2},
    "copper":      {"name": "Copper",      "base_range": (2, 3),  "tier": 2},
    "bronze":      {"name": "Bronze",      "base_range": (3, 4),  "tier": 3},
    "iron":        {"name": "Iron",        "base_range": (3, 5),  "tier": 3},
    "steel":       {"name": "Steel",       "base_range": (5, 7),  "tier": 4},
    "silver":      {"name": "Silver",      "base_range": (5, 7),  "tier": 4},
    "gold":        {"name": "Gold",        "base_range": (6, 8),  "tier": 5},
    "mithril":     {"name": "Mithril",     "base_range": (8, 10), "tier": 5},
    "crystal":     {"name": "Crystal",     "base_range": (9, 11), "tier": 6},
    "void":        {"name": "Void",        "base_range": (10, 12), "tier": 6},
    "dragonscale": {"name": "Dragonscale", "base_range": (10, 12), "tier": 6},
    "frost":       {"name": "Frost",       "base_range": (10, 12), "tier": 6},
    "nature":      {"name": "Nature",      "base_range": (10, 12), "tier": 6},
    "soul":        {"name": "Soul",        "base_range": (11, 13), "tier": 7},
    "artifact":    {"name": "Artifact",    "base_range": (12, 15), "tier": 8},  # Mythic only
}

# ═════════════════════════════════════════════════════════════════════
# EQUIPMENT DATABASE
# ═════════════════════════════════════════════════════════════════════
# Every equippable item needs an entry here defining its slot and
# stat bonuses. Items NOT in this dict cannot be equipped.
#
# Fields:
#   name:        Display name
#   slot:        Equipment slot (weapon, armor, shield, helm, boots, gloves, accessory)
#   rarity:      Rarity tier (common, uncommon, rare, epic, legendary, mythic)
#   material:    Material tier for base stats
#   description: Flavor text
#   stats:       Stat bonuses dict
#   craftable:   Whether it can be crafted (default True)
#   source:      Where it comes from (forge, boss_name, dungeon_drop, etc.)
# ═════════════════════════════════════════════════════════════════════

EQUIPMENT_DATABASE = {
    # ══════════════════════════════════════════════════════════════════
    # WEAPONS - Common Tier
    # ══════════════════════════════════════════════════════════════════
    "wooden_club": {
        "name": "Wooden Club",
        "slot": "weapon",
        "rarity": "common",
        "material": "wood",
        "description": "A crude club fashioned from a tree branch.",
        "stats": {"strength": 1},
        "craftable": True,
        "source": "forge",
    },
    "rusty_sword": {
        "name": "Rusty Sword",
        "slot": "weapon",
        "rarity": "common",
        "material": "iron",
        "description": "A dull, corroded blade. Better than bare fists.",
        "stats": {"strength": 2},
        "craftable": False,
        "source": "dungeon_drop",
    },
    "rusty_dagger": {
        "name": "Rusty Dagger",
        "slot": "weapon",
        "rarity": "common",
        "material": "iron",
        "description": "A small, battered dagger. Barely functional.",
        "stats": {"strength": 1},
        "craftable": False,
        "source": "dungeon_drop",
    },
    "copper_dagger": {
        "name": "Copper Dagger",
        "slot": "weapon",
        "rarity": "common",
        "material": "copper",
        "description": "A simple copper blade. Light and nimble.",
        "stats": {"strength": 2, "dexterity": 1},
        "craftable": True,
        "source": "forge",
    },
    "wooden_staff": {
        "name": "Wooden Staff",
        "slot": "weapon",
        "rarity": "common",
        "material": "wood",
        "description": "A gnarled wooden staff, useful for walking and whacking.",
        "stats": {"strength": 1, "constitution": 1},
        "craftable": True,
        "source": "forge",
    },

    # ══════════════════════════════════════════════════════════════════
    # WEAPONS - Uncommon Tier
    # ══════════════════════════════════════════════════════════════════
    "iron_sword": {
        "name": "Iron Sword",
        "slot": "weapon",
        "rarity": "uncommon",
        "material": "iron",
        "description": "A sturdy iron sword. Dependable in combat.",
        "stats": {"strength": 4},
        "craftable": True,
        "source": "forge",
    },
    "iron_axe": {
        "name": "Iron Axe",
        "slot": "weapon",
        "rarity": "uncommon",
        "material": "iron",
        "description": "A heavy iron axe. Cleaves through armor.",
        "stats": {"strength": 5},
        "craftable": True,
        "source": "forge",
    },
    "iron_mace": {
        "name": "Iron Mace",
        "slot": "weapon",
        "rarity": "uncommon",
        "material": "iron",
        "description": "A brutal bludgeoning weapon. Crushes bones.",
        "stats": {"strength": 4, "constitution": 1},
        "craftable": True,
        "source": "forge",
    },
    "steel_dagger": {
        "name": "Steel Dagger",
        "slot": "weapon",
        "rarity": "uncommon",
        "material": "steel",
        "description": "A sharp, reliable dagger forged from iron and wood.",
        "stats": {"strength": 3, "dexterity": 2},
        "craftable": True,
        "source": "forge",
    },
    "bronze_spear": {
        "name": "Bronze Spear",
        "slot": "weapon",
        "rarity": "uncommon",
        "material": "bronze",
        "description": "A long-reaching spear with a bronze tip.",
        "stats": {"strength": 4, "dexterity": 1},
        "craftable": True,
        "source": "forge",
    },
    "hunting_bow": {
        "name": "Hunting Bow",
        "slot": "weapon",
        "rarity": "uncommon",
        "material": "wood",
        "description": "A well-crafted wooden bow for hunting.",
        "stats": {"strength": 3, "dexterity": 2, "perception": 1},
        "craftable": True,
        "source": "forge",
    },

    # ══════════════════════════════════════════════════════════════════
    # WEAPONS - Rare Tier
    # ══════════════════════════════════════════════════════════════════
    "steel_longsword": {
        "name": "Steel Longsword",
        "slot": "weapon",
        "rarity": "rare",
        "material": "steel",
        "description": "A long, balanced blade of tempered steel.",
        "stats": {"strength": 7, "dexterity": 2},
        "craftable": True,
        "source": "forge",
    },
    "steel_battleaxe": {
        "name": "Steel Battleaxe",
        "slot": "weapon",
        "rarity": "rare",
        "material": "steel",
        "description": "A massive two-handed axe. Devastating strikes.",
        "stats": {"strength": 9},
        "craftable": True,
        "source": "forge",
    },
    "silver_rapier": {
        "name": "Silver Rapier",
        "slot": "weapon",
        "rarity": "rare",
        "material": "silver",
        "description": "An elegant thrusting blade. Quick and precise.",
        "stats": {"strength": 5, "dexterity": 4},
        "craftable": True,
        "source": "forge",
    },
    "jeweled_dagger": {
        "name": "Jeweled Dagger",
        "slot": "weapon",
        "rarity": "rare",
        "material": "silver",
        "description": "A beautiful dagger set with precious stones. Deceptively deadly.",
        "stats": {"strength": 5, "charisma": 3},
        "craftable": True,
        "source": "forge",
    },
    "composite_bow": {
        "name": "Composite Bow",
        "slot": "weapon",
        "rarity": "rare",
        "material": "wood",
        "description": "A powerful bow made from layered materials.",
        "stats": {"strength": 6, "dexterity": 3, "perception": 2},
        "craftable": True,
        "source": "forge",
    },
    "arcane_staff": {
        "name": "Arcane Staff",
        "slot": "weapon",
        "rarity": "rare",
        "material": "silver",
        "description": "A staff crackling with magical energy.",
        "stats": {"strength": 4, "perception": 4, "charisma": 2},
        "craftable": True,
        "source": "forge",
    },
    # Monster-themed rare weapons
    "spectral_blade": {
        "name": "Spectral Blade",
        "slot": "weapon",
        "rarity": "rare",
        "material": "soul",
        "description": "A ghostly sword that phases through armor.",
        "stats": {"strength": 6, "perception": 3},
        "craftable": False,
        "source": "monster_spectral_knight",
    },
    "mimic_tooth_dagger": {
        "name": "Mimic's Tooth Dagger",
        "slot": "weapon",
        "rarity": "rare",
        "material": "iron",
        "description": "A dagger made from a mimic's razor-sharp tooth.",
        "stats": {"strength": 5, "dexterity": 3},
        "craftable": False,
        "source": "monster_mimic",
    },

    # ══════════════════════════════════════════════════════════════════
    # WEAPONS - Epic Tier
    # ══════════════════════════════════════════════════════════════════
    "mithril_blade": {
        "name": "Mithril Blade",
        "slot": "weapon",
        "rarity": "epic",
        "material": "mithril",
        "description": "Light as a feather, strong as mountains.",
        "stats": {"strength": 12, "dexterity": 4},
        "craftable": True,
        "source": "altar_iron",
    },
    "prismatic_blade": {
        "name": "Prismatic Blade",
        "slot": "weapon",
        "rarity": "epic",
        "material": "crystal",
        "description": "Splits light into deadly rainbows with each swing.",
        "stats": {"strength": 11, "perception": 4},
        "craftable": True,
        "source": "altar_crystal",
    },
    "shadow_blade": {
        "name": "Shadow Blade",
        "slot": "weapon",
        "rarity": "epic",
        "material": "void",
        "description": "Forged from void and obsidian. Cuts through shadow and steel.",
        "stats": {"strength": 10, "dexterity": 5},
        "craftable": True,
        "source": "altar_shadow",
    },
    "soul_blade": {
        "name": "Soul Blade",
        "slot": "weapon",
        "rarity": "epic",
        "material": "soul",
        "description": "Infused with spectral energy. Glows with ghostly fire.",
        "stats": {"strength": 11, "constitution": 4},
        "craftable": True,
        "source": "altar_catacomb",
    },
    "dragonbone_bow": {
        "name": "Dragonbone Bow",
        "slot": "weapon",
        "rarity": "epic",
        "material": "dragonscale",
        "description": "A bow carved from dragon bones. Arrows fly true.",
        "stats": {"strength": 10, "dexterity": 4, "perception": 3},
        "craftable": True,
        "source": "altar_iron",
    },
    "void_staff": {
        "name": "Void Staff",
        "slot": "weapon",
        "rarity": "epic",
        "material": "void",
        "description": "A staff that channels the power of the void.",
        "stats": {"strength": 8, "perception": 6, "constitution": 3},
        "craftable": True,
        "source": "altar_shadow",
    },
    # Monster-themed epic weapons
    "death_knight_blade": {
        "name": "Death Knight's Blade",
        "slot": "weapon",
        "rarity": "epic",
        "material": "soul",
        "description": "The cursed blade of a fallen knight.",
        "stats": {"strength": 12, "constitution": 3},
        "craftable": False,
        "source": "monster_death_knight",
    },
    "nightmare_scythe": {
        "name": "Nightmare Scythe",
        "slot": "weapon",
        "rarity": "epic",
        "material": "void",
        "description": "A wicked scythe that harvests nightmares.",
        "stats": {"strength": 11, "perception": 4},
        "craftable": False,
        "source": "monster_nightmare",
    },

    # ══════════════════════════════════════════════════════════════════
    # WEAPONS - Legendary Tier
    # ══════════════════════════════════════════════════════════════════
    "void_reaper": {
        "name": "Void Reaper",
        "slot": "weapon",
        "rarity": "legendary",
        "material": "void",
        "description": "A scythe forged in the deepest shadows. Consumes souls.",
        "stats": {"strength": 18, "dexterity": 5, "perception": 4},
        "craftable": True,
        "source": "rare_recipe_shadow",
    },
    "crystal_cleaver": {
        "name": "Crystal Cleaver",
        "slot": "weapon",
        "rarity": "legendary",
        "material": "crystal",
        "description": "A massive blade of living crystal. Shatters on impact, reforms instantly.",
        "stats": {"strength": 20, "perception": 5},
        "craftable": True,
        "source": "rare_recipe_crystal",
    },
    "frostbite_blade": {
        "name": "Frostbite",
        "slot": "weapon",
        "rarity": "legendary",
        "material": "frost",
        "description": "A blade of eternal ice. Freezes foes solid.",
        "stats": {"strength": 17, "dexterity": 6, "constitution": 4},
        "craftable": True,
        "source": "rare_recipe_frost",
    },
    "worldtree_branch": {
        "name": "Worldtree Branch",
        "slot": "weapon",
        "rarity": "legendary",
        "material": "nature",
        "description": "A living weapon from the heart of the ancient forest.",
        "stats": {"strength": 16, "constitution": 6, "perception": 5},
        "craftable": True,
        "source": "rare_recipe_verdant",
    },

    # ══════════════════════════════════════════════════════════════════
    # WEAPONS - Mythic Tier (Boss Drops Only)
    # ══════════════════════════════════════════════════════════════════
    "titans_crystalline_edge": {
        "name": "Titan's Crystalline Edge",
        "slot": "weapon",
        "rarity": "mythic",
        "material": "artifact",
        "description": "A blade carved from the heart of the Crystal Titan itself.",
        "stats": {"strength": 28, "defense": 8, "perception": 6},
        "craftable": False,
        "source": "boss_crystal_titan",
    },
    "forgemasters_warhammer": {
        "name": "Forgemaster's Warhammer",
        "slot": "weapon",
        "rarity": "mythic",
        "material": "artifact",
        "description": "The legendary hammer of the Iron Forgemaster. Sunders all armor.",
        "stats": {"strength": 32, "constitution": 8},
        "craftable": False,
        "source": "boss_iron_forgemaster",
    },
    "sovereigns_edge": {
        "name": "Sovereign's Edge",
        "slot": "weapon",
        "rarity": "mythic",
        "material": "artifact",
        "description": "The Shadow Sovereign's personal blade. Cuts through reality.",
        "stats": {"strength": 30, "dexterity": 10, "perception": 5},
        "craftable": False,
        "source": "boss_shadow_sovereign",
    },
    "lich_king_soul_blade": {
        "name": "Soul Blade of the Lich King",
        "slot": "weapon",
        "rarity": "mythic",
        "material": "artifact",
        "description": "The Lich King's phylactery-bound weapon. Steals souls with every strike.",
        "stats": {"strength": 28, "constitution": 10, "perception": 6},
        "craftable": False,
        "source": "boss_lich_king",
    },
    "frostbite_mythic": {
        "name": "Frostbite, Blade of Eternal Winter",
        "slot": "weapon",
        "rarity": "mythic",
        "material": "artifact",
        "description": "The legendary blade of the Frost Sovereign. Absolute zero given form.",
        "stats": {"strength": 35, "defense": 6, "dexterity": 8},
        "craftable": False,
        "source": "boss_frost_sovereign",
    },
    "verdant_wrath": {
        "name": "Verdant Wrath",
        "slot": "weapon",
        "rarity": "mythic",
        "material": "artifact",
        "description": "A living blade grown from the Verdant Guardian's heart.",
        "stats": {"strength": 33, "constitution": 12, "perception": 5},
        "craftable": False,
        "source": "boss_verdant_guardian",
    },
    # Craftable Mythic Weapons (require multiple boss materials)
    "chromatic_annihilator": {
        "name": "Chromatic Annihilator",
        "slot": "weapon",
        "rarity": "mythic",
        "material": "artifact",
        "description": "Forged from crystallized light and eternal flame. Devastation incarnate.",
        "stats": {"strength": 30, "perception": 8, "dexterity": 6},
        "craftable": True,
        "source": "altar_crystal",
    },
    "soulreaver_blade": {
        "name": "Soulreaver Blade",
        "slot": "weapon",
        "rarity": "mythic",
        "material": "artifact",
        "description": "A blade that devours souls and grows stronger.",
        "stats": {"strength": 28, "constitution": 8, "charisma": 6},
        "craftable": True,
        "source": "altar_catacomb",
    },

    # ══════════════════════════════════════════════════════════════════
    # ARMOR - Common Tier
    # ══════════════════════════════════════════════════════════════════
    "cloth_robes": {
        "name": "Cloth Robes",
        "slot": "armor",
        "rarity": "common",
        "material": "cloth",
        "description": "Simple cloth robes. Offer minimal protection.",
        "stats": {"defense": 1},
        "craftable": True,
        "source": "forge",
    },
    "padded_vest": {
        "name": "Padded Vest",
        "slot": "armor",
        "rarity": "common",
        "material": "cloth",
        "description": "A quilted vest. Better than nothing.",
        "stats": {"defense": 2},
        "craftable": True,
        "source": "forge",
    },

    # ══════════════════════════════════════════════════════════════════
    # ARMOR - Uncommon Tier
    # ══════════════════════════════════════════════════════════════════
    "leather_armor_piece": {
        "name": "Leather Armor",
        "slot": "armor",
        "rarity": "uncommon",
        "material": "leather",
        "description": "Light armor stitched from wolf pelts. Decent protection.",
        "stats": {"defense": 4, "dexterity": 1},
        "craftable": True,
        "source": "forge",
    },
    "bronze_chainmail": {
        "name": "Bronze Chainmail",
        "slot": "armor",
        "rarity": "uncommon",
        "material": "bronze",
        "description": "Interlocking bronze rings. Flexible yet protective.",
        "stats": {"defense": 5},
        "craftable": True,
        "source": "forge",
    },
    "ranger_leathers": {
        "name": "Ranger Leathers",
        "slot": "armor",
        "rarity": "uncommon",
        "material": "leather",
        "description": "Forest-green leather armor favored by scouts.",
        "stats": {"defense": 3, "dexterity": 2, "perception": 1},
        "craftable": True,
        "source": "forge",
    },

    # ══════════════════════════════════════════════════════════════════
    # ARMOR - Rare Tier
    # ══════════════════════════════════════════════════════════════════
    "iron_chainmail": {
        "name": "Iron Chainmail",
        "slot": "armor",
        "rarity": "rare",
        "material": "iron",
        "description": "Heavy iron chainmail. Solid protection.",
        "stats": {"defense": 7},
        "craftable": True,
        "source": "forge",
    },
    "steel_plate_armor": {
        "name": "Steel Plate Armor",
        "slot": "armor",
        "rarity": "rare",
        "material": "steel",
        "description": "Full plate armor. Heavy but extremely protective.",
        "stats": {"defense": 10, "constitution": 1},
        "craftable": True,
        "source": "forge",
    },
    "silver_threaded_robes": {
        "name": "Silver-threaded Robes",
        "slot": "armor",
        "rarity": "rare",
        "material": "silver",
        "description": "Elegant robes woven with silver threads. Magically resistant.",
        "stats": {"defense": 5, "perception": 3, "charisma": 2},
        "craftable": True,
        "source": "forge",
    },
    # Monster-themed rare armor
    "nightmare_cloak": {
        "name": "Nightmare Cloak",
        "slot": "armor",
        "rarity": "rare",
        "material": "void",
        "description": "A cloak woven from nightmares. Shrouds the wearer in fear.",
        "stats": {"defense": 6, "dexterity": 3, "perception": 2},
        "craftable": False,
        "source": "monster_nightmare",
    },

    # ══════════════════════════════════════════════════════════════════
    # ARMOR - Epic Tier
    # ══════════════════════════════════════════════════════════════════
    "mithril_chainmail": {
        "name": "Mithril Chainmail",
        "slot": "armor",
        "rarity": "epic",
        "material": "mithril",
        "description": "Featherlight mithril links. Supreme protection without weight.",
        "stats": {"defense": 14, "dexterity": 3},
        "craftable": True,
        "source": "altar_iron",
    },
    "dwarven_masterwork": {
        "name": "Dwarven Masterwork Armor",
        "slot": "armor",
        "rarity": "epic",
        "material": "mithril",
        "description": "Forged using ancient dwarven techniques. Nearly indestructible.",
        "stats": {"defense": 16, "constitution": 5},
        "craftable": True,
        "source": "altar_iron",
    },
    "sovereign_cloak": {
        "name": "Sovereign's Cloak",
        "slot": "armor",
        "rarity": "epic",
        "material": "void",
        "description": "Woven from the Shadow Sovereign's essence. Grants partial invisibility.",
        "stats": {"defense": 10, "dexterity": 5, "perception": 4},
        "craftable": True,
        "source": "altar_shadow",
    },
    "dragonhide_armor": {
        "name": "Dragonhide Armor",
        "slot": "armor",
        "rarity": "epic",
        "material": "dragonscale",
        "description": "Armor made from dragon scales. Fire-resistant and tough.",
        "stats": {"defense": 15, "constitution": 4},
        "craftable": True,
        "source": "altar_iron",
    },
    # Monster-themed epic armor
    "colossus_ribcage_plate": {
        "name": "Colossus Ribcage Plate",
        "slot": "armor",
        "rarity": "epic",
        "material": "soul",
        "description": "Armor fashioned from the Bone Colossus's ribs.",
        "stats": {"defense": 14, "constitution": 4},
        "craftable": False,
        "source": "miniboss_bone_colossus",
    },
    "warden_plating": {
        "name": "Iron Warden Plating",
        "slot": "armor",
        "rarity": "epic",
        "material": "iron",
        "description": "Salvaged plates from the Iron Warden automaton.",
        "stats": {"defense": 16, "constitution": 2},
        "craftable": False,
        "source": "miniboss_iron_warden",
    },

    # ══════════════════════════════════════════════════════════════════
    # ARMOR - Legendary Tier
    # ══════════════════════════════════════════════════════════════════
    "crystal_aegis_armor": {
        "name": "Crystal Aegis",
        "slot": "armor",
        "rarity": "legendary",
        "material": "crystal",
        "description": "Living crystal that grows to absorb impacts.",
        "stats": {"defense": 22, "perception": 5, "constitution": 4},
        "craftable": True,
        "source": "rare_recipe_crystal",
    },
    "glacial_plate": {
        "name": "Glacial Plate",
        "slot": "armor",
        "rarity": "legendary",
        "material": "frost",
        "description": "Armor forged from eternal ice. Cold emanates from every joint.",
        "stats": {"defense": 24, "constitution": 6},
        "craftable": True,
        "source": "rare_recipe_frost",
    },
    "guardian_bark_armor": {
        "name": "Guardian's Bark Armor",
        "slot": "armor",
        "rarity": "legendary",
        "material": "nature",
        "description": "Living wood armor that regenerates damage.",
        "stats": {"defense": 20, "constitution": 8},
        "craftable": True,
        "source": "rare_recipe_verdant",
    },

    # ══════════════════════════════════════════════════════════════════
    # ARMOR - Mythic Tier (Boss Drops & Craftable)
    # ══════════════════════════════════════════════════════════════════
    "titans_carapace": {
        "name": "Titan's Carapace",
        "slot": "armor",
        "rarity": "mythic",
        "material": "artifact",
        "description": "The outer shell of the Crystal Titan. Near-impervious.",
        "stats": {"defense": 35, "constitution": 10, "perception": 4},
        "craftable": False,
        "source": "boss_crystal_titan",
    },
    "forgemasters_plate": {
        "name": "Forgemaster's Eternal Plate",
        "slot": "armor",
        "rarity": "mythic",
        "material": "artifact",
        "description": "Armor worn by the Iron Forgemaster for millennia.",
        "stats": {"defense": 38, "constitution": 12},
        "craftable": False,
        "source": "boss_iron_forgemaster",
    },
    "cloak_of_eternal_night": {
        "name": "Cloak of Eternal Night",
        "slot": "armor",
        "rarity": "mythic",
        "material": "artifact",
        "description": "The Shadow Sovereign's mantle. Darkness made manifest.",
        "stats": {"defense": 28, "dexterity": 12, "perception": 8},
        "craftable": False,
        "source": "boss_shadow_sovereign",
    },
    "deathshroud_robes": {
        "name": "Deathshroud Robes",
        "slot": "armor",
        "rarity": "mythic",
        "material": "artifact",
        "description": "The Lich King's burial shroud. Death cannot touch its wearer.",
        "stats": {"defense": 26, "constitution": 14, "perception": 6},
        "craftable": False,
        "source": "boss_lich_king",
    },
    "glacial_sovereign_plate": {
        "name": "Glacial Sovereign Plate",
        "slot": "armor",
        "rarity": "mythic",
        "material": "artifact",
        "description": "Armor of the Frost Sovereign. Cold so absolute it burns.",
        "stats": {"defense": 40, "constitution": 8, "dexterity": 5},
        "craftable": False,
        "source": "boss_frost_sovereign",
    },
    "worldtree_bark_plate": {
        "name": "Worldtree Bark Plate",
        "slot": "armor",
        "rarity": "mythic",
        "material": "artifact",
        "description": "Grown from the Verdant Guardian's heartwood. Eternally regenerating.",
        "stats": {"defense": 38, "constitution": 15},
        "craftable": False,
        "source": "boss_verdant_guardian",
    },
    # Craftable Mythic Armor
    "worldforged_plate": {
        "name": "Worldforged Plate",
        "slot": "armor",
        "rarity": "mythic",
        "material": "artifact",
        "description": "Armor forged from the essence of multiple realms.",
        "stats": {"defense": 32, "constitution": 10, "dexterity": 4},
        "craftable": True,
        "source": "altar_iron",
    },
    "abyssal_vestments": {
        "name": "Abyssal Vestments",
        "slot": "armor",
        "rarity": "mythic",
        "material": "artifact",
        "description": "Robes woven from void and shadow essence.",
        "stats": {"defense": 25, "dexterity": 8, "perception": 10},
        "craftable": True,
        "source": "altar_shadow",
    },

    # ══════════════════════════════════════════════════════════════════
    # SHIELDS - Common to Legendary
    # ══════════════════════════════════════════════════════════════════
    "wooden_buckler": {
        "name": "Wooden Buckler",
        "slot": "shield",
        "rarity": "common",
        "material": "wood",
        "description": "A small wooden shield. Light and easy to use.",
        "stats": {"defense": 1},
        "craftable": True,
        "source": "forge",
    },
    "broken_shield": {
        "name": "Broken Shield",
        "slot": "shield",
        "rarity": "common",
        "material": "iron",
        "description": "A battered shield. Still blocks some blows.",
        "stats": {"defense": 2},
        "craftable": False,
        "source": "dungeon_drop",
    },
    "copper_shield": {
        "name": "Copper Shield",
        "slot": "shield",
        "rarity": "uncommon",
        "material": "copper",
        "description": "A simple copper shield. Reliable protection.",
        "stats": {"defense": 3},
        "craftable": True,
        "source": "forge",
    },
    "iron_kite_shield": {
        "name": "Iron Kite Shield",
        "slot": "shield",
        "rarity": "uncommon",
        "material": "iron",
        "description": "A large iron shield shaped like a kite.",
        "stats": {"defense": 5},
        "craftable": True,
        "source": "forge",
    },
    "steel_tower_shield": {
        "name": "Steel Tower Shield",
        "slot": "shield",
        "rarity": "rare",
        "material": "steel",
        "description": "A massive tower shield. Full body protection.",
        "stats": {"defense": 8, "constitution": 1},
        "craftable": True,
        "source": "forge",
    },
    "silver_mirror_shield": {
        "name": "Silver Mirror Shield",
        "slot": "shield",
        "rarity": "rare",
        "material": "silver",
        "description": "A polished silver shield that reflects magic.",
        "stats": {"defense": 6, "perception": 2},
        "craftable": True,
        "source": "forge",
    },
    "masterwork_shield": {
        "name": "Masterwork Shield",
        "slot": "shield",
        "rarity": "rare",
        "material": "steel",
        "description": "Reforged from scrap into something magnificent.",
        "stats": {"defense": 7, "constitution": 2},
        "craftable": True,
        "source": "forge",
    },
    "mithril_bulwark": {
        "name": "Mithril Bulwark",
        "slot": "shield",
        "rarity": "epic",
        "material": "mithril",
        "description": "An impossibly light yet sturdy mithril shield.",
        "stats": {"defense": 12, "dexterity": 2},
        "craftable": True,
        "source": "altar_iron",
    },
    "crystal_shield": {
        "name": "Crystal Shield",
        "slot": "shield",
        "rarity": "epic",
        "material": "crystal",
        "description": "Living crystal that refracts attacks into harmless light.",
        "stats": {"defense": 10, "perception": 3},
        "craftable": True,
        "source": "altar_crystal",
    },
    "warden_core_shield": {
        "name": "Warden Core Shield",
        "slot": "shield",
        "rarity": "epic",
        "material": "iron",
        "description": "Salvaged from the Iron Warden's core plating.",
        "stats": {"defense": 14, "constitution": 3},
        "craftable": False,
        "source": "miniboss_iron_warden",
    },
    "dragonscale_ward": {
        "name": "Dragonscale Ward",
        "slot": "shield",
        "rarity": "legendary",
        "material": "dragonscale",
        "description": "A shield of overlapping dragon scales.",
        "stats": {"defense": 18, "constitution": 4},
        "craftable": True,
        "source": "altar_iron",
    },
    "abyssal_aegis": {
        "name": "Abyssal Aegis",
        "slot": "shield",
        "rarity": "mythic",
        "material": "artifact",
        "description": "A shield that absorbs attacks into the void.",
        "stats": {"defense": 25, "constitution": 8, "perception": 4},
        "craftable": True,
        "source": "altar_shadow",
    },
    "eternal_anvil_shield": {
        "name": "Eternal Anvil Shield",
        "slot": "shield",
        "rarity": "mythic",
        "material": "artifact",
        "description": "The Forgemaster's personal shield, forged on the Eternal Anvil.",
        "stats": {"defense": 28, "constitution": 10},
        "craftable": False,
        "source": "boss_iron_forgemaster",
    },

    # ══════════════════════════════════════════════════════════════════
    # HELMS - All Tiers (NEW SLOT)
    # ══════════════════════════════════════════════════════════════════
    "cloth_cap": {
        "name": "Cloth Cap",
        "slot": "helm",
        "rarity": "common",
        "material": "cloth",
        "description": "A simple cloth cap. Barely protective.",
        "stats": {"defense": 1},
        "craftable": True,
        "source": "forge",
    },
    "leather_hood": {
        "name": "Leather Hood",
        "slot": "helm",
        "rarity": "uncommon",
        "material": "leather",
        "description": "A sturdy leather hood with good coverage.",
        "stats": {"defense": 2, "perception": 1},
        "craftable": True,
        "source": "forge",
    },
    "bronze_circlet": {
        "name": "Bronze Circlet",
        "slot": "helm",
        "rarity": "uncommon",
        "material": "bronze",
        "description": "A simple bronze circlet. Marks minor nobility.",
        "stats": {"defense": 2, "charisma": 1},
        "craftable": True,
        "source": "forge",
    },
    "iron_helm": {
        "name": "Iron Helm",
        "slot": "helm",
        "rarity": "rare",
        "material": "iron",
        "description": "A solid iron helmet. Standard military issue.",
        "stats": {"defense": 5},
        "craftable": True,
        "source": "forge",
    },
    "steel_greathelm": {
        "name": "Steel Greathelm",
        "slot": "helm",
        "rarity": "rare",
        "material": "steel",
        "description": "A full steel helm. Complete head protection.",
        "stats": {"defense": 7, "constitution": 1},
        "craftable": True,
        "source": "forge",
    },
    "silver_circlet": {
        "name": "Silver Circlet",
        "slot": "helm",
        "rarity": "rare",
        "material": "silver",
        "description": "An elegant silver circlet. Enhances mental focus.",
        "stats": {"defense": 3, "perception": 3, "charisma": 2},
        "craftable": True,
        "source": "forge",
    },
    "stalkers_hood": {
        "name": "Stalker's Hood",
        "slot": "helm",
        "rarity": "epic",
        "material": "void",
        "description": "A hood from a Shadow Stalker. See in darkness.",
        "stats": {"defense": 6, "dexterity": 4, "perception": 4},
        "craftable": False,
        "source": "monster_shadow_stalker",
    },
    "bonewrought_helm": {
        "name": "Bonewrought Helm",
        "slot": "helm",
        "rarity": "epic",
        "material": "soul",
        "description": "A helm fused from bones of the fallen.",
        "stats": {"defense": 10, "constitution": 4},
        "craftable": False,
        "source": "miniboss_bone_colossus",
    },
    "weaver_cowl": {
        "name": "Void Weaver's Cowl",
        "slot": "helm",
        "rarity": "epic",
        "material": "void",
        "description": "The cowl of a Void Weaver. See between dimensions.",
        "stats": {"defense": 8, "perception": 6, "dexterity": 3},
        "craftable": False,
        "source": "miniboss_void_weaver",
    },
    "mithril_crown": {
        "name": "Mithril Crown",
        "slot": "helm",
        "rarity": "epic",
        "material": "mithril",
        "description": "A crown of pure mithril. Light yet majestic.",
        "stats": {"defense": 9, "charisma": 4, "perception": 3},
        "craftable": True,
        "source": "altar_iron",
    },
    "crystal_diadem": {
        "name": "Crystal Diadem",
        "slot": "helm",
        "rarity": "legendary",
        "material": "crystal",
        "description": "A crown of living crystal. Amplifies the mind.",
        "stats": {"defense": 14, "perception": 6, "charisma": 4},
        "craftable": True,
        "source": "rare_recipe_crystal",
    },
    "crown_of_eternal_winter": {
        "name": "Crown of Eternal Winter",
        "slot": "helm",
        "rarity": "legendary",
        "material": "frost",
        "description": "A crown of eternal ice. Creates a blizzard aura.",
        "stats": {"defense": 16, "constitution": 6, "perception": 4},
        "craftable": True,
        "source": "rare_recipe_frost",
    },
    "crown_of_the_wild": {
        "name": "Crown of the Wild",
        "slot": "helm",
        "rarity": "legendary",
        "material": "nature",
        "description": "A crown of living vines and flowers.",
        "stats": {"defense": 14, "constitution": 8, "perception": 4},
        "craftable": True,
        "source": "rare_recipe_verdant",
    },
    # Mythic Helms
    "prismatic_crown": {
        "name": "Prismatic Crown",
        "slot": "helm",
        "rarity": "mythic",
        "material": "artifact",
        "description": "A crown that refracts all damage into harmless light.",
        "stats": {"defense": 22, "perception": 10, "charisma": 6},
        "craftable": False,
        "source": "boss_crystal_titan",
    },
    "forgemasters_helm": {
        "name": "Forgemaster's Helm",
        "slot": "helm",
        "rarity": "mythic",
        "material": "artifact",
        "description": "The helm of the Iron Forgemaster. Fire cannot harm.",
        "stats": {"defense": 25, "constitution": 10},
        "craftable": False,
        "source": "boss_iron_forgemaster",
    },
    "void_crown": {
        "name": "Void Crown",
        "slot": "helm",
        "rarity": "mythic",
        "material": "artifact",
        "description": "The Shadow Sovereign's crown. Inspires terror.",
        "stats": {"defense": 20, "perception": 8, "dexterity": 8, "charisma": 6},
        "craftable": False,
        "source": "boss_shadow_sovereign",
    },
    "crown_of_the_lich_king": {
        "name": "Crown of the Lich King",
        "slot": "helm",
        "rarity": "mythic",
        "material": "artifact",
        "description": "The Lich King's crown of dominion. Commands the dead.",
        "stats": {"defense": 22, "perception": 10, "constitution": 8},
        "craftable": False,
        "source": "boss_lich_king",
    },
    "frost_sovereign_crown": {
        "name": "Frost Sovereign's Crown",
        "slot": "helm",
        "rarity": "mythic",
        "material": "artifact",
        "description": "The crown of absolute cold. Freezes all who approach.",
        "stats": {"defense": 28, "constitution": 8, "perception": 6},
        "craftable": False,
        "source": "boss_frost_sovereign",
    },
    "worldtree_crown": {
        "name": "Worldtree Crown",
        "slot": "helm",
        "rarity": "mythic",
        "material": "artifact",
        "description": "A crown grown from the Verdant Guardian's essence.",
        "stats": {"defense": 24, "constitution": 12, "perception": 6},
        "craftable": False,
        "source": "boss_verdant_guardian",
    },
    # Craftable Mythic Helm
    "crown_of_the_ancients": {
        "name": "Crown of the Ancients",
        "slot": "helm",
        "rarity": "mythic",
        "material": "artifact",
        "description": "A crown restored from fragments of the Lich King's phylactery.",
        "stats": {"defense": 20, "perception": 8, "constitution": 8, "charisma": 6},
        "craftable": True,
        "source": "altar_catacomb",
    },

    # ══════════════════════════════════════════════════════════════════
    # BOOTS - All Tiers (NEW SLOT)
    # ══════════════════════════════════════════════════════════════════
    "sandals": {
        "name": "Sandals",
        "slot": "boots",
        "rarity": "common",
        "material": "cloth",
        "description": "Simple sandals. Offer no protection.",
        "stats": {"dexterity": 1},
        "craftable": True,
        "source": "forge",
    },
    "cloth_wraps": {
        "name": "Cloth Foot Wraps",
        "slot": "boots",
        "rarity": "common",
        "material": "cloth",
        "description": "Cloth wrapped around the feet. Basic footwear.",
        "stats": {"defense": 1},
        "craftable": True,
        "source": "forge",
    },
    "leather_boots": {
        "name": "Leather Boots",
        "slot": "boots",
        "rarity": "uncommon",
        "material": "leather",
        "description": "Sturdy leather boots. Good for traveling.",
        "stats": {"defense": 2, "dexterity": 2},
        "craftable": True,
        "source": "forge",
    },
    "travelers_boots": {
        "name": "Traveler's Boots",
        "slot": "boots",
        "rarity": "uncommon",
        "material": "leather",
        "description": "Well-worn boots built for long journeys.",
        "stats": {"defense": 1, "dexterity": 3, "constitution": 1},
        "craftable": True,
        "source": "forge",
    },
    "iron_boots": {
        "name": "Iron Boots",
        "slot": "boots",
        "rarity": "rare",
        "material": "iron",
        "description": "Heavy iron boots. Crushing kicks.",
        "stats": {"defense": 5, "strength": 1},
        "craftable": True,
        "source": "forge",
    },
    "steel_greaves": {
        "name": "Steel Greaves",
        "slot": "boots",
        "rarity": "rare",
        "material": "steel",
        "description": "Protective steel leg armor.",
        "stats": {"defense": 6, "constitution": 1},
        "craftable": True,
        "source": "forge",
    },
    "silvertipped_boots": {
        "name": "Silver-tipped Boots",
        "slot": "boots",
        "rarity": "rare",
        "material": "silver",
        "description": "Elegant boots with silver toe caps.",
        "stats": {"defense": 4, "dexterity": 3, "charisma": 1},
        "craftable": True,
        "source": "forge",
    },
    "wyrm_scale_boots": {
        "name": "Wyrm Scale Boots",
        "slot": "boots",
        "rarity": "epic",
        "material": "dragonscale",
        "description": "Boots made from gem wyrm scales.",
        "stats": {"defense": 9, "dexterity": 4},
        "craftable": False,
        "source": "monster_gem_wyrm",
    },
    "phase_shift_boots": {
        "name": "Phase Shift Boots",
        "slot": "boots",
        "rarity": "epic",
        "material": "void",
        "description": "Boots that allow brief dimensional shifts.",
        "stats": {"defense": 6, "dexterity": 6, "perception": 3},
        "craftable": False,
        "source": "miniboss_void_weaver",
    },
    "mithril_sabatons": {
        "name": "Mithril Sabatons",
        "slot": "boots",
        "rarity": "epic",
        "material": "mithril",
        "description": "Lightweight yet incredibly protective footwear.",
        "stats": {"defense": 10, "dexterity": 4},
        "craftable": True,
        "source": "altar_iron",
    },
    "winged_boots": {
        "name": "Winged Boots",
        "slot": "boots",
        "rarity": "legendary",
        "material": "crystal",
        "description": "Boots with crystalline wings. Grant incredible speed.",
        "stats": {"defense": 8, "dexterity": 10, "perception": 4},
        "craftable": True,
        "source": "rare_recipe_crystal",
    },
    "rootwalker_boots": {
        "name": "Rootwalker Boots",
        "slot": "boots",
        "rarity": "legendary",
        "material": "nature",
        "description": "Living root boots. Walk on any terrain.",
        "stats": {"defense": 10, "dexterity": 6, "constitution": 6},
        "craftable": True,
        "source": "rare_recipe_verdant",
    },
    "permafrost_boots": {
        "name": "Permafrost Boots",
        "slot": "boots",
        "rarity": "legendary",
        "material": "frost",
        "description": "Boots of eternal ice. Leave frost in your wake.",
        "stats": {"defense": 12, "dexterity": 5, "constitution": 5},
        "craftable": True,
        "source": "rare_recipe_frost",
    },
    # Mythic Boots
    "shadow_walker_treads": {
        "name": "Shadow Walker's Treads",
        "slot": "boots",
        "rarity": "mythic",
        "material": "artifact",
        "description": "The Shadow Sovereign's boots. Walk between shadows.",
        "stats": {"defense": 15, "dexterity": 15, "perception": 8},
        "craftable": False,
        "source": "boss_shadow_sovereign",
    },
    "ironclad_greaves": {
        "name": "Ironclad Greaves",
        "slot": "boots",
        "rarity": "mythic",
        "material": "artifact",
        "description": "The Forgemaster's personal leg armor.",
        "stats": {"defense": 20, "strength": 8, "constitution": 6},
        "craftable": False,
        "source": "boss_iron_forgemaster",
    },
    "titan_treads": {
        "name": "Titan Treads",
        "slot": "boots",
        "rarity": "mythic",
        "material": "artifact",
        "description": "Boots carved from the Crystal Titan's feet.",
        "stats": {"defense": 18, "strength": 6, "dexterity": 8, "perception": 4},
        "craftable": False,
        "source": "boss_crystal_titan",
    },
    "lichbone_greaves": {
        "name": "Lichbone Greaves",
        "slot": "boots",
        "rarity": "mythic",
        "material": "artifact",
        "description": "Greaves made from the Lich King's bones.",
        "stats": {"defense": 16, "constitution": 12, "perception": 6},
        "craftable": False,
        "source": "boss_lich_king",
    },
    "glacial_striders": {
        "name": "Glacial Striders",
        "slot": "boots",
        "rarity": "mythic",
        "material": "artifact",
        "description": "The Frost Sovereign's boots. Freeze the ground.",
        "stats": {"defense": 20, "dexterity": 10, "constitution": 8},
        "craftable": False,
        "source": "boss_frost_sovereign",
    },
    "rootwarden_greaves": {
        "name": "Rootwarden Greaves",
        "slot": "boots",
        "rarity": "mythic",
        "material": "artifact",
        "description": "Grown from the Verdant Guardian's roots.",
        "stats": {"defense": 18, "constitution": 14, "dexterity": 6},
        "craftable": False,
        "source": "boss_verdant_guardian",
    },
    # Craftable Mythic Boots
    "boots_of_the_void_walker": {
        "name": "Boots of the Void Walker",
        "slot": "boots",
        "rarity": "mythic",
        "material": "artifact",
        "description": "Phase through reality itself.",
        "stats": {"defense": 14, "dexterity": 14, "perception": 10},
        "craftable": True,
        "source": "altar_shadow",
    },

    # ══════════════════════════════════════════════════════════════════
    # GLOVES - All Tiers (NEW SLOT)
    # ══════════════════════════════════════════════════════════════════
    "cloth_gloves": {
        "name": "Cloth Gloves",
        "slot": "gloves",
        "rarity": "common",
        "material": "cloth",
        "description": "Simple cloth gloves. Barely protective.",
        "stats": {"dexterity": 1},
        "craftable": True,
        "source": "forge",
    },
    "cloth_wraps_hands": {
        "name": "Hand Wraps",
        "slot": "gloves",
        "rarity": "common",
        "material": "cloth",
        "description": "Cloth wrapped around the hands.",
        "stats": {"strength": 1},
        "craftable": True,
        "source": "forge",
    },
    "leather_gloves": {
        "name": "Leather Gloves",
        "slot": "gloves",
        "rarity": "uncommon",
        "material": "leather",
        "description": "Sturdy leather gloves. Good grip.",
        "stats": {"defense": 1, "dexterity": 2},
        "craftable": True,
        "source": "forge",
    },
    "leather_bracers": {
        "name": "Leather Bracers",
        "slot": "gloves",
        "rarity": "uncommon",
        "material": "leather",
        "description": "Forearm guards of hardened leather.",
        "stats": {"defense": 2, "strength": 1},
        "craftable": True,
        "source": "forge",
    },
    "chainmail_gloves": {
        "name": "Chainmail Gloves",
        "slot": "gloves",
        "rarity": "rare",
        "material": "iron",
        "description": "Flexible chain gloves. Good protection.",
        "stats": {"defense": 4, "strength": 2},
        "craftable": True,
        "source": "forge",
    },
    "steel_gauntlets": {
        "name": "Steel Gauntlets",
        "slot": "gloves",
        "rarity": "rare",
        "material": "steel",
        "description": "Heavy steel gauntlets. Crushing grip.",
        "stats": {"defense": 5, "strength": 3},
        "craftable": True,
        "source": "forge",
    },
    "silver_bracers": {
        "name": "Silver Bracers",
        "slot": "gloves",
        "rarity": "rare",
        "material": "silver",
        "description": "Elegant silver bracers with arcane inscriptions.",
        "stats": {"defense": 3, "perception": 3, "charisma": 1},
        "craftable": True,
        "source": "forge",
    },
    "spidersilk_gloves": {
        "name": "Spidersilk Gloves",
        "slot": "gloves",
        "rarity": "epic",
        "material": "crystal",
        "description": "Gloves woven from crystal spider silk.",
        "stats": {"defense": 5, "dexterity": 6, "perception": 3},
        "craftable": False,
        "source": "miniboss_crystal_matriarch",
    },
    "ember_gauntlets": {
        "name": "Ember Gauntlets",
        "slot": "gloves",
        "rarity": "epic",
        "material": "iron",
        "description": "Gauntlets infused with forge elemental fire.",
        "stats": {"defense": 8, "strength": 6},
        "craftable": False,
        "source": "monster_forge_elemental",
    },
    "wraith_touch_gloves": {
        "name": "Wraith Touch Gloves",
        "slot": "gloves",
        "rarity": "epic",
        "material": "void",
        "description": "Ghostly gloves that phase through armor.",
        "stats": {"defense": 5, "strength": 5, "dexterity": 4},
        "craftable": False,
        "source": "monster_void_wraith",
    },
    "mithril_vambraces": {
        "name": "Mithril Vambraces",
        "slot": "gloves",
        "rarity": "epic",
        "material": "mithril",
        "description": "Mithril arm guards. Light as air.",
        "stats": {"defense": 8, "dexterity": 4, "strength": 3},
        "craftable": True,
        "source": "altar_iron",
    },
    "dragonhide_grips": {
        "name": "Dragonhide Grips",
        "slot": "gloves",
        "rarity": "legendary",
        "material": "dragonscale",
        "description": "Gloves of dragon hide. Unyielding grip.",
        "stats": {"defense": 10, "strength": 8, "dexterity": 4},
        "craftable": True,
        "source": "altar_iron",
    },
    "crystal_focus_gloves": {
        "name": "Crystal Focus Gloves",
        "slot": "gloves",
        "rarity": "legendary",
        "material": "crystal",
        "description": "Channel magical energy with precision.",
        "stats": {"defense": 8, "perception": 8, "dexterity": 6},
        "craftable": True,
        "source": "rare_recipe_crystal",
    },
    "frostweave_gloves": {
        "name": "Frostweave Gloves",
        "slot": "gloves",
        "rarity": "legendary",
        "material": "frost",
        "description": "Gloves of woven frost. Touch freezes.",
        "stats": {"defense": 10, "dexterity": 6, "strength": 6},
        "craftable": True,
        "source": "rare_recipe_frost",
    },
    "vinegrasp_gloves": {
        "name": "Vinegrasp Gloves",
        "slot": "gloves",
        "rarity": "legendary",
        "material": "nature",
        "description": "Living vine gloves. Unbreakable grip.",
        "stats": {"defense": 8, "strength": 8, "constitution": 6},
        "craftable": True,
        "source": "rare_recipe_verdant",
    },
    # Mythic Gloves
    "titans_grasp": {
        "name": "Titan's Grasp",
        "slot": "gloves",
        "rarity": "mythic",
        "material": "artifact",
        "description": "The Crystal Titan's hands. Shatter anything.",
        "stats": {"defense": 18, "strength": 15, "perception": 6},
        "craftable": False,
        "source": "boss_crystal_titan",
    },
    "molten_gauntlets": {
        "name": "Molten Gauntlets",
        "slot": "gloves",
        "rarity": "mythic",
        "material": "artifact",
        "description": "The Forgemaster's forge-hot gauntlets.",
        "stats": {"defense": 16, "strength": 18, "constitution": 6},
        "craftable": False,
        "source": "boss_iron_forgemaster",
    },
    "void_grasp": {
        "name": "Void Grasp",
        "slot": "gloves",
        "rarity": "mythic",
        "material": "artifact",
        "description": "Gloves that reach into the void.",
        "stats": {"defense": 14, "strength": 10, "dexterity": 10, "perception": 6},
        "craftable": False,
        "source": "boss_shadow_sovereign",
    },
    "bonelord_gauntlets": {
        "name": "Bonelord Gauntlets",
        "slot": "gloves",
        "rarity": "mythic",
        "material": "artifact",
        "description": "The Lich King's phylactery-bone gauntlets.",
        "stats": {"defense": 16, "strength": 12, "constitution": 10},
        "craftable": False,
        "source": "boss_lich_king",
    },
    "permafrost_gauntlets": {
        "name": "Permafrost Gauntlets",
        "slot": "gloves",
        "rarity": "mythic",
        "material": "artifact",
        "description": "Gauntlets of the Frost Sovereign. Eternal cold.",
        "stats": {"defense": 18, "strength": 14, "constitution": 8},
        "craftable": False,
        "source": "boss_frost_sovereign",
    },
    "rootwarden_grips": {
        "name": "Rootwarden Grips",
        "slot": "gloves",
        "rarity": "mythic",
        "material": "artifact",
        "description": "Entangling root gloves from the Guardian.",
        "stats": {"defense": 16, "strength": 10, "constitution": 14},
        "craftable": False,
        "source": "boss_verdant_guardian",
    },
    # Craftable Mythic Gloves
    "gauntlets_of_creation": {
        "name": "Gauntlets of Creation",
        "slot": "gloves",
        "rarity": "mythic",
        "material": "artifact",
        "description": "Shape reality with your hands.",
        "stats": {"defense": 14, "strength": 12, "dexterity": 10, "perception": 8},
        "craftable": True,
        "source": "altar_crystal",
    },

    # ══════════════════════════════════════════════════════════════════
    # ACCESSORIES - All Tiers
    # ══════════════════════════════════════════════════════════════════
    "copper_ring": {
        "name": "Copper Ring",
        "slot": "accessory",
        "rarity": "common",
        "material": "copper",
        "description": "A simple copper band. Slightly lucky.",
        "stats": {"perception": 1},
        "craftable": True,
        "source": "forge",
    },
    "silver_ring": {
        "name": "Silver Ring",
        "slot": "accessory",
        "rarity": "uncommon",
        "material": "silver",
        "description": "A polished silver ring. Faintly magical.",
        "stats": {"charisma": 2},
        "craftable": True,
        "source": "forge",
    },
    "golden_ring": {
        "name": "Golden Ring",
        "slot": "accessory",
        "rarity": "uncommon",
        "material": "gold",
        "description": "A gleaming golden ring. Radiates authority.",
        "stats": {"charisma": 3},
        "craftable": True,
        "source": "forge",
    },
    "leather_belt": {
        "name": "Leather Belt",
        "slot": "accessory",
        "rarity": "uncommon",
        "material": "leather",
        "description": "A sturdy belt for holding gear.",
        "stats": {"constitution": 2, "strength": 1},
        "craftable": True,
        "source": "forge",
    },
    "golem_core_amulet": {
        "name": "Golem Core Amulet",
        "slot": "accessory",
        "rarity": "rare",
        "material": "crystal",
        "description": "An amulet containing a crystal golem's core.",
        "stats": {"defense": 3, "constitution": 3},
        "craftable": False,
        "source": "monster_crystal_golem",
    },
    "clockwork_ring": {
        "name": "Clockwork Ring",
        "slot": "accessory",
        "rarity": "rare",
        "material": "iron",
        "description": "A ring with tiny moving gears.",
        "stats": {"dexterity": 4, "perception": 2},
        "craftable": False,
        "source": "monster_gear_golem",
    },
    "trollhide_belt": {
        "name": "Trollhide Belt",
        "slot": "accessory",
        "rarity": "rare",
        "material": "leather",
        "description": "A belt made from troll hide. Regenerative properties.",
        "stats": {"constitution": 5, "strength": 2},
        "craftable": False,
        "source": "monster_moss_troll",
    },
    "wisp_lantern": {
        "name": "Wisp Lantern",
        "slot": "accessory",
        "rarity": "rare",
        "material": "crystal",
        "description": "A captured prism wisp. Lights the darkness.",
        "stats": {"perception": 4, "charisma": 2},
        "craftable": False,
        "source": "monster_prism_wisp",
    },
    "magic_amulet": {
        "name": "Magic Amulet",
        "slot": "accessory",
        "rarity": "rare",
        "material": "silver",
        "description": "Pulses with arcane energy. Sharpens the senses.",
        "stats": {"perception": 3, "constitution": 2},
        "craftable": True,
        "source": "forge",
    },
    "gold_amulet": {
        "name": "Gold Amulet",
        "slot": "accessory",
        "rarity": "rare",
        "material": "gold",
        "description": "A heavy gold amulet. Symbol of wealth.",
        "stats": {"charisma": 4, "constitution": 2},
        "craftable": True,
        "source": "forge",
    },
    "enchanted_cloak": {
        "name": "Enchanted Cloak",
        "slot": "accessory",
        "rarity": "rare",
        "material": "cloth",
        "description": "A cloak woven with protective enchantments.",
        "stats": {"defense": 3, "dexterity": 2, "perception": 2},
        "craftable": True,
        "source": "forge",
    },
    "enchanted_ring": {
        "name": "Enchanted Ring",
        "slot": "accessory",
        "rarity": "epic",
        "material": "crystal",
        "description": "Humming with crystalline energy.",
        "stats": {"perception": 4, "charisma": 3},
        "craftable": True,
        "source": "altar_crystal",
    },
    "void_amulet": {
        "name": "Void Amulet",
        "slot": "accessory",
        "rarity": "epic",
        "material": "void",
        "description": "Pulsing with void energy. Protects against shadow attacks.",
        "stats": {"defense": 5, "constitution": 4},
        "craftable": True,
        "source": "altar_shadow",
    },
    "matriarch_eye_amulet": {
        "name": "Matriarch's Eye Amulet",
        "slot": "accessory",
        "rarity": "epic",
        "material": "crystal",
        "description": "Contains the eye of the Crystal Matriarch.",
        "stats": {"perception": 6, "dexterity": 3},
        "craftable": False,
        "source": "miniboss_crystal_matriarch",
    },
    "overclock_gear_ring": {
        "name": "Overclock Gear Ring",
        "slot": "accessory",
        "rarity": "epic",
        "material": "iron",
        "description": "A ring that accelerates everything.",
        "stats": {"dexterity": 6, "strength": 4},
        "craftable": False,
        "source": "miniboss_iron_warden",
    },
    "lich_crown": {
        "name": "Lich Crown",
        "slot": "accessory",
        "rarity": "epic",
        "material": "soul",
        "description": "A crown of dark power, restored from its shattered form.",
        "stats": {"strength": 5, "perception": 5, "constitution": 4},
        "craftable": True,
        "source": "altar_catacomb",
    },
    "void_pendant": {
        "name": "Void Pendant",
        "slot": "accessory",
        "rarity": "legendary",
        "material": "void",
        "description": "A pendant containing a fragment of the void.",
        "stats": {"defense": 6, "perception": 6, "dexterity": 4},
        "craftable": True,
        "source": "rare_recipe_shadow",
    },
    "diamond_of_the_depths": {
        "name": "Diamond of the Depths",
        "slot": "accessory",
        "rarity": "legendary",
        "material": "crystal",
        "description": "A massive diamond from the deepest mines.",
        "stats": {"perception": 8, "charisma": 6, "defense": 4},
        "craftable": True,
        "source": "rare_recipe_crystal",
    },
    "frozen_heart_pendant": {
        "name": "Frozen Heart Pendant",
        "slot": "accessory",
        "rarity": "legendary",
        "material": "frost",
        "description": "A pendant containing a heart of eternal ice.",
        "stats": {"defense": 8, "constitution": 8},
        "craftable": True,
        "source": "rare_recipe_frost",
    },
    "seed_of_life": {
        "name": "Seed of Life",
        "slot": "accessory",
        "rarity": "legendary",
        "material": "nature",
        "description": "A seed from the Worldtree. Pulses with life energy.",
        "stats": {"constitution": 10, "perception": 6},
        "craftable": True,
        "source": "rare_recipe_verdant",
    },
    # Mythic Accessories
    "heart_of_the_titan": {
        "name": "Heart of the Titan",
        "slot": "accessory",
        "rarity": "mythic",
        "material": "artifact",
        "description": "The Crystal Titan's heart. Unbreakable will.",
        "stats": {"constitution": 20, "defense": 10, "perception": 6},
        "craftable": False,
        "source": "boss_crystal_titan",
    },
    "eternal_ember_core": {
        "name": "Eternal Ember Core",
        "slot": "accessory",
        "rarity": "mythic",
        "material": "artifact",
        "description": "The core that powered the Iron Forgemaster.",
        "stats": {"strength": 15, "constitution": 12, "defense": 6},
        "craftable": False,
        "source": "boss_iron_forgemaster",
    },
    "sovereigns_sigil": {
        "name": "Sovereign's Sigil",
        "slot": "accessory",
        "rarity": "mythic",
        "material": "artifact",
        "description": "The Shadow Sovereign's seal of power.",
        "stats": {"perception": 14, "dexterity": 12, "charisma": 8},
        "craftable": False,
        "source": "boss_shadow_sovereign",
    },
    "phylactery_shard": {
        "name": "Phylactery Shard",
        "slot": "accessory",
        "rarity": "mythic",
        "material": "artifact",
        "description": "A shard of the Lich King's phylactery. Defy death once.",
        "stats": {"constitution": 18, "perception": 10, "defense": 6},
        "craftable": False,
        "source": "boss_lich_king",
    },
    "frozen_heart_mythic": {
        "name": "Frozen Heart",
        "slot": "accessory",
        "rarity": "mythic",
        "material": "artifact",
        "description": "The Frost Sovereign's heart of absolute zero.",
        "stats": {"constitution": 16, "defense": 14, "perception": 6},
        "craftable": False,
        "source": "boss_frost_sovereign",
    },
    "heart_of_the_forest": {
        "name": "Heart of the Forest",
        "slot": "accessory",
        "rarity": "mythic",
        "material": "artifact",
        "description": "The Verdant Guardian's life force. Full heal once.",
        "stats": {"constitution": 22, "perception": 8, "charisma": 6},
        "craftable": False,
        "source": "boss_verdant_guardian",
    },
    # Craftable Mythic Accessory
    "frostfire_ring": {
        "name": "Frostfire Ring",
        "slot": "accessory",
        "rarity": "mythic",
        "material": "artifact",
        "description": "Forged from eternal frost and flame. Paradox made real.",
        "stats": {"defense": 10, "strength": 10, "constitution": 10, "dexterity": 8},
        "craftable": True,
        "source": "altar_iron",
    },
    "mana_chalice": {
        "name": "Mana Chalice",
        "slot": "accessory",
        "rarity": "rare",
        "material": "crystal",
        "description": "An ornate chalice imbued with arcane magic. Slowly replenishes your mana.",
        "stats": {"mana_regen_bonus": 0.05},
        "craftable": False,
        "source": "shop",
    },

    # ══════════════════════════════════════════════════════════════════
    # REGION-THEMED EQUIPMENT
    # ══════════════════════════════════════════════════════════════════
    # Forest/Elderwood Region
    "elderwood_staff": {
        "name": "Elderwood Staff",
        "slot": "weapon",
        "rarity": "uncommon",
        "material": "wood",
        "description": "A staff carved from ancient elderwood.",
        "stats": {"strength": 3, "perception": 2, "constitution": 1},
        "craftable": False,
        "source": "region_forest",
    },
    "rangers_hood": {
        "name": "Ranger's Hood",
        "slot": "helm",
        "rarity": "uncommon",
        "material": "leather",
        "description": "A hood favored by forest rangers.",
        "stats": {"defense": 2, "perception": 2, "dexterity": 1},
        "craftable": False,
        "source": "region_forest",
    },
    "wolf_pelt_cloak": {
        "name": "Wolf Pelt Cloak",
        "slot": "accessory",
        "rarity": "uncommon",
        "material": "leather",
        "description": "A cloak made from wolf pelts.",
        "stats": {"defense": 2, "constitution": 2},
        "craftable": False,
        "source": "region_forest",
    },
    "boar_tusk_helm": {
        "name": "Boar Tusk Helm",
        "slot": "helm",
        "rarity": "rare",
        "material": "leather",
        "description": "A helm adorned with boar tusks.",
        "stats": {"defense": 4, "strength": 2, "constitution": 1},
        "craftable": False,
        "source": "region_forest",
    },
    # Mountain/Stormspire Region
    "mountain_goat_boots": {
        "name": "Mountain Goat Boots",
        "slot": "boots",
        "rarity": "uncommon",
        "material": "leather",
        "description": "Boots with incredible grip for climbing.",
        "stats": {"defense": 2, "dexterity": 3},
        "craftable": False,
        "source": "region_mountain",
    },
    "rock_elemental_shield": {
        "name": "Rock Elemental Shield",
        "slot": "shield",
        "rarity": "rare",
        "material": "iron",
        "description": "A shield made from rock elemental remains.",
        "stats": {"defense": 8, "constitution": 2},
        "craftable": False,
        "source": "region_mountain",
    },
    "highland_blade": {
        "name": "Highland Brigand's Blade",
        "slot": "weapon",
        "rarity": "rare",
        "material": "steel",
        "description": "A blade used by mountain brigands.",
        "stats": {"strength": 6, "dexterity": 2},
        "craftable": False,
        "source": "region_mountain",
    },
    # Swamp Region
    "bog_leather_armor": {
        "name": "Bog Leather Armor",
        "slot": "armor",
        "rarity": "uncommon",
        "material": "leather",
        "description": "Waterlogged leather armor. Smells terrible.",
        "stats": {"defense": 4, "constitution": 1},
        "craftable": False,
        "source": "region_swamp",
    },
    "hags_hex_ring": {
        "name": "Hag's Hex Ring",
        "slot": "accessory",
        "rarity": "rare",
        "material": "iron",
        "description": "A cursed ring from a marsh hag.",
        "stats": {"perception": 4, "constitution": 2},
        "craftable": False,
        "source": "region_swamp",
    },
    "viper_fang_dagger": {
        "name": "Viper Fang Dagger",
        "slot": "weapon",
        "rarity": "rare",
        "material": "iron",
        "description": "A dagger tipped with a viper's fang. Venomous.",
        "stats": {"strength": 4, "dexterity": 3},
        "craftable": False,
        "source": "region_swamp",
    },
    # Desert Region
    "scorpion_carapace_armor": {
        "name": "Scorpion Carapace Armor",
        "slot": "armor",
        "rarity": "rare",
        "material": "leather",
        "description": "Armor made from giant scorpion shell.",
        "stats": {"defense": 7, "constitution": 2},
        "craftable": False,
        "source": "region_desert",
    },
    "sand_viper_hood": {
        "name": "Sand Viper Hood",
        "slot": "helm",
        "rarity": "rare",
        "material": "leather",
        "description": "A hood that protects from sandstorms.",
        "stats": {"defense": 4, "perception": 3},
        "craftable": False,
        "source": "region_desert",
    },
    "mirage_cloak": {
        "name": "Mirage Cloak",
        "slot": "accessory",
        "rarity": "epic",
        "material": "cloth",
        "description": "A cloak that shimmers like a desert mirage.",
        "stats": {"dexterity": 5, "perception": 4, "charisma": 2},
        "craftable": False,
        "source": "region_desert",
    },
    # Tundra Region
    "frost_wolf_pelt": {
        "name": "Frost Wolf Pelt Armor",
        "slot": "armor",
        "rarity": "rare",
        "material": "leather",
        "description": "Armor lined with frost wolf fur. Warm.",
        "stats": {"defense": 6, "constitution": 3},
        "craftable": False,
        "source": "region_tundra",
    },
    "ice_wraith_robes": {
        "name": "Ice Wraith Robes",
        "slot": "armor",
        "rarity": "epic",
        "material": "frost",
        "description": "Robes woven from an ice wraith's essence.",
        "stats": {"defense": 8, "perception": 4, "dexterity": 3},
        "craftable": False,
        "source": "region_tundra",
    },
    "polar_bear_gauntlets": {
        "name": "Polar Bear Gauntlets",
        "slot": "gloves",
        "rarity": "rare",
        "material": "leather",
        "description": "Massive gauntlets lined with polar bear fur.",
        "stats": {"defense": 5, "strength": 4},
        "craftable": False,
        "source": "region_tundra",
    },
    # Coast Region
    "crab_shell_shield": {
        "name": "Crab Shell Shield",
        "slot": "shield",
        "rarity": "rare",
        "material": "iron",
        "description": "A shield crafted from giant crab shell.",
        "stats": {"defense": 7, "constitution": 1},
        "craftable": False,
        "source": "region_coast",
    },
    "serpent_scale_armor": {
        "name": "Sea Serpent Scale Armor",
        "slot": "armor",
        "rarity": "epic",
        "material": "dragonscale",
        "description": "Armor made from sea serpent scales.",
        "stats": {"defense": 12, "dexterity": 3},
        "craftable": False,
        "source": "region_coast",
    },
    "pirates_cutlass": {
        "name": "Pirate's Cutlass",
        "slot": "weapon",
        "rarity": "rare",
        "material": "steel",
        "description": "A curved blade favored by coastal raiders.",
        "stats": {"strength": 6, "dexterity": 3},
        "craftable": False,
        "source": "region_coast",
    },
    "drowned_sailors_ring": {
        "name": "Drowned Sailor's Ring",
        "slot": "accessory",
        "rarity": "rare",
        "material": "silver",
        "description": "A ring from a drowned sailor. Curiously dry.",
        "stats": {"constitution": 3, "perception": 3},
        "craftable": False,
        "source": "region_coast",
    },

    # ══════════════════════════════════════════════════════════════════
    # DUNGEON SET PIECES (Craftable at Altars)
    # ══════════════════════════════════════════════════════════════════
    # Crystal Caverns - Prismatic Set
    "prismatic_helm": {
        "name": "Prismatic Helm",
        "slot": "helm",
        "rarity": "legendary",
        "material": "crystal",
        "description": "A helm that refracts light into blinding rainbows.",
        "stats": {"defense": 12, "perception": 8},
        "craftable": True,
        "source": "altar_crystal",
    },
    "prismatic_armor": {
        "name": "Prismatic Armor",
        "slot": "armor",
        "rarity": "legendary",
        "material": "crystal",
        "description": "Crystal armor that splits incoming damage into harmless light.",
        "stats": {"defense": 18, "perception": 6},
        "craftable": True,
        "source": "altar_crystal",
    },
    "prismatic_gauntlets": {
        "name": "Prismatic Gauntlets",
        "slot": "gloves",
        "rarity": "legendary",
        "material": "crystal",
        "description": "Gloves of living light crystal.",
        "stats": {"defense": 8, "strength": 6, "perception": 4},
        "craftable": True,
        "source": "altar_crystal",
    },
    "prismatic_boots": {
        "name": "Prismatic Boots",
        "slot": "boots",
        "rarity": "legendary",
        "material": "crystal",
        "description": "Boots that leave trails of colored light.",
        "stats": {"defense": 8, "dexterity": 6, "perception": 4},
        "craftable": True,
        "source": "altar_crystal",
    },
    # Iron Halls - Forgeborn Set
    "forgeborn_helm": {
        "name": "Forgeborn Helm",
        "slot": "helm",
        "rarity": "legendary",
        "material": "mithril",
        "description": "A helm forged on the Dwarven Eternal Anvil.",
        "stats": {"defense": 14, "constitution": 6},
        "craftable": True,
        "source": "altar_iron",
    },
    "forgeborn_plate": {
        "name": "Forgeborn Plate",
        "slot": "armor",
        "rarity": "legendary",
        "material": "mithril",
        "description": "The pinnacle of dwarven smithing.",
        "stats": {"defense": 22, "constitution": 8},
        "craftable": True,
        "source": "altar_iron",
    },
    "forgeborn_gauntlets": {
        "name": "Forgeborn Gauntlets",
        "slot": "gloves",
        "rarity": "legendary",
        "material": "mithril",
        "description": "Gauntlets that never dull or break.",
        "stats": {"defense": 10, "strength": 8, "constitution": 4},
        "craftable": True,
        "source": "altar_iron",
    },
    "forgeborn_greaves": {
        "name": "Forgeborn Greaves",
        "slot": "boots",
        "rarity": "legendary",
        "material": "mithril",
        "description": "Boots forged to last eternities.",
        "stats": {"defense": 12, "constitution": 6, "strength": 4},
        "craftable": True,
        "source": "altar_iron",
    },
    # Shadow Depths - Voidwalker Set
    "voidwalker_hood": {
        "name": "Voidwalker Hood",
        "slot": "helm",
        "rarity": "legendary",
        "material": "void",
        "description": "A hood that peers into the void.",
        "stats": {"defense": 10, "perception": 8, "dexterity": 4},
        "craftable": True,
        "source": "altar_shadow",
    },
    "voidwalker_cloak": {
        "name": "Voidwalker Cloak",
        "slot": "armor",
        "rarity": "legendary",
        "material": "void",
        "description": "A cloak woven from shadows and void essence.",
        "stats": {"defense": 14, "dexterity": 8, "perception": 6},
        "craftable": True,
        "source": "altar_shadow",
    },
    "voidwalker_gloves": {
        "name": "Voidwalker Gloves",
        "slot": "gloves",
        "rarity": "legendary",
        "material": "void",
        "description": "Gloves that reach between dimensions.",
        "stats": {"defense": 6, "dexterity": 8, "perception": 6},
        "craftable": True,
        "source": "altar_shadow",
    },
    "voidwalker_boots": {
        "name": "Voidwalker Boots",
        "slot": "boots",
        "rarity": "legendary",
        "material": "void",
        "description": "Boots for walking the boundary between worlds.",
        "stats": {"defense": 8, "dexterity": 10, "perception": 4},
        "craftable": True,
        "source": "altar_shadow",
    },
    # Sunken Catacombs - Soulbinder Set
    "soulbinder_crown": {
        "name": "Soulbinder Crown",
        "slot": "helm",
        "rarity": "legendary",
        "material": "soul",
        "description": "A crown that binds spirits to your will.",
        "stats": {"defense": 10, "perception": 8, "constitution": 6},
        "craftable": True,
        "source": "altar_catacomb",
    },
    "soulbinder_robes": {
        "name": "Soulbinder Robes",
        "slot": "armor",
        "rarity": "legendary",
        "material": "soul",
        "description": "Robes woven from spiritual energy.",
        "stats": {"defense": 14, "perception": 6, "constitution": 8},
        "craftable": True,
        "source": "altar_catacomb",
    },
    "soulbinder_gauntlets": {
        "name": "Soulbinder Gauntlets",
        "slot": "gloves",
        "rarity": "legendary",
        "material": "soul",
        "description": "Gauntlets that grip souls.",
        "stats": {"defense": 8, "strength": 6, "constitution": 6},
        "craftable": True,
        "source": "altar_catacomb",
    },
    "soulbinder_greaves": {
        "name": "Soulbinder Greaves",
        "slot": "boots",
        "rarity": "legendary",
        "material": "soul",
        "description": "Boots that walk among the dead.",
        "stats": {"defense": 8, "dexterity": 4, "constitution": 8},
        "craftable": True,
        "source": "altar_catacomb",
    },

    # ══════════════════════════════════════════════════════════════════
    # MYTHIC TIER — Hidden Rooms, Easter Eggs & Secret Boss Rewards
    # ══════════════════════════════════════════════════════════════════

    # ── Mythic Weapons ────────────────────────────────────────────────
    "solaris_blade": {
        "name": "Solaris Blade",
        "slot": "weapon",
        "rarity": "mythic",
        "material": "starforged",
        "description": "A legendary sword forged from a fallen star. Its edge never dulls, and it radiates warm golden light that burns the undead.",
        "lore": "Carried by the first Champion of the Light, then lost in the Underground Archive for five hundred years.",
        "stats": {"strength": 25, "dexterity": 10, "constitution": 5},
        "craftable": False,
        "source": "underground_archive",
    },
    "forgotten_blade": {
        "name": "Blade of the Forgotten",
        "slot": "weapon",
        "rarity": "mythic",
        "material": "void",
        "description": "A sword that exists between dimensions. Strikes always find the weakest point, bypassing half of all armour.",
        "lore": "Left on the altar of the Forgotten Shrine by the Unnamed Hero, whose name was erased from all records.",
        "stats": {"strength": 22, "dexterity": 15},
        "craftable": False,
        "source": "forgotten_shrine_puzzle",
    },
    "dragonfang_dagger": {
        "name": "Dragonfang Dagger",
        "slot": "weapon",
        "rarity": "mythic",
        "material": "dragonbone",
        "description": "A dagger carved from a true dragonbone fang. Poisons targets with dragonfire essence on each hit.",
        "lore": "Recovered from the body of the Void Titan after the legendary secret battle.",
        "stats": {"strength": 18, "dexterity": 20},
        "craftable": False,
        "source": "secret_boss_drop",
    },
    "pirate_captain_sword": {
        "name": "Dread Captain's Cutlass",
        "slot": "weapon",
        "rarity": "mythic",
        "material": "bloodiron",
        "description": "The cutlass of a legendary pirate captain. Still drips with salt water and reeks of gunpowder.",
        "lore": "Found in the Pirate Vault, locked in a glass case for two hundred years.",
        "stats": {"strength": 20, "dexterity": 12, "constitution": 5},
        "craftable": False,
        "source": "pirate_vault",
    },
    "devs_blade": {
        "name": "The Developer's Blade",
        "slot": "weapon",
        "rarity": "mythic",
        "material": "codeforged",
        "description": "A perfectly balanced sword with 'git push -f' etched on the blade. Does precisely 9,001 damage, but only in the changelog.",
        "lore": "Created by the developers who shape this world. Left as a gift for those curious enough to find the hidden workshop.",
        "stats": {"strength": 30, "dexterity": 30, "constitution": 10},
        "craftable": False,
        "source": "developers_corner",
    },

    # ── Mythic Armour ─────────────────────────────────────────────────
    "dragonscale_armor": {
        "name": "Dragonscale Armour",
        "slot": "armor",
        "rarity": "mythic",
        "material": "dragonscale",
        "description": "Armour crafted from the scales of an elder dragon. Each scale shimmers between black and deep crimson. Virtually impenetrable.",
        "lore": "Crafted in the Hidden Alchemy Lab from scales traded by a mysterious cloaked figure.",
        "stats": {"defense": 35, "constitution": 15, "strength": 5},
        "craftable": False,
        "source": "hidden_alchemy_lab",
    },
    "archive_robe": {
        "name": "Archivist's Robe",
        "slot": "armor",
        "rarity": "mythic",
        "material": "spellwoven",
        "description": "Robes worn by the ancient archivist who catalogued every secret of the realm. Every stitch contains a preserved spell.",
        "lore": "Preserved in the Underground Archive for centuries, waiting for someone literate enough to deserve them.",
        "stats": {"defense": 15, "constitution": 20, "dexterity": 10},
        "craftable": False,
        "source": "underground_archive",
    },
    "void_cloak": {
        "name": "Void Cloak",
        "slot": "armor",
        "rarity": "mythic",
        "material": "void",
        "description": "A cloak that absorbs all light around it. Grants resistance to void magic and the ability to slip through shadows.",
        "lore": "Discovered in the Void Sanctuary, discarded by a being that no longer needed a physical form.",
        "stats": {"defense": 20, "dexterity": 25, "constitution": 10},
        "craftable": False,
        "source": "void_sanctuary",
    },

    # ── Mythic Helms ──────────────────────────────────────────────────
    "crown_of_stars": {
        "name": "Crown of Stars",
        "slot": "helm",
        "rarity": "mythic",
        "material": "starforged",
        "description": "A crown set with seven gemstones, each containing a trapped star. When worn, the stars whisper secrets of the cosmos.",
        "lore": "Hidden atop the Clocktower Interior for a thousand years, waiting for someone worthy to climb high enough.",
        "stats": {"defense": 12, "constitution": 15, "strength": 8, "dexterity": 8},
        "craftable": False,
        "source": "clocktower_interior",
    },
    "void_titan_crown": {
        "name": "Void Titan's Diadem",
        "slot": "helm",
        "rarity": "mythic",
        "material": "void",
        "description": "The crown worn by the Void Titan. Still radiates incomprehensible power. Wearing it makes reality feel slightly thin.",
        "lore": "Torn from the Void Titan's brow after the legendary secret ritual battle.",
        "stats": {"defense": 20, "strength": 15, "constitution": 20},
        "craftable": False,
        "source": "secret_boss_drop",
    },

    # ── Mythic Accessories ────────────────────────────────────────────
    "ethereal_orb": {
        "name": "Ethereal Orb",
        "slot": "accessory",
        "rarity": "mythic",
        "material": "ether",
        "description": "A sphere of pure crystallised magic. Pulses with inner light and amplifies all spells and abilities.",
        "lore": "The centrepiece of the Forgotten Shrine's altar. Placed there by a mage who transcended mortality.",
        "stats": {"constitution": 20, "dexterity": 15, "strength": 5},
        "craftable": False,
        "source": "forgotten_shrine_puzzle",
    },
    "clockwork_pendant": {
        "name": "Clockwork Pendant",
        "slot": "accessory",
        "rarity": "mythic",
        "material": "clockwork",
        "description": "A small mechanical pendant that ticks perfectly. Legend says the wearer always arrives exactly at the right time.",
        "lore": "Crafted by the master clockmaker who built the tower. Still keeping perfect time centuries later.",
        "stats": {"dexterity": 20, "constitution": 10},
        "craftable": False,
        "source": "clocktower_interior",
    },
    "starweave_ring": {
        "name": "Starweave Ring",
        "slot": "accessory",
        "rarity": "mythic",
        "material": "starforged",
        "description": "A ring woven from light itself. The setting shifts colour with the wearer's emotions.",
        "lore": "Found in the Void Sanctuary, left by someone who no longer had fingers — or a body.",
        "stats": {"strength": 10, "dexterity": 10, "constitution": 10, "defense": 10},
        "craftable": False,
        "source": "void_sanctuary",
    },

    # ── Mythic Boots ──────────────────────────────────────────────────
    "clockwork_boots": {
        "name": "Clockwork Boots",
        "slot": "boots",
        "rarity": "mythic",
        "material": "clockwork",
        "description": "Mechanical boots that measure and optimise your every step.",
        "lore": "Built into the Clocktower Interior floor, welded to the platform until someone found the release mechanism.",
        "stats": {"dexterity": 20, "defense": 10, "constitution": 5},
        "craftable": False,
        "source": "clocktower_interior",
    },

    # ── Mythic Gloves ─────────────────────────────────────────────────
    "voidborn_gauntlets": {
        "name": "Voidborn Gauntlets",
        "slot": "gloves",
        "rarity": "mythic",
        "material": "void",
        "description": "Gauntlets that crackle with contained void energy. Each punch tears a small hole in the fabric of the target.",
        "lore": "Forged in the heart of the Void Sanctuary, where the walls between worlds are paper-thin.",
        "stats": {"defense": 12, "strength": 18, "constitution": 8},
        "craftable": False,
        "source": "void_sanctuary",
    },
}

# ═════════════════════════════════════════════════════════════════════
# SLOT CONFIGURATION
# ═════════════════════════════════════════════════════════════════════

# Slot display names and icons
SLOT_INFO = {
    "weapon":    {"name": "Weapon",    "icon": "⚔️"},
    "armor":     {"name": "Armor",     "icon": "🛡️"},
    "shield":    {"name": "Shield",    "icon": "🔰"},
    "helm":      {"name": "Helm",      "icon": "⛑️"},
    "boots":     {"name": "Boots",     "icon": "🥾"},
    "gloves":    {"name": "Gloves",    "icon": "🧤"},
    "accessory": {"name": "Accessory", "icon": "💍"},
}

EQUIPMENT_SLOTS = ["weapon", "armor", "shield", "helm", "boots", "gloves", "accessory"]


# ═════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═════════════════════════════════════════════════════════════════════

def get_rarity_display(item_id):
    """Get the display string for an item's rarity."""
    item = EQUIPMENT_DATABASE.get(item_id)
    if not item:
        return ""
    rarity = item.get("rarity", "common")
    rarity_info = RARITY_TIERS.get(rarity, RARITY_TIERS["common"])
    return f"{rarity_info['icon']} {rarity_info['name']}"


def get_item_with_rarity_name(item_id):
    """Get item name with rarity indicator prefix."""
    item = EQUIPMENT_DATABASE.get(item_id)
    if not item:
        return item_id.replace("_", " ").title()
    rarity = item.get("rarity", "common")
    rarity_info = RARITY_TIERS.get(rarity, RARITY_TIERS["common"])
    return f"{rarity_info['icon']} {item['name']}"


def get_items_by_rarity(rarity):
    """Get all items of a specific rarity tier."""
    return {k: v for k, v in EQUIPMENT_DATABASE.items() if v.get("rarity") == rarity}


def get_items_by_slot(slot):
    """Get all items that go in a specific equipment slot."""
    return {k: v for k, v in EQUIPMENT_DATABASE.items() if v.get("slot") == slot}


def get_craftable_items():
    """Get all items that can be crafted."""
    return {k: v for k, v in EQUIPMENT_DATABASE.items() if v.get("craftable", True)}


def get_boss_drops():
    """Get all items that drop from bosses."""
    return {k: v for k, v in EQUIPMENT_DATABASE.items() 
            if v.get("source", "").startswith("boss_")}


def get_miniboss_drops():
    """Get all items that drop from mini-bosses."""
    return {k: v for k, v in EQUIPMENT_DATABASE.items() 
            if v.get("source", "").startswith("miniboss_")}


def get_monster_drops():
    """Get all items that drop from regular monsters."""
    return {k: v for k, v in EQUIPMENT_DATABASE.items() 
            if v.get("source", "").startswith("monster_")}


# ═════════════════════════════════════════════════════════════════════
# EQUIPMENT FUNCTIONS
# ═════════════════════════════════════════════════════════════════════

def is_equippable(item_id):
    """Check if an item can be equipped."""
    return item_id in EQUIPMENT_DATABASE


def get_equipment_info(item_id):
    """Get full equipment data for an item, or None."""
    return EQUIPMENT_DATABASE.get(item_id)


def get_equipment(player):
    """Get the player's current equipment dict. Creates it if missing."""
    if "equipment" not in player.state:
        player.state["equipment"] = {s: None for s in EQUIPMENT_SLOTS}
    else:
        # Ensure all slots exist (for save migration)
        for s in EQUIPMENT_SLOTS:
            if s not in player.state["equipment"]:
                player.state["equipment"][s] = None
    return player.state["equipment"]


def get_equipped_item(player, slot):
    """Get the item ID equipped in a given slot, or None."""
    equip = get_equipment(player)
    return equip.get(slot)


def equip_item(player, item_name):
    """
    Equip an item from the player's inventory.

    Returns:
        (success: bool, message: str)
    """
    # Normalize item name
    item_id = item_name.lower().replace(" ", "_")

    # Check if item exists in equipment database
    eq_data = EQUIPMENT_DATABASE.get(item_id)
    if not eq_data:
        return False, f"'{item_name.replace('_', ' ')}' cannot be equipped."

    # Check if player has the item in inventory
    inv = player.inventory
    if inv.get(item_id, 0) <= 0:
        return False, f"You don't have a {eq_data['name']} to equip."

    slot = eq_data["slot"]
    slot_info = SLOT_INFO[slot]
    equip = get_equipment(player)

    # If something is already in this slot, unequip it first
    unequip_msg = ""
    old_item = equip.get(slot)
    if old_item:
        old_data = EQUIPMENT_DATABASE.get(old_item, {})
        old_name = old_data.get("name", old_item.replace("_", " "))
        # Return old item to inventory
        inv[old_item] = inv.get(old_item, 0) + 1
        # Remove stat bonuses from old item
        for stat, val in old_data.get("stats", {}).items():
            player.stats[stat] = player.stats.get(stat, 0) - val
        unequip_msg = f"  Unequipped: {old_name}\n"

    # Remove new item from inventory
    inv[item_id] = inv.get(item_id, 0) - 1
    if inv[item_id] <= 0:
        del inv[item_id]

    # Place in equipment slot
    equip[slot] = item_id

    # Apply stat bonuses
    for stat, val in eq_data.get("stats", {}).items():
        player.stats[stat] = player.stats.get(stat, 0) + val

    # Build result message
    result = "\n" + "=" * 50 + "\n"
    result += f"  {slot_info['icon']} EQUIPPED: {eq_data['name']}\n"
    result += "=" * 50 + "\n"
    if unequip_msg:
        result += unequip_msg
    result += f"  Slot: {slot_info['name']}\n"
    result += f"  {eq_data['description']}\n"
    if eq_data.get("stats"):
        result += "\n  Stat bonuses:\n"
        for stat, val in eq_data["stats"].items():
            nice = stat.replace("_", " ").capitalize()
            result += f"    {nice}: +{val}\n"
    result += "=" * 50 + "\n"
    return True, result


def unequip_item(player, slot_or_name):
    """
    Unequip an item by slot name or item name.

    Returns:
        (success: bool, message: str)
    """
    equip = get_equipment(player)
    slot_or_name = slot_or_name.lower().replace(" ", "_")

    # Try to match by slot first
    if slot_or_name in EQUIPMENT_SLOTS:
        slot = slot_or_name
    else:
        # Try to find by item name
        slot = None
        for s, item_id in equip.items():
            if item_id and (item_id == slot_or_name or
                            item_id.replace("_", " ") == slot_or_name.replace("_", " ")):
                slot = s
                break
        # Also check by display name
        if not slot:
            for s, item_id in equip.items():
                if item_id:
                    eq_data = EQUIPMENT_DATABASE.get(item_id, {})
                    if eq_data.get("name", "").lower().replace(" ", "_") == slot_or_name:
                        slot = s
                        break

    if not slot:
        return False, f"Nothing matching '{slot_or_name.replace('_', ' ')}' is equipped."

    item_id = equip.get(slot)
    if not item_id:
        slot_name = SLOT_INFO.get(slot, {}).get("name", slot)
        return False, f"Nothing is equipped in the {slot_name} slot."

    eq_data = EQUIPMENT_DATABASE.get(item_id, {})
    item_name = eq_data.get("name", item_id.replace("_", " "))
    slot_info = SLOT_INFO[slot]

    # Remove stat bonuses
    for stat, val in eq_data.get("stats", {}).items():
        player.stats[stat] = player.stats.get(stat, 0) - val

    # Return to inventory
    player.inventory[item_id] = player.inventory.get(item_id, 0) + 1

    # Clear slot
    equip[slot] = None

    result = "\n" + "=" * 50 + "\n"
    result += f"  {slot_info['icon']} UNEQUIPPED: {item_name}\n"
    result += "=" * 50 + "\n"
    result += f"  {item_name} returned to inventory.\n"
    if eq_data.get("stats"):
        result += "\n  Removed stat bonuses:\n"
        for stat, val in eq_data["stats"].items():
            nice = stat.replace("_", " ").capitalize()
            result += f"    {nice}: -{val}\n"
    result += "=" * 50 + "\n"
    return True, result


def get_equipment_display(player):
    """
    Get a formatted text display of all equipment slots.

    Returns:
        str: formatted equipment overview
    """
    equip = get_equipment(player)

    result = "\n" + "=" * 50 + "\n"
    result += "  EQUIPMENT\n"
    result += "=" * 50 + "\n"

    for slot in EQUIPMENT_SLOTS:
        info = SLOT_INFO[slot]
        item_id = equip.get(slot)
        if item_id:
            eq_data = EQUIPMENT_DATABASE.get(item_id, {})
            item_name = eq_data.get("name", item_id.replace("_", " "))
            stat_parts = []
            for stat, val in eq_data.get("stats", {}).items():
                nice = stat.replace("_", " ").capitalize()
                stat_parts.append(f"+{val} {nice}")
            stat_str = ", ".join(stat_parts) if stat_parts else ""
            result += f"  {info['icon']} {info['name']:10s} {item_name}"
            if stat_str:
                result += f"  ({stat_str})"
            result += "\n"
        else:
            result += f"  {info['icon']} {info['name']:10s} (empty)\n"

    # Show total equipment bonuses
    totals = get_total_equipment_bonuses(player)
    if any(v != 0 for v in totals.values()):
        result += "\n  --- Total Equipment Bonuses ---\n"
        for stat, val in sorted(totals.items()):
            if val != 0:
                nice = stat.replace("_", " ").capitalize()
                result += f"    {nice}: +{val}\n"

    result += "=" * 50 + "\n"
    return result


def get_total_equipment_bonuses(player):
    """Calculate the total stat bonuses from all equipped items."""
    equip = get_equipment(player)
    totals = {}
    for slot in EQUIPMENT_SLOTS:
        item_id = equip.get(slot)
        if item_id:
            eq_data = EQUIPMENT_DATABASE.get(item_id, {})
            for stat, val in eq_data.get("stats", {}).items():
                totals[stat] = totals.get(stat, 0) + val
    return totals


def get_attack_power(player):
    """
    Calculate the player's total attack power for combat.
    Base: strength stat + weapon bonus.
    """
    strength = player.stats.get("strength", 0)
    # Weapon bonus is already applied to strength via equip_item,
    # but we also add a flat base so unarmed isn't 0
    base_attack = max(1, strength)
    return base_attack


def get_defense_power(player):
    """
    Calculate the player's total defense for combat.
    Defense stat already includes equipment bonuses.
    """
    return player.stats.get("defense", 0)
