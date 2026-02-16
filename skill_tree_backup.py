"""
Skill Tree System
=================
Class-based skill trees with tiered nodes:
  - Passive nodes: permanent stat bonuses
  - Active nodes: usable abilities with cooldowns

Each class (Warrior, Rogue, Mage) has its own tree with 12 nodes
across 5 tiers. Nodes require prerequisite nodes and cost skill points.

The graphical skill tree window is built using Tkinter Canvas,
similar to the LiveMapWindow pattern.
"""

import tkinter as tk
from tkinter import font as tkfont

# =====================================================================
# SKILL NODE SCHEMA
# =====================================================================
# {
#   "id":            unique string
#   "name":          display name
#   "description":   tooltip / details
#   "tier":          1-5 (determines position)
#   "type":          "passive" or "active"
#   "cost":          skill points to unlock
#   "prerequisites": list of node IDs that must be unlocked first
#   "stat_bonuses":  dict of stat_name -> value (for passive nodes)
#   "ability":       dict defining the active ability (for active nodes):
#       "name":       ability name
#       "cooldown":   number of moves before it can be used again
#       "effect":     what it does (parsed by ability system)
#       "use_text":   message shown when used
# }
# =====================================================================


# ═════════════════════════════════════════════════════════════════════
# WARRIOR SKILL TREE
# ═════════════════════════════════════════════════════════════════════

WARRIOR_TREE = [
    # ── Tier 1 (starting skills) ──
    {
        "id": "w_toughened_skin",
        "name": "Toughened Skin",
        "description": "Years of battle have hardened your body.\n+2 Defense",
        "tier": 1,
        "type": "passive",
        "cost": 1,
        "prerequisites": [],
        "stat_bonuses": {"defense": 2},
    },
    {
        "id": "w_iron_grip",
        "name": "Iron Grip",
        "description": "Your hands are strong as iron.\n+2 Strength",
        "tier": 1,
        "type": "passive",
        "cost": 1,
        "prerequisites": [],
        "stat_bonuses": {"strength": 2},
    },

    # ── Tier 2 ──
    {
        "id": "w_shield_bash",
        "name": "Shield Bash",
        "description": "Slam your shield to stun a trap mechanism,\npreventing it from triggering for 3 moves.\nCooldown: 8 moves",
        "tier": 2,
        "type": "active",
        "cost": 1,
        "prerequisites": ["w_toughened_skin"],
        "stat_bonuses": {},
        "ability": {
            "name": "Shield Bash",
            "cooldown": 8,
            "effect": "stun_trap",
            "duration": 3,
            "use_text": "You slam your shield against the mechanism! The trap is stunned!",
        },
    },
    {
        "id": "w_heavy_lifter",
        "name": "Heavy Lifter",
        "description": "Carry heavier gear without slowing down.\n+2 Strength, +1 Constitution",
        "tier": 2,
        "type": "passive",
        "cost": 1,
        "prerequisites": ["w_iron_grip"],
        "stat_bonuses": {"strength": 2, "constitution": 1},
    },

    # ── Tier 3 ──
    {
        "id": "w_fortify",
        "name": "Fortify",
        "description": "Brace yourself, gaining a temporary\ndefense boost for the next 5 moves.\n+5 Defense (temporary). Cooldown: 10 moves",
        "tier": 3,
        "type": "active",
        "cost": 2,
        "prerequisites": ["w_shield_bash"],
        "stat_bonuses": {},
        "ability": {
            "name": "Fortify",
            "cooldown": 10,
            "effect": "temp_defense",
            "value": 5,
            "duration": 5,
            "use_text": "You plant your feet and brace yourself. Your defense surges!",
        },
    },
    {
        "id": "w_battle_hardened",
        "name": "Battle Hardened",
        "description": "Combat has forged your body into steel.\n+15 Max Health, +1 Defense",
        "tier": 3,
        "type": "passive",
        "cost": 2,
        "prerequisites": ["w_heavy_lifter"],
        "stat_bonuses": {"defense": 1, "health_max_bonus": 15},
    },
    {
        "id": "w_iron_will",
        "name": "Iron Will",
        "description": "Your mental fortitude is unshakable.\n+2 Constitution (reduces poison duration)",
        "tier": 3,
        "type": "passive",
        "cost": 1,
        "prerequisites": ["w_toughened_skin"],
        "stat_bonuses": {"constitution": 2},
    },

    # ── Tier 4 ──
    {
        "id": "w_war_cry",
        "name": "War Cry",
        "description": "Let out a mighty shout that reveals all\ntraps in adjacent rooms.\nCooldown: 12 moves",
        "tier": 4,
        "type": "active",
        "cost": 2,
        "prerequisites": ["w_fortify", "w_iron_will"],
        "stat_bonuses": {},
        "ability": {
            "name": "War Cry",
            "cooldown": 12,
            "effect": "reveal_adjacent_traps",
            "use_text": "Your war cry echoes through the dungeon! You sense the dangers ahead!",
        },
    },
    {
        "id": "w_armor_mastery",
        "name": "Armor Mastery",
        "description": "Master of armor, you reduce ALL incoming\ndamage by a flat 5 points.\n+3 Defense",
        "tier": 4,
        "type": "passive",
        "cost": 2,
        "prerequisites": ["w_battle_hardened"],
        "stat_bonuses": {"defense": 3},
    },

    # ── Tier 5 (ultimate) ──
    {
        "id": "w_unstoppable",
        "name": "Unstoppable",
        "description": "ULTIMATE: You become immune to the next\ntrap that triggers. Automatically blocks it.\nCooldown: 20 moves",
        "tier": 5,
        "type": "active",
        "cost": 3,
        "prerequisites": ["w_war_cry", "w_armor_mastery"],
        "stat_bonuses": {},
        "ability": {
            "name": "Unstoppable",
            "cooldown": 20,
            "effect": "trap_immunity",
            "duration": 1,
            "use_text": "An aura of invincibility surrounds you! The next trap cannot harm you!",
        },
    },
    {
        "id": "w_titan",
        "name": "Titan's Endurance",
        "description": "ULTIMATE PASSIVE: The body of a titan.\n+4 Strength, +3 Defense, +3 Constitution,\n+25 Max Health",
        "tier": 5,
        "type": "passive",
        "cost": 3,
        "prerequisites": ["w_armor_mastery"],
        "stat_bonuses": {"strength": 4, "defense": 3, "constitution": 3, "health_max_bonus": 25},
    },
]


# ═════════════════════════════════════════════════════════════════════
# ROGUE SKILL TREE
# ═════════════════════════════════════════════════════════════════════

ROGUE_TREE = [
    # ── Tier 1 ──
    {
        "id": "r_keen_eye",
        "name": "Keen Eye",
        "description": "Your sharp eyes miss nothing.\n+2 Perception (better trap detection)",
        "tier": 1,
        "type": "passive",
        "cost": 1,
        "prerequisites": [],
        "stat_bonuses": {"perception": 2},
    },
    {
        "id": "r_nimble_fingers",
        "name": "Nimble Fingers",
        "description": "Your hands move with practised ease.\n+2 Dexterity (better disarm chance)",
        "tier": 1,
        "type": "passive",
        "cost": 1,
        "prerequisites": [],
        "stat_bonuses": {"dexterity": 2},
    },

    # ── Tier 2 ──
    {
        "id": "r_locksmith",
        "name": "Locksmith",
        "description": "You've picked so many locks, it's second nature.\n+15% disarm success rate.\n+1 Dexterity",
        "tier": 2,
        "type": "passive",
        "cost": 1,
        "prerequisites": ["r_nimble_fingers"],
        "stat_bonuses": {"dexterity": 1, "disarm_bonus": 0.15},
    },
    {
        "id": "r_sneak",
        "name": "Sneak",
        "description": "Become one with the shadows. The next trap\nyou walk into will NOT trigger.\nCooldown: 8 moves",
        "tier": 2,
        "type": "active",
        "cost": 1,
        "prerequisites": ["r_keen_eye"],
        "stat_bonuses": {},
        "ability": {
            "name": "Sneak",
            "cooldown": 8,
            "effect": "bypass_trap",
            "duration": 1,
            "use_text": "You melt into the shadows, moving silently...",
        },
    },

    # ── Tier 3 ──
    {
        "id": "r_critical_eye",
        "name": "Critical Eye",
        "description": "Focus intensely — guaranteed trap detection\nfor the next 3 rooms you enter.\nCooldown: 10 moves",
        "tier": 3,
        "type": "active",
        "cost": 2,
        "prerequisites": ["r_sneak"],
        "stat_bonuses": {},
        "ability": {
            "name": "Critical Eye",
            "cooldown": 10,
            "effect": "guaranteed_detection",
            "duration": 3,
            "use_text": "Your eyes glow with intense focus. Every trap ahead will be revealed!",
        },
    },
    {
        "id": "r_haggler",
        "name": "Haggler",
        "description": "Your silver tongue gets better prices.\n+3 Charisma (better shop deals)",
        "tier": 3,
        "type": "passive",
        "cost": 1,
        "prerequisites": ["r_nimble_fingers"],
        "stat_bonuses": {"charisma": 3},
    },
    {
        "id": "r_shadow_step",
        "name": "Shadow Step",
        "description": "Move through shadows to avoid danger.\n+2 Dexterity, +1 Perception",
        "tier": 3,
        "type": "passive",
        "cost": 2,
        "prerequisites": ["r_locksmith"],
        "stat_bonuses": {"dexterity": 2, "perception": 1},
    },

    # ── Tier 4 ──
    {
        "id": "r_plunder",
        "name": "Plunder",
        "description": "Your next chest gives DOUBLE loot!\nGold and items are doubled.\nCooldown: 15 moves",
        "tier": 4,
        "type": "active",
        "cost": 2,
        "prerequisites": ["r_critical_eye", "r_shadow_step"],
        "stat_bonuses": {},
        "ability": {
            "name": "Plunder",
            "cooldown": 15,
            "effect": "double_loot",
            "duration": 1,
            "use_text": "Your treasure-hunting instincts kick in! The next chest will yield double!",
        },
    },
    {
        "id": "r_evasion",
        "name": "Evasion Master",
        "description": "You dodge like the wind.\n+3 Dexterity, +2 Perception",
        "tier": 4,
        "type": "passive",
        "cost": 2,
        "prerequisites": ["r_shadow_step"],
        "stat_bonuses": {"dexterity": 3, "perception": 2},
    },

    # ── Tier 5 ──
    {
        "id": "r_phantom",
        "name": "Phantom",
        "description": "ULTIMATE: Become invisible for 5 moves.\nAll traps are bypassed, all detection is\nguaranteed. Cooldown: 20 moves",
        "tier": 5,
        "type": "active",
        "cost": 3,
        "prerequisites": ["r_plunder", "r_evasion"],
        "stat_bonuses": {},
        "ability": {
            "name": "Phantom",
            "cooldown": 20,
            "effect": "phantom_mode",
            "duration": 5,
            "use_text": "You vanish from sight! For the next 5 moves, you are a phantom!",
        },
    },
    {
        "id": "r_master_thief",
        "name": "Master Thief",
        "description": "ULTIMATE PASSIVE: The pinnacle of roguish talent.\n+4 Dexterity, +3 Perception, +3 Charisma",
        "tier": 5,
        "type": "passive",
        "cost": 3,
        "prerequisites": ["r_evasion"],
        "stat_bonuses": {"dexterity": 4, "perception": 3, "charisma": 3},
    },
]


# ═════════════════════════════════════════════════════════════════════
# MAGE SKILL TREE
# ═════════════════════════════════════════════════════════════════════

MAGE_TREE = [
    # ── Tier 1 ──
    {
        "id": "m_arcane_mind",
        "name": "Arcane Mind",
        "description": "Your mind is attuned to magical energies.\n+2 Perception",
        "tier": 1,
        "type": "passive",
        "cost": 1,
        "prerequisites": [],
        "stat_bonuses": {"perception": 2},
    },
    {
        "id": "m_mana_well",
        "name": "Mana Well",
        "description": "A deep reservoir of life force sustains you.\n+2 Constitution",
        "tier": 1,
        "type": "passive",
        "cost": 1,
        "prerequisites": [],
        "stat_bonuses": {"constitution": 2},
    },

    # ── Tier 2 ──
    {
        "id": "m_arcane_shield",
        "name": "Arcane Shield",
        "description": "Conjure a magical barrier that absorbs\nthe next trap hit entirely (0 damage).\nCooldown: 8 moves",
        "tier": 2,
        "type": "active",
        "cost": 1,
        "prerequisites": ["m_mana_well"],
        "stat_bonuses": {},
        "ability": {
            "name": "Arcane Shield",
            "cooldown": 8,
            "effect": "absorb_trap",
            "duration": 1,
            "use_text": "A shimmering shield of arcane energy surrounds you!",
        },
    },
    {
        "id": "m_mystic_aura",
        "name": "Mystic Aura",
        "description": "Your presence radiates magical charm.\n+2 Charisma, +1 Perception",
        "tier": 2,
        "type": "passive",
        "cost": 1,
        "prerequisites": ["m_arcane_mind"],
        "stat_bonuses": {"charisma": 2, "perception": 1},
    },

    # ── Tier 3 ──
    {
        "id": "m_heal",
        "name": "Heal",
        "description": "Channel magical energy to restore 40 HP.\nCooldown: 6 moves",
        "tier": 3,
        "type": "active",
        "cost": 2,
        "prerequisites": ["m_arcane_shield"],
        "stat_bonuses": {},
        "ability": {
            "name": "Heal",
            "cooldown": 6,
            "effect": "heal",
            "value": 40,
            "use_text": "Warm golden light flows through your body, mending your wounds!",
        },
    },
    {
        "id": "m_enchanted_touch",
        "name": "Enchanted Touch",
        "description": "Your crafting is enhanced by magic.\n+2 Charisma, +1 Constitution\n(Crafted items gain bonus value)",
        "tier": 3,
        "type": "passive",
        "cost": 1,
        "prerequisites": ["m_mystic_aura"],
        "stat_bonuses": {"charisma": 2, "constitution": 1},
    },
    {
        "id": "m_elemental_resistance",
        "name": "Elemental Resistance",
        "description": "Magical wards protect you from elemental harm.\n+2 Defense, +1 Constitution\n(Reduces trap damage)",
        "tier": 3,
        "type": "passive",
        "cost": 2,
        "prerequisites": ["m_mana_well"],
        "stat_bonuses": {"defense": 2, "constitution": 1},
    },

    # ── Tier 4 ──
    {
        "id": "m_reveal",
        "name": "Reveal",
        "description": "Cast a revelation spell that shows ALL\ntraps and secrets on the current floor.\nCooldown: 12 moves",
        "tier": 4,
        "type": "active",
        "cost": 2,
        "prerequisites": ["m_heal", "m_elemental_resistance"],
        "stat_bonuses": {},
        "ability": {
            "name": "Reveal",
            "cooldown": 12,
            "effect": "reveal_floor",
            "use_text": "Arcane symbols pulse outward... The floor's secrets are laid bare!",
        },
    },
    {
        "id": "m_sage",
        "name": "Sage's Wisdom",
        "description": "Deep magical knowledge empowers you.\n+3 Perception, +2 Constitution",
        "tier": 4,
        "type": "passive",
        "cost": 2,
        "prerequisites": ["m_enchanted_touch"],
        "stat_bonuses": {"perception": 3, "constitution": 2},
    },

    # ── Tier 5 ──
    {
        "id": "m_archmage",
        "name": "Archmage",
        "description": "ULTIMATE: Become an archmage for 5 moves.\nAll traps are detected, you take 50% less\ndamage, and your next heal is doubled.\nCooldown: 20 moves",
        "tier": 5,
        "type": "active",
        "cost": 3,
        "prerequisites": ["m_reveal", "m_sage"],
        "stat_bonuses": {},
        "ability": {
            "name": "Archmage",
            "cooldown": 20,
            "effect": "archmage_mode",
            "duration": 5,
            "use_text": "ARCANE POWER SURGES THROUGH YOU! You ascend to Archmage!",
        },
    },
    {
        "id": "m_eternal_ward",
        "name": "Eternal Ward",
        "description": "ULTIMATE PASSIVE: Permanent magical protection.\n+4 Constitution, +3 Defense, +3 Charisma,\n+20 Max Health",
        "tier": 5,
        "type": "passive",
        "cost": 3,
        "prerequisites": ["m_sage"],
        "stat_bonuses": {"constitution": 4, "defense": 3, "charisma": 3, "health_max_bonus": 20},
    },
]


# =====================================================================
# SKILL TREES REGISTRY — maps class_id -> tree
# =====================================================================

SKILL_TREES = {
    "warrior": WARRIOR_TREE,
    "rogue": ROGUE_TREE,
    "mage": MAGE_TREE,
}


# =====================================================================
# SKILL TREE LOGIC
# =====================================================================

def get_tree_for_class(class_id):
    """Get the skill tree node list for a class."""
    return SKILL_TREES.get(class_id, [])


def get_node_by_id(class_id, node_id):
    """Find a specific skill node by its ID."""
    tree = get_tree_for_class(class_id)
    for node in tree:
        if node["id"] == node_id:
            return node
    return None


def get_all_nodes_by_id(class_id):
    """Return a dict mapping node_id -> node for quick lookups."""
    return {n["id"]: n for n in get_tree_for_class(class_id)}


def get_unlocked_skills(player):
    """Return list of unlocked skill IDs."""
    return list(player.state.get("unlocked_skills", []))


def is_skill_unlocked(player, skill_id):
    """Check if a specific skill is unlocked."""
    return skill_id in player.state.get("unlocked_skills", [])


def get_available_skills(player):
    """
    Return list of skill nodes the player CAN unlock right now
    (prerequisites met, not already unlocked, has enough skill points).
    """
    class_id = player.stats.get("class", "")
    tree = get_tree_for_class(class_id)
    unlocked = set(get_unlocked_skills(player))
    sp = player.stats.get("skill_points", 0)

    available = []
    for node in tree:
        if node["id"] in unlocked:
            continue
        # Check prerequisites
        prereqs_met = all(p in unlocked for p in node.get("prerequisites", []))
        if not prereqs_met:
            continue
        # Check cost
        if sp >= node["cost"]:
            available.append(node)

    return available


def unlock_skill(player, skill_id):
    """
    Unlock a skill node for the player.

    Args:
        player: Player object
        skill_id: ID of the skill to unlock

    Returns:
        (success: bool, message: str)
    """
    class_id = player.stats.get("class", "")
    node = get_node_by_id(class_id, skill_id)

    if not node:
        return False, "Unknown skill."

    unlocked = set(get_unlocked_skills(player))

    if skill_id in unlocked:
        return False, f"{node['name']} is already unlocked."

    # Check prerequisites
    for prereq in node.get("prerequisites", []):
        if prereq not in unlocked:
            prereq_node = get_node_by_id(class_id, prereq)
            prereq_name = prereq_node["name"] if prereq_node else prereq
            return False, f"Requires: {prereq_name}"

    # Check skill points
    sp = player.stats.get("skill_points", 0)
    if sp < node["cost"]:
        return False, f"Need {node['cost']} skill point{'s' if node['cost'] > 1 else ''}, have {sp}."

    # Spend skill points
    player.stats["skill_points"] = sp - node["cost"]

    # Add to unlocked list
    if "unlocked_skills" not in player.state:
        player.state["unlocked_skills"] = []
    player.state["unlocked_skills"].append(skill_id)

    # Apply stat bonuses (passive)
    for stat, value in node.get("stat_bonuses", {}).items():
        if stat == "health_max_bonus":
            player.stats["health_max"] = player.stats.get("health_max", 100) + value
            player.stats["health"] = min(
                player.stats.get("health", 100) + value,
                player.stats.get("health_max", 100)
            )
        else:
            player.stats[stat] = player.stats.get(stat, 0) + value

    # Build success message
    result = "\n" + "=" * 50 + "\n"
    result += f"  SKILL UNLOCKED: {node['name']}\n"
    result += "=" * 50 + "\n"
    result += f"  {node['description']}\n"

    if node["type"] == "active":
        ability = node.get("ability", {})
        result += f"\n  New ability: {ability.get('name', node['name'])}\n"
        result += f"  Cooldown: {ability.get('cooldown', 0)} moves\n"
        result += f"  Use it with: ability {ability.get('name', '').lower().replace(' ', '_')}\n"

    if node.get("stat_bonuses"):
        result += "\n  Stat changes:\n"
        for stat, val in node["stat_bonuses"].items():
            nice = stat.replace("_", " ").replace("health max bonus", "Max Health")
            result += f"    {nice.capitalize()}: +{val}\n"

    result += f"\n  Remaining skill points: {player.stats.get('skill_points', 0)}\n"
    result += "=" * 50 + "\n"

    return True, result


def get_active_abilities(player):
    """
    Return list of active ability dicts the player has unlocked.
    """
    class_id = player.stats.get("class", "")
    tree = get_tree_for_class(class_id)
    unlocked = set(get_unlocked_skills(player))

    abilities = []
    for node in tree:
        if node["id"] in unlocked and node["type"] == "active":
            ability = dict(node.get("ability", {}))
            ability["skill_id"] = node["id"]
            ability["skill_name"] = node["name"]
            abilities.append(ability)

    return abilities


def use_ability(player, ability_name):
    """
    Attempt to use an active ability.

    Args:
        player: Player object
        ability_name: Name or key of the ability to use

    Returns:
        (success: bool, message: str)
    """
    abilities = get_active_abilities(player)
    if not abilities:
        return False, "You don't have any active abilities yet."

    # Normalize the search term
    search = ability_name.lower().replace("_", " ").strip()

    # Find matching ability
    found = None
    for ab in abilities:
        ab_name = ab.get("name", "").lower()
        ab_key = ab_name.replace(" ", "_")
        if search in (ab_name, ab_key) or ab_name.startswith(search):
            found = ab
            break

    if not found:
        # Show available abilities
        names = [a["name"] for a in abilities]
        return False, f"Unknown ability. Your abilities: {', '.join(names)}"

    # Check cooldown
    cooldowns = player.state.get("cooldowns", {})
    cd_key = found["skill_id"]
    remaining = cooldowns.get(cd_key, 0)
    if remaining > 0:
        return False, f"{found['name']} is on cooldown ({remaining} moves remaining)."

    # Activate the ability
    effect = found.get("effect", "")
    duration = found.get("duration", 1)
    value = found.get("value", 0)

    # Set cooldown
    if "cooldowns" not in player.state:
        player.state["cooldowns"] = {}
    player.state["cooldowns"][cd_key] = found.get("cooldown", 10)

    # Apply effect to player state
    _apply_ability_effect(player, effect, duration, value)

    result = "\n" + "-" * 50 + "\n"
    result += f"  {found.get('use_text', 'You use ' + found['name'] + '!')}\n"
    result += f"  [{found['name']} active"
    if duration > 1:
        result += f" for {duration} moves"
    result += f"]\n"
    result += "-" * 50 + "\n"

    return True, result


def _apply_ability_effect(player, effect, duration, value):
    """Apply an ability's effect to the player state."""
    active_effects = player.state.get("active_effects", {})

    if effect == "stun_trap":
        active_effects["trap_stunned"] = duration
    elif effect == "temp_defense":
        active_effects["defense_boost"] = {"value": value, "duration": duration}
        player.stats["defense"] = player.stats.get("defense", 0) + value
    elif effect == "reveal_adjacent_traps":
        active_effects["reveal_traps"] = 1
    elif effect == "trap_immunity":
        active_effects["trap_immune"] = duration
    elif effect == "bypass_trap":
        active_effects["sneak_active"] = duration
    elif effect == "guaranteed_detection":
        active_effects["guaranteed_detection"] = duration
    elif effect == "double_loot":
        active_effects["double_loot"] = duration
    elif effect == "phantom_mode":
        active_effects["sneak_active"] = duration
        active_effects["guaranteed_detection"] = duration
    elif effect == "absorb_trap":
        active_effects["trap_immune"] = duration
    elif effect == "heal":
        hp = player.stats.get("health", 100)
        hp_max = player.stats.get("health_max", 100)
        heal_amt = value
        # Check for archmage double heal
        if active_effects.get("archmage_mode", 0) > 0:
            heal_amt *= 2
        player.stats["health"] = min(hp + heal_amt, hp_max)
    elif effect == "reveal_floor":
        active_effects["reveal_floor"] = 1
    elif effect == "archmage_mode":
        active_effects["archmage_mode"] = duration
        active_effects["guaranteed_detection"] = duration

    player.state["active_effects"] = active_effects


def tick_effects(player):
    """
    Called after each player move to decrement durations of active effects.
    Also ticks cooldowns.
    Returns list of messages about expired effects.
    """
    messages = []

    # Tick cooldowns
    cooldowns = player.state.get("cooldowns", {})
    expired_cds = []
    for key in list(cooldowns.keys()):
        cooldowns[key] -= 1
        if cooldowns[key] <= 0:
            expired_cds.append(key)
    for key in expired_cds:
        del cooldowns[key]

    # Tick active effects
    active = player.state.get("active_effects", {})
    expired = []
    for key in list(active.keys()):
        val = active[key]
        if isinstance(val, dict):
            # Effect with value and duration
            val["duration"] -= 1
            if val["duration"] <= 0:
                expired.append(key)
                # Remove temp stat boost
                if key == "defense_boost":
                    player.stats["defense"] = max(0, player.stats.get("defense", 0) - val.get("value", 0))
                    messages.append("  Your defense boost fades.")
        elif isinstance(val, int):
            active[key] = val - 1
            if active[key] <= 0:
                expired.append(key)
                if key == "trap_immune":
                    messages.append("  Your trap immunity fades.")
                elif key == "sneak_active":
                    messages.append("  You step out of the shadows.")
                elif key == "guaranteed_detection":
                    messages.append("  Your heightened awareness fades.")
                elif key == "archmage_mode":
                    messages.append("  Your archmage power fades.")
                elif key == "trap_stunned":
                    messages.append("  The stunned trap mechanism resets.")

    for key in expired:
        del active[key]

    # Clean up one-shot effects
    for key in ("reveal_traps", "reveal_floor"):
        if key in active:
            del active[key]

    player.state["active_effects"] = active

    return messages


def has_active_effect(player, effect_name):
    """Check if player has an active effect."""
    active = player.state.get("active_effects", {})
    val = active.get(effect_name, 0)
    if isinstance(val, dict):
        return val.get("duration", 0) > 0
    return val > 0


# =====================================================================
# GRAPHICAL SKILL TREE WINDOW (Tkinter Canvas)
# =====================================================================

# Layout constants
NODE_WIDTH = 120
NODE_HEIGHT = 50
TIER_SPACING_X = 180
NODE_SPACING_Y = 80
PADDING = 40

# Colors
COLOR_LOCKED = "#555555"
COLOR_AVAILABLE = "#2196F3"
COLOR_UNLOCKED = "#4CAF50"
COLOR_ACTIVE_ABILITY = "#FF9800"
COLOR_BG = "#1e1e1e"
COLOR_TEXT = "#ffffff"
COLOR_LINE = "#888888"
COLOR_LINE_UNLOCKED = "#4CAF50"
COLOR_TOOLTIP_BG = "#333333"
COLOR_TIER_LABEL = "#666666"


class SkillTreeWindow:
    """
    Graphical skill tree window using Tkinter Canvas.
    Shows skill nodes as rectangles connected by lines,
    organized by tier (left to right).
    """

    def __init__(self, root, player, engine=None):
        self.root = root
        self.player = player
        self.engine = engine
        self.window = None
        self.canvas = None
        self.node_items = {}  # canvas_id -> node_id
        self.node_rects = {}  # node_id -> (rect_id, text_id)
        self.tooltip = None
        self.tooltip_text = None
        self.info_frame = None
        self.info_label = None
        self.sp_label = None
        self._font = None

    def is_open(self):
        """Check if the window is currently open."""
        return self.window is not None and tk.Toplevel.winfo_exists(self.window)

    def create_window(self):
        """Create or focus the skill tree window."""
        if self.is_open():
            self.window.lift()
            self.window.focus_force()
            return

        self.window = tk.Toplevel(self.root)
        class_id = self.player.stats.get("class", "warrior")
        class_name = class_id.capitalize()
        self.window.title(f"Skill Tree - {class_name}")
        self.window.geometry("1000x650")
        self.window.configure(bg=COLOR_BG)
        self.window.resizable(True, True)

        self._font = tkfont.Font(family="Courier New", size=9)
        self._font_bold = tkfont.Font(family="Courier New", size=10, weight="bold")
        self._font_small = tkfont.Font(family="Courier New", size=8)

        # Top info bar
        self.info_frame = tk.Frame(self.window, bg="#2a2a2a", padx=10, pady=6)
        self.info_frame.pack(fill="x")

        class_label = tk.Label(
            self.info_frame,
            text=f"Class: {class_name}  |  Level: {self.player.stats.get('level', 1)}",
            font=self._font_bold, bg="#2a2a2a", fg=COLOR_TEXT
        )
        class_label.pack(side="left")

        self.sp_label = tk.Label(
            self.info_frame,
            text=f"Skill Points: {self.player.stats.get('skill_points', 0)}",
            font=self._font_bold, bg="#2a2a2a", fg="#FFD700"
        )
        self.sp_label.pack(side="right")

        # Legend
        legend_frame = tk.Frame(self.window, bg=COLOR_BG, padx=10, pady=4)
        legend_frame.pack(fill="x")
        for color, label in [
            (COLOR_LOCKED, "Locked"),
            (COLOR_AVAILABLE, "Available"),
            (COLOR_UNLOCKED, "Unlocked (Passive)"),
            (COLOR_ACTIVE_ABILITY, "Unlocked (Active)"),
        ]:
            tk.Canvas(legend_frame, width=14, height=14, bg=color, highlightthickness=0).pack(side="left", padx=(8, 2))
            tk.Label(legend_frame, text=label, font=self._font_small, bg=COLOR_BG, fg=COLOR_TEXT).pack(side="left", padx=(0, 6))

        # Canvas
        self.canvas = tk.Canvas(
            self.window, bg=COLOR_BG,
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True, padx=6, pady=6)

        # Detail panel at bottom
        self.detail_frame = tk.Frame(self.window, bg="#2a2a2a", padx=10, pady=8)
        self.detail_frame.pack(fill="x")
        self.detail_label = tk.Label(
            self.detail_frame,
            text="Click a skill node for details. Click an available node to unlock it.",
            font=self._font, bg="#2a2a2a", fg="#aaaaaa",
            wraplength=900, justify="left"
        )
        self.detail_label.pack(fill="x")

        # Draw the tree
        self._draw_tree()

        # Bind events
        self.canvas.bind("<Button-1>", self._on_click)
        self.canvas.bind("<Motion>", self._on_hover)

        # Close handler
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)

    def close_window(self):
        """Close the skill tree window."""
        if self.window:
            try:
                self.window.destroy()
            except Exception:
                pass
        self.window = None
        self.canvas = None

    def _draw_tree(self):
        """Draw all nodes and connections on the canvas."""
        if not self.canvas:
            return

        self.canvas.delete("all")
        self.node_items.clear()
        self.node_rects.clear()

        class_id = self.player.stats.get("class", "warrior")
        tree = get_tree_for_class(class_id)
        unlocked = set(get_unlocked_skills(self.player))
        available_ids = {n["id"] for n in get_available_skills(self.player)}

        if not tree:
            self.canvas.create_text(
                400, 300, text="No skill tree available.",
                font=self._font_bold, fill=COLOR_TEXT
            )
            return

        # Calculate positions for each node
        # Group by tier
        tiers = {}
        for node in tree:
            t = node["tier"]
            if t not in tiers:
                tiers[t] = []
            tiers[t].append(node)

        positions = {}  # node_id -> (cx, cy)
        max_tier = max(tiers.keys()) if tiers else 1

        for tier_num, nodes in sorted(tiers.items()):
            x = PADDING + (tier_num - 1) * TIER_SPACING_X
            n_nodes = len(nodes)
            # Center nodes vertically
            total_height = (n_nodes - 1) * NODE_SPACING_Y
            start_y = PADDING + (400 - total_height) / 2

            # Tier label
            self.canvas.create_text(
                x + NODE_WIDTH // 2, PADDING - 20,
                text=f"Tier {tier_num}",
                font=self._font_small, fill=COLOR_TIER_LABEL
            )

            for i, node in enumerate(nodes):
                cx = x + NODE_WIDTH // 2
                cy = start_y + i * NODE_SPACING_Y + NODE_HEIGHT // 2
                positions[node["id"]] = (cx, cy)

        # Draw connections first (so they appear behind nodes)
        for node in tree:
            if node["id"] not in positions:
                continue
            cx, cy = positions[node["id"]]
            for prereq_id in node.get("prerequisites", []):
                if prereq_id in positions:
                    px, py = positions[prereq_id]
                    # Check if both are unlocked
                    both_unlocked = node["id"] in unlocked and prereq_id in unlocked
                    line_color = COLOR_LINE_UNLOCKED if both_unlocked else COLOR_LINE
                    self.canvas.create_line(
                        px + NODE_WIDTH // 2 - 5, py,
                        cx - NODE_WIDTH // 2 + 5, cy,
                        fill=line_color, width=2, arrow=tk.LAST
                    )

        # Draw nodes
        for node in tree:
            if node["id"] not in positions:
                continue
            cx, cy = positions[node["id"]]
            x1 = cx - NODE_WIDTH // 2
            y1 = cy - NODE_HEIGHT // 2
            x2 = cx + NODE_WIDTH // 2
            y2 = cy + NODE_HEIGHT // 2

            # Determine color
            if node["id"] in unlocked:
                if node["type"] == "active":
                    color = COLOR_ACTIVE_ABILITY
                else:
                    color = COLOR_UNLOCKED
            elif node["id"] in available_ids:
                color = COLOR_AVAILABLE
            else:
                color = COLOR_LOCKED

            # Draw rectangle
            rect_id = self.canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=color, outline="#ffffff", width=2,
                tags=("node",)
            )

            # Draw text
            display_name = node["name"]
            if len(display_name) > 14:
                # Split long names
                words = display_name.split()
                if len(words) > 1:
                    mid = len(words) // 2
                    display_name = " ".join(words[:mid]) + "\n" + " ".join(words[mid:])

            text_id = self.canvas.create_text(
                cx, cy - 5,
                text=display_name,
                font=self._font_small, fill=COLOR_TEXT,
                width=NODE_WIDTH - 10, justify="center",
                tags=("node",)
            )

            # Type indicator
            type_text = "A" if node["type"] == "active" else "P"
            cost_text = f"[{type_text}] {node['cost']}SP"
            self.canvas.create_text(
                cx, y2 - 10,
                text=cost_text,
                font=self._font_small, fill="#cccccc",
                tags=("node",)
            )

            # Store mappings
            self.node_items[rect_id] = node["id"]
            self.node_items[text_id] = node["id"]
            self.node_rects[node["id"]] = (rect_id, text_id)

    def _on_click(self, event):
        """Handle click on a skill node."""
        items = self.canvas.find_overlapping(event.x - 2, event.y - 2, event.x + 2, event.y + 2)
        node_id = None
        for item_id in items:
            if item_id in self.node_items:
                node_id = self.node_items[item_id]
                break

        if not node_id:
            return

        class_id = self.player.stats.get("class", "warrior")
        node = get_node_by_id(class_id, node_id)
        if not node:
            return

        unlocked = set(get_unlocked_skills(self.player))

        if node_id in unlocked:
            # Already unlocked — show info
            info = f"[UNLOCKED] {node['name']}\n{node['description']}"
            if node["type"] == "active":
                ab = node.get("ability", {})
                cd = self.player.state.get("cooldowns", {}).get(node_id, 0)
                info += f"\nCooldown: {'Ready!' if cd == 0 else f'{cd} moves'}"
            self.detail_label.config(text=info)
            return

        # Try to unlock
        available_ids = {n["id"] for n in get_available_skills(self.player)}
        if node_id not in available_ids:
            # Show why it's locked
            unmet_prereqs = []
            for prereq_id in node.get("prerequisites", []):
                if prereq_id not in unlocked:
                    prereq_node = get_node_by_id(class_id, prereq_id)
                    unmet_prereqs.append(prereq_node["name"] if prereq_node else prereq_id)
            sp = self.player.stats.get("skill_points", 0)
            info = f"[LOCKED] {node['name']}\n{node['description']}\n"
            if unmet_prereqs:
                info += f"Requires: {', '.join(unmet_prereqs)}\n"
            if sp < node["cost"]:
                info += f"Need {node['cost']} SP (have {sp})"
            self.detail_label.config(text=info)
            return

        # Unlock the skill
        success, msg = unlock_skill(self.player, node_id)
        if success:
            self.detail_label.config(text=f"UNLOCKED: {node['name']}!")
            # Redraw tree
            self._draw_tree()
            # Update SP label
            self.sp_label.config(text=f"Skill Points: {self.player.stats.get('skill_points', 0)}")
            # Show message in main game console
            if self.engine and hasattr(self.engine, 'display_message'):
                self.engine.display_message(msg)
        else:
            self.detail_label.config(text=msg)

    def _on_hover(self, event):
        """Show tooltip on hover."""
        items = self.canvas.find_overlapping(event.x - 2, event.y - 2, event.x + 2, event.y + 2)
        node_id = None
        for item_id in items:
            if item_id in self.node_items:
                node_id = self.node_items[item_id]
                break

        # Remove old tooltip
        if self.tooltip:
            self.canvas.delete(self.tooltip)
            self.canvas.delete(self.tooltip_text)
            self.tooltip = None
            self.tooltip_text = None

        if not node_id:
            return

        class_id = self.player.stats.get("class", "warrior")
        node = get_node_by_id(class_id, node_id)
        if not node:
            return

        # Build tooltip text
        unlocked = set(get_unlocked_skills(self.player))
        status = "UNLOCKED" if node_id in unlocked else "AVAILABLE" if node_id in {n["id"] for n in get_available_skills(self.player)} else "LOCKED"
        tip = f"{node['name']} [{status}]"

        # Draw tooltip
        tx = event.x + 15
        ty = event.y - 15
        self.tooltip_text = self.canvas.create_text(
            tx, ty, text=tip, anchor="nw",
            font=self._font_small, fill=COLOR_TEXT
        )
        bbox = self.canvas.bbox(self.tooltip_text)
        if bbox:
            self.tooltip = self.canvas.create_rectangle(
                bbox[0] - 4, bbox[1] - 2, bbox[2] + 4, bbox[3] + 2,
                fill=COLOR_TOOLTIP_BG, outline="#555555"
            )
            self.canvas.tag_raise(self.tooltip_text)

    def refresh(self):
        """Redraw the tree (e.g., after spending skill points)."""
        if not self.is_open():
            return
        self._draw_tree()
        self.sp_label.config(text=f"Skill Points: {self.player.stats.get('skill_points', 0)}")
