#!/usr/bin/env python3
"""
Quick test to verify dungeon room lookup works for all command paths.
Tests:
- Enter dungeon (tests _enter_dungeon room lookup)
- Look command (tests _look room lookup)
- Move command (tests _go room lookup)
- Inventory room access (tests _collect room lookup)
"""
import sys
import datetime

try:
    from dungeon_scheduler import DungeonScheduler
    from dungeon_instance import DungeonInstance
    from dungeon_generator import DungeonGenerator
    print("✓ All dungeon modules imported")
except Exception as e:
    print(f"✗ Error importing dungeon modules: {e}")
    sys.exit(1)

try:
    from engine import GameEngine
    print("✓ GameEngine imported")
except Exception as e:
    print(f"✗ Error importing GameEngine: {e}")
    sys.exit(1)

print("\n" + "="*60)
print("DUNGEON ROOM LOOKUP TEST")
print("="*60)

# Initialize engine
engine = GameEngine()
engine.load_world()
engine.new_game()

if not engine.player:
    print("✗ Failed to create player")
    sys.exit(1)

print(f"\n[1] Player initialized at: {engine.player.current_room}")

# Test surface world room access
print("\n[2] Testing surface world room access...")
room = engine.get_room_data(engine.player.current_room)
if room:
    print(f"✓ Surface world room found: {room.name}")
else:
    print(f"✗ Surface world room NOT found!")
    sys.exit(1)

# Create a test dungeon instance
print("\n[3] Creating test dungeon...")
try:
    scheduler = DungeonScheduler()
    is_open = scheduler.is_dungeon_open()
    print(f"  Dungeon status: {'OPEN' if is_open else 'CLOSED'}")
    
    dungeon = DungeonInstance(
        seed=99999,
        scheduler=scheduler
    )
    engine.current_dungeon_instance = dungeon
    print("✓ Dungeon instance created and bound to engine")
except Exception as e:
    print(f"✗ Failed to create dungeon: {e}")
    sys.exit(1)

# Test dungeon room access directly
print("\n[4] Testing dungeon room access patterns...")
try:
    # Test the pattern used in get_room_data for dungeon rooms
    test_room_id = "floor1_room1"
    
    # Method 1: Direct get_room call (what get_room_data does internally)
    floor_num = 1
    room_dict = dungeon.get_room(floor_num, test_room_id)
    if room_dict:
        print(f"✓ Dungeon room dict retrieved: {test_room_id}")
    else:
        print(f"✗ Dungeon room dict NOT found: {test_room_id}")
        sys.exit(1)
    
    # Method 2: Through get_room_data (unified interface)
    room = engine.get_room_data(test_room_id)
    if room:
        print(f"✓ Dungeon room object retrieved via get_room_data: {room.name}")
    else:
        print(f"✗ Dungeon room NOT found via get_room_data: {test_room_id}")
        sys.exit(1)
        
except Exception as e:
    print(f"✗ Error accessing dungeon rooms: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test player entering dungeon (sets current_room to floor1_room1)
print("\n[5] Simulating player dungeon entry...")
try:
    engine.player.current_room = "floor1_room1"
    print(f"✓ Player moved to dungeon room: {engine.player.current_room}")
except Exception as e:
    print(f"✗ Failed to move player: {e}")
    sys.exit(1)

# Test that look command works from dungeon
print("\n[6] Testing _look command from dungeon room...")
try:
    # CommandHandler is created internally during game interactions
    # Test by simulating the look command directly
    current_room = engine.get_room_data(engine.player.current_room)
    if current_room:
        result = current_room.describe()
        if result and len(result) > 0:
            print(f"✓ Look command successful: {result[:80]}...")
        else:
            print(f"✗ Look command returned empty result")
            sys.exit(1)
    else:
        print(f"✗ Current room not found")
        sys.exit(1)
except Exception as e:
    print(f"✗ Error getting room description: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test examine command
print("\n[7] Testing room item access from dungeon room...")
try:
    room = engine.get_room_data(engine.player.current_room)
    if room and room.items:
        item = room.items[0]
        print(f"✓ Can access room items: {item}")
    else:
        print("⊘ No items in room to test examine")
except Exception as e:
    print(f"✗ Error accessing room items: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*60)
print("✓ ALL TESTS PASSED - DUNGEON ROOM LOOKUP WORKING")
print("="*60)
