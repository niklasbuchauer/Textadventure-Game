"""Tests for debug progression commands (level set + level up)."""

from debug_commands import handle_debug_commands
from progression_system import XP_TABLE


class MockPlayer:
    def __init__(self):
        self.current_room = "village_square"
        self.state = {"game_feel_intensity": "normal"}
        self.inventory = {}
        self.stats = {
            "gold": 0,
            "class": "warrior",
            "level": 1,
            "xp": 0,
            "xp_to_next": XP_TABLE[1],
            "skill_points": 0,
            "health": 100,
            "health_max": 100,
            "mana": 80,
            "max_mana": 80,
        }


class MockEngine:
    def __init__(self):
        self.player = MockPlayer()


def test_debug_level_up_triggers_level_up_text_marker():
    engine = MockEngine()
    result = handle_debug_commands(engine, ["level", "up"])

    assert "Level advanced:" in result
    assert "LEVEL UP: Level 2" in result
    assert engine.player.stats["level"] == 2


def test_debug_levelup_alias_accepts_count():
    engine = MockEngine()
    result = handle_debug_commands(engine, ["levelup", "2"])

    assert "Level advanced:" in result
    assert engine.player.stats["level"] >= 3


def test_debug_level_usage_shows_new_syntax():
    engine = MockEngine()
    result = handle_debug_commands(engine, ["level"])

    assert "Usage: debug level <level_number> | debug level up [count]" in result


if __name__ == "__main__":
    tests = [
        test_debug_level_up_triggers_level_up_text_marker,
        test_debug_levelup_alias_accepts_count,
        test_debug_level_usage_shows_new_syntax,
    ]
    for test_fn in tests:
        test_fn()
        print(f"PASS: {test_fn.__name__}")
    print("All debug progression command tests passed.")
