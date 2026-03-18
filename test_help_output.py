"""
Quick manual test to see what the help command outputs
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from engine import GameEngine
from debug_commands import handle_debug_commands

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

print("\nTesting debug menu entries:")
debug_menu = handle_debug_commands(engine, [])
print(f"Contains 'debug home free': {('debug home free' in debug_menu)}")
print(f"Contains 'debug home items': {('debug home items' in debug_menu)}")
print(f"Contains 'debug home reset': {('debug home reset' in debug_menu)}")
