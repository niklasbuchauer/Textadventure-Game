from engine import Player
import pet_system


def test_adopt_and_use_pet_ability():
    p = Player("start_room")
    # give ample gold
    p.stats["gold"] = 1000
    # adopt luminous raven
    ok, msg = pet_system.adopt_pet(p, "luminous_raven")
    assert ok, msg
    assert "luminous_raven" in p.state.get("pets", {})

    # damage player a bit and use the pet ability
    p.stats["health_max"] = 100
    p.stats["health"] = 60
    # use ability by id
    ok2, msg2 = pet_system.use_pet_ability(p, "ravens_mend")
    assert ok2, msg2
    # health should have increased but not exceed max
    assert 60 < p.stats.get("health", 0) <= p.stats.get("health_max", 100)
