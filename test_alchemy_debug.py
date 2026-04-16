"""
Test script to debug alchemy minigame crash with actual game simulation
"""
import sys
sys.path.insert(0, '.')

# More complete pygame mock
class MockFont:
    def metrics(self, text):
        text = str(text)
        return [(0, 0, 8, 8, 8) for _ in text] or [(0, 0, 8, 8, 8)]

    def render(self, text, aa, color):
        width = max(1, len(str(text)) * 8)
        return MockSurface((width, 16))

class MockFontModule:
    @staticmethod
    def Font(name, size):
        return MockFont()
    @staticmethod
    def SysFont(name, size, bold=False, italic=False):
        return MockFont()
    @staticmethod
    def init():
        pass

class MockSurface:
    def __init__(self, size=(1000, 800), flags=0):
        if isinstance(size, tuple):
            self.width, self.height = size
        else:
            self.width = self.height = 100
    
    def get_size(self):
        return (self.width, self.height)

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height
    
    def get_rect(self):
        class Rect:
            topleft = (0, 0)
        return Rect()
    
    def blit(self, src, dest):
        pass
    
    def fill(self, color):
        pass

class MockDraw:
    @staticmethod
    def rect(*args, **kwargs):
        pass
    @staticmethod
    def line(*args, **kwargs):
        pass

class MockEvent:
    KEYDOWN = 1
    K_SPACE = 32
    K_RETURN = 13

class MockTime:
    tick_count = 0
    @staticmethod
    def get_ticks():
        MockTime.tick_count += 16
        return MockTime.tick_count

# Create full pygame mock
import types
pygame = types.ModuleType('pygame')
pygame.SRCALPHA = 65536
pygame.KEYDOWN = 1
pygame.K_SPACE = 32
pygame.K_RETURN = 13
pygame.font = MockFontModule()
pygame.draw = MockDraw()
pygame.time = MockTime()
pygame.Surface = MockSurface
pygame.event = MockEvent()

def mock_init():
    pass
pygame.init = mock_init

sys.modules['pygame'] = pygame
sys.modules['pygame.draw'] = MockDraw
sys.modules['pygame.time'] = MockTime
sys.modules['pygame.font'] = MockFontModule

# Mock ascii_art properly
class MockAscii:
    ANIMATION_FRAMES = {"alchemy_brew": [["═" * 10], ["≈" * 10]]}
    
    @staticmethod
    def render_ascii_block(*args, **kwargs):
        pass
    
    @staticmethod
    def render_title(*args, **kwargs):
        pass
    
    @staticmethod
    def render_label(*args, **kwargs):
        pass
    
    @staticmethod
    def draw_dim_overlay(*args, **kwargs):
        pass
    
    @staticmethod
    def draw_panel(*args, **kwargs):
        pass
    
    @staticmethod
    def draw_timer_bar(*args, **kwargs):
        pass
    
    @staticmethod
    def _ensure_fonts():
        pass
    
    @staticmethod
    def get_diff_params(tier=2):
        return {
            "bar_speed_mult": 1.0,
            "zone_mult": 1.0,
            "heat_rate_mult": 1.0,
            "flash_mult": 1.0,
            "seq_delta": 0,
            "result_secs": 0.0,
            "timer_mult": 1.0
        }
    
    @staticmethod
    def infer_recipe_tier(ing):
        return 2

sys.modules['ascii_art'] = MockAscii()

# Now import and test
print("Testing alchemy minigame...")
try:
    from alchemy_system import AlchemyOverlay, AlchemySystem, ALCHEMY_RECIPES
    print("✓ Imports successful")
except Exception as e:
    print(f"✗ Import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Create mock engine and system
class MockEngine:
    gui = []

class MockAlchemySystem:
    def __init__(self):
        self.engine = MockEngine()
    
    def _apply_brew(self, recipe, quality="normal"):
        return f"{quality.upper()} {recipe['name']}"

# Test with brew_mana recipe
try:
    system = MockAlchemySystem()
    recipe = ALCHEMY_RECIPES["brew_mana"]
    overlay = AlchemyOverlay(system, recipe)
    print(f"✓ AlchemyOverlay created for {recipe['name']}")
    
    # Simulate a few update cycles
    print("\nSimulating game loop...")
    surface = MockSurface()
    
    for i in range(5):
        dt = 0.016  # ~60 FPS
        overlay.update(dt)
        overlay.render(surface)
        print(f"  Frame {i+1}: heat={overlay._heat:.2f}, running={overlay.running}")
    
    print("✓ Game loop simulation successful!")
    
except Exception as e:
    print(f"✗ Error during simulation: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n✓ All tests passed!")
