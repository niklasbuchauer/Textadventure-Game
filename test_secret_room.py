#!/usr/bin/env python3
"""Test script for secret room discovery and room connectivity validation."""

import sys
sys.path.insert(0, 'C:\\Users\\nikbu\\Documents\\Coding\\Unitopia style game')

from dungeon_generator import DungeonGenerator
from dungeon_instance import DungeonInstance
import json

def test_secret_room_generation():
    """Test that secret rooms are generated in boss chambers."""
    print("=" * 70)
    print("Testing Secret Room Generation")
    print("=" * 70)
    
    generator = DungeonGenerator()
    dungeon = generator.generate_complete_dungeon(seed=54321)
    
    # Check all floors for secret rooms
    total_secret_rooms = 0
    for floor_num, floor_data in dungeon["floors"].items():
        rooms = floor_data["rooms"]
        
        # Find boss room
        boss_room_id = None
        for rid in rooms:
            if rooms[rid].get("is_boss_room"):
                boss_room_id = rid
                break
        
        if boss_room_id:
            boss_room = rooms[boss_room_id]
            if boss_room.get("secret_room_id"):
                total_secret_rooms += 1
                secret_id = boss_room.get("secret_room_id")
                if secret_id in rooms:
                    secret_room = rooms[secret_id]
                    print(f"\n✓ Floor {floor_num}: Found secret room")
                    print(f"  Boss Room: {boss_room['name']}")
                    print(f"  Secret Room: {secret_room['name']}")
                    print(f"  Secret has 'back' exit: {'back' in secret_room.get('exits', {})}")
                else:
                    print(f"\n✗ Floor {floor_num}: Secret room ID not in rooms dict!")
    
    print(f"\n✓ Total secret rooms generated: {total_secret_rooms}")
    return total_secret_rooms > 0

def test_room_connectivity():
    """Test that all public rooms are reachable."""
    print("\n" + "=" * 70)
    print("Testing Room Connectivity (BFS from entrance)")
    print("=" * 70)
    
    generator = DungeonGenerator()
    dungeon = generator.generate_complete_dungeon(seed=99999)
    
    all_connected = True
    for floor_num, floor_data in dungeon["floors"].items():
        rooms = floor_data["rooms"]
        # Exclude secret rooms from connectivity check (they're hidden)
        room_ids = [rid for rid in rooms.keys() if not rid.endswith('_secret')]
        
        if not room_ids:
            continue
        
        # BFS from first room (entrance)
        visited = set()
        queue = [room_ids[0]]
        visited.add(room_ids[0])
        
        while queue:
            room_id = queue.pop(0)
            room = rooms[room_id]
            for direction, exit_data in room.get("exits", {}).items():
                target = exit_data.get("target") if isinstance(exit_data, dict) else exit_data
                # Only follow exits to non-secret rooms
                if target and target in rooms and '_secret' not in target and target not in visited:
                    visited.add(target)
                    queue.append(target)
        
        unreachable = set(room_ids) - visited
        
        print(f"\nFloor {floor_num}:")
        print(f"  Total public rooms: {len(room_ids)}")
        print(f"  Reachable: {len(visited)}")
        print(f"  Unreachable: {len(unreachable)}")
        
        if unreachable:
            all_connected = False
            print(f"  ✗ Unreachable rooms: {unreachable}")
        else:
            print(f"  ✓ All public rooms connected!")
    
    return all_connected

def test_validation_calls():
    """Test that validation function is being called."""
    print("\n" + "=" * 70)
    print("Testing Validation Function Presence")
    print("=" * 70)
    
    generator = DungeonGenerator()
    
    if hasattr(generator, 'ensure_all_rooms_connected'):
        print("✓ ensure_all_rooms_connected method exists")
    else:
        print("✗ ensure_all_rooms_connected method NOT found")
        return False
    
    if hasattr(generator, 'add_secret_room'):
        print("✓ add_secret_room method exists")
    else:
        print("✗ add_secret_room method NOT found")
        return False
    
    return True

if __name__ == "__main__":
    print("\nRunning Secret Room & Connectivity Tests\n")
    
    results = []
    
    # Test 1: Validation functions exist
    results.append(("Validation Functions Present", test_validation_calls()))
    
    # Test 2: Secret rooms are generated
    results.append(("Secret Room Generation", test_secret_room_generation()))
    
    # Test 3: All rooms are connected
    results.append(("Room Connectivity", test_room_connectivity()))
    
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(result[1] for result in results)
    print("\n" + ("=" * 70))
    if all_passed:
        print("All tests PASSED! ✓")
    else:
        print("Some tests FAILED! ✗")
    print("=" * 70)
