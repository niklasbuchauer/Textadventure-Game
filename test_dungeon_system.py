#!/usr/bin/env python3
"""
Test suite for the fixed dungeon system with timezone fallback handling.
"""

import sys
import os

print("=" * 80)
print("DUNGEON SYSTEM - TIMEZONE FIX TEST")
print("=" * 80)

# Test 1: Check dungeon scheduler initialization
print("\n[TEST 1] Dungeon scheduler initialization...")
try:
    from dungeon_scheduler import DungeonScheduler
    
    scheduler = DungeonScheduler()
    print(f"  [PASS] Scheduler initialized")
    print(f"  Timezone: {scheduler.timezone_name}")
    print(f"  Using fallback: {scheduler.using_fallback}")
    print(f"  Dungeon open: {scheduler.is_dungeon_open()}")
    print(f"  Status: {scheduler.get_status_message()}")
    
except Exception as e:
    print(f"  [FAIL] Error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Test 2: Check game engine initialization
print("\n[TEST 2] Game engine initialization...")
try:
    import engine
    
    print(f"  [PASS] Engine loaded")
    print(f"  DUNGEON_AVAILABLE: {engine.DUNGEON_AVAILABLE}")
    
    if engine.DUNGEON_AVAILABLE:
        print(f"  [PASS] Dungeon system ENABLED")
    else:
        print(f"  [FAIL] Dungeon system DISABLED: {engine._DUNGEON_IMPORT_ERROR}")
        exit(1)
        
except Exception as e:
    print(f"  [FAIL] Error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Test 3: Check dungeon instance creation
print("\n[TEST 3] Dungeon instance creation...")
try:
    from dungeon_instance import DungeonInstance
    from dungeon_scheduler import get_scheduler
    
    scheduler = get_scheduler()
    seed = 12345
    
    instance = DungeonInstance(seed=seed, scheduler=scheduler)
    print(f"  [PASS] Instance created")
    print(f"  Seed: {instance.seed}")
    print(f"  Timezone: {instance.scheduler.timezone_name}")
    print(f"  Active: {instance.active}")
    print(f"  Dungeon data generated: {instance.dungeon_data is not None}")
    
except Exception as e:
    print(f"  [FAIL] Error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Test 4: Summary
print("\n" + "=" * 80)
print("ALL TESTS PASSED")
print("=" * 80)
print()
print("Summary:")
print("  - DungeonScheduler initializes with timezone (or fallback)")
print("  - Game engine successfully initializes dungeon system")
print("  - DungeonInstance can be created and dungeon data generated")
print("  - No timezone-related errors")
print()
print("The dungeon system is ready to use!")
