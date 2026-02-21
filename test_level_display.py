"""Test the enemy level display in combat UI."""
from combat_system import create_enemy_instance, create_boss_instance, get_combat_status

# Create a simple mock player
class MockPlayer:
    def __init__(self):
        self.stats = {
            "health": 80,
            "health_max": 100
        }
        self.state = {}

player = MockPlayer()

# Test regular enemy at different levels
print("=== REGULAR ENEMY (Floor 1) ===")
enemy_floor1 = create_enemy_instance('crystal_beetle', floor_num=1)
print(get_combat_status(player, enemy_floor1))

print("\n=== REGULAR ENEMY (Floor 3) ===")
enemy_floor3 = create_enemy_instance('crystal_beetle', floor_num=3)
print(get_combat_status(player, enemy_floor3))

print("\n=== BOSS (Floor 1) ===")
boss_floor1 = create_boss_instance('crystal_caverns', floor_num=1)
print(get_combat_status(player, boss_floor1))

print("\n=== BOSS (Floor 3) ===")
boss_floor3 = create_boss_instance('crystal_caverns', floor_num=3)
print(get_combat_status(player, boss_floor3))

print("\n=== CUSTOM LEVEL (Lv.15) ===")
enemy_lv15 = create_enemy_instance('crystal_beetle', level=15)
print(get_combat_status(player, enemy_lv15))
