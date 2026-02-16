"""
NPC Reputation & Memory System
===============================
Tracks player relationships with NPCs:
- Affinity score (-100 to 100) per NPC
- Mood derived from affinity thresholds
- Visit counter & dialogue history
- Gift giving with NPC-specific preferences
- Favor tracking for completed tasks
- Reputation-gated dialogue and shop discounts
"""


# =====================================================================
# MOOD THRESHOLDS
# =====================================================================
MOOD_THRESHOLDS = {
	"hostile":  (-100, -30),
	"wary":     (-30, -5),
	"neutral":  (-5, 20),
	"friendly": (20, 60),
	"devoted":  (60, 100),
}

MOOD_ORDER = ["hostile", "wary", "neutral", "friendly", "devoted"]

MOOD_ICONS = {
	"hostile":  "💀",
	"wary":     "😠",
	"neutral":  "😐",
	"friendly": "😊",
	"devoted":  "💛",
}

# =====================================================================
# GIFT PREFERENCES PER NPC
# =====================================================================
# liked = +5 affinity, neutral = +2, disliked = -3
# Each NPC has a set of liked items, disliked items; anything else is neutral

GIFT_PREFERENCES = {
	"blacksmith": {
		"name": "Tormund",
		"liked": {"iron_ingot", "raw_mithril", "refined_iron", "tempered_steel_ingot",
				  "steel_longsword", "steel_dagger", "mithril_dust", "eternal_ember",
				  "gold_bar"},
		"disliked": {"old_boot", "moldy_bread", "seaweed", "old_bone"},
		"loved": {"raw_mithril", "mithril_blade"},  # +10 affinity
		"reactions": {
			"loved": "Tormund's eyes go wide. \"This is... magnificent! I've dreamt of holding something like this!\"",
			"liked": "Tormund grins appreciatively. \"Fine material! I can always use this.\"",
			"neutral": "Tormund nods politely. \"Thanks, friend. I'll find a use for it.\"",
			"disliked": "Tormund frowns. \"What am I supposed to do with THIS? Get it out of my forge.\"",
		},
	},
	"hermit": {
		"name": "Old Finn",
		"liked": {"strange_herb", "mushroom", "shelf_mushroom", "giant_truffle",
				  "luminous_cap", "glowing_moss", "healing_potion", "mineral_water_flask",
				  "ancient_acorn"},
		"disliked": {"torch", "iron_ingot", "old_boot", "obsidian_shard"},
		"loved": {"giant_truffle", "ancient_acorn"},
		"reactions": {
			"loved": "Finn cradles the gift reverently. \"Do you know how rare this is? Thank you, truly.\"",
			"liked": "Finn smiles warmly. \"Ah, you know what an old hermit values. Thank you.\"",
			"neutral": "Finn accepts your gift. \"Kind of you. I'll put it to good use.\"",
			"disliked": "Finn sighs. \"I appreciate the thought, but this really isn't my sort of thing.\"",
		},
	},
	"priest": {
		"name": "Father Aldric",
		"liked": {"prayer_candle", "holy_water", "healing_potion", "healing_salve",
				  "antidote", "enchanted_candle", "intact_tome", "dusty_tome"},
		"disliked": {"shadow_tome", "dread_idol", "void_heart_fragment", "soul_gem",
					 "lich_crown", "necrotic_dust", "nightmare_essence"},
		"loved": {"holy_water", "prayer_candle"},
		"reactions": {
			"loved": "Father Aldric clasps his hands. \"A gift for the chapel! Your generosity touches my soul.\"",
			"liked": "Father Aldric smiles serenely. \"Thank you, child. This will serve the light.\"",
			"neutral": "Father Aldric accepts your offering. \"Blessings upon you for your kindness.\"",
			"disliked": "Father Aldric recoils. \"Please... keep such dark things away from this holy place!\"",
		},
	},
	"swamp_witch": {
		"name": "Old Martha",
		"liked": {"strange_herb", "marsh_lily", "glowing_moss", "shelf_mushroom",
				  "poison_cure", "swamp_reed", "swamp_moss", "luminous_cap",
				  "spider_silk"},
		"disliked": {"prayer_candle", "holy_water", "torch"},
		"loved": {"spider_silk", "concentrated_void_essence"},
		"reactions": {
			"loved": "Martha's eyes gleam with delight. \"Now THIS is a proper gift! You've got good taste, dearie.\"",
			"liked": "Martha cackles happily. \"Ooh, useful ingredients! You know the way to a witch's heart.\"",
			"neutral": "Martha takes your gift. \"Hmph. Not bad. I'll find something to do with it.\"",
			"disliked": "Martha scowls. \"Are you trying to insult me? Take that sanctimonious rubbish away!\"",
		},
	},
	"bartender": {
		"name": "Bren",
		"liked": {"ale_mug", "golden_fish", "large_fish", "small_fish", "gold_coin",
				  "ancient_coin", "golden_ring"},
		"disliked": {"old_boot", "old_bone", "seaweed", "moldy_bread"},
		"loved": {"golden_fish", "golden_ring"},
		"reactions": {
			"loved": "Bren whistles appreciatively. \"Now THAT'S a gift! The best kind of customer, you are!\"",
			"liked": "Bren grins. \"Much appreciated, friend! Here, this round's on the house.\"",
			"neutral": "Bren nods. \"Thanks! I'll put it behind the bar.\"",
			"disliked": "Bren wrinkles his nose. \"Mate, I run a TAVERN. What am I gonna do with that?\"",
		},
	},
	"patron": {
		"name": "Gareth",
		"liked": {"ale_mug", "broken_arrow", "rusty_sword", "broken_shield",
				  "wolf_pelt", "healing_potion", "iron_ingot"},
		"disliked": {"wildflower", "seashell", "prayer_candle", "mushroom"},
		"loved": {"ale_mug", "warriors_medallion"},
		"reactions": {
			"loved": "Gareth's weathered face breaks into a rare grin. \"You know what a soldier needs. Respect.\"",
			"liked": "Gareth nods approvingly. \"Good kit. Reminds me of the old days.\"",
			"neutral": "Gareth grunts. \"Alright. Thanks, I guess.\"",
			"disliked": "Gareth stares at you flatly. \"Do I LOOK like I need flowers and mushrooms?\"",
		},
	},
	"town_crier": {
		"name": "Herald Pip",
		"liked": {"dusty_tome", "intact_tome", "faded_map", "worn_map",
				  "ancient_coin", "gold_coin", "research_notes"},
		"disliked": {"old_boot", "stick", "moldy_bread", "old_bone"},
		"loved": {"intact_tome", "ancient_coin"},
		"reactions": {
			"loved": "Pip's eyes light up. \"A genuine artifact! This'll make for BRILLIANT announcements!\"",
			"liked": "Pip beams. \"Wonderful! A Herald can always use more source material!\"",
			"neutral": "Pip accepts your gift with a small bow. \"Much appreciated, citizen!\"",
			"disliked": "Pip looks confused. \"I... appreciate the thought? But I don't think I need this.\"",
		},
	},
	"merchant": {
		"name": "Silvia",
		"liked": {"gold_coin", "ancient_coin", "golden_ring", "rare_gemstone",
				  "raw_diamond", "golden_fish", "platinum_bar", "gold_bar",
				  "enchanted_ring"},
		"disliked": {"old_boot", "old_bone", "stick", "seaweed", "moldy_bread"},
		"loved": {"raw_diamond", "platinum_bar"},
		"reactions": {
			"loved": "Silvia's professional facade cracks into genuine delight. \"You have EXCELLENT taste in gifts!\"",
			"liked": "Silvia smiles shrewdly. \"A quality offering. Consider us on good terms.\"",
			"neutral": "Silvia nods. \"I accept. A gesture of goodwill between trading partners.\"",
			"disliked": "Silvia raises an eyebrow. \"I trade in valuables, not... whatever this is.\"",
		},
	},
}


# =====================================================================
# REPUTATION-GATED DIALOGUE NODES
# =====================================================================
# These are injected into NPC dialogue when the player reaches specific
# affinity thresholds. Keys match NPC IDs.

REPUTATION_DIALOGUE = {
	"blacksmith": {
		"friendly_craft": {
			"min_reputation": 20,
			"label": "🔥 [Friendly] Any secret techniques?",
			"node": {
				"text": "Tormund leans in conspiratorially.\n\n\"Since we're friends now... I'll share a finishing "
						"technique my master taught me. When you forge at any altar, listen to the metal sing. "
						"It'll tell you when the temper is right.\n\nAlso — bring me more iron and I'll give "
						"you discount prices on repairs.\"",
				"effects": {"set_state": {"blacksmith_friendly": True}},
				"options": [{"label": "Thanks, Tormund!", "next": "root"}],
			},
		},
		"devoted_lore": {
			"min_reputation": 60,
			"label": "⭐ [Devoted] Tell me about the legendary forge.",
			"node": {
				"text": "Tormund speaks in a hushed voice.\n\n\"There is a legend among smiths — a fifth forge. "
						"Not in any dungeon. They say the Master Smith's spirit guards it still, "
						"somewhere beneath the mountain peak.\n\nI've never found it. But you... you might. "
						"Take this — my best quality steel. You've earned my trust completely.\"",
				"effects": {"give_items": {"tempered_steel_ingot": 3}},
				"options": [{"label": "I won't let you down.", "next": "root"}],
			},
		},
	},
	"hermit": {
		"friendly_herbs": {
			"min_reputation": 20,
			"label": "🌿 [Friendly] Know any rare herb locations?",
			"node": {
				"text": "Finn scratches his chin thoughtfully.\n\n\"Well, since you're a friend... there's a "
						"patch of rare herbs growing behind my cabin. Most folk never notice them. "
						"The ancient grove also has herbs that only bloom when someone trustworthy is near.\n\n"
						"Here — take these. Gathered them this morning.\"",
				"effects": {"give_items": {"strange_herb": 3, "glowing_moss": 2}},
				"options": [{"label": "Thank you, Finn!", "next": "root"}],
			},
		},
		"devoted_wisdom": {
			"min_reputation": 60,
			"label": "⭐ [Devoted] Share your deepest forest secret.",
			"node": {
				"text": "Finn's eyes grow distant.\n\n\"You've shown me real kindness. So I'll tell you what "
						"the trees told me.\n\nThe ancient grove's acorn — the one that won't sprout? "
						"It's not dead. It's sleeping. It waits for someone worthy. Plant it at the "
						"woodland shrine when the time is right.\n\nI never dared. But you... you have "
						"a good heart.\"",
				"effects": {"set_state": {"hermit_secret_known": True}},
				"options": [{"label": "I'll remember that.", "next": "root"}],
			},
		},
	},
	"priest": {
		"friendly_blessing": {
			"min_reputation": 20,
			"label": "🙏 [Friendly] Can you give me a special blessing?",
			"node": {
				"text": "Father Aldric places both hands on your head.\n\n\"You have shown faith through "
						"action, child. I sense the light favors you.\"\n\nA warm glow envelops you.\n\n"
						"\"This blessing will strengthen your spirit against the darkness below.\"",
				"effects": {"give_items": {"holy_water": 2, "prayer_candle": 2}},
				"options": [{"label": "I feel stronger. Thank you, Father.", "next": "root"}],
			},
		},
		"devoted_sacred": {
			"min_reputation": 60,
			"label": "⭐ [Devoted] Teach me about sacred artifacts.",
			"node": {
				"text": "Father Aldric's voice drops to a whisper.\n\n\"There is a relic beneath the "
						"Sunken Catacombs — a blessed chalice that can purify any dark artifact. "
						"The lich on the third floor guards it jealously.\n\nIf you could retrieve it... "
						"bring it here. Together we could undo the Shadow Sovereign's curse entirely.\n\n"
						"I've told no one else this. Only you.\"",
				"effects": {"set_state": {"priest_relic_quest_known": True}},
				"options": [{"label": "I'll find it.", "next": "root"}],
			},
		},
	},
	"swamp_witch": {
		"friendly_potions": {
			"min_reputation": 20,
			"label": "🧪 [Friendly] Got any special brews?",
			"node": {
				"text": "Martha rummages through her shelf and pulls out two murky bottles.\n\n\"For a "
						"friend? Sure. These are my personal stash — stronger than what I teach.\n\n"
						"The purple one clears ANY poison. The green one... well, it tastes horrible but "
						"it'll save your life.\"\n\nShe winks. \"Don't tell the priest.\"",
				"effects": {"give_items": {"antidote": 3, "healing_potion": 2}},
				"options": [{"label": "Your secret's safe with me.", "next": "root"}],
			},
		},
		"devoted_dark": {
			"min_reputation": 60,
			"label": "⭐ [Devoted] Tell me about YOUR past, Martha.",
			"node": {
				"text": "Martha stops stirring. For once, she looks serious.\n\n\"Nobody's asked that in "
						"forty years. Alright... I wasn't always a swamp witch. I was a court alchemist.\n\n"
						"When the Shadow Sovereign rose, I was the one who brewed the binding agent that "
						"sealed it away. Cost me my position, my reputation, my home.\n\n"
						"So I came here. The swamp doesn't judge.\"\n\nShe hands you a vial.\n\n"
						"\"This is the last of that binding agent. If the Sovereign ever stirs again... "
						"you'll need it.\"",
				"effects": {"give_items": {"binding_essence": 1},
							"set_state": {"martha_past_known": True}},
				"options": [{"label": "Thank you for trusting me, Martha.", "next": "root"}],
			},
		},
	},
	"bartender": {
		"friendly_rumors": {
			"min_reputation": 20,
			"label": "🍺 [Friendly] Any rumors for your favorite customer?",
			"node": {
				"text": "Bren pours you a drink and slides it over.\n\n\"On the house. And here's something "
						"I don't share with just anyone:\n\nA traveler came through last week claiming "
						"he found a way into a hidden room in the Crystal Caverns — something about "
						"matching crystal frequencies.\n\nAlso — the fisherman at the old dock? He left "
						"behind some special bait. It's still there if nobody's taken it.\"",
				"effects": {"set_state": {"bren_secret_rumors": True}},
				"options": [{"label": "Cheers, Bren!", "next": "root"}],
			},
		},
	},
	"patron": {
		"friendly_stories": {
			"min_reputation": 20,
			"label": "⚔️ [Friendly] Tell me your best war story.",
			"node": {
				"text": "Gareth's eyes focus, sharp as they must have been twenty years ago.\n\n\"The final "
						"charge. We were outnumbered three to one. The captain fell. I picked up his sword — "
						"this old thing—\"\n\nHe pulls out a battered but serviceable blade.\n\n\"Rallied the "
						"line. We held. Barely.\"\n\nHe pushes something across the table.\n\n\"Here. My old "
						"whetstone. Keep your blade sharp out there.\"",
				"effects": {"give_items": {"iron_ingot": 2}},
				"options": [{"label": "I'm honored, Gareth.", "next": "root"}],
			},
		},
	},
	"town_crier": {
		"friendly_gossip": {
			"min_reputation": 20,
			"label": "📢 [Friendly] Any OFF-record gossip?",
			"node": {
				"text": "Pip looks around nervously and drops his Herald voice.\n\n\"Okay, okay, but "
						"you didn't hear this from me:\n\nThe merchant, Silvia? She's got a map to "
						"something she won't sell. Keeps it in her coat pocket.\n\nAlso, I'm pretty sure "
						"the bartender waters down Thursday's ale. But he gives me free drinks so I keep "
						"quiet about that.\"\n\nHe straightens up. \"HEAR YE! Nothing happened here!\"",
				"effects": {"set_state": {"pip_gossip_known": True}},
				"options": [{"label": "My lips are sealed.", "next": "root"}],
			},
		},
	},
	"merchant": {
		"friendly_deals": {
			"min_reputation": 20,
			"label": "💰 [Friendly] Any special deals for a friend?",
			"node": {
				"text": "Silvia smirks.\n\n\"'Friend' is a strong word. Let's say 'preferred customer.'\n\n"
						"I do have some items I don't put on the regular shelf. Rare stock, you understand. "
						"For someone who's proven they appreciate quality...\"\n\nShe slides you a small "
						"pouch.\n\n\"Consider it a loyalty bonus. Shop with me again soon.\"",
				"effects": {"give_items": {"lockpick_set": 1, "enchanted_candle": 1}},
				"options": [{"label": "Pleasure doing business.", "next": "root"}],
			},
		},
		"devoted_map": {
			"min_reputation": 60,
			"label": "⭐ [Devoted] What about that map in your pocket?",
			"node": {
				"text": "Silvia's eyes widen, then narrow.\n\n\"How did you— Pip. That loudmouth Herald.\"\n\n"
						"She sighs, then reaches into her coat.\n\n\"Fine. You've earned enough trust. "
						"This map shows the location of a hidden cache I found years ago but never had the "
						"nerve to retrieve. It's somewhere in the ancient ruins — behind a false wall.\n\n"
						"Take it. If you survive, we split the profits. Deal?\"",
				"effects": {"give_items": {"faded_map": 1},
							"set_state": {"silvia_cache_known": True}},
				"options": [{"label": "Deal.", "next": "root"}],
			},
		},
	},
}


# =====================================================================
# AFFINITY CHANGE EVENTS
# =====================================================================
# Predefined reasons for affinity changes (besides gifts)

AFFINITY_EVENTS = {
	"first_visit":       2,   # First time talking to an NPC
	"complete_quest":    8,   # Completed a quest for them
	"learn_recipe":      3,   # Learned a recipe from them
	"repeated_visit":    1,   # Visiting again (max once per 5 visits)
}


class NPCRelationship:
	"""Tracks the player's relationship with a single NPC."""

	def __init__(self, npc_id):
		self.npc_id = npc_id
		self.affinity = 0           # -100 to 100
		self.visit_count = 0
		self.gifts_given = {}       # item_id -> count
		self.total_gifts = 0
		self.favors_completed = []  # list of favor/quest IDs
		self.dialogue_seen = set()  # set of dialogue node IDs visited
		self.rep_rewards_claimed = set()  # set of rep dialogue IDs already claimed

	def get_mood(self):
		"""Return the current mood based on affinity thresholds."""
		for mood in MOOD_ORDER:
			low, high = MOOD_THRESHOLDS[mood]
			if low <= self.affinity <= high:
				return mood
		if self.affinity > 100:
			return "devoted"
		return "hostile"

	def modify_affinity(self, delta):
		"""Change affinity, clamping to [-100, 100]."""
		self.affinity = max(-100, min(100, self.affinity + delta))

	def to_dict(self):
		return {
			"npc_id": self.npc_id,
			"affinity": self.affinity,
			"visit_count": self.visit_count,
			"gifts_given": dict(self.gifts_given),
			"total_gifts": self.total_gifts,
			"favors_completed": list(self.favors_completed),
			"dialogue_seen": list(self.dialogue_seen),
			"rep_rewards_claimed": list(self.rep_rewards_claimed),
		}

	@classmethod
	def from_dict(cls, data):
		r = cls(data["npc_id"])
		r.affinity = data.get("affinity", 0)
		r.visit_count = data.get("visit_count", 0)
		r.gifts_given = data.get("gifts_given", {})
		r.total_gifts = data.get("total_gifts", 0)
		r.favors_completed = data.get("favors_completed", [])
		r.dialogue_seen = set(data.get("dialogue_seen", []))
		r.rep_rewards_claimed = set(data.get("rep_rewards_claimed", []))
		return r


class ReputationManager:
	"""Manages all NPC relationships for the player."""

	def __init__(self, engine):
		self.engine = engine
		self.relationships = {}  # npc_id -> NPCRelationship

	def _ensure(self, npc_id):
		"""Ensure a relationship object exists for this NPC."""
		if npc_id not in self.relationships:
			self.relationships[npc_id] = NPCRelationship(npc_id)
		return self.relationships[npc_id]

	def get_relationship(self, npc_id):
		"""Get the relationship object for an NPC (creates if needed)."""
		return self._ensure(npc_id)

	def get_affinity(self, npc_id):
		"""Get the current affinity score for an NPC."""
		return self._ensure(npc_id).affinity

	def get_mood(self, npc_id):
		"""Get the current mood string for an NPC."""
		return self._ensure(npc_id).get_mood()

	def modify_affinity(self, npc_id, delta, reason=""):
		"""Change affinity for an NPC. Returns description of change."""
		rel = self._ensure(npc_id)
		old = rel.affinity
		rel.modify_affinity(delta)
		new = rel.affinity
		old_mood = self._mood_for_value(old)
		new_mood = rel.get_mood()
		result = ""
		if old_mood != new_mood:
			icon = MOOD_ICONS.get(new_mood, "")
			npc_name = GIFT_PREFERENCES.get(npc_id, {}).get("name", npc_id.replace("_", " ").title())
			result = f"\n  {icon} {npc_name}'s attitude toward you changed to: {new_mood.upper()}"
		return result

	def _mood_for_value(self, value):
		"""Get mood for a raw affinity value."""
		for mood in MOOD_ORDER:
			low, high = MOOD_THRESHOLDS[mood]
			if low <= value <= high:
				return mood
		return "devoted" if value > 100 else "hostile"

	def record_visit(self, npc_id):
		"""Record a visit to an NPC. Returns affinity change message."""
		rel = self._ensure(npc_id)
		rel.visit_count += 1
		msg = ""
		if rel.visit_count == 1:
			msg = self.modify_affinity(npc_id, AFFINITY_EVENTS["first_visit"], "first meeting")
		elif rel.visit_count % 5 == 0:
			msg = self.modify_affinity(npc_id, AFFINITY_EVENTS["repeated_visit"], "regular visitor")
		return msg

	def record_dialogue_node(self, npc_id, node_id):
		"""Record that a dialogue node was visited."""
		rel = self._ensure(npc_id)
		rel.dialogue_seen.add(node_id)

	def give_gift(self, npc_id, item_id):
		"""
		Process giving a gift to an NPC.
		Returns (success: bool, message: str).
		"""
		prefs = GIFT_PREFERENCES.get(npc_id)
		if not prefs:
			return False, "This person doesn't accept gifts."

		# Check player has the item
		player = self.engine.player
		if not player or player.inventory.get(item_id, 0) <= 0:
			return False, f"You don't have any {item_id.replace('_', ' ')}."

		# Remove from inventory
		player.inventory[item_id] -= 1
		if player.inventory[item_id] <= 0:
			del player.inventory[item_id]
		self.engine._inventory_changed = True

		rel = self._ensure(npc_id)
		rel.gifts_given[item_id] = rel.gifts_given.get(item_id, 0) + 1
		rel.total_gifts += 1

		# Determine preference level
		loved = prefs.get("loved", set())
		liked = prefs.get("liked", set())
		disliked = prefs.get("disliked", set())
		reactions = prefs.get("reactions", {})

		if item_id in loved:
			delta = 10
			level = "loved"
		elif item_id in liked:
			delta = 5
			level = "liked"
		elif item_id in disliked:
			delta = -3
			level = "disliked"
		else:
			delta = 2
			level = "neutral"

		mood_msg = self.modify_affinity(npc_id, delta)

		nice_name = item_id.replace("_", " ")
		result = f"\n  🎁 You give {nice_name} to {prefs['name']}.\n\n"
		result += reactions.get(level, "They accept your gift.") + "\n"

		# Show affinity change
		direction = "▲" if delta > 0 else "▼"
		result += f"\n  {direction} Affinity {'+'if delta>0 else ''}{delta} (now: {rel.affinity})"
		if mood_msg:
			result += mood_msg
		result += "\n"

		# Notify quest system
		try:
			if hasattr(self.engine, 'quest_manager') and self.engine.quest_manager:
				self.engine.quest_manager.on_item_changed()
		except Exception:
			pass

		return True, result

	def complete_favor(self, npc_id, favor_id):
		"""Record completing a favor/quest for an NPC."""
		rel = self._ensure(npc_id)
		if favor_id not in rel.favors_completed:
			rel.favors_completed.append(favor_id)
			return self.modify_affinity(npc_id, AFFINITY_EVENTS["complete_quest"], "quest completed")
		return ""

	def get_available_rep_dialogue(self, npc_id):
		"""Get reputation-gated dialogue options available for this NPC."""
		rel = self._ensure(npc_id)
		rep_nodes = REPUTATION_DIALOGUE.get(npc_id, {})
		available = []
		for node_id, node_data in rep_nodes.items():
			min_rep = node_data.get("min_reputation", 0)
			if rel.affinity >= min_rep and node_id not in rel.rep_rewards_claimed:
				available.append({
					"node_id": node_id,
					"label": node_data["label"],
					"node": node_data["node"],
				})
		return available

	def claim_rep_reward(self, npc_id, node_id):
		"""Mark a reputation dialogue reward as claimed so it doesn't repeat."""
		rel = self._ensure(npc_id)
		rel.rep_rewards_claimed.add(node_id)

	def get_summary(self, npc_id=None):
		"""Get a formatted reputation summary for a specific NPC."""
		if npc_id is None:
			return self.get_all_summaries()

		rel = self.relationships.get(npc_id)
		if not rel:
			# Try matching by partial name
			for rid, r in self.relationships.items():
				if npc_id in rid:
					npc_id = rid
					rel = r
					break
		if not rel:
			return f"You haven't met anyone matching '{npc_id}'."

		prefs = GIFT_PREFERENCES.get(npc_id, {})
		name = prefs.get("name", npc_id.replace("_", " ").title())
		mood = rel.get_mood()
		icon = MOOD_ICONS.get(mood, "")
		bar_len = 20
		bar_pos = int((rel.affinity + 100) / 200 * bar_len)
		bar_pos = max(0, min(bar_len, bar_pos))
		bar = "░" * bar_pos + "█" + "░" * (bar_len - bar_pos)

		lines = []
		lines.append("\n" + "═" * 55)
		lines.append(f"  {icon} {name} — Relationship")
		lines.append("═" * 55 + "\n")
		lines.append(f"  Mood: {mood.upper():<10s}  Affinity: {rel.affinity:>4d} [{bar}]")
		lines.append(f"  Visits: {rel.visit_count}  |  Gifts: {rel.total_gifts}  |  Favors: {len(rel.favors_completed)}")
		if rel.gifts_given:
			lines.append("\n  Gifts given:")
			for item, count in sorted(rel.gifts_given.items()):
				lines.append(f"    • {item.replace('_', ' ')}: {count}")
		lines.append("")
		return "\n".join(lines)

	def get_all_summaries(self):
		"""Get a formatted reputation summary for all known NPCs."""
		lines = []
		lines.append("\n" + "═" * 55)
		lines.append("  📊 NPC RELATIONSHIPS")
		lines.append("═" * 55 + "\n")

		if not self.relationships:
			lines.append("  You haven't met anyone yet.\n")
			return "\n".join(lines)

		for npc_id, rel in sorted(self.relationships.items()):
			prefs = GIFT_PREFERENCES.get(npc_id, {})
			name = prefs.get("name", npc_id.replace("_", " ").title())
			mood = rel.get_mood()
			icon = MOOD_ICONS.get(mood, "")

			# Affinity bar
			bar_len = 20
			bar_pos = int((rel.affinity + 100) / 200 * bar_len)
			bar_pos = max(0, min(bar_len, bar_pos))
			bar = "░" * bar_pos + "█" + "░" * (bar_len - bar_pos)

			lines.append(f"  {icon} {name}")
			lines.append(f"     Mood: {mood.upper():<10s}  Affinity: {rel.affinity:>4d} [{bar}]")
			lines.append(f"     Visits: {rel.visit_count}  |  Gifts: {rel.total_gifts}"
						 f"  |  Favors: {len(rel.favors_completed)}")
			lines.append("")

		lines.append("─" * 55)
		lines.append("  Tip: Use 'gift <npc> <item>' to improve relationships!")
		lines.append("─" * 55)
		return "\n".join(lines)

	def to_dict(self):
		"""Serialize all relationships for saving."""
		return {npc_id: rel.to_dict() for npc_id, rel in self.relationships.items()}

	def load_from_dict(self, data):
		"""Restore relationships from saved data."""
		self.relationships = {}
		if isinstance(data, dict):
			for npc_id, rel_data in data.items():
				try:
					self.relationships[npc_id] = NPCRelationship.from_dict(rel_data)
				except Exception:
					pass
