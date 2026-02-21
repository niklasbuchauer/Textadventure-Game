#!/usr/bin/env python3
"""
Test dungeon entry with full debug output to identify the error source
"""

import json
import os
import sys
# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

print("=" * 70)
print("DUNGEON ENTRY DEBUG TEST")
print("=" * 70)

# Test 1: Check imports and flags
print("\n[TEST 1] Checking module imports...")
try:
    from engine import GameEngine, CommandHandler, DUNGEON_AVAILABLE
    
    print(f"✓ Engine imported")
    print(f"✓ DUNGEON_AVAILABLE = {DUNGEON_AVAILABLE}")
    
    if not DUNGEON_AVAILABLE:
        print("✗ ERROR: DUNGEON_AVAILABLE is False!")
        print("   This is why the dungeon system is not available.")
        print("   The dungeon modules failed to import.")
        
        # Try to diagnose the import error
        print("\n[DIAGNOSIS] Trying to import dungeon modules directly...")
        try:
            from dungeon_scheduler import DungeonScheduler
            print("  ✓ DungeonScheduler imported")
        except Exception as e:
            print(f"  ✗ DungeonScheduler import failed: {e}")
        
        try:
            from dungeon_instance import get_current_dungeon
            print("  ✓ dungeon_instance imported")
        except Exception as e:
            print(f"  ✗ dungeon_instance import failed: {e}")
        
        exit(1)
    
except Exception as e:
    print(f"✗ Error importing engine: {e}")
    exit(1)

# Test 2: Initialize GameEngine
print("\n[TEST 2] Initializing GameEngine...")
try:
    engine = GameEngine()
    print("✓ GameEngine initialized")
    
    # Need to start a new game to initialize player
    print("   Initializing new game...")
    engine.new_game()
    print("✓ New game started, player initialized")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Test 3: Create CommandHandler
print("\n[TEST 3] Creating CommandHandler...")
try:
    cmd_handler = CommandHandler(engine)
    print("✓ CommandHandler created")
except Exception as e:
    print(f"✗ Error: {e}")
    exit(1)

# Test 4: Check current room for dungeon entrance
print("\n[TEST 4] Checking current room for dungeon entrance...")
try:
    current_room_name = engine.player.current_room
    current_room = engine.rooms.get(current_room_name)
    
    print(f"Current room: {current_room_name}")
    
    if current_room:
        exits = current_room.exits
        print(f"Exits in room: {list(exits.keys())}")
        
        # Check for dungeon entrance
        has_dungeon = False
        for exit_name, exit_data in exits.items():
            if isinstance(exit_data, dict):
                exit_type = exit_data.get("type")
                print(f"  - '{exit_name}': type={exit_type}")
                if exit_type == "time_gated_dungeon":
                    has_dungeon = True
                    print(f"    ✓ Found dungeon entrance!")
        
        if not has_dungeon:
            print("\n⚠ No dungeon entrance in current room!")
            print("   Need to find a room with a dungeon entrance to test.")
            print("   Checking world.json for dungeon exits...")
            
            # Search all rooms for dungeon entrances
            found_any = False
            for room_name, room_obj in engine.rooms.items():
                for exit_name, exit_data in room_obj.exits.items():
                    if isinstance(exit_data, dict) and exit_data.get("type") == "time_gated_dungeon":
                        print(f"\n✓ Found dungeon entrance in room '{room_name}', exit '{exit_name}'")
                        found_any = True
            
            if not found_any:
                print("✗ No dungeon entrances found in any room!")
                print("   World needs a dungeon entrance defined.")
                exit(1)
    else:
        print(f"✗ Current room not found: {current_room_name}")
        exit(1)
        
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Test 5: Navigate to dungeon entrance room
print("\n[TEST 5] Moving to dungeon entrance room...")
try:
    dungeon_entrance_room = "dungeon_forest_entrance"
    
    if dungeon_entrance_room in engine.rooms:
        engine.player.current_room = dungeon_entrance_room
        print(f"✓ Moved to room: {dungeon_entrance_room}")
        
        room_obj = engine.rooms[dungeon_entrance_room]
        print(f"  Room name: {room_obj.name}")
        print(f"  Exits: {list(room_obj.exits.keys())}")
    else:
        print(f"✗ Room not found: {dungeon_entrance_room}")
        exit(1)

except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Test 6: Simulate entering dungeon
print("\n[TEST 6] Simulating 'enter' command in dungeon entrance room...")
print("-" * 70)
try:
    # Call the handle_enter_command which is what gets called when user types 'enter'
    print("[SIMULATING USER INPUT] > enter\n")
    
    result = cmd_handler.handle_enter_command()
    
    print("-" * 70)
    print("\n[RESULT]")
    print(result)
    
    if "dungeon system is not available" in result.lower():
        print("\n✗ ERROR REPRODUCED: Got 'dungeon system is not available' message!")
        print("   Check the [DEBUG] lines above to see where it failed.")
    else:
        print("\n✓ No error! Dungeon entrance detected correctly.")
        
except Exception as e:
    print(f"\n✗ Exception: {e}")
    import traceback
    traceback.print_exc()

# Cleanup
try:
    root.destroy()
except:
    pass

print("\n" + "=" * 70)
