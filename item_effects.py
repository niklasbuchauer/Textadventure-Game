"""
Item Effects System
==================
Defines usable items with effects (healing, curing, tools).
Consumables are removed after use; tools persist in inventory.
"""

# =====================================================================
# ITEM EFFECTS DATABASE
# =====================================================================
# Each entry: {
#   "type": "consumable" | "tool",
#   "effect": effect_type string,
#   "value": numeric value for the effect (e.g. HP restored),
#   "description": flavor text shown when used,
#   "use_text": what happens when you use it,
#   "requires_context": optional — e.g. "water" for fishing rod
# }
# =====================================================================

ITEM_EFFECTS = {
	# ───── CONSUMABLE: HEALING ─────
	"healing_potion": {
		"type": "consumable",
		"effect": "heal",
		"value": 50,
		"description": "A shimmering red potion that restores vitality.",
		"use_text": "You uncork the healing potion and drink deeply. Warmth spreads through your body as your wounds close.",
	},
	"healing_salve": {
		"type": "consumable",
		"effect": "heal",
		"value": 25,
		"description": "A thick herbal paste that promotes healing.",
		"use_text": "You apply the healing salve to your wounds. It stings briefly, then soothes.",
	},
	"holy_water": {
		"type": "consumable",
		"effect": "heal_and_cure",
		"value": 30,
		"description": "Blessed water that purifies body and soul.",
		"use_text": "You drink the holy water. A warm, golden light washes through you, mending wounds and purging toxins.",
	},
	"mineral_water_flask": {
		"type": "consumable",
		"effect": "heal",
		"value": 10,
		"description": "Refreshing mineral water from a cave spring.",
		"use_text": "You drink the mineral water. It's cool and revitalizing.",
	},
	"ale_mug": {
		"type": "consumable",
		"effect": "heal",
		"value": 5,
		"description": "A mug of hearty tavern ale.",
		"use_text": "You down the ale in one go. Not exactly medicine, but you feel a bit better. And braver.",
	},
	"mushroom": {
		"type": "consumable",
		"effect": "heal",
		"value": 3,
		"description": "A common forest mushroom. Mildly nourishing.",
		"use_text": "You eat the mushroom. It's earthy and chewy. Slightly rejuvenating.",
	},
	"shelf_mushroom": {
		"type": "consumable",
		"effect": "heal",
		"value": 3,
		"description": "A shelf mushroom growing on old trees. Edible.",
		"use_text": "You nibble on the shelf mushroom. Not gourmet, but it's sustenance.",
	},
	"giant_truffle": {
		"type": "consumable",
		"effect": "heal",
		"value": 15,
		"description": "A rare and enormous truffle with restorative properties.",
		"use_text": "You eat the giant truffle. Rich, earthy flavors flood your mouth, and you feel significantly refreshed.",
	},
	"luminous_cap": {
		"type": "consumable",
		"effect": "heal",
		"value": 8,
		"description": "A softly glowing mushroom cap with mild healing properties.",
		"use_text": "You eat the luminous cap. It tastes electric and slightly minty. A warm glow spreads through you.",
	},

	# ───── CONSUMABLE: CURE POISON ─────
	"antidote": {
		"type": "consumable",
		"effect": "cure_poison",
		"value": 0,
		"description": "A carefully prepared antidote that neutralizes most poisons.",
		"use_text": "You drink the antidote. The burning in your veins subsides immediately.",
	},
	"poison_cure": {
		"type": "consumable",
		"effect": "cure_poison",
		"value": 0,
		"description": "A swamp-brewed remedy against venoms and toxins.",
		"use_text": "You gulp down the bitter cure. The poison's grip on your body loosens and fades.",
	},
	"strange_herb": {
		"type": "consumable",
		"effect": "cure_poison",
		"value": 0,
		"description": "A peculiar herb with detoxifying properties.",
		"use_text": "You chew the strange herb. It's intensely bitter, but the poison weakens.",
	},

	# ───── CONSUMABLE: SPECIAL ─────
	"spell_scroll": {
		"type": "consumable",
		"effect": "reveal_traps",
		"value": 0,
		"description": "A magical scroll that reveals hidden dangers.",
		"use_text": "You unroll the spell scroll and read the incantation. The parchment crumbles as magic ripples outward...",
	},
	"enchanted_candle": {
		"type": "consumable",
		"effect": "trap_detection_boost",
		"value": 3,
		"description": "A candle that burns with magical light, revealing hidden things.",
		"use_text": "You light the enchanted candle. Its otherworldly flame illuminates things normally invisible...",
	},
	"prayer_candle": {
		"type": "consumable",
		"effect": "heal",
		"value": 8,
		"description": "A blessed candle from the chapel. Soothes body and spirit.",
		"use_text": "You light the prayer candle and sit in its warm glow. Peace washes over you.",
	},
	"moldy_bread": {
		"type": "consumable",
		"effect": "heal",
		"value": 1,
		"description": "Very old bread. Barely edible, but it's something.",
		"use_text": "You force down the moldy bread. You feel... marginally less hungry.",
	},

	# ───── TOOL: PERSISTENT ITEMS ─────
	"old_spyglass": {
		"type": "tool",
		"effect": "scout",
		"value": 0,
		"description": "An old but functional spyglass. Use it to scout nearby areas.",
		"use_text": "You raise the spyglass to your eye and peer into the distance...",
	},
	"old_fishing_rod": {
		"type": "tool",
		"effect": "fish",
		"value": 0,
		"description": "A battered fishing rod. Still functional near water.",
		"use_text": "You cast the line into the water and wait...",
		"requires_context": "water",
	},
	"torch": {
		"type": "tool",
		"effect": "light",
		"value": 0,
		"description": "A simple torch. Provides light in dark places.",
		"use_text": "You light the torch. Shadows retreat as warm light fills the area.",
	},
	"quality_torch": {
		"type": "tool",
		"effect": "light",
		"value": 0,
		"description": "A well-made torch with a long-lasting flame.",
		"use_text": "You light the quality torch. Its bright, steady flame pushes back the darkness.",
	},
	"faded_map": {
		"type": "tool",
		"effect": "reveal_map",
		"value": 0,
		"description": "An old map showing forgotten paths and hidden places.",
		"use_text": "You study the faded map carefully...",
	},
	"worn_map": {
		"type": "tool",
		"effect": "reveal_map",
		"value": 0,
		"description": "A worn but legible map showing local landmarks.",
		"use_text": "You spread out the worn map and study it...",
	},
	"lockpick_set": {
		"type": "tool",
		"effect": "lockpick",
		"value": 0,
		"description": "A set of lockpicks. Useful for locked chests and disarming traps.",
		"use_text": "You examine your lockpick set. The picks are ready for use.",
	},
	"miner_journal": {
		"type": "tool",
		"effect": "read",
		"value": 0,
		"description": "A miner's journal from the Crystal Caverns.",
		"use_text": "You flip through the miner's journal. The last entries are frantic:\n  'The crystals sing at night. They want us to stay.'\n  'Door won't open. It opened yesterday. Did the cave change?'\n  'Found something deep. Beautiful. Terrible. Don't touch the heart.'",
	},
	"dusty_tome": {
		"type": "tool",
		"effect": "read",
		"value": 0,
		"description": "An ancient book filled with forgotten knowledge.",
		"use_text": "You carefully open the dusty tome. Much is illegible, but fragments remain:\n  '...and the Shadow Sovereign was sealed beneath the crypt...'\n  '...three altars of power, one in each deep place...'\n  '...combine the shards at the forge to unlock...'",
	},
	"intact_tome": {
		"type": "tool",
		"effect": "read",
		"value": 0,
		"description": "A remarkably well-preserved book from the ruined library.",
		"use_text": "You read the intact tome. It describes ancient crafting techniques:\n  'The four forges each resonate with a different energy.'\n  'Crystal bends light into form. Shadow unmakes and remakes.'\n  'Iron endures all. The catacombs forge binds soul to steel.'\n  'Seek the masters: the smith, the hermit, the witch, the priest.'",
	},
	"shadow_tome": {
		"type": "tool",
		"effect": "read",
		"value": 0,
		"description": "A tome bound in solidified shadow. The pages whisper.",
		"use_text": "You open the shadow tome. The text writhes on the page:\n  '...void essence is the key to shadow-forging...'\n  '...the Sovereign's crown holds residual power...'\n  '...combine dread and void at the Shadowforge...'",
	},
	"forgemaster_journal": {
		"type": "tool",
		"effect": "read",
		"value": 0,
		"description": "The journal of the Iron Halls' master smith.",
		"use_text": "You read the forgemaster's journal:\n  'Mithril must be tempered with eternal embers, nothing less.'\n  'The old formula: raw mithril + ember = a blade beyond iron.'\n  'My finest work was forged here. The altar remembers.'",
	},
	"research_notes": {
		"type": "tool",
		"effect": "read",
		"value": 0,
		"description": "Crystal growth research notes from an unknown scientist.",
		"use_text": "You study the research notes:\n  'Diamond and heart-crystal combine at the Forge of Light.'\n  'Resonance crystals amplify enchantments on rings.'\n  'The growth solution accelerates crystalline bonding.'",
	},
}

# Water-adjacent rooms for fishing
WATER_ROOMS = {
	"riverbank", "fishing_spot", "beach", "tidal_caves", "old_dock",
	"lakeside_camp", "foggy_marsh", "deep_swamp", "swamp_edge",
}

# Fishing loot table: (item_name, value, weight)
FISHING_LOOT = [
	("old_boot", 2, 30),
	("small_fish", 5, 35),
	("large_fish", 12, 20),
	("golden_fish", 40, 8),
	("waterlogged_chest", 25, 5),
	("seaweed", 2, 15),
	("ancient_coin", 60, 2),
]

# Scouting data: rooms whose exits can be revealed
# (uses the engine's room data at runtime)


class ItemEffects:
	"""Handles the 'use <item>' command."""

	def __init__(self, engine):
		self.engine = engine

	def use_item(self, item_name):
		"""
		Use an item from the player's inventory.
		Returns a string result message.
		"""
		player = self.engine.player
		if not player:
			return "No game in progress."

		# Normalize item name
		item_name = item_name.strip().lower().replace(" ", "_")

		# Check inventory
		if item_name not in player.inventory or player.inventory[item_name] <= 0:
			return f"You don't have any {item_name.replace('_', ' ')}."

		# Check if item has defined effects
		if item_name not in ITEM_EFFECTS:
			return f"You can't figure out how to use the {item_name.replace('_', ' ')}."

		effect_data = ITEM_EFFECTS[item_name]
		effect_type = effect_data["effect"]
		item_type = effect_data["type"]
		use_text = effect_data.get("use_text", f"You use the {item_name.replace('_', ' ')}.")
		result = use_text + "\n"

		# ─── Context checks ───
		if effect_data.get("requires_context") == "water":
			current_room = player.current_room
			if current_room not in WATER_ROOMS:
				return f"You need to be near water to use the {item_name.replace('_', ' ')}."

		# ─── Apply effect ───
		if effect_type == "heal":
			result += self._apply_heal(effect_data["value"])
		elif effect_type == "heal_and_cure":
			result += self._apply_heal(effect_data["value"])
			result += self._apply_cure_poison()
		elif effect_type == "cure_poison":
			result += self._apply_cure_poison()
		elif effect_type == "reveal_traps":
			result += self._apply_reveal_traps()
		elif effect_type == "trap_detection_boost":
			result += self._apply_trap_boost(effect_data["value"])
		elif effect_type == "scout":
			result += self._apply_scout()
		elif effect_type == "fish":
			result += self._apply_fish()
		elif effect_type == "light":
			result += self._apply_light()
		elif effect_type == "reveal_map":
			result += self._apply_reveal_map()
		elif effect_type == "lockpick":
			result += "Your lockpicks are ready. Use 'disarm' near traps or locked chests."
		elif effect_type == "read":
			pass  # use_text already contains the reading content
		else:
			result += "Nothing seems to happen."

		# ─── Consume if consumable ───
		if item_type == "consumable":
			inv = player.inventory
			if inv.get(item_name, 0) > 1:
				inv[item_name] -= 1
			else:
				inv.pop(item_name, None)
			self.engine._inventory_changed = True

		return result

	def _apply_heal(self, amount):
		"""Heal the player by amount, capped at health_max."""
		stats = self.engine.player.stats
		current = stats.get("health", 100)
		max_hp = stats.get("health_max", 100)
		new_hp = min(current + amount, max_hp)
		healed = new_hp - current
		stats["health"] = new_hp

		if healed <= 0:
			return "  You're already at full health.\n"
		return f"  ❤️ Restored {healed} health. (Health: {new_hp}/{max_hp})\n"

	def _apply_cure_poison(self):
		"""Cure active poison."""
		if self.engine.poison_status:
			self.engine.poison_status = None
			return "  🧪 Poison cured!\n"
		return "  You weren't poisoned.\n"

	def _apply_reveal_traps(self):
		"""Reveal all traps in current room."""
		room_id = self.engine.player.current_room
		raw_room = self._get_raw_dungeon_room(room_id)
		if not raw_room:
			return "  No hidden dangers detected in this area.\n"

		traps = raw_room.get("traps", [])
		if not traps:
			return "  ✨ The magic confirms: this room is safe. No traps present.\n"

		revealed = 0
		for trap in traps:
			if not trap.get("detected") and not trap.get("triggered") and not trap.get("disarmed"):
				trap["detected"] = True
				revealed += 1

		if revealed == 0:
			return "  All traps here were already known.\n"
		return f"  ✨ The scroll's magic reveals {revealed} hidden trap{'s' if revealed != 1 else ''}!\n  Use 'disarm' to attempt disarming them.\n"

	def _apply_trap_boost(self, moves):
		"""Temporarily boost trap detection."""
		state = self.engine.player.state
		current_boost = state.get("trap_detection_boost", 0)
		state["trap_detection_boost"] = current_boost + moves
		return f"  🕯️ Trap detection enhanced for {moves} rooms!\n"

	def _apply_scout(self):
		"""Scout adjacent rooms with the spyglass."""
		room = self.engine.get_room_data(self.engine.player.current_room)
		if not room or not room.exits:
			return "  You can't see much from here.\n"

		lines = ["  Through the spyglass, you can make out:\n"]
		for direction, exit_data in room.exits.items():
			target = exit_data if isinstance(exit_data, str) else exit_data.get("target", "unknown")
			target_room = self.engine.get_room_data(target) if target else None
			if target_room:
				name = target_room.name if hasattr(target_room, "name") else target
				lines.append(f"    {direction.capitalize()}: {name}")
			else:
				lines.append(f"    {direction.capitalize()}: (obscured)")
		return "\n".join(lines) + "\n"

	def _apply_fish(self):
		"""Fish at a water location."""
		import random
		total_weight = sum(w for _, _, w in FISHING_LOOT)
		roll = random.randint(1, total_weight)
		cumulative = 0
		caught_item = None
		caught_value = 0

		for item, value, weight in FISHING_LOOT:
			cumulative += weight
			if roll <= cumulative:
				caught_item = item
				caught_value = value
				break

		if not caught_item:
			caught_item = "small_fish"
			caught_value = 5

		# Add to inventory
		inv = self.engine.player.inventory
		inv[caught_item] = inv.get(caught_item, 0) + 1
		self.engine._inventory_changed = True

		# Register worth
		if caught_item not in self.engine.item_worth:
			self.engine.item_worth[caught_item] = caught_value

		nice_name = caught_item.replace("_", " ")
		if caught_item == "old_boot":
			return f"  🎣 You caught... an old boot. Not exactly a prize.\n  Added {nice_name} to inventory.\n"
		elif caught_item == "golden_fish":
			return f"  🎣 ✨ You caught a golden fish! It shimmers magnificently!\n  Added {nice_name} to inventory.\n"
		elif caught_item == "waterlogged_chest":
			return f"  🎣 You pull up a small waterlogged chest from the depths!\n  Added {nice_name} to inventory.\n"
		elif caught_item == "ancient_coin":
			return f"  🎣 Something heavy on the line... an ancient coin from the riverbed!\n  Added {nice_name} to inventory.\n"
		else:
			return f"  🎣 You caught a {nice_name}!\n  Added {nice_name} to inventory.\n"

	def _apply_light(self):
		"""Light a torch — boosts trap detection for current dungeon visit."""
		state = self.engine.player.state
		state["torch_lit"] = True
		return "  🔥 The area brightens. You'll have better chances of spotting traps.\n"

	def _apply_reveal_map(self):
		"""Reveal adjacent unvisited rooms on the player's visited map."""
		room = self.engine.get_room_data(self.engine.player.current_room)
		if not room or not room.exits:
			return "  The map doesn't show anything useful for this area.\n"

		revealed = 0
		for direction, exit_data in room.exits.items():
			target = exit_data if isinstance(exit_data, str) else exit_data.get("target", "")
			if target and target not in self.engine.player.visited_rooms:
				self.engine.player.visited_rooms.add(target)
				revealed += 1

		if revealed == 0:
			return "  🗺️ You've already visited all nearby areas shown on the map.\n"
		return f"  🗺️ The map reveals {revealed} nearby area{'s' if revealed != 1 else ''} you haven't visited!\n  Check your map to see them.\n"

	def _get_raw_dungeon_room(self, room_id):
		"""Get raw dungeon room data for trap manipulation."""
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

	@staticmethod
	def get_item_info(item_name):
		"""Return effect info for an item, or None if not usable."""
		return ITEM_EFFECTS.get(item_name)

	@staticmethod
	def is_usable(item_name):
		"""Check if an item has a defined use."""
		return item_name in ITEM_EFFECTS
