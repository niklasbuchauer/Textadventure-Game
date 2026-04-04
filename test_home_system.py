"""Home system regression tests for core ownership and placement flows."""

from home_system import (
    HOME_GRID_WIDTH,
    HOME_GRID_HEIGHT,
    HOME_DATA_VERSION,
    build_default_home_data,
    ensure_player_home_state,
    place_item,
    remove_item,
    list_placed_items,
    list_upgrades,
    list_rooms,
    set_active_room,
    unlock_room,
    list_containers,
    store_inventory_item,
    retrieve_inventory_item,
    set_spawn_room,
    plant_garden_crop,
    harvest_garden,
    garden_status,
    reset_player_home_state,
)
from home_items import HOME_ITEMS


class MockPlayer:
    def __init__(self):
        self.stats = {"gold": 2000}
        self.inventory = {}
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
    assert player.state["home_data"]["version"] == HOME_DATA_VERSION
    assert player.state["home_data"]["active_room_id"] == "foyer"
    assert player.state["home_data"]["placed_items"] == []


def test_old_home_schema_hard_resets_to_v2():
    player = MockPlayer()
    player.state["home_data"] = {
        "grid_width": 99,
        "grid_height": 99,
        "placed_items": [{"item_id": "home_workbench", "x": 1, "y": 1}],
        "version": 1,
    }

    ensure_player_home_state(player)
    home_data = player.state["home_data"]
    assert home_data["version"] == HOME_DATA_VERSION
    assert home_data["grid_width"] == HOME_GRID_WIDTH
    assert home_data["unlocked_rooms"] == ["foyer"]
    assert home_data["placed_items"] == []


def test_room_unlock_and_switch_flow():
    player = MockPlayer()
    ensure_player_home_state(player)

    home_data = player.state["home_data"]
    assert "Foyer" in list_rooms(home_data)

    ok, msg = unlock_room(player, "workshop")
    assert ok, msg
    assert "workshop" in player.state["home_data"]["unlocked_rooms"]

    ok, msg = set_active_room(player.state["home_data"], "workshop")
    assert ok, msg
    assert player.state["home_data"]["active_room_id"] == "workshop"


def test_room_container_store_and_take_round_trip():
    player = MockPlayer()
    ensure_player_home_state(player)
    home_data = player.state["home_data"]

    assert "Foyer Cache" in list_containers(home_data)

    player.inventory["wood"] = 7
    ok, msg = store_inventory_item(player, "wood", 5)
    assert ok, msg
    assert player.inventory["wood"] == 2

    ok, msg = retrieve_inventory_item(player, "wood", 3)
    assert ok, msg
    assert player.inventory["wood"] == 5


def test_set_spawn_room_requires_unlocked_room():
    player = MockPlayer()
    ensure_player_home_state(player)
    home_data = player.state["home_data"]

    ok, msg = set_spawn_room(home_data, "bedroom")
    assert not ok
    assert "locked" in msg.lower()

    ok, msg = unlock_room(player, "bedroom")
    assert ok, msg
    ok, msg = set_spawn_room(home_data, "bedroom")
    assert ok, msg
    assert home_data["spawn_room_id"] == "bedroom"


def test_garden_plant_and_harvest_cycle():
    player = MockPlayer()
    ensure_player_home_state(player)
    home_data = player.state["home_data"]

    ok, msg = unlock_room(player, "garden")
    assert ok, msg
    ok, msg = set_active_room(home_data, "garden")
    assert ok, msg

    player.inventory["strange_herb"] = 2
    ok, msg = plant_garden_crop(player, "strange_herb", 2)
    assert ok, msg
    assert player.inventory.get("strange_herb", 0) == 0
    assert "Garden plots" in garden_status(home_data)

    for plot in home_data["garden_state"]["plots"]:
        plot["ready_at"] = 0

    ok, msg = harvest_garden(player)
    assert ok, msg
    assert player.inventory.get("strange_herb", 0) >= 2


def test_place_and_remove_item_round_trip():
    player = MockPlayer()
    ensure_player_home_state(player)
    home_data = player.state["home_data"]

    ok, msg = unlock_room(player, "workshop")
    assert ok, msg
    ok, msg = set_active_room(home_data, "workshop")
    assert ok, msg

    ok, msg = place_item(home_data, "home_workbench", 2, 1)
    assert ok, msg
    assert len(home_data["placed_items"]) == 1
    placed = home_data["placed_items"][0]
    assert placed["item_id"] == "home_workbench"
    assert placed["stored"] is False

    ok, item_id, msg = remove_item(home_data, "home_workbench")
    assert ok, msg
    assert item_id == "home_workbench"
    assert home_data["placed_items"] == []


def test_listing_helpers_are_stable():
    player = MockPlayer()
    ensure_player_home_state(player)
    home_data = player.state["home_data"]

    assert "No items placed" in list_placed_items(home_data)
    upgrades = list_upgrades(home_data)
    assert "Home room unlocks:" in upgrades
    assert "Bedroom" in upgrades


def test_reset_player_home_state_full_wipe():
    player = MockPlayer()
    ensure_player_home_state(player)
    player.state["home_owned"] = True
    player.state["home_name"] = "My Lair"
    player.state["active_home_bonuses"] = {"attack": 3}

    home_data = player.state["home_data"]
    ok, msg = unlock_room(player, "workshop")
    assert ok, msg
    ok, msg = set_active_room(home_data, "workshop")
    assert ok, msg
    ok, _ = place_item(home_data, "home_workbench", 1, 1)
    assert ok
    home_data["unlocked_expansions"].append("study_annex")

    reset_player_home_state(player)

    assert player.state["home_owned"] is False
    assert player.state["home_name"] == "Pocket Dimension"
    assert player.state["active_home_bonuses"] == {}
    assert player.state["home_data"]["placed_items"] == []
    assert player.state["home_data"]["unlocked_expansions"] == []


def test_room_restricted_item_rules():
    player = MockPlayer()
    ensure_player_home_state(player)
    home_data = player.state["home_data"]

    player.inventory["garden_planter"] = 1
    ok, msg = place_item(home_data, "garden_planter", 1, 1)
    assert not ok
    assert "Garden Planter" in msg
    assert "Garden Room" in msg

    ok, msg = unlock_room(player, "garden")
    assert ok, msg
    ok, msg = set_active_room(home_data, "garden")
    assert ok, msg
    ok, msg = place_item(home_data, "garden_planter", 1, 1)
    assert ok, msg
    assert home_data["placed_items"][0]["item_id"] == "garden_planter"


def test_every_placeable_has_room_rules():
    for item_id, data in HOME_ITEMS.items():
        if not isinstance(data, dict):
            continue
        if not isinstance(data.get("sprite"), dict):
            continue
        allowed_rooms = data.get("allowed_rooms")
        assert allowed_rooms, f"{item_id} is missing room restrictions"


if __name__ == "__main__":
    tests = [
        test_default_home_data_shape,
        test_ensure_player_home_state_sets_defaults,
        test_old_home_schema_hard_resets_to_v2,
        test_room_unlock_and_switch_flow,
        test_room_container_store_and_take_round_trip,
        test_set_spawn_room_requires_unlocked_room,
        test_garden_plant_and_harvest_cycle,
        test_place_and_remove_item_round_trip,
        test_listing_helpers_are_stable,
        test_reset_player_home_state_full_wipe,
        test_room_restricted_item_rules,
        test_every_placeable_has_room_rules,
    ]
    for test_fn in tests:
        test_fn()
        print(f"PASS: {test_fn.__name__}")
    print("All home system tests passed.")
