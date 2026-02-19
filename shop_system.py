"""
Shop System with NPC Shopkeeper and Negotiation
Handles shop inventory rotation, buying/selling, dynamic shopkeeper dialogue, and beautiful ASCII UI.
"""

import datetime
from zoneinfo import ZoneInfo
import random


# Item database with metadata for display
ITEM_DATABASE = {
    # Common crafting materials
    "rope_coil": {"name": "Rope Coil", "icon": "🪢", "desc": "Sturdy rope for climbing or binding", "value": 20, "rarity": "common", "spawn_chance": 0.35},
    "quality_torch": {"name": "Quality Torch", "icon": "🔦", "desc": "Bright and reliable light source", "value": 15, "rarity": "common", "spawn_chance": 0.32},
    "lockpick_set": {"name": "Lockpick Set", "icon": "🔓", "desc": "Tools for opening locked containers", "value": 50, "rarity": "common", "spawn_chance": 0.25},
    "coin_pouch": {"name": "Coin Pouch", "icon": "💰", "desc": "Secure leather pouch for valuables", "value": 20, "rarity": "common", "spawn_chance": 0.30},
    "craftsman_hammer": {"name": "Craftsman Hammer", "icon": "🔨", "desc": "Essential tool for the trade", "value": 38, "rarity": "common", "spawn_chance": 0.25},
    "healing_salve": {"name": "Healing Salve", "icon": "🧴", "desc": "Restores minor wounds and bruises", "value": 35, "rarity": "common", "spawn_chance": 0.30},
    "iron_key": {"name": "Iron Key", "icon": "🔑", "desc": "Unlocks iron-banded doors", "value": 25, "rarity": "common", "spawn_chance": 0.20},
    "torch": {"name": "Torch", "icon": "🔥", "desc": "Basic light source for dark places", "value": 3, "rarity": "common", "spawn_chance": 0.35},
    
    # Uncommon tools/equipment
    "steel_dagger": {"name": "Steel Dagger", "icon": "🗡️", "desc": "Reliable blade for self-defense", "value": 35, "rarity": "uncommon", "spawn_chance": 0.18},
    "iron_sword": {"name": "Iron Sword", "icon": "⚔️", "desc": "Well-forged weapon of quality", "value": 30, "rarity": "uncommon", "spawn_chance": 0.15},
    "leather_armor_piece": {"name": "Leather Armor", "icon": "🛡️", "desc": "Protects against common blows", "value": 25, "rarity": "uncommon", "spawn_chance": 0.12},
    "silver_ring": {"name": "Silver Ring", "icon": "💍", "desc": "Gleaming silver band with faint magic", "value": 40, "rarity": "uncommon", "spawn_chance": 0.15},
    "worn_map": {"name": "Worn Map", "icon": "🗺️", "desc": "Map with mysterious markings", "value": 45, "rarity": "uncommon", "spawn_chance": 0.12},
    "enchanted_candle": {"name": "Enchanted Candle", "icon": "🕯️", "desc": "Never burns out, always glows", "value": 55, "rarity": "uncommon", "spawn_chance": 0.10},
    
    # Rare items
    "healing_potion": {"name": "Healing Potion", "icon": "🧪", "desc": "Restores vitality and health", "value": 85, "rarity": "rare", "spawn_chance": 0.08},
    "spell_scroll": {"name": "Spell Scroll", "icon": "📜", "desc": "Ancient magic inscribed on parchment", "value": 95, "rarity": "rare", "spawn_chance": 0.08},
    "ancient_coin": {"name": "Ancient Coin", "icon": "🪙", "desc": "From a forgotten civilization", "value": 60, "rarity": "rare", "spawn_chance": 0.05},
    "magic_amulet": {"name": "Magic Amulet", "icon": "✨", "desc": "Radiates mysterious magical energy", "value": 130, "rarity": "rare", "spawn_chance": 0.05},
}

# ============================================================
#  ISLAND SHOP DATABASES - Themed items per island tier
# ============================================================

HARBOR_ITEM_DATABASE = {
    # Same as village but adds travel supplies
    "rope_coil": {"name": "Rope Coil", "icon": "🪢", "desc": "Sturdy rope for climbing or binding", "value": 20, "rarity": "common", "spawn_chance": 0.35},
    "quality_torch": {"name": "Quality Torch", "icon": "🔦", "desc": "Bright and reliable light source", "value": 15, "rarity": "common", "spawn_chance": 0.32},
    "healing_salve": {"name": "Healing Salve", "icon": "🧴", "desc": "Restores minor wounds and bruises", "value": 35, "rarity": "common", "spawn_chance": 0.30},
    "sailors_compass": {"name": "Sailor's Compass", "icon": "🧭", "desc": "Never lose your way at sea", "value": 45, "rarity": "common", "spawn_chance": 0.25},
    "sea_rations": {"name": "Sea Rations", "icon": "🥫", "desc": "Preserved food for long voyages", "value": 18, "rarity": "common", "spawn_chance": 0.35},
    "waterproof_satchel": {"name": "Waterproof Satchel", "icon": "🎒", "desc": "Keeps your gear dry in any storm", "value": 55, "rarity": "uncommon", "spawn_chance": 0.18},
    "iron_sword": {"name": "Iron Sword", "icon": "⚔️", "desc": "Well-forged weapon of quality", "value": 30, "rarity": "uncommon", "spawn_chance": 0.15},
    "leather_armor_piece": {"name": "Leather Armor", "icon": "🛡️", "desc": "Protects against common blows", "value": 25, "rarity": "uncommon", "spawn_chance": 0.12},
    "healing_potion": {"name": "Healing Potion", "icon": "🧪", "desc": "Restores vitality and health", "value": 85, "rarity": "rare", "spawn_chance": 0.08},
    "island_chart": {"name": "Island Chart", "icon": "🗺️", "desc": "Detailed maps of nearby islands", "value": 120, "rarity": "rare", "spawn_chance": 0.06},
}

SUNSTONE_ITEM_DATABASE = {
    # Tropical themed, Level 5-10 gear
    "coconut_water": {"name": "Coconut Water", "icon": "🥥", "desc": "Refreshing drink that restores energy", "value": 12, "rarity": "common", "spawn_chance": 0.35},
    "palm_fiber_rope": {"name": "Palm Fiber Rope", "icon": "🪢", "desc": "Light but strong tropical rope", "value": 22, "rarity": "common", "spawn_chance": 0.30},
    "coral_dagger": {"name": "Coral Dagger", "icon": "🗡️", "desc": "Sharp blade carved from hardened coral", "value": 45, "rarity": "common", "spawn_chance": 0.25},
    "sun_salve": {"name": "Sun Salve", "icon": "☀️", "desc": "Healing balm infused with sunlight", "value": 50, "rarity": "common", "spawn_chance": 0.28},
    "shell_shield": {"name": "Shell Shield", "icon": "🛡️", "desc": "Shield crafted from giant turtle shell", "value": 65, "rarity": "uncommon", "spawn_chance": 0.18},
    "pearl_necklace": {"name": "Pearl Necklace", "icon": "📿", "desc": "Gleaming pearls with minor enchantment", "value": 80, "rarity": "uncommon", "spawn_chance": 0.14},
    "trident": {"name": "Trident", "icon": "🔱", "desc": "Three-pronged spear of the sea", "value": 90, "rarity": "uncommon", "spawn_chance": 0.12},
    "sunstone_charm": {"name": "Sunstone Charm", "icon": "✨", "desc": "Warm gem that glows in darkness", "value": 110, "rarity": "rare", "spawn_chance": 0.08},
    "solar_potion": {"name": "Solar Potion", "icon": "🧪", "desc": "Potion brewed in direct sunlight", "value": 130, "rarity": "rare", "spawn_chance": 0.06},
    "ancient_sun_medallion": {"name": "Sun Medallion", "icon": "🏅", "desc": "Relic from the Temple of the Sun", "value": 200, "rarity": "rare", "spawn_chance": 0.04},
}

EMERALD_ITEM_DATABASE = {
    # Jungle/druid themed, Level 10-15 gear
    "jungle_antidote": {"name": "Jungle Antidote", "icon": "🧴", "desc": "Cures most natural poisons", "value": 40, "rarity": "common", "spawn_chance": 0.30},
    "vine_whip": {"name": "Vine Whip", "icon": "🌿", "desc": "Living vine that strikes with thorns", "value": 65, "rarity": "common", "spawn_chance": 0.25},
    "hardwood_shield": {"name": "Hardwood Shield", "icon": "🛡️", "desc": "Dense ironwood shield, light but strong", "value": 75, "rarity": "common", "spawn_chance": 0.22},
    "herbal_remedy": {"name": "Herbal Remedy", "icon": "🌱", "desc": "Powerful healing herbs from the deep jungle", "value": 70, "rarity": "common", "spawn_chance": 0.28},
    "emerald_blade": {"name": "Emerald Blade", "icon": "⚔️", "desc": "Sword with an emerald-edged blade", "value": 120, "rarity": "uncommon", "spawn_chance": 0.15},
    "druid_staff": {"name": "Druid Staff", "icon": "🪵", "desc": "Gnarled staff pulsing with nature magic", "value": 140, "rarity": "uncommon", "spawn_chance": 0.12},
    "panther_cloak": {"name": "Panther Cloak", "icon": "🧥", "desc": "Camouflage cloak, improves stealth", "value": 130, "rarity": "uncommon", "spawn_chance": 0.10},
    "greater_healing_potion": {"name": "Greater Healing Potion", "icon": "🧪", "desc": "Restores significant health", "value": 160, "rarity": "rare", "spawn_chance": 0.07},
    "nature_amulet": {"name": "Nature Amulet", "icon": "✨", "desc": "Grants resistance to poison and disease", "value": 220, "rarity": "rare", "spawn_chance": 0.05},
    "living_seed": {"name": "Living Seed", "icon": "🌰", "desc": "Legendary seed that grows into armor", "value": 300, "rarity": "rare", "spawn_chance": 0.03},
}

STORMBREAK_ITEM_DATABASE = {
    # Storm/lightning themed, Level 15-20 gear
    "storm_ration": {"name": "Storm Ration", "icon": "🥫", "desc": "Preserved food that won't spoil in wet conditions", "value": 35, "rarity": "common", "spawn_chance": 0.30},
    "rubber_cloak": {"name": "Rubber Cloak", "icon": "🧥", "desc": "Insulates against lightning strikes", "value": 85, "rarity": "common", "spawn_chance": 0.25},
    "storm_blade": {"name": "Storm Blade", "icon": "⚔️", "desc": "Crackling blade that arcs with electricity", "value": 150, "rarity": "uncommon", "spawn_chance": 0.15},
    "thunder_shield": {"name": "Thunder Shield", "icon": "🛡️", "desc": "Absorbs electrical damage and redirects it", "value": 170, "rarity": "uncommon", "spawn_chance": 0.12},
    "lightning_rod": {"name": "Lightning Rod", "icon": "⚡", "desc": "Channels storm energy into devastating attacks", "value": 200, "rarity": "uncommon", "spawn_chance": 0.10},
    "tempest_potion": {"name": "Tempest Potion", "icon": "🧪", "desc": "Grants temporary lightning speed", "value": 180, "rarity": "uncommon", "spawn_chance": 0.10},
    "stormforged_mail": {"name": "Stormforged Mail", "icon": "🛡️", "desc": "Chainmail forged during a lightning storm", "value": 280, "rarity": "rare", "spawn_chance": 0.06},
    "kraken_ink_vial": {"name": "Kraken Ink", "icon": "🫙", "desc": "Rare ink for enchanting storm magic", "value": 320, "rarity": "rare", "spawn_chance": 0.05},
    "eye_of_the_storm": {"name": "Eye of the Storm", "icon": "✨", "desc": "Amulet of absolute calm amid chaos", "value": 400, "rarity": "rare", "spawn_chance": 0.03},
}

CINDERFORGE_ITEM_DATABASE = {
    # Fire/volcanic themed, Level 20-25 gear
    "fireproof_salve": {"name": "Fireproof Salve", "icon": "🧴", "desc": "Protects skin from extreme heat", "value": 55, "rarity": "common", "spawn_chance": 0.30},
    "obsidian_blade": {"name": "Obsidian Blade", "icon": "🗡️", "desc": "Razor-sharp volcanic glass sword", "value": 180, "rarity": "uncommon", "spawn_chance": 0.15},
    "magma_shield": {"name": "Magma Shield", "icon": "🛡️", "desc": "Shield that radiates searing heat", "value": 220, "rarity": "uncommon", "spawn_chance": 0.12},
    "forge_hammer": {"name": "Forge Hammer", "icon": "🔨", "desc": "Hammer that never cools, perfect for smithing", "value": 250, "rarity": "uncommon", "spawn_chance": 0.10},
    "lava_potion": {"name": "Lava Potion", "icon": "🧪", "desc": "Grants immunity to fire for a short time", "value": 200, "rarity": "uncommon", "spawn_chance": 0.10},
    "fire_opal": {"name": "Fire Opal", "icon": "💎", "desc": "Gem containing trapped volcanic fire", "value": 300, "rarity": "rare", "spawn_chance": 0.06},
    "salamander_scale_armor": {"name": "Salamander Armor", "icon": "🛡️", "desc": "Armor of fire-immune salamander scales", "value": 420, "rarity": "rare", "spawn_chance": 0.05},
    "inferno_blade": {"name": "Inferno Blade", "icon": "⚔️", "desc": "Sword wreathed in eternal flame", "value": 500, "rarity": "rare", "spawn_chance": 0.03},
}

DREADMIST_ITEM_DATABASE = {
    # Undead/shadow themed, Level 25-30 gear
    "holy_water": {"name": "Holy Water", "icon": "💧", "desc": "Burns undead on contact", "value": 60, "rarity": "common", "spawn_chance": 0.28},
    "ghost_lantern": {"name": "Ghost Lantern", "icon": "🏮", "desc": "Reveals hidden undead and spirits", "value": 120, "rarity": "common", "spawn_chance": 0.22},
    "silver_sword": {"name": "Silver Sword", "icon": "⚔️", "desc": "Blessed blade, devastating to undead", "value": 250, "rarity": "uncommon", "spawn_chance": 0.14},
    "death_ward_amulet": {"name": "Death Ward", "icon": "✨", "desc": "Protects against necromantic magic", "value": 280, "rarity": "uncommon", "spawn_chance": 0.12},
    "banshee_silk_cloak": {"name": "Banshee Silk Cloak", "icon": "🧥", "desc": "Phase through attacks like a ghost", "value": 320, "rarity": "uncommon", "spawn_chance": 0.10},
    "resurrection_potion": {"name": "Resurrection Potion", "icon": "🧪", "desc": "Restores from the brink of death", "value": 350, "rarity": "rare", "spawn_chance": 0.06},
    "lich_bane": {"name": "Lich Bane", "icon": "⚔️", "desc": "Enchanted mace that shatters phylacteries", "value": 550, "rarity": "rare", "spawn_chance": 0.04},
    "soul_shield": {"name": "Soul Shield", "icon": "🛡️", "desc": "Shield powered by captured spirits", "value": 600, "rarity": "rare", "spawn_chance": 0.03},
}

WYRMSCALE_ITEM_DATABASE = {
    # Dragon themed, Level 30-35 gear
    "dragonscale_salve": {"name": "Dragonscale Salve", "icon": "🧴", "desc": "Toughens skin to match dragon hide", "value": 100, "rarity": "common", "spawn_chance": 0.25},
    "drake_fang_dagger": {"name": "Drake Fang Dagger", "icon": "🗡️", "desc": "Dagger carved from a drake's fang", "value": 200, "rarity": "uncommon", "spawn_chance": 0.14},
    "wyvern_wing_shield": {"name": "Wyvern Shield", "icon": "🛡️", "desc": "Shield of stretched wyvern membrane", "value": 350, "rarity": "uncommon", "spawn_chance": 0.12},
    "dragon_breath_flask": {"name": "Dragon Breath Flask", "icon": "🧪", "desc": "Breathe fire for 30 seconds", "value": 400, "rarity": "uncommon", "spawn_chance": 0.08},
    "dragonbone_sword": {"name": "Dragonbone Sword", "icon": "⚔️", "desc": "Sword forged from ancient dragonbone", "value": 600, "rarity": "rare", "spawn_chance": 0.05},
    "wyrm_scale_armor": {"name": "Wyrm Armor", "icon": "🛡️", "desc": "Full suit of elder wyrm scales", "value": 750, "rarity": "rare", "spawn_chance": 0.04},
    "dragon_eye_gem": {"name": "Dragon Eye Gem", "icon": "💎", "desc": "See through walls and detect treasure", "value": 800, "rarity": "rare", "spawn_chance": 0.03},
    "wyrm_heart_elixir": {"name": "Wyrm Heart Elixir", "icon": "🧪", "desc": "Gain draconic power temporarily", "value": 900, "rarity": "rare", "spawn_chance": 0.02},
}

ABYSSAL_ITEM_DATABASE = {
    # Eldritch/cosmic themed, Level 35+ gear (endgame)
    "sanity_tonic": {"name": "Sanity Tonic", "icon": "🧴", "desc": "Keeps the madness at bay... temporarily", "value": 120, "rarity": "common", "spawn_chance": 0.22},
    "void_touched_blade": {"name": "Void Blade", "icon": "🗡️", "desc": "Blade that cuts through reality itself", "value": 400, "rarity": "uncommon", "spawn_chance": 0.12},
    "eldritch_ward": {"name": "Eldritch Ward", "icon": "✨", "desc": "Protection against mind-bending attacks", "value": 500, "rarity": "uncommon", "spawn_chance": 0.10},
    "dimension_anchor": {"name": "Dimension Anchor", "icon": "⚓", "desc": "Prevents forced teleportation", "value": 550, "rarity": "uncommon", "spawn_chance": 0.08},
    "reality_potion": {"name": "Reality Potion", "icon": "🧪", "desc": "Anchors you to this plane of existence", "value": 450, "rarity": "uncommon", "spawn_chance": 0.10},
    "void_reaver": {"name": "Void Reaver", "icon": "⚔️", "desc": "Sword that devours what it cuts", "value": 900, "rarity": "rare", "spawn_chance": 0.04},
    "cosmic_plate": {"name": "Cosmic Plate", "icon": "🛡️", "desc": "Armor forged from collapsed stars", "value": 1000, "rarity": "rare", "spawn_chance": 0.03},
    "reality_shard_amulet": {"name": "Reality Shard", "icon": "💎", "desc": "Fragment of a broken universe", "value": 1200, "rarity": "rare", "spawn_chance": 0.02},
    "genesis_spark": {"name": "Genesis Spark", "icon": "✨", "desc": "Spark of creation itself — ultimate power", "value": 1500, "rarity": "rare", "spawn_chance": 0.01},
}

# Map shop room IDs to their item databases
SHOP_DATABASES = {
    "village_shop": ITEM_DATABASE,
    "harbor_shop": HARBOR_ITEM_DATABASE,
    "sunstone_village_east": SUNSTONE_ITEM_DATABASE,
    "emerald_village_market": EMERALD_ITEM_DATABASE,
    "stormbreak_town_market": STORMBREAK_ITEM_DATABASE,
    "cinder_village_market": CINDERFORGE_ITEM_DATABASE,
    "dreadmist_village_market": DREADMIST_ITEM_DATABASE,
    "wyrm_village_market": WYRMSCALE_ITEM_DATABASE,
    "abyssal_outpost_supply_depot": ABYSSAL_ITEM_DATABASE,
}

# Backwards compatibility reference
SHOP_INVENTORY_POOL = {item_id: {"value": data["value"], "rarity": data["rarity"], "spawn_chance": data["spawn_chance"]} 
                       for item_id, data in ITEM_DATABASE.items()}


class Shop:
    """Manages shop inventory rotation and pricing."""
    
    def __init__(self, shop_id="village_shop", item_database=None):
        """Initialize shop with automatic hourly inventory rotation."""
        self.shop_id = shop_id
        self.timezone = self._get_timezone()
        self.inventory = {}
        self.shop_inventory = {}  # Modern interface
        self.last_rotation_hour = self._get_current_hour()
        self.item_database = item_database if item_database else ITEM_DATABASE
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
    
    def refresh_inventory(self):
        """Alias for check_and_rotate for new UI compatibility."""
        return self.check_and_rotate()
    
    def generate_inventory(self):
        """Generate random inventory based on spawn chances."""
        self.inventory = {}
        self.shop_inventory = {}
        for item_id, item_data in self.item_database.items():
            if random.random() < item_data["spawn_chance"]:
                quantity = random.randint(1, 3)
                price = item_data["value"]
                self.inventory[item_id] = {
                    "quantity": quantity,
                    "value": price,
                    "rarity": item_data["rarity"]
                }
                # Modern interface
                self.shop_inventory[item_id] = {
                    "quantity": quantity,
                    "price": price
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
            # Update modern interface
            if item_name in self.shop_inventory:
                self.shop_inventory[item_name]["quantity"] -= 1
                if self.shop_inventory[item_name]["quantity"] <= 0:
                    del self.shop_inventory[item_name]
            if self.inventory[item_name]["quantity"] <= 0:
                del self.inventory[item_name]
            return True
        return False
    
    def format_inventory(self):
        """Return formatted inventory display for UI."""
        return self.get_inventory()

    def to_dict(self):
        """Serialize shop state for saving."""
        return {
            "shop_id": self.shop_id,
            "inventory": self.inventory,
            "last_rotation_hour": self.last_rotation_hour,
        }

    def load_from_dict(self, data):
        """Restore shop state from saved data."""
        if isinstance(data, dict):
            self.shop_id = data.get("shop_id", self.shop_id)
            self.inventory = data.get("inventory", {})
            self.last_rotation_hour = data.get("last_rotation_hour", self._get_current_hour())
            # Rebuild modern interface from inventory
            self.shop_inventory = {}
            for item_id, item_data in self.inventory.items():
                self.shop_inventory[item_id] = {
                    "quantity": item_data["quantity"],
                    "price": item_data["value"]
                }


class ShopUI:
    """Beautiful ASCII art UI for the shop system."""
    
    def __init__(self, shop, shopkeeper=None, engine=None):
        """Initialize shop UI."""
        self.shop = shop
        self.shopkeeper = shopkeeper
        self.engine = engine  # Reference to GameEngine for displaying messages
        self.item_database = shop.item_database
        self.shop_inventory = shop.shop_inventory
        self.refused_items = {}  # Track refused sales: {player_id: [item_ids]}
        self.pending_negotiation = None

    def _remove_one_from_inventory(self, player, item_id):
        """Remove one unit of an item from player inventory.
        Handles both int and legacy dict inventory formats."""
        if item_id in player.inventory:
            if isinstance(player.inventory[item_id], int):
                if player.inventory[item_id] > 1:
                    player.inventory[item_id] -= 1
                else:
                    del player.inventory[item_id]
            elif isinstance(player.inventory[item_id], dict):
                qty = player.inventory[item_id].get('quantity', 1)
                if qty > 1:
                    player.inventory[item_id]['quantity'] -= 1
                else:
                    del player.inventory[item_id]
    
    def _get_charisma_discount(self, player):
        """Get buy price multiplier based on player charisma (lower = cheaper buys)."""
        charisma = 0
        if hasattr(player, 'stats') and isinstance(player.stats, dict):
            charisma = player.stats.get("charisma", 0)
        return max(0.70, 1.0 - charisma * 0.02)  # Up to 30% off at charisma 15

    def _get_charisma_sell_bonus(self, player):
        """Get sell price multiplier based on player charisma (higher = better sell prices)."""
        charisma = 0
        if hasattr(player, 'stats') and isinstance(player.stats, dict):
            charisma = player.stats.get("charisma", 0)
        return min(1.30, 1.0 + charisma * 0.015)  # Up to 30% bonus at charisma 20

    def display(self, message):
        """
        Display a message to the player.
        Routes to game engine's display function if available, otherwise prints.
        """
        if self.engine and hasattr(self.engine, 'display_message'):
            self.engine.display_message(message)
        else:
            # Fallback to print if engine not available
            print(message)
    
    def show_shop_welcome(self):
        """
        Display beautiful shop welcome screen.
        Called when player enters shop or types 'shop' or 'shop help'.
        """
        self.display("""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  ╔═══╗                                            ╔═══╗ ┃
┃  ║ ◈ ║          ⚜ THE WANDERING MERCHANT ⚜      ║ ◈ ║ ┃
┃  ╚═══╝          "Fair Trades & Rare Wares"        ╚═══╝ ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃                                                         ┃
┃  📜 AVAILABLE COMMANDS:                                 ┃
┃  ┌────────────────────────────────────────────────────┐ ┃
┃  │ shop browse      ▸ View wares for sale             │ ┃
┃  │ shop buy <item>  ▸ Purchase an item                │ ┃
┃  │ shop sell <item> <gold> ▸ Sell to shopkeeper       │ ┃
┃  │ shop talk        ▸ Speak with merchant             │ ┃
┃  │ shop info        ▸ Trading tips & shop details     │ ┃
┃  └────────────────────────────────────────────────────┘ ┃
┃                                                         ┃
┃  💡 Quick Tips:                                         ┃
┃     • 'shop view' or 'shop inventory' = 'shop browse'   ┃
┃     • 'talk to shopkeeper' also works                   ┃
┃                                                         ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
""")
    
    def show_shop_inventory(self, player):
        """
        Display shop inventory with beautiful ASCII art.
        Called when player types 'shop browse' or 'shop inventory'.
        """
        # Refresh inventory if needed
        self.shop.refresh_inventory()
        self.shop_inventory = self.shop.shop_inventory
        
        output = """
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃         🏺 GENERAL STORE - CURRENT INVENTORY 🏺                 ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃                                                                  ┃
┃  ╔═════════════════ COMMON WARES ════════════════════════════╗   ┃
┃  ║                                                           ║   ┃"""
        
        # Display each item in inventory
        if not self.shop_inventory:
            output += """
┃  ║     ~ No items currently in stock ~                       ║   ┃
┃  ║     (Inventory refreshes hourly at :00)                   ║   ┃"""
        else:
            for item_id, stock in self.shop_inventory.items():
                item_data = self.item_database.get(item_id, {})
                
                name = item_data.get("name", item_id)
                icon = item_data.get("icon", "📦")
                desc = item_data.get("desc", "A mysterious item")
                price = stock.get("price", 0)
                quantity = stock.get("quantity", 0)
                
                # Format item line with proper spacing
                # Icon + Name (padded to 30 chars) + Quantity + Price
                name_padded = f"{icon} {name}".ljust(30)
                qty_str = f"{quantity}x"
                price_str = f"{price}g"
                
                output += f"\n┃  ║  {name_padded} {qty_str:>3}  •••  {price_str:>4}  [BUY]  ║   ┃"
                output += f"\n┃  ║     └─ \"{desc}\"{'':>{48-len(desc)}}║   ┃"
                output += "\n┃   ║                              ║   ┃"                        
                                                    
        output += """
┃  ╚════════════════════════════════════════════════════════════╝   ┃
┃                                                                   ┃
┃  ⏰ Stock refreshes hourly at XX:00(Germany Time)                         ┃
┃  💬 Type 'shop talk' to negotiate with the merchant               ┃
┃                                                                   ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""
        
        # Show player's gold
        player_gold = getattr(player, 'gold', 0)
        if not hasattr(player, 'gold'):
            # Try stats dict
            player_gold = player.stats.get("gold", 0) if hasattr(player, 'stats') else 0
        output += f"\n💰 Your gold: {player_gold}g"
        
        self.display(output)
    
    def show_shop_info(self):
        """
        Display merchant's guide to negotiation.
        Called when player types 'shop info'.
        """
        self.display("""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃      📖 MERCHANT'S GUIDE TO FAIR NEGOTIATION 📖        ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃                                                         ┃
┃  The shopkeeper is shrewd but honest. Master the art    ┃
┃  of negotiation to maximize your profits!               ┃
┃                                                         ┃
┃  ╔═══════════════ PRICING STRATEGIES ═══════════════╗   ┃
┃  ║                                                  ║   ┃
┃  ║  ⛔ TOO LOW (≤30% of value)                      ║   ┃
┃  ║     → Permanently REFUSED! Merchant won't budge  ║   ┃
┃  ║                                                  ║   ┃
┃  ║  🤝 LOWBALL (30-50% of value)                    ║   ┃
┃  ║     → Counter-offer at ~75% of your asking price ║   ┃
┃  ║                                                  ║   ┃
┃  ║  ✨ FAIR DEAL (50-85% of value)                  ║   ┃
┃  ║     → ACCEPTED at ~80% of your offer             ║   ┃
┃  ║                                                  ║   ┃
┃  ║  💎 PREMIUM (85-100% of value)                   ║   ┃
┃  ║     → ACCEPTED at ~95% of your offer             ║   ┃
┃  ║                                                  ║   ┃
┃  ║  😂 OUTRAGEOUS (>100% of value)                  ║   ┃
┃  ║     → Merchant laughs, counters at 60-70%        ║   ┃
┃  ║                                                  ║   ┃
┃  ╚══════════════════════════════════════════════════╝   ┃
┃                                                         ┃
┃  ⚠️  IMPORTANT NOTES:                                   ┃
┃  • Once refused on an item, you cannot sell it again    ┃
┃  • Different items have different base values           ┃
┃  • Better negotiation = more gold in your pocket        ┃
┃  • Shop inventory rotates every hour at :00 (Germany)   ┃
┃                                                         ┃
┃  💡 Pro Tip: Start high but reasonable - aim for the    ┃
┃     85-100% sweet spot for maximum profit!              ┃
┃                                                         ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
""")
    
    def buy_item(self, player, item_id):
        """
        Handle buying an item with beautiful confirmation.
        """
        # Check if item exists in shop
        if item_id not in self.shop_inventory:
            self.display("⚠️  That item is not available in the shop.")
            return False
        
        item_data = self.item_database.get(item_id, {})
        stock = self.shop_inventory[item_id]
        
        name = item_data.get("name", item_id)
        icon = item_data.get("icon", "📦")
        base_price = stock.get("price", 0)
        # Apply charisma discount
        price = max(1, int(base_price * self._get_charisma_discount(player)))
        quantity = stock.get("quantity", 0)
        
        # Check if in stock
        if quantity <= 0:
            self.display(f"⚠️  Sorry, {name} is out of stock!")
            return False
        
        # Check if player has enough gold
        player_gold = getattr(player, 'gold', 0)
        if not hasattr(player, 'gold'):
            # Try stats dict
            player_gold = player.stats.get("gold", 0) if hasattr(player, 'stats') else 0
        
        if player_gold < price:
            self.display(f"""
┌─────────────────────────────────────────────┐
│  ⚠️  INSUFFICIENT FUNDS                     │
├─────────────────────────────────────────────┤
│  {icon} {name}
│  Price: {price}g
│  Your gold: {player_gold}g
│  Need: {price - player_gold}g more
└─────────────────────────────────────────────┘
""")
            return False
        
        # Purchase successful
        self.display(f"""
┌─────────────────────────────────────────────┐
│  ✅ PURCHASE SUCCESSFUL!                    │
├─────────────────────────────────────────────┤
│  {icon} {name}
│  Paid: {price}g
│  Remaining gold: {player_gold - price}g
└─────────────────────────────────────────────┘
""")
        
        # Update player inventory and gold
        if hasattr(player, 'gold'):
            player.gold -= price
        else:
            player.stats["gold"] = player.stats.get("gold", 0) - price
        
        # Add item to player inventory (always use int count format for consistency)
        if hasattr(player, 'inventory'):
            if item_id in player.inventory:
                if isinstance(player.inventory[item_id], dict):
                    # Convert legacy dict format to int
                    player.inventory[item_id] = player.inventory[item_id].get('quantity', 1) + 1
                else:
                    player.inventory[item_id] += 1
            else:
                player.inventory[item_id] = 1
        
        # Reduce shop stock
        self.shop_inventory[item_id]['quantity'] -= 1
        self.shop.shop_inventory[item_id]['quantity'] -= 1
        
        # Remove from shop if out of stock
        if self.shop_inventory[item_id]['quantity'] <= 0:
            del self.shop_inventory[item_id]
            if item_id in self.shop.shop_inventory:
                del self.shop.shop_inventory[item_id]
        
        return True
    
    def sell_item(self, player, item_id, asking_price):
        """
        Handle selling with negotiation mechanics and beautiful UI.
        """
        # Check if player has the item
        if not hasattr(player, 'inventory') or item_id not in player.inventory:
            print("\n⚠️  You don't have that item to sell.\n")
            return False
        
        # Check if already refused
        player_id = getattr(player, 'id', 'default_player')
        if player_id in self.refused_items and item_id in self.refused_items[player_id]:
            self.display(f"""
┌─────────────────────────────────────────────┐
│  ⛔ PERMANENTLY REFUSED                     │
├─────────────────────────────────────────────┤
│  The merchant shakes his head firmly.       │
│  "I told you before - I won't buy that      │
│  item from you. My decision is final!"      │
└─────────────────────────────────────────────┘
""")
            return False
        
        # Get item true value
        item_data = player.inventory[item_id]
        if isinstance(item_data, dict):
            true_value = item_data.get('value', 50)
        else:
            # Fallback to item database
            true_value = self.item_database.get(item_id, {}).get('value', 50)
        
        # Calculate percentage of true value
        percentage = (asking_price / true_value) * 100 if true_value > 0 else 0
        
        # TOO LOW - Permanent refusal
        if percentage <= 30:
            self.display(f"""
┌─────────────────────────────────────────────┐
│  ⛔ INSULTING OFFER - PERMANENTLY REFUSED!  │
├─────────────────────────────────────────────┤
│  The merchant's face turns red with anger.  │
│  "How DARE you insult me with such a        │
│  pathetic offer! I will NEVER buy this      │
│  item from you. Get out!"                   │
│                                             │
│  Your offer: {asking_price}g
│  True value: {true_value}g
│  Percentage: {percentage:.1f}%
└─────────────────────────────────────────────┘
""")
            # Mark as permanently refused
            if player_id not in self.refused_items:
                self.refused_items[player_id] = []
            self.refused_items[player_id].append(item_id)
            return False
        
        # LOWBALL - Counter offer
        elif percentage <= 50:
            counter_offer = int(asking_price * 0.75 * self._get_charisma_sell_bonus(player))
            self.display(f"""
┌─────────────────────────────────────────────┐
│  🤝 COUNTER-OFFER                           │
├─────────────────────────────────────────────┤
│  The merchant frowns and strokes his beard. │
│  "That's quite low, friend. I can offer     │
│  you {counter_offer}g - that's my final price."
│                                             │
│  Your offer: {asking_price}g
│  Counter: {counter_offer}g
│  True value: {true_value}g
└─────────────────────────────────────────────┘

Accept counter-offer? (yes/no)
""")
            # Set pending negotiation
            self.pending_negotiation = {
                'item_id': item_id,
                'counter_offer': counter_offer
            }
            return 'pending'
        
        # FAIR DEAL - Accepted with slight reduction
        elif percentage <= 85:
            final_price = int(asking_price * 0.80 * self._get_charisma_sell_bonus(player))
            self.display(f"""
┌─────────────────────────────────────────────┐
│  ✨ FAIR DEAL - ACCEPTED!                   │
├─────────────────────────────────────────────┤
│  The merchant nods approvingly.             │
│  "A reasonable price. I'll take it for      │
│  {final_price}g - fair and square."
│                                             │
│  Your offer: {asking_price}g
│  Final price: {final_price}g
│  You earned: {final_price}g
└─────────────────────────────────────────────┘
""")
            # Complete sale
            if hasattr(player, 'gold'):
                player.gold += final_price
            else:
                player.stats["gold"] = player.stats.get("gold", 0) + final_price
            self._remove_one_from_inventory(player, item_id)
            return True
        
        # PREMIUM - Accepted at high percentage
        elif percentage <= 100:
            final_price = int(asking_price * 0.95 * self._get_charisma_sell_bonus(player))
            self.display(f"""
┌───────────────────────────────────────────────┐
│  💎 PREMIUM DEAL - ACCEPTED!                  │
├───────────────────────────────────────────────┤
│  The merchant's eyes light up.                │
│  "You drive a hard bargain! Very well,        │
│  {final_price}g it is. Excellent merchandise!"
│                                               │
│  Your offer: {asking_price}g
│  Final price: {final_price}g
│  You earned: {final_price}g
└───────────────────────────────────────────────┘
""")
            # Complete sale
            if hasattr(player, 'gold'):
                player.gold += final_price
            else:
                player.stats["gold"] = player.stats.get("gold", 0) + final_price
            self._remove_one_from_inventory(player, item_id)
            return True
        
        # OUTRAGEOUS - Merchant laughs, low counter
        else:
            counter_offer = int(true_value * 0.65 * self._get_charisma_sell_bonus(player))
            self.display(f"""
┌───────────────────────────────────────────────┐
│  😂 OUTRAGEOUS OFFER                          │
├───────────────────────────────────────────────┤
│  The merchant bursts into laughter!           │
│  "You must be joking! That's absurd!          │
│  I'll give you {counter_offer}g and not a coin
│  more. Take it or leave it!"
│                                               │
│  Your offer: {asking_price}g
│  Counter: {counter_offer}g
│  True value: {true_value}g
└───────────────────────────────────────────────┘

Accept counter-offer? (yes/no)
""")
            # Set pending negotiation
            self.pending_negotiation = {
                'item_id': item_id,
                'counter_offer': counter_offer
            }
            return 'pending'

    def respond_to_negotiation(self, player, response):
        """
        Handle user's yes/no response to pending negotiation.
        
        Args:
            player: The player object
            response: User's response string (yes/no)
            
        Returns:
            String message to display to player
        """
        if not self.pending_negotiation:
            return "There's no pending negotiation to respond to."
        
        response = response.lower().strip()
        
        if response in ["yes", "y"]:
            # Accept the counter offer
            item_id = self.pending_negotiation['item_id']
            counter_offer = self.pending_negotiation['counter_offer']
            
            # Complete the sale
            if hasattr(player, 'gold'):
                player.gold += counter_offer
            else:
                player.stats["gold"] = player.stats.get("gold", 0) + counter_offer
            
            # Remove item from inventory
            self._remove_one_from_inventory(player, item_id)
            
            # Clear pending negotiation
            self.pending_negotiation = None
            
            return f"""
┌────────────────────────────────────────────┐
│  ✅ DEAL ACCEPTED!                         │
├────────────────────────────────────────────┤
│  The merchant smiles broadly and hands     │
│  you {counter_offer}g.                          │
│  "A pleasure doing business with you!"     │
└────────────────────────────────────────────┘
"""
        
        elif response in ["no", "n"]:
            # Decline the counter offer
            item_id = self.pending_negotiation['item_id']
            
            # Clear pending negotiation
            self.pending_negotiation = None
            
            return f"""
┌────────────────────────────────────────────┐
│  ❌ DEAL DECLINED                          │
├────────────────────────────────────────────┤
│  The merchant nods understandingly.        │
│  "No? Fair enough. Come back if you        │
│  change your mind."                        │
└────────────────────────────────────────────┘
"""
        
        else:
            # Invalid response - keep pending so they can answer again
            return f"\nInvalid response: '{response}'\nPlease type 'yes' to accept or 'no' to decline the counter-offer.\n"


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
