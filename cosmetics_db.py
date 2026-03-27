"""
Cosmetics database and helpers for equipment appearance overrides.
"""

COSMETICS_DATABASE = {
    "veteran_polish": {
        "name": "Veteran Polish",
        "description": "A clean, battle-worn finish.",
        "allowed_slots": ["weapon", "armor", "shield", "helm", "boots", "gloves", "accessory"],
        "source": "default",
    },
    "slayer_crimson": {
        "name": "Slayer Crimson",
        "description": "Deep red finish earned through boss hunting.",
        "allowed_slots": ["weapon", "armor", "shield", "helm", "boots", "gloves"],
        "source": "achievement:boss_slayer",
    },
    "delver_mantle": {
        "name": "Delver Mantle",
        "description": "Dusty stone look from deep dungeon expeditions.",
        "allowed_slots": ["armor", "shield", "helm", "boots", "gloves"],
        "source": "achievement:dungeon_master",
    },
    "astral_thread": {
        "name": "Astral Thread",
        "description": "A star-sheened weave for true masters.",
        "allowed_slots": ["armor", "helm", "gloves", "accessory"],
        "source": "achievement:mastery",
    },
    "void_crown": {
        "name": "Void Crown",
        "description": "A dark shimmer that bends light around edges.",
        "allowed_slots": ["weapon", "armor", "shield", "helm", "gloves", "accessory"],
        "source": "achievement:void_titan_slayer",
    },
}

DEFAULT_UNLOCKED_COSMETICS = ["veteran_polish"]


def normalize_cosmetic_id(value):
    return str(value or "").strip().lower().replace(" ", "_")


def get_cosmetic(cosmetic_id):
    return COSMETICS_DATABASE.get(normalize_cosmetic_id(cosmetic_id))


def get_cosmetics_for_slot(slot):
    slot = str(slot or "").strip().lower()
    out = {}
    for cid, data in COSMETICS_DATABASE.items():
        allowed = data.get("allowed_slots", [])
        if slot in allowed:
            out[cid] = data
    return out
