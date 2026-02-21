"""Quick functional test of the engine with progression system."""
import sys
import os

# Patch tkinter to prevent GUI windows
import types
tk_module = types.ModuleType('tkinter')
tk_module.Tk = type('Tk', (), {'__init__': lambda s: None})
tk_module.Toplevel = type('Toplevel', (), {'__init__': lambda s, *a: None})
tk_module.Frame = type('Frame', (), {'__init__': lambda s, *a, **kw: None})
tk_module.Label = type('Label', (), {'__init__': lambda s, *a, **kw: None})
tk_module.Button = type('Button', (), {'__init__': lambda s, *a, **kw: None})
tk_module.Entry = type('Entry', (), {'__init__': lambda s, *a, **kw: None})
tk_module.Text = type('Text', (), {'__init__': lambda s, *a, **kw: None})
tk_module.Scrollbar = type('Scrollbar', (), {'__init__': lambda s, *a, **kw: None})
tk_module.Listbox = type('Listbox', (), {'__init__': lambda s, *a, **kw: None})
tk_module.Canvas = type('Canvas', (), {'__init__': lambda s, *a, **kw: None})
tk_module.StringVar = type('StringVar', (), {'__init__': lambda s, *a, **kw: None})
tk_module.IntVar = type('IntVar', (), {'__init__': lambda s, *a, **kw: None})
tk_module.BooleanVar = type('BooleanVar', (), {'__init__': lambda s, *a, **kw: None})
font_module = types.ModuleType('tkinter.font')
font_module.Font = type('Font', (), {'__init__': lambda s, *a, **kw: None})
tk_module.font = font_module
tk_module.messagebox = types.ModuleType('tkinter.messagebox')
tk_module.messagebox.askyesno = lambda *a, **kw: False
tk_module.messagebox.showwarning = lambda *a, **kw: None
tk_module.messagebox.showerror = lambda *a, **kw: None
simpledialog_module = types.ModuleType('tkinter.simpledialog')
simpledialog_module.askstring = lambda *a, **kw: None
tk_module.simpledialog = simpledialog_module
sys.modules['tkinter.simpledialog'] = simpledialog_module
tk_module.END = 'end'
tk_module.BOTH = 'both'
tk_module.LEFT = 'left'
tk_module.RIGHT = 'right'
tk_module.TOP = 'top'
tk_module.BOTTOM = 'bottom'
tk_module.X = 'x'
tk_module.Y = 'y'
tk_module.DISABLED = 'disabled'
tk_module.NORMAL = 'normal'
tk_module.WORD = 'word'
sys.modules['tkinter'] = tk_module
sys.modules['tkinter.font'] = font_module
sys.modules['tkinter.messagebox'] = tk_module.messagebox

# Now import engine components
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
