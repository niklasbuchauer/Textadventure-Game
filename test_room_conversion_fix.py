"""
Test to verify the AttributeError fix in _convert_dungeon_room_to_world()
Tests both list and dict item formats to ensure backward compatibility.
"""

import sys
import json
from dungeon_generator import DungeonGenerator
import engine
from engine import GameEngine

def test_room_conversion():
    """Test converting dungeon rooms with both item format types"""
    
    print("=" * 70)
    print("ROOM CONVERSION FIX TEST")
    print("=" * 70)
    
    # Initialize engine
    engine_instance = GameEngine()
    print("\n[TEST 1] Engine initialization...")
    print(f"  DUNGEON_AVAILABLE: {engine.DUNGEON_AVAILABLE}")
    assert engine.DUNGEON_AVAILABLE, "Dungeon system should be available"
    print("  [PASS] Engine ready\n")
    
    # Create test rooms with both item formats
    print("[TEST 2] Creating test rooms with different item formats...")
    
    # Room with dict-format items (traditional format)
    room_dict_format = {
        "id": "test_room_1",
        "name": "Test Room (Dict Format)",
        "description": "A room with dict items",
        "items": {
            "gold_coin": {"quantity": 10, "value": 1},
            "silver_coin": {"quantity": 5, "value": 2}
        }
    }
    
    # Room with list-format items (secret room format)
    room_list_format = {
        "id": "test_room_2",
        "name": "Test Room (List Format)",
        "description": "A room with list items",
        "items": ["legendary_artifact", "ancient_relic"]
    }
    
    # Room with empty items
    room_empty_format = {
        "id": "test_room_3",
        "name": "Test Room (Empty)",
        "description": "A room with no items",
        "items": {}
    }
    
    test_rooms = [room_dict_format, room_list_format, room_empty_format]
    print(f"  Created {len(test_rooms)} test rooms\n")
    
    # Test conversion - this is where the AttributeError occurred
    print("[TEST 3] Converting test rooms (AttributeError should NOT occur)...")
    attribute_errors = []
    other_errors = []
    
    for room in test_rooms:
        try:
            engine_instance._convert_dungeon_room_to_world(room)
            print(f"  ✓ {room['name']}: SUCCESS")
        except AttributeError as e:
            attribute_errors.append((room['id'], room['name'], str(e)))
            print(f"  ✗ {room['name']}: AttributeError")
        except Exception as e:
            other_errors.append((room['id'], room['name'], type(e).__name__, str(e)))
            print(f"  ⚠ {room['name']}: {type(e).__name__}")
    
    print()
    
    if attribute_errors:
        print("  [FAIL] AttributeErrors found:")
        for room_id, name, error in attribute_errors:
            print(f"    - {name}: {error}")
        return False
    
    if other_errors:
        print(f"  [WARN] Other errors found ({len(other_errors)}):")
        for room_id, name, etype, error in other_errors:
            print(f"    - {name}: {etype}: {error}")
    
    print(f"  [PASS] All test rooms converted without AttributeError!\n")
    
    # Now test with an actual generated dungeon
    print("[TEST 4] Testing with actual generated dungeon...")
    generator = DungeonGenerator()
    dungeon = generator.generate_complete_dungeon(seed=42)
    
    # Collect all rooms from all floors
    all_rooms = []
    for floor_num, floor_data in dungeon.get('floors', {}).items():
        floor_rooms = floor_data.get('rooms', {})
        # Handle both list and dict structures
        if isinstance(floor_rooms, dict):
            all_rooms.extend(floor_rooms.values())
        elif isinstance(floor_rooms, list):
            all_rooms.extend(floor_rooms)
    
    print(f"  Total rooms in generated dungeon: {len(all_rooms)}")
    
    # Check item format distribution
    list_format_count = 0
    dict_format_count = 0
    for room in all_rooms:
        items = room.get('items', {})
        if isinstance(items, list):
            list_format_count += 1
        elif isinstance(items, dict):
            dict_format_count += 1
    
    print(f"  Rooms with list-format items: {list_format_count}")
    print(f"  Rooms with dict-format items: {dict_format_count}")
    
    # Test conversion of generated dungeon rooms
    print(f"\n  Converting {len(all_rooms)} generated rooms...")
    conversion_errors = []
    
    for room in all_rooms:
        try:
            engine_instance._convert_dungeon_room_to_world(room)
        except AttributeError as e:
            conversion_errors.append((room.get('id'), room.get('name'), str(e)))
    
    if conversion_errors:
        print(f"  [FAIL] Found {len(conversion_errors)} AttributeErrors in generated dungeon")
        for room_id, name, error in conversion_errors:
            print(f"    - {name}: {error}")
        return False
    else:
        print(f"  [PASS] All {len(all_rooms)} generated rooms converted successfully!")
    
    print("\n" + "=" * 70)
    print("ALL TESTS PASSED - AttributeError fix is working!")
    print("=" * 70)
    return True

if __name__ == "__main__":
    try:
        success = test_room_conversion()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n[ERROR] Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
