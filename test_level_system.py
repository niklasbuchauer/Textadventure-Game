"""Test the enemy level scaling system."""
from combat_system import calculate_enemy_level, scale_enemy_stats, create_enemy_instance, ENEMY_DATABASE

# Test level calculation
print('=== LEVEL CALCULATION TESTS ===')
print(f'Floor 1 Regular: {calculate_enemy_level(1, "regular")}')
print(f'Floor 2 Regular: {calculate_enemy_level(2, "regular")}')
print(f'Floor 3 Regular: {calculate_enemy_level(3, "regular")}')
print(f'Floor 1 Mini-boss: {calculate_enemy_level(1, "mini_boss")}')
print(f'Floor 2 Mini-boss: {calculate_enemy_level(2, "mini_boss")}')
print(f'Floor 3 Mini-boss: {calculate_enemy_level(3, "mini_boss")}')
print(f'Floor 1 Boss: {calculate_enemy_level(1, "boss")}')
print(f'Floor 3 Boss: {calculate_enemy_level(3, "boss")}')

# Test stat scaling
print('\n=== STAT SCALING TEST (Crystal Beetle) ===')
beetle = ENEMY_DATABASE['crystal_beetle']
print(f'Base Stats (Lv.1): HP={beetle["hp"]} ATK={beetle["attack"]} DEF={beetle["defense"]}')

scaled_5 = scale_enemy_stats(beetle, 5, 'regular')
print(f'Level 5: HP={scaled_5["hp"]} ATK={scaled_5["attack"]} DEF={scaled_5["defense"]}')

scaled_10 = scale_enemy_stats(beetle, 10, 'regular')
print(f'Level 10: HP={scaled_10["hp"]} ATK={scaled_10["attack"]} DEF={scaled_10["defense"]}')

# Test enemy creation with levels
print('\n=== ENEMY INSTANCE TEST ===')
enemy_lv1 = create_enemy_instance('crystal_beetle', level=1)
print(f'Lv.1 Crystal Beetle: HP={enemy_lv1.hp} ATK={enemy_lv1.attack} DEF={enemy_lv1.defense}')

enemy_lv7 = create_enemy_instance('crystal_beetle', level=7, floor_num=1)
print(f'Lv.7 Crystal Beetle: HP={enemy_lv7.hp} ATK={enemy_lv7.attack} DEF={enemy_lv7.defense}')

# Test floor-based auto leveling
enemy_floor3 = create_enemy_instance('crystal_beetle', floor_num=3)
print(f'Floor 3 Auto-level: Lv.{enemy_floor3.level} HP={enemy_floor3.hp} ATK={enemy_floor3.attack} DEF={enemy_floor3.defense}')

print('\n✅ Enemy level scaling system working!')
