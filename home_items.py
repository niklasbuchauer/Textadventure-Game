"""
Home item database for the pocket-dimension player home.
Data-only module so gameplay systems can remain logic-focused.
"""

HOME_ITEMS = {
    # Functional utilities
    "home_workbench": {
        "name": "Home Workbench",
        "category": "functional",
        "description": "A sturdy workbench for crafting at home.",
        "source": "elara_shop",
        "price": 200,
        "map_icon": "W",
        "map_color": "#9c6b3a",
        "use_action": "craft",
        "allowed_rooms": ["workshop"],
    },
    "home_alchemy_table": {
        "name": "Home Alchemy Table",
        "category": "functional",
        "description": "Glassware and reagents for brewing potions.",
        "source": "elara_shop",
        "price": 250,
        "map_icon": "A",
        "map_color": "#6b8f4e",
        "use_action": "alchemy",
        "allowed_rooms": ["workshop"],
    },
    "home_forge": {
        "name": "Home Forge",
        "category": "functional",
        "description": "A compact forge for weapon and armor work.",
        "source": "elara_shop",
        "price": 350,
        "map_icon": "F",
        "map_color": "#7f5a3c",
        "use_action": "forge",
        "allowed_rooms": ["workshop"],
    },
    "home_enchanting_table": {
        "name": "Home Enchanting Table",
        "category": "functional",
        "description": "An etched table used for enchantment rituals.",
        "source": "elara_shop",
        "price": 300,
        "map_icon": "E",
        "map_color": "#4f6ca8",
        "use_action": "enchant",
        "allowed_rooms": ["workshop"],
    },
    "home_smelting_furnace": {
        "name": "Home Smelting Furnace",
        "category": "functional",
        "description": "A furnace for refining ores into bars.",
        "source": "elara_shop",
        "price": 200,
        "map_icon": "S",
        "map_color": "#915a36",
        "use_action": "smelt",
        "allowed_rooms": ["workshop"],
    },
    "personal_chest": {
        "name": "Personal Chest",
        "category": "functional",
        "description": "A 20-slot chest linked to your home storage.",
        "source": "elara_shop",
        "price": 150,
        "map_icon": "C",
        "map_color": "#8a6234",
        "use_action": "chest",
        "capacity": 20,
    },
    "cozy_bed": {
        "name": "Cozy Bed",
        "category": "functional",
        "description": "A bed that lets you fully rest at home.",
        "source": "elara_shop",
        "price": 100,
        "map_icon": "B",
        "map_color": "#8b6b93",
        "use_action": "rest",
        "allowed_rooms": ["bedroom"],
    },
    "trophy_mount": {
        "name": "Trophy Mount",
        "category": "functional",
        "description": "A wall mount to display boss trophies.",
        "source": "boss_blueprint",
        "map_icon": "T",
        "map_color": "#7b4a2a",
        "wall_only": True,
        "allowed_rooms": ["trophy"],
    },
    "bookshelf": {
        "name": "Bookshelf",
        "category": "functional",
        "description": "Stores and displays your collected tomes.",
        "source": "elara_shop",
        "price": 75,
        "map_icon": "K",
        "map_color": "#6c5136",
        "use_action": "bookshelf",
    },
    "caldron": {
        "name": "Caldron",
        "category": "functional",
        "description": "A ritual cauldron for special concoctions.",
        "source": "swamp_witch_quest",
        "map_icon": "R",
        "map_color": "#4a6b52",
        "use_action": "ritual",
        "allowed_rooms": ["workshop"],
    },

    # Altars
    "altar_of_strength": {
        "name": "Altar of Strength",
        "category": "altar",
        "description": "Gain +3 attack for one run.",
        "source": "crafting",
        "map_icon": "1",
        "map_color": "#b34b3d",
        "altar_bonus": {"attack": 3},
    },
    "altar_of_warding": {
        "name": "Altar of Warding",
        "category": "altar",
        "description": "Gain +3 defense for one run.",
        "source": "crafting",
        "map_icon": "2",
        "map_color": "#3d5fb3",
        "altar_bonus": {"defense": 3},
    },
    "altar_of_fortune": {
        "name": "Altar of Fortune",
        "category": "altar",
        "description": "Gain +15 percent gold from enemies for one run.",
        "source": "treasure_golem_drop",
        "map_icon": "3",
        "map_color": "#b3993d",
        "altar_bonus": {"gold_multiplier": 0.15},
    },
    "altar_of_knowledge": {
        "name": "Altar of Knowledge",
        "category": "altar",
        "description": "Gain +25 percent XP for one run.",
        "source": "hermit_quest",
        "map_icon": "4",
        "map_color": "#5a6bb0",
        "altar_bonus": {"xp_multiplier": 0.25},
    },
    "altar_of_souls": {
        "name": "Altar of Souls",
        "category": "altar",
        "description": "Revive once with 50 percent HP for one run.",
        "source": "catacombs_boss_drop",
        "map_icon": "5",
        "map_color": "#6b4f8f",
        "altar_bonus": {"revive_once": 0.5},
    },
    "altar_of_shadows": {
        "name": "Altar of Shadows",
        "category": "altar",
        "description": "Gain +10 percent crit chance for one run.",
        "source": "shadow_reputation_reward",
        "map_icon": "6",
        "map_color": "#4d4d66",
        "altar_bonus": {"crit_chance": 0.10},
    },
    "grand_altar": {
        "name": "Grand Altar",
        "category": "altar",
        "description": "Choose any one altar effect for a run.",
        "source": "elara_shop",
        "price": 1500,
        "map_icon": "G",
        "map_color": "#8b6f2f",
        "altar_bonus": {"choose_any": True},
    },

    # Decorations
    "wolf_pelt_rug": {
        "name": "Wolf Pelt Rug",
        "category": "decoration",
        "description": "A thick pelt softens the stone floor.",
        "source": "wolf_drop",
        "map_icon": "r",
        "map_color": "#6f5a45",
    },
    "crystal_chandelier": {
        "name": "Crystal Chandelier",
        "category": "decoration",
        "description": "Prismatic light fills the room.",
        "source": "crystal_chest_drop",
        "map_icon": "c",
        "map_color": "#5f8fb3",
        "wall_only": True,
    },
    "iron_sconce": {
        "name": "Iron Sconce",
        "category": "decoration",
        "description": "A torch in iron housing casts warm light.",
        "source": "elara_shop",
        "price": 50,
        "map_icon": "s",
        "map_color": "#7b5737",
        "wall_only": True,
    },
    "old_painting_seascape": {
        "name": "Old Painting - Seascape",
        "category": "decoration",
        "description": "A faded painting of a stormy sea.",
        "source": "fishing_rare",
        "map_icon": "p",
        "map_color": "#4f7f9b",
        "wall_only": True,
    },
    "old_painting_forest": {
        "name": "Old Painting - Forest",
        "category": "decoration",
        "description": "Sunlight filters through a painted forest.",
        "source": "fishing_rare",
        "map_icon": "p",
        "map_color": "#537f4f",
        "wall_only": True,
    },
    "dungeon_banner": {
        "name": "Dungeon Banner",
        "category": "decoration",
        "description": "A banner bearing the symbol of a conquered dungeon.",
        "source": "first_clear_reward",
        "map_icon": "d",
        "map_color": "#8f3f3f",
        "wall_only": True,
    },
    "mounted_skull": {
        "name": "Mounted Skull",
        "category": "decoration",
        "description": "The skull of a fearsome beast.",
        "source": "boss_drop",
        "map_icon": "m",
        "map_color": "#8a8a8a",
        "wall_only": True,
    },
    "enchanted_mirror": {
        "name": "Enchanted Mirror",
        "category": "decoration",
        "description": "Your reflection looks slightly braver.",
        "source": "all_dungeons_achievement",
        "map_icon": "e",
        "map_color": "#7b92b8",
    },
    "garden_planter": {
        "name": "Garden Planter",
        "category": "decoration",
        "description": "Herbs grow quietly in the corner.",
        "source": "old_martha_quest",
        "map_icon": "g",
        "map_color": "#4f7a4f",
        "allowed_rooms": ["garden"],
    },
    "arcane_orrery": {
        "name": "Arcane Orrery",
        "category": "decoration",
        "description": "Tiny planets orbit a central gem.",
        "source": "elara_rare_stock",
        "price": 500,
        "spawn_chance": 0.10,
        "map_icon": "o",
        "map_color": "#6b6bb3",
    },
    "battle_map": {
        "name": "Battle Map",
        "category": "decoration",
        "description": "A map of your adventures thus far.",
        "source": "visit_50_rooms_achievement",
        "map_icon": "b",
        "map_color": "#8f7b3f",
    },
    "healer_shrine": {
        "name": "Healer Shrine",
        "category": "decoration",
        "description": "A small shrine to the god of healing.",
        "source": "father_aldric_quest",
        "map_icon": "h",
        "map_color": "#6b8f8f",
    },

    # Expansions (home unlock markers)
    "study_annex": {
        "name": "Study Annex",
        "category": "expansion",
        "description": "Adds a 12-tile study section.",
        "source": "elara_shop",
        "price": 400,
        "map_icon": "U",
        "map_color": "#8a6a45",
    },
    "training_chamber": {
        "name": "Training Chamber",
        "category": "expansion",
        "description": "Adds 12 tiles and a training area.",
        "source": "elara_shop",
        "price": 600,
        "map_icon": "N",
        "map_color": "#7f5a4a",
    },
    "garden_room": {
        "name": "Garden Room",
        "category": "expansion",
        "description": "Adds 12 tiles for herb growth.",
        "source": "elara_shop",
        "price": 500,
        "map_icon": "V",
        "map_color": "#4f7f4f",
    },
    "vault_room": {
        "name": "Vault Room",
        "category": "expansion",
        "description": "Adds 12 tiles and large chest access.",
        "source": "elara_shop",
        "price": 700,
        "map_icon": "L",
        "map_color": "#6b6b6b",
    },
}


def _normalized_room_ids(room_ids):
    normalized = []
    for room_id in room_ids or []:
        text = str(room_id or "").strip().lower().replace(" ", "_")
        if text:
            normalized.append(text)
    return list(dict.fromkeys(normalized))


def _default_allowed_rooms(item_id, data):
    existing = data.get("allowed_rooms")
    if existing:
        return _normalized_room_ids(existing)

    use_action = str(data.get("use_action", "")).strip().lower()
    category = str(data.get("category", "")).strip().lower()
    source = str(data.get("source", "")).strip().lower()

    if item_id == "garden_planter":
        return ["garden"]
    if item_id == "cozy_bed" or use_action == "rest":
        return ["bedroom"]
    if item_id == "trophy_mount" or source in {"boss_drop", "boss_blueprint"}:
        return ["trophy"]
    if item_id == "personal_chest" or use_action == "chest":
        return ["storage"]
    if item_id in {"home_workbench", "home_alchemy_table", "home_forge", "home_enchanting_table", "home_smelting_furnace", "caldron"}:
        return ["workshop"]
    if use_action in {"craft", "alchemy", "forge", "enchant", "smelt", "ritual"}:
        return ["workshop"]
    if use_action == "bookshelf":
        return ["bedroom"]
    if category == "altar":
        return ["foyer"]
    if category == "expansion":
        return ["foyer"]
    if category == "decoration":
        return ["foyer"]

    return ["foyer"]


def _apply_default_room_restrictions():
    for item_id, data in HOME_ITEMS.items():
        if not isinstance(data, dict):
            continue
        data["allowed_rooms"] = _default_allowed_rooms(item_id, data)
_apply_default_room_restrictions()


def get_home_item(item_id):
    return HOME_ITEMS.get(item_id)


def get_home_items_by_category(category):
    return {iid: data for iid, data in HOME_ITEMS.items() if data.get("category") == category}


def get_elara_catalog():
    return {
        iid: data
        for iid, data in HOME_ITEMS.items()
        if data.get("source") in ("elara_shop", "elara_rare_stock")
    }
