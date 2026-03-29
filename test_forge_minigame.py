#!/usr/bin/env python3
"""Test script to check for forge minigame issues."""

import sys
import traceback

try:
    print("Testing forge minigame imports...")
    from forging_system import ForgingSystem, ForgingOverlay, FORGING_RECIPES
    print("✓ Imports successful")
    
    # Test that the overlay can be instantiated
    print("\nTesting ForgingOverlay instantiation...")
    
    # Mock the system and engine
    class MockEngine:
        def __init__(self):
            self.gui = None
            self.player = None
    
    class MockSystem:
        def __init__(self):
            self.engine = MockEngine()
        
        def _apply_forge(self, recipe, quality="normal"):
            return f"Forged with {quality} quality"
    
    system = MockSystem()
    recipe = FORGING_RECIPES.get("forged_iron_sword", {})
    
    if recipe:
        print(f"Using recipe: {recipe.get('name', 'unknown')}")
        overlay = ForgingOverlay(system, recipe)
        print(f"✓ ForgingOverlay created successfully")
        
        # Test the _finish method
        print("\nTesting _finish method...")
        overlay._perfect_rounds = 2
        overlay._total_rounds = 3
        overlay._finish()
        print(f"✓ _finish() executed: {overlay._result_text}")
    else:
        print("✗ No forging recipe found")
    
    print("\n✓ All tests passed!")
    
except Exception as e:
    print(f"\n✗ Error occurred:")
    print(f"  {type(e).__name__}: {e}")
    traceback.print_exc()
    sys.exit(1)
