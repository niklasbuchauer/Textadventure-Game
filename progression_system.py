"""
Character Progression System
=============================
Handles XP, leveling, class definitions, and stat growth.
Classes: Warrior, Rogue, Mage — each with unique starting bonuses.
Level range: 1-60, extended pacing with radial skill tree.
"""
import math
# Level 15 = endgame (~3000+ total XP from all sources)
# =====================================================================

# Levels 1-15: original hand-tuned values
# Levels 16-30: +200 XP/level growth
# Levels 31-45: +400 XP/level growth
# Levels 46-60: +600 XP/level growth
_BASE_XP = [
    0,      # Level 1  (start)
    100,    # Level 2
    250,    # Level 3
    450,    # Level 4
    700,    # Level 5
    1000,   # Level 6
    1350,   # Level 7
    1750,   # Level 8
    2200,   # Level 9
    2700,   # Level 10
    3300,   # Level 11
    4000,   # Level 12
    4800,   # Level 13
    5700,   # Level 14
    6800,   # Level 15
]

def _build_xp_table():
    table = list(_BASE_XP)
    last = table[-1]
    for lvl in range(16, 61):
        if lvl <= 30:
            increment = 200 * (lvl - 15) + 800
        elif lvl <= 45:
            increment = 400 * (lvl - 30) + 3800
        else:
            increment = 600 * (lvl - 45) + 9800
        last = last + increment
        table.append(last)
    return table

XP_TABLE = _build_xp_table()

MAX_LEVEL = len(XP_TABLE)

# =====================================================================
# CLASS DEFINITIONS
# =====================================================================
# Each class has:
#   name:           Display name
#   description:    Flavor text + gameplay summary
#   starting_stats: Bonus stats added at character creation
#   stat_focus:     Which stats this class naturally excels at
#   icon:           ASCII icon for the class
# =====================================================================

CLASS_DEFINITIONS = {
    "warrior": {
        "name": "Warrior",
        "description": (
            "A battle-hardened fighter who thrives in the heat of danger.\n"
            "Warriors are tough, strong, and can shrug off blows that would\n"
            "fell lesser adventurers. They specialise in defense and brute force."
        ),
        "starting_stats": {
            "strength": 4,
            "defense": 3,
            "constitution": 3,
            "dexterity": 1,
            "perception": 1,
            "charisma": 0,
        },
        "stat_focus": ["Strength", "Defense", "Constitution"],
        "icon": r"""
   /\
  /  \
 / /\ \
/_/  \_\
 ||  ||
 ||  ||
  \  /
   \/
        """,
    },
    "rogue": {
        "name": "Rogue",
        "description": (
            "A cunning trickster with quick hands and sharper eyes.\n"
            "Rogues excel at spotting traps, picking locks, and finding\n"
            "hidden treasures. They strike with precision, not power."
        ),
        "starting_stats": {
            "strength": 1,
            "defense": 1,
            "constitution": 1,
            "dexterity": 4,
            "perception": 3,
            "charisma": 2,
        },
        "stat_focus": ["Dexterity", "Perception", "Charisma"],
        "icon": r"""
     _
    / \
   | o |
   /| |\
  / | | \
    | |
   / | \
  /  |  \
        """,
    },
    "mage": {
        "name": "Mage",
        "description": (
            "A scholar of the arcane arts, wielding mystical forces.\n"
            "Mages channel magical energy to shield, heal, and reveal\n"
            "what is hidden. Wisdom and willpower are their weapons."
        ),
        "starting_stats": {
            "strength": 0,
            "defense": 1,
            "constitution": 3,
            "dexterity": 1,
            "perception": 3,
            "charisma": 4,
        },
        "stat_focus": ["Constitution", "Perception", "Charisma"],
        "icon": r"""
    /\
   /  \
  / *  \
 /  ||  \
/___||___\
    ||
    ||
   /  \
        """,
    },
}

# =====================================================================
# XP AWARD VALUES — how much XP each gameplay event gives
# =====================================================================

XP_AWARDS = {
    # Traps
    "disarm_trap_easy":         15,
    "disarm_trap_medium":       25,
    "disarm_trap_hard":         35,
    "disarm_trap_very_hard":    50,
    "survive_trap":             5,
    # Chests
    "open_chest_wooden":        10,
    "open_chest_iron":          15,
    "open_chest_ornate":        25,
    # Exploration
    "first_visit_room":         3,
    "discover_secret_room":     50,
    # Crafting
    "craft_basic":              10,
    "craft_advanced":           20,
    "craft_legendary":          30,
    # NPCs
    "complete_dialogue":        10,
    "learn_recipe":             15,
    # Commerce
    "sell_item":                2,
    # Fishing
    "catch_fish":               5,
}

# Skill points awarded per level up — flat 3 SP/level for 200+ node tree
SKILL_POINTS_PER_LEVEL = {level: 3 for level in range(2, 61)}

# Save version for migration (incremented on tree redesign)
SAVE_VERSION = 3


def get_xp_for_next_level(current_level):
    """Return XP threshold for the next level, or None if max level."""
    if current_level >= MAX_LEVEL:
        return None
    return XP_TABLE[current_level]  # index = next level - 1, but since table is 0-indexed by level-1


def get_level_from_xp(total_xp):
    """Determine level from total accumulated XP."""
    level = 1
    for i in range(1, MAX_LEVEL):
        if total_xp >= XP_TABLE[i]:
            level = i + 1
        else:
            break
    return level


def check_level_up(player):
    """
    Check if the player has enough XP to level up.
    Applies level ups (possibly multiple) and awards skill points.

    Args:
        player: Player object with player.stats dict

    Returns:
        list of (new_level, skill_points_earned) tuples for each level gained,
        or empty list if no level up occurred.
    """
    stats = player.stats
    current_level = stats.get("level", 1)
    total_xp = stats.get("xp", 0)
    level_ups = []

    while current_level < MAX_LEVEL:
        xp_needed = XP_TABLE[current_level]  # XP to reach current_level + 1
        if total_xp >= xp_needed:
            current_level += 1
            sp = SKILL_POINTS_PER_LEVEL.get(current_level, 3)
            stats["level"] = current_level
            stats["skill_points"] = stats.get("skill_points", 0) + sp
            # Health growth: +5 base, diminishing past 40
            if current_level <= 40:
                hp_gain = 5
            else:
                hp_gain = max(2, int(5 * math.sqrt(40 / current_level)))
            stats["health_max"] = stats.get("health_max", 100) + hp_gain
            stats["health"] = stats.get("health_max", 100)  # Full heal on level up
            # Mana growth per level
            class_id = stats.get("class", "warrior")
            mana_gain = {"warrior": 5, "rogue": 6, "mage": 10}.get(class_id, 5)
            stats["max_mana"] = stats.get("max_mana", 0) + mana_gain
            stats["mana"] = stats.get("max_mana", 0)  # Full mana restore on level up
            level_ups.append((current_level, sp))
        else:
            break

    # Update xp_to_next for display
    if current_level < MAX_LEVEL:
        stats["xp_to_next"] = XP_TABLE[current_level] - total_xp
    else:
        stats["xp_to_next"] = 0

    return level_ups


def award_xp(player, amount, source="unknown"):
    """
    Award XP to the player and check for level ups.

    Args:
        player: Player object
        amount: XP to add (int)
        source: Description of why XP was earned

    Returns:
        str: Message describing XP gain and any level ups
    """
    if amount <= 0:
        return ""

    # Prestige meta-progression can scale incoming XP.
    mult = float(player.stats.get("prestige_xp_multiplier", 1.0))
    if mult < 1.0:
        mult = 1.0
    amount = int(round(amount * mult))

    stats = player.stats
    old_xp = stats.get("xp", 0)
    stats["xp"] = old_xp + amount

    # Check for level ups
    level_ups = check_level_up(player)

    # Build result message
    result = f"\n  +{amount} XP ({source})"

    feel = "normal"
    try:
        feel = str(player.state.get("game_feel_intensity", "normal") or "normal").strip().lower()
    except Exception:
        feel = "normal"
    if feel not in ("low", "normal", "high"):
        feel = "normal"

    if level_ups:
        for new_level, sp in level_ups:
            class_id2 = stats.get("class", "warrior")
            mg = {"warrior": 5, "rogue": 6, "mage": 10}.get(class_id2, 5)

            if feel == "low":
                result += "\n\n"
                result += f"  LEVEL UP! You reached Level {new_level}.\n"
                result += f"  +{sp} Skill Point{'s' if sp > 1 else ''} | HP/MP fully restored.\n"
                result += f"  Max HP: {stats.get('health_max', 100)} | Max MP: {stats.get('max_mana', 0)} (+{mg})\n"
                result += f"  Total Skill Points: {stats.get('skill_points', 0)}\n"
            elif feel == "high":
                result += "\n\n"
                result += "╔" + "═" * 53 + "╗\n"
                result += "║              ✨✨ LEVEL ASCENSION! ✨✨               ║\n"
                result += "╠" + "═" * 53 + "╣\n"
                result += f"║  You have reached Level {new_level:<2}!{' ' * 28}║\n"
                result += f"║  +{sp} Skill Point{'s' if sp > 1 else ''} earned!{' ' * 29}║\n"
                result += f"║  Max Health increased to {stats.get('health_max', 100):<3}{' ' * 24}║\n"
                result += "║  Health fully restored!                              ║\n"
                result += f"║  Max Mana increased to {stats.get('max_mana', 0):<3} (+{mg}){' ' * 19}║\n"
                result += "║  Mana fully restored!                                ║\n"
                result += "╠" + "═" * 53 + "╣\n"
                result += f"║  Total Skill Points: {stats.get('skill_points', 0):<3}{' ' * 27}║\n"
                result += "║  Power hums through your veins. Press onward.        ║\n"
                result += "║  Tip: use 'skills' to open your skill tree.         ║\n"
                result += "╚" + "═" * 53 + "╝\n"
            else:
                result += "\n\n"
                result += "╔" + "═" * 53 + "╗\n"
                result += "║                 ✨ LEVEL ASCENSION ✨                 ║\n"
                result += "╠" + "═" * 53 + "╣\n"
                result += f"║  You have reached Level {new_level:<2}!{' ' * 28}║\n"
                result += f"║  +{sp} Skill Point{'s' if sp > 1 else ''} earned!{' ' * 29}║\n"
                result += f"║  Max Health increased to {stats.get('health_max', 100):<3}{' ' * 24}║\n"
                result += "║  Health fully restored!                              ║\n"
                result += f"║  Max Mana increased to {stats.get('max_mana', 0):<3} (+{mg}){' ' * 19}║\n"
                result += "║  Mana fully restored!                                ║\n"
                result += "╠" + "═" * 53 + "╣\n"
                result += f"║  Total Skill Points: {stats.get('skill_points', 0):<3}{' ' * 27}║\n"
                result += "║  Tip: use 'skills' to open your skill tree.         ║\n"
                result += "╚" + "═" * 53 + "╝\n"
    else:
        # Show progress to next level
        xp_to_next = stats.get("xp_to_next", 0)
        if xp_to_next > 0:
            result += f"  ({xp_to_next} XP to next level)"

    return result


def apply_class(player, class_id):
    """
    Apply a class to a player, setting starting stats.

    Args:
        player: Player object
        class_id: One of 'warrior', 'rogue', 'mage'
    """
    class_def = CLASS_DEFINITIONS.get(class_id)
    if not class_def:
        return

    stats = player.stats

    # Set class
    stats["class"] = class_id

    # Set progression defaults
    stats["level"] = 1
    stats["xp"] = 0
    stats["xp_to_next"] = XP_TABLE[1] if len(XP_TABLE) > 1 else 0
    stats["skill_points"] = 0

    # Set base RPG stats (all start at 0, class adds bonuses)
    base_stats = ["strength", "defense", "constitution", "dexterity", "perception", "charisma"]
    for stat in base_stats:
        stats[stat] = 0

    # Apply class starting bonuses
    for stat, value in class_def["starting_stats"].items():
        stats[stat] = stats.get(stat, 0) + value

    # Initialize unlocked skills and cooldowns
    if "unlocked_skills" not in player.state:
        player.state["unlocked_skills"] = []
    if "cooldowns" not in player.state:
        player.state["cooldowns"] = {}

    # Set starting mana based on class
    mana_base = {"warrior": 80, "rogue": 90, "mage": 120}.get(class_id, 80)
    stats["mana"] = mana_base
    stats["max_mana"] = mana_base
    stats["mana_regen_bonus"] = 0.0  # extra regen from passives/gear

    # Auto-unlock the tier 0 center node for the chosen class
    center_nodes = {
        "warrior": "w_origin",
        "rogue": "r_origin",
        "mage": "m_origin",
    }
    center = center_nodes.get(class_id)
    if center and center not in player.state["unlocked_skills"]:
        player.state["unlocked_skills"].append(center)


def get_class_selection_text():
    """
    Return the ASCII art class selection screen.

    Returns:
        str: Formatted text for class choice
    """
    result = "\n"
    result += "=" * 60 + "\n"
    result += "          CHOOSE YOUR CLASS\n"
    result += "=" * 60 + "\n\n"
    result += "Your class determines your starting stats and\n"
    result += "which skill tree you can unlock. Choose wisely!\n"
    result += "This choice is permanent for this character.\n\n"
    result += "-" * 60 + "\n"

    for i, (class_id, cls) in enumerate(CLASS_DEFINITIONS.items(), 1):
        result += f"\n  [{i}] {cls['name'].upper()}\n"
        result += cls["icon"].rstrip() + "\n"
        result += f"\n{cls['description']}\n"
        result += f"\n  Starting focus: {', '.join(cls['stat_focus'])}\n"

        # Show starting stats
        result += "  Stats: "
        stat_parts = []
        for stat, val in cls["starting_stats"].items():
            if val > 0:
                stat_parts.append(f"{stat.capitalize()} +{val}")
        result += ", ".join(stat_parts) + "\n"
        result += "-" * 60 + "\n"

    result += "\nType 1, 2, or 3 to choose your class:\n"

    return result


def get_stat_modifier(player, stat_name):
    """
    Get how much a stat modifies gameplay.
    Returns a float modifier (0.0 if stat is 0).

    This is the central function used by other systems to
    query stat influence.
    """
    value = player.stats.get(stat_name, 0)
    return float(value)
