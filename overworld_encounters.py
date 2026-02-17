"""
Overworld Encounter System
==========================
Random and visible enemy encounters in the overworld (non-dungeon).
Enemies scale to player level and are region-appropriate.

Two encounter types:
  1. Random encounters — chance-based on room entry (wilderness only)
  2. Visible encounters — persistent enemies that show in room description
"""

import random

# =====================================================================
# OVERWORLD ENEMY DATABASE
# =====================================================================
# Enemies organized by region/biome. Stats are base values, scaled by
# player level when spawned.

OVERWORLD_ENEMIES = {
	# ── Forest Region ──
	"wild_wolf": {
		"name": "Wild Wolf",
		"description": "A snarling grey wolf with hungry yellow eyes.",
		"hp": 22, "attack": 6, "defense": 2,
		"xp_reward": 12, "gold_reward": (2, 6),
		"loot": [("wolf_pelt", 0.40), ("raw_meat", 0.30), ("wolf_fang", 0.15)],
		"abilities": ["bite", "howl"],
		"regions": ["forest"],
	},
	"forest_spider": {
		"name": "Forest Spider",
		"description": "A large spider with bristly legs and dripping fangs.",
		"hp": 16, "attack": 7, "defense": 1,
		"xp_reward": 10, "gold_reward": (1, 4),
		"loot": [("spider_silk", 0.35), ("venom_sac", 0.15)],
		"abilities": ["bite", "web"],
		"regions": ["forest"],
	},
	"wild_boar": {
		"name": "Wild Boar",
		"description": "A stocky boar with sharp tusks and a foul temper.",
		"hp": 28, "attack": 5, "defense": 3,
		"xp_reward": 14, "gold_reward": (3, 7),
		"loot": [("raw_meat", 0.50), ("boar_tusk", 0.20), ("leather_scrap", 0.25)],
		"abilities": ["charge", "gore"],
		"regions": ["forest", "farmland"],
	},
	"forest_bandit": {
		"name": "Forest Bandit",
		"description": "A ragged outlaw hiding among the trees, blade drawn.",
		"hp": 25, "attack": 8, "defense": 2,
		"xp_reward": 18, "gold_reward": (8, 20),
		"loot": [("health_potion", 0.20), ("iron_dagger", 0.10), ("lockpick", 0.15)],
		"abilities": ["slash", "dodge"],
		"regions": ["forest", "road"],
	},

	# ── Mountain Region ──
	"mountain_goat": {
		"name": "Aggressive Mountain Goat",
		"description": "A wild mountain goat that charges at intruders.",
		"hp": 20, "attack": 5, "defense": 4,
		"xp_reward": 10, "gold_reward": (1, 5),
		"loot": [("raw_meat", 0.40), ("leather_scrap", 0.30)],
		"abilities": ["charge", "headbutt"],
		"regions": ["mountain"],
	},
	"rock_elemental": {
		"name": "Rock Elemental",
		"description": "A hulking mass of stone and gravel, eyes glowing with dull orange light.",
		"hp": 40, "attack": 7, "defense": 6,
		"xp_reward": 25, "gold_reward": (5, 15),
		"loot": [("stone_chunk", 0.50), ("raw_diamond", 0.05), ("cave_crystal", 0.15)],
		"abilities": ["slam", "stone_shield"],
		"regions": ["mountain"],
	},
	"highland_brigand": {
		"name": "Highland Brigand",
		"description": "A hardened mountain bandit wrapped in furs and leather.",
		"hp": 30, "attack": 9, "defense": 3,
		"xp_reward": 22, "gold_reward": (10, 25),
		"loot": [("health_potion", 0.25), ("iron_sword", 0.08), ("gold_ring", 0.10)],
		"abilities": ["slash", "intimidate"],
		"regions": ["mountain", "road"],
	},

	# ── Swamp Region ──
	"swamp_snake": {
		"name": "Swamp Viper",
		"description": "A venomous snake slithering through the murky water.",
		"hp": 14, "attack": 8, "defense": 1,
		"xp_reward": 11, "gold_reward": (1, 4),
		"loot": [("venom_sac", 0.35), ("snake_scale", 0.20)],
		"abilities": ["bite", "poison_strike"],
		"regions": ["swamp"],
	},
	"bog_shambler": {
		"name": "Bog Shambler",
		"description": "A rotting, moss-covered figure that lurches from the murk.",
		"hp": 35, "attack": 6, "defense": 4,
		"xp_reward": 20, "gold_reward": (3, 8),
		"loot": [("swamp_moss", 0.40), ("bone_fragment", 0.25), ("health_potion", 0.10)],
		"abilities": ["slam", "poison_touch"],
		"regions": ["swamp"],
	},
	"marsh_hag": {
		"name": "Marsh Hag",
		"description": "A hunched crone surrounded by sickly green mist and muttering curses.",
		"hp": 24, "attack": 10, "defense": 2,
		"xp_reward": 28, "gold_reward": (6, 18),
		"loot": [("health_potion", 0.30), ("shadow_essence", 0.15), ("enchanted_charm", 0.08)],
		"abilities": ["curse", "drain_life"],
		"regions": ["swamp"],
	},

	# ── Graveyard/Undead Region ──
	"skeleton_warrior": {
		"name": "Skeleton Warrior",
		"description": "A rattling skeleton with rusted armor and a chipped sword.",
		"hp": 20, "attack": 7, "defense": 3,
		"xp_reward": 15, "gold_reward": (4, 10),
		"loot": [("bone_fragment", 0.40), ("iron_sword", 0.05), ("old_shield", 0.10)],
		"abilities": ["slash", "bone_throw"],
		"regions": ["graveyard"],
	},
	"restless_spirit": {
		"name": "Restless Spirit",
		"description": "A translucent figure wailing in sorrow, cold mist trailing behind.",
		"hp": 18, "attack": 9, "defense": 1,
		"xp_reward": 16, "gold_reward": (2, 8),
		"loot": [("ectoplasm", 0.35), ("shadow_essence", 0.20)],
		"abilities": ["chill_touch", "wail"],
		"regions": ["graveyard"],
	},

	# ── Farmland/Road (easier) ──
	"rabid_dog": {
		"name": "Rabid Dog",
		"description": "A feral dog foaming at the mouth, growling viciously.",
		"hp": 15, "attack": 5, "defense": 1,
		"xp_reward": 8, "gold_reward": (1, 3),
		"loot": [("raw_meat", 0.30), ("leather_scrap", 0.20)],
		"abilities": ["bite"],
		"regions": ["farmland", "road"],
	},
	"highway_thief": {
		"name": "Highway Thief",
		"description": "A cloaked figure blocking the road with a dagger drawn.",
		"hp": 22, "attack": 7, "defense": 2,
		"xp_reward": 14, "gold_reward": (12, 30),
		"loot": [("lockpick", 0.25), ("health_potion", 0.15), ("gold_ring", 0.08)],
		"abilities": ["slash", "dodge"],
		"regions": ["road"],
	},
}

# =====================================================================
# ROOM → REGION MAPPING
# =====================================================================
# Maps room IDs to encounter regions. Rooms not listed use their
# location_type to infer region.

ROOM_REGION_MAP = {
	# Forest
	"clearing": "forest",
	"forest_path": "forest",
	"mossy_hollow": "forest",
	"deep_forest": "forest",
	"woodland_shrine": "forest",
	"ancient_grove": "forest",
	"forest_grove": "forest",
	"dungeon_forest_entrance": "forest",

	# Mountain
	"highland_trail": "mountain",
	"mountain_foothills": "mountain",
	"mountain_path": "mountain",
	"mountain_peak": "mountain",
	"dungeon_mountain_entrance": "mountain",

	# Swamp
	"swamp_trail": "swamp",
	"foggy_marsh": "swamp",
	"swamp_edge": "swamp",

	# Graveyard
	"graveyard_gates": "graveyard",
	"graveyard": "graveyard",
	"open_crypt": "graveyard",

	# Road/transition
	"village_road": "road",
	"village_outskirts": "road",
	"crossroads": "road",
	"watchtower_hill": "road",

	# Farmland
	"farmland": "farmland",
}

# Settlement/building rooms that NEVER have encounters
SAFE_ROOMS = {
	"village_square", "village_tavern", "village_shop", "village_blacksmith",
	"village_east_end", "chapel", "hermit_cabin",
}

# =====================================================================
# ENCOUNTER CONFIGURATION
# =====================================================================

# Base chance of random encounter in wilderness rooms (0.0 - 1.0)
OVERWORLD_SPAWN_CHANCE = 0.20

# Rooms recently visited have lower encounter chance (cooldown tracking)
ENCOUNTER_COOLDOWN = 3  # Must visit N other rooms before re-roll

# Chance multiplier by region danger level
REGION_DANGER = {
	"forest": 1.0,
	"mountain": 1.2,
	"swamp": 1.3,
	"graveyard": 1.5,
	"road": 0.6,
	"farmland": 0.4,
}

# Level scaling: stat multiplier per player level above 1
OVERWORLD_LEVEL_SCALE = 0.08  # +8% stats per player level

# =====================================================================
# VISIBLE ENCOUNTER SYSTEM
# =====================================================================
# Some rooms have persistent visible enemies that appear in descriptions
# and must be engaged before looting/progressing freely.

# Probability that a wilderness room has a visible enemy on first visit
VISIBLE_ENEMY_CHANCE = 0.15


class OverworldEncounterManager:
	"""Manages random and visible overworld encounters."""

	def __init__(self, engine):
		self.engine = engine
		# Tracks recent rooms for cooldown
		self.recent_rooms = []
		# Persistent visible enemies: {room_id: enemy_data_dict}
		self.visible_enemies = {}
		# Rooms that have already been rolled for visible enemies
		self.rooms_rolled = set()

	# ─── Region Detection ───

	def get_region(self, room_id):
		"""Determine the encounter region for a room."""
		if room_id in ROOM_REGION_MAP:
			return ROOM_REGION_MAP[room_id]
		# Infer from room name
		rid = room_id.lower()
		if "forest" in rid or "grove" in rid or "wood" in rid:
			return "forest"
		if "mountain" in rid or "highland" in rid or "peak" in rid or "foothill" in rid:
			return "mountain"
		if "swamp" in rid or "marsh" in rid or "bog" in rid:
			return "swamp"
		if "grave" in rid or "crypt" in rid or "tomb" in rid:
			return "graveyard"
		if "farm" in rid or "field" in rid:
			return "farmland"
		if "road" in rid or "trail" in rid or "path" in rid or "crossroad" in rid:
			return "road"
		return "forest"  # default

	def is_safe_room(self, room_id):
		"""Check if a room is a safe zone (no encounters)."""
		if room_id in SAFE_ROOMS:
			return True
		# Check location_type
		room = self.engine.rooms.get(room_id)
		if room:
			lt = getattr(room, "location_type", "wilderness")
			if lt in ("settlement", "building"):
				return True
		# Dungeon rooms handled separately
		if room_id.startswith("dungeon_") and "_floor" in room_id:
			return True
		if hasattr(self.engine, 'fixed_dungeon_room_ids') and room_id in self.engine.fixed_dungeon_room_ids:
			return True
		return False

	# ─── Enemy Selection ───

	def get_enemies_for_region(self, region):
		"""Get list of enemy IDs suitable for a region."""
		result = []
		for eid, edata in OVERWORLD_ENEMIES.items():
			if region in edata.get("regions", []):
				result.append(eid)
		return result

	def scale_enemy(self, enemy_id, player_level=1):
		"""Create a scaled enemy data dict for combat."""
		template = OVERWORLD_ENEMIES.get(enemy_id)
		if not template:
			return None

		data = dict(template)
		data["id"] = enemy_id

		# Scale stats based on player level
		scale = 1 + (player_level - 1) * OVERWORLD_LEVEL_SCALE
		data["hp"] = max(10, int(data["hp"] * scale))
		data["attack"] = max(3, int(data["attack"] * scale))
		data["defense"] = max(1, int(data["defense"] * scale))
		data["xp_reward"] = max(5, int(data["xp_reward"] * scale))

		# Scale gold reward
		gmin, gmax = data["gold_reward"]
		data["gold_reward"] = (max(1, int(gmin * scale)), max(2, int(gmax * scale)))

		return data

	# ─── Random Encounter Check ───

	def check_random_encounter(self, room_id):
		"""Check if a random encounter should trigger on entering a room.
		Returns (should_fight: bool, enemy_data: dict or None).
		"""
		if self.is_safe_room(room_id):
			return False, None

		# Cooldown check — skip if recently visited
		if room_id in self.recent_rooms:
			return False, None

		# Track room in recent list
		self.recent_rooms.append(room_id)
		if len(self.recent_rooms) > ENCOUNTER_COOLDOWN:
			self.recent_rooms.pop(0)

		# Don't trigger if there's a visible enemy here (fight that instead)
		if room_id in self.visible_enemies:
			return False, None

		# Get region and check eligible enemies
		region = self.get_region(room_id)
		eligible = self.get_enemies_for_region(region)
		if not eligible:
			return False, None

		# Roll for encounter
		danger = REGION_DANGER.get(region, 1.0)
		chance = OVERWORLD_SPAWN_CHANCE * danger
		if random.random() >= chance:
			return False, None

		# Spawn an enemy
		enemy_id = random.choice(eligible)
		player_level = 1
		if hasattr(self.engine, 'player') and self.engine.player:
			player_level = self.engine.player.stats.get("level", 1)

		enemy_data = self.scale_enemy(enemy_id, player_level)
		return True, enemy_data

	# ─── Visible Encounter System ───

	def roll_visible_enemy(self, room_id):
		"""Roll once for a visible enemy in a room (only on first visit).
		Returns enemy description text to add to room, or empty string.
		"""
		if self.is_safe_room(room_id):
			return ""
		if room_id in self.rooms_rolled:
			return ""

		self.rooms_rolled.add(room_id)

		# Roll chance
		if random.random() >= VISIBLE_ENEMY_CHANCE:
			return ""

		region = self.get_region(room_id)
		eligible = self.get_enemies_for_region(region)
		if not eligible:
			return ""

		enemy_id = random.choice(eligible)
		player_level = 1
		if hasattr(self.engine, 'player') and self.engine.player:
			player_level = self.engine.player.stats.get("level", 1)

		enemy_data = self.scale_enemy(enemy_id, player_level)
		if not enemy_data:
			return ""

		# Store visible enemy
		self.visible_enemies[room_id] = {
			"enemy_id": enemy_id,
			"enemy_data": enemy_data,
		}

		return f"\n  ⚠️ A {enemy_data['name']} lurks here! (Type 'fight' to engage)"

	def get_visible_enemy_text(self, room_id):
		"""Get text about any visible enemy in a room."""
		if room_id not in self.visible_enemies:
			return ""
		enemy = self.visible_enemies[room_id]
		return f"\n  ⚠️ A {enemy['enemy_data']['name']} lurks here! (Type 'fight' to engage)"

	def engage_visible_enemy(self, room_id):
		"""Start combat with a visible enemy. Returns enemy_data or None."""
		if room_id not in self.visible_enemies:
			return None
		enemy_info = self.visible_enemies.pop(room_id)
		return enemy_info["enemy_data"]

	# ─── Persistence ───

	def to_dict(self):
		"""Serialize for saving."""
		return {
			"recent_rooms": list(self.recent_rooms),
			"visible_enemies": {
				room_id: {
					"enemy_id": info["enemy_id"],
					"enemy_data": {
						k: v for k, v in info["enemy_data"].items()
						if k != "regions"  # don't save region tags
					},
				}
				for room_id, info in self.visible_enemies.items()
			},
			"rooms_rolled": list(self.rooms_rolled),
		}

	def load_from_dict(self, data):
		"""Restore from saved data."""
		if not isinstance(data, dict):
			return
		self.recent_rooms = list(data.get("recent_rooms", []))
		self.rooms_rolled = set(data.get("rooms_rolled", []))
		self.visible_enemies = {}
		for room_id, info in data.get("visible_enemies", {}).items():
			self.visible_enemies[room_id] = {
				"enemy_id": info.get("enemy_id", "unknown"),
				"enemy_data": info.get("enemy_data", {}),
			}
