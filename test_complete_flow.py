#!/usr/bin/env python3
"""Complete integration test for dungeon connectivity and secret room discovery."""

import sys
sys.path.insert(0, 'C:\\Users\\nikbu\\Documents\\Coding\\Unitopia style game')

from dungeon_generator import DungeonGenerator
import random

def test_multiple_seeds():
    """Test dungeon generation with multiple seeds to ensure consistency."""
    print("=" * 80)
    print("TESTING MULTIPLE DUNGEON GENERATIONS")
    print("=" * 80)
    
    generator = DungeonGenerator()
    
    # Test 10 different seeds
    test_seeds = [12345, 99999, 54321, 11111, 22222, 33333, 44444, 55555, 66666, 77777]
    
    all_pass = True
    total_disconnected = 0
    total_floors_checked = 0
    total_secrets_found = 0
    
    for seed in test_seeds:
        print(f"\n--- Testing Seed {seed} ---")
        
        dungeon = generator.generate_complete_dungeon(seed)
        
        # Check each floor
        for floor_num in sorted(dungeon["floors"].keys()):
            total_floors_checked += 1
            floor_data = dungeon["floors"][floor_num]
            rooms = floor_data["rooms"]
            entrance = floor_data.get("entrance_room")
            
            # BFS connectivity check
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
                        
                        if target and target in rooms and "_secret" not in target:
                            queue.append(target)
            
            # Check disconnected (excluding secret rooms)
            public_rooms = [rid for rid in rooms.keys() if "_secret" not in rid]
            disconnected = set(public_rooms) - visited
            
            if disconnected:
                print(f"  ❌ Floor {floor_num}: {len(disconnected)} disconnected rooms!")
                all_pass = False
                total_disconnected += len(disconnected)
            else:
                print(f"  ✓ Floor {floor_num}: All {len(public_rooms)} public rooms connected")
            
            # Check for secret room on final floor
            if floor_data.get("boss_room"):
                boss_room_id = floor_data["boss_room"]
                boss_room = rooms[boss_room_id]
                
                if boss_room.get("has_secret"):
                    secret_id = boss_room.get("secret_room_id")
                    if secret_id and secret_id in rooms:
                        print(f"  ✓ Floor {floor_num}: Secret room found ({secret_id})")
                        total_secrets_found += 1
                    else:
                        print(f"  ❌ Floor {floor_num}: Secret room ID in boss but not in rooms!")
                        all_pass = False
                else:
                    print(f"  ❌ Floor {floor_num}: Boss room has NO secret!")
                    all_pass = False
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Seeds tested: {len(test_seeds)}")
    print(f"Floors checked: {total_floors_checked}")
    print(f"Total disconnected rooms: {total_disconnected}")
    print(f"Secret rooms found: {total_secrets_found}")
    
    if all_pass and total_disconnected == 0:
        print("\n✓✓✓ ALL TESTS PASSED! ✓✓✓")
        print("All dungeons have:")
        print("  - 100% room connectivity")
        print("  - Secret rooms on all boss floors")
        print("  - Proper exit configuration")
        return True
    else:
        print("\n❌❌❌ SOME TESTS FAILED! ❌❌❌")
        return False

if __name__ == "__main__":
    success = test_multiple_seeds()
    sys.exit(0 if success else 1)
