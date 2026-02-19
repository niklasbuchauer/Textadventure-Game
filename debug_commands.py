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
    elif subcommand == "skill":
        if len(args) > 2 and args[1].lower() == "points":
            return _debug_set_skill_points(engine, args[2])
        return "Usage: debug skill points <amount>"
    elif subcommand == "level":
        if len(args) > 1:
            return _debug_set_level(engine, args[1])
        return "Usage: debug level <level_number>"
    elif subcommand == "items":
        if len(args) > 1:
            sub = args[1].lower()
            if sub == "all":
                return _debug_open_items_window(engine)
            elif sub == "list":
                return _debug_list_all_items()
        return _debug_list_items(engine)
    elif subcommand == "enemies":
        return _debug_list_all_enemies()
    elif subcommand == "spawn":
        if len(args) < 3:
            return "Usage: debug spawn enemy <id> [level] | debug spawn item <id>"
        spawn_type = args[1].lower()
        if spawn_type == "enemy":
            level = None
            if len(args) > 3:
                try:
                    level = int(args[3])
                except ValueError:
                    return f"Invalid level: {args[3]}. Must be a number."
            return _debug_spawn_enemy(engine, args[2], level)
        elif spawn_type == "item":
            return _debug_spawn_item(engine, args[2])
        return "Usage: debug spawn enemy <id> [level] | debug spawn item <id>"
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
    elif subcommand == "mode":
        if len(args) < 2:
            return "Usage: debug mode traps"
        mode = args[1].lower()
        if mode == "traps":
            return _debug_toggle_free_disarm(engine)
        return f"Unknown mode: {mode}\nUsage: debug mode traps"
    else:
        return f"Unknown debug command: {subcommand}\n{_show_debug_menu()}"


def _show_debug_menu():
    """Return the debug commands menu."""
    return """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              DEBUG COMMANDS                                   ║
╚═══════════════════════════════════════════════════════════════════════════════╝

World & Navigation:
  debug reveal map              - Show all rooms on map
  debug hide map                - Hide unvisited rooms
  debug teleport <id>           - Teleport to a room
  debug rooms [page]            - List rooms (paginated)

Combat & Enemies:
  debug enemies                 - List all enemies with IDs
  debug spawn enemy <id> [lv]   - Spawn enemy (optional level override)
  debug heal                    - Restore health

Items & Inventory:
  debug items                   - Show your inventory
  debug items all               - Open searchable items window
  debug items list              - Print full item list to console (old behavior)
  debug spawn item <id>         - Add item to inventory
  debug gold <amount>           - Set gold amount

Dungeons:
  debug dungeon open [room_id]  - Force open dungeon for testing
  debug dungeon close <id>      - Remove force-open override
  debug dungeon list            - List force-opened dungeons
  debug dungeon check           - Check dungeon integrity

Skills & Stats:
  debug skill points <amount>   - Set skill points
  debug level <level_number>    - Set player level
  debug stats                   - Show player stats

Debug Modes:
  debug mode traps              - Toggle free disarm (no items required)

───────────────────────────────────────────────────────────────────────────────
Examples:
  debug spawn enemy crystal_beetle
  debug spawn enemy crystal_beetle 10
  debug spawn item iron_sword
  debug teleport mountain_peak
  debug dungeon open dungeon_forest_entrance
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
    """Restore player to full health (uses health_max, not hardcoded 100)."""
    if engine.player:
        health_max = engine.player.state.get('health_max', 100)
        engine.player.stats['health'] = health_max
        return f"Health restored to {health_max}!"
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


def _debug_set_skill_points(engine, amount):
    """Set player skill points amount."""
    try:
        sp_amount = int(amount)
        if engine.player:
            engine.player.stats['skill_points'] = sp_amount
            return f"Skill points set to {sp_amount}"
        return "No player found"
    except ValueError:
        return f"Invalid amount: {amount}"


def _debug_set_level(engine, level):
    """Set player level."""
    try:
        level_amount = int(level)
        if engine.player:
            engine.player.stats['level'] = level_amount
            return f"Level set to {level_amount}"
        return "No player found"
    except ValueError:
        return f"Invalid level: {level}"


def _debug_list_items(engine):
    """Show player inventory with nice formatting."""
    if not engine.player:
        return "No player found"
    
    inventory = engine.player.inventory
    
    result = "\n"
    result += "╔═══════════════════════════════════════════════════════════════════════════════╗\n"
    result += "║                             YOUR INVENTORY                                    ║\n"
    result += "╚═══════════════════════════════════════════════════════════════════════════════╝\n\n"
    
    if not inventory:
        result += "  (empty)\n"
    else:
        total_items = 0
        for item, qty in sorted(inventory.items()):
            result += f"  {item:50s} x{qty}\n"
            total_items += qty
        
        result += f"\n{'─' * 79}\n"
        result += f"Total: {len(inventory)} item types, {total_items} items\n"
    
    result += "Use 'debug items all' to open the searchable item window\n"
    return result


def _debug_show_stats(engine):
    """Display player stats."""
    if not engine.player:
        return "No player found"
    
    stats = engine.player.stats
    inventory = engine.player.inventory
    
    health_max = engine.player.state.get('health_max', 100)
    msg = f"""
=== PLAYER STATS ===
Health:   {stats.get('health', 0)}/{health_max}
Gold:     {engine.player.state.get('gold', 0)}
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


def _debug_toggle_free_disarm(engine):
	"""Toggle free disarm mode (disarm traps without items required)."""
	engine.debug_disarm_free = not engine.debug_disarm_free
	status = "ENABLED" if engine.debug_disarm_free else "DISABLED"
	return f"\n🔧 Free Disarm Mode: {status}\n\nYou can now disarm traps without requiring lockpick sets or other tools."


def _debug_list_all_enemies():
	"""List all enemies from the combat system database."""
	try:
		from combat_system import ENEMY_DATABASE, BOSS_DATABASE, MINI_BOSS_DATABASE
	except ImportError:
		return "Combat system not available."
	
	result = "\n"
	result += "╔═══════════════════════════════════════════════════════════════════════════════╗\n"
	result += "║                          ALL ENEMIES DATABASE                                 ║\n"
	result += "╚═══════════════════════════════════════════════════════════════════════════════╝\n\n"
	
	# Regular enemies
	result += "┌─ REGULAR ENEMIES ─────────────────────────────────────────────────────────────┐\n\n"
	for enemy_id in sorted(ENEMY_DATABASE.keys()):
		enemy = ENEMY_DATABASE[enemy_id]
		result += f"  {enemy_id:35s} - {enemy['name']}\n"
	
	# Mini-bosses
	result += "\n┌─ MINI-BOSSES ─────────────────────────────────────────────────────────────────┐\n\n"
	for mb_id in sorted(MINI_BOSS_DATABASE.keys()):
		mb = MINI_BOSS_DATABASE[mb_id]
		result += f"  {mb_id:35s} - {mb['name']}\n"
	
	# Bosses
	result += "\n┌─ BOSSES ──────────────────────────────────────────────────────────────────────┐\n\n"
	for boss_id in sorted(BOSS_DATABASE.keys()):
		boss = BOSS_DATABASE[boss_id]
		result += f"  {boss_id:35s} - {boss['name']}\n"
	
	result += f"\n{'─' * 79}\n"
	result += f"Total: {len(ENEMY_DATABASE)} regular enemies, {len(MINI_BOSS_DATABASE)} mini-bosses, {len(BOSS_DATABASE)} bosses\n"
	result += "Usage: debug spawn enemy <id> [level]\n"
	result += "Example: debug spawn enemy crystal_beetle 10\n"
	
	return result


def _debug_spawn_enemy(engine, enemy_id, level=None):
	"""Spawn an enemy and start combat."""
	try:
		from combat_system import (ENEMY_DATABASE, BOSS_DATABASE, MINI_BOSS_DATABASE,
		                           create_enemy_instance, create_boss_instance, 
		                           create_mini_boss_instance, get_combat_status)
	except ImportError:
		return "Combat system not available."
	
	# Check if already in combat
	if hasattr(engine, 'pending_combat') and engine.pending_combat:
		return "You're already in combat! Finish the current fight first."
	
	# Try to create the enemy
	combat = None
	if enemy_id in ENEMY_DATABASE:
		combat = create_enemy_instance(enemy_id, level=level)
		is_boss = False
	elif enemy_id in MINI_BOSS_DATABASE:
		# Create mini-boss by dungeon (we'll use the ID directly)
		for dungeon, mb_id in [("crystal_caverns", "crystal_matriarch"),
		                       ("iron_halls", "iron_warden"),
		                       ("shadow_depths", "void_weaver"),
		                       ("sunken_catacombs", "bone_colossus")]:
			if mb_id == enemy_id:
				if level is None:
					combat = create_mini_boss_instance(dungeon)
				else:
					combat = create_mini_boss_instance(dungeon, floor_num=1)
					# Override the level with the specified value
					combat.level = level
					from combat_system import scale_enemy_stats
					# Re-scale the stats with the new level
					mb_data_for_dungeon = {}
					for d, id in [("crystal_caverns", "crystal_matriarch"),
					              ("iron_halls", "iron_warden"),
					              ("shadow_depths", "void_weaver"),
					              ("sunken_catacombs", "bone_colossus")]:
						if id == enemy_id:
							from combat_system import get_mini_boss_for_dungeon
							template = get_mini_boss_for_dungeon(d)
							if template:
								scaled = scale_enemy_stats(template, level, "mini_boss")
								combat.max_hp = scaled["hp"]
								combat.hp = scaled["hp"]
								combat.attack = scaled["attack"]
								combat.defense = scaled["defense"]
								combat.xp_reward = scaled["xp_reward"]
								combat.gold_reward = scaled["gold_reward"]
							break
				break
		is_boss = False
	elif enemy_id in BOSS_DATABASE:
		# Create boss by dungeon
		for dungeon, boss_id in [("crystal_caverns", "crystal_titan"),
		                         ("iron_halls", "iron_forgemaster"),
		                         ("shadow_depths", "shadow_sovereign"),
		                         ("sunken_catacombs", "lich_king")]:
			if boss_id == enemy_id:
				if level is None:
					combat = create_boss_instance(dungeon)
				else:
					combat = create_boss_instance(dungeon, floor_num=1)
					# Override the level with the specified value
					combat.level = level
					from combat_system import scale_enemy_stats, get_boss_for_dungeon
					# Re-scale the stats with the new level
					template = get_boss_for_dungeon(dungeon)
					if template:
						scaled = scale_enemy_stats(template, level, "boss")
						combat.max_hp = scaled["hp"]
						combat.hp = scaled["hp"]
						combat.attack = scaled["attack"]
						combat.defense = scaled["defense"]
						combat.xp_reward = scaled["xp_reward"]
						combat.gold_reward = scaled["gold_reward"]
				break
		is_boss = True
	else:
		return f"Enemy '{enemy_id}' not found.\nUse 'debug enemies' to see all available enemies."
	
	if not combat:
		return f"Failed to create enemy '{enemy_id}'."
	
	# Set up combat
	engine.pending_combat = combat
	
	# Build result message
	result = "\n" + "═" * 79 + "\n"
	if combat.is_boss:
		result += f"⚔️  BOSS SPAWNED: {combat.enemy_name} [Lv.{combat.level}]\n"
	elif combat.is_mini_boss:
		result += f"⚔️  MINI-BOSS SPAWNED: {combat.enemy_name} [Lv.{combat.level}]\n"
	else:
		result += f"⚔️  ENEMY SPAWNED: {combat.enemy_name} [Lv.{combat.level}]\n"
	result += "═" * 79 + "\n"
	result += f"{combat.enemy_description}\n"
	result += f"HP: {combat.hp} | Attack: {combat.attack} | Defense: {combat.defense}\n"
	
	if combat.intro_text:
		result += combat.intro_text + "\n"
	
	result += get_combat_status(engine.player, combat)
	
	return result


def _debug_open_items_window(engine):
	"""Open the searchable items database window."""
	try:
		from searchable_items_window import SearchableItemsWindow
	except ImportError as e:
		return f"Items window not available: {e}"

	# Get the root tkinter widget from the engine
	root = None
	if hasattr(engine, 'root'):
		root = engine.root
	elif hasattr(engine, 'master'):
		root = engine.master
	else:
		return "Items window requires a running GUI (tkinter root not found)."

	# Close existing window if open
	existing = getattr(engine, 'items_search_window', None)
	if existing and existing.is_open():
		existing.window.lift()
		return "  Items search window is already open (brought to front)."

	# Create and open new window
	win = SearchableItemsWindow(root, game_engine=engine)
	win.create_window()
	engine.items_search_window = win
	return "  Opened item database search window."


def _debug_list_all_items():
	"""List ALL items from every source in the game — equipment, shop, crafting,
	combat loot, dungeon loot, world rooms, fishing, fixed dungeons, quests, and item effects."""

	# ── Collect from every source ──────────────────────────────────────
	# Master dict: item_id -> set of source labels
	master = {}

	def _add(item_id, source):
		if not item_id or not isinstance(item_id, str):
			return
		master.setdefault(item_id, set()).add(source)

	# 1) Equipment database
	try:
		from equipment_system import EQUIPMENT_DATABASE
		for k in EQUIPMENT_DATABASE:
			_add(k, "equipment")
	except Exception:
		EQUIPMENT_DATABASE = {}

	# 2) Shop item database
	try:
		from shop_system import ITEM_DATABASE
		for k in ITEM_DATABASE:
			_add(k, "shop")
	except Exception:
		ITEM_DATABASE = {}

	# 3) Item effects (usable items + fishing loot) — module-level globals
	try:
		from item_effects import ITEM_EFFECTS as _IE_ITEMS
		for item_id in _IE_ITEMS:
			_add(item_id, "item_effects")
	except Exception:
		pass
	try:
		from item_effects import FISHING_LOOT as _FISH
		for entry in _FISH:
			if isinstance(entry, (list, tuple)) and len(entry) >= 1:
				_add(str(entry[0]), "fishing")
			elif isinstance(entry, dict) and 'item' in entry:
				_add(entry['item'], "fishing")
	except Exception:
		pass

	# 4) Crafting recipes (outputs + ingredients)
	try:
		from crafting_system import RECIPE_DATABASE
		for recipe_id, recipe in RECIPE_DATABASE.items():
			# Output item (often same as recipe_id or has 'output' key)
			output = recipe.get('output', recipe_id)
			_add(output, "crafting_output")
			# Ingredients
			for ingr in recipe.get('ingredients', {}):
				_add(ingr, "crafting_ingredient")
	except Exception:
		pass

	# 5) Combat loot drops
	try:
		from combat_system import ENEMY_DATABASE, BOSS_DATABASE, MINI_BOSS_DATABASE
		for db_name, db, label in [
			("enemies", ENEMY_DATABASE, "enemy_loot"),
			("bosses", BOSS_DATABASE, "boss_loot"),
			("mini_bosses", MINI_BOSS_DATABASE, "mini_boss_loot")
		]:
			for eid, edata in db.items():
				for drop in edata.get('loot', []):
					if isinstance(drop, dict):
						_add(drop.get('item', ''), label)
					elif isinstance(drop, (list, tuple)) and len(drop) >= 1:
						_add(str(drop[0]), label)
	except Exception:
		pass

	# 6) Dungeon generator — uses ITEM_DATABASE at runtime, no separate loot tables

	# 7) World.json room items
	try:
		import json, os
		world_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "world.json")
		if os.path.exists(world_path):
			with open(world_path, 'r', encoding='utf-8') as f:
				world = json.load(f)
			rooms = world.get('rooms', {})
			if isinstance(rooms, dict):
				for room_data in rooms.values():
					for it in room_data.get('items', []):
						_add(str(it), "world")
			elif isinstance(rooms, list):
				for room_data in rooms:
					for it in room_data.get('items', []):
						_add(str(it), "world")
	except Exception:
		pass

	# 8) Fixed dungeon items
	try:
		import json, os, glob
		fd_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixed_dungeons")
		if os.path.isdir(fd_dir):
			for fpath in glob.glob(os.path.join(fd_dir, "*.json")):
				dname = os.path.splitext(os.path.basename(fpath))[0]
				with open(fpath, 'r', encoding='utf-8') as f:
					ddata = json.load(f)
				# floors can be dict or list
				floors = ddata.get('floors', {})
				floor_iter = floors.values() if isinstance(floors, dict) else floors
				for floor in floor_iter:
					rooms = floor.get('rooms', {})
					room_iter = rooms.values() if isinstance(rooms, dict) else rooms
					for room in room_iter:
						# Items can be dict {item_id: {qty, val}} or list
						room_items = room.get('items', {})
						if isinstance(room_items, dict):
							for it in room_items:
								_add(str(it), f"dungeon:{dname}")
						elif isinstance(room_items, list):
							for it in room_items:
								_add(str(it), f"dungeon:{dname}")
						# Also check chests
						for chest in room.get('chests', []):
							chest_items = chest.get('items', {})
							if isinstance(chest_items, dict):
								for it in chest_items:
									_add(str(it), f"dungeon:{dname}")
							elif isinstance(chest_items, list):
								for it in chest_items:
									_add(str(it), f"dungeon:{dname}")
							# Chest contents
							contents = chest.get('contents', {})
							c_items = contents.get('items', {})
							if isinstance(c_items, dict):
								for it in c_items:
									_add(str(it), f"dungeon:{dname}")
	except Exception:
		pass

	# 9) Quest rewards and objectives
	try:
		from quest_system import QUEST_DATABASE
		for qid, qdef in QUEST_DATABASE.items():
			for it, count in qdef.get('rewards', {}).get('items', {}).items():
				_add(it, "quest_reward")
			for obj in qdef.get('objectives', []):
				if obj.get('type') == 'collect':
					_add(obj.get('item', ''), "quest_objective")
	except Exception:
		pass

	# ── Remove empty entries ───────────────────────────────────────────
	master.pop('', None)

	# ── Categorize items ──────────────────────────────────────────────

	# Equipment by slot
	equip_by_slot = {'weapon': [], 'armor': [], 'shield': [], 'accessory': []}
	for item_id in sorted(master):
		if item_id in EQUIPMENT_DATABASE:
			slot = EQUIPMENT_DATABASE[item_id].get('slot', 'other')
			equip_by_slot.setdefault(slot, []).append(item_id)

	# Consumables & tools (from item_effects / shop)
	consumables = []
	# Crafting materials (ingredients only, not outputs that are equipment)
	materials = []
	# Dungeon loot & drops
	dungeon_items = []
	# World / environmental items
	world_items = []
	# Quest-specific items
	quest_items = []
	# Uncategorized
	other_items = []

	for item_id in sorted(master):
		if item_id in EQUIPMENT_DATABASE:
			continue  # already handled above
		sources = master[item_id]
		src_str = ", ".join(sorted(sources))

		# Categorize by primary source
		if 'shop' in sources or 'item_effects' in sources or 'fishing' in sources:
			consumables.append((item_id, src_str))
		elif 'crafting_ingredient' in sources and 'crafting_output' not in sources:
			materials.append((item_id, src_str))
		elif 'crafting_output' in sources:
			consumables.append((item_id, src_str))
		elif any(s.startswith('dungeon') for s in sources) or any('loot' in s for s in sources):
			dungeon_items.append((item_id, src_str))
		elif 'world' in sources:
			world_items.append((item_id, src_str))
		elif 'quest_reward' in sources or 'quest_objective' in sources:
			quest_items.append((item_id, src_str))
		else:
			other_items.append((item_id, src_str))

	# ── Build output ──────────────────────────────────────────────────
	result = "\n"
	result += "╔═══════════════════════════════════════════════════════════════════════════════╗\n"
	result += "║                     COMPLETE ITEM DATABASE (ALL SOURCES)                      ║\n"
	result += "╚═══════════════════════════════════════════════════════════════════════════════╝\n\n"

	# Equipment by slot
	result += "┌─ EQUIPMENT ───────────────────────────────────────────────────────────────────┐\n"
	slot_labels = [('weapon', 'Weapons'), ('armor', 'Armor'), ('shield', 'Shields'), ('accessory', 'Accessories')]
	for slot_key, slot_label in slot_labels:
		items = equip_by_slot.get(slot_key, [])
		if items:
			result += f"\n  {slot_label}:\n"
			for item_id in items:
				edata = EQUIPMENT_DATABASE[item_id]
				stats_str = ""
				if edata.get('stats'):
					stats_str = "  (" + ", ".join(f"+{v} {k}" for k, v in edata['stats'].items()) + ")"
				result += f"    {item_id:35s}  {edata.get('name', item_id)}{stats_str}\n"
	eq_total = sum(len(v) for v in equip_by_slot.values())
	result += f"\n  ({eq_total} equipment items)\n\n"

	# Consumables & usable items
	if consumables:
		result += "┌─ CONSUMABLES & TOOLS ─────────────────────────────────────────────────────────┐\n\n"
		for item_id, src_str in consumables:
			nice = item_id.replace('_', ' ').title()
			result += f"    {item_id:35s}  {nice:25s}  [{src_str}]\n"
		result += f"\n  ({len(consumables)} items)\n\n"

	# Crafting materials
	if materials:
		result += "┌─ CRAFTING MATERIALS ──────────────────────────────────────────────────────────┐\n\n"
		for item_id, src_str in materials:
			nice = item_id.replace('_', ' ').title()
			result += f"    {item_id:35s}  {nice:25s}  [{src_str}]\n"
		result += f"\n  ({len(materials)} items)\n\n"

	# Dungeon loot
	if dungeon_items:
		result += "┌─ DUNGEON LOOT & DROPS ────────────────────────────────────────────────────────┐\n\n"
		for item_id, src_str in dungeon_items:
			nice = item_id.replace('_', ' ').title()
			result += f"    {item_id:35s}  {nice:25s}  [{src_str}]\n"
		result += f"\n  ({len(dungeon_items)} items)\n\n"

	# World items
	if world_items:
		result += "┌─ WORLD / ENVIRONMENT ─────────────────────────────────────────────────────────┐\n\n"
		for item_id, src_str in world_items:
			nice = item_id.replace('_', ' ').title()
			result += f"    {item_id:35s}  {nice:25s}  [{src_str}]\n"
		result += f"\n  ({len(world_items)} items)\n\n"

	# Quest items
	if quest_items:
		result += "┌─ QUEST ITEMS ─────────────────────────────────────────────────────────────────┐\n\n"
		for item_id, src_str in quest_items:
			nice = item_id.replace('_', ' ').title()
			result += f"    {item_id:35s}  {nice:25s}  [{src_str}]\n"
		result += f"\n  ({len(quest_items)} items)\n\n"

	# Other / uncategorized
	if other_items:
		result += "┌─ OTHER ────────────────────────────────────────────────────────────────────────┐\n\n"
		for item_id, src_str in other_items:
			nice = item_id.replace('_', ' ').title()
			result += f"    {item_id:35s}  {nice:25s}  [{src_str}]\n"
		result += f"\n  ({len(other_items)} items)\n\n"

	result += "═" * 79 + "\n"
	result += f"  TOTAL: {len(master)} unique items across all sources\n"
	result += "  Usage: debug spawn item <id>\n"
	result += "═" * 79 + "\n"

	return result


def _debug_spawn_item(engine, item_id):
	"""Add an item to the player's inventory. Accepts ANY item ID from any source."""
	# Build a validation set of all known items (same logic as _debug_list_all_items)
	known_items = set()

	try:
		from equipment_system import EQUIPMENT_DATABASE
		known_items.update(EQUIPMENT_DATABASE.keys())
	except Exception:
		EQUIPMENT_DATABASE = {}

	try:
		from shop_system import ITEM_DATABASE
		known_items.update(ITEM_DATABASE.keys())
	except Exception:
		ITEM_DATABASE = {}

	try:
		from item_effects import ITEM_EFFECTS as _IE_ITEMS2
		known_items.update(_IE_ITEMS2.keys())
	except Exception:
		pass
	try:
		from item_effects import FISHING_LOOT as _FISH2
		for entry in _FISH2:
			if isinstance(entry, (list, tuple)) and len(entry) >= 1:
				known_items.add(str(entry[0]))
			elif isinstance(entry, dict) and 'item' in entry:
				known_items.add(entry['item'])
	except Exception:
		pass

	try:
		from crafting_system import RECIPE_DATABASE
		for rid, recipe in RECIPE_DATABASE.items():
			known_items.add(recipe.get('output', rid))
			known_items.update(recipe.get('ingredients', {}).keys())
	except Exception:
		pass

	try:
		from combat_system import ENEMY_DATABASE, BOSS_DATABASE, MINI_BOSS_DATABASE
		for db in (ENEMY_DATABASE, BOSS_DATABASE, MINI_BOSS_DATABASE):
			for edata in db.values():
				for drop in edata.get('loot', []):
					if isinstance(drop, dict):
						known_items.add(drop.get('item', ''))
					elif isinstance(drop, (list, tuple)) and len(drop) >= 1:
						known_items.add(str(drop[0]))
	except Exception:
		pass

	try:
		import json, os, glob
		fd_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixed_dungeons")
		if os.path.isdir(fd_dir):
			for fpath in glob.glob(os.path.join(fd_dir, "*.json")):
				with open(fpath, 'r', encoding='utf-8') as f:
					ddata = json.load(f)
				floors = ddata.get('floors', {})
				floor_iter = floors.values() if isinstance(floors, dict) else floors
				for floor in floor_iter:
					rooms = floor.get('rooms', {})
					room_iter = rooms.values() if isinstance(rooms, dict) else rooms
					for room in room_iter:
						room_items = room.get('items', {})
						if isinstance(room_items, dict):
							known_items.update(room_items.keys())
						elif isinstance(room_items, list):
							known_items.update(str(it) for it in room_items)
						for chest in room.get('chests', []):
							ci = chest.get('items', {})
							if isinstance(ci, dict):
								known_items.update(ci.keys())
							elif isinstance(ci, list):
								known_items.update(str(it) for it in ci)
							cc = chest.get('contents', {}).get('items', {})
							if isinstance(cc, dict):
								known_items.update(cc.keys())
	except Exception:
		pass

	try:
		import json, os
		world_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "world.json")
		if os.path.exists(world_path):
			with open(world_path, 'r', encoding='utf-8') as f:
				world = json.load(f)
			rooms = world.get('rooms', {})
			if isinstance(rooms, dict):
				for room_data in rooms.values():
					known_items.update(str(it) for it in room_data.get('items', []))
			elif isinstance(rooms, list):
				for room_data in rooms:
					known_items.update(str(it) for it in room_data.get('items', []))
	except Exception:
		pass

	try:
		from quest_system import QUEST_DATABASE
		for qdef in QUEST_DATABASE.values():
			known_items.update(qdef.get('rewards', {}).get('items', {}).keys())
			for obj in qdef.get('objectives', []):
				if obj.get('type') == 'collect':
					known_items.add(obj.get('item', ''))
	except Exception:
		pass

	known_items.discard('')

	if not engine.player:
		return "No player found."

	# Check if item exists in any source (or allow force-spawn with ! prefix)
	force = item_id.startswith('!')
	if force:
		item_id = item_id[1:]

	if item_id not in known_items and not force:
		# Suggest close matches
		suggestions = [k for k in sorted(known_items) if item_id in k]
		msg = f"Item '{item_id}' not found in any database.\n"
		if suggestions:
			msg += "Did you mean:\n"
			for s in suggestions[:10]:
				msg += f"  {s}\n"
		msg += "\nUse 'debug items all' to open the searchable item window.\n"
		msg += "Prefix with ! to force-spawn any ID (e.g. debug spawn item !custom_item)\n"
		return msg

	# Add to inventory
	if item_id in engine.player.inventory:
		engine.player.inventory[item_id] += 1
		qty_msg = f"(now have {engine.player.inventory[item_id]})"
	else:
		engine.player.inventory[item_id] = 1
		qty_msg = "(new item)"

	# Trigger inventory UI update
	if hasattr(engine, '_inventory_changed'):
		engine._inventory_changed = True

	# Notify quest system
	try:
		if hasattr(engine, 'quest_manager') and engine.quest_manager:
			engine.quest_manager.on_item_changed()
	except Exception:
		pass

	# Build result
	result = "\n" + "═" * 79 + "\n"

	# Get display name from known databases
	display_name = item_id.replace('_', ' ').title()
	extra_info = ""
	if item_id in EQUIPMENT_DATABASE:
		edata = EQUIPMENT_DATABASE[item_id]
		display_name = edata.get('name', display_name)
		extra_info += f"Type: {edata.get('slot', 'unknown').title()}\n"
		extra_info += f"Description: {edata.get('description', 'No description')}\n"
		if edata.get('stats'):
			extra_info += f"Stats: {', '.join(f'+{v} {k}' for k, v in edata['stats'].items())}\n"
	elif item_id in ITEM_DATABASE:
		idata = ITEM_DATABASE[item_id]
		display_name = idata.get('name', display_name)
		icon = idata.get('icon', '')
		if icon:
			extra_info += f"Icon: {icon}\n"
		extra_info += f"Description: {idata.get('desc', 'No description')}\n"
		if 'value' in idata:
			extra_info += f"Value: {idata['value']} gold\n"

	result += f"✓ SPAWNED: {display_name}\n"
	result += "═" * 79 + "\n"
	result += f"Added to inventory {qty_msg}\n"
	if extra_info:
		result += "\n" + extra_info

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

