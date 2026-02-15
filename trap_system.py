"""
Trap System for Text-Based Dungeon
Handles trap placement, triggering, disarming, and effects.

This module is the single source of truth for all trap-related data:
  - TRAP_TYPES: definitions for every trap type
  - BLOCKING_TRAP_TYPES: traps that prevent movement until dealt with
  - SUBTLE_HINTS: atmospheric flavour text per trap type
  - DISARM_CHALLENGES: choice-based disarm minigame data
  - DISARM_SUCCESS_RATES: base success rates by difficulty

The GameEngine (engine.py) imports these constants and handles runtime
behaviour (detection, triggering, minigame flow, poison ticks).
The DungeonGenerator (dungeon_generator.py) uses add_traps_to_floor()
during world generation.
"""

import random


class TrapSystem:
    """
    Text-based trap system with chance-based triggers and disarming mechanics.
    """
    
    # ── Trap type definitions ──────────────────────────────────────────
    TRAP_TYPES = {
        "spike_trap": {
            "name": "Hidden Spike Trap",
            "description": "Sharp spikes suddenly shoot up from the floor!",
            "trigger_chance": 0.30,
            "damage": (10, 25),
            "disarm_difficulty": "medium",
            "warning_signs": "You notice scratches on the floor and suspicious holes."
        },
        "poison_dart": {
            "name": "Poison Dart Trap",
            "description": "A dart shoots from the wall and strikes you!",
            "trigger_chance": 0.25,
            "damage": (5, 15),
            "poison_damage": 3,
            "poison_duration": 3,
            "disarm_difficulty": "hard",
            "warning_signs": "You see tiny holes in the walls.",
            "disarm_tools": ["lockpick_set"]
        },
        "pit_trap": {
            "name": "Concealed Pit",
            "description": "The floor gives way beneath you! You fall into a pit!",
            "trigger_chance": 0.20,
            "damage": (15, 30),
            "disarm_difficulty": "easy",
            "warning_signs": "The floor sounds hollow here.",
            "disarm_tools": ["rope_coil"],
            "blocking": True
        },
        "gas_trap": {
            "name": "Poison Gas Trap",
            "description": "Noxious gas fills the room!",
            "trigger_chance": 0.15,
            "damage": (8, 20),
            "area_effect": True,
            "disarm_difficulty": "hard",
            "warning_signs": "You smell something faint and chemical.",
            "disarm_tools": ["lockpick_set"]
        },
        "crushing_ceiling": {
            "name": "Crushing Ceiling Trap",
            "description": "The ceiling begins descending rapidly!",
            "trigger_chance": 0.10,
            "damage": (20, 40),
            "escape_difficulty": "medium",
            "warning_signs": "The ceiling has strange grooves and mechanisms.",
            "disarm_tools": ["iron_key"],
            "blocking": True
        },
        "magic_rune": {
            "name": "Magical Rune Trap",
            "description": "Ancient runes flare to life, releasing magical energy!",
            "trigger_chance": 0.20,
            "damage": (12, 28),
            "magic_damage": True,
            "disarm_difficulty": "very_hard",
            "warning_signs": "Glowing symbols are carved into the floor.",
            "disarm_tools": ["spell_scroll"]
        }
    }
    
    # ── Blocking traps ─────────────────────────────────────────────────
    # These trap types prevent movement out of the room until disarmed/triggered
    BLOCKING_TRAP_TYPES = {"pit_trap", "crushing_ceiling"}
    
    # ── Atmospheric / subtle hints ─────────────────────────────────────
    # Shown even when the trap is NOT fully detected (70 % chance)
    SUBTLE_HINTS = {
        "spike_trap": [
            "The floor has strange scratch marks...",
            "You feel an odd draft coming from below the floorboards.",
        ],
        "poison_dart": [
            "You notice tiny holes in the walls, barely visible.",
            "There's a faint chemical smell in the air.",
        ],
        "pit_trap": [
            "The floor sounds hollow beneath your feet.",
            "Some of the tiles seem looser than others.",
        ],
        "gas_trap": [
            "You detect a faint, acrid odor.",
            "The air feels thicker here, slightly harder to breathe.",
        ],
        "crushing_ceiling": [
            "You notice grooves cut into the ceiling above.",
            "The walls have deep vertical tracks running along them.",
        ],
        "magic_rune": [
            "Faint symbols on the floor seem to shimmer briefly.",
            "You feel a tingling sensation on your skin.",
        ],
    }
    
    # ── Disarm minigame challenges ─────────────────────────────────────
    DISARM_CHALLENGES = {
        "spike_trap": {
            "description": "The spike mechanism has three visible components. Which do you target?",
            "options": [
                "Jam the spring mechanism with your tool",
                "Cut the trigger wire near the floor plate",
                "Bend the spikes themselves to be harmless",
            ],
            "correct": 2,
        },
        "poison_dart": {
            "description": "The dart launcher has tiny tubes in the wall. How do you disable it?",
            "options": [
                "Block the tubes with cloth and wax",
                "Trigger all darts from a safe distance",
                "Carefully remove the pressure plate trigger",
            ],
            "correct": 3,
        },
        "pit_trap": {
            "description": "A concealed pit stretches across the path. How do you neutralize it?",
            "options": [
                "Tie a rope across to create a safe crossing",
                "Trigger the pit and wedge it open with your tool",
                "Find the locking mechanism and secure the floor tiles",
            ],
            "correct": 1,
        },
        "gas_trap": {
            "description": "You see gas nozzles hidden in crevices. What's your approach?",
            "options": [
                "Plug each nozzle with wax and cloth",
                "Find and close the main gas valve",
                "Light a torch to burn off the gas safely",
            ],
            "correct": 2,
        },
        "crushing_ceiling": {
            "description": "The ceiling mechanism runs on massive gears. Which approach?",
            "options": [
                "Jam the main gear with an iron wedge",
                "Cut the chains holding the counterweight",
                "Find the keyhole and lock the mechanism in place",
            ],
            "correct": 3,
        },
        "magic_rune": {
            "description": "Glowing runes form a magical circle on the floor. How do you dispel it?",
            "options": [
                "Break the circle by scratching through one rune",
                "Channel counter-magic through your spell scroll",
                "Pour water over the runes to wash them away",
            ],
            "correct": 2,
        },
    }
    
    DISARM_CHALLENGE_DEFAULT = {
        "description": "The trap's mechanism is exposed. How do you disarm it?",
        "options": [
            "Carefully cut the main trigger wire",
            "Jam the mechanism with your tool",
            "Disassemble the trigger plate",
        ],
        "correct": 1,
    }
    
    # ── Disarm success rates ───────────────────────────────────────────
    DISARM_SUCCESS_RATES = {
        "easy": 0.70,
        "medium": 0.50,
        "hard": 0.30,
        "very_hard": 0.15
    }
    
    def __init__(self):
        """Initialize trap system."""
        pass
    
    # ── Utility: find raw room inside dungeon data ─────────────────────
    @staticmethod
    def find_raw_room(dungeon_instance, room_id):
        """Return the raw room dict for *room_id* from the active dungeon,
        or None if the room is not found or no dungeon is active."""
        if dungeon_instance and dungeon_instance.dungeon_data:
            for _fnum, fdata in dungeon_instance.dungeon_data.get("floors", {}).items():
                if room_id in fdata.get("rooms", {}):
                    return fdata["rooms"][room_id]
        return None
    
    @classmethod
    def get_disarm_challenge(cls, trap_type):
        """Return a *copy* of the disarm challenge for *trap_type*."""
        challenge = cls.DISARM_CHALLENGES.get(trap_type, cls.DISARM_CHALLENGE_DEFAULT).copy()
        challenge["options"] = list(challenge["options"])
        return challenge
    
    def add_traps_to_floor(self, floor_data, floor_number):
        """
        Adds traps to some rooms on a floor.
        Trap frequency increases with floor depth.
        
        Args:
            floor_data: Dict containing floor information and rooms
            floor_number: Which floor (1-4)
            
        Returns:
            dict: Updated floor_data with traps added
        """
        num_rooms = len(floor_data.get("rooms", {}))
        
        # Trap probability per room based on floor
        trap_chance_per_room = {
            1: 0.15,  # 15% of rooms
            2: 0.25,  # 25% of rooms
            3: 0.35,  # 35% of rooms
            4: 0.50   # 50% of rooms (final floor)
        }
        
        chance = trap_chance_per_room.get(floor_number, 0.20)
        
        for room_id, room in floor_data.get("rooms", {}).items():
            if random.random() < chance:
                # Don't trap entrance room
                if room_id == floor_data.get("entrance_room"):
                    continue
                
                # Select trap type
                trap_type = random.choice(list(self.TRAP_TYPES.keys()))
                trap_data = self.TRAP_TYPES[trap_type].copy()
                trap_data["type"] = trap_type
                trap_data["triggered"] = False
                trap_data["disarmed"] = False
                
                if "traps" not in room:
                    room["traps"] = []
                
                room["traps"].append(trap_data)
        
        return floor_data
    
    # ── Description helpers ────────────────────────────────────────────
    
    def get_trap_description(self, trap):
        """
        Get a text description of a trap for the player.
        
        Args:
            trap: Trap dict
            
        Returns:
            str: Formatted description
        """
        if trap.get("disarmed"):
            return f"A disarmed {trap.get('name', 'trap')} is visible in the floor."
        
        if trap.get("triggered"):
            return f"The remnants of a triggered {trap.get('name', 'trap')} are visible."
        
        return f"You spot a {trap.get('name', 'trap')}! (Armed)"
    
    def get_warning_message(self, trap):
        """
        Get warning message for a trap.
        
        Args:
            trap: Trap dict
            
        Returns:
            str: Warning message
        """
        return f"⚠ {trap.get('warning_signs', 'Something feels off about this room.')}"
