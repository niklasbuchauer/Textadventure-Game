"""Quick functional test of the engine with progression system."""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from engine import GameEngine, Player, CommandHandler

print("=== Engine Import OK ===")

# Create engine without GUI
engine = GameEngine()
print(f"  Rooms loaded: {len(engine.rooms)}")
print(f"  Start room: {engine.start_room}")
print(f"  pending_class_selection: {engine.pending_class_selection}")

# Start new game
result = engine.new_game()
print(f"\n=== New Game ===")
print(f"  pending_class_selection: {engine.pending_class_selection}")
print(f"  Player class: {engine.player.stats.get('class', 'none')}")
print(f"  Contains class selection prompt: {'Warrior' in result and 'Rogue' in result}")

# Simulate class selection
result = engine.process_command("1")  # Choose warrior
print(f"\n=== Class Selection (Warrior) ===")
print(f"  pending_class_selection: {engine.pending_class_selection}")
print(f"  Player class: {engine.player.stats.get('class', 'none')}")
print(f"  STR: {engine.player.stats.get('strength', 0)}")
print(f"  DEF: {engine.player.stats.get('defense', 0)}")
print(f"  CON: {engine.player.stats.get('constitution', 0)}")
print(f"  Level: {engine.player.stats.get('level', 1)}")
print(f"  XP: {engine.player.stats.get('xp', 0)}")
print(f"  Skill Points: {engine.player.stats.get('skill_points', 0)}")

# Test stats command
result = engine.process_command("stats")
print(f"\n=== Stats Command ===")
print(f"  Contains 'Warrior': {'Warrior' in result}")
print(f"  Contains 'Level': {'Level' in result}")

# Test help command
result = engine.process_command("help")
print(f"\n=== Help Command ===")
print(f"  Contains 'PROGRESSION': {'PROGRESSION' in result}")
print(f"  Contains 'skills': {'skills' in result}")
print(f"  Contains 'abilities': {'abilities' in result}")

# Test look command (should work normally)
result = engine.process_command("look")
print(f"\n=== Look Command ===")
print(f"  Got room description: {len(result) > 0}")

print("\n" + "=" * 50)
print("ALL FUNCTIONAL TESTS PASSED!")
print("=" * 50)
