"""
Combat System
=============
Turn-based combat for dungeon encounters.

Enemies spawn in dungeon rooms and engage the player when they enter.
Combat is turn-based: player chooses attack/defend/flee/ability each turn.
Damage uses the player's strength (boosted by weapon) vs enemy defense,
and enemy attack vs player defense (boosted by armor/shield).

The system is designed to be non-blocking — each combat round is a single
command/response cycle using pending_combat state on the engine.
"""

import random

# ═════════════════════════════════════════════════════════════════════
# ENEMY DATABASE
# ═════════════════════════════════════════════════════════════════════
# Enemies are grouped by dungeon theme and floor difficulty.
# Each enemy has: name, hp, attack, defense, xp_reward, gold_reward,
# loot (list of (item, chance)), description, and optional abilities.
# ═════════════════════════════════════════════════════════════════════

ENEMY_DATABASE = {
    # ── CRYSTAL CAVERNS ENEMIES ───────────────────────────────────
    "crystal_beetle": {
        "name": "Crystal Beetle",
        "description": "A large beetle with a shimmering crystalline shell.",
        "hp": 20, "attack": 5, "defense": 1,
        "xp_reward": 15, "gold_reward": (3, 8),
        "loot": [("cave_crystal", 0.30), ("raw_diamond", 0.05)],
        "floor_range": (1, 2),
        "dungeon": "crystal_caverns",
    },
    "crystal_spider": {
        "name": "Crystal Spider",
        "description": "Its legs are translucent crystal. Fast and venomous.",
        "hp": 25, "attack": 7, "defense": 2,
        "xp_reward": 20, "gold_reward": (5, 12),
        "loot": [("cave_crystal", 0.25), ("spider_silk", 0.15)],
        "floor_range": (1, 3),
        "dungeon": "crystal_caverns",
    },
    "crystal_golem": {
        "name": "Crystal Golem",
        "description": "A towering construct of living crystal. Slow but devastating.",
        "hp": 50, "attack": 10, "defense": 5,
        "xp_reward": 40, "gold_reward": (15, 30),
        "loot": [("heart_crystal_fragment", 0.20), ("raw_diamond", 0.10)],
        "floor_range": (2, 3),
        "dungeon": "crystal_caverns",
    },

    # ── IRON HALLS ENEMIES ────────────────────────────────────────
    "rust_rat": {
        "name": "Rust Rat",
        "description": "A dog-sized rat with iron-hard teeth that gnaw through metal.",
        "hp": 18, "attack": 5, "defense": 1,
        "xp_reward": 12, "gold_reward": (2, 6),
        "loot": [("iron_ingot", 0.15), ("old_bone", 0.25)],
        "floor_range": (1, 2),
        "dungeon": "iron_halls",
    },
    "iron_sentinel": {
        "name": "Iron Sentinel",
        "description": "An animated suit of armor. Its eyes glow with ancient fire.",
        "hp": 40, "attack": 9, "defense": 6,
        "xp_reward": 35, "gold_reward": (10, 25),
        "loot": [("iron_ingot", 0.30), ("tempered_steel_ingot", 0.10)],
        "floor_range": (2, 3),
        "dungeon": "iron_halls",
    },
    "forge_elemental": {
        "name": "Forge Elemental",
        "description": "A being of living flame and molten metal.",
        "hp": 45, "attack": 12, "defense": 4,
        "xp_reward": 40, "gold_reward": (15, 35),
        "loot": [("eternal_ember", 0.15), ("raw_mithril", 0.08)],
        "floor_range": (2, 3),
        "dungeon": "iron_halls",
    },

    # ── SHADOW DEPTHS ENEMIES ─────────────────────────────────────
    "shadow_wisp": {
        "name": "Shadow Wisp",
        "description": "A flickering orb of dark energy. Hard to hit.",
        "hp": 15, "attack": 6, "defense": 0,
        "xp_reward": 10, "gold_reward": (1, 5),
        "loot": [("concentrated_void_essence", 0.10)],
        "floor_range": (1, 2),
        "dungeon": "shadow_depths",
    },
    "shadow_stalker": {
        "name": "Shadow Stalker",
        "description": "A humanoid shape of pure darkness. Silent and deadly.",
        "hp": 35, "attack": 10, "defense": 3,
        "xp_reward": 30, "gold_reward": (8, 20),
        "loot": [("umbral_thread", 0.20), ("obsidian_blade_fragment", 0.10)],
        "floor_range": (1, 3),
        "dungeon": "shadow_depths",
    },
    "void_wraith": {
        "name": "Void Wraith",
        "description": "A screaming horror from the space between worlds.",
        "hp": 45, "attack": 13, "defense": 4,
        "xp_reward": 45, "gold_reward": (15, 30),
        "loot": [("void_heart_fragment", 0.15), ("concentrated_void_essence", 0.20)],
        "floor_range": (2, 3),
        "dungeon": "shadow_depths",
    },

    # ── SUNKEN CATACOMBS ENEMIES ──────────────────────────────────
    "skeletal_warrior": {
        "name": "Skeletal Warrior",
        "description": "The animated bones of a fallen soldier, sword in hand.",
        "hp": 22, "attack": 6, "defense": 2,
        "xp_reward": 15, "gold_reward": (3, 10),
        "loot": [("old_bone", 0.35), ("rusty_sword", 0.10)],
        "floor_range": (1, 2),
        "dungeon": "sunken_catacombs",
    },
    "ghoul": {
        "name": "Ghoul",
        "description": "A rotting creature that feeds on the dead. Its claws drip with disease.",
        "hp": 30, "attack": 8, "defense": 2,
        "xp_reward": 25, "gold_reward": (5, 15),
        "loot": [("soul_gem", 0.10), ("old_bone", 0.20)],
        "floor_range": (1, 3),
        "dungeon": "sunken_catacombs",
    },
    "spectral_knight": {
        "name": "Spectral Knight",
        "description": "A ghostly warrior in ethereal plate armor. Its blade passes through shields.",
        "hp": 50, "attack": 12, "defense": 5,
        "xp_reward": 45, "gold_reward": (15, 35),
        "loot": [("cracked_phylactery", 0.12), ("soul_gem", 0.15)],
        "floor_range": (2, 3),
        "dungeon": "sunken_catacombs",
    },

    # ── GENERIC / OVERWORLD ENEMIES (fallback) ────────────────────
    "giant_rat": {
        "name": "Giant Rat",
        "description": "An oversized rat with glowing red eyes.",
        "hp": 12, "attack": 3, "defense": 0,
        "xp_reward": 8, "gold_reward": (1, 4),
        "loot": [],
        "floor_range": (1, 1),
        "dungeon": "any",
    },
    "cave_bat": {
        "name": "Cave Bat",
        "description": "A large bat that swoops aggressively from the darkness.",
        "hp": 10, "attack": 4, "defense": 0,
        "xp_reward": 6, "gold_reward": (1, 3),
        "loot": [],
        "floor_range": (1, 1),
        "dungeon": "any",
    },
}


# ═════════════════════════════════════════════════════════════════════
# BOSS DATABASE
# ═════════════════════════════════════════════════════════════════════
# Bosses appear in boss rooms on the final floor of each dungeon.
# They're significantly stronger and have special abilities.
# ═════════════════════════════════════════════════════════════════════

BOSS_DATABASE = {
    "crystal_titan": {
        "name": "Crystal Titan",
        "description": "A massive golem of pure crystal. Its fists could shatter mountains.",
        "hp": 120, "attack": 15, "defense": 8,
        "xp_reward": 150, "gold_reward": (50, 100),
        "loot": [("heart_crystal_fragment", 0.80), ("raw_diamond", 0.50),
                 ("spectrum_prism", 0.30)],
        "abilities": ["crystal_slam", "regenerate"],
        "dungeon": "crystal_caverns",
        "intro_text": (
            "\n" + "═" * 55 + "\n"
            "  ⚔️  BOSS ENCOUNTER: CRYSTAL TITAN  ⚔️\n"
            "═" * 55 + "\n"
            "  The ground trembles as a colossal figure of living\n"
            "  crystal rises from the floor. Light refracts through\n"
            "  its body in blinding rainbows. It regards you with\n"
            "  eyes like blazing diamonds.\n"
            "═" * 55 + "\n"
        ),
    },
    "iron_forgemaster": {
        "name": "Iron Forgemaster",
        "description": "A dwarven automaton wreathed in flames. Its hammer rings like thunder.",
        "hp": 130, "attack": 17, "defense": 10,
        "xp_reward": 160, "gold_reward": (60, 120),
        "loot": [("eternal_ember", 0.70), ("raw_mithril", 0.40),
                 ("forgemaster_hammer", 0.25)],
        "abilities": ["flame_strike", "fortify"],
        "dungeon": "iron_halls",
        "intro_text": (
            "\n" + "═" * 55 + "\n"
            "  ⚔️  BOSS ENCOUNTER: IRON FORGEMASTER  ⚔️\n"
            "═" * 55 + "\n"
            "  A massive dwarven construct slams its hammer on the\n"
            "  anvil, sending sparks cascading across the chamber.\n"
            "  Molten iron flows through its joints like blood.\n"
            "  It turns to face you with furnace-bright eyes.\n"
            "═" * 55 + "\n"
        ),
    },
    "shadow_sovereign": {
        "name": "Shadow Sovereign",
        "description": "The lord of shadows. Darkness itself given terrible form.",
        "hp": 110, "attack": 18, "defense": 6,
        "xp_reward": 170, "gold_reward": (50, 110),
        "loot": [("sovereign_shadow_crown", 0.60), ("concentrated_void_essence", 0.70),
                 ("void_heart_fragment", 0.40)],
        "abilities": ["shadow_strike", "darkness"],
        "dungeon": "shadow_depths",
        "intro_text": (
            "\n" + "═" * 55 + "\n"
            "  ⚔️  BOSS ENCOUNTER: SHADOW SOVEREIGN  ⚔️\n"
            "═" * 55 + "\n"
            "  The shadows in the room coalesce into a towering\n"
            "  figure wearing a crown of pure darkness. Its voice\n"
            "  echoes from everywhere and nowhere at once:\n"
            '  "You dare enter MY domain?"\n'
            "═" * 55 + "\n"
        ),
    },
    "lich_king": {
        "name": "Lich King",
        "description": "An ancient undead sorcerer. Death magic crackles around his skeletal form.",
        "hp": 140, "attack": 16, "defense": 7,
        "xp_reward": 180, "gold_reward": (70, 130),
        "loot": [("lich_crown_fragment", 0.70), ("soul_gem", 0.60),
                 ("cracked_phylactery", 0.50), ("blood_ruby", 0.30)],
        "abilities": ["death_bolt", "summon_skeleton"],
        "dungeon": "sunken_catacombs",
        "intro_text": (
            "\n" + "═" * 55 + "\n"
            "  ⚔️  BOSS ENCOUNTER: LICH KING  ⚔️\n"
            "═" * 55 + "\n"
            "  A skeletal figure draped in tattered robes rises\n"
            "  from a throne of bones. Green fire burns in its\n"
            "  empty eye sockets. It raises a bony hand and the\n"
            "  temperature plummets.\n"
            '  "Another fool seeks my crown..."\n'
            "═" * 55 + "\n"
        ),
    },
}

# Map dungeon IDs to their boss
DUNGEON_BOSS_MAP = {
    "crystal_caverns": "crystal_titan",
    "iron_halls": "iron_forgemaster",
    "shadow_depths": "shadow_sovereign",
    "sunken_catacombs": "lich_king",
}

# Spawn chances per floor (enemy appears in a room)
ENEMY_SPAWN_CHANCE = {
    1: 0.25,   # 25% of rooms on floor 1
    2: 0.35,   # 35% of rooms on floor 2
    3: 0.40,   # 40% of rooms on floor 3
}


# ═════════════════════════════════════════════════════════════════════
# COMBAT STATE
# ═════════════════════════════════════════════════════════════════════

class CombatState:
    """Tracks the state of an active combat encounter."""

    def __init__(self, enemy_data, is_boss=False):
        self.enemy_id = enemy_data.get("id", "unknown")
        self.enemy_name = enemy_data["name"]
        self.enemy_description = enemy_data["description"]
        self.max_hp = enemy_data["hp"]
        self.hp = enemy_data["hp"]
        self.attack = enemy_data["attack"]
        self.defense = enemy_data["defense"]
        self.xp_reward = enemy_data["xp_reward"]
        self.gold_reward = enemy_data["gold_reward"]
        self.loot = list(enemy_data.get("loot", []))
        self.abilities = list(enemy_data.get("abilities", []))
        self.is_boss = is_boss
        self.intro_text = enemy_data.get("intro_text", "")
        self.turn = 0
        self.player_defending = False
        self.enemy_buff_defense = 0  # temporary defense from boss abilities
        self.player_fled = False

    def to_dict(self):
        """Serialize for save/load."""
        return {
            "enemy_id": self.enemy_id,
            "enemy_name": self.enemy_name,
            "enemy_description": self.enemy_description,
            "max_hp": self.max_hp,
            "hp": self.hp,
            "attack": self.attack,
            "defense": self.defense,
            "xp_reward": self.xp_reward,
            "gold_reward": self.gold_reward,
            "loot": self.loot,
            "abilities": self.abilities,
            "is_boss": self.is_boss,
            "turn": self.turn,
            "player_defending": self.player_defending,
            "enemy_buff_defense": self.enemy_buff_defense,
        }

    @classmethod
    def from_dict(cls, data):
        """Deserialize from save."""
        cs = cls.__new__(cls)
        cs.enemy_id = data.get("enemy_id", "unknown")
        cs.enemy_name = data.get("enemy_name", "Enemy")
        cs.enemy_description = data.get("enemy_description", "")
        cs.max_hp = data.get("max_hp", 30)
        cs.hp = data.get("hp", 30)
        cs.attack = data.get("attack", 5)
        cs.defense = data.get("defense", 2)
        cs.xp_reward = data.get("xp_reward", 10)
        cs.gold_reward = data.get("gold_reward", (5, 15))
        cs.loot = data.get("loot", [])
        cs.abilities = data.get("abilities", [])
        cs.is_boss = data.get("is_boss", False)
        cs.intro_text = ""
        cs.turn = data.get("turn", 0)
        cs.player_defending = data.get("player_defending", False)
        cs.enemy_buff_defense = data.get("enemy_buff_defense", 0)
        cs.player_fled = False
        return cs


# ═════════════════════════════════════════════════════════════════════
# COMBAT LOGIC
# ═════════════════════════════════════════════════════════════════════

def calculate_player_damage(player, combat):
    """
    Calculate damage the player deals to the enemy.
    Strength determines base damage with some randomness.
    """
    strength = player.stats.get("strength", 0)
    base = max(1, strength)
    # Damage range: base ± 25%, minimum 1
    low = max(1, int(base * 0.75))
    high = max(low + 1, int(base * 1.25) + 1)
    raw_damage = random.randint(low, high)

    # Apply enemy defense
    effective_defense = combat.defense + combat.enemy_buff_defense
    reduction = effective_defense * 0.04  # 4% per defense point
    damage = max(1, int(raw_damage * max(0.20, 1 - reduction)))

    return damage


def calculate_enemy_damage(player, combat):
    """
    Calculate damage the enemy deals to the player.
    Uses player's defense stat (which includes equipment bonuses).
    """
    # Enemy base attack with ± 20% variance
    base = combat.attack
    low = max(1, int(base * 0.80))
    high = max(low + 1, int(base * 1.20) + 1)
    raw_damage = random.randint(low, high)

    # Player defense reduces damage
    defense = player.stats.get("defense", 0)
    reduction = defense * 0.03  # 3% per defense point
    damage = max(1, int(raw_damage * max(0.25, 1 - reduction)))

    # Defending halves damage
    if combat.player_defending:
        damage = max(1, damage // 2)

    return damage


def process_player_attack(player, combat):
    """
    Process the player's attack action.

    Returns:
        str: Combat narrative for this round
    """
    combat.turn += 1
    combat.player_defending = False

    # Player attacks
    player_dmg = calculate_player_damage(player, combat)
    combat.hp -= player_dmg

    result = f"\n  ⚔️ You strike the {combat.enemy_name} for {player_dmg} damage!"

    # Check if enemy is dead
    if combat.hp <= 0:
        combat.hp = 0
        return result + "\n"

    # Enemy attacks back
    enemy_dmg = calculate_enemy_damage(player, combat)
    player.stats["health"] = player.stats.get("health", 100) - enemy_dmg
    result += f"\n  🩸 The {combat.enemy_name} hits you for {enemy_dmg} damage!"

    # Boss special ability (every 3 turns)
    boss_msg = _process_boss_ability(player, combat)
    if boss_msg:
        result += boss_msg

    return result + "\n"


def process_player_defend(player, combat):
    """
    Process the player's defend action (halves incoming damage this turn).

    Returns:
        str: Combat narrative for this round
    """
    combat.turn += 1
    combat.player_defending = True

    result = "\n  🛡️ You raise your guard, bracing for the attack!"

    # Enemy attacks (damage halved due to defending)
    enemy_dmg = calculate_enemy_damage(player, combat)
    player.stats["health"] = player.stats.get("health", 100) - enemy_dmg
    result += f"\n  🩸 The {combat.enemy_name} hits you for {enemy_dmg} damage! (reduced)"

    # Small heal from defending (constitution based)
    con = player.stats.get("constitution", 0)
    if con > 0:
        heal = min(con, player.stats.get("health_max", 100) - player.stats.get("health", 0))
        if heal > 0:
            player.stats["health"] = player.stats.get("health", 0) + heal
            result += f"\n  💚 Your fortitude restores {heal} HP!"

    # Boss special ability
    boss_msg = _process_boss_ability(player, combat)
    if boss_msg:
        result += boss_msg

    return result + "\n"


def process_player_flee(player, combat):
    """
    Attempt to flee from combat.
    Dexterity increases flee chance. Cannot flee from bosses.

    Returns:
        (success: bool, message: str)
    """
    combat.turn += 1
    combat.player_defending = False

    if combat.is_boss:
        # Take a hit while failing to flee the boss
        enemy_dmg = calculate_enemy_damage(player, combat)
        player.stats["health"] = player.stats.get("health", 100) - enemy_dmg
        return False, (
            f"\n  🚫 You cannot flee from the {combat.enemy_name}!"
            f"\n  🩸 It strikes you as you turn — {enemy_dmg} damage!\n"
        )

    # Base flee chance: 40% + 5% per dexterity point, capped at 85%
    dex = player.stats.get("dexterity", 0)
    flee_chance = min(0.85, 0.40 + dex * 0.05)

    if random.random() < flee_chance:
        combat.player_fled = True
        return True, "\n  💨 You successfully flee from combat!\n"
    else:
        # Failed flee — enemy gets a free hit
        enemy_dmg = calculate_enemy_damage(player, combat)
        player.stats["health"] = player.stats.get("health", 100) - enemy_dmg
        return False, (
            f"\n  ❌ You fail to escape!"
            f"\n  🩸 The {combat.enemy_name} strikes you — {enemy_dmg} damage!\n"
        )


def get_combat_status(player, combat):
    """Get the current combat status display."""
    # Enemy HP bar
    pct = max(0, combat.hp / combat.max_hp)
    bar_len = 20
    filled = int(pct * bar_len)
    bar = "█" * filled + "░" * (bar_len - filled)

    # Player HP
    php = player.stats.get("health", 0)
    php_max = player.stats.get("health_max", 100)
    ppct = max(0, php / php_max) if php_max > 0 else 0
    pfilled = int(ppct * 15)
    pbar = "█" * pfilled + "░" * (15 - pfilled)

    boss_marker = "  👑 BOSS" if combat.is_boss else ""

    result = "\n" + "-" * 50 + "\n"
    result += f"  {combat.enemy_name}{boss_marker}\n"
    result += f"  HP: [{bar}] {combat.hp}/{combat.max_hp}\n"
    result += f"\n  You\n"
    result += f"  HP: [{pbar}] {php}/{php_max}\n"
    result += "-" * 50 + "\n"
    result += "  Commands: attack | defend | flee"
    # Show ability option if player has active abilities
    if hasattr(player, 'state') and player.state.get("unlocked_skills"):
        result += " | ability <name>"
    result += "\n"
    return result


def generate_victory_result(player, combat):
    """
    Generate the victory message, award XP and loot.

    Returns:
        str: Victory message with all rewards
    """
    result = "\n" + "=" * 55 + "\n"
    if combat.is_boss:
        result += f"  🏆 BOSS DEFEATED: {combat.enemy_name}! 🏆\n"
    else:
        result += f"  ⚔️ VICTORY! {combat.enemy_name} defeated!\n"
    result += "=" * 55 + "\n"

    # Gold reward
    if isinstance(combat.gold_reward, (list, tuple)) and len(combat.gold_reward) == 2:
        gold = random.randint(combat.gold_reward[0], combat.gold_reward[1])
    else:
        gold = int(combat.gold_reward) if combat.gold_reward else 0
    if gold > 0:
        player.stats["gold"] = player.stats.get("gold", 0) + gold
        result += f"  💰 Gold: +{gold}\n"

    # Loot drops
    dropped = []
    for item_id, chance in combat.loot:
        if random.random() < chance:
            player.inventory[item_id] = player.inventory.get(item_id, 0) + 1
            nice = item_id.replace("_", " ")
            dropped.append(nice)
    if dropped:
        result += "  📦 Loot:\n"
        for d in dropped:
            result += f"     • {d}\n"

    result += "=" * 55 + "\n"

    return result


def get_enemies_for_dungeon(dungeon_id, floor_num):
    """
    Get a list of eligible enemy IDs for a dungeon + floor.
    """
    eligible = []
    for eid, edata in ENEMY_DATABASE.items():
        dun = edata.get("dungeon", "any")
        frange = edata.get("floor_range", (1, 3))
        if (dun == dungeon_id or dun == "any") and frange[0] <= floor_num <= frange[1]:
            eligible.append(eid)
    # Always include generics
    for eid, edata in ENEMY_DATABASE.items():
        if edata.get("dungeon") == "any" and eid not in eligible:
            eligible.append(eid)
    return eligible


def get_boss_for_dungeon(dungeon_id):
    """Get the boss data for a dungeon, or None."""
    boss_id = DUNGEON_BOSS_MAP.get(dungeon_id)
    if boss_id and boss_id in BOSS_DATABASE:
        data = dict(BOSS_DATABASE[boss_id])
        data["id"] = boss_id
        return data
    return None


def should_spawn_enemy(floor_num, room_data):
    """
    Decide if an enemy should spawn in a given room.
    No enemies in entrance rooms, altar rooms, or rooms with NPC.
    """
    # Don't spawn in special rooms
    if room_data.get("is_boss_room"):
        return False
    if room_data.get("crafting_altar"):
        return False
    if room_data.get("npcs"):
        return False
    room_id = room_data.get("_room_id", "")
    # Don't put enemies in entrance rooms
    if "entrance" in room_id or "mouth" in room_id:
        return False

    chance = ENEMY_SPAWN_CHANCE.get(floor_num, 0.30)
    return random.random() < chance


def create_enemy_instance(enemy_id):
    """Create a fresh enemy instance from the database."""
    template = ENEMY_DATABASE.get(enemy_id)
    if not template:
        return None
    data = dict(template)
    data["id"] = enemy_id
    return CombatState(data, is_boss=False)


def create_boss_instance(dungeon_id):
    """Create a boss instance for the given dungeon."""
    boss_data = get_boss_for_dungeon(dungeon_id)
    if not boss_data:
        return None
    return CombatState(boss_data, is_boss=True)


def _process_boss_ability(player, combat):
    """Process boss special abilities (triggered every 3 turns)."""
    if not combat.is_boss or not combat.abilities:
        return ""
    if combat.turn % 3 != 0:
        return ""

    ability = random.choice(combat.abilities)
    result = ""

    if ability == "crystal_slam":
        dmg = random.randint(8, 15)
        player.stats["health"] = player.stats.get("health", 100) - dmg
        result = f"\n  💎 The {combat.enemy_name} SLAMS the ground with crystal fists! ({dmg} damage)"
    elif ability == "regenerate":
        heal = random.randint(10, 20)
        combat.hp = min(combat.max_hp, combat.hp + heal)
        result = f"\n  ✨ The {combat.enemy_name} regenerates {heal} HP!"
    elif ability == "flame_strike":
        dmg = random.randint(10, 18)
        player.stats["health"] = player.stats.get("health", 100) - dmg
        result = f"\n  🔥 The {combat.enemy_name} unleashes a FLAME STRIKE! ({dmg} damage)"
    elif ability == "fortify":
        combat.enemy_buff_defense += 2
        result = f"\n  🛡️ The {combat.enemy_name} hardens its defenses! (+2 Defense)"
    elif ability == "shadow_strike":
        dmg = random.randint(12, 20)
        player.stats["health"] = player.stats.get("health", 100) - dmg
        result = f"\n  🌑 The {combat.enemy_name} strikes from the shadows! ({dmg} damage)"
    elif ability == "darkness":
        # Reduce player perception temporarily (affects next detect)
        result = f"\n  🌫️ The {combat.enemy_name} plunges the room into DARKNESS!"
    elif ability == "death_bolt":
        dmg = random.randint(10, 22)
        player.stats["health"] = player.stats.get("health", 100) - dmg
        result = f"\n  💀 The {combat.enemy_name} launches a bolt of death magic! ({dmg} damage)"
    elif ability == "summon_skeleton":
        # Heal the boss slightly (representing reinforcement)
        heal = random.randint(5, 15)
        combat.hp = min(combat.max_hp, combat.hp + heal)
        result = f"\n  💀 The {combat.enemy_name} summons spectral reinforcements! (+{heal} HP)"

    return result
