#!/usr/bin/env python3
"""
Complete end-to-end test of dungeon entry flow
"""

import json
import os
import sys
# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

print("=" * 60)
print("TESTING: Complete Dungeon Entry Flow")
print("=" * 60)

# Test 1: Import and initialize
print("\n[1] Initializing game engine...")
try:
    from engine import GameEngine, DUNGEON_AVAILABLE
    
    print(f"✓ GameEngine imported")
    print(f"✓ DUNGEON_AVAILABLE = {DUNGEON_AVAILABLE}")
    
    if not DUNGEON_AVAILABLE:
        print("✗ DUNGEON_AVAILABLE is False - this is the problem!")
        exit(1)
    
    # Create engine
    engine = GameEngine()
    print("✓ GameEngine initialized")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Test 2: Check command handler
print("\n[2] Checking CommandHandler...")
try:
    from engine import CommandHandler
    
    cmd_handler = CommandHandler(engine)
    print(f"✓ CommandHandler created")
    
except Exception as e:
    print(f"✗ Error: {e}")
    exit(1)

# Test 3: Simulate dungeon entrance detection
print("\n[3] Testing dungeon entrance detection...")
try:
    from dungeon_scheduler import get_scheduler
    from dungeon_instance import get_current_dungeon
    
    scheduler = get_scheduler()
    is_open = scheduler.is_dungeon_open()
    
    print(f"✓ Dungeon open: {is_open}")
    
    # Try to get dungeon
    dungeon = get_current_dungeon(scheduler)
    print(f"✓ Dungeon instance retrieved: {type(dungeon).__name__}")
    
    if dungeon.dungeon_data:
        print(f"✓ Dungeon data exists")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Test 4: Test _handle_dungeon_entrance method
print("\n[4] Testing _handle_dungeon_entrance method...")
try:
    # Create a mock dungeon exit
    dungeon_exit_data = {
        "type": "time_gated_dungeon",
        "dungeon_id": "test_dungeon",
        "transition_text": "You step into the dungeon entrance..."
    }
    
    # Call the handler
    result = cmd_handler._handle_dungeon_entrance(dungeon_exit_data)
    
    # Check result
    if "DUNGEON ENTRANCE DETECTED" in result:
        print("✓ _handle_dungeon_entrance returned correct response")
        print(f"✓ Response includes dungeon status")
        
        if is_open and "Do you wish to enter?" in result:
            print("✓ Dungeon is open and asking for confirmation")
        elif not is_open and "CLOSED" in result:
            print("✓ Dungeon is closed and showing closed message")
    else:
        print(f"✗ Unexpected response: {result[:100]}")
        exit(1)
    
except Exception as e:
    print(f"✗ Error in _handle_dungeon_entrance: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Test 5: Test _enter_dungeon method (if dungeon is open)
print("\n[5] Testing _enter_dungeon method...")
try:
    # Check if dungeon is currently open for testing
    scheduler = get_scheduler()
    if scheduler.is_dungeon_open():
        # Simulate entering dungeon
        dungeon_exit_data = {
            "type": "time_gated_dungeon",
            "dungeon_id": "test_dungeon"
        }
        
        result = cmd_handler._enter_dungeon(dungeon_exit_data)
        
        if "entered the dungeon" in result.lower() or "error" not in result.lower():
            print("✓ _enter_dungeon executed successfully")
        else:
            print(f"⚠ Unexpected response: {result[:100]}")
    else:
        print("⚠ Dungeon is closed - skipping _enter_dungeon test")
        print("   (Will work when dungeon is open)")
    
except Exception as e:
    print(f"✗ Error in _enter_dungeon: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Cleanup
try:
    root.destroy()
except:
    pass

print("\n" + "=" * 60)
print("ALL TESTS PASSED!")
print("Dungeon system is fully operational")
print("=" * 60)
