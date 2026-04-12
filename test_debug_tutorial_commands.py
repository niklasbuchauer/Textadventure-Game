"""Tests for debug tutorial commands: status/start/step/skip/complete/reset."""

import quest_system
import tutorial_system
from debug_commands import handle_debug_commands


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


class MockEngine:
    def __init__(self):
        self.player = MockPlayer()
        self.pending_combat = None
        self.gui = None
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


def _available_quest_ids(engine, npc_id):
    return {q.get("id") for q in engine.quest_manager.get_available_quests(npc_id)}


def test_debug_tutorial_status_before_start():
    engine = MockEngine()
    result = handle_debug_commands(engine, ["tutorial", "status"])
    assert "Tutorial Debug State:" in result
    assert "Tutorial not started" in result


def test_debug_tutorial_start_initializes_state():
    engine = MockEngine()
    result = handle_debug_commands(engine, ["tutorial", "start"])

    state = tutorial_system.ensure_tutorial_state(engine.player)
    assert "Tutorial started from the beginning" in result
    assert state["started"] is True
    assert state["current_step"] == 0
    assert state["completed_steps"] == []
    assert state["is_complete"] is False


def test_debug_tutorial_step_advances_and_marks_complete():
    engine = MockEngine()
    handle_debug_commands(engine, ["tutorial", "start"])

    result = handle_debug_commands(engine, ["tutorial", "step"])
    state = tutorial_system.ensure_tutorial_state(engine.player)

    assert "Step 0 completed" in result
    assert state["current_step"] == 1
    assert state["completed_steps"] == [0]


def test_debug_tutorial_skip_advances_without_marking_step_complete():
    engine = MockEngine()
    handle_debug_commands(engine, ["tutorial", "start"])

    result = handle_debug_commands(engine, ["tutorial", "skip"])
    state = tutorial_system.ensure_tutorial_state(engine.player)

    assert "Skipped step 0" in result
    assert state["current_step"] == 1
    assert state["completed_steps"] == []


def test_debug_tutorial_skip_advances_chapter_and_prerequisite():
    engine = MockEngine()
    handle_debug_commands(engine, ["tutorial", "start"])

    state = tutorial_system.ensure_tutorial_state(engine.player)
    state["current_step"] = tutorial_system.TUTORIAL_STEP_COUNT - 1
    state["active_tutorial_quest"] = "welcome_to_havenbrook"

    assert "tutorial_trade_routes" not in _available_quest_ids(engine, "merchant")

    result = handle_debug_commands(engine, ["tutorial", "skip"])

    assert "Advanced to next chapter" in result
    assert state["active_tutorial_quest"] == "tutorial_trade_routes"

    turned_in = engine.quest_manager.quests.get("welcome_to_havenbrook")
    assert turned_in is not None
    assert getattr(turned_in, "status", "") == quest_system.QuestState.STATUS_TURNED_IN

    assert "tutorial_trade_routes" in _available_quest_ids(engine, "merchant")


def test_debug_tutorial_complete_sets_flag():
    engine = MockEngine()
    handle_debug_commands(engine, ["tutorial", "start"])

    result = handle_debug_commands(engine, ["tutorial", "complete"])
    state = tutorial_system.ensure_tutorial_state(engine.player)

    assert "Tutorial complete" in result
    assert state["is_complete"] is True


def test_debug_tutorial_reset_clears_state_and_tutorial_quests():
    engine = MockEngine()
    handle_debug_commands(engine, ["tutorial", "start"])
    state = tutorial_system.ensure_tutorial_state(engine.player)
    state["current_step"] = tutorial_system.TUTORIAL_STEP_COUNT - 1
    handle_debug_commands(engine, ["tutorial", "skip"])

    result = handle_debug_commands(engine, ["tutorial", "reset"])

    assert "Tutorial state removed" in result
    assert "tutorial_state" not in engine.player.state
    for quest_id in tutorial_system.TUTORIAL_QUEST_CHAIN:
        assert quest_id not in engine.quest_manager.quests


def test_debug_tutorial_default_shows_status():
    engine = MockEngine()
    handle_debug_commands(engine, ["tutorial", "start"])

    result = handle_debug_commands(engine, ["tutorial"])

    assert "Tutorial Debug State:" in result
    assert "Current tutorial status:" in result


def test_debug_tutorial_usage_on_invalid_action():
    engine = MockEngine()
    result = handle_debug_commands(engine, ["tutorial", "oops"])
    assert "Usage: debug tutorial" in result


if __name__ == "__main__":
    tests = [
        test_debug_tutorial_status_before_start,
        test_debug_tutorial_start_initializes_state,
        test_debug_tutorial_step_advances_and_marks_complete,
        test_debug_tutorial_skip_advances_without_marking_step_complete,
        test_debug_tutorial_skip_advances_chapter_and_prerequisite,
        test_debug_tutorial_complete_sets_flag,
        test_debug_tutorial_reset_clears_state_and_tutorial_quests,
        test_debug_tutorial_default_shows_status,
        test_debug_tutorial_usage_on_invalid_action,
    ]
    for test_fn in tests:
        test_fn()
        print(f"PASS: {test_fn.__name__}")
    print("All debug tutorial command tests passed.")
