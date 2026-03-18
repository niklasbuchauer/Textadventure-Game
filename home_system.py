"""
Core home-dimension logic for the player pocket home.
"""

from home_items import HOME_ITEMS, get_home_item

HOME_ROOM_ID = "player_home"
HOME_FALLBACK_ROOM = "village_square"
HOME_GRID_WIDTH = 8
HOME_GRID_HEIGHT = 6

PLACED_ITEM_DEFAULTS = {
    "rotation": 0,
    "tint": None,
    "skin": "default",
    "texture": "default",
    "stored": False,
}

HOME_EXPANSIONS = {
    "study_annex": {"tiles": [(8, y) for y in range(0, 6)] + [(9, y) for y in range(0, 6)]},
    "training_chamber": {"tiles": [(x, 6) for x in range(0, 6)] + [(x, 7) for x in range(0, 6)]},
    "garden_room": {"tiles": [(10, y) for y in range(0, 6)] + [(11, y) for y in range(0, 6)]},
    "vault_room": {"tiles": [(x, 8) for x in range(0, 6)] + [(x, 9) for x in range(0, 6)]},
}


def build_default_home_data():
    return {
        "grid_width": HOME_GRID_WIDTH,
        "grid_height": HOME_GRID_HEIGHT,
        "placed_items": [],
        "stored_items": [],
        "unlocked_expansions": [],
        "chest_contents": {},
        "vault_contents": {},
        "active_altars": {},
    }


def _normalize_placed_item(placed):
    """Normalize placed-item data so older saves remain compatible."""
    if not isinstance(placed, dict):
        return None

    item_id = placed.get("item_id")
    if not item_id:
        return None

    try:
        x = int(placed.get("x", 0))
        y = int(placed.get("y", 0))
    except Exception:
        x, y = 0, 0

    normalized = {
        "item_id": str(item_id),
        "x": x,
        "y": y,
        "active": bool(placed.get("active", True)),
    }
    for key, default_value in PLACED_ITEM_DEFAULTS.items():
        normalized[key] = placed.get(key, default_value)
    return normalized


def ensure_player_home_state(player):
    state = player.state
    state.setdefault("home_owned", False)
    state.setdefault("home_name", "Pocket Dimension")
    state.setdefault("home_return_room", HOME_FALLBACK_ROOM)
    if not isinstance(state.get("home_data"), dict):
        state["home_data"] = build_default_home_data()
    home_data = state["home_data"]
    home_data.setdefault("grid_width", HOME_GRID_WIDTH)
    home_data.setdefault("grid_height", HOME_GRID_HEIGHT)
    placed_items = home_data.setdefault("placed_items", [])
    if not isinstance(placed_items, list):
        placed_items = []
    normalized_placed = []
    for placed in placed_items:
        normalized = _normalize_placed_item(placed)
        if normalized:
            normalized_placed.append(normalized)
    home_data["placed_items"] = normalized_placed
    home_data.setdefault("stored_items", [])

    home_data.setdefault("unlocked_expansions", [])
    home_data.setdefault("chest_contents", {})
    home_data.setdefault("vault_contents", {})
    home_data.setdefault("active_altars", {})
    state.setdefault("active_home_bonuses", {})


def reset_player_home_state(player):
    """Completely wipe home ownership and restore brand-new home defaults."""
    state = player.state
    state["home_owned"] = False
    state["home_name"] = "Pocket Dimension"
    state["home_return_room"] = HOME_FALLBACK_ROOM
    state["home_data"] = build_default_home_data()
    state["active_home_bonuses"] = {}


def is_home_room(room_id):
    if not room_id:
        return False
    return room_id == HOME_ROOM_ID or room_id.startswith(HOME_ROOM_ID + "_")


def get_unlocked_tiles(home_data):
    tiles = [(x, y) for x in range(HOME_GRID_WIDTH) for y in range(HOME_GRID_HEIGHT)]
    unlocked = home_data.get("unlocked_expansions", [])
    for expansion_id in unlocked:
        info = HOME_EXPANSIONS.get(expansion_id)
        if info:
            tiles.extend(info.get("tiles", []))
    return tiles


def _occupied_map(home_data):
    occupied = {}
    for placed in home_data.get("placed_items", []):
        occupied[(placed.get("x"), placed.get("y"))] = placed
    return occupied


def _is_wall_tile(x, y, unlocked_tiles):
    xs = [tile[0] for tile in unlocked_tiles]
    ys = [tile[1] for tile in unlocked_tiles]
    return x in (min(xs), max(xs)) or y in (min(ys), max(ys))


def find_next_free_tile(home_data, item_def=None):
    unlocked_tiles = get_unlocked_tiles(home_data)
    occupied = _occupied_map(home_data)
    wall_only = bool(item_def and item_def.get("wall_only"))

    for x, y in unlocked_tiles:
        if (x, y) in occupied:
            continue
        if wall_only and not _is_wall_tile(x, y, unlocked_tiles):
            continue
        return x, y
    return None


def place_item(home_data, item_id, x=None, y=None):
    item_def = get_home_item(item_id)
    if not item_def:
        return False, "That item cannot be placed in your home."
    if not isinstance(item_def.get("sprite"), dict):
        return False, "That item has no usable home texture and cannot be placed."

    unlocked_tiles = set(get_unlocked_tiles(home_data))
    occupied = _occupied_map(home_data)

    if x is None or y is None:
        free_tile = find_next_free_tile(home_data, item_def=item_def)
        if free_tile is None:
            return False, "No free placement tile is available."
        x, y = free_tile

    if (x, y) not in unlocked_tiles:
        return False, "That tile is outside your unlocked home space."
    if (x, y) in occupied:
        return False, "That tile is already occupied."
    if item_def.get("wall_only") and not _is_wall_tile(x, y, list(unlocked_tiles)):
        return False, "That item must be placed on a wall tile."

    home_data["placed_items"].append({
        "item_id": item_id,
        "x": int(x),
        "y": int(y),
        "active": True,
        "rotation": 0,
        "tint": None,
        "skin": "default",
        "texture": "default",
        "stored": False,
    })
    return True, f"Placed {item_def.get('name', item_id)} at ({x}, {y})."


def remove_item(home_data, item_query):
    query = item_query.strip().lower().replace(" ", "_")
    placed_items = home_data.get("placed_items", [])

    for idx, placed in enumerate(placed_items):
        item_id = placed.get("item_id", "")
        if item_id == query or query in item_id:
            removed = placed_items.pop(idx)
            return True, removed.get("item_id"), f"Removed {removed.get('item_id', 'item')} from your home."

    return False, None, "No placed item matched that name."


def _query_matches(item_id, query):
    return item_id == query or query in item_id


def find_placed_item(home_data, item_query=None, x=None, y=None):
    placed_items = home_data.get("placed_items", [])
    query = None
    if isinstance(item_query, str):
        query = item_query.strip().lower().replace(" ", "_")

    for idx, placed in enumerate(placed_items):
        px = placed.get("x")
        py = placed.get("y")
        item_id = placed.get("item_id", "")
        if x is not None and y is not None and (px, py) == (x, y):
            return idx, placed
        if query and _query_matches(item_id, query):
            return idx, placed
    return None, None


def move_item(home_data, item_query, new_x, new_y):
    idx, placed = find_placed_item(home_data, item_query=item_query)
    if placed is None:
        return False, "No placed item matched that name."

    item_def = get_home_item(placed.get("item_id")) or {}
    unlocked_tiles = set(get_unlocked_tiles(home_data))
    occupied = _occupied_map(home_data)
    old_pos = (placed.get("x"), placed.get("y"))

    if (new_x, new_y) not in unlocked_tiles:
        return False, "That tile is outside your unlocked home space."
    if (new_x, new_y) in occupied and (new_x, new_y) != old_pos:
        return False, "That tile is already occupied."
    if item_def.get("wall_only") and not _is_wall_tile(new_x, new_y, list(unlocked_tiles)):
        return False, "That item must be placed on a wall tile."

    placed["x"] = int(new_x)
    placed["y"] = int(new_y)
    return True, f"Moved {placed.get('item_id', 'item')} to ({new_x}, {new_y})."


def rotate_item(home_data, item_query, step=90):
    _, placed = find_placed_item(home_data, item_query=item_query)
    if placed is None:
        return False, "No placed item matched that name."

    current = int(placed.get("rotation", 0))
    placed["rotation"] = (current + int(step)) % 360
    return True, f"Rotated {placed.get('item_id', 'item')} to {placed['rotation']} degrees."


def recolor_item(home_data, item_query, tint):
    _, placed = find_placed_item(home_data, item_query=item_query)
    if placed is None:
        return False, "No placed item matched that name."

    cleaned = (tint or "").strip()
    placed["tint"] = cleaned if cleaned else None
    return True, f"Updated color for {placed.get('item_id', 'item')}."


def set_item_skin_texture(home_data, item_query, skin=None, texture=None):
    _, placed = find_placed_item(home_data, item_query=item_query)
    if placed is None:
        return False, "No placed item matched that name."

    if skin is not None and str(skin).strip():
        placed["skin"] = str(skin).strip().lower()
    if texture is not None and str(texture).strip():
        placed["texture"] = str(texture).strip().lower()
    return True, f"Updated appearance for {placed.get('item_id', 'item')}."


def store_item(home_data, item_query):
    idx, placed = find_placed_item(home_data, item_query=item_query)
    if placed is None:
        return False, None, "No placed item matched that name."

    stored_items = home_data.setdefault("stored_items", [])
    stored_entry = dict(placed)
    stored_entry["stored"] = True
    stored_items.append(stored_entry)
    home_data.get("placed_items", []).pop(idx)
    return True, stored_entry.get("item_id"), f"Stored {stored_entry.get('item_id', 'item')} in home storage."


def retrieve_stored_item(home_data, item_query, x=None, y=None):
    query = item_query.strip().lower().replace(" ", "_")
    stored_items = home_data.setdefault("stored_items", [])
    for idx, entry in enumerate(stored_items):
        item_id = entry.get("item_id", "")
        if not _query_matches(item_id, query):
            continue

        ok, msg = place_item(home_data, item_id, x=x, y=y)
        if not ok:
            return False, msg
        stored_items.pop(idx)
        return True, f"Retrieved {item_id} from storage."
    return False, "No stored item matched that name."


def sell_item(home_data, item_query, ratio=0.5):
    idx, placed = find_placed_item(home_data, item_query=item_query)
    if placed is None:
        return False, 0, "No placed item matched that name."

    item_id = placed.get("item_id")
    item_def = HOME_ITEMS.get(item_id, {})
    base_price = int(item_def.get("price", 0) or 0)
    value = int(round(base_price * float(ratio))) if base_price > 0 else 0
    home_data.get("placed_items", []).pop(idx)
    return True, value, f"Sold {item_id} for {value} gold."


def list_placed_items(home_data):
    placed_items = home_data.get("placed_items", [])
    if not placed_items:
        return "Your home is empty."

    lines = ["Placed home items:"]
    for placed in placed_items:
        item_id = placed.get("item_id", "unknown")
        item_def = HOME_ITEMS.get(item_id, {})
        display = item_def.get("name", item_id.replace("_", " ").title())
        lines.append(f"- {display} at ({placed.get('x')}, {placed.get('y')})")
    return "\n".join(lines)


def list_upgrades(home_data):
    unlocked = set(home_data.get("unlocked_expansions", []))
    lines = ["Home upgrades:"]
    for expansion_id in HOME_EXPANSIONS:
        status = "Unlocked" if expansion_id in unlocked else "Locked"
        lines.append(f"- {expansion_id.replace('_', ' ').title()}: {status}")
    return "\n".join(lines)


def rename_home(player, new_name):
    cleaned = (new_name or "").strip()
    if not cleaned:
        return False, "Home name cannot be empty."
    if len(cleaned) > 40:
        cleaned = cleaned[:40]
    player.state["home_name"] = cleaned
    return True, f"Your home is now named: {cleaned}"


def build_home_description(player):
    ensure_player_home_state(player)
    home_name = player.state.get("home_name", "Pocket Dimension")
    home_data = player.state.get("home_data", {})
    placed = home_data.get("placed_items", [])
    active_bonuses = player.state.get("active_home_bonuses", {})

    lines = [home_name, "A quiet pocket dimension isolated from the outside world."]
    lines.append(f"Placed objects: {len(placed)}")

    if active_bonuses:
        lines.append("Active altar effects:")
        for key, value in active_bonuses.items():
            lines.append(f"- {key}: {value}")

    if placed:
        lines.append("Notable furnishings:")
        seen = set()
        for placed_item in placed:
            item_id = placed_item.get("item_id")
            if item_id in seen:
                continue
            seen.add(item_id)
            item_def = HOME_ITEMS.get(item_id, {})
            lines.append(f"- {item_def.get('name', item_id.replace('_', ' ').title())}")

    return "\n".join(lines)


def activate_altar(player, item_id):
    item_def = HOME_ITEMS.get(item_id)
    if not item_def or item_def.get("category") != "altar":
        return False, "That object is not an altar."

    bonus = item_def.get("altar_bonus", {})
    active = player.state.setdefault("active_home_bonuses", {})
    active.clear()
    active.update(bonus)
    return True, f"You attune to {item_def.get('name', 'the altar')}."


def clear_home_run_bonuses(player):
    player.state["active_home_bonuses"] = {}
