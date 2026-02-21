"""
Quick manual test to see what the help command outputs
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from engine import GameEngine

engine = GameEngine()
if not engine.player:
    engine.new_game()

print("Testing 'help' command:")
print("="*80)
response = engine.process_command("help")
print(response)
print("="*80)
print(f"\nResponse length: {len(response)} characters")
print(f"Contains '[MOVEMENT]': {('[MOVEMENT]' in response)}")
print(f"Contains '[EXPLORATION]': {('[EXPLORATION]' in response)}")
print(f"Contains 'AVAILABLE COMMANDS': {('AVAILABLE COMMANDS' in response)}")
