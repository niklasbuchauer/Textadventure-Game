"""Test the debug spawn command with level parameter."""
from engine import GameEngine

# Create engine instance
engine = GameEngine()

# Import the debug command
from debug_commands import handle_debug_commands

# Test spawning without level
print("=== Test 1: Spawn enemy without level ===")
result = handle_debug_commands(engine, ["spawn", "enemy", "crystal_beetle"])
print(result[:500] if result else "No result")  # Print first 500 chars

# Test spawning with level
print("\n=== Test 2: Spawn enemy with level 10 ===")
result = handle_debug_commands(engine, ["spawn", "enemy", "crystal_beetle", "10"])
print(result[:500] if result else "No result")

# Test spawning a boss with level
print("\n=== Test 3: Spawn boss with level 20 ===")
result = handle_debug_commands(engine, ["spawn", "enemy", "crystal_titan", "20"])
print(result[:500] if result else "No result")

# Test invalid level
print("\n=== Test 4: Invalid level parameter ===")
result = handle_debug_commands(engine, ["spawn", "enemy", "crystal_beetle", "xyz"])
print(result)

# Test help command (list enemies)
print("\n=== Test 5: List enemies command ===")
result = handle_debug_commands(engine, ["enemies"])
# Show just the usage line
lines = result.split('\n')
for line in lines[-3:]:
    print(line)
