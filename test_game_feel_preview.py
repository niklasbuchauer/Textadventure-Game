"""Smoke test for hidden game-feel preview command behavior."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from engine import GameEngine


def _bootstrap_engine():
    engine = GameEngine()
    engine.new_game()
    # Choose Warrior so command flow is fully active.
    engine.process_command("1")
    return engine


def test_preview_modes_and_hidden_help():
    engine = _bootstrap_engine()

    # The preview command should remain hidden from normal player help.
    help_text = engine.process_command("help").lower()
    assert "feel preview" not in help_text
    assert "preview feel" not in help_text

    # Low profile preview should render compact command sample style.
    low_text = engine.process_command("feel preview low")
    assert "GAME FEEL PREVIEW" in low_text
    assert "[LOW]" in low_text
    assert "COMMANDS (COMPACT)" in low_text

    # Normal profile preview should include default command panel header.
    normal_text = engine.process_command("feel preview normal")
    assert "[NORMAL]" in normal_text
    assert "AVAILABLE COMMANDS" in normal_text

    # High profile preview should render high section and never persist override.
    high_text = engine.process_command("feel preview high")
    assert "[HIGH]" in high_text

    # Preview must not leave a temporary override behind.
    assert "game_feel_preview_override" not in engine.player.state
    assert engine.get_game_feel_intensity() == "normal"


if __name__ == "__main__":
    test_preview_modes_and_hidden_help()
    print("[PASS] test_game_feel_preview")
