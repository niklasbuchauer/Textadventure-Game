"""
Basic regression checks for elite loot table rewards.
Ensures boss and mini-boss victories grant guaranteed table drops.
"""

from combat_system import BOSS_DATABASE, MINI_BOSS_DATABASE, CombatState, generate_victory_result
from engine import GameEngine
from equipment_system import get_set_progress


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


def test_guaranteed_miniboss_table_drop():
    player = DummyPlayer()

    enemy_data = dict(MINI_BOSS_DATABASE["crystal_matriarch"])
    enemy_data["id"] = "crystal_matriarch"
    combat = CombatState(enemy_data, is_mini_boss=True, level=1)

    msg = generate_victory_result(player, combat)

    assert player.inventory.get("heart_crystal_fragment", 0) >= 1
    assert "Mini-Boss Loot Table" in msg


def test_loot_command_output():
    engine = GameEngine()
    engine.new_game()

    boss_msg = engine.process_command("loot boss")
    mini_msg = engine.process_command("loot miniboss")
    targeted_msg = engine.process_command("loot crystal titan")
    fuzzy_titan_msg = engine.process_command("loot titan")
    fuzzy_lich_msg = engine.process_command("loot lich")
    ambiguous_msg = engine.process_command("loot sovereign")

    assert "BOSS LOOT TABLES" in boss_msg
    assert "MINI-BOSS LOOT TABLES" in mini_msg
    assert "TARGETED LOOT LOOKUP" in targeted_msg
    assert "Crystal Titan" in targeted_msg
    assert "[Set: Crystal Titan Regalia]" in targeted_msg
    assert "Set Progress" in targeted_msg
    assert "owned 0/4" in targeted_msg
    assert "missing" in targeted_msg
    assert "TARGETED LOOT LOOKUP" in fuzzy_titan_msg
    assert "Crystal Titan" in fuzzy_titan_msg
    assert "TARGETED LOOT LOOKUP" in fuzzy_lich_msg
    assert "Lich King" in fuzzy_lich_msg
    assert "Multiple close matches found" in ambiguous_msg


def test_debug_loot_and_set_commands():
    engine = GameEngine()
    engine.new_game()

    dbg_loot_msg = engine.process_command("debug loot boss")
    dbg_sim_msg = engine.process_command("debug loot sim boss crystal_titan 10")
    dbg_grant_msg = engine.process_command("debug set grant crystal titan regalia equip")
    dbg_status_msg = engine.process_command("debug set status crystal titan regalia")

    assert "BOSS LOOT TABLES" in dbg_loot_msg
    assert "DEBUG ELITE LOOT SIMULATION" in dbg_sim_msg
    assert "Crystal Titan Regalia" in dbg_grant_msg
    assert "DEBUG SET STATUS" in dbg_status_msg

    progress = get_set_progress(engine.player, "Crystal Titan Regalia")
    assert progress is not None
    assert progress["owned_count"] >= 4

    dbg_clear_msg = engine.process_command("debug set clear crystal titan regalia")
    assert "Cleared Crystal Titan Regalia" in dbg_clear_msg

    progress_after = get_set_progress(engine.player, "Crystal Titan Regalia")
    assert progress_after is not None
    assert progress_after["owned_count"] == 0


def test_debug_cosmetics_commands():
    engine = GameEngine()
    engine.new_game()

    # Ensure we have an equipped weapon slot for apply testing.
    engine.process_command("debug spawn item iron_sword")
    engine.process_command("equip iron_sword")

    list_msg = engine.process_command("debug cosmetics list")
    unlock_msg = engine.process_command("debug cosmetics unlock all")
    apply_msg = engine.process_command("debug cosmetics apply weapon slayer_crimson")
    status_msg = engine.process_command("debug cosmetics status")
    reset_msg = engine.process_command("debug cosmetics reset")

    assert "DEBUG COSMETICS LIST" in list_msg
    assert "Unlocked" in unlock_msg or "unlocked" in unlock_msg
    assert "Applied" in apply_msg
    assert "COSMETICS" in status_msg
    assert "Cleared" in reset_msg


if __name__ == "__main__":
    test_guaranteed_boss_table_drop()
    test_guaranteed_miniboss_table_drop()
    test_loot_command_output()
    test_debug_loot_and_set_commands()
    test_debug_cosmetics_commands()
    print("PASS: elite loot tables and loot command")
