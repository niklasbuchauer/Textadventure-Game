"""Test script to debug alchemy minigame crash"""
import sys
sys.path.insert(0, '.')

# Mock pygame
class MockSurface:
    def __init__(self, size=(1000, 800), flags=0):
        self.width, self.height = size
    def get_size(self): return (self.width, self.height)
    def get_width(self): return self.width
    def get_height(self): return self.height
    def blit(self, *args, **kwargs): pass
    def fill(self, *args, **kwargs): pass

class MockClock:
    def get_ticks(self): return 0

class MockEvent:
    KEYDOWN = 1
    K_SPACE = 32


class MockFont:
    def metrics(self, text):
        text = str(text)
        return [(0, 0, 8, 8, 8) for _ in text] or [(0, 0, 8, 8, 8)]

    def render(self, text, aa, color, background=None):
        width = max(1, len(str(text)) * 8)
        return MockSurface((width, 16))


class MockFontModule:
    @staticmethod
    def init():
        pass

    @staticmethod
    def SysFont(name, size, bold=False, italic=False):
        return MockFont()

    @staticmethod
    def Font(name, size):
        return MockFont()


class MockDraw:
    @staticmethod
    def rect(*args, **kwargs):
        pass

    @staticmethod
    def ellipse(*args, **kwargs):
        pass

    @staticmethod
    def circle(*args, **kwargs):
        pass

class MockModule:
    SRCALPHA = 65536
    KEYDOWN = 1
    K_SPACE = 32
    K_RETURN = 13
    font = MockFontModule
    draw = MockDraw
    Surface = MockSurface
    
    class time:
        @staticmethod
        def get_ticks():
            return 0
    
sys.modules['pygame'] = MockModule()
sys.modules['pygame.draw'] = MockDraw
sys.modules['pygame.time'] = MockModule.time
sys.modules['pygame.font'] = MockFontModule

# Mock ascii_art
class MockAscii:
    ANIMATION_FRAMES = {"alchemy_brew": [["test"]]}
    
    @staticmethod
    def render_ascii_block(*args, **kwargs): pass
    @staticmethod
    def render_title(*args, **kwargs): pass
    @staticmethod
    def render_label(*args, **kwargs): pass
    @staticmethod
    def draw_dim_overlay(*args, **kwargs): pass
    @staticmethod
    def draw_panel(*args, **kwargs): pass
    @staticmethod
    def draw_timer_bar(*args, **kwargs): pass
    @staticmethod
    def _ensure_fonts(): pass
    @staticmethod
    def get_diff_params(tier=2):
        return {"bar_speed_mult":1.0,"zone_mult":1.0,"heat_rate_mult":1.0,
                "flash_mult":1.0,"seq_delta":0,"result_secs":0.0,"timer_mult":1.0}
    @staticmethod
    def infer_recipe_tier(ing): return 2

sys.modules['ascii_art'] = MockAscii()

# Now test
print("Testing alchemy minigame imports...")
try:
    from alchemy_system import AlchemyOverlay, AlchemySystem, ALCHEMY_RECIPES
    print("✓ Imports successful")
except Exception as e:
    print(f"✗ Import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\nTesting AlchemyOverlay instantiation...")
try:
    class MockEngine:
        gui = []
    
    class MockAlchemySystem:
        def __init__(self):
            self.engine = MockEngine()
        def _apply_brew(self, recipe, quality="normal"):
            return f"Brewed {recipe['name']}"
    
    system = MockAlchemySystem()
    recipe = ALCHEMY_RECIPES["brew_healing"]
    overlay = AlchemyOverlay(system, recipe)
    print(f"✓ AlchemyOverlay created successfully")
except Exception as e:
    print(f"✗ Creation failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\nTesting render method...")
try:
    surface = MockSurface()
    overlay.render(surface)
    print("✓ render() executed successfully")
except Exception as e:
    print(f"✗ render() failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n✓ All tests passed!")
