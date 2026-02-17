"""
Skill Tree System
=================
Class-based skill trees with tiered nodes:
  - Passive nodes: permanent stat bonuses (most nodes - small +1/+2 increments)
  - Active nodes: usable abilities with cooldowns (combat, exploration, crafting, trap)

Each class (Warrior, Rogue, Mage) has its own tree with ~55 nodes
across 10 tiers. Nodes require prerequisite nodes and cost skill points.

The graphical skill tree window is built using Tkinter Canvas with
horizontal scrolling to accommodate the large tree.
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
#   "tier":          1-10 (determines position)
#   "type":          "passive" or "active"
#   "cost":          skill points to unlock
#   "prerequisites": list of node IDs that must be unlocked first
#   "stat_bonuses":  dict of stat_name -> value (for passive nodes)
#   "ability":       dict defining the active ability (for active nodes):
#       "name":       ability name
#       "cooldown":   number of moves/turns before it can be used again
#       "effect":     what it does (parsed by ability system)
#       "use_text":   message shown when used
#       "combat":     True if usable in combat, False for out-of-combat
# }
# =====================================================================


# =====================================================================
# WARRIOR SKILL TREE  (55 nodes: ~47 passive, ~8 active)
# =====================================================================
# Branches: LEFT = Tank/Defense path, RIGHT = Offense/Strength path
# Abilities are combat-focused: power strikes, stuns, war cries, etc.
# =====================================================================

WARRIOR_TREE = [
    # =========== TIER 1 - Entry (6 nodes) ===========
    {"id": "w_thick_skin", "name": "Thick Skin", "tier": 1, "type": "passive", "cost": 1,
     "prerequisites": [], "stat_bonuses": {"defense": 1},
     "description": "Your skin is tougher than average.\n+1 Defense"},
    {"id": "w_strong_arm", "name": "Strong Arm", "tier": 1, "type": "passive", "cost": 1,
     "prerequisites": [], "stat_bonuses": {"strength": 1},
     "description": "Raw physical power fills your muscles.\n+1 Strength"},
    {"id": "w_endurance", "name": "Endurance", "tier": 1, "type": "passive", "cost": 1,
     "prerequisites": [], "stat_bonuses": {"constitution": 1},
     "description": "You can endure more than most.\n+1 Constitution"},
    {"id": "w_battle_stance", "name": "Battle Stance", "tier": 1, "type": "passive", "cost": 1,
     "prerequisites": [], "stat_bonuses": {"strength": 1},
     "description": "Proper fighting form.\n+1 Strength"},
    {"id": "w_sturdy_build", "name": "Sturdy Build", "tier": 1, "type": "passive", "cost": 1,
     "prerequisites": [], "stat_bonuses": {"health_max_bonus": 5},
     "description": "A solid frame that takes punishment.\n+5 Max Health"},
    {"id": "w_grit", "name": "Grit", "tier": 1, "type": "passive", "cost": 1,
     "prerequisites": [], "stat_bonuses": {"defense": 1},
     "description": "Sheer determination keeps you standing.\n+1 Defense"},

    # =========== TIER 2 - Foundation (7 nodes, 1 ability) ===========
    {"id": "w_iron_grip", "name": "Iron Grip", "tier": 2, "type": "passive", "cost": 1,
     "prerequisites": ["w_strong_arm"], "stat_bonuses": {"strength": 1},
     "description": "Your grip never falters.\n+1 Strength"},
    {"id": "w_toughened_body", "name": "Toughened Body", "tier": 2, "type": "passive", "cost": 1,
     "prerequisites": ["w_thick_skin"], "stat_bonuses": {"defense": 1, "constitution": 1},
     "description": "Battle scars have made you harder.\n+1 Defense, +1 Constitution"},
    {"id": "w_conditioning", "name": "Conditioning", "tier": 2, "type": "passive", "cost": 1,
     "prerequisites": ["w_endurance"], "stat_bonuses": {"health_max_bonus": 5, "constitution": 1},
     "description": "Rigorous training pays off.\n+5 Max Health, +1 Constitution"},
    {"id": "w_sharp_eye", "name": "Sharp Eye", "tier": 2, "type": "passive", "cost": 1,
     "prerequisites": ["w_battle_stance"], "stat_bonuses": {"perception": 1},
     "description": "A warrior must read the battlefield.\n+1 Perception"},
    {"id": "w_heavy_blows", "name": "Heavy Blows", "tier": 2, "type": "passive", "cost": 1,
     "prerequisites": ["w_battle_stance"], "stat_bonuses": {"strength": 2},
     "description": "Your strikes land with crushing force.\n+2 Strength"},
    {"id": "w_resilience", "name": "Resilience", "tier": 2, "type": "passive", "cost": 1,
     "prerequisites": ["w_sturdy_build", "w_grit"], "stat_bonuses": {"health_max_bonus": 5},
     "description": "You bounce back from anything.\n+5 Max Health"},
    {"id": "w_power_strike", "name": "Power Strike", "tier": 2, "type": "active", "cost": 1,
     "prerequisites": ["w_strong_arm"],
     "stat_bonuses": {},
     "ability": {"name": "Power Strike", "cooldown": 3, "effect": "combat_damage",
                 "value": 1.6, "combat": True,
                 "use_text": "You wind up and deliver a devastating blow!"},
     "description": "A mighty overhead strike.\nDeals 1.6x damage. Cooldown: 3 turns"},

    # =========== TIER 3 - Branching (7 nodes, 1 ability) ===========
    {"id": "w_shield_wall", "name": "Shield Wall", "tier": 3, "type": "passive", "cost": 1,
     "prerequisites": ["w_toughened_body"], "stat_bonuses": {"defense": 2},
     "description": "You use your shield like an extension of yourself.\n+2 Defense"},
    {"id": "w_vitality", "name": "Vitality", "tier": 3, "type": "passive", "cost": 1,
     "prerequisites": ["w_conditioning"], "stat_bonuses": {"health_max_bonus": 10, "constitution": 1},
     "description": "Life force surges through you.\n+10 Max Health, +1 Constitution"},
    {"id": "w_weapon_focus", "name": "Weapon Focus", "tier": 3, "type": "passive", "cost": 1,
     "prerequisites": ["w_iron_grip", "w_heavy_blows"], "stat_bonuses": {"strength": 2},
     "description": "Mastering a single weapon style.\n+2 Strength"},
    {"id": "w_armor_training", "name": "Armor Training", "tier": 3, "type": "passive", "cost": 1,
     "prerequisites": ["w_toughened_body", "w_resilience"], "stat_bonuses": {"defense": 1, "dexterity": 1},
     "description": "Move naturally in heavy armor.\n+1 Defense, +1 Dexterity"},
    {"id": "w_intimidate", "name": "Intimidating Presence", "tier": 3, "type": "passive", "cost": 1,
     "prerequisites": ["w_heavy_blows"], "stat_bonuses": {"charisma": 1, "strength": 1},
     "description": "Your sheer size unnerves others.\n+1 Charisma, +1 Strength"},
    {"id": "w_scouts_sense", "name": "Scout's Sense", "tier": 3, "type": "passive", "cost": 1,
     "prerequisites": ["w_sharp_eye"], "stat_bonuses": {"perception": 1, "dexterity": 1},
     "description": "Awareness honed by many ambushes.\n+1 Perception, +1 Dexterity"},
    {"id": "w_shield_bash", "name": "Shield Bash", "tier": 3, "type": "active", "cost": 1,
     "prerequisites": ["w_shield_wall"],
     "stat_bonuses": {},
     "ability": {"name": "Shield Bash", "cooldown": 4, "effect": "combat_stun",
                 "value": 0.8, "duration": 1, "combat": True,
                 "use_text": "You slam your shield into the enemy, stunning them!"},
     "description": "Bash with your shield.\nDeals 0.8x damage and stuns enemy for 1 turn.\nCooldown: 4 turns"},

    # =========== TIER 4 - Specialization (6 nodes, 1 ability) ===========
    {"id": "w_iron_will", "name": "Iron Will", "tier": 4, "type": "passive", "cost": 1,
     "prerequisites": ["w_vitality"], "stat_bonuses": {"constitution": 2},
     "description": "Your willpower sustains your body.\n+2 Constitution"},
    {"id": "w_fortress", "name": "Fortress", "tier": 4, "type": "passive", "cost": 2,
     "prerequisites": ["w_shield_wall", "w_armor_training"], "stat_bonuses": {"defense": 2, "health_max_bonus": 10},
     "description": "You ARE the wall.\n+2 Defense, +10 Max Health"},
    {"id": "w_brutal_strikes", "name": "Brutal Strikes", "tier": 4, "type": "passive", "cost": 1,
     "prerequisites": ["w_weapon_focus"], "stat_bonuses": {"strength": 2, "crit_chance_bonus": 0.05},
     "description": "Find weaknesses in enemy armor.\n+2 Strength, +5% Crit Chance"},
    {"id": "w_battle_scarred", "name": "Battle Scarred", "tier": 4, "type": "passive", "cost": 1,
     "prerequisites": ["w_armor_training"], "stat_bonuses": {"defense": 1, "constitution": 1},
     "description": "Every scar is a lesson learned.\n+1 Defense, +1 Constitution"},
    {"id": "w_commanding_voice", "name": "Commanding Voice", "tier": 4, "type": "passive", "cost": 1,
     "prerequisites": ["w_intimidate", "w_scouts_sense"], "stat_bonuses": {"charisma": 2, "perception": 1},
     "description": "Your voice carries authority.\n+2 Charisma, +1 Perception"},
    {"id": "w_war_cry", "name": "War Cry", "tier": 4, "type": "active", "cost": 2,
     "prerequisites": ["w_intimidate"],
     "stat_bonuses": {},
     "ability": {"name": "War Cry", "cooldown": 6, "effect": "buff_attack",
                 "value": 4, "duration": 3, "combat": True,
                 "use_text": "You let out a thundering war cry! Your attacks surge with power!"},
     "description": "A mighty shout that boosts your attack.\n+4 Strength for 3 turns. Cooldown: 6 turns"},

    # =========== TIER 5 - Mid-Tree (6 nodes, 1 ability) ===========
    {"id": "w_bulwark", "name": "Bulwark", "tier": 5, "type": "passive", "cost": 2,
     "prerequisites": ["w_fortress"], "stat_bonuses": {"defense": 3},
     "description": "An unbreakable defensive stance.\n+3 Defense"},
    {"id": "w_bloodlust", "name": "Bloodlust", "tier": 5, "type": "passive", "cost": 2,
     "prerequisites": ["w_brutal_strikes"], "stat_bonuses": {"strength": 3, "health_max_bonus": 5},
     "description": "The thrill of battle empowers you.\n+3 Strength, +5 Max Health"},
    {"id": "w_troll_blood", "name": "Troll Blood", "tier": 5, "type": "passive", "cost": 2,
     "prerequisites": ["w_iron_will", "w_battle_scarred"], "stat_bonuses": {"constitution": 2, "health_max_bonus": 10},
     "description": "Unnatural regenerative ability.\n+2 Constitution, +10 Max Health"},
    {"id": "w_trap_breaker", "name": "Trap Breaker", "tier": 5, "type": "passive", "cost": 1,
     "prerequisites": ["w_commanding_voice"], "stat_bonuses": {"perception": 2, "disarm_bonus": 0.10},
     "description": "You smash traps with brute force.\n+2 Perception, +10% Disarm Bonus"},
    {"id": "w_deep_wounds", "name": "Deep Wounds", "tier": 5, "type": "passive", "cost": 2,
     "prerequisites": ["w_brutal_strikes"], "stat_bonuses": {"strength": 2, "crit_chance_bonus": 0.05},
     "description": "Your strikes leave lingering wounds.\n+2 Strength, +5% Crit Chance"},
    {"id": "w_fortify", "name": "Fortify", "tier": 5, "type": "active", "cost": 2,
     "prerequisites": ["w_bulwark"],
     "stat_bonuses": {},
     "ability": {"name": "Fortify", "cooldown": 8, "effect": "temp_defense",
                 "value": 6, "duration": 4, "combat": True,
                 "use_text": "You plant your feet and brace yourself! Defense surges!"},
     "description": "Temporarily boost defense by 6 for 4 turns.\nCooldown: 8 turns"},

    # =========== TIER 6 - Advanced (5 nodes, 1 ability) ===========
    {"id": "w_juggernaut", "name": "Juggernaut", "tier": 6, "type": "passive", "cost": 2,
     "prerequisites": ["w_bulwark", "w_troll_blood"], "stat_bonuses": {"defense": 2, "constitution": 2},
     "description": "An unstoppable force.\n+2 Defense, +2 Constitution"},
    {"id": "w_berserker", "name": "Berserker", "tier": 6, "type": "passive", "cost": 2,
     "prerequisites": ["w_bloodlust", "w_deep_wounds"], "stat_bonuses": {"strength": 3, "crit_chance_bonus": 0.05},
     "description": "Rage fuels impossible strength.\n+3 Strength, +5% Crit Chance"},
    {"id": "w_second_wind", "name": "Second Wind", "tier": 6, "type": "passive", "cost": 2,
     "prerequisites": ["w_troll_blood"], "stat_bonuses": {"health_max_bonus": 15, "constitution": 1},
     "description": "When others fall, you rise.\n+15 Max Health, +1 Constitution"},
    {"id": "w_sunder_armor", "name": "Sunder Armor", "tier": 6, "type": "passive", "cost": 2,
     "prerequisites": ["w_deep_wounds"], "stat_bonuses": {"strength": 2},
     "description": "Your attacks reduce enemy defense.\nPassive: basic attacks have -1 enemy defense."},
    {"id": "w_cleave", "name": "Cleave", "tier": 6, "type": "active", "cost": 2,
     "prerequisites": ["w_berserker"],
     "stat_bonuses": {},
     "ability": {"name": "Cleave", "cooldown": 5, "effect": "combat_damage",
                 "value": 2.0, "combat": True,
                 "use_text": "You swing a devastating cleave!"},
     "description": "A massive 2.0x damage strike.\nCooldown: 5 turns"},

    # =========== TIER 7 - High (4 nodes, 1 ability) ===========
    {"id": "w_living_fortress", "name": "Living Fortress", "tier": 7, "type": "passive", "cost": 2,
     "prerequisites": ["w_juggernaut"], "stat_bonuses": {"defense": 3, "health_max_bonus": 10},
     "description": "Your body is harder than castle walls.\n+3 Defense, +10 Max Health"},
    {"id": "w_weapon_master", "name": "Weapon Master", "tier": 7, "type": "passive", "cost": 2,
     "prerequisites": ["w_berserker", "w_sunder_armor"], "stat_bonuses": {"strength": 3, "dexterity": 1},
     "description": "Every weapon is an extension of your will.\n+3 Strength, +1 Dexterity"},
    {"id": "w_unbreakable", "name": "Unbreakable", "tier": 7, "type": "passive", "cost": 2,
     "prerequisites": ["w_second_wind", "w_juggernaut"], "stat_bonuses": {"constitution": 3, "defense": 1},
     "description": "Nothing can break you.\n+3 Constitution, +1 Defense"},
    {"id": "w_rallying_cry", "name": "Rallying Cry", "tier": 7, "type": "active", "cost": 2,
     "prerequisites": ["w_second_wind"],
     "stat_bonuses": {},
     "ability": {"name": "Rallying Cry", "cooldown": 10, "effect": "combat_heal",
                 "value": 30, "combat": True,
                 "use_text": "Your battle cry rallies your spirit! You heal your wounds!"},
     "description": "Heal 30 HP through sheer willpower.\nCooldown: 10 turns"},

    # =========== TIER 8 - Elite (4 nodes, 1 ability) ===========
    {"id": "w_warlord", "name": "Warlord", "tier": 8, "type": "passive", "cost": 2,
     "prerequisites": ["w_weapon_master"], "stat_bonuses": {"strength": 3, "charisma": 2},
     "description": "You command the battlefield.\n+3 Strength, +2 Charisma"},
    {"id": "w_steel_body", "name": "Steel Body", "tier": 8, "type": "passive", "cost": 2,
     "prerequisites": ["w_living_fortress", "w_unbreakable"], "stat_bonuses": {"defense": 3, "constitution": 2},
     "description": "Your body is forged steel.\n+3 Defense, +2 Constitution"},
    {"id": "w_death_dealer", "name": "Death Dealer", "tier": 8, "type": "passive", "cost": 2,
     "prerequisites": ["w_weapon_master"], "stat_bonuses": {"strength": 2, "crit_chance_bonus": 0.08},
     "description": "Every strike could be the last.\n+2 Strength, +8% Crit Chance"},
    {"id": "w_earthquake", "name": "Earthquake", "tier": 8, "type": "active", "cost": 3,
     "prerequisites": ["w_living_fortress", "w_weapon_master"],
     "stat_bonuses": {},
     "ability": {"name": "Earthquake", "cooldown": 8, "effect": "combat_damage_stun",
                 "value": 1.8, "duration": 2, "combat": True,
                 "use_text": "You SLAM the ground! The earth itself trembles!"},
     "description": "Ground-shaking blow: 1.8x damage + stun 2 turns.\nCooldown: 8 turns"},

    # =========== TIER 9 - Master (3 nodes) ===========
    {"id": "w_titan_body", "name": "Titan's Body", "tier": 9, "type": "passive", "cost": 3,
     "prerequisites": ["w_steel_body"], "stat_bonuses": {"defense": 4, "constitution": 3, "health_max_bonus": 25},
     "description": "The body of a mythical titan.\n+4 Defense, +3 Constitution, +25 Max Health"},
    {"id": "w_executioner", "name": "Executioner", "tier": 9, "type": "passive", "cost": 3,
     "prerequisites": ["w_death_dealer", "w_warlord"], "stat_bonuses": {"strength": 4, "crit_chance_bonus": 0.10},
     "description": "Judge, jury, and executioner.\n+4 Strength, +10% Crit Chance"},
    {"id": "w_undying", "name": "Undying", "tier": 9, "type": "passive", "cost": 3,
     "prerequisites": ["w_steel_body", "w_warlord"], "stat_bonuses": {"health_max_bonus": 30, "constitution": 2, "defense": 2},
     "description": "No wound can keep you down.\n+30 Max Health, +2 Constitution, +2 Defense"},

    # =========== TIER 10 - Ultimate (2 nodes) ===========
    {"id": "w_titan_slam", "name": "Titan Slam", "tier": 10, "type": "active", "cost": 3,
     "prerequisites": ["w_executioner", "w_titan_body"],
     "stat_bonuses": {},
     "ability": {"name": "Titan Slam", "cooldown": 12, "effect": "combat_damage",
                 "value": 3.0, "combat": True,
                 "use_text": "You channel the power of a TITAN and bring your weapon down with CATACLYSMIC FORCE!"},
     "description": "ULTIMATE: A blow of godlike power.\n3.0x damage. Cooldown: 12 turns"},
    {"id": "w_immortal", "name": "Immortal", "tier": 10, "type": "passive", "cost": 3,
     "prerequisites": ["w_undying", "w_titan_body"],
     "stat_bonuses": {"strength": 5, "defense": 5, "constitution": 4, "health_max_bonus": 40},
     "description": "ULTIMATE PASSIVE: Transcend mortality.\n+5 Str, +5 Def, +4 Con, +40 Max HP"},
]


# =====================================================================
# ROGUE SKILL TREE  (55 nodes: ~47 passive, ~8 active)
# =====================================================================
# Branches: LEFT = Stealth/Evasion, RIGHT = Precision/Damage
# Abilities: backstab, poison, pickpocket, smoke bomb, assassinate, etc.
# =====================================================================

ROGUE_TREE = [
    # =========== TIER 1 - Entry (6 nodes) ===========
    {"id": "r_quick_hands", "name": "Quick Hands", "tier": 1, "type": "passive", "cost": 1,
     "prerequisites": [], "stat_bonuses": {"dexterity": 1},
     "description": "Fast fingers for fast work.\n+1 Dexterity"},
    {"id": "r_keen_eye", "name": "Keen Eye", "tier": 1, "type": "passive", "cost": 1,
     "prerequisites": [], "stat_bonuses": {"perception": 1},
     "description": "You notice what others miss.\n+1 Perception"},
    {"id": "r_light_step", "name": "Light Step", "tier": 1, "type": "passive", "cost": 1,
     "prerequisites": [], "stat_bonuses": {"dexterity": 1},
     "description": "Move without making a sound.\n+1 Dexterity"},
    {"id": "r_sharp_blade", "name": "Sharp Blade", "tier": 1, "type": "passive", "cost": 1,
     "prerequisites": [], "stat_bonuses": {"strength": 1},
     "description": "A well-maintained edge cuts deep.\n+1 Strength"},
    {"id": "r_street_smarts", "name": "Street Smarts", "tier": 1, "type": "passive", "cost": 1,
     "prerequisites": [], "stat_bonuses": {"charisma": 1},
     "description": "You know how the underworld works.\n+1 Charisma"},
    {"id": "r_survivalist", "name": "Survivalist", "tier": 1, "type": "passive", "cost": 1,
     "prerequisites": [], "stat_bonuses": {"constitution": 1},
     "description": "You know when to duck.\n+1 Constitution"},

    # =========== TIER 2 - Foundation (7 nodes, 1 ability) ===========
    {"id": "r_nimble_fingers", "name": "Nimble Fingers", "tier": 2, "type": "passive", "cost": 1,
     "prerequisites": ["r_quick_hands"], "stat_bonuses": {"dexterity": 1, "disarm_bonus": 0.05},
     "description": "Perfect finger control.\n+1 Dexterity, +5% Disarm"},
    {"id": "r_awareness", "name": "Awareness", "tier": 2, "type": "passive", "cost": 1,
     "prerequisites": ["r_keen_eye"], "stat_bonuses": {"perception": 1, "dexterity": 1},
     "description": "Always alert, always ready.\n+1 Perception, +1 Dexterity"},
    {"id": "r_silent_movement", "name": "Silent Movement", "tier": 2, "type": "passive", "cost": 1,
     "prerequisites": ["r_light_step"], "stat_bonuses": {"dexterity": 2},
     "description": "Ghost-like movement.\n+2 Dexterity"},
    {"id": "r_precise_strikes", "name": "Precise Strikes", "tier": 2, "type": "passive", "cost": 1,
     "prerequisites": ["r_sharp_blade"], "stat_bonuses": {"strength": 1, "crit_chance_bonus": 0.05},
     "description": "Strike where it hurts most.\n+1 Strength, +5% Crit Chance"},
    {"id": "r_silver_tongue", "name": "Silver Tongue", "tier": 2, "type": "passive", "cost": 1,
     "prerequisites": ["r_street_smarts"], "stat_bonuses": {"charisma": 2},
     "description": "Charm and deception flow naturally.\n+2 Charisma"},
    {"id": "r_dodge_roll", "name": "Dodge Roll", "tier": 2, "type": "passive", "cost": 1,
     "prerequisites": ["r_survivalist", "r_light_step"], "stat_bonuses": {"dexterity": 1, "defense": 1},
     "description": "Roll away from danger.\n+1 Dexterity, +1 Defense"},
    {"id": "r_backstab", "name": "Backstab", "tier": 2, "type": "active", "cost": 1,
     "prerequisites": ["r_sharp_blade"],
     "stat_bonuses": {},
     "ability": {"name": "Backstab", "cooldown": 3, "effect": "combat_crit_attack",
                 "value": 2.0, "combat": True,
                 "use_text": "You strike from the shadows - a critical hit!"},
     "description": "Guaranteed critical hit dealing 2.0x damage.\nCooldown: 3 turns"},

    # =========== TIER 3 - Branching (7 nodes, 1 ability) ===========
    {"id": "r_locksmith", "name": "Locksmith", "tier": 3, "type": "passive", "cost": 1,
     "prerequisites": ["r_nimble_fingers"], "stat_bonuses": {"dexterity": 1, "disarm_bonus": 0.10},
     "description": "Locks are just suggestions.\n+1 Dexterity, +10% Disarm Bonus"},
    {"id": "r_shadow_step", "name": "Shadow Step", "tier": 3, "type": "passive", "cost": 1,
     "prerequisites": ["r_silent_movement", "r_awareness"], "stat_bonuses": {"dexterity": 2, "perception": 1},
     "description": "Step through shadows like doorways.\n+2 Dexterity, +1 Perception"},
    {"id": "r_deadly_precision", "name": "Deadly Precision", "tier": 3, "type": "passive", "cost": 1,
     "prerequisites": ["r_precise_strikes"], "stat_bonuses": {"strength": 2, "crit_chance_bonus": 0.05},
     "description": "Every strike finds vital spots.\n+2 Strength, +5% Crit Chance"},
    {"id": "r_haggler", "name": "Haggler", "tier": 3, "type": "passive", "cost": 1,
     "prerequisites": ["r_silver_tongue"], "stat_bonuses": {"charisma": 2},
     "description": "Better prices everywhere.\n+2 Charisma"},
    {"id": "r_acrobatics", "name": "Acrobatics", "tier": 3, "type": "passive", "cost": 1,
     "prerequisites": ["r_dodge_roll"], "stat_bonuses": {"dexterity": 2, "defense": 1},
     "description": "Flip, roll, and tumble past danger.\n+2 Dexterity, +1 Defense"},
    {"id": "r_trap_sense", "name": "Trap Sense", "tier": 3, "type": "passive", "cost": 1,
     "prerequisites": ["r_awareness"], "stat_bonuses": {"perception": 2},
     "description": "An instinctive feel for hidden dangers.\n+2 Perception"},
    {"id": "r_poison_strike", "name": "Poison Strike", "tier": 3, "type": "active", "cost": 1,
     "prerequisites": ["r_precise_strikes"],
     "stat_bonuses": {},
     "ability": {"name": "Poison Strike", "cooldown": 4, "effect": "combat_poison",
                 "value": 4, "duration": 3, "combat": True,
                 "use_text": "Your envenomed blade bites deep! Poison courses through the enemy!"},
     "description": "Strike with a poisoned blade.\nDeals normal damage + 4 poison/turn for 3 turns.\nCooldown: 4 turns"},

    # =========== TIER 4 - Specialization (6 nodes, 1 ability) ===========
    {"id": "r_master_lockpick", "name": "Master Lockpick", "tier": 4, "type": "passive", "cost": 2,
     "prerequisites": ["r_locksmith"], "stat_bonuses": {"disarm_bonus": 0.15, "dexterity": 1},
     "description": "You can pick any lock.\n+15% Disarm Bonus, +1 Dexterity"},
    {"id": "r_shadow_dancer", "name": "Shadow Dancer", "tier": 4, "type": "passive", "cost": 2,
     "prerequisites": ["r_shadow_step"], "stat_bonuses": {"dexterity": 2, "defense": 2},
     "description": "Dance between the shadows.\n+2 Dexterity, +2 Defense"},
    {"id": "r_executioners_mark", "name": "Executioner's Mark", "tier": 4, "type": "passive", "cost": 2,
     "prerequisites": ["r_deadly_precision"], "stat_bonuses": {"strength": 2, "crit_chance_bonus": 0.05},
     "description": "Mark your targets for death.\n+2 Strength, +5% Crit Chance"},
    {"id": "r_fence", "name": "Fence", "tier": 4, "type": "passive", "cost": 1,
     "prerequisites": ["r_haggler"], "stat_bonuses": {"charisma": 2, "perception": 1},
     "description": "You know all the best fences.\n+2 Charisma, +1 Perception"},
    {"id": "r_ghost_walk", "name": "Ghost Walk", "tier": 4, "type": "passive", "cost": 1,
     "prerequisites": ["r_acrobatics", "r_trap_sense"], "stat_bonuses": {"dexterity": 1, "perception": 1},
     "description": "Walk through trapped halls undetected.\n+1 Dexterity, +1 Perception"},
    {"id": "r_smoke_bomb", "name": "Smoke Bomb", "tier": 4, "type": "active", "cost": 2,
     "prerequisites": ["r_shadow_step"],
     "stat_bonuses": {},
     "ability": {"name": "Smoke Bomb", "cooldown": 8, "effect": "guaranteed_flee",
                 "combat": True,
                 "use_text": "You hurl a smoke bomb! The room fills with thick smoke!"},
     "description": "Guaranteed escape from any non-boss combat.\nCooldown: 8 turns"},

    # =========== TIER 5 - Mid-Tree (6 nodes, 1 ability) ===========
    {"id": "r_vault_cracker", "name": "Vault Cracker", "tier": 5, "type": "passive", "cost": 2,
     "prerequisites": ["r_master_lockpick"], "stat_bonuses": {"disarm_bonus": 0.10, "perception": 2},
     "description": "No vault is safe from you.\n+10% Disarm, +2 Perception"},
    {"id": "r_blade_dancer", "name": "Blade Dancer", "tier": 5, "type": "passive", "cost": 2,
     "prerequisites": ["r_shadow_dancer", "r_executioners_mark"], "stat_bonuses": {"strength": 2, "dexterity": 2},
     "description": "A deadly dance of blades.\n+2 Strength, +2 Dexterity"},
    {"id": "r_lethality", "name": "Lethality", "tier": 5, "type": "passive", "cost": 2,
     "prerequisites": ["r_executioners_mark"], "stat_bonuses": {"strength": 3, "crit_chance_bonus": 0.05},
     "description": "Your strikes are lethal.\n+3 Strength, +5% Crit"},
    {"id": "r_con_artist", "name": "Con Artist", "tier": 5, "type": "passive", "cost": 1,
     "prerequisites": ["r_fence"], "stat_bonuses": {"charisma": 3},
     "description": "A master of deception.\n+3 Charisma"},
    {"id": "r_evasion", "name": "Evasion", "tier": 5, "type": "passive", "cost": 2,
     "prerequisites": ["r_ghost_walk", "r_shadow_dancer"], "stat_bonuses": {"dexterity": 3, "defense": 2},
     "description": "Untouchable.\n+3 Dexterity, +2 Defense"},
    {"id": "r_pickpocket", "name": "Pickpocket", "tier": 5, "type": "active", "cost": 2,
     "prerequisites": ["r_fence"],
     "stat_bonuses": {},
     "ability": {"name": "Pickpocket", "cooldown": 6, "effect": "extra_gold",
                 "value": 2.0, "duration": 1, "combat": True,
                 "use_text": "Your nimble fingers find extra treasures!"},
     "description": "Next enemy drops 2x gold.\nCooldown: 6 turns"},

    # =========== TIER 6 - Advanced (5 nodes, 1 ability) ===========
    {"id": "r_phantom_stride", "name": "Phantom Stride", "tier": 6, "type": "passive", "cost": 2,
     "prerequisites": ["r_evasion"], "stat_bonuses": {"dexterity": 3, "defense": 1, "perception": 1},
     "description": "You exist between moments.\n+3 Dexterity, +1 Defense, +1 Perception"},
    {"id": "r_assassins_edge", "name": "Assassin's Edge", "tier": 6, "type": "passive", "cost": 2,
     "prerequisites": ["r_lethality", "r_blade_dancer"], "stat_bonuses": {"strength": 3, "crit_chance_bonus": 0.08},
     "description": "The edge between life and death.\n+3 Strength, +8% Crit Chance"},
    {"id": "r_treasure_hunter", "name": "Treasure Hunter", "tier": 6, "type": "passive", "cost": 2,
     "prerequisites": ["r_vault_cracker", "r_con_artist"], "stat_bonuses": {"perception": 3, "charisma": 2},
     "description": "You find treasure everywhere.\n+3 Perception, +2 Charisma"},
    {"id": "r_vital_strike", "name": "Vital Strike", "tier": 6, "type": "passive", "cost": 2,
     "prerequisites": ["r_lethality"], "stat_bonuses": {"strength": 2, "crit_chance_bonus": 0.05},
     "description": "Aim for vital organs.\n+2 Strength, +5% Crit"},
    {"id": "r_vanish", "name": "Vanish", "tier": 6, "type": "active", "cost": 2,
     "prerequisites": ["r_phantom_stride"],
     "stat_bonuses": {},
     "ability": {"name": "Vanish", "cooldown": 10, "effect": "bypass_trap",
                 "duration": 3,
                 "use_text": "You melt into the shadows, becoming invisible!"},
     "description": "Bypass all traps for 3 moves.\nCooldown: 10 moves"},

    # =========== TIER 7 - High (4 nodes, 1 ability) ===========
    {"id": "r_death_from_shadows", "name": "Death From Shadows", "tier": 7, "type": "passive", "cost": 2,
     "prerequisites": ["r_assassins_edge", "r_phantom_stride"], "stat_bonuses": {"strength": 3, "dexterity": 2},
     "description": "Emerge from darkness to deliver death.\n+3 Strength, +2 Dexterity"},
    {"id": "r_untouchable", "name": "Untouchable", "tier": 7, "type": "passive", "cost": 2,
     "prerequisites": ["r_phantom_stride"], "stat_bonuses": {"dexterity": 3, "defense": 3},
     "description": "They can never hit you.\n+3 Dexterity, +3 Defense"},
    {"id": "r_kingpin", "name": "Kingpin", "tier": 7, "type": "passive", "cost": 2,
     "prerequisites": ["r_treasure_hunter"], "stat_bonuses": {"charisma": 3, "perception": 2},
     "description": "You run the underworld.\n+3 Charisma, +2 Perception"},
    {"id": "r_ambush", "name": "Ambush", "tier": 7, "type": "active", "cost": 2,
     "prerequisites": ["r_vital_strike", "r_assassins_edge"],
     "stat_bonuses": {},
     "ability": {"name": "Ambush", "cooldown": 5, "effect": "combat_bleed_attack",
                 "value": 1.5, "bleed": 5, "duration": 3, "combat": True,
                 "use_text": "You strike from hiding - the enemy bleeds profusely!"},
     "description": "Deal 1.5x damage + 5 bleed/turn for 3 turns.\nCooldown: 5 turns"},

    # =========== TIER 8 - Elite (4 nodes) ===========
    {"id": "r_shadow_lord", "name": "Shadow Lord", "tier": 8, "type": "passive", "cost": 2,
     "prerequisites": ["r_death_from_shadows", "r_untouchable"],
     "stat_bonuses": {"dexterity": 3, "strength": 2, "defense": 2},
     "description": "Lord of the shadows.\n+3 Dexterity, +2 Strength, +2 Defense"},
    {"id": "r_grand_larceny", "name": "Grand Larceny", "tier": 8, "type": "passive", "cost": 2,
     "prerequisites": ["r_kingpin"], "stat_bonuses": {"charisma": 3, "dexterity": 2},
     "description": "The greatest heist of all.\n+3 Charisma, +2 Dexterity"},
    {"id": "r_death_mark", "name": "Death Mark", "tier": 8, "type": "passive", "cost": 3,
     "prerequisites": ["r_death_from_shadows"], "stat_bonuses": {"strength": 3, "crit_chance_bonus": 0.10},
     "description": "Mark of certain death.\n+3 Strength, +10% Crit"},
    {"id": "r_perfect_evasion", "name": "Perfect Evasion", "tier": 8, "type": "passive", "cost": 3,
     "prerequisites": ["r_untouchable"], "stat_bonuses": {"dexterity": 4, "defense": 3},
     "description": "Absolute evasion mastery.\n+4 Dexterity, +3 Defense"},

    # =========== TIER 9 - Master (3 nodes) ===========
    {"id": "r_master_assassin", "name": "Master Assassin", "tier": 9, "type": "passive", "cost": 3,
     "prerequisites": ["r_death_mark", "r_shadow_lord"],
     "stat_bonuses": {"strength": 4, "dexterity": 3, "crit_chance_bonus": 0.10},
     "description": "Apex predator of the shadows.\n+4 Str, +3 Dex, +10% Crit"},
    {"id": "r_crime_lord", "name": "Crime Lord", "tier": 9, "type": "passive", "cost": 3,
     "prerequisites": ["r_grand_larceny", "r_shadow_lord"],
     "stat_bonuses": {"charisma": 4, "perception": 3, "dexterity": 2},
     "description": "The underworld bows to you.\n+4 Cha, +3 Perc, +2 Dex"},
    {"id": "r_ghost", "name": "Ghost", "tier": 9, "type": "passive", "cost": 3,
     "prerequisites": ["r_perfect_evasion"],
     "stat_bonuses": {"dexterity": 4, "defense": 4, "perception": 2},
     "description": "You don't exist.\n+4 Dex, +4 Def, +2 Perception"},

    # =========== TIER 10 - Ultimate (2 nodes) ===========
    {"id": "r_assassinate", "name": "Assassinate", "tier": 10, "type": "active", "cost": 3,
     "prerequisites": ["r_master_assassin"],
     "stat_bonuses": {},
     "ability": {"name": "Assassinate", "cooldown": 12, "effect": "combat_execute",
                 "value": 0.30, "combat": True,
                 "use_text": "You find the perfect opening and strike with lethal precision!"},
     "description": "ULTIMATE: Instant kill if enemy below 30% HP.\nOtherwise deals 3.0x damage.\nCooldown: 12 turns"},
    {"id": "r_phantom", "name": "Phantom", "tier": 10, "type": "passive", "cost": 3,
     "prerequisites": ["r_ghost", "r_master_assassin"],
     "stat_bonuses": {"dexterity": 5, "strength": 4, "perception": 4, "crit_chance_bonus": 0.15},
     "description": "ULTIMATE PASSIVE: Pure shadow given lethal form.\n+5 Dex, +4 Str, +4 Perc, +15% Crit"},
]


# =====================================================================
# MAGE SKILL TREE  (55 nodes: ~47 passive, ~8 active)
# =====================================================================
# Branches: LEFT = Defense/Healing, RIGHT = Offensive magic
# Abilities: fireball, ice shard, heal, arcane shield, thunder, reveal, etc.
# =====================================================================

MAGE_TREE = [
    # =========== TIER 1 - Entry (6 nodes) ===========
    {"id": "m_arcane_mind", "name": "Arcane Mind", "tier": 1, "type": "passive", "cost": 1,
     "prerequisites": [], "stat_bonuses": {"perception": 1},
     "description": "Your mind touches the arcane.\n+1 Perception"},
    {"id": "m_mana_well", "name": "Mana Well", "tier": 1, "type": "passive", "cost": 1,
     "prerequisites": [], "stat_bonuses": {"constitution": 1},
     "description": "A deep reservoir of magical energy.\n+1 Constitution"},
    {"id": "m_spark", "name": "Spark", "tier": 1, "type": "passive", "cost": 1,
     "prerequisites": [], "stat_bonuses": {"strength": 1},
     "description": "Even a spark can start a fire.\n+1 Strength (magic damage)"},
    {"id": "m_focus", "name": "Focus", "tier": 1, "type": "passive", "cost": 1,
     "prerequisites": [], "stat_bonuses": {"perception": 1},
     "description": "Mental clarity sharpens your magic.\n+1 Perception"},
    {"id": "m_mystic_charm", "name": "Mystic Charm", "tier": 1, "type": "passive", "cost": 1,
     "prerequisites": [], "stat_bonuses": {"charisma": 1},
     "description": "An aura of magical charisma.\n+1 Charisma"},
    {"id": "m_tough_robes", "name": "Tough Robes", "tier": 1, "type": "passive", "cost": 1,
     "prerequisites": [], "stat_bonuses": {"defense": 1},
     "description": "Enchanted robes that protect you.\n+1 Defense"},

    # =========== TIER 2 - Foundation (7 nodes, 1 ability) ===========
    {"id": "m_deep_pool", "name": "Deep Pool", "tier": 2, "type": "passive", "cost": 1,
     "prerequisites": ["m_mana_well"], "stat_bonuses": {"constitution": 1, "health_max_bonus": 5},
     "description": "Your life force deepens.\n+1 Constitution, +5 Max HP"},
    {"id": "m_arcane_attunement", "name": "Arcane Attunement", "tier": 2, "type": "passive", "cost": 1,
     "prerequisites": ["m_arcane_mind"], "stat_bonuses": {"perception": 2},
     "description": "Deeper connection to magical currents.\n+2 Perception"},
    {"id": "m_fire_affinity", "name": "Fire Affinity", "tier": 2, "type": "passive", "cost": 1,
     "prerequisites": ["m_spark"], "stat_bonuses": {"strength": 2},
     "description": "Flames answer your call eagerly.\n+2 Strength (magic damage)"},
    {"id": "m_concentration", "name": "Concentration", "tier": 2, "type": "passive", "cost": 1,
     "prerequisites": ["m_focus"], "stat_bonuses": {"perception": 1, "constitution": 1},
     "description": "Unwavering mental focus.\n+1 Perception, +1 Constitution"},
    {"id": "m_mystic_aura", "name": "Mystic Aura", "tier": 2, "type": "passive", "cost": 1,
     "prerequisites": ["m_mystic_charm"], "stat_bonuses": {"charisma": 2},
     "description": "Your magical presence impresses others.\n+2 Charisma"},
    {"id": "m_ward", "name": "Ward", "tier": 2, "type": "passive", "cost": 1,
     "prerequisites": ["m_tough_robes", "m_mana_well"], "stat_bonuses": {"defense": 1, "constitution": 1},
     "description": "A simple protective ward.\n+1 Defense, +1 Constitution"},
    {"id": "m_fireball", "name": "Fireball", "tier": 2, "type": "active", "cost": 1,
     "prerequisites": ["m_fire_affinity"],
     "stat_bonuses": {},
     "ability": {"name": "Fireball", "cooldown": 3, "effect": "combat_damage_burn",
                 "value": 1.5, "burn": 3, "duration": 2, "combat": True,
                 "use_text": "You hurl a blazing fireball! Flames engulf the enemy!"},
     "description": "Hurl a ball of fire.\n1.5x damage + 3 burn/turn for 2 turns.\nCooldown: 3 turns"},

    # =========== TIER 3 - Branching (7 nodes, 1 ability) ===========
    {"id": "m_arcane_shield", "name": "Arcane Shield", "tier": 3, "type": "passive", "cost": 1,
     "prerequisites": ["m_ward"], "stat_bonuses": {"defense": 2},
     "description": "A persistent magical barrier.\n+2 Defense"},
    {"id": "m_elemental_mastery", "name": "Elemental Mastery", "tier": 3, "type": "passive", "cost": 1,
     "prerequisites": ["m_fire_affinity"], "stat_bonuses": {"strength": 2},
     "description": "Command over the elements grows.\n+2 Strength (magic damage)"},
    {"id": "m_third_eye", "name": "Third Eye", "tier": 3, "type": "passive", "cost": 1,
     "prerequisites": ["m_arcane_attunement", "m_concentration"], "stat_bonuses": {"perception": 2, "dexterity": 1},
     "description": "See beyond the physical.\n+2 Perception, +1 Dexterity"},
    {"id": "m_enchanted_touch", "name": "Enchanted Touch", "tier": 3, "type": "passive", "cost": 1,
     "prerequisites": ["m_mystic_aura"], "stat_bonuses": {"charisma": 2, "crafting_bonus": 1},
     "description": "Your touched items gain magical properties.\n+2 Charisma, +1 Crafting Bonus"},
    {"id": "m_life_force", "name": "Life Force", "tier": 3, "type": "passive", "cost": 1,
     "prerequisites": ["m_deep_pool"], "stat_bonuses": {"constitution": 2, "health_max_bonus": 5},
     "description": "Deep reserves of life energy.\n+2 Constitution, +5 Max HP"},
    {"id": "m_flame_weave", "name": "Flame Weave", "tier": 3, "type": "passive", "cost": 1,
     "prerequisites": ["m_fire_affinity", "m_concentration"], "stat_bonuses": {"strength": 1, "perception": 1},
     "description": "Weave fire with precision.\n+1 Strength, +1 Perception"},
    {"id": "m_ice_shard", "name": "Ice Shard", "tier": 3, "type": "active", "cost": 1,
     "prerequisites": ["m_elemental_mastery"],
     "stat_bonuses": {},
     "ability": {"name": "Ice Shard", "cooldown": 4, "effect": "combat_freeze_attack",
                 "value": 1.2, "duration": 2, "combat": True,
                 "use_text": "You launch a razor-sharp ice shard! The cold seeps into the enemy!"},
     "description": "Ice projectile: 1.2x damage + freeze enemy (-30% attack) 2 turns.\nCooldown: 4 turns"},

    # =========== TIER 4 - Specialization (6 nodes, 1 ability) ===========
    {"id": "m_barrier", "name": "Barrier", "tier": 4, "type": "passive", "cost": 2,
     "prerequisites": ["m_arcane_shield", "m_life_force"], "stat_bonuses": {"defense": 2, "health_max_bonus": 10},
     "description": "A strong magical barrier.\n+2 Defense, +10 Max HP"},
    {"id": "m_pyromaniac", "name": "Pyromaniac", "tier": 4, "type": "passive", "cost": 2,
     "prerequisites": ["m_elemental_mastery", "m_flame_weave"], "stat_bonuses": {"strength": 3},
     "description": "Absolute mastery of fire.\n+3 Strength (magic damage)"},
    {"id": "m_divination", "name": "Divination", "tier": 4, "type": "passive", "cost": 1,
     "prerequisites": ["m_third_eye"], "stat_bonuses": {"perception": 3},
     "description": "See what is hidden from mortal eyes.\n+3 Perception"},
    {"id": "m_enchanting", "name": "Enchanting", "tier": 4, "type": "passive", "cost": 1,
     "prerequisites": ["m_enchanted_touch"], "stat_bonuses": {"charisma": 2, "crafting_bonus": 1},
     "description": "Imbue items with magic.\n+2 Charisma, +1 Crafting Bonus"},
    {"id": "m_resilient_ward", "name": "Resilient Ward", "tier": 4, "type": "passive", "cost": 1,
     "prerequisites": ["m_arcane_shield"], "stat_bonuses": {"defense": 1, "constitution": 2},
     "description": "Wards that strengthen over time.\n+1 Defense, +2 Constitution"},
    {"id": "m_heal", "name": "Heal", "tier": 4, "type": "active", "cost": 2,
     "prerequisites": ["m_life_force"],
     "stat_bonuses": {},
     "ability": {"name": "Heal", "cooldown": 5, "effect": "combat_heal",
                 "value": 35, "combat": True,
                 "use_text": "Golden light flows through you, mending your wounds!"},
     "description": "Restore 35 HP.\nCooldown: 5 turns"},

    # =========== TIER 5 - Mid-Tree (6 nodes, 1 ability) ===========
    {"id": "m_mage_armor", "name": "Mage Armor", "tier": 5, "type": "passive", "cost": 2,
     "prerequisites": ["m_barrier"], "stat_bonuses": {"defense": 3, "constitution": 1},
     "description": "Arcane energy reinforces your body.\n+3 Defense, +1 Constitution"},
    {"id": "m_inferno", "name": "Inferno", "tier": 5, "type": "passive", "cost": 2,
     "prerequisites": ["m_pyromaniac"], "stat_bonuses": {"strength": 3, "crit_chance_bonus": 0.05},
     "description": "Unleash devastating flames.\n+3 Strength, +5% Crit"},
    {"id": "m_seer", "name": "Seer", "tier": 5, "type": "passive", "cost": 2,
     "prerequisites": ["m_divination"], "stat_bonuses": {"perception": 2, "dexterity": 2},
     "description": "See moments before they happen.\n+2 Perception, +2 Dexterity"},
    {"id": "m_master_enchanter", "name": "Master Enchanter", "tier": 5, "type": "passive", "cost": 2,
     "prerequisites": ["m_enchanting"], "stat_bonuses": {"charisma": 3, "crafting_bonus": 1},
     "description": "A master of magical crafting.\n+3 Charisma, +1 Crafting Bonus"},
    {"id": "m_vitality_surge", "name": "Vitality Surge", "tier": 5, "type": "passive", "cost": 2,
     "prerequisites": ["m_barrier", "m_resilient_ward"], "stat_bonuses": {"health_max_bonus": 15, "constitution": 2},
     "description": "Life energy overflows.\n+15 Max HP, +2 Constitution"},
    {"id": "m_reveal", "name": "Reveal", "tier": 5, "type": "active", "cost": 2,
     "prerequisites": ["m_divination"],
     "stat_bonuses": {},
     "ability": {"name": "Reveal", "cooldown": 12, "effect": "reveal_floor",
                 "use_text": "Arcane symbols pulse outward... The floor's secrets are laid bare!"},
     "description": "Reveal ALL traps and secrets on current floor.\nCooldown: 12 moves"},

    # =========== TIER 6 - Advanced (5 nodes, 1 ability) ===========
    {"id": "m_arcane_fortress", "name": "Arcane Fortress", "tier": 6, "type": "passive", "cost": 2,
     "prerequisites": ["m_mage_armor", "m_vitality_surge"], "stat_bonuses": {"defense": 3, "health_max_bonus": 10},
     "description": "A fortress of pure magic.\n+3 Defense, +10 Max HP"},
    {"id": "m_firestorm", "name": "Firestorm", "tier": 6, "type": "passive", "cost": 2,
     "prerequisites": ["m_inferno"], "stat_bonuses": {"strength": 3, "crit_chance_bonus": 0.05},
     "description": "Rain fire from the sky.\n+3 Strength, +5% Crit"},
    {"id": "m_oracle", "name": "Oracle", "tier": 6, "type": "passive", "cost": 2,
     "prerequisites": ["m_seer"], "stat_bonuses": {"perception": 3, "dexterity": 1, "charisma": 1},
     "description": "The all-seeing oracle.\n+3 Perception, +1 Dexterity, +1 Charisma"},
    {"id": "m_grand_enchanter", "name": "Grand Enchanter", "tier": 6, "type": "passive", "cost": 2,
     "prerequisites": ["m_master_enchanter", "m_oracle"], "stat_bonuses": {"charisma": 3, "crafting_bonus": 2},
     "description": "Legendary enchanting prowess.\n+3 Charisma, +2 Crafting Bonus"},
    {"id": "m_thunder_strike", "name": "Thunder Strike", "tier": 6, "type": "active", "cost": 2,
     "prerequisites": ["m_firestorm"],
     "stat_bonuses": {},
     "ability": {"name": "Thunder Strike", "cooldown": 5, "effect": "combat_damage_stun",
                 "value": 2.0, "duration": 1, "combat": True,
                 "use_text": "LIGHTNING crashes down from above, striking the enemy!"},
     "description": "Lightning bolt: 2.0x damage + stun 1 turn.\nCooldown: 5 turns"},

    # =========== TIER 7 - High (4 nodes, 1 ability) ===========
    {"id": "m_spell_fortress", "name": "Spell Fortress", "tier": 7, "type": "passive", "cost": 2,
     "prerequisites": ["m_arcane_fortress"], "stat_bonuses": {"defense": 3, "constitution": 3},
     "description": "Impregnable magical defenses.\n+3 Defense, +3 Constitution"},
    {"id": "m_cataclysm", "name": "Cataclysm", "tier": 7, "type": "passive", "cost": 2,
     "prerequisites": ["m_firestorm"], "stat_bonuses": {"strength": 4, "crit_chance_bonus": 0.08},
     "description": "Apocalyptic magical power.\n+4 Strength, +8% Crit"},
    {"id": "m_sage", "name": "Sage's Wisdom", "tier": 7, "type": "passive", "cost": 2,
     "prerequisites": ["m_oracle", "m_grand_enchanter"], "stat_bonuses": {"perception": 3, "charisma": 2, "constitution": 2},
     "description": "Wisdom beyond mortal ken.\n+3 Perception, +2 Charisma, +2 Constitution"},
    {"id": "m_greater_heal", "name": "Greater Heal", "tier": 7, "type": "active", "cost": 2,
     "prerequisites": ["m_vitality_surge", "m_arcane_fortress"],
     "stat_bonuses": {},
     "ability": {"name": "Greater Heal", "cooldown": 8, "effect": "combat_heal",
                 "value": 60, "combat": True,
                 "use_text": "Brilliant golden light envelops you - your wounds close instantly!"},
     "description": "Restore 60 HP.\nCooldown: 8 turns"},

    # =========== TIER 8 - Elite (4 nodes) ===========
    {"id": "m_arcane_supremacy", "name": "Arcane Supremacy", "tier": 8, "type": "passive", "cost": 3,
     "prerequisites": ["m_spell_fortress", "m_cataclysm"],
     "stat_bonuses": {"strength": 3, "defense": 3, "constitution": 2},
     "description": "Supreme magical mastery.\n+3 Str, +3 Def, +2 Con"},
    {"id": "m_annihilation", "name": "Annihilation", "tier": 8, "type": "passive", "cost": 3,
     "prerequisites": ["m_cataclysm"], "stat_bonuses": {"strength": 4, "crit_chance_bonus": 0.10},
     "description": "Destructive power beyond measure.\n+4 Strength, +10% Crit"},
    {"id": "m_omniscience", "name": "Omniscience", "tier": 8, "type": "passive", "cost": 3,
     "prerequisites": ["m_sage"], "stat_bonuses": {"perception": 4, "charisma": 3, "dexterity": 2},
     "description": "Know all, see all.\n+4 Perception, +3 Charisma, +2 Dexterity"},
    {"id": "m_eternal_ward", "name": "Eternal Ward", "tier": 8, "type": "passive", "cost": 3,
     "prerequisites": ["m_spell_fortress"],
     "stat_bonuses": {"defense": 4, "constitution": 3, "health_max_bonus": 25},
     "description": "A ward that will never falter.\n+4 Defense, +3 Con, +25 Max HP"},

    # =========== TIER 9 - Master (3 nodes) ===========
    {"id": "m_divine_shield", "name": "Divine Shield", "tier": 9, "type": "passive", "cost": 3,
     "prerequisites": ["m_eternal_ward", "m_arcane_supremacy"],
     "stat_bonuses": {"defense": 5, "constitution": 4, "health_max_bonus": 30},
     "description": "God-like protection.\n+5 Defense, +4 Constitution, +30 Max HP"},
    {"id": "m_world_ender", "name": "World Ender", "tier": 9, "type": "passive", "cost": 3,
     "prerequisites": ["m_annihilation"],
     "stat_bonuses": {"strength": 5, "crit_chance_bonus": 0.12},
     "description": "Power to end worlds.\n+5 Strength, +12% Crit"},
    {"id": "m_all_knowing", "name": "All-Knowing", "tier": 9, "type": "passive", "cost": 3,
     "prerequisites": ["m_omniscience", "m_arcane_supremacy"],
     "stat_bonuses": {"perception": 4, "charisma": 3, "crafting_bonus": 3},
     "description": "Knowledge of all things.\n+4 Perc, +3 Cha, +3 Crafting"},

    # =========== TIER 10 - Ultimate (2 nodes) ===========
    {"id": "m_meteor", "name": "Meteor", "tier": 10, "type": "active", "cost": 3,
     "prerequisites": ["m_world_ender", "m_divine_shield"],
     "stat_bonuses": {},
     "ability": {"name": "Meteor", "cooldown": 12, "effect": "combat_damage_burn",
                 "value": 3.0, "burn": 8, "duration": 3, "combat": True,
                 "use_text": "You call down a METEOR FROM THE HEAVENS! The sky tears open with CATACLYSMIC FIRE!"},
     "description": "ULTIMATE: Call down a meteor.\n3.0x damage + 8 burn/turn for 3 turns.\nCooldown: 12 turns"},
    {"id": "m_transcendence", "name": "Transcendence", "tier": 10, "type": "passive", "cost": 3,
     "prerequisites": ["m_divine_shield", "m_all_knowing"],
     "stat_bonuses": {"strength": 5, "defense": 5, "constitution": 4, "perception": 4, "health_max_bonus": 40},
     "description": "ULTIMATE PASSIVE: Transcend mortal limits.\n+5 Str, +5 Def, +4 Con, +4 Perc, +40 Max HP"},
]


# =====================================================================
# SKILL TREES REGISTRY
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
        prereqs_met = all(p in unlocked for p in node.get("prerequisites", []))
        if not prereqs_met:
            continue
        if sp >= node["cost"]:
            available.append(node)

    return available


def unlock_skill(player, skill_id):
    """
    Unlock a skill node for the player.
    Returns: (success: bool, message: str)
    """
    class_id = player.stats.get("class", "")
    node = get_node_by_id(class_id, skill_id)

    if not node:
        return False, "Unknown skill."

    unlocked = set(get_unlocked_skills(player))

    if skill_id in unlocked:
        return False, f"{node['name']} is already unlocked."

    for prereq in node.get("prerequisites", []):
        if prereq not in unlocked:
            prereq_node = get_node_by_id(class_id, prereq)
            prereq_name = prereq_node["name"] if prereq_node else prereq
            return False, f"Requires: {prereq_name}"

    sp = player.stats.get("skill_points", 0)
    if sp < node["cost"]:
        return False, f"Need {node['cost']} skill point{'s' if node['cost'] > 1 else ''}, have {sp}."

    # Spend skill points
    player.stats["skill_points"] = sp - node["cost"]

    # Add to unlocked list
    if "unlocked_skills" not in player.state:
        player.state["unlocked_skills"] = []
    player.state["unlocked_skills"].append(skill_id)

    # Apply stat bonuses
    for stat, value in node.get("stat_bonuses", {}).items():
        if stat == "health_max_bonus":
            player.stats["health_max"] = player.stats.get("health_max", 100) + value
            player.stats["health"] = min(
                player.stats.get("health", 100) + value,
                player.stats.get("health_max", 100)
            )
        elif stat in ("crafting_bonus", "crit_chance_bonus", "disarm_bonus"):
            player.stats[stat] = player.stats.get(stat, 0) + value
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
        result += f"  Cooldown: {ability.get('cooldown', 0)} turns\n"
        if ability.get("combat"):
            result += "  Usable in combat!\n"
        cmd_name = ability.get('name', '').lower().replace(' ', '_')
        result += f"  Use: ability {cmd_name}\n"

    if node.get("stat_bonuses"):
        result += "\n  Stat changes:\n"
        for stat, val in node["stat_bonuses"].items():
            nice = stat.replace("_", " ").replace("health max bonus", "Max Health")
            nice = nice.replace("crit chance bonus", "Crit Chance")
            nice = nice.replace("crafting bonus", "Crafting Bonus")
            nice = nice.replace("disarm bonus", "Disarm Bonus")
            if isinstance(val, float):
                result += f"    {nice.capitalize()}: +{val:.0%}\n"
            else:
                result += f"    {nice.capitalize()}: +{val}\n"

    result += f"\n  Remaining skill points: {player.stats.get('skill_points', 0)}\n"
    result += "=" * 50 + "\n"

    return True, result


def get_active_abilities(player):
    """Return list of active ability dicts the player has unlocked."""
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
    """Attempt to use an active ability. Returns (success, message, ability_data)."""
    abilities = get_active_abilities(player)
    if not abilities:
        return False, "You don't have any active abilities yet.", None

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
        names = [a["name"] for a in abilities]
        return False, f"Unknown ability. Your abilities: {', '.join(names)}", None

    # Check cooldown
    cooldowns = player.state.get("cooldowns", {})
    cd_key = found["skill_id"]
    remaining = cooldowns.get(cd_key, 0)
    if remaining > 0:
        return False, f"{found['name']} is on cooldown ({remaining} turns remaining).", None

    # Activate the ability
    effect = found.get("effect", "")

    # Set cooldown
    if "cooldowns" not in player.state:
        player.state["cooldowns"] = {}
    player.state["cooldowns"][cd_key] = found.get("cooldown", 10)

    # Combat effects are returned to the engine for processing
    combat_effects = (
        "combat_damage", "combat_crit_attack", "combat_stun",
        "combat_poison", "combat_freeze_attack", "combat_damage_burn",
        "combat_damage_stun", "combat_heal", "combat_execute",
        "combat_bleed_attack", "guaranteed_flee", "buff_attack",
        "extra_gold"
    )

    if effect not in combat_effects:
        _apply_ability_effect(player, effect, found.get("duration", 1), found.get("value", 0))

    result = "\n" + "-" * 50 + "\n"
    result += f"  {found.get('use_text', 'You use ' + found['name'] + '!')}\n"
    result += f"  [{found['name']} active"
    if found.get("duration", 1) > 1:
        result += f" for {found['duration']} turns"
    result += "]\n"
    result += "-" * 50 + "\n"

    return True, result, found


def _apply_ability_effect(player, effect, duration, value):
    """Apply non-combat ability effects to the player state."""
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
        player.stats["health"] = min(hp + value, hp_max)
    elif effect == "reveal_floor":
        active_effects["reveal_floor"] = 1
    elif effect == "archmage_mode":
        active_effects["archmage_mode"] = duration
        active_effects["guaranteed_detection"] = duration

    player.state["active_effects"] = active_effects


def tick_effects(player):
    """
    Called after each player move to decrement durations.
    Also ticks cooldowns. Returns list of expiry messages.
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
            val["duration"] -= 1
            if val["duration"] <= 0:
                expired.append(key)
                if key == "defense_boost":
                    player.stats["defense"] = max(0, player.stats.get("defense", 0) - val.get("value", 0))
                    messages.append("  Your defense boost fades.")
                elif key == "attack_boost":
                    player.stats["strength"] = max(0, player.stats.get("strength", 0) - val.get("value", 0))
                    messages.append("  Your attack boost fades.")
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
        if key in active:
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
# GRAPHICAL SKILL TREE WINDOW (Tkinter Canvas with scrolling)
# =====================================================================

NODE_WIDTH = 100
NODE_HEIGHT = 42
TIER_SPACING_X = 145
NODE_SPACING_Y = 60
PADDING = 50

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
    organized by tier (left to right) with scrollbars.
    """

    def __init__(self, root, player, engine=None):
        self.root = root
        self.player = player
        self.engine = engine
        self.window = None
        self.canvas = None
        self.node_items = {}
        self.node_rects = {}
        self.tooltip = None
        self.tooltip_text = None
        self.info_frame = None
        self.info_label = None
        self.sp_label = None
        self._font = None

    def is_open(self):
        return self.window is not None and tk.Toplevel.winfo_exists(self.window)

    def create_window(self):
        if self.is_open():
            self.window.lift()
            self.window.focus_force()
            return

        self.window = tk.Toplevel(self.root)
        class_id = self.player.stats.get("class", "warrior")
        class_name = class_id.capitalize()
        self.window.title(f"Skill Tree - {class_name}")
        self.window.geometry("1200x750")
        self.window.configure(bg=COLOR_BG)
        self.window.resizable(True, True)

        self._font = tkfont.Font(family="Courier New", size=8)
        self._font_bold = tkfont.Font(family="Courier New", size=9, weight="bold")
        self._font_small = tkfont.Font(family="Courier New", size=7)

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
            (COLOR_UNLOCKED, "Passive"),
            (COLOR_ACTIVE_ABILITY, "Active Ability"),
        ]:
            tk.Canvas(legend_frame, width=12, height=12, bg=color,
                      highlightthickness=0).pack(side="left", padx=(6, 2))
            tk.Label(legend_frame, text=label, font=self._font_small,
                     bg=COLOR_BG, fg=COLOR_TEXT).pack(side="left", padx=(0, 4))

        # Scrollable canvas frame
        canvas_frame = tk.Frame(self.window, bg=COLOR_BG)
        canvas_frame.pack(fill="both", expand=True, padx=6, pady=6)

        self.canvas = tk.Canvas(canvas_frame, bg=COLOR_BG, highlightthickness=0)

        h_scroll = tk.Scrollbar(canvas_frame, orient="horizontal", command=self.canvas.xview)
        v_scroll = tk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)

        h_scroll.pack(side="bottom", fill="x")
        v_scroll.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Mouse wheel scrolling
        self.canvas.bind("<MouseWheel>",
                         lambda e: self.canvas.yview_scroll(-1 * (e.delta // 120), "units"))
        self.canvas.bind("<Shift-MouseWheel>",
                         lambda e: self.canvas.xview_scroll(-1 * (e.delta // 120), "units"))

        # Detail panel at bottom
        self.detail_frame = tk.Frame(self.window, bg="#2a2a2a", padx=10, pady=8)
        self.detail_frame.pack(fill="x")
        self.detail_label = tk.Label(
            self.detail_frame,
            text="Click a skill node for details. Click an available (blue) node to unlock it.",
            font=self._font, bg="#2a2a2a", fg="#aaaaaa",
            wraplength=1100, justify="left"
        )
        self.detail_label.pack(fill="x")

        self._draw_tree()

        self.canvas.bind("<Button-1>", self._on_click)
        self.canvas.bind("<Motion>", self._on_hover)
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)

    def close_window(self):
        if self.window:
            try:
                self.window.destroy()
            except Exception:
                pass
        self.window = None
        self.canvas = None

    def _draw_tree(self):
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
            self.canvas.create_text(400, 300, text="No skill tree available.",
                                    font=self._font_bold, fill=COLOR_TEXT)
            return

        # Group by tier
        tiers = {}
        for node in tree:
            t = node["tier"]
            if t not in tiers:
                tiers[t] = []
            tiers[t].append(node)

        max_tier = max(tiers.keys()) if tiers else 1
        max_nodes_in_tier = max(len(v) for v in tiers.values()) if tiers else 1

        canvas_width = PADDING * 2 + max_tier * TIER_SPACING_X + NODE_WIDTH
        canvas_height = PADDING * 2 + max_nodes_in_tier * NODE_SPACING_Y + 40

        # Calculate positions
        positions = {}
        for tier_num, nodes in sorted(tiers.items()):
            x = PADDING + (tier_num - 1) * TIER_SPACING_X
            n_nodes = len(nodes)
            total_height = (n_nodes - 1) * NODE_SPACING_Y
            start_y = PADDING + 30 + (canvas_height - PADDING * 2 - 30 - total_height) / 2

            # Tier label
            self.canvas.create_text(
                x + NODE_WIDTH // 2, PADDING,
                text=f"T{tier_num}",
                font=self._font_small, fill=COLOR_TIER_LABEL
            )

            for i, node in enumerate(nodes):
                cx = x + NODE_WIDTH // 2
                cy = start_y + i * NODE_SPACING_Y + NODE_HEIGHT // 2
                positions[node["id"]] = (cx, cy)

        self.canvas.configure(scrollregion=(0, 0, canvas_width, canvas_height))

        # Draw connections
        for node in tree:
            if node["id"] not in positions:
                continue
            cx, cy = positions[node["id"]]
            for prereq_id in node.get("prerequisites", []):
                if prereq_id in positions:
                    px, py = positions[prereq_id]
                    both_unlocked = node["id"] in unlocked and prereq_id in unlocked
                    line_color = COLOR_LINE_UNLOCKED if both_unlocked else COLOR_LINE
                    self.canvas.create_line(
                        px + NODE_WIDTH // 2 - 3, py,
                        cx - NODE_WIDTH // 2 + 3, cy,
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

            if node["id"] in unlocked:
                color = COLOR_ACTIVE_ABILITY if node["type"] == "active" else COLOR_UNLOCKED
            elif node["id"] in available_ids:
                color = COLOR_AVAILABLE
            else:
                color = COLOR_LOCKED

            rect_id = self.canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=color, outline="#ffffff", width=1, tags=("node",)
            )

            display_name = node["name"]
            if len(display_name) > 13:
                words = display_name.split()
                if len(words) > 1:
                    mid = len(words) // 2
                    display_name = " ".join(words[:mid]) + "\n" + " ".join(words[mid:])

            text_id = self.canvas.create_text(
                cx, cy - 4,
                text=display_name,
                font=self._font_small, fill=COLOR_TEXT,
                width=NODE_WIDTH - 8, justify="center", tags=("node",)
            )

            type_text = "A" if node["type"] == "active" else "P"
            cost_text = f"[{type_text}] {node['cost']}SP"
            self.canvas.create_text(
                cx, y2 - 8,
                text=cost_text,
                font=self._font_small, fill="#cccccc", tags=("node",)
            )

            self.node_items[rect_id] = node["id"]
            self.node_items[text_id] = node["id"]
            self.node_rects[node["id"]] = (rect_id, text_id)

    def _on_click(self, event):
        cx = self.canvas.canvasx(event.x)
        cy = self.canvas.canvasy(event.y)
        items = self.canvas.find_overlapping(cx - 2, cy - 2, cx + 2, cy + 2)
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
            info = f"[UNLOCKED] {node['name']}\n{node['description']}"
            if node["type"] == "active":
                ab = node.get("ability", {})
                cd = self.player.state.get("cooldowns", {}).get(node_id, 0)
                info += f"\nCooldown: {'Ready!' if cd == 0 else f'{cd} turns'}"
                if ab.get("combat"):
                    info += "  |  Combat ability"
            self.detail_label.config(text=info)
            return

        available_ids = {n["id"] for n in get_available_skills(self.player)}
        if node_id not in available_ids:
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

        success, msg = unlock_skill(self.player, node_id)
        if success:
            self.detail_label.config(text=f"UNLOCKED: {node['name']}!")
            self._draw_tree()
            self.sp_label.config(
                text=f"Skill Points: {self.player.stats.get('skill_points', 0)}"
            )
            if self.engine and hasattr(self.engine, 'display_message'):
                self.engine.display_message(msg)
        else:
            self.detail_label.config(text=msg)

    def _on_hover(self, event):
        cx = self.canvas.canvasx(event.x)
        cy = self.canvas.canvasy(event.y)
        items = self.canvas.find_overlapping(cx - 2, cy - 2, cx + 2, cy + 2)
        node_id = None
        for item_id in items:
            if item_id in self.node_items:
                node_id = self.node_items[item_id]
                break

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

        unlocked = set(get_unlocked_skills(self.player))
        available = {n["id"] for n in get_available_skills(self.player)}
        status = "UNLOCKED" if node_id in unlocked else "AVAILABLE" if node_id in available else "LOCKED"
        tip = f"{node['name']} [{status}]"

        tx = cx + 15
        ty = cy - 15
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
        if not self.is_open():
            return
        self._draw_tree()
        self.sp_label.config(
            text=f"Skill Points: {self.player.stats.get('skill_points', 0)}"
        )
