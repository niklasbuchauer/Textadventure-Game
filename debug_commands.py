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
        return _debug_list_rooms(engine)
    elif subcommand == "gold":
        if len(args) > 1:
            return _debug_set_gold(engine, args[1])
        return "Usage: debug gold <amount>"
    elif subcommand == "items":
        return _debug_list_items(engine)
    elif subcommand == "stats":
        return _debug_show_stats(engine)
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
  debug heal             - Restore health
  debug rooms            - List all rooms
  debug gold <amount>    - Set gold
  debug items            - Show inventory
  debug stats            - Show player stats

Example: debug teleport mountain_peak
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
    """Teleport the player to a specific room."""
    if room_id not in engine.rooms:
        return f"Room '{room_id}' not found."
    
    if hasattr(engine.player, 'visited_rooms'):
        engine.player.visited_rooms.add(room_id)
    
    engine.player.current_room = room_id
    
    if hasattr(engine, 'map_window') and engine.map_window:
        if hasattr(engine.player, 'visited_rooms'):
            engine.map_window.update_location(room_id, engine.player.visited_rooms)
    
    room = engine.rooms[room_id]
    if hasattr(room, 'name'):
        room_name = room.name
    else:
        room_name = room.get('name', room_id)
    
    return f"Teleported to {room_name}!"


def _debug_heal(engine):
    """Restore player to full health."""
    if engine.player:
        engine.player.stats['health'] = 100
        return "Health restored to 100!"
    return "No player found"


def _debug_list_rooms(engine):
    """List all available room IDs."""
    rooms = sorted(engine.rooms.keys())
    if not rooms:
        return "No rooms found"
    
    room_list = []
    for room_id in rooms:
        room = engine.rooms[room_id]
        if hasattr(room, 'name'):
            room_name = room.name
        else:
            room_name = room.get('name', 'Unknown')
        room_list.append(f"  {room_id:30s} - {room_name}")
    
    return "Available rooms:\n" + "\n".join(room_list)


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

