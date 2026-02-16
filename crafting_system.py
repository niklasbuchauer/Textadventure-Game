"""
Crafting System
===============
Station-based crafting with discoverable recipes.
Recipes are learned from NPCs, books, or discovered at altars.
Crafting requires being at the correct station type.
"""

# Progression integration
try:
	from progression_system import award_xp, XP_AWARDS
	PROGRESSION_AVAILABLE = True
except ImportError:
	PROGRESSION_AVAILABLE = False

# =====================================================================
# STATION TYPES
# =====================================================================
# "forge"          — Village Blacksmith
# "altar_crystal"  — Crystal Caverns (Forge of Light)
# "altar_shadow"   — Shadow Depths (Shadowforge)
# "altar_iron"     — Iron Halls (Dwarven Anvil / altar)
# "altar_catacomb" — Sunken Catacombs (altar)
# "any"            — Any crafting station (forge or any altar)
# =====================================================================

STATION_NAMES = {
	"forge": "Blacksmith's Forge",
	"altar_crystal": "Forge of Light",
	"altar_shadow": "The Shadowforge",
	"altar_iron": "Dwarven Eternal Anvil",
	"altar_catacomb": "Catacomb Soul Altar",
	"campfire": "Campfire",
}

# =====================================================================
# RECIPE DATABASE
# =====================================================================
# Each recipe:
#   id:          unique string identifier
#   name:        display name
#   ingredients: {item_name: count_needed}
#   result:      (item_name, count_produced)
#   station:     station type required (or "any")
#   description: flavor text
#   auto_discover: True if discovered when visiting the altar (not NPC-taught)
# =====================================================================

RECIPE_DATABASE = {
	# ─── FORGE (Blacksmith) Recipes ─────────────────────────────────
	"steel_dagger": {
		"id": "steel_dagger",
		"name": "Steel Dagger",
		"ingredients": {"iron_ingot": 1, "stick": 1},
		"result": ("steel_dagger", 1),
		"station": "forge",
		"description": "A sharp, reliable dagger forged from iron and wood.",
	},
	"iron_sword": {
		"id": "iron_sword",
		"name": "Iron Sword",
		"ingredients": {"iron_ingot": 2, "stick": 1},
		"result": ("iron_sword", 1),
		"station": "forge",
		"description": "A sturdy iron sword. The blacksmith's bread and butter.",
	},
	"steel_longsword": {
		"id": "steel_longsword",
		"name": "Steel Longsword",
		"ingredients": {"iron_ingot": 3, "refined_iron": 1},
		"result": ("steel_longsword", 1),
		"station": "forge",
		"description": "A long, balanced blade of tempered steel.",
	},
	"leather_armor_piece": {
		"id": "leather_armor_piece",
		"name": "Leather Armor",
		"ingredients": {"wolf_pelt": 2, "rope_coil": 1},
		"result": ("leather_armor_piece", 1),
		"station": "forge",
		"description": "Light armor stitched from wolf pelts. Offers decent protection.",
	},
	"masterwork_shield": {
		"id": "masterwork_shield",
		"name": "Masterwork Shield",
		"ingredients": {"iron_ingot": 2, "broken_shield": 1, "refined_iron": 1},
		"result": ("masterwork_shield", 1),
		"station": "forge",
		"description": "A shield reforged from scrap into something magnificent.",
	},
	"refined_iron": {
		"id": "refined_iron",
		"name": "Refined Iron",
		"ingredients": {"iron_ingot": 2},
		"result": ("refined_iron", 1),
		"station": "forge",
		"description": "Purified iron, ready for advanced smithing.",
	},

	# ─── ANY STATION Recipes (potions, simpler crafts) ──────────────
	"healing_potion": {
		"id": "healing_potion",
		"name": "Healing Potion",
		"ingredients": {"strange_herb": 2, "mineral_water_flask": 1},
		"result": ("healing_potion", 1),
		"station": "any",
		"description": "A powerful restorative potion brewed from rare herbs.",
	},
	"antidote": {
		"id": "antidote",
		"name": "Antidote",
		"ingredients": {"strange_herb": 1, "shelf_mushroom": 2},
		"result": ("antidote", 1),
		"station": "any",
		"description": "A remedy that neutralizes most poisons.",
	},
	"poison_cure": {
		"id": "poison_cure",
		"name": "Swamp Poison Cure",
		"ingredients": {"glowing_moss": 2, "marsh_lily": 1},
		"result": ("poison_cure", 1),
		"station": "any",
		"description": "A potent cure brewed from swamp ingredients. The witch's specialty.",
	},
	"holy_water": {
		"id": "holy_water",
		"name": "Holy Water",
		"ingredients": {"prayer_candle": 1, "mineral_water_flask": 1},
		"result": ("holy_water", 1),
		"station": "any",
		"description": "Water blessed with divine energy. Heals and purifies.",
	},
	"quality_torch": {
		"id": "quality_torch",
		"name": "Quality Torch",
		"ingredients": {"torch": 1, "rope_coil": 1, "glowing_moss": 1},
		"result": ("quality_torch", 1),
		"station": "any",
		"description": "A well-made torch with a long-lasting, bright flame.",
	},

	# ─── CRYSTAL ALTAR Recipes ──────────────────────────────────────
	"crystal_shield": {
		"id": "crystal_shield",
		"name": "Crystal Shield",
		"ingredients": {"raw_diamond": 1, "heart_crystal_fragment": 1},
		"result": ("crystal_shield", 1),
		"station": "altar_crystal",
		"description": "A shield of living crystal that refracts attacks into harmless light.",
		"auto_discover": True,
	},
	"enchanted_ring": {
		"id": "enchanted_ring",
		"name": "Enchanted Ring",
		"ingredients": {"golden_ring": 1, "resonance_crystal": 1},
		"result": ("enchanted_ring", 1),
		"station": "altar_crystal",
		"description": "A ring humming with crystalline energy.",
		"auto_discover": True,
	},
	"prismatic_blade": {
		"id": "prismatic_blade",
		"name": "Prismatic Blade",
		"ingredients": {"spectrum_prism": 1, "steel_longsword": 1, "concentrated_light_essence": 1},
		"result": ("prismatic_blade", 1),
		"station": "altar_crystal",
		"description": "A sword that splits light into deadly rainbows with each swing.",
		"auto_discover": True,
	},

	# ─── SHADOW ALTAR Recipes ───────────────────────────────────────
	"shadow_blade": {
		"id": "shadow_blade",
		"name": "Shadow Blade",
		"ingredients": {"obsidian_blade_fragment": 2, "concentrated_void_essence": 1},
		"result": ("shadow_blade", 1),
		"station": "altar_shadow",
		"description": "A blade forged from void and obsidian. Cuts through shadow and steel alike.",
		"auto_discover": True,
	},
	"void_amulet": {
		"id": "void_amulet",
		"name": "Void Amulet",
		"ingredients": {"dread_idol": 1, "void_heart_fragment": 1},
		"result": ("void_amulet", 1),
		"station": "altar_shadow",
		"description": "An amulet pulsing with void energy. Protects against shadow attacks.",
		"auto_discover": True,
	},
	"sovereign_cloak": {
		"id": "sovereign_cloak",
		"name": "Sovereign's Cloak",
		"ingredients": {"sovereign_shadow_crown": 1, "enchanted_cloak_fragment": 1, "umbral_thread": 2},
		"result": ("sovereign_cloak", 1),
		"station": "altar_shadow",
		"description": "A cloak woven from the Shadow Sovereign's own essence. Grants partial invisibility.",
		"auto_discover": True,
	},

	# ─── IRON ALTAR Recipes ─────────────────────────────────────────
	"mithril_blade": {
		"id": "mithril_blade",
		"name": "Mithril Blade",
		"ingredients": {"raw_mithril": 1, "eternal_ember": 1},
		"result": ("mithril_blade", 1),
		"station": "altar_iron",
		"description": "The finest blade that can be forged. Light as a feather, strong as mountains.",
		"auto_discover": True,
	},
	"dwarven_masterwork": {
		"id": "dwarven_masterwork",
		"name": "Dwarven Masterwork Armor",
		"ingredients": {"tempered_steel_ingot": 2, "mithril_dust": 1, "forgemaster_hammer": 1},
		"result": ("dwarven_masterwork", 1),
		"station": "altar_iron",
		"description": "Armor forged using ancient dwarven techniques. Nearly indestructible.",
		"auto_discover": True,
	},

	# ─── CATACOMB ALTAR Recipes ─────────────────────────────────────
	"soul_blade": {
		"id": "soul_blade",
		"name": "Soul Blade",
		"ingredients": {"soul_gem": 1, "cracked_phylactery": 1, "iron_sword": 1},
		"result": ("soul_blade", 1),
		"station": "altar_catacomb",
		"description": "A blade infused with spectral energy. Glows with ghostly fire.",
		"auto_discover": True,
	},
	"lich_crown": {
		"id": "lich_crown",
		"name": "Lich Crown",
		"ingredients": {"lich_crown_fragment": 1, "enchanted_ring": 1, "blood_ruby": 1},
		"result": ("lich_crown", 1),
		"station": "altar_catacomb",
		"description": "A crown of dark power, restored from its shattered form.",
		"auto_discover": True,
	},
}

# =====================================================================
# FISH COOKING RECIPES (loaded dynamically from fishing_system)
# =====================================================================
try:
	from fishing_system import FISH_COOKING_RECIPES
	RECIPE_DATABASE.update(FISH_COOKING_RECIPES)
except ImportError:
	pass

# Item worth for crafted items (that don't already exist in the item_worth table)
CRAFTED_ITEM_WORTH = {
	"steel_dagger": 35,
	"iron_sword": 30,
	"steel_longsword": 110,
	"leather_armor_piece": 25,
	"masterwork_shield": 125,
	"refined_iron": 40,
	"healing_potion": 85,
	"antidote": 45,
	"poison_cure": 50,
	"holy_water": 55,
	"quality_torch": 15,
	"crystal_shield": 220,
	"enchanted_ring": 120,
	"prismatic_blade": 350,
	"shadow_blade": 280,
	"void_amulet": 250,
	"sovereign_cloak": 400,
	"mithril_blade": 320,
	"dwarven_masterwork": 380,
	"soul_blade": 300,
	"lich_crown": 350,
	# Cooked food
	"cooked_fish": 10,
	"grilled_trout": 18,
	"grilled_perch": 15,
	"hearty_fish_stew": 40,
	"eel_skewer": 25,
	"fried_catfish": 22,
	"golden_sashimi": 80,
	"pike_feast": 60,
	"ethereal_broth": 55,
	"legendary_feast": 200,
	"rainbow_sushi": 180,
}


class CraftingSystem:
	"""Handles station-based crafting with discoverable recipes."""

	def __init__(self, engine):
		self.engine = engine

	def get_known_recipes(self):
		"""Get list of recipe IDs the player knows."""
		return self.engine.player.state.get("known_recipes", [])

	def learn_recipe(self, recipe_id):
		"""
		Teach the player a recipe. Returns a message string.
		"""
		if recipe_id not in RECIPE_DATABASE:
			return None

		known = self.engine.player.state.get("known_recipes", [])
		if recipe_id in known:
			return None  # Already known, no message

		known.append(recipe_id)
		self.engine.player.state["known_recipes"] = known

		recipe = RECIPE_DATABASE[recipe_id]
		return f"  📜 New recipe learned: {recipe['name']}!"

	def get_current_station_type(self):
		"""
		Determine what crafting station (if any) is in the current room.
		Returns station type string or None.
		"""
		room_id = self.engine.player.current_room

		# Check Room object's crafting_station property (world rooms)
		room_obj = self.engine.get_room_data(room_id)
		if room_obj and hasattr(room_obj, 'crafting_station') and room_obj.crafting_station:
			return room_obj.crafting_station

		# Check village blacksmith (fallback)
		if room_id == "village_blacksmith":
			return "forge"

		# Check dungeon altar rooms
		raw_room = self._get_raw_room(room_id)
		if raw_room and raw_room.get("crafting_altar"):
			# Determine altar type from dungeon context
			if self.engine.current_fixed_dungeon:
				dungeon_id = self.engine.current_fixed_dungeon.get("dungeon_id", "")
				if dungeon_id == "crystal_caverns":
					return "altar_crystal"
				elif dungeon_id == "shadow_depths":
					return "altar_shadow"
				elif dungeon_id == "iron_halls":
					return "altar_iron"
				elif dungeon_id == "sunken_catacombs":
					return "altar_catacomb"
			# Fallback: check room ID prefix
			if room_id.startswith("cc_"):
				return "altar_crystal"
			elif room_id.startswith("sd_"):
				return "altar_shadow"
			elif room_id.startswith("ih_"):
				return "altar_iron"
			elif room_id.startswith("sc_"):
				return "altar_catacomb"

		return None

	def get_available_recipes(self, station_type):
		"""
		Get recipes the player knows that can be crafted at this station.
		Returns list of (recipe_id, recipe_data, can_craft_bool) tuples.
		"""
		known = self.get_known_recipes()
		available = []

		for rid in known:
			recipe = RECIPE_DATABASE.get(rid)
			if not recipe:
				continue
			# Check station compatibility
			req_station = recipe["station"]
			if req_station == "any" or req_station == station_type:
				can_craft = self._has_ingredients(recipe)
				available.append((rid, recipe, can_craft))

		return available

	def _has_ingredients(self, recipe):
		"""Check if player has all ingredients for a recipe."""
		inv = self.engine.player.inventory
		for item, count in recipe["ingredients"].items():
			if inv.get(item, 0) < count:
				return False
		return True

	def craft_recipe(self, recipe_id):
		"""
		Attempt to craft a recipe. Consumes ingredients, produces result.
		Returns result message string.
		"""
		recipe = RECIPE_DATABASE.get(recipe_id)
		if not recipe:
			return "Unknown recipe."

		# Verify station
		station = self.get_current_station_type()
		req = recipe["station"]
		if req != "any" and req != station:
			station_name = STATION_NAMES.get(req, req)
			return f"This recipe requires: {station_name}"

		# Verify ingredients
		inv = self.engine.player.inventory
		missing = []
		for item, count in recipe["ingredients"].items():
			have = inv.get(item, 0)
			if have < count:
				nice = item.replace("_", " ")
				missing.append(f"  {nice}: need {count}, have {have}")

		if missing:
			result = f"Not enough materials for {recipe['name']}:\n"
			result += "\n".join(missing)
			return result

		# Consume ingredients
		for item, count in recipe["ingredients"].items():
			if inv[item] > count:
				inv[item] -= count
			else:
				inv.pop(item, None)

		# Produce result
		result_item, result_count = recipe["result"]
		inv[result_item] = inv.get(result_item, 0) + result_count
		self.engine._inventory_changed = True

		# Register item worth if not already known
		if result_item not in self.engine.item_worth:
			self.engine.item_worth[result_item] = CRAFTED_ITEM_WORTH.get(result_item, 50)

		nice_name = result_item.replace("_", " ")
		result_text = "\n" + "═" * 50 + "\n"
		result_text += f"  ⚒️  CRAFTED: {recipe['name']}\n"
		result_text += "═" * 50 + "\n\n"
		result_text += f"  {recipe['description']}\n\n"
		result_text += f"  +{result_count} {nice_name} added to inventory.\n"
		result_text += "═" * 50 + "\n"

		# Award XP for crafting (tiered by station type)
		if PROGRESSION_AVAILABLE:
			try:
				station_type = recipe.get("station", "any")
				if station_type.startswith("altar_"):
					# Altar recipes are legendary
					xp_key = "craft_legendary"
				elif station_type == "forge":
					# Forge recipes are advanced
					xp_key = "craft_advanced"
				else:
					xp_key = "craft_basic"
				result_text += award_xp(self.engine.player, XP_AWARDS.get(xp_key, 10), "crafted item")
			except Exception:
				pass

		return result_text

	def use_station(self, choice=None):
		"""
		Main entry point when player uses 'craft' command at a station.
		If choice is None, shows the recipe menu.
		If choice is a number, attempts to craft that recipe.
		"""
		station = self.get_current_station_type()
		if not station:
			return "There is no crafting station here.\nYou can craft at the Blacksmith's Forge or at dungeon altars."

		station_name = STATION_NAMES.get(station, "Crafting Station")

		# Auto-discover altar recipes when first visiting
		self._auto_discover_recipes(station)

		# Get available recipes
		recipes = self.get_available_recipes(station)

		if not recipes:
			result = "\n" + "═" * 50 + "\n"
			result += f"  ⚒️  {station_name}\n"
			result += "═" * 50 + "\n\n"
			result += "  You don't know any recipes for this station yet.\n"
			result += "  Talk to NPCs to learn crafting recipes!\n\n"
			result += "  Hint: The blacksmith, hermit, priest, and\n"
			result += "  swamp witch all know useful recipes.\n"
			result += "═" * 50 + "\n"
			return result

		if choice is not None:
			# Craft specific recipe
			try:
				idx = int(choice) - 1
				if 0 <= idx < len(recipes):
					recipe_id = recipes[idx][0]
					return self.craft_recipe(recipe_id)
				else:
					return "Invalid recipe number."
			except ValueError:
				return "Please enter a recipe number."

		# Show recipe menu — store pending state
		result = "\n" + "═" * 50 + "\n"
		result += f"  ⚒️  {station_name}\n"
		result += "═" * 50 + "\n\n"
		result += "  Available recipes:\n\n"

		for i, (rid, recipe, can_craft) in enumerate(recipes, 1):
			status = "✅" if can_craft else "❌"
			result += f"  {i}. {status} {recipe['name']}\n"
			# Show ingredients
			for item, count in recipe["ingredients"].items():
				have = self.engine.player.inventory.get(item, 0)
				nice = item.replace("_", " ")
				indicator = "✓" if have >= count else "✗"
				result += f"       {indicator} {nice}: {have}/{count}\n"
			result += f"       → {recipe['description']}\n\n"

		result += "  Enter a number to craft, or anything else to cancel.\n"
		result += "═" * 50 + "\n"

		# Set pending crafting state
		self.engine.pending_crafting = {
			"station": station,
			"recipes": [(rid, r["name"]) for rid, r, _ in recipes],
		}

		return result

	def handle_crafting_choice(self, cmd):
		"""Handle player's response to crafting menu."""
		pending = self.engine.pending_crafting
		if not pending:
			return None

		self.engine.pending_crafting = None

		cmd = cmd.strip().lower()
		if cmd in ("cancel", "no", "back", "quit", "exit"):
			return "You step back from the crafting station."

		try:
			idx = int(cmd) - 1
			recipes = pending["recipes"]
			if 0 <= idx < len(recipes):
				recipe_id = recipes[idx][0]
				return self.craft_recipe(recipe_id)
			else:
				return "Invalid choice. Crafting cancelled."
		except ValueError:
			return "Crafting cancelled."

	def _auto_discover_recipes(self, station_type):
		"""Auto-discover recipes marked for this station type."""
		learned_any = False
		for rid, recipe in RECIPE_DATABASE.items():
			if recipe.get("auto_discover") and recipe["station"] == station_type:
				msg = self.learn_recipe(rid)
				if msg:
					learned_any = True
					# We'll show the discovery as part of the station display
		return learned_any

	def _get_raw_room(self, room_id):
		"""Get raw room data from dungeon."""
		if self.engine.current_dungeon_instance:
			try:
				from trap_system import TrapSystem
				raw = TrapSystem.find_raw_room(self.engine.current_dungeon_instance, room_id)
				if raw:
					return raw
			except Exception:
				pass
		if self.engine.current_fixed_dungeon:
			for _fnum, fdata in self.engine.current_fixed_dungeon.get("floors", {}).items():
				if room_id in fdata.get("rooms", {}):
					return fdata["rooms"][room_id]
		return None

	# ═══════════════════════════════════════════════════════════════
	# CRAFTING EXPERIMENTATION / DISCOVERY
	# ═══════════════════════════════════════════════════════════════

	def start_experiment(self):
		"""Begin an experimentation session at a crafting station.
		Player selects items from inventory to combine."""
		station = self.get_current_station_type()
		if not station:
			return "There is no crafting station here to experiment at."

		station_name = STATION_NAMES.get(station, "Crafting Station")
		inv = self.engine.player.inventory

		# Get items that could be ingredients
		available_items = []
		for item_id, count in sorted(inv.items()):
			if count > 0:
				available_items.append((item_id, count))

		if len(available_items) < 1:
			return "You don't have any items to experiment with."

		result = "\n" + "═" * 55 + "\n"
		result += f"  🧪 EXPERIMENTATION — {station_name}\n"
		result += "═" * 55 + "\n\n"
		result += "  Select items to combine (2-4 items).\n"
		result += "  Enter item numbers separated by spaces.\n"
		result += "  ⚠️ Failed experiments consume ingredients!\n\n"

		for i, (item_id, count) in enumerate(available_items, 1):
			nice = item_id.replace("_", " ")
			result += f"  {i:>3}. {nice} (x{count})\n"

		result += "\n  Example: '1 3' to combine items 1 and 3\n"
		result += "  Type 'cancel' to stop experimenting.\n"
		result += "═" * 55 + "\n"

		# Store pending experiment state
		self.engine.pending_experiment = {
			"station": station,
			"items": available_items,
		}

		return result

	def handle_experiment_choice(self, cmd):
		"""Handle the player's item selection for experimentation."""
		import random as _rng

		pending = self.engine.pending_experiment
		if not pending:
			return None

		self.engine.pending_experiment = None

		cmd = cmd.strip().lower()
		if cmd in ("cancel", "no", "back", "quit", "exit"):
			return "You step back from the station."

		# Parse item indices
		try:
			indices = [int(x) - 1 for x in cmd.split()]
		except ValueError:
			return "Invalid input. Enter numbers separated by spaces, or 'cancel'."

		available = pending["items"]
		station = pending["station"]

		if len(indices) < 2 or len(indices) > 4:
			return "Combine 2-4 items. Try again with 'experiment'."

		# Validate indices
		selected_items = {}
		for idx in indices:
			if idx < 0 or idx >= len(available):
				return f"Invalid item number: {idx + 1}. Try again."
			item_id, max_count = available[idx]
			selected_items[item_id] = selected_items.get(item_id, 0) + 1
			if selected_items[item_id] > max_count:
				nice = item_id.replace("_", " ")
				return f"You don't have enough {nice}."

		# Check if this combination matches any recipe at this station
		known = self.get_known_recipes()
		match_recipe = None
		for rid, recipe in RECIPE_DATABASE.items():
			if rid in known:
				continue  # Already known
			req_station = recipe["station"]
			if req_station != "any" and req_station != station:
				continue
			# Check ingredients match exactly
			if recipe["ingredients"] == selected_items:
				match_recipe = (rid, recipe)
				break

		if match_recipe:
			rid, recipe = match_recipe
			# SUCCESS! Learn and craft
			self.learn_recipe(rid)

			# Consume ingredients
			inv = self.engine.player.inventory
			for item_id, count in selected_items.items():
				inv[item_id] = inv.get(item_id, 0) - count
				if inv[item_id] <= 0:
					del inv[item_id]

			# Produce result
			result_item, result_count = recipe["result"]
			inv[result_item] = inv.get(result_item, 0) + result_count
			self.engine._inventory_changed = True

			if result_item not in self.engine.item_worth:
				self.engine.item_worth[result_item] = CRAFTED_ITEM_WORTH.get(result_item, 50)

			result = "\n" + "═" * 55 + "\n"
			result += "  🧪✨ DISCOVERY!\n"
			result += "═" * 55 + "\n\n"
			result += f"  You discovered how to make: {recipe['name']}!\n"
			result += f"  {recipe['description']}\n\n"
			nice = result_item.replace("_", " ")
			result += f"  +{result_count} {nice} added to inventory.\n"
			result += f"  📜 Recipe permanently learned!\n\n"

			# XP for discovery
			if PROGRESSION_AVAILABLE:
				try:
					xp_msg = award_xp(self.engine.player, XP_AWARDS.get("discover_recipe", 25), "recipe discovery")
					if xp_msg:
						result += xp_msg + "\n"
				except Exception:
					pass

			result += "═" * 55 + "\n"
			return result
		else:
			# FAILURE — consume ingredients with partial recovery chance
			inv = self.engine.player.inventory
			recovered = []
			for item_id, count in selected_items.items():
				inv[item_id] = inv.get(item_id, 0) - count
				if inv[item_id] <= 0:
					del inv[item_id]
				# 30% chance to recover each ingredient
				for _ in range(count):
					if _rng.random() < 0.30:
						inv[item_id] = inv.get(item_id, 0) + 1
						recovered.append(item_id)

			self.engine._inventory_changed = True

			result = "\n" + "═" * 55 + "\n"
			result += "  🧪💨 EXPERIMENT FAILED\n"
			result += "═" * 55 + "\n\n"
			result += "  The materials fizz and sputter... nothing useful forms.\n"

			items_text = ", ".join(item.replace("_", " ") for item in selected_items)
			result += f"  Lost: {items_text}\n"

			if recovered:
				rec_text = ", ".join(r.replace("_", " ") for r in recovered)
				result += f"  Salvaged: {rec_text}\n"

			# Hint system — check if any recipe partially matches
			hint = self._get_experiment_hint(selected_items, station)
			if hint:
				result += f"\n  💡 {hint}\n"

			result += "\n═" * 55 + "\n"
			return result

	def _get_experiment_hint(self, selected_items, station):
		"""Provide a hint if the selection is close to a real recipe."""
		known = self.get_known_recipes()
		best_match = 0
		best_recipe = None

		for rid, recipe in RECIPE_DATABASE.items():
			if rid in known:
				continue
			req_station = recipe["station"]
			if req_station != "any" and req_station != station:
				continue

			# Count matching ingredients
			match_count = 0
			for item in selected_items:
				if item in recipe["ingredients"]:
					match_count += 1

			total_needed = len(recipe["ingredients"])
			if match_count > best_match and match_count >= 1:
				best_match = match_count
				best_recipe = recipe

		if best_recipe and best_match >= 1:
			total = len(best_recipe["ingredients"])
			if best_match == total - 1:
				# Very close — give a strong hint
				missing = [item for item in best_recipe["ingredients"] if item not in selected_items]
				if missing:
					nice = missing[0].replace("_", " ")
					return f"You feel like you're close... maybe try adding {nice}?"
			elif best_match >= 1:
				return "Some of these materials resonated briefly. You might be on to something..."

		return None
