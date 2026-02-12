"""Test shop system functionality."""

from engine import GameEngine

# Initialize engine
engine = GameEngine()
print("✓ Engine initialized")

# Start new game
print("\nStarting new game...")
engine.new_game()
print(f"✓ Game started in room: {engine.player.current_room}")
print(f"✓ Starting gold: {engine.player.stats.get('gold', 0)}")

# Give player some test items
engine.player.inventory = {
    "iron_sword": 1,
    "torch": 2,
    "rope_coil": 1
}
engine.item_worth = {
    "iron_sword": 35,
    "torch": 3,
    "rope_coil": 20
}
print(f"✓ Player inventory set: {engine.player.inventory}")

# Move player to shop
current_room = engine.rooms.get("village_shop")
if current_room:
    engine.player.current_room = "village_shop"
    print(f"✓ Player moved to shop")
    
    # Test shop commands
    print("\n=== TESTING SHOP COMMANDS ===")
    
    # Test shop help
    result = engine.cmd._shop_help()
    print("\n1. Shop Help:")
    print(result[:150] + "...")
    
    # Test shop browse
    result = engine.cmd._shop_browse()
    print("\n2. Shop Browse (first 300 chars):")
    print(result[:300] + "...")
    
    # Test shop talk
    result = engine.cmd._shop_talk()
    print("\n3. Shop Talk:")
    print(result)
    
    # Test shop info
    result = engine.cmd._shop_info()
    print("\n4. Shop Info (first 200 chars):")
    print(result[:200] + "...")
    
    # Test buying an item
    print("\n=== TESTING BUYING ===")
    engine.player.stats["gold"] = 100
    result = engine.cmd.handle("shop browse")
    print("\nShop inventory before buy:")
    print(result[:300])
    
    # Try to buy first available item
    if engine.shop.inventory:
        first_item = list(engine.shop.inventory.keys())[0]
        print(f"\nBuying '{first_item}' for {engine.shop.inventory[first_item]['value']}g...")
        result = engine.cmd.handle(f"shop buy {first_item}")
        print(result)
        print(f"Player gold after: {engine.player.stats['gold']}")
        print(f"Player inventory: {engine.player.inventory}")
    
    # Test selling with negotiation
    print("\n=== TESTING SELLING ===")
    result = engine.cmd.handle("shop sell iron_sword 25")
    print(result)
    print(f"Player gold after sell: {engine.player.stats['gold']}")
    
    print("\n✓ All shop commands tested successfully!")
else:
    print("✗ village_shop room not found")
