"""
Home item database for the pocket-dimension player home.
Data-only module so gameplay systems can remain logic-focused.
"""

from home_assets import SHEET_LAYOUTS

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
    },
    "trophy_mount": {
        "name": "Trophy Mount",
        "category": "functional",
        "description": "A wall mount to display boss trophies.",
        "source": "boss_blueprint",
        "map_icon": "T",
        "map_color": "#7b4a2a",
        "wall_only": True,
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


def _iter_sheet_tiles(sheet_name):
    cols, rows = SHEET_LAYOUTS.get(sheet_name, (0, 0))
    for y in range(rows):
        for x in range(cols):
            yield x, y


def _sprite_meta(sheet_name, x, y, w=1, h=1):
    return {"sheet": sheet_name, "x": int(x), "y": int(y), "w": int(w), "h": int(h)}


def _sheet_id(sheet_name):
    base = sheet_name.replace("TopDownHouse_", "").replace(".png", "")
    return base.lower()


def _assign_and_generate_home_asset_items():
    primary_sheet_order = [
        "TopDownHouse_FurnitureState1.png",
        "TopDownHouse_SmallItems.png",
        "TopDownHouse_DoorsAndWindows.png",
        "TopDownHouse_FloorsAndWalls.png",
        "TopDownHouse_FloorsAndWalls_OpenDoors.png",
    ]

    all_coords = []
    for sheet in primary_sheet_order:
        for x, y in _iter_sheet_tiles(sheet):
            all_coords.append((sheet, x, y))

    # 1) Ensure all existing home items receive a sprite.
    existing_ids = list(HOME_ITEMS.keys())
    coord_idx = 0
    for item_id in existing_ids:
        data = HOME_ITEMS[item_id]
        if not isinstance(data, dict):
            continue
        if isinstance(data.get("sprite"), dict):
            continue
        if coord_idx >= len(all_coords):
            break

        sheet, x, y = all_coords[coord_idx]
        coord_idx += 1
        data["sprite"] = _sprite_meta(sheet, x, y)

        # Furniture state 2 is used as an alternate texture where available.
        if sheet == "TopDownHouse_FurnitureState1.png":
            data.setdefault("texture_variants", {})
            data["texture_variants"]["state2"] = _sprite_meta("TopDownHouse_FurnitureState2.png", x, y)

    # 2) Add every unused texture as a new placeable decoration item.
    used = set()
    for _item_id, data in HOME_ITEMS.items():
        if not isinstance(data, dict):
            continue
        sprite = data.get("sprite")
        if isinstance(sprite, dict):
            used.add((sprite.get("sheet"), int(sprite.get("x", 0)), int(sprite.get("y", 0))))
        tex_var = data.get("texture_variants", {})
        if isinstance(tex_var, dict):
            for _k, var in tex_var.items():
                if isinstance(var, dict):
                    used.add((var.get("sheet"), int(var.get("x", 0)), int(var.get("y", 0))))

    generated = 0
    for sheet_name in SHEET_LAYOUTS.keys():
        sid = _sheet_id(sheet_name)
        for x, y in _iter_sheet_tiles(sheet_name):
            key = (sheet_name, x, y)
            if key in used:
                continue

            item_id = f"home_asset_{sid}_{x}_{y}"
            if item_id in HOME_ITEMS:
                continue

            HOME_ITEMS[item_id] = {
                "name": f"{sid.replace('_', ' ').title()} Tile {x},{y}",
                "category": "decoration",
                "description": f"Decorative asset tile from {sheet_name} at ({x}, {y}).",
                "source": "home_asset_pack",
                "price": 15,
                "map_icon": "*",
                "map_color": "#a8a8a8",
                "sprite": _sprite_meta(sheet_name, x, y),
            }

            # If this tile exists in both furniture states, expose the counterpart as texture variant.
            if sheet_name == "TopDownHouse_FurnitureState1.png":
                HOME_ITEMS[item_id]["texture_variants"] = {
                    "state2": _sprite_meta("TopDownHouse_FurnitureState2.png", x, y)
                }
            elif sheet_name == "TopDownHouse_FurnitureState2.png":
                HOME_ITEMS[item_id]["texture_variants"] = {
                    "state1": _sprite_meta("TopDownHouse_FurnitureState1.png", x, y)
                }

            generated += 1

    return generated


GENERATED_HOME_ASSET_ITEMS = _assign_and_generate_home_asset_items()


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
