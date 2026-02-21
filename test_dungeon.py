#!/usr/bin/env python3
"""
Quick test of dungeon system components
"""

print("=" * 60)
print("DUNGEON SYSTEM TEST")
print("=" * 60)

# Test 1: Scheduler
print("\n[1] Testing DungeonScheduler...")
from dungeon_scheduler import DungeonScheduler
scheduler = DungeonScheduler()
print(f"✓ Scheduler initialized")
print(f"  Status: {scheduler.get_status_message()}")
print(f"  Current seed: {scheduler.get_current_dungeon_seed()}")

# Test 2: TrapSystem
print("\n[2] Testing TrapSystem...")
from trap_system import TrapSystem
trap_system = TrapSystem()
print(f"✓ Trap system initialized")
print(f"  Available traps: {len(trap_system.TRAP_TYPES)}")
for trap_type in list(trap_system.TRAP_TYPES.keys())[:3]:
    trap = trap_system.TRAP_TYPES[trap_type]
    print(f"    - {trap['name']}")

# Test 3: DungeonGenerator
print("\n[3] Testing DungeonGenerator...")
from dungeon_generator import DungeonGenerator
gen = DungeonGenerator(12345)
dungeon = gen.generate_complete_dungeon()
print(f"✓ Dungeon generated")
print(f"  Seed: {dungeon['seed']}")
print(f"  Floors: {dungeon['num_floors']}")
for floor_num in range(1, dungeon['num_floors'] + 1):
    floor = dungeon['floors'][floor_num]
    print(f"    Floor {floor_num}: {len(floor['rooms'])} rooms")
    
# Test 4: DungeonInstance
print("\n[4] Testing DungeonInstance...")
from dungeon_instance import DungeonInstance
instance = DungeonInstance(scheduler.get_current_dungeon_seed(), scheduler)
print(f"✓ Dungeon instance created")
print(f"  Floors: {instance.dungeon_data['num_floors']}")
print(f"  Active: {instance.active}")

print("\n" + "=" * 60)
print("ALL TESTS PASSED!")
print("=" * 60)
