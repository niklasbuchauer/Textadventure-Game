"""
Prestige / Ascension system.

Resets progression at max level while granting permanent meta bonuses.
"""

from progression_system import CLASS_DEFINITIONS, MAX_LEVEL, XP_TABLE

_CENTER_NODES = {
    "warrior": "w_origin",
    "rogue": "r_origin",
    "mage": "m_origin",
}

_CLASS_PRESTIGE_BONUS = {
    "warrior": {"strength": 1, "defense": 1},
    "rogue": {"dexterity": 1, "perception": 1},
    "mage": {"charisma": 1, "perception": 1},
}


def _ensure_prestige_state(player):
    state = player.state
    stats = player.stats

    state.setdefault("prestige_level", 0)
    state.setdefault("ascension_tokens", 0)
    state.setdefault("prestige_bonuses", {})
    state.setdefault("prestige_runs", 0)
    state.setdefault("prestige_history", [])
    stats.setdefault("prestige_xp_multiplier", 1.0)


def can_ascend(player):
    _ensure_prestige_state(player)
    level = int(player.stats.get("level", 1))
    class_id = str(player.stats.get("class", "none"))
    return level >= MAX_LEVEL and class_id in CLASS_DEFINITIONS


def _return_equipped_items_to_inventory(player):
    equip = player.state.get("equipment", {})
    if not isinstance(equip, dict):
        return
    for slot, item_id in list(equip.items()):
        if item_id:
            player.inventory[item_id] = int(player.inventory.get(item_id, 0)) + 1
            equip[slot] = None


def _reset_progression(player):
    stats = player.stats
    state = player.state

    class_id = str(stats.get("class", "none"))
    class_def = CLASS_DEFINITIONS.get(class_id)
    if not class_def:
        return False, "Choose a class before ascending."

    _return_equipped_items_to_inventory(player)

    # Reset progression values.
    stats["level"] = 1
    stats["xp"] = 0
    stats["xp_to_next"] = XP_TABLE[1] if len(XP_TABLE) > 1 else 0
    stats["skill_points"] = 0

    # Reset base combat resources.
    stats["health_max"] = 100
    stats["health"] = 100
    mana_base = {"warrior": 80, "rogue": 90, "mage": 120}.get(class_id, 80)
    stats["max_mana"] = mana_base
    stats["mana"] = mana_base

    # Rebuild class-core attributes from scratch.
    base_stats = ["strength", "defense", "constitution", "dexterity", "perception", "charisma"]
    for stat in base_stats:
        stats[stat] = 0
    for stat, val in class_def.get("starting_stats", {}).items():
        stats[stat] = int(stats.get(stat, 0)) + int(val)

    # Clear active progression-specific runtime state.
    state["unlocked_skills"] = []
    center = _CENTER_NODES.get(class_id)
    if center:
        state["unlocked_skills"].append(center)
    state["cooldowns"] = {}
    state["active_effects"] = {}
    state["enchantments"] = {}

    # Clear equipped appearance overrides but preserve unlocked cosmetics.
    appearance = state.get("equipment_appearance", {})
    if isinstance(appearance, dict):
        for slot in appearance.keys():
            appearance[slot] = None

    return True, ""


def _grant_prestige_bonuses(player, new_prestige_level):
    class_id = str(player.stats.get("class", "none"))
    base_bonus = dict(_CLASS_PRESTIGE_BONUS.get(class_id, {}))

    # Every second ascension grants +1 constitution.
    if new_prestige_level % 2 == 0:
        base_bonus["constitution"] = int(base_bonus.get("constitution", 0)) + 1

    bonus_store = player.state.get("prestige_bonuses", {})
    for stat, val in base_bonus.items():
        bonus_store[stat] = int(bonus_store.get(stat, 0)) + int(val)
    player.state["prestige_bonuses"] = bonus_store

    # Apply all accumulated prestige bonuses to current stat line.
    for stat, total in bonus_store.items():
        player.stats[stat] = int(player.stats.get(stat, 0)) + int(total)

    # Scale XP income gently per ascension.
    player.stats["prestige_xp_multiplier"] = round(1.0 + (new_prestige_level * 0.10), 2)

    return base_bonus


def apply_prestige(player):
    _ensure_prestige_state(player)

    if not can_ascend(player):
        return False, f"Ascension requires level {MAX_LEVEL}."

    old_level = int(player.stats.get("level", 1))
    class_id = str(player.stats.get("class", "none"))

    state = player.state
    state["prestige_level"] = int(state.get("prestige_level", 0)) + 1
    state["ascension_tokens"] = int(state.get("ascension_tokens", 0)) + 1
    state["prestige_runs"] = int(state.get("prestige_runs", 0)) + 1

    ok, err = _reset_progression(player)
    if not ok:
        return False, err

    granted = _grant_prestige_bonuses(player, state["prestige_level"])

    state["prestige_history"].append({
        "class": class_id,
        "from_level": old_level,
        "to_prestige": state["prestige_level"],
    })

    parts = [
        "\n" + "=" * 58,
        "  ASCENSION COMPLETE",
        "=" * 58,
        f"  Prestige Level: {state['prestige_level']}",
        f"  Ascension Tokens: {state['ascension_tokens']}",
        f"  XP Multiplier: x{player.stats.get('prestige_xp_multiplier', 1.0):.2f}",
        "",
        "  Permanent bonuses gained this ascension:",
    ]
    for stat, val in sorted(granted.items()):
        parts.append(f"    {stat.capitalize()}: +{val}")

    parts.extend([
        "",
        "  Progression reset to Level 1. Your class remains the same.",
        "  Use 'skills' to rebuild your tree and grow stronger.",
        "=" * 58,
    ])

    return True, "\n".join(parts)


def get_prestige_status_text(player):
    _ensure_prestige_state(player)

    state = player.state
    stats = player.stats
    level = int(stats.get("level", 1))
    class_id = str(stats.get("class", "none"))
    class_name = CLASS_DEFINITIONS.get(class_id, {}).get("name", "None")

    lines = [
        "\n" + "=" * 58,
        "  ASCENSION STATUS",
        "=" * 58,
        f"  Class: {class_name}",
        f"  Current Level: {level}/{MAX_LEVEL}",
        f"  Prestige Level: {state.get('prestige_level', 0)}",
        f"  Ascension Tokens: {state.get('ascension_tokens', 0)}",
        f"  XP Multiplier: x{stats.get('prestige_xp_multiplier', 1.0):.2f}",
        "",
    ]

    bonuses = state.get("prestige_bonuses", {})
    if bonuses:
        lines.append("  Permanent Prestige Bonuses:")
        for stat, val in sorted(bonuses.items()):
            lines.append(f"    {stat.capitalize()}: +{val}")
    else:
        lines.append("  Permanent Prestige Bonuses: none yet")

    lines.append("")
    if can_ascend(player):
        lines.append("  You are eligible to ascend now. Type: prestige")
    else:
        lines.append(f"  Reach level {MAX_LEVEL} to ascend. ({MAX_LEVEL - level} levels remaining)")

    lines.append("=" * 58)
    return "\n".join(lines)
