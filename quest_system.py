"""
Quest & Journal System
======================
Structured quests with objectives, rewards, and NPC integration.
Supports:
- Multi-objective quests (kill, collect, visit, talk)
- Quest chains (completing one unlocks the next)
- Progress tracking with journal UI
- NPC quest givers and turn-in
- XP and item rewards on completion
"""

# Progression integration
try:
	from progression_system import award_xp, XP_AWARDS
	PROGRESSION_AVAILABLE = True
except ImportError:
	PROGRESSION_AVAILABLE = False


# =====================================================================
# QUEST DATABASE
# =====================================================================
# Each quest definition:
#   id:            unique string identifier
#   name:          display name
#   giver:         NPC id who gives the quest
#   turn_in:       NPC id who completes the quest (often same as giver)
#   description:   flavor text shown in journal
#   objectives:    list of Objective dicts (see below)
#   rewards:       dict with xp, gold, items
#   prerequisite:  quest_id that must be completed first (None = always available)
#   chain_next:    quest_id to auto-offer after completing this one (None = standalone)
#   level_req:     minimum player level (default 1)
#   dialogue:      dict of dialogue node overrides for giver NPC
#
# Objective types:
#   kill:    {"type": "kill",    "target": "<enemy_name>",  "count": N, "description": "..."}
#   collect: {"type": "collect", "item": "<item_name>",     "count": N, "description": "..."}
#   visit:   {"type": "visit",  "room": "<room_id>",       "description": "..."}
#   talk:    {"type": "talk",   "npc": "<npc_id>",          "description": "..."}
# =====================================================================

QUEST_DATABASE = {
	# ── Tutorial Campaign: Multi-Quest Onboarding ─────────────────────
	"welcome_to_havenbrook": {
		"id": "welcome_to_havenbrook",
		"name": "Welcome to Havenbrook",
		"giver": "tutorial_guide",
		"turn_in": "tutorial_guide",
		"description": (
			"Follow Rowan into Havenbrook, visit the town's key services, and return with your first report."
		),
		"objectives": [
			{
				"type": "visit",
				"room": "village_square",
				"description": "Reach Havenbrook Village Square",
			},
			{
				"type": "talk",
				"npc": "tutorial_guide",
				"description": "Meet the tutorial guide",
			},
			{
				"type": "visit",
				"room": "village_shop",
				"description": "Visit the village shop",
			},
			{
				"type": "visit",
				"room": "village_blacksmith",
				"description": "Visit the blacksmith",
			},
		],
		"rewards": {"xp": 25, "gold": 0, "items": {}},
		"prerequisite": None,
		"chain_next": "tutorial_trade_routes",
		"level_req": 1,
		"tutorial_only": True,
	},

	"tutorial_trade_routes": {
		"id": "tutorial_trade_routes",
		"name": "Trade Routes",
		"giver": "merchant",
		"turn_in": "merchant",
		"description": (
			"Silvia will teach you shop fundamentals. Accept the task, use shop commands, then report back."
		),
		"objectives": [
			{
				"type": "talk",
				"npc": "merchant",
				"description": "Speak with Silvia the merchant",
			},
			{
				"type": "visit",
				"room": "village_shop",
				"description": "Step inside the village shop",
			},
		],
		"rewards": {"xp": 30, "gold": 15, "items": {}},
		"prerequisite": "welcome_to_havenbrook",
		"chain_next": "tutorial_bank_basics",
		"level_req": 1,
		"tutorial_only": True,
	},

	"tutorial_bank_basics": {
		"id": "tutorial_bank_basics",
		"name": "Bank Basics",
		"giver": "banker",
		"turn_in": "banker",
		"description": (
			"Learn how to check balance and move gold safely with the Bank of Estoria."
		),
		"objectives": [
			{
				"type": "visit",
				"room": "bank_of_estoria",
				"description": "Visit the Bank of Estoria",
			},
			{
				"type": "talk",
				"npc": "banker",
				"description": "Speak with the banker",
			},
		],
		"rewards": {"xp": 35, "gold": 10, "items": {}},
		"prerequisite": "tutorial_trade_routes",
		"chain_next": "tutorial_combat_drill",
		"level_req": 1,
		"tutorial_only": True,
	},

	"tutorial_combat_drill": {
		"id": "tutorial_combat_drill",
		"name": "Combat Drill",
		"giver": "patron",
		"turn_in": "patron",
		"description": (
			"Run a safe combat drill at the training grounds and prove you can fight with intent."
		),
		"objectives": [
			{
				"type": "visit",
				"room": "village_training_grounds",
				"description": "Reach the training grounds",
			},
			{
				"type": "kill",
				"target": "Training Dummy",
				"count": 1,
				"description": "Defeat the training dummy",
			},
		],
		"rewards": {"xp": 40, "gold": 20, "items": {}},
		"prerequisite": "tutorial_bank_basics",
		"chain_next": "tutorial_recovery_check",
		"level_req": 1,
		"tutorial_only": True,
		"spawn_visible_enemy": {
			"room": "village_training_grounds",
			"enemy_id": "training_dummy",
			"persistent": True,
			"reset_on_engage": True,
		},
	},

	"tutorial_recovery_check": {
		"id": "tutorial_recovery_check",
		"name": "Recovery Check",
		"giver": "priest",
		"turn_in": "priest",
		"description": (
			"Father Aldric asks you to review your active objectives and return with your notes."
		),
		"objectives": [
			{
				"type": "visit",
				"room": "chapel",
				"description": "Visit the chapel",
			},
			{
				"type": "talk",
				"npc": "priest",
				"description": "Speak with Father Aldric",
			},
		],
		"rewards": {"xp": 30, "gold": 10, "items": {"prayer_candle": 1}},
		"prerequisite": "tutorial_combat_drill",
		"chain_next": "tutorial_crafting_kickoff",
		"level_req": 1,
		"tutorial_only": True,
	},

	"tutorial_crafting_kickoff": {
		"id": "tutorial_crafting_kickoff",
		"name": "Forgemaster's Starter",
		"giver": "blacksmith",
		"turn_in": "blacksmith",
		"description": (
			"Tormund wants proof you can use the forge and gather a basic ingot."
		),
		"objectives": [
			{
				"type": "visit",
				"room": "village_blacksmith",
				"description": "Return to Tormund's forge",
			},
			{
				"type": "collect",
				"item": "iron_ingot",
				"count": 1,
				"description": "Obtain 1 iron ingot",
			},
		],
		"rewards": {"xp": 40, "gold": 20, "items": {"iron_dagger": 1}},
		"prerequisite": "tutorial_recovery_check",
		"chain_next": "tutorial_graduation",
		"level_req": 1,
		"tutorial_only": True,
	},

	"tutorial_graduation": {
		"id": "tutorial_graduation",
		"name": "Graduation Checklist",
		"giver": "tutorial_guide",
		"turn_in": "tutorial_guide",
		"description": (
			"Return to Rowan and demonstrate that you can inspect progression and save your game."
		),
		"objectives": [
			{
				"type": "talk",
				"npc": "tutorial_guide",
				"description": "Report back to Elder Rowan",
			},
		],
		"rewards": {"xp": 60, "gold": 35, "items": {"health_potion": 2}},
		"prerequisite": "tutorial_crafting_kickoff",
		"chain_next": None,
		"level_req": 1,
		"tutorial_only": True,
		"tutorial_final": True,
	},

	# ── Chain 1: Blacksmith's Needs (Tormund) ──────────────────────────
	"blacksmith_errand": {
		"id": "blacksmith_errand",
		"name": "The Blacksmith's Errand",
		"giver": "blacksmith",
		"turn_in": "blacksmith",
		"description": (
			"Tormund the blacksmith needs iron ingots to keep his forge running. "
			"He's asked you to gather some from the surrounding area or the Iron Halls dungeon."
		),
		"objectives": [
			{
				"type": "collect",
				"item": "iron_ingot",
				"count": 3,
				"description": "Collect 3 iron ingots",
			},
		],
		"rewards": {"xp": 75, "gold": 50, "items": {"steel_dagger": 1}, "skill_points": 1},
		"prerequisite": None,
		"chain_next": "blacksmith_masterwork",
		"level_req": 1,
	},
	"blacksmith_masterwork": {
		"id": "blacksmith_masterwork",
		"name": "Masterwork Ambition",
		"giver": "blacksmith",
		"turn_in": "blacksmith",
		"description": (
			"Tormund wants to create a masterwork weapon but needs rare materials. "
			"Venture into the Iron Halls and retrieve a mithril shard from the deep floors."
		),
		"objectives": [
			{
				"type": "collect",
				"item": "raw_mithril",
				"count": 1,
				"description": "Find raw mithril in the Iron Halls",
			},
			{
				"type": "collect",
				"item": "eternal_ember",
				"count": 1,
				"description": "Obtain an eternal ember",
			},
		],
		"rewards": {"xp": 200, "gold": 100, "items": {"mithril_blade": 1}, "skill_points": 2},
		"prerequisite": "blacksmith_errand",
		"chain_next": None,
		"level_req": 5,
	},

	# ── Chain 2: Swamp Witch's Request (Old Martha) ────────────────────
	"swamp_gathering": {
		"id": "swamp_gathering",
		"name": "Witch's Brew",
		"giver": "swamp_witch",
		"turn_in": "swamp_witch",
		"description": (
			"Old Martha the Swamp Witch needs rare herbs and fungi from the "
			"swamp and surrounding areas for one of her concoctions."
		),
		"objectives": [
			{
				"type": "collect",
				"item": "swamp_moss",
				"count": 3,
				"description": "Gather 3 bundles of swamp moss",
			},
			{
				"type": "collect",
				"item": "glowing_mushroom",
				"count": 2,
				"description": "Find 2 glowing mushrooms",
			},
		],
		"rewards": {"xp": 100, "gold": 30, "items": {"greater_healing_potion": 2, "antidote": 2}, "skill_points": 1},
		"prerequisite": None,
		"chain_next": None,
		"level_req": 2,
	},

	# ── Chain 3: Hermit's Exploration (Old Finn) ──────────────────────
	"hermit_explore": {
		"id": "hermit_explore",
		"name": "The Hermit's Curiosity",
		"giver": "hermit",
		"turn_in": "hermit",
		"description": (
			"Old Finn the Hermit has heard rumours of ancient ruins deep in the forest. "
			"He wants you to explore several remote locations and report what you find."
		),
		"objectives": [
			{
				"type": "visit",
				"room": "dungeon_ruins_entrance",
				"description": "Find the ancient ruins entrance",
			},
			{
				"type": "visit",
				"room": "open_crypt",
				"description": "Visit the open crypt in the graveyard",
			},
			{
				"type": "visit",
				"room": "mountain_peak",
				"description": "Reach the mountain peak",
			},
		],
		"rewards": {"xp": 120, "gold": 40, "items": {"spyglass": 1}, "skill_points": 1},
		"prerequisite": None,
		"chain_next": "hermit_shadow",
		"level_req": 2,
	},
	"hermit_shadow": {
		"id": "hermit_shadow",
		"name": "Into the Shadow Depths",
		"giver": "hermit",
		"turn_in": "hermit",
		"description": (
			"Old Finn is fascinated by the Shadow Depths beneath the crypt. "
			"He wants you to brave the dungeon, defeat its guardian, and return."
		),
		"objectives": [
			{
				"type": "kill",
				"target": "Shadow Lord",
				"count": 1,
				"description": "Defeat the Shadow Lord in the Shadow Depths",
			},
		],
		"rewards": {"xp": 300, "gold": 150, "items": {"enchanted_candle": 1}, "skill_points": 3},
		"prerequisite": "hermit_explore",
		"chain_next": None,
		"level_req": 5,
	},

	# ── Chain 4: Priest's Blessing (Father Aldric) ────────────────────
	"priest_undead": {
		"id": "priest_undead",
		"name": "Cleansing the Graveyard",
		"giver": "priest",
		"turn_in": "priest",
		"description": (
			"Father Aldric is troubled by restless undead in the graveyard. "
			"He has asked you to venture there and put the tormented souls to rest."
		),
		"objectives": [
			{
				"type": "kill",
				"target": "Skeleton",
				"count": 5,
				"description": "Destroy 5 skeletons",
			},
			{
				"type": "kill",
				"target": "Ghost",
				"count": 3,
				"description": "Banish 3 ghosts",
			},
		],
		"rewards": {"xp": 150, "gold": 60, "items": {"blessed_water": 2}, "skill_points": 2},
		"prerequisite": None,
		"chain_next": None,
		"level_req": 3,
	},

	# ── Chain 5: War Veteran's Trial (Gareth) ─────────────────────────
	"veteran_trial": {
		"id": "veteran_trial",
		"name": "The Veteran's Trial",
		"giver": "war_veteran",
		"turn_in": "war_veteran",
		"description": (
			"Gareth the War Veteran wants to test your combat skill. "
			"Prove yourself by defeating powerful enemies across multiple dungeons."
		),
		"objectives": [
			{
				"type": "kill",
				"target": "any_mini_boss",
				"count": 2,
				"description": "Defeat 2 mini-bosses in any dungeon",
			},
			{
				"type": "kill",
				"target": "any_boss",
				"count": 1,
				"description": "Defeat a dungeon boss",
			},
		],
		"rewards": {"xp": 400, "gold": 200, "items": {"warriors_medallion": 1}, "skill_points": 5},
		"prerequisite": None,
		"chain_next": None,
		"level_req": 6,
	},

	# ── Chain 6: Bartender's Favour (Bren) ────────────────────────────
	"tavern_delivery": {
		"id": "tavern_delivery",
		"name": "A Round for the House",
		"giver": "bartender",
		"turn_in": "bartender",
		"description": (
			"Bren the bartender needs fresh fish for tonight's special. "
			"He's heard the river has some fine catches — bring him a few."
		),
		"objectives": [
			{
				"type": "collect",
				"item": "fresh_fish",
				"count": 3,
				"description": "Catch 3 fresh fish from the river",
			},
		],
		"rewards": {"xp": 50, "gold": 30, "items": {"healing_potion": 2}, "skill_points": 1},
		"prerequisite": None,
		"chain_next": "tavern_archaeologists_gambit",
		"level_req": 1,
	},
	"tavern_archaeologists_gambit": {
		"id": "tavern_archaeologists_gambit",
		"name": "Archaeologist's Gambit",
		"giver": "bartender",
		"turn_in": "hermit",
		"description": (
			"Bren heard of a scholar searching old ruins. Prepare for the trip by bringing fish and iron, "
			"then scout the crypt and report your findings to Old Finn."
		),
		"objectives": [
			{
				"type": "collect",
				"item": "fresh_fish",
				"count": 2,
				"description": "Secure 2 fresh fish for the road",
			},
			{
				"type": "collect",
				"item": "iron_ingot",
				"count": 2,
				"description": "Bring 2 iron ingots for field gear",
			},
			{
				"type": "visit",
				"room": "open_crypt",
				"description": "Scout the open crypt entrance",
			},
			{
				"type": "talk",
				"npc": "hermit",
				"description": "Report to Old Finn",
			},
		],
		"rewards": {"xp": 180, "gold": 90, "items": {"quality_torch": 1, "healing_potion": 2}, "skill_points": 2},
		"prerequisite": "tavern_delivery",
		"chain_next": "tavern_shadow_recovery",
		"level_req": 3,
	},
	"tavern_shadow_recovery": {
		"id": "tavern_shadow_recovery",
		"name": "Shadow Recovery Run",
		"giver": "hermit",
		"turn_in": "blacksmith",
		"description": (
			"Old Finn needs proof from the depths. Defeat a mini-boss, recover ancient coins, "
			"and deliver the haul to Tormund for analysis."
		),
		"objectives": [
			{
				"type": "kill",
				"target": "any_mini_boss",
				"count": 1,
				"description": "Defeat 1 mini-boss",
			},
			{
				"type": "collect",
				"item": "ancient_coin",
				"count": 2,
				"description": "Recover 2 ancient coins",
			},
			{
				"type": "talk",
				"npc": "blacksmith",
				"description": "Deliver findings to Tormund",
			},
		],
		"rewards": {"xp": 320, "gold": 140, "items": {"masterwork_shield": 1}, "skill_points": 3},
		"prerequisite": "tavern_archaeologists_gambit",
		"chain_next": None,
		"level_req": 5,
	},

	# ── Chain 7: Merchant's Request (Silvia) ──────────────────────────
	"merchant_gems": {
		"id": "merchant_gems",
		"name": "Precious Cargo",
		"giver": "merchant",
		"turn_in": "merchant",
		"description": (
			"Silvia the Merchant is looking for rare crystals from the Crystal Caverns. "
			"She'll pay handsomely for any you can find."
		),
		"objectives": [
			{
				"type": "collect",
				"item": "crystal_shard",
				"count": 5,
				"description": "Collect 5 crystal shards",
			},
		],
		"rewards": {"xp": 100, "gold": 120, "items": {}, "skill_points": 2},
		"prerequisite": None,
		"chain_next": None,
		"level_req": 3,
	},

	# ── Chain 8: Town Crier's Plea (Herald Pip) ───────────────────────
	"herald_news": {
		"id": "herald_news",
		"name": "Spread the Word",
		"giver": "herald",
		"turn_in": "herald",
		"description": (
			"Herald Pip wants someone brave enough to scout the dungeon entrances "
			"and report back about what threats lurk nearby."
		),
		"objectives": [
			{
				"type": "visit",
				"room": "dungeon_forest_entrance",
				"description": "Scout the Crystal Caverns entrance",
			},
			{
				"type": "visit",
				"room": "dungeon_mountain_entrance",
				"description": "Scout the Iron Halls entrance",
			},
			{
				"type": "visit",
				"room": "open_crypt",
				"description": "Scout the Shadow Depths entrance",
			},
		],
		"rewards": {"xp": 80, "gold": 45, "items": {"torch": 3}, "skill_points": 1},
		"prerequisite": None,
		"chain_next": None,
		"level_req": 1,
	},
}


# =====================================================================
# QUEST STATE TRACKING
# =====================================================================

class QuestState:
	"""Tracks a single quest's current progress and status."""

	STATUS_AVAILABLE = "available"     # Can be accepted
	STATUS_ACTIVE = "active"           # Currently in progress
	STATUS_COMPLETE = "complete"       # Objectives done, ready to turn in
	STATUS_TURNED_IN = "turned_in"     # Rewards collected, quest finished

	def __init__(self, quest_id):
		self.quest_id = quest_id
		self.status = self.STATUS_AVAILABLE
		# progress tracks per-objective completion: {obj_index: current_count}
		self.progress = {}

	def to_dict(self):
		return {
			"quest_id": self.quest_id,
			"status": self.status,
			"progress": {str(k): v for k, v in self.progress.items()},
		}

	@classmethod
	def from_dict(cls, data):
		qs = cls(data["quest_id"])
		qs.status = data.get("status", cls.STATUS_AVAILABLE)
		qs.progress = {int(k): v for k, v in data.get("progress", {}).items()}
		return qs


# =====================================================================
# QUEST MANAGER
# =====================================================================

class QuestManager:
	"""Central quest logic — accepts/tracks/completes quests and checks triggers."""

	def __init__(self, engine):
		self.engine = engine
		# quest_id -> QuestState
		self.quests = {}

	def _get_game_feel_intensity(self):
		"""Resolve gameplay intensity for journal/quest text verbosity."""
		if hasattr(self.engine, "get_game_feel_intensity"):
			return self.engine.get_game_feel_intensity()
		level = "normal"
		try:
			cfg = getattr(getattr(self.engine, "gui", None), "config", None)
			if isinstance(cfg, dict):
				gameplay = cfg.get("gameplay", {})
				if isinstance(gameplay, dict):
					level = gameplay.get("game_feel_intensity", "normal")
		except Exception:
			level = "normal"
		level = str(level or "normal").strip().lower()
		if level not in ("low", "normal", "high"):
			return "normal"
		return level

	# ── Serialization ────────────────────────────────────────────────

	def to_dict(self):
		return {qid: qs.to_dict() for qid, qs in self.quests.items()}

	def load_from_dict(self, data):
		"""Restore quest states from save data."""
		self.quests = {}
		if not data:
			return
		for qid, qdata in data.items():
			try:
				self.quests[qid] = QuestState.from_dict(qdata)
			except Exception:
				pass

	# ── Quest availability ───────────────────────────────────────────

	def get_available_quests(self, npc_id=None):
		"""Return list of quest definitions available to accept, optionally filtered by NPC."""
		available = []
		player = self.engine.player
		level = player.stats.get("level", 1) if player else 1

		for qid, qdef in QUEST_DATABASE.items():
			# Already known?
			if qid in self.quests:
				continue
			# Level requirement
			if level < qdef.get("level_req", 1):
				continue
			# Prerequisite
			prereq = qdef.get("prerequisite")
			if prereq:
				prereq_state = self.quests.get(prereq)
				if not prereq_state or prereq_state.status != QuestState.STATUS_TURNED_IN:
					continue
			# NPC filter
			if npc_id and qdef.get("giver") != npc_id:
				continue
			available.append(qdef)
		return available

	def get_active_quests(self):
		"""Return list of (quest_def, quest_state) for all active quests."""
		result = []
		for qid, qs in self.quests.items():
			if qs.status in (QuestState.STATUS_ACTIVE, QuestState.STATUS_COMPLETE):
				qdef = QUEST_DATABASE.get(qid)
				if qdef:
					result.append((qdef, qs))
		return result

	def get_completed_quests(self):
		"""Return list of quest_defs that are turned in."""
		result = []
		for qid, qs in self.quests.items():
			if qs.status == QuestState.STATUS_TURNED_IN:
				qdef = QUEST_DATABASE.get(qid)
				if qdef:
					result.append(qdef)
		return result

	# ── Accept / progress / complete ─────────────────────────────────

	def accept_quest(self, quest_id):
		"""Accept a quest. Returns display text."""
		qdef = QUEST_DATABASE.get(quest_id)
		if not qdef:
			return "Quest not found."

		if quest_id in self.quests:
			existing = self.quests[quest_id]
			if existing.status == QuestState.STATUS_ACTIVE:
				return f"You've already accepted \"{qdef['name']}\"."
			if existing.status == QuestState.STATUS_TURNED_IN:
				return f"You've already completed \"{qdef['name']}\"."

		qs = QuestState(quest_id)
		qs.status = QuestState.STATUS_ACTIVE
		# Initialize progress counters
		for i, obj in enumerate(qdef.get("objectives", [])):
			if obj["type"] in ("kill", "collect"):
				qs.progress[i] = 0
			elif obj["type"] in ("visit", "talk"):
				qs.progress[i] = 0  # 0 = not done, 1 = done
		self.quests[quest_id] = qs

		# Check if any objectives are already satisfied
		self._check_all_objectives(quest_id)
		spawn_notice = self._spawn_visible_enemy_for_quest(qdef)

		result = "\n" + "═" * 55 + "\n"
		result += f"  📜 QUEST ACCEPTED: {qdef['name']}\n"
		result += "═" * 55 + "\n\n"
		result += f"  {qdef['description']}\n\n"
		result += "  Objectives:\n"
		for i, obj in enumerate(qdef["objectives"]):
			progress = qs.progress.get(i, 0)
			count = obj.get("count", 1)
			done = progress >= count
			mark = "✅" if done else "☐"
			if obj["type"] in ("kill", "collect"):
				result += f"    {mark} {obj['description']} ({progress}/{count})\n"
			else:
				result += f"    {mark} {obj['description']}\n"
		if spawn_notice:
			result += f"\n  {spawn_notice}\n"
		result += "\n  Type 'journal' to track your quests.\n"
		return result

	def turn_in_quest(self, quest_id):
		"""Turn in a completed quest for rewards. Returns display text."""
		qdef = QUEST_DATABASE.get(quest_id)
		qs = self.quests.get(quest_id)
		if not qdef or not qs:
			return "Quest not found."
		if qs.status != QuestState.STATUS_COMPLETE:
			return f"\"{qdef['name']}\" is not ready to turn in yet."

		if qdef.get("tutorial_only"):
			try:
				import tutorial_system
				unmet = tutorial_system.get_unmet_tutorial_requirements(self.engine, quest_id)
				if unmet:
					return tutorial_system.format_tutorial_requirement_reminder(self.engine, quest_id, unmet)
			except Exception:
				pass
		feel = self._get_game_feel_intensity()

		qs.status = QuestState.STATUS_TURNED_IN
		rewards = qdef.get("rewards", {})

		if feel == "low":
			result = f"\n🏆 QUEST COMPLETE: {qdef['name']}\n\n"
		elif feel == "high":
			result = "\n" + "═" * 55 + "\n"
			result += f"  🏆 QUEST COMPLETE: {qdef['name']}\n"
			result += "  Your actions reshape the road ahead.\n"
			result += "═" * 55 + "\n\n"
		else:
			result = "\n" + "═" * 55 + "\n"
			result += f"  🏆 QUEST COMPLETE: {qdef['name']}\n"
			result += "═" * 55 + "\n\n"

		# Award XP
		xp_reward = rewards.get("xp", 0)
		if xp_reward and PROGRESSION_AVAILABLE:
			try:
				xp_msg = award_xp(self.engine.player, xp_reward, f"Quest: {qdef['name']}")
				if xp_msg:
					result += f"  {xp_msg}\n"
			except Exception:
				pass

		# Award gold
		gold_reward = rewards.get("gold", 0)
		if gold_reward:
			self.engine.player.stats["gold"] = self.engine.player.stats.get("gold", 0) + gold_reward
			result += f"  💰 Received {gold_reward} gold\n"

		# Award skill points
		sp_reward = rewards.get("skill_points", 0)
		if sp_reward:
			self.engine.player.stats["skill_points"] = self.engine.player.stats.get("skill_points", 0) + sp_reward
			result += f"  ⭐ Received {sp_reward} Skill Point{'s' if sp_reward > 1 else ''}\n"

		# Award items
		item_rewards = rewards.get("items", {})
		for item_name, count in item_rewards.items():
			inv = self.engine.player.inventory
			inv[item_name] = inv.get(item_name, 0) + count
			self.engine._inventory_changed = True
			nice = item_name.replace("_", " ").title()
			result += f"  📦 Received: {count}x {nice}\n"

		result += "\n"

		# Track achievements for quest completion
		try:
			from achievement_system import track_event, check_achievements, format_achievement_unlock
			if not qdef.get("tutorial_only"):
				track_event(self.engine.player, "quests_completed")
			if gold_reward:
				track_event(self.engine.player, "total_gold", gold_reward)
			newly_unlocked = check_achievements(self.engine.player)
			for ach_id, ach_data in newly_unlocked:
				result += format_achievement_unlock(ach_id, ach_data)
		except Exception:
			pass

		if qdef.get("tutorial_only"):
			try:
				import tutorial_system
				result += tutorial_system.on_tutorial_quest_turned_in(self.engine, quest_id)
			except Exception:
				pass

		# Check if chain_next should be offered
		chain_next = qdef.get("chain_next")
		if chain_next and chain_next in QUEST_DATABASE and not qdef.get("tutorial_only"):
			next_def = QUEST_DATABASE[chain_next]
			level = self.engine.player.stats.get("level", 1)
			if level >= next_def.get("level_req", 1):
				result += f"  💬 New quest available from {self._npc_display_name(next_def['giver'])}: \"{next_def['name']}\"\n"
				result += f"  Talk to them to accept it!\n"

		return result

	# ── Event hooks (called by engine) ────────────────────────────────

	def on_enemy_killed(self, enemy_name, is_boss=False, is_mini_boss=False):
		"""Called when player kills an enemy. Updates kill objectives."""
		for qid, qs in self.quests.items():
			if qs.status != QuestState.STATUS_ACTIVE:
				continue
			qdef = QUEST_DATABASE.get(qid)
			if not qdef:
				continue
			changed = False
			for i, obj in enumerate(qdef["objectives"]):
				if obj["type"] != "kill":
					continue
				target = obj["target"]
				count = obj.get("count", 1)
				current = qs.progress.get(i, 0)
				if current >= count:
					continue  # already done

				# Match enemy name or special meta-targets
				matched = False
				if target == "any_boss" and is_boss:
					matched = True
				elif target == "any_mini_boss" and is_mini_boss:
					matched = True
				elif enemy_name.lower() == target.lower():
					matched = True

				if matched:
					qs.progress[i] = min(current + 1, count)
					changed = True

			if changed:
				self._check_quest_completion(qid)

	def on_item_changed(self):
		"""Called when player inventory changes. Re-checks collect objectives."""
		for qid, qs in self.quests.items():
			if qs.status != QuestState.STATUS_ACTIVE:
				continue
			self._check_all_objectives(qid)

	def on_room_entered(self, room_id):
		"""Called when player enters a room. Updates visit objectives."""
		for qid, qs in self.quests.items():
			if qs.status != QuestState.STATUS_ACTIVE:
				continue
			qdef = QUEST_DATABASE.get(qid)
			if not qdef:
				continue
			changed = False
			for i, obj in enumerate(qdef["objectives"]):
				if obj["type"] != "visit":
					continue
				if obj["room"] == room_id and qs.progress.get(i, 0) == 0:
					qs.progress[i] = 1
					changed = True
			if changed:
				self._check_quest_completion(qid)

	def on_npc_talked(self, npc_id):
		"""Called when player talks to an NPC. Updates talk objectives."""
		for qid, qs in self.quests.items():
			if qs.status != QuestState.STATUS_ACTIVE:
				continue
			qdef = QUEST_DATABASE.get(qid)
			if not qdef:
				continue
			changed = False
			for i, obj in enumerate(qdef["objectives"]):
				if obj["type"] != "talk":
					continue
				if obj["npc"] == npc_id and qs.progress.get(i, 0) == 0:
					qs.progress[i] = 1
					changed = True
			if changed:
				self._check_quest_completion(qid)

	# ── Notification generation ──────────────────────────────────────

	def get_objective_update(self, quest_id, obj_index):
		"""Generate a progress notification string for a specific objective."""
		qdef = QUEST_DATABASE.get(quest_id)
		qs = self.quests.get(quest_id)
		if not qdef or not qs:
			return ""
		obj = qdef["objectives"][obj_index]
		current = qs.progress.get(obj_index, 0)
		count = obj.get("count", 1)
		if obj["type"] in ("kill", "collect"):
			return f"  📜 [{qdef['name']}] {obj['description']} ({current}/{count})"
		else:
			status = "✅ Done" if current >= 1 else "In progress"
			return f"  📜 [{qdef['name']}] {obj['description']} — {status}"

	def get_quest_notifications(self):
		"""Check for any quests that just became complete and return notification text."""
		feel = self._get_game_feel_intensity()
		notifications = []
		for qid, qs in self.quests.items():
			if qs.status == QuestState.STATUS_COMPLETE:
				qdef = QUEST_DATABASE.get(qid)
				if qdef:
					turn_in_name = self._npc_display_name(qdef.get("turn_in", qdef.get("giver", "???")))
					if feel == "low":
						notifications.append(
							f"  ✨ Quest complete: {qdef['name']} (turn in at {turn_in_name})"
						)
					elif feel == "high":
						notifications.append(
							f"  ✨ Quest \"{qdef['name']}\" objectives complete! "
							f"Return to {turn_in_name} to claim your reward and push the story forward."
						)
					else:
						notifications.append(
							f"  ✨ Quest \"{qdef['name']}\" objectives complete! "
							f"Return to {turn_in_name} to claim your reward."
						)
		return "\n".join(notifications)

	def _get_tutorial_journal_snapshot(self):
		"""Return a compact tutorial status snapshot for journal rendering."""
		try:
			import tutorial_system
		except Exception:
			return None

		player = getattr(self.engine, "player", None)
		state = tutorial_system.ensure_tutorial_state(player)
		if state is None or not tutorial_system.tutorial_is_active(state):
			return None

		total_steps = int(getattr(tutorial_system, "TUTORIAL_STEP_COUNT", 8) or 8)
		if total_steps <= 0:
			total_steps = 8
		current_step = int(state.get("current_step", 0) or 0)
		current_step = max(0, min(total_steps - 1, current_step))

		active_qid = str(state.get("active_tutorial_quest") or "").strip().lower()
		if active_qid:
			lesson_name = tutorial_system.TUTORIAL_QUEST_NAMES.get(
				active_qid,
				active_qid.replace("_", " ").title(),
			)
		else:
			lesson_name = "Getting Started"

		next_prompt = str(tutorial_system._step_prompt(self.engine, current_step, state) or "")
		next_lines = []
		for raw in next_prompt.splitlines():
			line = str(raw).strip()
			if not line:
				continue
			lower = line.lower()
			if lower.startswith("lesson:"):
				continue
			if lower.startswith("what to do:"):
				continue
			if len(line) > 2 and line[0].isdigit() and line[1] == ".":
				line = line[2:].strip()
			next_lines.append(line)
			if len(next_lines) >= 4:
				break

		unmet = []
		if active_qid:
			try:
				unmet = tutorial_system.get_unmet_tutorial_requirements(self.engine, active_qid)
			except Exception:
				unmet = []

		hints = [tutorial_system.TUTORIAL_REQUIREMENT_HINTS.get(k, k) for k in unmet[:3]]
		extra_unmet = max(0, len(unmet) - len(hints))

		return {
			"step_label": f"{current_step + 1}/{total_steps}",
			"lesson": lesson_name,
			"next_lines": next_lines,
			"unmet_hints": hints,
			"extra_unmet": extra_unmet,
		}

	# ── Journal display ──────────────────────────────────────────────

	def get_journal_text(self):
		"""Generate the full journal display text."""
		active = self.get_active_quests()
		completed = self.get_completed_quests()
		feel = self._get_game_feel_intensity()
		tutorial_snapshot = self._get_tutorial_journal_snapshot()

		if feel == "low":
			if not active and not completed and not tutorial_snapshot:
				return "\nQUEST JOURNAL\n- No quests yet. Talk to NPCs to find work.\n"

			lines = ["\nQUEST JOURNAL", f"- Active: {len(active)}", f"- Completed: {len(completed)}"]
			if tutorial_snapshot:
				lines.append("\nTUTORIAL TRACKER")
				lines.append(f"- Step: {tutorial_snapshot['step_label']}")
				lines.append(f"- Lesson: {tutorial_snapshot['lesson']}")
				if tutorial_snapshot["next_lines"]:
					lines.append("- Next:")
					for line in tutorial_snapshot["next_lines"]:
						lines.append(f"  - {line}")
				if tutorial_snapshot["unmet_hints"]:
					lines.append("- Before turn-in:")
					for hint in tutorial_snapshot["unmet_hints"]:
						lines.append(f"  - {hint}")
					if tutorial_snapshot["extra_unmet"] > 0:
						lines.append(f"  - ... and {tutorial_snapshot['extra_unmet']} more.")
			if active:
				lines.append("\nACTIVE")
				for qdef, qs in active:
					status = "READY" if qs.status == QuestState.STATUS_COMPLETE else "IN PROGRESS"
					lines.append(f"- {qdef['name']} [{status}]")
					for i, obj in enumerate(qdef["objectives"]):
						progress = qs.progress.get(i, 0)
						count = obj.get("count", 1)
						if obj["type"] in ("kill", "collect"):
							lines.append(f"  - {obj['description']} ({progress}/{count})")
						else:
							state = "done" if progress >= count else "pending"
							lines.append(f"  - {obj['description']} [{state}]")
			if completed:
				lines.append("\nCOMPLETED")
				for qdef in completed[-8:]:
					lines.append(f"- {qdef['name']}")
			return "\n".join(lines) + "\n"

		result = "\n" + "╔" + "═" * 58 + "╗\n"
		result += "║" + "QUEST JOURNAL".center(58) + "║\n"
		result += "╠" + "═" * 58 + "╣\n"

		if not active and not completed and not tutorial_snapshot:
			result += "║" + "  No quests yet. Talk to NPCs to find work!".ljust(58) + "║\n"
			result += "╚" + "═" * 58 + "╝\n"
			return result

		def _wrap_words(text, width=58):
			words = str(text).split()
			if not words:
				return [""]
			wrapped = []
			current = ""
			for word in words:
				candidate = (current + " " + word).strip()
				if len(candidate) <= width:
					current = candidate
				else:
					if current:
						wrapped.append(current)
					current = word
			if current:
				wrapped.append(current)
			return wrapped

		def _append_wrapped(line):
			nonlocal result
			for segment in _wrap_words(line, 58):
				result += "║" + segment.ljust(58) + "║\n"

		if feel == "high":
			ready_count = sum(1 for _, qs in active if qs.status == QuestState.STATUS_COMPLETE)
			result += "║" + f"  Active: {len(active)}  |  Completed: {len(completed)}  |  Ready: {ready_count}".ljust(58) + "║\n"
			result += "║" + "  Your journal pages crackle with urgency and unfinished vows.".ljust(58) + "║\n"
			result += "╠" + "═" * 58 + "╣\n"

		if tutorial_snapshot:
			result += "║" + "  TUTORIAL TRACKER".ljust(58) + "║\n"
			result += "║" + ("  " + "─" * 50).ljust(58) + "║\n"
			_append_wrapped(f"  Step: {tutorial_snapshot['step_label']}")
			_append_wrapped(f"  Lesson: {tutorial_snapshot['lesson']}")
			if tutorial_snapshot["next_lines"]:
				_append_wrapped("  Next:")
				for line in tutorial_snapshot["next_lines"]:
					_append_wrapped(f"    • {line}")
			if tutorial_snapshot["unmet_hints"]:
				_append_wrapped("  Before turn-in:")
				for hint in tutorial_snapshot["unmet_hints"]:
					_append_wrapped(f"    ☐ {hint}")
				if tutorial_snapshot["extra_unmet"] > 0:
					_append_wrapped(f"    ... and {tutorial_snapshot['extra_unmet']} more.")
			result += "║" + " ".ljust(58) + "║\n"

		# Active quests
		if active:
			result += "║" + "  ACTIVE QUESTS".ljust(58) + "║\n"
			result += "║" + ("  " + "─" * 50).ljust(58) + "║\n"
			for qdef, qs in active:
				status_icon = "🔔" if qs.status == QuestState.STATUS_COMPLETE else "📜"
				status_text = " [READY TO TURN IN]" if qs.status == QuestState.STATUS_COMPLETE else ""
				result += "║" + f"  {status_icon} {qdef['name']}{status_text}".ljust(58) + "║\n"
				result += "║" + f"     {qdef['description'][:50]}...".ljust(58) + "║\n" if len(qdef['description']) > 50 else ""
				
				# Show objectives with progress
				for i, obj in enumerate(qdef["objectives"]):
					progress = qs.progress.get(i, 0)
					count = obj.get("count", 1)
					done = progress >= count
					mark = "✅" if done else "☐"
					if obj["type"] in ("kill", "collect"):
						line = f"     {mark} {obj['description']} ({progress}/{count})"
					else:
						line = f"     {mark} {obj['description']}"
					result += "║" + line.ljust(58) + "║\n"

				# Show turn-in NPC if complete
				if qs.status == QuestState.STATUS_COMPLETE:
					turn_in = self._npc_display_name(qdef.get("turn_in", qdef.get("giver")))
					result += "║" + f"     → Return to {turn_in}".ljust(58) + "║\n"
				result += "║" + " ".ljust(58) + "║\n"

		# Completed quests
		if completed:
			result += "║" + "  COMPLETED QUESTS".ljust(58) + "║\n"
			result += "║" + ("  " + "─" * 50).ljust(58) + "║\n"
			for qdef in completed:
				result += "║" + f"  ✅ {qdef['name']}".ljust(58) + "║\n"

		result += "╚" + "═" * 58 + "╝\n"
		return result

	# ── NPC integration ──────────────────────────────────────────────

	def get_npc_quest_dialogue(self, npc_id):
		"""
		Generate quest-specific dialogue options for an NPC.
		Returns list of option dicts: [{"label": ..., "quest_action": ...}, ...]
		"""
		options = []
		player_level = self.engine.player.stats.get("level", 1) if self.engine.player else 1

		# Available quests to accept from this NPC
		for qdef in self.get_available_quests(npc_id):
			options.append({
				"label": f"📜 [Quest] {qdef['name']}",
				"quest_action": ("offer", qdef["id"]),
			})

		# Active quests that turn in to this NPC
		for qid, qs in self.quests.items():
			qdef = QUEST_DATABASE.get(qid)
			if not qdef:
				continue
			if qdef.get("turn_in") != npc_id:
				continue
			if qs.status == QuestState.STATUS_COMPLETE:
				options.append({
					"label": f"🏆 [Turn in] {qdef['name']}",
					"quest_action": ("turn_in", qdef["id"]),
				})
			elif qs.status == QuestState.STATUS_ACTIVE:
				options.append({
					"label": f"📋 [Progress] {qdef['name']}",
					"quest_action": ("progress", qdef["id"]),
				})

		return options

	def handle_quest_dialogue(self, action_type, quest_id):
		"""
		Handle a quest-related dialogue action.
		Returns display text.
		"""
		if action_type == "offer":
			return self._quest_offer_text(quest_id)
		elif action_type == "accept":
			return self.accept_quest(quest_id)
		elif action_type == "turn_in":
			return self.turn_in_quest(quest_id)
		elif action_type == "progress":
			return self._quest_progress_text(quest_id)
		return ""

	# ── Internal helpers ─────────────────────────────────────────────

	def _spawn_visible_enemy_for_quest(self, qdef):
		"""Spawn a visible enemy in a specific room for scripted quest beats."""
		spawn_cfg = qdef.get("spawn_visible_enemy") if isinstance(qdef, dict) else None
		if not isinstance(spawn_cfg, dict):
			return ""

		room_id = str(spawn_cfg.get("room") or "").strip()
		enemy_id = str(spawn_cfg.get("enemy_id") or "").strip()
		if not room_id or not enemy_id:
			return ""

		encounter_manager = getattr(self.engine, "encounter_manager", None)
		if not encounter_manager:
			return ""

		player = getattr(self.engine, "player", None)
		level = 1
		if player and isinstance(getattr(player, "stats", None), dict):
			level = int(player.stats.get("level", 1) or 1)

		enemy_data = None
		try:
			enemy_data = encounter_manager.scale_enemy(enemy_id, level)
		except Exception:
			enemy_data = None
		if not enemy_data:
			return ""

		visible = getattr(encounter_manager, "visible_enemies", None)
		if not isinstance(visible, dict):
			return ""

		visible[room_id] = {
			"enemy_id": enemy_id,
			"enemy_data": enemy_data,
			"persistent": bool(spawn_cfg.get("persistent", False)),
			"reset_on_engage": bool(spawn_cfg.get("reset_on_engage", spawn_cfg.get("persistent", False))),
		}
		rooms_rolled = getattr(encounter_manager, "rooms_rolled", None)
		if isinstance(rooms_rolled, set):
			rooms_rolled.add(room_id)

		enemy_name = enemy_data.get("name", enemy_id.replace("_", " ").title())
		if room_id == "village_training_grounds":
			return f"Training target deployed: {enemy_name}. Head to the Training Grounds and type 'fight'."
		return f"A quest target has appeared in {room_id}: {enemy_name}."

	def reconcile_scripted_visible_enemies(self):
		"""Ensure scripted quest targets still exist after load/resume state drift."""
		encounter_manager = getattr(self.engine, "encounter_manager", None)
		visible = getattr(encounter_manager, "visible_enemies", None) if encounter_manager else None
		if not isinstance(visible, dict):
			return 0

		spawned = 0
		for qid, qs in self.quests.items():
			if qs.status not in (QuestState.STATUS_ACTIVE, QuestState.STATUS_COMPLETE):
				continue
			qdef = QUEST_DATABASE.get(qid)
			if not qdef:
				continue
			spawn_cfg = qdef.get("spawn_visible_enemy") if isinstance(qdef, dict) else None
			if not isinstance(spawn_cfg, dict):
				continue
			room_id = str(spawn_cfg.get("room") or "").strip()
			if not room_id or room_id in visible:
				continue
			if self._spawn_visible_enemy_for_quest(qdef):
				spawned += 1

		return spawned

	def _check_all_objectives(self, quest_id):
		"""Re-check all objectives for a quest (useful for collect/visit on accept)."""
		qdef = QUEST_DATABASE.get(quest_id)
		qs = self.quests.get(quest_id)
		if not qdef or not qs or qs.status != QuestState.STATUS_ACTIVE:
			return

		player = self.engine.player
		for i, obj in enumerate(qdef["objectives"]):
			if obj["type"] == "collect":
				item = obj["item"]
				needed = obj.get("count", 1)
				have = self._get_collect_amount(player, item)
				qs.progress[i] = min(have, needed)
			elif obj["type"] == "visit":
				room = obj["room"]
				if room in player.visited_rooms:
					qs.progress[i] = 1
			# kill/talk objectives only update on events

		self._check_quest_completion(quest_id)

	def _get_collect_amount(self, player, item_id):
		"""Resolve collect objective quantity, including grouped objective aliases."""
		inv = player.inventory if player else {}
		if not isinstance(inv, dict):
			return 0

		# Fish bundle used by tavern and exploration quest lines.
		if item_id == "fresh_fish":
			fish_items = (
				"small_fish", "river_trout", "mudfish", "large_fish", "striped_perch",
				"swamp_catfish", "cave_eel", "golden_fish", "ancient_pike",
				"ghost_fish", "leviathan_fry", "prismatic_koi",
			)
			return sum(int(inv.get(fid, 0)) for fid in fish_items)

		return int(inv.get(item_id, 0))

	def _check_quest_completion(self, quest_id):
		"""Check if all objectives are met and update status to COMPLETE."""
		qdef = QUEST_DATABASE.get(quest_id)
		qs = self.quests.get(quest_id)
		if not qdef or not qs or qs.status != QuestState.STATUS_ACTIVE:
			return

		all_done = True
		for i, obj in enumerate(qdef["objectives"]):
			count = obj.get("count", 1)
			current = qs.progress.get(i, 0)
			if current < count:
				all_done = False
				break

		if all_done:
			qs.status = QuestState.STATUS_COMPLETE
			feel = self._get_game_feel_intensity()
			# Notify the player
			if self.engine.gui:
				qdef_name = qdef['name']
				turn_in = self._npc_display_name(qdef.get("turn_in", qdef.get("giver")))
				if feel == "low":
					notification = (
						f"\n  ✨ Quest complete: {qdef_name}\n"
						f"  Turn in at {turn_in}.\n"
					)
				elif feel == "high":
					notification = (
						f"\n  ✨ Quest \"{qdef_name}\" objectives complete!\n"
						f"  Return to {turn_in} - your reward and the next chapter await.\n"
					)
				else:
					notification = (
						f"\n  ✨ Quest \"{qdef_name}\" objectives complete!\n"
						f"  Return to {turn_in} to claim your reward.\n"
					)
				try:
					self.engine.gui.append(notification)
				except Exception:
					pass

	def _quest_offer_text(self, quest_id):
		"""Generate the quest offer dialogue with accept prompt."""
		qdef = QUEST_DATABASE.get(quest_id)
		if not qdef:
			return "Quest not found."
		feel = self._get_game_feel_intensity()

		giver_name = self._npc_display_name(qdef.get("giver"))

		if feel == "low":
			result = f"\nQUEST OFFER: {qdef['name']}\n"
			result += f"From: {giver_name}\n"
			result += f"{qdef['description']}\n"
			result += "Objectives:\n"
			for obj in qdef["objectives"]:
				count = obj.get("count", 1)
				if obj["type"] in ("kill", "collect"):
					result += f"- {obj['description']} (0/{count})\n"
				else:
					result += f"- {obj['description']}\n"
			rewards = qdef.get("rewards", {})
			reward_parts = []
			if rewards.get("xp"):
				reward_parts.append(f"{rewards['xp']} XP")
			if rewards.get("gold"):
				reward_parts.append(f"{rewards['gold']}g")
			if rewards.get("skill_points"):
				reward_parts.append(f"{rewards['skill_points']} SP")
			if reward_parts:
				result += "Rewards: " + ", ".join(reward_parts) + "\n"
			result += "Accept? (yes/no)\n"
			self.engine.pending_quest_action = ("accept", quest_id)
			return result

		result = "\n" + "═" * 55 + "\n"
		result += f"  📜 {giver_name} offers you a quest:\n"
		result += f"  \"{qdef['name']}\"\n"
		result += "═" * 55 + "\n\n"
		result += f"  {qdef['description']}\n\n"
		result += "  Objectives:\n"
		for obj in qdef["objectives"]:
			count = obj.get("count", 1)
			if obj["type"] in ("kill", "collect"):
				result += f"    ☐ {obj['description']} (0/{count})\n"
			else:
				result += f"    ☐ {obj['description']}\n"

		# Show rewards
		rewards = qdef.get("rewards", {})
		result += "\n  Rewards:\n"
		if rewards.get("xp"):
			result += f"    ⭐ {rewards['xp']} XP\n"
		if rewards.get("gold"):
			result += f"    💰 {rewards['gold']} gold\n"
		if rewards.get("skill_points"):
			sp = rewards['skill_points']
			result += f"    ⭐ {sp} Skill Point{'s' if sp > 1 else ''}\n"
		for item, count in rewards.get("items", {}).items():
			nice = item.replace("_", " ").title()
			result += f"    📦 {count}x {nice}\n"

		if feel == "high":
			result += "\n  The request carries weight. You can almost feel the story shifting.\n"

		result += "\n  Accept this quest? (yes/no)\n"

		# Set pending state
		self.engine.pending_quest_action = ("accept", quest_id)

		return result

	def _quest_progress_text(self, quest_id):
		"""Show current progress for an active quest."""
		qdef = QUEST_DATABASE.get(quest_id)
		qs = self.quests.get(quest_id)
		if not qdef or not qs:
			return "Quest not found."
		feel = self._get_game_feel_intensity()

		# Re-check collect objectives
		self._check_all_objectives(quest_id)

		giver_name = self._npc_display_name(qdef.get("giver"))

		result = "\n" + "─" * 55 + "\n"
		result += f"  📋 Quest Progress: {qdef['name']}\n"
		result += "─" * 55 + "\n\n"

		for i, obj in enumerate(qdef["objectives"]):
			progress = qs.progress.get(i, 0)
			count = obj.get("count", 1)
			done = progress >= count
			mark = "✅" if done else "☐"
			if obj["type"] in ("kill", "collect"):
				result += f"    {mark} {obj['description']} ({progress}/{count})\n"
			else:
				result += f"    {mark} {obj['description']}\n"

		if qs.status == QuestState.STATUS_COMPLETE:
			turn_in = self._npc_display_name(qdef.get("turn_in", qdef.get("giver")))
			result += f"\n  ✨ All objectives complete! Talk to {turn_in} to turn in.\n"
		else:
			if feel == "high":
				result += "\n  Keep going - every step is pulling this thread tighter.\n"
			elif feel == "low":
				result += "\n  Keep going.\n"
			else:
				result += "\n  Keep going — you're making progress!\n"

		return result

	def _npc_display_name(self, npc_id):
		"""Get the display name for an NPC id."""
		if not npc_id:
			return "Unknown"
		try:
			from npc_system import NPC_DATABASE
			npc = NPC_DATABASE.get(npc_id)
			if npc:
				return f"{npc['name']} ({npc['title']})"
		except ImportError:
			pass
		return npc_id.replace("_", " ").title()
