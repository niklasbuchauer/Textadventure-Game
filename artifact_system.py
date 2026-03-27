"""
Artifact / relic system.

Artifacts are unique items that occupy a dedicated slot and grant passive stats.
"""

ARTIFACT_DATABASE = {
    "void_heart": {
        "name": "Void Heart",
        "description": "A shard pulsing with distant gravity.",
        "stats": {"attack": 2, "perception": 1},
        "source": "boss:void_titan",
    },
    "dragon_idol": {
        "name": "Dragon Idol",
        "description": "An idol warm to the touch, resonating with might.",
        "stats": {"strength": 2, "constitution": 1},
        "source": "boss:dragon_lair",
    },
    "moon_sigil": {
        "name": "Moon Sigil",
        "description": "Silver glyph that sharpens focus in darkness.",
        "stats": {"dexterity": 1, "perception": 2},
        "source": "dungeon:shadow_depths",
    },
    "warden_emblem": {
        "name": "Warden Emblem",
        "description": "A weathered crest carried by old protectors.",
        "stats": {"defense": 2, "health_max": 8},
        "source": "dungeon:iron_halls",
    },
    "astral_lens": {
        "name": "Astral Lens",
        "description": "Crystalline lens attuned to arcane current.",
        "stats": {"max_mana": 12, "charisma": 1},
        "source": "dungeon:crystal_caverns",
    },
}

# Combat-specific passive effects keyed by artifact id.
# Multipliers are applied directly in combat math.
ARTIFACT_COMBAT_EFFECTS = {
    "void_heart": {
        "outgoing_mult": 1.05,
        "tag_multipliers": {"arcane": 1.15, "poison": 1.10},
        "lifesteal_pct": 0.08,
        "incoming_mult": 0.97,
    },
    "dragon_idol": {
        "outgoing_mult": 1.04,
        "tag_multipliers": {"physical": 1.12},
        "incoming_mult": 0.94,
    },
    "moon_sigil": {
        "outgoing_mult": 1.03,
        "crit_chance_bonus": 0.05,
        "crit_damage_bonus": 0.20,
    },
    "warden_emblem": {
        "incoming_mult": 0.86,
    },
    "astral_lens": {
        "outgoing_mult": 1.04,
        "tag_multipliers": {"arcane": 1.18, "burn": 1.10, "frost": 1.10},
        "crit_chance_bonus": 0.02,
    },
}


def _ensure_artifact_state(player):
    if "artifact_slot" not in player.state:
        player.state["artifact_slot"] = None


def _resolve_artifact_id(query):
    q = str(query or "").strip().lower().replace(" ", "_")
    if q in ARTIFACT_DATABASE:
        return q
    for aid, data in ARTIFACT_DATABASE.items():
        if data.get("name", "").strip().lower().replace(" ", "_") == q:
            return aid
    return None


def _apply_artifact_stats(player, artifact_id, sign=1):
    data = ARTIFACT_DATABASE.get(artifact_id, {})
    for stat, val in data.get("stats", {}).items():
        player.stats[stat] = int(player.stats.get(stat, 0)) + (int(val) * int(sign))


def get_equipped_artifact(player):
    _ensure_artifact_state(player)
    return player.state.get("artifact_slot")


def get_artifact_combat_effects(player):
    """Return combat effect dict for the currently equipped artifact."""
    artifact_id = get_equipped_artifact(player)
    if not artifact_id:
        return {}, None
    return dict(ARTIFACT_COMBAT_EFFECTS.get(artifact_id, {})), artifact_id


def equip_artifact(player, query):
    _ensure_artifact_state(player)
    artifact_id = _resolve_artifact_id(query)
    if not artifact_id:
        return False, f"Unknown artifact '{query}'."

    if int(player.inventory.get(artifact_id, 0)) <= 0:
        return False, f"You do not have {ARTIFACT_DATABASE[artifact_id]['name']}."

    old = player.state.get("artifact_slot")
    if old:
        _apply_artifact_stats(player, old, sign=-1)
        player.inventory[old] = int(player.inventory.get(old, 0)) + 1

    player.inventory[artifact_id] = int(player.inventory.get(artifact_id, 0)) - 1
    if player.inventory[artifact_id] <= 0:
        del player.inventory[artifact_id]

    player.state["artifact_slot"] = artifact_id
    _apply_artifact_stats(player, artifact_id, sign=1)

    return True, f"Equipped artifact: {ARTIFACT_DATABASE[artifact_id]['name']}."


def unequip_artifact(player):
    _ensure_artifact_state(player)
    old = player.state.get("artifact_slot")
    if not old:
        return False, "No artifact is equipped."

    _apply_artifact_stats(player, old, sign=-1)
    player.inventory[old] = int(player.inventory.get(old, 0)) + 1
    player.state["artifact_slot"] = None

    return True, f"Unequipped artifact: {ARTIFACT_DATABASE[old]['name']}."


def get_artifact_display(player):
    _ensure_artifact_state(player)
    equipped = player.state.get("artifact_slot")

    result = "\n" + "=" * 55 + "\n"
    result += "  ARTIFACTS\n"
    result += "=" * 55 + "\n"

    if equipped:
        data = ARTIFACT_DATABASE.get(equipped, {})
        result += f"  Equipped: {data.get('name', equipped)}\n"
        result += f"  {data.get('description', '')}\n"
        stats = data.get("stats", {})
        if stats:
            result += "  Bonuses:\n"
            for stat, val in sorted(stats.items()):
                result += f"    {stat.replace('_', ' ').capitalize()}: +{val}\n"
    else:
        result += "  Equipped: none\n"

    result += "\n  Owned artifacts in inventory:\n"
    found = False
    for aid, qty in sorted(player.inventory.items()):
        if aid in ARTIFACT_DATABASE and int(qty) > 0:
            found = True
            result += f"    - {ARTIFACT_DATABASE[aid]['name']} x{qty}\n"
    if not found:
        result += "    (none)\n"

    result += "=" * 55 + "\n"
    return result
