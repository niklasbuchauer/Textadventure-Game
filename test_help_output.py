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

box_lines = [
    ln for ln in response.splitlines()
    if ln.startswith(("╔", "╠", "╚", "║"))
]
box_widths = sorted(set(len(ln) for ln in box_lines))
print(f"Box line widths: {box_widths}")
assert len(box_widths) == 1, f"Expected one box width, found {box_widths}"

synthetic = (
    "╔════════╗\n"
    "║  sample command           - this description should wrap and keep tail_token_visible for regression coverage.║\n"
    "╚════════╝\n"
)
normalized = engine.cmd._normalize_boxed_help_output(synthetic)
assert "tail_token_visible" in normalized, "Expected wrapped boxed content to keep full tail text"

print("\nTesting debug menu entries:")
debug_menu = handle_debug_commands(engine, [])
print(f"Contains 'debug home free': {('debug home free' in debug_menu)}")
print(f"Contains 'debug home items': {('debug home items' in debug_menu)}")
print(f"Contains 'debug home reset': {('debug home reset' in debug_menu)}")
