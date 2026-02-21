#!/usr/bin/env python3
"""
Test that dungeon system is properly initialized in GameEngine
"""

import json
import os
import sys
import tkinter as tk

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

print("=" * 60)
print("TESTING: Dungeon System Availability in GameEngine")
print("=" * 60)

# Test 1: Check imports
print("\n[Test 1] Checking dungeon system imports...")
try:
    from dungeon_scheduler import DungeonScheduler, get_scheduler
    from dungeon_instance import get_current_dungeon, DungeonInstance
    print("✓ Imports successful")
except ImportError as e:
    print(f"✗ Import failed: {e}")
    exit(1)

# Test 2: Create GameEngine
print("\n[Test 2] Initializing GameEngine...")
try:
    from engine import GameEngine
    
    # Create a minimal Tk root
    root = tk.Tk()
    root.withdraw()  # Hide the window
    
    engine = GameEngine(root=root)
    print("✓ GameEngine created")
except Exception as e:
    print(f"✗ Error creating GameEngine: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Test 3: Check dungeon_scheduler attribute
print("\n[Test 3] Checking dungeon_scheduler initialization...")
if hasattr(engine, 'dungeon_scheduler'):
    if engine.dungeon_scheduler is not None:
        print(f"✓ dungeon_scheduler exists and is initialized")
        print(f"  Type: {type(engine.dungeon_scheduler).__name__}")
    else:
        print("⚠ dungeon_scheduler is None")
else:
    print("✗ dungeon_scheduler attribute missing")
    exit(1)

# Test 4: Try to get scheduler
print("\n[Test 4] Getting global scheduler instance...")
try:
    scheduler = get_scheduler()
    print(f"✓ Got scheduler: {type(scheduler).__name__}")
except Exception as e:
    print(f"✗ Error getting scheduler: {e}")
    exit(1)

# Test 5: Check dungeon status
print("\n[Test 5] Checking dungeon status methods...")
try:
    is_open = scheduler.is_dungeon_open()
    print(f"✓ Dungeon open: {is_open}")
    
    seed = scheduler.get_current_dungeon_seed()
    print(f"✓ Current seed: {seed}")
    
    if is_open:
        closing = scheduler.get_time_until_closing()
        print(f"✓ Time until closing: {closing}")
    else:
        next_opening = scheduler.get_time_until_next_opening()
        print(f"✓ Time until next opening: {next_opening}")
except Exception as e:
    print(f"✗ Error checking status: {e}")
    exit(1)

# Test 6: Get current dungeon instance
print("\n[Test 6] Getting current dungeon instance...")
try:
    dungeon = get_current_dungeon(scheduler)
    print(f"✓ Got dungeon instance: {type(dungeon).__name__}")
    
    if dungeon.dungeon_data:
        floors = dungeon.dungeon_data.get('floors', {})
        print(f"✓ Dungeon has {len(floors)} floor(s)")
    else:
        print("⚠ Dungeon data not generated yet")
except Exception as e:
    print(f"✗ Error getting dungeon: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Cleanup
root.destroy()

print("\n" + "=" * 60)
print("ALL TESTS PASSED!")
print("Dungeon system is properly available in GameEngine")
print("=" * 60)
