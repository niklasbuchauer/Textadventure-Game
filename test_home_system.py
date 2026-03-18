"""Home system regression tests for core ownership and placement flows."""

from home_system import (
    HOME_GRID_WIDTH,
    HOME_GRID_HEIGHT,
    build_default_home_data,
    ensure_player_home_state,
    place_item,
    remove_item,
    list_placed_items,
    list_upgrades,
    reset_player_home_state,
)


class MockPlayer:
    def __init__(self):
        self.state = {}


def test_default_home_data_shape():
    home_data = build_default_home_data()
    assert home_data["grid_width"] == HOME_GRID_WIDTH
    assert home_data["grid_height"] == HOME_GRID_HEIGHT
    assert home_data["placed_items"] == []
    assert home_data["unlocked_expansions"] == []


def test_ensure_player_home_state_sets_defaults():
    player = MockPlayer()
    ensure_player_home_state(player)

    assert player.state["home_owned"] is False
    assert player.state["home_name"] == "Pocket Dimension"
    assert isinstance(player.state["home_data"], dict)
    assert player.state["home_data"]["placed_items"] == []


def test_place_and_remove_item_round_trip():
    player = MockPlayer()
    ensure_player_home_state(player)
    home_data = player.state["home_data"]

    ok, msg = place_item(home_data, "home_workbench", 2, 1)
    assert ok, msg
    assert len(home_data["placed_items"]) == 1
    placed = home_data["placed_items"][0]
    assert placed["item_id"] == "home_workbench"
    assert placed["rotation"] == 0
    assert placed["skin"] == "default"
    assert placed["texture"] == "default"
    assert placed["stored"] is False

    ok, item_id, msg = remove_item(home_data, "home_workbench")
    assert ok, msg
    assert item_id == "home_workbench"
    assert home_data["placed_items"] == []


def test_listing_helpers_are_stable():
    player = MockPlayer()
    ensure_player_home_state(player)
    home_data = player.state["home_data"]

    assert "Your home is empty." in list_placed_items(home_data)
    upgrades = list_upgrades(home_data)
    assert "Home upgrades:" in upgrades
    assert "Study Annex" in upgrades


def test_reset_player_home_state_full_wipe():
    player = MockPlayer()
    ensure_player_home_state(player)
    player.state["home_owned"] = True
    player.state["home_name"] = "My Lair"
    player.state["active_home_bonuses"] = {"attack": 3}

    home_data = player.state["home_data"]
    ok, _ = place_item(home_data, "home_workbench", 1, 1)
    assert ok
    home_data["unlocked_expansions"].append("study_annex")

    reset_player_home_state(player)

    assert player.state["home_owned"] is False
    assert player.state["home_name"] == "Pocket Dimension"
    assert player.state["active_home_bonuses"] == {}
    assert player.state["home_data"]["placed_items"] == []
    assert player.state["home_data"]["unlocked_expansions"] == []


if __name__ == "__main__":
    tests = [
        test_default_home_data_shape,
        test_ensure_player_home_state_sets_defaults,
        test_place_and_remove_item_round_trip,
        test_listing_helpers_are_stable,
        test_reset_player_home_state_full_wipe,
    ]
    for test_fn in tests:
        test_fn()
        print(f"PASS: {test_fn.__name__}")
    print("All home system tests passed.")
