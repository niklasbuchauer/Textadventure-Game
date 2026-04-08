from engine import GameEngine


def test_pet_ability_command_aliases():
    engine = GameEngine()
    if not engine.player:
        engine.new_game()

    player = engine.player
    player.stats["gold"] = 1000

    adopt_msg = engine.process_command("pet adopt luminous_raven")
    assert "Adopted pet" in adopt_msg or "already have" in adopt_msg

    roadmap = engine.process_command("pet abilities")
    assert "LOCKED" in roadmap or "UNLOCKED" in roadmap or "ready" in roadmap

    usage_msg = engine.process_command("pet ability")
    assert "Usage: pet ability" in usage_msg

    ability_msg = engine.process_command("pet ability ravens_mend")
    assert isinstance(ability_msg, str)
    assert len(ability_msg.strip()) > 0

    bandage_msg = engine.process_command("pet bandage")
    assert isinstance(bandage_msg, str)
    assert len(bandage_msg.strip()) > 0


if __name__ == "__main__":
    test_pet_ability_command_aliases()
