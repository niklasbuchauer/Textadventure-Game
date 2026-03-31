"""
Regression checks for elite equipment set bonuses.
"""

from equipment_system import (
    equip_item,
    unequip_item,
    get_active_set_bonuses,
    get_active_set_utility_effects,
)


class DummyPlayer:
    def __init__(self):
        self.inventory = {
            "titans_crystalline_edge": 1,
            "titans_carapace": 1,
            "prismatic_crown": 1,
            "heart_of_the_titan": 1,
        }
        self.state = {}
        self.stats = {
            "strength": 0,
            "defense": 0,
            "perception": 0,
            "constitution": 0,
            "charisma": 0,
        }


def test_crystal_set_two_piece_activation():
    player = DummyPlayer()

    ok, _ = equip_item(player, "titans_crystalline_edge")
    assert ok
    ok, _ = equip_item(player, "titans_carapace")
    assert ok

    active_sets, totals = get_active_set_bonuses(player)
    assert any(s["set_id"] == "crystal_titan_regalia" and s["tier"] >= 2 for s in active_sets)
    assert totals.get("strength", 0) >= 2
    assert totals.get("defense", 0) >= 2


def test_set_bonus_removed_on_unequip():
    player = DummyPlayer()

    equip_item(player, "titans_crystalline_edge")
    equip_item(player, "titans_carapace")
    ok, _ = unequip_item(player, "armor")
    assert ok

    active_sets, totals = get_active_set_bonuses(player)
    assert not any(s["set_id"] == "crystal_titan_regalia" and s["tier"] >= 2 for s in active_sets)
    assert totals.get("strength", 0) == 0
    assert totals.get("defense", 0) == 0


def test_crystal_set_four_piece_utility_effects():
    player = DummyPlayer()

    equip_item(player, "titans_crystalline_edge")
    equip_item(player, "titans_carapace")
    equip_item(player, "prismatic_crown")
    equip_item(player, "heart_of_the_titan")

    active_sets, totals = get_active_set_bonuses(player)
    utility = get_active_set_utility_effects(player)
    assert any(s["set_id"] == "crystal_titan_regalia" and s["tier"] >= 4 for s in active_sets)
    assert totals.get("strength", 0) >= 6
    assert utility.get("combat_gold_mult", 1.0) >= 1.10


if __name__ == "__main__":
    test_crystal_set_two_piece_activation()
    test_set_bonus_removed_on_unequip()
    test_crystal_set_four_piece_utility_effects()
    print("PASS: set bonus activation and removal")
