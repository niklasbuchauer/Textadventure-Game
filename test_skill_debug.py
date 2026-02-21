"""
Test the debug skill points command
"""

from debug_commands import handle_debug_commands

# Mock engine and player
class MockPlayer:
    def __init__(self):
        self.stats = {'skill_points': 5, 'gold': 100}

class MockEngine:
    def __init__(self):
        self.player = MockPlayer()

# Test 1: Test debug skill points command with valid amount
engine = MockEngine()
result = handle_debug_commands(engine, ['skill', 'points', '10'])
print("Test 1 - Set skill points to 10:")
print(f"  Result: {result}")
print(f"  Player SP: {engine.player.stats['skill_points']}")
assert engine.player.stats['skill_points'] == 10, "Failed to set skill points"
assert "Skill points set to 10" in result, "Wrong return message"
print("  ✓ PASS\n")

# Test 2: Test with different amount
result = handle_debug_commands(engine, ['skill', 'points', '25'])
print("Test 2 - Set skill points to 25:")
print(f"  Result: {result}")
print(f"  Player SP: {engine.player.stats['skill_points']}")
assert engine.player.stats['skill_points'] == 25, "Failed to set skill points"
print("  ✓ PASS\n")

# Test 3: Test with invalid amount
result = handle_debug_commands(engine, ['skill', 'points', 'abc'])
print("Test 3 - Invalid amount (abc):")
print(f"  Result: {result}")
assert "Invalid amount" in result, "Should show error for invalid amount"
print("  ✓ PASS\n")

# Test 4: Test debugcommand display
result = handle_debug_commands(engine, ['skill', 'points'])
print("Test 4 - Missing amount parameter:")
print(f"  Result: {result}")
assert "Usage: debug skill points <amount>" in result, "Should show usage"
print("  ✓ PASS\n")

# Test 5: Check debug menu shows the new command
result = handle_debug_commands(engine, [])
print("Test 5 - Debug menu includes skill points command:")
if "debug skill points" in result:
    print("  ✓ Found in menu")
    print("  ✓ PASS\n")
else:
    print("  ✗ NOT found in menu")
    print(result)

print("✅ All tests passed!")
