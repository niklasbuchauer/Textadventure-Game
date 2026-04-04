"""
Core home-dimension logic for the player pocket home.
"""

import time

from home_items import HOME_ITEMS, get_home_item

HOME_ROOM_ID = "player_home"
HOME_FALLBACK_ROOM = "village_square"
HOME_GRID_WIDTH = 8
HOME_GRID_HEIGHT = 6
HOME_DATA_VERSION = 2

HOME_ROOMS = {
    "foyer": {
        "name": "Foyer",
        "description": "Your entry hall and general staging space.",
        "unlock_cost": 0,
        "features": ["place", "store", "use"],
    },
    "bedroom": {
        "name": "Bedroom",
        "description": "A calm room for resting and recovery bonuses.",
        "unlock_cost": 300,
        "features": ["rest", "spawn"],
    },
    "workshop": {
        "name": "Workshop",
        "description": "Dedicated space for efficient crafting and forging.",
        "unlock_cost": 550,
        "features": ["craft", "forge", "smelt", "enchant", "alchemy"],
    },
    "storage": {
        "name": "Storage Wing",
        "description": "Bulk storage with larger containers and safer sorting.",
        "unlock_cost": 450,
        "features": ["storage"],
    },
    "trophy": {
        "name": "Trophy Hall",
        "description": "Display victories and gain passive prestige perks.",
        "unlock_cost": 700,
        "features": ["trophy"],
    },
    "garden": {
        "name": "Garden Room",
        "description": "Cultivation space for seeds, herbs, and nature resources.",
        "unlock_cost": 650,
        "features": ["garden"],
    },
}

HOME_DEFAULT_CONTAINERS = [
    {"container_id": "foyer_cache", "room_id": "foyer", "name": "Foyer Cache", "capacity": 20},
    {"container_id": "bedroom_chest", "room_id": "bedroom", "name": "Bedroom Chest", "capacity": 28},
    {"container_id": "workshop_crate", "room_id": "workshop", "name": "Workshop Supply Crate", "capacity": 35},
    {"container_id": "storage_chest", "room_id": "storage", "name": "Storage Chest", "capacity": 80},
    {"container_id": "vault_locker", "room_id": "storage", "name": "Vault Locker", "capacity": 40},
    {"container_id": "trophy_case", "room_id": "trophy", "name": "Trophy Case", "capacity": 30},
    {"container_id": "garden_crate", "room_id": "garden", "name": "Garden Crate", "capacity": 35},
]

GARDEN_DEFAULT_PLOTS = 4
GARDEN_MAX_PLOTS = 8
GARDEN_GROWTH_SECONDS = {
    "strange_herb": 120,
    "wildflower": 90,
    "wheat_bundle": 140,
    "mushroom": 160,
}

GARDEN_SEED_OUTPUT = {
    "strange_herb_seed": "strange_herb",
    "wildflower_seed": "wildflower",
    "wheat_seed": "wheat_bundle",
    "mushroom_seed": "mushroom",
}

PLACED_ITEM_DEFAULTS = {
    "stored": False,
}

HOME_EXPANSIONS = {
    "study_annex": {"tiles": [(8, y) for y in range(0, 6)] + [(9, y) for y in range(0, 6)]},
    "training_chamber": {"tiles": [(x, 6) for x in range(0, 6)] + [(x, 7) for x in range(0, 6)]},
    "garden_room": {"tiles": [(10, y) for y in range(0, 6)] + [(11, y) for y in range(0, 6)]},
    "vault_room": {"tiles": [(x, 8) for x in range(0, 6)] + [(x, 9) for x in range(0, 6)]},
}


def build_default_home_data():
    data = {
        "version": HOME_DATA_VERSION,
        "grid_width": HOME_GRID_WIDTH,
        "grid_height": HOME_GRID_HEIGHT,
        "active_room_id": "foyer",
        "spawn_room_id": "foyer",
        "unlocked_rooms": ["foyer"],
        "placed_items": [],
        "stored_items": [],
        "containers": [],
        "garden_state": {"plots": []},
        "unlocked_expansions": [],
        "chest_contents": {},
        "vault_contents": {},
        "active_altars": {},
    }
    _ensure_default_containers(data)
    return data


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
        "room_id": str(placed.get("room_id") or "foyer").strip().lower(),
        "active": bool(placed.get("active", True)),
    }
    for key, default_value in PLACED_ITEM_DEFAULTS.items():
        normalized[key] = placed.get(key, default_value)
    return normalized


def _normalized_room_id(room_id):
    return str(room_id or "foyer").strip().lower().replace(" ", "_")


def get_active_room_id(home_data):
    room_id = _normalized_room_id(home_data.get("active_room_id"))
    unlocked = set(home_data.get("unlocked_rooms", []))
    if room_id not in unlocked:
        return "foyer"
    return room_id


def _ensure_default_containers(home_data):
    containers = home_data.setdefault("containers", [])
    if not isinstance(containers, list):
        containers = []
    home_data["containers"] = containers

    unlocked = set(home_data.get("unlocked_rooms", []))
    existing_ids = {c.get("container_id") for c in containers if isinstance(c, dict)}
    for template in HOME_DEFAULT_CONTAINERS:
        if template["room_id"] not in unlocked:
            continue
        if template["container_id"] in existing_ids:
            continue
        containers.append({
            "container_id": template["container_id"],
            "room_id": template["room_id"],
            "name": template["name"],
            "capacity": int(template["capacity"]),
            "items": {},
        })


def _items_in_container(container):
    items = container.setdefault("items", {})
    if not isinstance(items, dict):
        items = {}
    container["items"] = items
    return items


def _container_used_slots(container):
    items = _items_in_container(container)
    return sum(max(0, int(v)) for v in items.values())


def _ensure_garden_state(home_data):
    garden = home_data.setdefault("garden_state", {})
    if not isinstance(garden, dict):
        garden = {}
        home_data["garden_state"] = garden

    plots = garden.setdefault("plots", [])
    if not isinstance(plots, list):
        plots = []
        garden["plots"] = plots

    max_plots = min(GARDEN_MAX_PLOTS, GARDEN_DEFAULT_PLOTS + max(0, len(home_data.get("unlocked_rooms", [])) - 1))
    if len(plots) > max_plots:
        garden["plots"] = plots[:max_plots]
    return garden


def _garden_output_from_seed(seed_item_id):
    sid = str(seed_item_id or "").strip().lower().replace(" ", "_")
    if sid in GARDEN_SEED_OUTPUT:
        return GARDEN_SEED_OUTPUT[sid]
    if sid.endswith("_seed") and len(sid) > 5:
        return sid[:-5]
    if sid in GARDEN_GROWTH_SECONDS:
        return sid
    return None


def _first_container_for_room(home_data, room_id):
    room_id = _normalized_room_id(room_id)
    for container in home_data.get("containers", []):
        if container.get("room_id") == room_id:
            return container
    return None


def _allowed_rooms_for_item(item_def):
    allowed = item_def.get("allowed_rooms") if isinstance(item_def, dict) else None
    if not allowed:
        return None
    normalized = []
    for room_id in allowed:
        room_key = _normalized_room_id(room_id)
        if room_key in HOME_ROOMS:
            normalized.append(room_key)
    return normalized or None


def _format_room_list(room_ids):
    names = []
    for room_id in room_ids:
        room_name = HOME_ROOMS.get(room_id, {}).get("name", room_id)
        names.append(room_name)
    return ", ".join(names)


def _check_item_room_restriction(item_def, room_id):
    allowed_rooms = _allowed_rooms_for_item(item_def)
    if not allowed_rooms:
        return True, None

    room_id = _normalized_room_id(room_id)
    if room_id in allowed_rooms:
        return True, None

    item_name = item_def.get("name", "that item") if isinstance(item_def, dict) else "that item"
    allowed_text = _format_room_list(allowed_rooms)
    return False, f"{item_name} can only be placed in: {allowed_text}."


def ensure_player_home_state(player):
    state = player.state
    state.setdefault("home_owned", False)
    state.setdefault("home_name", "Pocket Dimension")
    state.setdefault("home_return_room", HOME_FALLBACK_ROOM)
    if not isinstance(state.get("home_data"), dict):
        state["home_data"] = build_default_home_data()
    elif int(state["home_data"].get("version", 0) or 0) != HOME_DATA_VERSION:
        # User-selected behavior: hard-reset old home schema to the new model.
        state["home_data"] = build_default_home_data()
    home_data = state["home_data"]
    home_data["version"] = HOME_DATA_VERSION
    home_data.setdefault("grid_width", HOME_GRID_WIDTH)
    home_data.setdefault("grid_height", HOME_GRID_HEIGHT)
    home_data.setdefault("active_room_id", "foyer")
    unlocked_rooms = home_data.setdefault("unlocked_rooms", ["foyer"])
    if not isinstance(unlocked_rooms, list):
        unlocked_rooms = ["foyer"]
    unlocked_rooms = [_normalized_room_id(r) for r in unlocked_rooms if _normalized_room_id(r) in HOME_ROOMS]
    if "foyer" not in unlocked_rooms:
        unlocked_rooms.insert(0, "foyer")
    home_data["unlocked_rooms"] = list(dict.fromkeys(unlocked_rooms))
    home_data["spawn_room_id"] = _normalized_room_id(home_data.get("spawn_room_id") or "foyer")
    if home_data["spawn_room_id"] not in home_data["unlocked_rooms"]:
        home_data["spawn_room_id"] = "foyer"

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
    for stored in home_data.get("stored_items", []):
        if isinstance(stored, dict):
            stored.setdefault("room_id", get_active_room_id(home_data))

    home_data.setdefault("unlocked_expansions", [])
    home_data.setdefault("chest_contents", {})
    home_data.setdefault("vault_contents", {})
    home_data.setdefault("active_altars", {})
    _ensure_default_containers(home_data)
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
    # Tile unlocks are currently room-local; all unlocked rooms share base footprint.
    # Expansion IDs are retained only for legacy compatibility.
    tiles = [(x, y) for x in range(HOME_GRID_WIDTH) for y in range(HOME_GRID_HEIGHT)]
    unlocked = home_data.get("unlocked_expansions", [])
    for expansion_id in unlocked:
        info = HOME_EXPANSIONS.get(expansion_id)
        if info:
            tiles.extend(info.get("tiles", []))
    return tiles


def _occupied_map(home_data):
    room_id = get_active_room_id(home_data)
    occupied = {}
    for placed in home_data.get("placed_items", []):
        if _normalized_room_id(placed.get("room_id")) != room_id:
            continue
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

    active_room = get_active_room_id(home_data)
    ok, msg = _check_item_room_restriction(item_def, active_room)
    if not ok:
        return False, msg

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
        "room_id": get_active_room_id(home_data),
        "active": True,
        "stored": False,
    })
    return True, f"Placed {item_def.get('name', item_id)} at ({x}, {y})."


def remove_item(home_data, item_query):
    query = item_query.strip().lower().replace(" ", "_")
    placed_items = home_data.get("placed_items", [])
    active_room = get_active_room_id(home_data)

    for idx, placed in enumerate(placed_items):
        if _normalized_room_id(placed.get("room_id")) != active_room:
            continue
        item_id = placed.get("item_id", "")
        if item_id == query or query in item_id:
            removed = placed_items.pop(idx)
            return True, removed.get("item_id"), f"Removed {removed.get('item_id', 'item')} from your home."

    return False, None, "No placed item matched that name."


def _query_matches(item_id, query):
    return item_id == query or query in item_id


def find_placed_item(home_data, item_query=None, x=None, y=None):
    placed_items = home_data.get("placed_items", [])
    active_room = get_active_room_id(home_data)
    query = None
    if isinstance(item_query, str):
        query = item_query.strip().lower().replace(" ", "_")

    for idx, placed in enumerate(placed_items):
        if _normalized_room_id(placed.get("room_id")) != active_room:
            continue
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
    ok, msg = _check_item_room_restriction(item_def, get_active_room_id(home_data))
    if not ok:
        return False, msg
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


def store_item(home_data, item_query):
    idx, placed = find_placed_item(home_data, item_query=item_query)
    if placed is None:
        return False, None, "No placed item matched that name."

    stored_items = home_data.setdefault("stored_items", [])
    stored_entry = dict(placed)
    stored_entry["stored"] = True
    stored_entry["room_id"] = get_active_room_id(home_data)
    stored_items.append(stored_entry)
    home_data.get("placed_items", []).pop(idx)
    return True, stored_entry.get("item_id"), f"Stored {stored_entry.get('item_id', 'item')} in home storage."


def retrieve_stored_item(home_data, item_query, x=None, y=None):
    query = item_query.strip().lower().replace(" ", "_")
    active_room = get_active_room_id(home_data)
    stored_items = home_data.setdefault("stored_items", [])
    for idx, entry in enumerate(stored_items):
        if _normalized_room_id(entry.get("room_id")) != active_room:
            continue
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
    active_room = get_active_room_id(home_data)
    placed_items = [p for p in home_data.get("placed_items", []) if _normalized_room_id(p.get("room_id")) == active_room]
    if not placed_items:
        return f"No items placed in {HOME_ROOMS[active_room]['name']} yet."

    lines = [f"Placed items in {HOME_ROOMS[active_room]['name']}:"]
    for placed in placed_items:
        item_id = placed.get("item_id", "unknown")
        item_def = HOME_ITEMS.get(item_id, {})
        display = item_def.get("name", item_id.replace("_", " ").title())
        lines.append(f"- {display} at ({placed.get('x')}, {placed.get('y')})")
    return "\n".join(lines)


def list_upgrades(home_data):
    unlocked = set(home_data.get("unlocked_rooms", []))
    lines = ["Home room unlocks:"]
    for room_id, info in HOME_ROOMS.items():
        status = "Unlocked" if room_id in unlocked else f"Locked ({info['unlock_cost']}g)"
        lines.append(f"- {info['name']}: {status}")
    return "\n".join(lines)


def list_rooms(home_data):
    unlocked = set(home_data.get("unlocked_rooms", []))
    active_room = get_active_room_id(home_data)
    lines = ["Home rooms:"]
    for room_id, info in HOME_ROOMS.items():
        marker = "*" if room_id == active_room else " "
        status = "Unlocked" if room_id in unlocked else f"Locked ({info['unlock_cost']}g)"
        lines.append(f"{marker} {room_id:8s} {info['name']:14s} {status}")
    lines.append("Use: home room <room_id> to switch rooms.")
    lines.append("Use: home unlock <room_id> to unlock a room.")
    return "\n".join(lines)


def set_active_room(home_data, room_id):
    normalized = _normalized_room_id(room_id)
    if normalized not in HOME_ROOMS:
        return False, f"Unknown room '{room_id}'. Use 'home rooms' to list valid IDs."
    unlocked = set(home_data.get("unlocked_rooms", []))
    if normalized not in unlocked:
        return False, f"{HOME_ROOMS[normalized]['name']} is locked. Use 'home unlock {normalized}'."
    home_data["active_room_id"] = normalized
    return True, f"Moved to {HOME_ROOMS[normalized]['name']}."


def unlock_room(player, room_id):
    ensure_player_home_state(player)
    home_data = player.state.get("home_data", {})
    normalized = _normalized_room_id(room_id)
    if normalized not in HOME_ROOMS:
        return False, f"Unknown room '{room_id}'."
    unlocked = set(home_data.get("unlocked_rooms", []))
    if normalized in unlocked:
        return False, f"{HOME_ROOMS[normalized]['name']} is already unlocked."

    cost = int(HOME_ROOMS[normalized].get("unlock_cost", 0) or 0)
    gold = int(player.stats.get("gold", 0) or 0)
    if gold < cost:
        return False, f"You need {cost} gold to unlock {HOME_ROOMS[normalized]['name']}."

    player.stats["gold"] = gold - cost
    home_data.setdefault("unlocked_rooms", []).append(normalized)
    _ensure_default_containers(home_data)
    _ensure_garden_state(home_data)
    return True, f"Unlocked {HOME_ROOMS[normalized]['name']} for {cost} gold."


def set_spawn_room(home_data, room_id):
    normalized = _normalized_room_id(room_id)
    if normalized not in HOME_ROOMS:
        return False, f"Unknown room '{room_id}'."
    unlocked = set(home_data.get("unlocked_rooms", []))
    if normalized not in unlocked:
        return False, f"{HOME_ROOMS[normalized]['name']} is locked. Unlock it first."
    home_data["spawn_room_id"] = normalized
    return True, f"Home spawn room set to {HOME_ROOMS[normalized]['name']}."


def list_containers(home_data, room_id=None):
    room_id = _normalized_room_id(room_id or get_active_room_id(home_data))
    lines = [f"Containers in {HOME_ROOMS.get(room_id, {}).get('name', room_id)}:"]
    any_rows = False
    for c in home_data.get("containers", []):
        if c.get("room_id") != room_id:
            continue
        used = _container_used_slots(c)
        cap = int(c.get("capacity", 0) or 0)
        lines.append(f"- {c.get('container_id')} ({c.get('name')}): {used}/{cap} slots")
        items = _items_in_container(c)
        if items:
            for item_id, qty in sorted(items.items()):
                lines.append(f"    {item_id} x{qty}")
        any_rows = True
    if not any_rows:
        lines.append("- No containers are available in this room yet.")
    return "\n".join(lines)


def store_inventory_item(player, item_id, quantity=1, room_id=None, container_id=None):
    ensure_player_home_state(player)
    home_data = player.state.get("home_data", {})
    room_id = _normalized_room_id(room_id or get_active_room_id(home_data))
    qty = max(1, int(quantity or 1))
    item_id = str(item_id or "").strip().lower().replace(" ", "_")
    if not item_id:
        return False, "Choose an item to store."

    inv = getattr(player, "inventory", {})
    have = int(inv.get(item_id, 0) or 0)
    if have < qty:
        return False, f"You only have {have}x {item_id}."

    target = None
    if container_id:
        cid = str(container_id).strip().lower()
        for c in home_data.get("containers", []):
            if c.get("container_id") == cid and c.get("room_id") == room_id:
                target = c
                break
    else:
        target = _first_container_for_room(home_data, room_id)

    if not target:
        return False, "No container is available in this room."

    used = _container_used_slots(target)
    cap = int(target.get("capacity", 0) or 0)
    free = max(0, cap - used)
    if free <= 0:
        return False, f"{target.get('name', 'Container')} is full."

    moved = min(qty, free)
    items = _items_in_container(target)
    items[item_id] = int(items.get(item_id, 0) or 0) + moved
    inv[item_id] = have - moved
    if inv[item_id] <= 0:
        inv.pop(item_id, None)

    if moved < qty:
        return True, f"Stored {moved}/{qty} {item_id} in {target.get('name')} (container full)."
    return True, f"Stored {moved} {item_id} in {target.get('name')}."


def retrieve_inventory_item(player, item_id, quantity=1, room_id=None, container_id=None):
    ensure_player_home_state(player)
    home_data = player.state.get("home_data", {})
    room_id = _normalized_room_id(room_id or get_active_room_id(home_data))
    qty = max(1, int(quantity or 1))
    item_id = str(item_id or "").strip().lower().replace(" ", "_")
    if not item_id:
        return False, "Choose an item to retrieve."

    candidates = []
    if container_id:
        cid = str(container_id).strip().lower()
        for c in home_data.get("containers", []):
            if c.get("container_id") == cid and c.get("room_id") == room_id:
                candidates.append(c)
                break
    else:
        candidates = [c for c in home_data.get("containers", []) if c.get("room_id") == room_id]

    if not candidates:
        return False, "No container is available in this room."

    for c in candidates:
        items = _items_in_container(c)
        have = int(items.get(item_id, 0) or 0)
        if have <= 0:
            continue
        moved = min(qty, have)
        items[item_id] = have - moved
        if items[item_id] <= 0:
            items.pop(item_id, None)
        inv = getattr(player, "inventory", {})
        inv[item_id] = int(inv.get(item_id, 0) or 0) + moved
        return True, f"Retrieved {moved} {item_id} from {c.get('name')}"
    return False, f"No stored '{item_id}' found in this room's containers."


def garden_status(home_data):
    active_room = get_active_room_id(home_data)
    if active_room != "garden":
        return "Switch to the Garden Room first: home room garden"

    if "garden" not in set(home_data.get("unlocked_rooms", [])):
        return "Garden Room is locked. Use: home unlock garden"

    garden = _ensure_garden_state(home_data)
    plots = garden.get("plots", [])
    max_plots = min(GARDEN_MAX_PLOTS, GARDEN_DEFAULT_PLOTS + max(0, len(home_data.get("unlocked_rooms", [])) - 1))
    now = int(time.time())

    lines = [f"Garden plots: {len(plots)}/{max_plots}"]
    if not plots:
        lines.append("- No crops planted.")
        lines.append("Use: home plant <seed_or_crop> [qty]")
        return "\n".join(lines)

    for i, plot in enumerate(plots, start=1):
        crop = plot.get("crop_id", "unknown")
        qty = int(plot.get("yield_qty", 1) or 1)
        ready_at = int(plot.get("ready_at", 0) or 0)
        if now >= ready_at:
            lines.append(f"- Plot {i}: {crop} x{qty} (ready)")
        else:
            remaining = max(1, ready_at - now)
            lines.append(f"- Plot {i}: {crop} x{qty} (ready in {remaining}s)")
    lines.append("Use: home harvest")
    return "\n".join(lines)


def plant_garden_crop(player, seed_item_id, quantity=1):
    ensure_player_home_state(player)
    home_data = player.state.get("home_data", {})
    active_room = get_active_room_id(home_data)
    if active_room != "garden":
        return False, "Switch to the Garden Room first: home room garden"
    if "garden" not in set(home_data.get("unlocked_rooms", [])):
        return False, "Garden Room is locked. Use: home unlock garden"

    crop_id = _garden_output_from_seed(seed_item_id)
    if not crop_id:
        return False, "That item cannot be planted in the garden."

    inv = getattr(player, "inventory", {})
    seed_id = str(seed_item_id or "").strip().lower().replace(" ", "_")
    qty = max(1, int(quantity or 1))
    have = int(inv.get(seed_id, 0) or 0)
    if have < qty:
        return False, f"You only have {have}x {seed_id}."

    garden = _ensure_garden_state(home_data)
    plots = garden.setdefault("plots", [])
    max_plots = min(GARDEN_MAX_PLOTS, GARDEN_DEFAULT_PLOTS + max(0, len(home_data.get("unlocked_rooms", [])) - 1))
    free = max(0, max_plots - len(plots))
    if free <= 0:
        return False, "All garden plots are occupied. Harvest before planting more."

    plant_count = min(qty, free)
    grow_seconds = int(GARDEN_GROWTH_SECONDS.get(crop_id, 120))
    now = int(time.time())

    for _ in range(plant_count):
        plots.append({
            "seed_item_id": seed_id,
            "crop_id": crop_id,
            "planted_at": now,
            "ready_at": now + grow_seconds,
            "yield_qty": 1,
        })

    inv[seed_id] = have - plant_count
    if inv[seed_id] <= 0:
        inv.pop(seed_id, None)

    if plant_count < qty:
        return True, f"Planted {plant_count}/{qty} {seed_id}. Garden is now full."
    return True, f"Planted {plant_count} {seed_id} in the garden."


def harvest_garden(player):
    ensure_player_home_state(player)
    home_data = player.state.get("home_data", {})
    active_room = get_active_room_id(home_data)
    if active_room != "garden":
        return False, "Switch to the Garden Room first: home room garden"

    garden = _ensure_garden_state(home_data)
    plots = garden.setdefault("plots", [])
    if not plots:
        return False, "No crops are planted right now."

    now = int(time.time())
    ready = [p for p in plots if int(p.get("ready_at", 0) or 0) <= now]
    if not ready:
        return False, "Nothing is ready to harvest yet."

    inv = getattr(player, "inventory", {})
    harvested = {}
    remaining = []
    for plot in plots:
        if int(plot.get("ready_at", 0) or 0) > now:
            remaining.append(plot)
            continue
        crop = str(plot.get("crop_id", "")).strip().lower()
        qty = max(1, int(plot.get("yield_qty", 1) or 1))
        if not crop:
            continue
        inv[crop] = int(inv.get(crop, 0) or 0) + qty
        harvested[crop] = int(harvested.get(crop, 0) or 0) + qty

    garden["plots"] = remaining
    if not harvested:
        return False, "No valid crops were harvested."

    parts = [f"{item_id} x{qty}" for item_id, qty in sorted(harvested.items())]
    return True, "Harvested: " + ", ".join(parts)


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
    active_room = get_active_room_id(home_data)
    placed = [p for p in home_data.get("placed_items", []) if _normalized_room_id(p.get("room_id")) == active_room]
    active_bonuses = player.state.get("active_home_bonuses", {})

    lines = [home_name, "A quiet pocket dimension isolated from the outside world."]
    lines.append(f"Current room: {HOME_ROOMS[active_room]['name']}")
    lines.append(f"Placed objects: {len(placed)}")
    unlocked_count = len(set(home_data.get("unlocked_rooms", [])))
    lines.append(f"Unlocked rooms: {unlocked_count}/{len(HOME_ROOMS)}")

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
