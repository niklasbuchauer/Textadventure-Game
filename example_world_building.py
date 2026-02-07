"""
Example World Building Script
Demonstrates all major features of the world builder

Run this to see working examples of:
- Creating locations manually
- Using templates
- Grid generation
- Batch operations
- Copy/paste
"""

import os
import json
from world_builder import (
    load_world_data, save_world_data,
    create_room_from_template, create_room_grid,
    batch_modify_rooms, filter_rooms, copy_room,
    add_example_templates, migrate_world_format
)

WORLD_FILE = os.path.join(os.path.dirname(__file__), "world.json")


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def example_1_manual_creation():
    """Example 1: Manually create rooms and locations"""
    print_section("EXAMPLE 1: Manual Room Creation")
    
    world_data = load_world_data(WORLD_FILE)
    rooms = world_data.setdefault("rooms", {})
    
    print("\nCreating a small village manually...")
    
    # Create inn
    rooms["example_inn"] = {
        "name": "The Weary Traveler Inn",
        "description": "A cozy inn with a warm hearth and the smell of stew.",
        "location_type": "building",
        "items": {"ale": 5, "bread": 3, "bed": 2},
        "npcs": ["innkeeper"],
        "actions": {
            "order food": {"text": "The innkeeper brings you hearty stew."},
            "sleep": {"text": "You rest on a comfortable bed."}
        },
        "exits": {
            "outside": {
                "target": "example_town_square",
                "type": "named",
                "display": "Back to Town Square"
            }
        }
    }
    
    # Create town square
    rooms["example_town_square"] = {
        "name": "Town Square",
        "description": "The bustling heart of the town. Merchants and townspeople mingle.",
        "location_type": "settlement",
        "items": {"fountain": 1},
        "npcs": ["guard", "merchant"],
        "actions": {
            "drink fountain": {"text": "Cool, refreshing water."}
        },
        "exits": {
            "inn": {
                "target": "example_inn",
                "type": "named",
                "display": "The Weary Traveler Inn",
                "transition_text": "You walk toward the inn on the north side of the square."
            }
        }
    }
    
    save_world_data(WORLD_FILE, world_data)
    print(f"  ✓ Created inn: example_inn")
    print(f"  ✓ Created square: example_town_square")
    print(f"  ✓ Linked with named exit 'inn'")


def example_2_using_templates():
    """Example 2: Create rooms from templates"""
    print_section("EXAMPLE 2: Using Templates")
    
    world_data = load_world_data(WORLD_FILE)
    rooms = world_data.setdefault("rooms", {})
    
    print("\nCreating rooms from built-in templates...")
    
    # Ensure templates exist
    add_example_templates(WORLD_FILE)
    
    # Create multiple taverns from template
    for i, tavern_name in enumerate(["The Golden Dragon", "The Silver Stag"], 1):
        room_id = f"example_tavern_{i}"
        tavern = create_room_from_template(
            "tavern",
            room_id,
            variables={"tavern_name": tavern_name},
            world_file=WORLD_FILE
        )
        rooms[room_id] = tavern
        print(f"  ✓ Created {tavern_name} (ID: {room_id})")
    
    # Create forest areas
    for direction in ["north", "east", "south"]:
        room_id = f"example_forest_{direction}"
        forest = create_room_from_template(
            "forest",
            room_id,
            variables={"direction": direction.title()},
            world_file=WORLD_FILE
        )
        rooms[room_id] = forest
        print(f"  ✓ Created {direction.title()} Forest (ID: {room_id})")
    
    save_world_data(WORLD_FILE, world_data)
    print("\n  Templates used: tavern (2x), forest (3x)")


def example_3_grid_generation():
    """Example 3: Generate grids of connected rooms"""
    print_section("EXAMPLE 3: Grid Generation")
    
    print("\nGenerating a 3x3 dungeon grid (9 connected rooms)...")
    created, msg = create_room_grid(
        width=3,
        height=3,
        start_id=4000,
        location_type="building",
        world_file=WORLD_FILE,
        template_name="dungeon_cell",
        region_name="Example Dungeon"
    )
    
    if created:
        print(f"  ✓ {msg}")
        print(f"  ✓ Created rooms: {created[0]} to {created[-1]}")
        print(f"  ✓ Auto-connected in grid pattern")
        print(f"  ✓ Total rooms: {len(created)}")
    else:
        print(f"  ✗ Failed: {msg}")


def example_4_batch_operations():
    """Example 4: Modify multiple rooms with batch operations"""
    print_section("EXAMPLE 4: Batch Operations")
    
    print("\nBatch adding items to dungeon rooms...")
    
    dungeon_rooms = [str(i) for i in range(4000, 4009)]
    
    # Add treasure
    results = batch_modify_rooms(
        dungeon_rooms,
        operation="add_item",
        world_file=WORLD_FILE,
        item_name="gold coin",
        quantity=5
    )
    print(f"  ✓ Added gold coins: {results['success_count']} rooms")
    
    # Add magical item to some
    results = batch_modify_rooms(
        dungeon_rooms[:3],  # Just first 3
        operation="add_item",
        world_file=WORLD_FILE,
        item_name="crystal",
        quantity=1
    )
    print(f"  ✓ Added crystals: {results['success_count']} rooms")
    
    print("\nChanging location type of forest rooms...")
    forest_rooms = [f"example_forest_{d}" for d in ["north", "east", "south"]]
    
    results = batch_modify_rooms(
        forest_rooms,
        operation="change_location_type",
        world_file=WORLD_FILE,
        new_type="wilderness"
    )
    print(f"  ✓ Updated type: {results['success_count']} rooms")


def example_5_filtering():
    """Example 5: Filter rooms and then modify them"""
    print_section("EXAMPLE 5: Room Filtering")
    
    print("\nFinding rooms by criteria...")
    
    # Find all buildings
    buildings = filter_rooms(
        WORLD_FILE,
        criteria={"location_type": "building"}
    )
    print(f"  ✓ Found {len(buildings)} building-type rooms")
    
    # Find all settlements
    settlements = filter_rooms(
        WORLD_FILE,
        criteria={"location_type": "settlement"}
    )
    print(f"  ✓ Found {len(settlements)} settlement-type rooms")
    
    # Find all wilderness
    wilderness = filter_rooms(
        WORLD_FILE,
        criteria={"location_type": "wilderness"}
    )
    print(f"  ✓ Found {len(wilderness)} wilderness-type rooms")
    
    # Find by name
    example_rooms = filter_rooms(
        WORLD_FILE,
        criteria={"name_contains": "example"}
    )
    print(f"  ✓ Found {len(example_rooms)} rooms with 'example' in name")


def example_6_copy_paste():
    """Example 6: Copy and paste rooms"""
    print_section("EXAMPLE 6: Copy/Paste and Templates")
    
    print("\nCopying existing tavern to create variation...")
    
    new_tavern, msg = copy_room(
        source_room_id="example_tavern_1",
        new_room_id="example_tavern_copy",
        world_file=WORLD_FILE,
        copy_exits=False,
        save_as_template=False
    )
    
    if new_tavern:
        print(f"  ✓ {msg}")
        print(f"  ✓ New tavern has: {new_tavern.get('name')}")
        print(f"  ✓ Items: {list(new_tavern.get('items', {}).keys())}")
        print(f"  ✓ NPCs: {new_tavern.get('npcs', [])}")
    else:
        print(f"  ✗ Failed: {msg}")


def example_7_custom_template():
    """Example 7: Create and use a custom template"""
    print_section("EXAMPLE 7: Custom Templates")
    
    print("\nCreating custom 'shop' template...")
    
    world_data = load_world_data(WORLD_FILE)
    templates = world_data.setdefault("room_templates", {})
    
    # Create custom template
    templates["example_shop"] = {
        "name": "The {shop_name}",
        "description": "A well-stocked shop with shelves of wares.",
        "location_type": "building",
        "items": {"potion": 5, "scroll": 3, "gem": 2},
        "npcs": ["shopkeeper"],
        "actions": {
            "browse": {"text": "Fine goods at reasonable prices."},
            "buy potion": {"text": "You purchase a potion."}
        }
    }
    
    save_world_data(WORLD_FILE, world_data)
    print("  ✓ Created 'example_shop' template")
    
    # Use the template
    print("\nUsing template to create shop instances...")
    
    room = create_room_from_template(
        "example_shop",
        "example_apothecary",
        variables={"shop_name": "Apothecary"},
        world_file=WORLD_FILE
    )
    
    world_data = load_world_data(WORLD_FILE)
    world_data["rooms"]["example_apothecary"] = room
    save_world_data(WORLD_FILE, world_data)
    
    print(f"  ✓ Created shop: example_apothecary")
    print(f"  ✓ Using template: example_shop")
    print(f"  ✓ Variable substitution: 'The Apothecary'")


def example_8_complete_area():
    """Example 8: Build a complete area with multiple techniques"""
    print_section("EXAMPLE 8: Complete Area - Marketplace District")
    
    print("\nBuilding a complete marketplace district...")
    
    world_data = load_world_data(WORLD_FILE)
    rooms = world_data.setdefault("rooms", {})
    
    # Create market square (hub)
    rooms["example_market_square"] = {
        "name": "Market Square",
        "description": "A bustling marketplace with colorful stalls and merchants hawking wares.",
        "location_type": "settlement",
        "items": {"basket": 3, "apple": 10},
        "npcs": ["merchant", "customer"],
        "actions": {
            "browse stalls": {"text": "You browse the many goods on offer."}
        },
        "exits": {}
    }
    
    # Use templates for shops
    shops = ["apothecary", "armory", "general store"]
    for i, shop_name in enumerate(shops, 1):
        room_id = f"example_shop_{i}"
        room = create_room_from_template(
            "example_shop",
            room_id,
            variables={"shop_name": shop_name.title()},
            world_file=WORLD_FILE
        )
        rooms[room_id] = room
        
        # Connect back to market square
        room["exits"]["market"] = {
            "target": "example_market_square",
            "type": "named",
            "display": "Back to Market Square"
        }
    
    # Add named exits from market to shops
    rooms["example_market_square"]["exits"] = {
        "apothecary": {
            "target": "example_shop_1",
            "type": "named",
            "display": "The Apothecary"
        },
        "armory": {
            "target": "example_shop_2",
            "type": "named",
            "display": "The Armory"
        },
        "store": {
            "target": "example_shop_3",
            "type": "named",
            "display": "General Store"
        }
    }
    
    save_world_data(WORLD_FILE, world_data)
    
    print(f"  ✓ Created market square hub")
    print(f"  ✓ Created 3 shops from template")
    print(f"  ✓ Connected all locations")
    print(f"\n  Structure:")
    print(f"    Market Square (hub)")
    print(f"      ├─ Apothecary")
    print(f"      ├─ Armory")
    print(f"      └─ General Store")


def example_9_advanced_batch():
    """Example 9: Advanced batch operations"""
    print_section("EXAMPLE 9: Advanced Batch Operations")
    
    print("\nAdding items to specific room types...")
    
    # Add torches to all buildings
    buildings = filter_rooms(
        WORLD_FILE,
        criteria={"location_type": "building"}
    )
    
    if buildings:
        results = batch_modify_rooms(
            buildings,
            operation="add_item",
            world_file=WORLD_FILE,
            item_name="torch",
            quantity=1
        )
        print(f"  ✓ Added torches to {results['success_count']}/{len(buildings)} buildings")
    
    print("\nAdding exits between room groups...")
    
    # Connect market to forest
    world_data = load_world_data(WORLD_FILE)
    if "example_market_square" in world_data["rooms"]:
        world_data["rooms"]["example_market_square"]["exits"]["forest"] = {
            "target": "example_forest_north",
            "type": "direction",
            "transition_text": "You leave the market and enter the forest."
        }
        save_world_data(WORLD_FILE, world_data)
        print(f"  ✓ Connected Market Square to Forest")


def verify_examples():
    """Verify that examples were created successfully"""
    print_section("VERIFICATION")
    
    world_data = load_world_data(WORLD_FILE)
    rooms = world_data.get("rooms", {})
    
    print(f"\nTotal rooms created: {len(rooms)}")
    
    # Count by type
    types = {}
    for room in rooms.values():
        location_type = room.get("location_type", "unknown")
        types[location_type] = types.get(location_type, 0) + 1
    
    print("\nRooms by type:")
    for location_type, count in sorted(types.items()):
        print(f"  {location_type}: {count} rooms")
    
    # Check important example rooms exist
    print("\nExample rooms created:")
    example_rooms = [
        "example_town_square",
        "example_inn",
        "example_tavern_1",
        "example_tavern_2",
        "example_forest_north",
        "example_market_square",
        "example_apothecary"
    ]
    
    for room_id in example_rooms:
        if room_id in rooms:
            print(f"  ✓ {room_id}")
        else:
            print(f"  ✗ {room_id} (not found)")
    
    print("\nExample dungeon grid:")
    dungeon_rooms = [str(i) for i in range(4000, 4009)]
    existing = sum(1 for r in dungeon_rooms if r in rooms)
    print(f"  {existing}/9 rooms created (IDs 4000-4008)")


def main():
    """Run all examples"""
    print("\n" + "="*70)
    print("  WORLD BUILDER EXAMPLES")
    print("  Demonstrating all features of the bulk room creation system")
    print("="*70)
    
    try:
        # Prepare
        print("\n[Preparing] Migrating world format...")
        success, msg = migrate_world_format(WORLD_FILE)
        print(f"  {msg}")
        
        # Run examples
        example_1_manual_creation()
        example_2_using_templates()
        example_3_grid_generation()
        example_4_batch_operations()
        example_5_filtering()
        example_6_copy_paste()
        example_7_custom_template()
        example_8_complete_area()
        example_9_advanced_batch()
        
        # Verify
        verify_examples()
        
        print("\n" + "="*70)
        print("  ✓ ALL EXAMPLES COMPLETED SUCCESSFULLY")
        print("="*70)
        print("\nNext steps:")
        print("  1. Start the game: python engine.py")
        print("  2. Look around: type 'look'")
        print("  3. Navigate: type 'go north' or 'go tavern'")
        print("  4. Check inventory: type 'inventory'")
        print("  5. Open world editor: python world_editor.py")
        print("\nEdit world.json to see your new rooms!")
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
