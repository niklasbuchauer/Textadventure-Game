"""Test progression system integration."""

from progression_system import *
from skill_tree import *

class FakePlayer:
    def __init__(self):
        self.stats = {
            'health': 100, 'gold': 0, 'level': 1, 'xp': 0, 'xp_to_next': 100,
            'skill_points': 0, 'class': 'none', 'strength': 0, 'defense': 0,
            'dexterity': 0, 'perception': 0, 'charisma': 0, 'constitution': 0
        }
        self.state = {'unlocked_skills': [], 'cooldowns': {}, 'active_effects': {}}
        self.inventory = {}
        self.visited_rooms = set()

def test_class_application():
    print("=== Test: Class Application ===")
    p = FakePlayer()
    assert p.stats["class"] == "none"
    apply_class(p, "warrior")
    assert p.stats["class"] == "warrior"
    assert p.stats["strength"] > 0, "Warrior should have strength"
    assert p.stats["defense"] > 0, "Warrior should have defense"
    print(f"  Warrior: STR={p.stats['strength']}, DEF={p.stats['defense']}, CON={p.stats['constitution']}")
    
    p2 = FakePlayer()
    apply_class(p2, "rogue")
    assert p2.stats["dexterity"] > 0, "Rogue should have dexterity"
    print(f"  Rogue: DEX={p2.stats['dexterity']}, PER={p2.stats['perception']}, CHA={p2.stats['charisma']}")
    
    p3 = FakePlayer()
    apply_class(p3, "mage")
    assert p3.stats["perception"] > 0, "Mage should have perception"
    print(f"  Mage: PER={p3.stats['perception']}, CON={p3.stats['constitution']}")
    print("  PASSED\n")

def test_xp_and_leveling():
    print("=== Test: XP and Leveling ===")
    p = FakePlayer()
    apply_class(p, "warrior")
    
    # Award XP below level threshold
    msg = award_xp(p, 50, "test")
    assert p.stats["xp"] == 50
    assert p.stats["level"] == 1
    print(f"  After 50 XP: Level={p.stats['level']}, XP={p.stats['xp']}/{p.stats['xp_to_next']}")
    
    # Award enough to level up
    msg = award_xp(p, 60, "test2")
    assert p.stats["level"] == 2, f"Should be level 2, got {p.stats['level']}"
    assert p.stats["skill_points"] > 0, "Should have skill points"
    print(f"  After 110 XP: Level={p.stats['level']}, XP={p.stats['xp']}/{p.stats['xp_to_next']}, SP={p.stats['skill_points']}")
    print(f"  Level-up message contains banner: {'LEVEL UP' in msg}")
    print("  PASSED\n")

def test_skill_trees():
    print("=== Test: Skill Trees ===")
    w_tree = get_tree_for_class("warrior")
    r_tree = get_tree_for_class("rogue")
    m_tree = get_tree_for_class("mage")
    print(f"  Warrior nodes: {len(w_tree)}")
    print(f"  Rogue nodes: {len(r_tree)}")
    print(f"  Mage nodes: {len(m_tree)}")
    assert len(w_tree) >= 10
    assert len(r_tree) >= 10
    assert len(m_tree) >= 10
    print("  PASSED\n")

def test_skill_unlock():
    print("=== Test: Skill Unlock ===")
    p = FakePlayer()
    apply_class(p, "warrior")
    p.stats["skill_points"] = 5
    
    avail = get_available_skills(p)
    print(f"  Available: {[n['id'] for n in avail]}")
    assert len(avail) > 0
    
    result = unlock_skill(p, avail[0]["id"])
    success, msg = result
    print(f"  Unlocked '{avail[0]['id']}': success={success}")
    assert success, f"Unlock failed: {msg}"
    assert p.stats["skill_points"] == 4
    assert avail[0]["id"] in p.state["unlocked_skills"]
    print("  PASSED\n")

def test_active_abilities():
    print("=== Test: Active Abilities ===")
    p = FakePlayer()
    apply_class(p, "warrior")
    p.stats["skill_points"] = 10
    
    # Unlock prerequisite then shield bash
    unlock_skill(p, "w_toughened_skin")
    unlock_skill(p, "w_iron_grip")
    unlock_skill(p, "w_shield_bash")
    
    abilities = get_active_abilities(p)
    print(f"  Active abilities: {[a['name'] for a in abilities]}")
    assert len(abilities) > 0
    
    result = use_ability(p, "shield_bash")
    print(f"  Used shield_bash: {result[:80]}...")
    assert "active_effects" in p.state
    effects = p.state["active_effects"]
    print(f"  Effects: {effects}")
    
    # Tick to reduce duration
    tick_effects(p)
    print(f"  After tick: {p.state['active_effects']}")
    print("  PASSED\n")

def test_class_selection_text():
    print("=== Test: Class Selection Text ===")
    text = get_class_selection_text()
    assert "Warrior" in text
    assert "Rogue" in text
    assert "Mage" in text
    assert "1" in text and "2" in text and "3" in text
    print(f"  Text length: {len(text)} chars")
    print("  PASSED\n")

def test_stat_modifiers():
    print("=== Test: Stat Modifiers ===")
    p = FakePlayer()
    apply_class(p, "rogue")
    dex = get_stat_modifier(p, "dexterity")
    per = get_stat_modifier(p, "perception")
    cha = get_stat_modifier(p, "charisma")
    print(f"  Rogue modifiers - DEX: {dex}, PER: {per}, CHA: {cha}")
    assert dex > 0
    assert per > 0
    print("  PASSED\n")

def test_xp_awards_dict():
    print("=== Test: XP Awards Config ===")
    expected = ["first_visit_room", "survive_trap", "disarm_trap_easy", "open_chest_wooden", "sell_item",
                "craft_basic", "complete_dialogue", "discover_secret_room"]
    for key in expected:
        assert key in XP_AWARDS, f"Missing XP_AWARDS key: {key}"
        print(f"  {key}: {XP_AWARDS[key]} XP")
    print("  PASSED\n")

if __name__ == "__main__":
    test_class_application()
    test_xp_and_leveling()
    test_skill_trees()
    test_skill_unlock()
    test_active_abilities()
    test_class_selection_text()
    test_stat_modifiers()
    test_xp_awards_dict()
    print("=" * 50)
    print("ALL TESTS PASSED!")
    print("=" * 50)
