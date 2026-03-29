"""
Fishing Minigame System
=======================
Full fishing system with:
  - Pygame timing-bar minigame overlay
  - Bait types affecting catch quality
  - Location-specific fish pools
  - Fish rarity tiers
  - Cooking recipes (campfire station)

Usage:
  fish            — Cast line (uses equipped bait if any)
  fish <bait>     — Cast using specific bait
  bait            — Show current bait / available baits
"""

import random
import time

# =====================================================================
# BAIT DATABASE
# =====================================================================

BAIT_TYPES = {
	"worm": {
		"name": "Worm",
		"description": "A common earthworm. Good for small fish.",
		"rarity_bonus": 0,        # no bonus
		"sweet_spot_bonus": 0.05, # widens timing window by 5%
		"value": 1,
	},
	"cricket": {
		"name": "Cricket",
		"description": "A chirping cricket. Attracts medium-sized fish.",
		"rarity_bonus": 0.10,      # +10% rare chance
		"sweet_spot_bonus": 0.08,
		"value": 3,
	},
	"glowworm": {
		"name": "Glowworm",
		"description": "A luminescent worm that draws deep-water fish.",
		"rarity_bonus": 0.20,
		"sweet_spot_bonus": 0.10,
		"value": 8,
	},
	"golden_lure": {
		"name": "Golden Lure",
		"description": "A shimmering golden lure. Irresistible to rare fish.",
		"rarity_bonus": 0.35,
		"sweet_spot_bonus": 0.15,
		"value": 25,
	},
	"swamp_grub": {
		"name": "Swamp Grub",
		"description": "A fat grub found in swamp mud. Perfect for swamp fishing.",
		"rarity_bonus": 0.15,
		"sweet_spot_bonus": 0.08,
		"value": 5,
	},
}

# =====================================================================
# FISH DATABASE
# =====================================================================
# Rarity tiers: common, uncommon, rare, legendary
# Each fish has a base weight for the catch pool and a rarity tier

FISH_DATABASE = {
	# ── Common (frequent catches) ──
	"small_fish": {
		"name": "Small Fish",
		"description": "A tiny minnow. Not much of a catch.",
		"rarity": "common", "weight": 35, "value": 5,
		"cook_result": "cooked_fish",
		"locations": ["any"],
	},
	"river_trout": {
		"name": "River Trout",
		"description": "A speckled trout from the clear river waters.",
		"rarity": "common", "weight": 25, "value": 8,
		"cook_result": "grilled_trout",
		"locations": ["river"],
	},
	"mudfish": {
		"name": "Mudfish",
		"description": "A slimy fish from murky waters.",
		"rarity": "common", "weight": 20, "value": 4,
		"cook_result": "cooked_fish",
		"locations": ["swamp"],
	},
	"seaweed_clump": {
		"name": "Seaweed",
		"description": "A tangled clump of waterweeds.",
		"rarity": "common", "weight": 15, "value": 2,
		"cook_result": None,
		"locations": ["any"],
	},

	# ── Uncommon ──
	"large_fish": {
		"name": "Large Bass",
		"description": "A hefty largemouth bass. Good eating!",
		"rarity": "uncommon", "weight": 18, "value": 12,
		"cook_result": "hearty_fish_stew",
		"locations": ["lake", "river"],
	},
	"cave_eel": {
		"name": "Cave Eel",
		"description": "A pale, eyeless eel from underground waters.",
		"rarity": "uncommon", "weight": 12, "value": 15,
		"cook_result": "eel_skewer",
		"locations": ["cave"],
	},
	"striped_perch": {
		"name": "Striped Perch",
		"description": "A beautiful fish with blue and silver stripes.",
		"rarity": "uncommon", "weight": 14, "value": 10,
		"cook_result": "grilled_perch",
		"locations": ["lake"],
	},
	"swamp_catfish": {
		"name": "Swamp Catfish",
		"description": "A whiskered catfish pulled from the murky swamp.",
		"rarity": "uncommon", "weight": 10, "value": 14,
		"cook_result": "fried_catfish",
		"locations": ["swamp"],
	},

	# ── Rare ──
	"golden_fish": {
		"name": "Golden Carp",
		"description": "A magnificent golden carp that shimmers in the light.",
		"rarity": "rare", "weight": 6, "value": 40,
		"cook_result": "golden_sashimi",
		"locations": ["lake", "river"],
	},
	"ancient_pike": {
		"name": "Ancient Pike",
		"description": "An enormous pike said to be decades old.",
		"rarity": "rare", "weight": 5, "value": 35,
		"cook_result": "pike_feast",
		"locations": ["lake"],
	},
	"ghost_fish": {
		"name": "Ghost Fish",
		"description": "A translucent fish that seems to glow faintly.",
		"rarity": "rare", "weight": 4, "value": 50,
		"cook_result": "ethereal_broth",
		"locations": ["cave", "swamp"],
	},

	# ── Legendary ──
	"leviathan_fry": {
		"name": "Leviathan Fry",
		"description": "A tiny offspring of an ancient water beast. Surely a myth made real.",
		"rarity": "legendary", "weight": 1, "value": 150,
		"cook_result": "legendary_feast",
		"locations": ["lake"],
	},
	"prismatic_koi": {
		"name": "Prismatic Koi",
		"description": "A koi fish that shifts between every color of the rainbow.",
		"rarity": "legendary", "weight": 1, "value": 120,
		"cook_result": "rainbow_sushi",
		"locations": ["river"],
	},

	# ── Junk catches (no bait bonus needed) ──
	"old_boot": {
		"name": "Old Boot",
		"description": "A waterlogged boot. Not the catch of the day.",
		"rarity": "junk", "weight": 8, "value": 1,
		"cook_result": None,
		"locations": ["any"],
	},
	"waterlogged_chest": {
		"name": "Waterlogged Chest",
		"description": "A small chest that's been underwater for ages.",
		"rarity": "uncommon", "weight": 3, "value": 25,
		"cook_result": None,
		"locations": ["any"],
	},
}

# =====================================================================
# LOCATION MAPPING
# =====================================================================
# Maps room IDs to fishing location types for fish pool selection

FISHING_LOCATION_MAP = {
	"riverbank": "river",
	"fishing_spot": "river",
	"river_path": "river",
	"beach": "lake",
	"old_dock": "lake",
	"lakeside_camp": "lake",
	"tidal_caves": "cave",
	"foggy_marsh": "swamp",
	"deep_swamp": "swamp",
	"swamp_edge": "swamp",
}

WATER_ROOMS = set(FISHING_LOCATION_MAP.keys())

# =====================================================================
# COOKING RECIPES (for crafting system integration)
# =====================================================================

FISH_COOKING_RECIPES = {
	"cooked_fish": {
		"id": "cooked_fish",
		"name": "Cooked Fish",
		"ingredients": {"small_fish": 1},
		"result": ("cooked_fish", 1),
		"station": "campfire",
		"description": "A simply cooked fish. Restores some health.",
		"auto_discover": True,
	},
	"grilled_trout": {
		"id": "grilled_trout",
		"name": "Grilled Trout",
		"ingredients": {"river_trout": 1},
		"result": ("grilled_trout", 1),
		"station": "campfire",
		"description": "Grilled river trout with herbs. Restores health.",
		"auto_discover": True,
	},
	"grilled_perch": {
		"id": "grilled_perch",
		"name": "Grilled Perch",
		"ingredients": {"striped_perch": 1},
		"result": ("grilled_perch", 1),
		"station": "campfire",
		"description": "A delicately grilled perch. Restores health.",
		"auto_discover": True,
	},
	"hearty_fish_stew": {
		"id": "hearty_fish_stew",
		"name": "Hearty Fish Stew",
		"ingredients": {"large_fish": 1, "swamp_moss": 1},
		"result": ("hearty_fish_stew", 1),
		"station": "campfire",
		"description": "A filling stew that restores lots of health.",
	},
	"eel_skewer": {
		"id": "eel_skewer",
		"name": "Eel Skewer",
		"ingredients": {"cave_eel": 1, "stick": 1},
		"result": ("eel_skewer", 1),
		"station": "campfire",
		"description": "Grilled cave eel on a stick. Grants a small attack boost.",
	},
	"fried_catfish": {
		"id": "fried_catfish",
		"name": "Fried Catfish",
		"ingredients": {"swamp_catfish": 1},
		"result": ("fried_catfish", 1),
		"station": "campfire",
		"description": "Crispy fried catfish. Restores health and cures poison.",
		"auto_discover": True,
	},
	"golden_sashimi": {
		"id": "golden_sashimi",
		"name": "Golden Sashimi",
		"ingredients": {"golden_fish": 1},
		"result": ("golden_sashimi", 1),
		"station": "campfire",
		"description": "Exquisite raw golden carp. Grants major health and attack boost.",
	},
	"pike_feast": {
		"id": "pike_feast",
		"name": "Ancient Pike Feast",
		"ingredients": {"ancient_pike": 1, "swamp_moss": 1},
		"result": ("pike_feast", 1),
		"station": "campfire",
		"description": "A grand feast from an ancient pike. Fully restores health.",
	},
	"ethereal_broth": {
		"id": "ethereal_broth",
		"name": "Ethereal Broth",
		"ingredients": {"ghost_fish": 1, "ectoplasm": 1},
		"result": ("ethereal_broth", 1),
		"station": "campfire",
		"description": "A ghostly broth that temporarily boosts defense greatly.",
	},
	"legendary_feast": {
		"id": "legendary_feast",
		"name": "Leviathan Feast",
		"ingredients": {"leviathan_fry": 1},
		"result": ("legendary_feast", 1),
		"station": "campfire",
		"description": "A feast of mythic proportions. Fully heals and grants all stat boosts.",
	},
	"rainbow_sushi": {
		"id": "rainbow_sushi",
		"name": "Rainbow Sushi",
		"ingredients": {"prismatic_koi": 1},
		"result": ("rainbow_sushi", 1),
		"station": "campfire",
		"description": "Iridescent sushi that shimmers. Massive XP bonus and heals.",
	},
}

# =====================================================================
# COOKED FOOD EFFECTS
# =====================================================================

COOKED_FOOD_EFFECTS = {
	"cooked_fish": {"heal": 15, "description": "Restores 15 HP."},
	"grilled_trout": {"heal": 25, "description": "Restores 25 HP."},
	"grilled_perch": {"heal": 20, "description": "Restores 20 HP."},
	"hearty_fish_stew": {"heal": 50, "description": "Restores 50 HP."},
	"eel_skewer": {"heal": 20, "attack_boost": 3, "duration": 5, "description": "Restores 20 HP, +3 ATK for 5 turns."},
	"fried_catfish": {"heal": 30, "cure_poison": True, "description": "Restores 30 HP, cures poison."},
	"golden_sashimi": {"heal": 60, "attack_boost": 5, "duration": 8, "description": "Restores 60 HP, +5 ATK for 8 turns."},
	"pike_feast": {"heal_full": True, "description": "Fully restores HP."},
	"ethereal_broth": {"heal": 30, "defense_boost": 5, "duration": 8, "description": "Restores 30 HP, +5 DEF for 8 turns."},
	"legendary_feast": {"heal_full": True, "attack_boost": 8, "defense_boost": 5, "duration": 10, "description": "Full heal, +8 ATK, +5 DEF for 10 turns."},
	"rainbow_sushi": {"heal": 80, "xp_bonus": 50, "description": "Restores 80 HP, grants 50 bonus XP."},
}

# =====================================================================
# TIMING BAR CONFIGURATION
# =====================================================================

BASE_SWEET_SPOT = 0.20   # 20% of the bar is "perfect" zone
GOOD_ZONE = 0.15         # 15% padding on each side of sweet spot
BAR_SPEED = 2.0          # Cycles per second (base)
BAR_WIDTH = 300          # Pixels
BAR_HEIGHT = 40          # Pixels

# Rarity multipliers for timing difficulty
RARITY_SPEED = {
	"common": 1.0,
	"uncommon": 1.3,
	"rare": 1.6,
	"legendary": 2.0,
	"junk": 0.8,
}


class FishingMinigame:
	"""Manages the fishing minigame logic and pygame timing bar overlay."""

	def __init__(self, engine):
		self.engine = engine
		self.current_bait = None
		self.fish_caught_count = 0
		self.biggest_catch_value = 0

	def can_fish(self):
		"""Check if player can fish here."""
		room_id = self.engine.player.current_room
		if room_id not in WATER_ROOMS:
			return False, "You need to be near water to fish."

		# Check for fishing rod
		inv = self.engine.player.inventory
		if inv.get("old_fishing_rod", 0) <= 0:
			return False, "You need a fishing rod to fish. Try looking for one near water."

		return True, ""

	def get_location_type(self, room_id=None):
		"""Get the fishing location type for the current room."""
		if room_id is None:
			room_id = self.engine.player.current_room
		return FISHING_LOCATION_MAP.get(room_id, "any")

	def get_fish_pool(self, location_type, bait_id=None):
		"""Get the weighted fish pool for a location, modified by bait."""
		pool = []
		bait = BAIT_TYPES.get(bait_id, {}) if bait_id else {}
		rarity_bonus = bait.get("rarity_bonus", 0)

		for fish_id, fish in FISH_DATABASE.items():
			# Check location match
			if "any" not in fish["locations"] and location_type not in fish["locations"]:
				continue

			weight = fish["weight"]

			# Apply bait rarity bonus — increase weight of rare+ fish
			if fish["rarity"] in ("rare", "legendary") and rarity_bonus > 0:
				weight = int(weight * (1 + rarity_bonus * 5))
			elif fish["rarity"] == "junk" and rarity_bonus > 0:
				weight = max(1, int(weight * (1 - rarity_bonus * 2)))

			pool.append((fish_id, weight))

		return pool

	def roll_catch(self, pool, timing_quality):
		"""
		Roll for a catch based on pool and timing quality.
		timing_quality: "perfect" (1.0), "good" (0.7), "ok" (0.4), "miss" (0.1)
		"""
		quality_multipliers = {
			"perfect": {"common": 0.5, "uncommon": 1.5, "rare": 3.0, "legendary": 5.0, "junk": 0.1},
			"good": {"common": 0.8, "uncommon": 1.2, "rare": 1.5, "legendary": 2.0, "junk": 0.3},
			"ok": {"common": 1.0, "uncommon": 1.0, "rare": 0.8, "legendary": 0.5, "junk": 0.8},
			"miss": {"common": 1.0, "uncommon": 0.5, "rare": 0.1, "legendary": 0.0, "junk": 2.0},
		}

		mults = quality_multipliers.get(timing_quality, quality_multipliers["ok"])

		# Adjust pool weights
		adjusted = []
		for fish_id, weight in pool:
			rarity = FISH_DATABASE[fish_id]["rarity"]
			mult = mults.get(rarity, 1.0)
			adj_weight = max(0, int(weight * mult))
			if adj_weight > 0:
				adjusted.append((fish_id, adj_weight))

		if not adjusted:
			return None

		total = sum(w for _, w in adjusted)
		roll = random.randint(1, total)
		cumulative = 0
		for fish_id, w in adjusted:
			cumulative += w
			if roll <= cumulative:
				return fish_id

		return adjusted[-1][0]  # fallback

	def start_fishing(self, bait_id=None):
		"""
		Start fishing. Returns result text.
		If pygame GUI is available, opens timing bar minigame overlay.
		Otherwise falls back to simple random catch.
		"""
		can, msg = self.can_fish()
		if not can:
			return msg

		# Consume bait if specified
		if bait_id:
			if bait_id not in BAIT_TYPES:
				return f"Unknown bait type: {bait_id.replace('_', ' ')}. Use 'bait' to see available baits."
			inv = self.engine.player.inventory
			if inv.get(bait_id, 0) <= 0:
				return f"You don't have any {BAIT_TYPES[bait_id]['name']}."
			self.current_bait = bait_id
		else:
			self.current_bait = None

		# Try to use Pygame timing bar
		gui = getattr(self.engine, 'gui', None)
		if gui:
			return self._open_timing_bar()
		else:
			# Fallback: simple timing simulation
			return self._simple_fishing()

	def _simple_fishing(self):
		"""Fallback fishing without GUI — simulates timing quality randomly."""
		location = self.get_location_type()
		pool = self.get_fish_pool(location, self.current_bait)

		# Simulate timing quality
		quality_roll = random.random()
		if quality_roll < 0.15:
			quality = "perfect"
		elif quality_roll < 0.45:
			quality = "good"
		elif quality_roll < 0.75:
			quality = "ok"
		else:
			quality = "miss"

		return self._process_catch(pool, quality)

	def _open_timing_bar(self, _root_unused=None):
		"""Open a Pygame overlay with a timing-bar minigame."""

		# Consume bait before starting minigame
		if self.current_bait:
			inv = self.engine.player.inventory
			inv[self.current_bait] -= 1
			if inv[self.current_bait] <= 0:
				del inv[self.current_bait]
			self.engine._inventory_changed = True

		location = self.get_location_type()
		pool = self.get_fish_pool(location, self.current_bait)
		bait = BAIT_TYPES.get(self.current_bait, {})
		sweet_bonus = bait.get("sweet_spot_bonus", 0)

		# Calculate sweet spot
		sweet_size = BASE_SWEET_SPOT + sweet_bonus
		good_size = GOOD_ZONE
		sweet_start = random.uniform(0.2, 0.8 - sweet_size)
		sweet_end = sweet_start + sweet_size
		good_start = max(0, sweet_start - good_size)
		good_end = min(1, sweet_end + good_size)

		bait_text = f" (using {bait.get('name', 'no bait')})" if self.current_bait else " (no bait)"

		# Create the overlay and attach to the GUI
		overlay = FishingTimingOverlay(
			minigame=self,
			pool=pool,
			sweet_start=sweet_start, sweet_end=sweet_end,
			good_start=good_start, good_end=good_end,
			bait_text=bait_text,
		)
		gui = getattr(self.engine, 'gui', None)
		if gui:
			gui._fishing_overlay = overlay

		bait_name = bait.get("name", "")
		return f"🎣 You cast your line{f' with {bait_name}' if bait_name else ''}... (Press SPACE to catch!)"

	def _process_catch(self, pool, timing_quality):
		"""Process the catch result and add to inventory."""
		fish_id = self.roll_catch(pool, timing_quality)

		quality_text = {
			"perfect": "⭐ Perfect timing!",
			"good": "✓ Good timing!",
			"ok": "~ Decent timing.",
			"miss": "✗ Bad timing...",
		}

		result = "\n" + "═" * 55 + "\n"
		result += "  🎣 FISHING RESULT\n"
		result += "═" * 55 + "\n\n"
		result += f"  {quality_text.get(timing_quality, '')}\n\n"

		if not fish_id or fish_id not in FISH_DATABASE:
			result += "  The line comes up empty. Better luck next time!\n"
			return result

		fish = FISH_DATABASE[fish_id]
		rarity = fish["rarity"]
		rarity_colors = {
			"junk": "⬜",
			"common": "🟢",
			"uncommon": "🔵",
			"rare": "🟡",
			"legendary": "🟣",
		}

		icon = rarity_colors.get(rarity, "⬜")
		result += f"  {icon} You caught: {fish['name']}! ({rarity.upper()})\n"
		result += f"     {fish['description']}\n"
		result += f"     Value: {fish['value']} gold\n"

		# Add to inventory
		inv = self.engine.player.inventory
		inv[fish_id] = inv.get(fish_id, 0) + 1
		self.engine._inventory_changed = True

		# Register item worth
		if hasattr(self.engine, 'item_worth'):
			self.engine.item_worth[fish_id] = fish["value"]

		# Update stats
		self.fish_caught_count += 1
		if fish["value"] > self.biggest_catch_value:
			self.biggest_catch_value = fish["value"]

		# Bonus XP for rare catches
		try:
			from progression_system import award_xp, XP_AWARDS
			xp = {"junk": 2, "common": 5, "uncommon": 10, "rare": 25, "legendary": 75}.get(rarity, 5)
			xp_msg = award_xp(self.engine.player, xp, "fishing")
			if xp_msg:
				result += f"\n{xp_msg}"
		except (ImportError, Exception):
			pass

		# Cook hint for cookable fish
		if fish.get("cook_result"):
			result += f"\n  💡 This can be cooked at a campfire!\n"

		result += "\n" + "─" * 55 + "\n"
		return result

	def show_bait_info(self):
		"""Show available baits and current bait."""
		inv = self.engine.player.inventory
		result = "\n" + "═" * 55 + "\n"
		result += "  🪱 BAIT INVENTORY\n"
		result += "═" * 55 + "\n\n"

		has_any = False
		for bait_id, bait in BAIT_TYPES.items():
			count = inv.get(bait_id, 0)
			if count > 0:
				has_any = True
				result += f"  • {bait['name']} x{count}\n"
				result += f"    {bait['description']}\n"
				result += f"    Rarity bonus: +{int(bait['rarity_bonus']*100)}%  |  Sweet spot: +{int(bait['sweet_spot_bonus']*100)}%\n\n"

		if not has_any:
			result += "  You don't have any bait.\n"
			result += "  Try searching near water or buying from a shop!\n\n"

		result += "─" * 55 + "\n"
		result += "  Usage: fish <bait_name> — to fish with specific bait\n"
		result += "         fish            — to fish without bait\n"
		result += "─" * 55 + "\n"
		return result

	def use_cooked_food(self, food_id):
		"""Apply effects of cooked food. Returns result text."""
		effects = COOKED_FOOD_EFFECTS.get(food_id)
		if not effects:
			return None  # Not a cooked food item

		player = self.engine.player
		stats = player.stats
		parts = []

		# Heal
		if effects.get("heal_full"):
			max_hp = stats.get("health_max", 100)
			healed = max_hp - stats.get("health", 0)
			stats["health"] = max_hp
			parts.append(f"  ❤️ Fully healed! (+{healed} HP)")
		elif effects.get("heal"):
			amount = effects["heal"]
			max_hp = stats.get("health_max", 100)
			old_hp = stats.get("health", max_hp)
			stats["health"] = min(max_hp, old_hp + amount)
			actual = stats["health"] - old_hp
			parts.append(f"  ❤️ Restored {actual} HP")

		# Cure poison
		if effects.get("cure_poison"):
			if hasattr(self.engine, 'poison_status') and self.engine.poison_status:
				self.engine.poison_status = None
				parts.append("  🟢 Poison cured!")

		# Stat boosts (temporary — stored in player state)
		for boost_type in ("attack_boost", "defense_boost"):
			if effects.get(boost_type):
				amount = effects[boost_type]
				duration = effects.get("duration", 5)
				stat_name = boost_type.replace("_boost", "")
				# Store as temporary buff
				if "temp_buffs" not in player.state:
					player.state["temp_buffs"] = []
				player.state["temp_buffs"].append({
					"stat": stat_name,
					"amount": amount,
					"turns_left": duration,
				})
				stats[stat_name] = stats.get(stat_name, 0) + amount
				parts.append(f"  ⬆️ +{amount} {stat_name.upper()} for {duration} turns")

		# XP bonus
		if effects.get("xp_bonus"):
			try:
				from progression_system import award_xp
				xp_msg = award_xp(player, effects["xp_bonus"], "cooked food XP")
				if xp_msg:
					parts.append(xp_msg)
			except (ImportError, Exception):
				pass

		if not parts:
			return f"You eat the {food_id.replace('_', ' ')}."

		nice_name = food_id.replace("_", " ")
		result = f"\n  🍳 You eat the {nice_name}:\n\n"
		result += "\n".join(parts) + "\n"
		return result

	# ─── Persistence ───

	def to_dict(self):
		return {
			"fish_caught_count": self.fish_caught_count,
			"biggest_catch_value": self.biggest_catch_value,
		}

	def load_from_dict(self, data):
		if isinstance(data, dict):
			self.fish_caught_count = data.get("fish_caught_count", 0)
			self.biggest_catch_value = data.get("biggest_catch_value", 0)


# =====================================================================
# FISHING TIMING BAR OVERLAY (Pygame)
# =====================================================================

class FishingTimingOverlay:
	"""Rendered as an overlay by the main game loop.
	Bouncing marker, press Space/Enter to catch."""

	def __init__(self, minigame, pool, sweet_start, sweet_end,
				 good_start, good_end, bait_text=""):
		self.minigame = minigame
		self.pool = pool
		self.sweet_start = sweet_start
		self.sweet_end = sweet_end
		self.good_start = good_start
		self.good_end = good_end
		self.bait_text = bait_text

		self.pos = 0.0
		self.direction = 1
		self.running = True
		self.done = False
		self.result_text = ""
		self._finish_timer = 0.0
		self._quality = None
		self._quality_text = ""
		self._marker_color = (255, 255, 255)
		self._font = None
		self._small_font = None

	def _ensure_fonts(self):
		if self._font is None:
			import pygame
			self._font       = pygame.font.SysFont("Courier New", 15, bold=True)
			self._small_font = pygame.font.SysFont("Courier New", 11)
		# store extra fields if not present
		if not hasattr(self, '_anim_frame'):
			self._anim_frame = 0
			self._anim_t     = 0.0

	def handle_event(self, event):
		import pygame
		if self.done or not self.running:
			return
		if event.type == pygame.KEYDOWN:
			if event.key in (pygame.K_SPACE, pygame.K_RETURN):
				self._catch()

	def _catch(self):
		self.running = False
		pos = self.pos
		if self.sweet_start <= pos <= self.sweet_end:
			self._quality = "perfect"
			self._marker_color = (0, 255, 0)
			self._quality_text = "✨ PERFECT CAST! ✨"
		elif self.good_start <= pos <= self.good_end:
			self._quality = "good"
			self._marker_color = (255, 255, 0)
			self._quality_text = "⭐ Great catch!"
		else:
			dist = min(abs(pos - self.sweet_start), abs(pos - self.sweet_end))
			if dist < 0.15:
				self._quality = "ok"
				self._marker_color = (255, 136, 0)
				self._quality_text = "~ Okay catch"
			else:
				self._quality = "miss"
				self._marker_color = (255, 0, 0)
				self._quality_text = "❌ Missed! Poor catch..."

	def update(self, dt):
		if self.done:
			return
		# Advance ASCII animation frame
		if not hasattr(self, '_anim_frame'):
			self._anim_frame = 0
			self._anim_t     = 0.0
		self._anim_t += dt
		if self._anim_t >= 0.25:
			self._anim_t   = 0.0
			self._anim_frame += 1
		if self.running:
			self.pos += self.direction * BAR_SPEED * dt
			if self.pos >= 1.0:
				self.pos = 1.0
				self.direction = -1
			elif self.pos <= 0.0:
				self.pos = 0.0
				self.direction = 1
		else:
			self._finish_timer += dt
			if self._finish_timer >= 1.8:
				self._finish()

	def _finish(self):
		result = self.minigame._process_catch(self.pool, self._quality or "miss")
		gui = getattr(self.minigame.engine, 'gui', None)
		if gui:
			gui.append(result)
		self.done = True

	def render(self, surface):
		import pygame
		self._ensure_fonts()

		# Try to load ASCII art helpers (graceful fallback to legacy render)
		_ascii_ok = False
		try:
			from ascii_art import (ANIMATION_FRAMES, render_ascii_block,
			                       draw_dim_overlay, draw_panel, render_label,
			                       _ensure_fonts as _af)
			_af()
			_ascii_ok = True
		except ImportError:
			pass

		sw, sh = surface.get_size()

		if not _ascii_ok:
			# ─── Fallback legacy render (unchanged) ───────────────────────────
			ow, oh = 420, 180
			ox = (sw - ow) // 2
			oy = (sh - oh) // 2
			dim = pygame.Surface((sw, sh), pygame.SRCALPHA)
			dim.fill((0, 0, 0, 120))
			surface.blit(dim, (0, 0))
			pygame.draw.rect(surface, (20, 20, 40), (ox, oy, ow, oh), border_radius=8)
			pygame.draw.rect(surface, (80, 80, 120), (ox, oy, ow, oh), 2, border_radius=8)
			title = self._font.render(f"Fishing!{self.bait_text}", True, (200, 200, 255))
			surface.blit(title, (ox + ow // 2 - title.get_width() // 2, oy + 10))
			if self.running:
				inst = self._small_font.render("Press SPACE when marker is in the green zone!", True, (170, 170, 170))
			else:
				inst = self._font.render(self._quality_text, True, self._marker_color)
			surface.blit(inst, (ox + ow // 2 - inst.get_width() // 2, oy + 36))
			bar_x = ox + 20; bar_y = oy + 65; bar_w = ow - 40; bar_h = 40
			pygame.draw.rect(surface, (51, 51, 85), (bar_x, bar_y, bar_w, bar_h))
			gx0 = bar_x + int(self.good_start * bar_w);  gx1 = bar_x + int(self.good_end * bar_w)
			pygame.draw.rect(surface, (139, 128, 0), (gx0, bar_y, gx1 - gx0, bar_h))
			sx0 = bar_x + int(self.sweet_start * bar_w); sx1 = bar_x + int(self.sweet_end * bar_w)
			pygame.draw.rect(surface, (0, 170, 0), (sx0, bar_y, sx1 - sx0, bar_h))
			mx = bar_x + int(self.pos * bar_w)
			pygame.draw.rect(surface, self._marker_color, (mx, bar_y, 6, bar_h))
			hint = self._small_font.render("[SPACE] to catch!", True, (100, 150, 220))
			surface.blit(hint, (ox + ow // 2 - hint.get_width() // 2, oy + oh - 30))
			return

		# ─── Upgraded ASCII render ─────────────────────────────────────────────
		ow, oh = 540, 300
		ox = (sw - ow) // 2
		oy = (sh - oh) // 2

		draw_dim_overlay(surface, 145)
		draw_panel(surface, (ox, oy, ow, oh), title=f"FISHING{self.bait_text}")

		# Fisher animation (left side)
		fisher_frames = ANIMATION_FRAMES.get(
			"fish_jump" if not self.running else "fisher_cast", [[]])
		fisher_frame  = fisher_frames[getattr(self, '_anim_frame', 0) % max(len(fisher_frames), 1)]
		render_ascii_block(surface, fisher_frame, ox + 18, oy + 50,
		                   color=(100, 180, 255) if self.running else (255, 200, 60))

		# Water ripple line (ASCII)
		ripple_chars = ["~  ~  ~  ~  ~", "  ~  ~  ~  ~ ", " ~  ~~  ~   ~"]
		ripple = ripple_chars[getattr(self, '_anim_frame', 0) % 3]
		rip_surf = self._small_font.render(ripple, True, (60, 120, 200))
		surface.blit(rip_surf, (ox + 18, oy + 50 + len(fisher_frame) * 14 + 4))

		# ── Timing bar (block characters + pygame rects) ──────────────────────
		bar_x = ox + 20
		bar_y = oy + 185
		bar_w = ow - 40
		bar_h = 32

		# Background
		pygame.draw.rect(surface, (20, 30, 50), (bar_x, bar_y, bar_w, bar_h), border_radius=5)

		# Good zone
		gx0 = bar_x + int(self.good_start * bar_w)
		gx1 = bar_x + int(self.good_end   * bar_w)
		pygame.draw.rect(surface, (120, 100, 0), (gx0, bar_y, gx1 - gx0, bar_h), border_radius=3)

		# Sweet zone
		sx0 = bar_x + int(self.sweet_start * bar_w)
		sx1 = bar_x + int(self.sweet_end   * bar_w)
		pygame.draw.rect(surface, (0, 150, 0),   (sx0, bar_y, sx1 - sx0, bar_h), border_radius=3)

		# Block-char overlay for texture
		total_cells = (bar_w - 2) // 8
		bar_str = ""
		for i in range(total_cells):
			frac = i / max(total_cells - 1, 1)
			if self.sweet_start <= frac <= self.sweet_end:
				bar_str += "▓"
			elif self.good_start <= frac <= self.good_end:
				bar_str += "▒"
			else:
				bar_str += "░"
		blk_surf = self._small_font.render(bar_str, True, (80, 80, 80))
		surface.blit(blk_surf, (bar_x + 1, bar_y + bar_h // 2 - blk_surf.get_height() // 2))

		# Marker
		mx = bar_x + int(self.pos * bar_w)
		pygame.draw.rect(surface, self._marker_color, (mx - 3, bar_y - 4, 6, bar_h + 8), border_radius=3)
		pygame.draw.rect(surface, (255, 255, 200), (mx - 3, bar_y - 4, 6, bar_h + 8), 1, border_radius=3)

		# Border
		pygame.draw.rect(surface, (60, 80, 120), (bar_x, bar_y, bar_w, bar_h), 2, border_radius=5)

		# Zone labels inside bar
		lbl_sw = self._small_font.render("●SWEET", True, (0, 230, 0))
		surface.blit(lbl_sw, ((sx0 + sx1) // 2 - lbl_sw.get_width() // 2,
		                       bar_y + bar_h // 2 - lbl_sw.get_height() // 2))

		# ── Status text ───────────────────────────────────────────────────────
		if self.running:
			render_label(surface, "Press  [SPACE]  when marker hits the sweet zone!",
			             ox + ow // 2, oy + 155, color=(170, 200, 255))
		else:
			render_label(surface, self._quality_text,
			             ox + ow // 2, oy + 155, color=self._marker_color)

		# ── Catch hint ────────────────────────────────────────────────────────
		if self.running:
			render_label(surface, "[SPACE] — cast!",
			             ox + ow // 2, oy + oh - 28, color=(80, 120, 200), small=True)
		else:
			render_label(surface, "Reeling in...",
			             ox + ow // 2, oy + oh - 28, color=(140, 140, 180), small=True)
