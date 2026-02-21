"""Test fixed dungeon system integration."""
import sys, os
sys.path.insert(0, '.')

from engine import GameEngine, Room

def test_exit_conversion():
    """Test that _convert_dungeon_room_to_world preserves special exit types."""
    engine = GameEngine(world_file='world.json', root=None, gui=None)
    
    test_room = {
        'name': 'Test Room',
        'description': 'A test room',
        'coordinates': [0, 0],
        'exits': {
            'north': {'target': 'room_b', 'type': 'direction'},
            'leave': {'target': 'world_room', 'type': 'leave_dungeon', 'transition_text': 'You leave...'},
            'down': {'target': 'room_c', 'type': 'stairs_down', 'transition_text': 'Going down...'}
        },
        'items': {'sword': {'quantity': 2, 'value': 50}}
    }
    converted = engine._convert_dungeon_room_to_world(test_room)
    
    # Direction exit should be simplified to target string
    assert converted['exits']['north'] == 'room_b', f"Direction exit wrong: {converted['exits']['north']}"
    
    # leave_dungeon exit should preserve full dict
    leave = converted['exits']['leave']
    assert isinstance(leave, dict), f"leave_dungeon should be dict: {leave}"
    assert leave['type'] == 'leave_dungeon', f"leave type wrong: {leave}"
    assert leave['target'] == 'world_room'
    
    # stairs_down exit should preserve full dict
    down = converted['exits']['down']
    assert isinstance(down, dict), f"stairs_down should be dict: {down}"
    assert down['type'] == 'stairs_down', f"down type wrong: {down}"
    
    # Items should be converted to list format
    assert converted['items'] == ['sword', 'sword'], f"Items wrong: {converted['items']}"
    
    print("  [PASS] Exit conversion preserves special types")

def test_dungeon_entry_flow():
    """Test entering a fixed dungeon via the command handler."""
    engine = GameEngine(world_file='world.json', root=None, gui=None)
    engine.player = engine.__class__.__dict__  # Will call new_game
    result = engine.new_game()
    
    # Navigate to dungeon entrance
    cmd = engine.cmd
    
    # Move to dungeon_forest_entrance
    engine.player.current_room = 'dungeon_forest_entrance'
    engine.player.visited_rooms.add('dungeon_forest_entrance')
    
    # Try "enter" command - should detect fixed_dungeon
    result = cmd.handle("enter")
    assert "DUNGEON ENTRANCE DETECTED" in result, f"Expected dungeon entrance text, got: {result[:100]}"
    assert "Crystal Caverns" in result, f"Expected Crystal Caverns name: {result[:200]}"
    assert "ALWAYS OPEN" in result, f"Expected ALWAYS OPEN status: {result[:200]}"
    assert engine.pending_dungeon_entry is not None, "pending_dungeon_entry should be set"
    assert engine.pending_dungeon_entry.get('fixed') is True, "Should be marked as fixed"
    
    print("  [PASS] Enter command shows fixed dungeon prompt")
    
    # Say yes
    result = cmd.handle("yes")
    assert "ENTERING DUNGEON" in result, f"Expected entering text: {result[:100]}"
    assert "Crystal Cave Mouth" in result or "loaded" in result.lower(), f"Expected entrance room: {result[:200]}"
    
    # Player should now be inside the dungeon
    assert engine.player.current_room.startswith("cc_f1_"), f"Player should be in cc_f1: {engine.player.current_room}"
    assert engine.current_dungeon_instance is not None, "Dungeon instance should be set"
    assert engine.current_fixed_dungeon is not None, "Fixed dungeon data should be set"
    assert len(engine.fixed_dungeon_room_ids) > 0, "Fixed dungeon room IDs should be tracked"
    
    print(f"  [PASS] Entered Crystal Caverns (room: {engine.player.current_room})")
    print(f"  [INFO] {len(engine.fixed_dungeon_room_ids)} rooms registered")
    
    # Test movement within dungeon
    result = cmd.handle("look")
    assert "Crystal Cave Mouth" in result, f"Look should show room name: {result[:100]}"
    
    print("  [PASS] Look command works in fixed dungeon")
    
    # Test leaving the dungeon
    result = cmd.handle("leave")
    assert "left the dungeon" in result.lower() or "Dark Cave Entrance" in result, f"Expected leave text: {result[:200]}"
    assert engine.player.current_room == 'dungeon_forest_entrance', f"Should be back at entrance: {engine.player.current_room}"
    assert engine.current_dungeon_instance is None, "Dungeon instance should be cleared"
    assert engine.current_fixed_dungeon is None, "Fixed dungeon data should be cleared"
    assert len(engine.fixed_dungeon_room_ids) == 0, "Fixed dungeon room IDs should be cleared"
    
    print("  [PASS] Left dungeon successfully, back at overworld")

def test_crafting_altar():
    """Test crafting altar interaction."""
    engine = GameEngine(world_file='world.json', root=None, gui=None)
    result = engine.new_game()
    cmd = engine.cmd
    
    # Enter Crystal Caverns
    engine.player.current_room = 'dungeon_forest_entrance'
    cmd.handle("enter")
    cmd.handle("yes")
    
    # Try craft command outside altar room
    result = cmd.handle("craft")
    assert "no crafting altar" in result.lower(), f"Expected no altar message: {result[:100]}"
    
    # Move directly to the altar room
    engine.player.current_room = 'cc_f3_forge_of_light'
    engine.player.visited_rooms.add('cc_f3_forge_of_light')
    
    result = cmd.handle("craft")
    assert "Forge of Light" in result, f"Expected altar name: {result[:200]}"
    assert "coming soon" in result.lower(), f"Expected placeholder text: {result[:200]}"
    assert "found_altars" in engine.player.state, "Should track found altars"
    assert "Forge of Light" in engine.player.state["found_altars"], "Forge of Light should be in found altars"
    
    print("  [PASS] Crafting altar interaction works")
    
    # Clean up
    engine.cleanup_dungeon()

def test_all_three_dungeons():
    """Test entering and leaving all three dungeons."""
    engine = GameEngine(world_file='world.json', root=None, gui=None)
    engine.new_game()
    cmd = engine.cmd
    
    dungeons = [
        ('dungeon_forest_entrance', 'crystal_caverns', 'cc_f1_'),
        ('dungeon_mountain_entrance', 'iron_halls', 'ih_f1_'),
        ('dungeon_ruins_entrance', 'sunken_catacombs', 'sc_f1_'),
    ]
    
    for entrance, dungeon_id, prefix in dungeons:
        engine.player.current_room = entrance
        engine.player.visited_rooms.add(entrance)
        
        result = cmd.handle("enter")
        assert "DUNGEON ENTRANCE DETECTED" in result, f"Failed entrance for {dungeon_id}"
        
        result = cmd.handle("yes")
        assert engine.player.current_room.startswith(prefix), f"Wrong room for {dungeon_id}: {engine.player.current_room}"
        
        # Leave
        result = cmd.handle("leave")
        assert engine.player.current_room == entrance, f"Wrong return for {dungeon_id}: {engine.player.current_room}"
        assert engine.current_dungeon_instance is None
        
        print(f"  [PASS] {dungeon_id} entry/exit works")

def test_map_helpers():
    """Test map helper methods for fixed dungeon detection."""
    from live_map_window import LiveMapWindow
    
    # Test _current_floor_number with fixed dungeon IDs
    class FakeMap:
        current_location = 'sc_f2_something'
    
    fm = FakeMap()
    result = LiveMapWindow._current_floor_number(fm)
    assert result == 2, f"Expected floor 2 for sc_f2_something: {result}"
    
    fm.current_location = 'ih_f3_anvil'
    result = LiveMapWindow._current_floor_number(fm)
    assert result == 3, f"Expected floor 3 for ih_f3_anvil: {result}"
    
    fm.current_location = 'dungeon_123_floor1_room0'
    result = LiveMapWindow._current_floor_number(fm)
    assert result == 1, f"Expected floor 1 for procedural: {result}"
    
    print("  [PASS] Map floor number detection works for all patterns")

if __name__ == '__main__':
    print("Testing fixed dungeon system...")
    print()
    
    print("1. Exit conversion:")
    test_exit_conversion()
    
    print("\n2. Dungeon entry flow:")
    test_dungeon_entry_flow()
    
    print("\n3. Crafting altar:")
    test_crafting_altar()
    
    print("\n4. All three dungeons:")
    test_all_three_dungeons()
    
    print("\n5. Map helpers:")
    test_map_helpers()
    
    print("\n" + "=" * 50)
    print("ALL TESTS PASSED!")
    print("=" * 50)
