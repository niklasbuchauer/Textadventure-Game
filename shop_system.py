"""
Shop System with NPC Shopkeeper and Negotiation
Handles shop inventory rotation, buying/selling, and dynamic shopkeeper dialogue.
"""

import datetime
from zoneinfo import ZoneInfo
import random


# Items available for purchase at the shop
# These are useful crafting/common items, not too rare but occasional good items
SHOP_INVENTORY_POOL = {
    # Common crafting materials (high spawn chance)
    "rope_coil": {"value": 20, "rarity": "common", "spawn_chance": 0.35},
    "quality_torch": {"value": 15, "rarity": "common", "spawn_chance": 0.32},
    "lockpick_set": {"value": 50, "rarity": "common", "spawn_chance": 0.25},
    "coin_pouch": {"value": 20, "rarity": "common", "spawn_chance": 0.30},
    "craftsman_hammer": {"value": 38, "rarity": "common", "spawn_chance": 0.25},
    "healing_salve": {"value": 35, "rarity": "common", "spawn_chance": 0.30},
    "iron_key": {"value": 25, "rarity": "common", "spawn_chance": 0.20},
    "torch": {"value": 3, "rarity": "common", "spawn_chance": 0.35},
    
    # Decent tools/equipment (medium spawn chance)
    "steel_dagger": {"value": 35, "rarity": "uncommon", "spawn_chance": 0.18},
    "iron_sword": {"value": 30, "rarity": "uncommon", "spawn_chance": 0.15},
    "leather_armor_piece": {"value": 25, "rarity": "uncommon", "spawn_chance": 0.12},
    "silver_ring": {"value": 40, "rarity": "uncommon", "spawn_chance": 0.15},
    "worn_map": {"value": 45, "rarity": "uncommon", "spawn_chance": 0.12},
    "enchanted_candle": {"value": 55, "rarity": "uncommon", "spawn_chance": 0.10},
    
    # Rare better items (low spawn chance but still meaningful)
    "healing_potion": {"value": 85, "rarity": "rare", "spawn_chance": 0.08},
    "spell_scroll": {"value": 95, "rarity": "rare", "spawn_chance": 0.08},
    "ancient_coin": {"value": 60, "rarity": "rare", "spawn_chance": 0.05},
    "magic_amulet": {"value": 130, "rarity": "rare", "spawn_chance": 0.05},
}


class Shop:
    """Manages shop inventory rotation and pricing."""
    
    def __init__(self, shop_id="village_shop"):
        """Initialize shop with automatic hourly inventory rotation."""
        self.shop_id = shop_id
        self.timezone = self._get_timezone()
        self.inventory = {}
        self.last_rotation_hour = self._get_current_hour()
        self.generate_inventory()
    
    def _get_timezone(self):
        """Get Germany timezone."""
        try:
            return ZoneInfo('Europe/Berlin')
        except Exception:
            return None
    
    def _get_current_time(self):
        """Get current time in Germany timezone."""
        if self.timezone:
            return datetime.datetime.now(self.timezone)
        return datetime.datetime.now()
    
    def _get_current_hour(self):
        """Get current hour (0-23)."""
        return self._get_current_time().hour
    
    def check_and_rotate(self):
        """Check if an hour has passed and rotate inventory if needed."""
        current_hour = self._get_current_hour()
        if current_hour != self.last_rotation_hour:
            self.generate_inventory()
            self.last_rotation_hour = current_hour
            return True
        return False
    
    def generate_inventory(self):
        """Generate random inventory based on spawn chances."""
        self.inventory = {}
        for item_name, item_data in SHOP_INVENTORY_POOL.items():
            if random.random() < item_data["spawn_chance"]:
                quantity = random.randint(1, 3)
                self.inventory[item_name] = {
                    "quantity": quantity,
                    "value": item_data["value"],
                    "rarity": item_data["rarity"]
                }
    
    def get_inventory(self):
        """Return current inventory with formatting."""
        if not self.inventory:
            return "The shop appears to be empty today."
        
        items_by_rarity = {"common": [], "uncommon": [], "rare": []}
        for item_name, item_data in sorted(self.inventory.items()):
            qty = item_data["quantity"]
            price = item_data["value"]
            rarity = item_data["rarity"]
            items_by_rarity[rarity].append((item_name, qty, price))
        
        result = ""
        
        # Common items
        if items_by_rarity["common"]:
            result += "═ COMMON WARES ══════════════════════════════════════\n"
            for item_name, qty, price in items_by_rarity["common"]:
                result += f"  {item_name:30s} {qty:2d}x @ {price:3d}g\n"
            result += "\n"
        
        # Uncommon items
        if items_by_rarity["uncommon"]:
            result += "═ QUALITY GOODS ════════════════════════════════════\n"
            for item_name, qty, price in items_by_rarity["uncommon"]:
                result += f"  {item_name:30s} {qty:2d}x @ {price:3d}g\n"
            result += "\n"
        
        # Rare items
        if items_by_rarity["rare"]:
            result += "═ RARE FINDS ═══════════════════════════════════════\n"
            for item_name, qty, price in items_by_rarity["rare"]:
                result += f"  {item_name:30s} {qty:2d}x @ {price:3d}g\n"
            result += "\n"
        
        return result
    
    def can_buy(self, item_name):
        """Check if item is available for purchase."""
        return item_name in self.inventory and self.inventory[item_name]["quantity"] > 0
    
    def get_buy_price(self, item_name):
        """Get the shop's asking price for an item."""
        if item_name not in self.inventory:
            return None
        return self.inventory[item_name]["value"]
    
    def buy_item(self, item_name):
        """Remove item from shop inventory."""
        if self.can_buy(item_name):
            self.inventory[item_name]["quantity"] -= 1
            if self.inventory[item_name]["quantity"] <= 0:
                del self.inventory[item_name]
            return True
        return False
    
    def format_inventory(self):
        """Return formatted inventory display for UI."""
        return self.get_inventory()


class Shopkeeper:
    """NPC Shopkeeper with dialogue and negotiation system."""
    
    def __init__(self, shop):
        """Initialize shopkeeper."""
        self.shop = shop
        self.player_negotiations = {}  # Track refused sales
        self.last_offer_price = {}  # Track last offer prices
        
        self.greetings = [
            "Well met, traveler! Looking for something useful?",
            "Welcome to my humble shop. Browse at your leisure.",
            "Come in, come in! I've got some fine wares today.",
            "Ah, a customer! I was just organizing my inventory.",
        ]
        
        self.buying_dialogue = [
            "That'll be {price} gold, friend.",
            "You're looking at {price} gold for that one.",
            "That fine item? {price} gold, and it's a bargain too.",
            "Just {price} gold. It's a steal at that price.",
        ]
        
        self.farewell = [
            "Come back anytime! I'll have fresh stock next hour.",
            "Safe travels, friend!",
            "Thank you for your business!",
            "See you next hour when I rotate my inventory!",
        ]
    
    def greet(self):
        """Return a random greeting."""
        return random.choice(self.greetings)
    
    def farewell_message(self):
        """Return a random farewell."""
        return random.choice(self.farewell)
    
    def negotiate_price(self, item_name, player_offered_price, original_value):
        """
        Negotiate selling price with player.
        Returns: (accepted, final_price, dialogue)
        
        Strategy:
        - Offer too low (< 30% of value): Shopkeeper refuses (permanent)
        - Low offer (30-50% of value): Shopkeeper counters at ~75% value
        - Fair offer (50-85% of value): Shopkeeper accepts at ~80% of offered
        - Good offer (85-100% of value): Shopkeeper accepts most of it
        - Asking full value or more: Shopkeeper laughs, counters at 60-70%
        """
        
        # Check if player already failed to sell this item
        if item_name in self.player_negotiations and self.player_negotiations[item_name]["refused"]:
            return (False, 0, 
                   "I've already decided. The answer is no. Don't bother asking again.")
        
        percent_offered = (player_offered_price / original_value) * 100 if original_value > 0 else 0
        
        # Way too low offer - refuse permanently
        if percent_offered < 30:
            self.player_negotiations[item_name] = {"refused": True, "price": 0}
            dialogues = [
                f"You're offering {player_offered_price}g for something worth {original_value}g? I don't think so.",
                "That's insulting. I won't buy at that price.",
                f"Come on, {player_offered_price}g? I can get better items for that. No deal.",
            ]
            return (False, 0, random.choice(dialogues))
        
        # Low offer - counter offer
        elif percent_offered < 50:
            counter = int(original_value * 0.75)
            dialogues = [
                f"I appreciate the offer, but that's too low. How about {counter}g?",
                f"Not bad, but I was thinking more like {counter}g.",
                f"{player_offered_price}g? I need at least {counter}g.",
            ]
            self.last_offer_price[item_name] = counter
            return (False, counter, random.choice(dialogues))
        
        # Fair offer - accept most of it
        elif percent_offered < 85:
            accepted_price = int(player_offered_price * 0.8)
            dialogues = [
                f"That's closer. I'll take {accepted_price}g.",
                f"Fair enough. {accepted_price}g and we have a deal.",
                f"I can work with {accepted_price}g.",
            ]
            self.player_negotiations[item_name] = {"refused": False, "price": accepted_price}
            return (True, accepted_price, random.choice(dialogues))
        
        # Good to excellent offer
        else:
            # Accept most of what they offered
            accepted_price = int(player_offered_price * 0.95)
            dialogues = [
                f"Now THAT'S what I'm talking about! {accepted_price}g and it's yours.",
                f"You drive a hard bargain, friend. {accepted_price}g, final offer.",
                f"I respect a fair deal. {accepted_price}g works for me.",
            ]
            self.player_negotiations[item_name] = {"refused": False, "price": accepted_price}
            return (True, accepted_price, random.choice(dialogues))
    
    def get_buy_response(self, item_name, price):
        """Get response when player buys an item."""
        dialogue = random.choice(self.buying_dialogue)
        return dialogue.format(price=price)
    
    def get_item_not_found_response(self):
        """Response when requested item not found."""
        responses = [
            "Sorry, I don't stock that item.",
            "That's not something I currently have.",
            "Not today, friend. Check back next hour.",
            "I don't have that right now.",
        ]
        return random.choice(responses)
