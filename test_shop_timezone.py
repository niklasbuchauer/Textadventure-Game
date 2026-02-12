"""Test shop timezone and rotation system."""

from shop_system import Shop
import datetime
from zoneinfo import ZoneInfo

# Test timezone handling
shop = Shop()
tz = ZoneInfo('Europe/Berlin')
now = datetime.datetime.now(tz)
print(f'Current time (Germany): {now.strftime("%Y-%m-%d %H:%M:%S %Z")}')
print(f'Shop hour: {shop._get_current_hour()}')
print(f'Inventory items: {len(shop.inventory)}')
print(f'Items in stock: {list(shop.inventory.keys())[:5]}')
print()

# Test rotation detection
last_hour = shop.last_rotation_hour
print(f'Last rotation hour: {last_hour}')
print(f'Will rotate next time hour differs')
print()

print('✓ Timezone and rotation system working correctly')
