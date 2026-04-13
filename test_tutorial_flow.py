"""Tests for the player-facing tutorial flow."""

import combat_system
import overworld_encounters
import quest_system
import tutorial_system


class MockRoom:
    def __init__(self, name="Room", items=None):
        self.name = name
        self.items = items or []


class MockPlayer:
    def __init__(self):
        self.current_room = "village_square"
        self.state = {}
        self.stats = {"gold": 0, "xp": 0, "level": 1}
        self.inventory = {}
        self.visited_rooms = set()


class MockEncounterManager:
    def __init__(self):
        self.visible_enemies = {}
        self.rooms_rolled = set()

    def scale_enemy(self, enemy_id, _level):
        if enemy_id == "training_dummy":
            return {
                "name": "Training Dummy",
                "description": "A practice target.",
                "hp": 18,
                "attack": 3,
                "defense": 1,
                "xp_reward": 6,
                "gold_reward": (0, 0),
                "loot": [],
                "abilities": ["sway"],
            }
        return None


class MockEngine:
    def __init__(self):
        self.player = MockPlayer()
        self.pending_combat = None
        self.gui = None
        self.encounter_manager = MockEncounterManager()
        self._rooms = {
            "tutorial_spawn": MockRoom("Tutorial Path", ["torch", "faded_map"]),
            "village_square": MockRoom("Havenbrook Village Square"),
            "village_shop": MockRoom("Village Shop"),
            "village_blacksmith": MockRoom("Village Blacksmith"),
            "bank_of_estoria": MockRoom("Bank of Estoria"),
            "village_training_grounds": MockRoom("Training Grounds"),
            "chapel": MockRoom("Chapel"),
        }
        self.quest_manager = quest_system.QuestManager(self)

    def get_room_data(self, room_id):
        return self._rooms.get(room_id)


def _advance_route_tutorial(engine):
    outputs = []
    outputs.append(tutorial_system.process_player_command(engine, "look", "look", [], "You look around."))
    outputs.append(tutorial_system.process_player_command(engine, "take torch", "take", ["torch"], "You take the torch."))
    outputs.append(tutorial_system.process_player_command(engine, "inventory", "inventory", [], "Inventory opened."))
    outputs.append(tutorial_system.process_player_command(engine, "go north", "go", ["north"], "You head north."))
    outputs.append(tutorial_system.process_player_command(engine, "talk tutorial_guide", "talk", ["tutorial_guide"], "You start a conversation."))
    outputs.append(tutorial_system.process_player_command(engine, "4", "4", [], "QUEST OFFER: Welcome to Havenbrook"))
    accept_result = engine.quest_manager.accept_quest("welcome_to_havenbrook")
    outputs.append(tutorial_system.process_player_command(engine, "yes", "yes", [], accept_result))
    outputs.append(tutorial_system.process_player_command(engine, "help", "help", [], "Available commands."))
    outputs.append(tutorial_system.process_player_command(engine, "shop", "shop", [], "Browsing the shop."))
    outputs.append(tutorial_system.process_player_command(engine, "go blacksmith", "go", ["blacksmith"], "You head to the blacksmith."))
    return outputs


def _satisfy_objectives(engine, quest_id):
    qdef = quest_system.QUEST_DATABASE[quest_id]
    for obj in qdef.get("objectives", []):
        otype = obj.get("type")
        if otype == "visit":
            engine.quest_manager.on_room_entered(obj["room"])
        elif otype == "talk":
            engine.quest_manager.on_npc_talked(obj["npc"])
        elif otype == "kill":
            engine.quest_manager.on_enemy_killed(obj["target"])
        elif otype == "collect":
            item = obj["item"]
            count = int(obj.get("count", 1) or 1)
            engine.player.inventory[item] = max(count, engine.player.inventory.get(item, 0))
            engine.quest_manager.on_item_changed()


def _feed_command(engine, text):
    parts = text.strip().split()
    verb = parts[0].lower() if parts else ""
    args = [p.lower() for p in parts[1:]]
    return tutorial_system.process_player_command(engine, text, verb, args, "ok")


def _advance_to_combat_drill(engine):
    tutorial_system.start_tutorial(engine)
    _advance_route_tutorial(engine)

    _satisfy_objectives(engine, "welcome_to_havenbrook")
    engine.quest_manager.turn_in_quest("welcome_to_havenbrook")

    engine.quest_manager.accept_quest("tutorial_trade_routes")
    _feed_command(engine, "shop browse")
    _feed_command(engine, "shop buy torch 10")
    _satisfy_objectives(engine, "tutorial_trade_routes")
    engine.quest_manager.turn_in_quest("tutorial_trade_routes")

    engine.quest_manager.accept_quest("tutorial_bank_basics")
    _feed_command(engine, "balance")
    _feed_command(engine, "deposit 1")
    _feed_command(engine, "withdraw 1")
    _satisfy_objectives(engine, "tutorial_bank_basics")
    engine.quest_manager.turn_in_quest("tutorial_bank_basics")

    return engine.quest_manager.accept_quest("tutorial_combat_drill")


def _advance_to_step_three(engine):
    tutorial_system.start_tutorial(engine)
    tutorial_system.process_player_command(engine, "look", "look", [], "You look around.")
    tutorial_system.process_player_command(engine, "take torch", "take", ["torch"], "You take the torch.")
    tutorial_system.process_player_command(engine, "inventory", "inventory", [], "Inventory opened.")
    tutorial_system.process_player_command(engine, "go north", "go", ["north"], "You head north.")

    state = tutorial_system.ensure_tutorial_state(engine.player)
    assert state["current_step"] == 3
    return state


def test_tutorial_starts_at_spawn_and_advances_through_route():
    engine = MockEngine()

    result = tutorial_system.start_tutorial(engine)
    route_outputs = _advance_route_tutorial(engine)
    status = tutorial_system.get_tutorial_status(engine)

    assert engine.player.current_room == tutorial_system.TUTORIAL_START_ROOM
    assert "Tutorial started from the beginning" in result
    assert "Follow the route into Havenbrook" in result
    assert "Tutorial Path" in result
    assert "Good. Reading the room" in route_outputs[0]
    assert "Picking up supplies" not in route_outputs[1]
    assert "Picking up supplies" in route_outputs[2]
    assert "Movement opens the world" in route_outputs[3]
    assert "Talking to NPCs" not in route_outputs[4]
    assert "Talking to NPCs" not in route_outputs[5]
    assert "Talking to NPCs" in route_outputs[6]
    assert "Type: help (or commands)" in route_outputs[6]
    assert "Help is always there" in route_outputs[7]
    assert "Shops are where you can stock up" in route_outputs[8]
    assert "The blacksmith is where your equipment path begins" in route_outputs[9]
    assert "Current step: 8/8" in status
    assert "Lesson: Welcome to Havenbrook" in status


def test_tutorial_skip_prevents_progression_and_replay_resets():
    engine = MockEngine()

    skip_result = tutorial_system.handle_tutorial_command(engine, ["skip"])
    response = tutorial_system.process_player_command(engine, "look", "look", [], "You look around.")
    replay_result = tutorial_system.handle_tutorial_command(engine, ["start"])

    state = engine.player.state["tutorial_state"]

    assert "Tutorial skipped" in skip_result
    assert state["skipped"] is False
    assert state["started"] is True
    assert engine.player.current_room == tutorial_system.TUTORIAL_START_ROOM
    assert response == "You look around."
    assert "Tutorial started from the beginning" in replay_result


def test_tutorial_empty_response_returns_current_prompt():
    engine = MockEngine()
    tutorial_system.start_tutorial(engine)

    response = tutorial_system.process_player_command(engine, "jorunal", "jorunal", [], "   ")

    assert isinstance(response, str)
    assert response.strip() != ""
    assert "Type: look (or l)." in response


def test_step_three_advances_with_normal_quest_offer_text():
    engine = MockEngine()
    state = _advance_to_step_three(engine)

    tutorial_system.process_player_command(
        engine,
        "talk tutorial_guide",
        "talk",
        ["tutorial_guide"],
        "You start a conversation.",
    )

    offer_response = engine.quest_manager.handle_quest_dialogue("offer", "welcome_to_havenbrook")
    tutorial_system.process_player_command(engine, "4", "4", [], offer_response)

    accept_result = engine.quest_manager.accept_quest("welcome_to_havenbrook")
    response = tutorial_system.process_player_command(engine, "yes", "yes", [], accept_result)

    assert state["current_step"] == 4
    assert state["progress_flags"]["selected_quest_option"] is True
    assert "Type: help (or commands)" in response


def test_step_three_acceptance_fallback_advances_without_offer_marker():
    engine = MockEngine()
    state = _advance_to_step_three(engine)

    tutorial_system.process_player_command(
        engine,
        "talk tutorial_guide",
        "talk",
        ["tutorial_guide"],
        "You start a conversation.",
    )

    state["progress_flags"]["selected_quest_option"] = False

    accept_result = engine.quest_manager.accept_quest("welcome_to_havenbrook")
    response = tutorial_system.process_player_command(engine, "yes", "yes", [], accept_result)

    assert state["current_step"] == 4
    assert state["progress_flags"]["selected_quest_option"] is True
    assert state["progress_flags"]["accepted_quest"] is True
    assert "Type: help (or commands)" in response


def test_first_tutorial_turn_in_advances_chain_without_finishing():
    engine = MockEngine()
    tutorial_system.start_tutorial(engine)
    _advance_route_tutorial(engine)

    _satisfy_objectives(engine, "welcome_to_havenbrook")
    turn_in_result = engine.quest_manager.turn_in_quest("welcome_to_havenbrook")
    state = engine.player.state["tutorial_state"]

    assert "QUEST COMPLETE: Welcome to Havenbrook" in turn_in_result
    assert "Next lesson unlocked: Trade Routes" in turn_in_result
    assert "Lesson: Trade Routes" in turn_in_result
    assert "Before turn-in, complete these commands:" in turn_in_result
    assert "New quest available from" not in turn_in_result
    assert state["is_complete"] is False
    assert state["active_tutorial_quest"] == "tutorial_trade_routes"


def test_tutorial_turn_in_requirement_reminder_is_player_friendly():
    engine = MockEngine()
    tutorial_system.start_tutorial(engine)
    _advance_route_tutorial(engine)

    _satisfy_objectives(engine, "welcome_to_havenbrook")
    engine.quest_manager.turn_in_quest("welcome_to_havenbrook")

    engine.quest_manager.accept_quest("tutorial_trade_routes")
    _satisfy_objectives(engine, "tutorial_trade_routes")
    reminder = engine.quest_manager.turn_in_quest("tutorial_trade_routes")

    assert "Before turning in \"Trade Routes\", complete these commands:" in reminder
    assert "tutorial command checks" not in reminder.lower()
    assert "Type: shop browse" in reminder
    assert "Type: shop buy torch 10 (or shop sell torch 1)" in reminder
    assert "Then return to the same NPC and choose [Turn in]." in reminder


def test_tutorial_final_turn_in_completes_tutorial():
    engine = MockEngine()
    combat_accept = _advance_to_combat_drill(engine)

    # Combat drill
    assert "Training target deployed" in combat_accept
    _feed_command(engine, "fight")
    _feed_command(engine, "attack")
    _feed_command(engine, "defend")
    _feed_command(engine, "analyze")
    _feed_command(engine, "reposition")
    _feed_command(engine, "interrupt")
    _feed_command(engine, "charge")
    _feed_command(engine, "guard break")
    _satisfy_objectives(engine, "tutorial_combat_drill")
    engine.quest_manager.turn_in_quest("tutorial_combat_drill")

    # Recovery check
    engine.quest_manager.accept_quest("tutorial_recovery_check")
    _feed_command(engine, "journal")
    _satisfy_objectives(engine, "tutorial_recovery_check")
    engine.quest_manager.turn_in_quest("tutorial_recovery_check")

    # Crafting kickoff
    engine.quest_manager.accept_quest("tutorial_crafting_kickoff")
    _feed_command(engine, "smelt")
    _satisfy_objectives(engine, "tutorial_crafting_kickoff")
    engine.quest_manager.turn_in_quest("tutorial_crafting_kickoff")

    # Graduation checklist
    engine.quest_manager.accept_quest("tutorial_graduation")
    _feed_command(engine, "stats")
    _feed_command(engine, "skills")
    _feed_command(engine, "save")
    _satisfy_objectives(engine, "tutorial_graduation")

    turn_in_result = engine.quest_manager.turn_in_quest("tutorial_graduation")
    state = engine.player.state["tutorial_state"]

    assert "QUEST COMPLETE: Graduation Checklist" in turn_in_result
    assert "Tutorial complete" in turn_in_result
    assert state["is_complete"] is True
    assert state["reward_claimed"] is True
    assert engine.player.stats["gold"] >= tutorial_system.REWARD_GOLD


def test_combat_drill_turn_in_requires_all_tactical_commands():
    engine = MockEngine()
    combat_accept = _advance_to_combat_drill(engine)

    assert "Training target deployed" in combat_accept
    _feed_command(engine, "fight")
    _feed_command(engine, "attack")
    _feed_command(engine, "defend")
    _satisfy_objectives(engine, "tutorial_combat_drill")

    reminder = engine.quest_manager.turn_in_quest("tutorial_combat_drill")

    assert "Before turning in \"Combat Drill\", complete these commands:" in reminder
    assert "Type: analyze" in reminder
    assert "Type: reposition" in reminder
    assert "Type: interrupt" in reminder
    assert "Type: charge" in reminder
    assert "Type: guard break" in reminder


def test_journal_text_shows_tutorial_tracker_when_active():
    engine = MockEngine()
    tutorial_system.start_tutorial(engine)

    journal_text = engine.quest_manager.get_journal_text()

    assert "TUTORIAL TRACKER" in journal_text
    assert "Lesson:" in journal_text
    assert "Step:" in journal_text


def test_persistent_dummy_can_be_reengaged():
    class EncounterPlayer:
        def __init__(self):
            self.stats = {"level": 1}

    class EncounterEngine:
        def __init__(self):
            self.player = EncounterPlayer()
            self.rooms = {
                "village_training_grounds": MockRoom("Training Grounds"),
            }
            self.fixed_dungeon_room_ids = set()

    engine = EncounterEngine()
    manager = overworld_encounters.OverworldEncounterManager(engine)
    manager.visible_enemies["village_training_grounds"] = {
        "enemy_id": "training_dummy",
        "enemy_data": {
            "id": "training_dummy",
            "name": "Training Dummy",
            "description": "A practice target.",
            "hp": 18,
            "attack": 3,
            "defense": 1,
            "xp_reward": 6,
            "gold_reward": (0, 0),
            "loot": [],
            "abilities": ["sway"],
        },
        "persistent": True,
        "reset_on_engage": True,
    }

    first = manager.engage_visible_enemy("village_training_grounds")
    second = manager.engage_visible_enemy("village_training_grounds")

    assert first is not None
    assert second is not None
    assert first["hp"] == second["hp"]
    assert "village_training_grounds" in manager.visible_enemies


def test_flee_spam_has_cooldown_penalty():
    class CombatPlayer:
        def __init__(self):
            self.stats = {
                "health": 120,
                "health_max": 120,
                "defense": 3,
                "dexterity": 0,
                "level": 1,
            }
            self.state = {}

    player = CombatPlayer()
    combat = combat_system.CombatState(
        {
            "id": "training_dummy",
            "name": "Training Dummy",
            "description": "A practice target.",
            "hp": 18,
            "attack": 4,
            "defense": 1,
            "xp_reward": 6,
            "gold_reward": (0, 0),
            "loot": [],
            "abilities": [],
        }
    )

    original_roll = combat_system.random.random
    combat_system.random.random = lambda: 0.99  # Force flee failure.
    try:
        start_hp = player.stats["health"]
        success_one, msg_one = combat_system.process_player_flee(player, combat)
        hp_after_one = player.stats["health"]
        success_two, msg_two = combat_system.process_player_flee(player, combat)
        hp_after_two = player.stats["health"]
    finally:
        combat_system.random.random = original_roll

    assert success_one is False
    assert success_two is False
    assert "cooldown for 2 turns" in msg_one
    assert "Wait" in msg_two and "trying to flee again" in msg_two
    assert hp_after_one < start_hp
    assert hp_after_two < hp_after_one


if __name__ == "__main__":
    tests = [
        test_tutorial_starts_at_spawn_and_advances_through_route,
        test_tutorial_skip_prevents_progression_and_replay_resets,
        test_tutorial_empty_response_returns_current_prompt,
        test_step_three_advances_with_normal_quest_offer_text,
        test_step_three_acceptance_fallback_advances_without_offer_marker,
        test_first_tutorial_turn_in_advances_chain_without_finishing,
        test_tutorial_turn_in_requirement_reminder_is_player_friendly,
        test_combat_drill_turn_in_requires_all_tactical_commands,
        test_journal_text_shows_tutorial_tracker_when_active,
        test_persistent_dummy_can_be_reengaged,
        test_flee_spam_has_cooldown_penalty,
        test_tutorial_final_turn_in_completes_tutorial,
    ]
    for test_fn in tests:
        test_fn()
        print(f"PASS: {test_fn.__name__}")
    print("All tutorial flow tests passed.")
