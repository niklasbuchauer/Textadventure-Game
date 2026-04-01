"""
Combat System
=============
Turn-based combat for dungeon encounters.

Features:
  - 42+ unique enemies across 4 dungeons + 4 mini-bosses + 4 bosses
  - ALL enemies have abilities (not just bosses)
  - Status effects: poison, bleed, burn, stun, freeze
  - Critical hits based on dexterity, perception, and skill bonuses
  - Class-specific attacks (warrior/rogue/mage)
  - Revamped defend: counterattack chance + adrenaline buff
  - Enemy AI: varied actions (attack, ability, heavy attack, defend/heal)
  - Skill tree combat abilities integration
  - Enemy level scaling: enemies scale with dungeon floor depth
"""

import random

from progression_system import add_stat_bonus

try:
    from artifact_system import get_artifact_combat_effects, ARTIFACT_DATABASE
except Exception:
    def get_artifact_combat_effects(_player):
        return {}, None

    ARTIFACT_DATABASE = {}

# =====================================================================
# LEVEL SYSTEM
# =====================================================================

def calculate_enemy_level(floor_num, enemy_type="regular"):
    """
    Calculate enemy level based on dungeon floor and enemy type.
    
    Base levels:
      - Regular enemies: 1-3 (randomized)
      - Mini-bosses: 5
      - Bosses: 8
    
    Floor scaling: +3 levels per floor
      - Floor 1: Regular 1-3, Mini-boss 5, Boss 8
      - Floor 2: Regular 4-6, Mini-boss 8, Boss 11
      - Floor 3: Regular 7-9, Mini-boss 11, Boss 14
    """
    base_level = 1
    if enemy_type == "mini_boss":
        base_level = 5
    elif enemy_type == "boss":
        base_level = 8
    else:  # regular
        base_level = random.randint(1, 3)
    
    # Add floor scaling
    floor_bonus = (floor_num - 1) * 3
    return base_level + floor_bonus


def scale_enemy_stats(base_stats, level, enemy_type="regular", difficulty_modifier=1.0):
    """
    Scale enemy stats based on level and difficulty.
    
    Level 1 = base stats
    Each level adds:
      - HP: +15%
      - Attack: +10%
      - Defense: +8%
      - XP: +20%
      - Gold: +15%
    
    difficulty_modifier: Multiplier for enemy difficulty (0.5 = 50% weaker, 2.0 = 2x stronger)
    
    Returns dict with scaled stats.
    """
    if level <= 1:
        scaled = base_stats.copy()
    else:
        scaled = base_stats.copy()
        level_mult = level - 1  # Level 1 = no bonus
        
        # Scale HP (15% per level)
        if "hp" in scaled:
            scaled["hp"] = int(scaled["hp"] * (1 + 0.15 * level_mult))
        
        # Scale Attack (10% per level)
        if "attack" in scaled:
            scaled["attack"] = int(scaled["attack"] * (1 + 0.10 * level_mult))
        
        # Scale Defense (8% per level)
        if "defense" in scaled:
            scaled["defense"] = int(scaled["defense"] * (1 + 0.08 * level_mult))
        
        # Scale XP (20% per level)
        if "xp_reward" in scaled:
            scaled["xp_reward"] = int(scaled["xp_reward"] * (1 + 0.20 * level_mult))
        
        # Scale Gold (15% per level)
        if "gold_reward" in scaled:
            if isinstance(scaled["gold_reward"], (list, tuple)):
                low, high = scaled["gold_reward"]
                scaled["gold_reward"] = (
                    int(low * (1 + 0.15 * level_mult)),
                    int(high * (1 + 0.15 * level_mult))
                )
            else:
                scaled["gold_reward"] = int(scaled["gold_reward"] * (1 + 0.15 * level_mult))
    
    # Apply difficulty modifier to combat-relevant stats
    if difficulty_modifier != 1.0:
        if "hp" in scaled:
            scaled["hp"] = int(scaled["hp"] * difficulty_modifier)
        if "attack" in scaled:
            scaled["attack"] = int(scaled["attack"] * difficulty_modifier)
        if "defense" in scaled:
            scaled["defense"] = int(scaled["defense"] * difficulty_modifier)
    
    return scaled


def get_level_abilities(abilities, level):
    """
    Some abilities unlock only at higher levels.
    Returns filtered ability list based on enemy level.
    
    For now, all abilities are available at all levels.
    Future enhancement: add level requirements to specific abilities.
    """
    return abilities


# =====================================================================
# STATUS EFFECTS
# =====================================================================

STATUS_EFFECTS = {
    "poison": {
        "name": "Poison",
        "icon": "☠️",
        "type": "dot",           # damage over time
        "message_apply": "is poisoned!",
        "message_tick": "takes {dmg} poison damage!",
        "message_expire": "The poison wears off.",
    },
    "bleed": {
        "name": "Bleed",
        "icon": "🩸",
        "type": "dot",
        "message_apply": "is bleeding!",
        "message_tick": "bleeds for {dmg} damage!",
        "message_expire": "The bleeding stops.",
    },
    "burn": {
        "name": "Burn",
        "icon": "🔥",
        "type": "dot",
        "message_apply": "is burning!",
        "message_tick": "burns for {dmg} damage!",
        "message_expire": "The flames die out.",
    },
    "stun": {
        "name": "Stun",
        "icon": "💫",
        "type": "disable",       # skip turn
        "message_apply": "is stunned!",
        "message_tick": "is still stunned!",
        "message_expire": "shakes off the stun.",
    },
    "freeze": {
        "name": "Freeze",
        "icon": "❄️",
        "type": "debuff",        # reduces attack
        "reduction": 0.30,       # 30% attack reduction
        "message_apply": "is frozen! Attack reduced!",
        "message_tick": "is still frozen!",
        "message_expire": "thaws out.",
    },
}

DAMAGE_TAG_LABELS = {
    "physical": "Physical",
    "poison": "Poison",
    "burn": "Fire",
    "bleed": "Bleed",
    "frost": "Frost",
    "arcane": "Arcane",
}

GAME_FEEL_PROFILES = {
    "low": {
        "momentum_per_hit": 4,
        "momentum_cap": 30,
        "momentum_max_streak": 8,
        "enemy_damage_mult": 0.92,
        "enemy_bar_len": 16,
        "player_bar_len": 12,
        "show_weakness_hints": False,
        "detailed_hotbar": False,
    },
    "normal": {
        "momentum_per_hit": 5,
        "momentum_cap": 50,
        "momentum_max_streak": 10,
        "enemy_damage_mult": 1.0,
        "enemy_bar_len": 20,
        "player_bar_len": 15,
        "show_weakness_hints": True,
        "detailed_hotbar": True,
    },
    "high": {
        "momentum_per_hit": 6,
        "momentum_cap": 70,
        "momentum_max_streak": 12,
        "enemy_damage_mult": 1.08,
        "enemy_bar_len": 24,
        "player_bar_len": 18,
        "show_weakness_hints": True,
        "detailed_hotbar": True,
    },
}


def _normalize_feel_intensity(value):
    """Normalize game feel intensity to one of: low, normal, high."""
    normalized = str(value or "normal").strip().lower()
    if normalized in GAME_FEEL_PROFILES:
        return normalized
    return "normal"


def _get_feel_profile(combat):
    """Get combat feel profile for current encounter."""
    intensity = _normalize_feel_intensity(getattr(combat, "feel_intensity", "normal"))
    return GAME_FEEL_PROFILES[intensity]


# =====================================================================
# ENEMY ABILITY DEFINITIONS
# =====================================================================
# Each ability has: name, type, value(s), description, chance
# Types: damage, status, heal, buff_defense, heavy_attack

ENEMY_ABILITIES = {
    # -- Damage abilities --
    "bite": {"name": "Bite", "type": "damage", "value": (3, 6),
             "text": "bites down hard!"},
    "claw_swipe": {"name": "Claw Swipe", "type": "damage", "value": (4, 8),
                   "text": "swipes with razor claws!"},
    "acid_spit": {"name": "Acid Spit", "type": "damage_status", "value": (3, 5), "status": "poison",
                  "status_dmg": 3, "status_dur": 2, "text": "spits burning acid!"},
    "venom_fang": {"name": "Venom Fang", "type": "damage_status", "value": (2, 4), "status": "poison",
                   "status_dmg": 4, "status_dur": 3, "text": "strikes with venomous fangs!"},
    "fire_breath": {"name": "Fire Breath", "type": "damage_status", "value": (5, 10), "status": "burn",
                    "status_dmg": 3, "status_dur": 2, "text": "breathes fire!"},
    "ice_blast": {"name": "Ice Blast", "type": "status", "status": "freeze",
                  "status_dur": 2, "text": "unleashes a blast of freezing cold!"},
    "tail_slam": {"name": "Tail Slam", "type": "damage_stun", "value": (4, 7),
                  "stun_dur": 1, "text": "slams its massive tail!"},
    "death_gaze": {"name": "Death Gaze", "type": "damage", "value": (6, 12),
                   "text": "fixes you with a death gaze!"},
    "shadow_bolt": {"name": "Shadow Bolt", "type": "damage", "value": (5, 10),
                    "text": "hurls a bolt of shadow energy!"},
    "bone_throw": {"name": "Bone Throw", "type": "damage", "value": (3, 6),
                   "text": "throws a sharpened bone!"},
    "disease_touch": {"name": "Disease Touch", "type": "damage_status", "value": (2, 4), "status": "poison",
                      "status_dmg": 3, "status_dur": 3, "text": "touches you with rotting fingers!"},
    "soul_drain": {"name": "Soul Drain", "type": "damage_heal", "value": (4, 8),
                   "text": "drains your life force!"},
    "crystal_shard": {"name": "Crystal Shard", "type": "damage", "value": (4, 8),
                      "text": "launches razor-sharp crystal shards!"},
    "iron_slam": {"name": "Iron Slam", "type": "damage_stun", "value": (5, 9),
                  "stun_dur": 1, "text": "slams you with an iron fist!"},
    "void_touch": {"name": "Void Touch", "type": "damage_status", "value": (3, 7), "status": "bleed",
                   "status_dmg": 4, "status_dur": 2, "text": "touches you with void energy!"},
    "screech": {"name": "Screech", "type": "status", "status": "stun",
                "status_dur": 1, "text": "lets out an ear-splitting screech!"},
    "web_snare": {"name": "Web Snare", "type": "status", "status": "freeze",
                  "status_dur": 1, "text": "snares you in thick webbing!"},
    "charge": {"name": "Charge", "type": "damage", "value": (6, 10),
               "text": "charges at you with tremendous force!"},
    "drain_life": {"name": "Drain Life", "type": "damage_heal", "value": (5, 10),
                   "text": "drains your life energy!"},
    "corrosion": {"name": "Corrosion", "type": "damage_status", "value": (2, 5), "status": "bleed",
                  "status_dmg": 3, "status_dur": 2, "text": "corrodes your armor!"},
    "flame_slash": {"name": "Flame Slash", "type": "damage_status", "value": (5, 9), "status": "burn",
                    "status_dmg": 4, "status_dur": 2, "text": "strikes with a flaming blade!"},
    "necrotic_blast": {"name": "Necrotic Blast", "type": "damage_status", "value": (6, 12), "status": "poison",
                       "status_dmg": 5, "status_dur": 2, "text": "unleashes necrotic energy!"},
    "petrify_gaze": {"name": "Petrifying Gaze", "type": "damage_stun", "value": (3, 6),
                     "stun_dur": 2, "text": "locks eyes with a petrifying gaze!"},

    # -- Boss abilities --
    "crystal_slam": {"name": "Crystal Slam", "type": "damage", "value": (8, 15),
                     "text": "SLAMS the ground with crystal fists!"},
    "regenerate": {"name": "Regenerate", "type": "heal", "value": (10, 20),
                   "text": "regenerates!"},
    "flame_strike": {"name": "Flame Strike", "type": "damage_status", "value": (10, 18), "status": "burn",
                     "status_dmg": 5, "status_dur": 3, "text": "unleashes a FLAME STRIKE!"},
    "fortify": {"name": "Fortify", "type": "buff_defense", "value": 2,
                "text": "hardens its defenses!"},
    "shadow_strike": {"name": "Shadow Strike", "type": "damage", "value": (12, 20),
                      "text": "strikes from the shadows!"},
    "darkness": {"name": "Darkness", "type": "status", "status": "freeze",
                 "status_dur": 2, "text": "plunges the room into DARKNESS!"},
    "death_bolt": {"name": "Death Bolt", "type": "damage_status", "value": (10, 22), "status": "poison",
                   "status_dmg": 6, "status_dur": 3, "text": "launches a bolt of death magic!"},
    "summon_skeleton": {"name": "Summon Skeleton", "type": "heal", "value": (5, 15),
                        "text": "summons spectral reinforcements!"},

    # -- Mini-boss abilities --
    "crystal_nova": {"name": "Crystal Nova", "type": "damage_stun", "value": (6, 12),
                     "stun_dur": 1, "text": "explodes with crystal energy!"},
    "molten_core": {"name": "Molten Core", "type": "damage_status", "value": (7, 14), "status": "burn",
                    "status_dmg": 5, "status_dur": 3, "text": "erupts with molten metal!"},
    "void_rift": {"name": "Void Rift", "type": "damage_status", "value": (8, 14), "status": "bleed",
                  "status_dmg": 5, "status_dur": 3, "text": "tears open a rift in reality!"},
    "bone_storm": {"name": "Bone Storm", "type": "damage", "value": (8, 16),
                   "text": "summons a storm of flying bones!"},
}


# =====================================================================
# ENEMY DATABASE - 42+ enemies across 4 dungeons
# =====================================================================

ENEMY_DATABASE = {
    # ── CRYSTAL CAVERNS ENEMIES ──────────────────────────────────
    "crystal_beetle": {
        "name": "Crystal Beetle", "description": "A large beetle with a shimmering crystalline shell.",
        "hp": 20, "attack": 5, "defense": 1,
        "xp_reward": 15, "gold_reward": (3, 8),
        "loot": [("cave_crystal", 0.30), ("raw_diamond", 0.05)],
        "floor_range": (1, 2), "dungeon": "crystal_caverns",
        "abilities": ["bite", "crystal_shard"],
    },
    "crystal_spider": {
        "name": "Crystal Spider", "description": "Its legs are translucent crystal. Fast and venomous.",
        "hp": 25, "attack": 7, "defense": 2,
        "xp_reward": 20, "gold_reward": (5, 12),
        "loot": [("cave_crystal", 0.25), ("spider_silk", 0.15)],
        "floor_range": (1, 3), "dungeon": "crystal_caverns",
        "abilities": ["venom_fang", "web_snare"],
    },
    "crystal_golem": {
        "name": "Crystal Golem", "description": "A towering construct of living crystal. Slow but devastating.",
        "hp": 50, "attack": 10, "defense": 5,
        "xp_reward": 40, "gold_reward": (15, 30),
        "loot": [("heart_crystal_fragment", 0.20), ("raw_diamond", 0.10),
                 ("golem_core_amulet", 0.08)],
        "floor_range": (2, 3), "dungeon": "crystal_caverns",
        "abilities": ["crystal_shard", "iron_slam"],
    },
    "gem_wyrm": {
        "name": "Gem Wyrm", "description": "A serpentine creature with scales of living gemstone.",
        "hp": 30, "attack": 8, "defense": 3,
        "xp_reward": 25, "gold_reward": (8, 18),
        "loot": [("cave_crystal", 0.20), ("raw_diamond", 0.08),
                 ("wyrm_scale_boots", 0.05)],
        "floor_range": (1, 2), "dungeon": "crystal_caverns",
        "abilities": ["bite", "tail_slam"],
    },
    "prism_wisp": {
        "name": "Prism Wisp", "description": "A floating orb of refracted light. Blindingly bright.",
        "hp": 15, "attack": 6, "defense": 0,
        "xp_reward": 12, "gold_reward": (2, 7),
        "loot": [("cave_crystal", 0.15), ("wisp_lantern", 0.03)],
        "floor_range": (1, 2), "dungeon": "crystal_caverns",
        "abilities": ["screech", "crystal_shard"],
    },
    "crystal_crawler": {
        "name": "Crystal Crawler", "description": "A hulking insectoid covered in crystal growths.",
        "hp": 35, "attack": 8, "defense": 4,
        "xp_reward": 30, "gold_reward": (10, 22),
        "loot": [("cave_crystal", 0.25), ("heart_crystal_fragment", 0.08)],
        "floor_range": (2, 3), "dungeon": "crystal_caverns",
        "abilities": ["claw_swipe", "crystal_shard", "charge"],
    },
    "geode_guardian": {
        "name": "Geode Guardian", "description": "A humanoid crystal that shatters and reforms endlessly.",
        "hp": 45, "attack": 9, "defense": 6,
        "xp_reward": 35, "gold_reward": (12, 28),
        "loot": [("heart_crystal_fragment", 0.15), ("raw_diamond", 0.12)],
        "floor_range": (2, 3), "dungeon": "crystal_caverns",
        "abilities": ["crystal_shard", "iron_slam", "charge"],
    },

    # ── IRON HALLS ENEMIES ───────────────────────────────────────
    "rust_rat": {
        "name": "Rust Rat", "description": "A dog-sized rat with iron-hard teeth that gnaw through metal.",
        "hp": 18, "attack": 5, "defense": 1,
        "xp_reward": 12, "gold_reward": (2, 6),
        "loot": [("iron_ingot", 0.15), ("old_bone", 0.25)],
        "floor_range": (1, 2), "dungeon": "iron_halls",
        "abilities": ["bite", "corrosion"],
    },
    "iron_sentinel": {
        "name": "Iron Sentinel", "description": "An animated suit of armor. Its eyes glow with ancient fire.",
        "hp": 40, "attack": 9, "defense": 6,
        "xp_reward": 35, "gold_reward": (10, 25),
        "loot": [("iron_ingot", 0.30), ("tempered_steel_ingot", 0.10)],
        "floor_range": (2, 3), "dungeon": "iron_halls",
        "abilities": ["iron_slam", "charge"],
    },
    "forge_elemental": {
        "name": "Forge Elemental", "description": "A being of living flame and molten metal.",
        "hp": 45, "attack": 12, "defense": 4,
        "xp_reward": 40, "gold_reward": (15, 35),
        "loot": [("eternal_ember", 0.15), ("raw_mithril", 0.08),
                 ("ember_gauntlets", 0.05)],
        "floor_range": (2, 3), "dungeon": "iron_halls",
        "abilities": ["fire_breath", "flame_slash"],
    },
    "gear_golem": {
        "name": "Gear Golem", "description": "A construct of interlocking gears and pistons. It clicks menacingly.",
        "hp": 35, "attack": 7, "defense": 5,
        "xp_reward": 28, "gold_reward": (8, 18),
        "loot": [("iron_ingot", 0.20), ("tempered_steel_ingot", 0.05),
                 ("clockwork_ring", 0.04)],
        "floor_range": (1, 2), "dungeon": "iron_halls",
        "abilities": ["iron_slam", "claw_swipe"],
    },
    "slag_hound": {
        "name": "Slag Hound", "description": "A wolf-like creature forged from molten slag. Its bite sears flesh.",
        "hp": 25, "attack": 8, "defense": 2,
        "xp_reward": 20, "gold_reward": (5, 14),
        "loot": [("iron_ingot", 0.10), ("eternal_ember", 0.05)],
        "floor_range": (1, 2), "dungeon": "iron_halls",
        "abilities": ["bite", "fire_breath"],
    },
    "anvil_wraith": {
        "name": "Anvil Wraith", "description": "The ghost of a smith, its hammer still rings with spectral force.",
        "hp": 30, "attack": 9, "defense": 3,
        "xp_reward": 30, "gold_reward": (10, 20),
        "loot": [("tempered_steel_ingot", 0.10), ("iron_ingot", 0.20)],
        "floor_range": (1, 3), "dungeon": "iron_halls",
        "abilities": ["iron_slam", "screech"],
    },
    "molten_crawler": {
        "name": "Molten Crawler", "description": "A centipede-like creature that drips molten metal.",
        "hp": 38, "attack": 10, "defense": 3,
        "xp_reward": 32, "gold_reward": (12, 24),
        "loot": [("eternal_ember", 0.12), ("raw_mithril", 0.06)],
        "floor_range": (2, 3), "dungeon": "iron_halls",
        "abilities": ["fire_breath", "acid_spit", "bite"],
    },

    # ── SHADOW DEPTHS ENEMIES ────────────────────────────────────
    "shadow_wisp": {
        "name": "Shadow Wisp", "description": "A flickering orb of dark energy. Hard to hit.",
        "hp": 15, "attack": 6, "defense": 0,
        "xp_reward": 10, "gold_reward": (1, 5),
        "loot": [("concentrated_void_essence", 0.10)],
        "floor_range": (1, 2), "dungeon": "shadow_depths",
        "abilities": ["shadow_bolt", "screech"],
    },
    "shadow_stalker": {
        "name": "Shadow Stalker", "description": "A humanoid shape of pure darkness. Silent and deadly.",
        "hp": 35, "attack": 10, "defense": 3,
        "xp_reward": 30, "gold_reward": (8, 20),
        "loot": [("umbral_thread", 0.20), ("obsidian_blade_fragment", 0.10),
                 ("stalkers_hood", 0.04)],
        "floor_range": (1, 3), "dungeon": "shadow_depths",
        "abilities": ["shadow_bolt", "claw_swipe", "void_touch"],
    },
    "void_wraith": {
        "name": "Void Wraith", "description": "A screaming horror from the space between worlds.",
        "hp": 45, "attack": 13, "defense": 4,
        "xp_reward": 45, "gold_reward": (15, 30),
        "loot": [("void_heart_fragment", 0.15), ("concentrated_void_essence", 0.20),
                 ("wraith_touch_gloves", 0.04)],
        "floor_range": (2, 3), "dungeon": "shadow_depths",
        "abilities": ["void_touch", "death_gaze", "drain_life"],
    },
    "nightmare": {
        "name": "Nightmare", "description": "A horse-like creature of pure shadow. Its hooves crack the floor.",
        "hp": 40, "attack": 11, "defense": 3,
        "xp_reward": 35, "gold_reward": (10, 22),
        "loot": [("umbral_thread", 0.15), ("concentrated_void_essence", 0.12),
                 ("nightmare_cloak", 0.04), ("nightmare_scythe", 0.02)],
        "floor_range": (2, 3), "dungeon": "shadow_depths",
        "abilities": ["charge", "shadow_bolt", "screech"],
    },
    "gloom_bat": {
        "name": "Gloom Bat", "description": "A bat with wings of living darkness. Its screech unravels sanity.",
        "hp": 18, "attack": 7, "defense": 1,
        "xp_reward": 14, "gold_reward": (3, 8),
        "loot": [("concentrated_void_essence", 0.08)],
        "floor_range": (1, 2), "dungeon": "shadow_depths",
        "abilities": ["bite", "screech"],
    },
    "shade_weaver": {
        "name": "Shade Weaver", "description": "A spider-like entity that webs corridors with shadow threads.",
        "hp": 28, "attack": 8, "defense": 2,
        "xp_reward": 22, "gold_reward": (5, 14),
        "loot": [("umbral_thread", 0.25), ("concentrated_void_essence", 0.10)],
        "floor_range": (1, 3), "dungeon": "shadow_depths",
        "abilities": ["web_snare", "venom_fang", "shadow_bolt"],
    },
    "dark_elemental": {
        "name": "Dark Elemental", "description": "Pure darkness given terrible form. Light dies in its presence.",
        "hp": 42, "attack": 12, "defense": 4,
        "xp_reward": 40, "gold_reward": (14, 28),
        "loot": [("void_heart_fragment", 0.10), ("concentrated_void_essence", 0.18)],
        "floor_range": (2, 3), "dungeon": "shadow_depths",
        "abilities": ["shadow_bolt", "void_touch", "death_gaze"],
    },

    # ── SUNKEN CATACOMBS ENEMIES ─────────────────────────────────
    "skeletal_warrior": {
        "name": "Skeletal Warrior", "description": "The animated bones of a fallen soldier, sword in hand.",
        "hp": 22, "attack": 6, "defense": 2,
        "xp_reward": 15, "gold_reward": (3, 10),
        "loot": [("old_bone", 0.35), ("rusty_sword", 0.10)],
        "floor_range": (1, 2), "dungeon": "sunken_catacombs",
        "abilities": ["bone_throw", "claw_swipe"],
    },
    "ghoul": {
        "name": "Ghoul", "description": "A rotting creature that feeds on the dead. Its claws drip with disease.",
        "hp": 30, "attack": 8, "defense": 2,
        "xp_reward": 25, "gold_reward": (5, 15),
        "loot": [("soul_gem", 0.10), ("old_bone", 0.20)],
        "floor_range": (1, 3), "dungeon": "sunken_catacombs",
        "abilities": ["disease_touch", "claw_swipe", "bite"],
    },
    "spectral_knight": {
        "name": "Spectral Knight", "description": "A ghostly warrior in ethereal plate armor.",
        "hp": 50, "attack": 12, "defense": 5,
        "xp_reward": 45, "gold_reward": (15, 35),
        "loot": [("cracked_phylactery", 0.12), ("soul_gem", 0.15),
                 ("spectral_blade", 0.04)],
        "floor_range": (2, 3), "dungeon": "sunken_catacombs",
        "abilities": ["shadow_bolt", "charge", "death_gaze"],
    },
    "bone_crawler": {
        "name": "Bone Crawler", "description": "A horrifying spider made of fused bones.",
        "hp": 24, "attack": 7, "defense": 3,
        "xp_reward": 18, "gold_reward": (4, 12),
        "loot": [("old_bone", 0.30), ("soul_gem", 0.05)],
        "floor_range": (1, 2), "dungeon": "sunken_catacombs",
        "abilities": ["bone_throw", "web_snare"],
    },
    "plague_zombie": {
        "name": "Plague Zombie", "description": "A shambling corpse oozing with disease. Don't let it touch you.",
        "hp": 28, "attack": 6, "defense": 1,
        "xp_reward": 16, "gold_reward": (2, 8),
        "loot": [("old_bone", 0.20)],
        "floor_range": (1, 2), "dungeon": "sunken_catacombs",
        "abilities": ["disease_touch", "bite"],
    },
    "tomb_scarab": {
        "name": "Tomb Scarab", "description": "A massive beetle that burrows through bone and stone alike.",
        "hp": 20, "attack": 7, "defense": 4,
        "xp_reward": 15, "gold_reward": (3, 9),
        "loot": [("old_bone", 0.15)],
        "floor_range": (1, 2), "dungeon": "sunken_catacombs",
        "abilities": ["bite", "acid_spit"],
    },
    "wraith": {
        "name": "Wraith", "description": "An angry spirit that drains the warmth from your soul.",
        "hp": 32, "attack": 9, "defense": 2,
        "xp_reward": 28, "gold_reward": (6, 16),
        "loot": [("soul_gem", 0.12), ("cracked_phylactery", 0.06)],
        "floor_range": (1, 3), "dungeon": "sunken_catacombs",
        "abilities": ["soul_drain", "screech", "shadow_bolt"],
    },
    "death_knight": {
        "name": "Death Knight", "description": "A heavily armored skeleton warrior radiating dark energy.",
        "hp": 48, "attack": 11, "defense": 5,
        "xp_reward": 42, "gold_reward": (14, 30),
        "loot": [("cracked_phylactery", 0.15), ("soul_gem", 0.20),
                 ("death_knight_blade", 0.03)],
        "floor_range": (2, 3), "dungeon": "sunken_catacombs",
        "abilities": ["necrotic_blast", "charge", "bone_throw"],
    },

    # ── GENERIC / OVERWORLD ENEMIES ──────────────────────────────
    "giant_rat": {
        "name": "Giant Rat", "description": "An oversized rat with glowing red eyes.",
        "hp": 12, "attack": 3, "defense": 0,
        "xp_reward": 8, "gold_reward": (1, 4),
        "loot": [],
        "floor_range": (1, 1), "dungeon": "any",
        "abilities": ["bite"],
    },
    "cave_bat": {
        "name": "Cave Bat", "description": "A large bat that swoops aggressively from the darkness.",
        "hp": 10, "attack": 4, "defense": 0,
        "xp_reward": 6, "gold_reward": (1, 3),
        "loot": [],
        "floor_range": (1, 1), "dungeon": "any",
        "abilities": ["screech", "bite"],
    },
    "dungeon_spider": {
        "name": "Dungeon Spider", "description": "A huge spider with dripping fangs.",
        "hp": 16, "attack": 5, "defense": 1,
        "xp_reward": 10, "gold_reward": (2, 5),
        "loot": [("spider_silk", 0.15)],
        "floor_range": (1, 2), "dungeon": "any",
        "abilities": ["venom_fang", "web_snare"],
    },
    "tunnel_snake": {
        "name": "Tunnel Snake", "description": "A thick-bodied serpent that lurks in crevices.",
        "hp": 14, "attack": 5, "defense": 1,
        "xp_reward": 9, "gold_reward": (1, 4),
        "loot": [],
        "floor_range": (1, 1), "dungeon": "any",
        "abilities": ["bite", "venom_fang"],
    },
    "moss_troll": {
        "name": "Moss Troll", "description": "A hulking green-skinned troll overgrown with moss.",
        "hp": 55, "attack": 10, "defense": 3,
        "xp_reward": 38, "gold_reward": (10, 22),
        "loot": [("trollhide_belt", 0.06)],
        "floor_range": (2, 3), "dungeon": "any",
        "abilities": ["claw_swipe", "charge", "bite"],
    },
    "mimic": {
        "name": "Mimic", "description": "It looked like a treasure chest. It was NOT a treasure chest.",
        "hp": 30, "attack": 9, "defense": 4,
        "xp_reward": 35, "gold_reward": (15, 30),
        "loot": [("raw_diamond", 0.10), ("mimic_tooth_dagger", 0.05)],
        "floor_range": (1, 3), "dungeon": "any",
        "abilities": ["bite", "acid_spit", "claw_swipe"],
    },
}


# =====================================================================
# MINI-BOSS DATABASE - 1 per dungeon (floor 2)
# =====================================================================

MINI_BOSS_DATABASE = {
    "crystal_matriarch": {
        "name": "Crystal Matriarch",
        "description": "An ancient crystal spider of immense size. Smaller spiders skitter around her.",
        "hp": 75, "attack": 12, "defense": 5,
        "xp_reward": 80, "gold_reward": (30, 60),
        "loot": [("heart_crystal_fragment", 0.50), ("raw_diamond", 0.30),
                 # Mini-boss equipment drops
                 ("spidersilk_gloves", 0.20), ("matriarch_eye_amulet", 0.15)],
        "abilities": ["crystal_nova", "venom_fang", "web_snare", "crystal_shard"],
        "dungeon": "crystal_caverns",
        "intro_text": (
            "\n" + "=" * 55 + "\n"
            "  MINI-BOSS: CRYSTAL MATRIARCH\n"
            "=" * 55 + "\n"
            "  A massive spider of living crystal descends from the\n"
            "  ceiling, her body refracting light into deadly beams.\n"
            "  Smaller crystal spiders skitter around her legs.\n"
            "=" * 55 + "\n"
        ),
    },
    "iron_warden": {
        "name": "Iron Warden",
        "description": "A colossal automaton built to guard the inner halls. Steam hisses from its joints.",
        "hp": 80, "attack": 13, "defense": 8,
        "xp_reward": 85, "gold_reward": (35, 65),
        "loot": [("tempered_steel_ingot", 0.50), ("raw_mithril", 0.25),
                 # Mini-boss equipment drops
                 ("warden_core_shield", 0.18), ("warden_plating", 0.15),
                 ("overclock_gear_ring", 0.12)],
        "abilities": ["molten_core", "iron_slam", "charge", "fire_breath"],
        "dungeon": "iron_halls",
        "intro_text": (
            "\n" + "=" * 55 + "\n"
            "  MINI-BOSS: IRON WARDEN\n"
            "=" * 55 + "\n"
            "  A massive automaton rises from its station, gears\n"
            "  grinding with terrible purpose. Steam erupts from\n"
            "  its joints as its furnace-heart glows red hot.\n"
            "=" * 55 + "\n"
        ),
    },
    "void_weaver": {
        "name": "Void Weaver",
        "description": "A creature that exists partially in another dimension. Reality warps around it.",
        "hp": 70, "attack": 14, "defense": 4,
        "xp_reward": 90, "gold_reward": (30, 55),
        "loot": [("void_heart_fragment", 0.40), ("concentrated_void_essence", 0.50),
                 # Mini-boss equipment drops
                 ("phase_shift_boots", 0.18), ("weaver_cowl", 0.15)],
        "abilities": ["void_rift", "shadow_bolt", "void_touch", "death_gaze"],
        "dungeon": "shadow_depths",
        "intro_text": (
            "\n" + "=" * 55 + "\n"
            "  MINI-BOSS: VOID WEAVER\n"
            "=" * 55 + "\n"
            "  Reality cracks and fractures as a creature phase-shifts\n"
            "  into existence. It exists in multiple dimensions at once,\n"
            "  its form flickering between states of being.\n"
            "=" * 55 + "\n"
        ),
    },
    "bone_colossus": {
        "name": "Bone Colossus",
        "description": "Hundreds of skeletons fused into a towering horror. It never stops growing.",
        "hp": 85, "attack": 12, "defense": 6,
        "xp_reward": 85, "gold_reward": (35, 60),
        "loot": [("soul_gem", 0.50), ("cracked_phylactery", 0.35),
                 # Mini-boss equipment drops
                 ("colossus_ribcage_plate", 0.18), ("bonewrought_helm", 0.15)],
        "abilities": ["bone_storm", "necrotic_blast", "disease_touch", "bone_throw"],
        "dungeon": "sunken_catacombs",
        "intro_text": (
            "\n" + "=" * 55 + "\n"
            "  MINI-BOSS: BONE COLOSSUS\n"
            "=" * 55 + "\n"
            "  The bones in the walls begin to move. Hundreds of\n"
            "  skeletons rip free and fuse together into a towering\n"
            "  monstrosity that fills the chamber. It roars with\n"
            "  the voices of the dead.\n"
            "=" * 55 + "\n"
        ),
    },
}

# Map dungeon IDs to their mini-boss
DUNGEON_MINI_BOSS_MAP = {
    "crystal_caverns": "crystal_matriarch",
    "iron_halls": "iron_warden",
    "shadow_depths": "void_weaver",
    "sunken_catacombs": "bone_colossus",
}


# =====================================================================
# BOSS DATABASE
# =====================================================================

BOSS_DATABASE = {
    "crystal_titan": {
        "name": "Crystal Titan",
        "description": "A massive golem of pure crystal. Its fists could shatter mountains.",
        "hp": 120, "attack": 15, "defense": 8,
        "xp_reward": 150, "gold_reward": (50, 100),
        "loot": [("heart_crystal_fragment", 0.80), ("raw_diamond", 0.50),
                 ("spectrum_prism", 0.30),
                 # Mythic equipment drops
                 ("titans_crystalline_edge", 0.12), ("titans_carapace", 0.08),
                 ("titans_grasp", 0.15), ("prismatic_crown", 0.10),
                 ("heart_of_the_titan", 0.15), ("titan_treads", 0.12)],
        "abilities": ["crystal_slam", "regenerate", "crystal_shard", "iron_slam"],
        "dungeon": "crystal_caverns",
        "intro_text": (
            "\n" + "=" * 55 + "\n"
            + "  BOSS ENCOUNTER: CRYSTAL TITAN\n"
            + "=" * 55 + "\n"
            + "  The ground trembles as a colossal figure of living\n"
            + "  crystal rises from the floor. Light refracts through\n"
            + "  its body in blinding rainbows. It regards you with\n"
            + "  eyes like blazing diamonds.\n"
            + "=" * 55 + "\n"
        ),
    },
    "iron_forgemaster": {
        "name": "Iron Forgemaster",
        "description": "A dwarven automaton wreathed in flames. Its hammer rings like thunder.",
        "hp": 130, "attack": 17, "defense": 10,
        "xp_reward": 160, "gold_reward": (60, 120),
        "loot": [("eternal_ember", 0.70), ("raw_mithril", 0.40),
                 ("forgemaster_hammer", 0.25),
                 # Mythic equipment drops
                 ("forgemasters_warhammer", 0.12), ("forgemasters_plate", 0.08),
                 ("forgemasters_helm", 0.10), ("molten_gauntlets", 0.15),
                 ("ironclad_greaves", 0.15), ("eternal_anvil_shield", 0.12),
                 ("eternal_ember_core", 0.10)],
        "abilities": ["flame_strike", "fortify", "iron_slam", "fire_breath"],
        "dungeon": "iron_halls",
        "intro_text": (
            "\n" + "=" * 55 + "\n"
            + "  BOSS ENCOUNTER: IRON FORGEMASTER\n"
            + "=" * 55 + "\n"
            + "  A massive dwarven construct slams its hammer on the\n"
            + "  anvil, sending sparks cascading across the chamber.\n"
            + "  Molten iron flows through its joints like blood.\n"
            + "  It turns to face you with furnace-bright eyes.\n"
            + "=" * 55 + "\n"
        ),
    },
    "shadow_sovereign": {
        "name": "Shadow Sovereign",
        "description": "The lord of shadows. Darkness itself given terrible form.",
        "hp": 110, "attack": 18, "defense": 6,
        "xp_reward": 170, "gold_reward": (50, 110),
        "loot": [("sovereign_shadow_crown", 0.60), ("concentrated_void_essence", 0.70),
                 ("void_heart_fragment", 0.40),
                 # Mythic equipment drops
                 ("sovereigns_edge", 0.12), ("cloak_of_eternal_night", 0.10),
                 ("shadow_walker_treads", 0.15), ("void_crown", 0.12),
                 ("void_grasp", 0.14), ("sovereigns_sigil", 0.08)],
        "abilities": ["shadow_strike", "darkness", "void_touch", "drain_life"],
        "dungeon": "shadow_depths",
        "intro_text": (
            "\n" + "=" * 55 + "\n"
            + "  BOSS ENCOUNTER: SHADOW SOVEREIGN\n"
            + "=" * 55 + "\n"
            + "  The shadows in the room coalesce into a towering\n"
            + "  figure wearing a crown of pure darkness. Its voice\n"
            + "  echoes from everywhere and nowhere at once:\n"
            + '  "You dare enter MY domain?"\n'
            + "=" * 55 + "\n"
        ),
    },
    "lich_king": {
        "name": "Lich King",
        "description": "An ancient undead sorcerer. Death magic crackles around his skeletal form.",
        "hp": 140, "attack": 16, "defense": 7,
        "xp_reward": 180, "gold_reward": (70, 130),
        "loot": [("lich_crown_fragment", 0.70), ("soul_gem", 0.60),
                 ("cracked_phylactery", 0.50), ("blood_ruby", 0.30),
                 # Mythic equipment drops
                 ("lich_king_soul_blade", 0.12), ("deathshroud_robes", 0.12),
                 ("crown_of_the_lich_king", 0.10), ("bonelord_gauntlets", 0.15),
                 ("lichbone_greaves", 0.14), ("phylactery_shard", 0.06)],
        "abilities": ["death_bolt", "summon_skeleton", "necrotic_blast", "petrify_gaze"],
        "dungeon": "sunken_catacombs",
        "intro_text": (
            "\n" + "=" * 55 + "\n"
            + "  BOSS ENCOUNTER: LICH KING\n"
            + "=" * 55 + "\n"
            + "  A skeletal figure draped in tattered robes rises\n"
            + "  from a throne of bones. Green fire burns in its\n"
            + "  empty eye sockets. It raises a bony hand and the\n"
            + "  temperature plummets.\n"
            + '  "Another fool seeks my crown..."\n'
            + "=" * 55 + "\n"
        ),
    },
}

DUNGEON_BOSS_MAP = {
    "crystal_caverns": "crystal_titan",
    "iron_halls": "iron_forgemaster",
    "shadow_depths": "shadow_sovereign",
    "sunken_catacombs": "lich_king",
    "frozen_spire": "frost_sovereign",
    "verdant_labyrinth": "verdant_guardian",
}

# Targeted boss rewards layered on top of regular combat loot.
BOSS_LOOT_TABLES = {
    "crystal_titan": {
        "guaranteed": ["heart_crystal_fragment"],
        "rare": [("titans_crystalline_edge", 0.20), ("prismatic_crown", 0.18)],
    },
    "iron_forgemaster": {
        "guaranteed": ["eternal_ember"],
        "rare": [("forgemasters_warhammer", 0.20), ("eternal_anvil_shield", 0.18)],
    },
    "shadow_sovereign": {
        "guaranteed": ["concentrated_void_essence"],
        "rare": [("sovereigns_edge", 0.20), ("void_crown", 0.18)],
    },
    "lich_king": {
        "guaranteed": ["soul_gem"],
        "rare": [("lich_king_soul_blade", 0.20), ("crown_of_the_lich_king", 0.18)],
    },
    "frost_sovereign": {
        "guaranteed": ["eternal_frost_essence"],
        "rare": [("frostbite_mythic", 0.16), ("frost_sovereign_crown", 0.14)],
    },
    "verdant_guardian": {
        "guaranteed": ["guardian_heartwood"],
        "rare": [("verdant_wrath", 0.16), ("worldtree_crown", 0.14)],
    },
}

MINI_BOSS_LOOT_TABLES = {
    "crystal_matriarch": {
        "guaranteed": ["heart_crystal_fragment"],
        "rare": [("spidersilk_gloves", 0.18), ("matriarch_eye_amulet", 0.16)],
    },
    "iron_warden": {
        "guaranteed": ["tempered_steel_ingot"],
        "rare": [("warden_core_shield", 0.18), ("overclock_gear_ring", 0.14)],
    },
    "void_weaver": {
        "guaranteed": ["concentrated_void_essence"],
        "rare": [("phase_shift_boots", 0.18), ("weaver_cowl", 0.16)],
    },
    "bone_colossus": {
        "guaranteed": ["soul_gem"],
        "rare": [("colossus_ribcage_plate", 0.18), ("bonewrought_helm", 0.16)],
    },
}


def roll_elite_table_drops(player, combat):
    """Apply guaranteed + rare drops for bosses and mini-bosses."""
    enemy_id = getattr(combat, "enemy_id", "")
    table = None
    if getattr(combat, "is_boss", False):
        table = BOSS_LOOT_TABLES.get(enemy_id)
    elif getattr(combat, "is_mini_boss", False):
        table = MINI_BOSS_LOOT_TABLES.get(enemy_id)

    if not table:
        return []

    dropped = []
    for item_id in table.get("guaranteed", []):
        player.inventory[item_id] = player.inventory.get(item_id, 0) + 1
        dropped.append(item_id)

    utility_fx = player.state.get("active_set_utility_effects", {}) if hasattr(player, "state") else {}
    extra_roll_chance = float(utility_fx.get("extra_rare_roll_chance", 0.0))

    rare_hit = False
    for item_id, chance in table.get("rare", []):
        if random.random() < float(chance):
            player.inventory[item_id] = player.inventory.get(item_id, 0) + 1
            dropped.append(item_id)
            rare_hit = True
            break

    # Set utility: one extra rare roll attempt if the first rare roll misses.
    if not rare_hit and extra_roll_chance > 0 and random.random() < extra_roll_chance:
        for item_id, chance in table.get("rare", []):
            if random.random() < float(chance):
                player.inventory[item_id] = player.inventory.get(item_id, 0) + 1
                dropped.append(item_id)
                break

    return dropped

# Elite dungeon bosses
BOSS_DATABASE["frost_sovereign"] = {
    "name": "Frost Sovereign",
    "description": "An ancient being of pure cold, enthroned on living ice.",
    "hp": 200, "attack": 22, "defense": 14,
    "xp_reward": 350, "gold_reward": (150, 350),
    "loot": [("sovereign_crown", 0.90), ("eternal_frost_essence", 0.70),
             ("frost_wyrm_scale", 0.50), ("void_ice", 0.30),
             # Mythic equipment drops
             ("frostbite_mythic", 0.10), ("glacial_sovereign_plate", 0.08),
             ("frost_sovereign_crown", 0.10), ("glacial_striders", 0.12),
             ("permafrost_gauntlets", 0.14), ("frozen_heart_mythic", 0.08)],
    "abilities": ["frost_nova", "ice_armor", "crystal_shard", "drain_life"],
    "dungeon": "frozen_spire",
    "intro_text": (
        "\n" + "=" * 55 + "\n"
        + "  👑 BOSS ENCOUNTER: FROST SOVEREIGN 👑\n"
        + "=" * 55 + "\n"
        + "  Upon a throne of living ice sits a being of terrible\n"
        + "  beauty. Its skin is translucent crystal, and its eyes\n"
        + "  burn with the cold light of dying stars. The temperature\n"
        + "  plummets as it rises, and the very air freezes.\n"
        + '  "You have come far... but winter is eternal."\n'
        + "=" * 55 + "\n"
    ),
}

BOSS_DATABASE["verdant_guardian"] = {
    "name": "Verdant Guardian",
    "description": "An ancient treant fused with the World Tree. Nature given terrible form.",
    "hp": 220, "attack": 20, "defense": 16,
    "xp_reward": 380, "gold_reward": (180, 400),
    "loot": [("guardian_heartwood", 0.90), ("world_tree_bark", 0.70),
             ("creation_seed_shard", 0.50), ("eden_flower", 0.40),
             # Mythic equipment drops
             ("verdant_wrath", 0.10), ("worldtree_bark_plate", 0.08),
             ("worldtree_crown", 0.10), ("rootwarden_greaves", 0.12),
             ("rootwarden_grips", 0.14), ("heart_of_the_forest", 0.08)],
    "abilities": ["regenerate", "iron_slam", "darkness", "petrify_gaze"],
    "dungeon": "verdant_labyrinth",
    "intro_text": (
        "\n" + "=" * 55 + "\n"
        + "  👑 BOSS ENCOUNTER: VERDANT GUARDIAN 👑\n"
        + "=" * 55 + "\n"
        + "  The ground splits open as an ancient treant rises,\n"
        + "  its body woven from the roots of the World Tree itself.\n"
        + "  Eyes of blazing green fire regard you with ancient\n"
        + "  wisdom and terrible resolve.\n"
        + '  "The Seed must not be disturbed. Turn back or perish."\n'
        + "=" * 55 + "\n"
    ),
}

ENEMY_SPAWN_CHANCE = {
    1: 0.25,
    2: 0.35,
    3: 0.40,
}


# =====================================================================
# COMBAT STATE
# =====================================================================

class CombatState:
    """Tracks the state of an active combat encounter."""

    def __init__(self, enemy_data, is_boss=False, is_mini_boss=False, level=1, feel_intensity="normal"):
        self.enemy_id = enemy_data.get("id", "unknown")
        self.enemy_name = enemy_data["name"]
        self.enemy_description = enemy_data["description"]
        self.level = level
        self.max_hp = enemy_data["hp"]
        self.hp = enemy_data["hp"]
        self.attack = enemy_data["attack"]
        self.defense = enemy_data["defense"]
        self.xp_reward = enemy_data["xp_reward"]
        self.gold_reward = enemy_data["gold_reward"]
        self.loot = list(enemy_data.get("loot", []))
        self.abilities = list(enemy_data.get("abilities", []))
        self.is_boss = is_boss
        self.is_mini_boss = is_mini_boss
        self.intro_text = enemy_data.get("intro_text", "")
        self.turn = 0
        self.player_defending = False
        self.enemy_buff_defense = 0
        self.player_fled = False
        self.feel_intensity = _normalize_feel_intensity(feel_intensity)

        # Status effects: list of {"type": "poison", "dmg": 4, "duration": 3}
        self.player_statuses = []
        self.enemy_statuses = []

        # Adrenaline buff from blocking big hits
        self.player_adrenaline = 0  # bonus damage next attack

        # Momentum from consecutive basic attacks
        self.attack_streak = 0

        # Tactical affinity system for enemy weaknesses/resistances
        self.enemy_vulnerability, self.enemy_resistance = self._roll_enemy_affinities()
        self.last_damage_note = ""
        self.last_damage_tags = []

        # Boss phase system (phase 1 = full health, 2 = below 50%, 3 = below 25%)
        self.boss_phase = 1
        self.phase_transitions_done = set()  # tracks which phases have triggered

    def _roll_enemy_affinities(self):
        """Pick one vulnerability and one resistance to create tactical variety."""
        tags = ["physical", "poison", "burn", "bleed", "frost", "arcane"]
        eid = (self.enemy_id or "").lower()

        if "frost" in eid or "ice" in eid:
            return "burn", "frost"
        if "fire" in eid or "magma" in eid or "flame" in eid:
            return "frost", "burn"
        if "spider" in eid or "snake" in eid or "viper" in eid:
            return "physical", "poison"
        if "skeleton" in eid or "spirit" in eid or "wraith" in eid:
            return "arcane", "bleed"

        vulnerability = random.choice(tags)
        resistance = random.choice([t for t in tags if t != vulnerability])
        return vulnerability, resistance

    def to_dict(self):
        return {
            "enemy_id": self.enemy_id,
            "enemy_name": self.enemy_name,
            "enemy_description": self.enemy_description,
            "level": self.level,
            "max_hp": self.max_hp,
            "hp": self.hp,
            "attack": self.attack,
            "defense": self.defense,
            "xp_reward": self.xp_reward,
            "gold_reward": self.gold_reward,
            "loot": self.loot,
            "abilities": self.abilities,
            "is_boss": self.is_boss,
            "is_mini_boss": self.is_mini_boss,
            "turn": self.turn,
            "player_defending": self.player_defending,
            "enemy_buff_defense": self.enemy_buff_defense,
            "player_statuses": self.player_statuses,
            "enemy_statuses": self.enemy_statuses,
            "feel_intensity": getattr(self, "feel_intensity", "normal"),
            "player_adrenaline": self.player_adrenaline,
            "attack_streak": getattr(self, "attack_streak", 0),
            "enemy_vulnerability": getattr(self, "enemy_vulnerability", "physical"),
            "enemy_resistance": getattr(self, "enemy_resistance", "bleed"),
            "boss_phase": getattr(self, 'boss_phase', 1),
            "phase_transitions_done": list(getattr(self, 'phase_transitions_done', set())),
        }

    @classmethod
    def from_dict(cls, data):
        cs = cls.__new__(cls)
        cs.enemy_id = data.get("enemy_id", "unknown")
        cs.enemy_name = data.get("enemy_name", "Enemy")
        cs.enemy_description = data.get("enemy_description", "")
        cs.level = data.get("level", 1)
        cs.max_hp = data.get("max_hp", 30)
        cs.hp = data.get("hp", 30)
        cs.attack = data.get("attack", 5)
        cs.defense = data.get("defense", 2)
        cs.xp_reward = data.get("xp_reward", 10)
        cs.gold_reward = data.get("gold_reward", (5, 15))
        cs.loot = data.get("loot", [])
        cs.abilities = data.get("abilities", [])
        cs.is_boss = data.get("is_boss", False)
        cs.is_mini_boss = data.get("is_mini_boss", False)
        cs.intro_text = ""
        cs.turn = data.get("turn", 0)
        cs.player_defending = data.get("player_defending", False)
        cs.enemy_buff_defense = data.get("enemy_buff_defense", 0)
        cs.player_fled = False
        cs.feel_intensity = _normalize_feel_intensity(data.get("feel_intensity", "normal"))
        cs.player_statuses = data.get("player_statuses", [])
        cs.enemy_statuses = data.get("enemy_statuses", [])
        cs.player_adrenaline = data.get("player_adrenaline", 0)
        cs.attack_streak = data.get("attack_streak", 0)
        cs.enemy_vulnerability = data.get("enemy_vulnerability", "physical")
        cs.enemy_resistance = data.get("enemy_resistance", "bleed")
        cs.last_damage_note = ""
        cs.last_damage_tags = data.get("last_damage_tags", [])
        cs.boss_phase = data.get("boss_phase", 1)
        cs.phase_transitions_done = set(data.get("phase_transitions_done", []))
        return cs


# =====================================================================
# COMBAT LOGIC
# =====================================================================

def calculate_crit(player):
    """
    Check if the player's attack is a critical hit.
    Base 5% + 2% per dexterity + 1% per perception + crit_chance_bonus from skills.
    Returns (is_crit: bool, multiplier: float)
    """
    dex = player.stats.get("dexterity", 0)
    perc = player.stats.get("perception", 0)
    bonus = player.stats.get("crit_chance_bonus", 0)

    artifact_fx, _artifact_id = get_artifact_combat_effects(player)
    crit_bonus = float(artifact_fx.get("crit_chance_bonus", 0.0))
    crit_mult_bonus = float(artifact_fx.get("crit_damage_bonus", 0.0))

    crit_chance = min(0.60, 0.05 + dex * 0.02 + perc * 0.01 + bonus + crit_bonus)

    if random.random() < crit_chance:
        return True, 1.8 + crit_mult_bonus
    return False, 1.0


def _get_affinity_damage_bonus(combat, damage_tag):
    """Return (multiplier, note) for vulnerability/resistance interactions."""
    if not damage_tag:
        return 1.0, ""

    vulnerability = getattr(combat, "enemy_vulnerability", None)
    resistance = getattr(combat, "enemy_resistance", None)

    if damage_tag == vulnerability:
        return 1.35, "✨ Weakness exploited!"
    if damage_tag == resistance:
        return 0.75, "🛡️ Enemy resisted the hit!"
    return 1.0, ""


def _combat_tags(*tags):
    parts = [f"[{str(tag).upper()}]" for tag in tags if tag]
    return " ".join(parts)


def _format_combat_line(summary, details=None, tags=None):
    tag_text = _combat_tags(*(tags or ()))
    if tag_text:
        summary = f"{tag_text} {summary}"
    result = f"\n  {summary}"
    if details:
        result += f"\n  ↳ {details}"
    return result


def calculate_player_damage(player, combat, multiplier=1.0, damage_tag="physical"):
    """
    Calculate damage the player deals to the enemy.
    Strength determines base damage with some randomness.
    """
    strength = player.stats.get("strength", 0)
    base = max(1, strength)
    low = max(1, int(base * 0.75))
    high = max(low + 1, int(base * 1.25) + 1)
    raw_damage = random.randint(low, high)

    # Apply multiplier (from abilities, crits, etc.)
    raw_damage = int(raw_damage * multiplier)

    # Affinity interaction (weakness / resistance)
    affinity_mult, note = _get_affinity_damage_bonus(combat, damage_tag)
    raw_damage = int(raw_damage * affinity_mult)
    note_parts = [note] if note else []
    note_tags = []
    if damage_tag == getattr(combat, "enemy_vulnerability", None):
        note_tags.append("WEAK")
    elif damage_tag == getattr(combat, "enemy_resistance", None):
        note_tags.append("RESIST")

    # Artifact outgoing modifiers
    artifact_fx, artifact_id = get_artifact_combat_effects(player)
    outgoing_mult = float(artifact_fx.get("outgoing_mult", 1.0))
    tag_mult = float(artifact_fx.get("tag_multipliers", {}).get(damage_tag, 1.0))
    artifact_mult = max(0.1, outgoing_mult * tag_mult)
    raw_damage = int(raw_damage * artifact_mult)

    if artifact_id and artifact_mult > 1.001:
        aname = ARTIFACT_DATABASE.get(artifact_id, {}).get("name", artifact_id.replace("_", " ").title())
        note_parts.append(f"{aname} amplifies your strike.")

    # Apply adrenaline bonus
    if combat.player_adrenaline > 0:
        raw_damage += combat.player_adrenaline
        combat.player_adrenaline = 0

    # Apply enemy defense
    effective_defense = combat.defense + combat.enemy_buff_defense
    reduction = effective_defense * 0.04
    damage = max(1, int(raw_damage * max(0.20, 1 - reduction)))

    # Artifact lifesteal from dealt damage.
    lifesteal_pct = float(artifact_fx.get("lifesteal_pct", 0.0))
    if lifesteal_pct > 0 and damage > 0:
        heal = int(max(0, damage * lifesteal_pct))
        if heal > 0:
            hp = player.stats.get("health", 0)
            hp_max = player.stats.get("health_max", 100)
            actual = min(heal, max(0, hp_max - hp))
            if actual > 0:
                player.stats["health"] = hp + actual
                note_parts.append(f"You siphon {actual} HP.")

    combat.last_damage_note = " ".join(p for p in note_parts if p)
    combat.last_damage_tags = note_tags

    return damage


def calculate_enemy_damage(player, combat):
    """
    Calculate damage the enemy deals to the player.
    Accounts for freeze status on enemy.
    """
    base = combat.attack
    low = max(1, int(base * 0.80))
    high = max(low + 1, int(base * 1.20) + 1)
    raw_damage = random.randint(low, high)

    # Check if enemy is frozen (reduces attack)
    for status in combat.enemy_statuses:
        if status["type"] == "freeze":
            se = STATUS_EFFECTS.get("freeze", {})
            reduction_pct = se.get("reduction", 0.30)
            raw_damage = max(1, int(raw_damage * (1 - reduction_pct)))
            break

    # Player defense reduces damage
    defense = player.stats.get("defense", 0)
    reduction = defense * 0.03
    damage = max(1, int(raw_damage * max(0.25, 1 - reduction)))

    # Defending halves damage
    if combat.player_defending:
        damage = max(1, damage // 2)

    # Artifact incoming modifiers
    artifact_fx, _artifact_id = get_artifact_combat_effects(player)
    incoming_mult = float(artifact_fx.get("incoming_mult", 1.0))
    damage = max(1, int(damage * max(0.25, incoming_mult)))

    # Intensity scales perceived combat pressure.
    feel_profile = _get_feel_profile(combat)
    damage = max(1, int(damage * feel_profile.get("enemy_damage_mult", 1.0)))

    return damage


def _tick_status_effects(statuses, target_name):
    """
    Process status effects at start of turn.
    Returns (messages, total_damage, is_stunned)
    """
    messages = []
    total_damage = 0
    is_stunned = False
    expired = []

    for i, status in enumerate(statuses):
        se = STATUS_EFFECTS.get(status["type"], {})
        icon = se.get("icon", "")

        if se.get("type") == "dot":
            dmg = status.get("dmg", 0)
            total_damage += dmg
            msg = se.get("message_tick", "takes {dmg} damage!").format(dmg=dmg)
            messages.append(f"  {icon} {target_name} {msg}")
        elif se.get("type") == "disable":
            is_stunned = True
            messages.append(f"  {icon} {target_name} {se.get('message_tick', 'is stunned!')}")
        elif se.get("type") == "debuff":
            messages.append(f"  {icon} {target_name} {se.get('message_tick', 'is affected!')}")

        status["duration"] -= 1
        if status["duration"] <= 0:
            expired.append(i)
            expire_msg = se.get("message_expire", "")
            if expire_msg:
                messages.append(f"  {icon} {target_name} {expire_msg}")

    for i in reversed(expired):
        statuses.pop(i)

    return messages, total_damage, is_stunned


def _apply_status(statuses, status_type, dmg=0, duration=2):
    """Add a status effect, stacking duration if already present."""
    for s in statuses:
        if s["type"] == status_type:
            s["duration"] = max(s["duration"], duration)
            if dmg > 0:
                s["dmg"] = max(s.get("dmg", 0), dmg)
            return
    statuses.append({"type": status_type, "dmg": dmg, "duration": duration})


def _process_enemy_ability(player, combat):
    """
    Enemy uses one of its abilities.
    Returns message string.
    """
    if not combat.abilities:
        return ""

    ability_id = random.choice(combat.abilities)
    ab = ENEMY_ABILITIES.get(ability_id)
    if not ab:
        return ""

    result = ""
    ab_type = ab.get("type", "damage")
    text = ab.get("text", "attacks!")

    if ab_type == "damage":
        low, high = ab["value"]
        dmg = random.randint(low, high)
        if combat.player_defending:
            dmg = max(1, dmg // 2)
        player.stats["health"] = player.stats.get("health", 100) - dmg
        result = _format_combat_line(f"{combat.enemy_name} {text}.", f"Damage dealt: {dmg}.", tags=["DAMAGE"])

    elif ab_type == "damage_status":
        low, high = ab["value"]
        dmg = random.randint(low, high)
        if combat.player_defending:
            dmg = max(1, dmg // 2)
        player.stats["health"] = player.stats.get("health", 100) - dmg
        status = ab.get("status", "poison")
        status_dmg = ab.get("status_dmg", 3)
        status_dur = ab.get("status_dur", 2)
        _apply_status(combat.player_statuses, status, status_dmg, status_dur)
        se = STATUS_EFFECTS.get(status, {})
        icon = se.get("icon", "")
        result = _format_combat_line(
            f"{combat.enemy_name} {text}.",
            f"Damage dealt: {dmg}. {icon} You {se.get('message_apply', 'are afflicted!')}",
            tags=["POISON" if status == "poison" else status.upper(), "DAMAGE"]
        )

    elif ab_type == "status":
        status = ab.get("status", "stun")
        status_dur = ab.get("status_dur", 1)
        _apply_status(combat.player_statuses, status, 0, status_dur)
        se = STATUS_EFFECTS.get(status, {})
        icon = se.get("icon", "")
        result = _format_combat_line(
            f"{combat.enemy_name} {text}.",
            f"{icon} You {se.get('message_apply', 'are afflicted!')}",
            tags=[status.upper(), "DEBUFF"]
        )

    elif ab_type == "damage_stun":
        low, high = ab["value"]
        dmg = random.randint(low, high)
        if combat.player_defending:
            dmg = max(1, dmg // 2)
        player.stats["health"] = player.stats.get("health", 100) - dmg
        stun_dur = ab.get("stun_dur", 1)
        _apply_status(combat.player_statuses, "stun", 0, stun_dur)
        result = _format_combat_line(
            f"{combat.enemy_name} {text}.",
            f"Damage dealt: {dmg}. You are stunned for {stun_dur} turn(s).",
            tags=["STUN", "DAMAGE"]
        )

    elif ab_type == "heal":
        low, high = ab["value"]
        heal = random.randint(low, high)
        combat.hp = min(combat.max_hp, combat.hp + heal)
        result = _format_combat_line(f"{combat.enemy_name} {text}.", f"Heals {heal} HP.", tags=["HEAL"])

    elif ab_type == "damage_heal":
        low, high = ab["value"]
        dmg = random.randint(low, high)
        if combat.player_defending:
            dmg = max(1, dmg // 2)
        player.stats["health"] = player.stats.get("health", 100) - dmg
        combat.hp = min(combat.max_hp, combat.hp + dmg)
        result = _format_combat_line(
            f"{combat.enemy_name} {text}.",
            f"Deals {dmg} damage and heals {dmg} HP.",
            tags=["DAMAGE", "HEAL"]
        )

    elif ab_type == "buff_defense":
        buff_val = ab.get("value", 2)
        combat.enemy_buff_defense += buff_val
        result = _format_combat_line(f"{combat.enemy_name} {text}.", f"Defense +{buff_val}.", tags=["BUFF"])

    return result


# Boss phase transition messages and effects
BOSS_PHASE_TRANSITIONS = {
    2: {  # Below 50% HP
        "message": (
            "\n" + "!" * 50 + "\n"
            "  ⚠️  PHASE TRANSITION ⚠️\n"
            "  The {name} roars with fury as its wounds mount!\n"
            "  It enters a frenzied state — attacks grow more vicious!\n"
            + "!" * 50 + "\n"
        ),
        "attack_bonus": 3,
        "defense_bonus": 0,
        "heal_pct": 0.05,  # heals 5% on phase transition
    },
    3: {  # Below 25% HP
        "message": (
            "\n" + "!" * 50 + "\n"
            "  💀  FINAL PHASE 💀\n"
            "  The {name} unleashes its full power in desperation!\n"
            "  Its eyes burn with unholy energy — this is its last stand!\n"
            + "!" * 50 + "\n"
        ),
        "attack_bonus": 5,
        "defense_bonus": 2,
        "heal_pct": 0.0,
    },
}


def _check_boss_phase_transition(combat):
    """Check if a boss should enter a new phase based on HP percentage.
    Returns phase transition message or empty string."""
    if not combat.is_boss:
        return ""

    hp_pct = combat.hp / combat.max_hp if combat.max_hp > 0 else 1.0
    result = ""

    if hp_pct <= 0.25 and 3 not in getattr(combat, 'phase_transitions_done', set()):
        if not hasattr(combat, 'phase_transitions_done'):
            combat.phase_transitions_done = set()
        combat.phase_transitions_done.add(3)
        combat.boss_phase = 3
        transition = BOSS_PHASE_TRANSITIONS[3]
        result += transition["message"].format(name=combat.enemy_name)
        combat.attack += transition["attack_bonus"]
        combat.defense += transition["defense_bonus"]
        if transition["heal_pct"] > 0:
            heal_amt = int(combat.max_hp * transition["heal_pct"])
            combat.hp = min(combat.max_hp, combat.hp + heal_amt)
            result += f"  The {combat.enemy_name} recovers {heal_amt} HP!\n"

    elif hp_pct <= 0.50 and 2 not in getattr(combat, 'phase_transitions_done', set()):
        if not hasattr(combat, 'phase_transitions_done'):
            combat.phase_transitions_done = set()
        combat.phase_transitions_done.add(2)
        combat.boss_phase = 2
        transition = BOSS_PHASE_TRANSITIONS[2]
        result += transition["message"].format(name=combat.enemy_name)
        combat.attack += transition["attack_bonus"]
        combat.defense += transition["defense_bonus"]
        if transition["heal_pct"] > 0:
            heal_amt = int(combat.max_hp * transition["heal_pct"])
            combat.hp = min(combat.max_hp, combat.hp + heal_amt)
            result += f"  The {combat.enemy_name} recovers {heal_amt} HP!\n"

    return result


def _enemy_turn(player, combat):
    """
    Process the enemy's turn with AI decision-making.
    Returns narrative string.

    Enemy AI chances:
      Bosses/Mini-bosses: 35% basic attack, 40% ability, 15% heavy attack, 10% defend
      Regular enemies:    40% basic attack, 30% ability, 20% heavy attack, 10% nothing special
    
    Bosses have phase transitions at 50% and 25% HP that boost their stats.
    In phase 2+, bosses use abilities more often and hit harder.
    """
    result = ""

    # Check boss phase transitions
    phase_msg = _check_boss_phase_transition(combat)
    if phase_msg:
        result += phase_msg

    # Check if enemy is stunned
    enemy_stun_msgs, _, enemy_stunned = _tick_status_effects(
        combat.enemy_statuses, f"The {combat.enemy_name}"
    )
    if enemy_stun_msgs:
        result += "\n" + "\n".join(enemy_stun_msgs)

    if enemy_stunned:
        result += _format_combat_line(f"The {combat.enemy_name} is stunned and cannot act.", None, tags=["STUN"])
        return result

    # Enemy DOT damage (bleed, burn, poison on enemy)
    for status in combat.enemy_statuses:
        se = STATUS_EFFECTS.get(status["type"], {})
        if se.get("type") == "dot" and status.get("dmg", 0) > 0:
            combat.hp -= status["dmg"]

    # AI decision
    roll = random.random()

    if combat.is_boss or combat.is_mini_boss:
        # Adjust AI based on boss phase (more aggressive in later phases)
        phase = getattr(combat, 'boss_phase', 1)
        if phase >= 3:
            # Final phase: 20% basic, 50% ability, 25% heavy, 5% defend
            basic_thresh, ability_thresh, heavy_thresh = 0.20, 0.70, 0.95
        elif phase >= 2:
            # Enraged phase: 25% basic, 45% ability, 20% heavy, 10% defend
            basic_thresh, ability_thresh, heavy_thresh = 0.25, 0.70, 0.90
        else:
            # Normal: 35% basic, 40% ability, 15% heavy, 10% defend
            basic_thresh, ability_thresh, heavy_thresh = 0.35, 0.75, 0.90

        if roll < basic_thresh:
            # Basic attack
            enemy_dmg = calculate_enemy_damage(player, combat)
            player.stats["health"] = player.stats.get("health", 100) - enemy_dmg
            result += _format_combat_line(f"The {combat.enemy_name} attacks.", f"Damage dealt: {enemy_dmg}.", tags=["DAMAGE"])
        elif roll < ability_thresh:
            # Use ability
            ab_msg = _process_enemy_ability(player, combat)
            if ab_msg:
                result += ab_msg
            else:
                enemy_dmg = calculate_enemy_damage(player, combat)
                player.stats["health"] = player.stats.get("health", 100) - enemy_dmg
                result += _format_combat_line(f"The {combat.enemy_name} attacks.", f"Damage dealt: {enemy_dmg}.", tags=["DAMAGE"])
        elif roll < heavy_thresh:
            # Heavy attack (1.5x damage, 2x in final phase)
            base_dmg = calculate_enemy_damage(player, combat)
            heavy_mult = 2.0 if phase >= 3 else 1.5
            heavy_dmg = max(1, int(base_dmg * heavy_mult))
            player.stats["health"] = player.stats.get("health", 100) - heavy_dmg
            if phase >= 3:
                result += _format_combat_line(f"The {combat.enemy_name} unleashes a devastating attack.", f"Damage dealt: {heavy_dmg}.", tags=["HEAVY", "DAMAGE"])
            else:
                result += _format_combat_line(f"The {combat.enemy_name} winds up a heavy attack.", f"Damage dealt: {heavy_dmg}.", tags=["HEAVY", "DAMAGE"])
        else:
            # Defend / heal
            if combat.hp < combat.max_hp * 0.5:
                heal = random.randint(5, 15)
                combat.hp = min(combat.max_hp, combat.hp + heal)
                result += _format_combat_line(f"The {combat.enemy_name} retreats and recovers.", f"Heals {heal} HP.", tags=["HEAL"])
            else:
                combat.enemy_buff_defense += 1
                result += _format_combat_line(f"The {combat.enemy_name} takes a defensive stance.", "Defense +1.", tags=["BUFF"])
    else:
        # Regular enemy AI
        if roll < 0.40:
            enemy_dmg = calculate_enemy_damage(player, combat)
            player.stats["health"] = player.stats.get("health", 100) - enemy_dmg
            result += _format_combat_line(f"The {combat.enemy_name} attacks.", f"Damage dealt: {enemy_dmg}.", tags=["DAMAGE"])
        elif roll < 0.70:
            ab_msg = _process_enemy_ability(player, combat)
            if ab_msg:
                result += ab_msg
            else:
                enemy_dmg = calculate_enemy_damage(player, combat)
                player.stats["health"] = player.stats.get("health", 100) - enemy_dmg
                result += _format_combat_line(f"The {combat.enemy_name} attacks.", f"Damage dealt: {enemy_dmg}.", tags=["DAMAGE"])
        elif roll < 0.90:
            base_dmg = calculate_enemy_damage(player, combat)
            heavy_dmg = max(1, int(base_dmg * 1.3))
            player.stats["health"] = player.stats.get("health", 100) - heavy_dmg
            result += _format_combat_line(f"The {combat.enemy_name} strikes hard.", f"Damage dealt: {heavy_dmg}.", tags=["HEAVY", "DAMAGE"])
        else:
            # Enemy hesitates / weak attack
            weak_dmg = max(1, calculate_enemy_damage(player, combat) // 2)
            player.stats["health"] = player.stats.get("health", 100) - weak_dmg
            result += _format_combat_line(f"The {combat.enemy_name} hesitates.", f"Glancing blow: {weak_dmg} damage.", tags=["WEAK", "DAMAGE"])

    # Passive mana regen at end of every enemy turn
    mana_regen_bonus = player.stats.get("mana_regen_bonus", 0.0)
    max_mana = player.stats.get("max_mana", 0)
    if max_mana > 0:
        regen = max(1, int(max_mana * (0.02 + mana_regen_bonus)))
        player.stats["mana"] = min(player.stats.get("mana", 0) + regen, max_mana)

    return result


def process_player_attack(player, combat):
    """
    Process the player's basic attack action.
    Includes critical hits and status effect ticking.
    """
    combat.turn += 1
    combat.player_defending = False

    result = ""

    # Tick player status effects at start of turn
    player_status_msgs, player_dot_dmg, player_stunned = _tick_status_effects(
        combat.player_statuses, "You"
    )
    if player_status_msgs:
        result += "\n".join(player_status_msgs) + "\n"

    if player_dot_dmg > 0:
        player.stats["health"] = player.stats.get("health", 100) - player_dot_dmg

    if player_stunned:
        combat.attack_streak = 0
        result += _format_combat_line("You are stunned and cannot attack this turn.", None, tags=["STUN"])
        # Enemy still attacks
        enemy_result = _enemy_turn(player, combat)
        result += enemy_result
        return result + "\n"

    feel_profile = _get_feel_profile(combat)

    # Consecutive basic attacks build momentum, scaled by feel intensity.
    per_hit = int(feel_profile.get("momentum_per_hit", 5))
    streak_cap = int(feel_profile.get("momentum_max_streak", 10))
    bonus_cap = int(feel_profile.get("momentum_cap", 50))
    combat.attack_streak = min(streak_cap, getattr(combat, "attack_streak", 0) + 1)
    streak_bonus_pct = min(bonus_cap, combat.attack_streak * per_hit)
    streak_mult = 1.0 + (streak_bonus_pct / 100.0)

    # Check for critical hit
    is_crit, crit_mult = calculate_crit(player)

    # Player attacks
    player_dmg = calculate_player_damage(
        player,
        combat,
        multiplier=crit_mult * streak_mult,
        damage_tag="physical",
    )
    combat.hp -= player_dmg

    detail_parts = []
    if combat.last_damage_note:
        detail_parts.append(combat.last_damage_note)
    if combat.attack_streak >= 3:
        detail_parts.append(f"{combat.attack_streak}-hit momentum (+{streak_bonus_pct}% damage)")
    if getattr(combat, "feel_intensity", "normal") == "high" and combat.attack_streak >= 5:
        detail_parts.append("Battle rhythm surges.")

    result += _format_combat_line(
        f"You strike the {combat.enemy_name} for {player_dmg} damage.",
        " | ".join(detail_parts) if detail_parts else None,
        tags=["CRIT"] if is_crit else None,
    )

    if combat.hp <= 0:
        combat.hp = 0
        return result + "\n"

    # Enemy turn
    enemy_result = _enemy_turn(player, combat)
    result += enemy_result

    return result + "\n"


def process_player_defend(player, combat):
    """
    Process the player's defend action.
    - Halves incoming damage
    - Constitution heals
    - Counterattack chance based on class
    - Adrenaline buff if blocking a big hit
    """
    combat.turn += 1
    combat.player_defending = True
    combat.attack_streak = 0

    result = ""

    # Tick player status effects
    player_status_msgs, player_dot_dmg, player_stunned = _tick_status_effects(
        combat.player_statuses, "You"
    )
    if player_status_msgs:
        result += "\n".join(player_status_msgs) + "\n"

    if player_dot_dmg > 0:
        player.stats["health"] = player.stats.get("health", 100) - player_dot_dmg

    if player_stunned:
        result += _format_combat_line("You are stunned and cannot defend properly.", None, tags=["STUN"])
        combat.player_defending = False
        enemy_result = _enemy_turn(player, combat)
        result += enemy_result
        return result + "\n"

    result += _format_combat_line("You raise your guard.", None, tags=["BUFF"])

    # Enemy turn (will deal halved damage due to player_defending)
    hp_before = player.stats.get("health", 100)
    enemy_result = _enemy_turn(player, combat)
    result += enemy_result
    hp_after = player.stats.get("health", 100)

    damage_taken = max(0, hp_before - hp_after)

    # Constitution heal
    con = player.stats.get("constitution", 0)
    if con > 0:
        heal = min(con, player.stats.get("health_max", 100) - player.stats.get("health", 0))
        if heal > 0:
            player.stats["health"] = player.stats.get("health", 0) + heal
            result += _format_combat_line(f"Your fortitude restores {heal} HP.", None, tags=["HEAL"])

    # Counterattack chance (20% base + 2% per strength for warrior, 3% per dex for rogue)
    player_class = player.stats.get("class", "warrior")
    str_val = player.stats.get("strength", 0)
    dex_val = player.stats.get("dexterity", 0)

    if player_class == "warrior":
        counter_chance = min(0.45, 0.20 + str_val * 0.02)
    elif player_class == "rogue":
        counter_chance = min(0.50, 0.15 + dex_val * 0.03)
    else:
        counter_chance = min(0.30, 0.10 + str_val * 0.01)

    if random.random() < counter_chance and combat.hp > 0:
        counter_dmg = max(1, calculate_player_damage(player, combat, multiplier=0.6))
        combat.hp -= counter_dmg
        result += _format_combat_line(f"Counterattack lands for {counter_dmg} damage.", None, tags=["COUNTER"])

    # Adrenaline from big blocks (damage blocked > 8)
    if damage_taken > 0 and hp_before - hp_after < damage_taken * 2:
        blocked_amount = damage_taken  # the halved amount
        if blocked_amount >= 4:
            adrenaline = min(blocked_amount, 8)
            combat.player_adrenaline += adrenaline
            result += _format_combat_line(
                f"Adrenaline surges (+{adrenaline} bonus damage next attack).",
                None,
                tags=["BUFF"]
            )

    return result + "\n"


def process_player_flee(player, combat):
    """
    Attempt to flee from combat.
    Cannot flee from bosses. Mini-bosses have reduced flee chance.
    """
    combat.turn += 1
    combat.player_defending = False
    combat.attack_streak = 0

    if combat.is_boss:
        enemy_dmg = calculate_enemy_damage(player, combat)
        player.stats["health"] = player.stats.get("health", 100) - enemy_dmg
        return False, (
            _format_combat_line(
                f"You cannot flee from the {combat.enemy_name}.",
                f"It strikes you as you turn for {enemy_dmg} damage.",
                tags=["FAIL"]
            )
            + "\n"
        )

    dex = player.stats.get("dexterity", 0)
    flee_chance = min(0.85, 0.40 + dex * 0.05)

    if combat.is_mini_boss:
        flee_chance *= 0.6  # Much harder to flee mini-bosses

    if random.random() < flee_chance:
        combat.player_fled = True
        return True, _format_combat_line("You successfully flee from combat.", None, tags=["FLEE"]) + "\n"
    else:
        enemy_dmg = calculate_enemy_damage(player, combat)
        player.stats["health"] = player.stats.get("health", 100) - enemy_dmg
        return False, (
            _format_combat_line(
                "You fail to escape.",
                f"The {combat.enemy_name} strikes you for {enemy_dmg} damage.",
                tags=["FAIL"]
            )
            + "\n"
        )


def process_ability_in_combat(player, combat, ability_data):
    """
    Process a skill tree ability used in combat.
    Handles combat_damage, combat_stun, combat_poison, etc.
    Returns combat narrative string.
    """
    combat.turn += 1
    combat.player_defending = False
    combat.attack_streak = 0

    result = ""

    # Tick player status effects
    status_msgs, dot_dmg, player_stunned = _tick_status_effects(
        combat.player_statuses, "You"
    )
    if status_msgs:
        result += "\n".join(status_msgs) + "\n"
    if dot_dmg > 0:
        player.stats["health"] = player.stats.get("health", 100) - dot_dmg

    if player_stunned:
        result += _format_combat_line("You are stunned and cannot use abilities.", None, tags=["STUN"])
        enemy_result = _enemy_turn(player, combat)
        result += enemy_result
        return result + "\n"

    effect = ability_data.get("effect", "")
    value = ability_data.get("value", 1.0)
    damage_tag = "arcane"

    if effect in ("combat_damage", "combat_crit_attack", "combat_execute"):
        damage_tag = "physical"
    elif effect == "combat_poison":
        damage_tag = "poison"
    elif effect == "combat_damage_burn":
        damage_tag = "burn"
    elif effect == "combat_bleed_attack":
        damage_tag = "bleed"
    elif effect == "combat_freeze_attack":
        damage_tag = "frost"

    if effect == "combat_damage":
        # Pure damage with multiplier
        dmg = calculate_player_damage(player, combat, multiplier=value, damage_tag=damage_tag)
        combat.hp -= dmg
        result += _format_combat_line(f"You deal {dmg} damage.", None, tags=["DAMAGE"])

    elif effect == "combat_crit_attack":
        # Guaranteed crit with multiplier
        dmg = calculate_player_damage(player, combat, multiplier=value, damage_tag=damage_tag)
        combat.hp -= dmg
        result += _format_combat_line(f"You deal {dmg} damage.", None, tags=["CRIT", "DAMAGE"])

    elif effect == "combat_stun":
        # Damage + stun
        dmg = calculate_player_damage(player, combat, multiplier=value, damage_tag="physical")
        combat.hp -= dmg
        stun_dur = ability_data.get("duration", 1)
        _apply_status(combat.enemy_statuses, "stun", 0, stun_dur)
        result += _format_combat_line(
            f"You deal {dmg} damage.",
            f"The {combat.enemy_name} is stunned for {stun_dur} turn(s).",
            tags=["STUN", "DAMAGE"]
        )

    elif effect == "combat_poison":
        # Normal damage + poison DOT
        dmg = calculate_player_damage(player, combat, multiplier=1.0, damage_tag=damage_tag)
        combat.hp -= dmg
        poison_dmg = ability_data.get("value", 4)
        poison_dur = ability_data.get("duration", 3)
        _apply_status(combat.enemy_statuses, "poison", poison_dmg, poison_dur)
        result += _format_combat_line(
            f"You deal {dmg} damage.",
            f"The {combat.enemy_name} is poisoned for {poison_dur} turns ({poison_dmg}/turn).",
            tags=["POISON", "DAMAGE"]
        )

    elif effect == "combat_freeze_attack":
        # Damage + freeze debuff
        dmg = calculate_player_damage(player, combat, multiplier=value, damage_tag=damage_tag)
        combat.hp -= dmg
        freeze_dur = ability_data.get("duration", 2)
        _apply_status(combat.enemy_statuses, "freeze", 0, freeze_dur)
        result += _format_combat_line(
            f"You deal {dmg} damage.",
            f"The {combat.enemy_name} is frozen for {freeze_dur} turns.",
            tags=["FREEZE", "DEBUFF", "DAMAGE"]
        )

    elif effect == "combat_damage_burn":
        # Damage + burn DOT
        dmg = calculate_player_damage(player, combat, multiplier=value, damage_tag=damage_tag)
        combat.hp -= dmg
        burn_dmg = ability_data.get("burn", 3)
        burn_dur = ability_data.get("duration", 2)
        _apply_status(combat.enemy_statuses, "burn", burn_dmg, burn_dur)
        result += _format_combat_line(
            f"You deal {dmg} damage.",
            f"The {combat.enemy_name} is burning for {burn_dur} turns ({burn_dmg}/turn).",
            tags=["BURN", "DAMAGE"]
        )

    elif effect == "combat_damage_stun":
        # Damage + stun
        dmg = calculate_player_damage(player, combat, multiplier=value, damage_tag="physical")
        combat.hp -= dmg
        stun_dur = ability_data.get("duration", 1)
        _apply_status(combat.enemy_statuses, "stun", 0, stun_dur)
        result += _format_combat_line(
            f"You deal {dmg} damage.",
            f"The {combat.enemy_name} is stunned for {stun_dur} turn(s).",
            tags=["STUN", "DAMAGE"]
        )

    elif effect == "combat_heal":
        # Heal the player
        heal_val = int(value)
        hp = player.stats.get("health", 100)
        hp_max = player.stats.get("health_max", 100)
        actual_heal = min(heal_val, hp_max - hp)
        player.stats["health"] = hp + actual_heal
        result += _format_combat_line(f"You heal for {actual_heal} HP.", None, tags=["HEAL"])

    elif effect == "combat_execute":
        # Instant kill below threshold, otherwise big damage
        threshold = value  # e.g. 0.30 = 30% HP
        enemy_hp_pct = combat.hp / combat.max_hp if combat.max_hp > 0 else 1.0
        if enemy_hp_pct <= threshold:
            combat.hp = 0
            result += _format_combat_line(
                f"The {combat.enemy_name} is slain instantly.",
                None,
                tags=["EXECUTE", "CRIT"]
            )
        else:
            dmg = calculate_player_damage(player, combat, multiplier=3.0, damage_tag=damage_tag)
            combat.hp -= dmg
            result += _format_combat_line(f"You deal {dmg} massive damage.", None, tags=["EXECUTE", "DAMAGE"])

    elif effect == "combat_bleed_attack":
        # Damage + bleed DOT
        dmg = calculate_player_damage(player, combat, multiplier=value, damage_tag=damage_tag)
        combat.hp -= dmg
        bleed_dmg = ability_data.get("bleed", 5)
        bleed_dur = ability_data.get("duration", 3)
        _apply_status(combat.enemy_statuses, "bleed", bleed_dmg, bleed_dur)
        result += _format_combat_line(
            f"You deal {dmg} damage.",
            f"The {combat.enemy_name} is bleeding for {bleed_dur} turns ({bleed_dmg}/turn).",
            tags=["BLEED", "DAMAGE"]
        )

    elif effect == "guaranteed_flee":
        # Guaranteed flee (unless boss)
        if combat.is_boss:
            result += _format_combat_line(
                f"The {combat.enemy_name} cannot be escaped.",
                "The smoke clears and the boss holds firm.",
                tags=["FAIL"]
            )
        else:
            combat.player_fled = True
            result += _format_combat_line("You vanish in a cloud of smoke and escape.", None, tags=["FLEE"])
            return result + "\n"

    elif effect == "buff_attack":
        # Temporary strength boost
        boost = int(value)
        duration = ability_data.get("duration", 3)
        active_effects = player.state.get("active_effects", {})
        active_effects["attack_boost"] = {"value": boost, "duration": duration}
        player.state["active_effects"] = active_effects
        add_stat_bonus(player, "strength", boost, allow_overflow=True)
        result += _format_combat_line(f"Strength rises by {boost} for {duration} turns.", None, tags=["BUFF"])

    elif effect == "extra_gold":
        # Double gold on next kill
        active_effects = player.state.get("active_effects", {})
        active_effects["double_gold"] = int(value)
        player.state["active_effects"] = active_effects
        result += f"\n  💰 Next enemy will drop {value:.0f}x gold!"

    elif effect == "temp_defense":
        # Temporary defense boost
        boost = int(value)
        duration = ability_data.get("duration", 4)
        active_effects = player.state.get("active_effects", {})
        active_effects["defense_boost"] = {"value": boost, "duration": duration}
        player.state["active_effects"] = active_effects
        add_stat_bonus(player, "defense", boost, allow_overflow=True)
        result += _format_combat_line(f"Defense rises by {boost} for {duration} turns.", None, tags=["BUFF"])

    elif effect == "restore_mana":
        # Restore a percentage of max mana in combat
        max_mana = player.stats.get("max_mana", 0)
        restore_amt = max(1, int(value * max_mana))
        old_mana = player.stats.get("mana", 0)
        player.stats["mana"] = min(old_mana + restore_amt, max_mana)
        actual = player.stats["mana"] - old_mana
        result += f"\n  💙 You restore {actual} MP!  ({player.stats['mana']}/{max_mana})"

    elif effect == "traveling_fireball":
        # Damage + burn locally, then fireball travels through connected rooms
        dmg = calculate_player_damage(player, combat, multiplier=value, damage_tag="burn")
        combat.hp -= dmg
        burn_dmg = ability_data.get("burn", 4)
        burn_dur = ability_data.get("duration", 3)
        _apply_status(combat.enemy_statuses, "burn", burn_dmg, burn_dur)
        result += _format_combat_line(
            f"True Fireball deals {dmg} damage.",
            f"The {combat.enemy_name} burns for {burn_dur} turns ({burn_dmg}/turn).",
            tags=["BURN", "DAMAGE"]
        )
        player.state["pending_travel"] = {
            "source": ability_data.get("name", "True Fireball"),
            "type": "fireball",
            "range_left": ability_data.get("travel_range", 3),
            "damage": ability_data.get("travel_damage", 20),
            "burn": ability_data.get("travel_burn", 3),
            "burn_dur": ability_data.get("travel_burn_dur", 2),
        }
        result += _format_combat_line("The fireball streaks into the next room.", None, tags=["TRAVEL"])

    elif effect == "chain_bounce":
        # Damage to current enemy + pre-damages adjacent rooms
        dmg = calculate_player_damage(player, combat, multiplier=value, damage_tag="arcane")
        combat.hp -= dmg
        result += _format_combat_line(f"You deal {dmg} damage.", None, tags=["ARCANE", "DAMAGE"])
        bounce_dmg  = ability_data.get("bounce_damage", 15)
        bounce_range = ability_data.get("bounce_range", 2)
        player.state["pending_travel"] = {
            "source": ability_data.get("name", "Chain Bounce"),
            "type": "bounce",
            "range_left": bounce_range,
            "damage": bounce_dmg,
            "stun": ability_data.get("bounce_stun", 0),
        }
        result += _format_combat_line(
            f"The effect bounces into {bounce_range} nearby room(s).",
            None,
            tags=["TRAVEL"]
        )

    elif effect == "seismic_wave":
        # Damage + optional stun/freeze locally + shockwave pre-damages 1 adjacent room
        dmg = calculate_player_damage(player, combat, multiplier=value, damage_tag="physical")
        combat.hp -= dmg
        wave_effect = ability_data.get("wave_effect", "none")
        wave_dur    = ability_data.get("wave_dur", 1)
        if wave_effect == "stun":
            _apply_status(combat.enemy_statuses, "stun", 0, wave_dur)
            result += _format_combat_line(
                f"Shockwave deals {dmg} damage.",
                f"The {combat.enemy_name} is stunned for {wave_dur} turn(s).",
                tags=["STUN", "DAMAGE"]
            )
        elif wave_effect == "freeze":
            _apply_status(combat.enemy_statuses, "freeze", 0, wave_dur)
            result += _format_combat_line(
                f"Frost Wave deals {dmg} damage.",
                f"The {combat.enemy_name} is frozen for {wave_dur} turn(s).",
                tags=["FREEZE", "DEBUFF", "DAMAGE"]
            )
        else:
            result += _format_combat_line(f"Seismic Stomp deals {dmg} damage.", None, tags=["DAMAGE"])
        player.state["pending_travel"] = {
            "source": ability_data.get("name", "Seismic Wave"),
            "type": "wave",
            "range_left": ability_data.get("travel_range", 1),
            "damage": ability_data.get("wave_damage", 14),
            "wave_effect": wave_effect,
            "wave_dur": wave_dur,
        }
        result += _format_combat_line("A shockwave ripples into the next room.", None, tags=["TRAVEL"])

    elif effect == "shadow_drift":
        # Normal damage + poison current + optionally pre-poisons / pre-stuns adjacent room
        dmg = calculate_player_damage(player, combat, multiplier=value, damage_tag="poison")
        combat.hp -= dmg
        poison_dmg = ability_data.get("poison_dmg", 5)
        poison_dur = ability_data.get("poison_dur", 3)
        if poison_dmg > 0:
            _apply_status(combat.enemy_statuses, "poison", poison_dmg, poison_dur)
            result += _format_combat_line(
                f"You deal {dmg} damage.",
                f"The {combat.enemy_name} is poisoned for {poison_dur} turns ({poison_dmg}/turn).",
                tags=["POISON", "DAMAGE"]
            )
        else:
            result += _format_combat_line("Shadow Blink deals damage.", f"You deal {dmg} damage.", tags=["DAMAGE"])
        player.state["pending_travel"] = {
            "source": ability_data.get("name", "Shadow Drift"),
            "type": "drift",
            "range_left": ability_data.get("travel_range", 1),
            "damage": 0,
            "poison_dmg": ability_data.get("travel_poison_dmg", 4),
            "poison_dur": ability_data.get("travel_poison_dur", 2),
            "stun": ability_data.get("shadow_stun", 0),
        }
        result += _format_combat_line("A shadow trace drifts into the next room.", None, tags=["TRAVEL"])

    elif effect == "smoke_cascade":
        # Flee current combat (non-boss) + pre-stuns enemies in adjacent rooms
        cascade_range = ability_data.get("cascade_range", 1)
        cascade_stun  = ability_data.get("cascade_stun", 1)
        if combat.is_boss:
            result += _format_combat_line(
                f"The {combat.enemy_name} cannot be escaped.",
                "The smoke clears and the boss holds firm.",
                tags=["FAIL"]
            )
        else:
            combat.player_fled = True
            player.state["pending_travel"] = {
                "source": ability_data.get("name", "Smoke Cascade"),
                "type": "stun_wave",
                "range_left": cascade_range,
                "damage": 0,
                "stun": cascade_stun,
            }
            result += _format_combat_line("Smoke Cascade blinds the surrounding rooms.", "You vanish in a cloud of smoke.", tags=["FLEE", "DEBUFF"])
            return result + "\n"

    if combat.last_damage_note and ("You deal" in result or "You strike" in result):
        result += f"\n  {combat.last_damage_note}"

    # Check if enemy died from ability
    if combat.hp <= 0:
        combat.hp = 0
        return result + "\n"

    # Enemy turn
    enemy_result = _enemy_turn(player, combat)
    result += enemy_result

    return result + "\n"


def get_combat_status(player, combat):
    """Get the current combat status display with enhanced visuals."""
    feel_profile = _get_feel_profile(combat)

    # Enemy HP bar
    pct = max(0, combat.hp / combat.max_hp) if combat.max_hp > 0 else 0
    bar_len = int(feel_profile.get("enemy_bar_len", 20))
    filled = int(pct * bar_len)
    bar = "█" * filled + "░" * (bar_len - filled)

    # Player HP bar
    php = player.stats.get("health", 0)
    php_max = player.stats.get("health_max", 100)
    ppct = max(0, php / php_max) if php_max > 0 else 0
    player_bar_len = int(feel_profile.get("player_bar_len", 15))
    pfilled = int(ppct * player_bar_len)
    pbar = "█" * pfilled + "░" * (player_bar_len - pfilled)

    # HP urgency indicators
    if pct <= 0.25:
        enemy_hp_icon = "💀"
    elif pct <= 0.50:
        enemy_hp_icon = "⚠️"
    else:
        enemy_hp_icon = "❤️"

    if ppct <= 0.25:
        player_hp_icon = "💀 CRITICAL"
    elif ppct <= 0.50:
        player_hp_icon = "⚠️ WOUNDED"
    else:
        player_hp_icon = "❤️"

    boss_marker = ""
    if combat.is_boss:
        phase = getattr(combat, 'boss_phase', 1)
        if phase >= 3:
            boss_marker = "  👑 BOSS — 💀 FINAL PHASE"
        elif phase >= 2:
            boss_marker = "  👑 BOSS — ⚠️ ENRAGED"
        else:
            boss_marker = "  👑 BOSS"
    elif combat.is_mini_boss:
        boss_marker = "  ⚔️ MINI-BOSS"

    result = "\n" + "═" * 50 + "\n"
    result += f"  {combat.enemy_name} [Lv.{combat.level}]{boss_marker}\n"
    result += f"  {enemy_hp_icon} [{bar}] {combat.hp}/{combat.max_hp}\n"

    # Show enemy status effects with duration bars
    enemy_statuses = []
    for s in combat.enemy_statuses:
        se = STATUS_EFFECTS.get(s["type"], {})
        icon = se.get("icon", "")
        dur = s.get("duration", 0)
        dur_bar = "●" * min(dur, 5) + "○" * max(0, 5 - dur)
        enemy_statuses.append(f"  {icon} {se.get('name', s['type'])} [{dur_bar}] {dur}T")
    if enemy_statuses:
        result += "  Afflictions:\n"
        for es in enemy_statuses:
            result += f"  {es}\n"

    result += "─" * 50 + "\n"
    result += f"  You  {player_hp_icon}\n"
    result += f"  HP: [{pbar}] {php}/{php_max}\n"

    # Mana bar
    pmana = player.stats.get("mana", 0)
    pmana_max = player.stats.get("max_mana", 0)
    if pmana_max > 0:
        mpct = max(0, pmana / pmana_max)
        mfilled = int(mpct * 15)
        mbar = "█" * mfilled + "░" * (15 - mfilled)
        result += f"  MP: [{mbar}] {pmana}/{pmana_max}\n"

    # Show player status effects with detail
    player_statuses = []
    for s in combat.player_statuses:
        se = STATUS_EFFECTS.get(s["type"], {})
        icon = se.get("icon", "")
        dur = s.get("duration", 0)
        dur_bar = "●" * min(dur, 5) + "○" * max(0, 5 - dur)
        effect_type = se.get("type", "")
        if effect_type == "dot":
            detail = f"(dmg/turn)"
        elif effect_type == "disable":
            detail = f"(can't act)"
        elif effect_type == "debuff":
            reduction = se.get("reduction", 0)
            detail = f"(-{reduction:.0%} atk)"
        else:
            detail = ""
        player_statuses.append(f"  {icon} {se.get('name', s['type'])} [{dur_bar}] {dur}T {detail}")
    if player_statuses:
        result += "  Afflictions:\n"
        for ps in player_statuses:
            result += f"  {ps}\n"

    # Show active buffs from abilities
    if hasattr(player, 'state'):
        active_effects = player.state.get("active_effects", {})
        if active_effects:
            buff_list = []
            for eff_name, eff_data in active_effects.items():
                if isinstance(eff_data, dict):
                    dur = eff_data.get("duration", 0)
                    if dur > 0:
                        buff_list.append(f"✨ {eff_name.replace('_', ' ').title()} ({dur}T)")
                elif isinstance(eff_data, (int, float)) and eff_data > 0:
                    buff_list.append(f"✨ {eff_name.replace('_', ' ').title()} ({eff_data}T)")
            if buff_list:
                result += "  Buffs: " + " | ".join(buff_list) + "\n"

    # Show adrenaline with visual bar
    if combat.player_adrenaline > 0:
        adr = combat.player_adrenaline
        adr_bar = "🔥" * min(adr, 5)
        result += f"  {adr_bar} Adrenaline: +{adr} bonus damage\n"

    # Show momentum streak
    streak = getattr(combat, "attack_streak", 0)
    if streak > 0:
        per_hit = int(feel_profile.get("momentum_per_hit", 5))
        bonus_cap = int(feel_profile.get("momentum_cap", 50))
        streak_bonus_pct = min(bonus_cap, streak * per_hit)
        streak_bar = "⚔️" * min(streak, 6)
        result += f"  {streak_bar} Momentum: {streak} hit(s) (+{streak_bonus_pct}% damage)\n"

    if feel_profile.get("show_weakness_hints", True):
        vuln = DAMAGE_TAG_LABELS.get(getattr(combat, "enemy_vulnerability", "physical"), "Physical")
        resist = DAMAGE_TAG_LABELS.get(getattr(combat, "enemy_resistance", "bleed"), "Bleed")
        result += f"  🎯 Weak to: {vuln}  |  🧱 Resists: {resist}\n"

    result += f"  Feel: {getattr(combat, 'feel_intensity', 'normal').upper()}\n"

    result += "═" * 50 + "\n"
    result += "  Commands: attack | defend | flee"
    if hasattr(player, 'state') and player.state.get("unlocked_skills"):
        result += " | ability <name>"
        # Show ready abilities with hotbar numbers
        try:
            from skill_tree import get_active_abilities
            abilities = get_active_abilities(player)
            cooldowns = player.state.get("cooldowns", {})
            ready = []
            for i, ab in enumerate(abilities):
                cd = cooldowns.get(ab["skill_id"], 0)
                if cd > 0 and feel_profile.get("detailed_hotbar", True):
                    ready.append(f"[{i+1}] {ab['name']} ({cd}T cd)")
                else:
                    ready.append(f"[{i+1}] {ab['name']} ✦")
            if ready:
                result += "\n" + "─" * 50 + "\n"
                result += "  Abilities: " + " | ".join(ready)
        except Exception:
            pass
    result += "\n"
    return result


def generate_victory_result(player, combat):
    """Generate the victory message, award XP and loot."""
    feel = _normalize_feel_intensity(getattr(combat, "feel_intensity", "normal"))
    result = "\n" + "=" * 55 + "\n"
    if combat.is_boss:
        result += f"  👑 LEGENDARY VICTORY! BOSS DEFEATED: {combat.enemy_name}!\n"
    elif combat.is_mini_boss:
        result += f"  ⚔️ MINI-BOSS DEFEATED: {combat.enemy_name}!\n"
    else:
        result += f"  ✨ VICTORY! {combat.enemy_name} defeated!\n"
    result += "=" * 55 + "\n"

    # Gold reward
    if isinstance(combat.gold_reward, (list, tuple)) and len(combat.gold_reward) == 2:
        gold = random.randint(combat.gold_reward[0], combat.gold_reward[1])
    else:
        gold = int(combat.gold_reward) if combat.gold_reward else 0

    # Check for double gold effect
    active_effects = player.state.get("active_effects", {})
    set_utility = player.state.get("active_set_utility_effects", {}) if hasattr(player, "state") else {}
    set_gold_mult = float(set_utility.get("combat_gold_mult", 1.0))
    gold_mult = active_effects.get("double_gold", 1)
    if gold_mult > 1:
        gold = int(gold * gold_mult)
        del active_effects["double_gold"]
        result += f"  💰 Gold (x{gold_mult}): +{gold}\n"
    elif gold > 0:
        result += f"  💰 Gold: +{gold}\n"

    if gold > 0 and set_gold_mult > 1.0:
        bonus_gold = int(max(0, gold * (set_gold_mult - 1.0)))
        if bonus_gold > 0:
            gold += bonus_gold
            result += f"  ✨ Set bonus gold: +{bonus_gold}\n"

    if gold > 0:
        player.stats["gold"] = player.stats.get("gold", 0) + gold

    # Loot drops
    dropped = []
    for item_id, chance in combat.loot:
        if random.random() < chance:
            player.inventory[item_id] = player.inventory.get(item_id, 0) + 1
            nice = item_id.replace("_", " ")
            dropped.append(nice)
    if dropped:
        result += "  Loot:\n"
        for d in dropped:
            result += f"     - {d}\n"

    # Targeted boss loot tables guarantee progression-defining rewards.
    table_drops = roll_elite_table_drops(player, combat)
    if table_drops:
        table_label = "Boss Loot Table" if getattr(combat, "is_boss", False) else "Mini-Boss Loot Table"
        result += f"  {table_label}:\n"
        for item_id in table_drops:
            result += f"     - {item_id.replace('_', ' ')}\n"

    if feel == "high":
        streak = getattr(combat, "attack_streak", 0)
        if streak >= 4:
            result += f"  🔥 Finisher Momentum: {streak}-hit chain\n"
        if getattr(combat, "player_adrenaline", 0) > 0:
            result += "  ⚡ You finish the fight still pulsing with adrenaline.\n"
    elif feel == "low":
        result += "  Steady victory.\n"

    result += "=" * 55 + "\n"

    # Clear combat status effects
    combat.player_statuses.clear()
    combat.enemy_statuses.clear()

    return result


def get_enemies_for_dungeon(dungeon_id, floor_num):
    """Get a list of eligible enemy IDs for a dungeon + floor."""
    eligible = []
    for eid, edata in ENEMY_DATABASE.items():
        dun = edata.get("dungeon", "any")
        frange = edata.get("floor_range", (1, 3))
        if (dun == dungeon_id or dun == "any") and frange[0] <= floor_num <= frange[1]:
            eligible.append(eid)
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


def get_mini_boss_for_dungeon(dungeon_id):
    """Get the mini-boss data for a dungeon, or None."""
    mb_id = DUNGEON_MINI_BOSS_MAP.get(dungeon_id)
    if mb_id and mb_id in MINI_BOSS_DATABASE:
        data = dict(MINI_BOSS_DATABASE[mb_id])
        data["id"] = mb_id
        return data
    return None


def should_spawn_enemy(floor_num, room_data):
    """Decide if an enemy should spawn in a given room."""
    if room_data.get("is_boss_room"):
        return False
    if room_data.get("crafting_altar"):
        return False
    if room_data.get("npcs"):
        return False
    room_id = room_data.get("_room_id", "")
    if "entrance" in room_id or "mouth" in room_id:
        return False

    chance = ENEMY_SPAWN_CHANCE.get(floor_num, 0.30)
    return random.random() < chance


def create_enemy_instance(enemy_id, level=None, floor_num=1, feel_intensity="normal", difficulty_modifier=1.0):
    """Create a fresh enemy instance from the database with level scaling.
    
    Args:
        enemy_id: The enemy template ID
        level: Specific level (overrides floor_num calculation)
        floor_num: Dungeon floor for level calculation (default 1)
        feel_intensity: Game feel intensity level
        difficulty_modifier: Difficulty scaling multiplier (0.5 = easier, 2.0 = harder)
    """
    template = ENEMY_DATABASE.get(enemy_id)
    if not template:
        return None
    
    # Calculate level if not specified
    if level is None:
        level = calculate_enemy_level(floor_num, "regular")
    
    # Scale stats based on level and difficulty
    data = scale_enemy_stats(dict(template), level, "regular", difficulty_modifier)
    data["id"] = enemy_id
    
    # Filter abilities by level
    data["abilities"] = get_level_abilities(data["abilities"], level)
    
    return CombatState(data, is_boss=False, level=level, feel_intensity=feel_intensity)


def create_boss_instance(dungeon_id, floor_num=3, feel_intensity="normal", difficulty_modifier=1.0):
    """Create a boss instance for the given dungeon with level scaling."""
    boss_data = get_boss_for_dungeon(dungeon_id)
    if not boss_data:
        return None
    
    # Calculate boss level
    level = calculate_enemy_level(floor_num, "boss")
    
    # Scale stats including difficulty modifier
    scaled_data = scale_enemy_stats(boss_data, level, "boss", difficulty_modifier)
    scaled_data["abilities"] = get_level_abilities(scaled_data["abilities"], level)
    
    return CombatState(scaled_data, is_boss=True, level=level, feel_intensity=feel_intensity)


def create_mini_boss_instance(dungeon_id, floor_num=2, feel_intensity="normal", difficulty_modifier=1.0):
    """Create a mini-boss instance for the given dungeon with level scaling."""
    mb_data = get_mini_boss_for_dungeon(dungeon_id)
    if not mb_data:
        return None
    
    # Calculate mini-boss level
    level = calculate_enemy_level(floor_num, "mini_boss")
    
    # Scale stats including difficulty modifier
    scaled_data = scale_enemy_stats(mb_data, level, "mini_boss", difficulty_modifier)
    scaled_data["abilities"] = get_level_abilities(scaled_data["abilities"], level)
    
    return CombatState(scaled_data, is_boss=False, is_mini_boss=True, level=level, feel_intensity=feel_intensity)
