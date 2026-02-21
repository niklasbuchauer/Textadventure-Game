"""
Quick test to verify skill tree command and button fix
"""

import sys

# Test 1: Verify imports
try:
    from skill_tree import SkillTreeWindow, get_tree_for_class, get_unlocked_skills
    from progression_system import apply_class, CLASS_DEFINITIONS, award_xp, check_level_up
    print("✓ All importable modules loaded successfully")
except Exception as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)

# Test 2: Verify SkillTreeWindow has create_window method
if hasattr(SkillTreeWindow, 'create_window'):
    print("✓ SkillTreeWindow has create_window() method")
else:
    print("✗ SkillTreeWindow missing create_window() method")
    sys.exit(1)

# Test 3: Check that toggle_skills_window supports both call paths
try:
    # Read the engine.py and verify the fix
    with open('engine.py', 'r', encoding='utf-8', errors='ignore') as f:
        engine_content = f.read()
    
    # Check if create_window() is being called in toggle_skills_window
    if 'self.skill_tree_win.create_window()' in engine_content:
        print("✓ toggle_skills_window() calls create_window()")
    else:
        print("✗ toggle_skills_window() doesn't call create_window()")
        sys.exit(1)
    
    # Check if engine is passed to SkillTreeWindow
    if 'SkillTreeWindow(self.root, player, self.engine)' in engine_content:
        print("✓ SkillTreeWindow receives engine reference")
    else:
        print("✗ SkillTreeWindow not receiving engine reference")
        sys.exit(1)
        
except Exception as e:
    print(f"✗ Error checking engine.py: {e}")
    sys.exit(1)

print("\n✅ All skill tree fixes verified successfully!")
print("\nChanges made:")
print("  1. Added create_window() call in toggle_skills_window()")
print("  2. Passed self.engine to SkillTreeWindow constructor")
print("\nBoth the 'skills' command and '⚔ Skills' button should now work.")
