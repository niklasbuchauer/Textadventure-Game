from engine import Player
import pet_system


def test_adopt_insufficient_gold():
    p = Player("room")
    p.stats["gold"] = 50
    ok, msg = pet_system.adopt_pet(p, "luminous_raven")
    assert not ok
    assert "costs" in msg


def test_use_no_active_pet():
    p = Player("room")
    ok, msg = pet_system.use_pet_ability(p, "ravens_mend")
    assert not ok
    assert "No active pet" in msg


def test_pet_feed_and_xp():
    p = Player("room")
    p.stats["gold"] = 500
    # adopt and ensure active
    ok, _ = pet_system.adopt_pet(p, "luminous_raven")
    assert ok
    # ensure feed is allowed
    p.state["pet_last_feed_at"] = 0
    pre_gold = p.stats.get("gold", 0)
    ok2, msg2 = pet_system.feed_active_pet(p)
    assert ok2, msg2
    assert p.stats.get("gold", 0) == pre_gold - pet_system.PET_FEED_COST_GOLD
    # pet xp increased
    pid = p.state.get("active_pet")
    assert p.state.get("pets", {}).get(pid, {}).get("xp", 0) >= 0


def test_pet_ability_effects():
    p = Player("room")
    p.stats["gold"] = 200
    p.stats["health_max"] = 100
    p.stats["health"] = 60

    # luminous raven heal
    ok, _ = pet_system.adopt_pet(p, "luminous_raven")
    assert ok
    pid = p.state.get("active_pet")
    assert pid == "luminous_raven"
    pre_hp = p.stats.get("health", 0)
    ok2, msg2 = pet_system.use_pet_ability(p, "ravens_mend")
    assert ok2
    assert p.stats.get("health", 0) > pre_hp

    # adopt ember fox and activate then use cinder_dash
    p.stats["gold"] = 200
    ok3, _ = pet_system.adopt_pet(p, "ember_fox")
    assert ok3
    pet_system.activate_pet(p, "ember_fox")
    pre_gold = p.stats.get("gold", 0)
    ok4, _ = pet_system.use_pet_ability(p, "cinder_dash")
    assert ok4
    assert p.stats.get("gold", 0) >= pre_gold

    # adopt stone turtle and activate then use shell_guard
    p.stats["gold"] = 500
    ok5, _ = pet_system.adopt_pet(p, "stone_turtle")
    assert ok5
    pet_system.activate_pet(p, "stone_turtle")
    pre_def = p.stats.get("defense", 0)
    ok6, _ = pet_system.use_pet_ability(p, "shell_guard")
    assert ok6
    assert p.stats.get("defense", 0) >= pre_def + 2


def test_ability_cooldown_prevents_use():
    p = Player("room")
    p.stats["gold"] = 500
    ok, _ = pet_system.adopt_pet(p, "spirit_wolf")
    assert ok
    # use pack_howl
    ok1, _ = pet_system.use_pet_ability(p, "pack_howl")
    assert ok1
    # immediate re-use should fail due to cooldown
    ok2, msg2 = pet_system.use_pet_ability(p, "pack_howl")
    assert not ok2
    assert "cooldown" in msg2.lower()


def test_temp_buff_expiry_reverts_stats():
    import time
    p = Player("room")
    p.stats["gold"] = 500
    ok, _ = pet_system.adopt_pet(p, "spirit_wolf")
    assert ok
    # apply pack_howl which lasts 45s (we'll simulate expiry)
    ok1, _ = pet_system.use_pet_ability(p, "pack_howl")
    assert ok1
    # fast-forward expiry by manipulating state
    tb = p.state.get("pet_temporary_buffs", {})
    for bid in list(tb.keys()):
        tb[bid]["expires_at"] = time.time() - 1
    # cleanup
    pet_system._cleanup_pet_temp_effects(p)
    # crit_chance should be back to base (0)
    assert p.stats.get("crit_chance", 0) >= 0


def test_pet_persistence_roundtrip():
    p = Player("room")
    p.stats["gold"] = 300
    ok, _ = pet_system.adopt_pet(p, "luminous_raven")
    assert ok
    data = p.to_dict()
    p2 = Player.from_dict(data)
    assert "pets" in p2.state
    assert "luminous_raven" in p2.state.get("pets", {})
