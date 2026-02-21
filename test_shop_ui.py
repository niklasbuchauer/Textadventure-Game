#!/usr/bin/env python3
"""
Test script for the new beautiful shop UI.
"""

from shop_system import Shop, Shopkeeper, ShopUI, ITEM_DATABASE
import sys


class MockPlayer:
    """Mock player for testing."""
    def __init__(self):
        self.id = "test_player"
        self.gold = 500
        self.stats = {"gold": 500}
        self.inventory = {
            "rope_coil": {"name": "Rope Coil", "quantity": 2, "value": 20},
            "torch": {"name": "Torch", "quantity": 3, "value": 3},
        }


def test_shop_welcome():
    """Test showing the shop welcome screen."""
    print("\n" + "="*60)
    print("TEST: Shop Welcome Screen")
    print("="*60)
    
    shop = Shop("village_shop")
    shop_ui = ShopUI(shop)
    shop_ui.show_shop_welcome()


def test_shop_inventory():
    """Test showing shop inventory."""
    print("\n" + "="*60)
    print("TEST: Shop Inventory Display")
    print("="*60)
    
    shop = Shop("village_shop")
    shop_ui = ShopUI(shop)
    player = MockPlayer()
    shop_ui.show_shop_inventory(player)


def test_shop_info():
    """Test showing shop info."""
    print("\n" + "="*60)
    print("TEST: Shop Info Display")
    print("="*60)
    
    shop = Shop("village_shop")
    shop_ui = ShopUI(shop)
    shop_ui.show_shop_info()


def test_buy_item():
    """Test buying an item."""
    print("\n" + "="*60)
    print("TEST: Buy Item (Success)")
    print("="*60)
    
    shop = Shop("village_shop")
    shop_ui = ShopUI(shop)
    player = MockPlayer()
    
    # Get first available item
    if shop_ui.shop_inventory:
        item_id = list(shop_ui.shop_inventory.keys())[0]
        print(f"\nTrying to buy: {item_id}")
        result = shop_ui.buy_item(player, item_id)
        print(f"Purchase successful: {result}")
    else:
        print("No items in shop inventory!")


def test_buy_insufficient_funds():
    """Test buying with insufficient funds."""
    print("\n" + "="*60)
    print("TEST: Buy Item (Insufficient Funds)")
    print("="*60)
    
    shop = Shop("village_shop")
    shop_ui = ShopUI(shop)
    player = MockPlayer()
    player.gold = 1  # Very low gold
    player.stats["gold"] = 1
    
    # Get first available item
    if shop_ui.shop_inventory:
        item_id = list(shop_ui.shop_inventory.keys())[0]
        print(f"\nTrying to buy {item_id} with only 1 gold:")
        result = shop_ui.buy_item(player, item_id)
        print(f"Purchase result: {result}")


def test_sell_fair():
    """Test selling an item at fair price."""
    print("\n" + "="*60)
    print("TEST: Sell Item (Fair Price)")
    print("="*60)
    
    shop = Shop("village_shop")
    shop_ui = ShopUI(shop)
    player = MockPlayer()
    
    # Try to sell rope_coil at 60% of value  (value is 20, so asking 12)
    item_id = "rope_coil"
    true_value = ITEM_DATABASE[item_id]["value"]
    asking_price = int(true_value * 0.65)  # Fair deal range
    
    print(f"\nTrying to sell {item_id} (value: {true_value}g) for {asking_price}g:")
    result = shop_ui.sell_item(player, item_id, asking_price)
    print(f"Sell result: {result}")


def test_sell_too_low():
    """Test selling at too low a price."""
    print("\n" + "="*60)
    print("TEST: Sell Item (Too Low - Insulting Offer)")
    print("="*60)
    
    shop = Shop("village_shop")
    shop_ui = ShopUI(shop)
    player = MockPlayer()
    
    # Try to sell rope_coil at 20% of value (insulting)
    item_id = "rope_coil"
    true_value = ITEM_DATABASE[item_id]["value"]
    asking_price = int(true_value * 0.20)  # Too low
    
    print(f"\nTrying to sell {item_id} (value: {true_value}g) for {asking_price}g:")
    result = shop_ui.sell_item(player, item_id, asking_price)
    print(f"Sell result: {result}")


def test_sell_outrageous():
    """Test selling at outrageous price."""
    print("\n" + "="*60)
    print("TEST: Sell Item (Outrageous Price)")
    print("="*60)
    
    shop = Shop("village_shop")
    shop_ui = ShopUI(shop)
    player = MockPlayer()
    
    # Try to sell rope_coil at 200% of value (outrageous)
    item_id = "rope_coil"
    true_value = ITEM_DATABASE[item_id]["value"]
    asking_price = int(true_value * 2.0)  # Outrageous
    
    print(f"\nTrying to sell {item_id} (value: {true_value}g) for {asking_price}g:")
    result = shop_ui.sell_item(player, item_id, asking_price)
    print(f"Sell result: {result}")


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("SHOP UI BEAUTIFUL ASCII ART TEST SUITE")
    print("="*60)
    
    try:
        test_shop_welcome()
        test_shop_inventory()
        test_shop_info()
        test_buy_item()
        test_buy_insufficient_funds()
        test_sell_fair()
        test_sell_too_low()
        test_sell_outrageous()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
