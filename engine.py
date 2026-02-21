import json
import os
import sys


# =====================================================================
# SHOP SYSTEM INITIALIZATION
# =====================================================================
try:
	from shop_system import Shop, Shopkeeper, ShopUI
	SHOP_AVAILABLE = True
except Exception as e:
	SHOP_AVAILABLE = False
	print(f"[INIT] ⚠ Shop system DISABLED: {e}")

# =====================================================================
# TRAP SYSTEM INITIALIZATION
# =====================================================================
try:
	from trap_system import TrapSystem
	TRAP_AVAILABLE = True
except Exception as e:
	TRAP_AVAILABLE = False
	print(f"[INIT] ⚠ Trap system DISABLED: {e}")

# =====================================================================
# DUNGEON SYSTEM INITIALIZATION
# =====================================================================
# DUNGEON_AVAILABLE is set to True ONLY if all dungeon modules import
# successfully. Each module is tested independently to provide clear
# diagnostics if something fails. This is set at module load time and
# never changes after initialization.
# =====================================================================

DUNGEON_AVAILABLE: bool = False
_DUNGEON_IMPORT_ERROR: str = ""

try:
	# Test dungeon_scheduler module first
	try:
		from dungeon_scheduler import DungeonScheduler, get_scheduler
	except Exception as e:
		raise ImportError(f"Failed to import dungeon_scheduler: {type(e).__name__}: {e}")
	
	# Test dungeon_instance module second
	try:
		from dungeon_instance import get_current_dungeon, DungeonInstance
	except Exception as e:
		raise ImportError(f"Failed to import dungeon_instance: {type(e).__name__}: {e}")
	
	# If we got here, both modules loaded successfully
	DUNGEON_AVAILABLE = True
	print("[INIT] [SUCCESS] Dungeon system initialized (imports successful)")
	
except ImportError as e:
	# One or both dungeon modules failed to import
	DUNGEON_AVAILABLE = False
	_DUNGEON_IMPORT_ERROR = str(e)
	print(f"[INIT] [WARNING] Dungeon system DISABLED: {_DUNGEON_IMPORT_ERROR}")

# Map and debug system imports
try:
	from live_map_window import LiveMapWindow
	MAP_AVAILABLE = True
except ImportError:
	MAP_AVAILABLE = False

try:
	from searchable_items_window import SearchableItemsWindow
	ITEMS_WINDOW_AVAILABLE = True
except ImportError:
	ITEMS_WINDOW_AVAILABLE = False

try:
	from debug_commands import handle_debug_commands, show_player_commands
	DEBUG_AVAILABLE = True
except ImportError:
	DEBUG_AVAILABLE = False

# =====================================================================
# ITEM EFFECTS SYSTEM INITIALIZATION
# =====================================================================
try:
	from item_effects import ItemEffects
	ITEM_EFFECTS_AVAILABLE = True
except Exception as e:
	ITEM_EFFECTS_AVAILABLE = False
	print(f"[INIT] ⚠ Item effects system DISABLED: {e}")

# =====================================================================
# CRAFTING SYSTEM INITIALIZATION
# =====================================================================
try:
	from crafting_system import CraftingSystem
	CRAFTING_AVAILABLE = True
except Exception as e:
	CRAFTING_AVAILABLE = False
	print(f"[INIT] ⚠ Crafting system DISABLED: {e}")

# =====================================================================
# PROGRESSION SYSTEM INITIALIZATION
# =====================================================================
try:
	from progression_system import (
		award_xp, check_level_up, apply_class, get_class_selection_text,
		get_stat_modifier, XP_AWARDS, CLASS_DEFINITIONS
	)
	from skill_tree import (
		SkillTreeWindow, get_tree_for_class, get_unlocked_skills,
		get_available_skills, get_active_abilities, unlock_skill,
		use_ability, tick_effects, has_active_effect,
		is_skill_unlocked, get_node_by_id,
		get_synergy_bonuses, get_branch_counts, apply_synergy_bonuses,
		_apply_ability_effect
	)
	PROGRESSION_AVAILABLE = True
except Exception as e:
	PROGRESSION_AVAILABLE = False
	print(f"[INIT] Warning: Progression system DISABLED: {e}")

# =====================================================================
# EQUIPMENT SYSTEM INITIALIZATION
# =====================================================================
try:
	from equipment_system import (
		EQUIPMENT_DATABASE, EQUIPMENT_SLOTS,
		equip_item, unequip_item, get_equipment_display,
		get_total_equipment_bonuses, get_attack_power, get_defense_power
	)
	EQUIPMENT_AVAILABLE = True
except Exception as e:
	EQUIPMENT_AVAILABLE = False
	print(f"[INIT] ⚠ Equipment system DISABLED: {e}")

# =====================================================================
# COMBAT SYSTEM INITIALIZATION
# =====================================================================
try:
	from combat_system import (
		CombatState, ENEMY_DATABASE, BOSS_DATABASE, MINI_BOSS_DATABASE,
		process_player_attack, process_player_defend, process_player_flee,
		process_ability_in_combat,
		get_combat_status, generate_victory_result,
		get_enemies_for_dungeon, get_boss_for_dungeon, get_mini_boss_for_dungeon,
		should_spawn_enemy, create_enemy_instance, create_boss_instance,
		create_mini_boss_instance,
		ENEMY_SPAWN_CHANCE, DUNGEON_BOSS_MAP, DUNGEON_MINI_BOSS_MAP
	)
	COMBAT_AVAILABLE = True
except Exception as e:
	COMBAT_AVAILABLE = False
	print(f"[INIT] ⚠ Combat system DISABLED: {e}")

# =====================================================================
# NPC SYSTEM INITIALIZATION
# =====================================================================
try:
	from npc_system import NPCManager
	NPC_AVAILABLE = True
except Exception as e:
	NPC_AVAILABLE = False
	print(f"[INIT] ⚠ NPC system DISABLED: {e}")

# =====================================================================
# QUEST SYSTEM INITIALIZATION
# =====================================================================
try:
	from quest_system import QuestManager, QUEST_DATABASE
	QUEST_AVAILABLE = True
except Exception as e:
	QUEST_AVAILABLE = False
	print(f"[INIT] ⚠ Quest system DISABLED: {e}")

# =====================================================================
# NPC REPUTATION SYSTEM INITIALIZATION
# =====================================================================
try:
	from npc_reputation import ReputationManager
	NPC_REP_AVAILABLE = True
except Exception as e:
	NPC_REP_AVAILABLE = False
	print(f"[INIT] ⚠ NPC reputation system DISABLED: {e}")

# =====================================================================
# ACHIEVEMENT SYSTEM INITIALIZATION
# =====================================================================
try:
	from achievement_system import (
		check_achievements, track_event, get_achievements_display,
		format_achievement_unlock, ACHIEVEMENTS
	)
	ACHIEVEMENT_AVAILABLE = True
except Exception as e:
	ACHIEVEMENT_AVAILABLE = False
	print(f"[INIT] ⚠ Achievement system DISABLED: {e}")

# =====================================================================
# OVERWORLD ENCOUNTER SYSTEM INITIALIZATION
# =====================================================================
try:
	from overworld_encounters import OverworldEncounterManager
	OVERWORLD_AVAILABLE = True
except Exception as e:
	OVERWORLD_AVAILABLE = False
	print(f"[INIT] ⚠ Overworld encounters DISABLED: {e}")

# =====================================================================
# FISHING SYSTEM INITIALIZATION
# =====================================================================
try:
	from fishing_system import FishingMinigame, COOKED_FOOD_EFFECTS, FISH_COOKING_RECIPES, BAIT_TYPES
	FISHING_AVAILABLE = True
except Exception as e:
	FISHING_AVAILABLE = False
	print(f"[INIT] ⚠ Fishing system DISABLED: {e}")

# =====================================================================
# ENCHANTING SYSTEM INITIALIZATION
# =====================================================================
try:
	from enchanting_system import EnchantingSystem
	ENCHANTING_AVAILABLE = True
except Exception as e:
	ENCHANTING_AVAILABLE = False
	print(f"[INIT] ⚠ Enchanting system DISABLED: {e}")

WORLD_FILE  = os.path.join(os.path.dirname(__file__), "world.json")
SAVE_FILE   = os.path.join(os.path.dirname(__file__), "savegame.json")
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")

CONFIG_DEFAULTS = {
    "visual": {
        "colors": {
            "combat":   "#FF6B6B",
            "item":     "#98FB98",
            "dialogue": "#87CEEB",
            "status":   "#87CEFA",
            "warning":  "#FFD700",
            "system":   "#DA70D6",
            "command":  "#AAAAAA",
            "default":  "#DCDCDC",
        },
        "bg_color":    "#1e1e1e",
        "fg_color":    "#dcdcdc",
        "font_family": "Courier New",
        "font_size":   10,
        "theme":       "dark",
    },
    "gameplay": {
        "combat_speed":        "normal",
        "scroll_mode":         "auto",
        "confirm_dangerous":   True,
        "difficulty_modifier": 1.0,
    },
    "accessibility": {
        "high_contrast": False,
        "text_size":     10,
    },
    "ui": {
        "timestamps":   False,
        "max_messages": 50,
        "layout":       "side_by_side",
        "panels": {
            "main":     True,
            "combat":   True,
            "items":    True,
            "dialogue": False,
            "system":   False,
        },
    },
}

# PanelWidget has been moved to pygame_ui.py

class Room:
	"""Represents a room loaded from JSON. Mutable state includes items and actions (if desired)."""
	def __init__(self, data):
		self.name = data.get("name")
		self.description = data.get("description", "")
		self.exits = data.get("exits", {})  # dict: direction -> room_name
		self.items = list(data.get("items", []))  # items present in the room (list allows duplicates)
		# actions: dict mapping exact command string -> effect dict
		# effect dict can contain: response/text, add_item (list), remove_item (list), move_to (room name), effects, conditions
		self.actions = data.get("actions", {})
		self.coordinates = data.get("coordinates", [0, 0])
		self.location_type = data.get("location_type", "wilderness")
		self.npcs = data.get("npcs", [])
		self.crafting_station = data.get("crafting_station", None)
		self.shop = data.get("shop", False)

	def describe(self):
		"""Return room description with aggregated item counts (e.g. '3 bronze coins')."""
		desc = f"{self.name}\n{self.description}\n"
		# Show NPCs if any
		if self.npcs and NPC_AVAILABLE:
			try:
				from npc_system import NPC_DATABASE
				npc_names = []
				for npc_id in self.npcs:
					npc = NPC_DATABASE.get(npc_id)
					if npc:
						npc_names.append(f"{npc['name']} ({npc['title']})")
				if npc_names:
					desc += "People here: " + ", ".join(npc_names) + "\n"
			except ImportError:
				pass
		if self.items:
			# aggregate counts
			counts = {}
			for it in self.items:
				counts[it] = counts.get(it, 0) + 1
			parts = []
			for it, cnt in counts.items():
				if cnt > 1:
					# naive pluralize by adding 's' if necessary
					pl = it + "s" if not it.endswith("s") else it
					parts.append(f"{cnt} {pl}")
				else:
					parts.append(it)
			desc += "On the floor: " + ", ".join(parts) + "\n"
		if self.exits:
			desc += "Exits: " + ", ".join(self.exits.keys()) + "\n"
		return desc


class Player:
	"""Tracks current room, inventory (dict), and arbitrary state variables (for logic)."""
	def __init__(self, start_room):
		self.current_room = start_room
		# inventory now a dict: { item_name: count }
		self.inventory = {}
		# state holds arbitrary flags, e.g. {"sitting": False}
		self.state = {}
		# stats holds numeric values like gold, health, score
		self.stats = {}
		# visited_rooms tracks rooms the player has visited (for fog of war)
		self.visited_rooms = set([start_room])
		# Track which islands the player has unlocked boat travel to
		self.unlocked_islands = set()

	def to_dict(self):
		# Always serialize inventory as dict of string->int
		return {
			"current_room": self.current_room,
			"inventory": {str(k): int(v) for k, v in (self.inventory or {}).items()},
			"state": self.state,
			"stats": self.stats,
			"visited_rooms": list(self.visited_rooms) if self.visited_rooms else [],
			"unlocked_islands": list(self.unlocked_islands) if self.unlocked_islands else []
		}

	@classmethod
	def from_dict(cls, data):
		p = cls(data.get("current_room"))
		inv = data.get("inventory", {}) or {}
		# Accept either dict or list for backward compatibility
		if isinstance(inv, dict):
			# ensure inventory is dict of string->int
			p.inventory = {str(k): int(v) for k, v in inv.items()}
		elif isinstance(inv, list):
			# convert list like ["coin","coin","apple"] to {"coin":2,"apple":1}
			agg = {}
			for it in inv:
				if it is None:
					continue
				agg[str(it)] = agg.get(str(it), 0) + 1
			p.inventory = agg
		else:
			p.inventory = {}
		p.state = dict(data.get("state", {}))
		p.stats = dict(data.get("stats", {}))
		# Load visited_rooms from save, or use current room as fallback
		visited = data.get("visited_rooms", [])
		p.visited_rooms = set(visited) if visited else {p.current_room}
		# Load unlocked islands (backward compat: default to empty)
		unlocked = data.get("unlocked_islands", [])
		p.unlocked_islands = set(unlocked) if unlocked else set()
		return p


# ─── Bank of Estoria — tiered storage caps ───────────────────────────────────
# Index = bank_tier (0–19).  Tier 0 is free; tiers 1-19 require gold + materials.
BANK_TIERS = [
	{"capacity": 5_000,   "gold_cost": 0,      "material_cost": {}},
	{"capacity": 10_000,  "gold_cost": 500,    "material_cost": {"copper_ingot": 5}},
	{"capacity": 15_000,  "gold_cost": 1_000,  "material_cost": {"copper_ingot": 10}},
	{"capacity": 20_000,  "gold_cost": 2_000,  "material_cost": {"iron_ingot": 5}},
	{"capacity": 25_000,  "gold_cost": 3_000,  "material_cost": {"iron_ingot": 10}},
	{"capacity": 30_000,  "gold_cost": 5_000,  "material_cost": {"iron_ingot": 15}},
	{"capacity": 37_500,  "gold_cost": 7_500,  "material_cost": {"steel_ingot": 5}},
	{"capacity": 45_000,  "gold_cost": 10_000, "material_cost": {"steel_ingot": 10}},
	{"capacity": 52_500,  "gold_cost": 12_500, "material_cost": {"steel_ingot": 15}},
	{"capacity": 60_000,  "gold_cost": 15_000, "material_cost": {"mithril_ore": 5}},
	{"capacity": 67_500,  "gold_cost": 20_000, "material_cost": {"mithril_ore": 10}},
	{"capacity": 72_500,  "gold_cost": 25_000, "material_cost": {"mithril_ore": 15}},
	{"capacity": 77_500,  "gold_cost": 30_000, "material_cost": {"mithril_ore": 20, "gold_dust": 5}},
	{"capacity": 82_500,  "gold_cost": 35_000, "material_cost": {"mithril_ore": 20, "gold_dust": 10}},
	{"capacity": 87_500,  "gold_cost": 40_000, "material_cost": {"mithril_ore": 20, "gold_dust": 10, "rare_crystal": 3}},
	{"capacity": 90_000,  "gold_cost": 42_500, "material_cost": {"mithril_ore": 20, "gold_dust": 10, "rare_crystal": 5}},
	{"capacity": 93_000,  "gold_cost": 45_000, "material_cost": {"mithril_ore": 20, "gold_dust": 10, "rare_crystal": 5}},
	{"capacity": 96_000,  "gold_cost": 47_500, "material_cost": {"mithril_ore": 20, "gold_dust": 10, "rare_crystal": 5}},
	{"capacity": 98_000,  "gold_cost": 49_000, "material_cost": {"mithril_ore": 20, "gold_dust": 10, "rare_crystal": 5}},
	{"capacity": 100_000, "gold_cost": 50_000, "material_cost": {"mithril_ore": 20, "gold_dust": 10, "rare_crystal": 5}},
]


class CommandHandler:
	"""Parse and execute commands. Delegates to GameEngine for state changes.
	All handler methods return a string (the response) instead of printing.
	"""
	def __init__(self, engine):
		self.engine = engine

	def _check_conditions(self, conds):
		"""Check conditions dict: supports {"state": {"key": value}}.
		Returns (True, '') if satisfied, otherwise (False, message).
		"""
		if not conds:
			return True, ""
		# only 'state' supported for now
		state_conds = conds.get("state", {})
		for k, v in state_conds.items():
			if self.engine.player.state.get(k) != v:
				# Allow optional custom 'fail_text' in conditions in future
				return False, conds.get("fail_text") or "You can't do that now."
		return True, ""

	def handle(self, raw):
		cmd = (raw or "").strip()
		if not cmd:
			return ""
		
		# CRITICAL: Check if we're waiting for class selection
		if PROGRESSION_AVAILABLE and getattr(self.engine, 'pending_class_selection', False):
			return self._handle_class_selection(cmd)
		
		# CRITICAL: Check if we're waiting for yes/no response to dungeon entry
		if self.engine.pending_dungeon_entry is not None:
			# Player is answering yes/no question
			return self.confirm_dungeon_entry(cmd)
		
		# Check if we're waiting for boat travel unlock confirmation
		if getattr(self.engine, 'pending_boat_travel', None) is not None:
			return self._confirm_boat_travel(cmd)
		
		# Check if we're waiting for quest accept/decline
		if QUEST_AVAILABLE and getattr(self.engine, 'pending_quest_action', None) is not None:
			return self._handle_quest_accept(cmd)
		
		# Check if we're waiting for yes/no response to shop negotiation
		if SHOP_AVAILABLE and self.engine.shop_ui and self.engine.shop_ui.pending_negotiation:
			# Player is answering yes/no to counter-offer
			return self.engine.shop_ui.respond_to_negotiation(self.engine.player, cmd)
		
		# Check if we're in a disarm minigame
		if hasattr(self.engine, 'pending_disarm') and self.engine.pending_disarm is not None:
			result = self.confirm_disarm_choice(cmd)
			if result is not None:
				return result
		
		# Check if we're in an NPC dialogue
		if self.engine.pending_dialogue is not None:
			if NPC_AVAILABLE and self.engine.npc_manager:
				return self.engine.npc_manager.handle_dialogue_choice(cmd)
			else:
				self.engine.pending_dialogue = None
		
		# Check if we're in a crafting menu
		if self.engine.pending_crafting is not None:
			if CRAFTING_AVAILABLE and self.engine.crafting_system:
				return self.engine.crafting_system.handle_crafting_choice(cmd)
			else:
				self.engine.pending_crafting = None

		# Check if we're in an experiment session
		if getattr(self.engine, 'pending_experiment', None) is not None:
			if CRAFTING_AVAILABLE and self.engine.crafting_system:
				return self.engine.crafting_system.handle_experiment_choice(cmd)
			else:
				self.engine.pending_experiment = None

		# Check if we're in an enchanting menu
		if getattr(self.engine, 'pending_enchant', None) is not None:
			if ENCHANTING_AVAILABLE and self.engine.enchanting_system:
				pending = self.engine.pending_enchant
				if pending.get("choosing_slot"):
					return self.engine.enchanting_system.handle_slot_choice(cmd)
				else:
					return self.engine.enchanting_system.handle_enchant_choice(cmd)
			else:
				self.engine.pending_enchant = None
		
		# Check if we're in combat — restrict available commands
		if COMBAT_AVAILABLE and getattr(self.engine, 'pending_combat', None):
			combat_cmds = {"attack", "defend", "flee", "ability", "abilities", "ab", "stats", "equipment", "help", "?", "commands", "save", "inventory", "inv", "i"}
			test_verb = cmd.strip().split()[0].lower() if cmd.strip() else ""
			if test_verb not in combat_cmds:
				combat = self.engine.pending_combat
				return (
					f"You're in combat with {combat.enemy_name}!\n"
					"Available commands: attack | defend | flee | ability <name>\n"
				)

		parts = cmd.split()
		verb = parts[0].lower()
		args = parts[1:]
		
		# Command aliases for easier play
		aliases = {
			"n": "north",
			"s": "south",
			"e": "east",
			"w": "west",
			"u": "up",
			"d": "down",
		}
		
		# Expand single-letter movement aliases
		if verb in aliases and not args:
			verb = "go"
			args = [aliases[cmd.lower()]]

		# Example generic blocking: if sitting, block movement and taking until they stand.
		# To change this behavior, update the blocked_verbs list or add more complex checks.
		if self.engine.player.state.get("sitting"):
			if verb in ("go", "walk", "move", "take", "get", "collect"):
				return "You need to stand up first."

		# First check global commands (work anywhere)
		if cmd in getattr(self.engine, "global_commands", {}):
			effect = self.engine.global_commands[cmd]
			ok, msg = self._check_conditions(effect.get("conditions", {}))
			if not ok:
				return msg
			return self._perform_global_command(effect)

		# check for room-specific action (exact command match)
		room = self.engine.get_room_data(self.engine.player.current_room)
		if not room:
			return "[Room not found - game state error]"
		if cmd in room.actions:
			effect = room.actions[cmd]
			ok, msg = self._check_conditions(effect.get("conditions", {}))
			if not ok:
				return msg
			return self._perform_action(effect, room, cmd)

		# fallback to built-in verbs
		if verb in ("go", "walk", "move"):
			if not args:
				return "Go where?"
			direction = args[0].lower()
			# Special case: "go enter" still works for compatibility
			if direction == "enter":
				return self.handle_enter_command()
			return self._go(direction)
		
		# NEW: Standalone ENTER command
		if verb == "enter":
			return self.handle_enter_command()
		
		if verb in ("look", "l"):
			return self._look()
		# Support new collect command and keep old aliases
		if verb in ("collect", "take", "get", "pickup", "pick"):
			if not args:
				return "Pick up what?"
			return self._collect(" ".join(args))
		if verb == "drop":
			if not args:
				return "Drop what?"
			return self._drop(" ".join(args))
		if verb in ("inventory", "inv", "i"):
			return self._inventory()
		if verb == "save":
			return self.engine.save_game()
		if verb == "load":
			return self.engine.load_game(interactive=False)
		if verb == "disarm":
			return self._disarm_trap()
		if verb in ("craft", "forge", "altar"):
			return self._use_crafting_altar()
		if verb == "experiment":
			if CRAFTING_AVAILABLE and self.engine.crafting_system:
				return self.engine.crafting_system.start_experiment()
			return "Crafting system not available."
		if verb == "use":
			if args and args[0].lower() == "altar":
				return self._use_crafting_altar()
			if not args:
				return "Use what? (e.g. 'use healing_potion')"
			return self._use_item(" ".join(args))
		if verb == "leave":
			return self._go("leave")
		if verb in ("quit", "exit"):
			# set flag so GUI can act on it
			self.engine.should_quit = True
			return "Goodbye."
		if verb in ("help", "?"):
			return self._show_commands()
		if verb in ("recipes", "crafting"):
			return self._show_recipes()
		if verb in ("examine", "inspect", "x"):
			if not args:
				return "Examine what?"
			return self._examine(" ".join(args))
		# Quest / Journal commands
		if verb in ("journal", "quests", "quest", "j"):
			return self._show_journal()
		# add sell verb handling
		if verb == "sell":
			if not args:
				return "Sell what?"
			return self._sell(" ".join(args))
		
		# Shop commands
		if verb == "shop":
			if not args:
				return self._shop_help()
			subcommand = args[0].lower()
			if subcommand == "browse" or subcommand == "view" or subcommand == "inventory":
				return self._shop_browse()
			elif subcommand == "buy":
				if len(args) < 2:
					return "Buy what? (Usage: shop buy <item_name>)"
				item_name = " ".join(args[1:]).lower()
				return self._shop_buy(item_name)
			elif subcommand == "sell":
				if len(args) < 3:
					return "Usage: shop sell <item_name> <gold_amount>"
				item_name = " ".join(args[1:-1]).lower()
				try:
					price = int(args[-1])
				except ValueError:
					return "Price must be a number."
				return self._shop_sell(item_name, price)
			elif subcommand == "talk":
				return self._shop_talk()
			elif subcommand == "info":
				return self._shop_info()
			else:
				return self._shop_help()
		
		if verb == "talk":
			if len(args) >= 2 and args[0].lower() == "to":
				target = " ".join(args[1:]).lower()
				# Try shopkeeper first (in shop rooms)
				if target == "shopkeeper":
					return self._shop_talk()
				# Try NPC system
				if NPC_AVAILABLE and self.engine.npc_manager:
					return self.engine.npc_manager.start_conversation(target)
				return "There's nobody here by that name."
			if not args:
				return "Talk to whom? (e.g. 'talk to bartender')"
			# Also support "talk bartender" (without "to")
			target = " ".join(args).lower()
			if NPC_AVAILABLE and self.engine.npc_manager:
				return self.engine.npc_manager.start_conversation(target)
			return "Talk to whom?"

		# ── Bank commands (only available in bank_of_estoria) ──────────────────────
		if verb == "bank":
			if not args:
				return self._bank_help()
			sub = args[0].lower()
			if sub == "help":
				return self._bank_help()
			elif sub == "balance":
				return self._bank_balance()
			elif sub == "upgrade":
				return self._bank_upgrade()
			else:
				return self._bank_help()

		if verb == "deposit":
			if not args:
				return "Deposit how much? (e.g. 'deposit 500')"
			try:
				amount = int(args[0])
			except ValueError:
				# allow "all"
				if args[0].lower() == "all":
					amount = self.engine.player.stats.get("gold", 0)
				else:
					return "Amount must be a number."
			return self._bank_deposit(amount)

		if verb == "withdraw":
			if not args:
				return "Withdraw how much? (e.g. 'withdraw 200')"
			try:
				amount = int(args[0])
			except ValueError:
				if args[0].lower() == "all":
					amount = self.engine.player.state.get("bank_gold", 0)
				else:
					return "Amount must be a number."
			return self._bank_withdraw(amount)

		if verb == "balance":
			return self._bank_balance()

		if verb in ("upgrade",) and args and args[0].lower() == "bank":
			return self._bank_upgrade()

		# Gift command: gift <npc> <item>
		if verb == "gift" or verb == "give":
			if not args:
				return "Gift what to whom? (e.g. 'gift bartender health_potion')"
			if len(args) < 2:
				return "Usage: gift <npc_name> <item_name>\nExample: gift bartender health_potion"
			npc_target = args[0].lower()
			item_target = "_".join(args[1:]).lower()
			if NPC_AVAILABLE and self.engine.npc_manager:
				return self.engine.npc_manager.handle_gift(npc_target, item_target)
			return "The NPC system is not available."

		# Reputation command
		if verb in ("reputation", "rep"):
			if not NPC_REP_AVAILABLE or not self.engine.reputation_manager:
				return "The reputation system is not available."
			if args:
				# Show specific NPC reputation
				npc_target = args[0].lower()
				return self.engine.reputation_manager.get_summary(npc_target)
			# Show all NPC reputations
			return self.engine.reputation_manager.get_all_summaries()
		
		# Search command
		if verb == "search":
			return self._search_room()

		# Fishing commands
		if verb == "fish":
			if not FISHING_AVAILABLE or not self.engine.fishing_system:
				return "The fishing system is not available."
			bait_id = args[0].lower() if args else None
			return self.engine.fishing_system.start_fishing(bait_id)
		if verb == "bait":
			if not FISHING_AVAILABLE or not self.engine.fishing_system:
				return "The fishing system is not available."
			return self.engine.fishing_system.show_bait_info()

		# Enchanting command — use an altar to enchant equipment
		if verb == "enchant":
			if not ENCHANTING_AVAILABLE or not self.engine.enchanting_system:
				return "The enchanting system is not available."
			return self.engine.enchanting_system.show_enchanting_menu()

		# Fight command — engage visible overworld enemy
		if verb == "fight":
			return self._fight_visible_enemy()
		
		# Map commands
		if verb == "open":
			if args and args[0].lower() == "map":
				return self._open_map()
			if args and args[0].lower() == "chest":
				return self._open_chest()
			return "Open what?"
		if verb == "close":
			if args and args[0].lower() == "map":
				return self._close_map()
			return "Close what?"
		# Commands and debug
		if verb == "commands":
			return self._show_commands()
		if verb == "debug":
			if args and args[0].lower() == "commands":
				return self._show_debug_menu()
			return self._handle_debug_command(args)

		# Progression commands
		if verb in ("stats", "level", "class"):
			return self._show_player_stats()
		if verb in ("skills", "skilltree", "skill"):
			if args and args[0].lower() == "list":
				return self._show_skills_text()
			return self._open_skill_tree()
		if verb in ("ability", "abilities", "ab"):
			if not args:
				return self._show_abilities()
			return self._use_ability(" ".join(args))
		if verb in ("synergy", "synergies"):
			return self._show_synergies()
		if verb in ("achievements", "achieve", "ach"):
			return self._show_achievements()

		# Equipment commands
		if verb == "equip":
			if not args:
				return "Equip what? (e.g. 'equip iron_sword')"
			return self._equip_item(" ".join(args))
		if verb == "unequip":
			if not args:
				return "Unequip what? (e.g. 'unequip weapon' or 'unequip iron_sword')"
			return self._unequip_item(" ".join(args))
		if verb == "equipment":
			return self._show_equipment()

		# Combat commands
		if verb == "attack":
			return self._combat_attack()
		if verb == "defend":
			return self._combat_defend()
		if verb == "flee":
			return self._combat_flee()

		# Board / ship travel command
		if verb == "board":
			room = self.engine.get_room_data(self.engine.player.current_room)
			exits = room.exits if hasattr(room, 'exits') else (room.get('exits', {}) if isinstance(room, dict) else {})
			# Exact exit key match — delegate to _go
			if cmd in exits:
				return self._go(cmd)
			# Collect all boat_travel exits
			boat_exits = {k: v for k, v in exits.items()
						  if isinstance(v, dict) and v.get("type") == "boat_travel"}
			if not boat_exits:
				return "There is no ship here to board."
			if not args:
				# List available ships
				lines = ["\n╔══════════════════════════════════════════════════════╗",
						 "║                  AVAILABLE SHIPS                    ║",
						 "╠══════════════════════════════════════════════════════╣"]
				for key, info in boat_exits.items():
					display = info.get("display", key)
					fare = info.get("fare_cost", 0)
					lvl = info.get("min_level", 1)
					if fare > 0:
						row = f"║  {key:<22}  → {display:<18} {fare}g lvl{lvl}+ ║"
					else:
						row = f"║  {key:<22}  → {display:<28} ║"
					lines.append(row)
				lines.append("╚══════════════════════════════════════════════════════╝")
				lines.append("  Type the full command to sail (e.g. 'board mainland')")
				return "\n".join(lines)
			# Typed "board <something>" — try partial match
			partial = cmd.lower()
			for k in boat_exits:
				if k.startswith(partial) or partial in k:
					return self._go(k)
			return f"No ship going to '{' '.join(args)}'. Type 'board' to see available ships."

		# Room Browser window
		if verb in ("rooms", "room_browser", "areas"):
			return "__OPEN_ROOMS__"

		# Bestiary window
		if verb in ("bestiary", "monsters", "enemies"):
			return "__OPEN_BESTIARY__"

		return "I don't understand that."

	# ========== CLASS SELECTION ==========

	def _handle_class_selection(self, cmd):
		"""Handle the player's class choice during new game setup."""
		cmd = cmd.strip()
		class_map = {"1": "warrior", "2": "rogue", "3": "mage"}
		# Also accept class names
		for cid in ("warrior", "rogue", "mage"):
			if cmd.lower() == cid:
				class_map[cmd.lower()] = cid

		choice = class_map.get(cmd.lower() if cmd.lower() in class_map else cmd)
		if not choice:
			return "Invalid choice. Type 1 (Warrior), 2 (Rogue), or 3 (Mage):"

		# Apply the chosen class
		apply_class(self.engine.player, choice)
		self.engine.pending_class_selection = False

		class_name = CLASS_DEFINITIONS[choice]["name"]
		icon = CLASS_DEFINITIONS[choice]["icon"]

		result = "\n" + "=" * 60 + "\n"
		result += f"  You have chosen: {class_name.upper()}\n"
		result += "=" * 60 + "\n"
		result += icon.rstrip() + "\n\n"
		result += f"  Your {class_name} skills are now available.\n"
		result += "  Type 'skills' to view your skill tree.\n"
		result += "  Type 'stats' to see your attributes.\n"
		result += "=" * 60 + "\n\n"

		# Show the starting room
		room = self.engine.get_room_data(self.engine.player.current_room)
		if room:
			result += room.describe()

		return result

	# ========== QUEST COMMANDS ==========

	def _handle_quest_accept(self, cmd):
		"""Handle yes/no response to a quest offer."""
		action = self.engine.pending_quest_action
		self.engine.pending_quest_action = None
		if not action:
			return ""
		action_type, quest_id = action
		answer = cmd.strip().lower()
		if answer in ("yes", "y", "accept", "1"):
			if QUEST_AVAILABLE and self.engine.quest_manager:
				return self.engine.quest_manager.accept_quest(quest_id)
			return "Quest system not available."
		elif answer in ("no", "n", "decline", "2"):
			return "You declined the quest."
		else:
			# Re-set pending so they can answer
			self.engine.pending_quest_action = action
			return "Accept the quest? (yes/no)"

	def _show_journal(self):
		"""Show the quest journal."""
		if not QUEST_AVAILABLE or not self.engine.quest_manager:
			return "Quest system not available."
		return self.engine.quest_manager.get_journal_text()

	# ========== PROGRESSION COMMANDS ==========

	def _show_player_stats(self):
		"""Show detailed player stats in console."""
		if not PROGRESSION_AVAILABLE:
			# Fallback: show basic stats
			stats = self.engine.player.stats
			parts = [f"  {k}: {v}" for k, v in sorted(stats.items())]
			return "\n" + "\n".join(parts)

		stats = self.engine.player.stats
		class_id = stats.get("class", "none")
		class_name = CLASS_DEFINITIONS.get(class_id, {}).get("name", "None") if class_id != "none" else "None"

		result = "\n" + "=" * 50 + "\n"
		result += "  CHARACTER STATS\n"
		result += "=" * 50 + "\n"
		result += f"  Class:    {class_name}\n"
		result += f"  Level:    {stats.get('level', 1)}\n"

		# XP bar
		xp = stats.get("xp", 0)
		xp_to_next = stats.get("xp_to_next", 0)
		if xp_to_next > 0:
			from progression_system import XP_TABLE
			level = stats.get("level", 1)
			if level < len(XP_TABLE):
				xp_for_level = XP_TABLE[level]
				xp_prev = XP_TABLE[level - 1] if level > 1 else 0
				progress = xp - xp_prev
				total_needed = xp_for_level - xp_prev
				if total_needed > 0:
					bar_len = 20
					filled = int((progress / total_needed) * bar_len)
					bar = "#" * filled + "-" * (bar_len - filled)
					result += f"  XP:       [{bar}] {xp}/{xp_for_level}\n"
				else:
					result += f"  XP:       {xp}\n"
			else:
				result += f"  XP:       {xp} (MAX LEVEL)\n"
		else:
			result += f"  XP:       {xp} (MAX LEVEL)\n"

		result += f"  SP:       {stats.get('skill_points', 0)} skill points\n"
		result += "\n  --- Vitals ---\n"
		result += f"  Health:   {stats.get('health', 100)}/{stats.get('health_max', 100)}\n"
		if stats.get('max_mana', 0) > 0:
			result += f"  Mana:     {stats.get('mana', 0)}/{stats.get('max_mana', 0)}\n"
		result += f"  Gold:     {stats.get('gold', 0)}\n"
		result += "\n  --- Attributes ---\n"

		for stat_name in ["strength", "defense", "dexterity", "perception", "charisma", "constitution"]:
			val = stats.get(stat_name, 0)
			result += f"  {stat_name.capitalize():14s} {val}\n"

		# Show active effects
		active_effects = self.engine.player.state.get("active_effects", {})
		if active_effects:
			result += "\n  --- Active Effects ---\n"
			for eff, val in active_effects.items():
				nice = eff.replace("_", " ").title()
				if isinstance(val, dict):
					result += f"  {nice}: {val.get('duration', '?')} moves\n"
				elif isinstance(val, int) and val > 0:
					result += f"  {nice}: {val} moves\n"

		# Show equipment
		if EQUIPMENT_AVAILABLE:
			equip = self.engine.player.state.get("equipment", {})
			has_equip = any(v for v in equip.values()) if equip else False
			if has_equip:
				result += "\n  --- Equipment ---\n"
				slot_icons = {"weapon": "⚔️", "armor": "🛡️", "shield": "🔰", "helm": "⛑️", "boots": "🥾", "gloves": "🧤", "accessory": "💍"}
				for slot in EQUIPMENT_SLOTS:
					item = equip.get(slot)
					if item:
						# Show rarity indicator if available
						eq_data = EQUIPMENT_DATABASE.get(item, {})
						rarity = eq_data.get("rarity", "common")
						from equipment_system import RARITY_TIERS
						rarity_icon = RARITY_TIERS.get(rarity, {}).get("icon", "")
						nice = eq_data.get("name", item.replace("_", " ").title())
						icon = slot_icons.get(slot, "•")
						result += f"  {icon} {slot.capitalize():12s} {rarity_icon} {nice}\n"
				bonuses = get_total_equipment_bonuses(self.engine.player)
				if bonuses:
					result += f"  Attack Power:  {get_attack_power(self.engine.player)}\n"
					result += f"  Defense Power: {get_defense_power(self.engine.player)}\n"

		result += "=" * 50 + "\n"
		return result

	# ========== EQUIPMENT COMMANDS ==========

	def _equip_item(self, item_name):
		"""Equip an item from inventory."""
		if not EQUIPMENT_AVAILABLE:
			return "Equipment system not available."
		# Block if in combat
		if COMBAT_AVAILABLE and getattr(self.engine, 'pending_combat', None):
			return "You can't change equipment during combat!"
		# Determine target slot for enchantment handling
		item_id = item_name.lower().replace(" ", "_")
		eq_data = EQUIPMENT_DATABASE.get(item_id, {})
		target_slot = eq_data.get("slot")
		success, message = equip_item(self.engine.player, item_name)
		if success:
			self.engine._inventory_changed = True
			# Remove enchantment from slot (old item was auto-unequipped)
			if target_slot and ENCHANTING_AVAILABLE and self.engine.enchanting_system:
				self.engine.enchanting_system.on_unequip(target_slot, None)
		return message

	def _unequip_item(self, target):
		"""Unequip an item by slot name or item name."""
		if not EQUIPMENT_AVAILABLE:
			return "Equipment system not available."
		if COMBAT_AVAILABLE and getattr(self.engine, 'pending_combat', None):
			return "You can't change equipment during combat!"
		# Determine slot for enchantment handling
		target_lower = target.lower().replace(" ", "_")
		enchant_slot = None
		if target_lower in EQUIPMENT_SLOTS:
			enchant_slot = target_lower
		else:
			# Find slot by item id
			equip = self.engine.player.state.get("equipment", {})
			for s, eid in equip.items():
				if eid and (eid == target_lower or eid.replace("_", " ") == target_lower.replace("_", " ")):
					enchant_slot = s
					break
		success, message = unequip_item(self.engine.player, target)
		if success:
			self.engine._inventory_changed = True
			# Remove enchantment from slot
			if enchant_slot and ENCHANTING_AVAILABLE and self.engine.enchanting_system:
				self.engine.enchanting_system.on_unequip(enchant_slot, None)
		return message

	def _show_equipment(self):
		"""Show current equipment."""
		if not EQUIPMENT_AVAILABLE:
			return "Equipment system not available."
		return get_equipment_display(self.engine.player)

	# ========== COMBAT COMMANDS ==========

	def _track_combat_victory(self, combat):
		"""Track achievement events for a combat victory."""
		if not ACHIEVEMENT_AVAILABLE:
			return ""
		player = self.engine.player
		try:
			# Track kill
			track_event(player, "kills")
			# Track boss / mini-boss kills
			if getattr(combat, 'is_boss', False):
				track_event(player, "bosses_killed")
				# Track elite boss kills (check if in a fixed dungeon with extreme difficulty)
				fd = getattr(self.engine, 'current_fixed_dungeon', None)
				if fd and fd.get('difficulty') == 'extreme':
					track_event(player, "elite_bosses_killed")
				# Track dungeon completion (boss kill = dungeon done)
				track_event(player, "dungeons_completed")
			if getattr(combat, 'is_mini_boss', False):
				track_event(player, "mini_bosses_killed")
			# Track close calls (won with < 10% HP)
			hp = player.stats.get('health', 1)
			hp_max = player.stats.get('health_max', 100)
			if hp_max > 0 and hp / hp_max < 0.10:
				track_event(player, "close_calls")
			# Track flawless wins (HP unchanged from max)
			if hp >= hp_max:
				track_event(player, "flawless_wins")
			# Track gold earned from combat
			if isinstance(combat.gold_reward, (list, tuple)) and len(combat.gold_reward) == 2:
				gold = (combat.gold_reward[0] + combat.gold_reward[1]) // 2
			else:
				gold = int(combat.gold_reward) if combat.gold_reward else 0
			if gold > 0:
				track_event(player, "total_gold", gold)
			return self._check_and_show_achievements()
		except Exception:
			return ""

	def _combat_attack(self):
		"""Handle attack command during combat."""
		if not COMBAT_AVAILABLE:
			return "Combat system not available."
		combat = getattr(self.engine, 'pending_combat', None)
		if not combat:
			return "You're not in combat. There's nothing to attack."

		result = process_player_attack(self.engine.player, combat)

		# Check if enemy is dead
		if combat.hp <= 0:
			victory_msg = generate_victory_result(self.engine.player, combat)
			# Track achievements
			ach_msg = self._track_combat_victory(combat)
			# Award XP through progression system
			xp_msg = ""
			if PROGRESSION_AVAILABLE:
				try:
					xp_msg = award_xp(self.engine.player, combat.xp_reward, f"defeating {combat.enemy_name}")
					level_msg = check_level_up(self.engine.player)
					if level_msg:
						xp_msg += "\n" + level_msg
				except Exception:
					pass
			self.engine.pending_combat = None
			self.engine._inventory_changed = True
			# Notify quest system of enemy kill
			if QUEST_AVAILABLE and self.engine.quest_manager:
				self.engine.quest_manager.on_enemy_killed(
					combat.enemy_name,
					is_boss=getattr(combat, 'is_boss', False),
					is_mini_boss=getattr(combat, 'is_mini_boss', False)
				)
				self.engine.quest_manager.on_item_changed()
			return result + victory_msg + xp_msg + ach_msg

		# Check if player died
		death_msg = self._check_player_death()
		if death_msg:
			self.engine.pending_combat = None
			return result + death_msg

		# Show combat status
		return result + get_combat_status(self.engine.player, combat)

	def _combat_defend(self):
		"""Handle defend command during combat."""
		if not COMBAT_AVAILABLE:
			return "Combat system not available."
		combat = getattr(self.engine, 'pending_combat', None)
		if not combat:
			return "You're not in combat."

		result = process_player_defend(self.engine.player, combat)

		# Check if player died
		death_msg = self._check_player_death()
		if death_msg:
			self.engine.pending_combat = None
			return result + death_msg

		return result + get_combat_status(self.engine.player, combat)

	def _combat_flee(self):
		"""Handle flee command during combat."""
		if not COMBAT_AVAILABLE:
			return "Combat system not available."
		combat = getattr(self.engine, 'pending_combat', None)
		if not combat:
			return "You're not in combat."

		success, msg = process_player_flee(self.engine.player, combat)

		if success:
			self.engine.pending_combat = None
			return msg

		# Check if player died from the failed flee hit
		death_msg = self._check_player_death()
		if death_msg:
			self.engine.pending_combat = None
			return msg + death_msg

		return msg + get_combat_status(self.engine.player, combat)

	def _start_combat_encounter(self, enemy_id=None, boss_dungeon=None, floor_num=None):
		"""
		Start a combat encounter. Called from room entry.
		Returns the intro text, or empty string if no combat.
		"""
		if not COMBAT_AVAILABLE:
			return ""

		# Extract floor_num from current room if not provided
		if floor_num is None:
			import re
			floor_match = re.search(r'_floor(\d+)', self.engine.player.current_room)
			floor_num = int(floor_match.group(1)) if floor_match else 1

		if boss_dungeon:
			combat = create_boss_instance(boss_dungeon, floor_num)
			if not combat:
				return ""
			self.engine.pending_combat = combat
			intro = combat.intro_text if combat.intro_text else (
				f"\n⚔️ A powerful {combat.enemy_name} blocks your path!\n"
			)
			return intro + get_combat_status(self.engine.player, combat)

		if enemy_id:
			combat = create_enemy_instance(enemy_id, floor_num=floor_num)
			if not combat:
				return ""
			self.engine.pending_combat = combat
			result = f"\n⚔️ A {combat.enemy_name} appears!\n"
			result += f"  {combat.enemy_description}\n"
			return result + get_combat_status(self.engine.player, combat)

		return ""

	def _fight_visible_enemy(self):
		"""Engage a visible overworld enemy in the current room."""
		if not OVERWORLD_AVAILABLE or not self.engine.encounter_manager:
			return "There's nothing to fight here."
		if getattr(self.engine, 'pending_combat', None):
			return "You're already in combat!"

		room_id = self.engine.player.current_room
		enemy_data = self.engine.encounter_manager.engage_visible_enemy(room_id)
		if not enemy_data:
			return "There's nothing to fight here."

		return self._start_overworld_combat(enemy_data)

	def _start_overworld_combat(self, enemy_data):
		"""Start combat with an overworld enemy (from scaled data dict)."""
		if not COMBAT_AVAILABLE:
			return "Combat system not available."

		# Create CombatState from the pre-scaled data
		combat = CombatState(enemy_data, is_boss=False, level=self.engine.player.stats.get("level", 1))
		self.engine.pending_combat = combat

		result = f"\n⚔️ A {combat.enemy_name} attacks!\n"
		result += f"  {combat.enemy_description}\n"
		return result + get_combat_status(self.engine.player, combat)

	def _check_player_death(self):
		"""Check if the player has died and handle respawn."""
		hp = self.engine.player.stats.get("health", 1)
		if hp > 0:
			return ""

		# Player is dead!
		result = "\n" + "=" * 55 + "\n"
		result += "  💀 YOU HAVE FALLEN! 💀\n"
		result += "=" * 55 + "\n"

		# Gold penalty: lose 5-10% of carried gold (bank_gold is safe)
		import random as _rnd
		gold = self.engine.player.stats.get("gold", 0)
		pct = _rnd.uniform(0.05, 0.10)
		gold_lost = int(gold * pct)
		self.engine.player.stats["gold"] = gold - gold_lost
		self.engine.player.state["death_gold_lost_total"] = (
			self.engine.player.state.get("death_gold_lost_total", 0) + gold_lost
		)
		if gold_lost > 0:
			result += f"  You lost {gold_lost}g ({pct*100:.0f}% of your carried gold)...\n"

		# Find respawn location: village or chapel, fallback to start
		respawn_room = self.engine.start_room
		for room_id, room in self.engine.rooms.items():
			lt = getattr(room, 'location_type', '') or ''
			name = getattr(room, 'name', '') or ''
			if 'chapel' in name.lower() or 'chapel' in room_id.lower():
				respawn_room = room_id
				break
			elif 'village' in name.lower() or 'village_square' in room_id.lower():
				respawn_room = room_id

		# Respawn
		self.engine.player.stats["health"] = self.engine.player.stats.get("health_max", 100) // 2
		self.engine.poison_status = None  # clear poison on death

		# Fully clean up dungeon state if player died inside one (fixes map not updating)
		in_dungeon = (
			getattr(self.engine, 'current_dungeon_instance', None) is not None
			or getattr(self.engine, 'current_fixed_dungeon', None) is not None
		)
		if in_dungeon:
			self.engine.cleanup_dungeon()

		# Set respawn location AFTER cleanup (cleanup may have moved player to entrance)
		self.engine.player.current_room = respawn_room

		# Update map so it shows the respawn room immediately
		if hasattr(self.engine.player, 'visited_rooms'):
			self.engine.player.visited_rooms.add(respawn_room)
		if hasattr(self.engine, 'map_window') and self.engine.map_window:
			if self.engine.map_window.is_open():
				self.engine.map_window.update_location(
					respawn_room,
					getattr(self.engine.player, 'visited_rooms', set())
				)

		respawn_name = respawn_room.replace("_", " ").title()
		result += f"\n  You wake up at {respawn_name} with half health.\n"
		result += "=" * 55 + "\n\n"

		# Show respawn room
		dest = self.engine.get_room_data(respawn_room)
		if dest:
			result += dest.describe()

		return result

	def _open_skill_tree(self):
		"""Open the graphical skill tree window."""
		if not PROGRESSION_AVAILABLE:
			return "Progression system not available."

		class_id = self.engine.player.stats.get("class", "none")
		if class_id == "none":
			return "You haven't chosen a class yet."

		# Open via GUI
		if self.engine.gui and hasattr(self.engine.gui, 'toggle_skills_window'):
			self.engine.gui.toggle_skills_window()
			return "Skill tree opened."

		# Fallback: text-based
		return self._show_skills_text()

	def _show_skills_text(self):
		"""Show skills as text in the console (fallback), grouped by branch."""
		if not PROGRESSION_AVAILABLE:
			return "Progression system not available."

		class_id = self.engine.player.stats.get("class", "none")
		if class_id == "none":
			return "You haven't chosen a class yet."

		tree = get_tree_for_class(class_id)
		unlocked = set(get_unlocked_skills(self.engine.player))
		available = {n["id"] for n in get_available_skills(self.engine.player)}

		result = "\n" + "=" * 50 + "\n"
		result += f"  SKILL TREE ({class_id.upper()}) — {len(tree)} nodes\n"
		result += f"  Skill Points: {self.engine.player.stats.get('skill_points', 0)}\n"
		result += f"  Unlocked: {len(unlocked)}  |  Available: {len(available)}\n"
		result += "=" * 50 + "\n\n"

		# Group by branch, then tier
		branches = {}
		for node in tree:
			b = node.get("branch", "origin")
			branches.setdefault(b, []).append(node)

		for branch_name in sorted(branches.keys()):
			nodes = sorted(branches[branch_name], key=lambda n: (n["tier"], n["name"]))
			# Count unlocked in this branch
			b_unlocked = sum(1 for n in nodes if n["id"] in unlocked)
			result += f"  [{branch_name.upper()}] ({b_unlocked}/{len(nodes)})\n"
			for node in nodes:
				if node["id"] in unlocked:
					status = "+"
				elif node["id"] in available:
					status = ">"
				else:
					status = " "
				type_tag = "A" if node["type"] == "active" else "P"
				result += f"    {status} T{node['tier']} [{type_tag}] {node['name']} ({node['cost']}SP)\n"
			result += "\n"

		result += "  + = unlocked, > = available\n"
		result += "  Use 'skills' to open the graphical skill tree.\n"
		result += "=" * 50 + "\n"
		return result

	def _show_abilities(self):
		"""Show active abilities and their cooldowns."""
		if not PROGRESSION_AVAILABLE:
			return "Progression system not available."

		abilities = get_active_abilities(self.engine.player)
		if not abilities:
			return "You don't have any active abilities yet.\nUnlock active skills in your skill tree ('skills')."

		cooldowns = self.engine.player.state.get("cooldowns", {})

		result = "\n" + "=" * 50 + "\n"
		result += "  ACTIVE ABILITIES\n"
		result += "=" * 50 + "\n\n"

		for ab in abilities:
			cd_remaining = cooldowns.get(ab["skill_id"], 0)
			status = "READY" if cd_remaining == 0 else f"Cooldown: {cd_remaining} moves"
			name = ab.get("name", "Unknown")
			cmd_name = name.lower().replace(" ", "_")

			result += f"  {name} [{status}]\n"
			result += f"    Cooldown: {ab.get('cooldown', 0)} moves\n"
			result += f"    Use: ability {cmd_name}\n\n"

		result += "=" * 50 + "\n"
		return result

	def _show_synergies(self):
		"""Show active branch synergy bonuses."""
		if not PROGRESSION_AVAILABLE:
			return "Progression system not available."

		class_id = self.engine.player.stats.get("class", "none")
		if class_id == "none":
			return "You haven't chosen a class yet."

		branch_counts = get_branch_counts(self.engine.player)
		synergy_total, descriptions = get_synergy_bonuses(self.engine.player)

		result = "\n" + "=" * 50 + "\n"
		result += "  BRANCH SYNERGIES\n"
		result += "=" * 50 + "\n\n"

		if not branch_counts:
			result += "  No branch skills unlocked yet.\n"
			result += "  Unlock 3+ skills in a branch for synergy bonuses!\n"
		else:
			from skill_tree import SYNERGY_THRESHOLDS, BRANCH_SYNERGY_EXTRAS
			for branch, count in sorted(branch_counts.items(), key=lambda x: -x[1]):
				# Find current rank
				current_rank = "—"
				next_threshold = SYNERGY_THRESHOLDS[0][0] if SYNERGY_THRESHOLDS else 99
				for i, (thresh, rank, _) in enumerate(SYNERGY_THRESHOLDS):
					if count >= thresh:
						current_rank = rank
						next_threshold = SYNERGY_THRESHOLDS[i + 1][0] if i + 1 < len(SYNERGY_THRESHOLDS) else None
					else:
						next_threshold = thresh
						break

				branch_label = branch.replace("_", " ").title()
				if current_rank == "—":
					result += f"  {branch_label}: {count} nodes (need {next_threshold} for Initiate)\n"
				elif next_threshold:
					result += f"  ★ {branch_label}: {current_rank} ({count} nodes, {next_threshold - count} more for next)\n"
				else:
					result += f"  ★ {branch_label}: {current_rank} ({count} nodes) — MAX RANK!\n"

			if synergy_total:
				result += "\n  Total synergy bonuses:\n"
				for stat, val in sorted(synergy_total.items()):
					nice = stat.replace("_", " ").replace("health max bonus", "Max HP")
					nice = nice.replace("crit chance bonus", "Crit Chance")
					if isinstance(val, float):
						result += f"    +{val:.0%} {nice}\n"
					else:
						result += f"    +{val} {nice}\n"

		result += "\n" + "=" * 50 + "\n"
		return result

	def _show_achievements(self):
		"""Show the player's achievements."""
		if not ACHIEVEMENT_AVAILABLE:
			return "Achievement system not available."
		return get_achievements_display(self.engine.player)

	def _check_and_show_achievements(self):
		"""Check for new achievements and return notification text."""
		if not ACHIEVEMENT_AVAILABLE:
			return ""
		newly_unlocked = check_achievements(self.engine.player)
		if not newly_unlocked:
			return ""
		result = ""
		for ach_id, ach_data in newly_unlocked:
			result += format_achievement_unlock(ach_id, ach_data)
		return result

	def _use_ability(self, ability_name):
		"""Use an active ability. Handles both exploration and combat abilities."""
		if not PROGRESSION_AVAILABLE:
			return "Progression system not available."

		success, msg, ability_data = use_ability(self.engine.player, ability_name)

		if not success:
			return msg

		effect = ability_data.get("effect", "") if ability_data else ""

		# If in combat and this is a combat ability, process it through combat system
		combat = getattr(self.engine, 'pending_combat', None)
		if combat and COMBAT_AVAILABLE and effect.startswith("combat_"):
			combat_result = process_ability_in_combat(self.engine.player, combat, ability_data)
			result = msg + "\n" + combat_result

			# Check if enemy died
			if combat.hp <= 0:
				victory_msg = generate_victory_result(self.engine.player, combat)
				xp_msg = ""
				if PROGRESSION_AVAILABLE:
					try:
						xp_msg = award_xp(self.engine.player, combat.xp_reward, f"defeating {combat.enemy_name}")
						level_msg = check_level_up(self.engine.player)
						if level_msg:
							xp_msg += "\n" + level_msg
					except Exception:
						pass
				self.engine.pending_combat = None
				self.engine._inventory_changed = True
				# Track achievements
				ach_msg = self._track_combat_victory(combat)
				# Notify quest system of enemy kill
				if QUEST_AVAILABLE and self.engine.quest_manager:
					self.engine.quest_manager.on_enemy_killed(
						combat.enemy_name,
						is_boss=getattr(combat, 'is_boss', False),
						is_mini_boss=getattr(combat, 'is_mini_boss', False)
					)
					self.engine.quest_manager.on_item_changed()
				return result + victory_msg + xp_msg + ach_msg

			# Check if player died
			death_msg = self._check_player_death()
			if death_msg:
				self.engine.pending_combat = None
				return result + death_msg

			# Check if player fled (smoke bomb / guaranteed_flee)
			if combat.player_fled:
				self.engine.pending_combat = None
				return result

			return result + get_combat_status(self.engine.player, combat)

		# Handle combat abilities used in combat that don't start with combat_
		if combat and COMBAT_AVAILABLE and effect in ("guaranteed_flee", "buff_attack", "extra_gold", "temp_defense", "restore_mana"):
			combat_result = process_ability_in_combat(self.engine.player, combat, ability_data)
			result = msg + "\n" + combat_result

			if combat.player_fled:
				self.engine.pending_combat = None
				return result

			death_msg = self._check_player_death()
			if death_msg:
				self.engine.pending_combat = None
				return result + death_msg

			return result + get_combat_status(self.engine.player, combat)

		# Non-combat ability effects (exploration/utility)
		if effect == "reveal_floor" and hasattr(self.engine, 'current_dungeon_instance'):
			msg += self._handle_reveal_floor()
		elif effect == "reveal_adjacent_traps":
			msg += self._handle_reveal_adjacent_traps()
		elif effect in ("heal", "combat_heal"):
			# Healing works outside combat as a self-heal
			value = ability_data.get("value", 0) if ability_data else 0
			if effect == "combat_heal" and not combat:
				# Apply the heal directly since _apply_ability_effect wasn't called for combat effects
				hp = self.engine.player.stats.get("health", 100)
				hp_max = self.engine.player.stats.get("health_max", 100)
				heal_amount = int(value)
				self.engine.player.stats["health"] = min(hp + heal_amount, hp_max)
			hp = self.engine.player.stats.get("health", 100)
			hp_max = self.engine.player.stats.get("health_max", 100)
			msg += f"\n  Health: {hp}/{hp_max}\n"
		elif effect == "buff_attack" and not combat:
			# Apply attack buff outside combat
			value = ability_data.get("value", 0) if ability_data else 0
			duration = ability_data.get("duration", 1) if ability_data else 1
			active_effects = self.engine.player.state.get("active_effects", {})
			active_effects["attack_boost"] = {"value": value, "duration": duration}
			self.engine.player.stats["strength"] = self.engine.player.stats.get("strength", 0) + value
			self.engine.player.state["active_effects"] = active_effects
			msg += f"\n  Strength boosted by +{value} for {duration} moves!\n"
		elif effect == "temp_defense" and not combat:
			# Apply defense buff outside combat
			value = ability_data.get("value", 0) if ability_data else 0
			duration = ability_data.get("duration", 1) if ability_data else 1
			_apply_ability_effect(self.engine.player, "temp_defense", duration, value)
			msg += f"\n  Defense boosted by +{value} for {duration} moves!\n"

		return msg

	def _handle_reveal_floor(self):
		"""Handle the Reveal Floor ability effect — mark all traps on current floor as detected and reveal secrets."""
		di = self.engine.current_dungeon_instance
		if not di or not di.dungeon_data:
			return "\n  (No dungeon floor to reveal.)\n"

		# Determine which floor the player is on
		room_id = self.engine.player.current_room
		traps_found = 0
		secrets_found = 0
		for _fnum, fdata in di.dungeon_data.get("floors", {}).items():
			rooms = fdata.get("rooms", {})
			if room_id in rooms:
				# This is the player's current floor — reveal everything
				for rid, rdata in rooms.items():
					for trap in rdata.get("traps", []):
						if not trap.get("triggered") and not trap.get("disarmed"):
							trap["detected"] = True
							traps_found += 1
					# Reveal secret rooms
					if rdata.get("has_secret") and not rdata.get("secret_discovered"):
						rdata["secret_discovered"] = True
						secrets_found += 1
				break

		result = "\n  All traps and secrets on this floor are now visible!\n"
		if traps_found:
			result += f"  Traps revealed: {traps_found}\n"
		if secrets_found:
			result += f"  Secret passages revealed: {secrets_found}\n"
		if not traps_found and not secrets_found:
			result += "  (Nothing hidden was found on this floor.)\n"
		return result

	def _handle_reveal_adjacent_traps(self):
		"""Handle revealing traps in adjacent rooms — mark traps in connected rooms as detected."""
		di = self.engine.current_dungeon_instance
		if not di or not di.dungeon_data:
			return "\n  You sense the traps in nearby rooms!\n"

		room_id = self.engine.player.current_room
		# Find current room and its exits
		for _fnum, fdata in di.dungeon_data.get("floors", {}).items():
			rooms = fdata.get("rooms", {})
			if room_id in rooms:
				current_room = rooms[room_id]
				exits = current_room.get("exits", {})
				traps_found = 0
				for _dir, exit_data in exits.items():
					target = exit_data.get("target") if isinstance(exit_data, dict) else exit_data
					if target and target in rooms:
						for trap in rooms[target].get("traps", []):
							if not trap.get("triggered") and not trap.get("disarmed"):
								trap["detected"] = True
								traps_found += 1
				result = "\n  You sense the traps in nearby rooms!\n"
				if traps_found:
					result += f"  Traps detected in adjacent rooms: {traps_found}\n"
				else:
					result += "  (No traps sensed nearby.)\n"
				return result

		return "\n  You sense the traps in nearby rooms!\n"

	def _perform_action(self, effect, room, invoked_cmd):
		# effect is a dict possibly containing keys: text/response, add_item, remove_item, move_to, effects, conditions
		parts = []
		# support both legacy keys: 'response' and new 'text'
		text = effect.get("text") or effect.get("response")
		if text:
			parts.append(text)

		# Apply logical effects: e.g. {"state": {"sitting": True}}
		effects_block = effect.get("effects", {})
		inv_changed = False
		if effects_block:
			# handle state changes
			state_changes = effects_block.get("state", {})
			for k, v in state_changes.items():
				self.engine.player.state[k] = v

			# inventory additions
			for it in effects_block.get("inventory_add", []) if isinstance(effects_block.get("inventory_add", []), list) else []:
				if it:
					self._add_to_inventory(it)
					inv_changed = True
			# inventory removals
			for it in effects_block.get("inventory_remove", []) if isinstance(effects_block.get("inventory_remove", []), list) else []:
				if it:
					self._remove_from_inventory(it)
					inv_changed = True

		# add/remove items (older action keys)
		for it in effect.get("add_item", []):
			target = effect.get("add_target", "player")
			if target == "player":
				self._add_to_inventory(it)
				inv_changed = True
			else:
				if it not in room.items:
					room.items.append(it)
		for it in effect.get("remove_item", []):
			target = effect.get("remove_target", "room")
			if target == "room":
				if it in room.items:
					room.items.remove(it)
			else:
				# remove from player
				if it in self.engine.player.inventory:
					self._remove_from_inventory(it)
					inv_changed = True

		# move player if specified
		if "move_to" in effect:
			new_room = effect["move_to"]
			if new_room in self.engine.rooms:
				self.engine.player.current_room = new_room
			room = self.engine.get_room_data(new_room)
			if room:
				parts.append(room.describe())
			else:
				parts.append("[Room not found]")
		# notify engine that inventory changed so UI can refresh
		if inv_changed:
			try:
				self.engine._inventory_changed = True
			except Exception:
				pass

		return "\n".join(parts)

	def _perform_global_command(self, effect):
		"""Apply a global command's effects: text, inventory changes, state changes, and stats."""
		parts = []
		# support legacy keys too
		text = effect.get("text") or effect.get("response")
		if text:
			parts.append(text)

		inv_changed = False

		# inventory add/remove via effects
		for it in effect.get("effects", {}).get("inventory_add", []):
			if it:
				self._add_to_inventory(it)
				inv_changed = True
		for it in effect.get("effects", {}).get("inventory_remove", []):
			if it:
				self._remove_from_inventory(it)
				inv_changed = True

		# state changes
		for k, v in effect.get("effects", {}).get("state", {}).items():
			self.engine.player.state[k] = v

		# stats modifications: can be numbers to set or sign-prefixed increments
		stats_block = effect.get("effects", {}).get("stats", {})
		for k, v in stats_block.items():
			# support integer set or incremental value (e.g., 1 or "+1")
			cur = self.engine.player.stats.get(k, 0)
			if isinstance(v, str) and (v.startswith("+") or v.startswith("-")):
				try:
					cur += int(v)
				except ValueError:
					pass
				self.engine.player.stats[k] = cur
			elif isinstance(v, (int, float)):
				# treat as increment:
				self.engine.player.stats[k] = cur + v
			else:
				# fallback: set as-is
				self.engine.player.stats[k] = v

		# notify engine that inventory changed so UI can refresh
		if inv_changed:
			try:
				self.engine._inventory_changed = True
			except Exception:
				pass

		return "\n".join(parts)

	def _go(self, direction):
		"""Navigate to an exit: supports both compass directions and named locations."""
		if self.engine.player.state.get("sitting"):
			return "You need to stand up first."
		
		# Check for blocking traps in the current room
		block_msg = self._check_blocking_traps()
		if block_msg and direction != "leave":
			return block_msg
		
		room = self.engine.get_room_data(self.engine.player.current_room)
		if not room:
			return "[Current room not found]"
		exits = room.exits
		
		# Handle old-style exits (backward compatibility): "exits": {"north": "room_id"}
		if not exits:
			return "There are no exits here."
		
		# Check for secret room access (both dict and Room object)
		if direction == "secret":
			is_boss = False
			has_secret_discovered = False
			secret_room_id = None
			
			if isinstance(room, dict):
				is_boss = room.get("is_boss_room")
				has_secret_discovered = room.get("secret_discovered")
				secret_room_id = room.get("secret_room_id")
			elif hasattr(room, "is_boss_room"):
				is_boss = room.is_boss_room
				has_secret_discovered = getattr(room, "secret_discovered", False)
				secret_room_id = getattr(room, "secret_room_id", None)
			
			if is_boss:
				if not has_secret_discovered:
					return "You don't see a secret exit here. Perhaps you should examine the walls more carefully."
				if secret_room_id:
					return self._enter_secret_room(secret_room_id)
		
		# Check for exact exit match (handles both old string format and new dict format)
		target_room_id = None
		exit_info = None
		
		if direction in exits:
			exit_data = exits[direction]
			if isinstance(exit_data, str):
				# Old format: direct room ID
				target_room_id = exit_data
			elif isinstance(exit_data, dict):
				# New format: exit object
				target_room_id = exit_data.get("target")
				exit_info = exit_data
		
		# Handle time-gated dungeon entrance
		if exit_info and isinstance(exit_info, dict) and exit_info.get("type") == "time_gated_dungeon":
			print(f"[DEBUG _go] Dungeon entrance detected via '{direction}'")
			
			# Check if dungeon system is available
			is_available, reason = self._check_dungeon_system_available()
			
			if is_available:
				print("[DEBUG _go] System check passed, routing to entrance handler")
				return self._handle_dungeon_entrance(exit_info)
			else:
				print(f"[ERROR _go] Dungeon system unavailable: {reason}")
				error_msg = (
					"The dungeon system is currently unavailable.\n"
					f"Reason: {reason}\n"
					"Please contact an administrator."
				)
				return error_msg
		
		# Handle fixed dungeon entrance (always open, hand-crafted)
		if exit_info and isinstance(exit_info, dict) and exit_info.get("type") == "fixed_dungeon":
			print(f"[DEBUG _go] Fixed dungeon entrance detected via '{direction}'")
			return self._handle_fixed_dungeon_entrance(exit_info)
		
		# Handle boat travel to islands
		if exit_info and isinstance(exit_info, dict) and exit_info.get("type") == "boat_travel":
			return self._handle_boat_travel(exit_info)
		
		# Handle leaving the dungeon
		if exit_info and isinstance(exit_info, dict) and exit_info.get("type") == "leave_dungeon":
			return self._leave_dungeon(exit_info)
		
		if not target_room_id:
			# No valid exit found
			location_type = room.__dict__.get('location_type', 'wilderness')
			return self._describe_exits(room, location_type)
		
		# Check if target room exists (in world or dungeon)
		dest_room = self.engine.get_room_data(target_room_id)
		if not dest_room:
			location_type = room.__dict__.get('location_type', 'wilderness')
			return self._describe_exits(room, location_type)
		
		# Move player
		self.engine.player.current_room = target_room_id
		
		# Tick ability effects and cooldowns on movement
		effect_msgs = ""
		if PROGRESSION_AVAILABLE:
			try:
				msgs = tick_effects(self.engine.player)
				if msgs:
					effect_msgs = "\n".join(msgs) + "\n"
			except Exception:
				pass
		
		# Award exploration XP on first visit
		xp_msg = ""
		if PROGRESSION_AVAILABLE:
			try:
				is_first_visit = target_room_id not in self.engine.player.visited_rooms
				if is_first_visit:
					xp_msg = award_xp(self.engine.player, XP_AWARDS.get("first_visit_room", 3), "exploring new room")
			except Exception:
				pass
		
		# Check for traps in the new room
		trap_msg = self._check_room_traps(target_room_id)
		
		# Tick poison damage on movement
		poison_msg = self._tick_poison()

		# Check for combat encounter in rooms (dungeon + overworld)
		combat_msg = ""
		if COMBAT_AVAILABLE and not getattr(self.engine, 'pending_combat', None):
			combat_msg = self._check_room_enemy(target_room_id, dest_room)

		# Get visible enemy text (if any visible enemy lingers but didn't trigger random combat)
		visible_enemy_msg = ""
		if OVERWORLD_AVAILABLE and self.engine.encounter_manager and not combat_msg:
			visible_enemy_msg = self.engine.encounter_manager.get_visible_enemy_text(target_room_id)

		# Check for death from traps/poison
		death_msg = self._check_player_death()
		
		# Show transition text if available
		if exit_info and isinstance(exit_info, dict):
			transition_text = exit_info.get("transition_text")
			if transition_text:
				result = f"{transition_text}\n\n"
				result += dest_room.describe()
				if trap_msg:
					result += "\n" + trap_msg
				if poison_msg:
					result += poison_msg
				if xp_msg:
					result += xp_msg
				if effect_msgs:
					result += effect_msgs
				if death_msg:
					result += death_msg
				elif combat_msg:
					result += combat_msg
				elif visible_enemy_msg:
					result += visible_enemy_msg
				self._update_map_on_move(target_room_id)
				# Check exploration achievements
				result += self._check_and_show_achievements()
				return result
		
		self._update_map_on_move(target_room_id)
		result = dest_room.describe()
		if trap_msg:
			result += "\n" + trap_msg
		if poison_msg:
			result += poison_msg
		if xp_msg:
			result += xp_msg
		if effect_msgs:
			result += effect_msgs
		if death_msg:
			result += death_msg
		elif combat_msg:
			result += combat_msg
		elif visible_enemy_msg:
			result += visible_enemy_msg
		# Check exploration achievements
		result += self._check_and_show_achievements()
		return result
	
	def _update_map_on_move(self, new_room_id):
		"""Update the live map when player moves."""
		try:
			# Mark room as visited
			if hasattr(self.engine.player, 'visited_rooms'):
				self.engine.player.visited_rooms.add(new_room_id)
			
			# Notify quest system of room entry
			if QUEST_AVAILABLE and hasattr(self.engine, 'quest_manager') and self.engine.quest_manager:
				self.engine.quest_manager.on_room_entered(new_room_id)
			
			# Update map if it's open
			if hasattr(self.engine, 'map_window') and self.engine.map_window:
				if self.engine.map_window.is_open():
					self.engine.map_window.update_location(
						new_room_id,
						getattr(self.engine.player, 'visited_rooms', set())
					)
		except Exception:
			pass  # Silently fail if map update fails
	
	def _leave_dungeon(self, exit_info):
		"""Handle the player leaving the dungeon back to the surface."""
		target = exit_info.get("target", "dungeon_forest_entrance")
		transition = exit_info.get("transition_text", "You climb back to the surface...")

		# Clean up dungeon state
		self.engine.cleanup_dungeon()

		# Move player to surface room
		self.engine.player.current_room = target
		self._update_map_on_move(target)

		dest = self.engine.get_room_data(target)
		result = f"\n{transition}\n\n"
		result += "\n" + "=" * 50 + "\n"
		result += "You have left the dungeon!\n"
		result += "=" * 50 + "\n\n"
		if dest:
			result += dest.describe()
		return result

	def _handle_boat_travel(self, exit_info):
		"""Handle boat travel exits to islands. Checks level req, unlock status, and fare."""
		island_id = exit_info.get("island_id", "unknown")
		island_name = exit_info.get("display", island_id.replace("_", " ").title())
		min_level = exit_info.get("min_level", 1)
		unlock_cost = exit_info.get("unlock_cost", 0)
		fare_cost = exit_info.get("fare_cost", 0)
		target = exit_info.get("target")
		
		player = self.engine.player
		player_level = player.stats.get("level", 1)
		player_gold = player.stats.get("gold", 0)
		
		# Check level requirement
		if player_level < min_level:
			result = "\n" + "=" * 60 + "\n"
			result += f"  PASSAGE DENIED — {island_name}\n"
			result += "=" * 60 + "\n\n"
			result += f"The captain looks you over and shakes his head.\n"
			result += f"\"You're not seasoned enough for {island_name}, adventurer.\"\n"
			result += f"\"Come back when you've reached level {min_level}.\"\n\n"
			result += f"  Your level: {player_level} | Required: {min_level}\n"
			result += "-" * 60 + "\n"
			return result
		
		# Check if island is unlocked
		if not hasattr(player, 'unlocked_islands'):
			player.unlocked_islands = set()
		
		if island_id not in player.unlocked_islands:
			# Need to unlock first — prompt player
			if player_gold < unlock_cost:
				result = "\n" + "=" * 60 + "\n"
				result += f"  PASSAGE TO {island_name.upper()}\n"
				result += "=" * 60 + "\n\n"
				result += f"The captain strokes his beard thoughtfully.\n"
				result += f"\"First voyage to {island_name}? That'll cost {unlock_cost} gold\n"
				result += f" to charter the route. Plus {fare_cost} gold per trip after.\"\n\n"
				result += f"  Your gold: {player_gold} | Unlock cost: {unlock_cost}\n"
				result += f"  You don't have enough gold!\n"
				result += "-" * 60 + "\n"
				return result
			
			# Player can afford it — ask for confirmation
			self.engine.pending_boat_travel = {
				"island_id": island_id,
				"island_name": island_name,
				"unlock_cost": unlock_cost,
				"fare_cost": fare_cost,
				"target": target,
				"exit_info": exit_info,
				"needs_unlock": True
			}
			result = "\n" + "=" * 60 + "\n"
			result += f"  CHARTER PASSAGE — {island_name}\n"
			result += "=" * 60 + "\n\n"
			result += f"The captain nods. \"Aye, I can take you to {island_name}.\"\n"
			result += f"\"First time? Chartering the route costs {unlock_cost} gold.\"\n"
			result += f"\"After that, it's {fare_cost} gold per voyage.\"\n\n"
			result += f"  Unlock cost: {unlock_cost} gold\n"
			result += f"  Your gold:   {player_gold} gold\n\n"
			result += f"Charter passage to {island_name}? (yes/no)\n"
			result += "-" * 60 + "\n"
			return result
		
		# Island already unlocked — just charge fare
		if fare_cost > 0 and player_gold < fare_cost:
			result = "\n" + "-" * 60 + "\n"
			result += f"The captain shrugs. \"Voyage to {island_name} costs {fare_cost} gold.\n"
			result += f"You only have {player_gold}. Come back when you can pay.\"\n"
			result += "-" * 60 + "\n"
			return result
		
		# Deduct fare and travel
		if fare_cost > 0:
			player.stats["gold"] = player_gold - fare_cost
		
		return self._execute_boat_travel(exit_info, fare_cost)
	
	def _confirm_boat_travel(self, cmd):
		"""Handle yes/no response to boat travel unlock prompt."""
		pending = self.engine.pending_boat_travel
		if pending is None:
			return "I don't understand that command. Type 'help' for available commands."
		
		response = cmd.lower().strip()
		player = self.engine.player
		
		if response in ("yes", "y"):
			island_id = pending["island_id"]
			island_name = pending["island_name"]
			unlock_cost = pending["unlock_cost"]
			fare_cost = pending["fare_cost"]
			target = pending["target"]
			exit_info = pending["exit_info"]
			player_gold = player.stats.get("gold", 0)
			
			total_cost = unlock_cost + fare_cost
			
			if player_gold < total_cost:
				# Check if they can at least afford the unlock
				if player_gold < unlock_cost:
					self.engine.pending_boat_travel = None
					return f"\nYou no longer have enough gold for the unlock fee ({unlock_cost}g).\n"
				
				# Unlock but can't afford fare right now
				player.stats["gold"] = player_gold - unlock_cost
				if not hasattr(player, 'unlocked_islands'):
					player.unlocked_islands = set()
				player.unlocked_islands.add(island_id)
				self.engine.pending_boat_travel = None
				
				result = "\n" + "=" * 60 + "\n"
				result += f"  ROUTE CHARTERED — {island_name}\n"
				result += "=" * 60 + "\n\n"
				result += f"The captain pockets your {unlock_cost} gold.\n"
				result += f"\"Route's chartered! But you'll need {fare_cost} gold for the\n"
				result += f" voyage itself. Come back when you have the fare.\"\n\n"
				result += f"  Remaining gold: {player.stats['gold']}\n"
				result += "-" * 60 + "\n"
				return result
			
			# Can afford both — unlock and travel
			player.stats["gold"] = player_gold - total_cost
			if not hasattr(player, 'unlocked_islands'):
				player.unlocked_islands = set()
			player.unlocked_islands.add(island_id)
			self.engine.pending_boat_travel = None
			
			return self._execute_boat_travel(exit_info, total_cost)
		
		elif response in ("no", "n"):
			island_name = pending["island_name"]
			self.engine.pending_boat_travel = None
			result = "\n" + "-" * 60 + "\n"
			result += f"You step back from the dock.\n"
			result += f"\"Suit yourself,\" the captain says. \"{island_name} ain't\n"
			result += f" going anywhere... for now.\"\n"
			result += "-" * 60 + "\n"
			return result
		else:
			return f"\nPlease type 'yes' to charter passage or 'no' to decline.\n"
	
	def _execute_boat_travel(self, exit_info, gold_spent):
		"""Actually move the player via boat to the target island room."""
		target = exit_info.get("target")
		island_name = exit_info.get("display", "the island")
		transition_text = exit_info.get("transition_text", "")
		
		if not target:
			return "[Error: No target destination for boat travel]"
		
		# Check if target room exists
		dest_room = self.engine.get_room_data(target)
		if not dest_room:
			return f"[Error: Destination room '{target}' not found]"
		
		# Move player
		self.engine.player.current_room = target
		
		# Build result text
		result = "\n" + "=" * 60 + "\n"
		result += "  SETTING SAIL\n"
		result += "=" * 60 + "\n\n"
		
		if gold_spent > 0:
			result += f"  [{gold_spent} gold spent]\n\n"
		
		if transition_text:
			result += transition_text + "\n\n"
		else:
			result += f"You board the weathered ship. The crew casts off the mooring\n"
			result += f"lines and the sails catch the wind. The mainland shrinks behind\n"
			result += f"you as the ship cuts through the open ocean.\n\n"
			result += f"After days at sea, the silhouette of {island_name}\n"
			result += f"emerges from the horizon...\n\n"
		
		result += "=" * 60 + "\n"
		result += f"  ARRIVED AT {island_name.upper()}\n"
		result += "=" * 60 + "\n\n"
		
		# Award exploration XP on first visit
		xp_msg = ""
		if PROGRESSION_AVAILABLE:
			try:
				is_first_visit = target not in self.engine.player.visited_rooms
				if is_first_visit:
					xp_msg = award_xp(self.engine.player, XP_AWARDS.get("first_visit_room", 3) * 5, f"discovering {island_name}")
			except Exception:
				pass
		
		self._update_map_on_move(target)
		result += dest_room.describe()
		if xp_msg:
			result += xp_msg
		
		# Check achievements
		result += self._check_and_show_achievements()

		# Signal the GUI to show the travel animation before rendering this text
		self.engine.pending_travel_animation = island_name
		return result

	def _check_room_enemy(self, room_id, dest_room):
		"""Check for enemy encounter when entering a room.
		Handles both dungeon and overworld encounters.
		Returns combat intro text or empty string."""
		if not COMBAT_AVAILABLE:
			return ""

		# Don't spawn if already in combat
		if getattr(self.engine, 'pending_combat', None):
			return ""

		# Check for dungeon encounters first
		in_dungeon = (room_id.startswith("dungeon_") and "_floor" in room_id) or room_id in self.engine.fixed_dungeon_room_ids
		if in_dungeon:
			return self._check_dungeon_enemy(room_id, dest_room)

		# Check for overworld encounters
		overworld_msg = ""
		if OVERWORLD_AVAILABLE and self.engine.encounter_manager:
			# Roll for visible enemy (only on first visit)
			vis_msg = self.engine.encounter_manager.roll_visible_enemy(room_id)

			# Roll for random encounter
			should_fight, enemy_data = self.engine.encounter_manager.check_random_encounter(room_id)
			if should_fight and enemy_data:
				overworld_msg = self._start_overworld_combat(enemy_data)
			elif vis_msg:
				overworld_msg = vis_msg

		return overworld_msg

	def _check_dungeon_enemy(self, room_id, dest_room):
		"""Check for enemy encounter in dungeon rooms specifically."""

		# Check for already-cleared rooms (track by room id)
		cleared = self.engine.player.state.get("cleared_rooms", [])
		if not isinstance(cleared, list):
			cleared = list(cleared)
			self.engine.player.state["cleared_rooms"] = cleared
		if room_id in cleared:
			return ""

		# Determine dungeon ID
		dungeon_id = None
		di = getattr(self.engine, 'current_dungeon_instance', None)
		if di:
			dungeon_id = getattr(di, 'dungeon_id', None) or getattr(di, 'template_id', None)

		# Check for boss room
		raw_room = None
		if di and hasattr(di, 'floors'):
			for floor in di.floors:
				for rid, rdata in floor.get("rooms", {}).items():
					if rid == room_id:
						raw_room = rdata
						break
		is_boss_room = False
		if raw_room:
			is_boss_room = raw_room.get("is_boss_room", False) or raw_room.get("boss_room", False)
		elif hasattr(dest_room, 'name') and dest_room.name:
			is_boss_room = "boss" in dest_room.name.lower()

		if is_boss_room and dungeon_id:
			# Mark room as cleared so boss doesn't respawn
			cleared.append(room_id)
			# Extract floor number for level scaling
			import re
			floor_num = 1
			floor_match = re.search(r'_floor(\d+)', room_id)
			if floor_match:
				floor_num = int(floor_match.group(1))
			return self._start_combat_encounter(boss_dungeon=dungeon_id, floor_num=floor_num)

		# Regular enemy spawn
		# Determine current floor number
		floor_num = 1
		import re
		floor_match = re.search(r'_floor(\d+)', room_id)
		if floor_match:
			floor_num = int(floor_match.group(1))

		# Build room_data dict for spawn check
		room_data_dict = {}
		if raw_room:
			room_data_dict = raw_room
		elif hasattr(dest_room, '__dict__'):
			room_data_dict = dest_room.__dict__
		room_data_dict["_room_id"] = room_id

		if should_spawn_enemy(floor_num, room_data_dict):
			enemies = get_enemies_for_dungeon(dungeon_id or "any", floor_num)
			if enemies:
				import random
				chosen = random.choice(enemies)
				# Mark room as cleared
				cleared.append(room_id)
				return self._start_combat_encounter(enemy_id=chosen, floor_num=floor_num)

		return ""

	def _check_room_traps(self, room_id):
		"""Check for traps when entering a room. Returns message string or empty.
		
		Three outcomes per trap:
		  1. Detected (40%) — full warning, player can disarm
		  2. Not detected but subtle hint (70% of non-detect) — atmospheric text
		  3. Triggered — trap fires based on trigger_chance
		"""
		import random as _rng
		
		try:
			# Use TrapSystem helper to find the raw room dict
			raw_room = TrapSystem.find_raw_room(
				self.engine.current_dungeon_instance, room_id
			) if TRAP_AVAILABLE else None
			if not raw_room:
				return ""

			traps = raw_room.get("traps", [])
			if not traps:
				return ""

			for trap in traps:
				if trap.get("triggered") or trap.get("disarmed"):
					continue

				# Check for active ability effects
				if PROGRESSION_AVAILABLE:
					# Sneak / Phantom: bypass the trap entirely
					if has_active_effect(self.engine.player, "sneak_active"):
						continue
					# Trap immunity / Arcane Shield: won't trigger
					if has_active_effect(self.engine.player, "trap_immune"):
						continue
					# Trap stunned via Shield Bash
					if has_active_effect(self.engine.player, "trap_stunned"):
						continue

				# Chance to fully detect the trap
				detect = trap.get("detection_chance", 0.40)
				# Already revealed by ability (Reveal / War Cry)
				if trap.get("detected"):
					detect = 1.0
				# Perception bonus: +3% per point
				elif PROGRESSION_AVAILABLE:
					perception = get_stat_modifier(self.engine.player, "perception")
					detect = min(0.95, detect + perception * 0.03)
					# Guaranteed detection from ability
					if has_active_effect(self.engine.player, "guaranteed_detection"):
						detect = 1.0
				if _rng.random() < detect:
					trap_name = trap.get("name", trap.get("type", "trap").replace("_", " "))
					warning = trap.get("warning_signs", "Something feels off about this room.")
					return (
						f"\n⚠️  You notice a {trap_name}!\n"
						f"{warning}\n"
						"Type 'disarm' to attempt to disarm it, or 'search' to investigate further.\n"
					)

				# Roll for trigger
				trigger_chance = trap.get("trigger_chance", 0.30)
				if _rng.random() < trigger_chance:
					return self._trigger_trap(trap)
				
				# If neither detected nor triggered, show a subtle atmospheric hint (70% chance)
				if _rng.random() < 0.70:
					trap_type = trap.get("type", "")
					hints = TrapSystem.SUBTLE_HINTS.get(trap_type, ["Something feels off about this room..."]) if TRAP_AVAILABLE else ["Something feels off about this room..."]
					hint = _rng.choice(hints)
					return f"\n💭 {hint}\n(Try 'search' to investigate.)\n"

			return ""
		except Exception:
			return ""

	def _check_blocking_traps(self):
		"""Check if there's a blocking trap in the current room preventing movement.
		Returns a warning message if blocked, or None if movement is allowed."""
		room_id = self.engine.player.current_room
		raw_room = TrapSystem.find_raw_room(
			self.engine.current_dungeon_instance, room_id
		) if TRAP_AVAILABLE else None
		if not raw_room:
			return None
		
		blocking = TrapSystem.BLOCKING_TRAP_TYPES if TRAP_AVAILABLE else {"pit_trap", "crushing_ceiling"}
		
		traps = raw_room.get("traps", [])
		for trap in traps:
			if trap.get("triggered") or trap.get("disarmed"):
				continue
			trap_type = trap.get("type", "")
			if trap_type in blocking:
				trap_name = trap.get("name", trap_type.replace("_", " "))
				if trap_type == "pit_trap":
					return (
						f"\n🚫 A {trap_name} blocks your path!\n"
						"A gaping pit stretches across the room. You can't cross safely.\n"
						"You must 'disarm' the trap before you can proceed.\n"
					)
				elif trap_type == "crushing_ceiling":
					return (
						f"\n🚫 A {trap_name} blocks your path!\n"
						"The ceiling mechanism is active — moving further would be deadly.\n"
						"You must 'disarm' the trap before you can proceed.\n"
					)
		return None

	def _trigger_trap(self, trap):
		"""Trigger a trap and deal damage. Applies poison if applicable."""
		import random as _rng

		# Check for trap immunity from abilities
		if PROGRESSION_AVAILABLE and has_active_effect(self.engine.player, "trap_immune"):
			trap["triggered"] = True
			trap_name = trap.get("name", trap.get("type", "trap").replace("_", " "))
			result = "\n" + "-" * 50 + "\n"
			result += f"  A {trap_name} activates, but your magical protection absorbs it!\n"
			result += "  You take no damage!\n"
			result += "-" * 50 + "\n"
			# Clear one-shot immunity
			active = self.engine.player.state.get("active_effects", {})
			if "trap_immune" in active:
				active["trap_immune"] = 0
			xp_msg = ""
			try:
				xp_msg = award_xp(self.engine.player, XP_AWARDS.get("survive_trap", 5), "survived trap (immunity)")
			except Exception:
				pass
			return result + xp_msg

		trap["triggered"] = True

		dmg_spec = trap.get("damage", (10, 20))
		if isinstance(dmg_spec, (list, tuple)) and len(dmg_spec) == 2:
			damage = _rng.randint(dmg_spec[0], dmg_spec[1])
		elif isinstance(dmg_spec, (int, float)):
			damage = int(dmg_spec)
		else:
			damage = 15

		# Defense stat reduces damage (min 30% of original)
		if PROGRESSION_AVAILABLE:
			defense = get_stat_modifier(self.engine.player, "defense")
			damage_reduction = defense * 0.02
			damage = int(damage * max(0.30, 1 - damage_reduction))
			# Archmage mode: 50% damage reduction
			if has_active_effect(self.engine.player, "archmage_mode"):
				damage = damage // 2

		trap_name = trap.get("name", trap.get("type", "trap").replace("_", " "))
		desc = trap.get("description", "A trap activates!")

		result = "\n" + "=" * 50 + "\n"
		result += "\U0001f480 TRAP TRIGGERED! \U0001f480\n"
		result += "=" * 50 + "\n"
		result += f"{desc}\n"
		result += f"You take {damage} damage!\n"

		if hasattr(self.engine.player, 'stats'):
			hp = self.engine.player.stats.get("health", 100)
			hp -= damage
			self.engine.player.stats["health"] = hp
			result += f"Health: {hp}\n"

		# Apply poison effect if this is a poison trap
		poison_dmg = trap.get("poison_damage")
		poison_dur = trap.get("poison_duration", 0)
		if poison_dmg and poison_dur > 0:
			# Constitution reduces poison duration
			if PROGRESSION_AVAILABLE:
				con = get_stat_modifier(self.engine.player, "constitution")
				poison_dur = max(1, int(poison_dur - con * 0.5))
			self.engine.poison_status = {
				"damage_per_move": poison_dmg,
				"moves_remaining": poison_dur,
				"source": trap_name,
			}
			result += f"\n🧪 You've been POISONED!\n"
			result += f"   {poison_dmg} damage per move for {poison_dur} moves.\n"

		result += "=" * 50 + "\n"

		# Award XP for surviving a trap
		xp_msg = ""
		if PROGRESSION_AVAILABLE:
			try:
				xp_msg = award_xp(self.engine.player, XP_AWARDS.get("survive_trap", 5), "survived trap")
			except Exception:
				pass

		return result + xp_msg

	def _tick_poison(self):
		"""Apply poison damage when player moves. Returns message or empty string."""
		if not hasattr(self.engine, 'poison_status') or self.engine.poison_status is None:
			return ""
		
		poison = self.engine.poison_status
		dmg = poison.get("damage_per_move", 0)
		remaining = poison.get("moves_remaining", 0)
		
		if remaining <= 0 or dmg <= 0:
			self.engine.poison_status = None
			return ""
		
		# Apply poison damage
		if hasattr(self.engine.player, 'stats'):
			hp = self.engine.player.stats.get("health", 100)
			hp -= dmg
			self.engine.player.stats["health"] = hp
		
		poison["moves_remaining"] = remaining - 1
		
		result = f"\n🧪 Poison deals {dmg} damage! (Health: {self.engine.player.stats.get('health', '?')})\n"
		
		if poison["moves_remaining"] <= 0:
			self.engine.poison_status = None
			result += "   The poison has worn off.\n"
		else:
			result += f"   Poison: {poison['moves_remaining']} moves remaining.\n"
		
		return result

	def _use_crafting_altar(self):
		"""
		Interact with a crafting altar/station in the current room.
		Delegates to the crafting system for menu display and crafting.
		Also works at the village blacksmith (forge station).
		"""
		# Try crafting system first
		if CRAFTING_AVAILABLE and self.engine.crafting_system:
			return self.engine.crafting_system.use_station()
		
		# Fallback if crafting system unavailable
		return "The crafting system is not available."

	def _use_item(self, item_name):
		"""Use an item from inventory."""
		# Check for cooked food from fishing system
		if FISHING_AVAILABLE and self.engine.fishing_system:
			item_key = item_name.replace(" ", "_").lower()
			result = self.engine.fishing_system.use_cooked_food(item_key)
			if result:
				# Consume the food item
				inv = self.engine.player.inventory
				if inv.get(item_key, 0) > 0:
					inv[item_key] -= 1
					if inv[item_key] <= 0:
						del inv[item_key]
					self.engine._inventory_changed = True
				return result

		if ITEM_EFFECTS_AVAILABLE and self.engine.item_effects:
			return self.engine.item_effects.use_item(item_name)
		return "You can't use items right now."

	def _disarm_trap(self):
		"""Attempt to disarm a trap in the current room."""
		import random as _rng
		room_id = self.engine.player.current_room
		raw_room = TrapSystem.find_raw_room(
			self.engine.current_dungeon_instance, room_id
		) if TRAP_AVAILABLE else None
		if not raw_room:
			return "There are no traps to disarm here."

		traps = raw_room.get("traps", [])
		active = [t for t in traps if not t.get("triggered") and not t.get("disarmed")]
		if not active:
			return "There are no active traps here."

		trap = active[0]

		# Check for disarm tools
		difficulty = trap.get("disarm_difficulty", "medium")
		success_rate = TrapSystem.DISARM_SUCCESS_RATES.get(difficulty, 0.50) if TRAP_AVAILABLE else 0.50

		# Dexterity bonus: +2% per point
		if PROGRESSION_AVAILABLE:
			dex = get_stat_modifier(self.engine.player, "dexterity")
			success_rate = min(0.95, success_rate + dex * 0.02)
			# Locksmith bonus: flat +15% from r_locksmith skill
			disarm_bonus = self.engine.player.stats.get("disarm_bonus", 0)
			if disarm_bonus > 0:
				success_rate = min(0.95, success_rate + disarm_bonus)

		required_tools = trap.get("disarm_tools", ["lockpick_set"])
		has_tool = any(t in self.engine.player.inventory for t in required_tools)

		# Debug mode: bypass tool requirement
		if not has_tool and not self.engine.debug_disarm_free:
			return f"You need one of these tools: {', '.join(required_tools)}"

		trap_name = trap.get("name", trap.get("type", "trap").replace("_", " "))
		trap_type = trap.get("type", "unknown")

		# Start disarm minigame — present the player with a choice
		challenge = TrapSystem.get_disarm_challenge(trap_type) if TRAP_AVAILABLE else {"description": "How do you disarm it?", "options": ["Cut the wire", "Jam it", "Disassemble"], "correct": 1}
		
		# Store pending disarm state
		self.engine.pending_disarm = {
			"trap": trap,
			"trap_name": trap_name,
			"correct_answer": challenge["correct"],
			"success_rate": success_rate,
			"has_tool": has_tool,
		}
		
		result = "\n" + "=" * 50 + "\n"
		result += f"🔧 DISARMING: {trap_name}\n"
		result += "=" * 50 + "\n"
		result += f"\n{challenge['description']}\n\n"
		for i, option in enumerate(challenge["options"], 1):
			result += f"  {i}. {option}\n"
		result += f"\nDifficulty: {difficulty.replace('_', ' ').title()}\n"
		if has_tool:
			result += f"✓ Tool bonus active\n"
		result += "\nType the number of your choice (1, 2, or 3):\n"
		result += "=" * 50 + "\n"
		return result

	def confirm_disarm_choice(self, choice):
		"""Handle the player's disarm minigame choice."""
		import random as _rng
		
		if not hasattr(self.engine, 'pending_disarm') or self.engine.pending_disarm is None:
			return None  # Not in a disarm minigame
		
		pending = self.engine.pending_disarm
		trap = pending["trap"]
		trap_name = pending["trap_name"]
		correct = pending["correct_answer"]
		success_rate = pending["success_rate"]
		has_tool = pending["has_tool"]
		
		# Clear pending state
		self.engine.pending_disarm = None
		
		# Parse choice
		try:
			choice_num = int(choice.strip())
		except (ValueError, AttributeError):
			# Invalid input — treat as failed attempt
			result = "Invalid choice! Your fumbling almost triggers the trap!\n"
			if _rng.random() < 0.30:
				result += self._trigger_trap(trap)
			else:
				result += f"You narrowly avoid triggering the {trap_name}. Try 'disarm' again."
			return result
		
		if choice_num < 1 or choice_num > 3:
			result = "Invalid choice! You hesitate and lose your focus.\n"
			return result + f"The {trap_name} is still active. Try 'disarm' again."
		
		# Correct choice + tool bonus gives high success; wrong choice reduces it
		if choice_num == correct:
			# Correct answer: success_rate boosted by tool
			final_rate = min(0.95, success_rate + (0.25 if has_tool else 0.0))
		else:
			# Wrong answer: much lower success rate
			final_rate = max(0.05, success_rate * 0.3)
		
		if _rng.random() < final_rate:
			trap["disarmed"] = True
			result = "\n" + "=" * 50 + "\n"
			result += f"✅ You successfully disarm the {trap_name}!\n"
			if choice_num == correct:
				result += "Your approach was perfect — the mechanism clicks into a safe state.\n"
			else:
				result += "Despite a rough approach, you managed to disable it through sheer luck!\n"
			result += "=" * 50 + "\n"
			# Award XP based on difficulty
			if PROGRESSION_AVAILABLE:
				try:
					difficulty = trap.get("disarm_difficulty", "medium")
					xp_key = f"disarm_trap_{difficulty}"
					xp_amount = XP_AWARDS.get(xp_key, XP_AWARDS.get("disarm_trap_medium", 25))
					result += award_xp(self.engine.player, xp_amount, f"disarmed {trap_name}")
				except Exception:
					pass
			return result
		else:
			# Failed — chance to trigger
			if _rng.random() < 0.50:
				result = f"Your disarm attempt fails and the {trap_name} activates!\n"
				result += self._trigger_trap(trap)
				return result
			else:
				return f"Your disarm attempt on the {trap_name} fails, but you avoid triggering it.\nTry 'disarm' again to reattempt."

	def confirm_dungeon_entry(self, response):
		"""
		Handles the yes/no response to dungeon entry.
		
		Args:
			response: User's yes/no answer
		"""
		if self.engine.pending_dungeon_entry is None:
			# User typed yes/no but we're not asking
			return "I don't understand that command. Type 'help' for available commands."
		
		response = response.lower().strip()
		
		if response in ["yes", "y"]:
			result = "\n" + "=" * 60 + "\n"
			result += "  ENTERING DUNGEON\n"
			result += "=" * 60 + "\n"
			result += "\nYou steel your nerves and step into the entrance.\n"
			result += "The air grows cold as you descend the ancient stairs...\n\n"
			
			# Actually enter the dungeon (fixed or procedural)
			dungeon_exit_data = self.engine.pending_dungeon_entry.get("dungeon_data")
			is_fixed = self.engine.pending_dungeon_entry.get("fixed", False)
			
			if is_fixed:
				result += "[Loading dungeon...]\n"
				dungeon_result = self._enter_fixed_dungeon(dungeon_exit_data)
			else:
				result += "[Generating dungeon layout, please wait...]\n"
				dungeon_result = self._enter_dungeon(dungeon_exit_data)
			result += dungeon_result
			
			# Clear pending flag
			self.engine.pending_dungeon_entry = None
			return result
			
		elif response in ["no", "n"]:
			result = "\n" + "-" * 60 + "\n"
			result += "You step back from the entrance.\n"
			result += "The dungeon remains open, patiently waiting...\n"
			result += "-" * 60 + "\n"
			
			# Clear pending flag
			self.engine.pending_dungeon_entry = None
			return result
			
		else:
			# Invalid response - keep the pending flag so they can answer again
			return f"\nInvalid response: '{response}'\nPlease type 'yes' to enter or 'no' to decline.\n"

	def _check_dungeon_system_available(self) -> tuple[bool, str]:
		"""
		Check if the dungeon system is available for use.
		
		Returns:
			(is_available: bool, reason: str)
			- If True: (True, "")
			- If False: (False, "reason why it's unavailable")
		"""
		if DUNGEON_AVAILABLE:
			# System is fully initialized
			return True, ""
		
		# System is disabled - provide detailed reason
		if _DUNGEON_IMPORT_ERROR:
			reason = f"System initialization failed: {_DUNGEON_IMPORT_ERROR}"
		else:
			reason = "Dungeon system failed to initialize (unknown reason)"
		
		return False, reason

	def _check_dungeon_requirements(self, dungeon_data):
		"""
		Check if the player meets dungeon entry requirements.
		
		Returns:
			(met: bool, message: str)
		"""
		reqs = dungeon_data.get("requirements")
		if not reqs:
			return True, ""

		player = self.engine.player
		if not player:
			return False, "No active player."

		failures = []

		# Level requirement
		min_level = reqs.get("min_level")
		if min_level:
			player_level = player.stats.get("level", 1)
			if player_level < min_level:
				failures.append(f"  ✗ Requires level {min_level} (you are level {player_level})")

		# Require ANY of listed skills (class-flexible)
		skills_any = reqs.get("skills_any")
		if skills_any and PROGRESSION_AVAILABLE:
			has_one = False
			for sid in skills_any:
				if is_skill_unlocked(player, sid):
					has_one = True
					break
			if not has_one:
				# Build a readable list of skill names
				skill_names = []
				player_class = player.stats.get("class", "")
				for sid in skills_any:
					node = get_node_by_id(player_class, sid)
					if node:
						skill_names.append(node.get("name", sid))
					else:
						skill_names.append(sid)
				failures.append(f"  ✗ Requires one of: {', '.join(skill_names)}")

		# Require ALL of listed skills
		skills_all = reqs.get("skills_all")
		if skills_all and PROGRESSION_AVAILABLE:
			for sid in skills_all:
				if not is_skill_unlocked(player, sid):
					node = get_node_by_id(player.stats.get("class", ""), sid)
					name = node.get("name", sid) if node else sid
					failures.append(f"  ✗ Requires skill: {name}")

		# Quest prerequisite
		quest_req = reqs.get("quest_complete")
		if quest_req:
			completed_quests = player.state.get("completed_quests", [])
			if quest_req not in completed_quests:
				failures.append(f"  ✗ Requires quest completion: {quest_req}")

		if failures:
			desc = reqs.get("description", "You do not meet the requirements.")
			msg = "\n" + "=" * 50 + "\n"
			msg += "  ⛔ ENTRY DENIED\n"
			msg += "=" * 50 + "\n\n"
			msg += f"  {desc}\n\n"
			msg += "  Requirements not met:\n"
			msg += "\n".join(failures) + "\n\n"
			msg += "  Grow stronger and return when you are ready.\n"
			msg += "=" * 50 + "\n"
			return False, msg

		return True, ""

	def handle_enter_command(self):
		"""
		Smart ENTER command that handles:
		- Dungeon entrances (time-gated)
		- Building entrances
		
		Automatically detects what kind of entrance based on current room.
		
		Why we need to check DUNGEON_AVAILABLE:
		- DUNGEON_AVAILABLE is a module-level flag set at import time
		- It is True ONLY if dungeon_scheduler and dungeon_instance modules loaded
		- If either module has an import error, it becomes False
		- This check happens BEFORE time-gating checks, preventing errors
		"""
		if self.engine.player.state.get("sitting"):
			return "You need to stand up first."
		
		current_room = self.engine.get_room_data(self.engine.player.current_room)
		if not current_room:
			return "[Current room not found]"
		
		# Check for dungeon entrance (time-gated)
		for exit_name, exit_data in current_room.exits.items():
			if isinstance(exit_data, dict) and exit_data.get("type") == "time_gated_dungeon":
				# This is marked as a dungeon entrance
				print(f"[DEBUG handle_enter] Dungeon entrance detected via '{exit_name}'")
				
				# **CRITICAL CHECK**: Verify dungeon system is actually available
				is_available, reason = self._check_dungeon_system_available()
				
				if not is_available:
					# Dungeon system is broken - provide diagnostic info
					print(f"[ERROR handle_enter] Dungeon system unavailable: {reason}")
					error_msg = (
						"The dungeon system is currently unavailable.\n"
						f"Reason: {reason}\n"
						"Please contact an administrator."
					)
					return error_msg
				
				# System is available - proceed to entrance handler
				print(f"[DEBUG handle_enter] Dungeon system OK (DUNGEON_AVAILABLE={DUNGEON_AVAILABLE})")
				return self._handle_dungeon_entrance(exit_data)
		
		# Check for fixed dungeon entrance (always open, hand-crafted)
		for exit_name, exit_data in current_room.exits.items():
			if isinstance(exit_data, dict) and exit_data.get("type") == "fixed_dungeon":
				print(f"[DEBUG handle_enter] Fixed dungeon entrance detected via '{exit_name}'")
				return self._handle_fixed_dungeon_entrance(exit_data)
		
		# Check for explicit "enter" exit
		if "enter" in current_room.exits:
			exit_data = current_room.exits["enter"]
			target_room_id = None
			
			if isinstance(exit_data, str):
				target_room_id = exit_data
			elif isinstance(exit_data, dict):
				target_room_id = exit_data.get("target")
			
			if target_room_id and target_room_id in self.engine.rooms:
				self.engine.player.current_room = target_room_id
			dest_room = self.engine.get_room_data(target_room_id)
			if dest_room:
				self._update_map_on_move(target_room_id)
				return dest_room.describe()
			else:
				return "[Room not found]"
		return "There's nothing to enter here.\nTry: 'look' to see available exits."

	def _handle_dungeon_entrance(self, exit_info):
		"""
		Handle time-gated dungeon entrance interaction.
		Sets up pending state and asks for confirmation.
		
		This is the SECOND line of defense - after handle_enter_command already checked
		that DUNGEON_AVAILABLE is True. We check again here for safety.
		"""
		try:
			print("[DEBUG _handle_dungeon_entrance] Called")
			
			# Defensive check: verify dungeon system is still available
			is_available, reason = self._check_dungeon_system_available()
			print(f"[DEBUG] Dungeon system available: {is_available}")
			
			if not is_available:
				print(f"[ERROR _handle_dungeon_entrance] System check failed: {reason}")
				return f"Dungeon system error: {reason}"
			
			print("[DEBUG] Getting scheduler...")
			scheduler = get_scheduler(game_engine=self.engine)
			print(f"[DEBUG] Scheduler obtained: {type(scheduler).__name__}")
			
			# Visual separator
			result = "\n" + "-" * 60 + "\n"
			result += "╔════════════════════════════════════════════════════════╗\n"
			result += "║              DUNGEON ENTRANCE DETECTED                 ║\n"
			result += "╚════════════════════════════════════════════════════════╝\n"
			
			# Get dungeon_id from exit info for debug override check
			dungeon_id = exit_info.get("dungeon_id") if isinstance(exit_info, dict) else None
			
			# Check if dungeon is open (by schedule OR debug override)
			dungeon_is_open = scheduler.is_dungeon_open(dungeon_id=dungeon_id)
			
			# Check if specifically debug-forced
			is_debug_forced = (
				hasattr(self.engine, 'debug_force_open_dungeons') and
				dungeon_id is not None and
				dungeon_id in self.engine.debug_force_open_dungeons
			)
			
			print(f"[DEBUG] Dungeon ID: {dungeon_id}")
			print(f"[DEBUG] Time-based open: {scheduler.is_dungeon_open()}")
			print(f"[DEBUG] Debug force-open: {is_debug_forced}")
			print(f"[DEBUG] Final is_open: {dungeon_is_open}")
			
			if not dungeon_is_open:
				# CLOSED and not forced open
				_, time_until_str = scheduler.get_time_until_next_opening()
				result += f"""
Status: CLOSED (sealed by magic)

The entrance is sealed by powerful magic. Ancient runes
pulse with a faint red glow, barring your passage.

A mystical inscription reads:
  "The depths shift with the tides of time.
   Return when the stars align."

Next Opening: {time_until_str}

Schedule: Opens every 3 hours for 1 hour
  Opening times: 00:00, 03:00, 06:00, 09:00, 12:00, 
                 15:00, 18:00, 21:00 (Germany time)
"""
				result += "-" * 60 + "\n"
				
			else:
				# OPEN (or forced open)
				if is_debug_forced and not scheduler.is_dungeon_open():
					status_text = "OPEN (Debug Mode)"
					extra_note = "\n⚙️  This dungeon has been force-opened for testing.\n   It will remain open for this game session.\n"
					time_info = "N/A (debug override)"
				else:
					status_text = "OPEN"
					_, time_remaining_str = scheduler.get_time_until_closing()
					extra_note = ""
					time_info = time_remaining_str
				
				result += f"""
Status: {status_text}{extra_note}
The magical barrier has faded! The entrance yawns before you,
revealing ancient stone steps descending into darkness. A
cold wind blows up from the depths.

Time Remaining: {time_info}

WARNINGS:
  * The dungeon will close in {time_info}
  * If inside when it closes, you'll be teleported out
  * Your loot and progress will be saved
  * The dungeon layout regenerates each opening

This dungeon contains:
  * Randomly generated rooms and layouts
  * Valuable treasure and rare items
  * Dangerous traps
  * Multiple floors of increasing difficulty

---

Do you wish to enter? (yes/no)
"""
				# Set pending flag so we wait for yes/no response
				self.engine.pending_dungeon_entry = {
					"dungeon_data": exit_info
				}
				result += "-" * 60 + "\n"
			
			return result
		
		except Exception as e:
			return f"Error accessing dungeon system: {str(e)}"

	def _enter_dungeon(self, dungeon_exit_data):
		"""
		Actually enters the dungeon (after yes confirmation).
		
		Args:
			dungeon_exit_data: The exit data containing dungeon info
			
		Note: This is the THIRD line of defense - we check availability once more
		just before actually creating the dungeon instance.
		"""
		try:
			# Final defensive check before entering
			is_available, reason = self._check_dungeon_system_available()
			if not is_available:
				return f"Dungeon system error: {reason}"
			
			dungeon_id = dungeon_exit_data.get("dungeon_id")
			transition_text = dungeon_exit_data.get("transition_text", "You enter the dungeon...")
			
			result = f"\n{transition_text}\n"
			
			# Get the scheduler instance
			scheduler = get_scheduler(game_engine=self.engine)
			
			# Determine which overworld room the player is entering from
			# so we can route the "leave" exit back to the correct entrance
			overworld_entrance = self.engine.player.current_room
			
			# Try to get the active dungeon instance
			# First check if we have one stored (from debug command)
			active_dungeon = self.engine.current_dungeon_instance
			
			# Fallback: try to get from global state
			if not active_dungeon:
				active_dungeon = get_current_dungeon(scheduler, entrance_room_id=overworld_entrance)
			
			if not active_dungeon:
				return result + "\n[Error: Could not load dungeon instance]"
			
			if not active_dungeon.dungeon_data:
				return result + "\n[Error: Dungeon has no data]"
			
			result += "\n✓ Dungeon generated!\n"
			
			# Store the dungeon instance on engine
			self.engine.current_dungeon_instance = active_dungeon
			
			# PRE-REGISTER all dungeon rooms into engine.rooms
			# This ensures get_room_data() finds them immediately via the rooms dict
			# instead of needing the dungeon parsing path (which can fail silently)
			self._register_dungeon_rooms(active_dungeon)
			
			# Get entrance room
			floor_1_data = active_dungeon.dungeon_data.get("floors", {}).get(1, {})
			entrance_room_id = floor_1_data.get("entrance_room")
			
			if not entrance_room_id:
				return result + "\n[Error: No entrance room in dungeon]"
			
			# Move player to entrance
			self.engine.player.current_room = entrance_room_id
			self._update_map_on_move(entrance_room_id)
			
			result += "\n╔════════════════════════════════════════════════════════╗\n"
			result += "║  You have entered the dungeon!                         ║\n"
			result += "╚════════════════════════════════════════════════════════╝\n"
			
			# Get the room description (should always work now since rooms are pre-registered)
			room = self.engine.get_room_data(entrance_room_id)
			if room:
				result += "\n" + room.describe()
			else:
				# Last-resort fallback: build description from raw dungeon data
				direct_room = floor_1_data.get("rooms", {}).get(entrance_room_id)
				if direct_room:
					name = direct_room.get("name", "Dungeon Entrance")
					desc = direct_room.get("description", "You stand in the dungeon entrance.")
					exits = direct_room.get("exits", {})
					exit_names = list(exits.keys())
					result += f"\n{name}\n{desc}\n"
					if exit_names:
						result += f"Exits: {', '.join(exit_names)}\n"
				else:
					result += "\n[Dungeon entrance room not found]"
			
			# Update live map to show dungeon floor
			self._update_map_on_move(entrance_room_id)
			
			return result
		
		except Exception as e:
			import traceback
			traceback.print_exc()
			return f"Error entering dungeon: {str(e)}"
	
	def _handle_fixed_dungeon_entrance(self, exit_info):
		"""
		Handle entering a fixed (always-open, hand-crafted) dungeon.
		Shows dungeon info and asks for yes/no confirmation.
		"""
		dungeon_id = exit_info.get("dungeon_id", "unknown")
		
		# Load the dungeon data to get name/description
		dungeon_data = self.engine._load_fixed_dungeon(dungeon_id)
		if not dungeon_data:
			return f"The entrance seems sealed. [Error: Fixed dungeon '{dungeon_id}' not found]"
		
		# Check skill/level requirements
		meets_reqs, req_msg = self._check_dungeon_requirements(dungeon_data)
		if not meets_reqs:
			name = dungeon_data.get("name", "Unknown Dungeon")
			return f"\n  {name}\n{req_msg}"
		
		name = dungeon_data.get("name", "Unknown Dungeon")
		description = dungeon_data.get("description", "A mysterious dungeon.")
		num_floors = dungeon_data.get("num_floors", "?")
		difficulty = dungeon_data.get("difficulty", "unknown")
		
		result = "\n" + "-" * 60 + "\n"
		result += "╔════════════════════════════════════════════════════════╗\n"
		result += "║              DUNGEON ENTRANCE DETECTED                 ║\n"
		result += "╚════════════════════════════════════════════════════════╝\n"
		result += f"\n  {name}\n"
		result += f"  {description}\n\n"
		result += f"  Floors: {num_floors}\n"
		result += f"  Difficulty: {difficulty.replace('_', ' ').title()}\n\n"
		result += "  Status: ALWAYS OPEN\n\n"
		result += "  This is a permanent dungeon with a fixed layout.\n"
		result += "  Unlike time-gated dungeons, this dungeon:\n"
		result += "    * Never closes or regenerates\n"
		result += "    * Has a hand-crafted layout with unique rooms\n"
		result += "    * Contains many traps and valuable loot\n"
		result += "    * Has a crafting altar on the deepest floor\n\n"
		result += "---\n\n"
		result += "Do you wish to enter? (yes/no)\n"
		
		# Set pending flag with fixed marker
		self.engine.pending_dungeon_entry = {
			"dungeon_data": exit_info,
			"fixed": True
		}
		result += "-" * 60 + "\n"
		
		return result

	def _enter_fixed_dungeon(self, exit_data):
		"""
		Actually enter a fixed dungeon (after yes confirmation).
		Loads dungeon from JSON, registers rooms, moves player to entrance.
		"""
		try:
			dungeon_id = exit_data.get("dungeon_id")
			transition_text = exit_data.get("transition_text", "You enter the dungeon...")
			
			result = f"\n{transition_text}\n"
			
			# Load the dungeon data
			dungeon_data = self.engine._load_fixed_dungeon(dungeon_id)
			if not dungeon_data:
				return result + f"\n[Error: Could not load fixed dungeon '{dungeon_id}']"
			
			# Store the overworld room we're entering from
			overworld_entrance = self.engine.player.current_room
			
			# Create a lightweight wrapper for trap system compatibility
			# TrapSystem.find_raw_room needs .dungeon_data with floors/rooms structure
			class FixedDungeonWrapper:
				def __init__(self, data, entrance_id):
					self.dungeon_data = data
					self.entrance_room_id = entrance_id
			
			wrapper = FixedDungeonWrapper(dungeon_data, overworld_entrance)
			self.engine.current_dungeon_instance = wrapper
			self.engine.current_fixed_dungeon = dungeon_data
			
			# Register all rooms from the fixed dungeon
			self.engine.fixed_dungeon_room_ids.clear()
			floors = dungeon_data.get("floors", {})
			registered = 0
			for floor_num, floor_data in floors.items():
				rooms = floor_data.get("rooms", {})
				for room_id, room_dict in rooms.items():
					if room_id not in self.engine.rooms:
						try:
							converted = self.engine._convert_dungeon_room_to_world(room_dict)
							self.engine.rooms[room_id] = Room(converted)
							self.engine.fixed_dungeon_room_ids.add(room_id)
							registered += 1
						except Exception as e:
							print(f"[ERROR] Failed to register fixed dungeon room '{room_id}': {e}")
			
			print(f"[DEBUG] Registered {registered} fixed dungeon rooms into engine.rooms")
			
			# Get entrance room (floor keys are strings in JSON)
			floor_1_data = floors.get("1", floors.get(1, {}))
			entrance_room_id = floor_1_data.get("entrance_room")
			
			if not entrance_room_id:
				return result + "\n[Error: No entrance room in fixed dungeon]"
			
			# Move player
			self.engine.player.current_room = entrance_room_id
			self._update_map_on_move(entrance_room_id)
			
			result += "\n✓ Dungeon loaded!\n"
			
			dungeon_name = dungeon_data.get('name', 'the dungeon')
			result += "\n╔════════════════════════════════════════════════════════╗\n"
			result += f"║  You have entered {dungeon_name}!{' ' * max(0, 37 - len(dungeon_name))}║\n"
			result += "╚════════════════════════════════════════════════════════╝\n"
			
			room = self.engine.get_room_data(entrance_room_id)
			if room:
				result += "\n" + room.describe()
			
			# Check for traps in entrance room
			trap_msg = self._check_room_traps(entrance_room_id)
			if trap_msg:
				result += "\n" + trap_msg
			
			# Track achievement for elite dungeon entry
			if ACHIEVEMENT_AVAILABLE:
				try:
					difficulty = dungeon_data.get('difficulty', '')
					if difficulty == 'extreme':
						track_event(self.engine.player, "elite_dungeons_entered")
					result += self._check_and_show_achievements()
				except Exception:
					pass
			
			return result
		
		except Exception as e:
			import traceback
			traceback.print_exc()
			return f"Error entering fixed dungeon: {str(e)}"
	
	def _register_dungeon_rooms(self, dungeon_instance):
		"""
		Pre-register all dungeon rooms into self.engine.rooms so they can be
		found by get_room_data() through the normal world rooms lookup.
		This avoids issues with the dungeon-specific parsing path.
		
		Args:
			dungeon_instance: Active DungeonInstance with generated data
		"""
		if not dungeon_instance or not dungeon_instance.dungeon_data:
			return
		
		registered = 0
		floors = dungeon_instance.dungeon_data.get("floors", {})
		for floor_num, floor_data in floors.items():
			rooms = floor_data.get("rooms", {})
			for room_id, room_dict in rooms.items():
				if room_id not in self.engine.rooms:
					try:
						converted = self.engine._convert_dungeon_room_to_world(room_dict)
						self.engine.rooms[room_id] = Room(converted)
						registered += 1
					except Exception as e:
						print(f"[ERROR] Failed to register dungeon room '{room_id}': {e}")
						import traceback
						traceback.print_exc()
		
		print(f"[DEBUG] Registered {registered} dungeon rooms into engine.rooms")

	def _unregister_dungeon_rooms(self):
		"""
		Remove all dungeon rooms from engine.rooms.
		Called when the dungeon closes or regenerates so stale rooms don't linger.
		"""
		to_remove = [rid for rid in self.engine.rooms if rid.startswith("dungeon_") and "_floor" in rid]
		for rid in to_remove:
			del self.engine.rooms[rid]
		if to_remove:
			print(f"[DEBUG] Unregistered {len(to_remove)} dungeon rooms from engine.rooms")
	
	def _describe_exits(self, room, location_type="wilderness"):
		"""Format exit description based on location type."""
		exits = room.exits or {}
		if not exits:
			return "There are no exits here."
		
		directional = []
		named = []
		
		for direction, exit_data in exits.items():
			if isinstance(exit_data, str):
				# Old format
				if direction in {"north", "south", "east", "west"}:
					directional.append(direction)
				else:
					named.append(direction)
			elif isinstance(exit_data, dict):
				# New format
				exit_type = exit_data.get("type", "direction")
				display = exit_data.get("display", direction)
				if exit_type == "direction":
					directional.append(direction)
				else:
					named.append(display)
		
		parts = []
		
		if location_type == "settlement" or location_type == "building":
			if named:
				parts.append(f"You can travel to: {', '.join(named)}")
			if directional:
				parts.append(f"Compass directions: {', '.join(directional)}")
		else:
			# Wilderness style
			if directional:
				parts.append(f"Exits: {', '.join(directional)}")
			if named:
				parts.append(f"You can also travel to: {', '.join(named)}")
		
		if not parts:
			return "There are no exits here."
		
		return "\n".join(parts)

	def _look(self):
		room = self.engine.get_room_data(self.engine.player.current_room)
		if not room:
			return "[Current room not found]"
		result = room.describe()
		# Show visible overworld enemies
		if OVERWORLD_AVAILABLE and self.engine.encounter_manager:
			vis = self.engine.encounter_manager.get_visible_enemy_text(self.engine.player.current_room)
			if vis:
				result += vis
		return result

	# helper inventory modifiers
	def _add_to_inventory(self, item_name, count=1):
		if not item_name:
			return
		inv = self.engine.player.inventory
		inv[item_name] = inv.get(item_name, 0) + int(count)

	def _remove_from_inventory(self, item_name, count=1):
		inv = self.engine.player.inventory
		if item_name not in inv:
			return False
		try:
			cnt = int(count)
		except Exception:
			cnt = 1
		if inv[item_name] > cnt:
			inv[item_name] -= cnt
		else:
			# remove key
			inv.pop(item_name, None)
		return True

	def _collect(self, item_spec):
		"""Collect an item from the current room into the player's inventory.
		Supports: 'collect <item>' or 'collect <N> <item>' where N is an integer count.
		"""
		if not self.engine.player:
			return "No game in progress."
		room = self.engine.get_room_data(self.engine.player.current_room)
		if room is None:
			return "You are nowhere."

		spec = (item_spec or "").strip()
		if not spec:
			return "Collect what?"
		# parse optional leading count
		toks = spec.split()
		count = 1
		item = spec
		if toks:
			try:
				first = int(toks[0])
				if first > 0 and len(toks) > 1:
					count = first
					item = " ".join(toks[1:])
			except Exception:
				# not a number; treat entire spec as item name
				item = spec

		item = item.strip()
		if not item:
			return "Collect what?"

		available = room.items.count(item)
		if available <= 0:
			return "There is no such item here."
		to_take = min(count, available)
		# remove that many occurrences from room.items
		removed = 0
		for _ in range(to_take):
			try:
				room.items.remove(item)
				removed += 1
			except ValueError:
				break
		if removed <= 0:
			return "There is no such item here."
		# add to player's inventory
		self._add_to_inventory(item, removed)
		try:
			self.engine._inventory_changed = True
		except Exception:
			pass
		# Notify quest system of inventory change
		if QUEST_AVAILABLE and hasattr(self.engine, 'quest_manager') and self.engine.quest_manager:
			self.engine.quest_manager.on_item_changed()
		if removed == 1:
			return f"collected `{item}`"
		else:
			return f"collected {removed} `{item}`"

	def _drop(self, item_name):
		"""Drop an item from the player's inventory into the current room.
		Decrement count, and add to room.items.
		"""
		if not self.engine.player:
			return "No game in progress."
		item_name = item_name.strip()
		if not item_name:
			return "Drop what?"
		inv = self.engine.player.inventory
		if item_name in inv:
			# decrement count or remove
			if inv[item_name] > 1:
				inv[item_name] -= 1
			else:
				inv.pop(item_name, None)
			# add to current room items
			room = self.engine.get_room_data(self.engine.player.current_room)
			if room is None:
				# put it back if something goes wrong
				inv[item_name] = inv.get(item_name, 0) + 1
				return "You are nowhere to drop that."
			# add an instance to room items (allow duplicates)
			room.items.append(item_name)
			# mark inventory changed for UI
			try:
				self.engine._inventory_changed = True
			except Exception:
				pass
			# auto-save so the dropped item persists permanently
			try:
				self.engine.save_game()
			except Exception:
				pass
			# Build a summary of what's now on the floor
			floor_counts = {}
			for it in room.items:
				floor_counts[it] = floor_counts.get(it, 0) + 1
			floor_parts = []
			for it, cnt in floor_counts.items():
				if cnt > 1:
					pl = it + "s" if not it.endswith("s") else it
					floor_parts.append(f"{cnt} {pl}")
				else:
					floor_parts.append(it)
			floor_line = "  On the floor: " + ", ".join(floor_parts) + "."
			return f"You drop the {item_name}.\n{floor_line}"
		else:
			return "You don't have that."

	def _inventory(self):
		inv = self.engine.player.inventory
		if not inv:
			return "You are carrying nothing."

		# Categorize items
		equipment_items = {}
		consumables = {}
		materials = {}
		misc = {}

		for item_id, qty in inv.items():
			# Check if it's equipment
			if EQUIPMENT_AVAILABLE and item_id in EQUIPMENT_DATABASE:
				equipment_items[item_id] = qty
			elif ITEM_EFFECTS_AVAILABLE and self.engine.item_effects and self.engine.item_effects.get_item_info(item_id):
				consumables[item_id] = qty
			elif CRAFTING_AVAILABLE and self._is_crafting_material(item_id):
				materials[item_id] = qty
			else:
				misc[item_id] = qty

		result = "\n" + "═" * 55 + "\n"
		result += "  🎒 INVENTORY\n"
		result += "═" * 55 + "\n"

		def _nice(item_id):
			"""Get display name from various databases."""
			if EQUIPMENT_AVAILABLE and item_id in EQUIPMENT_DATABASE:
				return EQUIPMENT_DATABASE[item_id].get("name", item_id.replace("_", " ").title())
			if ITEM_EFFECTS_AVAILABLE and self.engine.item_effects:
				info = self.engine.item_effects.get_item_info(item_id)
				if info and info.get("description"):
					pass  # Just use item_id formatting below
			if SHOP_AVAILABLE:
				try:
					from shop_system import ITEM_DATABASE
					if item_id in ITEM_DATABASE:
						return ITEM_DATABASE[item_id].get("name", item_id.replace("_", " ").title())
				except ImportError:
					pass
			return item_id.replace("_", " ").title()

		def _icon(item_id):
			"""Get icon for item."""
			if SHOP_AVAILABLE:
				try:
					from shop_system import ITEM_DATABASE
					if item_id in ITEM_DATABASE:
						return ITEM_DATABASE[item_id].get("icon", "•")
				except ImportError:
					pass
			if EQUIPMENT_AVAILABLE and item_id in EQUIPMENT_DATABASE:
				slot = EQUIPMENT_DATABASE[item_id].get("slot", "")
				icons = {"weapon": "⚔️", "armor": "🛡️", "shield": "🛡️", "accessory": "💍"}
				return icons.get(slot, "•")
			return "•"

		if equipment_items:
			result += "\n  ⚔️  EQUIPMENT\n"
			for iid, qty in equipment_items.items():
				eq = EQUIPMENT_DATABASE.get(iid, {})
				name = eq.get("name", iid.replace("_", " ").title())
				stats = eq.get("stats", {})
				stat_str = ", ".join(f"+{v} {k[:3].upper()}" for k, v in stats.items())
				result += f"    {name} x{qty}"
				if stat_str:
					result += f"  ({stat_str})"
				result += "\n"

		if consumables:
			result += "\n  🧪 CONSUMABLES\n"
			for iid, qty in consumables.items():
				name = _nice(iid)
				result += f"    {name} x{qty}\n"

		if materials:
			result += "\n  🔧 MATERIALS\n"
			for iid, qty in materials.items():
				name = _nice(iid)
				result += f"    {name} x{qty}\n"

		if misc:
			result += "\n  📦 OTHER\n"
			for iid, qty in misc.items():
				name = _nice(iid)
				result += f"    {name} x{qty}\n"

		# Gold
		gold = self.engine.player.state.get("gold", 0)
		result += f"\n  💰 Gold: {gold}\n"
		result += "\n  Tip: 'inspect <item>' for details\n"
		result += "═" * 55 + "\n"
		return result

	def _is_crafting_material(self, item_id):
		"""Check if an item is used as a crafting ingredient."""
		if not CRAFTING_AVAILABLE:
			return False
		try:
			from crafting_system import RECIPE_DATABASE
			for recipe in RECIPE_DATABASE.values():
				if item_id in recipe.get("ingredients", {}):
					return True
		except ImportError:
			pass
		# Check enchanting materials
		if ENCHANTING_AVAILABLE:
			try:
				from enchanting_system import ENCHANTMENTS
				for altar_enchants in ENCHANTMENTS.values():
					for ench in altar_enchants.values():
						if item_id in ench.get("materials", {}):
							return True
			except ImportError:
				pass
		return False

	def _help(self):
		return "Commands: go [dir], look, collect [item], drop [item], inventory, save, load, quit\nRooms may also define custom actions (try commands specific to the room)."

	def _examine(self, target):
		"""Examine/inspect an object or location. Handles secret room discovery and provides detailed feedback."""
		target = target.lower()
		room = self.engine.get_room_data(self.engine.player.current_room)
		
		# Check for secret room discovery in boss chamber
		if room and target in ("wall", "walls", "room", "stone", "carvings", "ornate wall", "ornate walls", "the wall", "stone wall"):
			# Check for is_boss_room attribute (works with both dicts and Room objects)
			is_boss = False
			has_secret = False
			secret_discovered = False
			
			if isinstance(room, dict):
				is_boss = room.get("is_boss_room")
				has_secret = room.get("has_secret")
				secret_discovered = room.get("secret_discovered")
			elif hasattr(room, "is_boss_room"):
				is_boss = getattr(room, "is_boss_room", False)
				has_secret = getattr(room, "has_secret", False)
				secret_discovered = getattr(room, "secret_discovered", False)
			
			if is_boss and has_secret and not secret_discovered:
				return self._discover_secret_room(room)
			elif is_boss and secret_discovered:
				return "The secret passage you discovered is still open.\nUse 'go secret' to enter it."
			elif is_boss:
				return "You carefully examine the walls of the boss chamber.\nThe ancient stone shows signs of many battles, but nothing else stands out."
			else:
				# Not a boss room, but still examining walls
				return "You carefully examine the walls.\nThe stone is cold and weathered. Nothing unusual stands out."
		
		# Chest inspection
		if target in ("chest", "treasure chest", "box", "the chest"):
			if isinstance(room, dict):
				chests = room.get("chests", [])
				if chests:
					unopened = [c for c in chests if not c.get("opened")]
					if unopened:
						chest_type = unopened[0].get("type", "wooden")
						return f"You inspect the chest closely.\nIt's a {chest_type} chest, securely locked.\nType 'open chest' to attempt to open it."
					else:
						return "The chest is empty - already looted."
				return "There's no chest here to inspect."
		
		# Trap inspection
		if "trap" in target:
			if isinstance(room, dict):
				traps = room.get("traps", [])
				visible_traps = [t for t in traps if not t.get("triggered") and not t.get("disarmed")]
				if visible_traps:
					trap = visible_traps[0]
					trap_type = trap.get("type", "unknown")
					return f"You spot a {trap_type.replace('_', ' ')}!\nIt looks dangerous.\nType 'disarm' to attempt to disarm it."
				else:
					return "You don't see any traps here.\nTry 'search' to look for hidden traps."
			return "You don't see any traps here."
		
		# Ground/floor inspection
		if target in ("ground", "floor", "the floor", "the ground"):
			if isinstance(room, dict):
				items = room.get("items", {})
				if items:
					return "You examine the ground.\nYou see some items scattered about.\nType 'look' to see what's available."
				else:
					return "You examine the ground.\nNothing interesting on the floor."
			elif hasattr(room, "items"):
				if room.items:
					return "You examine the ground.\nYou see some items scattered about.\nType 'look' to see what's available."
				else:
					return "You examine the ground.\nNothing interesting on the floor."
		
		# Regular inventory/item examination
		target_id = target.replace(" ", "_")
		if target_id in self.engine.player.inventory or target in self.engine.player.inventory:
			item_id = target_id if target_id in self.engine.player.inventory else target
			return self._examine_item(item_id)
		if not room:
			return "You don't see that here."
		if target in room.items:
			return f"You examine the {target} in the room.\nIt looks useful. Type 'take {target}' to pick it up."
		# Also try snake_case version for room items
		if target_id in room.items:
			return f"You examine the {target} in the room.\nIt looks useful. Type 'take {target_id}' to pick it up."
		return f"You don't see any '{target}' here to examine.\n\nTry examining:\n  - wall (look for secrets)\n  - chest (examine containers)\n  - ground (search the floor)\n  - <item_name> (inspect items)"

	def _examine_item(self, item_id):
		"""Show detailed info about an inventory item, pulling from all databases."""
		qty = self.engine.player.inventory.get(item_id, 0)
		nice_name = item_id.replace("_", " ").title()

		result = "\n" + "═" * 55 + "\n"

		# ── Equipment ──
		if EQUIPMENT_AVAILABLE and item_id in EQUIPMENT_DATABASE:
			eq = EQUIPMENT_DATABASE[item_id]
			result += f"  ⚔️  {eq.get('name', nice_name)}\n"
			result += "═" * 55 + "\n"
			result += f"  {eq.get('description', 'No description.')}\n\n"
			result += f"  Type: Equipment ({eq.get('slot', '?').title()})\n"
			result += f"  Quantity: {qty}\n"
			if eq.get("stats"):
				result += "\n  Stats when equipped:\n"
				for stat, val in eq["stats"].items():
					nice_stat = stat.replace("_", " ").capitalize()
					result += f"    +{val} {nice_stat}\n"
			# Show current player stat comparison
			equipment = self.engine.player.state.get("equipment", {})
			current_in_slot = equipment.get(eq.get("slot"))
			if current_in_slot and current_in_slot != item_id:
				cur_data = EQUIPMENT_DATABASE.get(current_in_slot, {})
				result += f"\n  Currently equipped: {cur_data.get('name', current_in_slot)}\n"
				result += "  Comparison:\n"
				all_stats = set(list(eq.get("stats", {}).keys()) + list(cur_data.get("stats", {}).keys()))
				for stat in sorted(all_stats):
					new_val = eq.get("stats", {}).get(stat, 0)
					old_val = cur_data.get("stats", {}).get(stat, 0)
					diff = new_val - old_val
					nice_stat = stat.replace("_", " ").capitalize()
					if diff > 0:
						result += f"    {nice_stat}: +{new_val} (▲ +{diff})\n"
					elif diff < 0:
						result += f"    {nice_stat}: +{new_val} (▼ {diff})\n"
					else:
						result += f"    {nice_stat}: +{new_val} (=)\n"
			elif not current_in_slot:
				result += f"\n  Slot is empty — equip with 'equip {item_id}'\n"
			# Show worth
			try:
				from crafting_system import CRAFTED_ITEM_WORTH
				if item_id in CRAFTED_ITEM_WORTH:
					result += f"\n  Worth: {CRAFTED_ITEM_WORTH[item_id]} gold\n"
			except ImportError:
				pass
			result += "═" * 55 + "\n"
			return result

		# ── Consumable / Usable ──
		item_info = None
		if ITEM_EFFECTS_AVAILABLE and self.engine.item_effects:
			item_info = self.engine.item_effects.get_item_info(item_id)
		if item_info:
			result += f"  🧪 {nice_name}\n"
			result += "═" * 55 + "\n"
			desc = item_info.get("description", "No description.")
			result += f"  {desc}\n\n"
			result += f"  Type: {item_info.get('type', 'item').title()}\n"
			result += f"  Effect: {item_info.get('effect', 'none').replace('_', ' ').title()}\n"
			if item_info.get("value"):
				result += f"  Power: {item_info['value']}\n"
			result += f"  Quantity: {qty}\n"
			result += f"\n  Use with 'use {item_id}'\n"
			result += "═" * 55 + "\n"
			return result

		# ── Cooked food ──
		if FISHING_AVAILABLE:
			try:
				from fishing_system import COOKED_FOOD_EFFECTS
				if item_id in COOKED_FOOD_EFFECTS:
					food = COOKED_FOOD_EFFECTS[item_id]
					result += f"  🍳 {nice_name}\n"
					result += "═" * 55 + "\n"
					result += f"  Type: Cooked Food\n"
					result += f"  Quantity: {qty}\n\n"
					effects = []
					if food.get("heal"):
						effects.append(f"Heals {food['heal']} HP")
					if food.get("cure_poison"):
						effects.append("Cures poison")
					if food.get("temp_stats"):
						for stat, val in food["temp_stats"].items():
							effects.append(f"+{val} {stat.upper()} (temporary)")
					if food.get("xp"):
						effects.append(f"+{food['xp']} XP")
					if effects:
						result += "  Effects:\n"
						for e in effects:
							result += f"    • {e}\n"
					result += f"\n  Use with 'use {item_id}'\n"
					result += "═" * 55 + "\n"
					return result
			except ImportError:
				pass

		# ── Shop database ──
		if SHOP_AVAILABLE:
			try:
				from shop_system import ITEM_DATABASE
				if item_id in ITEM_DATABASE:
					idata = ITEM_DATABASE[item_id]
					result += f"  {idata.get('icon', '📦')} {idata.get('name', nice_name)}\n"
					result += "═" * 55 + "\n"
					result += f"  {idata.get('desc', 'No description.')}\n\n"
					result += f"  Rarity: {idata.get('rarity', 'common').title()}\n"
					result += f"  Value: {idata.get('value', '?')} gold\n"
					result += f"  Quantity: {qty}\n"
					result += "═" * 55 + "\n"
					return result
			except ImportError:
				pass

		# ── Crafting recipes that produce this item ──
		recipe_info = ""
		if CRAFTING_AVAILABLE:
			try:
				from crafting_system import RECIPE_DATABASE, CRAFTED_ITEM_WORTH
				for rid, recipe in RECIPE_DATABASE.items():
					res_id = recipe.get("result", (None,))[0]
					if res_id == item_id:
						recipe_info = f"\n  Crafted from: {recipe.get('name', rid)}\n"
						recipe_info += f"  {recipe.get('description', '')}\n"
						break
				worth = CRAFTED_ITEM_WORTH.get(item_id)
				if worth:
					recipe_info += f"  Worth: {worth} gold\n"
			except ImportError:
				pass

		# ── Generic fallback ──
		result += f"  📦 {nice_name}\n"
		result += "═" * 55 + "\n"
		result += f"  Quantity: {qty}\n"

		# Check if it's used in any recipe
		used_in = []
		if CRAFTING_AVAILABLE:
			try:
				from crafting_system import RECIPE_DATABASE
				for rid, recipe in RECIPE_DATABASE.items():
					if item_id in recipe.get("ingredients", {}):
						used_in.append(recipe.get("name", rid))
			except ImportError:
				pass
		if ENCHANTING_AVAILABLE:
			try:
				from enchanting_system import ENCHANTMENTS
				for altar_enchants in ENCHANTMENTS.values():
					for ench in altar_enchants.values():
						if item_id in ench.get("materials", {}):
							used_in.append(f"{ench['name']} (enchant)")
			except ImportError:
				pass

		if used_in:
			result += "\n  Used in:\n"
			for u in used_in[:6]:
				result += f"    • {u}\n"
			if len(used_in) > 6:
				result += f"    ... and {len(used_in)-6} more\n"

		if recipe_info:
			result += recipe_info

		result += "═" * 55 + "\n"
		return result

	def _search_room(self):
		"""Actively search the current room for hidden traps and items."""
		room_id = self.engine.player.current_room
		room = self.engine.get_room_data(room_id)
		if not room:
			return "[Room not found]"
		
		result_parts = []
		found_something = False
		
		# Search for traps in dungeon rooms
		raw_room = TrapSystem.find_raw_room(
			self.engine.current_dungeon_instance, room_id
		) if TRAP_AVAILABLE else None
		
		if raw_room:
			traps = raw_room.get("traps", [])
			active_traps = [t for t in traps if not t.get("triggered") and not t.get("disarmed")]
			if active_traps:
				found_something = True
				for trap in active_traps:
					trap_name = trap.get("name", trap.get("type", "trap").replace("_", " "))
					warning = trap.get("warning_signs", "Something seems dangerous here.")
					result_parts.append(
						f"⚠️  You found a {trap_name}!\n"
						f"   {warning}\n"
						f"   Type 'disarm' to attempt to disarm it."
					)
			
			# Search for chests
			chests = raw_room.get("chests", [])
			unopened = [c for c in chests if not c.get("opened")]
			if unopened:
				found_something = True
				for chest in unopened:
					chest_type = chest.get("type", "wooden").replace("_", " ")
					result_parts.append(
						f"📦 You found a {chest_type}!\n"
						f"   Type 'open chest' to try opening it."
					)
			
			# Check for triggered/disarmed traps
			old_traps = [t for t in traps if t.get("triggered") or t.get("disarmed")]
			if old_traps:
				for trap in old_traps:
					trap_name = trap.get("name", trap.get("type", "trap").replace("_", " "))
					if trap.get("disarmed"):
						result_parts.append(f"   A disarmed {trap_name} lies here.")
					else:
						result_parts.append(f"   The remains of a triggered {trap_name} are visible.")
		
		# Check for items on the ground
		if hasattr(room, "items") and room.items:
			found_something = True
			result_parts.append(f"You see items on the ground. Type 'look' to see what's available.")
		
		if not found_something:
			return "You search the room carefully...\n\nYou don't find anything hidden."
		
		header = "You search the room carefully...\n\n"
		return header + "\n\n".join(result_parts)

	def _open_chest(self):
		"""Open a treasure chest in the current room."""
		room_id = self.engine.player.current_room
		
		# Find chest in raw dungeon data
		raw_room = TrapSystem.find_raw_room(
			self.engine.current_dungeon_instance, room_id
		) if TRAP_AVAILABLE else None
		
		if not raw_room:
			return "There's no chest here to open."
		
		chests = raw_room.get("chests", [])
		if not chests:
			return "There's no chest here to open."
		
		# Find first unopened chest
		chest = None
		for c in chests:
			if not c.get("opened"):
				chest = c
				break
		
		if not chest:
			return "All chests in this room have already been opened."
		
		# Open the chest
		chest["opened"] = True
		chest_type = chest.get("type", "wooden").replace("_", " ")
		contents = chest.get("contents", {})
		
		result = "\n" + "=" * 50 + "\n"
		result += f"📦 You open the {chest_type}!\n"
		result += "=" * 50 + "\n"
		
		got_something = False
		
		# Check for double loot ability (Rogue Plunder)
		loot_multiplier = 1
		if PROGRESSION_AVAILABLE and has_active_effect(self.engine.player, "double_loot"):
			loot_multiplier = 2
			result += "\n  ** PLUNDER ACTIVE — Double loot! **\n"
			# Clear the one-shot effect
			active = self.engine.player.state.get("active_effects", {})
			if "double_loot" in active:
				active["double_loot"] = 0

		# Add gold
		gold = contents.get("gold", 0) * loot_multiplier
		if gold > 0:
			got_something = True
			self.engine.player.stats["gold"] = self.engine.player.stats.get("gold", 0) + gold
			result += f"\n💰 You found {gold} gold!\n"
		
		# Add items
		items = contents.get("items", {})
		if items:
			got_something = True
			result += "\nItems found:\n"
			for item_name, item_data in items.items():
				if isinstance(item_data, dict):
					qty = item_data.get("quantity", 1) * loot_multiplier
					value = item_data.get("value", 10)
				else:
					qty = 1 * loot_multiplier
					value = 10
				
				self._add_to_inventory(item_name, qty)
				# Store item value
				if item_name not in self.engine.item_worth:
					self.engine.item_worth[item_name] = value
				
				result += f"  • {item_name} x{qty}\n"
		
		if not got_something:
			result += "\nThe chest is empty!\n"
		
		result += "\n" + "=" * 50 + "\n"
		
		# Award XP for opening chest
		if PROGRESSION_AVAILABLE:
			try:
				chest_raw = chest.get("type", "wooden")
				xp_key = f"open_chest_{chest_raw}"
				xp_amount = XP_AWARDS.get(xp_key, XP_AWARDS.get("open_chest_wooden", 10))
				result += award_xp(self.engine.player, xp_amount, f"opened {chest_type}")
			except Exception:
				pass
		
		# Track chest gold for achievements
		if ACHIEVEMENT_AVAILABLE and gold > 0:
			try:
				track_event(self.engine.player, "total_gold", gold)
				result += self._check_and_show_achievements()
			except Exception:
				pass
		
		# Notify UI of inventory change
		try:
			self.engine._inventory_changed = True
		except Exception:
			pass
		
		return result

	def _discover_secret_room(self, boss_room):
		"""Handle secret room discovery in boss chamber with full visual experience."""
		# Handle both dict and Room objects
		has_secret = False
		secret_room_id = None
		
		if isinstance(boss_room, dict):
			has_secret = boss_room.get("has_secret")
			secret_room_id = boss_room.get("secret_room_id")
		elif hasattr(boss_room, "has_secret"):
			has_secret = boss_room.has_secret
			secret_room_id = getattr(boss_room, "secret_room_id", None)
		
		if not has_secret:
			return "You examine the walls carefully, but find nothing unusual."
		
		# Mark secret as discovered (both in room and player state)
		if isinstance(boss_room, dict):
			boss_room["secret_discovered"] = True
		elif hasattr(boss_room, "secret_discovered"):
			boss_room.secret_discovered = True
		
		self.engine.player.state["secret_discovered"] = True
		
		# Add secret exit to boss room
		if secret_room_id:
			if isinstance(boss_room, dict):
				boss_room["exits"]["secret"] = {
					"target": secret_room_id,
					"type": "secret"
				}
			elif hasattr(boss_room, "exits"):
				boss_room.exits["secret"] = {
					"target": secret_room_id,
					"type": "secret"
				}
		
		xp_msg = ""
		if PROGRESSION_AVAILABLE:
			try:
				xp_msg = award_xp(self.engine.player, XP_AWARDS.get("discover_secret_room", 50), "discovered secret room!")
			except Exception:
				pass
		
		return ("\n" + "="*80 + "\n"
				"You carefully examine the walls...\n"
				"\n"
				"Wait... one section seems different!\n"
				"The carvings form a pattern... it's a hidden mechanism!\n"
				"\n"
				"You press the suspicious stone...\n"
				"\n"
				"*CLICK*\n"
				"\n"
				"A hidden doorway grinds open with ancient gears!\n"
				"A secret passage is revealed!\n"
				"="*80 + "\n"
				"\n"
				"You can now 'go secret' to enter the hidden passage!\n"
				+ xp_msg)

	def _enter_secret_room(self, secret_room_id):
		"""Enter and display the secret chamber with ASCII art easter egg."""
		self.engine.player.current_room = secret_room_id
		
		room = self.engine.get_room_data(secret_room_id)
		if not room:
			return "The secret passage leads nowhere..."
		
		self._update_map_on_move(secret_room_id)
		
		# Display spectacular entrance with ASCII art
		ascii_art = r"""
               ___.-------.___
           _.-'     /   \     '-._
         .'   /   /  |  \  \   '.
        /   /   / /| |\ \   \   \
       /   /   /_/ | | \_\   \   \
      |   |  .' \  | |  / '.  |   |
      |   | /    `.|.|.'    \ |   |
      |   |/  .-.  |||  .-.  \|   |
      |    \ |   | ||| |   | /    |
      |     \\  '-' ||| '-'  //     |
      |.     `\    |||    /'     .|
      |  '-.   `.  |||  .'   .-'  |
      |     '-. ;--'-'--; .-'     |
      |        '| VAULT |'        |
      |         | ~~~~~ |         |
      \         |  ___  |         /
       \        | |   | |        /
        `.      | |___| |      .'
          `-.   |_______|   .-'
             `-.  |   |  .-'
                `-'   '-'
"""
		
		room_name = ""
		room_desc = ""
		if isinstance(room, dict):
			room_name = room.get("name", "Secret Chamber")
			room_desc = room.get("description", "A hidden chamber.")
		else:
			room_name = room.name
			room_desc = room.description
		
		return ("\n\n"
				"="*80 + "\n"
				"🌟 YOU'VE DISCOVERED THE SECRET CHAMBER! 🌟\n"
				"="*80 + "\n"
				"\n"
				+ ascii_art +
				"\n"
				"Ancient runes glow on the walls, spelling out a legendary name...\n"
				"This secret has been hidden for centuries.\n"
				"You are among the few who have found it.\n"
				"\n"
				+ f"{room_name}\n"
				+ f"{room_desc}\n"
				"\n"
				"[Type 'go back' to return to the treasure vault]")

	def _sell(self, item_name):
		"""Sell an item for its standard worth value."""
		if not item_name:
			return "Sell what?"
		inv = self.engine.player.inventory
		if item_name not in inv or inv[item_name] <= 0:
			return "You don't have that."
		# lookup worth (must be present in engine.item_worth)
		worth_map = getattr(self.engine, "item_worth", {}) or {}
		if item_name not in worth_map:
			return "That can't be sold."
		try:
			price = int(worth_map.get(item_name, 0))
		except Exception:
			price = 0
		# remove one from inventory
		self._remove_from_inventory(item_name, 1)
		# add gold to player's stats
		self.engine.player.stats["gold"] = int(self.engine.player.stats.get("gold", 0)) + price
		# notify UI
		try:
			self.engine._inventory_changed = True
		except Exception:
			pass
		result = f"You sold 1 {item_name} for {price} gold."
		# Award XP for selling
		if PROGRESSION_AVAILABLE:
			try:
				result += award_xp(self.engine.player, XP_AWARDS.get("sell_item", 2), "sold item")
			except Exception:
				pass
		# Track gold for achievements
		if ACHIEVEMENT_AVAILABLE and price > 0:
			try:
				track_event(self.engine.player, "total_gold", price)
				result += self._check_and_show_achievements()
			except Exception:
				pass
		return result

	# ========== SHOP SYSTEM METHODS ==========
	
	def _check_in_shop(self):
		"""Verify player is in a shop room and activate the correct shop."""
		current_room_id = self.engine.player.current_room
		current_room = self.engine.rooms.get(current_room_id)
		
		# Check if this room is a shop (by room property or known shop ID)
		is_shop_room = False
		if current_room and hasattr(current_room, 'shop') and current_room.shop:
			is_shop_room = True
		elif current_room_id == "village_shop":
			is_shop_room = True
		
		if not is_shop_room:
			return False, "You need to be in a shop to do that."
		
		# Activate the right shop for this room
		if not self._activate_shop_for_room(current_room_id):
			return False, "The shop system is not available."
		
		if not self.engine.shop or not self.engine.shopkeeper:
			return False, "The shop system is not available."
		# Check if inventory needs rotation
		if self.engine.shop.check_and_rotate():
			pass  # Silently rotated
		return True, ""
	
	def _activate_shop_for_room(self, room_id):
		"""Switch to the correct shop instance for the given room."""
		if not SHOP_AVAILABLE:
			return False
		try:
			from shop_system import SHOP_DATABASES
			# Check if we need to switch shops
			if self.engine.shop and self.engine.shop.shop_id == room_id:
				return True  # Already on the right shop
			
			# Get the item database for this room 
			item_db = SHOP_DATABASES.get(room_id)
			if item_db is None:
				# Fallback: use default database
				item_db = SHOP_DATABASES.get("village_shop")
			
			# Create or switch to the appropriate shop
			if room_id not in self.engine.island_shops:
				shop = Shop(shop_id=room_id, item_database=item_db)
				self.engine.island_shops[room_id] = shop
			
			self.engine.shop = self.engine.island_shops[room_id]
			self.engine.shopkeeper = Shopkeeper(self.engine.shop)
			self.engine.shop_ui = ShopUI(self.engine.shop, self.engine.shopkeeper, self.engine)
			return True
		except Exception as e:
			print(f"[ERROR] Failed to activate shop for {room_id}: {e}")
			return False
	
	def _shop_help(self):
		"""Show shop command help with beautiful UI."""
		if not self._check_in_shop()[0]:
			return self._check_in_shop()[1]
		self.engine.shop_ui.show_shop_welcome()
		return ""
	
	def _shop_browse(self):
		"""Display shop inventory with beautiful UI."""
		ok, msg = self._check_in_shop()
		if not ok:
			return msg
		
		self.engine.shop_ui.show_shop_inventory(self.engine.player)
		return ""
	
	def _shop_buy(self, item_name):
		"""Buy an item from the shop with beautiful UI."""
		ok, msg = self._check_in_shop()
		if not ok:
			return msg
		
		item_name = item_name.strip().lower()
		
		# Use beautiful UI for the buy process
		if self.engine.shop_ui.buy_item(self.engine.player, item_name):
			# Update engine player inventory
			if item_name not in self.engine.player.inventory:
				self.engine.player.inventory[item_name] = 1
			else:
				self.engine.player.inventory[item_name] += 1
			return ""
		else:
			return ""
	
	def _shop_sell(self, item_name, offered_price):
		"""Attempt to sell an item to shopkeeper with beautiful negotiation UI."""
		ok, msg = self._check_in_shop()
		if not ok:
			return msg
		
		item_name = item_name.strip().lower()
		
		# Check if player has item
		if item_name not in self.engine.player.inventory or self.engine.player.inventory[item_name] <= 0:
			self.engine.display_message(f"⚠️  You don't have any {item_name}.")
			return ""
		
		# Validate offered price
		if offered_price <= 0:
			self.engine.display_message("⚠️  Price must be positive!")
			return ""
		
		# Use beautiful UI for selling
		result = self.engine.shop_ui.sell_item(self.engine.player, item_name, offered_price)
		
		if result == 'pending':
			# Waiting for user response on counter offer
			return ""
		elif result:
			# Sale completed
			return ""
		else:
			# Sale refused
			return ""
	
	def _shop_talk(self):
		"""Talk to shopkeeper."""
		ok, msg = self._check_in_shop()
		if not ok:
			return msg
		
		greeting = self.engine.shopkeeper.greet()
		self.engine.display_message(f"💬 Shopkeeper: \"{greeting}\"")
		return ""
	
	def _shop_info(self):
		"""Show negotiation tips and shop information with beautiful UI."""
		ok, msg = self._check_in_shop()
		if not ok:
			return msg
		
		self.engine.shop_ui.show_shop_info()
		return ""

	# ── Bank of Estoria helpers ────────────────────────────────────────────────

	def _require_bank(self):
		"""Return (True, '') if the player is in the bank, else (False, error_msg)."""
		if self.engine.player.current_room != "bank_of_estoria":
			return (False, "You must be in the Bank of Estoria to use banking commands.")
		return (True, "")

	def _bank_help(self):
		ok, msg = self._require_bank()
		if not ok:
			return msg
		tier = self.engine.player.state.get("bank_tier", 0)
		cap = BANK_TIERS[tier]["capacity"]
		bal = self.engine.player.state.get("bank_gold", 0)
		result  = "\n╔══════════════════════════════════════╗\n"
		result += "║      🏦  BANK OF ESTORIA              ║\n"
		result += "╠══════════════════════════════════════╣\n"
		result += f"║  Balance:  {bal:>8,}g                ║\n"
		result += f"║  Capacity: {cap:>8,}g  (Tier {tier})       ║\n"
		result += "╠══════════════════════════════════════╣\n"
		result += "║  deposit <amount>  — store gold      ║\n"
		result += "║  withdraw <amount> — retrieve gold   ║\n"
		result += "║  balance           — check balance   ║\n"
		result += "║  upgrade bank      — expand vault    ║\n"
		result += "╚══════════════════════════════════════╝\n"
		return result

	def _bank_balance(self):
		ok, msg = self._require_bank()
		if not ok:
			return msg
		tier = self.engine.player.state.get("bank_tier", 0)
		cap  = BANK_TIERS[tier]["capacity"]
		bal  = self.engine.player.state.get("bank_gold", 0)
		carried = self.engine.player.stats.get("gold", 0)
		result  = f"\n  🏦 Bank of Estoria — Account Summary\n"
		result += f"  ─────────────────────────────────\n"
		result += f"  Deposited : {bal:,}g  /  {cap:,}g capacity  (Tier {tier})\n"
		result += f"  Carried   : {carried:,}g\n"
		result += f"  ─────────────────────────────────\n"
		if tier < len(BANK_TIERS) - 1:
			next_tier = BANK_TIERS[tier + 1]
			result += f"  Next tier ({tier+1}): {next_tier['capacity']:,}g capacity"
			result += f"  —  costs {next_tier['gold_cost']:,}g"
			if next_tier["material_cost"]:
				mats = ", ".join(f"{v}× {k.replace('_',' ')}" for k, v in next_tier["material_cost"].items())
				result += f" + {mats}"
			result += "\n  Type 'upgrade bank' when ready.\n"
		else:
			result += "  You have reached the maximum vault tier!\n"
		return result

	def _bank_deposit(self, amount):
		ok, msg = self._require_bank()
		if not ok:
			return msg
		if amount <= 0:
			return "  Amount must be positive."
		carried = self.engine.player.stats.get("gold", 0)
		if amount > carried:
			return f"  You only have {carried:,}g on you."
		tier = self.engine.player.state.get("bank_tier", 0)
		cap  = BANK_TIERS[tier]["capacity"]
		bal  = self.engine.player.state.get("bank_gold", 0)
		space = cap - bal
		if space <= 0:
			return f"  Your vault is full ({bal:,}/{cap:,}g).  Upgrade to store more."
		actual = min(amount, space)
		self.engine.player.stats["gold"] = carried - actual
		self.engine.player.state["bank_gold"] = bal + actual
		result = f"  🏦 Deposited {actual:,}g.\n"
		result += f"  Vault: {bal + actual:,}/{cap:,}g   |   Carried: {carried - actual:,}g\n"
		if actual < amount:
			result += f"  (Only {actual:,}g deposited — vault is now full.)\n"
		return result

	def _bank_withdraw(self, amount):
		ok, msg = self._require_bank()
		if not ok:
			return msg
		if amount <= 0:
			return "  Amount must be positive."
		bal = self.engine.player.state.get("bank_gold", 0)
		if amount > bal:
			return f"  You only have {bal:,}g in the vault."
		self.engine.player.state["bank_gold"] = bal - amount
		carried = self.engine.player.stats.get("gold", 0)
		self.engine.player.stats["gold"] = carried + amount
		result = f"  🏦 Withdrew {amount:,}g.\n"
		result += f"  Vault: {bal - amount:,}g   |   Carried: {carried + amount:,}g\n"
		return result

	def _bank_upgrade(self):
		ok, msg = self._require_bank()
		if not ok:
			return msg
		tier = self.engine.player.state.get("bank_tier", 0)
		if tier >= len(BANK_TIERS) - 1:
			return "  Your vault is already at the maximum tier (19)!"
		next_tier = BANK_TIERS[tier + 1]
		gold_cost = next_tier["gold_cost"]
		mat_cost  = next_tier["material_cost"]
		carried   = self.engine.player.stats.get("gold", 0)

		# Check gold
		if carried < gold_cost:
			needed = gold_cost - carried
			return f"  You need {gold_cost:,}g to upgrade.  You have {carried:,}g  (need {needed:,}g more)."

		# Check materials
		inv = self.engine.player.inventory
		for item_id, qty_needed in mat_cost.items():
			have = inv.get(item_id, 0)
			if have < qty_needed:
				name = item_id.replace("_", " ").title()
				return (f"  Missing materials: need {qty_needed}× {name} "
						f"(you have {have}).")

		# Deduct gold + materials
		self.engine.player.stats["gold"] = carried - gold_cost
		for item_id, qty_needed in mat_cost.items():
			inv[item_id] -= qty_needed
			if inv[item_id] <= 0:
				del inv[item_id]

		# Apply upgrade
		new_tier = tier + 1
		self.engine.player.state["bank_tier"] = new_tier
		new_cap = BANK_TIERS[new_tier]["capacity"]
		result  = f"  🏦 Vault upgraded to Tier {new_tier}!\n"
		result += f"  New capacity: {new_cap:,}g\n"
		if gold_cost:
			result += f"  Cost: {gold_cost:,}g"
			if mat_cost:
				mats = ", ".join(f"{v}× {k.replace('_',' ')}" for k,v in mat_cost.items())
				result += f" + {mats}"
			result += "\n"
		return result

	def _open_map(self):
		"""Open the live map window."""
		if not MAP_AVAILABLE:
			return "Map feature not available. Missing live_map_window module."
		
		try:
			# Create or focus the map window
			if not self.engine.map_window:
				app = self.engine.gui.app if self.engine.gui else None
				self.engine.map_window = LiveMapWindow(
					app,
					self.engine.rooms,
					game_engine=self.engine
				)
			
			self.engine.map_window.create_window()
			
			# Update map with current player info
			if self.engine.player and hasattr(self.engine.player, 'visited_rooms'):
				self.engine.map_window.update_location(
					self.engine.player.current_room,
					self.engine.player.visited_rooms
				)
			
			return "Map opened!"
		except Exception as e:
			return f"Failed to open map: {e}"

	def _close_map(self):
		"""Close the live map window."""
		if self.engine.map_window:
			self.engine.map_window.close_window()
			self.engine.map_window = None
			return "Map closed."
		return "Map is not open."

	def _show_commands(self):
		"""Display comprehensive command list with context awareness."""
		current_room = self.engine.get_room_data(self.engine.player.current_room)
		cr = self.engine.player.current_room
		in_dungeon = (cr.startswith("dungeon_") and "_floor" in cr) or cr in self.engine.fixed_dungeon_room_ids
		in_shop = False
		
		if isinstance(current_room, dict):
			in_shop = current_room.get("shop", False)
		elif hasattr(current_room, "shop"):
			in_shop = current_room.shop
		
		result = """
╔════════════════════════════════════════════════════════════════╗
║                     AVAILABLE COMMANDS                         ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  [MOVEMENT]                                                    ║
║ ---------------------------------------------------------------║
║    go <direction>       - Move (north, south, east, west)      ║
║    n / s / e / w        - Quick movement shortcuts             ║
║    go up / u            - Climb stairs to previous floor       ║
║    go down / d          - Descend stairs to next floor         ║
║    enter                - Enter building/dungeon               ║
║    leave / exit         - Leave current location               ║
║                                                                ║
║  [EXPLORATION]                                                 ║
║ ---------------------------------------------------------------║
║    look / l             - Look around current room             ║
║    examine <target>     - Examine something closely            ║
║    inspect <target>     - Same as examine (inspect wall!)      ║
║    search               - Search for hidden items/traps        ║
║    fight                - Engage a visible enemy in the room   ║
║    open map             - Open live map window                 ║
║    close map            - Close map window                     ║
║    rooms / areas        - Browse all game areas                ║
║    bestiary / monsters  - Browse all enemies                   ║
║                                                                ║
║  [INVENTORY]                                                   ║
║ ---------------------------------------------------------------║
║    inventory / inv / i  - View your inventory                  ║
║    take <item>          - Pick up an item                      ║
║    drop <item>          - Drop an item from inventory          ║
║    sell <item>          - Sell item for standard value         ║
║    use <item>           - Use an item (potion, torch, etc.)    ║
║                                                                ║
"""

		# Ship travel commands (show when dock has boat exits)
		_room_for_help = self.engine.get_room_data(self.engine.player.current_room)
		_help_exits = _room_for_help.exits if hasattr(_room_for_help, 'exits') else (_room_for_help.get('exits', {}) if isinstance(_room_for_help, dict) else {})
		_has_boat = any(isinstance(v, dict) and v.get('type') == 'boat_travel' for v in _help_exits.values())
		if _has_boat:
			result += """║  [SHIP TRAVEL]                                                 ║
║ ---------------------------------------------------------------║
║    board                - List all ships at this dock          ║
║    board mainland       - Return to Grand Harbor               ║
║    board <island>       - Sail to a discovered island          ║
║                                                                ║
"""

		# Fishing commands (show near water)
		if FISHING_AVAILABLE:
			from fishing_system import WATER_ROOMS as FISH_WATER_ROOMS
			if self.engine.player.current_room in FISH_WATER_ROOMS:
				result += """║  [FISHING]                                                     ║
║ ---------------------------------------------------------------║
║    fish                 - Cast your line (no bait)             ║
║    fish <bait>          - Fish with specific bait              ║
║    bait                 - View your bait inventory             ║
║                                                                ║
"""
		
		# NPC commands (show when NPCs are present)
		if NPC_AVAILABLE:
			room_obj = self.engine.get_room_data(self.engine.player.current_room)
			has_npcs = hasattr(room_obj, 'npcs') and room_obj.npcs
			if has_npcs:
				result += """║  [NPC INTERACTION]                                             ║
║ ---------------------------------------------------------------║
║    talk to <name>       - Start conversation with an NPC       ║
║    gift <npc> <item>    - Give an item as a gift to an NPC     ║
║    reputation / rep     - View NPC relationship standings      ║
║    rep <npc_name>       - View specific NPC relationship       ║
║                                                                ║
"""
		
		# Context-specific commands
		if in_dungeon:
			result += """║  [DUNGEON ACTIONS]                                            ║
║ ---------------------------------------------------------------║
║    open chest           - Open a treasure chest                ║
║    disarm / disarm trap - Attempt to disarm a trap             ║
║    go secret            - Enter secret passage (if discovered) ║
║    craft / forge        - Use crafting altar (if present)      ║
║    experiment           - Experiment with items to discover    ║
║    use altar            - Same as craft                        ║
║                                                                ║
"""
		
		if SHOP_AVAILABLE and in_shop:
			result += """║  [SHOP COMMANDS]                                              ║
║ ---------------------------------------------------------------║
║    shop browse          - View items for sale                  ║
║    shop buy <item>      - Purchase an item                     ║
║    shop sell <item> <price> - Sell item to merchant            ║
║    shop info            - Trading tips and pricing guide       ║
║    shop talk            - Chat with merchant                   ║
║                                                                ║
"""
		
		result += """║  [SYSTEM]                                                      ║
║ ---------------------------------------------------------------║
║    help / commands / ?  - Show this command list               ║
║    recipes / crafting   - View all known crafting recipes      ║
║    journal / quests / j - View quest journal                   ║
║    save                 - Save your game                       ║
║    quit / exit          - Save and exit game                   ║
║                                                                ║
"""
		
		# Progression commands
		if PROGRESSION_AVAILABLE:
			result += """║  [PROGRESSION]                                                 ║
║ ---------------------------------------------------------------║
║    stats / level        - View stats, level, and XP            ║
║    skills / skilltree   - Open graphical skill tree            ║
║    abilities / ab       - List your active abilities           ║
║    ability <name>       - Use an active ability                ║
║                                                                ║
"""
		
		# Equipment commands
		if EQUIPMENT_AVAILABLE:
			result += """║  [EQUIPMENT]                                                   ║
║ ---------------------------------------------------------------║
║    equip <item>         - Equip a weapon/armor/accessory       ║
║    unequip <slot/item>  - Remove equipment (e.g. weapon)       ║
║    equipment            - View current equipment               ║
║    enchant              - Enchant equipment at an altar        ║
║                                                                ║
"""
		
		# Combat commands (show when in combat or in dungeon)
		if COMBAT_AVAILABLE and (in_dungeon or getattr(self.engine, 'pending_combat', None)):
			result += """║  [COMBAT]                                                      ║
║ ---------------------------------------------------------------║
║    attack               - Attack the enemy                     ║
║    defend               - Reduce incoming damage this turn     ║
║    flee                  - Attempt to escape (can't flee boss) ║
║                                                                ║
"""
		
		result += """╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  [TIPS]                                                        ║
║    • Commands are not case-sensitive                           ║
║    • Use 'look' often to get your bearings                     ║
║    • 'inspect wall' in boss rooms may reveal secrets!          ║
║    • 'search' can find hidden traps before they trigger        ║
║    • Keep the map open to track your progress                  ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
"""
		
		# Show contextual hints
		hints = self._get_contextual_hints()
		if hints:
			result += "\n" + hints
		
		# Add debug commands note if available
		if DEBUG_AVAILABLE:
			result += "\n[DEBUG MODE] Type 'debug commands' to see debug menu.\n"
		
		return result

	def _show_recipes(self):
		"""Display all learned crafting recipes."""
		if not CRAFTING_AVAILABLE or not self.engine.crafting_system:
			return "The crafting system is not available."
		
		# Get known recipes
		known_recipe_ids = self.engine.crafting_system.get_known_recipes()
		
		if not known_recipe_ids:
			return "\nYou haven't learned any crafting recipes yet.\n\nTalk to NPCs like the Blacksmith, Hermit, Priest, or Swamp Witch to learn recipes!\n"
		
		# Import recipe database
		try:
			from crafting_system import RECIPE_DATABASE, STATION_NAMES
		except ImportError:
			return "Could not load recipe database."
		
		result = "\n" + "=" * 65 + "\n"
		result += "  📚 KNOWN CRAFTING RECIPES\n"
		result += "=" * 65 + "\n\n"
		
		for idx, recipe_id in enumerate(known_recipe_ids, 1):
			recipe = RECIPE_DATABASE.get(recipe_id)
			if not recipe:
				continue
			
			result += f"[{idx}] {recipe['name']}\n"
			
			# Ingredients
			result += "    Materials: "
			ingredients = []
			for item_name, count in recipe['ingredients'].items():
				nice_name = item_name.replace("_", " ").title()
				ingredients.append(f"{count}x {nice_name}")
			result += ", ".join(ingredients) + "\n"
			
			# Station
			station_type = recipe['station']
			if station_type == "any":
				result += "    Location: Any Crafting Station (Forge or Altar)\n"
			else:
				station_name = STATION_NAMES.get(station_type, station_type)
				result += f"    Location: {station_name}\n"
			
			# Description
			result += f"    {recipe['description']}\n\n"
		
		result += "=" * 65 + "\n"
		result += "Use 'craft' command at a crafting station to make items.\n"
		result += "=" * 65 + "\n"
		
		return result

	def _get_contextual_hints(self):
		"""Get hints based on current situation."""
		current_room = self.engine.get_room_data(self.engine.player.current_room)
		
		if not current_room:
			return ""
		
		hints = []
		
		if isinstance(current_room, dict):
			# Secret room hint
			if current_room.get("has_secret") and not current_room.get("secret_discovered"):
				hints.append("[HINT] This room feels unusual. Try 'inspect wall' to look for secrets!")
			
			# Trap hint
			if current_room.get("traps"):
				unsprung = [t for t in current_room["traps"] if not t.get("triggered") and not t.get("disarmed")]
				if unsprung:
					hints.append("[WARNING] Be careful! This area looks dangerous. Use 'search' to look for traps.")
			
			# Loot hint
			if current_room.get("items"):
				hints.append("[LOOT] Items are available here. Use 'take <item>' or look around.")
			
			# Chest hint
			if current_room.get("chests"):
				unopened = [c for c in current_room["chests"] if not c.get("opened")]
				if unopened:
					hints.append("[TREASURE] A chest is here! Try 'open chest' to see what's inside.")
			
			# Available exits hint
			exits = current_room.get("exits", {})
			if "secret" in exits:
				hints.append("[SECRET] Secret passage available - use 'go secret'")
			if "up" in exits:
				hints.append("[EXIT] Stairs up available - use 'go up' or 'u'")
			if "down" in exits:
				hints.append("[EXIT] Stairs down available - use 'go down' or 'd'")
		
		if hints:
			result = "\n[AVAILABLE ACTIONS IN THIS ROOM]\n"
			for hint in hints:
				result += "   " + hint + "\n"
			return result
		
		return ""
	
	def _show_debug_menu(self):
		"""Display the debug commands menu."""
		if DEBUG_AVAILABLE:
			return handle_debug_commands(self.engine, [])
		return "Debug commands not available."

	def _handle_debug_command(self, args):
		"""Handle a debug command."""
		if not DEBUG_AVAILABLE:
			return "Debug commands not available. Missing debug_commands module."
		
		try:
			return handle_debug_commands(self.engine, args)
		except Exception as e:
			return f"Debug command error: {e}"


class GameEngine:
	"""Main engine: loads world, manages game state, save/load functionality.
	All public methods return strings to be displayed by the UI.
	"""
	def __init__(self, world_file=WORLD_FILE, gui=None):
		self.world_file = world_file
		self.gui = gui  # Reference to AdventureGUI for displaying messages
		self.rooms = {}  # name -> Room
		self.player = None
		self.cmd = None
		self.should_quit = False
		self.sample_world_created = False  # set True if we auto-create a sample world.json
		# defaults loaded from world: default stats and global commands
		self.default_stats = {}
		self.global_commands = {}
		# default starting inventory from world.json (if present) - list form in world; convert to dict for runtime
		self.default_inventory = []
		# runtime flag to indicate inventory changed (UI may poll or check after commands)
		self._inventory_changed = False
		# item worth mapping (item_name -> int gold)
		self.item_worth = {}
		# map window for live display
		self.map_window = None
		# searchable items debug window
		self.items_search_window = None
		# Track pending dungeon entry confirmation
		self.pending_dungeon_entry = None
		# Track pending disarm minigame
		self.pending_disarm = None
		# Track poison status
		self.poison_status = None
		# Track pending NPC dialogue
		self.pending_dialogue = None
		# Track pending crafting menu
		self.pending_crafting = None
		# Track pending crafting experiment
		self.pending_experiment = None
		# Track pending enchanting menu
		self.pending_enchant = None
		# Track pending combat encounter
		self.pending_combat = None
		
		# Track pending class selection (progression system)
		self.pending_class_selection = False
		# Track pending quest action (accept/decline)
		self.pending_quest_action = None
		# Track pending boat travel (island unlock confirmation)
		self.pending_boat_travel = None
		# Track pending travel animation (set by _execute_boat_travel, consumed by AdventureGUI)
		self.pending_travel_animation = None
		
		# Debug overrides for dungeons
		self.debug_force_open_dungeons = set()  # Stores dungeon_ids that are force-opened
		# Debug mode: free disarm (no items required)
		self.debug_disarm_free = False
		
		# Fixed dungeon tracking
		self.current_fixed_dungeon = None  # Loaded fixed dungeon JSON data
		self.fixed_dungeon_room_ids = set()  # Room IDs belonging to current fixed dungeon
		
		# Island shop registry (lazy-created per shop room)
		self.island_shops = {}
		
		# Initialize shop system
		if SHOP_AVAILABLE:
			try:
				self.shop = Shop("village_shop")
				self.shopkeeper = Shopkeeper(self.shop)
				self.shop_ui = ShopUI(self.shop, self.shopkeeper, self)
				self.island_shops["village_shop"] = self.shop
			except Exception as e:
				print(f"[ERROR] Failed to initialize shop: {e}")
				self.shop = None
				self.shopkeeper = None
				self.shop_ui = None
		else:
			self.shop = None
			self.shopkeeper = None
			self.shop_ui = None
		
		# Initialize dungeon systems
		if DUNGEON_AVAILABLE:
			try:
				self.dungeon_scheduler = DungeonScheduler(game_engine=self)
				self.current_dungeon_instance = None  # Will be set when player enters dungeon
			except Exception as e:
				print(f"[ERROR] Failed to initialize DungeonScheduler: {e}")
				self.dungeon_scheduler = None
				self.current_dungeon_instance = None
		else:
			self.dungeon_scheduler = None
			self.current_dungeon_instance = None
		
		# Initialize NPC system
		if NPC_AVAILABLE:
			self.npc_manager = NPCManager(self)
		else:
			self.npc_manager = None
		
		# Initialize quest system
		if QUEST_AVAILABLE:
			self.quest_manager = QuestManager(self)
		else:
			self.quest_manager = None

		# Initialize NPC reputation system
		if NPC_REP_AVAILABLE:
			self.reputation_manager = ReputationManager(self)
		else:
			self.reputation_manager = None

		# Initialize overworld encounter system
		if OVERWORLD_AVAILABLE:
			self.encounter_manager = OverworldEncounterManager(self)
		else:
			self.encounter_manager = None

		# Initialize fishing system
		if FISHING_AVAILABLE:
			self.fishing_system = FishingMinigame(self)
		else:
			self.fishing_system = None
		
		# Initialize crafting system
		if CRAFTING_AVAILABLE:
			self.crafting_system = CraftingSystem(self)
		else:
			self.crafting_system = None
		
		# Initialize item effects system
		if ITEM_EFFECTS_AVAILABLE:
			self.item_effects = ItemEffects(self)
		else:
			self.item_effects = None
		
		# Initialize enchanting system
		if ENCHANTING_AVAILABLE:
			self.enchanting_system = EnchantingSystem(self)
		else:
			self.enchanting_system = None
		
		self.load_world()
		# Quit handler is managed by pygame_ui.py

	def cleanup_dungeon(self):
		"""
		Clean up dungeon state when a dungeon closes or player leaves.
		Removes registered dungeon rooms from engine.rooms,
		clears the dungeon instance, and updates the map.
		Handles both procedural (time-gated) and fixed dungeons.
		"""
		# Remove procedural dungeon rooms from engine.rooms
		to_remove = [rid for rid in self.rooms
		             if rid.startswith("dungeon_") and "_floor" in rid]
		# Also remove fixed dungeon rooms
		to_remove.extend(rid for rid in self.fixed_dungeon_room_ids if rid in self.rooms)
		
		for rid in to_remove:
			del self.rooms[rid]
		if to_remove:
			print(f"[DEBUG] Cleaned up {len(to_remove)} dungeon rooms from engine.rooms")

		# Teleport player out if still inside a dungeon room
		player_in_dungeon = False
		if self.player:
			cr = self.player.current_room
			if (cr.startswith("dungeon_") and "_floor" in cr):
				player_in_dungeon = True
			elif cr in self.fixed_dungeon_room_ids:
				player_in_dungeon = True
		
		if player_in_dungeon:
			# Use the entrance_room_id stored in the dungeon data if available
			exit_target = "dungeon_forest_entrance"  # fallback
			if self.current_dungeon_instance:
				if hasattr(self.current_dungeon_instance, 'entrance_room_id'):
					exit_target = self.current_dungeon_instance.entrance_room_id
				elif self.current_dungeon_instance.dungeon_data:
					exit_target = self.current_dungeon_instance.dungeon_data.get("entrance_room_id", exit_target)
			self.player.current_room = exit_target

		# Clear dungeon instance and fixed dungeon state
		self.current_dungeon_instance = None
		self.current_fixed_dungeon = None
		self.fixed_dungeon_room_ids.clear()

		# Refresh map to show overworld
		if self.map_window and self.map_window.is_open():
			self.map_window.update_location(
				self.player.current_room,
				getattr(self.player, "visited_rooms", set())
			)

	def _load_fixed_dungeon(self, dungeon_id):
		"""Load fixed dungeon data from fixed_dungeons/{dungeon_id}.json."""
		try:
			base_dir = os.path.dirname(os.path.abspath(self.world_file))
			dungeon_path = os.path.join(base_dir, "fixed_dungeons", f"{dungeon_id}.json")
			if not os.path.exists(dungeon_path):
				print(f"[ERROR] Fixed dungeon file not found: {dungeon_path}")
				return None
			with open(dungeon_path, "r", encoding="utf-8") as f:
				return json.load(f)
		except Exception as e:
			print(f"[ERROR] Failed to load fixed dungeon '{dungeon_id}': {e}")
			return None

	def load_world(self):
		# If world file does not exist, create a sample (so users can edit it without touching code)
		if not os.path.exists(self.world_file):
			sample = {
				"start_room": "Village",
				"rooms": {
					"Village": {
						"description": "A small peaceful village. A path leads north to a Forest.",
						"exits": {"north": "Forest"},
						"items": ["map"],
						"actions": {
							"look at well": "The old well is dry, but you see carved symbols on the rim."
						}
					},
					"Forest": {
						"description": "A dark forest filled with tall trees. A cave mouth yawns to the east.",
						"exits": {"south": "Village", "east": "Cave"},
						"items": ["stick"],
						"actions": {
							"climb tree": "You climb a low branch and get a better view of the surroundings."
						}
					},
					"Cave": {
						"description": "A damp cave. It's dim but you spot something glinting deeper inside.",
						"exits": {"west": "Forest"},
						"items": ["old coin"],
						"actions": {
							"search": "You search the cave and find an old coin half-buried in mud."
						}
					}
				}
			}
			try:
				with open(self.world_file, "w", encoding="utf-8") as f:
					json.dump(sample, f, indent=2)
				self.sample_world_created = True
			except Exception as e:
				# If writing fails, raise so GUI can show an error
				raise RuntimeError(f"Failed to create sample world file: {e}")

		# Load the world file
		try:
			with open(self.world_file, "r", encoding="utf-8") as f:
				data = json.load(f)
		except FileNotFoundError:
			# shouldn't happen because we auto-created above, but keep safety
			raise FileNotFoundError(f"World file not found: {self.world_file}")
		except Exception as e:
			# Any JSON parse error or IO error should be reported
			raise RuntimeError(f"Failed to load world file: {e}")

		# create rooms
		self.rooms = {}
		rooms_data = data.get("rooms", {})
		# load item worth mapping if present
		raw_worth = data.get("item_worth", {}) or {}
		if isinstance(raw_worth, dict):
			wmap = {}
			for k, v in raw_worth.items():
				try:
					wmap[str(k)] = int(v)
				except Exception:
					try:
						wmap[str(k)] = int(float(v))
					except Exception:
						wmap[str(k)] = 0
			self.item_worth = wmap
		else:
			self.item_worth = {}
		for rname, rdata in rooms_data.items():
			if not isinstance(rdata, dict):
				continue
			rdata.setdefault("description", "")
			rdata.setdefault("exits", {})
			# support 'items' as either list (legacy) or dict mapping item->count (new)
			raw_items = rdata.get("items", []) if ("items" in rdata) else []
			if isinstance(raw_items, dict):
				# expand mapping into a list with repeated entries
				items_expanded = []
				for it, cnt in raw_items.items():
					try:
						n = int(cnt)
					except Exception:
						try:
							n = int(float(cnt))
						except Exception:
							n = 1
					for _ in range(max(0, n)):
						items_expanded.append(str(it))
				rdata["items"] = items_expanded
			else:
				# assume list-like; coerce to list of strings
				rdata["items"] = [str(it) for it in (raw_items or [])]
			rdata.setdefault("actions", {})
			# Normalize actions: allow "action": "response string", old {"response":...}, or new structured form
			normalized_actions = {}
			for act_cmd, act_val in rdata.get("actions", {}).items():
				if isinstance(act_val, str):
					# simple string => text-only action
					normalized_actions[act_cmd] = {"text": act_val}
				elif isinstance(act_val, dict):
					# map legacy 'response' to 'text' for consistency
					act_copy = dict(act_val)
					if "response" in act_copy and "text" not in act_copy:
						act_copy["text"] = act_copy.pop("response")
					# keep 'effects' and 'conditions' if present
					normalized_actions[act_cmd] = act_copy
				else:
					continue
			rdata["actions"] = normalized_actions
			rdata.setdefault("name", rname)
			self.rooms[rname] = Room(rdata)
		# after reading `data` from JSON file:
		# load default stats and global commands
		self.default_stats = dict(data.get("default_stats", {}))
		# Normalize default_inventory: support both dict and list in world.json
		raw_def_inv = data.get("default_inventory", {}) if ("default_inventory" in data) else {}
		if isinstance(raw_def_inv, dict):
			# already dict of counts
			self.default_inventory = {str(k): int(v) for k, v in raw_def_inv.items()}
		elif isinstance(raw_def_inv, list):
			# convert list to dict counts
			agg = {}
			for it in raw_def_inv:
				if it is None:
					continue
				agg[str(it)] = agg.get(str(it), 0) + 1
			self.default_inventory = agg
		else:
			# fallback empty dict
			self.default_inventory = {}

		gcmds = data.get("global_commands", {}) or {}
		# normalize global commands: allow string or dict
		n_gcmds = {}
		for cmd, val in gcmds.items():
			if isinstance(val, str):
				n_gcmds[cmd] = {"text": val, "effects": {}}
			elif isinstance(val, dict):
				vcopy = dict(val)
				# legacy 'response' -> 'text'
				if "response" in vcopy and "text" not in vcopy:
					vcopy["text"] = vcopy.pop("response")
				# ensure effects key exists
				vcopy.setdefault("effects", {})
				n_gcmds[cmd] = vcopy
		self.global_commands = n_gcmds

		# Determine start room: prefer "start_room", fall back to legacy "start"
		self.start_room = data.get("start_room") or data.get("start") or (next(iter(self.rooms)) if self.rooms else None)
		# handler
		self.cmd = CommandHandler(self)
		# ensure item_worth exists even if not in file
		self.item_worth = getattr(self, "item_worth", {}) or {}

	CURRENT_SAVE_VERSION = 4

	def _migrate_save(self, state, from_version):
		"""Migrate old save formats to current version.
		Returns (state, notes) where notes is a list of migration descriptions."""
		notes = []
		if from_version >= self.CURRENT_SAVE_VERSION:
			return state, notes

		# ── v1 → v2 migration ──
		if from_version < 2:
			player = state.get("player", {})
			p_state = player.get("state", {})

			# Ensure health_max exists (older saves may lack it)
			if "health_max" not in p_state:
				# Calculate from constitution
				stats = player.get("stats", {})
				con = stats.get("constitution", 0)
				base_hp = 100
				p_state["health_max"] = base_hp + (con * 5)
				notes.append("added health_max")

			# Ensure enchantments dict exists
			if "enchantments" not in p_state:
				p_state["enchantments"] = {}

			# Ensure equipment dict exists
			if "equipment" not in p_state:
				p_state["equipment"] = {}

			# Ensure gold exists
			if "gold" not in p_state:
				p_state["gold"] = 0

			player["state"] = p_state
			state["player"] = player
			state["save_version"] = 2
			if notes:
				notes.insert(0, "v1\u2192v2")

		# ── v2 → v3 migration (Skill Tree Redesign) ──
		if from_version < 3:
			player = state.get("player", {})
			p_stats = player.get("stats", {})
			p_state = player.get("state", {})
			old_skills = p_state.get("unlocked_skills", [])

			# Detect old-format skill IDs (v2 trees used IDs like w_power_strike,
			# r_backstab, m_fireball without branch prefixes like w_ber_ / w_tank_).
			# New trees use w_origin / r_origin / m_origin for the center node.
			old_format_ids = [
				s for s in old_skills
				if s not in ("w_origin", "r_origin", "m_origin")
				and not any(s.startswith(p) for p in (
					"w_ber_", "w_tank_", "w_arc_", "w_cmd_", "w_wm_", "w_glad_",
					"r_asn_", "r_trk_", "r_thf_", "r_bh_", "r_phn_",
					"m_fir_", "m_ice_", "m_ear_", "m_wnd_", "m_ltn_",
					"m_arc_", "m_heal_", "m_shd_",
				))
			]

			if old_format_ids:
				# Refund all SP spent on old tree and reset skills
				refunded = 0
				for sid in old_skills:
					# Old nodes cost 1-3 SP based on tier; approximate = 1 each
					refunded += 1
				p_stats["skill_points"] = p_stats.get("skill_points", 0) + refunded

				# Reset all skill-granted stat bonuses by recalculating from
				# base class + level.  This is a best-effort reset.
				class_id = p_stats.get("class", "none")
				p_state["unlocked_skills"] = []
				p_state["cooldowns"] = {}
				p_state["active_effects"] = {}

				# Auto-unlock origin node if class is set
				origin_map = {"warrior": "w_origin", "rogue": "r_origin", "mage": "m_origin"}
				origin = origin_map.get(class_id)
				if origin:
					p_state["unlocked_skills"].append(origin)

				notes.append(f"v2\u2192v3 skill tree reset: refunded {refunded} SP")
			else:
				notes.append("v2\u2192v3")

			player["stats"] = p_stats
			player["state"] = p_state
			state["player"] = player
			state["save_version"] = 3

		# ── v3 → v4 migration (Mana System + Bank) ──
		if from_version < 4:
			player = state.get("player", {})
			p_stats = player.get("stats", {})
			p_state = player.get("state", {})

			# Ensure mana stats exist (old saves get mana = max_mana)
			if "max_mana" not in p_stats:
				class_id = p_stats.get("class", "none")
				mana_base = {"warrior": 80, "rogue": 90, "mage": 120}.get(class_id, 80)
				# Add mana for levels beyond 1
				level_gain = {"warrior": 5, "rogue": 6, "mage": 10}.get(class_id, 5)
				lvl = max(1, p_stats.get("level", 1))
				mana_base += (lvl - 1) * level_gain
				p_stats["max_mana"] = mana_base
				p_stats["mana"] = mana_base
				p_stats["mana_regen_bonus"] = 0.0
				notes.append(f"v3→v4 added mana ({mana_base}/{mana_base})")
			elif "mana" not in p_stats:
				p_stats["mana"] = p_stats["max_mana"]
				notes.append("v3→v4 set mana = max_mana")

			# Ensure bank fields exist
			if "bank_gold" not in p_state:
				p_state["bank_gold"] = 0
				notes.append("v3→v4 added bank_gold")
			if "bank_tier" not in p_state:
				p_state["bank_tier"] = 0
				notes.append("v3→v4 added bank_tier")

			player["stats"] = p_stats
			player["state"] = p_state
			state["player"] = player
			state["save_version"] = 4

		return state, notes

	def on_closing(self):
		"""
		Called when user clicks X button on window.
		Saves game and shuts down gracefully.
		"""
		print("\n╔════════════════════════════════════════╗")
		print("║  Closing game. Saving progress...      ║")
		print("╚════════════════════════════════════════╝")
		
		# Save game
		try:
			self.save_game()
			print("Game saved successfully.")
		except Exception as e:
			print(f"Could not save game: {e}")
		
		# Close map window if open
		if self.map_window:
			try:
				if self.map_window.is_open():
					self.map_window.close_window()
			except Exception:
				pass
		
		# Signal quit instead of destroying root
		self.should_quit = True
		
		print("\nGoodbye!\n")

	def get_room_data(self, room_name):
		"""
		Get a room from either the world (surface) or the current dungeon.
		Dungeon rooms are cached in self.rooms after first access for performance.
		
		Args:
			room_name: Name/ID of the room
			
		Returns:
			Room object (always returns as Room object for consistency)
		"""
		# Check world/cached rooms first (dungeon rooms get cached here too)
		if room_name in self.rooms:
			return self.rooms[room_name]
		
		# If not in cache, check if we're in a dungeon
		if DUNGEON_AVAILABLE and self.current_dungeon_instance:
			try:
				if room_name.startswith("dungeon_"):
					# Parse "dungeon_{seed}_floor{N}_room{M}" format
					parts = room_name.split("_")
					floor_num = None
					for part in parts:
						if part.startswith("floor"):
							floor_num = int(part[5:])
							break
					
					if floor_num is not None:
						room_dict = self.current_dungeon_instance.get_room(floor_num, room_name)
						if room_dict:
							converted_room = self._convert_dungeon_room_to_world(room_dict)
							room_obj = Room(converted_room)
							# Cache in self.rooms so subsequent lookups are instant
							self.rooms[room_name] = room_obj
							return room_obj
			except Exception as e:
				# Catch ALL exceptions to prevent silent failures
				print(f"[ERROR get_room_data] Failed to load dungeon room '{room_name}': {e}")
				import traceback
				traceback.print_exc()
		
		return None

	def _convert_dungeon_room_to_world(self, dungeon_room):
		"""
		Convert a dungeon room dict to world room format for the Room class.
		Dungeon rooms have different item/chest formats that need conversion.
		
		Args:
			dungeon_room: Raw dungeon room dict from dungeon_data
			
		Returns:
			dict: Room data in world room format
		"""
		# Convert items to list format and preserve item values
		items_list = []
		if dungeon_room.get("items"):
			items_data = dungeon_room.get("items", {})
			
			# Handle both list and dict formats
			if isinstance(items_data, list):
				# List format: ["item1", "item2"]
				for item_name in items_data:
					items_list.append(item_name)
					# Set default value if not already set
					if item_name not in self.item_worth:
						self.item_worth[item_name] = 10
			elif isinstance(items_data, dict):
				# Dict format: {"item_name": {"quantity": 1, "value": 10}}
				for item_name, item_data in items_data.items():
					# Add item_name to list qty times
					if isinstance(item_data, dict):
						qty = item_data.get("quantity", 1)
						value = item_data.get("value", 10)
					else:
						qty = 1
						value = 10
					
					# Store the item value in engine.item_worth so it can be sold
					if item_name not in self.item_worth:
						self.item_worth[item_name] = value
					
					for _ in range(qty):
						items_list.append(item_name)
		
		# Convert exits format if needed
		# Preserve full dict for special exit types (leave_dungeon, stairs, etc.)
		exits = {}
		raw_exits = dungeon_room.get("exits", {})
		for direction, exit_data in raw_exits.items():
			if isinstance(exit_data, dict):
				exit_type = exit_data.get("type", "direction")
				if exit_type in ("leave_dungeon", "stairs_up", "stairs_down", "fixed_dungeon"):
					# Preserve full dict for special exit types
					exits[direction] = exit_data
				else:
					exits[direction] = exit_data.get("target", exit_data)
			else:
				exits[direction] = exit_data
		
		return {
			"name": dungeon_room.get("name", "Unknown Room"),
			"description": dungeon_room.get("description", ""),
			"exits": exits,
			"items": items_list,
			"actions": {},  # Dungeon rooms don't have custom actions
			"coordinates": dungeon_room.get("coordinates", [0, 0]),
			"location_type": "dungeon"
		}

	def display_message(self, message, msg_type=None):
		"""
		Display a message in the game window via the GUI.

		Args:
			message:  Text to display
			msg_type: Optional type hint (combat/item/dialogue/status/warning/system/default)
		"""
		if self.gui and hasattr(self.gui, 'append'):
			self.gui.append(message, msg_type)
		else:
			# Fallback to print if GUI not available
			print(message)

	def new_game(self):
		if not self.start_room:
			return "No start room defined."
		self.player = Player(self.start_room)
		# initialize player stats with defaults from world
		self.player.stats = dict(self.default_stats)
		# Initialize progression state
		if PROGRESSION_AVAILABLE:
			self.player.state["unlocked_skills"] = []
			self.player.state["cooldowns"] = {}
			self.player.state["active_effects"] = {}
		# Initialize equipment slots
		if EQUIPMENT_AVAILABLE:
			self.player.state["equipment"] = {slot: None for slot in EQUIPMENT_SLOTS}
		# Initialize combat state
		self.pending_combat = None
		self.player.state["cleared_rooms"] = []
		# initialize player inventory from default_inventory (dict counts)
		inv = {}
		for it, cnt in (self.default_inventory or {}).items():
			try:
				c = int(cnt)
			except Exception:
				c = 1
			if it:
				inv[str(it)] = inv.get(str(it), 0) + max(0, c)
		self.player.inventory = inv
		self.should_quit = False
		# reset inventory-changed flag
		self._inventory_changed = True
		# Initialize map window if available
		if MAP_AVAILABLE and not self.map_window:
			pass  # Map will be created when 'open map' command is used
		out = []
		out.append("Starting new game...")
		# Trigger class selection if progression system is available
		if PROGRESSION_AVAILABLE:
			self.pending_class_selection = True
			out.append("")
			out.append(get_class_selection_text())
		else:
			out.append(self.rooms[self.player.current_room].describe())
		return "\n".join(out)

	def save_game(self, path=SAVE_FILE):
		"""Persist runtime game state to path.
		Stores player's full state and the current per-room items so collected items stay removed.
		"""
		if not self.player:
			return "No game in progress to save."

		# Build a save structure containing only runtime-modified state (player + room items)
		state = {
			"save_version": 4,  # Save format version for migration
			"player": self.player.to_dict(),  # inventory serialized as dict by Player.to_dict()
			"rooms": {}
		}
		for name, room in self.rooms.items():
			# persist only the dynamic item list for each room
			# save as aggregated mapping item -> count so editor/game show counts consistently
			item_counts = {}
			for it in (room.items or []):
				if it is None:
					continue
				item_counts[str(it)] = item_counts.get(str(it), 0) + 1
			state["rooms"][name] = {"items": item_counts}
		# persist item worth mapping so save contains current worth table (helps editors/changes)
		state["item_worth"] = {str(k): int(v) for k, v in (self.item_worth or {}).items()}

		# persist quest progress
		if QUEST_AVAILABLE and self.quest_manager:
			state["quests"] = self.quest_manager.to_dict()

		# persist NPC reputation data
		if NPC_REP_AVAILABLE and self.reputation_manager:
			state["npc_reputation"] = self.reputation_manager.to_dict()

		# persist overworld encounter state
		if OVERWORLD_AVAILABLE and self.encounter_manager:
			state["overworld_encounters"] = self.encounter_manager.to_dict()

		# persist fishing stats
		if FISHING_AVAILABLE and self.fishing_system:
			state["fishing"] = self.fishing_system.to_dict()

		# persist enchantment data
		enchants = self.player.state.get("enchantments", {})
		if enchants:
			state["enchantments"] = enchants

		# persist dungeon state (CRITICAL: allows player to reload inside dungeons)
		if self.player and self.player.current_room:
			cr = self.player.current_room
			# Check if player is in a dungeon
			in_procedural = cr.startswith("dungeon_") and "_floor" in cr
			in_fixed = cr in self.fixed_dungeon_room_ids
			
			if in_procedural and self.current_dungeon_instance:
				# Save procedural dungeon state
				state["dungeon"] = {
					"type": "procedural",
					"dungeon_id": self.current_dungeon_instance.dungeon_id,
					"seed": self.current_dungeon_instance.seed,
					"entrance_room_id": self.current_dungeon_instance.entrance_room_id,
					"dungeon_data": self.current_dungeon_instance.dungeon_data,
				}
			elif in_fixed and self.current_fixed_dungeon:
				# Save fixed dungeon state
				state["dungeon"] = {
					"type": "fixed",
					"dungeon_id": self.current_fixed_dungeon.get("dungeon_id"),
					"entrance_room_id": self.current_fixed_dungeon.get("entrance_room_id"),
				}

		# persist NPC dialogue progress
		if NPC_AVAILABLE and self.npc_manager and hasattr(self.npc_manager, 'to_dict'):
			state["npc_dialogue"] = self.npc_manager.to_dict()

		# persist shop inventory state
		if SHOP_AVAILABLE and self.shop and hasattr(self.shop, 'to_dict'):
			state["shop"] = self.shop.to_dict()

		# persist dungeon scheduler state
		if DUNGEON_AVAILABLE and self.dungeon_scheduler and hasattr(self.dungeon_scheduler, 'to_dict'):
			state["dungeon_scheduler"] = self.dungeon_scheduler.to_dict()

		# Write atomically
		tmp_path = f"{path}.tmp"
		try:
			with open(tmp_path, "w", encoding="utf-8") as f:
				json.dump(state, f, indent=2, ensure_ascii=False)
			# Use os.replace for atomic swap across platforms
			os.replace(tmp_path, path)
			# reset inventory-changed flag after successful save
			self._inventory_changed = False
			return f"Game saved to {path}."
		except Exception as e:
			# attempt to clean up tmp file if present
			try:
				if os.path.exists(tmp_path):
					os.remove(tmp_path)
			except Exception:
				pass
			return f"Failed to save: {e}"

	def load_game(self, path=SAVE_FILE, interactive=True):
		"""Load runtime state previously saved with save_game.
		Only applies player state and per-room item lists; other room definitions from the world file remain intact.
		"""
		if not os.path.exists(path):
			return "No savegame found."

		try:
			with open(path, "r", encoding="utf-8") as f:
				state = json.load(f)
		except Exception as e:
			return f"Failed to load save: {e}"

		# ── Save format migration ──
		save_ver = state.get("save_version", 1)
		state, migration_notes = self._migrate_save(state, save_ver)

		# Validate and restore player (supports both dict and legacy list formats)
		player_data = state.get("player")
		if not isinstance(player_data, dict):
			return "Save file is corrupted (missing player data)."

		try:
			self.player = Player.from_dict(player_data)
		except Exception as e:
			return f"Failed to restore player from save: {e}"
		# if saved, restore item_worth mapping (optional)
		if isinstance(state.get("item_worth"), dict):
			wmap = {}
			for k, v in state.get("item_worth", {}).items():
				try:
					wmap[str(k)] = int(v)
				except Exception:
					try:
						wmap[str(k)] = int(float(v))
					except Exception:
						wmap[str(k)] = 0
			self.item_worth = wmap
		# ensure item_worth exists
		self.item_worth = getattr(self, "item_worth", {}) or {}

		# ── RESTORE DUNGEON STATE (must happen BEFORE room items restore) ──
		dungeon_state = state.get("dungeon")
		if dungeon_state and isinstance(dungeon_state, dict):
			dtype = dungeon_state.get("type")
			if dtype == "procedural":
				# Recreate procedural dungeon instance
				try:
					seed = dungeon_state.get("seed")
					dungeon_id = dungeon_state.get("dungeon_id")
					entrance_room_id = dungeon_state.get("entrance_room_id", "dungeon_forest_entrance")
					dungeon_data = dungeon_state.get("dungeon_data")
					
					if DUNGEON_AVAILABLE and seed and dungeon_data:
						# Create a wrapper object that mimics DungeonInstance
						class SavedDungeonInstance:
							def __init__(self, seed, dungeon_id, entrance_room_id, dungeon_data, scheduler):
								self.seed = seed
								self.dungeon_id = dungeon_id
								self.entrance_room_id = entrance_room_id
								self.dungeon_data = dungeon_data
								self.scheduler = scheduler
								self.active = True
						
						self.current_dungeon_instance = SavedDungeonInstance(
							seed, dungeon_id, entrance_room_id, dungeon_data, self.dungeon_scheduler
						)
						
						# Register all dungeon rooms
						for room_id, room_data in dungeon_data.get("rooms", {}).items():
							self.rooms[room_id] = Room(room_data)
				except Exception as e:
					print(f"[WARN] Failed to restore procedural dungeon: {e}")
					
			elif dtype == "fixed":
				# Recreate fixed dungeon
				try:
					dungeon_id = dungeon_state.get("dungeon_id")
					if dungeon_id:
						dungeon_data = self._load_fixed_dungeon(dungeon_id)
						if dungeon_data:
							self.current_fixed_dungeon = dungeon_data
							self.fixed_dungeon_room_ids.clear()
							
							# Register all fixed dungeon rooms
							for floor_data in dungeon_data.get("floors", {}).values():
								for room_id, room_data in floor_data.get("rooms", {}).items():
									self.rooms[room_id] = Room(room_data)
									self.fixed_dungeon_room_ids.add(room_id)
				except Exception as e:
					print(f"[WARN] Failed to restore fixed dungeon: {e}")

		# Apply saved per-room item lists without touching other room metadata.
		rooms_state = state.get("rooms", {})
		if isinstance(rooms_state, dict):
			for name, info in rooms_state.items():
				if name in self.rooms and isinstance(info, dict):
					raw_items = info.get("items")
					expanded = None
					# support mapping (item->count) or legacy list
					if isinstance(raw_items, dict):
						exp = []
						for it, cnt in raw_items.items():
							try:
								n = int(cnt)
							except Exception:
								try:
									n = int(float(cnt))
								except Exception:
									n = 1
							for _ in range(max(0, n)):
								exp.append(str(it))
						expanded = exp
					elif isinstance(raw_items, list):
						expanded = [str(it) for it in raw_items]
					# Apply expanded list if available
					if isinstance(expanded, list):
						# FIX: Always apply saved state (even if empty)
						# This ensures collected items stay collected
						self.rooms[name].items = expanded
		# Ensure flags
		self.should_quit = False
		# signal that inventory changed so UI may refresh
		self._inventory_changed = True

		# Migrate old saves: add missing progression fields
		if PROGRESSION_AVAILABLE and self.player:
			defaults = {"level": 1, "xp": 0, "xp_to_next": 100, "skill_points": 0,
						"class": "none", "strength": 0, "defense": 0, "dexterity": 0,
						"perception": 0, "charisma": 0, "constitution": 0}
			for k, v in defaults.items():
				if k not in self.player.stats:
					self.player.stats[k] = v
			# Initialize skill/ability tracking if missing
			if not hasattr(self.player, 'state'):
				self.player.state = {}
			if "unlocked_skills" not in self.player.state:
				self.player.state["unlocked_skills"] = []
			if "cooldowns" not in self.player.state:
				self.player.state["cooldowns"] = {}
			if "active_effects" not in self.player.state:
				self.player.state["active_effects"] = {}
			# If class not chosen yet, prompt selection
			if self.player.stats.get("class", "none") == "none":
				self.pending_class_selection = True
			# Recalculate synergy bonuses on load
			try:
				apply_synergy_bonuses(self.player)
			except Exception:
				pass

		# Migrate old saves: add equipment slots if missing
		if EQUIPMENT_AVAILABLE and self.player:
			if "equipment" not in self.player.state:
				self.player.state["equipment"] = {slot: None for slot in EQUIPMENT_SLOTS}
			else:
				# Migrate existing equipment dict to add new slots (helm, boots, gloves)
				for slot in EQUIPMENT_SLOTS:
					if slot not in self.player.state["equipment"]:
						self.player.state["equipment"][slot] = None
		# Migrate old saves: add cleared rooms tracking if missing
		if self.player and "cleared_rooms" not in self.player.state:
			self.player.state["cleared_rooms"] = []

		# Initialize achievement tracking if missing
		if ACHIEVEMENT_AVAILABLE and self.player:
			if "achievements" not in self.player.state:
				self.player.state["achievements"] = []
			if "achievement_tracking" not in self.player.state:
				self.player.state["achievement_tracking"] = {}

		# Reset combat state on load
		self.pending_combat = None

		# Restore quest progress from save
		if QUEST_AVAILABLE and self.quest_manager:
			quest_data = state.get("quests", {})
			self.quest_manager.load_from_dict(quest_data)

		# Restore NPC reputation data from save
		if NPC_REP_AVAILABLE and self.reputation_manager:
			rep_data = state.get("npc_reputation", {})
			self.reputation_manager.load_from_dict(rep_data)

		# Restore overworld encounter state from save
		if OVERWORLD_AVAILABLE and self.encounter_manager:
			enc_data = state.get("overworld_encounters", {})
			self.encounter_manager.load_from_dict(enc_data)

		# Restore fishing stats from save
		if FISHING_AVAILABLE and self.fishing_system:
			fish_data = state.get("fishing", {})
			self.fishing_system.load_from_dict(fish_data)

		# Restore enchantment data
		enchant_data = state.get("enchantments", {})
		if enchant_data:
			self.player.state["enchantments"] = enchant_data
			# Reapply enchantment stat bonuses for equipped items
			equipment = self.player.state.get("equipment", {})
			for slot, ench in enchant_data.items():
				if equipment.get(slot) and ench.get("stats"):
					for stat, val in ench["stats"].items():
						self.player.stats[stat] = self.player.stats.get(stat, 0) + val

		# Restore NPC dialogue progress
		if NPC_AVAILABLE and self.npc_manager and hasattr(self.npc_manager, 'load_from_dict'):
			npc_data = state.get("npc_dialogue", {})
			if npc_data:
				self.npc_manager.load_from_dict(npc_data)

		# Restore shop inventory
		if SHOP_AVAILABLE and self.shop and hasattr(self.shop, 'load_from_dict'):
			shop_data = state.get("shop", {})
			if shop_data:
				self.shop.load_from_dict(shop_data)

		# Restore dungeon scheduler state
		if DUNGEON_AVAILABLE and self.dungeon_scheduler and hasattr(self.dungeon_scheduler, 'load_from_dict'):
			scheduler_data = state.get("dungeon_scheduler", {})
			if scheduler_data:
				self.dungeon_scheduler.load_from_dict(scheduler_data)

		out = [f"Loaded game from {path}."]
		if migration_notes:
			out.append("📋 Save migrated: " + "; ".join(migration_notes))
		# If player's current room exists in world, show its description; otherwise choose a fallback
		cur = getattr(self.player, "current_room", None)
		if cur and cur in self.rooms:
			out.append(self.rooms[cur].describe())
		else:
			# fallback to engine start room
			if self.start_room and self.start_room in self.rooms:
				self.player.current_room = self.start_room
				out.append(self.rooms[self.start_room].describe())
			else:
				out.append("Loaded game, but current room not found in world.")
		# Show class selection if needed for migrated save
		if self.pending_class_selection and PROGRESSION_AVAILABLE:
			out.append("")
			out.append(get_class_selection_text())
		return "\n".join(out)

	def process_command(self, cmd: str):
		"""Process a command string and return the text output for display.
		The GUI should prepend the echoed input (e.g. '> cmd') itself if desired.
		"""
		if not self.player:
			return "No game in progress. Start a new game or load one."
		response = self.cmd.handle(cmd)
		return response or ""



# ===========================================================================
#  AdventureGUI has been moved to pygame_ui.py -> PygameAdventureGUI
#  The main() entry point is now in pygame_ui.py
# ===========================================================================

def main():
    """Launch the game via Pygame UI."""
    from pygame_ui import main as _pg_main
    _pg_main()


if __name__ == "__main__":
    main()
