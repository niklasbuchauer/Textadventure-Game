"""
World Generator - Creates a massive 250+ room world.json
Run this script once to generate the new world.
"""

import json
from generate_islands import generate_all_islands

def generate_world():
    """Generate the complete world data structure."""
    
    world = {
        "start_room": "village_square",
        "rooms": {},
        "global_commands": {
            "sit": {
                "text": "You sit down.",
                "effects": {"state": {"sitting": True}}
            },
            "stand up": {
                "text": "You stand back up.",
                "effects": {"state": {"sitting": False}}
            }
        },
        "default_stats": {
            "gold": 0,
            "health": 100,
            "health_max": 100,
            "level": 1,
            "xp": 0,
            "xp_to_next": 100,
            "skill_points": 0,
            "class": "none",
            "strength": 0,
            "defense": 0,
            "dexterity": 0,
            "perception": 0,
            "charisma": 0,
            "constitution": 0
        },
        "item_worth": {
            "gold_coin": 2, "old_coin": 3, "rusty_key": 5, "silver_ring": 10,
            "bronze_coin": 1, "golden_ring": 40, "smooth_stone": 8, "eagle_feather": 35,
            "ancient_acorn": 50, "cave_crystal": 22, "marsh_lily": 12, "intact_tome": 45,
            "dusty_tome": 35, "faded_map": 20, "wolf_pelt": 18, "old_spyglass": 30,
            "old_fishing_rod": 15, "glowing_moss": 8, "strange_herb": 25, "iron_ingot": 20,
            "ancient_brick": 10, "heather_sprig": 3, "wheat_bundle": 3, "prayer_candle": 5,
            "old_bone": 2, "shelf_mushroom": 4, "seaweed": 2, "broken_arrow": 2,
            "torch": 5, "rope_coil": 20, "old_rope": 6, "rusty_sword": 12,
            "broken_shield": 8, "mushroom": 5, "wildflower": 2, "stick": 1,
            "ale_mug": 3, "seashell": 4, "smooth_pebble": 1, "swamp_reed": 3,
            "cactus_fruit": 8, "desert_rose": 15, "scorpion_tail": 12, "sandstone_chunk": 5,
            "ice_crystal": 18, "frost_flower": 20, "polar_moss": 6, "frozen_fish": 10,
            "driftwood": 3, "coral_piece": 12, "pearl": 35, "fishing_net": 15,
            "raw_meat": 8, "leather_scrap": 6, "iron_ore": 15, "copper_ore": 10
        },
        "default_inventory": {},
        "room_templates": {}
    }
    
    rooms = world["rooms"]
    
    # =========================================================================
    # HAVENBROOK VILLAGE (Main Hub) - Center of the world
    # Coordinates around [0, 0]
    # =========================================================================
    
    rooms["village_square"] = {
        "id": "village_square",
        "name": "Havenbrook Village Square",
        "description": "The heart of Havenbrook village. A beautiful stone fountain bubbles in the center of the cobblestone square. Colorful market stalls line the edges, and villagers bustle about their daily business. Roads lead in all directions - north toward the mountains, south to the coast, east to the farmlands, and west into the deep forests.",
        "location_type": "settlement",
        "coordinates": [0, 0],
        "items": {},
        "npcs": ["town_crier", "merchant"],
        "exits": {
            "north": {"target": "village_north_gate", "type": "direction"},
            "south": {"target": "village_south_road", "type": "direction"},
            "east": {"target": "village_east_end", "type": "direction"},
            "west": {"target": "village_west_end", "type": "direction"},
            "tavern": {"target": "village_tavern", "type": "named", "display": "The Golden Tankard Tavern"},
            "shop": {"target": "village_shop", "type": "named", "display": "General Store"},
            "blacksmith": {"target": "village_blacksmith", "type": "named", "display": "Blacksmith's Forge"}
        }
    }
    
    rooms["village_tavern"] = {
        "id": "village_tavern",
        "name": "The Golden Tankard",
        "description": "A warm and inviting tavern filled with the smell of roasted meat and fresh ale. A roaring fireplace crackles in the corner. Wooden tables are scattered about, some occupied by locals sharing stories and drinks.",
        "location_type": "building",
        "coordinates": [0, -1],
        "items": {"ale_mug": {"quantity": 2, "value": 3}},
        "npcs": ["bartender", "patron"],
        "exits": {
            "outside": {"target": "village_square", "type": "direction"}
        }
    }
    
    rooms["village_shop"] = {
        "id": "village_shop",
        "name": "Harwin's General Store",
        "description": "A well-organized shop with shelves stacked with supplies, tools, and adventuring gear. The shopkeeper watches you from behind a worn wooden counter.",
        "location_type": "building",
        "coordinates": [1, 0],
        "items": {},
        "npcs": ["shopkeeper"],
        "shop": True,
        "exits": {
            "outside": {"target": "village_square", "type": "direction"}
        }
    }
    
    rooms["village_blacksmith"] = {
        "id": "village_blacksmith",
        "name": "Tormund's Forge",
        "description": "Heat radiates from the massive forge at the center of the smithy. Weapons and armor line the walls, and the ring of hammer on anvil fills the air. Tormund, a burly man with soot-covered arms, works tirelessly.",
        "location_type": "building",
        "coordinates": [-1, 0],
        "items": {"iron_ingot": {"quantity": 2, "value": 20}},
        "npcs": ["blacksmith"],
        "crafting_station": "forge",
        "exits": {
            "outside": {"target": "village_square", "type": "direction"}
        }
    }
    
    rooms["village_east_end"] = {
        "id": "village_east_end",
        "name": "Village East End",
        "description": "The eastern edge of Havenbrook. Modest wooden houses line the street, with small gardens behind each. The village chapel stands nearby, its bell tower visible above the rooftops.",
        "location_type": "settlement",
        "coordinates": [2, 0],
        "items": {},
        "exits": {
            "west": {"target": "village_square", "type": "direction"},
            "chapel": {"target": "chapel", "type": "named", "display": "Village Chapel"},
            "east": {"target": "farmland_west", "type": "direction"}
        }
    }
    
    rooms["chapel"] = {
        "id": "chapel",
        "name": "Chapel of the Light",
        "description": "A peaceful stone chapel with stained glass windows depicting scenes of hope and salvation. Candles flicker on the altar, and the soft scent of incense fills the air. Father Aldric tends to the faithful here.",
        "location_type": "building",
        "coordinates": [2, -1],
        "items": {"prayer_candle": {"quantity": 3, "value": 5}},
        "npcs": ["priest"],
        "exits": {
            "outside": {"target": "village_east_end", "type": "direction"}
        }
    }
    
    rooms["village_west_end"] = {
        "id": "village_west_end",
        "name": "Village West End",
        "description": "The western part of Havenbrook where the village meets the wilderness. The road here turns to dirt and leads into the shadowy Elderwood Forest. A few hardy souls have built their homes on this frontier edge.",
        "location_type": "settlement",
        "coordinates": [-2, 0],
        "items": {},
        "exits": {
            "east": {"target": "village_square", "type": "direction"},
            "west": {"target": "forest_edge", "type": "direction"},
            "north": {"target": "village_gardens", "type": "direction"}
        }
    }
    
    rooms["village_north_gate"] = {
        "id": "village_north_gate",
        "name": "Havenbrook North Gate",
        "description": "A sturdy wooden gate marks the northern entrance to Havenbrook. Beyond it, a winding road climbs toward the distant Stormspire Mountains. Guards occasionally patrol here, watching for trouble from the highlands.",
        "location_type": "settlement",
        "coordinates": [0, 2],
        "items": {},
        "exits": {
            "south": {"target": "village_square", "type": "direction"},
            "north": {"target": "northern_road", "type": "direction"},
            "east": {"target": "village_training_grounds", "type": "direction"}
        }
    }
    
    rooms["village_south_road"] = {
        "id": "village_south_road",
        "name": "Southern Village Road",
        "description": "The cobblestones give way to packed earth as the road leads south from the village. You can smell salt on the breeze - the Azure Coast lies that way. Merchants often travel this route to Port Haven.",
        "location_type": "settlement",
        "coordinates": [0, -2],
        "items": {},
        "exits": {
            "north": {"target": "village_square", "type": "direction"},
            "south": {"target": "crossroads", "type": "direction"},
            "west": {"target": "village_pond", "type": "direction"}
        }
    }
    
    rooms["village_gardens"] = {
        "id": "village_gardens",
        "name": "Village Gardens",
        "description": "A peaceful garden area where villagers grow herbs and flowers. Bees buzz among the blossoms, and a small bench offers a place to rest and enjoy the scenery.",
        "location_type": "settlement",
        "coordinates": [-2, 1],
        "items": {"wildflower": {"quantity": 4, "value": 2}, "strange_herb": {"quantity": 1, "value": 25}},
        "exits": {
            "south": {"target": "village_west_end", "type": "direction"},
            "west": {"target": "orchard", "type": "direction"}
        }
    }
    
    rooms["village_pond"] = {
        "id": "village_pond",
        "name": "Village Pond",
        "description": "A tranquil pond at the edge of the village where ducks paddle lazily. Children sometimes come here to fish with makeshift poles. Lily pads dot the surface.",
        "location_type": "settlement",
        "coordinates": [-1, -2],
        "items": {"old_fishing_rod": {"quantity": 1, "value": 15}},
        "exits": {
            "east": {"target": "village_south_road", "type": "direction"},
            "south": {"target": "meadow", "type": "direction"}
        }
    }
    
    rooms["village_training_grounds"] = {
        "id": "village_training_grounds",
        "name": "Training Grounds",
        "description": "An open area where the village militia practices combat. Training dummies stand in rows, and weapon racks line the perimeter. The ground is worn from countless drills.",
        "location_type": "settlement",
        "coordinates": [1, 2],
        "items": {"broken_arrow": {"quantity": 3, "value": 2}},
        "exits": {
            "west": {"target": "village_north_gate", "type": "direction"},
            "east": {"target": "stables", "type": "direction"}
        }
    }
    
    rooms["stables"] = {
        "id": "stables",
        "name": "Village Stables",
        "description": "A large wooden stable housing horses and pack animals. The smell of hay and animals is strong. A stable hand tends to the creatures with care.",
        "location_type": "building",
        "coordinates": [2, 2],
        "items": {"rope_coil": {"quantity": 1, "value": 20}},
        "exits": {
            "west": {"target": "village_training_grounds", "type": "direction"},
            "north": {"target": "northern_road", "type": "direction"}
        }
    }
    
    rooms["orchard"] = {
        "id": "orchard",
        "name": "Apple Orchard",
        "description": "Rows of apple trees stretch across this hillside orchard. In season, the branches hang heavy with fruit. A weathered ladder leans against one of the larger trees.",
        "location_type": "wilderness",
        "coordinates": [-3, 1],
        "items": {},
        "exits": {
            "east": {"target": "village_gardens", "type": "direction"},
            "west": {"target": "forest_edge", "type": "direction"},
            "north": {"target": "windmill_hill", "type": "direction"}
        }
    }
    
    # =========================================================================
    # FARMLANDS & PLAINS - East/Southeast of village
    # =========================================================================
    
    rooms["farmland_west"] = {
        "id": "farmland_west",
        "name": "Western Farmlands",
        "description": "Golden fields of wheat sway in the breeze. Farmhouses dot the landscape, and the distant sound of roosters carries on the wind. This is the breadbasket of Havenbrook.",
        "location_type": "wilderness",
        "coordinates": [4, 0],
        "items": {"wheat_bundle": {"quantity": 3, "value": 3}},
        "exits": {
            "west": {"target": "village_east_end", "type": "direction"},
            "east": {"target": "farmland_center", "type": "direction"},
            "south": {"target": "old_battlefield", "type": "direction"}
        }
    }
    
    rooms["farmland_center"] = {
        "id": "farmland_center",
        "name": "Central Farmlands",
        "description": "The heart of the farming district. A large barn stands nearby, and scarecrows guard the fields against crows. Farmers work the land with dedication.",
        "location_type": "wilderness",
        "coordinates": [6, 0],
        "items": {"wheat_bundle": {"quantity": 2, "value": 3}},
        "exits": {
            "west": {"target": "farmland_west", "type": "direction"},
            "east": {"target": "farmland_east", "type": "direction"},
            "north": {"target": "farmland_north", "type": "direction"},
            "south": {"target": "farmland_south", "type": "direction"}
        }
    }
    
    rooms["farmland_east"] = {
        "id": "farmland_east",
        "name": "Eastern Farmlands",
        "description": "The farmland gives way to rolling hills here. You can see the desert wastes shimmering in the distant east. A lonely windmill creaks in the breeze.",
        "location_type": "wilderness",
        "coordinates": [8, 0],
        "items": {},
        "exits": {
            "west": {"target": "farmland_center", "type": "direction"},
            "east": {"target": "desert_border", "type": "direction"},
            "south": {"target": "dusty_crossroads", "type": "direction"}
        }
    }
    
    rooms["farmland_north"] = {
        "id": "farmland_north",
        "name": "Northern Farmlands",
        "description": "Sheep graze on the gentle slopes here. Stone walls divide the pastures. The road north leads toward the mountains.",
        "location_type": "wilderness",
        "coordinates": [6, 2],
        "items": {},
        "exits": {
            "south": {"target": "farmland_center", "type": "direction"},
            "north": {"target": "highland_road", "type": "direction"},
            "west": {"target": "shepherd_cottage", "type": "direction"}
        }
    }
    
    rooms["farmland_south"] = {
        "id": "farmland_south",
        "name": "Southern Farmlands",
        "description": "The fields here grow vegetables and herbs. A small stream provides irrigation. The road continues south toward the coast.",
        "location_type": "wilderness",
        "coordinates": [6, -2],
        "items": {"strange_herb": {"quantity": 1, "value": 25}},
        "exits": {
            "north": {"target": "farmland_center", "type": "direction"},
            "south": {"target": "coastal_road_north", "type": "direction"},
            "west": {"target": "old_battlefield", "type": "direction"}
        }
    }
    
    rooms["shepherd_cottage"] = {
        "id": "shepherd_cottage",
        "name": "Shepherd's Cottage",
        "description": "A humble stone cottage where a shepherd lives with their flock. Wool blankets hang on a line to dry. A friendly dog watches over the sheep.",
        "location_type": "building",
        "coordinates": [5, 2],
        "items": {"wolf_pelt": {"quantity": 1, "value": 18}},
        "exits": {
            "east": {"target": "farmland_north", "type": "direction"}
        }
    }
    
    rooms["old_battlefield"] = {
        "id": "old_battlefield",
        "name": "Old Battlefield",
        "description": "A somber field where an ancient battle was fought. Rusted weapons and scattered bones still emerge from the earth after heavy rains. A weathered monument honors the fallen.",
        "location_type": "wilderness",
        "coordinates": [4, -2],
        "items": {"rusty_sword": {"quantity": 1, "value": 12}, "broken_shield": {"quantity": 1, "value": 8}},
        "exits": {
            "north": {"target": "farmland_west", "type": "direction"},
            "east": {"target": "farmland_south", "type": "direction"},
            "south": {"target": "graveyard_road", "type": "direction"},
            "west": {"target": "crossroads", "type": "direction"}
        }
    }
    
    rooms["windmill_hill"] = {
        "id": "windmill_hill",
        "name": "Windmill Hill",
        "description": "A tall stone windmill stands atop this hill, its great sails turning slowly in the wind. The miller grinds grain here for the whole region. You can see for miles in every direction.",
        "location_type": "wilderness",
        "coordinates": [-3, 3],
        "items": {},
        "exits": {
            "south": {"target": "orchard", "type": "direction"},
            "east": {"target": "northern_road", "type": "direction"},
            "north": {"target": "forest_clearing", "type": "direction"}
        }
    }
    
    # =========================================================================
    # ELDERWOOD FOREST - West/Northwest of village
    # Contains: Crystal Caverns entrance, Verdant Labyrinth entrance, Hermit
    # =========================================================================
    
    rooms["forest_edge"] = {
        "id": "forest_edge",
        "name": "Edge of Elderwood",
        "description": "The trees of Elderwood Forest rise before you like a green wall. Sunlight barely penetrates the canopy ahead. This ancient forest is said to hide many secrets... and dangers.",
        "location_type": "wilderness",
        "coordinates": [-4, 0],
        "items": {"stick": {"quantity": 2, "value": 1}},
        "exits": {
            "east": {"target": "village_west_end", "type": "direction"},
            "west": {"target": "forest_path", "type": "direction"},
            "north": {"target": "orchard", "type": "direction"},
            "south": {"target": "forest_south_edge", "type": "direction"}
        }
    }
    
    rooms["forest_path"] = {
        "id": "forest_path",
        "name": "Forest Path",
        "description": "A winding path through the dense forest. Birds chirp overhead and small animals rustle in the undergrowth. The trees seem to press in from all sides.",
        "location_type": "wilderness",
        "coordinates": [-6, 0],
        "items": {"mushroom": {"quantity": 3, "value": 5}},
        "exits": {
            "east": {"target": "forest_edge", "type": "direction"},
            "west": {"target": "deep_forest", "type": "direction"},
            "north": {"target": "forest_clearing", "type": "direction"},
            "south": {"target": "mossy_hollow", "type": "direction"}
        }
    }
    
    rooms["forest_clearing"] = {
        "id": "forest_clearing",
        "name": "Sunny Clearing",
        "description": "A beautiful clearing where sunlight streams through a gap in the canopy. Wildflowers carpet the ground, and butterflies dance on the breeze. A moment of peace in the wild forest.",
        "location_type": "wilderness",
        "coordinates": [-5, 2],
        "items": {"wildflower": {"quantity": 5, "value": 2}},
        "exits": {
            "south": {"target": "forest_path", "type": "direction"},
            "west": {"target": "forest_grove", "type": "direction"},
            "east": {"target": "windmill_hill", "type": "direction"},
            "north": {"target": "woodland_shrine", "type": "direction"}
        }
    }
    
    rooms["deep_forest"] = {
        "id": "deep_forest",
        "name": "Deep Forest",
        "description": "The forest grows darker here. Ancient trees tower above, their branches blocking most of the sunlight. The air is cool and damp. Strange sounds echo from deeper within.",
        "location_type": "wilderness",
        "coordinates": [-8, 0],
        "items": {"glowing_moss": {"quantity": 2, "value": 8}},
        "exits": {
            "east": {"target": "forest_path", "type": "direction"},
            "west": {"target": "ancient_grove", "type": "direction"},
            "north": {"target": "dungeon_forest_entrance", "type": "direction"},
            "south": {"target": "forest_pool", "type": "direction"}
        }
    }
    
    rooms["mossy_hollow"] = {
        "id": "mossy_hollow",
        "name": "Mossy Hollow",
        "description": "A damp depression where soft emerald moss covers everything. Fallen logs create natural seats. Fireflies drift lazily between ferns even during the day.",
        "location_type": "wilderness",
        "coordinates": [-6, -2],
        "items": {"glowing_moss": {"quantity": 3, "value": 8}, "shelf_mushroom": {"quantity": 2, "value": 4}},
        "exits": {
            "north": {"target": "forest_path", "type": "direction"},
            "west": {"target": "forest_pool", "type": "direction"},
            "south": {"target": "forest_south_edge", "type": "direction"}
        }
    }
    
    rooms["forest_grove"] = {
        "id": "forest_grove",
        "name": "Tranquil Grove",
        "description": "A peaceful grove where birds sing sweetly. Ancient oaks form a natural cathedral. This place feels sacred, untouched by the troubles of the outside world.",
        "location_type": "wilderness",
        "coordinates": [-7, 2],
        "items": {},
        "exits": {
            "east": {"target": "forest_clearing", "type": "direction"},
            "west": {"target": "hermit_cabin", "type": "direction"},
            "north": {"target": "woodland_shrine", "type": "direction"}
        }
    }
    
    rooms["woodland_shrine"] = {
        "id": "woodland_shrine",
        "name": "Woodland Shrine",
        "description": "Stone monoliths draped in ivy mark an ancient place of worship. Offerings of wilted flowers and small coins are scattered at the base of a moss-covered altar. The air hums with faint energy.",
        "location_type": "wilderness",
        "coordinates": [-6, 4],
        "items": {"old_coin": {"quantity": 3, "value": 3}},
        "exits": {
            "south": {"target": "forest_clearing", "type": "direction"},
            "west": {"target": "ancient_grove", "type": "direction"},
            "east": {"target": "northern_road", "type": "direction"}
        }
    }
    
    rooms["hermit_cabin"] = {
        "id": "hermit_cabin",
        "name": "Hermit's Cabin",
        "description": "A rough-hewn log cabin in a small clearing. Smoke curls from a stone chimney. Herbs and animal pelts dry on a line. Old Finn, the forest hermit, watches you from the doorway with knowing eyes.",
        "location_type": "building",
        "coordinates": [-9, 2],
        "items": {"strange_herb": {"quantity": 2, "value": 25}},
        "npcs": ["hermit"],
        "exits": {
            "east": {"target": "forest_grove", "type": "direction"},
            "south": {"target": "ancient_grove", "type": "direction"}
        }
    }
    
    rooms["ancient_grove"] = {
        "id": "ancient_grove",
        "name": "Ancient Grove",
        "description": "Massive, impossibly old trees form a living cathedral. Shafts of golden light pierce the canopy. This place feels sacred and timeless. A strange energy pulses from between the roots of the largest tree.",
        "location_type": "wilderness",
        "coordinates": [-10, 0],
        "items": {"ancient_acorn": {"quantity": 1, "value": 50}},
        "exits": {
            "east": {"target": "deep_forest", "type": "direction"},
            "north": {"target": "hermit_cabin", "type": "direction"},
            "enter": {
                "target": "FIXED",
                "type": "fixed_dungeon",
                "dungeon_id": "verdant_labyrinth",
                "transition_text": "The ancient roots part before you, revealing a passage into the living depths beneath the World Tree..."
            }
        }
    }
    
    rooms["dungeon_forest_entrance"] = {
        "id": "dungeon_forest_entrance",
        "name": "Crystal Cave Entrance",
        "description": "A foreboding cave mouth opens in a moss-covered hillside. Strange energy pulses from within, and faint crystalline lights glimmer in the darkness. Ancient runes are carved into the stone archway.",
        "location_type": "wilderness",
        "coordinates": [-8, 2],
        "items": {},
        "exits": {
            "south": {"target": "deep_forest", "type": "direction"},
            "east": {"target": "woodland_shrine", "type": "direction"},
            "enter": {
                "target": "DUNGEON",
                "type": "time_gated_dungeon",
                "dungeon_id": "crystal_caverns",
                "transition_text": "You step into the shimmering cave mouth. Crystal formations catch and scatter the light as you descend into the depths..."
            }
        }
    }
    
    rooms["forest_pool"] = {
        "id": "forest_pool",
        "name": "Forest Pool",
        "description": "A clear pool fed by a small waterfall. The water is cold and refreshing. Fish dart beneath the surface, and ferns grow thick around the edges.",
        "location_type": "wilderness",
        "coordinates": [-8, -2],
        "items": {},
        "exits": {
            "east": {"target": "mossy_hollow", "type": "direction"},
            "north": {"target": "deep_forest", "type": "direction"},
            "south": {"target": "forest_swamp_border", "type": "direction"}
        }
    }
    
    rooms["forest_south_edge"] = {
        "id": "forest_south_edge",
        "name": "Southern Forest Edge",
        "description": "The forest thins here, transitioning to wetlands to the south. The ground becomes softer and wetter. Mist curls between the trees.",
        "location_type": "wilderness",
        "coordinates": [-5, -2],
        "items": {"stick": {"quantity": 1, "value": 1}},
        "exits": {
            "north": {"target": "mossy_hollow", "type": "direction"},
            "east": {"target": "forest_edge", "type": "direction"},
            "south": {"target": "swamp_trail", "type": "direction"}
        }
    }
    
    # =========================================================================
    # SHADOWMIRE SWAMP - Southwest
    # Contains: Shadow Depths entrance (via graveyard/crypt)
    # =========================================================================
    
    rooms["swamp_trail"] = {
        "id": "swamp_trail",
        "name": "Swamp Trail",
        "description": "A treacherous trail winds through the misty Shadowmire Swamp. The ground squelches underfoot, and the air reeks of decay. Gnarled trees draped in moss loom overhead.",
        "location_type": "wilderness",
        "coordinates": [-5, -4],
        "items": {"swamp_reed": {"quantity": 2, "value": 3}},
        "exits": {
            "north": {"target": "forest_south_edge", "type": "direction"},
            "south": {"target": "foggy_marsh", "type": "direction"},
            "west": {"target": "swamp_edge", "type": "direction"},
            "east": {"target": "meadow", "type": "direction"}
        }
    }
    
    rooms["meadow"] = {
        "id": "meadow",
        "name": "Misty Meadow",
        "description": "A low-lying meadow where mist clings to the ground. The grass is damp and thick. This area marks the boundary between the swamp and more hospitable lands.",
        "location_type": "wilderness",
        "coordinates": [-3, -4],
        "items": {"wildflower": {"quantity": 2, "value": 2}},
        "exits": {
            "west": {"target": "swamp_trail", "type": "direction"},
            "north": {"target": "village_pond", "type": "direction"},
            "east": {"target": "crossroads", "type": "direction"}
        }
    }
    
    rooms["foggy_marsh"] = {
        "id": "foggy_marsh",
        "name": "Foggy Marsh",
        "description": "Thick fog obscures your vision. You can barely see a few feet ahead. The ground is waterlogged, and strange sounds echo through the mist. Something moves in the murky water.",
        "location_type": "wilderness",
        "coordinates": [-5, -6],
        "items": {"marsh_lily": {"quantity": 2, "value": 12}},
        "exits": {
            "north": {"target": "swamp_trail", "type": "direction"},
            "south": {"target": "deep_swamp", "type": "direction"},
            "west": {"target": "witch_hut", "type": "direction"}
        }
    }
    
    rooms["swamp_edge"] = {
        "id": "swamp_edge",
        "name": "Swamp Edge",
        "description": "The western edge of the swamp. The ground rises slightly here, becoming more solid. Dead trees stand like skeletal sentinels. A foul smell drifts from the east.",
        "location_type": "wilderness",
        "coordinates": [-7, -4],
        "items": {},
        "exits": {
            "east": {"target": "swamp_trail", "type": "direction"},
            "south": {"target": "witch_hut", "type": "direction"},
            "west": {"target": "forest_swamp_border", "type": "direction"}
        }
    }
    
    rooms["forest_swamp_border"] = {
        "id": "forest_swamp_border",
        "name": "Forest-Swamp Border",
        "description": "Where the forest meets the swamp. Trees thin out and become twisted. The ground transitions from firm soil to soggy muck. An uneasy feeling pervades this place.",
        "location_type": "wilderness",
        "coordinates": [-9, -4],
        "items": {},
        "exits": {
            "north": {"target": "forest_pool", "type": "direction"},
            "east": {"target": "swamp_edge", "type": "direction"},
            "south": {"target": "sunken_ruins", "type": "direction"}
        }
    }
    
    rooms["witch_hut"] = {
        "id": "witch_hut",
        "name": "Witch's Hut",
        "description": "A decrepit hut on stilts rises from the murk. Skulls and strange charms hang from the eaves. Smoke rises from a crooked chimney. Old Martha, the swamp witch, watches you with rheumy eyes.",
        "location_type": "building",
        "coordinates": [-7, -6],
        "items": {"strange_herb": {"quantity": 3, "value": 25}},
        "npcs": ["swamp_witch"],
        "exits": {
            "east": {"target": "foggy_marsh", "type": "direction"},
            "north": {"target": "swamp_edge", "type": "direction"}
        }
    }
    
    rooms["deep_swamp"] = {
        "id": "deep_swamp",
        "name": "Deep Swamp",
        "description": "The heart of Shadowmire, where few dare to tread. The water is waist-deep in places, murky and foul. Strange lights flicker in the distance - will-o'-wisps leading the unwary to their doom.",
        "location_type": "wilderness",
        "coordinates": [-5, -8],
        "items": {"glowing_moss": {"quantity": 1, "value": 8}},
        "exits": {
            "north": {"target": "foggy_marsh", "type": "direction"},
            "west": {"target": "sunken_ruins", "type": "direction"},
            "east": {"target": "graveyard_gates", "type": "direction"}
        }
    }
    
    rooms["sunken_ruins"] = {
        "id": "sunken_ruins",
        "name": "Sunken Ruins",
        "description": "The remains of an ancient civilization, half-submerged in the swamp. Crumbling stone walls and collapsed archways hint at former grandeur. What secrets lie beneath the murky water?",
        "location_type": "wilderness",
        "coordinates": [-8, -6],
        "items": {"ancient_brick": {"quantity": 2, "value": 10}, "old_coin": {"quantity": 1, "value": 3}},
        "exits": {
            "north": {"target": "forest_swamp_border", "type": "direction"},
            "east": {"target": "deep_swamp", "type": "direction"}
        }
    }
    
    rooms["graveyard_gates"] = {
        "id": "graveyard_gates",
        "name": "Graveyard Gates",
        "description": "Rusted iron gates mark the entrance to an ancient, overgrown graveyard. The fog is especially thick here, and the silence is oppressive. Tombstones lean at odd angles beyond the gate.",
        "location_type": "wilderness",
        "coordinates": [-3, -8],
        "items": {},
        "exits": {
            "west": {"target": "deep_swamp", "type": "direction"},
            "south": {"target": "graveyard", "type": "direction"},
            "north": {"target": "graveyard_road", "type": "direction"}
        }
    }
    
    rooms["graveyard_road"] = {
        "id": "graveyard_road",
        "name": "Graveyard Road",
        "description": "A gloomy road leading to the old graveyard. Dead trees line the path, their branches reaching like skeletal fingers. Few travel this way willingly.",
        "location_type": "wilderness",
        "coordinates": [-3, -6],
        "items": {},
        "exits": {
            "south": {"target": "graveyard_gates", "type": "direction"},
            "north": {"target": "crossroads", "type": "direction"},
            "east": {"target": "old_battlefield", "type": "direction"}
        }
    }
    
    rooms["graveyard"] = {
        "id": "graveyard",
        "name": "Overgrown Graveyard",
        "description": "Row upon row of ancient tombstones, many cracked or toppled. Weeds and thorns have overrun the graves. The mausoleums at the far end look particularly foreboding. The dead do not rest easy here.",
        "location_type": "wilderness",
        "coordinates": [-3, -10],
        "items": {"old_bone": {"quantity": 3, "value": 2}},
        "exits": {
            "north": {"target": "graveyard_gates", "type": "direction"},
            "crypt": {"target": "open_crypt", "type": "named", "display": "An open crypt"}
        }
    }
    
    rooms["open_crypt"] = {
        "id": "open_crypt",
        "name": "Open Crypt",
        "description": "The door to this ancient crypt hangs open. Stone steps descend into darkness. A cold wind blows up from below, carrying whispers of the dead. Something powerful lurks in the depths.",
        "location_type": "building",
        "coordinates": [-4, -10],
        "items": {},
        "exits": {
            "outside": {"target": "graveyard", "type": "direction"},
            "enter": {
                "target": "FIXED",
                "type": "fixed_dungeon",
                "dungeon_id": "shadow_depths",
                "transition_text": "You descend the cold stone steps. The whispers grow louder, and shadows seem to move with malevolent purpose..."
            }
        }
    }
    
    # =========================================================================
    # CROSSROADS & CENTRAL CONNECTIONS
    # =========================================================================
    
    rooms["crossroads"] = {
        "id": "crossroads",
        "name": "Lonely Crossroads",
        "description": "Four roads meet at this windswept crossroads. A weathered signpost points in each direction: North to the Mountains, South to the Coast, East to the Desert, West to the Swamp. Travelers sometimes camp here.",
        "location_type": "wilderness",
        "coordinates": [0, -4],
        "items": {},
        "exits": {
            "north": {"target": "village_south_road", "type": "direction"},
            "south": {"target": "coastal_road_north", "type": "direction"},
            "east": {"target": "eastern_road", "type": "direction"},
            "west": {"target": "meadow", "type": "direction"}
        }
    }
    
    rooms["northern_road"] = {
        "id": "northern_road",
        "name": "Northern Road",
        "description": "A well-traveled road leading north from Havenbrook toward the Stormspire Mountains. The ground begins to rise, and the air grows cooler. Snow-capped peaks are visible in the distance.",
        "location_type": "wilderness",
        "coordinates": [0, 4],
        "items": {},
        "exits": {
            "south": {"target": "village_north_gate", "type": "direction"},
            "north": {"target": "mountain_foothills", "type": "direction"},
            "west": {"target": "woodland_shrine", "type": "direction"},
            "east": {"target": "highland_road", "type": "direction"}
        }
    }
    
    rooms["eastern_road"] = {
        "id": "eastern_road",
        "name": "Eastern Road",
        "description": "A dusty road leading east toward the Sunscorch Desert. The vegetation grows sparse, and the air dry. Heat shimmers on the horizon.",
        "location_type": "wilderness",
        "coordinates": [4, -4],
        "items": {},
        "exits": {
            "west": {"target": "crossroads", "type": "direction"},
            "east": {"target": "dusty_crossroads", "type": "direction"},
            "north": {"target": "old_battlefield", "type": "direction"}
        }
    }
    
    rooms["dusty_crossroads"] = {
        "id": "dusty_crossroads",
        "name": "Dusty Crossroads",
        "description": "Where the eastern road meets paths from the coast and desert. The ground is parched and cracked. A lonely water well offers respite to travelers.",
        "location_type": "wilderness",
        "coordinates": [8, -4],
        "items": {},
        "exits": {
            "west": {"target": "eastern_road", "type": "direction"},
            "north": {"target": "farmland_east", "type": "direction"},
            "east": {"target": "desert_border", "type": "direction"},
            "south": {"target": "coastal_road_east", "type": "direction"}
        }
    }
    
    # =========================================================================
    # STORMSPIRE MOUNTAINS - North
    # Contains: Iron Halls entrance, Mountain Peak (Frozen Spire entrance)
    # =========================================================================
    
    rooms["highland_road"] = {
        "id": "highland_road",
        "name": "Highland Road",
        "description": "The road climbs through rocky highlands. Hardy shrubs and heather dot the landscape. The wind is stronger here, carrying the scent of snow from the peaks above.",
        "location_type": "wilderness",
        "coordinates": [4, 4],
        "items": {"heather_sprig": {"quantity": 2, "value": 3}},
        "exits": {
            "west": {"target": "northern_road", "type": "direction"},
            "south": {"target": "farmland_north", "type": "direction"},
            "north": {"target": "highland_pass", "type": "direction"},
            "east": {"target": "eastern_highlands", "type": "direction"}
        }
    }
    
    rooms["mountain_foothills"] = {
        "id": "mountain_foothills",
        "name": "Mountain Foothills",
        "description": "The terrain rises sharply here at the base of the Stormspire Mountains. Rocky outcroppings jut from the hillside, and mountain goats graze on the slopes. The main peak towers above.",
        "location_type": "wilderness",
        "coordinates": [0, 6],
        "items": {"smooth_stone": {"quantity": 2, "value": 8}},
        "exits": {
            "south": {"target": "northern_road", "type": "direction"},
            "north": {"target": "mountain_path", "type": "direction"},
            "east": {"target": "rocky_valley", "type": "direction"},
            "west": {"target": "mountain_stream", "type": "direction"}
        }
    }
    
    rooms["mountain_stream"] = {
        "id": "mountain_stream",
        "name": "Mountain Stream",
        "description": "A crystal-clear stream rushes down from the mountains. The water is ice-cold and pure. Fish dart through the shallows, and the sound of the water is soothing.",
        "location_type": "wilderness",
        "coordinates": [-2, 6],
        "items": {},
        "exits": {
            "east": {"target": "mountain_foothills", "type": "direction"},
            "north": {"target": "waterfall_base", "type": "direction"}
        }
    }
    
    rooms["waterfall_base"] = {
        "id": "waterfall_base",
        "name": "Waterfall Basin",
        "description": "A magnificent waterfall cascades down the cliff face into a deep pool. Mist fills the air, creating rainbows in the sunlight. The roar of the water is deafening.",
        "location_type": "wilderness",
        "coordinates": [-2, 8],
        "items": {"smooth_pebble": {"quantity": 3, "value": 1}},
        "exits": {
            "south": {"target": "mountain_stream", "type": "direction"},
            "east": {"target": "mountain_path", "type": "direction"}
        }
    }
    
    rooms["mountain_path"] = {
        "id": "mountain_path",
        "name": "Mountain Path",
        "description": "A treacherous path winds up the mountainside. Loose rocks make footing dangerous. The higher you go, the colder it gets. Snow begins to appear on the ground.",
        "location_type": "wilderness",
        "coordinates": [0, 8],
        "items": {},
        "exits": {
            "south": {"target": "mountain_foothills", "type": "direction"},
            "north": {"target": "high_pass", "type": "direction"},
            "west": {"target": "waterfall_base", "type": "direction"},
            "east": {"target": "dungeon_mountain_entrance", "type": "direction"}
        }
    }
    
    rooms["rocky_valley"] = {
        "id": "rocky_valley",
        "name": "Rocky Valley",
        "description": "A valley strewn with boulders and rocky debris. Old mining equipment lies abandoned - perhaps from failed prospecting attempts. A cave opening is visible in the cliff face.",
        "location_type": "wilderness",
        "coordinates": [2, 6],
        "items": {"iron_ore": {"quantity": 2, "value": 15}},
        "exits": {
            "west": {"target": "mountain_foothills", "type": "direction"},
            "north": {"target": "dungeon_mountain_entrance", "type": "direction"},
            "east": {"target": "highland_pass", "type": "direction"}
        }
    }
    
    rooms["dungeon_mountain_entrance"] = {
        "id": "dungeon_mountain_entrance",
        "name": "Ancient Mountain Gate",
        "description": "Massive stone doors carved with dwarven runes mark the entrance to the legendary Iron Halls. The craftsmanship is ancient but still magnificent. Strange sounds echo from within.",
        "location_type": "wilderness",
        "coordinates": [2, 8],
        "items": {},
        "exits": {
            "south": {"target": "rocky_valley", "type": "direction"},
            "west": {"target": "mountain_path", "type": "direction"},
            "enter": {
                "target": "DUNGEON",
                "type": "time_gated_dungeon",
                "dungeon_id": "iron_halls",
                "transition_text": "The great stone doors grind open. You step into halls that have stood for millennia, lit by an eternal forge-glow..."
            }
        }
    }
    
    rooms["highland_pass"] = {
        "id": "highland_pass",
        "name": "Highland Pass",
        "description": "A narrow pass between two peaks. The wind howls through the gap. Snow drifts against the rocks. This is the main route to the frozen north.",
        "location_type": "wilderness",
        "coordinates": [4, 6],
        "items": {},
        "exits": {
            "south": {"target": "highland_road", "type": "direction"},
            "west": {"target": "rocky_valley", "type": "direction"},
            "north": {"target": "high_pass", "type": "direction"},
            "east": {"target": "eastern_highlands", "type": "direction"}
        }
    }
    
    rooms["high_pass"] = {
        "id": "high_pass",
        "name": "High Mountain Pass",
        "description": "Near the top of the mountain range. The air is thin and bitterly cold. Ice clings to the rocks, and snow covers everything. The path ahead leads to the peak itself.",
        "location_type": "wilderness",
        "coordinates": [2, 10],
        "items": {"ice_crystal": {"quantity": 1, "value": 18}},
        "exits": {
            "south": {"target": "mountain_path", "type": "direction"},
            "east": {"target": "highland_pass", "type": "direction"},
            "north": {"target": "mountain_peak", "type": "direction"}
        }
    }
    
    rooms["mountain_peak"] = {
        "id": "mountain_peak",
        "name": "Stormspire Summit",
        "description": "The highest point in the realm. You stand above the clouds, with an endless vista spread before you. A frozen spire of ice rises nearby, its surface etched with ancient magic. This is the entrance to the Frozen Spire.",
        "location_type": "wilderness",
        "coordinates": [2, 12],
        "items": {"eagle_feather": {"quantity": 1, "value": 35}},
        "exits": {
            "south": {"target": "high_pass", "type": "direction"},
            "north": {"target": "frozen_approach", "type": "direction"},
            "enter": {
                "target": "FIXED",
                "type": "fixed_dungeon",
                "dungeon_id": "frozen_spire",
                "transition_text": "You touch the frozen spire and reality fractures. You step through into a realm of eternal ice and ancient power..."
            }
        }
    }
    
    rooms["eastern_highlands"] = {
        "id": "eastern_highlands",
        "name": "Eastern Highlands",
        "description": "The eastern slopes of the mountains, where the terrain transitions to drier lands. The vegetation is sparse, adapted to the harsh climate. Far below, the desert shimmers.",
        "location_type": "wilderness",
        "coordinates": [6, 6],
        "items": {},
        "exits": {
            "west": {"target": "highland_pass", "type": "direction"},
            "south": {"target": "highland_road", "type": "direction"},
            "east": {"target": "desert_cliffs", "type": "direction"},
            "north": {"target": "kingshold_approach", "type": "direction"}
        }
    }
    
    # =========================================================================
    # FROZEN WASTES - Far North
    # =========================================================================
    
    rooms["frozen_approach"] = {
        "id": "frozen_approach",
        "name": "Frozen Approach",
        "description": "Beyond the mountain peak lies a frozen wilderness. Eternal snow covers the ground, and the wind cuts like knives. Few venture this far north and return.",
        "location_type": "wilderness",
        "coordinates": [2, 14],
        "items": {"frost_flower": {"quantity": 1, "value": 20}},
        "exits": {
            "south": {"target": "mountain_peak", "type": "direction"},
            "north": {"target": "tundra_edge", "type": "direction"},
            "east": {"target": "frozen_outpost", "type": "direction"}
        }
    }
    
    rooms["tundra_edge"] = {
        "id": "tundra_edge",
        "name": "Tundra Edge",
        "description": "The beginning of the endless tundra. Nothing but snow and ice stretches to the horizon. The cold is intense, sapping your strength with every step.",
        "location_type": "wilderness",
        "coordinates": [2, 16],
        "items": {"polar_moss": {"quantity": 2, "value": 6}},
        "exits": {
            "south": {"target": "frozen_approach", "type": "direction"},
            "north": {"target": "frozen_lake", "type": "direction"},
            "west": {"target": "ice_fields", "type": "direction"}
        }
    }
    
    rooms["frozen_lake"] = {
        "id": "frozen_lake",
        "name": "Frozen Lake",
        "description": "A vast lake frozen solid. The ice is thick enough to walk on, but cracks and groans ominously. Dark shapes can be seen frozen beneath the surface.",
        "location_type": "wilderness",
        "coordinates": [2, 18],
        "items": {"frozen_fish": {"quantity": 2, "value": 10}},
        "exits": {
            "south": {"target": "tundra_edge", "type": "direction"},
            "west": {"target": "ice_caves_entrance", "type": "direction"}
        }
    }
    
    rooms["ice_fields"] = {
        "id": "ice_fields",
        "name": "Ice Fields",
        "description": "Jagged ice formations rise from the frozen ground. The wind has carved the ice into bizarre, beautiful shapes. The cold here is deadly - you cannot stay long.",
        "location_type": "wilderness",
        "coordinates": [0, 16],
        "items": {"ice_crystal": {"quantity": 2, "value": 18}},
        "exits": {
            "east": {"target": "tundra_edge", "type": "direction"},
            "south": {"target": "ice_caves_entrance", "type": "direction"}
        }
    }
    
    rooms["ice_caves_entrance"] = {
        "id": "ice_caves_entrance",
        "name": "Ice Caves Entrance",
        "description": "The entrance to a network of ice caves. Blue light filters through the frozen walls. The caves offer shelter from the wind, but strange creatures are said to lurk within.",
        "location_type": "wilderness",
        "coordinates": [0, 18],
        "items": {},
        "exits": {
            "north": {"target": "ice_fields", "type": "direction"},
            "east": {"target": "frozen_lake", "type": "direction"}
        }
    }
    
    rooms["frozen_outpost"] = {
        "id": "frozen_outpost",
        "name": "Abandoned Outpost",
        "description": "The ruins of a research outpost, abandoned long ago. Frozen supplies and equipment lie scattered about. Whatever happened here, it was sudden.",
        "location_type": "building",
        "coordinates": [4, 14],
        "items": {"torch": {"quantity": 2, "value": 5}, "faded_map": {"quantity": 1, "value": 20}},
        "exits": {
            "west": {"target": "frozen_approach", "type": "direction"},
            "south": {"target": "kingshold_approach", "type": "direction"}
        }
    }
    
    # =========================================================================
    # KINGSHOLD CASTLE - Northeast
    # =========================================================================
    
    rooms["kingshold_approach"] = {
        "id": "kingshold_approach",
        "name": "Approach to Kingshold",
        "description": "A grand road paved with white stone leads to the magnificent Kingshold Castle. Banners flutter from distant towers. This is the seat of royal power in the realm.",
        "location_type": "wilderness",
        "coordinates": [6, 10],
        "items": {},
        "exits": {
            "south": {"target": "eastern_highlands", "type": "direction"},
            "north": {"target": "frozen_outpost", "type": "direction"},
            "east": {"target": "castle_gates", "type": "direction"}
        }
    }
    
    rooms["castle_gates"] = {
        "id": "castle_gates",
        "name": "Castle Gates",
        "description": "Massive iron-bound gates stand before you, flanked by towers manned by vigilant guards. The royal banner - a golden crown on blue - flies overhead. Visitors must state their business.",
        "location_type": "settlement",
        "coordinates": [8, 10],
        "items": {},
        "exits": {
            "west": {"target": "kingshold_approach", "type": "direction"},
            "enter": {"target": "castle_courtyard", "type": "named", "display": "Enter the castle"}
        }
    }
    
    rooms["castle_courtyard"] = {
        "id": "castle_courtyard",
        "name": "Castle Courtyard",
        "description": "A spacious courtyard within the castle walls. Knights train in one corner, servants hurry about their duties, and nobles stroll in fine clothes. The castle keep rises impressively ahead.",
        "location_type": "settlement",
        "coordinates": [9, 10],
        "items": {},
        "exits": {
            "gate": {"target": "castle_gates", "type": "direction"},
            "keep": {"target": "castle_hall", "type": "named", "display": "Castle Great Hall"},
            "barracks": {"target": "castle_barracks", "type": "named", "display": "Barracks"},
            "garden": {"target": "royal_garden", "type": "named", "display": "Royal Garden"}
        }
    }
    
    rooms["castle_hall"] = {
        "id": "castle_hall",
        "name": "Castle Great Hall",
        "description": "A magnificent hall with vaulted ceilings and stained glass windows. Tapestries depicting the realm's history line the walls. At the far end sits the empty throne - the king is often away on matters of state.",
        "location_type": "building",
        "coordinates": [10, 10],
        "items": {},
        "exits": {
            "outside": {"target": "castle_courtyard", "type": "direction"},
            "tower": {"target": "castle_tower", "type": "named", "display": "Tower stairs"}
        }
    }
    
    rooms["castle_tower"] = {
        "id": "castle_tower",
        "name": "Castle Tower",
        "description": "A high tower offering a commanding view of the surrounding lands. Maps and telescopes are arranged near the windows. From here, you can see across the entire realm.",
        "location_type": "building",
        "coordinates": [10, 11],
        "items": {"old_spyglass": {"quantity": 1, "value": 30}},
        "exits": {
            "down": {"target": "castle_hall", "type": "direction"}
        }
    }
    
    rooms["castle_barracks"] = {
        "id": "castle_barracks",
        "name": "Castle Barracks",
        "description": "Housing for the castle guard. Bunk beds line the walls, and weapon racks hold an impressive array of arms. Soldiers rest between patrols.",
        "location_type": "building",
        "coordinates": [9, 11],
        "items": {"broken_arrow": {"quantity": 2, "value": 2}},
        "exits": {
            "outside": {"target": "castle_courtyard", "type": "direction"}
        }
    }
    
    rooms["royal_garden"] = {
        "id": "royal_garden",
        "name": "Royal Garden",
        "description": "An exquisite garden with manicured hedges, flowering bushes, and marble statues. A fountain tinkles pleasantly in the center. This is a place of beauty and contemplation.",
        "location_type": "settlement",
        "coordinates": [9, 9],
        "items": {"wildflower": {"quantity": 3, "value": 2}},
        "exits": {
            "inside": {"target": "castle_courtyard", "type": "direction"}
        }
    }
    
    # =========================================================================
    # SUNSCORCH DESERT - East/Southeast
    # =========================================================================
    
    rooms["desert_border"] = {
        "id": "desert_border",
        "name": "Desert Border",
        "description": "The last of the grass gives way to sand and rock. Before you stretches the Sunscorch Desert, a vast expanse of dunes and deadly heat. Only the foolish or desperate venture further unprepared.",
        "location_type": "wilderness",
        "coordinates": [10, 0],
        "items": {},
        "exits": {
            "west": {"target": "farmland_east", "type": "direction"},
            "south": {"target": "dusty_crossroads", "type": "direction"},
            "east": {"target": "desert_dunes_west", "type": "direction"},
            "north": {"target": "desert_cliffs", "type": "direction"}
        }
    }
    
    rooms["desert_cliffs"] = {
        "id": "desert_cliffs",
        "name": "Desert Cliffs",
        "description": "Red sandstone cliffs rise sharply from the desert floor. Caves and overhangs offer some shade. Ancient drawings are etched into the rock face.",
        "location_type": "wilderness",
        "coordinates": [10, 4],
        "items": {"sandstone_chunk": {"quantity": 2, "value": 5}},
        "exits": {
            "south": {"target": "desert_border", "type": "direction"},
            "west": {"target": "eastern_highlands", "type": "direction"},
            "east": {"target": "canyon_entrance", "type": "direction"}
        }
    }
    
    rooms["canyon_entrance"] = {
        "id": "canyon_entrance",
        "name": "Canyon Entrance",
        "description": "The entrance to a deep canyon carved by an ancient river long since dried up. The walls tower above you, providing blessed shade. The passage winds deeper into the badlands.",
        "location_type": "wilderness",
        "coordinates": [12, 4],
        "items": {},
        "exits": {
            "west": {"target": "desert_cliffs", "type": "direction"},
            "east": {"target": "canyon_depths", "type": "direction"}
        }
    }
    
    rooms["canyon_depths"] = {
        "id": "canyon_depths",
        "name": "Canyon Depths",
        "description": "Deep within the canyon. Strange rock formations cast bizarre shadows. The silence is oppressive, broken only by the wind whistling through the narrows.",
        "location_type": "wilderness",
        "coordinates": [14, 4],
        "items": {"cave_crystal": {"quantity": 1, "value": 22}},
        "exits": {
            "west": {"target": "canyon_entrance", "type": "direction"},
            "south": {"target": "hidden_oasis", "type": "direction"}
        }
    }
    
    rooms["desert_dunes_west"] = {
        "id": "desert_dunes_west",
        "name": "Western Dunes",
        "description": "Endless sand dunes stretch before you. The sun beats down mercilessly. Navigation is difficult - one dune looks much like another. Tracks in the sand are quickly erased by the wind.",
        "location_type": "wilderness",
        "coordinates": [12, 0],
        "items": {},
        "exits": {
            "west": {"target": "desert_border", "type": "direction"},
            "east": {"target": "desert_dunes_center", "type": "direction"},
            "south": {"target": "scorpion_flats", "type": "direction"}
        }
    }
    
    rooms["desert_dunes_center"] = {
        "id": "desert_dunes_center",
        "name": "Central Dunes",
        "description": "The heart of the Sunscorch Desert. The dunes here are massive, some rising hundreds of feet. The heat is almost unbearable. Mirages shimmer on the horizon.",
        "location_type": "wilderness",
        "coordinates": [14, 0],
        "items": {},
        "exits": {
            "west": {"target": "desert_dunes_west", "type": "direction"},
            "east": {"target": "oasis_village", "type": "direction"},
            "north": {"target": "hidden_oasis", "type": "direction"}
        }
    }
    
    rooms["hidden_oasis"] = {
        "id": "hidden_oasis",
        "name": "Hidden Oasis",
        "description": "A miraculous oasis hidden among the dunes. Palm trees provide shade, and a crystal-clear pool offers cool water. A few resilient plants grow here. This is a lifesaver in the deadly desert.",
        "location_type": "wilderness",
        "coordinates": [14, 2],
        "items": {"cactus_fruit": {"quantity": 2, "value": 8}},
        "exits": {
            "south": {"target": "desert_dunes_center", "type": "direction"},
            "north": {"target": "canyon_depths", "type": "direction"}
        }
    }
    
    rooms["scorpion_flats"] = {
        "id": "scorpion_flats",
        "name": "Scorpion Flats",
        "description": "A rocky, flat area infested with scorpions. Their burrows dot the sandy ground. One must tread carefully here - the creatures are aggressive and venomous.",
        "location_type": "wilderness",
        "coordinates": [12, -2],
        "items": {"scorpion_tail": {"quantity": 1, "value": 12}},
        "exits": {
            "north": {"target": "desert_dunes_west", "type": "direction"},
            "east": {"target": "mesa_base", "type": "direction"},
            "south": {"target": "desert_ruins", "type": "direction"}
        }
    }
    
    rooms["mesa_base"] = {
        "id": "mesa_base",
        "name": "Mesa Base",
        "description": "A massive flat-topped mesa rises from the desert. The climb looks treacherous but possible. From the top, one could see for miles. Ancient trails wind up the sides.",
        "location_type": "wilderness",
        "coordinates": [14, -2],
        "items": {},
        "exits": {
            "west": {"target": "scorpion_flats", "type": "direction"},
            "up": {"target": "mesa_top", "type": "direction"},
            "east": {"target": "oasis_village", "type": "direction"}
        }
    }
    
    rooms["mesa_top"] = {
        "id": "mesa_top",
        "name": "Mesa Summit",
        "description": "The top of the great mesa. The view is breathtaking - you can see the entire desert, the distant mountains, and even a glint of the sea to the south. Old ruins are half-buried in sand here.",
        "location_type": "wilderness",
        "coordinates": [14, -1],
        "items": {"desert_rose": {"quantity": 1, "value": 15}, "ancient_brick": {"quantity": 1, "value": 10}},
        "exits": {
            "down": {"target": "mesa_base", "type": "direction"}
        }
    }
    
    rooms["oasis_village"] = {
        "id": "oasis_village",
        "name": "Oasis Village of Al-Zahir",
        "description": "A small but thriving village built around a large oasis. Adobe buildings provide shelter from the sun. The locals are friendly but wary of outsiders. Traders pass through regularly.",
        "location_type": "settlement",
        "coordinates": [16, 0],
        "items": {},
        "exits": {
            "west": {"target": "desert_dunes_center", "type": "direction"},
            "south": {"target": "mesa_base", "type": "direction"},
            "east": {"target": "desert_ruins", "type": "direction"}
        }
    }
    
    rooms["desert_ruins"] = {
        "id": "desert_ruins",
        "name": "Desert Ruins",
        "description": "The remains of an ancient civilization, half-swallowed by the sands. Crumbling pillars and broken statues hint at former glory. Treasures - and dangers - await those who explore.",
        "location_type": "wilderness",
        "coordinates": [14, -4],
        "items": {"old_coin": {"quantity": 2, "value": 3}, "dusty_tome": {"quantity": 1, "value": 35}},
        "exits": {
            "north": {"target": "scorpion_flats", "type": "direction"},
            "west": {"target": "oasis_village", "type": "direction"},
            "south": {"target": "sandstone_fortress", "type": "direction"}
        }
    }
    
    rooms["sandstone_fortress"] = {
        "id": "sandstone_fortress",
        "name": "Sandstone Fortress",
        "description": "A crumbling fortress of sandstone, once a mighty stronghold, now home to bandits and desert creatures. The walls still stand, offering shelter from sandstorms.",
        "location_type": "building",
        "coordinates": [14, -6],
        "items": {"rusty_sword": {"quantity": 1, "value": 12}, "broken_shield": {"quantity": 1, "value": 8}},
        "exits": {
            "north": {"target": "desert_ruins", "type": "direction"},
            "west": {"target": "coastal_road_east", "type": "direction"}
        }
    }
    
    # =========================================================================
    # AZURE COAST & PORT HAVEN - South
    # Contains: Sunken Catacombs entrance
    # =========================================================================
    
    rooms["coastal_road_north"] = {
        "id": "coastal_road_north",
        "name": "Northern Coastal Road",
        "description": "A sandy road leading south toward the Azure Coast. You can smell the salt on the breeze and hear the distant cry of seagulls. The road is well-traveled by merchants.",
        "location_type": "wilderness",
        "coordinates": [0, -6],
        "items": {},
        "exits": {
            "north": {"target": "crossroads", "type": "direction"},
            "south": {"target": "coastal_cliffs", "type": "direction"},
            "east": {"target": "farmland_south", "type": "direction"}
        }
    }
    
    rooms["coastal_cliffs"] = {
        "id": "coastal_cliffs",
        "name": "Coastal Cliffs",
        "description": "Dramatic cliffs overlook the sparkling Azure Coast. The waves crash against the rocks far below. A winding path descends to the beaches. Seabirds wheel overhead.",
        "location_type": "wilderness",
        "coordinates": [0, -8],
        "items": {"eagle_feather": {"quantity": 1, "value": 35}},
        "exits": {
            "north": {"target": "coastal_road_north", "type": "direction"},
            "south": {"target": "sandy_beach", "type": "direction"},
            "east": {"target": "lighthouse_hill", "type": "direction"},
            "west": {"target": "graveyard_road", "type": "direction"}
        }
    }
    
    rooms["lighthouse_hill"] = {
        "id": "lighthouse_hill",
        "name": "Lighthouse Hill",
        "description": "A tall white lighthouse stands on this promontory, its light guiding ships safely into harbor. The keeper maintains it diligently. The view of the coast is spectacular.",
        "location_type": "building",
        "coordinates": [2, -8],
        "items": {"old_spyglass": {"quantity": 1, "value": 30}},
        "exits": {
            "west": {"target": "coastal_cliffs", "type": "direction"},
            "south": {"target": "port_haven_north", "type": "direction"}
        }
    }
    
    rooms["sandy_beach"] = {
        "id": "sandy_beach",
        "name": "Sandy Beach",
        "description": "A beautiful stretch of golden sand. Waves lap gently at the shore. Shells and driftwood are scattered about. Children play in the surf while fishermen mend their nets.",
        "location_type": "wilderness",
        "coordinates": [0, -10],
        "items": {"seashell": {"quantity": 4, "value": 4}, "driftwood": {"quantity": 2, "value": 3}},
        "exits": {
            "north": {"target": "coastal_cliffs", "type": "direction"},
            "east": {"target": "port_haven_docks", "type": "direction"},
            "west": {"target": "tidal_caves", "type": "direction"},
            "south": {"target": "reef_shallows", "type": "direction"}
        }
    }
    
    rooms["tidal_caves"] = {
        "id": "tidal_caves",
        "name": "Tidal Caves",
        "description": "Sea caves carved by millennia of waves. At low tide, you can explore the shallow caves. Tide pools teem with colorful marine life. Locals gather shellfish here.",
        "location_type": "wilderness",
        "coordinates": [-2, -10],
        "items": {"seaweed": {"quantity": 3, "value": 2}, "coral_piece": {"quantity": 1, "value": 12}},
        "exits": {
            "east": {"target": "sandy_beach", "type": "direction"},
            "north": {"target": "rocky_shore", "type": "direction"}
        }
    }
    
    rooms["rocky_shore"] = {
        "id": "rocky_shore",
        "name": "Rocky Shore",
        "description": "A stretch of coast dominated by large boulders and rocky outcroppings. The surf crashes violently against the rocks. Crabs scuttle between the tide pools.",
        "location_type": "wilderness",
        "coordinates": [-2, -8],
        "items": {},
        "exits": {
            "south": {"target": "tidal_caves", "type": "direction"},
            "east": {"target": "coastal_cliffs", "type": "direction"}
        }
    }
    
    rooms["reef_shallows"] = {
        "id": "reef_shallows",
        "name": "Reef Shallows",
        "description": "Clear, shallow water over a coral reef. The water is warm and teeming with colorful fish. Pieces of coral and shells can be gathered here. The reef protects a small cove.",
        "location_type": "wilderness",
        "coordinates": [0, -12],
        "items": {"coral_piece": {"quantity": 2, "value": 12}, "pearl": {"quantity": 1, "value": 35}},
        "exits": {
            "north": {"target": "sandy_beach", "type": "direction"},
            "east": {"target": "smugglers_cove", "type": "direction"}
        }
    }
    
    rooms["smugglers_cove"] = {
        "id": "smugglers_cove",
        "name": "Smuggler's Cove",
        "description": "A hidden cove accessible only by a narrow passage. Evidence of illegal activity is everywhere - crates, ropes, and hidden paths. The authorities rarely find this place.",
        "location_type": "wilderness",
        "coordinates": [2, -12],
        "items": {"rope_coil": {"quantity": 1, "value": 20}},
        "exits": {
            "west": {"target": "reef_shallows", "type": "direction"},
            "north": {"target": "port_haven_docks", "type": "direction"},
            "east": {"target": "grand_harbor_road", "type": "direction"}
        }
    }
    
    rooms["port_haven_north"] = {
        "id": "port_haven_north",
        "name": "Port Haven - North District",
        "description": "The northern part of Port Haven, the largest coastal settlement. Ships' masts are visible over the rooftops. The smell of fish and salt fills the air. Sailors and merchants bustle about.",
        "location_type": "settlement",
        "coordinates": [3, -8],
        "items": {},
        "exits": {
            "north": {"target": "lighthouse_hill", "type": "direction"},
            "south": {"target": "port_haven_market", "type": "direction"},
            "west": {"target": "coastal_road_east", "type": "direction"}
        }
    }
    
    rooms["port_haven_market"] = {
        "id": "port_haven_market",
        "name": "Port Haven Market",
        "description": "A bustling marketplace where goods from across the seas are traded. Exotic spices, foreign silks, and strange artifacts catch your eye. Haggling is expected.",
        "location_type": "settlement",
        "coordinates": [3, -9],
        "items": {},
        "exits": {
            "north": {"target": "port_haven_north", "type": "direction"},
            "south": {"target": "port_haven_docks", "type": "direction"},
            "inn": {"target": "harbor_inn", "type": "named", "display": "The Salty Sailor Inn"}
        }
    }
    
    rooms["harbor_inn"] = {
        "id": "harbor_inn",
        "name": "The Salty Sailor Inn",
        "description": "A rowdy inn frequented by sailors and travelers. Sea chanties fill the air, and the ale flows freely. Rooms can be rented upstairs. Stories of adventure are shared over drinks.",
        "location_type": "building",
        "coordinates": [4, -9],
        "items": {"ale_mug": {"quantity": 2, "value": 3}},
        "exits": {
            "outside": {"target": "port_haven_market", "type": "direction"}
        }
    }
    
    rooms["port_haven_docks"] = {
        "id": "port_haven_docks",
        "name": "Port Haven Docks",
        "description": "The busy docks of Port Haven. Ships from distant lands are moored here, loading and unloading cargo. The creak of wood and shout of sailors creates a constant din. A well-maintained road leads south toward the Grand Harbor.",
        "location_type": "settlement",
        "coordinates": [3, -10],
        "items": {"fishing_net": {"quantity": 1, "value": 15}},
        "exits": {
            "north": {"target": "port_haven_market", "type": "direction"},
            "west": {"target": "sandy_beach", "type": "direction"},
            "south": {"target": "grand_harbor_road", "type": "direction"},
            "east": {"target": "old_pier", "type": "direction"}
        }
    }
    
    rooms["old_pier"] = {
        "id": "old_pier",
        "name": "Old Pier",
        "description": "A weathered wooden pier extending into the sea. Fishermen cast their lines here. The boards creak underfoot. At the end, you can see the ancient sea ruins in the distance.",
        "location_type": "wilderness",
        "coordinates": [5, -10],
        "items": {"old_fishing_rod": {"quantity": 1, "value": 15}},
        "exits": {
            "west": {"target": "port_haven_docks", "type": "direction"},
            "south": {"target": "dungeon_ruins_entrance", "type": "direction"}
        }
    }
    
    rooms["dungeon_ruins_entrance"] = {
        "id": "dungeon_ruins_entrance",
        "name": "Sunken Catacombs Entrance",
        "description": "Ancient stone steps descend into the sea. At low tide, the entrance to the Sunken Catacombs is revealed - a flooded tomb complex from a civilization lost to the waves long ago.",
        "location_type": "wilderness",
        "coordinates": [5, -12],
        "items": {},
        "exits": {
            "north": {"target": "old_pier", "type": "direction"},
            "enter": {
                "target": "DUNGEON",
                "type": "time_gated_dungeon",
                "dungeon_id": "sunken_catacombs",
                "transition_text": "You descend the algae-slick steps into the flooded darkness. The air is thick with the scent of brine and ancient death..."
            }
        }
    }
    
    rooms["coastal_road_east"] = {
        "id": "coastal_road_east",
        "name": "Eastern Coastal Road",
        "description": "A road connecting Port Haven to the eastern desert. The terrain transitions from coastal greenery to arid scrubland. Camel caravans sometimes pass this way.",
        "location_type": "wilderness",
        "coordinates": [6, -6],
        "items": {},
        "exits": {
            "north": {"target": "dusty_crossroads", "type": "direction"},
            "south": {"target": "port_haven_north", "type": "direction"},
            "east": {"target": "sandstone_fortress", "type": "direction"}
        }
    }
    
    # =========================================================================
    # ADDITIONAL FOREST AREAS - West expansion
    # =========================================================================
    
    rooms["twilight_woods"] = {
        "id": "twilight_woods",
        "name": "Twilight Woods",
        "description": "These woods are perpetually dim, even at midday. Strange blue mushrooms grow on the trees, providing an eerie glow. The silence here is unsettling.",
        "location_type": "wilderness",
        "coordinates": [-10, -2],
        "items": {"glowing_moss": {"quantity": 3, "value": 8}},
        "exits": {
            "north": {"target": "ancient_grove", "type": "direction"},
            "south": {"target": "dark_hollow", "type": "direction"},
            "west": {"target": "forgotten_shrine", "type": "direction"}
        }
    }
    
    rooms["dark_hollow"] = {
        "id": "dark_hollow",
        "name": "Dark Hollow",
        "description": "A depression in the forest floor where light barely reaches. Twisted roots create a maze-like terrain. Something watches from the shadows.",
        "location_type": "wilderness",
        "coordinates": [-10, -4],
        "items": {"mushroom": {"quantity": 4, "value": 5}},
        "exits": {
            "north": {"target": "twilight_woods", "type": "direction"},
            "east": {"target": "forest_swamp_border", "type": "direction"}
        }
    }
    
    rooms["forgotten_shrine"] = {
        "id": "forgotten_shrine",
        "name": "Forgotten Shrine",
        "description": "An ancient stone shrine covered in moss and vines. Offerings left here long ago have rotted away. The carved face on the altar still watches with empty eyes.",
        "location_type": "wilderness",
        "coordinates": [-12, -2],
        "items": {"old_coin": {"quantity": 2, "value": 3}, "prayer_candle": {"quantity": 1, "value": 5}},
        "exits": {
            "east": {"target": "twilight_woods", "type": "direction"},
            "north": {"target": "wolf_den", "type": "direction"},
            "south": {"target": "tangled_thicket", "type": "direction"}
        }
    }
    
    rooms["wolf_den"] = {
        "id": "wolf_den",
        "name": "Wolf Den",
        "description": "A rocky outcropping with caves beneath. Wolf tracks and bones are scattered about. The pack seems to be away, but may return at any moment.",
        "location_type": "wilderness",
        "coordinates": [-12, 0],
        "items": {"wolf_pelt": {"quantity": 1, "value": 18}, "old_bone": {"quantity": 4, "value": 2}},
        "exits": {
            "south": {"target": "forgotten_shrine", "type": "direction"},
            "east": {"target": "hermit_cabin", "type": "direction"}
        }
    }
    
    rooms["tangled_thicket"] = {
        "id": "tangled_thicket",
        "name": "Tangled Thicket",
        "description": "Dense undergrowth makes passage difficult. Thorns and briars tear at your clothes. Animal trails crisscross through the vegetation.",
        "location_type": "wilderness",
        "coordinates": [-12, -4],
        "items": {"stick": {"quantity": 3, "value": 1}},
        "exits": {
            "north": {"target": "forgotten_shrine", "type": "direction"},
            "east": {"target": "dark_hollow", "type": "direction"},
            "south": {"target": "old_logging_camp", "type": "direction"}
        }
    }
    
    rooms["old_logging_camp"] = {
        "id": "old_logging_camp",
        "name": "Old Logging Camp",
        "description": "An abandoned logging camp. Rusted saws and rotten stumps remain. A collapsed cabin offers little shelter. Nature is reclaiming this place.",
        "location_type": "building",
        "coordinates": [-12, -6],
        "items": {"rope_coil": {"quantity": 1, "value": 20}, "rusty_sword": {"quantity": 1, "value": 12}},
        "exits": {
            "north": {"target": "tangled_thicket", "type": "direction"},
            "east": {"target": "western_swamp_approach", "type": "direction"}
        }
    }
    
    rooms["western_swamp_approach"] = {
        "id": "western_swamp_approach",
        "name": "Western Swamp Approach",
        "description": "The ground becomes increasingly soggy as the forest gives way to swampland. Mist curls through the trees, and the croaking of frogs fills the air.",
        "location_type": "wilderness",
        "coordinates": [-10, -6],
        "items": {"swamp_reed": {"quantity": 2, "value": 3}},
        "exits": {
            "west": {"target": "old_logging_camp", "type": "direction"},
            "east": {"target": "sunken_ruins", "type": "direction"}
        }
    }
    
    rooms["fairy_ring"] = {
        "id": "fairy_ring",
        "name": "Fairy Ring",
        "description": "A perfect circle of mushrooms in a moonlit glade. Legend says fairies dance here at night. The air shimmers with faint magic.",
        "location_type": "wilderness",
        "coordinates": [-7, 4],
        "items": {"mushroom": {"quantity": 6, "value": 5}},
        "exits": {
            "south": {"target": "forest_grove", "type": "direction"},
            "east": {"target": "woodland_shrine", "type": "direction"}
        }
    }
    
    rooms["fallen_giant"] = {
        "id": "fallen_giant",
        "name": "Fallen Giant",
        "description": "A massive ancient tree has fallen here, creating a bridge over a ravine. Moss and fungi cover its enormous trunk. The hollow interior could shelter several people.",
        "location_type": "wilderness",
        "coordinates": [-8, 4],
        "items": {"shelf_mushroom": {"quantity": 3, "value": 4}},
        "exits": {
            "east": {"target": "fairy_ring", "type": "direction"},
            "south": {"target": "dungeon_forest_entrance", "type": "direction"},
            "west": {"target": "ravine_crossing", "type": "direction"}
        }
    }
    
    rooms["ravine_crossing"] = {
        "id": "ravine_crossing",
        "name": "Ravine Crossing",
        "description": "A rope bridge spans a deep ravine. The boards creak ominously. Far below, a stream glints in the shadows. Brave souls cross quickly.",
        "location_type": "wilderness",
        "coordinates": [-10, 4],
        "items": {"old_rope": {"quantity": 1, "value": 6}},
        "exits": {
            "east": {"target": "fallen_giant", "type": "direction"},
            "north": {"target": "hunter_camp", "type": "direction"}
        }
    }
    
    rooms["hunter_camp"] = {
        "id": "hunter_camp",
        "name": "Hunter's Camp",
        "description": "A small camp used by hunters and trappers. A fire pit is surrounded by log seats. Animal traps hang from nearby branches. Fresh tracks suggest recent use.",
        "location_type": "building",
        "coordinates": [-10, 6],
        "items": {"wolf_pelt": {"quantity": 1, "value": 18}, "raw_meat": {"quantity": 2, "value": 8}},
        "exits": {
            "south": {"target": "ravine_crossing", "type": "direction"},
            "east": {"target": "wolf_den", "type": "direction"}
        }
    }
    
    # =========================================================================
    # ADDITIONAL MOUNTAIN AREAS - North expansion
    # =========================================================================
    
    rooms["goat_trail"] = {
        "id": "goat_trail",
        "name": "Goat Trail",
        "description": "A narrow trail used by mountain goats winds along the cliff face. One wrong step would be fatal. The view is breathtaking.",
        "location_type": "wilderness",
        "coordinates": [-2, 10],
        "items": {},
        "exits": {
            "east": {"target": "high_pass", "type": "direction"},
            "south": {"target": "waterfall_base", "type": "direction"},
            "north": {"target": "eagle_nest", "type": "direction"}
        }
    }
    
    rooms["eagle_nest"] = {
        "id": "eagle_nest",
        "name": "Eagle's Nest",
        "description": "A high plateau where eagles nest. Feathers and bones are scattered about. The view of the realm is magnificent. The wind is strong and cold.",
        "location_type": "wilderness",
        "coordinates": [-2, 12],
        "items": {"eagle_feather": {"quantity": 3, "value": 35}},
        "exits": {
            "south": {"target": "goat_trail", "type": "direction"},
            "east": {"target": "mountain_peak", "type": "direction"}
        }
    }
    
    rooms["mining_tunnels"] = {
        "id": "mining_tunnels",
        "name": "Old Mining Tunnels",
        "description": "Abandoned mine shafts bore into the mountain. The timbers are rotted and dangerous. Occasional glints suggest valuable ore might still be found.",
        "location_type": "building",
        "coordinates": [4, 8],
        "items": {"iron_ore": {"quantity": 3, "value": 15}, "copper_ore": {"quantity": 2, "value": 10}},
        "exits": {
            "outside": {"target": "dungeon_mountain_entrance", "type": "direction"}
        }
    }
    
    rooms["hermit_peak"] = {
        "id": "hermit_peak",
        "name": "Hermit's Peak",
        "description": "A secluded peak where a meditation shrine sits. Prayer flags flutter in the wind. Someone has carved steps into the rock face.",
        "location_type": "wilderness",
        "coordinates": [0, 12],
        "items": {"prayer_candle": {"quantity": 2, "value": 5}},
        "exits": {
            "south": {"target": "high_pass", "type": "direction"},
            "west": {"target": "eagle_nest", "type": "direction"},
            "east": {"target": "mountain_peak", "type": "direction"}
        }
    }
    
    rooms["avalanche_path"] = {
        "id": "avalanche_path",
        "name": "Avalanche Path",
        "description": "A path through an area prone to avalanches. Debris from past slides is visible. Snow hangs precariously on the slopes above. Move quickly and quietly.",
        "location_type": "wilderness",
        "coordinates": [4, 10],
        "items": {},
        "exits": {
            "south": {"target": "highland_pass", "type": "direction"},
            "north": {"target": "mountain_peak", "type": "direction"},
            "east": {"target": "kingshold_approach", "type": "direction"}
        }
    }
    
    rooms["frozen_stream"] = {
        "id": "frozen_stream",
        "name": "Frozen Stream",
        "description": "A stream frozen solid. Ice formations hang from the rocks. The surface is slippery but crossable. Fish are visible beneath the clear ice.",
        "location_type": "wilderness",
        "coordinates": [-4, 8],
        "items": {"frozen_fish": {"quantity": 2, "value": 10}},
        "exits": {
            "east": {"target": "waterfall_base", "type": "direction"},
            "north": {"target": "goat_trail", "type": "direction"},
            "south": {"target": "mountain_stream", "type": "direction"}
        }
    }
    
    rooms["dwarf_ruins"] = {
        "id": "dwarf_ruins",
        "name": "Dwarven Ruins",
        "description": "The crumbling remains of an ancient dwarven outpost. Stone foundations and collapsed walls hint at former glory. Runes are carved into surviving stones.",
        "location_type": "building",
        "coordinates": [4, 12],
        "items": {"iron_ingot": {"quantity": 1, "value": 20}, "ancient_brick": {"quantity": 2, "value": 10}},
        "exits": {
            "south": {"target": "avalanche_path", "type": "direction"},
            "west": {"target": "mountain_peak", "type": "direction"}
        }
    }
    
    rooms["northern_lookout"] = {
        "id": "northern_lookout",
        "name": "Northern Lookout",
        "description": "A stone watchtower on a mountain spur. From here, guards once watched for threats from the north. The tower still stands, though abandoned.",
        "location_type": "building",
        "coordinates": [6, 12],
        "items": {"old_spyglass": {"quantity": 1, "value": 30}},
        "exits": {
            "south": {"target": "kingshold_approach", "type": "direction"},
            "west": {"target": "dwarf_ruins", "type": "direction"}
        }
    }
    
    # =========================================================================
    # ADDITIONAL DESERT AREAS - East expansion
    # =========================================================================
    
    rooms["bleached_bones"] = {
        "id": "bleached_bones",
        "name": "Valley of Bones",
        "description": "A valley littered with the bleached bones of countless creatures. Some are enormous, suggesting ancient beasts. The desert has claimed many victims.",
        "location_type": "wilderness",
        "coordinates": [16, -4],
        "items": {"old_bone": {"quantity": 5, "value": 2}},
        "exits": {
            "west": {"target": "oasis_village", "type": "direction"},
            "south": {"target": "ancient_pyramid", "type": "direction"},
            "north": {"target": "sand_sea", "type": "direction"}
        }
    }
    
    rooms["sand_sea"] = {
        "id": "sand_sea",
        "name": "Sea of Sand",
        "description": "An endless expanse of sand dunes that seemingly goes on forever. The wind shifts the sands constantly, erasing all tracks. Navigation is nearly impossible.",
        "location_type": "wilderness",
        "coordinates": [16, 0],
        "items": {},
        "exits": {
            "south": {"target": "bleached_bones", "type": "direction"},
            "west": {"target": "oasis_village", "type": "direction"},
            "east": {"target": "mirage_oasis", "type": "direction"}
        }
    }
    
    rooms["mirage_oasis"] = {
        "id": "mirage_oasis",
        "name": "Mirage Oasis",
        "description": "An oasis that seems to shimmer and shift. Is it real or illusion? Desperate travelers have died chasing mirages. But the water here seems real enough...",
        "location_type": "wilderness",
        "coordinates": [18, 0],
        "items": {"cactus_fruit": {"quantity": 2, "value": 8}},
        "exits": {
            "west": {"target": "sand_sea", "type": "direction"},
            "south": {"target": "serpent_canyon", "type": "direction"}
        }
    }
    
    rooms["serpent_canyon"] = {
        "id": "serpent_canyon",
        "name": "Serpent Canyon",
        "description": "A winding canyon with walls that twist like a serpent. Sand snakes are common here, lurking in crevices. Ancient pictographs cover the walls.",
        "location_type": "wilderness",
        "coordinates": [18, -2],
        "items": {"scorpion_tail": {"quantity": 2, "value": 12}},
        "exits": {
            "north": {"target": "mirage_oasis", "type": "direction"},
            "west": {"target": "ancient_pyramid", "type": "direction"}
        }
    }
    
    rooms["ancient_pyramid"] = {
        "id": "ancient_pyramid",
        "name": "Ancient Pyramid",
        "description": "A massive stone pyramid rises from the sands. Once a tomb for ancient rulers, now home to treasure seekers and worse. The entrance yawns darkly.",
        "location_type": "building",
        "coordinates": [16, -6],
        "items": {"dusty_tome": {"quantity": 1, "value": 35}, "golden_ring": {"quantity": 1, "value": 40}},
        "exits": {
            "north": {"target": "bleached_bones", "type": "direction"},
            "east": {"target": "serpent_canyon", "type": "direction"},
            "west": {"target": "sandstone_fortress", "type": "direction"}
        }
    }
    
    rooms["desert_temple"] = {
        "id": "desert_temple",
        "name": "Desert Temple",
        "description": "A temple dedicated to the sun god, half-buried in sand. Pillars still stand, casting long shadows. The altar within is said to grant visions.",
        "location_type": "building",
        "coordinates": [12, 2],
        "items": {"prayer_candle": {"quantity": 2, "value": 5}, "old_coin": {"quantity": 3, "value": 3}},
        "exits": {
            "south": {"target": "desert_dunes_west", "type": "direction"},
            "east": {"target": "hidden_oasis", "type": "direction"}
        }
    }
    
    rooms["nomad_camp"] = {
        "id": "nomad_camp",
        "name": "Nomad Camp",
        "description": "A camp of desert nomads with colorful tents. Camels rest nearby, and the smell of spiced food fills the air. The nomads are wary but not hostile.",
        "location_type": "settlement",
        "coordinates": [14, 4],
        "items": {},
        "exits": {
            "south": {"target": "hidden_oasis", "type": "direction"},
            "west": {"target": "canyon_entrance", "type": "direction"}
        }
    }
    
    rooms["dust_storm_plains"] = {
        "id": "dust_storm_plains",
        "name": "Dust Storm Plains",
        "description": "A flat area where dust storms are common. Visibility can drop to zero without warning. Travelers have been lost for days in these storms.",
        "location_type": "wilderness",
        "coordinates": [10, 2],
        "items": {},
        "exits": {
            "south": {"target": "desert_border", "type": "direction"},
            "east": {"target": "desert_temple", "type": "direction"}
        }
    }
    
    rooms["salt_flats"] = {
        "id": "salt_flats",
        "name": "Salt Flats",
        "description": "A vast expanse of white salt crusted earth. The sun reflects blindingly off the surface. Nothing grows here, but the salt itself has value.",
        "location_type": "wilderness",
        "coordinates": [18, -4],
        "items": {"smooth_pebble": {"quantity": 2, "value": 1}},
        "exits": {
            "north": {"target": "serpent_canyon", "type": "direction"},
            "west": {"target": "ancient_pyramid", "type": "direction"}
        }
    }
    
    rooms["caravan_waystation"] = {
        "id": "caravan_waystation",
        "name": "Caravan Waystation",
        "description": "A fortified rest stop for caravans crossing the desert. Wells provide water, and sturdy walls offer protection. Merchants often trade goods here.",
        "location_type": "settlement",
        "coordinates": [12, -6],
        "items": {"rope_coil": {"quantity": 1, "value": 20}},
        "exits": {
            "north": {"target": "scorpion_flats", "type": "direction"},
            "east": {"target": "sandstone_fortress", "type": "direction"},
            "west": {"target": "dusty_crossroads", "type": "direction"}
        }
    }
    
    # =========================================================================
    # ADDITIONAL TUNDRA/FROZEN AREAS - Far north expansion
    # =========================================================================
    
    rooms["blizzard_pass"] = {
        "id": "blizzard_pass",
        "name": "Blizzard Pass",
        "description": "A treacherous pass where blizzards rage constantly. Snow piles in deep drifts. Only the most determined or foolhardy push through.",
        "location_type": "wilderness",
        "coordinates": [4, 16],
        "items": {},
        "exits": {
            "west": {"target": "tundra_edge", "type": "direction"},
            "east": {"target": "frost_giant_territory", "type": "direction"},
            "south": {"target": "frozen_outpost", "type": "direction"}
        }
    }
    
    rooms["frost_giant_territory"] = {
        "id": "frost_giant_territory",
        "name": "Frost Giant Territory",
        "description": "Land claimed by frost giants. Enormous footprints mark the snow. Ruins of their crude structures dot the landscape. Best to be quiet here.",
        "location_type": "wilderness",
        "coordinates": [6, 16],
        "items": {"ice_crystal": {"quantity": 2, "value": 18}},
        "exits": {
            "west": {"target": "blizzard_pass", "type": "direction"},
            "south": {"target": "northern_lookout", "type": "direction"}
        }
    }
    
    rooms["aurora_viewing"] = {
        "id": "aurora_viewing",
        "name": "Aurora Watching Point",
        "description": "A clearing perfect for viewing the aurora borealis. The dancing lights paint the sky in greens and purples. Magic seems stronger here.",
        "location_type": "wilderness",
        "coordinates": [0, 20],
        "items": {"frost_flower": {"quantity": 2, "value": 20}},
        "exits": {
            "south": {"target": "ice_caves_entrance", "type": "direction"}
        }
    }
    
    rooms["frozen_waterfall"] = {
        "id": "frozen_waterfall",
        "name": "Frozen Waterfall",
        "description": "A massive waterfall frozen mid-flow. The ice formations are beautiful, like a sculpture made by nature. Behind the ice, a cave might be hidden.",
        "location_type": "wilderness",
        "coordinates": [-2, 14],
        "items": {"ice_crystal": {"quantity": 3, "value": 18}},
        "exits": {
            "south": {"target": "frozen_approach", "type": "direction"},
            "north": {"target": "ice_fields", "type": "direction"},
            "east": {"target": "tundra_edge", "type": "direction"}
        }
    }
    
    rooms["mammoth_graveyard"] = {
        "id": "mammoth_graveyard",
        "name": "Mammoth Graveyard",
        "description": "A place where ancient mammoths came to die. Enormous tusks and bones protrude from the snow. A somber, eerie place.",
        "location_type": "wilderness",
        "coordinates": [4, 18],
        "items": {"old_bone": {"quantity": 4, "value": 2}},
        "exits": {
            "south": {"target": "blizzard_pass", "type": "direction"},
            "west": {"target": "frozen_lake", "type": "direction"}
        }
    }
    
    rooms["ice_fishing_hole"] = {
        "id": "ice_fishing_hole",
        "name": "Ice Fishing Hole",
        "description": "A spot where a hole has been cut in the ice for fishing. Someone left equipment behind. Cold work, but the fish here are prized.",
        "location_type": "wilderness",
        "coordinates": [4, 20],
        "items": {"frozen_fish": {"quantity": 3, "value": 10}, "old_fishing_rod": {"quantity": 1, "value": 15}},
        "exits": {
            "south": {"target": "mammoth_graveyard", "type": "direction"},
            "west": {"target": "aurora_viewing", "type": "direction"}
        }
    }
    
    # =========================================================================
    # ADDITIONAL COASTAL/OCEAN AREAS - South expansion
    # =========================================================================
    
    rooms["shipwreck_beach"] = {
        "id": "shipwreck_beach",
        "name": "Shipwreck Beach",
        "description": "The skeletal remains of a ship lie on this beach. The hull is broken, and debris is scattered across the sand. What secrets does it hold?",
        "location_type": "wilderness",
        "coordinates": [-4, -10],
        "items": {"driftwood": {"quantity": 4, "value": 3}, "rope_coil": {"quantity": 1, "value": 20}},
        "exits": {
            "east": {"target": "tidal_caves", "type": "direction"},
            "north": {"target": "rocky_shore", "type": "direction"},
            "south": {"target": "pirates_cove", "type": "direction"}
        }
    }
    
    rooms["pirates_cove"] = {
        "id": "pirates_cove",
        "name": "Pirate's Cove",
        "description": "A hidden cove once used by pirates. X marks on rocks hint at buried treasure. The locals avoid this place, but treasure hunters come regularly.",
        "location_type": "wilderness",
        "coordinates": [-4, -12],
        "items": {"gold_coin": {"quantity": 5, "value": 2}, "rusty_key": {"quantity": 1, "value": 5}},
        "exits": {
            "north": {"target": "shipwreck_beach", "type": "direction"},
            "east": {"target": "reef_shallows", "type": "direction"}
        }
    }
    
    rooms["fishing_village"] = {
        "id": "fishing_village",
        "name": "Fishing Village",
        "description": "A small coastal village where everyone fishes. Nets dry on racks, and the smell of fish is everywhere. Simple folk living simple lives.",
        "location_type": "settlement",
        "coordinates": [6, -12],
        "items": {"fishing_net": {"quantity": 1, "value": 15}},
        "exits": {
            "north": {"target": "dungeon_ruins_entrance", "type": "direction"},
            "west": {"target": "smugglers_cove", "type": "direction"}
        }
    }
    
    rooms["coral_reef"] = {
        "id": "coral_reef",
        "name": "Coral Reef Shallows",
        "description": "Crystal clear water over a vibrant coral reef. Colorful fish dart between the coral formations. The reef extends far into the sea.",
        "location_type": "wilderness",
        "coordinates": [2, -14],
        "items": {"coral_piece": {"quantity": 3, "value": 12}, "seashell": {"quantity": 5, "value": 4}},
        "exits": {
            "north": {"target": "smugglers_cove", "type": "direction"},
            "east": {"target": "fishing_village", "type": "direction"}
        }
    }
    
    rooms["tide_pools"] = {
        "id": "tide_pools",
        "name": "Tide Pools",
        "description": "Pools left behind by the retreating tide. Starfish, anemones, and small crabs can be found. Children love to explore here.",
        "location_type": "wilderness",
        "coordinates": [-2, -12],
        "items": {"seaweed": {"quantity": 4, "value": 2}},
        "exits": {
            "north": {"target": "tidal_caves", "type": "direction"},
            "east": {"target": "reef_shallows", "type": "direction"},
            "west": {"target": "pirates_cove", "type": "direction"}
        }
    }
    
    rooms["sea_cave"] = {
        "id": "sea_cave",
        "name": "Sea Cave",
        "description": "A cave accessible only at low tide. The walls are covered in barnacles and sea life. Strange echoes come from deep within.",
        "location_type": "building",
        "coordinates": [-4, -14],
        "items": {"pearl": {"quantity": 1, "value": 35}, "seaweed": {"quantity": 2, "value": 2}},
        "exits": {
            "north": {"target": "pirates_cove", "type": "direction"}
        }
    }
    
    rooms["cliffside_overlook"] = {
        "id": "cliffside_overlook",
        "name": "Cliffside Overlook",
        "description": "A dramatic viewpoint high above the sea. Seabirds nest on the cliff face below. The sunset view from here is renowned.",
        "location_type": "wilderness",
        "coordinates": [4, -8],
        "items": {"eagle_feather": {"quantity": 1, "value": 35}},
        "exits": {
            "west": {"target": "lighthouse_hill", "type": "direction"},
            "south": {"target": "port_haven_north", "type": "direction"}
        }
    }
    
    rooms["kelp_forest"] = {
        "id": "kelp_forest",
        "name": "Kelp Forest Shallows",
        "description": "A underwater forest of giant kelp in the shallows. The fronds sway with the currents. Many fish hide among the kelp.",
        "location_type": "wilderness",
        "coordinates": [4, -12],
        "items": {"seaweed": {"quantity": 5, "value": 2}},
        "exits": {
            "west": {"target": "port_haven_docks", "type": "direction"},
            "north": {"target": "cliffside_overlook", "type": "direction"},
            "south": {"target": "coral_reef", "type": "direction"}
        }
    }
    
    # =========================================================================
    # ADDITIONAL SWAMP AREAS - Southwest expansion
    # =========================================================================
    
    rooms["corpse_grove"] = {
        "id": "corpse_grove",
        "name": "Corpse Grove",
        "description": "A grove of dead trees standing in stagnant water. Moss hangs like funeral shrouds. The locals say restless spirits haunt this place.",
        "location_type": "wilderness",
        "coordinates": [-7, -8],
        "items": {"old_bone": {"quantity": 2, "value": 2}, "glowing_moss": {"quantity": 1, "value": 8}},
        "exits": {
            "east": {"target": "deep_swamp", "type": "direction"},
            "north": {"target": "witch_hut", "type": "direction"},
            "south": {"target": "will_o_wisp_bog", "type": "direction"}
        }
    }
    
    rooms["will_o_wisp_bog"] = {
        "id": "will_o_wisp_bog",
        "name": "Will-o'-Wisp Bog",
        "description": "Strange lights dance over this treacherous bog. Following them leads only to quicksand. Many have drowned here, lured by the lights.",
        "location_type": "wilderness",
        "coordinates": [-7, -10],
        "items": {},
        "exits": {
            "north": {"target": "corpse_grove", "type": "direction"},
            "east": {"target": "graveyard", "type": "direction"}
        }
    }
    
    rooms["quicksand_marsh"] = {
        "id": "quicksand_marsh",
        "name": "Quicksand Marsh",
        "description": "A deceptively solid-looking marsh with hidden quicksand. Test each step carefully. Many an unwary traveler has sunk beneath the surface.",
        "location_type": "wilderness",
        "coordinates": [-5, -10],
        "items": {},
        "exits": {
            "north": {"target": "deep_swamp", "type": "direction"},
            "west": {"target": "will_o_wisp_bog", "type": "direction"},
            "east": {"target": "graveyard_gates", "type": "direction"}
        }
    }
    
    rooms["swamp_village"] = {
        "id": "swamp_village",
        "name": "Frogmorton Village",
        "description": "A village of stilt houses built over the swamp. The locals are reclusive and suspicious of outsiders. They know the swamp's secrets.",
        "location_type": "settlement",
        "coordinates": [-9, -6],
        "items": {},
        "exits": {
            "east": {"target": "sunken_ruins", "type": "direction"},
            "south": {"target": "crocodile_bog", "type": "direction"}
        }
    }
    
    rooms["crocodile_bog"] = {
        "id": "crocodile_bog",
        "name": "Crocodile Bog",
        "description": "A stretch of swamp infested with crocodiles. Their eyes watch from the murky water. Crossing requires extreme caution.",
        "location_type": "wilderness",
        "coordinates": [-9, -8],
        "items": {"leather_scrap": {"quantity": 2, "value": 6}},
        "exits": {
            "north": {"target": "swamp_village", "type": "direction"},
            "east": {"target": "corpse_grove", "type": "direction"}
        }
    }
    
    rooms["giant_lily_pads"] = {
        "id": "giant_lily_pads",
        "name": "Giant Lily Pad Crossing",
        "description": "Enormous lily pads float on the water here, large enough to stand on. Careful leaping can get you across without swimming.",
        "location_type": "wilderness",
        "coordinates": [-3, -12],
        "items": {"marsh_lily": {"quantity": 3, "value": 12}},
        "exits": {
            "north": {"target": "graveyard", "type": "direction"},
            "west": {"target": "will_o_wisp_bog", "type": "direction"}
        }
    }
    
    rooms["drowned_temple"] = {
        "id": "drowned_temple",
        "name": "Drowned Temple",
        "description": "An ancient temple half-submerged in the swamp. Water laps at the entrance. Who knows what lies in the flooded chambers below?",
        "location_type": "building",
        "coordinates": [-7, -12],
        "items": {"dusty_tome": {"quantity": 1, "value": 35}, "old_coin": {"quantity": 2, "value": 3}},
        "exits": {
            "east": {"target": "giant_lily_pads", "type": "direction"},
            "north": {"target": "will_o_wisp_bog", "type": "direction"}
        }
    }
    
    # =========================================================================
    # ADDITIONAL FARMLAND/PLAINS AREAS - Central expansion
    # =========================================================================
    
    rooms["corn_maze"] = {
        "id": "corn_maze",
        "name": "Corn Maze",
        "description": "Tall corn stalks form a natural maze. In autumn, villagers create paths for festivals. But some say things lurk in the corn year-round.",
        "location_type": "wilderness",
        "coordinates": [5, 0],
        "items": {"wheat_bundle": {"quantity": 2, "value": 3}},
        "exits": {
            "west": {"target": "farmland_west", "type": "direction"},
            "east": {"target": "farmland_center", "type": "direction"}
        }
    }
    
    rooms["scarecrow_field"] = {
        "id": "scarecrow_field",
        "name": "Scarecrow Field",
        "description": "A field guarded by an army of scarecrows. Their blank faces stare eternally. At night, some swear they move...",
        "location_type": "wilderness",
        "coordinates": [7, 0],
        "items": {"stick": {"quantity": 2, "value": 1}},
        "exits": {
            "west": {"target": "farmland_center", "type": "direction"},
            "east": {"target": "farmland_east", "type": "direction"}
        }
    }
    
    rooms["bee_meadow"] = {
        "id": "bee_meadow",
        "name": "Bee Meadow",
        "description": "A meadow buzzing with bees. Wildflowers of every color bloom here. The local beekeeper tends hives nearby. The honey is renowned.",
        "location_type": "wilderness",
        "coordinates": [3, 1],
        "items": {"wildflower": {"quantity": 6, "value": 2}},
        "exits": {
            "south": {"target": "farmland_west", "type": "direction"},
            "east": {"target": "shepherd_cottage", "type": "direction"}
        }
    }
    
    rooms["old_mill"] = {
        "id": "old_mill",
        "name": "Old Water Mill",
        "description": "An ancient water mill on a small stream. The wheel still turns, though no one mills grain here anymore. Moss covers the stones.",
        "location_type": "building",
        "coordinates": [5, -2],
        "items": {"wheat_bundle": {"quantity": 3, "value": 3}},
        "exits": {
            "north": {"target": "corn_maze", "type": "direction"},
            "east": {"target": "farmland_south", "type": "direction"}
        }
    }
    
    rooms["pasture_lands"] = {
        "id": "pasture_lands",
        "name": "Pasture Lands",
        "description": "Open grasslands where cattle graze lazily. Stone walls divide the pastures. Occasionally, a cowbell rings in the distance.",
        "location_type": "wilderness",
        "coordinates": [7, 2],
        "items": {},
        "exits": {
            "south": {"target": "scarecrow_field", "type": "direction"},
            "west": {"target": "farmland_north", "type": "direction"},
            "north": {"target": "highland_road", "type": "direction"}
        }
    }
    
    rooms["covered_bridge"] = {
        "id": "covered_bridge",
        "name": "Covered Bridge",
        "description": "An old wooden covered bridge spanning a small river. Travelers often rest here. Names and dates are carved into the timbers.",
        "location_type": "building",
        "coordinates": [3, -2],
        "items": {},
        "exits": {
            "north": {"target": "farmland_west", "type": "direction"},
            "south": {"target": "old_battlefield", "type": "direction"},
            "east": {"target": "old_mill", "type": "direction"}
        }
    }
    
    rooms["abandoned_farmhouse"] = {
        "id": "abandoned_farmhouse",
        "name": "Abandoned Farmhouse",
        "description": "A farmhouse abandoned years ago. Windows are broken, doors hang open. Rumor says the family left suddenly, leaving everything behind.",
        "location_type": "building",
        "coordinates": [8, 2],
        "items": {"rusty_key": {"quantity": 1, "value": 5}, "dusty_tome": {"quantity": 1, "value": 35}},
        "exits": {
            "west": {"target": "pasture_lands", "type": "direction"},
            "south": {"target": "farmland_east", "type": "direction"}
        }
    }
    
    rooms["rolling_hills"] = {
        "id": "rolling_hills",
        "name": "Rolling Hills",
        "description": "Gentle hills covered in grass that waves like the sea. The view stretches for miles. Hawks circle overhead hunting mice.",
        "location_type": "wilderness",
        "coordinates": [9, 0],
        "items": {},
        "exits": {
            "west": {"target": "farmland_east", "type": "direction"},
            "east": {"target": "desert_border", "type": "direction"},
            "north": {"target": "eastern_highlands", "type": "direction"}
        }
    }
    
    # =========================================================================
    # ADDITIONAL VILLAGE/SETTLEMENT AREAS - Around Havenbrook
    # =========================================================================
    
    rooms["market_alley"] = {
        "id": "market_alley",
        "name": "Market Alley",
        "description": "A narrow alley behind the market stalls. Discarded crates and boxes are piled here. Stray cats hunt for scraps.",
        "location_type": "settlement",
        "coordinates": [1, -1],
        "items": {"stick": {"quantity": 1, "value": 1}},
        "exits": {
            "west": {"target": "village_shop", "type": "direction"},
            "north": {"target": "well_square", "type": "direction"}
        }
    }
    
    rooms["well_square"] = {
        "id": "well_square",
        "name": "Well Square",
        "description": "A small square with an old stone well at the center. Women gather here to draw water and exchange gossip. A bucket hangs from a rope.",
        "location_type": "settlement",
        "coordinates": [1, 1],
        "items": {},
        "exits": {
            "south": {"target": "market_alley", "type": "direction"},
            "west": {"target": "village_square", "type": "direction"},
            "north": {"target": "village_training_grounds", "type": "direction"}
        }
    }
    
    rooms["apothecary"] = {
        "id": "apothecary",
        "name": "Apothecary Shop",
        "description": "A small shop filled with dried herbs, strange potions, and mysterious ingredients. The elderly apothecary knows remedies for almost any ailment.",
        "location_type": "building",
        "coordinates": [-1, -1],
        "items": {"strange_herb": {"quantity": 2, "value": 25}},
        "exits": {
            "outside": {"target": "village_tavern", "type": "direction"}
        }
    }
    
    rooms["village_graveyard"] = {
        "id": "village_graveyard",
        "name": "Village Graveyard",
        "description": "The village's own small graveyard behind the chapel. Well-tended graves of villagers past. Flowers are often placed on the headstones.",
        "location_type": "settlement",
        "coordinates": [3, -1],
        "items": {"wildflower": {"quantity": 2, "value": 2}},
        "exits": {
            "north": {"target": "chapel", "type": "direction"},
            "west": {"target": "village_east_end", "type": "direction"}
        }
    }
    
    rooms["baker_house"] = {
        "id": "baker_house",
        "name": "Baker's House",
        "description": "The home and shop of the village baker. The smell of fresh bread fills the air. Loaves cool on wooden racks.",
        "location_type": "building",
        "coordinates": [-1, 1],
        "items": {},
        "exits": {
            "outside": {"target": "village_gardens", "type": "direction"}
        }
    }
    
    rooms["village_stream"] = {
        "id": "village_stream",
        "name": "Village Stream",
        "description": "A clear stream flows past the village. Children play in the shallow water. Some villagers do their washing here.",
        "location_type": "settlement",
        "coordinates": [-3, -1],
        "items": {},
        "exits": {
            "east": {"target": "village_west_end", "type": "direction"},
            "south": {"target": "meadow", "type": "direction"}
        }
    }
    
    rooms["town_notice_board"] = {
        "id": "town_notice_board",
        "name": "Town Notice Board",
        "description": "A large wooden board where notices are posted. Job offerings, lost items, and official decrees can be found here. A small crowd often gathers to read.",
        "location_type": "settlement",
        "coordinates": [0, 1],
        "items": {},
        "exits": {
            "south": {"target": "village_square", "type": "direction"},
            "east": {"target": "well_square", "type": "direction"},
            "north": {"target": "village_north_gate", "type": "direction"}
        }
    }
    
    rooms["guild_hall"] = {
        "id": "guild_hall",
        "name": "Guild Hall",
        "description": "The hall where local guilds meet. Craftsmen display their best work here. Notices for apprenticeships are posted on the door.",
        "location_type": "building",
        "coordinates": [-1, 2],
        "items": {"iron_ingot": {"quantity": 1, "value": 20}},
        "exits": {
            "outside": {"target": "village_north_gate", "type": "direction"}
        }
    }
    
    # =========================================================================
    # ROAD/PATH CONNECTIONS - Added for better navigation
    # =========================================================================
    
    rooms["winding_path"] = {
        "id": "winding_path",
        "name": "Winding Path",
        "description": "A path that winds through light woodland. Birds sing in the trees, and wildflowers line the way. A peaceful route between destinations.",
        "location_type": "wilderness",
        "coordinates": [-4, 2],
        "items": {"wildflower": {"quantity": 2, "value": 2}},
        "exits": {
            "east": {"target": "orchard", "type": "direction"},
            "west": {"target": "forest_clearing", "type": "direction"},
            "south": {"target": "forest_edge", "type": "direction"}
        }
    }
    
    rooms["trade_road_north"] = {
        "id": "trade_road_north",
        "name": "Northern Trade Road",
        "description": "A wide road used by merchants traveling to and from the mountains. Wagon ruts are deep in the dirt. Mile markers guide the way.",
        "location_type": "wilderness",
        "coordinates": [2, 4],
        "items": {},
        "exits": {
            "south": {"target": "stables", "type": "direction"},
            "north": {"target": "rocky_valley", "type": "direction"},
            "west": {"target": "northern_road", "type": "direction"}
        }
    }
    
    rooms["southern_highway"] = {
        "id": "southern_highway",
        "name": "Southern Highway",
        "description": "The main road south to Port Haven. Well-maintained and frequently patrolled. Inns are spaced along the route for travelers.",
        "location_type": "wilderness",
        "coordinates": [2, -4],
        "items": {},
        "exits": {
            "north": {"target": "village_south_road", "type": "direction"},
            "south": {"target": "coastal_road_north", "type": "direction"},
            "east": {"target": "eastern_road", "type": "direction"},
            "west": {"target": "crossroads", "type": "direction"}
        }
    }
    
    rooms["forest_road"] = {
        "id": "forest_road",
        "name": "Forest Road",
        "description": "A road that skirts the edge of Elderwood Forest. Travelers move quickly here, wary of what might emerge from the trees.",
        "location_type": "wilderness",
        "coordinates": [-4, -2],
        "items": {},
        "exits": {
            "north": {"target": "forest_edge", "type": "direction"},
            "south": {"target": "swamp_trail", "type": "direction"},
            "east": {"target": "village_west_end", "type": "direction"},
            "west": {"target": "forest_path", "type": "direction"}
        }
    }
    
    rooms["mountain_road"] = {
        "id": "mountain_road",
        "name": "Mountain Road",
        "description": "A road climbing into the Stormspire Mountains. The grade is steep, and the air grows thinner. Snow appears earlier here than in the lowlands.",
        "location_type": "wilderness",
        "coordinates": [2, 8],
        "items": {},
        "exits": {
            "south": {"target": "trade_road_north", "type": "direction"},
            "north": {"target": "dungeon_mountain_entrance", "type": "direction"},
            "west": {"target": "mountain_path", "type": "direction"},
            "east": {"target": "highland_pass", "type": "direction"}
        }
    }
    
    # =========================================================================
    # HAUNTED RUINS - Scattered mysterious locations
    # =========================================================================
    
    rooms["haunted_manor"] = {
        "id": "haunted_manor",
        "name": "Haunted Manor",
        "description": "A decrepit manor on a hill, its windows like dark eyes. Strange lights flicker within at night. The locals avoid this place.",
        "location_type": "building",
        "coordinates": [-6, -8],
        "items": {"dusty_tome": {"quantity": 1, "value": 35}, "golden_ring": {"quantity": 1, "value": 40}},
        "exits": {
            "outside": {"target": "graveyard_road", "type": "direction"}
        }
    }
    
    rooms["collapsed_tower"] = {
        "id": "collapsed_tower",
        "name": "Collapsed Wizard's Tower",
        "description": "The ruins of a wizard's tower, collapsed during some magical catastrophe. Strange energies still linger. Broken artifacts are scattered about.",
        "location_type": "building",
        "coordinates": [-11, 4],
        "items": {"cave_crystal": {"quantity": 2, "value": 22}, "intact_tome": {"quantity": 1, "value": 45}},
        "exits": {
            "east": {"target": "hunter_camp", "type": "direction"}
        }
    }
    
    rooms["standing_stones"] = {
        "id": "standing_stones",
        "name": "Standing Stones",
        "description": "A circle of ancient standing stones on a windswept hill. Druids once performed rituals here. The stones hum with residual power.",
        "location_type": "wilderness",
        "coordinates": [-6, 6],
        "items": {"smooth_stone": {"quantity": 3, "value": 8}},
        "exits": {
            "south": {"target": "fairy_ring", "type": "direction"},
            "east": {"target": "windmill_hill", "type": "direction"}
        }
    }
    
    rooms["ruined_shrine"] = {
        "id": "ruined_shrine",
        "name": "Ruined Roadside Shrine",
        "description": "A small shrine to forgotten gods, now in ruins. Travelers once left offerings here for safe journeys. The statue is weathered beyond recognition.",
        "location_type": "building",
        "coordinates": [3, 6],
        "items": {"old_coin": {"quantity": 2, "value": 3}},
        "exits": {
            "south": {"target": "highland_road", "type": "direction"},
            "north": {"target": "rocky_valley", "type": "direction"}
        }
    }
    
    rooms["old_watchtower"] = {
        "id": "old_watchtower",
        "name": "Old Watchtower",
        "description": "A crumbling watchtower from a long-forgotten war. The stairs are dangerous, but the view from the top is excellent.",
        "location_type": "building",
        "coordinates": [-1, -6],
        "items": {"broken_arrow": {"quantity": 4, "value": 2}},
        "exits": {
            "north": {"target": "crossroads", "type": "direction"},
            "south": {"target": "coastal_road_north", "type": "direction"}
        }
    }
    
    # =========================================================================
    # WILDERNESS CAVES - Throughout the world
    # =========================================================================
    
    rooms["bear_cave"] = {
        "id": "bear_cave",
        "name": "Bear Cave",
        "description": "A large cave that serves as a bear's den. Fresh scratches on the entrance suggest recent activity. Bones and berry remnants litter the floor.",
        "location_type": "building",
        "coordinates": [-9, 6],
        "items": {"wolf_pelt": {"quantity": 1, "value": 18}, "raw_meat": {"quantity": 2, "value": 8}},
        "exits": {
            "outside": {"target": "hunter_camp", "type": "direction"}
        }
    }
    
    rooms["bat_cavern"] = {
        "id": "bat_cavern",
        "name": "Bat Cavern",
        "description": "A cavern filled with thousands of bats. Their droppings carpet the floor. The sound of their wings is deafening when disturbed.",
        "location_type": "building",
        "coordinates": [3, 10],
        "items": {"glowing_moss": {"quantity": 2, "value": 8}},
        "exits": {
            "outside": {"target": "high_pass", "type": "direction"}
        }
    }
    
    rooms["crystal_grotto"] = {
        "id": "crystal_grotto",
        "name": "Crystal Grotto",
        "description": "A small cave filled with natural crystal formations. Light refracts beautifully through the crystals, creating rainbows on the walls.",
        "location_type": "building",
        "coordinates": [-4, 6],
        "items": {"cave_crystal": {"quantity": 3, "value": 22}},
        "exits": {
            "outside": {"target": "mountain_stream", "type": "direction"}
        }
    }
    
    rooms["goblin_warren"] = {
        "id": "goblin_warren",
        "name": "Goblin Warren",
        "description": "A network of small tunnels that once housed goblins. Refuse and crude belongings are scattered about. The goblins seem to have moved on.",
        "location_type": "building",
        "coordinates": [-7, 0],
        "items": {"rusty_sword": {"quantity": 2, "value": 12}, "old_coin": {"quantity": 4, "value": 3}},
        "exits": {
            "outside": {"target": "deep_forest", "type": "direction"}
        }
    }
    
    rooms["spider_nest"] = {
        "id": "spider_nest",
        "name": "Spider Nest",
        "description": "A cave choked with thick webs. Large spiders lurk in the shadows. Wrapped cocoons hang from the ceiling - some are disturbingly human-sized.",
        "location_type": "building",
        "coordinates": [-11, -4],
        "items": {"rope_coil": {"quantity": 1, "value": 20}},
        "exits": {
            "outside": {"target": "tangled_thicket", "type": "direction"}
        }
    }
    
    # =========================================================================
    # SCENIC/REST AREAS - Points of interest
    # =========================================================================
    
    rooms["sunset_point"] = {
        "id": "sunset_point",
        "name": "Sunset Point",
        "description": "A beautiful overlook perfect for watching the sunset. Lovers often come here. Someone has carved a heart into a nearby tree.",
        "location_type": "wilderness",
        "coordinates": [-5, 0],
        "items": {"wildflower": {"quantity": 3, "value": 2}},
        "exits": {
            "east": {"target": "forest_edge", "type": "direction"},
            "west": {"target": "forest_path", "type": "direction"}
        }
    }
    
    rooms["meditation_rock"] = {
        "id": "meditation_rock",
        "name": "Meditation Rock",
        "description": "A large flat rock by a babbling stream. Someone has worn a smooth spot from years of sitting. The atmosphere is peaceful.",
        "location_type": "wilderness",
        "coordinates": [1, 6],
        "items": {"smooth_pebble": {"quantity": 5, "value": 1}},
        "exits": {
            "south": {"target": "mountain_foothills", "type": "direction"},
            "west": {"target": "waterfall_base", "type": "direction"}
        }
    }
    
    rooms["picnic_clearing"] = {
        "id": "picnic_clearing",
        "name": "Picnic Clearing",
        "description": "A lovely clearing where villagers come for picnics. Flat rocks serve as natural tables. Wildflowers bloom in profusion.",
        "location_type": "wilderness",
        "coordinates": [-2, 2],
        "items": {"wildflower": {"quantity": 4, "value": 2}},
        "exits": {
            "south": {"target": "village_gardens", "type": "direction"},
            "east": {"target": "northern_road", "type": "direction"}
        }
    }
    
    rooms["fishermans_rest"] = {
        "id": "fishermans_rest",
        "name": "Fisherman's Rest",
        "description": "A quiet spot by the river where fishermen come to relax. A wooden bench overlooks a deep pool. Fish jump occasionally.",
        "location_type": "wilderness",
        "coordinates": [4, -6],
        "items": {"old_fishing_rod": {"quantity": 1, "value": 15}},
        "exits": {
            "north": {"target": "farmland_south", "type": "direction"},
            "south": {"target": "coastal_road_east", "type": "direction"}
        }
    }
    
    rooms["stargazer_hill"] = {
        "id": "stargazer_hill",
        "name": "Stargazer's Hill",
        "description": "A hill away from village lights, perfect for stargazing. An old astronomer's shack sits at the top, mostly collapsed now.",
        "location_type": "wilderness",
        "coordinates": [5, 4],
        "items": {"faded_map": {"quantity": 1, "value": 20}},
        "exits": {
            "south": {"target": "pasture_lands", "type": "direction"},
            "west": {"target": "highland_road", "type": "direction"}
        }
    }
    
    # =========================================================================
    # ADDITIONAL DESERT OUTPOSTS
    # =========================================================================
    
    rooms["desert_well"] = {
        "id": "desert_well",
        "name": "Desert Well",
        "description": "An ancient well in the desert, still providing precious water. Travelers leave offerings of thanks. The stone is worn smooth by countless hands.",
        "location_type": "wilderness",
        "coordinates": [11, -2],
        "items": {},
        "exits": {
            "north": {"target": "desert_dunes_west", "type": "direction"},
            "south": {"target": "caravan_waystation", "type": "direction"},
            "east": {"target": "scorpion_flats", "type": "direction"}
        }
    }
    
    rooms["vulture_roost"] = {
        "id": "vulture_roost",
        "name": "Vulture Roost",
        "description": "A rocky outcropping where vultures gather. The birds circle overhead, waiting. A grim reminder of the desert's dangers.",
        "location_type": "wilderness",
        "coordinates": [15, -2],
        "items": {"old_bone": {"quantity": 3, "value": 2}},
        "exits": {
            "west": {"target": "mesa_base", "type": "direction"},
            "east": {"target": "bleached_bones", "type": "direction"}
        }
    }
    
    rooms["sand_whirlpool"] = {
        "id": "sand_whirlpool",
        "name": "Sand Whirlpool",
        "description": "A strange phenomenon - a permanent whirlpool in the sand. It's said to be caused by air currents from caves below. Getting too close would be fatal.",
        "location_type": "wilderness",
        "coordinates": [13, 2],
        "items": {},
        "exits": {
            "west": {"target": "desert_temple", "type": "direction"},
            "south": {"target": "desert_dunes_center", "type": "direction"},
            "east": {"target": "nomad_camp", "type": "direction"}
        }
    }
    
    rooms["ancient_obelisk"] = {
        "id": "ancient_obelisk",
        "name": "Ancient Obelisk",
        "description": "A tall stone obelisk covered in hieroglyphics. It marks the boundary of an ancient kingdom long since fallen. The writing is indecipherable.",
        "location_type": "wilderness",
        "coordinates": [17, 2],
        "items": {"ancient_brick": {"quantity": 1, "value": 10}},
        "exits": {
            "south": {"target": "sand_sea", "type": "direction"},
            "west": {"target": "nomad_camp", "type": "direction"}
        }
    }
    
    rooms["djinn_temple"] = {
        "id": "djinn_temple",
        "name": "Temple of the Djinn",
        "description": "A temple dedicated to the spirits of the air. Sand constantly swirls around it in patterns that seem almost alive. Strange whispers can be heard.",
        "location_type": "building",
        "coordinates": [18, 2],
        "items": {"prayer_candle": {"quantity": 3, "value": 5}, "silver_ring": {"quantity": 1, "value": 10}},
        "exits": {
            "west": {"target": "ancient_obelisk", "type": "direction"}
        }
    }
    
    # =========================================================================
    # ADDITIONAL TUNDRA LOCATIONS
    # =========================================================================
    
    rooms["polar_bear_territory"] = {
        "id": "polar_bear_territory",
        "name": "Polar Bear Territory",
        "description": "An area frequented by polar bears. Massive paw prints mark the snow. Best to keep moving and stay alert.",
        "location_type": "wilderness",
        "coordinates": [-2, 16],
        "items": {"raw_meat": {"quantity": 1, "value": 8}},
        "exits": {
            "east": {"target": "ice_fields", "type": "direction"},
            "south": {"target": "frozen_waterfall", "type": "direction"}
        }
    }
    
    rooms["seal_colony"] = {
        "id": "seal_colony",
        "name": "Seal Colony",
        "description": "A stretch of frozen coast where seals gather. They bark and splash in the icy water. The locals come here to hunt, though carefully.",
        "location_type": "wilderness",
        "coordinates": [-4, 18],
        "items": {"raw_meat": {"quantity": 2, "value": 8}},
        "exits": {
            "east": {"target": "ice_caves_entrance", "type": "direction"},
            "south": {"target": "polar_bear_territory", "type": "direction"}
        }
    }
    
    rooms["snow_shrine"] = {
        "id": "snow_shrine",
        "name": "Snow Shrine",
        "description": "A shrine carved entirely from ice. It never melts despite the seasons. Offerings left here freeze instantly. A place of cold magic.",
        "location_type": "building",
        "coordinates": [6, 18],
        "items": {"ice_crystal": {"quantity": 2, "value": 18}},
        "exits": {
            "west": {"target": "mammoth_graveyard", "type": "direction"},
            "south": {"target": "frost_giant_territory", "type": "direction"}
        }
    }
    
    rooms["wind_carved_spires"] = {
        "id": "wind_carved_spires",
        "name": "Wind-Carved Ice Spires",
        "description": "Tall spires of ice sculpted by eternal winds. They sing in the gales, creating an eerie melody. An artist's dream, a traveler's nightmare.",
        "location_type": "wilderness",
        "coordinates": [-4, 20],
        "items": {"frost_flower": {"quantity": 1, "value": 20}},
        "exits": {
            "east": {"target": "aurora_viewing", "type": "direction"},
            "south": {"target": "seal_colony", "type": "direction"}
        }
    }
    
    rooms["frozen_battlefield"] = {
        "id": "frozen_battlefield",
        "name": "Frozen Battlefield",
        "description": "An ancient battlefield preserved by the cold. Frozen warriors still stand in combat poses. Their weapons and armor remain, though touching them feels wrong.",
        "location_type": "wilderness",
        "coordinates": [6, 14],
        "items": {"broken_shield": {"quantity": 2, "value": 8}, "rusty_sword": {"quantity": 1, "value": 12}},
        "exits": {
            "south": {"target": "frozen_outpost", "type": "direction"},
            "north": {"target": "frost_giant_territory", "type": "direction"}
        }
    }
    
    # =========================================================================
    # ADDITIONAL COASTAL LOCATIONS
    # =========================================================================
    
    rooms["pelican_roost"] = {
        "id": "pelican_roost",
        "name": "Pelican Roost",
        "description": "A rocky area where pelicans nest. The birds are comically awkward on land but graceful in the air. Guano coats everything.",
        "location_type": "wilderness",
        "coordinates": [6, -10],
        "items": {"eagle_feather": {"quantity": 2, "value": 35}},
        "exits": {
            "west": {"target": "old_pier", "type": "direction"},
            "south": {"target": "fishing_village", "type": "direction"}
        }
    }
    
    rooms["underwater_cave_entrance"] = {
        "id": "underwater_cave_entrance",
        "name": "Underwater Cave Entrance",
        "description": "At low tide, a cave entrance is revealed. The cave floods at high tide, but treasures and mysteries are said to lie within.",
        "location_type": "wilderness",
        "coordinates": [0, -14],
        "items": {"seaweed": {"quantity": 3, "value": 2}},
        "exits": {
            "north": {"target": "reef_shallows", "type": "direction"},
            "west": {"target": "tide_pools", "type": "direction"}
        }
    }
    
    rooms["mermaid_rock"] = {
        "id": "mermaid_rock",
        "name": "Mermaid Rock",
        "description": "A large rock where sailors claim to have seen mermaids. Whether true or just wishful thinking, the rock is a local landmark.",
        "location_type": "wilderness",
        "coordinates": [6, -14],
        "items": {"seashell": {"quantity": 3, "value": 4}},
        "exits": {
            "north": {"target": "fishing_village", "type": "direction"},
            "west": {"target": "coral_reef", "type": "direction"}
        }
    }
    
    rooms["old_lighthouse"] = {
        "id": "old_lighthouse",
        "name": "Old Lighthouse (Ruined)",
        "description": "An abandoned lighthouse, its light long extinguished. The stairs are dangerous, but explorers still come seeking rumored treasure.",
        "location_type": "building",
        "coordinates": [-6, -10],
        "items": {"torch": {"quantity": 2, "value": 5}, "faded_map": {"quantity": 1, "value": 20}},
        "exits": {
            "east": {"target": "shipwreck_beach", "type": "direction"}
        }
    }
    
    rooms["shrimp_boats"] = {
        "id": "shrimp_boats",
        "name": "Shrimp Boat Dock",
        "description": "A small dock where shrimp boats tie up. Nets hang to dry, and the catch is sorted on the pier. Fresh shrimp can be bought here.",
        "location_type": "settlement",
        "coordinates": [5, -8],
        "items": {"fishing_net": {"quantity": 1, "value": 15}},
        "exits": {
            "west": {"target": "cliffside_overlook", "type": "direction"},
            "south": {"target": "port_haven_north", "type": "direction"}
        }
    }
    
    # =========================================================================
    # ADDITIONAL SWAMP LOCATIONS
    # =========================================================================
    
    rooms["leech_pond"] = {
        "id": "leech_pond",
        "name": "Leech Pond",
        "description": "A stagnant pond infested with leeches. Crossing requires wading through, and the leeches will find you. Villagers gather them for medicine.",
        "location_type": "wilderness",
        "coordinates": [-9, -10],
        "items": {},
        "exits": {
            "north": {"target": "crocodile_bog", "type": "direction"},
            "east": {"target": "will_o_wisp_bog", "type": "direction"}
        }
    }
    
    rooms["hermit_swamp_shack"] = {
        "id": "hermit_swamp_shack",
        "name": "Swamp Hermit's Shack",
        "description": "Another hermit's home, this one in the swamp. The owner is even more eccentric than most, speaking to the frogs as if they understand.",
        "location_type": "building",
        "coordinates": [-8, -10],
        "items": {"strange_herb": {"quantity": 2, "value": 25}},
        "exits": {
            "east": {"target": "leech_pond", "type": "direction"},
            "north": {"target": "corpse_grove", "type": "direction"}
        }
    }
    
    rooms["ancient_cypress"] = {
        "id": "ancient_cypress",
        "name": "Ancient Cypress",
        "description": "A massive cypress tree, thousands of years old. Its roots create a maze above the water. Carvings on its trunk suggest it was once sacred.",
        "location_type": "wilderness",
        "coordinates": [-4, -8],
        "items": {"ancient_acorn": {"quantity": 1, "value": 50}},
        "exits": {
            "north": {"target": "foggy_marsh", "type": "direction"},
            "south": {"target": "quicksand_marsh", "type": "direction"},
            "west": {"target": "deep_swamp", "type": "direction"}
        }
    }
    
    rooms["frog_chorus"] = {
        "id": "frog_chorus",
        "name": "Frog Chorus Pool",
        "description": "A pool where hundreds of frogs gather. Their evening chorus is deafening. The locals say the frogs predict the weather.",
        "location_type": "wilderness",
        "coordinates": [-6, -4],
        "items": {"marsh_lily": {"quantity": 2, "value": 12}},
        "exits": {
            "east": {"target": "swamp_trail", "type": "direction"},
            "south": {"target": "witch_hut", "type": "direction"},
            "north": {"target": "forest_swamp_border", "type": "direction"}
        }
    }
    
    # =========================================================================
    # ADDITIONAL CASTLE/SETTLEMENT LOCATIONS
    # =========================================================================
    
    rooms["castle_dungeon"] = {
        "id": "castle_dungeon",
        "name": "Castle Dungeon",
        "description": "The dungeons beneath Kingshold Castle. Thankfully empty of prisoners. Iron shackles hang from the walls, and old straw covers the floor.",
        "location_type": "building",
        "coordinates": [10, 9],
        "items": {"rusty_key": {"quantity": 1, "value": 5}, "old_bone": {"quantity": 2, "value": 2}},
        "exits": {
            "up": {"target": "castle_hall", "type": "direction"}
        }
    }
    
    rooms["castle_library"] = {
        "id": "castle_library",
        "name": "Castle Library",
        "description": "The royal library, filled with books and scrolls. Knowledge from across the realm is preserved here. Scholars study in quiet alcoves.",
        "location_type": "building",
        "coordinates": [11, 10],
        "items": {"dusty_tome": {"quantity": 2, "value": 35}, "intact_tome": {"quantity": 1, "value": 45}},
        "exits": {
            "west": {"target": "castle_hall", "type": "direction"}
        }
    }
    
    rooms["castle_armory"] = {
        "id": "castle_armory",
        "name": "Castle Armory",
        "description": "The castle's armory, where weapons and armor are stored. Rows of swords, shields, and suits of armor line the walls. Guards patrol regularly.",
        "location_type": "building",
        "coordinates": [9, 12],
        "items": {"iron_ingot": {"quantity": 2, "value": 20}},
        "exits": {
            "south": {"target": "castle_barracks", "type": "direction"}
        }
    }
    
    rooms["royal_stables"] = {
        "id": "royal_stables",
        "name": "Royal Stables",
        "description": "Stables housing the finest horses in the realm. The royal steeds are pampered and well-trained. Grooms tend to them constantly.",
        "location_type": "building",
        "coordinates": [8, 11],
        "items": {"rope_coil": {"quantity": 1, "value": 20}},
        "exits": {
            "south": {"target": "castle_courtyard", "type": "direction"}
        }
    }
    
    rooms["castle_chapel"] = {
        "id": "castle_chapel",
        "name": "Castle Chapel",
        "description": "A beautiful chapel within the castle. Stained glass depicts holy scenes. Royalty have been married and buried here for generations.",
        "location_type": "building",
        "coordinates": [10, 12],
        "items": {"prayer_candle": {"quantity": 4, "value": 5}},
        "exits": {
            "south": {"target": "castle_hall", "type": "direction"}
        }
    }
    
    # =========================================================================
    # OUTLYING VILLAGES AND HAMLETS
    # =========================================================================
    
    rooms["mining_village"] = {
        "id": "mining_village",
        "name": "Ironvale Mining Village",
        "description": "A rough village that grew up around the mountain mines. Miners and their families live in sturdy stone houses. Life is hard but honest here.",
        "location_type": "settlement",
        "coordinates": [4, 7],
        "items": {"iron_ore": {"quantity": 1, "value": 15}},
        "exits": {
            "south": {"target": "highland_pass", "type": "direction"},
            "north": {"target": "mining_tunnels", "type": "direction"}
        }
    }
    
    rooms["logging_settlement"] = {
        "id": "logging_settlement",
        "name": "Timberfall Settlement",
        "description": "A small settlement of loggers at the forest's edge. The sound of axes and falling trees echoes constantly. Sawdust covers everything.",
        "location_type": "settlement",
        "coordinates": [-5, -3],
        "items": {"stick": {"quantity": 4, "value": 1}},
        "exits": {
            "north": {"target": "forest_edge", "type": "direction"},
            "east": {"target": "forest_road", "type": "direction"}
        }
    }
    
    rooms["roadside_inn"] = {
        "id": "roadside_inn",
        "name": "Crossroads Inn",
        "description": "A welcoming inn at the crossroads. Travelers rest here before continuing their journeys. The innkeeper is friendly and full of gossip.",
        "location_type": "building",
        "coordinates": [1, -5],
        "items": {"ale_mug": {"quantity": 2, "value": 3}},
        "exits": {
            "north": {"target": "crossroads", "type": "direction"}
        }
    }
    
    rooms["border_watchtower"] = {
        "id": "border_watchtower",
        "name": "Border Watchtower",
        "description": "A watchtower marking the border between civilized lands and wilderness. Guards keep watch for bandits and monsters.",
        "location_type": "building",
        "coordinates": [9, 4],
        "items": {"broken_arrow": {"quantity": 3, "value": 2}},
        "exits": {
            "west": {"target": "desert_cliffs", "type": "direction"},
            "north": {"target": "kingshold_approach", "type": "direction"}
        }
    }
    
    rooms["ferry_crossing"] = {
        "id": "ferry_crossing",
        "name": "River Ferry Crossing",
        "description": "A simple ferry crosses a wide river here. The ferryman charges a small fee. The crossing takes several minutes.",
        "location_type": "settlement",
        "coordinates": [7, -4],
        "items": {},
        "exits": {
            "west": {"target": "eastern_road", "type": "direction"},
            "east": {"target": "caravan_waystation", "type": "direction"}
        }
    }
    
    # =========================================================================
    # SPECIAL ENCOUNTER LOCATIONS
    # =========================================================================
    
    rooms["bandits_hideout"] = {
        "id": "bandits_hideout",
        "name": "Bandit's Hideout",
        "description": "A concealed camp used by bandits. Evidence of their crimes is everywhere - stolen goods, weapons, and makeshift barricades.",
        "location_type": "building",
        "coordinates": [-5, -5],
        "items": {"gold_coin": {"quantity": 8, "value": 2}, "rusty_sword": {"quantity": 1, "value": 12}},
        "exits": {
            "outside": {"target": "forest_south_edge", "type": "direction"}
        }
    }
    
    rooms["dragon_bones"] = {
        "id": "dragon_bones",
        "name": "Dragon Bones",
        "description": "The massive skeleton of an ancient dragon lies half-buried in the hillside. Whether it died of age or battle is unclear. The bones dwarf everything around them.",
        "location_type": "wilderness",
        "coordinates": [8, 6],
        "items": {"old_bone": {"quantity": 3, "value": 2}, "cave_crystal": {"quantity": 1, "value": 22}},
        "exits": {
            "west": {"target": "eastern_highlands", "type": "direction"},
            "south": {"target": "stargazer_hill", "type": "direction"}
        }
    }
    
    rooms["ancient_battlefield"] = {
        "id": "ancient_battlefield",
        "name": "Ancient Battlefield",
        "description": "An even older battlefield than the one near the village. Rusted siege weapons and shattered armor litter the ground. The spirits of the fallen are said to walk at night.",
        "location_type": "wilderness",
        "coordinates": [11, 2],
        "items": {"broken_shield": {"quantity": 2, "value": 8}, "rusty_sword": {"quantity": 1, "value": 12}},
        "exits": {
            "west": {"target": "dust_storm_plains", "type": "direction"},
            "south": {"target": "desert_dunes_west", "type": "direction"}
        }
    }
    
    rooms["meteor_crater"] = {
        "id": "meteor_crater",
        "name": "Meteor Crater",
        "description": "A massive crater where a meteor fell long ago. Strange metals can be found here. The locals believe the site is cursed - or blessed.",
        "location_type": "wilderness",
        "coordinates": [12, 6],
        "items": {"iron_ore": {"quantity": 2, "value": 15}, "cave_crystal": {"quantity": 1, "value": 22}},
        "exits": {
            "west": {"target": "dragon_bones", "type": "direction"},
            "south": {"target": "canyon_entrance", "type": "direction"}
        }
    }
    
    rooms["giant_mushroom_grove"] = {
        "id": "giant_mushroom_grove",
        "name": "Giant Mushroom Grove",
        "description": "A grove where mushrooms grow to enormous size. Some are as tall as trees. The air is thick with spores. Everything here is slightly... wrong.",
        "location_type": "wilderness",
        "coordinates": [-8, -4],
        "items": {"mushroom": {"quantity": 5, "value": 5}, "shelf_mushroom": {"quantity": 3, "value": 4}},
        "exits": {
            "north": {"target": "dark_hollow", "type": "direction"},
            "east": {"target": "frog_chorus", "type": "direction"}
        }
    }
    
    # =========================================================================
    # FINAL EXPANSION - Additional locations to reach 250+
    # =========================================================================
    
    rooms["forgotten_tomb"] = {
        "id": "forgotten_tomb",
        "name": "Forgotten Tomb",
        "description": "An ancient tomb hidden in the hills. The entrance was recently uncovered by erosion. Treasures and terrors likely await within.",
        "location_type": "building",
        "coordinates": [5, -4],
        "items": {"dusty_tome": {"quantity": 1, "value": 35}, "old_coin": {"quantity": 4, "value": 3}},
        "exits": {
            "outside": {"target": "eastern_road", "type": "direction"}
        }
    }
    
    rooms["hollow_tree"] = {
        "id": "hollow_tree",
        "name": "Hollow Tree",
        "description": "An enormous hollow tree that could shelter several people. Someone has lived here - a small fire pit and crude bed remain.",
        "location_type": "building",
        "coordinates": [-7, -2],
        "items": {"torch": {"quantity": 1, "value": 5}},
        "exits": {
            "outside": {"target": "deep_forest", "type": "direction"}
        }
    }
    
    rooms["abandoned_mine"] = {
        "id": "abandoned_mine",
        "name": "Abandoned Mine",
        "description": "An old mine shaft that was abandoned after a collapse. Dangerous, but rumored to still hold valuable ore in its depths.",
        "location_type": "building",
        "coordinates": [5, 8],
        "items": {"copper_ore": {"quantity": 3, "value": 10}, "iron_ore": {"quantity": 1, "value": 15}},
        "exits": {
            "outside": {"target": "mountain_road", "type": "direction"}
        }
    }
    
    rooms["smugglers_tunnel"] = {
        "id": "smugglers_tunnel",
        "name": "Smuggler's Tunnel",
        "description": "A secret tunnel used by smugglers to move contraband. Crates of illicit goods line the walls. The authorities haven't found this place yet.",
        "location_type": "building",
        "coordinates": [4, -11],
        "items": {"gold_coin": {"quantity": 6, "value": 2}, "rope_coil": {"quantity": 1, "value": 20}},
        "exits": {
            "north": {"target": "port_haven_docks", "type": "direction"},
            "south": {"target": "smugglers_cove", "type": "direction"}
        }
    }
    
    rooms["moonlit_glade"] = {
        "id": "moonlit_glade",
        "name": "Moonlit Glade",
        "description": "A perfectly circular clearing that seems to glow even on moonless nights. Flowers here bloom only after dark. A place of subtle magic.",
        "location_type": "wilderness",
        "coordinates": [-9, 0],
        "items": {"wildflower": {"quantity": 4, "value": 2}},
        "exits": {
            "east": {"target": "ancient_grove", "type": "direction"},
            "north": {"target": "hermit_cabin", "type": "direction"}
        }
    }
    
    rooms["thundering_falls"] = {
        "id": "thundering_falls",
        "name": "Thundering Falls",
        "description": "A massive waterfall whose roar can be heard for miles. Rainbow mist fills the air. A hidden path leads behind the falls.",
        "location_type": "wilderness",
        "coordinates": [-3, 10],
        "items": {"smooth_pebble": {"quantity": 4, "value": 1}},
        "exits": {
            "south": {"target": "goat_trail", "type": "direction"},
            "east": {"target": "hermit_peak", "type": "direction"}
        }
    }
    
    rooms["cursed_crossroads"] = {
        "id": "cursed_crossroads",
        "name": "Cursed Crossroads",
        "description": "A crossroads where hangings once took place. The gallows tree still stands, twisted and dead. Strange things happen here at midnight.",
        "location_type": "wilderness",
        "coordinates": [-2, -6],
        "items": {"old_rope": {"quantity": 1, "value": 6}},
        "exits": {
            "north": {"target": "graveyard_road", "type": "direction"},
            "east": {"target": "old_watchtower", "type": "direction"}
        }
    }
    
    rooms["herb_garden"] = {
        "id": "herb_garden",
        "name": "Wild Herb Garden",
        "description": "A natural garden where medicinal herbs grow wild. The witch and apothecary both gather here. The plants have unusual properties.",
        "location_type": "wilderness",
        "coordinates": [-6, -5],
        "items": {"strange_herb": {"quantity": 3, "value": 25}},
        "exits": {
            "south": {"target": "witch_hut", "type": "direction"},
            "north": {"target": "swamp_edge", "type": "direction"}
        }
    }
    
    rooms["echo_canyon"] = {
        "id": "echo_canyon",
        "name": "Echo Canyon",
        "description": "A narrow canyon where sound echoes endlessly. Shout and you'll hear your voice returning for minutes. Locals tell stories here to hear them multiply.",
        "location_type": "wilderness",
        "coordinates": [13, 6],
        "items": {},
        "exits": {
            "west": {"target": "meteor_crater", "type": "direction"},
            "south": {"target": "canyon_depths", "type": "direction"}
        }
    }
    
    rooms["spring_meadow"] = {
        "id": "spring_meadow",
        "name": "Eternal Spring Meadow",
        "description": "A meadow where spring flowers bloom year-round. Magical in nature, it never sees winter. Butterflies dance among the flowers.",
        "location_type": "wilderness",
        "coordinates": [-1, 4],
        "items": {"wildflower": {"quantity": 6, "value": 2}},
        "exits": {
            "south": {"target": "northern_road", "type": "direction"},
            "east": {"target": "trade_road_north", "type": "direction"}
        }
    }
    
    rooms["ravens_perch"] = {
        "id": "ravens_perch",
        "name": "Raven's Perch",
        "description": "A dead tree where ravens gather. The birds seem unnaturally intelligent, watching travelers with knowing eyes. Locals consider them omens.",
        "location_type": "wilderness",
        "coordinates": [-4, -6],
        "items": {"eagle_feather": {"quantity": 1, "value": 35}},
        "exits": {
            "east": {"target": "graveyard_road", "type": "direction"},
            "south": {"target": "graveyard_gates", "type": "direction"}
        }
    }
    
    rooms["hot_springs"] = {
        "id": "hot_springs",
        "name": "Mountain Hot Springs",
        "description": "Natural hot springs steam in the mountain air. The water is said to have healing properties. A popular destination despite the difficult journey.",
        "location_type": "wilderness",
        "coordinates": [0, 10],
        "items": {},
        "exits": {
            "south": {"target": "mountain_path", "type": "direction"},
            "west": {"target": "thundering_falls", "type": "direction"}
        }
    }
    
    rooms["windswept_dunes"] = {
        "id": "windswept_dunes",
        "name": "Windswept Dunes",
        "description": "Tall dunes shaped by constant wind. Sand streams from their crests like smoke. The wind never stops, making travel exhausting.",
        "location_type": "wilderness",
        "coordinates": [15, 2],
        "items": {},
        "exits": {
            "south": {"target": "sand_sea", "type": "direction"},
            "west": {"target": "sand_whirlpool", "type": "direction"}
        }
    }
    
    rooms["cactus_garden"] = {
        "id": "cactus_garden",
        "name": "Cactus Garden",
        "description": "A natural garden of cacti of all shapes and sizes. Some bloom with beautiful flowers. Water can be extracted from them in emergencies.",
        "location_type": "wilderness",
        "coordinates": [11, 0],
        "items": {"cactus_fruit": {"quantity": 3, "value": 8}},
        "exits": {
            "east": {"target": "desert_dunes_west", "type": "direction"},
            "south": {"target": "desert_well", "type": "direction"}
        }
    }
    
    rooms["petrified_forest"] = {
        "id": "petrified_forest",
        "name": "Petrified Forest",
        "description": "An ancient forest turned to stone. The trees stand as they did millions of years ago, now mineral instead of wood. An eerie, silent place.",
        "location_type": "wilderness",
        "coordinates": [16, 4],
        "items": {"smooth_stone": {"quantity": 3, "value": 8}},
        "exits": {
            "south": {"target": "oasis_village", "type": "direction"},
            "west": {"target": "nomad_camp", "type": "direction"}
        }
    }
    
    rooms["glacier_edge"] = {
        "id": "glacier_edge",
        "name": "Glacier's Edge",
        "description": "The edge of an ancient glacier. Blue ice stretches beyond sight. Crevasses make travel dangerous. The cold is deadly.",
        "location_type": "wilderness",
        "coordinates": [0, 22],
        "items": {"ice_crystal": {"quantity": 2, "value": 18}},
        "exits": {
            "south": {"target": "aurora_viewing", "type": "direction"}
        }
    }
    
    rooms["whale_bones"] = {
        "id": "whale_bones",
        "name": "Whale Bones Beach",
        "description": "A beach where the skeleton of a massive whale lies. How it got here is a mystery. The bones create an eerie sculpture against the sea.",
        "location_type": "wilderness",
        "coordinates": [4, -14],
        "items": {"old_bone": {"quantity": 4, "value": 2}},
        "exits": {
            "west": {"target": "coral_reef", "type": "direction"},
            "north": {"target": "kelp_forest", "type": "direction"}
        }
    }
    
    rooms["hermit_island"] = {
        "id": "hermit_island",
        "name": "Hermit Island",
        "description": "A tiny island just offshore, accessible at low tide. A hermit lives in a hut here, seeking solitude from the world.",
        "location_type": "building",
        "coordinates": [8, -12],
        "items": {"seashell": {"quantity": 3, "value": 4}},
        "exits": {
            "west": {"target": "fishing_village", "type": "direction"}
        }
    }
    
    rooms["riverside_camp"] = {
        "id": "riverside_camp",
        "name": "Riverside Camp",
        "description": "A popular camping spot by a gentle river. Fire pits and cleared ground show frequent use. A peaceful place to rest.",
        "location_type": "wilderness",
        "coordinates": [3, -4],
        "items": {"torch": {"quantity": 1, "value": 5}},
        "exits": {
            "north": {"target": "southern_highway", "type": "direction"},
            "south": {"target": "fishermans_rest", "type": "direction"}
        }
    }
    
    rooms["wild_boar_territory"] = {
        "id": "wild_boar_territory",
        "name": "Wild Boar Territory",
        "description": "An area where wild boars root and forage. They're aggressive when startled. Hunters prize them but approach with caution.",
        "location_type": "wilderness",
        "coordinates": [-3, 2],
        "items": {"raw_meat": {"quantity": 1, "value": 8}},
        "exits": {
            "south": {"target": "village_gardens", "type": "direction"},
            "west": {"target": "winding_path", "type": "direction"}
        }
    }
    
    rooms["old_cemetery"] = {
        "id": "old_cemetery",
        "name": "Old Cemetery",
        "description": "An ancient cemetery, older than the village one. The headstones are unreadable. Some graves appear disturbed. Best not to linger.",
        "location_type": "wilderness",
        "coordinates": [-1, -8],
        "items": {"old_bone": {"quantity": 2, "value": 2}},
        "exits": {
            "north": {"target": "coastal_cliffs", "type": "direction"},
            "west": {"target": "graveyard_road", "type": "direction"}
        }
    }
    
    rooms["gnome_burrow"] = {
        "id": "gnome_burrow",
        "name": "Gnome Burrow",
        "description": "A hillside dotted with tiny doors and windows. If gnomes ever lived here, they're gone now. The tiny tunnels are too small for humans.",
        "location_type": "building",
        "coordinates": [-3, 0],
        "items": {"gold_coin": {"quantity": 3, "value": 2}},
        "exits": {
            "east": {"target": "village_west_end", "type": "direction"},
            "west": {"target": "forest_edge", "type": "direction"}
        }
    }
    
    rooms["berry_patch"] = {
        "id": "berry_patch",
        "name": "Wild Berry Patch",
        "description": "A patch where berries grow wild in abundance. Birds and bears compete for the harvest. Villagers come here in season.",
        "location_type": "wilderness",
        "coordinates": [-4, 4],
        "items": {"cactus_fruit": {"quantity": 2, "value": 8}},
        "exits": {
            "east": {"target": "windmill_hill", "type": "direction"},
            "south": {"target": "winding_path", "type": "direction"}
        }
    }
    
    rooms["fox_den"] = {
        "id": "fox_den",
        "name": "Fox Den",
        "description": "A den where foxes raise their young. The cunning creatures watch from hiding. They're neither threatening nor friendly - just wary.",
        "location_type": "wilderness",
        "coordinates": [-6, 2],
        "items": {},
        "exits": {
            "south": {"target": "forest_clearing", "type": "direction"},
            "east": {"target": "standing_stones", "type": "direction"}
        }
    }
    
    # Generate Grand Harbor and Island rooms
    generate_all_islands(rooms)
    
    return world

def main():
    world = generate_world()
    
    # Count rooms
    room_count = len(world["rooms"])
    print(f"Generated {room_count} rooms")
    
    # Save to file
    output_path = "world.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(world, f, indent=2, ensure_ascii=False)
    
    print(f"World saved to {output_path}")
    
    # Print region summary
    regions = {}
    for room_id, room in world["rooms"].items():
        loc_type = room.get("location_type", "unknown")
        regions[loc_type] = regions.get(loc_type, 0) + 1
    
    print("\nRoom types:")
    for region, count in sorted(regions.items()):
        print(f"  {region}: {count}")

if __name__ == "__main__":
    main()
