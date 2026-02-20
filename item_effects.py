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

	# ───── CONSUMABLE: MANA ─────
	"mana_potion": {
		"type": "consumable",
		"effect": "restore_mana",
		"value": 30,
		"description": "A cobalt-blue potion brimming with arcane energy. Restores 30% of your max mana.",
		"use_text": "You drink the mana potion. Cool azure light flows through you as arcane energy is restored.",
	},
	"major_mana_potion": {
		"type": "consumable",
		"effect": "restore_mana",
		"value": 60,
		"description": "A deep-crystalline flask suffused with potent mana. Restores 60% of your max mana.",
		"use_text": "You drink the major mana potion. A surge of brilliance floods your mind, sharply restoring your magical reserves.",
	},
	"mana_essence": {
		"type": "consumable",
		"effect": "increase_max_mana",
		"value": 10,
		"description": "A crystallised droplet of pure arcane essence. Permanently expands your mana pool by 10.",
		"use_text": "You absorb the mana essence. It dissolves into your soul, widening the channel through which magic flows.",
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

	# ═══════════════════════════════════════════════════════════════════
	# NEW CONSUMABLES - BUFF POTIONS
	# ═══════════════════════════════════════════════════════════════════

	"strength_potion": {
		"type": "consumable",
		"effect": "buff_attack",
		"value": 5,
		"duration": 5,
		"description": "A bubbling red potion that enhances physical strength.",
		"use_text": "You drink the strength potion. Your muscles surge with power!",
	},
	"ironhide_potion": {
		"type": "consumable",
		"effect": "buff_defense",
		"value": 5,
		"duration": 5,
		"description": "A thick gray potion that toughens your skin.",
		"use_text": "You drink the ironhide potion. Your skin hardens like armor!",
	},
	"elixir_of_might": {
		"type": "consumable",
		"effect": "buff_attack",
		"value": 10,
		"duration": 3,
		"description": "A powerful elixir that grants immense strength briefly.",
		"use_text": "You drink the elixir of might. Raw power courses through your veins!",
	},
	"stoneskin_elixir": {
		"type": "consumable",
		"effect": "buff_defense",
		"value": 10,
		"duration": 3,
		"description": "A rare elixir that turns skin to stone briefly.",
		"use_text": "You drink the stoneskin elixir. Your body becomes nearly impervious!",
	},
	"berserker_draught": {
		"type": "consumable",
		"effect": "buff_attack",
		"value": 15,
		"duration": 2,
		"description": "A dangerous brew that grants incredible strength at a cost.",
		"use_text": "You drink the berserker draught. Battle fury overwhelms you!",
	},
	"greater_healing_potion": {
		"type": "consumable",
		"effect": "heal",
		"value": 100,
		"description": "A large, glowing potion that restores significant vitality.",
		"use_text": "You drink the greater healing potion. A surge of life energy courses through you!",
	},
	"lesser_healing_potion": {
		"type": "consumable",
		"effect": "heal",
		"value": 25,
		"description": "A small healing potion for minor wounds.",
		"use_text": "You drink the lesser healing potion. Some of your wounds close.",
	},
	"regeneration_potion": {
		"type": "consumable",
		"effect": "regenerate",
		"value": 5,
		"duration": 5,
		"description": "A green potion that accelerates natural healing.",
		"use_text": "You drink the regeneration potion. Warmth spreads as healing begins.",
	},

	# ═══════════════════════════════════════════════════════════════════
	# NEW CONSUMABLES - RESISTANCE POTIONS
	# ═══════════════════════════════════════════════════════════════════

	"fire_resistance_potion": {
		"type": "consumable",
		"effect": "resist_fire",
		"value": 50,
		"duration": 5,
		"description": "A cool blue potion that protects against fire.",
		"use_text": "You drink the fire resistance potion. You feel protected from heat.",
	},
	"frost_resistance_potion": {
		"type": "consumable",
		"effect": "resist_frost",
		"value": 50,
		"duration": 5,
		"description": "A warm orange potion that protects against cold.",
		"use_text": "You drink the frost resistance potion. You feel protected from cold.",
	},
	"shadow_resistance_potion": {
		"type": "consumable",
		"effect": "resist_shadow",
		"value": 50,
		"duration": 5,
		"description": "A glowing white potion that protects against shadow magic.",
		"use_text": "You drink the shadow resistance potion. Light suffuses your being.",
	},
	"poison_resistance_potion": {
		"type": "consumable",
		"effect": "resist_poison",
		"value": 75,
		"duration": 5,
		"description": "A sickly green potion that protects against toxins.",
		"use_text": "You drink the poison resistance potion. Your blood feels fortified.",
	},

	# ═══════════════════════════════════════════════════════════════════
	# NEW CONSUMABLES - FOOD ITEMS
	# ═══════════════════════════════════════════════════════════════════

	"dried_meat": {
		"type": "consumable",
		"effect": "heal",
		"value": 8,
		"description": "Preserved strips of salted meat. Long lasting.",
		"use_text": "You chew on the dried meat. It's tough but nourishing.",
	},
	"fresh_bread": {
		"type": "consumable",
		"effect": "heal",
		"value": 12,
		"description": "A fresh loaf of hearty bread.",
		"use_text": "You eat the fresh bread. Its warmth fills your belly.",
	},
	"travelers_ration": {
		"type": "consumable",
		"effect": "heal",
		"value": 15,
		"description": "A compact package of mixed provisions.",
		"use_text": "You eat the traveler's ration. Simple but effective sustenance.",
	},
	"hearty_stew": {
		"type": "consumable",
		"effect": "heal",
		"value": 35,
		"description": "A bowl of thick, meaty stew.",
		"use_text": "You eat the hearty stew. Warmth and strength spread through you.",
	},
	"hunters_meal": {
		"type": "consumable",
		"effect": "buff_attack",
		"value": 3,
		"duration": 8,
		"description": "A meal of roasted game meat. Increases combat prowess.",
		"use_text": "You eat the hunter's meal. You feel ready for battle!",
	},
	"fortifying_soup": {
		"type": "consumable",
		"effect": "buff_defense",
		"value": 3,
		"duration": 8,
		"description": "A vegetable soup that strengthens the body.",
		"use_text": "You eat the fortifying soup. Your body feels tougher.",
	},
	"warriors_feast": {
		"type": "consumable",
		"effect": "buff_all",
		"value": 5,
		"duration": 5,
		"description": "A magnificent feast fit for a warrior.",
		"use_text": "You devour the warrior's feast. Power surges through you!",
	},
	"apple": {
		"type": "consumable",
		"effect": "heal",
		"value": 5,
		"description": "A fresh, crisp apple.",
		"use_text": "You eat the apple. It's refreshing and sweet.",
	},
	"cheese_wheel": {
		"type": "consumable",
		"effect": "heal",
		"value": 20,
		"description": "A wheel of aged cheese. Quite filling.",
		"use_text": "You cut slices from the cheese wheel and eat. Rich and satisfying.",
	},

	# ═══════════════════════════════════════════════════════════════════
	# NEW CONSUMABLES - SCROLLS
	# ═══════════════════════════════════════════════════════════════════

	"scroll_of_protection": {
		"type": "consumable",
		"effect": "buff_defense",
		"value": 8,
		"duration": 4,
		"description": "A magical scroll inscribed with protective runes.",
		"use_text": "You read the scroll of protection. A shield of light surrounds you!",
	},
	"scroll_of_strength": {
		"type": "consumable",
		"effect": "buff_attack",
		"value": 8,
		"duration": 4,
		"description": "A magical scroll inscribed with empowering runes.",
		"use_text": "You read the scroll of strength. Magic enhances your might!",
	},
	"scroll_of_insight": {
		"type": "consumable",
		"effect": "reveal_traps",
		"value": 0,
		"description": "A magical scroll that reveals hidden dangers.",
		"use_text": "You read the scroll of insight. Hidden truths are revealed!",
	},
	"scroll_of_escape": {
		"type": "consumable",
		"effect": "escape_combat",
		"value": 100,
		"description": "A scroll that guarantees escape from combat.",
		"use_text": "You read the scroll of escape. Reality bends and you vanish!",
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
		# New buff effects
		elif effect_type == "buff_attack":
			result += self._apply_buff("attack", effect_data["value"], effect_data.get("duration", 5))
		elif effect_type == "buff_defense":
			result += self._apply_buff("defense", effect_data["value"], effect_data.get("duration", 5))
		elif effect_type == "buff_all":
			result += self._apply_buff("attack", effect_data["value"], effect_data.get("duration", 5))
			result += self._apply_buff("defense", effect_data["value"], effect_data.get("duration", 5))
		elif effect_type == "regenerate":
			result += self._apply_regenerate(effect_data["value"], effect_data.get("duration", 5))
		elif effect_type in ("resist_fire", "resist_frost", "resist_shadow", "resist_poison"):
			resist_type = effect_type.replace("resist_", "")
			result += self._apply_resistance(resist_type, effect_data["value"], effect_data.get("duration", 5))
		elif effect_type == "restore_mana":
			result += self._apply_restore_mana(effect_data["value"])
		elif effect_type == "increase_max_mana":
			result += self._apply_increase_max_mana(int(effect_data["value"]))
		elif effect_type == "escape_combat":
			result += self._apply_escape_combat()
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

	def _apply_restore_mana(self, percent):
		"""Restore percent% of max_mana."""
		stats = self.engine.player.stats
		max_mana = stats.get("max_mana", 0)
		if max_mana == 0:
			return "  You have no mana pool to restore.\n"
		restore_amt = max(1, int(max_mana * percent / 100))
		old_mana = stats.get("mana", 0)
		new_mana = min(old_mana + restore_amt, max_mana)
		actual = new_mana - old_mana
		stats["mana"] = new_mana
		if actual <= 0:
			return "  Your mana is already full.\n"
		return f"  💙 Restored {actual} MP. (Mana: {new_mana}/{max_mana})\n"

	def _apply_increase_max_mana(self, amount):
		"""Permanently increase max_mana and current mana by amount."""
		stats = self.engine.player.stats
		max_mana = stats.get("max_mana", 0)
		new_max = max_mana + amount
		stats["max_mana"] = new_max
		stats["mana"] = min(stats.get("mana", 0) + amount, new_max)
		return f"  ✨ Max Mana permanently increased by {amount}! (Mana: {stats['mana']}/{new_max})\n"

	def _apply_cure_poison(self):
		"""Cure active poison."""
		if self.engine.poison_status:
			self.engine.poison_status = None
			return "  🧪 Poison cured!\n"
		return "  You weren't poisoned.\n"

	def _apply_buff(self, stat_type, value, duration):
		"""Apply a temporary stat buff."""
		state = self.engine.player.state
		buffs = state.setdefault("active_buffs", {})
		
		# Stack with existing buff or create new
		buff_key = f"buff_{stat_type}"
		if buff_key in buffs:
			# Extend duration if new buff is stronger or equal
			existing = buffs[buff_key]
			if value >= existing.get("value", 0):
				buffs[buff_key] = {"value": value, "duration": duration}
				return f"  ⬆️ {stat_type.title()} buff refreshed: +{value} for {duration} turns!\n"
			else:
				return f"  ⬆️ Current {stat_type} buff is stronger. Duration extended.\n"
		else:
			buffs[buff_key] = {"value": value, "duration": duration}
			return f"  ⬆️ {stat_type.title()} +{value} for {duration} turns!\n"

	def _apply_regenerate(self, heal_per_turn, duration):
		"""Apply a heal-over-time effect."""
		state = self.engine.player.state
		buffs = state.setdefault("active_buffs", {})
		buffs["regeneration"] = {"value": heal_per_turn, "duration": duration}
		return f"  💚 Regeneration active: +{heal_per_turn} HP per turn for {duration} turns!\n"

	def _apply_resistance(self, resist_type, value, duration):
		"""Apply elemental resistance."""
		state = self.engine.player.state
		buffs = state.setdefault("active_buffs", {})
		buffs[f"resist_{resist_type}"] = {"value": value, "duration": duration}
		return f"  🛡️ {resist_type.title()} resistance +{value}% for {duration} turns!\n"

	def _apply_escape_combat(self):
		"""Guarantee escape from combat."""
		if hasattr(self.engine, 'combat') and self.engine.combat:
			# Set a flag that guarantees escape
			self.engine.player.state["guaranteed_escape"] = True
			return "  ✨ You feel ready to vanish at will. Use 'run' to escape!\n"
		return "  You're not in combat.\n"

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
