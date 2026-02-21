#!/usr/bin/env python3
"""
Test the get_current_dungeon() fix with scheduler argument
"""

from dungeon_scheduler import DungeonScheduler, get_scheduler
from dungeon_instance import get_current_dungeon

print("=" * 60)
print("TESTING FIX: get_current_dungeon() with scheduler")
print("=" * 60)

# Test 1: Get scheduler
print("\n[Test 1] Getting scheduler...")
scheduler = get_scheduler()
print(f"✓ Got scheduler: {scheduler}")
print(f"✓ Scheduler type: {type(scheduler).__name__}")

# Test 2: Get current dungeon with scheduler argument
print("\n[Test 2] Getting current dungeon with scheduler argument...")
try:
    current_dungeon = get_current_dungeon(scheduler)
    print(f"✓ Got current dungeon: {current_dungeon}")
    print(f"✓ Dungeon type: {type(current_dungeon).__name__}")
except TypeError as e:
    print(f"✗ ERROR: {e}")
    exit(1)

# Test 3: Check dungeon data structure
print("\n[Test 3] Checking dungeon data structure...")
if current_dungeon.dungeon_data:
    print(f"✓ Dungeon data exists")
    
    floors = current_dungeon.dungeon_data.get('floors', {})
    print(f"✓ Floors in dungeon: {list(floors.keys())}")
    
    floor_1 = floors.get(1, {})
    if floor_1:
        entrance_room = floor_1.get('entrance_room')
        rooms_count = len(floor_1.get('rooms', {}))
        
        print(f"✓ Floor 1 entrance room: {entrance_room}")
        print(f"✓ Floor 1 rooms: {rooms_count} rooms")
        print(f"✓ Room list: {list(floor_1.get('rooms', {}).keys())[:3]}...")
    else:
        print(f"✗ No floor 1 data found")
        exit(1)
else:
    print(f"✗ No dungeon data")
    exit(1)

# Test 4: Simulate the _enter_dungeon logic
print("\n[Test 4] Simulating _enter_dungeon() logic...")
try:
    if active_dungeon := current_dungeon:  # Using walrus operator
        if active_dungeon.dungeon_data:
            floor_1_data = active_dungeon.dungeon_data.get("floors", {}).get(1, {})
            entrance_room_id = floor_1_data.get("entrance_room")
            
            if entrance_room_id:
                print(f"✓ Successfully extracted entrance room: {entrance_room_id}")
            else:
                print(f"✗ No entrance room found")
                exit(1)
        else:
            print(f"✗ No dungeon data")
            exit(1)
    else:
        print(f"✗ Could not get dungeon instance")
        exit(1)
except Exception as e:
    print(f"✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("\n" + "=" * 60)
print("ALL TESTS PASSED! Fix is working correctly.")
print("=" * 60)
