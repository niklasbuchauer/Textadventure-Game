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
            return "Usage: debug dungeon open [room_id] | debug dungeon close <dungeon_id> | debug dungeon list | debug dungeon check"
        action = args[1].lower()
        if action == "open":
            room_id = args[2] if len(args) > 2 else None
            return _debug_dungeon_open(engine, room_id)
        elif action == "close":
            if len(args) < 3:
                return "Usage: debug dungeon close <dungeon_id>"
            return _debug_dungeon_close(engine, args[2])
        elif action == "list":
            return _debug_dungeon_list(engine)
        elif action == "check":
            return _debug_dungeon_check_integrity(engine)
        return "Usage: debug dungeon open [room_id] | debug dungeon close <dungeon_id> | debug dungeon list | debug dungeon check"
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
  debug dungeon open <room_id> - Force open dungeon at specific entrance
  debug dungeon close <id>     - Remove force-open override
  debug dungeon list     - List force-opened dungeons
  debug dungeon check    - Check dungeon integrity (connectivity & secrets)
  debug heal             - Restore health
  debug rooms [page]     - List rooms (paginated)
  debug gold <amount>    - Set gold
  debug items            - Show inventory
  debug stats            - Show player stats

Example: debug teleport mountain_peak
Example: debug dungeon open
Example: debug dungeon open dungeon_forest_entrance
Example: debug dungeon close shifting_depths
Example: debug dungeon check
Example: debug rooms 1 (world) | debug rooms 2 (dungeon)
""".strip()


def _debug_reveal_map(engine):
    """Reveal all rooms on the map (toggle)."""
    if hasattr(engine, 'map_window') and engine.map_window:
        revealed = engine.map_window.toggle_reveal()
        if revealed:
            return "Map revealed: All rooms visible (fog of war disabled)"
        else:
            return "Map hidden: Fog of war restored"
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


def _debug_dungeon_open(engine, room_id=None):
    """Force open a dungeon for debug purposes.
    
    If room_id is provided, finds the dungeon entrance at that room and adds its
    dungeon_id to the force-open set so the player can enter normally via 'enter'.
    If room_id is None, uses the original behavior (closest opening time seed).
    """
    if not hasattr(engine, 'dungeon_scheduler') or not engine.dungeon_scheduler:
        return "Dungeon system not available."
    
    try:
        from dungeon_instance import DungeonInstance, set_current_dungeon
        
        scheduler = engine.dungeon_scheduler
        
        # If a room_id was provided, find the dungeon entrance and force-open it
        dungeon_id = None
        dungeon_exit = None
        
        if room_id:
            # Find the room
            room = engine.rooms.get(room_id)
            if not room:
                return f"[DEBUG] ❌ Room '{room_id}' not found!\nUse 'debug rooms' to list available rooms."
            
            # Find dungeon exit in this room
            exits = room.exits if hasattr(room, 'exits') else {}
            for exit_name, exit_data in exits.items():
                if isinstance(exit_data, dict) and exit_data.get("type") == "time_gated_dungeon":
                    dungeon_exit = exit_data
                    dungeon_id = exit_data.get("dungeon_id")
                    break
            
            if not dungeon_exit or not dungeon_id:
                return (f"[DEBUG] ❌ No dungeon entrance in room '{room_id}'!\n"
                        f"This room does not have a time_gated_dungeon exit.\n"
                        f"Available exits: {list(exits.keys())}")
        
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
        
        # Create dungeon instance with this seed and dungeon_id (if we have one)
        active_dungeon = DungeonInstance(seed, scheduler, dungeon_id=dungeon_id)
        
        # Update both the engine and the global dungeon state
        engine.current_dungeon_instance = active_dungeon
        set_current_dungeon(active_dungeon, seed)
        
        # Force it to be active/open
        active_dungeon.active = True
        
        if not active_dungeon or not active_dungeon.dungeon_data:
            return "Failed to generate dungeon data."
        
        # Add dungeon_id to force-open set if we found one
        if dungeon_id:
            if not hasattr(engine, 'debug_force_open_dungeons'):
                engine.debug_force_open_dungeons = set()
            engine.debug_force_open_dungeons.add(dungeon_id)
        
        # Also find and add ALL dungeon_ids from the world if no specific room given
        if not dungeon_id:
            for rid, room in engine.rooms.items():
                exits = room.exits if hasattr(room, 'exits') else {}
                for exit_name, exit_data in exits.items():
                    if isinstance(exit_data, dict) and exit_data.get("type") == "time_gated_dungeon":
                        did = exit_data.get("dungeon_id")
                        if did:
                            if not hasattr(engine, 'debug_force_open_dungeons'):
                                engine.debug_force_open_dungeons = set()
                            engine.debug_force_open_dungeons.add(did)
        
        # Check if it's actually the right time for the dungeon to be open
        is_open_now = scheduler.is_dungeon_open()
        
        # Get schedule info
        if is_open_now:
            time_info = f"(Currently open - closes in ~{59 - now.minute} minutes)"
        else:
            _, time_str = scheduler.get_time_until_next_opening()
            time_info = f"⚠ FORCING EARLY (normally opens in {time_str})"
        
        # Build force-open info
        force_open_info = ""
        if hasattr(engine, 'debug_force_open_dungeons') and engine.debug_force_open_dungeons:
            force_open_info = f"\nForce-opened dungeon IDs: {', '.join(engine.debug_force_open_dungeons)}"
            force_open_info += "\n✓ Time-gating OVERRIDDEN - you can enter normally using 'enter' command"
        
        result = f"""✓ Dungeon forced open for debugging! {time_info}
{force_open_info}

The dungeon is now ready to enter. You can:
  1. Travel to one of these entrances and type ENTER:
     - dungeon_forest_entrance (Dark Cave)
     - dungeon_mountain_entrance (Ancient Mountain Gate)
     - dungeon_ruins_entrance (Catacombs)
  2. Use 'debug teleport <room_id>' to jump to a specific dungeon room
  3. Use 'debug rooms' to list all available dungeon rooms"""
        
        if dungeon_id:
            result += f"\n\nSpecific dungeon '{dungeon_id}' at room '{room_id}' is now force-opened."
        
        return result
    
    except Exception as e:
        return f"Failed to force open dungeon: {e}"


def _debug_dungeon_close(engine, dungeon_id):
    """Remove debug override for a dungeon."""
    if not hasattr(engine, 'debug_force_open_dungeons'):
        return "[DEBUG] No dungeons are force-opened."
    
    if dungeon_id in engine.debug_force_open_dungeons:
        engine.debug_force_open_dungeons.remove(dungeon_id)
        return (f"[DEBUG] ✓ Removed '{dungeon_id}' from force-open list\n"
                f"[DEBUG] Dungeon will now follow normal time schedule")
    else:
        current = engine.debug_force_open_dungeons if engine.debug_force_open_dungeons else "(none)"
        return (f"[DEBUG] Dungeon '{dungeon_id}' is not force-opened\n"
                f"[DEBUG] Currently force-opened: {current}")


def _debug_dungeon_list(engine):
    """List force-opened dungeons."""
    if not hasattr(engine, 'debug_force_open_dungeons') or not engine.debug_force_open_dungeons:
        return "[DEBUG] No dungeons are currently force-opened."
    
    result = "\n[DEBUG] Force-opened dungeons:\n"
    for dung_id in engine.debug_force_open_dungeons:
        result += f"  - {dung_id}\n"
    result += "\nUse 'debug dungeon close <id>' to remove an override."
    return result


def _debug_dungeon_check_integrity(engine):
    """Check dungeon integrity: connectivity and secret room generation."""
    if not hasattr(engine, 'current_dungeon_instance') or not engine.current_dungeon_instance:
        return "No active dungeon. Enter a dungeon first to check its integrity."
    
    dungeon_instance = engine.current_dungeon_instance
    dungeon_data = dungeon_instance.dungeon_data
    
    if not dungeon_data:
        return "No dungeon data available."
    
    result = "\n" + "="*80 + "\n"
    result += "DUNGEON INTEGRITY CHECK\n"
    result += "="*80 + "\n"
    
    # Check each floor
    for floor_num in sorted(dungeon_data["floors"].keys()):
        floor_data = dungeon_data["floors"][floor_num]
        result += f"\n--- FLOOR {floor_num} ---\n"
        
        rooms = floor_data["rooms"]
        num_rooms = len(rooms)
        entrance = floor_data.get("entrance_room")
        boss = floor_data.get("boss_room")
        
        result += f"Total rooms: {num_rooms}\n"
        result += f"Entrance: {entrance}\n"
        result += f"Boss: {boss}\n"
        
        # Check connectivity using BFS
        if entrance:
            visited = set()
            queue = [entrance]
            
            while queue:
                current = queue.pop(0)
                if current in visited:
                    continue
                visited.add(current)
                
                room = rooms.get(current)
                if room:
                    for exit_data in room.get("exits", {}).values():
                        if isinstance(exit_data, dict):
                            target = exit_data.get("target")
                        else:
                            target = exit_data
                        
                        if target and target in rooms:
                            queue.append(target)
            
            disconnected = set(rooms.keys()) - visited
            
            if disconnected:
                result += f"❌ DISCONNECTED ROOMS: {len(disconnected)}\n"
                for room_id in list(disconnected)[:5]:
                    result += f"   - {room_id}\n"
                if len(disconnected) > 5:
                    result += f"   ... and {len(disconnected) - 5} more\n"
            else:
                result += f"✓ All {num_rooms} rooms connected\n"
        else:
            result += "⚠️ No entrance room defined!\n"
        
        # Check secret room on boss floor
        if boss:
            boss_room = rooms[boss]
            has_secret = boss_room.get("has_secret")
            secret_id = boss_room.get("secret_room_id")
            secret_discovered = boss_room.get("secret_discovered")
            
            if has_secret:
                result += f"✓ Boss room has secret: {secret_id}\n"
                
                if secret_id and secret_id in rooms:
                    result += f"✓ Secret room exists in floor data\n"
                    secret_room = rooms[secret_id]
                    
                    # Check secret room has items
                    if secret_room.get("items"):
                        result += f"✓ Secret room has items: {secret_room['items']}\n"
                    
                    # Check back exit
                    if "back" in secret_room.get("exits", {}):
                        result += f"✓ Secret room has 'back' exit\n"
                    else:
                        result += f"❌ Secret room missing 'back' exit!\n"
                    
                    # Check if discovered
                    if secret_discovered:
                        result += f"✓ Secret already discovered by player\n"
                        # Check if boss room has secret exit
                        if "secret" in boss_room.get("exits", {}):
                            result += f"✓ Boss room has 'secret' exit (discovered)\n"
                        else:
                            result += f"⚠️ Secret discovered but boss room missing 'secret' exit\n"
                    else:
                        result += f"⏳ Secret not yet discovered\n"
                        
                elif secret_id:
                    result += f"❌ Secret room {secret_id} NOT FOUND in floor data!\n"
            else:
                result += f"❌ Boss room has NO secret!\n"
    
    result += "\n" + "="*80 + "\n"
    return result


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

