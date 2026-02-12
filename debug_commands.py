"""Debug commands for testing and development."""


def handle_debug_commands(engine, args):
    """Handle debug commands."""
    if not args:
        return _show_debug_menu()
    
    subcommand = args[0].lower()
    
    if subcommand == "reveal":
        if len(args) > 1 and args[1].lower() == "map":
            return _debug_reveal_map(engine)
        return "Usage: debug reveal map"
    elif subcommand == "hide":
        if len(args) > 1 and args[1].lower() == "map":
            return _debug_hide_map(engine)
        return "Usage: debug hide map"
    elif subcommand == "teleport":
        if len(args) > 1:
            return _debug_teleport(engine, args[1])
        return "Usage: debug teleport <room_id>"
    elif subcommand == "heal":
        return _debug_heal(engine)
    elif subcommand == "rooms":
        page = 1
        if len(args) > 1:
            try:
                page = int(args[1])
            except ValueError:
                page = 1
        return _debug_list_rooms(engine, page)
    elif subcommand == "gold":
        if len(args) > 1:
            return _debug_set_gold(engine, args[1])
        return "Usage: debug gold <amount>"
    elif subcommand == "items":
        return _debug_list_items(engine)
    elif subcommand == "stats":
        return _debug_show_stats(engine)
    elif subcommand == "dungeon":
        if len(args) < 2:
            return "Usage: debug dungeon open"
        action = args[1].lower()
        if action == "open":
            return _debug_dungeon_open(engine)
        return "Usage: debug dungeon open"
    else:
        return f"Unknown debug command: {subcommand}\n{_show_debug_menu()}"


def _show_debug_menu():
    """Return the debug commands menu."""
    return """
=== DEBUG MENU ===
Available debug commands:

  debug reveal map       - Show all rooms on map
  debug hide map         - Hide unvisited rooms
  debug teleport <id>    - Teleport to a room
  debug dungeon open     - Force open dungeon for testing
  debug heal             - Restore health
  debug rooms [page]     - List rooms (paginated)
  debug gold <amount>    - Set gold
  debug items            - Show inventory
  debug stats            - Show player stats

Example: debug teleport mountain_peak
Example: debug dungeon open
Example: debug rooms 1 (world) | debug rooms 2 (dungeon)
""".strip()


def _debug_reveal_map(engine):
    """Reveal all rooms on the map."""
    if hasattr(engine, 'map_window') and engine.map_window:
        engine.map_window.reveal_all = True
        if engine.map_window.is_open():
            engine.map_window.redraw_map()
        return "Map revealed: All rooms visible"
    return "Map window not open. Use 'open map' first."


def _debug_hide_map(engine):
    """Hide unvisited rooms on the map."""
    if hasattr(engine, 'map_window') and engine.map_window:
        engine.map_window.reveal_all = False
        if engine.map_window.is_open():
            engine.map_window.redraw_map()
        return "Map hidden: Only visited rooms visible"
    return "Map window not open. Use 'open map' first."


def _debug_teleport(engine, room_id):
    """Teleport the player to a specific room (world or dungeon)."""
    # Check world rooms first
    if room_id in engine.rooms:
        room = engine.rooms[room_id]
    # Check dungeon rooms
    elif hasattr(engine, 'current_dungeon_instance') and engine.current_dungeon_instance:
        # Try to find room in dungeon
        room = engine.get_room_data(room_id)
        if not room:
            return f"Room '{room_id}' not found in world or dungeon."
    else:
        return f"Room '{room_id}' not found."
    
    if hasattr(engine.player, 'visited_rooms'):
        engine.player.visited_rooms.add(room_id)
    
    engine.player.current_room = room_id
    
    if hasattr(engine, 'map_window') and engine.map_window:
        if hasattr(engine.player, 'visited_rooms'):
            engine.map_window.update_location(room_id, engine.player.visited_rooms)
    
    if hasattr(room, 'name'):
        room_name = room.name
    else:
        room_name = room.get('name', room_id) if isinstance(room, dict) else room_id
    
    return f"✓ Teleported to {room_name}!"


def _debug_heal(engine):
    """Restore player to full health."""
    if engine.player:
        engine.player.stats['health'] = 100
        return "Health restored to 100!"
    return "No player found"


def _debug_list_rooms(engine, page=1):
    """List available rooms with pagination. 
    Page 1: World rooms, Pages 2+: Dungeon rooms by floor.
    Dynamically calculates total pages based on actual room count.
    """
    rooms_per_page = 15
    
    # First, calculate total pages needed for both world and dungeon
    world_rooms = sorted(engine.rooms.keys())
    world_pages = (len(world_rooms) + rooms_per_page - 1) // rooms_per_page if world_rooms else 1
    
    dungeon_pages = 0
    if hasattr(engine, 'current_dungeon_instance') and engine.current_dungeon_instance:
        dungeon = engine.current_dungeon_instance
        if dungeon.dungeon_data:
            dungeon_rooms_count = 0
            for floor_num in dungeon.dungeon_data.get("floors", {}).keys():
                floor_data = dungeon.dungeon_data["floors"][floor_num]
                dungeon_rooms_count += len(floor_data.get("rooms", {}))
            dungeon_pages = (dungeon_rooms_count + rooms_per_page - 1) // rooms_per_page if dungeon_rooms_count > 0 else 0
    
    total_pages = world_pages + dungeon_pages
    
    # Validate page number
    if page < 1 or page > total_pages:
        return f"Invalid page. Total pages: {total_pages}\nUse: debug rooms 1 (for world rooms) or debug rooms 2+ (for dungeon rooms)"
    
    # PAGE 1+: World rooms
    if page <= world_pages:
        if not world_rooms:
            return "No world rooms found"
        
        start_idx = (page - 1) * rooms_per_page
        end_idx = start_idx + rooms_per_page
        page_rooms = world_rooms[start_idx:end_idx]
        
        room_list = []
        for room_id in page_rooms:
            room = engine.rooms[room_id]
            if hasattr(room, 'name'):
                room_name = room.name
            else:
                room_name = room.get('name', 'Unknown')
            room_list.append(f"  {room_id:35s} - {room_name}")
        
        result = "═" * 80 + "\n"
        result += f"WORLD ROOMS (Page {page}/{world_pages})\n"
        result += "═" * 80 + "\n"
        result += "\n".join(room_list)
        result += f"\n\n{'─' * 80}\n"
        result += f"Page {page} of {total_pages} (showing {len(page_rooms)} rooms)\n"
        
        nav_text = "Navigation: "
        if page > 1:
            nav_text += f"debug rooms {page-1} (prev) | "
        if page < total_pages:
            nav_text += f"debug rooms {page+1} (next)"
        else:
            nav_text += "(last page)"
        
        result += nav_text + "\n"
        return result
    
    # PAGES 2+: Dungeon rooms organized by floor
    else:
        if not hasattr(engine, 'current_dungeon_instance') or not engine.current_dungeon_instance:
            return "No dungeon loaded. Use 'debug dungeon open' first."
        
        dungeon = engine.current_dungeon_instance
        if not dungeon.dungeon_data:
            return "Dungeon data not available."
        
        # Collect all dungeon rooms
        dungeon_rooms = []
        for floor_num in sorted(dungeon.dungeon_data.get("floors", {}).keys()):
            floor_data = dungeon.dungeon_data["floors"][floor_num]
            for room_id in sorted(floor_data.get("rooms", {}).keys()):
                room_data = floor_data["rooms"][room_id]
                dungeon_rooms.append((floor_num, room_id, room_data))
        
        if not dungeon_rooms:
            return "No dungeon rooms found."
        
        # Calculate page within dungeon section
        dungeon_page_num = page - world_pages
        start_idx = (dungeon_page_num - 1) * rooms_per_page
        end_idx = start_idx + rooms_per_page
        page_rooms = dungeon_rooms[start_idx:end_idx]
        
        result = "═" * 80 + "\n"
        result += f"DUNGEON ROOMS (Page {page}/{total_pages})\n"
        result += "═" * 80 + "\n\n"
        
        current_floor = None
        for floor_num, room_id, room_data in page_rooms:
            if current_floor != floor_num:
                if current_floor is not None:
                    result += "\n"
                result += f"┌─ FLOOR {floor_num} ─────────────────────────────────────────────────────────┐\n"
                current_floor = floor_num
            
            room_name = room_data.get('name', 'Unknown')
            result += f"  {room_id:40s} - {room_name}\n"
        
        result += f"\n{'─' * 80}\n"
        result += f"Page {page} of {total_pages} (showing {len(page_rooms)} rooms)\n"
        
        nav_text = "Navigation: "
        if page > 1:
            nav_text += f"debug rooms {page-1} (prev) | "
        if page < total_pages:
            nav_text += f"debug rooms {page+1} (next)"
        else:
            nav_text += "(last page)"
        
        result += nav_text + "\n"
        return result


def _debug_set_gold(engine, amount):
    """Set player gold amount."""
    try:
        gold_amount = int(amount)
        if engine.player:
            engine.player.stats['gold'] = gold_amount
            return f"Gold set to {gold_amount}"
        return "No player found"
    except ValueError:
        return f"Invalid amount: {amount}"


def _debug_list_items(engine):
    """Show player inventory."""
    if not engine.player:
        return "No player found"
    
    inventory = engine.player.inventory
    if not inventory:
        return "Your inventory is empty"
    
    items = []
    for item, qty in inventory.items():
        items.append(f"  {item}: {qty}")
    
    return "Your inventory:\n" + "\n".join(items)


def _debug_show_stats(engine):
    """Display player stats."""
    if not engine.player:
        return "No player found"
    
    stats = engine.player.stats
    inventory = engine.player.inventory
    
    msg = f"""
=== PLAYER STATS ===
Health:   {stats.get('health', 0)}/100
Gold:     {stats.get('gold', 0)}
Location: {engine.player.current_room}

Inventory ({len(inventory)} items):
"""
    
    if inventory:
        for item, qty in sorted(inventory.items()):
            msg += f"  {item}: {qty}\n"
    else:
        msg += "  (empty)\n"
    
    return msg


def _debug_dungeon_open(engine):
    """Force open a dungeon for debug purposes using the closest opening time's seed."""
    if not hasattr(engine, 'dungeon_scheduler') or not engine.dungeon_scheduler:
        return "Dungeon system not available."
    
    try:
        from dungeon_instance import DungeonInstance, set_current_dungeon
        
        scheduler = engine.dungeon_scheduler
        
        # Get current time
        now = scheduler._get_current_time()
        current_hour = now.hour
        
        # Find the closest opening hour
        opening_hours = scheduler.open_hours  # [0, 3, 6, 9, 12, 15, 18, 21]
        
        closest_hour = opening_hours[0]
        min_distance = abs(current_hour - opening_hours[0])
        
        for hour in opening_hours:
            distance = abs(current_hour - hour)
            if distance < min_distance:
                min_distance = distance
                closest_hour = hour
        
        # Generate seed using the closest opening hour
        date_str = now.strftime("%Y%m%d")
        seed = int(f"{date_str}{closest_hour:02d}")
        
        # Create dungeon instance with this seed
        active_dungeon = DungeonInstance(seed, scheduler)
        
        # Update both the engine and the global dungeon state
        engine.current_dungeon_instance = active_dungeon
        set_current_dungeon(active_dungeon, seed)
        
        # Force it to be active/open
        active_dungeon.active = True
        
        if not active_dungeon or not active_dungeon.dungeon_data:
            return "Failed to generate dungeon data."
        
        # Check if it's actually the right time for the dungeon to be open
        is_open_now = scheduler.is_dungeon_open()
        
        # Get schedule info
        if is_open_now:
            time_info = f"(Currently open - closes in ~{59 - now.minute} minutes)"
        else:
            _, time_str = scheduler.get_time_until_next_opening()
            time_info = f"⚠ FORCING EARLY (normally opens in {time_str})"
        
        return f"""✓ Dungeon forced open for debugging! {time_info}

The dungeon is now ready to enter. You can:
  1. Travel to one of these entrances and ENTER:
     - dungeon_forest_entrance (Dark Cave)
     - dungeon_mountain_entrance (Ancient Mountain Gate)
     - dungeon_ruins_entrance (Catacombs)
  2. Use 'debug teleport <room_id>' to jump to a specific dungeon room
  3. Use 'debug rooms' to list all available dungeon rooms"""
    
    except Exception as e:
        return f"Failed to force open dungeon: {e}"


def show_player_commands():
    """Return a list of available player commands."""
    return """
=== AVAILABLE COMMANDS ===

Movement:
  north, south, east, west     - Move in a direction
  go <direction>                - Alternative movement syntax

Actions:
  look, examine <item>          - Look around
  take <item>, get <item>       - Pick up an item
  drop <item>                   - Drop an item
  inventory, inv, i             - Check your inventory

General:
  help, commands                - Display help
  save                          - Save your game
  open map                      - Open interactive map
  close map                     - Close the map
  quit, exit                    - Exit the game

Debug:
  debug <command>               - Access debug menu
  debug commands                - Show all debug commands
""".strip()

