"""Tests for debug home command set: free, items, reset."""

from debug_commands import handle_debug_commands
from home_system import ensure_player_home_state
from home_items import HOME_ITEMS


class MockPlayer:
    def __init__(self):
        self.stats = {"gold": 0, "health": 10}
        self.inventory = {}
        self.current_room = "village_square"
        self.state = {}


class MockEngine:
    def __init__(self):
        self.player = MockPlayer()
        self.rooms = {"village_square": object()}
        self._inventory_changed = False
        self.refresh_calls = 0

    def refresh_home_room_description(self):
        self.refresh_calls += 1


def test_debug_home_free_grants_ownership():
    engine = MockEngine()
    result = handle_debug_commands(engine, ["home", "free"])

    assert "Home granted" in result
    assert engine.player.state["home_owned"] is True
    assert "home_data" in engine.player.state
    assert engine.refresh_calls >= 1


def test_debug_home_items_adds_every_home_item_once():
    engine = MockEngine()
    ensure_player_home_state(engine.player)

    result = handle_debug_commands(engine, ["home", "items"])
    assert "Added one copy of every home item" in result

    for item_id in HOME_ITEMS:
        assert engine.player.inventory.get(item_id, 0) == 1
    assert engine._inventory_changed is True


def test_debug_home_reset_full_wipe():
    engine = MockEngine()
    ensure_player_home_state(engine.player)
    engine.player.state["home_owned"] = True
    engine.player.state["home_name"] = "Custom Name"
    engine.player.state["active_home_bonuses"] = {"attack": 3}
    engine.player.state["home_data"]["placed_items"].append(
        {"item_id": "home_workbench", "x": 0, "y": 0, "active": True}
    )
    engine.player.current_room = "player_home"

    result = handle_debug_commands(engine, ["home", "reset"])

    assert "Home fully reset" in result
    assert engine.player.state["home_owned"] is False
    assert engine.player.state["home_name"] == "Pocket Dimension"
    assert engine.player.state["active_home_bonuses"] == {}
    assert engine.player.state["home_data"]["placed_items"] == []
    assert engine.player.current_room == "village_square"


def test_debug_home_usage_shown_for_missing_action():
    engine = MockEngine()
    result = handle_debug_commands(engine, ["home"])
    assert "Usage: debug home free | debug home items | debug home reset" in result


if __name__ == "__main__":
    tests = [
        test_debug_home_free_grants_ownership,
        test_debug_home_items_adds_every_home_item_once,
        test_debug_home_reset_full_wipe,
        test_debug_home_usage_shown_for_missing_action,
    ]
    for test_fn in tests:
        test_fn()
        print(f"PASS: {test_fn.__name__}")
    print("All debug home command tests passed.")
