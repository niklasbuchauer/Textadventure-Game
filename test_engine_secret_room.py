#!/usr/bin/env python3
"""Test script for secret room discovery methods in the engine."""

import sys
sys.path.insert(0, 'C:\\Users\\nikbu\\Documents\\Coding\\Unitopia style game')

from engine import CommandHandler, GameEngine, Room
from dungeon_instance import DungeonInstance

def test_engine_methods():
    """Test that engine methods exist and work with discovered secrets."""
    print("=" * 70)
    print("Testing Engine Secret Room Methods")
    print("=" * 70)
    
    # Create a mock engine and command handler
    engine = GameEngine()
    engine.load_game(interactive=False)
    
    handler = CommandHandler(engine)
    
    # Test that methods exist
    if not hasattr(handler, '_examine'):
        print("✗ _examine method NOT found")
        return False
    print("✓ _examine method found")
    
    if not hasattr(handler, '_discover_secret_room'):
        print("✗ _discover_secret_room method NOT found")
        return False
    print("✓ _discover_secret_room method found")
    
    if not hasattr(handler, '_enter_secret_room'):
        print("✗ _enter_secret_room method NOT found")
        return False
    print("✓ _enter_secret_room method found")
    
    # Test discovery logic with mock room dict
    print("\n--- Testing Discovery Logic ---")
    boss_room = {
        "name": "💎 TREASURE VAULT 💎",
        "description": "The final chamber of the dungeon",
        "is_boss_room": True,
        "has_secret": True,
        "secret_room_id": "dungeon_12345_floor3_room8_secret",
        "exits": {}
    }
    
    # Test _discover_secret_room with dict
    result = handler._discover_secret_room(boss_room)
    if "secret" in result.lower() and "revealed" in result.lower():
        print("✓ Secret discovery message correct")
    else:
        print(f"✗ Secret discovery message incorrect: {result}")
        return False
    
    if engine.player.state.get("secret_discovered"):
        print("✓ secret_discovered flag set after discovery")
    else:
        print("✗ secret_discovered flag NOT set")
        return False
    
    # Test discovery with no secret
    print("\n--- Testing Non-Secret Room ---")
    normal_room = {
        "name": "Normal Room",
        "description": "A regular room",
        "is_boss_room": False,
        "has_secret": False,
        "exits": {}
    }
    
    engine.player.state["secret_discovered"] = False
    result = handler._discover_secret_room(normal_room)
    if "nothing unusual" in result.lower():
        print("✓ Correctly indicated no secret")
    else:
        print(f"✗ Unexpected result for normal room: {result}")
        return False
    
    if not engine.player.state.get("secret_discovered"):
        print("✓ secret_discovered flag NOT set for normal room")
    else:
        print("✗ secret_discovered flag incorrectly set")
        return False
    
    return True
if __name__ == "__main__":
    print("\nRunning Engine Method Tests\n")
    
    success = test_engine_methods()
    
    print("\n" + "=" * 70)
    if success:
        print("✓ ENGINE METHOD TESTS PASSED!")
    else:
        print("✗ ENGINE METHOD TESTS FAILED!")
    print("=" * 70)
