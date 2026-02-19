"""
World Builder: Bulk room creation, templates, and batch operations for the adventure game world.
Supports grid generation, room templates, copy/paste, and batch modifications.
"""

import json
import os
from typing import Dict, List, Any, Optional, Tuple
import copy

# Constants for location types
LOCATION_TYPES = {"wilderness", "settlement", "building", "transition", "dock", "island"}
EXIT_TYPES = {"direction", "named", "boat_travel"}
DIRECTIONS = {"north", "south", "east", "west"}


def load_world_data(world_file: str) -> Dict[str, Any]:
    """Load world.json safely."""
    try:
        with open(world_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"rooms": {}, "room_templates": {}}
    except Exception as e:
        raise RuntimeError(f"Failed to load world file: {e}")


def save_world_data(world_file: str, data: Dict[str, Any]) -> bool:
    """Save world.json atomically using temp file + os.replace()."""
    tmp_path = f"{world_file}.tmp"
    try:
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        os.replace(tmp_path, world_file)
        return True
    except Exception as e:
        try:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        except Exception:
            pass
        raise RuntimeError(f"Failed to save world file: {e}")


def create_room_grid(
    width: int,
    height: int,
    start_id: int,
    location_type: str,
    world_file: str,
    template_name: Optional[str] = None,
    region_name: str = "",
    connect_edges: bool = False
) -> Tuple[List[str], str]:
    """
    Generate an NxM rectangular grid of connected rooms.
    
    Args:
        width: Grid width (columns)
        height: Grid height (rows)
        start_id: Starting room ID number
        location_type: Room type (wilderness/settlement/building/transition)
        world_file: Path to world.json
        template_name: Optional template name to use for all rooms
        region_name: Prefix for room names (e.g., "dungeon", "village")
        connect_edges: Whether edge rooms wrap around (for mazes)
    
    Returns:
        Tuple of (list of created room IDs, status message)
    """
    if location_type not in LOCATION_TYPES:
        return ([], f"Invalid location_type: {location_type}")
    
    if width <= 0 or height <= 0:
        return ([], "Grid dimensions must be positive")
    
    world_data = load_world_data(world_file)
    rooms = world_data.setdefault("rooms", {})
    templates = world_data.setdefault("room_templates", {})
    
    # Validate template if specified
    if template_name and template_name not in templates:
        return ([], f"Template not found: {template_name}")
    
    created_ids = []
    room_map = {}  # (row, col) -> room_id for exit creation
    
    # Phase 1: Create all rooms
    for row in range(height):
        for col in range(width):
            room_id = str(start_id)
            start_id += 1
            
            # Create room from template or defaults
            if template_name:
                room = create_room_from_template(
                    template_name, room_id, 
                    {"number": len(created_ids) + 1, "x": col, "y": row},
                    world_file
                )
            else:
                room = {
                    "name": f"{region_name} ({row},{col})" if region_name else f"Room ({row},{col})",
                    "description": f"Room at position {row},{col}.",
                    "location_type": location_type,
                    "exits": {},
                    "items": {},
                    "actions": {}
                }
            
            room["location_type"] = location_type  # Ensure correct type
            room.setdefault("exits", {})
            rooms[room_id] = room
            room_map[(row, col)] = room_id
            created_ids.append(room_id)
    
    # Phase 2: Connect adjacent rooms
    for row in range(height):
        for col in range(width):
            room_id = room_map[(row, col)]
            room = rooms[room_id]
            
            # North
            if row > 0 or connect_edges:
                target_row = (row - 1) % height if connect_edges else row - 1
                if 0 <= target_row < height:
                    target_id = room_map[(target_row, col)]
                    room["exits"]["north"] = {"target": target_id, "type": "direction"}
            
            # South
            if row < height - 1 or connect_edges:
                target_row = (row + 1) % height if connect_edges else row + 1
                if 0 <= target_row < height:
                    target_id = room_map[(target_row, col)]
                    room["exits"]["south"] = {"target": target_id, "type": "direction"}
            
            # East
            if col < width - 1 or connect_edges:
                target_col = (col + 1) % width if connect_edges else col + 1
                if 0 <= target_col < width:
                    target_id = room_map[(row, target_col)]
                    room["exits"]["east"] = {"target": target_id, "type": "direction"}
            
            # West
            if col > 0 or connect_edges:
                target_col = (col - 1) % width if connect_edges else col - 1
                if 0 <= target_col < width:
                    target_id = room_map[(row, target_col)]
                    room["exits"]["west"] = {"target": target_id, "type": "direction"}
    
    # Save world.json
    try:
        save_world_data(world_file, world_data)
        msg = f"Created {len(created_ids)}x{len(created_ids)//width or 1} grid: {created_ids[0]} to {created_ids[-1]}"
        return (created_ids, msg)
    except Exception as e:
        return ([], f"Failed to save world: {e}")


def create_room_from_template(
    template_name: str,
    room_id: str,
    variables: Optional[Dict[str, Any]] = None,
    world_file: str = ""
) -> Dict[str, Any]:
    """
    Instantiate a room from a template with variable substitution.
    
    Args:
        template_name: Name of template in world_templates
        room_id: Unique ID for new room
        variables: Dict of {var_name: value} for template substitution
        world_file: Path to world.json (optional, for loading template)
    
    Returns:
        Room dictionary ready to add to world.json
    """
    if variables is None:
        variables = {}
    
    # Load template from world if world_file provided
    if world_file:
        world_data = load_world_data(world_file)
        templates = world_data.get("room_templates", {})
    else:
        templates = {}
    
    if template_name not in templates:
        raise ValueError(f"Template not found: {template_name}")
    
    template = templates[template_name]
    
    # Deep copy to avoid mutating original
    room = copy.deepcopy(template)
    
    # Substitute variables in name and description
    for var_name, var_value in variables.items():
        placeholder = f"{{{var_name}}}"
        value_str = str(var_value)
        room.setdefault("name", "")
        room.setdefault("description", "")
        room["name"] = room["name"].replace(placeholder, value_str)
        room["description"] = room["description"].replace(placeholder, value_str)
    
    # Ensure standard fields exist
    room.setdefault("location_type", "wilderness")
    room.setdefault("exits", {})
    room.setdefault("items", {})
    room.setdefault("actions", {})
    room.setdefault("npcs", [])
    
    return room


def copy_room(
    source_room_id: str,
    new_room_id: str,
    world_file: str,
    copy_exits: bool = False,
    save_as_template: bool = False,
    template_name: str = ""
) -> Tuple[Dict[str, Any], str]:
    """
    Deep copy an existing room to create a new one.
    
    Args:
        source_room_id: ID of room to copy
        new_room_id: ID for new room
        world_file: Path to world.json
        copy_exits: Whether to copy exit structure (default False)
        save_as_template: Save as reusable template
        template_name: Name for saved template
    
    Returns:
        Tuple of (new room dict, status message)
    """
    world_data = load_world_data(world_file)
    rooms = world_data.get("rooms", {})
    templates = world_data.setdefault("room_templates", {})
    
    if source_room_id not in rooms:
        return ({}, f"Source room not found: {source_room_id}")
    
    if new_room_id in rooms:
        return ({}, f"Room already exists: {new_room_id}")
    
    # Deep copy room
    source_room = rooms[source_room_id]
    new_room = copy.deepcopy(source_room)
    
    # Clear exits unless copying
    if not copy_exits:
        new_room["exits"] = {}
    
    # Save as template if requested
    if save_as_template:
        if not template_name:
            return ({}, "template_name required when save_as_template=True")
        
        template = copy.deepcopy(new_room)
        template.pop("exits", None)  # Templates don't include exits
        templates[template_name] = template
    
    # Add room to world and save
    rooms[new_room_id] = new_room
    
    try:
        save_world_data(world_file, world_data)
        msg = f"Room copied: {source_room_id} -> {new_room_id}"
        if save_as_template:
            msg += f" (also saved as template: {template_name})"
        return (new_room, msg)
    except Exception as e:
        return ({}, f"Failed to save world: {e}")


def batch_modify_rooms(
    room_ids: List[str],
    operation: str,
    world_file: str,
    **params
) -> Dict[str, Any]:
    """
    Apply batch operations to multiple rooms.
    
    Args:
        room_ids: List of room IDs to modify
        operation: Operation type (add_item, remove_item, add_exit, remove_exit, 
                                  modify_description, add_action, change_location_type, add_npc)
        world_file: Path to world.json
        **params: Operation-specific parameters
    
    Returns:
        Dict with keys: success_count, failed_ids, errors, details
    """
    world_data = load_world_data(world_file)
    rooms = world_data.get("rooms", {})
    
    results = {
        "success_count": 0,
        "failed_ids": [],
        "errors": [],
        "details": []
    }
    
    for room_id in room_ids:
        if room_id not in rooms:
            results["failed_ids"].append(room_id)
            results["errors"].append(f"Room not found: {room_id}")
            continue
        
        room = rooms[room_id]
        
        try:
            if operation == "add_item":
                item_name = params.get("item_name", "")
                quantity = params.get("quantity", 1)
                if not item_name:
                    raise ValueError("item_name required")
                room.setdefault("items", {})[item_name] = quantity
                results["details"].append(f"{room_id}: added {quantity}x {item_name}")
            
            elif operation == "remove_item":
                item_name = params.get("item_name", "")
                if not item_name:
                    raise ValueError("item_name required")
                room.setdefault("items", {}).pop(item_name, None)
                results["details"].append(f"{room_id}: removed {item_name}")
            
            elif operation == "add_exit":
                direction = params.get("direction") or params.get("name", "")
                target_id = params.get("target_id", "")
                exit_type = params.get("exit_type", "direction")
                display = params.get("display", "")
                transition_text = params.get("transition_text", "")
                
                if not direction or not target_id:
                    raise ValueError("direction and target_id required")
                if exit_type not in EXIT_TYPES:
                    raise ValueError(f"Invalid exit_type: {exit_type}")
                
                exit_obj = {"target": target_id, "type": exit_type}
                if display:
                    exit_obj["display"] = display
                if transition_text:
                    exit_obj["transition_text"] = transition_text
                
                room.setdefault("exits", {})[direction] = exit_obj
                results["details"].append(f"{room_id}: added exit {direction} -> {target_id}")
            
            elif operation == "remove_exit":
                direction = params.get("direction") or params.get("name", "")
                if not direction:
                    raise ValueError("direction required")
                room.setdefault("exits", {}).pop(direction, None)
                results["details"].append(f"{room_id}: removed exit {direction}")
            
            elif operation == "modify_description":
                mode = params.get("mode", "append")  # append, prepend, replace
                text = params.get("text", "")
                find_text = params.get("find_text", "")
                
                if mode == "append":
                    room["description"] = room.get("description", "") + " " + text
                elif mode == "prepend":
                    room["description"] = text + " " + room.get("description", "")
                elif mode == "replace":
                    if not find_text:
                        raise ValueError("find_text required for replace mode")
                    room["description"] = room.get("description", "").replace(find_text, text)
                
                results["details"].append(f"{room_id}: description modified ({mode})")
            
            elif operation == "add_action":
                action_name = params.get("action_name", "")
                action_data = params.get("action_data", {})
                if not action_name:
                    raise ValueError("action_name required")
                room.setdefault("actions", {})[action_name] = action_data
                results["details"].append(f"{room_id}: added action {action_name}")
            
            elif operation == "change_location_type":
                new_type = params.get("new_type", "")
                if new_type not in LOCATION_TYPES:
                    raise ValueError(f"Invalid location_type: {new_type}")
                room["location_type"] = new_type
                results["details"].append(f"{room_id}: type changed to {new_type}")
            
            elif operation == "add_npc":
                npc_name = params.get("npc_name", "")
                npc_data = params.get("npc_data", {})
                if not npc_name:
                    raise ValueError("npc_name required")
                room.setdefault("npcs", []).append({npc_name: npc_data} if npc_data else npc_name)
                results["details"].append(f"{room_id}: added NPC {npc_name}")
            
            else:
                raise ValueError(f"Unknown operation: {operation}")
            
            results["success_count"] += 1
        
        except Exception as e:
            results["failed_ids"].append(room_id)
            results["errors"].append(f"{room_id}: {str(e)}")
    
    # Save all changes
    if results["success_count"] > 0:
        try:
            save_world_data(world_file, world_data)
        except Exception as e:
            results["errors"].insert(0, f"Failed to save world: {e}")
    
    return results


def filter_rooms(
    world_file: str,
    criteria: Optional[Dict[str, Any]] = None
) -> List[str]:
    """
    Filter rooms by various criteria.
    
    Args:
        world_file: Path to world.json
        criteria: Dict with filtering conditions:
            - location_type: exact match
            - name_contains: substring match (case-insensitive)
            - has_item: item name present
            - has_npc: NPC name present
            - has_action: action name present
            - description_contains: substring in description
    
    Returns:
        List of matching room IDs
    """
    if criteria is None:
        criteria = {}
    
    world_data = load_world_data(world_file)
    rooms = world_data.get("rooms", {})
    
    matches = []
    
    for room_id, room in rooms.items():
        match = True
        
        # Check location_type
        if "location_type" in criteria:
            if room.get("location_type") != criteria["location_type"]:
                match = False
        
        # Check name contains
        if "name_contains" in criteria:
            if criteria["name_contains"].lower() not in room.get("name", "").lower():
                match = False
        
        # Check has_item
        if "has_item" in criteria:
            if criteria["has_item"] not in room.get("items", {}):
                match = False
        
        # Check has_npc
        if "has_npc" in criteria:
            npcs = room.get("npcs", [])
            if criteria["has_npc"] not in npcs and criteria["has_npc"] not in str(npcs):
                match = False
        
        # Check has_action
        if "has_action" in criteria:
            if criteria["has_action"] not in room.get("actions", {}):
                match = False
        
        # Check description contains
        if "description_contains" in criteria:
            if criteria["description_contains"].lower() not in room.get("description", "").lower():
                match = False
        
        if match:
            matches.append(room_id)
    
    return matches


def migrate_world_format(world_file: str) -> Tuple[bool, str]:
    """
    Upgrade world.json from old exit format to new format.
    Converts: "exits": {"north": "room_id"} to new format with type/display.
    
    Args:
        world_file: Path to world.json
    
    Returns:
        Tuple of (success, message)
    """
    try:
        world_data = load_world_data(world_file)
        rooms = world_data.get("rooms", {})
        
        migrated_count = 0
        
        for room_id, room in rooms.items():
            exits = room.get("exits", {})
            needs_migration = False
            
            # Check if any exit is still in old string format
            for direction, target in list(exits.items()):
                if isinstance(target, str):
                    # Old format: convert to new format
                    exits[direction] = {
                        "target": target,
                        "type": "direction" if direction in DIRECTIONS else "named"
                    }
                    needs_migration = True
                    migrated_count += 1
            
            # Ensure location_type exists
            if "location_type" not in room:
                room["location_type"] = "wilderness"
                migrated_count += 1
            
            # Ensure items, npcs, actions exist
            room.setdefault("items", {})
            room.setdefault("npcs", [])
            room.setdefault("actions", {})
        
        if migrated_count > 0:
            save_world_data(world_file, world_data)
            return (True, f"Migrated {migrated_count} items in world.json")
        else:
            return (True, "World.json already in new format")
    
    except Exception as e:
        return (False, f"Migration failed: {e}")


def add_example_templates(world_file: str) -> Tuple[bool, str]:
    """
    Add 3 example templates to world.json if they don't exist.
    
    Args:
        world_file: Path to world.json
    
    Returns:
        Tuple of (success, message)
    """
    try:
        world_data = load_world_data(world_file)
        templates = world_data.setdefault("room_templates", {})
        
        example_templates = {
            "tavern": {
                "name": "The {tavern_name}",
                "description": "A cozy tavern with wooden tables, flickering candles, and the warm aroma of roasted meat and ale. A roaring fireplace dominates one wall.",
                "location_type": "building",
                "items": {"chair": 4, "table": 2, "mug": 3},
                "npcs": ["bartender", "patron"],
                "actions": {"order_drink": {"text": "You order a drink from the barkeep."}, "sit": {"text": "You take a seat at a wooden table."}}
            },
            "forest": {
                "name": "Deep Forest - {direction}",
                "description": "Tall trees surround you, their branches forming a dense canopy above. Sunlight filters through in scattered beams. The air smells of pine and damp earth. Birds call from unseen perches.",
                "location_type": "wilderness",
                "items": {"mushroom": 2, "stick": 1, "berry": 3},
                "npcs": [],
                "actions": {"examine plants": {"text": "You examine the various plants and fungi around you. Many look edible, some dangerous."}}
            },
            "dungeon_cell": {
                "name": "Dungeon Cell {number}",
                "description": "A cramped stone cell with damp, slimy walls. Water drips from cracks in the ceiling. The air is thick with moisture and the smell of mildew. Iron bars form one wall, leading to a dark corridor beyond.",
                "location_type": "building",
                "items": {"chain": 1, "bones": 2, "torch": 1},
                "npcs": [],
                "actions": {"examine bars": {"text": "The bars are rusted but still solid. They won't be easy to break."}}
            }
        }
        
        added_count = 0
        for name, template in example_templates.items():
            if name not in templates:
                templates[name] = template
                added_count += 1
        
        if added_count > 0:
            save_world_data(world_file, world_data)
            return (True, f"Added {added_count} example templates")
        else:
            return (True, "Example templates already exist")
    
    except Exception as e:
        return (False, f"Failed to add templates: {e}")


# ============ EXAMPLE USAGE ============
if __name__ == "__main__":
    import sys
    
    world_file = os.path.join(os.path.dirname(__file__), "world.json")
    
    # Example 1: Migrate existing world
    success, msg = migrate_world_format(world_file)
    print(f"[Migrate] {msg}")
    
    # Example 2: Add example templates
    success, msg = add_example_templates(world_file)
    print(f"[Templates] {msg}")
    
    # Example 3: Create a 3x3 dungeon grid
    created, msg = create_room_grid(
        width=3,
        height=3,
        start_id=1000,
        location_type="building",
        world_file=world_file,
        template_name="dungeon_cell",
        region_name="Dungeon"
    )
    print(f"[Grid] {msg}")
    
    # Example 4: Add item to all dungeon rooms
    if created:
        results = batch_modify_rooms(
            room_ids=created,
            operation="add_item",
            world_file=world_file,
            item_name="gold coin",
            quantity=5
        )
        print(f"[Batch] Success: {results['success_count']}, Failed: {len(results['failed_ids'])}")
    
    # Example 5: Filter and modify
    forest_rooms = filter_rooms(world_file, {"location_type": "wilderness"})
    print(f"[Filter] Found {len(forest_rooms)} wilderness rooms")
