"""
Achievements System
===================
Track player accomplishments across combat, exploration, skills, and dungeons.
Achievements are checked after significant events and award titles/bonuses.
"""

try:
    from equipment_system import unlock_cosmetic
except Exception:
    unlock_cosmetic = None

from progression_system import add_stat_bonus


# =====================================================================
# ACHIEVEMENT DEFINITIONS
# =====================================================================

ACHIEVEMENTS = {
    # Combat achievements
    "first_blood": {
        "name": "First Blood",
        "description": "Defeat your first enemy.",
        "icon": "⚔️",
        "category": "combat",
        "check": "kills >= 1",
        "reward": {"xp": 25},
    },
    "warrior_proven": {
        "name": "Warrior Proven",
        "description": "Defeat 10 enemies.",
        "icon": "🗡️",
        "category": "combat",
        "check": "kills >= 10",
        "reward": {"xp": 100},
    },
    "slayer": {
        "name": "Slayer",
        "description": "Defeat 50 enemies.",
        "icon": "💀",
        "category": "combat",
        "check": "kills >= 50",
        "reward": {"xp": 500, "attack": 1},
    },
    "boss_hunter": {
        "name": "Boss Hunter",
        "description": "Defeat your first boss.",
        "icon": "👑",
        "category": "combat",
        "check": "bosses_killed >= 1",
        "reward": {"xp": 200},
    },
    "boss_slayer": {
        "name": "Boss Slayer",
        "description": "Defeat 3 different bosses.",
        "icon": "🏆",
        "category": "combat",
        "check": "bosses_killed >= 3",
        "reward": {"xp": 500, "attack": 2, "defense": 1, "cosmetics": ["slayer_crimson"]},
    },
    "mini_boss_crusher": {
        "name": "Mini-Boss Crusher",
        "description": "Defeat 3 mini-bosses.",
        "icon": "⚔️",
        "category": "combat",
        "check": "mini_bosses_killed >= 3",
        "reward": {"xp": 300},
    },
    "survivor": {
        "name": "Survivor",
        "description": "Win a fight with less than 10% HP remaining.",
        "icon": "❤️‍🩹",
        "category": "combat",
        "check": "close_calls >= 1",
        "reward": {"xp": 150, "health_max_bonus": 5},
    },
    "flawless_victory": {
        "name": "Flawless Victory",
        "description": "Win a fight without taking any damage.",
        "icon": "✨",
        "category": "combat",
        "check": "flawless_wins >= 1",
        "reward": {"xp": 200},
    },

    # Exploration achievements
    "explorer": {
        "name": "Explorer",
        "description": "Visit 10 different locations.",
        "icon": "🗺️",
        "category": "exploration",
        "check": "rooms_visited >= 10",
        "reward": {"xp": 75},
    },
    "cartographer": {
        "name": "Cartographer",
        "description": "Visit 30 different locations.",
        "icon": "🧭",
        "category": "exploration",
        "check": "rooms_visited >= 30",
        "reward": {"xp": 300},
    },
    "dungeon_delver": {
        "name": "Dungeon Delver",
        "description": "Complete your first dungeon.",
        "icon": "🏰",
        "category": "exploration",
        "check": "dungeons_completed >= 1",
        "reward": {"xp": 200},
    },
    "dungeon_master": {
        "name": "Dungeon Master",
        "description": "Complete 5 dungeons.",
        "icon": "🏯",
        "category": "exploration",
        "check": "dungeons_completed >= 5",
        "reward": {"xp": 750, "defense": 2, "cosmetics": ["delver_mantle"]},
    },
    "treasure_hunter": {
        "name": "Treasure Hunter",
        "description": "Collect 500 gold total.",
        "icon": "💰",
        "category": "exploration",
        "check": "total_gold >= 500",
        "reward": {"xp": 150},
    },
    "wealthy": {
        "name": "Wealthy",
        "description": "Collect 2000 gold total.",
        "icon": "💎",
        "category": "exploration",
        "check": "total_gold >= 2000",
        "reward": {"xp": 500},
    },

    # Skill achievements
    "first_skill": {
        "name": "First Steps",
        "description": "Unlock your first skill.",
        "icon": "📖",
        "category": "skills",
        "check": "skills_unlocked >= 1",
        "reward": {"xp": 50},
    },
    "skilled": {
        "name": "Skilled",
        "description": "Unlock 10 skills.",
        "icon": "📚",
        "category": "skills",
        "check": "skills_unlocked >= 10",
        "reward": {"xp": 200},
    },
    "mastery": {
        "name": "Mastery",
        "description": "Unlock 25 skills.",
        "icon": "🌟",
        "category": "skills",
        "check": "skills_unlocked >= 25",
        "reward": {"xp": 500, "attack": 1, "defense": 1, "cosmetics": ["astral_thread"]},
    },
    "branch_initiate": {
        "name": "Branch Initiate",
        "description": "Reach Initiate rank in any branch synergy.",
        "icon": "★",
        "category": "skills",
        "check": "max_branch_count >= 3",
        "reward": {"xp": 100},
    },
    "branch_master": {
        "name": "Branch Master",
        "description": "Reach Master rank in any branch synergy.",
        "icon": "🌠",
        "category": "skills",
        "check": "max_branch_count >= 12",
        "reward": {"xp": 1000, "attack": 3, "defense": 2},
    },

    # Level achievements
    "level_5": {
        "name": "Apprentice",
        "description": "Reach level 5.",
        "icon": "⬆️",
        "category": "progression",
        "check": "level >= 5",
        "reward": {"xp": 100},
    },
    "level_10": {
        "name": "Journeyman",
        "description": "Reach level 10.",
        "icon": "⬆️",
        "category": "progression",
        "check": "level >= 10",
        "reward": {"xp": 250},
    },
    "level_20": {
        "name": "Veteran",
        "description": "Reach level 20.",
        "icon": "⬆️",
        "category": "progression",
        "check": "level >= 20",
        "reward": {"xp": 500, "health_max_bonus": 10},
    },
    "level_30": {
        "name": "Champion",
        "description": "Reach level 30.",
        "icon": "👑",
        "category": "progression",
        "check": "level >= 30",
        "reward": {"xp": 1000, "attack": 2, "defense": 2},
    },

    # Quest achievements
    "quest_starter": {
        "name": "Quest Starter",
        "description": "Complete your first quest.",
        "icon": "📜",
        "category": "quests",
        "check": "quests_completed >= 1",
        "reward": {"xp": 50},
    },
    "questmaster": {
        "name": "Questmaster",
        "description": "Complete 10 quests.",
        "icon": "📋",
        "category": "quests",
        "check": "quests_completed >= 10",
        "reward": {"xp": 400, "attack": 1},
    },

    # Elite dungeon achievements
    "elite_challenger": {
        "name": "Elite Challenger",
        "description": "Enter an elite (extreme difficulty) dungeon.",
        "icon": "🔥",
        "category": "exploration",
        "check": "elite_dungeons_entered >= 1",
        "reward": {"xp": 300},
    },
    "elite_conqueror": {
        "name": "Elite Conqueror",
        "description": "Defeat a boss in an elite dungeon.",
        "icon": "🏅",
        "category": "combat",
        "check": "elite_bosses_killed >= 1",
        "reward": {"xp": 1000, "attack": 3, "defense": 3, "health_max_bonus": 15},
    },

    # Hidden content achievements
    "secrets_seeker": {
        "name": "Secrets Seeker",
        "description": "Discover 3 hidden rooms.",
        "icon": "🔍",
        "category": "exploration",
        "check": "secrets_found >= 3",
        "reward": {"xp": 750},
    },
    "secrets_master": {
        "name": "Master of Secrets",
        "description": "Discover all 7 hidden rooms.",
        "icon": "🗝️",
        "category": "exploration",
        "check": "secrets_found >= 7",
        "reward": {"xp": 2000, "attack": 3, "defense": 3, "health_max_bonus": 20},
    },
    "void_titan_slayer": {
        "name": "Void Titan Slayer",
        "description": "Defeat the legendary Void Titan in the secret ritual battle.",
        "icon": "⚡",
        "category": "combat",
        "check": "void_titan_killed >= 1",
        "reward": {"xp": 5000, "attack": 5, "defense": 5, "health_max_bonus": 25, "cosmetics": ["void_crown"]},
    },
    "easter_egg_hunter": {
        "name": "Easter Egg Hunter",
        "description": "Find 5 hidden easter eggs scattered throughout the world.",
        "icon": "🥚",
        "category": "exploration",
        "check": "easter_eggs_found >= 5",
        "reward": {"xp": 1000, "dexterity": 5},
    },
}


# =====================================================================
# ACHIEVEMENT TRACKING
# =====================================================================

def get_achievement_stats(player):
    """Extract achievement-relevant stats from the player object."""
    stats = player.stats
    state = player.state if hasattr(player, 'state') else {}
    ach_tracking = state.get("achievement_tracking", {})

    return {
        "kills": ach_tracking.get("kills", 0),
        "bosses_killed": ach_tracking.get("bosses_killed", 0),
        "mini_bosses_killed": ach_tracking.get("mini_bosses_killed", 0),
        "close_calls": ach_tracking.get("close_calls", 0),
        "flawless_wins": ach_tracking.get("flawless_wins", 0),
        "rooms_visited": len(getattr(player, 'visited_rooms', set())),
        "dungeons_completed": ach_tracking.get("dungeons_completed", 0),
        "total_gold": ach_tracking.get("total_gold", 0),
        "skills_unlocked": len(state.get("unlocked_skills", [])),
        "max_branch_count": _get_max_branch_count(player),
        "level": stats.get("level", 1),
        "quests_completed": ach_tracking.get("quests_completed", 0),
        "elite_dungeons_entered": ach_tracking.get("elite_dungeons_entered", 0),
        "elite_bosses_killed": ach_tracking.get("elite_bosses_killed", 0),
        "secrets_found": ach_tracking.get("secrets_found", 0),
        "easter_eggs_found": ach_tracking.get("easter_eggs_found", 0),
        "void_titan_killed": ach_tracking.get("void_titan_killed", 0),
    }


def _get_max_branch_count(player):
    """Get the maximum number of skills in any single branch."""
    try:
        from skill_tree import get_branch_counts
        counts = get_branch_counts(player)
        return max(counts.values()) if counts else 0
    except Exception:
        return 0


def _evaluate_check(check_str, stats):
    """Evaluate an achievement check string against stats."""
    try:
        # Parse "stat_name >= value" format
        parts = check_str.split()
        if len(parts) == 3:
            stat_name, op, value = parts
            stat_val = stats.get(stat_name, 0)
            target = int(value) if '.' not in value else float(value)
            if op == ">=":
                return stat_val >= target
            elif op == ">":
                return stat_val > target
            elif op == "==":
                return stat_val == target
    except Exception:
        pass
    return False


def check_achievements(player):
    """
    Check all achievements and return newly unlocked ones.
    Returns list of (achievement_id, achievement_data) tuples.
    """
    if not hasattr(player, 'state'):
        player.state = {}
    if "achievements" not in player.state:
        player.state["achievements"] = []
    if "achievement_tracking" not in player.state:
        player.state["achievement_tracking"] = {}
    if "achievement_rewards_granted" not in player.state:
        player.state["achievement_rewards_granted"] = []

    unlocked = set(player.state["achievements"])
    stats = get_achievement_stats(player)
    newly_unlocked = []

    for ach_id, ach_data in ACHIEVEMENTS.items():
        if ach_id in unlocked:
            continue
        if _evaluate_check(ach_data["check"], stats):
            newly_unlocked.append((ach_id, ach_data))
            player.state["achievements"].append(ach_id)
            apply_achievement_reward(player, ach_id, ach_data)

    return newly_unlocked


def track_event(player, event, amount=1):
    """Track an achievement-relevant event."""
    if not hasattr(player, 'state'):
        player.state = {}
    if "achievement_tracking" not in player.state:
        player.state["achievement_tracking"] = {}

    tracking = player.state["achievement_tracking"]
    tracking[event] = tracking.get(event, 0) + amount


def apply_achievement_reward(player, ach_id, ach_data):
    """Apply reward exactly once per achievement unlock."""
    if not hasattr(player, 'state'):
        player.state = {}
    granted = set(player.state.get("achievement_rewards_granted", []))
    if ach_id in granted:
        return False

    reward = ach_data.get("reward", {})
    for stat, val in reward.items():
        if stat == "xp":
            player.stats["xp"] = player.stats.get("xp", 0) + val
        elif stat == "health_max_bonus":
            player.stats["health_max"] = player.stats.get("health_max", 100) + val
            player.stats["health"] = min(
                player.stats.get("health", 100) + val,
                player.stats.get("health_max", 100)
            )
        elif stat == "cosmetics":
            if unlock_cosmetic and isinstance(val, list):
                for cosmetic_id in val:
                    try:
                        unlock_cosmetic(player, cosmetic_id)
                    except Exception:
                        pass
        else:
              add_stat_bonus(player, stat, val)

    granted.add(ach_id)
    player.state["achievement_rewards_granted"] = list(granted)
    return True


def get_achievements_display(player):
    """Generate a formatted display of all achievements."""
    if not hasattr(player, 'state'):
        return "No achievement data."

    unlocked = set(player.state.get("achievements", []))

    result = "\n" + "=" * 55 + "\n"
    result += "  🏆 ACHIEVEMENTS\n"
    result += "=" * 55 + "\n\n"

    categories = {}
    for ach_id, ach_data in ACHIEVEMENTS.items():
        cat = ach_data.get("category", "other")
        categories.setdefault(cat, []).append((ach_id, ach_data))

    total_unlocked = 0
    total = len(ACHIEVEMENTS)

    for cat_name in ["combat", "exploration", "skills", "progression", "quests"]:
        if cat_name not in categories:
            continue
        achs = categories[cat_name]
        cat_unlocked = sum(1 for a_id, _ in achs if a_id in unlocked)
        total_unlocked += cat_unlocked

        result += f"  [{cat_name.upper()}] ({cat_unlocked}/{len(achs)})\n"

        for ach_id, ach_data in achs:
            icon = ach_data.get("icon", "•")
            name = ach_data.get("name", ach_id)
            desc = ach_data.get("description", "")

            if ach_id in unlocked:
                result += f"    ✅ {icon} {name}\n"
                result += f"       {desc}\n"
            else:
                result += f"    ◻️ {icon} {name}\n"
                result += f"       {desc}\n"
        result += "\n"

    result += f"  Progress: {total_unlocked}/{total} unlocked\n"
    result += "=" * 55 + "\n"
    return result


def format_achievement_unlock(ach_id, ach_data):
    """Format an achievement unlock notification."""
    icon = ach_data.get("icon", "🏆")
    name = ach_data.get("name", ach_id)
    desc = ach_data.get("description", "")
    reward = ach_data.get("reward", {})

    result = "\n" + "★" * 40 + "\n"
    result += f"  {icon} ACHIEVEMENT UNLOCKED: {name}\n"
    result += f"  {desc}\n"

    if reward:
        reward_parts = []
        for stat, val in reward.items():
            if stat == "xp":
                reward_parts.append(f"+{val} XP")
            elif stat == "health_max_bonus":
                reward_parts.append(f"+{val} Max HP")
            elif stat == "attack":
                reward_parts.append(f"+{val} Attack")
            elif stat == "defense":
                reward_parts.append(f"+{val} Defense")
            elif stat == "cosmetics":
                if isinstance(val, list):
                    count = len(val)
                    reward_parts.append(f"+{count} cosmetic unlock{'s' if count != 1 else ''}")
            else:
                reward_parts.append(f"+{val} {stat}")
        result += f"  Rewards: {', '.join(reward_parts)}\n"

    result += "★" * 40 + "\n"
    return result
