import random

from engine import Player
from combat_system import CombatState, process_player_defend
import pet_system


def _build_player():
    p = Player("room")
    p.stats.update({
        "level": 30,
        "gold": 99999,
        "health": 200,
        "health_max": 200,
        "mana": 120,
        "max_mana": 120,
        "strength": 14,
        "defense": 10,
        "dexterity": 8,
        "perception": 8,
        "constitution": 7,
        "crit_chance": 0,
    })
    p.state.setdefault("achievements", ["boss_slayer", "dungeon_master", "void_titan_slayer"])
    return p


def test_pet_roster_is_large_enough():
    assert len(pet_system.PETS) >= 20


def test_high_tier_pet_has_gates():
    p = Player("room")
    p.stats["gold"] = 99999
    p.stats["level"] = 5
    p.state["achievements"] = []

    ok, msg = pet_system.adopt_pet(p, "astral_phoenix")
    assert not ok
    assert "requires player level" in msg.lower() or "requires achievement" in msg.lower()


def test_high_tier_pet_adoption_with_requirements_met():
    p = _build_player()
    p.inventory["star_fragment"] = 20
    p.inventory["void_essence"] = 20

    ok, msg = pet_system.adopt_pet(p, "astral_phoenix")
    assert ok, msg
    assert "astral_phoenix" in p.state.get("pets", {})


def test_quest_gated_pet_requires_completed_quest():
    p = _build_player()
    p.inventory["star_fragment"] = 20
    p.inventory["sun_shard"] = 20
    p.state["completed_quests"] = []

    ok, msg = pet_system.adopt_pet(p, "celestial_gryphon")
    assert not ok
    assert "requires completed quest" in msg.lower()

    p.state["completed_quests"] = ["sky_trial"]
    ok2, msg2 = pet_system.adopt_pet(p, "celestial_gryphon")
    assert ok2, msg2


def test_hybrid_pet_combat_turn_triggers():
    p = _build_player()
    ok, msg = pet_system.adopt_pet(p, "spirit_wolf")
    assert ok, msg
    pet_system.activate_pet(p, "spirit_wolf")

    enemy = {
        "id": "test_dummy",
        "name": "Training Dummy",
        "description": "A patient sparring target.",
        "hp": 400,
        "attack": 6,
        "defense": 12,
        "xp_reward": 1,
        "gold_reward": 1,
        "loot": [],
        "abilities": [],
    }

    random.seed(7)
    combat = CombatState(enemy, level=1)
    process_player_defend(p, combat)
    assert combat.pet_combatant is not None
    assert str(combat.pet_combatant.get("pet_id", "")) == "spirit_wolf"


def test_pet_injury_aftermath_and_bandage_recovery():
    p = _build_player()
    ok, msg = pet_system.adopt_pet(p, "spirit_wolf")
    assert ok, msg

    # Simulate a finished combat where the pet was knocked out.
    class _DummyCombat:
        pass

    c = _DummyCombat()
    c.pet_knocked = True
    c.pet_combatant = {
        "pet_id": "spirit_wolf",
        "pet_name": "Spirit Wolf",
    }

    aftermath = pet_system.apply_pet_combat_aftermath(p, c)
    assert "injured" in aftermath.lower()
    injury = p.state.get("pet_injured", {}).get("spirit_wolf", {})
    assert isinstance(injury, dict)
    assert injury.get("severity") == "critical"
    assert int(injury.get("wins_left", 0)) >= 1

    # Recover with a bandage item.
    p.inventory["bandage"] = 1
    ok2, msg2 = pet_system.bandage_active_pet(p)
    assert ok2, msg2
    assert "bandage" in msg2.lower() or "recover" in msg2.lower()
    injury_after = p.state.get("pet_injured", {}).get("spirit_wolf", {})
    assert not injury_after.get("severity")


def test_injury_auto_recovers_after_wins():
    p = _build_player()
    ok, msg = pet_system.adopt_pet(p, "spirit_wolf")
    assert ok, msg

    p.state.setdefault("pet_injured", {})["spirit_wolf"] = {
        "severity": "light",
        "wins_left": 1,
    }

    msg2 = pet_system.advance_pet_recovery(p, wins=1)
    assert "Recovered" in msg2
    injury = p.state.get("pet_injured", {}).get("spirit_wolf", {})
    assert not injury.get("severity")


if __name__ == "__main__":
    test_pet_roster_is_large_enough()
    test_high_tier_pet_has_gates()
    test_high_tier_pet_adoption_with_requirements_met()
    test_quest_gated_pet_requires_completed_quest()
    test_hybrid_pet_combat_turn_triggers()
    test_pet_injury_aftermath_and_bandage_recovery()
    test_injury_auto_recovers_after_wins()
