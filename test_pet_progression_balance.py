from engine import Player
import pet_system


def test_xp_curve_monotonic():
    values = [pet_system._xp_to_next(level) for level in range(1, pet_system.MAX_PET_LEVEL)]
    assert all(v > 0 for v in values)
    assert values == sorted(values)


def test_bonus_scaling_sanity():
    # Non-mana companion grows slowly but steadily.
    wolf_l1 = pet_system._pet_bonus_data("spirit_wolf", 1).get("perception", 0)
    wolf_l10 = pet_system._pet_bonus_data("spirit_wolf", 10).get("perception", 0)
    wolf_l30 = pet_system._pet_bonus_data("spirit_wolf", 30).get("perception", 0)
    assert 1 <= wolf_l1 <= wolf_l10 <= wolf_l30

    # Mana companion should scale faster on max_mana.
    mana_l1 = pet_system._pet_bonus_data("arcane_wisp", 1).get("max_mana", 0)
    mana_l10 = pet_system._pet_bonus_data("arcane_wisp", 10).get("max_mana", 0)
    mana_l30 = pet_system._pet_bonus_data("arcane_wisp", 30).get("max_mana", 0)
    assert 1 <= mana_l1 <= mana_l10 <= mana_l30


def test_max_level_xp_guard():
    p = Player("room")
    p.stats["gold"] = 1000
    ok, msg = pet_system.adopt_pet(p, "spirit_wolf")
    assert ok, msg

    pid = p.state.get("active_pet")
    p.state["pets"][pid]["level"] = pet_system.MAX_PET_LEVEL
    p.state["pets"][pid]["xp"] = 999

    pet_system.gain_pet_xp(p, 5000, source="test")

    assert p.state["pets"][pid]["level"] == pet_system.MAX_PET_LEVEL
    assert p.state["pets"][pid]["xp"] == 0


def test_temp_buff_refresh_does_not_stack():
    p = Player("room")
    p.stats["gold"] = 1000

    ok, msg = pet_system.adopt_pet(p, "stone_turtle")
    assert ok, msg
    pet_system.activate_pet(p, "stone_turtle")

    base_def = int(p.stats.get("defense", 0))
    ok1, msg1 = pet_system.use_pet_ability(p, "shell_guard")
    assert ok1, msg1
    after_first = int(p.stats.get("defense", 0))
    assert after_first == base_def + 2

    # Force cooldown reset while buff is still active, then reapply.
    p.state.setdefault("pet_ability_cooldowns", {})["shell_guard"] = 0
    ok2, msg2 = pet_system.use_pet_ability(p, "shell_guard")
    assert ok2, msg2
    after_second = int(p.stats.get("defense", 0))
    assert after_second == base_def + 2


if __name__ == "__main__":
    test_xp_curve_monotonic()
    test_bonus_scaling_sanity()
    test_max_level_xp_guard()
    test_temp_buff_refresh_does_not_stack()
