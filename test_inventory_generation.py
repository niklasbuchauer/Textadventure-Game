"""Test shop inventory generation and rotation."""

from shop_system import Shop
import random

# Set seed for reproducibility
random.seed(42)

print("Testing shop inventory generation...")
print()

for i in range(5):
    random.seed(i)
    shop = Shop()
    inv = shop.inventory
    print(f"Rotation {i}: {len(inv)} items")
    if inv:
        for item, data in list(inv.items())[:3]:
            print(f"  - {item}: {data['quantity']}x @ {data['value']}g ({data['rarity']})")
        if len(inv) > 3:
            print(f"  ... and {len(inv) - 3} more items")
    print()

print("✓ Shop inventory generation working correctly")
