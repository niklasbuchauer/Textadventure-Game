# 🏪 Village Shop System Guide

## Overview
The Village Shop is a fully implemented trading system with:
- **Dynamic Inventory** that rotates every hour (Germany timezone)
- **NPC Shopkeeper** with personality and dialogue
- **Negotiation System** for selling items with realistic merchant behavior
- **Rich Item Pool** with common tools, quality goods, and rare finds

---

## Shop Inventory

### Inventory Rotation
- Shop inventory **resets every hour** (on the hour, Germany time)
- Each rotation randomly selects from 16 available item types
- Item spawn chances range from 1% to 15% per hour
- Each item available in 1-3 quantities per rotation

### Item Categories

#### Common Wares (Useful crafting items)
- `rope_coil` (20g) - Common merchant item
- `quality_torch` (15g) - Better than standard torches
- `lockpick_set` (50g) - Useful for adventuring
- `coin_pouch` (20g) - Traditional currency item
- `craftsman_hammer` (38g) - Quality tool
- `healing_salve` (35g) - Medicinal item
- `iron_key` (25g) - Universal key item
- `torch` (3g) - Basic light source

#### Quality Goods (Mid-tier equipment)
- `steel_dagger` (35g) - Solid weapon
- `iron_sword` (30g) - Dependable blade
- `leather_armor_piece` (25g) - Light protection
- `silver_ring` (40g) - Accessory
- `worn_map` (45g) - Navigation aid
- `enchanted_candle` (55g) - Magical light

#### Rare Finds (Premium items)
- `healing_potion` (85g) - Rare medicine
- `spell_scroll` (95g) - Magical manuscript
- `ancient_coin` (60g) - Collector's item
- `magic_amulet` (130g) - High-value treasure

---

## Using the Shop

### Basic Commands

```
shop browse          Display all available items
shop buy <item>      Purchase an item
shop sell <item> <gold>  Offer an item for sale
shop talk            Chat with the shopkeeper
shop info            Learn about negotiation
```

### Alternative Commands
- `talk to shopkeeper` - Same as `shop talk`
- `shop view` - Same as `shop browse`
- `shop inventory` - Same as `shop browse`

---

## Buying Items

### How to Buy
```
shop buy silver_ring
```

### Purchase Flow
1. Shopkeeper announces the price
2. Gold is deducted from your account
3. Item is added to your inventory
4. Item is removed from shop stock

### Requirements
- Item must be in stock
- You must have enough gold
- You must be in the village shop

---

## Selling Items (Negotiation)

### The Negotiation System

The shopkeeper is a **skilled negotiator** who uses realistic pricing strategies. Your asking price determines his response:

#### Strategy 1: Ask Too Little (≤30% of value)
**Result:** PERMANENT REFUSAL ❌
- Shopkeeper feels insulted
- Cannot negotiate this item anymore (for rest of session)
- Example: Item worth 100g, you ask 20g

#### Strategy 2: Ask Low (30-50% of value)
**Result:** Counter Offer
- Shopkeeper counters at ~75% of item value
- You can accept or try different price
- Example: Item worth 100g, you ask 40g → he offers ~75g

#### Strategy 3: Fair Offer (50-85% of value)
**Result:** GOOD DEAL ✓
- Shopkeeper accepts at ~80% of your offer
- Best balanced negotiation range
- Example: Item worth 100g, you ask 70g → he accepts ~56g

#### Strategy 4: Generous Offer (85-100% of value)
**Result:** EXCELLENT DEAL ✓✓
- Shopkeeper accepts at ~95% of your offer
- He's very happy with this price
- Example: Item worth 100g, you ask 95g → he accepts ~90g

#### Strategy 5: Asking Full Value (>100%)
**Result:** Insulted Counter
- Shopkeeper laughs and counters at 60-70% of value
- Feels like you're the one being greedy
- Example: Item worth 100g, you ask 120g → he offers ~65g

### How to Negotiate
```
shop sell iron_sword 25
```

Response patterns:
- If accepted: `Deal complete! You received X gold.`
- If counter: `How about Xg instead? Type 'shop sell iron_sword X' to accept`
- If refused: `Refuses to buy - won't buy this item anymore`

### Tips for Best Prices
1. **Research value first** - Check `inventory` to see what you own
2. **Start modest** - Ask for 60-70% of item value
3. **Accept counters quickly** - Don't be greedy
4. **Different items** - Each item has different base value
5. **Don't ask too much** - Permanent refusal is permanent!

---

## NPC Shopkeeper

### Personality
- **Friendly but sharp** - knows a good deal
- **Variable moods** - different greetings each visit
- **Memorable** - remembers refusals
- **Professional** - responds to market conditions

### Dialogue Examples

**Greetings:**
- "Well met, traveler! Looking for something useful?"
- "Welcome to my humble shop. Browse at your leisure."
- "Come in, come in! I've got some fine wares today."

**Selling Responses:**
- (Good price) "Now THAT'S what I'm talking about! [Gold] and it's yours."
- (Fair price) "That's closer. I'll take [Gold]."
- (Too low) "I can get better items for that. No deal."
- (Too high) "You're offering [Gold] for something worth [Value]g? I don't think so."

**Farewells:**
- "Come back anytime! I'll have fresh stock next hour."
- "Safe travels, friend!"
- "Thank you for your business!"

---

## Tips & Strategies

### Making Gold
1. **Hunt valuables** - Collect items from dungeons/world
2. **Negotiate smart** - Offer 60-70% of item value
3. **Accept first counter** - Avoid getting refused
4. **Stock rotation** - Check back each hour for different items

### Spending Gold
1. **Buy useful items** - Healing potions, tools, equipment
2. **Wait for good stock** - Rare items appear unpredictably
3. **Save for emergencies** - Keep gold for healing potions

### Balancing Strategy
- **Buying:** Only buy what you need; rare items appear frequently enough
- **Selling:** Be strategic with high-value items; negotiate fairly
- **Inventory:** Keep diverse items for negotiation leverage

---

## Technical Details

### Inventory Rotation
- Rotation happens at the **top of each hour** (Germany time)
- Rotation is automatic when entering shop
- Uses `Europe/Berlin` timezone
- Independent seed-based random selection

### Item Values
- Each item has a base value (3g to 130g)
- Shopkeeper knows real values
- Negotiation based on item's true worth
- Values fixed in `SHOP_INVENTORY_POOL`

### Negotiation Rules
- Once refused (asked too little), can't sell that item again
- Counter offers are calculated from original value
- Acceptance threshold triggers automatically
- Final prices are always rounded to integers

### Save/Load
- Shop inventory is regenerated on each session
- Negotiation refusals don't persist (reset on load)
- Your inventory and gold are saved normally

---

## Future Enhancements

Possible additions (not currently implemented):
- Multiple NPCs with different personalities
- Special seasonal items
- Player reputation affecting prices
- Trade routes/merchant rotation
- Bulk buying discounts
- Custom item categories

---

## Troubleshooting

### "You need to be in the village shop"
- You're trying shop commands outside the shop
- Use `go outside` then navigate to the shop

### "Item not found"
- Item might not be in stock this hour
- Shop inventory rotates every hour
- Try checking again next hour

### "Shopkeeper refuses to buy"
- You asked too little for an item
- This refusal is permanent for this session
- Try selling a different item

### "Don't have enough gold"
- Item costs more than your gold
- Sell some items first or explore for valuables

---

## Village Shop Location

**Room:** village_shop  
**Description:** Shelves lined with goods of all kinds. The shopkeeper watches carefully from behind the counter.  
**NPCs:** Shopkeeper (friendly merchant)  
**Features:** Hourly inventory rotation, negotiation system, dialogue system

---

**Last Updated:** February 2026  
**Shop System Version:** 1.0  
**Shopkeeper AI:** Negotiation v1.0
