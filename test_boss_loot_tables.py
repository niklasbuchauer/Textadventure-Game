"""
Basic regression checks for boss loot table rewards.
Ensures boss victories grant guaranteed boss-table drops.
"""

from combat_system import BOSS_DATABASE, CombatState, generate_victory_result


class DummyPlayer:
    def __init__(self):
        self.stats = {"gold": 0}
        self.state = {}
        self.inventory = {}


def test_guaranteed_boss_table_drop():
    player = DummyPlayer()

    enemy_data = dict(BOSS_DATABASE["crystal_titan"])
    enemy_data["id"] = "crystal_titan"
    combat = CombatState(enemy_data, is_boss=True, level=1)

    msg = generate_victory_result(player, combat)

    assert player.inventory.get("heart_crystal_fragment", 0) >= 1
    assert "Boss Loot Table" in msg


if __name__ == "__main__":
    test_guaranteed_boss_table_drop()
    print("PASS: boss loot table guaranteed drop")
