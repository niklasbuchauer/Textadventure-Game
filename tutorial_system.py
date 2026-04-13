"""Player-facing tutorial flow and progression helpers."""

REWARD_GOLD = 50

TUTORIAL_START_ROOM = "tutorial_spawn"
TUTORIAL_GUIDE_NPC = "tutorial_guide"
TUTORIAL_QUEST_ID = "welcome_to_havenbrook"

TUTORIAL_QUEST_CHAIN = [
	"welcome_to_havenbrook",
	"tutorial_trade_routes",
	"tutorial_bank_basics",
	"tutorial_combat_drill",
	"tutorial_recovery_check",
	"tutorial_crafting_kickoff",
	"tutorial_graduation",
]
TUTORIAL_FINAL_QUEST = TUTORIAL_QUEST_CHAIN[-1]

TUTORIAL_QUEST_NAMES = {
	"welcome_to_havenbrook": "Welcome to Havenbrook",
	"tutorial_trade_routes": "Trade Routes",
	"tutorial_bank_basics": "Bank Basics",
	"tutorial_combat_drill": "Combat Drill",
	"tutorial_recovery_check": "Recovery Check",
	"tutorial_crafting_kickoff": "Forgemaster's Starter",
	"tutorial_graduation": "Graduation Checklist",
}

TUTORIAL_QUEST_GIVERS = {
	"welcome_to_havenbrook": "Elder Rowan in the village square",
	"tutorial_trade_routes": "Silvia the merchant in the village square",
	"tutorial_bank_basics": "the banker at the Bank of Estoria",
	"tutorial_combat_drill": "the tavern patron",
	"tutorial_recovery_check": "Father Aldric in the chapel",
	"tutorial_crafting_kickoff": "Tormund at the blacksmith",
	"tutorial_graduation": "Elder Rowan in the village square",
}

TUTORIAL_QUEST_REQUIREMENTS = {
	"welcome_to_havenbrook": [],
	"tutorial_trade_routes": ["used_shop_browse", "used_shop_buy_or_sell"],
	"tutorial_bank_basics": ["used_balance", "used_deposit", "used_withdraw"],
	"tutorial_combat_drill": ["used_fight", "used_attack", "used_defend"],
	"tutorial_recovery_check": ["opened_journal"],
	"tutorial_crafting_kickoff": ["used_smelt"],
	"tutorial_graduation": ["used_stats", "used_skills", "used_save"],
}

TUTORIAL_REQUIREMENT_HINTS = {
	"used_shop_browse": "Type: shop browse",
	"used_shop_buy_or_sell": "Type: shop buy torch 10 (or shop sell torch 1)",
	"used_balance": "Type: balance",
	"used_deposit": "Type: deposit 1",
	"used_withdraw": "Type: withdraw 1",
	"used_fight": "Type: fight",
	"used_attack": "Type: attack",
	"used_defend": "Type: defend",
	"opened_journal": "Type: journal",
	"used_smelt": "Type: smelt",
	"used_stats": "Type: stats",
	"used_skills": "Type: skills",
	"used_save": "Type: save",
}

DEFAULT_PROGRESS_FLAGS = {
	"picked_item": False,
	"checked_inventory": False,
	"talked_to_guide": False,
	"selected_quest_option": False,
	"accepted_quest": False,
}

DEFAULT_TUTORIAL_STATE = {
	"started": False,
	"skipped": False,
	"is_complete": False,
	"reward_claimed": False,
	"current_step": 0,
	"completed_steps": [],
	"progress_flags": dict(DEFAULT_PROGRESS_FLAGS),
	"active_tutorial_quest": TUTORIAL_QUEST_ID,
	"completed_tutorial_quests": [],
	"quest_command_flags": {},
	"quest_stage": 0,
}

TUTORIAL_STEP_COUNT = 8


def _clone_default(value):
	if isinstance(value, list):
		return list(value)
	if isinstance(value, dict):
		return dict(value)
	return value


def _join_messages(*parts):
	clean_parts = [str(part).strip() for part in parts if part]
	return "\n\n".join(clean_parts)


def _reset_progress_flags(state):
	state["progress_flags"] = dict(DEFAULT_PROGRESS_FLAGS)
	return state["progress_flags"]


def _normalize_progress_flags(state):
	flags = state.get("progress_flags")
	if not isinstance(flags, dict):
		flags = {}
	for key, value in DEFAULT_PROGRESS_FLAGS.items():
		flags[key] = bool(flags.get(key, value))
	state["progress_flags"] = flags
	return flags


def _normalize_quest_command_flags(state):
	flags = state.get("quest_command_flags")
	if not isinstance(flags, dict):
		flags = {}
	for key, value in list(flags.items()):
		flags[key] = bool(value)
	state["quest_command_flags"] = flags
	return flags


def _normalize_completed_tutorial_quests(state):
	completed = state.get("completed_tutorial_quests")
	if not isinstance(completed, list):
		completed = []
	normalized = []
	for quest_id in completed:
		qid = str(quest_id).strip().lower()
		if qid in TUTORIAL_QUEST_CHAIN and qid not in normalized:
			normalized.append(qid)
	state["completed_tutorial_quests"] = normalized
	return normalized


def _next_tutorial_quest(quest_id):
	if quest_id not in TUTORIAL_QUEST_CHAIN:
		return None
	idx = TUTORIAL_QUEST_CHAIN.index(quest_id)
	if idx + 1 >= len(TUTORIAL_QUEST_CHAIN):
		return None
	return TUTORIAL_QUEST_CHAIN[idx + 1]


def _quest_state_status(quest_state):
	if quest_state is None:
		return ""
	if isinstance(quest_state, dict):
		return str(quest_state.get("status", "")).strip().lower()
	return str(getattr(quest_state, "status", "")).strip().lower()


def _is_pickup_verb(verb):
	return (verb or "").lower() in ("collect", "take", "get", "pickup", "pick")


def _is_inventory_verb(verb):
	return (verb or "").lower() in ("inventory", "inv", "i")


def _pickup_targets_tutorial_item(args):
	target = " ".join(str(arg).strip().lower() for arg in (args or []) if str(arg).strip())
	if not target:
		return False
	return (
		"torch" in target
		or "faded map" in target
		or "faded_map" in target
		or target == "map"
		or target.endswith(" map")
	)


def _is_talk_to_guide(verb, args):
	if (verb or "").lower() != "talk":
		return False
	return any(str(arg).strip().lower() == TUTORIAL_GUIDE_NPC for arg in (args or []))


def _is_quest_accept_verb(verb):
	return (verb or "").lower() in ("yes", "y", "accept", "1")


def _is_tutorial_welcome_offer_response(response):
	text = str(response or "").strip().lower()
	if not text:
		return False
	if "welcome to havenbrook" not in text:
		return False
	if "quest offer" in text or "offers you a quest" in text:
		return True
	if "quest" in text and "accept" in text and "yes/no" in text:
		return True
	return False


def _tutorial_quest_status(engine, quest_id):
	quest_manager = getattr(engine, "quest_manager", None)
	if not quest_manager:
		return ""
	quest_state = getattr(quest_manager, "quests", {}).get(quest_id)
	return _quest_state_status(quest_state)


def _tutorial_quest_accepted(engine, quest_id):
	return _tutorial_quest_status(engine, quest_id) in ("active", "complete", "turned_in")


def _resolve_active_tutorial_quest(engine, state):
	active = str(state.get("active_tutorial_quest", "") or "").strip().lower()
	if active in TUTORIAL_QUEST_CHAIN:
		return active

	quest_manager = getattr(engine, "quest_manager", None)
	if quest_manager:
		for qid in TUTORIAL_QUEST_CHAIN:
			status = _quest_state_status(getattr(quest_manager, "quests", {}).get(qid))
			if status in ("active", "complete"):
				state["active_tutorial_quest"] = qid
				return qid

	completed = _normalize_completed_tutorial_quests(state)
	for qid in TUTORIAL_QUEST_CHAIN:
		if qid not in completed:
			state["active_tutorial_quest"] = qid
			return qid

	state["active_tutorial_quest"] = None
	return None


def _current_room(engine):
	player = getattr(engine, "player", None)
	room_id = getattr(player, "current_room", None)
	if not room_id or not hasattr(engine, "get_room_data"):
		return None
	try:
		return engine.get_room_data(room_id)
	except Exception:
		return None


def _set_player_room(engine, room_id):
	player = getattr(engine, "player", None)
	if not player:
		return
	player.current_room = room_id
	visited = getattr(player, "visited_rooms", None)
	if isinstance(visited, set):
		visited.add(room_id)


def _reset_tutorial_quests(engine):
	quest_manager = getattr(engine, "quest_manager", None)
	if not quest_manager:
		return
	try:
		for quest_id in TUTORIAL_QUEST_CHAIN:
			quest_manager.quests.pop(quest_id, None)
	except Exception:
		pass


def _room_name(room):
	if isinstance(room, dict):
		return str(room.get("name") or room.get("title") or "this place")
	return str(getattr(room, "name", None) or getattr(room, "title", None) or "this place")


def _room_items(room):
	if isinstance(room, dict):
		items = room.get("items", [])
	else:
		items = getattr(room, "items", [])
	if isinstance(items, dict):
		expanded = []
		for item_name, quantity in items.items():
			try:
				count = int(quantity)
			except Exception:
				count = 1
			for _ in range(max(0, count)):
				expanded.append(str(item_name))
		return expanded
	if isinstance(items, list):
		return [str(item) for item in items if item is not None]
	return []


def _get_unmet_requirements(state, quest_id):
	reqs = TUTORIAL_QUEST_REQUIREMENTS.get(quest_id, [])
	flags = _normalize_quest_command_flags(state)
	return [key for key in reqs if not flags.get(key, False)]


def get_unmet_tutorial_requirements(engine, quest_id):
	player = getattr(engine, "player", None)
	state = ensure_tutorial_state(player)
	if state is None:
		return []
	return _get_unmet_requirements(state, quest_id)


def _format_requirement_block(unmet, heading):
	if not unmet:
		return ""
	lines = [str(heading)]
	for key in unmet:
		lines.append(f"  - {TUTORIAL_REQUIREMENT_HINTS.get(key, key)}")
	return "\n".join(lines)


def _format_lesson_block(title, where_to_start, steps, turn_in):
	lines = [
		f"Lesson: {title}",
		f"Where to start: {where_to_start}",
		"What to do:",
	]
	for idx, step in enumerate(steps, start=1):
		lines.append(f"  {idx}. {step}")
	lines.append(f"Turn in: {turn_in}")
	return "\n".join(lines)


def format_tutorial_requirement_reminder(engine, quest_id, unmet=None):
	player = getattr(engine, "player", None)
	state = ensure_tutorial_state(player)
	if state is None:
		return ""
	if unmet is None:
		unmet = _get_unmet_requirements(state, quest_id)
	if not unmet:
		return ""
	quest_name = TUTORIAL_QUEST_NAMES.get(quest_id, quest_id)
	requirement_block = _format_requirement_block(
		unmet,
		f"Before turning in \"{quest_name}\", complete these commands:",
	)
	return _join_messages(
		requirement_block,
		"Then return to the same NPC and choose [Turn in].",
	)


def _quest_stage_prompt(engine, state):
	quest_id = _resolve_active_tutorial_quest(engine, state)
	if not quest_id:
		return "Tutorial route complete. Check journal and continue your adventure."

	if quest_id == "welcome_to_havenbrook":
		base = _format_lesson_block(
			"Welcome to Havenbrook",
			"Village square (Elder Rowan).",
			[
				"If you are inside the forge, type: outside.",
				"Type: talk tutorial_guide.",
				"Choose [Turn in] and confirm the hand-in.",
			],
			"Talk to tutorial_guide and choose [Turn in].",
		)
	elif quest_id == "tutorial_trade_routes":
		base = _format_lesson_block(
			"Trade Routes",
			"Village square (Silvia the merchant).",
			[
				"Type: talk merchant.",
				"Choose [Quest], then type: yes.",
				"Type: go shop (or shop).",
				"Type: shop browse.",
				"Type: shop buy <item> <price> (or shop sell <item> <price>).",
			],
			"Talk to merchant and choose [Turn in].",
		)
	elif quest_id == "tutorial_bank_basics":
		base = _format_lesson_block(
			"Bank Basics",
			"Bank of Estoria (the banker).",
			[
				"Type: go bank.",
				"Type: talk banker.",
				"Choose [Quest], then type: yes.",
				"Type: balance.",
				"Type: deposit 1.",
				"Type: withdraw 1.",
			],
			"Talk to banker and choose [Turn in].",
		)
	elif quest_id == "tutorial_combat_drill":
		base = _format_lesson_block(
			"Combat Drill",
			"Village tavern (the patron).",
			[
				"Type: go tavern.",
				"Type: talk patron.",
				"Choose [Quest], then type: yes.",
				"Type: outside, then north, then east.",
				"Type: fight.",
				"During battle, type: attack and defend.",
			],
			"Talk to patron and choose [Turn in].",
		)
	elif quest_id == "tutorial_recovery_check":
		base = _format_lesson_block(
			"Recovery Check",
			"Chapel (Father Aldric).",
			[
				"Type: go east, then chapel.",
				"Type: talk priest.",
				"Choose [Quest], then type: yes.",
				"Open your quest log with journal (or quests).",
			],
			"Talk to priest and choose [Turn in].",
		)
	elif quest_id == "tutorial_crafting_kickoff":
		base = _format_lesson_block(
			"Forgemaster's Starter",
			"Village blacksmith (Tormund).",
			[
				"Type: go blacksmith.",
				"Type: talk blacksmith.",
				"Choose [Quest], then type: yes.",
				"Type: smelt.",
				"Make sure you have an iron_ingot in your inventory.",
			],
			"Talk to blacksmith and choose [Turn in].",
		)
	else:
		base = _format_lesson_block(
			"Graduation Checklist",
			"Village square (Elder Rowan).",
			[
				"Type: talk tutorial_guide.",
				"Choose [Quest], then type: yes.",
				"Type: stats.",
				"Type: skills.",
				"Type: save.",
			],
			"Talk to tutorial_guide and choose [Turn in].",
		)

	unmet = _get_unmet_requirements(state, quest_id)
	if not unmet:
		return base

	return _join_messages(
		base,
		_format_requirement_block(unmet, "Before turn-in, complete these commands:"),
	)


def _step_prompt(engine, step_index, state=None):
	room = _current_room(engine)
	room_name = _room_name(room)
	items = _room_items(room)
	if step_index == 0:
		return f"You are at the tutorial spawn in {room_name}. Type: look (or l)."
	if step_index == 1:
		if items:
			return "Type: take torch (or take faded map). Then type: inventory (or i)."
		return "Type: take <item> (or get <item>). Then type: inventory (or i)."
	if step_index == 2:
		return "Leave the spawn for town. Type: go north (or n)."
	if step_index == 3:
		return (
			"Type: talk tutorial_guide. In Rowan's dialogue, choose the [Quest] option number, "
			"then type: yes."
		)
	if step_index == 4:
		return "Type: help (or commands) to open the command reference."
	if step_index == 5:
		return "Type: go shop (or shop) to visit the shop."
	if step_index == 6:
		return "Type: go blacksmith to visit the blacksmith."
	if step_index == 7:
		return _quest_stage_prompt(engine, state or {})
	return ""


def _step_success(step_index):
	if step_index == 0:
		return "Good. Reading the room gives you context before you act. Next, type: take torch (or take faded map), then inventory."
	if step_index == 1:
		return "Good. Picking up supplies and checking inventory is the first habit of a prepared adventurer. Next, type: go north (or n)."
	if step_index == 2:
		return "Good. Movement opens the world and leads you into the town's main path. Next, type: talk tutorial_guide, choose the [Quest] option number, then yes."
	if step_index == 3:
		return "Good. Talking to NPCs is how you get quests and learn what matters in town. Next, type: help (or commands)."
	if step_index == 4:
		return "Good. Help is always there when you need a quick reminder. Next, type: go shop (or shop)."
	if step_index == 5:
		return "Good. Shops are where you can stock up and compare prices. Next, type: go blacksmith."
	if step_index == 6:
		return "Good. The blacksmith is where your equipment path begins. Next, type: outside, then talk tutorial_guide."
	if step_index == 7:
		return "Good. You have completed the guided route into Havenbrook."
	return ""


def _step_matches(step_index, _engine, verb, args, _cmd):
	verb = (verb or "").lower()
	if step_index == 0:
		return verb in ("look", "l")
	if step_index == 1:
		return False
	if step_index == 2:
		if verb in ("n", "north"):
			return True
		if verb not in ("go", "walk", "move", "enter"):
			return False
		if not args:
			return False
		return args[0].lower() == "north"
	if step_index == 3:
		return False
	if step_index == 4:
		return verb in ("help", "commands", "?")
	if step_index == 5:
		if verb == "shop":
			return True
		if verb in ("go", "walk", "move") and args:
			return args[0].lower() == "shop"
		return False
	if step_index == 6:
		if verb in ("go", "walk", "move") and args:
			return args[0].lower() == "blacksmith"
		return False
	if step_index == 7:
		return False
	return False


def _mark_step_complete(state, step_index):
	completed = state.setdefault("completed_steps", [])
	if step_index not in completed:
		completed.append(step_index)
	state["current_step"] = step_index + 1
	if state["current_step"] >= TUTORIAL_STEP_COUNT:
		state["current_step"] = TUTORIAL_STEP_COUNT - 1


def _grant_reward(player, state):
	if state.get("reward_claimed"):
		return ""
	stats = getattr(player, "stats", None)
	if not isinstance(stats, dict):
		stats = {}
		player.stats = stats
	current_gold = int(stats.get("gold", 0) or 0)
	stats["gold"] = current_gold + REWARD_GOLD
	state["reward_claimed"] = True
	return f"You gained {REWARD_GOLD} gold as a thank-you for finishing the tutorial."


def _track_tutorial_command_flags(state, verb, args, _response):
	verb = (verb or "").lower()
	args = [str(arg).strip().lower() for arg in (args or []) if str(arg).strip()]
	first = args[0] if args else ""
	flags = _normalize_quest_command_flags(state)

	if verb == "outside":
		flags["used_outside"] = True

	if verb == "shop":
		if first in ("browse", "view", "list", "inventory", "stock"):
			flags["used_shop_browse"] = True
		if first in ("buy", "sell"):
			flags["used_shop_buy_or_sell"] = True

	if verb == "balance":
		flags["used_balance"] = True
	if verb == "deposit":
		flags["used_deposit"] = True
	if verb == "withdraw":
		flags["used_withdraw"] = True
	if verb == "bank":
		if first == "balance":
			flags["used_balance"] = True
		if first == "deposit":
			flags["used_deposit"] = True
		if first == "withdraw":
			flags["used_withdraw"] = True

	if verb == "fight":
		flags["used_fight"] = True
	if verb == "attack":
		flags["used_attack"] = True
	if verb == "defend":
		flags["used_defend"] = True

	if verb in ("journal", "j", "quests", "quest"):
		flags["opened_journal"] = True

	if verb == "smelt":
		flags["used_smelt"] = True

	if verb in ("stats", "level", "class"):
		flags["used_stats"] = True
	if verb in ("skills", "skill", "skilltree"):
		flags["used_skills"] = True
	if verb == "save":
		flags["used_save"] = True


def complete_tutorial(engine):
	player = getattr(engine, "player", None)
	state = ensure_tutorial_state(player)
	if state is None:
		return "Tutorial state could not be loaded."
	state["started"] = True
	state["skipped"] = False
	state["is_complete"] = True
	state["current_step"] = TUTORIAL_STEP_COUNT
	state["completed_steps"] = list(range(TUTORIAL_STEP_COUNT))
	state["active_tutorial_quest"] = None
	reward_line = _grant_reward(player, state)
	completion = (
		"Tutorial complete. You reached Havenbrook, finished every starter lesson, and proved you can navigate the core systems."
	)
	encouragement = "You are ready for full quests, dungeons, and long-form progression."
	return _join_messages(completion, encouragement, reward_line)


def on_tutorial_quest_turned_in(engine, quest_id):
	player = getattr(engine, "player", None)
	state = ensure_tutorial_state(player)
	if state is None or quest_id not in TUTORIAL_QUEST_CHAIN:
		return ""

	completed = _normalize_completed_tutorial_quests(state)
	if quest_id not in completed:
		completed.append(quest_id)

	if quest_id == TUTORIAL_FINAL_QUEST:
		return complete_tutorial(engine)

	next_quest = _next_tutorial_quest(quest_id)
	state["active_tutorial_quest"] = next_quest
	if next_quest in TUTORIAL_QUEST_CHAIN:
		state["quest_stage"] = TUTORIAL_QUEST_CHAIN.index(next_quest)

	if not next_quest:
		return ""

	completed_name = TUTORIAL_QUEST_NAMES.get(quest_id, quest_id)
	next_name = TUTORIAL_QUEST_NAMES.get(next_quest, next_quest)
	return _join_messages(
		f"Tutorial chapter complete: {completed_name}.",
		f"Next lesson unlocked: {next_name}.",
		_step_prompt(engine, 7, state),
	)


def start_tutorial(engine):
	player = getattr(engine, "player", None)
	state = ensure_tutorial_state(player)
	if state is None:
		return "No player found."

	_reset_tutorial_quests(engine)
	if getattr(player, "current_room", None) != TUTORIAL_START_ROOM:
		_set_player_room(engine, TUTORIAL_START_ROOM)

	state["started"] = True
	state["skipped"] = False
	state["is_complete"] = False
	state["current_step"] = 0
	state["completed_steps"] = []
	state["reward_claimed"] = False
	state["active_tutorial_quest"] = TUTORIAL_QUEST_ID
	state["completed_tutorial_quests"] = []
	state["quest_command_flags"] = {}
	state["quest_stage"] = 0
	_reset_progress_flags(state)

	intro = (
		"Tutorial started from the beginning. Follow the route into Havenbrook, then complete every tutorial quest chapter."
	)
	return _join_messages(intro, _step_prompt(engine, state["current_step"], state))


def skip_tutorial(engine):
	player = getattr(engine, "player", None)
	state = ensure_tutorial_state(player)
	if state is None:
		return "No player found."

	state["started"] = False
	state["skipped"] = True
	state["is_complete"] = False
	state["current_step"] = 0
	state["completed_steps"] = []
	state["active_tutorial_quest"] = None
	state["completed_tutorial_quests"] = []
	state["quest_command_flags"] = {}
	state["quest_stage"] = 0
	_reset_progress_flags(state)
	return "Tutorial skipped. You can type tutorial start later if you want the guided version."


def ensure_tutorial_state(player):
	"""Ensure the player has a normalized tutorial state dict."""
	if player is None or not hasattr(player, "state") or not isinstance(player.state, dict):
		return None

	state = player.state.get("tutorial_state")
	if not isinstance(state, dict):
		state = {}
		player.state["tutorial_state"] = state

	for key, value in DEFAULT_TUTORIAL_STATE.items():
		state.setdefault(key, _clone_default(value))
	_normalize_progress_flags(state)
	_normalize_quest_command_flags(state)
	_normalize_completed_tutorial_quests(state)

	completed_steps = state.get("completed_steps", [])
	if not isinstance(completed_steps, list):
		completed_steps = []
	normalized_steps = []
	for step in completed_steps:
		try:
			normalized_steps.append(int(step))
		except Exception:
			continue
	state["completed_steps"] = normalized_steps

	step_value = int(state.get("current_step", 0) or 0)
	if step_value < 0:
		step_value = 0
	if step_value >= TUTORIAL_STEP_COUNT:
		step_value = TUTORIAL_STEP_COUNT - 1
	state["current_step"] = step_value

	active = state.get("active_tutorial_quest")
	if active is not None:
		active = str(active).strip().lower()
	if active not in TUTORIAL_QUEST_CHAIN:
		state["active_tutorial_quest"] = TUTORIAL_QUEST_ID

	return state


def tutorial_is_active(state):
	return bool(state) and not state.get("is_complete") and not state.get("skipped") and bool(state.get("started"))


def get_tutorial_status(engine):
	player = getattr(engine, "player", None)
	state = ensure_tutorial_state(player)
	if state is None:
		return "Player state is not available."

	if not state.get("started") and not state.get("skipped") and not state.get("is_complete"):
		return (
			"Tutorial not started. Type tutorial start for a guided intro, or tutorial skip to keep playing normally."
		)

	current_step = int(state.get("current_step", 0) or 0)
	lines = ["Tutorial status:"]
	if state.get("skipped"):
		lines.append("  State: skipped")
		lines.append("  You can restart it with tutorial start.")
		return "\n".join(lines)

	if state.get("is_complete"):
		lines.append("  State: complete")
		lines.append(f"  Reward claimed: {bool(state.get('reward_claimed'))}")
		lines.append("  You can replay the tutorial with tutorial start.")
		return "\n".join(lines)

	lines.append(f"  Current step: {current_step + 1}/{TUTORIAL_STEP_COUNT}")
	lines.append(f"  Next: {_step_prompt(engine, current_step, state)}")

	active_quest = _resolve_active_tutorial_quest(engine, state)
	if active_quest in TUTORIAL_QUEST_CHAIN:
		quest_name = TUTORIAL_QUEST_NAMES.get(active_quest, active_quest)
		lines.append(f"  Active tutorial quest: {quest_name}")
		unmet = _get_unmet_requirements(state, active_quest)
		if unmet:
			lines.append("  Before turn-in, complete these commands:")
			for key in unmet:
				lines.append(f"    - {TUTORIAL_REQUIREMENT_HINTS.get(key, key)}")

	lines.append("  Tip: type tutorial status any time to see this again.")
	return "\n".join(lines)


def handle_tutorial_command(engine, args):
	args = [str(arg).strip().lower() for arg in (args or []) if str(arg).strip()]
	if not args:
		return get_tutorial_status(engine)
	action = args[0]
	if action in ("status", "info"):
		return get_tutorial_status(engine)
	if action in ("start", "begin", "replay"):
		return start_tutorial(engine)
	if action == "skip":
		return skip_tutorial(engine)
	return "Usage: tutorial [start|status|skip]"


def process_player_command(engine, cmd, verb, args, response):
	if (verb or "").lower() == "tutorial":
		return response

	player = getattr(engine, "player", None)
	state = ensure_tutorial_state(player)
	if not tutorial_is_active(state):
		return response

	step_index = int(state.get("current_step", 0) or 0)
	if step_index < 0:
		step_index = 0
	if step_index >= TUTORIAL_STEP_COUNT:
		step_index = TUTORIAL_STEP_COUNT - 1
		state["current_step"] = step_index

	if response is None:
		return _step_prompt(engine, step_index, state)

	flags = _normalize_progress_flags(state)
	active_quest = _resolve_active_tutorial_quest(engine, state)
	unmet_before = _get_unmet_requirements(state, active_quest) if active_quest else []
	_track_tutorial_command_flags(state, verb, args, response)

	if step_index == 1:
		if _is_pickup_verb(verb) and _pickup_targets_tutorial_item(args):
			flags["picked_item"] = True
		if _is_inventory_verb(verb):
			flags["checked_inventory"] = True
		if flags["picked_item"] and flags["checked_inventory"]:
			_mark_step_complete(state, step_index)
			success = _step_success(step_index)
			return _join_messages(response, success, _step_prompt(engine, state["current_step"], state))

	if step_index == 3:
		if _is_talk_to_guide(verb, args):
			flags["talked_to_guide"] = True

		response_text = str(response)
		if (verb or "").isdigit() and _is_tutorial_welcome_offer_response(response_text):
			flags["selected_quest_option"] = True
		if _is_tutorial_welcome_offer_response(response_text):
			flags["selected_quest_option"] = True

		if (
			flags["talked_to_guide"]
			and _is_quest_accept_verb(verb)
			and _tutorial_quest_accepted(engine, TUTORIAL_QUEST_ID)
		):
			# Accepting the tutorial quest confirms the offer flow even if offer text format varied.
			flags["selected_quest_option"] = True
			flags["accepted_quest"] = True
			_mark_step_complete(state, step_index)
			success = _step_success(step_index)
			return _join_messages(response, success, _step_prompt(engine, state["current_step"], state))

	if _step_matches(step_index, engine, verb, args, cmd):
		_mark_step_complete(state, step_index)
		success = _step_success(step_index)
		return _join_messages(response, success, _step_prompt(engine, state["current_step"], state))

	if step_index == 7 and active_quest:
		unmet_after = _get_unmet_requirements(state, active_quest)
		if len(unmet_after) < len(unmet_before):
			total = len(TUTORIAL_QUEST_REQUIREMENTS.get(active_quest, []))
			done = total - len(unmet_after)
			if not unmet_after:
				return _join_messages(
					response,
					"Good. All command checks for this lesson are complete. Return to the quest giver and choose [Turn in].",
				)
			if total > 0:
				return _join_messages(
					response,
					f"Good. Lesson command checks: {done}/{total} complete.",
					_step_prompt(engine, step_index, state),
				)

	response_text = str(response)
	if not response_text.strip():
		return _step_prompt(engine, step_index, state)
	if response_text.strip().lower().startswith(("unknown command", "i don't understand")):
		return _join_messages(response, _step_prompt(engine, step_index, state))
	return response