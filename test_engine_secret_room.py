#!/usr/bin/env python3
"""Test script for secret room discovery methods in the engine."""

import sys
sys.path.insert(0, 'C:\\Users\\nikbu\\Documents\\Coding\\Unitopia style game')

from engine import CommandHandler, GameEngine, Room
from dungeon_instance import DungeonInstance
from easter_egg_data import get_easter_egg_room_payload

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


def test_non_boss_secret_route_payload():
    """Regression: non-boss hidden rooms should still route through _enter_secret_room."""
    print("\n--- Testing Non-Boss Secret Route ---")

    engine = GameEngine()
    engine.load_game(interactive=False)
    handler = CommandHandler(engine)

    start_room = Room({
        "name": "Chapel",
        "description": "Quiet and old.",
        "exits": {"secret": {"target": "underground_archive", "type": "secret"}},
    })
    start_room.is_boss_room = False
    start_room.secret_discovered = True
    secret_room = Room({
        "name": "Underground Archive",
        "description": "A hidden archive chamber.",
        "exits": {"back": "chapel"},
    })
    engine.rooms["chapel"] = start_room
    engine.rooms["underground_archive"] = secret_room
    engine.player.current_room = "chapel"

    result = handler._go("secret")
    payload = getattr(engine, "pending_easter_egg_room", None)

    if engine.player.current_room == "underground_archive":
        print("✓ Player moved to secret room")
    else:
        print(f"✗ Player did not move to secret room: {engine.player.current_room}")
        return False

    if isinstance(payload, dict) and payload.get("room_id") == "underground_archive":
        print("✓ Easter egg payload prepared")
    else:
        print(f"✗ Missing/incorrect easter egg payload: {payload}")
        return False

    layout = payload.get("layout") if isinstance(payload, dict) else None
    hotspots = layout.get("hotspots") if isinstance(layout, dict) else None
    if isinstance(layout, dict) and isinstance(hotspots, list) and hotspots:
        print("✓ Layout and hotspot metadata present")
    else:
        print(f"✗ Missing layout/hotspot metadata: {layout}")
        return False

    interactions = payload.get("interactions") if isinstance(payload, dict) else None
    if isinstance(interactions, list) and interactions and all("action_id" in i for i in interactions):
        print("✓ Interactions expose stable action IDs")
    else:
        print(f"✗ Missing action IDs in interactions: {interactions}")
        return False

    if "SECRET ROOM" in (result or "") and "_" not in (result or ""):
        print("✓ Fallback text returned without ascii wall")
    else:
        print(f"✗ Unexpected fallback text: {result}")
        return False

    return True


def test_easter_egg_content_depth():
    """Regression: easter egg rooms should ship with rich hotspot content."""
    print("\n--- Testing Easter Egg Content Depth ---")

    lab = get_easter_egg_room_payload("hidden_alchemy_lab", "Hidden Alchemy Lab", "A practical workshop")
    lab_layout = lab.get("layout", {})
    lab_hotspots = lab_layout.get("hotspots", []) if isinstance(lab_layout, dict) else []
    lab_interactions = lab.get("interactions", [])

    if len(lab_hotspots) >= 5 and len(lab_interactions) >= 5:
        print("✓ Hidden Alchemy Lab has dense hotspot content")
    else:
        print(f"✗ Hidden Alchemy Lab content too shallow: hotspots={len(lab_hotspots)}, interactions={len(lab_interactions)}")
        return False

    if all(isinstance(x.get("text", ""), str) and len(x.get("text", "").strip()) > 120 for x in lab_interactions if x.get("type") == "note"):
        print("✓ Hidden Alchemy Lab notes are long-form")
    else:
        print("✗ Hidden Alchemy Lab notes are still too short")
        return False

    archive = get_easter_egg_room_payload("underground_archive", "Underground Archive", "Archive")
    if len(archive.get("interactions", [])) >= 5:
        print("✓ Archive room includes expanded interaction set")
    else:
        print("✗ Archive room interaction count too low")
        return False

    return True


if __name__ == "__main__":
    print("\nRunning Engine Method Tests\n")
    
    success = test_engine_methods()
    success = test_non_boss_secret_route_payload() and success
    success = test_easter_egg_content_depth() and success
    
    print("\n" + "=" * 70)
    if success:
        print("✓ ENGINE METHOD TESTS PASSED!")
    else:
        print("✗ ENGINE METHOD TESTS FAILED!")
    print("=" * 70)
