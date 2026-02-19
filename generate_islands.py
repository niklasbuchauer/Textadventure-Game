"""
Island Generation Module - Generates all Grand Harbor + 7 Island rooms.
This module is imported by generate_world.py to add island content.
"""


def generate_grand_harbor(rooms):
    """Add Grand Harbor rooms connecting mainland to island boat travel."""
    
    # =========================================================================
    # GRAND HARBOR - Main hub for boat travel to islands
    # Connected from Port Haven Docks, coordinates [3, -12] to [7, -16]
    # =========================================================================
    
    rooms["grand_harbor_road"] = {
        "id": "grand_harbor_road",
        "name": "Harbor Road",
        "description": "A wide cobblestone road leads south from Port Haven toward the Grand Harbor. "
                       "The smell of salt and tar grows stronger. Seagulls wheel overhead and you can "
                       "hear the distant crack of sails. Merchant wagons rumble past carrying exotic goods.",
        "location_type": "transition",
        "coordinates": [3, -12],
        "items": {},
        "exits": {
            "north": {"target": "port_haven_docks", "type": "direction"},
            "south": {"target": "grand_harbor_gate", "type": "direction"},
            "west": {"target": "smugglers_cove", "type": "direction"}
        }
    }
    
    rooms["grand_harbor_gate"] = {
        "id": "grand_harbor_gate",
        "name": "Grand Harbor Gate",
        "description": "An impressive stone archway marks the entrance to the Grand Harbor district. "
                       "Guards in blue uniforms check cargo manifests. A sign reads: "
                       "'GRAND HARBOR - Gateway to the Outer Isles'. Beyond the gate, you can see "
                       "tall masts and hear the bustle of the harbor square.",
        "location_type": "transition",
        "coordinates": [3, -13],
        "items": {},
        "exits": {
            "north": {"target": "grand_harbor_road", "type": "direction"},
            "south": {"target": "grand_harbor_square", "type": "direction"},
            "west": {"target": "harbor_customs_office", "type": "direction"}
        }
    }
    
    rooms["grand_harbor_square"] = {
        "id": "grand_harbor_square",
        "name": "Grand Harbor Square",
        "description": "The heart of the Grand Harbor district. A large fountain shaped like a "
                       "kraken dominates the center. Sailors, merchants, and adventurers mingle "
                       "around market stalls. The Harbor Master's office stands to the east. "
                       "Docks extend in every direction, each leading to different island routes. "
                       "A weathered notice board displays island information and travel costs.",
        "location_type": "settlement",
        "coordinates": [3, -14],
        "npcs": ["harbor_master"],
        "items": {},
        "exits": {
            "north": {"target": "grand_harbor_gate", "type": "direction"},
            "east": {"target": "harbor_master_office", "type": "direction"},
            "west": {"target": "harbor_provisions_market", "type": "direction"},
            "south": {"target": "harbor_south_pier", "type": "direction"},
            "northeast": {"target": "harbor_north_dock", "type": "direction"},
            "southeast": {"target": "harbor_east_dock", "type": "direction"},
            "southwest": {"target": "harbor_west_dock", "type": "direction"}
        }
    }
    
    rooms["harbor_master_office"] = {
        "id": "harbor_master_office",
        "name": "Harbor Master's Office",
        "description": "A sturdy building filled with maps, charts, and shipping manifests. "
                       "A large world map on the wall shows the mainland surrounded by ocean, "
                       "with seven islands marked at various distances:\n\n"
                       "  [Lvl 5]  Sunstone Atoll    - Tropical paradise, ancient sun temples\n"
                       "  [Lvl 10] Emerald Isle      - Dense rainforest, overgrown ruins\n"
                       "  [Lvl 15] Stormbreak Island - Thunder cliffs, shipwreck coast\n"
                       "  [Lvl 20] Cinderforge Island- Volcanic lands, obsidian forges\n"
                       "  [Lvl 25] Dreadmist Isle    - Cursed fog, undead horrors\n"
                       "  [Lvl 30] Wyrmscale Island  - Dragon-infested peaks\n"
                       "  [Lvl 40] The Abyssal Reach - Eldritch void, cosmic terrors\n\n"
                       "The Harbor Master can tell you more about each destination.",
        "location_type": "building",
        "coordinates": [5, -14],
        "npcs": ["harbor_clerk"],
        "items": {"island_chart": {"quantity": 1, "value": 25}},
        "exits": {
            "west": {"target": "grand_harbor_square", "type": "direction"},
            "east": {"target": "merchant_wharf_entrance", "type": "direction"}
        }
    }
    
    rooms["harbor_tavern"] = {
        "id": "harbor_tavern",
        "name": "The Salty Compass Tavern",
        "description": "A rowdy sailor's tavern. Exotic drinks line the shelves and the walls "
                       "are covered with maps, harpoons, and trophies from distant islands. "
                       "Grizzled captains share tales of sea monsters and lost treasure. "
                       "The barkeep serves drinks that glow faintly in the dim light.",
        "location_type": "building",
        "coordinates": [1, -14],
        "npcs": ["tavern_keeper", "old_captain"],
        "items": {"rum": {"quantity": 2, "value": 8}, "sea_biscuit": {"quantity": 3, "value": 3}},
        "exits": {
            "east": {"target": "harbor_provisions_market", "type": "direction"},
            "upstairs": {"target": "harbor_inn_room", "type": "named", "display": "Inn Room"},
            "cellar": {"target": "harbor_tavern_cellar", "type": "named", "display": "Tavern Cellar"}
        }
    }
    
    rooms["harbor_inn_room"] = {
        "id": "harbor_inn_room",
        "name": "Harbor Inn Room",
        "description": "A small but clean room above the tavern. A porthole window looks out "
                       "over the harbor. The bed has a nautical-themed quilt. You can rest here "
                       "before your voyage.",
        "location_type": "building",
        "coordinates": [1, -13],
        "items": {},
        "exits": {
            "downstairs": {"target": "harbor_tavern", "type": "named", "display": "Back to Tavern"}
        }
    }
    
    rooms["harbor_shop"] = {
        "id": "harbor_shop",
        "name": "Seaside Outfitters",
        "description": "A well-stocked shop catering to ocean-bound adventurers. Waterproof bags, "
                       "healing potions, antidotes, and sturdy rope hang from the ceiling. "
                       "The shopkeeper is a retired sailor who knows what you'll need out there.",
        "location_type": "building",
        "coordinates": [5, -15],
        "shop": True,
        "items": {},
        "exits": {
            "outside": {"target": "harbor_south_pier", "type": "direction"}
        }
    }
    
    rooms["harbor_south_pier"] = {
        "id": "harbor_south_pier",
        "name": "South Pier",
        "description": "A long wooden pier stretching into the deep harbor waters. Crates and "
                       "barrels are stacked along its length. A shop for traveling supplies "
                       "is nestled at the pier's base. From here you can see the open ocean "
                       "stretching to the horizon.",
        "location_type": "dock",
        "coordinates": [3, -15],
        "items": {},
        "exits": {
            "north": {"target": "grand_harbor_square", "type": "direction"},
            "shop": {"target": "harbor_shop", "type": "named", "display": "Seaside Outfitters"},
            "east": {"target": "harbor_east_dock", "type": "direction"},
            "west": {"target": "harbor_west_dock", "type": "direction"},
            "south": {"target": "harbor_lighthouse_base", "type": "direction"}
        }
    }
    
    rooms["harbor_watchtower"] = {
        "id": "harbor_watchtower",
        "name": "Harbor Watchtower",
        "description": "A tall stone tower overlooking the entire harbor and the open ocean beyond. "
                       "From this vantage point you can see the dark shapes of distant islands "
                       "on the horizon. A telescope is mounted on the observation deck. "
                       "Seven distinct landmasses are visible, each in a different direction.",
        "location_type": "building",
        "coordinates": [5, -13],
        "items": {"spyglass": {"quantity": 1, "value": 30}},
        "exits": {
            "down": {"target": "harbor_north_dock", "type": "direction"}
        }
    }
    
    # --- Dock rooms with boat_travel exits ---
    
    rooms["harbor_north_dock"] = {
        "id": "harbor_north_dock",
        "name": "North Dock - Tropical Routes",
        "description": "The northern dock is painted in warm colors. Ships here are built for "
                       "warm waters. Route boards advertise:\n\n"
                       "  SUNSTONE ATOLL - 'Paradise awaits! Sun, sand, and ancient mysteries.'\n"
                       "    Unlock: 50g | Fare: 10g | Recommended Level: 5+\n\n"
                       "  EMERALD ISLE - 'Untamed jungle. Forgotten temples. Priceless relics.'\n"
                       "    Unlock: 150g | Fare: 25g | Recommended Level: 10+\n\n"
                       "Type 'board sunstone' or 'board emerald' to sail.",
        "location_type": "dock",
        "coordinates": [4, -13],
        "items": {},
        "exits": {
            "southwest": {"target": "grand_harbor_square", "type": "direction"},
            "up": {"target": "harbor_watchtower", "type": "direction"},
            "board sunstone": {
                "target": "sunstone_docks",
                "type": "boat_travel",
                "island_id": "sunstone_atoll",
                "display": "Sunstone Atoll",
                "unlock_cost": 50,
                "fare_cost": 10,
                "min_level": 5,
                "transition_text": "You board a sleek tropical vessel. The crew raises colorful sails\nand the ship cuts through warm turquoise waters. Schools of flying\nfish leap alongside the hull. After two days at sea, golden beaches\nand swaying palms emerge from the horizon..."
            },
            "board emerald": {
                "target": "emerald_docks",
                "type": "boat_travel",
                "island_id": "emerald_isle",
                "display": "Emerald Isle",
                "unlock_cost": 150,
                "fare_cost": 25,
                "min_level": 10,
                "transition_text": "You board a sturdy exploration vessel covered in vine motifs.\nThe ship navigates through increasingly dense fog. Strange bird\ncalls echo across the water. After three days, an impossibly green\nisland rises from the mist, its canopy touching the clouds..."
            }
        }
    }
    
    rooms["harbor_east_dock"] = {
        "id": "harbor_east_dock",
        "name": "East Dock - Dangerous Waters",
        "description": "The eastern dock is reinforced with heavy iron. The ships here are "
                       "built like warships. Route boards warn:\n\n"
                       "  STORMBREAK ISLAND - 'Brace yourself. The storms never stop.'\n"
                       "    Unlock: 300g | Fare: 50g | Recommended Level: 15+\n\n"
                       "  CINDERFORGE ISLAND - 'Where fire meets the sea. Bring heat protection.'\n"
                       "    Unlock: 500g | Fare: 75g | Recommended Level: 20+\n\n"
                       "Type 'board stormbreak' or 'board cinderforge' to sail.",
        "location_type": "dock",
        "coordinates": [5, -15],
        "items": {},
        "exits": {
            "northwest": {"target": "grand_harbor_square", "type": "direction"},
            "west": {"target": "harbor_south_pier", "type": "direction"},
            "board stormbreak": {
                "target": "stormbreak_docks",
                "type": "boat_travel",
                "island_id": "stormbreak_island",
                "display": "Stormbreak Island",
                "unlock_cost": 300,
                "fare_cost": 50,
                "min_level": 15,
                "transition_text": "You board an ironclad vessel with storm shields on every porthole.\nWithin hours, the sky darkens and rain lashes the deck. Lightning\nforks across the heavens as the ship battles through towering waves.\nAfter four harrowing days, jagged cliffs appear through the storm..."
            },
            "board cinderforge": {
                "target": "cinder_docks",
                "type": "boat_travel",
                "island_id": "cinderforge_island",
                "display": "Cinderforge Island",
                "unlock_cost": 500,
                "fare_cost": 75,
                "min_level": 20,
                "transition_text": "You board a ship with a hull treated in fireproof lacquer.\nThe ocean temperature rises as you sail south. Steam vents\nbubble from the sea floor. After five days, a volcanic island\nglowing with rivers of lava dominates the horizon..."
            }
        }
    }
    
    rooms["harbor_west_dock"] = {
        "id": "harbor_west_dock",
        "name": "West Dock - The Forbidden Routes",
        "description": "The western dock is shrouded in shadow despite the open sky. The ships "
                       "here are dark-hulled, crewed by grim-faced sailors. Route boards read:\n\n"
                       "  DREADMIST ISLE - 'Turn back. The dead don't rest here.'\n"
                       "    Unlock: 750g | Fare: 100g | Recommended Level: 25+\n\n"
                       "  WYRMSCALE ISLAND - 'Dragons rule these skies. You've been warned.'\n"
                       "    Unlock: 1200g | Fare: 150g | Recommended Level: 30+\n\n"
                       "  THE ABYSSAL REACH - 'Beyond the edge of reality itself.'\n"
                       "    Unlock: 2000g | Fare: 250g | Recommended Level: 40+\n\n"
                       "Type 'board dreadmist', 'board wyrmscale', or 'board abyssal' to sail.",
        "location_type": "dock",
        "coordinates": [1, -15],
        "items": {},
        "exits": {
            "northeast": {"target": "grand_harbor_square", "type": "direction"},
            "east": {"target": "harbor_south_pier", "type": "direction"},
            "board dreadmist": {
                "target": "dreadmist_docks",
                "type": "boat_travel",
                "island_id": "dreadmist_isle",
                "display": "Dreadmist Isle",
                "unlock_cost": 750,
                "fare_cost": 100,
                "min_level": 25,
                "transition_text": "You board a black-sailed vessel. The crew speaks in whispers.\nAs you sail, the fog thickens until you can barely see the bow.\nUnnatural moans echo across the water. After six days of\nblind navigation, a shore of pale bone-white sand appears..."
            },
            "board wyrmscale": {
                "target": "wyrm_docks",
                "type": "boat_travel",
                "island_id": "wyrmscale_island",
                "display": "Wyrmscale Island",
                "unlock_cost": 1200,
                "fare_cost": 150,
                "min_level": 30,
                "transition_text": "You board a ship reinforced with dragon-scale plates. The crew\nwears fireproof armor. As you approach the island, massive shadows\npass overhead — dragons circling their domain. After seven days,\nscorched cliffs and the stench of sulfur welcome you..."
            },
            "board abyssal": {
                "target": "abyssal_docks",
                "type": "boat_travel",
                "island_id": "abyssal_reach",
                "display": "The Abyssal Reach",
                "unlock_cost": 2000,
                "fare_cost": 250,
                "min_level": 40,
                "transition_text": "You board a ship that seems to exist between worlds. Its hull\nshimmers with void energy. Reality warps as you sail — stars\nappear where sky should be, the ocean turns colors that shouldn't\nexist. After an eternity (or moments?), a shore of impossible\ngeometry materializes from the void..."
            }
        }
    }
    
    rooms["harbor_warehouse"] = {
        "id": "harbor_warehouse",
        "name": "Harbor Warehouse",
        "description": "A massive warehouse storing goods from the outer islands. Crates labeled "
                       "with exotic names are stacked to the ceiling. Some crates seem to glow, "
                       "others are chained shut, and a few emit strange sounds. Workers move "
                       "carefully around the more dangerous cargo.",
        "location_type": "building",
        "coordinates": [1, -16],
        "items": {"torch": {"quantity": 2, "value": 5}, "rope": {"quantity": 1, "value": 10}},
        "exits": {
            "east": {"target": "harbor_south_pier", "type": "direction"},
            "south": {"target": "harbor_dry_dock", "type": "direction"}
        }
    }

    # --- Expanded Harbor Area (8 rooms) ---

    rooms["harbor_customs_office"] = {
        "id": "harbor_customs_office",
        "name": "Customs Office",
        "description": "A squat stone building where all incoming cargo is inspected and taxed. "
                       "Clerks in ink-stained uniforms pore over manifests behind a long counter. "
                       "A board on the wall lists contraband items, and a confiscation cage "
                       "in the corner holds seized goods — some of which look distinctly alive.",
        "location_type": "building",
        "coordinates": [2, -13],
        "items": {"customs_ledger": {"quantity": 1, "value": 5}},
        "exits": {
            "east": {"target": "grand_harbor_gate", "type": "direction"},
            "south": {"target": "harbor_provisions_market", "type": "direction"}
        }
    }

    rooms["harbor_provisions_market"] = {
        "id": "harbor_provisions_market",
        "name": "Provisions Market",
        "description": "An open-air market squeezed between the tavern and the harbor square. "
                       "Stalls overflow with salted meats, hardtack, barrels of fresh water, "
                       "and bundles of medicinal herbs. A weathered woman selling charms claims "
                       "her talismans ward off sea serpents. The smell of smoked fish is overwhelming.",
        "location_type": "settlement",
        "coordinates": [2, -14],
        "items": {"salted_meat": {"quantity": 3, "value": 6}, "hardtack": {"quantity": 5, "value": 2},
                  "sea_charm": {"quantity": 1, "value": 15}},
        "exits": {
            "north": {"target": "harbor_customs_office", "type": "direction"},
            "east": {"target": "grand_harbor_square", "type": "direction"},
            "west": {"target": "harbor_tavern", "type": "direction"},
            "south": {"target": "harbor_sailors_barracks", "type": "direction"}
        }
    }

    rooms["harbor_sailors_barracks"] = {
        "id": "harbor_sailors_barracks",
        "name": "Sailors' Barracks",
        "description": "A long, low building with rows of hammocks strung between timber posts. "
                       "Off-duty sailors snore, gamble with bone dice, or mend their clothes. "
                       "Personal effects dangle from hooks — lucky coins, faded letters, small "
                       "carvings of loved ones. A duty roster on the wall lists upcoming voyages.",
        "location_type": "building",
        "coordinates": [2, -15],
        "items": {"bone_dice": {"quantity": 1, "value": 3}},
        "exits": {
            "north": {"target": "harbor_provisions_market", "type": "direction"},
            "east": {"target": "harbor_south_pier", "type": "direction"}
        }
    }

    rooms["harbor_lighthouse_base"] = {
        "id": "harbor_lighthouse_base",
        "name": "Harbor Lighthouse - Base",
        "description": "The base of a tall stone lighthouse that guides ships safely into port. "
                       "Coils of heavy chain and spare lantern glass are stored here. A spiral "
                       "staircase winds upward into the tower. The lighthouse keeper's cat watches "
                       "you from atop a barrel, its eyes reflecting the distant sea.",
        "location_type": "building",
        "coordinates": [3, -16],
        "items": {"lantern_oil": {"quantity": 2, "value": 8}},
        "exits": {
            "north": {"target": "harbor_south_pier", "type": "direction"},
            "up": {"target": "harbor_lighthouse_top", "type": "direction"}
        }
    }

    rooms["harbor_lighthouse_top"] = {
        "id": "harbor_lighthouse_top",
        "name": "Harbor Lighthouse - Lantern Room",
        "description": "The top of the lighthouse. An enormous crystal lens focuses the flame "
                       "of a magical ever-burning lantern, sending a beam of light far across "
                       "the ocean. The view is breathtaking — you can see every dock, every "
                       "ship, and on clear days, the faint smudge of distant islands. Wind "
                       "howls through the iron railing circling the narrow observation deck.",
        "location_type": "building",
        "coordinates": [3, -17],
        "items": {},
        "exits": {
            "down": {"target": "harbor_lighthouse_base", "type": "direction"}
        }
    }

    rooms["harbor_dry_dock"] = {
        "id": "harbor_dry_dock",
        "name": "Dry Dock",
        "description": "A massive stone basin where ships are hauled out of the water for repairs. "
                       "A half-dismantled brigantine sits on wooden supports, its hull crawling "
                       "with shipwrights scraping barnacles and replacing planks. The air is thick "
                       "with the smell of tar and fresh-cut timber. A crane looms overhead.",
        "location_type": "building",
        "coordinates": [1, -17],
        "items": {"ship_plank": {"quantity": 2, "value": 4}, "tar_bucket": {"quantity": 1, "value": 6}},
        "exits": {
            "north": {"target": "harbor_warehouse", "type": "direction"}
        }
    }

    rooms["harbor_tavern_cellar"] = {
        "id": "harbor_tavern_cellar",
        "name": "Tavern Cellar",
        "description": "A damp stone cellar beneath the Salty Compass. Barrels of rum, wine, "
                       "and strange glowing spirits line the walls. A trapdoor that apparently "
                       "once connected to smuggling tunnels has been nailed shut — mostly. "
                       "Rats skitter in the shadows, and you notice scratch marks on one of "
                       "the barrels that look almost like a coded message.",
        "location_type": "building",
        "coordinates": [1, -15],
        "items": {"aged_rum": {"quantity": 1, "value": 25}, "dusty_wine": {"quantity": 2, "value": 12}},
        "exits": {
            "up": {"target": "harbor_tavern", "type": "direction"}
        }
    }

    rooms["harbor_supply_depot"] = {
        "id": "harbor_supply_depot",
        "name": "Harbor Supply Depot",
        "description": "A heavily guarded storage facility behind the Seaside Outfitters shop. "
                       "Sturdy crates stamped with naval insignia contain emergency provisions "
                       "for the harbor fleet. Racks hold coiled rope, folded canvas, signal flags, "
                       "and casks of pitch. A quartermaster checks inventory with methodical precision.",
        "location_type": "building",
        "coordinates": [5, -16],
        "items": {"naval_rope": {"quantity": 1, "value": 15}, "signal_flag": {"quantity": 1, "value": 10}},
        "exits": {
            "north": {"target": "harbor_shop", "type": "direction"}
        }
    }

    # --- Merchant's Wharf (New Sub-region, 8 rooms) ---

    rooms["merchant_wharf_entrance"] = {
        "id": "merchant_wharf_entrance",
        "name": "Merchant's Wharf - Entrance",
        "description": "A newer section of the harbor, built on reclaimed land east of the "
                       "master's office. An ornate wooden arch carved with leaping dolphins "
                       "marks the entrance. The wharf is alive with commerce — foreign merchants "
                       "in colorful garb haggle over prices while dock workers haul exotic cargo.",
        "location_type": "settlement",
        "coordinates": [6, -14],
        "items": {},
        "exits": {
            "west": {"target": "harbor_master_office", "type": "direction"},
            "east": {"target": "wharf_market_row", "type": "direction"},
            "south": {"target": "wharf_loading_bay", "type": "direction"}
        }
    }

    rooms["wharf_market_row"] = {
        "id": "wharf_market_row",
        "name": "Wharf Market Row",
        "description": "A bustling lane of permanent market stalls built from reclaimed ship "
                       "timber. Each stall bears flags from distant lands. Merchants sell "
                       "silks dyed in impossible colors, spices that tingle on the tongue, "
                       "and trinkets that hum with faint enchantment. A juggler entertains "
                       "a crowd while a pickpocket works the audience.",
        "location_type": "settlement",
        "coordinates": [7, -14],
        "items": {"exotic_silk": {"quantity": 1, "value": 30}, "rare_spice": {"quantity": 2, "value": 18}},
        "exits": {
            "west": {"target": "merchant_wharf_entrance", "type": "direction"},
            "north": {"target": "wharf_auction_house", "type": "direction"},
            "east": {"target": "wharf_foreign_quarters", "type": "direction"}
        }
    }

    rooms["wharf_auction_house"] = {
        "id": "wharf_auction_house",
        "name": "Wharf Auction House",
        "description": "A large open-sided pavilion where rare goods from the outer islands "
                       "go under the hammer. Rows of benches face a raised platform where an "
                       "auctioneer with a booming voice displays lots — a dragon scale here, "
                       "a vial of moonwater there. Wealthy merchants bid with subtle hand "
                       "signals. The tension in the room is palpable.",
        "location_type": "building",
        "coordinates": [7, -13],
        "items": {"auction_catalog": {"quantity": 1, "value": 5}},
        "exits": {
            "south": {"target": "wharf_market_row", "type": "direction"}
        }
    }

    rooms["wharf_foreign_quarters"] = {
        "id": "wharf_foreign_quarters",
        "name": "Foreign Traders' Quarter",
        "description": "A cluster of colorful tents and semi-permanent structures where traders "
                       "from the outer islands maintain a presence on the mainland. Each tent "
                       "is decorated in the style of its home island — tropical flowers for "
                       "Sunstone, living vines for Emerald, flickering embers for Cinderforge. "
                       "The air is a heady mix of incense, cooking fires, and unfamiliar perfumes.",
        "location_type": "settlement",
        "coordinates": [8, -14],
        "items": {"incense_bundle": {"quantity": 2, "value": 8}},
        "exits": {
            "west": {"target": "wharf_market_row", "type": "direction"},
            "north": {"target": "wharf_cartographer", "type": "direction"}
        }
    }

    rooms["wharf_cartographer"] = {
        "id": "wharf_cartographer",
        "name": "The Cartographer's Study",
        "description": "A cramped but fascinating shop belonging to a retired explorer who now "
                       "makes maps. Every surface is covered with charts — ocean currents, wind "
                       "patterns, island topographies, and a few maps marked 'HERE BE DRAGONS' "
                       "in red ink. The cartographer peers at you through a jeweler's loupe, "
                       "her fingers permanently stained with ink.",
        "location_type": "building",
        "coordinates": [8, -13],
        "items": {"detailed_sea_chart": {"quantity": 1, "value": 40}, "compass": {"quantity": 1, "value": 20}},
        "exits": {
            "south": {"target": "wharf_foreign_quarters", "type": "direction"},
            "up": {"target": "wharf_lookout_tower", "type": "direction"}
        }
    }

    rooms["wharf_lookout_tower"] = {
        "id": "wharf_lookout_tower",
        "name": "Merchant's Lookout Tower",
        "description": "A tall wooden tower at the eastern edge of the Merchant's Wharf, built "
                       "so traders can spot incoming ships before their competitors. Flags snap "
                       "in the wind at the top. A large brass telescope is bolted to the railing. "
                       "From here you can see ships approaching from every direction, and on "
                       "the clearest days, the volcanic glow of Cinderforge on the horizon.",
        "location_type": "building",
        "coordinates": [8, -12],
        "items": {},
        "exits": {
            "down": {"target": "wharf_cartographer", "type": "direction"}
        }
    }

    rooms["wharf_loading_bay"] = {
        "id": "wharf_loading_bay",
        "name": "Wharf Loading Bay",
        "description": "A wide stone platform at the water's edge where cargo is loaded and "
                       "unloaded from merchant vessels. A massive wooden crane swings crates "
                       "from ship decks onto waiting wagons. Dock workers shout instructions "
                       "over the creak of ropes and splash of waves. Seagulls dive for "
                       "scraps from burst crates of provisions.",
        "location_type": "dock",
        "coordinates": [6, -15],
        "items": {},
        "exits": {
            "north": {"target": "merchant_wharf_entrance", "type": "direction"},
            "east": {"target": "wharf_cargo_yard", "type": "direction"}
        }
    }

    rooms["wharf_cargo_yard"] = {
        "id": "wharf_cargo_yard",
        "name": "Cargo Yard",
        "description": "An open yard behind the loading bay, stacked with crates, barrels, and "
                       "mysterious packages awaiting collection. Each item bears tags in different "
                       "languages. Guard dogs patrol between the rows. A manifest board lists "
                       "expected shipments — some entries are crossed out and marked 'LOST AT SEA' "
                       "in somber ink.",
        "location_type": "building",
        "coordinates": [7, -15],
        "items": {"manifest_page": {"quantity": 1, "value": 3}},
        "exits": {
            "west": {"target": "wharf_loading_bay", "type": "direction"}
        }
    }


def generate_sunstone_atoll(rooms):
    """Generate Island 1: Sunstone Atoll - Tropical paradise with sun temples (~200 rooms)."""
    
    cx, cy = 50, -10  # Center coordinates
    
    # =========================================================================
    # SUNSTONE ATOLL - Tropical Island (Level 5+)
    # Coordinates: [42, -18] to [58, -2]
    # Sub-regions: Docks, Village, Palm Beach, Coral Lagoon, Jungle Interior,
    #              Sun Temple Ruins, Hidden Coves
    # =========================================================================
    
    # --- Docks & Arrival (5 rooms) ---
    rooms["sunstone_docks"] = {
        "id": "sunstone_docks",
        "name": "Sunstone Atoll - Harbor",
        "description": "A weathered wooden dock extends into crystal-clear turquoise water. "
                       "Palm trees sway in the warm breeze. The harbor is small but well-maintained, "
                       "with a few fishing boats and the larger vessel that brought you here. "
                       "A sandy path leads inland toward the village.",
        "location_type": "dock",
        "coordinates": [cx-4, cy],
        "items": {},
        "exits": {
            "board mainland": {
                "target": "harbor_north_dock",
                "type": "boat_travel",
                "island_id": "sunstone_atoll",
                "display": "Grand Harbor (Mainland)",
                "unlock_cost": 0,
                "fare_cost": 0,
                "min_level": 1,
                "transition_text": "You board the return vessel. The tropical island shrinks behind\nyou as the ship sets course for the mainland. After a peaceful\nvoyage, the familiar Grand Harbor comes into view..."
            },
            "east": {"target": "sunstone_dock_market", "type": "direction"},
            "south": {"target": "sunstone_beach_south", "type": "direction"}
        }
    }
    
    rooms["sunstone_dock_market"] = {
        "id": "sunstone_dock_market",
        "name": "Dockside Market",
        "description": "A small open-air market near the docks. Local fishermen sell fresh catch "
                       "and traders offer tropical goods. Colorful awnings provide shade from the "
                       "relentless sun. The aroma of grilled fish and exotic spices fills the air.",
        "location_type": "settlement",
        "coordinates": [cx-3, cy],
        "items": {"tropical_fish": {"quantity": 2, "value": 8}, "coconut": {"quantity": 3, "value": 4}},
        "exits": {
            "west": {"target": "sunstone_docks", "type": "direction"},
            "east": {"target": "sunstone_village_west", "type": "direction"},
            "south": {"target": "sunstone_tide_pools", "type": "direction"}
        }
    }
    
    rooms["sunstone_dock_storage"] = {
        "id": "sunstone_dock_storage",
        "name": "Dock Storage Shed",
        "description": "A small thatched-roof storage shed near the pier. Fishing nets, "
                       "crab traps, and diving equipment are stored here. A sunbleached map "
                       "on the wall shows the atoll's layout.",
        "location_type": "building",
        "coordinates": [cx-4, cy+1],
        "items": {"fishing_net": {"quantity": 1, "value": 12}, "diving_mask": {"quantity": 1, "value": 20}},
        "exits": {
            "south": {"target": "sunstone_docks", "type": "direction"},
            "north": {"target": "sunstone_dock_boathouse", "type": "direction"}
        }
    }

    # --- Sunstone Village (15 rooms) ---
    rooms["sunstone_village_west"] = {
        "id": "sunstone_village_west",
        "name": "Sunstone Village - West",
        "description": "The western edge of Sunstone Village. Thatched-roof huts sit on stilts "
                       "above the sandy ground. Village children play with carved wooden toys. "
                       "A gentle drumbeat echoes from the village center.",
        "location_type": "settlement",
        "coordinates": [cx-2, cy],
        "items": {},
        "exits": {
            "west": {"target": "sunstone_dock_market", "type": "direction"},
            "east": {"target": "sunstone_village_center", "type": "direction"},
            "south": {"target": "sunstone_palm_grove", "type": "direction"}
        }
    }
    
    rooms["sunstone_village_center"] = {
        "id": "sunstone_village_center",
        "name": "Sunstone Village - Center",
        "description": "The heart of Sunstone Village. A large bonfire pit surrounded by carved "
                       "stone seats serves as the gathering place. An enormous sun-shaped totem "
                       "stands in the center, its golden surface gleaming. Villagers go about "
                       "their daily lives with quiet contentment.",
        "location_type": "settlement",
        "coordinates": [cx-1, cy],
        "npcs": ["village_elder", "sun_priest"],
        "items": {},
        "exits": {
            "west": {"target": "sunstone_village_west", "type": "direction"},
            "east": {"target": "sunstone_village_east", "type": "direction"},
            "north": {"target": "sunstone_village_shrine", "type": "direction"},
            "south": {"target": "sunstone_village_south", "type": "direction"},
            "inn": {"target": "sunstone_inn", "type": "named", "display": "The Golden Shell Inn"}
        }
    }
    
    rooms["sunstone_village_east"] = {
        "id": "sunstone_village_east",
        "name": "Sunstone Village - East",
        "description": "The eastern part of the village. A trading post sells equipment to "
                       "adventurers. Dried fish and tropical fruit hang from wooden racks. "
                       "A path leads east into the jungle interior.",
        "location_type": "settlement",
        "coordinates": [cx, cy],
        "shop": True,
        "items": {},
        "exits": {
            "west": {"target": "sunstone_village_center", "type": "direction"},
            "east": {"target": "sunstone_jungle_edge", "type": "direction"},
            "north": {"target": "sunstone_village_training", "type": "direction"},
            "south": {"target": "sunstone_lagoon_path", "type": "direction"}
        }
    }
    
    rooms["sunstone_village_south"] = {
        "id": "sunstone_village_south",
        "name": "Sunstone Village - South Path",
        "description": "A sandy path leading south from the village toward the beaches. "
                       "Torches line the path, their flames dancing in the ocean breeze. "
                       "You can hear waves crashing on the shore ahead.",
        "location_type": "settlement",
        "coordinates": [cx-1, cy-1],
        "items": {},
        "exits": {
            "north": {"target": "sunstone_village_center", "type": "direction"},
            "south": {"target": "sunstone_palm_beach_north", "type": "direction"},
            "east": {"target": "sunstone_lagoon_path", "type": "direction"}
        }
    }
    
    rooms["sunstone_inn"] = {
        "id": "sunstone_inn",
        "name": "The Golden Shell Inn",
        "description": "A cozy thatched building with hammocks instead of beds. Shell windchimes "
                       "tinkle in the breeze. The innkeeper serves fresh coconut water and "
                       "grilled tropical fruit. A parrot on a perch squawks about treasure.",
        "location_type": "building",
        "coordinates": [cx-1, cy+1],
        "items": {"coconut_water": {"quantity": 2, "value": 5}},
        "exits": {
            "outside": {"target": "sunstone_village_center", "type": "direction"}
        }
    }
    
    rooms["sunstone_village_shrine"] = {
        "id": "sunstone_village_shrine",
        "name": "Sun Shrine",
        "description": "A small open-air shrine dedicated to the Sun God. Golden offerings "
                       "gleam on a stone altar. The villagers come here at dawn and dusk to pray. "
                       "Warm light seems to radiate from the shrine itself, even at night.",
        "location_type": "building",
        "coordinates": [cx-1, cy+2],
        "items": {"golden_offering": {"quantity": 1, "value": 25}},
        "exits": {
            "south": {"target": "sunstone_village_center", "type": "direction"},
            "east": {"target": "sunstone_village_training", "type": "direction"}
        }
    }
    
    rooms["sunstone_village_training"] = {
        "id": "sunstone_village_training",
        "name": "Training Grounds",
        "description": "An open sandy area where village warriors practice their combat skills. "
                       "Wooden dummies carved to look like monsters are set up as targets. "
                       "A grizzled warrior offers to spar with travelers.",
        "location_type": "settlement",
        "coordinates": [cx, cy+1],
        "npcs": ["weapons_trainer"],
        "items": {},
        "exits": {
            "south": {"target": "sunstone_village_east", "type": "direction"},
            "west": {"target": "sunstone_village_shrine", "type": "direction"},
            "north": {"target": "sunstone_north_trail", "type": "direction"}
        }
    }
    
    rooms["sunstone_herbalist_hut"] = {
        "id": "sunstone_herbalist_hut",
        "name": "Herbalist's Hut",
        "description": "A small hut overflowing with dried herbs, flowers, and strange roots. "
                       "Glass bottles of colorful potions line makeshift shelves. The herbalist, "
                       "an old woman with sun-darkened skin, knows remedies for everything.",
        "location_type": "building",
        "coordinates": [cx-2, cy+1],
        "items": {"healing_herb": {"quantity": 3, "value": 10}, "antidote": {"quantity": 2, "value": 15}},
        "exits": {
            "east": {"target": "sunstone_village_west", "type": "direction"},
            "west": {"target": "sunstone_herb_garden", "type": "direction"}
        }
    }

    rooms["sunstone_fishermans_wharf"]= {
        "id": "sunstone_fishermans_wharf",
        "name": "Fisherman's Wharf",
        "description": "A small wharf where the village fishermen mend nets and clean their catch. "
                       "Pelicans perch on the wooden posts, eyeing the fish buckets. An old "
                       "fisherman tells tales of giant sea creatures lurking in the deep waters.",
        "location_type": "settlement",
        "coordinates": [cx-3, cy-1],
        "items": {"raw_fish": {"quantity": 2, "value": 6}},
        "exits": {
            "north": {"target": "sunstone_dock_market", "type": "direction"},
            "east": {"target": "sunstone_palm_grove", "type": "direction"},
            "south": {"target": "sunstone_beach_south", "type": "direction"}
        }
    }
    
    rooms["sunstone_craft_hut"] = {
        "id": "sunstone_craft_hut",
        "name": "Craftsman's Workshop",
        "description": "A workshop where islanders craft items from shells, coral, and driftwood. "
                       "Beautiful jewelry and weapons made from natural materials are displayed. "
                       "The craftsman can work with materials you bring from the island.",
        "location_type": "building",
        "coordinates": [cx-2, cy-1],
        "crafting_station": "island_workbench",
        "items": {"shell_necklace": {"quantity": 1, "value": 18}},
        "exits": {
            "north": {"target": "sunstone_village_west", "type": "direction"},
            "south": {"target": "sunstone_workshop_yard", "type": "direction"}
        }
    }

    # --- Palm Beach (35 rooms) ---
    rooms["sunstone_palm_grove"] = {
        "id": "sunstone_palm_grove",
        "name": "Palm Grove",
        "description": "A grove of towering coconut palms. Their fronds create dappled shade "
                       "on the sandy ground. Coconuts litter the ground and crabs scuttle between "
                       "the roots. A warm breeze rustles through the leaves.",
        "location_type": "wilderness",
        "coordinates": [cx-2, cy-1],
        "items": {"coconut": {"quantity": 2, "value": 4}},
        "exits": {
            "north": {"target": "sunstone_village_west", "type": "direction"},
            "south": {"target": "sunstone_palm_beach_west", "type": "direction"},
            "east": {"target": "sunstone_palm_trail", "type": "direction"},
            "west": {"target": "sunstone_fishermans_wharf", "type": "direction"}
        }
    }
    
    rooms["sunstone_palm_trail"] = {
        "id": "sunstone_palm_trail",
        "name": "Palm Trail",
        "description": "A winding trail through dense palm trees. Tropical birds flit between "
                       "branches, their feathers brilliant shades of red, blue, and gold. "
                       "The trail slopes gently downward toward the beach.",
        "location_type": "wilderness",
        "coordinates": [cx-1, cy-2],
        "items": {},
        "exits": {
            "west": {"target": "sunstone_palm_grove", "type": "direction"},
            "south": {"target": "sunstone_palm_beach_north", "type": "direction"},
            "east": {"target": "sunstone_lagoon_path", "type": "direction"}
        }
    }
    
    rooms["sunstone_palm_beach_north"] = {
        "id": "sunstone_palm_beach_north",
        "name": "Palm Beach - North",
        "description": "Golden sand stretches in both directions. The water is impossibly clear — "
                       "you can see colorful fish swimming near the shore. Palm trees lean out "
                       "over the water as if reaching for the sea. Hermit crabs leave tiny tracks.",
        "location_type": "wilderness",
        "coordinates": [cx-1, cy-3],
        "items": {"seashell": {"quantity": 3, "value": 3}, "starfish": {"quantity": 1, "value": 7}},
        "exits": {
            "north": {"target": "sunstone_village_south", "type": "direction"},
            "south": {"target": "sunstone_palm_beach_center", "type": "direction"},
            "west": {"target": "sunstone_palm_beach_west", "type": "direction"},
            "east": {"target": "sunstone_palm_beach_east", "type": "direction"}
        }
    }
    
    rooms["sunstone_palm_beach_west"] = {
        "id": "sunstone_palm_beach_west",
        "name": "Palm Beach - West",
        "description": "The western stretch of Palm Beach. Rocky outcrops jut from the sand, "
                       "creating tide pools teeming with small sea creatures. Driftwood logs "
                       "provide natural seating. A faint path leads to hidden coves further west.",
        "location_type": "wilderness",
        "coordinates": [cx-3, cy-3],
        "items": {"driftwood": {"quantity": 2, "value": 3}},
        "exits": {
            "north": {"target": "sunstone_palm_grove", "type": "direction"},
            "east": {"target": "sunstone_palm_beach_north", "type": "direction"},
            "south": {"target": "sunstone_rocky_shore", "type": "direction"},
            "west": {"target": "sunstone_hidden_cove_path", "type": "direction"}
        }
    }
    
    rooms["sunstone_palm_beach_east"] = {
        "id": "sunstone_palm_beach_east",
        "name": "Palm Beach - East",
        "description": "The eastern end of Palm Beach curves toward a sparkling lagoon. "
                       "The water here changes from turquoise to deep blue where the reef drops off. "
                       "Colorful coral is visible just below the surface.",
        "location_type": "wilderness",
        "coordinates": [cx+1, cy-3],
        "items": {"coral_fragment": {"quantity": 1, "value": 12}},
        "exits": {
            "west": {"target": "sunstone_palm_beach_north", "type": "direction"},
            "south": {"target": "sunstone_coral_beach", "type": "direction"},
            "east": {"target": "sunstone_lagoon_shore", "type": "direction"}
        }
    }
    
    rooms["sunstone_palm_beach_center"] = {
        "id": "sunstone_palm_beach_center",
        "name": "Palm Beach - Center",
        "description": "The widest stretch of Palm Beach. The sand is fine and almost white. "
                       "A large flat rock in the surf serves as a natural diving platform. "
                       "Something glints beneath the shallow water nearby.",
        "location_type": "wilderness",
        "coordinates": [cx-1, cy-4],
        "items": {"pearl": {"quantity": 1, "value": 20}},
        "exits": {
            "north": {"target": "sunstone_palm_beach_north", "type": "direction"},
            "south": {"target": "sunstone_beach_far_south", "type": "direction"},
            "east": {"target": "sunstone_coral_beach", "type": "direction"},
            "west": {"target": "sunstone_rocky_shore", "type": "direction"}
        }
    }
    
    rooms["sunstone_beach_south"] = {
        "id": "sunstone_beach_south",
        "name": "Southern Shore",
        "description": "A quiet stretch of beach south of the docks. Waves lap gently at the shore. "
                       "Fishing boats are beached on the sand. An abandoned campfire surrounded "
                       "by footprints suggests others have rested here recently.",
        "location_type": "wilderness",
        "coordinates": [cx-4, cy-2],
        "items": {"charcoal": {"quantity": 1, "value": 2}},
        "exits": {
            "north": {"target": "sunstone_docks", "type": "direction"},
            "east": {"target": "sunstone_palm_beach_west", "type": "direction"},
            "south": {"target": "sunstone_hidden_cove_path", "type": "direction"}
        }
    }
    
    rooms["sunstone_rocky_shore"] = {
        "id": "sunstone_rocky_shore",
        "name": "Rocky Shore",
        "description": "The beach gives way to jagged volcanic rock. Tide pools filled with "
                       "anemones, sea urchins, and small octopi dot the surface. Waves crash "
                       "dramatically against the rocks, sending spray high into the air.",
        "location_type": "wilderness",
        "coordinates": [cx-3, cy-5],
        "items": {"sea_urchin": {"quantity": 2, "value": 5}},
        "exits": {
            "north": {"target": "sunstone_palm_beach_west", "type": "direction"},
            "east": {"target": "sunstone_palm_beach_center", "type": "direction"},
            "south": {"target": "sunstone_sea_cave_entrance", "type": "direction"}
        }
    }
    
    rooms["sunstone_coral_beach"] = {
        "id": "sunstone_coral_beach",
        "name": "Coral Beach",
        "description": "A beach made entirely of crushed coral, giving it a pink-white hue. "
                       "The water here is phenomenally clear. Tropical fish school in the shallows "
                       "and you can see the reef structure extending far out to sea.",
        "location_type": "wilderness",
        "coordinates": [cx, cy-4],
        "items": {"pink_coral": {"quantity": 1, "value": 15}},
        "exits": {
            "north": {"target": "sunstone_palm_beach_east", "type": "direction"},
            "west": {"target": "sunstone_palm_beach_center", "type": "direction"},
            "east": {"target": "sunstone_lagoon_south", "type": "direction"},
            "south": {"target": "sunstone_beach_far_south", "type": "direction"}
        }
    }
    
    rooms["sunstone_beach_far_south"] = {
        "id": "sunstone_beach_far_south",
        "name": "Far Southern Beach",
        "description": "The southernmost point of the atoll's beaches. Wild and untouched, "
                       "with tangled seaweed and shells washing up in heaps. A weathered "
                       "stone statue half-buried in sand points toward the temple ruins inland.",
        "location_type": "wilderness",
        "coordinates": [cx-1, cy-6],
        "items": {"ancient_coin": {"quantity": 1, "value": 20}},
        "exits": {
            "north": {"target": "sunstone_palm_beach_center", "type": "direction"},
            "east": {"target": "sunstone_coral_beach", "type": "direction"},
            "west": {"target": "sunstone_sea_cave_entrance", "type": "direction"}
        }
    }
    
    rooms["sunstone_tide_pools"] = {
        "id": "sunstone_tide_pools",
        "name": "Tide Pool Flats",
        "description": "A wide flat area of volcanic rock exposed at low tide. Dozens of tide "
                       "pools teem with small crabs, colorful fish, and swaying anemones. "
                       "It's a naturalist's paradise. Be careful — the rocks are slippery.",
        "location_type": "wilderness",
        "coordinates": [cx-3, cy-1],
        "items": {"hermit_crab": {"quantity": 1, "value": 6}},
        "exits": {
            "north": {"target": "sunstone_dock_market", "type": "direction"},
            "south": {"target": "sunstone_palm_beach_west", "type": "direction"},
            "east": {"target": "sunstone_palm_grove", "type": "direction"}
        }
    }
    
    # Beach cleanup/additions
    rooms["sunstone_sea_cave_entrance"] = {
        "id": "sunstone_sea_cave_entrance",
        "name": "Sea Cave Entrance",
        "description": "A dark cave mouth opens in the rocky cliff face. Waves surge in and out "
                       "of the opening. The cave walls are encrusted with barnacles and mussels. "
                       "Eerie echoes comes from deep within. Something glows faintly in the dark.",
        "location_type": "wilderness",
        "coordinates": [cx-3, cy-6],
        "items": {},
        "exits": {
            "north": {"target": "sunstone_rocky_shore", "type": "direction"},
            "east": {"target": "sunstone_beach_far_south", "type": "direction"},
            "enter": {"target": "sunstone_sea_cave_inner", "type": "direction"}
        }
    }
    
    rooms["sunstone_sea_cave_inner"] = {
        "id": "sunstone_sea_cave_inner",
        "name": "Sea Cave Interior",
        "description": "The cave opens into a surprisingly spacious grotto. Bioluminescent "
                       "algae coats the walls, casting an ethereal blue glow. The floor is covered "
                       "in smooth pebbles and shallow tidal water. Treasure might be hidden here.",
        "location_type": "wilderness",
        "coordinates": [cx-4, cy-7],
        "items": {"glowing_algae": {"quantity": 2, "value": 10}, "gold_doubloon": {"quantity": 1, "value": 30}},
        "exits": {
            "outside": {"target": "sunstone_sea_cave_entrance", "type": "direction"},
            "deeper": {"target": "sunstone_sea_cave_deep", "type": "direction"}
        }
    }
    
    rooms["sunstone_sea_cave_deep"] = {
        "id": "sunstone_sea_cave_deep",
        "name": "Deep Sea Grotto",
        "description": "The deepest part of the sea cave. A pool of perfectly still water "
                       "reflects the bioluminescent ceiling like a mirror. Ancient carvings "
                       "on the walls depict the Sun God descending into the ocean. "
                       "A chest sits on a ledge above the waterline.",
        "location_type": "wilderness",
        "coordinates": [cx-5, cy-8],
        "items": {"sun_medallion": {"quantity": 1, "value": 45}, "pearl_necklace": {"quantity": 1, "value": 35}},
        "exits": {
            "back": {"target": "sunstone_sea_cave_inner", "type": "direction"},
            "south": {"target": "sunstone_sea_cave_crystal", "type": "direction"}
        }
    }

    # --- Coral Lagoon (35 rooms) ---
    rooms["sunstone_lagoon_path"] = {
        "id": "sunstone_lagoon_path",
        "name": "Lagoon Path",
        "description": "A sandy trail winding through low scrub toward the lagoon. Butterflies "
                       "drift between tropical flowers. The air is sweetly scented with frangipani "
                       "and jasmine. The sound of gentle waves grows louder ahead.",
        "location_type": "wilderness",
        "coordinates": [cx, cy-1],
        "items": {},
        "exits": {
            "north": {"target": "sunstone_village_east", "type": "direction"},
            "south": {"target": "sunstone_lagoon_shore", "type": "direction"},
            "west": {"target": "sunstone_palm_trail", "type": "direction"},
            "east": {"target": "sunstone_lagoon_overlook", "type": "direction"}
        }
    }
    
    rooms["sunstone_lagoon_overlook"] = {
        "id": "sunstone_lagoon_overlook",
        "name": "Lagoon Overlook",
        "description": "A raised rocky point with a stunning view of the coral lagoon below. "
                       "The water is a mesmerizing gradient of blues and greens. You can see "
                       "the dark shapes of large fish moving in the lagoon. A wooden bench "
                       "has been placed here by previous visitors.",
        "location_type": "wilderness",
        "coordinates": [cx+1, cy-1],
        "items": {},
        "exits": {
            "west": {"target": "sunstone_lagoon_path", "type": "direction"},
            "south": {"target": "sunstone_lagoon_east", "type": "direction"},
            "east": {"target": "sunstone_jungle_edge", "type": "direction"}
        }
    }
    
    rooms["sunstone_lagoon_shore"] = {
        "id": "sunstone_lagoon_shore",
        "name": "Lagoon Shore",
        "description": "The sheltered shore of the coral lagoon. The water barely ripples here, "
                       "protected from ocean swells by the reef. Colorful fish dart between "
                       "coral heads just feet from shore. Sea turtles sometimes surface nearby.",
        "location_type": "wilderness",
        "coordinates": [cx+1, cy-2],
        "items": {"turtle_shell_piece": {"quantity": 1, "value": 12}},
        "exits": {
            "west": {"target": "sunstone_palm_beach_east", "type": "direction"},
            "north": {"target": "sunstone_lagoon_overlook", "type": "direction"},
            "south": {"target": "sunstone_lagoon_south", "type": "direction"},
            "east": {"target": "sunstone_lagoon_east", "type": "direction"}
        }
    }
    
    rooms["sunstone_lagoon_east"] = {
        "id": "sunstone_lagoon_east",
        "name": "Eastern Lagoon",
        "description": "The eastern edge of the lagoon where the water deepens. Coral formations "
                       "create natural channels. Schools of angelfish and parrotfish swim in "
                       "formation. A natural rock bridge arches over a narrow channel.",
        "location_type": "wilderness",
        "coordinates": [cx+2, cy-2],
        "items": {"angel_fish": {"quantity": 1, "value": 10}},
        "exits": {
            "west": {"target": "sunstone_lagoon_shore", "type": "direction"},
            "north": {"target": "sunstone_lagoon_overlook", "type": "direction"},
            "south": {"target": "sunstone_reef_shallows", "type": "direction"},
            "east": {"target": "sunstone_reef_edge", "type": "direction"}
        }
    }
    
    rooms["sunstone_lagoon_south"] = {
        "id": "sunstone_lagoon_south",
        "name": "Southern Lagoon",
        "description": "The southern reaches of the lagoon. The water is deeper here and "
                       "takes on a rich sapphire hue. Large coral heads break the surface. "
                       "An underwater cave entrance is visible through the clear water.",
        "location_type": "wilderness",
        "coordinates": [cx+1, cy-4],
        "items": {"sapphire_coral": {"quantity": 1, "value": 18}},
        "exits": {
            "north": {"target": "sunstone_lagoon_shore", "type": "direction"},
            "west": {"target": "sunstone_coral_beach", "type": "direction"},
            "east": {"target": "sunstone_reef_shallows", "type": "direction"},
            "south": {"target": "sunstone_lagoon_deep", "type": "direction"}
        }
    }
    
    rooms["sunstone_lagoon_deep"] = {
        "id": "sunstone_lagoon_deep",
        "name": "Deep Lagoon",
        "description": "The deepest part of the lagoon. The water is almost impossibly blue. "
                       "Manta rays glide through the depths. Ancient stone pillars, remnants of "
                       "a sunken temple, rise from the lagoon floor. Something shimmers below.",
        "location_type": "wilderness",
        "coordinates": [cx+1, cy-5],
        "items": {"sunken_idol": {"quantity": 1, "value": 30}},
        "exits": {
            "north": {"target": "sunstone_lagoon_south", "type": "direction"},
            "east": {"target": "sunstone_reef_deep", "type": "direction"}
        }
    }
    
    rooms["sunstone_reef_shallows"] = {
        "id": "sunstone_reef_shallows",
        "name": "Reef Shallows",
        "description": "Shallow water over a vibrant coral reef. You can walk here at low tide, "
                       "though the coral is sharp. Tropical fish of every color imaginable dart "
                       "between the formations. Giant clams sit partially open on the reef floor.",
        "location_type": "wilderness",
        "coordinates": [cx+2, cy-4],
        "items": {"giant_clam_pearl": {"quantity": 1, "value": 25}},
        "exits": {
            "north": {"target": "sunstone_lagoon_east", "type": "direction"},
            "west": {"target": "sunstone_lagoon_south", "type": "direction"},
            "south": {"target": "sunstone_reef_deep", "type": "direction"},
            "east": {"target": "sunstone_reef_edge", "type": "direction"}
        }
    }
    
    rooms["sunstone_reef_edge"] = {
        "id": "sunstone_reef_edge",
        "name": "Reef Edge",
        "description": "The outer edge of the coral reef. Beyond here the ocean floor drops "
                       "away into deep blue. The reef wall is alive with sea fans, sponges, "
                       "and corals. Reef sharks patrol the drop-off. Not safe for swimming.",
        "location_type": "wilderness",
        "coordinates": [cx+3, cy-3],
        "items": {"sea_fan": {"quantity": 1, "value": 8}},
        "exits": {
            "west": {"target": "sunstone_lagoon_east", "type": "direction"},
            "south": {"target": "sunstone_reef_shallows", "type": "direction"},
            "north": {"target": "sunstone_reef_north", "type": "direction"}
        }
    }
    
    rooms["sunstone_reef_north"] = {
        "id": "sunstone_reef_north",
        "name": "Northern Reef",
        "description": "The northern section of the reef system. Strong currents sweep through "
                       "here, bringing nutrients that attract larger fish. Barracuda and tuna "
                       "are common sights. The reef is less colorful but more dramatic.",
        "location_type": "wilderness",
        "coordinates": [cx+3, cy-1],
        "items": {},
        "exits": {
            "south": {"target": "sunstone_reef_edge", "type": "direction"},
            "west": {"target": "sunstone_jungle_clearing", "type": "direction"}
        }
    }
    
    rooms["sunstone_reef_deep"] = {
        "id": "sunstone_reef_deep",
        "name": "Deep Reef Waters",
        "description": "The deepest accessible part of the reef. Giant brain corals and "
                       "towering pillar corals create an underwater forest. A sunken ship's "
                       "mast protrudes from the sand. Something valuable might be down there.",
        "location_type": "wilderness",
        "coordinates": [cx+2, cy-6],
        "items": {"shipwreck_compass": {"quantity": 1, "value": 22}, "barnacle_encrusted_sword": {"quantity": 1, "value": 30}},
        "exits": {
            "north": {"target": "sunstone_reef_shallows", "type": "direction"},
            "west": {"target": "sunstone_lagoon_deep", "type": "direction"}
        }
    }
    
    # --- Jungle Interior (40 rooms) ---
    rooms["sunstone_jungle_edge"] = {
        "id": "sunstone_jungle_edge",
        "name": "Jungle Edge",
        "description": "The border between the village clearing and dense tropical jungle. "
                       "Tall trees with massive buttress roots block the sky. Vines hang like "
                       "curtains. The air is thick, humid, and alive with insect sounds. "
                       "A machete-cut trail leads deeper into the green darkness.",
        "location_type": "wilderness",
        "coordinates": [cx+1, cy],
        "items": {},
        "exits": {
            "west": {"target": "sunstone_village_east", "type": "direction"},
            "east": {"target": "sunstone_jungle_trail", "type": "direction"},
            "south": {"target": "sunstone_lagoon_overlook", "type": "direction"},
            "north": {"target": "sunstone_jungle_north", "type": "direction"}
        }
    }
    
    rooms["sunstone_jungle_trail"] = {
        "id": "sunstone_jungle_trail",
        "name": "Jungle Trail",
        "description": "A narrow trail hacked through dense vegetation. Enormous ferns brush "
                       "against you. Colorful parrots screech from above. Strange fruit hangs "
                       "from branches just out of reach. The canopy is so thick that only "
                       "dappled light reaches the ground.",
        "location_type": "wilderness",
        "coordinates": [cx+2, cy],
        "items": {"jungle_fruit": {"quantity": 2, "value": 6}},
        "exits": {
            "west": {"target": "sunstone_jungle_edge", "type": "direction"},
            "east": {"target": "sunstone_jungle_heart", "type": "direction"},
            "south": {"target": "sunstone_jungle_clearing", "type": "direction"},
            "north": {"target": "sunstone_jungle_canopy_path", "type": "direction"}
        }
    }
    
    rooms["sunstone_jungle_north"] = {
        "id": "sunstone_jungle_north",
        "name": "Northern Jungle",
        "description": "The northern section of the jungle. The trees here are ancient, their "
                       "trunks wider than houses. Moss and orchids cling to every surface. "
                       "Monkey troops swing through the canopy above, chattering warnings.",
        "location_type": "wilderness",
        "coordinates": [cx+1, cy+1],
        "items": {"orchid": {"quantity": 1, "value": 12}},
        "exits": {
            "south": {"target": "sunstone_jungle_edge", "type": "direction"},
            "east": {"target": "sunstone_jungle_canopy_path", "type": "direction"},
            "north": {"target": "sunstone_north_trail", "type": "direction"}
        }
    }
    
    rooms["sunstone_north_trail"] = {
        "id": "sunstone_north_trail",
        "name": "North Trail",
        "description": "A trail climbing northward through the jungle. Stone steps, partially "
                       "overgrown, suggest this was once a well-traveled road. Broken pottery "
                       "and carved stones litter the edges. The Sun Temple must be nearby.",
        "location_type": "wilderness",
        "coordinates": [cx+1, cy+2],
        "items": {"broken_pottery": {"quantity": 1, "value": 5}},
        "exits": {
            "south": {"target": "sunstone_jungle_north", "type": "direction"},
            "west": {"target": "sunstone_village_training", "type": "direction"},
            "north": {"target": "sunstone_temple_approach", "type": "direction"},
            "east": {"target": "sunstone_ancient_road", "type": "direction"}
        }
    }
    
    rooms["sunstone_jungle_canopy_path"] = {
        "id": "sunstone_jungle_canopy_path",
        "name": "Canopy Path",
        "description": "A series of rope bridges and wooden platforms high in the jungle canopy. "
                       "The view is breathtaking — you can see the glittering lagoon in one "
                       "direction and the volcanic peak in another. Toucans perch nearby.",
        "location_type": "wilderness",
        "coordinates": [cx+2, cy+1],
        "items": {"toucan_feather": {"quantity": 1, "value": 14}},
        "exits": {
            "west": {"target": "sunstone_jungle_north", "type": "direction"},
            "south": {"target": "sunstone_jungle_trail", "type": "direction"},
            "east": {"target": "sunstone_canopy_nest", "type": "direction"},
            "north": {"target": "sunstone_ancient_road", "type": "direction"}
        }
    }
    
    rooms["sunstone_canopy_nest"] = {
        "id": "sunstone_canopy_nest",
        "name": "Eagle's Nest Lookout",
        "description": "The highest point in the canopy walkway. A massive eagle's nest "
                       "occupies a platform. The eagles have moved on, but left behind "
                       "gleaming feathers and curious trinkets stolen from travelers below.",
        "location_type": "wilderness",
        "coordinates": [cx+3, cy+1],
        "items": {"eagle_feather": {"quantity": 1, "value": 18}, "shiny_trinket": {"quantity": 1, "value": 10}},
        "exits": {
            "west": {"target": "sunstone_jungle_canopy_path", "type": "direction"},
            "east": {"target": "sunstone_canopy_observatory", "type": "direction"}
        }
    }

    rooms["sunstone_jungle_heart"]= {
        "id": "sunstone_jungle_heart",
        "name": "Heart of the Jungle",
        "description": "The deepest, wildest part of the jungle. Ancient trees tower overhead "
                       "and the undergrowth is nearly impenetrable. Strange sounds echo around "
                       "you — clicks, hisses, and deep rumbles. The air is thick with humidity "
                       "and the scent of decay mixed with blooming flowers.",
        "location_type": "wilderness",
        "coordinates": [cx+3, cy],
        "items": {"rare_mushroom": {"quantity": 2, "value": 15}},
        "exits": {
            "west": {"target": "sunstone_jungle_trail", "type": "direction"},
            "south": {"target": "sunstone_jungle_ravine", "type": "direction"},
            "east": {"target": "sunstone_overgrown_ruins", "type": "direction"},
            "north": {"target": "sunstone_jungle_waterfall", "type": "direction"}
        }
    }
    
    rooms["sunstone_jungle_clearing"] = {
        "id": "sunstone_jungle_clearing",
        "name": "Jungle Clearing",
        "description": "A natural opening in the jungle canopy. Sunlight pours in, encouraging "
                       "a riot of wildflowers and butterflies. Standing stones arranged in a "
                       "circle suggest ancient rituals were performed here. The stones still "
                       "feel warm to the touch.",
        "location_type": "wilderness",
        "coordinates": [cx+2, cy-1],
        "items": {"sunstone_shard": {"quantity": 1, "value": 20}},
        "exits": {
            "north": {"target": "sunstone_jungle_trail", "type": "direction"},
            "east": {"target": "sunstone_jungle_ravine", "type": "direction"},
            "south": {"target": "sunstone_lagoon_overlook", "type": "direction"},
            "west": {"target": "sunstone_reef_north", "type": "direction"}
        }
    }
    
    rooms["sunstone_jungle_ravine"] = {
        "id": "sunstone_jungle_ravine",
        "name": "Jungle Ravine",
        "description": "A deep ravine cuts through the jungle floor. A stream trickles along "
                       "the bottom. Rope bridges cross at various points. The ravine walls are "
                       "lined with exposed roots and glittering mineral deposits.",
        "location_type": "wilderness",
        "coordinates": [cx+3, cy-1],
        "items": {"mineral_deposit": {"quantity": 1, "value": 16}},
        "exits": {
            "north": {"target": "sunstone_jungle_heart", "type": "direction"},
            "west": {"target": "sunstone_jungle_clearing", "type": "direction"},
            "south": {"target": "sunstone_jungle_stream", "type": "direction"}
        }
    }
    
    rooms["sunstone_jungle_stream"] = {
        "id": "sunstone_jungle_stream",
        "name": "Jungle Stream",
        "description": "A clear freshwater stream winds through the jungle. Smooth rocks "
                       "create small waterfalls and pools. Freshwater fish dart in the shallows. "
                       "The stream flows from the volcanic hills to the east.",
        "location_type": "wilderness",
        "coordinates": [cx+3, cy-2],
        "items": {"freshwater_fish": {"quantity": 1, "value": 7}},
        "exits": {
            "north": {"target": "sunstone_jungle_ravine", "type": "direction"},
            "south": {"target": "sunstone_reef_edge", "type": "direction"}
        }
    }
    
    rooms["sunstone_jungle_waterfall"] = {
        "id": "sunstone_jungle_waterfall",
        "name": "Jungle Waterfall",
        "description": "A beautiful waterfall cascades down a moss-covered cliff into a "
                       "crystal pool. Rainbows dance in the mist. Behind the waterfall, "
                       "you can barely make out the entrance to a hidden grotto.",
        "location_type": "wilderness",
        "coordinates": [cx+3, cy+2],
        "items": {"rainbow_crystal": {"quantity": 1, "value": 22}},
        "exits": {
            "south": {"target": "sunstone_jungle_heart", "type": "direction"},
            "behind waterfall": {"target": "sunstone_hidden_grotto", "type": "named", "display": "Hidden Grotto"},
            "west": {"target": "sunstone_ancient_road", "type": "direction"}
        }
    }
    
    rooms["sunstone_hidden_grotto"] = {
        "id": "sunstone_hidden_grotto",
        "name": "Hidden Grotto",
        "description": "A secret cave behind the waterfall. The walls sparkle with embedded "
                       "crystals. A natural hot spring bubbles in the corner. Ancient offerings "
                       "to the Sun God line stone shelves — this was a sacred bathing place.",
        "location_type": "wilderness",
        "coordinates": [cx+4, cy+2],
        "items": {"sun_crystal": {"quantity": 1, "value": 35}, "ancient_offering": {"quantity": 1, "value": 25}},
        "exits": {
            "outside": {"target": "sunstone_jungle_waterfall", "type": "direction"},
            "south": {"target": "sunstone_grotto_depths", "type": "direction"}
        }
    }

    rooms["sunstone_overgrown_ruins"]= {
        "id": "sunstone_overgrown_ruins",
        "name": "Overgrown Temple Ruins",
        "description": "Crumbling stone walls and pillars choked with vines. This was once "
                       "an outer building of the Sun Temple complex. Carved sun motifs are "
                       "still visible on the remaining stonework. Snakes slither through "
                       "the ruins and something hisses from the shadows.",
        "location_type": "wilderness",
        "coordinates": [cx+4, cy],
        "items": {"carved_sun_stone": {"quantity": 1, "value": 18}},
        "exits": {
            "west": {"target": "sunstone_jungle_heart", "type": "direction"},
            "north": {"target": "sunstone_temple_outer_east", "type": "direction"},
            "east": {"target": "sunstone_temple_garden", "type": "direction"}
        }
    }
    
    # --- Sun Temple Ruins (25-30 rooms) ---
    rooms["sunstone_ancient_road"] = {
        "id": "sunstone_ancient_road",
        "name": "Ancient Sun Road",
        "description": "A wide stone road, cracked and overgrown but still impressive. "
                       "Sun-disc carvings are set into the paving stones at regular intervals. "
                       "This was clearly the main processional route to the Sun Temple. "
                       "Broken columns line both sides like silent sentinels.",
        "location_type": "wilderness",
        "coordinates": [cx+2, cy+2],
        "items": {"sun_disc_fragment": {"quantity": 1, "value": 12}},
        "exits": {
            "south": {"target": "sunstone_jungle_canopy_path", "type": "direction"},
            "west": {"target": "sunstone_north_trail", "type": "direction"},
            "north": {"target": "sunstone_temple_approach", "type": "direction"},
            "east": {"target": "sunstone_jungle_waterfall", "type": "direction"}
        }
    }
    
    rooms["sunstone_temple_approach"] = {
        "id": "sunstone_temple_approach",
        "name": "Temple Approach",
        "description": "The final stretch before the Sun Temple. Enormous stone guardian "
                       "statues flank the road, their eyes set with amber gems that still "
                       "glow faintly. The jungle has been kept at bay here as if by magic. "
                       "The temperature rises noticeably near the temple.",
        "location_type": "wilderness",
        "coordinates": [cx+1, cy+3],
        "items": {"amber_gem": {"quantity": 1, "value": 28}},
        "exits": {
            "south": {"target": "sunstone_north_trail", "type": "direction"},
            "east": {"target": "sunstone_ancient_road", "type": "direction"},
            "north": {"target": "sunstone_temple_gate", "type": "direction"}
        }
    }
    
    rooms["sunstone_temple_gate"] = {
        "id": "sunstone_temple_gate",
        "name": "Sun Temple Gate",
        "description": "A massive stone gateway carved with scenes of sun worship. Twin "
                       "obelisks topped with gold-plated sun discs frame the entrance. "
                       "Despite centuries of abandonment, the gate still radiates warmth. "
                       "The main temple courtyard lies beyond.",
        "location_type": "wilderness",
        "coordinates": [cx+1, cy+4],
        "items": {},
        "exits": {
            "south": {"target": "sunstone_temple_approach", "type": "direction"},
            "north": {"target": "sunstone_temple_courtyard", "type": "direction"},
            "east": {"target": "sunstone_temple_outer_east", "type": "direction"},
            "west": {"target": "sunstone_temple_outer_west", "type": "direction"}
        }
    }
    
    rooms["sunstone_temple_outer_west"] = {
        "id": "sunstone_temple_outer_west",
        "name": "Temple Outer Wall - West",
        "description": "The western exterior of the Sun Temple. Fallen blocks and rubble "
                       "create natural hiding spots. Jungle vines have begun reclaiming "
                       "the walls. Strange sigils glow faintly when shadows pass over them.",
        "location_type": "wilderness",
        "coordinates": [cx, cy+4],
        "items": {"temple_brick": {"quantity": 1, "value": 8}},
        "exits": {
            "east": {"target": "sunstone_temple_gate", "type": "direction"},
            "north": {"target": "sunstone_temple_west_wing", "type": "direction"}
        }
    }
    
    rooms["sunstone_temple_outer_east"] = {
        "id": "sunstone_temple_outer_east",
        "name": "Temple Outer Wall - East",
        "description": "The eastern exterior of the Sun Temple. A collapsed section of wall "
                       "reveals the temple's internal chambers. Gold leaf still clings to some "
                       "stones. Something moves in the rubble — temple guardians still patrol.",
        "location_type": "wilderness",
        "coordinates": [cx+3, cy+3],
        "items": {"gold_leaf": {"quantity": 1, "value": 15}},
        "exits": {
            "west": {"target": "sunstone_temple_gate", "type": "direction"},
            "south": {"target": "sunstone_overgrown_ruins", "type": "direction"},
            "north": {"target": "sunstone_temple_east_wing", "type": "direction"}
        }
    }
    
    rooms["sunstone_temple_courtyard"] = {
        "id": "sunstone_temple_courtyard",
        "name": "Sun Temple Courtyard",
        "description": "The central courtyard of the Sun Temple. A massive sundial dominates "
                       "the center, its gnomon still casting a shadow that tracks the sun. "
                       "Doorways lead to the temple wings. The main sanctuary lies to the north. "
                       "Faded murals on the walls depict the Sun God's blessings.",
        "location_type": "wilderness",
        "coordinates": [cx+1, cy+5],
        "items": {"sundial_fragment": {"quantity": 1, "value": 20}},
        "exits": {
            "south": {"target": "sunstone_temple_gate", "type": "direction"},
            "north": {"target": "sunstone_temple_sanctuary", "type": "direction"},
            "east": {"target": "sunstone_temple_east_wing", "type": "direction"},
            "west": {"target": "sunstone_temple_west_wing", "type": "direction"}
        }
    }
    
    rooms["sunstone_temple_east_wing"] = {
        "id": "sunstone_temple_east_wing",
        "name": "Temple East Wing",
        "description": "The eastern wing of the temple. This was the Hall of Offerings — "
                       "stone pedestals hold the remnants of ancient gifts to the Sun God. "
                       "Some treasures remain, protected by magical wards that still flicker.",
        "location_type": "wilderness",
        "coordinates": [cx+3, cy+4],
        "items": {"golden_chalice": {"quantity": 1, "value": 30}},
        "exits": {
            "west": {"target": "sunstone_temple_courtyard", "type": "direction"},
            "south": {"target": "sunstone_temple_outer_east", "type": "direction"},
            "north": {"target": "sunstone_temple_treasury", "type": "direction"}
        }
    }
    
    rooms["sunstone_temple_west_wing"] = {
        "id": "sunstone_temple_west_wing",
        "name": "Temple West Wing",
        "description": "The western wing contains the priests' quarters. Small cells with "
                       "stone beds line the corridor. Prayer scrolls in faded ink cover the "
                       "walls. A well in the center still holds fresh water, impossibly pure.",
        "location_type": "wilderness",
        "coordinates": [cx, cy+5],
        "items": {"prayer_scroll": {"quantity": 1, "value": 12}, "holy_water": {"quantity": 1, "value": 18}},
        "exits": {
            "east": {"target": "sunstone_temple_courtyard", "type": "direction"},
            "south": {"target": "sunstone_temple_outer_west", "type": "direction"},
            "north": {"target": "sunstone_temple_library", "type": "direction"}
        }
    }
    
    rooms["sunstone_temple_sanctuary"] = {
        "id": "sunstone_temple_sanctuary",
        "name": "Temple Sanctuary",
        "description": "The holiest chamber of the Sun Temple. A giant golden sun disc hangs "
                       "from the ceiling, still catching light through a precision-cut skylight. "
                       "The altar beneath it radiates gentle warmth. Ancient magic lingers here — "
                       "this is where the Sun Priests performed their greatest rituals.",
        "location_type": "wilderness",
        "coordinates": [cx+1, cy+6],
        "items": {"sun_priest_robe": {"quantity": 1, "value": 35}},
        "exits": {
            "south": {"target": "sunstone_temple_courtyard", "type": "direction"},
            "east": {"target": "sunstone_temple_treasury", "type": "direction"},
            "west": {"target": "sunstone_temple_library", "type": "direction"},
            "descend": {"target": "sunstone_temple_catacombs", "type": "direction"}
        }
    }
    
    rooms["sunstone_temple_treasury"] = {
        "id": "sunstone_temple_treasury",
        "name": "Temple Treasury",
        "description": "A heavily reinforced chamber that once held the temple's wealth. "
                       "Most has been looted over the centuries, but some treasures remain "
                       "in magical containment fields that thieves couldn't penetrate. "
                       "Gold dust covers the floor.",
        "location_type": "wilderness",
        "coordinates": [cx+3, cy+5],
        "items": {"sun_gold_ingot": {"quantity": 1, "value": 45}, "temple_key": {"quantity": 1, "value": 15}},
        "exits": {
            "south": {"target": "sunstone_temple_east_wing", "type": "direction"},
            "west": {"target": "sunstone_temple_sanctuary", "type": "direction"}
        }
    }
    
    rooms["sunstone_temple_library"] = {
        "id": "sunstone_temple_library",
        "name": "Temple Library",
        "description": "Shelves of stone tablets and preserved scrolls fill this room. "
                       "The knowledge of an entire civilization is stored here — astronomy, "
                       "medicine, magic, history. Some tablets glow with enchanted text. "
                       "A reading lectern holds an open tome about the Sun God's champions.",
        "location_type": "wilderness",
        "coordinates": [cx, cy+6],
        "items": {"ancient_tome": {"quantity": 1, "value": 25}, "enchanted_tablet": {"quantity": 1, "value": 30}},
        "exits": {
            "east": {"target": "sunstone_temple_sanctuary", "type": "direction"},
            "south": {"target": "sunstone_temple_west_wing", "type": "direction"}
        }
    }
    
    rooms["sunstone_temple_catacombs"] = {
        "id": "sunstone_temple_catacombs",
        "name": "Temple Catacombs",
        "description": "Deep beneath the sanctuary, narrow passages wind between ancient "
                       "burial niches. The Sun Priests were interred here with their sacred "
                       "artifacts. The air is dry and warm — preserving everything perfectly. "
                       "A heavy stone door leads to the true depths below.",
        "location_type": "wilderness",
        "coordinates": [cx+1, cy+7],
        "items": {"priest_amulet": {"quantity": 1, "value": 32}},
        "exits": {
            "up": {"target": "sunstone_temple_sanctuary", "type": "direction"},
            "deeper": {"target": "sunstone_temple_deep_crypt", "type": "direction"}
        }
    }
    
    rooms["sunstone_temple_deep_crypt"] = {
        "id": "sunstone_temple_deep_crypt",
        "name": "Deep Crypt - Dungeon Entrance",
        "description": "The deepest level of the temple catacombs. A massive stone door, "
                       "carved with the image of the Solar Pharaoh, stands before you. "
                       "Golden light seeps from the cracks. Beyond lies the Temple of the Sun — "
                       "a living dungeon where the Sun God's final guardians still stand watch.",
        "location_type": "wilderness",
        "coordinates": [cx+1, cy+8],
        "items": {},
        "exits": {
            "up": {"target": "sunstone_temple_catacombs", "type": "direction"},
            "enter": {
                "target": "FIXED_DUNGEON",
                "type": "fixed_dungeon",
                "dungeon_id": "temple_of_the_sun",
                "transition_text": "You push open the ancient door. Blinding golden light floods the passage. The heat intensifies as you descend into the Temple of the Sun..."
            }
        }
    }
    
    rooms["sunstone_temple_garden"] = {
        "id": "sunstone_temple_garden",
        "name": "Temple Garden",
        "description": "An overgrown sacred garden east of the temple complex. Plants here "
                       "have grown wild and strange — some flowers glow, others move to track "
                       "the sun. Medicinal herbs of incredible potency grow among the weeds.",
        "location_type": "wilderness",
        "coordinates": [cx+5, cy],
        "items": {"sunbloom_flower": {"quantity": 2, "value": 18}, "golden_herb": {"quantity": 1, "value": 22}},
        "exits": {
            "west": {"target": "sunstone_overgrown_ruins", "type": "direction"},
            "north": {"target": "sunstone_temple_outer_east", "type": "direction"}
        }
    }
    
    # --- Hidden Coves (10 rooms) ---
    rooms["sunstone_hidden_cove_path"] = {
        "id": "sunstone_hidden_cove_path",
        "name": "Hidden Path",
        "description": "A barely visible trail through dense coastal scrub. Someone has "
                       "marked the path with small stacks of stones. The trail winds along "
                       "the cliff edge with dangerous drops to the sea below.",
        "location_type": "wilderness",
        "coordinates": [cx-5, cy-3],
        "items": {},
        "exits": {
            "east": {"target": "sunstone_palm_beach_west", "type": "direction"},
            "north": {"target": "sunstone_beach_south", "type": "direction"},
            "south": {"target": "sunstone_hidden_cove", "type": "direction"}
        }
    }
    
    rooms["sunstone_hidden_cove"] = {
        "id": "sunstone_hidden_cove",
        "name": "Hidden Cove",
        "description": "A secluded cove accessible only at low tide or by the hidden path. "
                       "The small beach is littered with washed-up treasures from shipwrecks. "
                       "A makeshift shelter suggests someone has been living here. "
                       "Crates marked with skull and crossbones are stacked against the cliff.",
        "location_type": "wilderness",
        "coordinates": [cx-5, cy-5],
        "items": {"pirate_map": {"quantity": 1, "value": 30}, "smuggled_gems": {"quantity": 1, "value": 40}},
        "exits": {
            "north": {"target": "sunstone_hidden_cove_path", "type": "direction"},
            "cave": {"target": "sunstone_smuggler_cave", "type": "named", "display": "Smuggler's Cave"}
        }
    }
    
    rooms["sunstone_smuggler_cave"] = {
        "id": "sunstone_smuggler_cave",
        "name": "Smuggler's Cave",
        "description": "A cave that was clearly used by smugglers or pirates. Rusty weapon "
                       "racks, empty rum barrels, and a makeshift table with a card game "
                       "frozen mid-hand fill the space. A locked chest sits in the corner — "
                       "the lock is old and might be breakable.",
        "location_type": "wilderness",
        "coordinates": [cx-6, cy-5],
        "items": {"rusty_cutlass": {"quantity": 1, "value": 15}, "rum_barrel": {"quantity": 1, "value": 12}, "locked_chest_key": {"quantity": 1, "value": 5}},
        "exits": {
            "outside": {"target": "sunstone_hidden_cove", "type": "direction"},
            "south": {"target": "sunstone_smuggler_tunnel", "type": "direction"}
        }
    }

    # --- Volcanic Hill Area (extra rooms for ~200 total) ---
    rooms["sunstone_volcanic_hill_base"] = {
        "id": "sunstone_volcanic_hill_base",
        "name": "Volcanic Hill Base",
        "description": "The base of a small dormant volcano at the atoll's center. Dark volcanic "
                       "rock contrasts with the lush green jungle. Hot springs bubble from cracks "
                       "in the rock. The soil is incredibly fertile here.",
        "location_type": "wilderness",
        "coordinates": [cx+4, cy+3],
        "items": {"volcanic_rock": {"quantity": 2, "value": 8}},
        "exits": {
            "south": {"target": "sunstone_temple_outer_east", "type": "direction"},
            "north": {"target": "sunstone_volcanic_slope", "type": "direction"},
            "west": {"target": "sunstone_temple_courtyard", "type": "direction"}
        }
    }
    
    rooms["sunstone_volcanic_slope"] = {
        "id": "sunstone_volcanic_slope",
        "name": "Volcanic Slope",
        "description": "The steep slope of the dormant volcano. Steam vents hiss from the "
                       "dark rock. Hardy plants cling to the mountainside. The view from "
                       "here encompasses the entire atoll — beaches, lagoon, jungle, and temple.",
        "location_type": "wilderness",
        "coordinates": [cx+4, cy+4],
        "items": {"obsidian_shard": {"quantity": 1, "value": 14}},
        "exits": {
            "south": {"target": "sunstone_volcanic_hill_base", "type": "direction"},
            "north": {"target": "sunstone_volcanic_summit", "type": "direction"}
        }
    }
    
    rooms["sunstone_volcanic_summit"] = {
        "id": "sunstone_volcanic_summit",
        "name": "Volcanic Summit",
        "description": "The summit of the dormant volcano. A small crater lake fills the top, "
                       "its water a vivid emerald green. Steam rises from the warm surface. "
                       "The entire atoll spreads below you. On clear days, you might see other "
                       "islands on the far horizon.",
        "location_type": "wilderness",
        "coordinates": [cx+4, cy+5],
        "items": {"volcanic_crystal": {"quantity": 1, "value": 28}},
        "exits": {
            "south": {"target": "sunstone_volcanic_slope", "type": "direction"},
            "north": {"target": "sunstone_volcanic_crater", "type": "direction"}
        }
    }

    rooms["sunstone_hot_springs"]= {
        "id": "sunstone_hot_springs",
        "name": "Natural Hot Springs",
        "description": "A cluster of natural hot springs fed by volcanic heat. The mineral-rich "
                       "water is said to have healing properties. Stone basins have been carved "
                       "out for bathing. A peaceful, restorative spot.",
        "location_type": "wilderness",
        "coordinates": [cx+5, cy+3],
        "items": {"mineral_salt": {"quantity": 2, "value": 10}},
        "exits": {
            "west": {"target": "sunstone_volcanic_hill_base", "type": "direction"},
            "south": {"target": "sunstone_temple_garden", "type": "direction"}
        }
    }
    
    # Additional connecting rooms to reach ~200
    rooms["sunstone_bamboo_bridge"] = {
        "id": "sunstone_bamboo_bridge",
        "name": "Bamboo Bridge",
        "description": "A swaying bamboo bridge crossing a deep jungle gorge. The bridge "
                       "creaks alarmingly with each step. Far below, a river rushes through "
                       "the rocky canyon. Monkeys swing on the bridge's support ropes.",
        "location_type": "wilderness",
        "coordinates": [cx+5, cy+1],
        "items": {},
        "exits": {
            "west": {"target": "sunstone_canopy_nest", "type": "direction"},
            "south": {"target": "sunstone_temple_garden", "type": "direction"}
        }
    }
    
    rooms["sunstone_mushroom_hollow"] = {
        "id": "sunstone_mushroom_hollow",
        "name": "Mushroom Hollow",
        "description": "A damp hollow filled with enormous mushrooms, some taller than a person. "
                       "They glow softly in shades of blue and purple. The air is thick with "
                       "spores. Some of these mushrooms are valuable alchemical ingredients.",
        "location_type": "wilderness",
        "coordinates": [cx+4, cy-1],
        "items": {"giant_mushroom_cap": {"quantity": 2, "value": 12}, "luminescent_spore": {"quantity": 1, "value": 16}},
        "exits": {
            "west": {"target": "sunstone_jungle_ravine", "type": "direction"},
            "north": {"target": "sunstone_overgrown_ruins", "type": "direction"}
        }
    }
    
    rooms["sunstone_tidal_cave"] = {
        "id": "sunstone_tidal_cave",
        "name": "Tidal Cave",
        "description": "A cave that floods at high tide. Right now the water is low enough "
                       "to explore. Polished stones and shells line the floor. Strange "
                       "carved symbols on the walls suggest this was a sacred place.",
        "location_type": "wilderness",
        "coordinates": [cx-5, cy-1],
        "items": {"polished_stone": {"quantity": 2, "value": 5}},
        "exits": {
            "east": {"target": "sunstone_tide_pools", "type": "direction"},
            "west": {"target": "sunstone_tidal_deep", "type": "direction"}
        }
    }

    rooms["sunstone_sunset_point"]= {
        "id": "sunstone_sunset_point",
        "name": "Sunset Point",
        "description": "A rocky promontory on the western coast. This is the best spot on "
                       "the entire atoll to watch the sunset. Carved stone benches face the "
                       "ocean. At dusk, the sky erupts in gold and crimson.",
        "location_type": "wilderness",
        "coordinates": [cx-6, cy-3],
        "items": {"sunset_painting": {"quantity": 1, "value": 20}},
        "exits": {
            "east": {"target": "sunstone_hidden_cove_path", "type": "direction"},
            "west": {"target": "sunstone_sunset_arch", "type": "direction"}
        }
    }

    rooms["sunstone_mangrove_swamp"]= {
        "id": "sunstone_mangrove_swamp",
        "name": "Mangrove Swamp",
        "description": "A tangle of mangrove trees with their roots submerged in brackish water. "
                       "Crabs and mudskippers inhabit the roots. The footing is treacherous. "
                       "Mosquitoes buzz relentlessly. This area connects the beach to the jungle.",
        "location_type": "wilderness",
        "coordinates": [cx-2, cy-3],
        "items": {"mangrove_root": {"quantity": 1, "value": 6}},
        "exits": {
            "east": {"target": "sunstone_palm_beach_north", "type": "direction"},
            "north": {"target": "sunstone_palm_grove", "type": "direction"},
            "south": {"target": "sunstone_palm_beach_center", "type": "direction"}
        }
    }
    
    rooms["sunstone_ancient_pier"] = {
        "id": "sunstone_ancient_pier",
        "name": "Ancient Stone Pier",
        "description": "Remnants of an ancient pier built from carved stone blocks. "
                       "Whoever lived here long ago had a sophisticated harbor. "
                       "Barnacles and coral have claimed most of the structure, "
                       "but the engineering is still impressive.",
        "location_type": "wilderness",
        "coordinates": [cx-4, cy+2],
        "items": {"ancient_anchor": {"quantity": 1, "value": 18}},
        "exits": {
            "south": {"target": "sunstone_dock_storage", "type": "direction"},
            "east": {"target": "sunstone_village_shrine", "type": "direction"}
        }
    }



    # === SUNSTONE ATOLL EXPANSION ===

    # --- Expanded Docks (+3 rooms) ---

    rooms["sunstone_dock_boathouse"] = {
        "id": "sunstone_dock_boathouse",
        "name": "Old Boathouse",
        "description": "A weathered boathouse perched over the water on barnacle-crusted stilts. "
                       "Fishing boats in various states of repair are stacked inside, their hulls "
                       "painted in fading tropical colours. A cat sleeps atop a coil of rope, "
                       "unbothered by the creaking timbers.",
        "coordinates": [cx - 5, cy + 1],
        "location_type": "building",
        "items": {"boat_repair_kit": {"quantity": 1, "value": 15}, "old_fishing_rod": {"quantity": 1, "value": 10}},
        "exits": {
            "south": {"target": "sunstone_dock_storage", "type": "direction"},
            "east": {"target": "sunstone_dock_chandlery", "type": "direction"}
        }
    }

    rooms["sunstone_dock_chandlery"] = {
        "id": "sunstone_dock_chandlery",
        "name": "Ship's Chandlery",
        "description": "A supply shop catering to sailors and fishermen. Ropes, tackle, canvas, "
                       "tar, and navigational instruments fill every surface. The owner, a retired "
                       "sailor with sun-leathered skin, trades stories as readily as supplies.",
        "coordinates": [cx - 3, cy + 2],
        "location_type": "building",
        "items": {"navigation_compass": {"quantity": 1, "value": 22}, "waterproof_canvas": {"quantity": 1, "value": 12}},
        "exits": {
            "west": {"target": "sunstone_dock_boathouse", "type": "direction"},
            "south": {"target": "sunstone_dock_market", "type": "direction"}
        }
    }

    rooms["sunstone_dock_lighthouse"] = {
        "id": "sunstone_dock_lighthouse",
        "name": "Sunstone Lighthouse",
        "description": "A squat lighthouse built from coral blocks, its flame burning with a warm "
                       "amber glow that guides ships through the treacherous reef. The keeper "
                       "maintains a log of every vessel sighted, including several that appear "
                       "in no shipping registry.",
        "coordinates": [cx - 5, cy],
        "location_type": "building",
        "items": {"lighthouse_log_page": {"quantity": 1, "value": 10}, "amber_lens_shard": {"quantity": 1, "value": 25}},
        "exits": {
            "east": {"target": "sunstone_docks", "type": "direction"}
        }
    }

    # --- Expanded Village (+5 rooms) ---

    rooms["sunstone_herb_garden"] = {
        "id": "sunstone_herb_garden",
        "name": "Terraced Herb Garden",
        "description": "A lovingly maintained garden of terraced beds cascading down a gentle slope. "
                       "Medicinal herbs, tropical spices, and rare flowers grow in organized profusion. "
                       "Butterflies drift between the blooms, and the air is thick with fragrance.",
        "coordinates": [cx - 3, cy + 1],
        "location_type": "wilderness",
        "items": {"tropical_spice": {"quantity": 2, "value": 8}, "rare_orchid": {"quantity": 1, "value": 20}},
        "exits": {
            "east": {"target": "sunstone_herbalist_hut", "type": "direction"},
            "south": {"target": "sunstone_village_orchard", "type": "direction"}
        }
    }

    rooms["sunstone_village_orchard"] = {
        "id": "sunstone_village_orchard",
        "name": "Tropical Orchard",
        "description": "Rows of fruit trees heavy with mangoes, papayas, and breadfruit. "
                       "The orchard provides much of the village's food, and the ground beneath "
                       "the trees is littered with fallen fruit that attracts colourful birds.",
        "coordinates": [cx - 4, cy - 1],
        "location_type": "wilderness",
        "items": {"tropical_mango": {"quantity": 3, "value": 3}, "breadfruit": {"quantity": 2, "value": 4}},
        "exits": {
            "north": {"target": "sunstone_herb_garden", "type": "direction"},
            "east": {"target": "sunstone_village_west", "type": "direction"}
        }
    }

    rooms["sunstone_workshop_yard"] = {
        "id": "sunstone_workshop_yard",
        "name": "Workshop Yard",
        "description": "An open-air workspace where village craftspeople shape wood, weave "
                       "palm fronds, and carve bone. Half-finished canoes, baskets, and "
                       "decorative masks are propped against every surface. Children play "
                       "among the wood shavings.",
        "coordinates": [cx - 2, cy - 2],
        "location_type": "building",
        "items": {"carved_mask": {"quantity": 1, "value": 15}, "palm_weave_basket": {"quantity": 1, "value": 8}},
        "exits": {
            "north": {"target": "sunstone_craft_hut", "type": "direction"},
            "east": {"target": "sunstone_village_lookout", "type": "direction"}
        }
    }

    rooms["sunstone_village_lookout"] = {
        "id": "sunstone_village_lookout",
        "name": "Village Lookout Platform",
        "description": "A raised wooden platform offering panoramic views of the atoll. The "
                       "turquoise lagoon sparkles to the east, palm-fringed beaches stretch "
                       "south, and the volcanic hill rises to the northeast. Signal flags "
                       "hang ready for use if trouble approaches.",
        "coordinates": [cx - 3, cy - 2],
        "location_type": "building",
        "items": {"signal_flag": {"quantity": 1, "value": 8}, "spyglass": {"quantity": 1, "value": 25}},
        "exits": {
            "west": {"target": "sunstone_workshop_yard", "type": "direction"}
        }
    }

    rooms["sunstone_village_well"] = {
        "id": "sunstone_village_well",
        "name": "Sacred Well",
        "description": "An ancient well lined with sun-bleached coral, said to have been blessed "
                       "by the sun priests who first settled the atoll. The water is always cool "
                       "and sweet despite the tropical heat. Villagers leave small offerings of "
                       "flowers and shells at its base.",
        "coordinates": [cx, cy + 2],
        "location_type": "building",
        "items": {"blessed_water": {"quantity": 1, "value": 12}, "coral_offering": {"quantity": 1, "value": 6}},
        "exits": {
            "north": {"target": "sunstone_village_east", "type": "direction"}
        }
    }

    # --- Expanded Palm Beach (+8 rooms) ---

    rooms["sunstone_driftwood_cove"] = {
        "id": "sunstone_driftwood_cove",
        "name": "Driftwood Cove",
        "description": "A small cove where ocean currents deposit enormous quantities of driftwood, "
                       "creating natural sculptures bleached white by sun and salt. Among the "
                       "driftwood, treasures occasionally wash up — bottles with messages, exotic "
                       "shells, and fragments of far-off shipwrecks.",
        "coordinates": [cx - 4, cy - 3],
        "location_type": "wilderness",
        "items": {"message_bottle": {"quantity": 1, "value": 15}, "exotic_shell": {"quantity": 1, "value": 10}},
        "exits": {
            "east": {"target": "sunstone_palm_beach_west", "type": "direction"},
            "south": {"target": "sunstone_washed_reef", "type": "direction"}
        }
    }

    rooms["sunstone_washed_reef"] = {
        "id": "sunstone_washed_reef",
        "name": "Wave-Washed Reef",
        "description": "A section of reef exposed at low tide, creating a natural maze of "
                       "rock pools and coral channels. The pools teem with tiny fish, sea "
                       "urchins, and starfish in vivid colours. The footing is treacherous "
                       "on the slippery coral.",
        "coordinates": [cx - 4, cy - 4],
        "location_type": "wilderness",
        "items": {"starfish": {"quantity": 1, "value": 5}, "sea_urchin_spine": {"quantity": 2, "value": 3}},
        "exits": {
            "north": {"target": "sunstone_driftwood_cove", "type": "direction"}
        }
    }

    rooms["sunstone_palm_hammock_grove"] = {
        "id": "sunstone_palm_hammock_grove",
        "name": "Hammock Grove",
        "description": "A grove of coconut palms with hammocks strung between them, swaying "
                       "gently in the ocean breeze. This is where the village relaxes during "
                       "the hottest part of the day. The sound of waves and rustling palm "
                       "fronds creates a natural lullaby.",
        "coordinates": [cx, cy - 3],
        "location_type": "wilderness",
        "items": {"coconut": {"quantity": 2, "value": 3}, "palm_shade_token": {"quantity": 1, "value": 5}},
        "exits": {
            "west": {"target": "sunstone_palm_beach_north", "type": "direction"},
            "east": {"target": "sunstone_palm_beach_east", "type": "direction"}
        }
    }

    rooms["sunstone_beach_bonfire"] = {
        "id": "sunstone_beach_bonfire",
        "name": "Bonfire Circle",
        "description": "A permanent bonfire pit surrounded by driftwood seats, where villagers "
                       "gather for celebrations, storytelling, and feasts. The blackened sand "
                       "around the pit is studded with shell fragments and the remnants of "
                       "countless meals.",
        "coordinates": [cx - 2, cy - 4],
        "location_type": "wilderness",
        "items": {"bonfire_ash": {"quantity": 1, "value": 2}, "feast_remnant": {"quantity": 1, "value": 5}},
        "exits": {
            "north": {"target": "sunstone_palm_beach_west", "type": "direction"},
            "east": {"target": "sunstone_palm_beach_center", "type": "direction"}
        }
    }

    rooms["sunstone_surf_break"] = {
        "id": "sunstone_surf_break",
        "name": "Surf Break",
        "description": "Where the reef creates a natural break, producing consistent waves "
                       "that crash against the shore with rhythmic precision. Local surfers "
                       "ride the waves on carved wooden boards. The spray catches the sunlight, "
                       "creating constant miniature rainbows.",
        "coordinates": [cx + 2, cy - 3],
        "location_type": "wilderness",
        "items": {"surf_board_fragment": {"quantity": 1, "value": 12}, "sea_spray_crystal": {"quantity": 1, "value": 8}},
        "exits": {
            "west": {"target": "sunstone_palm_beach_east", "type": "direction"}
        }
    }

    rooms["sunstone_shell_beach"] = {
        "id": "sunstone_shell_beach",
        "name": "Shell Beach",
        "description": "A beach made entirely of shells — millions of them, in every colour "
                       "and shape imaginable. Walking on them produces a musical tinkling. "
                       "Collectors come here to find rare specimens, and the most valuable "
                       "shells are traded as currency among the island's children.",
        "coordinates": [cx, cy - 5],
        "location_type": "wilderness",
        "items": {"rare_conch_shell": {"quantity": 1, "value": 18}, "rainbow_shell": {"quantity": 1, "value": 12}},
        "exits": {
            "north": {"target": "sunstone_coral_beach", "type": "direction"}
        }
    }

    rooms["sunstone_beach_wreck"] = {
        "id": "sunstone_beach_wreck",
        "name": "Beached Shipwreck",
        "description": "The rusting hull of an old merchant vessel, half-buried in sand and "
                       "colonized by barnacles and crabs. The interior is accessible through "
                       "gaps in the hull, and scavengers have picked it over many times — but "
                       "new treasures still emerge as the sand shifts.",
        "coordinates": [cx - 2, cy - 5],
        "location_type": "wilderness",
        "items": {"rusty_ship_nail": {"quantity": 2, "value": 3}, "ships_log_fragment": {"quantity": 1, "value": 15}},
        "exits": {
            "north": {"target": "sunstone_beach_bonfire", "type": "direction"}
        }
    }

    rooms["sunstone_turtle_beach"] = {
        "id": "sunstone_turtle_beach",
        "name": "Turtle Nesting Beach",
        "description": "A quiet stretch of shore where sea turtles come to nest during the "
                       "full moon. The sand is marked with their tracks — wide, sweeping "
                       "patterns leading from the water to carefully dug nests. The villagers "
                       "protect this beach fiercely from any disturbance.",
        "coordinates": [cx + 1, cy - 6],
        "location_type": "wilderness",
        "items": {"turtle_shell_fragment": {"quantity": 1, "value": 10}, "nesting_sand": {"quantity": 1, "value": 5}},
        "exits": {
            "north": {"target": "sunstone_lagoon_deep", "type": "direction"}
        }
    }

    # --- Expanded Coral Lagoon (+6 rooms) ---

    rooms["sunstone_lagoon_garden"] = {
        "id": "sunstone_lagoon_garden",
        "name": "Coral Garden",
        "description": "A shallow section of the lagoon where coral grows in spectacular formations "
                       "— brain coral, staghorn coral, and delicate fan coral in shades of orange, "
                       "purple, and electric blue. Schools of tropical fish weave between the formations "
                       "in flashes of colour.",
        "coordinates": [cx + 2, cy - 5],
        "location_type": "wilderness",
        "items": {"coral_fragment": {"quantity": 1, "value": 12}, "tropical_fish_scale": {"quantity": 2, "value": 5}},
        "exits": {
            "west": {"target": "sunstone_lagoon_overlook", "type": "direction"},
            "south": {"target": "sunstone_lagoon_sandbar", "type": "direction"}
        }
    }

    rooms["sunstone_lagoon_sandbar"] = {
        "id": "sunstone_lagoon_sandbar",
        "name": "Sandy Sandbar",
        "description": "A narrow strip of white sand barely above the waterline, surrounded by "
                       "crystal-clear lagoon water. At low tide it's wide enough to walk; at "
                       "high tide it nearly disappears. The views in every direction are "
                       "spectacular — reef, lagoon, beach, and distant jungle.",
        "coordinates": [cx - 1, cy - 5],
        "location_type": "wilderness",
        "items": {"sandbar_sand": {"quantity": 1, "value": 3}, "tide_gem": {"quantity": 1, "value": 15}},
        "exits": {
            "north": {"target": "sunstone_lagoon_garden", "type": "direction"}
        }
    }

    rooms["sunstone_sea_cave_crystal"] = {
        "id": "sunstone_sea_cave_crystal",
        "name": "Crystal Grotto",
        "description": "Beyond the deep cave, a hidden grotto where the walls are encrusted "
                       "with natural crystals that catch and multiply any light source into "
                       "a thousand dancing reflections. The air is cool and still, and the "
                       "silence is broken only by the slow drip of mineral-rich water.",
        "coordinates": [cx - 6, cy - 8],
        "location_type": "wilderness",
        "items": {"grotto_crystal": {"quantity": 1, "value": 35}, "mineral_drop": {"quantity": 1, "value": 12}},
        "exits": {
            "north": {"target": "sunstone_sea_cave_deep", "type": "direction"},
            "south": {"target": "sunstone_crystal_pool", "type": "direction"}
        }
    }

    rooms["sunstone_crystal_pool"] = {
        "id": "sunstone_crystal_pool",
        "name": "Crystal Pool",
        "description": "A perfectly still pool at the bottom of the crystal grotto, its surface "
                       "reflecting the crystals above like a mirror. The water is preternaturally "
                       "clear, and at its bottom lies a collection of offerings — coins, jewellery, "
                       "and small carved figures — left by generations of islanders.",
        "coordinates": [cx - 7, cy - 8],
        "location_type": "wilderness",
        "items": {"pool_offering_coin": {"quantity": 1, "value": 18}, "carved_offering_figure": {"quantity": 1, "value": 22}},
        "exits": {
            "north": {"target": "sunstone_sea_cave_crystal", "type": "direction"}
        }
    }

    rooms["sunstone_reef_coral_wall"] = {
        "id": "sunstone_reef_coral_wall",
        "name": "Coral Wall Drop-Off",
        "description": "The reef drops away here in a sheer vertical wall of coral, plunging "
                       "into deep blue water. Larger fish patrol the wall's edge — barracuda, "
                       "reef sharks, and the occasional manta ray gliding past like a shadow. "
                       "The wall teems with colourful life.",
        "coordinates": [cx + 3, cy - 4],
        "location_type": "wilderness",
        "items": {"barracuda_scale": {"quantity": 1, "value": 15}, "deep_coral_piece": {"quantity": 1, "value": 20}},
        "exits": {
            "north": {"target": "sunstone_reef_edge", "type": "direction"}
        }
    }

    rooms["sunstone_lagoon_mangrove"] = {
        "id": "sunstone_lagoon_mangrove",
        "name": "Lagoon Mangroves",
        "description": "A stand of mangroves growing at the lagoon's edge, their tangled roots "
                       "creating a protected nursery for juvenile fish. The roots are draped "
                       "with oysters and the shallow water is warm and murky. Herons wade "
                       "through the shallows on stilt-like legs.",
        "coordinates": [cx, cy - 2],
        "location_type": "wilderness",
        "items": {"mangrove_oyster": {"quantity": 2, "value": 6}, "heron_feather": {"quantity": 1, "value": 8}},
        "exits": {
            "north": {"target": "sunstone_lagoon_path", "type": "direction"}
        }
    }

    # --- Expanded Jungle (+8 rooms) ---

    rooms["sunstone_canopy_observatory"] = {
        "id": "sunstone_canopy_observatory",
        "name": "Canopy Observatory",
        "description": "A wooden platform built high in the jungle canopy, accessible via a "
                       "rope ladder. From here, the entire atoll is visible — the ring of reef, "
                       "the lagoon, the village, and the distant volcanic hill. A brass telescope "
                       "is mounted on a swivel for observing ships at sea.",
        "coordinates": [cx + 4, cy + 1],
        "location_type": "building",
        "items": {"brass_telescope": {"quantity": 1, "value": 30}, "canopy_map": {"quantity": 1, "value": 15}},
        "exits": {
            "west": {"target": "sunstone_canopy_nest", "type": "direction"},
            "south": {"target": "sunstone_canopy_bridge", "type": "direction"}
        }
    }

    rooms["sunstone_canopy_bridge"] = {
        "id": "sunstone_canopy_bridge",
        "name": "Rope Canopy Bridge",
        "description": "A swaying rope bridge connecting two massive trees at canopy height. "
                       "The bridge offers vertigo-inducing views straight down through layers "
                       "of leaves and vines. Monkeys chatter from nearby branches, occasionally "
                       "swinging across the bridge path.",
        "coordinates": [cx + 5, cy - 1],
        "location_type": "wilderness",
        "items": {"monkey_fruit": {"quantity": 1, "value": 4}, "vine_rope": {"quantity": 1, "value": 8}},
        "exits": {
            "north": {"target": "sunstone_canopy_observatory", "type": "direction"}
        }
    }

    rooms["sunstone_grotto_depths"] = {
        "id": "sunstone_grotto_depths",
        "name": "Grotto of Sun Spirits",
        "description": "Deeper within the hidden grotto, a chamber where ancient sun priests "
                       "communed with nature spirits. Carvings of sun and wave adorn the walls, "
                       "and at certain times of day, light streams through a natural chimney "
                       "to illuminate a stone altar covered in dried flower offerings.",
        "coordinates": [cx + 5, cy - 2],
        "location_type": "wilderness",
        "items": {"sun_spirit_carving": {"quantity": 1, "value": 25}, "dried_offering_petals": {"quantity": 1, "value": 8}},
        "exits": {
            "north": {"target": "sunstone_hidden_grotto", "type": "direction"}
        }
    }

    rooms["sunstone_jungle_pond"] = {
        "id": "sunstone_jungle_pond",
        "name": "Jungle Pond",
        "description": "A still, dark pond surrounded by giant ferns and moss-covered logs. "
                       "Dragonflies hover over the surface and frogs chorus from the reeds. "
                       "The water is stained brown by tannins but perfectly drinkable. An "
                       "old stone bench sits at the water's edge.",
        "coordinates": [cx + 4, cy - 4],
        "location_type": "wilderness",
        "items": {"dragonfly_wing": {"quantity": 1, "value": 5}, "pond_water": {"quantity": 1, "value": 3}},
        "exits": {
            "south": {"target": "sunstone_jungle_stream", "type": "direction"},
            "east": {"target": "sunstone_jungle_ruins_path", "type": "direction"}
        }
    }

    rooms["sunstone_jungle_ruins_path"] = {
        "id": "sunstone_jungle_ruins_path",
        "name": "Overgrown Path",
        "description": "A path of ancient stone blocks, half-swallowed by jungle growth. The "
                       "blocks are carved with worn sun symbols, suggesting this was once a "
                       "processional route to the temple. Vines have woven a natural tunnel "
                       "overhead, creating a shaded corridor.",
        "coordinates": [cx + 4, cy - 3],
        "location_type": "wilderness",
        "items": {"carved_path_stone": {"quantity": 1, "value": 10}, "jungle_vine": {"quantity": 1, "value": 5}},
        "exits": {
            "west": {"target": "sunstone_jungle_pond", "type": "direction"}
        }
    }

    rooms["sunstone_jungle_spring"] = {
        "id": "sunstone_jungle_spring",
        "name": "Mountain Spring",
        "description": "A natural spring bubbling from the volcanic rock, feeding a small stream "
                       "that winds through the jungle. The water is mineral-rich and slightly warm, "
                       "and the rocks around the spring are tinted orange by iron deposits. Local "
                       "legend says drinking from it brings good luck.",
        "coordinates": [cx + 4, cy - 2],
        "location_type": "wilderness",
        "items": {"spring_water": {"quantity": 1, "value": 8}, "iron_stone": {"quantity": 1, "value": 6}},
        "exits": {
            "north": {"target": "sunstone_jungle_ruins_path", "type": "direction"}
        }
    }

    rooms["sunstone_jungle_clearing_south"] = {
        "id": "sunstone_jungle_clearing_south",
        "name": "Southern Jungle Clearing",
        "description": "A natural clearing where a fallen giant tree has created an opening in "
                       "the canopy. Sunlight streams down in golden shafts, nurturing a carpet "
                       "of wildflowers and ferns. Butterflies of impossible colours dance in "
                       "the light. The fallen trunk serves as a natural bridge and bench.",
        "coordinates": [cx + 5, cy - 3],
        "location_type": "wilderness",
        "items": {"wildflower_bouquet": {"quantity": 1, "value": 6}, "fallen_bark": {"quantity": 1, "value": 3}},
        "exits": {
            "east": {"target": "sunstone_jungle_spring", "type": "direction"},
            "north": {"target": "sunstone_jungle_pond", "type": "direction"}
        }
    }

    rooms["sunstone_jungle_ancient_tree"] = {
        "id": "sunstone_jungle_ancient_tree",
        "name": "Ancient Banyan Tree",
        "description": "A banyan tree of extraordinary age, its aerial roots forming a maze "
                       "of woody columns around the original trunk. The tree is easily three "
                       "hundred years old and has become a sacred site — offerings and prayers "
                       "are tied to its branches on colourful ribbons.",
        "coordinates": [cx + 2, cy + 3],
        "location_type": "wilderness",
        "items": {"prayer_ribbon": {"quantity": 1, "value": 5}, "banyan_fruit": {"quantity": 1, "value": 3}},
        "exits": {
            "west": {"target": "sunstone_ancient_road", "type": "direction"}
        }
    }

    # --- Expanded Sun Temple Ruins (+6 rooms) ---

    rooms["sunstone_temple_meditation"] = {
        "id": "sunstone_temple_meditation",
        "name": "Meditation Terrace",
        "description": "A stone terrace overlooking the jungle canopy, where sun priests once "
                       "meditated at dawn and dusk. The terrace is oriented perfectly east-west, "
                       "and the sunrise view is said to be transcendent. Stone cushion-seats "
                       "are worn smooth by centuries of use.",
        "coordinates": [cx + 2, cy + 4],
        "location_type": "wilderness",
        "items": {"meditation_stone": {"quantity": 1, "value": 12}, "dawn_incense": {"quantity": 1, "value": 8}},
        "exits": {
            "west": {"target": "sunstone_temple_gate", "type": "direction"}
        }
    }

    rooms["sunstone_temple_sundial"] = {
        "id": "sunstone_temple_sundial",
        "name": "Grand Sundial",
        "description": "An enormous sundial carved from a single block of golden stone, still "
                       "perfectly accurate after millennia. The gnomon casts its shadow across "
                       "a dial marked not just with hours but with celestial events, seasons, "
                       "and dates that correspond to no known calendar.",
        "coordinates": [cx + 2, cy + 5],
        "location_type": "wilderness",
        "items": {"sundial_gnomon_chip": {"quantity": 1, "value": 25}, "golden_stone_fragment": {"quantity": 1, "value": 15}},
        "exits": {
            "west": {"target": "sunstone_temple_courtyard", "type": "direction"}
        }
    }

    rooms["sunstone_temple_bath"] = {
        "id": "sunstone_temple_bath",
        "name": "Priests' Ritual Bath",
        "description": "A sunken bath of polished stone where priests purified themselves before "
                       "ceremonies. The bath is fed by a natural warm spring, and the water still "
                       "flows. The steam carries a faint scent of flowers, and the stone is "
                       "stained gold by centuries of mineral deposits.",
        "coordinates": [cx - 1, cy + 5],
        "location_type": "building",
        "items": {"mineral_bath_water": {"quantity": 1, "value": 10}, "gold_stained_stone": {"quantity": 1, "value": 18}},
        "exits": {
            "east": {"target": "sunstone_temple_west_wing", "type": "direction"}
        }
    }

    rooms["sunstone_temple_solar_room"] = {
        "id": "sunstone_temple_solar_room",
        "name": "Solar Alignment Chamber",
        "description": "A chamber designed so that on the solstice, sunlight enters through a "
                       "single narrow slit and illuminates a golden disc on the far wall. The "
                       "effect is breathtaking — the entire room floods with reflected golden "
                       "light. Even on ordinary days, the architecture is awe-inspiring.",
        "coordinates": [cx + 2, cy + 6],
        "location_type": "building",
        "items": {"golden_disc_fragment": {"quantity": 1, "value": 35}, "solstice_prism": {"quantity": 1, "value": 28}},
        "exits": {
            "west": {"target": "sunstone_temple_sanctuary", "type": "direction"}
        }
    }

    rooms["sunstone_temple_star_map"] = {
        "id": "sunstone_temple_star_map",
        "name": "Star Map Chamber",
        "description": "A domed ceiling painted with a star map of extraordinary accuracy, "
                       "depicting constellations, planets, and celestial bodies — some of "
                       "which modern astronomers have only recently discovered. The ancient "
                       "priests clearly possessed knowledge far beyond their era.",
        "coordinates": [cx - 1, cy + 6],
        "location_type": "building",
        "items": {"star_chart": {"quantity": 1, "value": 30}, "celestial_paint_flake": {"quantity": 1, "value": 12}},
        "exits": {
            "east": {"target": "sunstone_temple_library", "type": "direction"}
        }
    }

    rooms["sunstone_temple_collapsed"] = {
        "id": "sunstone_temple_collapsed",
        "name": "Collapsed Gallery",
        "description": "A section of the temple where the roof has caved in, allowing jungle "
                       "to reclaim the space. Vines drape from broken pillars, ferns sprout "
                       "from between flagstones, and a tree grows from what was once the altar. "
                       "Nature and architecture have merged into something beautiful.",
        "coordinates": [cx + 3, cy + 6],
        "location_type": "wilderness",
        "items": {"broken_pillar_piece": {"quantity": 1, "value": 10}, "temple_vine_flower": {"quantity": 1, "value": 8}},
        "exits": {
            "west": {"target": "sunstone_temple_sanctuary", "type": "direction"},
            "north": {"target": "sunstone_temple_treasury", "type": "direction"}
        }
    }

    # --- Expanded Hidden Coves (+5 rooms) ---

    rooms["sunstone_smuggler_tunnel"] = {
        "id": "sunstone_smuggler_tunnel",
        "name": "Smuggler's Tunnel",
        "description": "A hand-carved tunnel leading from the smuggler's cave deeper into the "
                       "island. The walls bear chisel marks and the occasional scratched arrow "
                       "pointing the way. Niches in the walls once held lanterns. The tunnel "
                       "smells of salt, damp, and old rum.",
        "coordinates": [cx - 6, cy - 6],
        "location_type": "wilderness",
        "items": {"smuggler_map_fragment": {"quantity": 1, "value": 20}, "old_lantern": {"quantity": 1, "value": 8}},
        "exits": {
            "north": {"target": "sunstone_smuggler_cave", "type": "direction"},
            "east": {"target": "sunstone_smuggler_stash", "type": "direction"}
        }
    }

    rooms["sunstone_smuggler_stash"] = {
        "id": "sunstone_smuggler_stash",
        "name": "Hidden Stash Chamber",
        "description": "A concealed chamber at the end of the tunnel where smugglers stored "
                       "their most valuable cargo. A few old crates remain, their contents "
                       "long since removed — but a false bottom in the floor conceals a "
                       "compartment that might still hold treasure.",
        "coordinates": [cx - 5, cy - 6],
        "location_type": "building",
        "items": {"false_bottom_key": {"quantity": 1, "value": 15}, "old_spice_trade_sample": {"quantity": 1, "value": 22}},
        "exits": {
            "west": {"target": "sunstone_smuggler_tunnel", "type": "direction"}
        }
    }

    rooms["sunstone_sunset_arch"] = {
        "id": "sunstone_sunset_arch",
        "name": "Sunset Stone Arch",
        "description": "A natural stone arch carved by wind and waves, framing the western "
                       "horizon perfectly. At sunset, the arch creates a golden frame around "
                       "the sinking sun — a spectacle that draws visitors from across the "
                       "atoll. The rocks are warm from a full day of tropical sun.",
        "coordinates": [cx - 7, cy - 3],
        "location_type": "wilderness",
        "items": {"sunset_stone": {"quantity": 1, "value": 12}, "warm_arch_pebble": {"quantity": 1, "value": 5}},
        "exits": {
            "east": {"target": "sunstone_sunset_point", "type": "direction"},
            "south": {"target": "sunstone_sunset_reef", "type": "direction"}
        }
    }

    rooms["sunstone_sunset_reef"] = {
        "id": "sunstone_sunset_reef",
        "name": "Sunset Reef",
        "description": "A reef visible from the sunset arch, painted gold and orange by the "
                       "setting sun. At twilight, the reef comes alive with nocturnal creatures "
                       "emerging for the night hunt. The transition between day and night reef "
                       "life is one of nature's most dramatic shows.",
        "coordinates": [cx - 7, cy - 4],
        "location_type": "wilderness",
        "items": {"sunset_coral": {"quantity": 1, "value": 15}, "nocturnal_sea_creature": {"quantity": 1, "value": 18}},
        "exits": {
            "north": {"target": "sunstone_sunset_arch", "type": "direction"}
        }
    }

    rooms["sunstone_tidal_deep"] = {
        "id": "sunstone_tidal_deep",
        "name": "Deep Tidal Pool",
        "description": "A large, deep tidal pool connected to the ocean by an underwater "
                       "channel. The pool functions as a natural aquarium, trapping a "
                       "rotating selection of sea creatures with each tide cycle. Today "
                       "a small octopus explores the pool's edges with curious tentacles.",
        "coordinates": [cx - 6, cy - 1],
        "location_type": "wilderness",
        "items": {"octopus_ink": {"quantity": 1, "value": 12}, "tidal_pool_specimen": {"quantity": 1, "value": 10}},
        "exits": {
            "east": {"target": "sunstone_tidal_cave", "type": "direction"}
        }
    }

    # --- Expanded Volcanic Hill (+5 rooms) ---

    rooms["sunstone_volcanic_crater"] = {
        "id": "sunstone_volcanic_crater",
        "name": "Volcanic Crater",
        "description": "The dormant crater at the volcano's peak, a shallow bowl of darkite "
                       "rock with wisps of steam rising from vents. The crater floor is "
                       "surprisingly hospitable — hardy plants grow in the mineral-rich soil, "
                       "and a small lake of warm, mineral-blue water fills the lowest point.",
        "coordinates": [cx + 4, cy + 6],
        "location_type": "wilderness",
        "items": {"volcanic_mineral": {"quantity": 1, "value": 20}, "crater_water": {"quantity": 1, "value": 10}},
        "exits": {
            "south": {"target": "sunstone_volcanic_summit", "type": "direction"},
            "east": {"target": "sunstone_volcanic_vent_field", "type": "direction"}
        }
    }

    rooms["sunstone_volcanic_vent_field"] = {
        "id": "sunstone_volcanic_vent_field",
        "name": "Steam Vent Field",
        "description": "A field of fumaroles and steam vents on the volcano's flank, each "
                       "billowing clouds of sulphurous steam. The ground is warm underfoot "
                       "and stained yellow by mineral deposits. The vents hiss and gurgle "
                       "like a living thing breathing through the earth.",
        "coordinates": [cx + 5, cy + 6],
        "location_type": "wilderness",
        "items": {"sulphur_crystal": {"quantity": 1, "value": 15}, "vent_stone": {"quantity": 1, "value": 8}},
        "exits": {
            "west": {"target": "sunstone_volcanic_crater", "type": "direction"}
        }
    }

    rooms["sunstone_lava_tube"] = {
        "id": "sunstone_lava_tube",
        "name": "Ancient Lava Tube",
        "description": "A tunnel carved by flowing lava thousands of years ago, its walls "
                       "smoothed and glazed to a glassy finish. The tube winds through the "
                       "volcano's interior, occasionally opening into chambers where the lava "
                       "pooled and cooled. Stalactites of volcanic glass hang from the ceiling.",
        "coordinates": [cx + 5, cy + 4],
        "location_type": "wilderness",
        "items": {"volcanic_glass_stalactite": {"quantity": 1, "value": 22}, "lava_tube_stone": {"quantity": 1, "value": 10}},
        "exits": {
            "north": {"target": "sunstone_volcanic_slope", "type": "direction"},
            "east": {"target": "sunstone_lava_tube_end", "type": "direction"}
        }
    }

    rooms["sunstone_lava_tube_end"] = {
        "id": "sunstone_lava_tube_end",
        "name": "Lava Tube Gallery",
        "description": "The deepest accessible point of the lava tube, where the tunnel opens "
                       "into a natural gallery of volcanic formations. Pillars of cooled lava "
                       "support the ceiling, and the walls sparkle with embedded crystals. "
                       "The silence here is absolute and almost sacred.",
        "coordinates": [cx + 6, cy + 4],
        "location_type": "wilderness",
        "items": {"embedded_crystal": {"quantity": 1, "value": 28}, "lava_pillar_chip": {"quantity": 1, "value": 12}},
        "exits": {
            "west": {"target": "sunstone_lava_tube", "type": "direction"}
        }
    }

    rooms["sunstone_volcanic_garden"] = {
        "id": "sunstone_volcanic_garden",
        "name": "Volcanic Flower Garden",
        "description": "A garden of heat-loving plants that thrive in the volcanic soil — fire "
                       "lilies with orange-red petals, sulphur orchids in vivid yellow, and "
                       "stone roses that grow from cracks in the cooled lava. The warm ground "
                       "creates a microclimate where tropical flowers bloom year-round.",
        "coordinates": [cx + 5, cy + 2],
        "location_type": "wilderness",
        "items": {"fire_lily": {"quantity": 1, "value": 15}, "sulphur_orchid": {"quantity": 1, "value": 18}},
        "exits": {
            "south": {"target": "sunstone_hot_springs", "type": "direction"}
        }
    }

    # === NEW SUB-REGION: Sunken Reef Caves (16 rooms) ===

    rooms["sunstone_reef_cave_entrance"] = {
        "id": "sunstone_reef_cave_entrance",
        "name": "Reef Cave Entrance",
        "description": "A crack in the reef wall leads to an underwater cave system. The entrance "
                       "is partially concealed by waving sea fans and guarded by a territorial "
                       "moray eel. Beyond, the water is calm and illuminated by bioluminescent "
                       "plankton that coat the ceiling like underwater stars.",
        "coordinates": [cx + 3, cy - 5],
        "location_type": "wilderness",
        "items": {"sea_fan": {"quantity": 1, "value": 10}, "bioluminescent_plankton": {"quantity": 1, "value": 15}},
        "exits": {
            "north": {"target": "sunstone_reef_edge", "type": "direction"},
            "south": {"target": "sunstone_reef_cave_passage", "type": "direction"}
        }
    }

    rooms["sunstone_reef_cave_passage"] = {
        "id": "sunstone_reef_cave_passage",
        "name": "Luminous Passage",
        "description": "A winding passage through the reef, lit by colonies of bioluminescent "
                       "organisms in blue and green. The cave walls are alive with life — sponges, "
                       "tunicates, and tiny shrimp that dart away from light. The water is "
                       "remarkably clear, offering visibility of thirty feet.",
        "coordinates": [cx + 3, cy - 6],
        "location_type": "wilderness",
        "items": {"luminous_sponge": {"quantity": 1, "value": 12}, "cave_shrimp": {"quantity": 1, "value": 5}},
        "exits": {
            "north": {"target": "sunstone_reef_cave_entrance", "type": "direction"},
            "east": {"target": "sunstone_reef_cave_grotto", "type": "direction"},
            "south": {"target": "sunstone_reef_cave_deep", "type": "direction"}
        }
    }

    rooms["sunstone_reef_cave_grotto"] = {
        "id": "sunstone_reef_cave_grotto",
        "name": "Pearl Grotto",
        "description": "A small grotto where oysters grow in dense clusters on every surface. "
                       "Some have been growing for decades, producing pearls of unusual size "
                       "and colour. The locals consider this a sacred place and only harvest "
                       "pearls as gifts for significant occasions.",
        "coordinates": [cx + 4, cy - 6],
        "location_type": "wilderness",
        "items": {"large_pearl": {"quantity": 1, "value": 35}, "pearl_oyster_shell": {"quantity": 1, "value": 10}},
        "exits": {
            "west": {"target": "sunstone_reef_cave_passage", "type": "direction"}
        }
    }

    rooms["sunstone_reef_cave_deep"] = {
        "id": "sunstone_reef_cave_deep",
        "name": "Deep Reef Chamber",
        "description": "A large chamber deep within the reef, its ceiling covered in translucent "
                       "stalactites that glow faintly with trapped minerals. Schools of glass "
                       "fish swirl through the space like living clouds. An underwater current "
                       "gently circulates the warm, clear water.",
        "coordinates": [cx + 3, cy - 7],
        "location_type": "wilderness",
        "items": {"glass_fish_scale": {"quantity": 1, "value": 8}, "glowing_stalactite_chip": {"quantity": 1, "value": 18}},
        "exits": {
            "north": {"target": "sunstone_reef_cave_passage", "type": "direction"},
            "east": {"target": "sunstone_reef_cave_turtle", "type": "direction"},
            "west": {"target": "sunstone_reef_cave_coral_room", "type": "direction"}
        }
    }

    rooms["sunstone_reef_cave_turtle"] = {
        "id": "sunstone_reef_cave_turtle",
        "name": "Sea Turtle Resting Pool",
        "description": "A still pool within the reef where old sea turtles come to rest. The "
                       "water is warm and protected from currents. Several massive green turtles "
                       "float serenely, their barnacle-encrusted shells marking decades of ocean "
                       "travel. They regard visitors with ancient, knowing eyes.",
        "coordinates": [cx + 4, cy - 7],
        "location_type": "wilderness",
        "items": {"turtle_barnacle": {"quantity": 1, "value": 8}, "sea_turtle_scale": {"quantity": 1, "value": 15}},
        "exits": {
            "west": {"target": "sunstone_reef_cave_deep", "type": "direction"}
        }
    }

    rooms["sunstone_reef_cave_coral_room"] = {
        "id": "sunstone_reef_cave_coral_room",
        "name": "Black Coral Chamber",
        "description": "A chamber where rare black coral grows in branching formations that "
                       "look like underwater trees. Black coral grows incredibly slowly — these "
                       "formations are thousands of years old. The coral is valuable but "
                       "protected by island law and fierce local sentiment.",
        "coordinates": [cx + 2, cy - 7],
        "location_type": "wilderness",
        "items": {"black_coral_fragment": {"quantity": 1, "value": 40}, "cave_floor_sediment": {"quantity": 1, "value": 5}},
        "exits": {
            "east": {"target": "sunstone_reef_cave_deep", "type": "direction"},
            "south": {"target": "sunstone_reef_cave_junction", "type": "direction"}
        }
    }

    rooms["sunstone_reef_cave_junction"] = {
        "id": "sunstone_reef_cave_junction",
        "name": "Cave Junction",
        "description": "A junction where three reef cave passages meet. The water currents "
                       "swirl here, creating gentle eddies that deposit fine sand on a small "
                       "ledge. Marker stones have been placed by previous explorers to help "
                       "with navigation in the maze-like system.",
        "coordinates": [cx + 2, cy - 8],
        "location_type": "wilderness",
        "items": {"marker_stone": {"quantity": 1, "value": 5}, "junction_sand": {"quantity": 1, "value": 3}},
        "exits": {
            "north": {"target": "sunstone_reef_cave_coral_room", "type": "direction"},
            "east": {"target": "sunstone_reef_cave_sunbeam", "type": "direction"},
            "west": {"target": "sunstone_reef_cave_anemone", "type": "direction"}
        }
    }

    rooms["sunstone_reef_cave_sunbeam"] = {
        "id": "sunstone_reef_cave_sunbeam",
        "name": "Sunbeam Chamber",
        "description": "A cave room where a crack in the reef above allows a single shaft of "
                       "sunlight to pierce the water, creating a pillar of golden light. The "
                       "beam illuminates a patch of cave floor where brilliant green algae "
                       "grows, fed by the precious light. Fish gather in the beam.",
        "coordinates": [cx + 3, cy - 8],
        "location_type": "wilderness",
        "items": {"sunbeam_algae": {"quantity": 1, "value": 10}, "light_crystal": {"quantity": 1, "value": 20}},
        "exits": {
            "west": {"target": "sunstone_reef_cave_junction", "type": "direction"}
        }
    }

    rooms["sunstone_reef_cave_anemone"] = {
        "id": "sunstone_reef_cave_anemone",
        "name": "Anemone Garden",
        "description": "The walls and floor of this chamber are covered in sea anemones of "
                       "every colour — pink, purple, orange, and electric green. Clownfish "
                       "dart between them, immune to the anemones' stinging tentacles. The "
                       "effect is like being inside a living kaleidoscope.",
        "coordinates": [cx + 1, cy - 8],
        "location_type": "wilderness",
        "items": {"anemone_extract": {"quantity": 1, "value": 15}, "clownfish_scale": {"quantity": 1, "value": 8}},
        "exits": {
            "east": {"target": "sunstone_reef_cave_junction", "type": "direction"},
            "south": {"target": "sunstone_reef_cave_arch", "type": "direction"}
        }
    }

    rooms["sunstone_reef_cave_arch"] = {
        "id": "sunstone_reef_cave_arch",
        "name": "Natural Arch Chamber",
        "description": "A chamber dominated by a natural stone arch that frames a passage to "
                       "deeper caves. The arch is decorated with natural mineral stains in "
                       "rust red and mineral green, creating an accidental work of art. "
                       "The water beyond the arch is noticeably deeper and cooler.",
        "coordinates": [cx + 1, cy - 9],
        "location_type": "wilderness",
        "items": {"mineral_stain_sample": {"quantity": 1, "value": 8}, "arch_stone": {"quantity": 1, "value": 10}},
        "exits": {
            "north": {"target": "sunstone_reef_cave_anemone", "type": "direction"},
            "east": {"target": "sunstone_reef_cave_echo", "type": "direction"}
        }
    }

    rooms["sunstone_reef_cave_echo"] = {
        "id": "sunstone_reef_cave_echo",
        "name": "Echo Chamber",
        "description": "An air pocket in the reef creates a natural echo chamber above the "
                       "waterline. Sounds are amplified and repeated, creating an eerie "
                       "chorus from even small noises. Islanders tell stories of hearing "
                       "voices here — the spirits of drowned sailors, they say.",
        "coordinates": [cx + 2, cy - 9],
        "location_type": "wilderness",
        "items": {"echo_shell": {"quantity": 1, "value": 12}, "spirit_candle": {"quantity": 1, "value": 8}},
        "exits": {
            "west": {"target": "sunstone_reef_cave_arch", "type": "direction"},
            "south": {"target": "sunstone_reef_cave_treasure", "type": "direction"}
        }
    }

    rooms["sunstone_reef_cave_treasure"] = {
        "id": "sunstone_reef_cave_treasure",
        "name": "Treasure Ledge",
        "description": "A natural ledge above the waterline where someone — perhaps the "
                       "smugglers — cached a small fortune in trade goods. The cache has been "
                       "partially looted but some items remain: exotic spices in sealed jars, "
                       "bolts of waterproofed silk, and a chest of antique navigation tools.",
        "coordinates": [cx + 2, cy - 10],
        "location_type": "building",
        "items": {"exotic_spice_jar": {"quantity": 1, "value": 25}, "waterproof_silk": {"quantity": 1, "value": 30}, "antique_sextant": {"quantity": 1, "value": 40}},
        "exits": {
            "north": {"target": "sunstone_reef_cave_echo", "type": "direction"}
        }
    }

    rooms["sunstone_reef_cave_manta"] = {
        "id": "sunstone_reef_cave_manta",
        "name": "Manta Ray Cavern",
        "description": "A vast underwater cavern where manta rays gather — their wingspans up "
                       "to twelve feet, gliding through the water with effortless grace. The "
                       "cavern is deep enough that the mantas can perform their characteristic "
                       "barrel rolls as they filter feed in the plankton-rich water.",
        "coordinates": [cx + 4, cy - 8],
        "location_type": "wilderness",
        "items": {"manta_skin_sample": {"quantity": 1, "value": 20}, "plankton_sample": {"quantity": 1, "value": 8}},
        "exits": {
            "west": {"target": "sunstone_reef_cave_sunbeam", "type": "direction"}
        }
    }

    rooms["sunstone_reef_cave_lobster"] = {
        "id": "sunstone_reef_cave_lobster",
        "name": "Lobster Den",
        "description": "A maze of small cave rooms populated by spiny lobsters of impressive "
                       "size. The lobsters emerge from hiding at dusk, their antennae waving "
                       "as they patrol their territory. Catching them is a rite of passage "
                       "for young islanders, requiring patience and quick hands.",
        "coordinates": [cx + 4, cy - 5],
        "location_type": "wilderness",
        "items": {"spiny_lobster": {"quantity": 1, "value": 12}, "lobster_antenna": {"quantity": 1, "value": 5}},
        "exits": {
            "west": {"target": "sunstone_reef_cave_entrance", "type": "direction"}
        }
    }

    # === NEW SUB-REGION: Ancient Observatory (15 rooms) ===

    rooms["sunstone_observatory_trail"] = {
        "id": "sunstone_observatory_trail",
        "name": "Observatory Trail",
        "description": "A well-worn path winding up the island's highest point, marked by "
                       "ancient stone cairns. The air grows cooler as you climb, and the "
                       "vegetation thins from dense jungle to hardy shrubs. Views of the "
                       "entire atoll unfold with each switchback.",
        "coordinates": [cx + 5, cy + 5],
        "location_type": "wilderness",
        "items": {"trail_cairn_stone": {"quantity": 1, "value": 5}, "highland_herb": {"quantity": 1, "value": 8}},
        "exits": {
            "west": {"target": "sunstone_volcanic_summit", "type": "direction"},
            "north": {"target": "sunstone_observatory_platform", "type": "direction"}
        }
    }

    rooms["sunstone_observatory_platform"] = {
        "id": "sunstone_observatory_platform",
        "name": "Observation Platform",
        "description": "A flat stone platform at the island's summit, perfectly level and "
                       "oriented to the cardinal directions. Grooves in the stone once held "
                       "astronomical instruments. On clear nights, the stars here are so "
                       "bright they cast shadows.",
        "coordinates": [cx + 5, cy + 8],
        "location_type": "building",
        "items": {"star_viewing_stone": {"quantity": 1, "value": 15}, "instrument_groove_rubbing": {"quantity": 1, "value": 10}},
        "exits": {
            "south": {"target": "sunstone_observatory_trail", "type": "direction"},
            "east": {"target": "sunstone_observatory_dome", "type": "direction"},
            "north": {"target": "sunstone_observatory_terrace", "type": "direction"}
        }
    }

    rooms["sunstone_observatory_dome"] = {
        "id": "sunstone_observatory_dome",
        "name": "Ruined Observatory Dome",
        "description": "The remains of a domed structure that once housed the ancient priests' "
                       "most sophisticated instruments for watching the heavens. The dome is "
                       "partially collapsed, but enough survives to show its ingenious design — "
                       "a rotating stone cap that could be aligned to any point in the sky.",
        "coordinates": [cx + 6, cy + 6],
        "location_type": "building",
        "items": {"dome_mechanism_gear": {"quantity": 1, "value": 30}, "star_glass_lens": {"quantity": 1, "value": 25}},
        "exits": {
            "west": {"target": "sunstone_observatory_platform", "type": "direction"},
            "south": {"target": "sunstone_observatory_workshop", "type": "direction"}
        }
    }

    rooms["sunstone_observatory_workshop"] = {
        "id": "sunstone_observatory_workshop",
        "name": "Instrument Workshop",
        "description": "A workshop where the ancient astronomers built and repaired their "
                       "instruments. Stone workbenches bear the marks of precision tools, "
                       "and drawers still contain fragments of lenses, gears, and calibration "
                       "weights of remarkable sophistication.",
        "coordinates": [cx + 6, cy + 5],
        "location_type": "building",
        "items": {"precision_weight": {"quantity": 1, "value": 18}, "lens_fragment": {"quantity": 1, "value": 22}},
        "exits": {
            "north": {"target": "sunstone_observatory_dome", "type": "direction"}
        }
    }

    rooms["sunstone_observatory_terrace"] = {
        "id": "sunstone_observatory_terrace",
        "name": "Stargazing Terrace",
        "description": "A broad terrace with stone seating arranged in semicircles, where "
                       "priests once taught astronomy to initiates under the night sky. The "
                       "terrace faces north, away from the island's light sources, providing "
                       "an unobstructed view of the celestial pole.",
        "coordinates": [cx + 5, cy + 7],
        "location_type": "building",
        "items": {"teaching_stone_tablet": {"quantity": 1, "value": 15}, "celestial_pole_marker": {"quantity": 1, "value": 20}},
        "exits": {
            "south": {"target": "sunstone_observatory_platform", "type": "direction"},
            "east": {"target": "sunstone_observatory_moon_room", "type": "direction"},
            "west": {"target": "sunstone_observatory_wind_cave", "type": "direction"}
        }
    }

    rooms["sunstone_observatory_moon_room"] = {
        "id": "sunstone_observatory_moon_room",
        "name": "Moon Phase Chamber",
        "description": "A chamber with small windows arranged to track the moon's phases "
                       "throughout the month. Each window illuminates a different marker on "
                       "the floor, and the complete cycle creates a lunar calendar of "
                       "extraordinary precision. The chamber is cool and dark.",
        "coordinates": [cx + 6, cy + 7],
        "location_type": "building",
        "items": {"moon_phase_marker": {"quantity": 1, "value": 22}, "lunar_calendar_stone": {"quantity": 1, "value": 30}},
        "exits": {
            "west": {"target": "sunstone_observatory_terrace", "type": "direction"}
        }
    }

    rooms["sunstone_observatory_wind_cave"] = {
        "id": "sunstone_observatory_wind_cave",
        "name": "Wind Cave",
        "description": "A natural cave below the terrace where wind patterns are channelled "
                       "through narrow passages, creating musical tones that vary with weather "
                       "conditions. The ancient priests used these sounds to predict storms "
                       "and changing seasons with remarkable accuracy.",
        "coordinates": [cx + 4, cy + 7],
        "location_type": "wilderness",
        "items": {"wind_chime_stone": {"quantity": 1, "value": 15}, "weather_prediction_chart": {"quantity": 1, "value": 18}},
        "exits": {
            "east": {"target": "sunstone_observatory_terrace", "type": "direction"},
            "south": {"target": "sunstone_observatory_meditation_pool", "type": "direction"}
        }
    }

    rooms["sunstone_observatory_meditation_pool"] = {
        "id": "sunstone_observatory_meditation_pool",
        "name": "Reflection Pool",
        "description": "A perfectly still pool of water in a stone basin, used by the priests "
                       "as a natural mirror for observing the night sky. The pool's surface is "
                       "so calm it creates perfect reflections of the stars above, doubling "
                       "the visible sky and making observation possible without neck strain.",
        "coordinates": [cx + 4, cy + 8],
        "location_type": "wilderness",
        "items": {"star_reflection_water": {"quantity": 1, "value": 10}, "basin_stone_chip": {"quantity": 1, "value": 5}},
        "exits": {
            "north": {"target": "sunstone_observatory_wind_cave", "type": "direction"}
        }
    }

    rooms["sunstone_observatory_solstice_pillar"] = {
        "id": "sunstone_observatory_solstice_pillar",
        "name": "Solstice Pillar",
        "description": "A tall stone pillar precisely placed to cast its shadow on specific "
                       "markers during the solstices and equinoxes. The pillar is carved with "
                       "a spiral that tracks the sun's annual journey across the sky. At its "
                       "base, offerings of sun-dried flowers and amber resin still appear.",
        "coordinates": [cx + 6, cy + 3],
        "location_type": "wilderness",
        "items": {"solstice_marker_stone": {"quantity": 1, "value": 18}, "amber_resin_offering": {"quantity": 1, "value": 12}},
        "exits": {
            "north": {"target": "sunstone_observatory_workshop", "type": "direction"},
            "west": {"target": "sunstone_hot_springs", "type": "direction"}
        }
    }

    rooms["sunstone_observatory_sun_throne"] = {
        "id": "sunstone_observatory_sun_throne",
        "name": "Sun Throne",
        "description": "A stone throne carved into the mountainside, positioned so that the "
                       "rising sun strikes the seated figure full in the face on the spring "
                       "equinox. The throne is massive — built for ceremony, not comfort. "
                       "The view from the throne encompasses the entire eastern horizon.",
        "coordinates": [cx + 6, cy + 2],
        "location_type": "building",
        "items": {"throne_armrest_carving": {"quantity": 1, "value": 20}, "equinox_sun_crystal": {"quantity": 1, "value": 30}},
        "exits": {
            "north": {"target": "sunstone_observatory_solstice_pillar", "type": "direction"}
        }
    }

    rooms["sunstone_observatory_calendar_wall"] = {
        "id": "sunstone_observatory_calendar_wall",
        "name": "Calendar Wall",
        "description": "An enormous wall carved with a calendar of astonishing complexity — "
                       "tracking not just days and months but eclipses, planetary conjunctions, "
                       "and astronomical events centuries into the future. Some predicted events "
                       "have proven accurate, raising questions about the builders' knowledge.",
        "coordinates": [cx + 6, cy + 1],
        "location_type": "building",
        "items": {"calendar_stone_fragment": {"quantity": 1, "value": 22}, "eclipse_prediction_tablet": {"quantity": 1, "value": 35}},
        "exits": {
            "south": {"target": "sunstone_observatory_sun_throne", "type": "direction"}
        }
    }

    rooms["sunstone_observatory_offering_circle"] = {
        "id": "sunstone_observatory_offering_circle",
        "name": "Offering Circle",
        "description": "A circle of standing stones where the ancient priests made offerings "
                       "to the sun. The stones are arranged to create specific light patterns "
                       "at different times of year. Fresh flowers appear among the old "
                       "offerings, suggesting someone still maintains the tradition.",
        "coordinates": [cx + 6, cy],
        "location_type": "wilderness",
        "items": {"standing_stone_chip": {"quantity": 1, "value": 10}, "sun_offering_flower": {"quantity": 1, "value": 6}},
        "exits": {
            "south": {"target": "sunstone_observatory_calendar_wall", "type": "direction"},
            "west": {"target": "sunstone_temple_garden", "type": "direction"}
        }
    }

    rooms["sunstone_observatory_echo_plaza"] = {
        "id": "sunstone_observatory_echo_plaza",
        "name": "Echo Plaza",
        "description": "A paved plaza where the stone layout creates acoustic effects — whispers "
                       "at one end can be heard clearly at the other, thirty yards away. The "
                       "priests used this for ceremonies and communication. The technology "
                       "is simple but the precision of execution is remarkable.",
        "coordinates": [cx + 7, cy + 5],
        "location_type": "building",
        "items": {"acoustic_stone": {"quantity": 1, "value": 12}, "echo_plaza_tile": {"quantity": 1, "value": 8}},
        "exits": {
            "west": {"target": "sunstone_observatory_workshop", "type": "direction"}
        }
    }

    rooms["sunstone_observatory_horizon_ring"] = {
        "id": "sunstone_observatory_horizon_ring",
        "name": "Horizon Ring",
        "description": "A circular stone structure with notches cut precisely along its rim, "
                       "each notch aligned with a significant point on the horizon — where "
                       "the sun rises and sets at different times of year, where particular "
                       "stars first appear, and where other islands are located.",
        "coordinates": [cx + 7, cy + 6],
        "location_type": "building",
        "items": {"horizon_notch_stone": {"quantity": 1, "value": 20}, "alignment_marker": {"quantity": 1, "value": 15}},
        "exits": {
            "west": {"target": "sunstone_observatory_dome", "type": "direction"}
        }
    }

    rooms["sunstone_observatory_comet_hall"] = {
        "id": "sunstone_observatory_comet_hall",
        "name": "Comet Hall",
        "description": "A long hall with a vaulted ceiling painted with depictions of comets "
                       "observed over centuries. Each comet is recorded with its date, trajectory, "
                       "and the events that followed its appearance. The oldest paintings are "
                       "faded but still legible, spanning over a thousand years of observation.",
        "coordinates": [cx + 7, cy + 7],
        "location_type": "building",
        "items": {"comet_painting_fragment": {"quantity": 1, "value": 25}, "ancient_star_chart": {"quantity": 1, "value": 30}},
        "exits": {
            "west": {"target": "sunstone_observatory_moon_room", "type": "direction"}
        }
    }

    rooms["sunstone_reef_cave_jellyfish"] = {
        "id": "sunstone_reef_cave_jellyfish",
        "name": "Jellyfish Gallery",
        "description": "A cave chamber where moon jellyfish drift in gentle currents, their "
                       "translucent bells pulsing with ethereal bioluminescence. Hundreds of "
                       "them fill the space like living lanterns, casting shifting blue-purple "
                       "light across the cave walls in a hypnotic display.",
        "coordinates": [cx + 5, cy - 7],
        "location_type": "wilderness",
        "items": {"jellyfish_essence": {"quantity": 1, "value": 18}, "bioluminescent_water": {"quantity": 1, "value": 12}},
        "exits": {
            "west": {"target": "sunstone_reef_cave_deep", "type": "direction"}
        }
    }

    rooms["sunstone_reef_cave_shipwreck"] = {
        "id": "sunstone_reef_cave_shipwreck",
        "name": "Sunken Ship Chamber",
        "description": "Deep within the reef caves, the bow of an ancient ship protrudes from "
                       "a cave wall, its timbers preserved by the mineral-rich water. The ship "
                       "carried cargo from a distant land — pottery, bronze tools, and sealed "
                       "amphorae that may predate the temple ruins above.",
        "coordinates": [cx + 5, cy - 8],
        "location_type": "wilderness",
        "items": {"ancient_amphora": {"quantity": 1, "value": 35}, "bronze_ship_fitting": {"quantity": 1, "value": 22}},
        "exits": {
            "west": {"target": "sunstone_reef_cave_manta", "type": "direction"}
        }
    }



def generate_emerald_isle(rooms):
    """Generate Island 2: Emerald Isle - Enchanted jungle / druid-nature island (~80 rooms)."""

    cx, cy = 55, 30  # Center coordinates

    # =========================================================================
    # EMERALD ISLE - Enchanted Jungle Island (Level 10+)
    # Sub-regions: Docks, Druid Village, Rainforest, Mushroom Grotto,
    #              Druid Sanctum, Beast Wilds, Crystal Waterfall, Overgrown Ruins
    # =========================================================================

    # --- Emerald Docks (3 rooms) ---

    rooms["emerald_docks"] = {
        "id": "emerald_docks",
        "name": "Emerald Isle Docks",
        "description": "A moss-covered stone dock juts into fog-shrouded waters. Thick jungle vines "
                       "drape over weather-beaten mooring posts, and the air hums with unseen insects. "
                       "The canopy beyond is so dense it swallows the sky in a wall of green.",
        "coordinates": [cx, cy],
        "location_type": "dock",
        "items": {},
        "exits": {
            "board mainland": {
                "target": "harbor_north_dock",
                "type": "boat_travel",
                "island_id": "emerald_isle",
                "unlock_cost": 0,
                "fare_cost": 0,
                "min_level": 1,
                "display": "Return to Grand Harbor",
                "transition_text": "You climb aboard the vine-draped vessel. The crew pushes off from the\nmossy dock and the impossibly green island slowly fades into the mist.\nAfter three days at sea, the familiar Grand Harbor emerges on the horizon..."
            },
            "south": {"target": "emerald_dock_cargo", "type": "direction"},
            "east": {"target": "emerald_dock_lookout", "type": "direction"},
            "north": {"target": "emerald_village_path", "type": "direction"}
        }
    }

    rooms["emerald_dock_cargo"] = {
        "id": "emerald_dock_cargo",
        "name": "Dock Cargo Area",
        "description": "Wooden crates stamped with druidic runes are stacked beneath a canopy of woven leaves. "
                       "Bundles of dried herbs and clay pots of strange unguents await transport. "
                       "A mossy crane mechanism, grown half-alive, lifts the heavier loads.",
        "coordinates": [cx, cy - 1],
        "location_type": "dock",
        "items": {"dried_herbs": {"quantity": 3, "value": 8}, "clay_unguent": {"quantity": 1, "value": 15}},
        "exits": {
            "north": {"target": "emerald_docks", "type": "direction"},
            "west": {"target": "emerald_dock_fishers_pier", "type": "direction"}
        }
    }

    rooms["emerald_dock_lookout"] = {
        "id": "emerald_dock_lookout",
        "name": "Dock Lookout",
        "description": "A rickety wooden platform raised on living stilts of twisted mangrove. "
                       "From here you can see the fog-bank surrounding the island and the distant glint "
                       "of the mainland. Bioluminescent jellyfish pulse in the shallows below.",
        "coordinates": [cx + 1, cy],
        "location_type": "dock",
        "items": {"spyglass_old": {"quantity": 1, "value": 12}},
        "exits": {
            "west": {"target": "emerald_docks", "type": "direction"},
            "east": {"target": "emerald_dock_tidal_ledge", "type": "direction"}
        }
    }

    # --- Druid Village (15 rooms) ---

    rooms["emerald_village_path"] = {
        "id": "emerald_village_path",
        "name": "Jungle Path to Village",
        "description": "A winding path of flat stepping-stones, each inscribed with a faint glowing rune, "
                       "leads uphill through dense undergrowth. Fireflies the size of fists drift lazily "
                       "between enormous fern fronds. The sound of distant drums echoes from ahead.",
        "coordinates": [cx, cy + 1],
        "location_type": "wilderness",
        "items": {},
        "exits": {
            "south": {"target": "emerald_docks", "type": "direction"},
            "north": {"target": "emerald_village_gate", "type": "direction"}
        }
    }

    rooms["emerald_village_gate"] = {
        "id": "emerald_village_gate",
        "name": "Druid Village Gate",
        "description": "Two ancient trees have been coaxed to grow into a living archway, their branches "
                       "intertwined to form a gate. Luminous glyphs carved into the bark pulse with a soft "
                       "green heartbeat. Beyond, rope bridges and treehouses fill the canopy.",
        "coordinates": [cx, cy + 2],
        "location_type": "settlement",
        "items": {},
        "exits": {
            "south": {"target": "emerald_village_path", "type": "direction"},
            "north": {"target": "emerald_village_center", "type": "direction"},
            "east": {"target": "emerald_village_garden", "type": "direction"},
            "west": {"target": "emerald_village_workshop", "type": "direction"}
        }
    }

    rooms["emerald_village_center"] = {
        "id": "emerald_village_center",
        "name": "Druid Village - Central Platform",
        "description": "An enormous platform built into the crown of a titan oak. Rope bridges "
                       "radiate outward to other treehouses. A fire-pit in the centre burns with "
                       "smokeless green flame, and druids in living-bark armor gather to discuss the "
                       "health of the island.",
        "coordinates": [cx, cy + 3],
        "location_type": "settlement",
        "npcs": ["druid_elder"],
        "items": {},
        "exits": {
            "south": {"target": "emerald_village_gate", "type": "direction"},
            "north": {"target": "emerald_village_lookout", "type": "direction"},
            "east": {"target": "emerald_village_market", "type": "direction"},
            "west": {"target": "emerald_village_healer", "type": "direction"},
            "up": {"target": "emerald_elder_house", "type": "direction"},
            "inn": {"target": "emerald_village_inn", "type": "named", "display": "The Mossy Hammock Inn"}
        }
    }

    rooms["emerald_elder_house"] = {
        "id": "emerald_elder_house",
        "name": "Elder's Treehouse",
        "description": "The highest treehouse, woven from living wood and flowering vines. "
                       "Shelves of bark scrolls line the curving walls. A crystal orb on a root-pedestal "
                       "shows a shimmering map of ley lines spanning the island.",
        "coordinates": [cx, cy + 4],
        "location_type": "building",
        "items": {"bark_scroll": {"quantity": 1, "value": 30}, "ley_line_map": {"quantity": 1, "value": 50}},
        "exits": {
            "down": {"target": "emerald_village_center", "type": "direction"},
            "east": {"target": "emerald_village_shrine", "type": "direction"}
        }
    }

    rooms["emerald_village_healer"] = {
        "id": "emerald_village_healer",
        "name": "Healer's Hut",
        "description": "A round treehouse thick with the scent of crushed herbs and simmering potions. "
                       "Bundles of dried moonpetal and thornroot hang from the ceiling. A druid healer "
                       "tends a softly bubbling cauldron of restorative sap.",
        "coordinates": [cx - 1, cy + 3],
        "location_type": "building",
        "npcs": ["druid_healer"],
        "items": {"healing_salve": {"quantity": 2, "value": 18}, "moonpetal_bundle": {"quantity": 1, "value": 12}},
        "exits": {
            "east": {"target": "emerald_village_center", "type": "direction"},
            "south": {"target": "emerald_village_workshop", "type": "direction"}
        }
    }

    rooms["emerald_village_workshop"] = {
        "id": "emerald_village_workshop",
        "name": "Woodshaper's Workshop",
        "description": "A cluttered platform where druids shape living wood into tools and armor. "
                       "Half-finished staffs sprout tiny leaves, and a suit of barkplate armor "
                       "grows on a mannequin of twisted roots. Sap-stained tools hang from pegs.",
        "coordinates": [cx - 1, cy + 2],
        "location_type": "building",
        "items": {"living_wood_staff": {"quantity": 1, "value": 35}},
        "exits": {
            "north": {"target": "emerald_village_healer", "type": "direction"},
            "east": {"target": "emerald_village_gate", "type": "direction"}
        }
    }

    rooms["emerald_village_market"] = {
        "id": "emerald_village_market",
        "name": "Canopy Market",
        "description": "A network of rope bridges connects merchant platforms hung between branches. "
                       "Traders sell rare herbs, enchanted seeds, fungal extracts, and living-wood trinkets. "
                       "Bright parrots carry messages between stalls.",
        "coordinates": [cx + 1, cy + 3],
        "location_type": "settlement",
        "shop": True,
        "items": {"emerald_seed": {"quantity": 2, "value": 20}, "fungal_extract": {"quantity": 3, "value": 10}},
        "exits": {
            "west": {"target": "emerald_village_center", "type": "direction"},
            "north": {"target": "emerald_village_shrine", "type": "direction"},
            "east": {"target": "emerald_village_training", "type": "direction"}
        }
    }

    rooms["emerald_village_inn"] = {
        "id": "emerald_village_inn",
        "name": "The Mossy Hammock Inn",
        "description": "A cozy treehouse inn where guests sleep in silk-moss hammocks strung between "
                       "branches. Bioluminescent vines provide a gentle nightlight. The innkeeper, "
                       "a jovial satyr, serves warm rootbrew and honeyed fruit.",
        "coordinates": [cx - 1, cy + 4],
        "location_type": "building",
        "items": {"rootbrew": {"quantity": 2, "value": 6}, "honeyed_fruit": {"quantity": 3, "value": 4}},
        "exits": {
            "outside": {"target": "emerald_village_center", "type": "direction"},
            "north": {"target": "emerald_village_stables", "type": "direction"}
        }
    }

    rooms["emerald_village_shrine"] = {
        "id": "emerald_village_shrine",
        "name": "Shrine of the Green Mother",
        "description": "A serene platform surrounding a living statue — a woman's form grown from "
                       "intertwined vines and flowering orchids. Offerings of rare seeds and spring water "
                       "are placed at her root-feet. The air here shimmers with healing energy.",
        "coordinates": [cx + 1, cy + 4],
        "location_type": "building",
        "items": {"blessed_water": {"quantity": 1, "value": 22}},
        "exits": {
            "south": {"target": "emerald_village_market", "type": "direction"},
            "west": {"target": "emerald_elder_house", "type": "direction"}
        }
    }

    rooms["emerald_village_training"] = {
        "id": "emerald_village_training",
        "name": "Training Glade",
        "description": "An open platform where young druids practice nature magic and staff combat. "
                       "Target dummies made of bundled vines regenerate after each strike. "
                       "A veteran druid ranger oversees the exercises with sharp eyes.",
        "coordinates": [cx + 2, cy + 3],
        "location_type": "settlement",
        "npcs": ["druid_ranger_trainer"],
        "items": {},
        "exits": {
            "west": {"target": "emerald_village_market", "type": "direction"},
            "south": {"target": "emerald_village_garden", "type": "direction"},
            "north": {"target": "emerald_rain_stream_crossing", "type": "direction"}
        }
    }

    rooms["emerald_village_garden"] = {
        "id": "emerald_village_garden",
        "name": "Herbalist's Garden",
        "description": "A terraced garden built into the hillside beneath the treehouses. Rows of "
                       "glowing moonpetals, shimmering frostmint, and pulsing heartbloom are tended "
                       "by sprite-like creatures. A small stream irrigates the beds.",
        "coordinates": [cx + 1, cy + 2],
        "location_type": "settlement",
        "items": {"moonpetal": {"quantity": 2, "value": 10}, "heartbloom": {"quantity": 1, "value": 16}, "frostmint": {"quantity": 2, "value": 8}},
        "exits": {
            "north": {"target": "emerald_village_training", "type": "direction"},
            "west": {"target": "emerald_village_gate", "type": "direction"}
        }
    }

    rooms["emerald_village_lookout"] = {
        "id": "emerald_village_lookout",
        "name": "Canopy Lookout",
        "description": "The highest point in the village — a crow's-nest platform lashed to the very "
                       "top of the titan oak. From here the entire island stretches out: dense jungle to "
                       "the east, glowing mushroom fields to the west, and misty waterfalls to the north.",
        "coordinates": [cx, cy + 5],
        "location_type": "settlement",
        "items": {},
        "exits": {
            "south": {"target": "emerald_village_center", "type": "direction"},
            "east": {"target": "emerald_village_east_bridge", "type": "direction"},
            "west": {"target": "emerald_village_stables", "type": "direction"}
        }
    }

    rooms["emerald_village_east_bridge"] = {
        "id": "emerald_village_east_bridge",
        "name": "Eastern Rope Bridge",
        "description": "A swaying rope bridge stretches from the village eastward over a misty chasm. "
                       "Below, a river churns white between mossy boulders. Parrots flash through "
                       "the canopy above, shrieking territorial warnings.",
        "coordinates": [cx + 1, cy + 5],
        "location_type": "settlement",
        "items": {},
        "exits": {
            "west": {"target": "emerald_village_lookout", "type": "direction"},
            "east": {"target": "emerald_rainforest_entrance", "type": "direction"}
        }
    }

    rooms["emerald_village_stables"] = {
        "id": "emerald_village_stables",
        "name": "Beast Stables",
        "description": "A ground-level enclosure where the druids keep tamed jungle beasts — giant "
                       "lizards, armored beetles, and a sleepy moss-bear. The smell of damp fur and "
                       "fresh hay fills the air. A beast handler feeds the creatures enchanted grain.",
        "coordinates": [cx - 1, cy + 5],
        "location_type": "building",
        "npcs": ["beast_handler"],
        "items": {"enchanted_grain": {"quantity": 2, "value": 7}},
        "exits": {
            "east": {"target": "emerald_village_lookout", "type": "direction"},
            "south": {"target": "emerald_village_inn", "type": "direction"}
        }
    }

    # --- Rainforest (15 rooms) ---

    rooms["emerald_rainforest_entrance"] = {
        "id": "emerald_rainforest_entrance",
        "name": "Rainforest Edge",
        "description": "The jungle closes in like a living wall. Enormous ferns tower overhead, "
                       "their fronds dripping with condensation. The air is thick, warm, and alive "
                       "with the chittering of unseen creatures. A narrow trail disappears into the green.",
        "coordinates": [cx + 2, cy + 5],
        "location_type": "wilderness",
        "items": {},
        "exits": {
            "west": {"target": "emerald_village_east_bridge", "type": "direction"},
            "east": {"target": "emerald_rain_dense_path", "type": "direction"},
            "south": {"target": "emerald_rain_stream_crossing", "type": "direction"}
        }
    }

    rooms["emerald_rain_dense_path"] = {
        "id": "emerald_rain_dense_path",
        "name": "Dense Jungle Path",
        "description": "Vines as thick as ship ropes hang from the canopy, forcing you to push through "
                       "a curtain of green. Giant butterflies with iridescent wings drift past. "
                       "The undergrowth rustles with the passage of unseen animals.",
        "coordinates": [cx + 3, cy + 5],
        "location_type": "wilderness",
        "items": {"jungle_vine": {"quantity": 2, "value": 5}},
        "exits": {
            "west": {"target": "emerald_rainforest_entrance", "type": "direction"},
            "north": {"target": "emerald_rain_canopy_walk", "type": "direction"},
            "east": {"target": "emerald_rain_ancient_tree", "type": "direction"}
        }
    }

    rooms["emerald_rain_canopy_walk"] = {
        "id": "emerald_rain_canopy_walk",
        "name": "Canopy Walkway",
        "description": "A series of planks and woven-vine bridges slung between enormous trees, "
                       "high above the jungle floor. Toucans and macaws perch on nearby branches. "
                       "The view stretches for miles — a rolling ocean of green dotted with mist.",
        "coordinates": [cx + 3, cy + 6],
        "location_type": "wilderness",
        "items": {"parrot_feather": {"quantity": 1, "value": 14}},
        "exits": {
            "south": {"target": "emerald_rain_dense_path", "type": "direction"},
            "east": {"target": "emerald_rain_canopy_nest", "type": "direction"},
            "west": {"target": "emerald_rain_vine_bridge", "type": "direction"}
        }
    }

    rooms["emerald_rain_vine_bridge"] = {
        "id": "emerald_rain_vine_bridge",
        "name": "Vine Bridge",
        "description": "A natural bridge formed by intertwined vines spans a deep ravine. "
                       "Mist rises from below where a hidden river roars. The bridge sways gently "
                       "and orchids bloom along its handrails, their petals closing as you pass.",
        "coordinates": [cx + 2, cy + 6],
        "location_type": "wilderness",
        "items": {},
        "exits": {
            "east": {"target": "emerald_rain_canopy_walk", "type": "direction"},
            "north": {"target": "emerald_rain_clearing", "type": "direction"}
        }
    }

    rooms["emerald_rain_clearing"] = {
        "id": "emerald_rain_clearing",
        "name": "Sunlit Clearing",
        "description": "A rare break in the canopy allows golden sunlight to pour down. The ground "
                       "is carpeted with violently green moss and tiny star-shaped flowers. "
                       "A stone waymarker, covered in lichen, points in several directions.",
        "coordinates": [cx + 2, cy + 7],
        "location_type": "wilderness",
        "items": {"star_flower": {"quantity": 3, "value": 6}},
        "exits": {
            "south": {"target": "emerald_rain_vine_bridge", "type": "direction"},
            "north": {"target": "emerald_rain_waterfall_path", "type": "direction"},
            "east": {"target": "emerald_rain_hollow_log", "type": "direction"},
            "west": {"target": "emerald_grotto_entrance", "type": "direction"}
        }
    }

    rooms["emerald_rain_canopy_nest"] = {
        "id": "emerald_rain_canopy_nest",
        "name": "Giant Nest Platform",
        "description": "A massive abandoned nest, easily ten feet across, sits wedged in the fork "
                       "of a titan tree. Iridescent feathers and strange eggshell fragments litter "
                       "the bowl. Whatever built this could carry off a horse.",
        "coordinates": [cx + 4, cy + 6],
        "location_type": "wilderness",
        "items": {"iridescent_feather": {"quantity": 2, "value": 18}, "strange_eggshell": {"quantity": 1, "value": 25}},
        "exits": {
            "west": {"target": "emerald_rain_canopy_walk", "type": "direction"},
            "south": {"target": "emerald_rain_ancient_tree", "type": "direction"}
        }
    }

    rooms["emerald_rain_ancient_tree"] = {
        "id": "emerald_rain_ancient_tree",
        "name": "Ancient Ironwood",
        "description": "The largest tree you have ever seen. Its trunk is wider than a castle tower, "
                       "its bark like rusted iron plate. Carved spiral stairs wind up into the canopy. "
                       "Strange faces seem to peer from knotholes in the bark.",
        "coordinates": [cx + 4, cy + 5],
        "location_type": "wilderness",
        "items": {"ironwood_bark": {"quantity": 1, "value": 20}},
        "exits": {
            "west": {"target": "emerald_rain_dense_path", "type": "direction"},
            "north": {"target": "emerald_rain_canopy_nest", "type": "direction"},
            "south": {"target": "emerald_rain_jungle_floor", "type": "direction"}
        }
    }

    rooms["emerald_rain_stream_crossing"] = {
        "id": "emerald_rain_stream_crossing",
        "name": "Stream Crossing",
        "description": "A shallow jungle stream cuts across the path, its water startlingly clear "
                       "over a bed of smooth colored pebbles. Tiny silver fish dart between your feet "
                       "as you wade across. Mossy stepping-stones offer a drier route.",
        "coordinates": [cx + 2, cy + 4],
        "location_type": "wilderness",
        "items": {"colored_pebble": {"quantity": 3, "value": 3}},
        "exits": {
            "north": {"target": "emerald_rainforest_entrance", "type": "direction"},
            "east": {"target": "emerald_rain_fern_valley", "type": "direction"},
            "south": {"target": "emerald_village_training", "type": "direction"}
        }
    }

    rooms["emerald_rain_fern_valley"] = {
        "id": "emerald_rain_fern_valley",
        "name": "Fern Valley",
        "description": "A low-lying valley choked with tree-ferns taller than houses. Their curled "
                       "fronds unfurl like green question marks. The humid air drips with moisture "
                       "and the ground squelches underfoot. Glowing spores drift on the breeze.",
        "coordinates": [cx + 3, cy + 4],
        "location_type": "wilderness",
        "items": {"fern_frond": {"quantity": 2, "value": 5}, "glowing_spore": {"quantity": 1, "value": 12}},
        "exits": {
            "west": {"target": "emerald_rain_stream_crossing", "type": "direction"},
            "east": {"target": "emerald_rain_jungle_floor", "type": "direction"}
        }
    }

    rooms["emerald_rain_jungle_floor"] = {
        "id": "emerald_rain_jungle_floor",
        "name": "Jungle Floor",
        "description": "The forest floor is a dim twilight world. Massive buttress roots form "
                       "walls and corridors. Fungi of every size and color sprout from rotting logs. "
                       "A jaguar's territorial scratch-marks scar a nearby trunk.",
        "coordinates": [cx + 4, cy + 4],
        "location_type": "wilderness",
        "items": {"jungle_mushroom": {"quantity": 3, "value": 6}},
        "exits": {
            "north": {"target": "emerald_rain_ancient_tree", "type": "direction"},
            "west": {"target": "emerald_rain_fern_valley", "type": "direction"},
            "south": {"target": "emerald_rain_predator_trail", "type": "direction"}
        }
    }

    rooms["emerald_rain_hollow_log"] = {
        "id": "emerald_rain_hollow_log",
        "name": "Hollow Log Passage",
        "description": "A fallen titan tree forms a natural tunnel, its interior colonized by "
                       "bioluminescent mushrooms that cast a blue-green glow. The soft wood underfoot "
                       "is spongy and quiet. Something has been nesting here recently.",
        "coordinates": [cx + 3, cy + 7],
        "location_type": "wilderness",
        "items": {"bioluminescent_cap": {"quantity": 2, "value": 14}},
        "exits": {
            "west": {"target": "emerald_rain_clearing", "type": "direction"},
            "east": {"target": "emerald_rain_spider_canopy", "type": "direction"}
        }
    }

    rooms["emerald_rain_waterfall_path"] = {
        "id": "emerald_rain_waterfall_path",
        "name": "Waterfall Path",
        "description": "The roar of falling water grows louder as the path follows a rocky ledge "
                       "alongside a rushing river. Spray soaks the air and rainbows form in the mist. "
                       "The path leads both north toward the falls and down into a mushroom-lit grotto.",
        "coordinates": [cx + 2, cy + 8],
        "location_type": "wilderness",
        "items": {},
        "exits": {
            "south": {"target": "emerald_rain_clearing", "type": "direction"},
            "north": {"target": "emerald_crystal_falls_base", "type": "direction"}
        }
    }

    rooms["emerald_rain_predator_trail"] = {
        "id": "emerald_rain_predator_trail",
        "name": "Predator's Trail",
        "description": "Claw marks, scattered bones, and tufts of bright fur line this narrow game trail. "
                       "The jungle is eerily quiet here — smaller creatures have fled. A low growl "
                       "rumbles from somewhere in the undergrowth ahead.",
        "coordinates": [cx + 4, cy + 3],
        "location_type": "wilderness",
        "items": {"beast_fang": {"quantity": 1, "value": 16}},
        "exits": {
            "north": {"target": "emerald_rain_jungle_floor", "type": "direction"},
            "south": {"target": "emerald_beast_hunting_grounds", "type": "direction"}
        }
    }

    # --- Mushroom Grotto (12 rooms) ---

    rooms["emerald_grotto_entrance"] = {
        "id": "emerald_grotto_entrance",
        "name": "Mushroom Grotto Entrance",
        "description": "The ground dips into a wide depression where the canopy thins. "
                       "Enormous mushrooms the size of houses cluster together, their caps glowing "
                       "in shifting hues of blue, violet, and teal. A warm, earthy mist rises from below.",
        "coordinates": [cx + 1, cy + 7],
        "location_type": "wilderness",
        "items": {},
        "exits": {
            "east": {"target": "emerald_rain_clearing", "type": "direction"},
            "south": {"target": "emerald_grotto_giant_caps", "type": "direction"},
            "west": {"target": "emerald_grotto_spore_tunnel", "type": "direction"}
        }
    }

    rooms["emerald_grotto_giant_caps"] = {
        "id": "emerald_grotto_giant_caps",
        "name": "Giant Mushroom Caps",
        "description": "You walk beneath mushroom caps broad enough to shelter a village. "
                       "Bioluminescent veins pulse through their gills, casting hypnotic patterns "
                       "on the ground. Dew collects in their caps and drips like warm rain.",
        "coordinates": [cx + 1, cy + 6],
        "location_type": "wilderness",
        "items": {"giant_mushroom_cap": {"quantity": 1, "value": 18}},
        "exits": {
            "north": {"target": "emerald_grotto_entrance", "type": "direction"},
            "west": {"target": "emerald_grotto_glow_pond", "type": "direction"}
        }
    }

    rooms["emerald_grotto_spore_tunnel"] = {
        "id": "emerald_grotto_spore_tunnel",
        "name": "Spore Tunnel",
        "description": "A tunnel bored through solid fungal matter. Clouds of luminous spores "
                       "puff from the walls with each footstep, swirling in mesmerizing patterns. "
                       "The air tastes faintly sweet and your thoughts feel strangely clear.",
        "coordinates": [cx, cy + 7],
        "location_type": "wilderness",
        "items": {"luminous_spores": {"quantity": 3, "value": 10}},
        "exits": {
            "east": {"target": "emerald_grotto_entrance", "type": "direction"},
            "south": {"target": "emerald_grotto_glow_pond", "type": "direction"},
            "west": {"target": "emerald_grotto_fungal_garden", "type": "direction"}
        }
    }

    rooms["emerald_grotto_glow_pond"] = {
        "id": "emerald_grotto_glow_pond",
        "name": "Glow Pond",
        "description": "A still, mirror-perfect pond radiates soft turquoise light from some source "
                       "deep below. Tiny luminous fish circle languidly. Giant lily-pads, thick enough "
                       "to stand on, float on the surface. The silence here is absolute.",
        "coordinates": [cx, cy + 6],
        "location_type": "wilderness",
        "items": {"glow_fish": {"quantity": 1, "value": 15}, "luminous_lily": {"quantity": 1, "value": 12}},
        "exits": {
            "north": {"target": "emerald_grotto_spore_tunnel", "type": "direction"},
            "east": {"target": "emerald_grotto_giant_caps", "type": "direction"},
            "south": {"target": "emerald_grotto_cavern", "type": "direction"},
            "west": {"target": "emerald_grotto_mycelium_web", "type": "direction"}
        }
    }

    rooms["emerald_grotto_cavern"] = {
        "id": "emerald_grotto_cavern",
        "name": "Spore Cavern",
        "description": "A vast underground chamber whose ceiling is lost in darkness. Pillars of "
                       "stacked mushrooms support the roof. A constant drizzle of spores drifts down "
                       "like golden snow. Ancient druidic carvings decorate the cavern walls.",
        "coordinates": [cx, cy + 5],
        "location_type": "wilderness",
        "items": {"ancient_spore_sample": {"quantity": 1, "value": 22}},
        "exits": {
            "north": {"target": "emerald_grotto_glow_pond", "type": "direction"},
            "west": {"target": "emerald_grotto_deep_roots", "type": "direction"}
        }
    }

    rooms["emerald_grotto_mycelium_web"] = {
        "id": "emerald_grotto_mycelium_web",
        "name": "Mycelium Network",
        "description": "White and silver threads of mycelium cover every surface, pulsing faintly "
                       "as if carrying signals. The druids say this network connects every plant on "
                       "the island. Touching it sends tingling warmth through your fingers.",
        "coordinates": [cx - 1, cy + 6],
        "location_type": "wilderness",
        "items": {"mycelium_thread": {"quantity": 2, "value": 14}},
        "exits": {
            "east": {"target": "emerald_grotto_glow_pond", "type": "direction"},
            "north": {"target": "emerald_grotto_fungal_garden", "type": "direction"},
            "south": {"target": "emerald_grotto_deep_roots", "type": "direction"},
            "west": {"target": "emerald_grotto_echo_chamber", "type": "direction"}
        }
    }

    rooms["emerald_grotto_fungal_garden"] = {
        "id": "emerald_grotto_fungal_garden",
        "name": "Fungal Garden",
        "description": "A cultivated grove of rare mushroom species tended by tiny fungal sprites. "
                       "Shelves of bracket fungi grow in neat rows, and puffball clusters sit like "
                       "round lanterns. A druid alchemist harvests specimens into crystal jars.",
        "coordinates": [cx - 1, cy + 7],
        "location_type": "wilderness",
        "items": {"rare_puffball": {"quantity": 1, "value": 20}, "bracket_fungus": {"quantity": 2, "value": 8}},
        "exits": {
            "east": {"target": "emerald_grotto_spore_tunnel", "type": "direction"},
            "south": {"target": "emerald_grotto_mycelium_web", "type": "direction"},
            "west": {"target": "emerald_grotto_shroomlight_hall", "type": "direction"}
        }
    }

    rooms["emerald_grotto_shroomlight_hall"] = {
        "id": "emerald_grotto_shroomlight_hall",
        "name": "Shroomlight Hall",
        "description": "A cathedral-like cavern lit entirely by towering mushrooms whose caps "
                       "blaze with orange and gold light. The warmth here is almost tropical. "
                       "Moss-covered benches suggest the druids once held ceremonies in this space.",
        "coordinates": [cx - 2, cy + 7],
        "location_type": "wilderness",
        "items": {"shroomlight_cap": {"quantity": 1, "value": 24}},
        "exits": {
            "east": {"target": "emerald_grotto_fungal_garden", "type": "direction"},
            "south": {"target": "emerald_grotto_echo_chamber", "type": "direction"}
        }
    }

    rooms["emerald_grotto_echo_chamber"] = {
        "id": "emerald_grotto_echo_chamber",
        "name": "Echo Chamber",
        "description": "A perfectly round cavern where every whisper bounces endlessly off the walls. "
                       "Crystallized fungal formations ring the chamber like organ pipes. "
                       "The druids use this place to commune with the island's living network.",
        "coordinates": [cx - 2, cy + 6],
        "location_type": "wilderness",
        "items": {"crystallized_fungus": {"quantity": 1, "value": 28}},
        "exits": {
            "north": {"target": "emerald_grotto_shroomlight_hall", "type": "direction"},
            "east": {"target": "emerald_grotto_mycelium_web", "type": "direction"},
            "south": {"target": "emerald_grotto_spore_nursery", "type": "direction"}
        }
    }

    rooms["emerald_grotto_deep_roots"] = {
        "id": "emerald_grotto_deep_roots",
        "name": "Deep Root Chamber",
        "description": "Massive tree roots burst through the cavern ceiling and plunge into "
                       "underground streams. The roots glow faintly where mycelium has colonized them. "
                       "This is the heart of the island's underground ecosystem.",
        "coordinates": [cx - 1, cy + 5],
        "location_type": "wilderness",
        "items": {"deep_root_sap": {"quantity": 1, "value": 30}},
        "exits": {
            "north": {"target": "emerald_grotto_mycelium_web", "type": "direction"},
            "east": {"target": "emerald_grotto_cavern", "type": "direction"},
            "west": {"target": "emerald_sanctum_entrance", "type": "direction"}
        }
    }

    # --- Druid Sanctum (12 rooms) ---

    rooms["emerald_sanctum_entrance"] = {
        "id": "emerald_sanctum_entrance",
        "name": "Sanctum Entrance",
        "description": "Ancient standing stones draped in living moss form a gateway into sacred ground. "
                       "The air crackles with latent magical energy. Runes carved into the stones glow "
                       "faintly green, and you feel the weight of ages pressing in around you.",
        "coordinates": [cx - 2, cy + 5],
        "location_type": "wilderness",
        "items": {},
        "exits": {
            "east": {"target": "emerald_grotto_deep_roots", "type": "direction"},
            "west": {"target": "emerald_sanctum_outer_ring", "type": "direction"},
            "south": {"target": "emerald_sanctum_spirit_path", "type": "direction"}
        }
    }

    rooms["emerald_sanctum_outer_ring"] = {
        "id": "emerald_sanctum_outer_ring",
        "name": "Outer Stone Circle",
        "description": "A ring of twelve monoliths towers over a grassy clearing. Each stone is carved "
                       "with the likeness of a different druidic animal spirit. Fireflies orbit the "
                       "stones in precise, spiraling patterns that suggest intelligence.",
        "coordinates": [cx - 3, cy + 5],
        "location_type": "wilderness",
        "items": {"carved_runestone": {"quantity": 1, "value": 22}},
        "exits": {
            "east": {"target": "emerald_sanctum_entrance", "type": "direction"},
            "west": {"target": "emerald_sanctum_inner_ring", "type": "direction"},
            "north": {"target": "emerald_sanctum_moon_pool", "type": "direction"},
            "south": {"target": "emerald_sanctum_ritual_clearing", "type": "direction"}
        }
    }

    rooms["emerald_sanctum_inner_ring"] = {
        "id": "emerald_sanctum_inner_ring",
        "name": "Inner Stone Circle",
        "description": "The inner sanctum. Five massive trilithons form a pentagonal enclosure. "
                       "The grass inside is impossibly lush, dotted with flowers that bloom and "
                       "wilt in seconds. A low hum vibrates through the earth itself.",
        "coordinates": [cx - 4, cy + 5],
        "location_type": "wilderness",
        "items": {"druidic_charm": {"quantity": 1, "value": 35}},
        "exits": {
            "east": {"target": "emerald_sanctum_outer_ring", "type": "direction"},
            "north": {"target": "emerald_sanctum_sacred_grove", "type": "direction"},
            "south": {"target": "emerald_sanctum_ley_nexus", "type": "direction"}
        }
    }

    rooms["emerald_sanctum_sacred_grove"] = {
        "id": "emerald_sanctum_sacred_grove",
        "name": "Sacred Grove",
        "description": "A grove of trees so ancient their trunks have fused together into one enormous "
                       "organism. Golden sap weeps from their bark. The druids' most powerful "
                       "enchantments were cast here, and residual magic makes the air shimmer.",
        "coordinates": [cx - 4, cy + 6],
        "location_type": "wilderness",
        "items": {"golden_sap": {"quantity": 1, "value": 40}, "sacred_acorn": {"quantity": 1, "value": 30}},
        "exits": {
            "south": {"target": "emerald_sanctum_inner_ring", "type": "direction"},
            "east": {"target": "emerald_sanctum_moon_pool", "type": "direction"},
            "north": {"target": "emerald_sanctum_world_tree_root", "type": "direction"}
        }
    }

    rooms["emerald_sanctum_moon_pool"] = {
        "id": "emerald_sanctum_moon_pool",
        "name": "Moon Pool",
        "description": "A perfectly circular pool of silver water that reflects the moon even during "
                       "the day. Druidic prophecies appear as visions on its surface. White lotus "
                       "flowers drift across the water, each one trailing a line of starlight.",
        "coordinates": [cx - 3, cy + 6],
        "location_type": "wilderness",
        "items": {"moonwater_vial": {"quantity": 1, "value": 25}, "white_lotus": {"quantity": 1, "value": 18}},
        "exits": {
            "south": {"target": "emerald_sanctum_outer_ring", "type": "direction"},
            "west": {"target": "emerald_sanctum_sacred_grove", "type": "direction"},
            "north": {"target": "emerald_sanctum_starlight_altar", "type": "direction"}
        }
    }

    rooms["emerald_sanctum_ritual_clearing"] = {
        "id": "emerald_sanctum_ritual_clearing",
        "name": "Ritual Clearing",
        "description": "A circular clearing where the grass has been worn away by countless ceremonies. "
                       "Scorch marks from druidfire form intricate patterns. Ritual drums and bone flutes "
                       "rest on a stone shelf, waiting for the next ceremony.",
        "coordinates": [cx - 3, cy + 4],
        "location_type": "wilderness",
        "items": {"ritual_drum": {"quantity": 1, "value": 16}, "bone_flute": {"quantity": 1, "value": 14}},
        "exits": {
            "north": {"target": "emerald_sanctum_outer_ring", "type": "direction"},
            "east": {"target": "emerald_sanctum_spirit_path", "type": "direction"},
            "south": {"target": "emerald_sanctum_ancestor_stones", "type": "direction"}
        }
    }

    rooms["emerald_sanctum_spirit_path"] = {
        "id": "emerald_sanctum_spirit_path",
        "name": "Spirit Path",
        "description": "A winding trail marked by standing stones, each topped with a softly glowing "
                       "crystal. Translucent shapes flit between the stones — animal spirits bound "
                       "to the sanctum. The path pulses faintly beneath your feet.",
        "coordinates": [cx - 2, cy + 4],
        "location_type": "wilderness",
        "items": {"spirit_crystal": {"quantity": 1, "value": 20}},
        "exits": {
            "north": {"target": "emerald_sanctum_entrance", "type": "direction"},
            "west": {"target": "emerald_sanctum_ritual_clearing", "type": "direction"},
            "south": {"target": "emerald_sanctum_spirit_pool", "type": "direction"}
        }
    }

    rooms["emerald_sanctum_ley_nexus"] = {
        "id": "emerald_sanctum_ley_nexus",
        "name": "Ley Line Nexus",
        "description": "Three ley lines converge here in a blinding knot of green energy. The ground "
                       "cracks with light, and plants grow visibly, sprouting and blooming in seconds. "
                       "Standing here makes your skin tingle and your senses sharpen.",
        "coordinates": [cx - 4, cy + 4],
        "location_type": "wilderness",
        "items": {"ley_crystal": {"quantity": 1, "value": 45}},
        "exits": {
            "north": {"target": "emerald_sanctum_inner_ring", "type": "direction"},
            "east": {"target": "emerald_sanctum_ancestor_stones", "type": "direction"}
        }
    }

    rooms["emerald_sanctum_ancestor_stones"] = {
        "id": "emerald_sanctum_ancestor_stones",
        "name": "Ancestor Stones",
        "description": "Weathered cairns mark the resting places of ancient druid elders. "
                       "Their spirits manifest as gentle green lights that hover over the stones. "
                       "Offerings of fruit and herbs are left regularly by the current generation.",
        "coordinates": [cx - 3, cy + 3],
        "location_type": "wilderness",
        "items": {"ancestor_offering": {"quantity": 1, "value": 15}},
        "exits": {
            "north": {"target": "emerald_sanctum_ritual_clearing", "type": "direction"},
            "west": {"target": "emerald_sanctum_ley_nexus", "type": "direction"},
            "east": {"target": "emerald_sanctum_spirit_pool", "type": "direction"}
        }
    }

    rooms["emerald_sanctum_spirit_pool"] = {
        "id": "emerald_sanctum_spirit_pool",
        "name": "Spirit Pool",
        "description": "A warm spring pool surrounded by weeping willows whose branches trail in "
                       "the water. Bathing here is said to let you speak with animal spirits. "
                       "The water glows faintly and tastes of honey and wildflowers.",
        "coordinates": [cx - 2, cy + 3],
        "location_type": "wilderness",
        "items": {"spirit_water": {"quantity": 1, "value": 22}},
        "exits": {
            "north": {"target": "emerald_sanctum_spirit_path", "type": "direction"},
            "west": {"target": "emerald_sanctum_ancestor_stones", "type": "direction"}
        }
    }

    rooms["emerald_sanctum_starlight_altar"] = {
        "id": "emerald_sanctum_starlight_altar",
        "name": "Starlight Altar",
        "description": "An altar of pale white stone stands in a clearing where the canopy opens "
                       "to the sky. Even by day, stars are visible overhead. Ancient druidic "
                       "constellations are mapped in silver inlay across the altar's surface.",
        "coordinates": [cx - 3, cy + 7],
        "location_type": "wilderness",
        "items": {"starlight_shard": {"quantity": 1, "value": 35}},
        "exits": {
            "south": {"target": "emerald_sanctum_moon_pool", "type": "direction"},
            "east": {"target": "emerald_sanctum_world_tree_root", "type": "direction"}
        }
    }

    rooms["emerald_sanctum_world_tree_root"] = {
        "id": "emerald_sanctum_world_tree_root",
        "name": "World Tree Root",
        "description": "A single colossal root, thicker than a city wall, breaks the surface here. "
                       "It pulses with visible life energy, and touching it fills you with visions "
                       "of the entire island — every tree, every creature, every heartbeat.",
        "coordinates": [cx - 4, cy + 7],
        "location_type": "wilderness",
        "items": {"world_tree_splinter": {"quantity": 1, "value": 50}},
        "exits": {
            "south": {"target": "emerald_sanctum_sacred_grove", "type": "direction"},
            "west": {"target": "emerald_sanctum_starlight_altar", "type": "direction"}
        }
    }

    # --- Beast Wilds (10 rooms) ---

    rooms["emerald_beast_hunting_grounds"] = {
        "id": "emerald_beast_hunting_grounds",
        "name": "Beast Hunting Grounds",
        "description": "The jungle here bristles with danger. Claw-scarred trees and territorial "
                       "markings speak of apex predators. The undergrowth is trampled flat by huge "
                       "footprints. A low, rumbling growl vibrates through the humid air.",
        "coordinates": [cx + 4, cy + 2],
        "location_type": "wilderness",
        "items": {},
        "exits": {
            "north": {"target": "emerald_rain_predator_trail", "type": "direction"},
            "south": {"target": "emerald_beast_ravine", "type": "direction"},
            "west": {"target": "emerald_beast_thicket", "type": "direction"}
        }
    }

    rooms["emerald_beast_thicket"] = {
        "id": "emerald_beast_thicket",
        "name": "Thorn Thicket",
        "description": "Dense thorny bushes form a natural barrier. Bright berries, poisonous to "
                       "most but prized by alchemists, hang in clusters. Animal paths weave through "
                       "gaps in the thorns, each just wide enough to squeeze through.",
        "coordinates": [cx + 3, cy + 2],
        "location_type": "wilderness",
        "items": {"thorn_berry": {"quantity": 3, "value": 9}, "barbed_thorn": {"quantity": 2, "value": 6}},
        "exits": {
            "east": {"target": "emerald_beast_hunting_grounds", "type": "direction"},
            "south": {"target": "emerald_beast_den", "type": "direction"},
            "west": {"target": "emerald_beast_meadow", "type": "direction"}
        }
    }

    rooms["emerald_beast_ravine"] = {
        "id": "emerald_beast_ravine",
        "name": "Beast Ravine",
        "description": "A deep ravine cuts through the jungle, its walls streaked with mineral deposits. "
                       "Bones of large prey animals litter the bottom. Something has been using this "
                       "as a feeding ground. The air reeks of musk and old blood.",
        "coordinates": [cx + 4, cy + 1],
        "location_type": "wilderness",
        "items": {"large_bone": {"quantity": 2, "value": 8}, "mineral_deposit": {"quantity": 1, "value": 16}},
        "exits": {
            "north": {"target": "emerald_beast_hunting_grounds", "type": "direction"},
            "west": {"target": "emerald_beast_den", "type": "direction"},
            "east": {"target": "emerald_fey_shimmer_path", "type": "direction"}
        }
    }

    rooms["emerald_beast_den"] = {
        "id": "emerald_beast_den",
        "name": "Predator's Den",
        "description": "A shallow cave beneath a rock overhang, littered with gnawed bones and "
                       "shed scales. The den is warm and stinks of a large reptilian predator. "
                       "Scratches on the walls suggest something enormous sleeps here.",
        "coordinates": [cx + 3, cy + 1],
        "location_type": "wilderness",
        "items": {"shed_scale": {"quantity": 2, "value": 18}, "predator_tooth": {"quantity": 1, "value": 22}},
        "exits": {
            "north": {"target": "emerald_beast_thicket", "type": "direction"},
            "east": {"target": "emerald_beast_ravine", "type": "direction"},
            "south": {"target": "emerald_beast_nesting_grounds", "type": "direction"}
        }
    }

    rooms["emerald_beast_meadow"] = {
        "id": "emerald_beast_meadow",
        "name": "Wild Meadow",
        "description": "A rare open meadow in the jungle, thick with tall grasses and wildflowers. "
                       "Herds of enchanted deer with crystalline antlers graze cautiously. "
                       "They watch you with unnervingly intelligent eyes before bounding away.",
        "coordinates": [cx + 2, cy + 2],
        "location_type": "wilderness",
        "items": {"enchanted_antler_shard": {"quantity": 1, "value": 28}},
        "exits": {
            "east": {"target": "emerald_beast_thicket", "type": "direction"},
            "south": {"target": "emerald_beast_watering_hole", "type": "direction"}
        }
    }

    rooms["emerald_beast_nesting_grounds"] = {
        "id": "emerald_beast_nesting_grounds",
        "name": "Nesting Grounds",
        "description": "A muddy clearing dotted with large mound-nests built from vegetation and mud. "
                       "Leathery eggshells crunch underfoot. Protective mothers hiss from the treeline — "
                       "giant jungle raptors with emerald plumage and razor talons.",
        "coordinates": [cx + 3, cy],
        "location_type": "wilderness",
        "items": {"raptor_eggshell": {"quantity": 2, "value": 14}, "emerald_plume": {"quantity": 1, "value": 20}},
        "exits": {
            "north": {"target": "emerald_beast_den", "type": "direction"},
            "west": {"target": "emerald_beast_watering_hole", "type": "direction"}
        }
    }

    rooms["emerald_beast_watering_hole"] = {
        "id": "emerald_beast_watering_hole",
        "name": "Watering Hole",
        "description": "A muddy pool fed by a trickling stream, surrounded by trampled earth. "
                       "Tracks of dozens of species converge here — a rare truce ground where "
                       "predator and prey drink side by side under an ancient pact of the wilds.",
        "coordinates": [cx + 2, cy + 1],
        "location_type": "wilderness",
        "items": {"enchanted_mud": {"quantity": 1, "value": 10}},
        "exits": {
            "north": {"target": "emerald_beast_meadow", "type": "direction"},
            "east": {"target": "emerald_beast_nesting_grounds", "type": "direction"},
            "south": {"target": "emerald_beast_alpha_territory", "type": "direction"}
        }
    }

    rooms["emerald_beast_alpha_territory"] = {
        "id": "emerald_beast_alpha_territory",
        "name": "Alpha's Territory",
        "description": "The jungle falls silent in this stretch of ancient trees. Deep claw gouges "
                       "scar every trunk, marking the territory of the island's apex predator. "
                       "Even the insects fall quiet. An oppressive, watchful presence fills the air.",
        "coordinates": [cx + 2, cy],
        "location_type": "wilderness",
        "items": {"alpha_claw_mark": {"quantity": 1, "value": 32}},
        "exits": {
            "north": {"target": "emerald_beast_watering_hole", "type": "direction"},
            "west": {"target": "emerald_beast_ancient_hollow", "type": "direction"}
        }
    }

    rooms["emerald_beast_ancient_hollow"] = {
        "id": "emerald_beast_ancient_hollow",
        "name": "Ancient Hollow",
        "description": "A massive hollow in the base of a primordial tree, large enough to stand in. "
                       "The interior is warm and sheltered. Shamanic paintings of beasts cover the "
                       "walls — ancient druids once communed with animal spirits here.",
        "coordinates": [cx + 1, cy],
        "location_type": "wilderness",
        "items": {"shamanic_paint": {"quantity": 1, "value": 16}, "beast_totem": {"quantity": 1, "value": 24}},
        "exits": {
            "east": {"target": "emerald_beast_alpha_territory", "type": "direction"},
            "north": {"target": "emerald_ruins_approach", "type": "direction"}
        }
    }

    # --- Crystal Waterfall (8 rooms) ---

    rooms["emerald_crystal_falls_base"] = {
        "id": "emerald_crystal_falls_base",
        "name": "Crystal Waterfall - Base",
        "description": "A thundering wall of water crashes into a wide pool lined with crystalline "
                       "deposits. Rainbow mist fills the air, refracting sunlight into permanent "
                       "prismatic arcs. The roar is deafening but strangely calming.",
        "coordinates": [cx + 2, cy + 9],
        "location_type": "wilderness",
        "items": {"rainbow_crystal": {"quantity": 1, "value": 30}},
        "exits": {
            "south": {"target": "emerald_rain_waterfall_path", "type": "direction"},
            "swim": {"target": "emerald_crystal_pool", "type": "named", "display": "Swim into Crystal Pool"},
            "up": {"target": "emerald_crystal_falls_middle", "type": "direction"},
            "climb": {"target": "emerald_crystal_falls_middle", "type": "named", "display": "Climb alongside falls"},
            "north": {"target": "emerald_crystal_falls_grotto", "type": "direction"}
        }
    }

    rooms["emerald_crystal_pool"] = {
        "id": "emerald_crystal_pool",
        "name": "Crystal Pool",
        "description": "You wade into the crystal-clear pool beneath the falls. The bottom is lined "
                       "with gemstones polished smooth by centuries of tumbling water. Schools of "
                       "prismatic fish dart between submerged crystal formations.",
        "coordinates": [cx + 2, cy + 10],
        "location_type": "wilderness",
        "items": {"water_gem": {"quantity": 2, "value": 20}, "prismatic_scale": {"quantity": 1, "value": 16}},
        "exits": {
            "swim back": {"target": "emerald_crystal_falls_base", "type": "named", "display": "Swim back to shore"},
            "dive": {"target": "emerald_crystal_underwater_cave", "type": "named", "display": "Dive beneath surface"}
        }
    }

    rooms["emerald_crystal_underwater_cave"] = {
        "id": "emerald_crystal_underwater_cave",
        "name": "Underwater Crystal Cave",
        "description": "A submerged cave behind the waterfall, its walls encrusted with glowing "
                       "aquamarine crystals. Air pockets in the ceiling let you breathe. "
                       "Ancient offerings — corroded coins and crystal figurines — litter the floor.",
        "coordinates": [cx + 2, cy + 11],
        "location_type": "wilderness",
        "items": {"aquamarine_crystal": {"quantity": 1, "value": 35}, "ancient_coin": {"quantity": 3, "value": 12}},
        "exits": {
            "surface": {"target": "emerald_crystal_pool", "type": "named", "display": "Swim to surface"}
        }
    }

    rooms["emerald_crystal_falls_middle"] = {
        "id": "emerald_crystal_falls_middle",
        "name": "Crystal Falls - Middle Ledge",
        "description": "A narrow ledge behind the curtain of falling water. The rock face sparkles "
                       "with veins of raw crystal. Looking through the waterfall is like peering through "
                       "a shimmering lens — the jungle beyond ripples and glows.",
        "coordinates": [cx + 1, cy + 9],
        "location_type": "wilderness",
        "items": {"raw_crystal_vein": {"quantity": 1, "value": 22}},
        "exits": {
            "down": {"target": "emerald_crystal_falls_base", "type": "direction"},
            "up": {"target": "emerald_crystal_falls_top", "type": "direction"},
            "enter cave": {"target": "emerald_crystal_hidden_cave", "type": "named", "display": "Enter hidden cave"}
        }
    }

    rooms["emerald_crystal_hidden_cave"] = {
        "id": "emerald_crystal_hidden_cave",
        "name": "Hidden Cave Behind the Falls",
        "description": "A dry cave concealed behind the waterfall curtain. Crystal stalactites hang "
                       "from the ceiling, chiming softly in the vibration of the falls. A druidic "
                       "cache of supplies and a meditation circle occupy the far end.",
        "coordinates": [cx, cy + 9],
        "location_type": "wilderness",
        "items": {"crystal_stalactite": {"quantity": 1, "value": 28}, "druidic_meditation_stone": {"quantity": 1, "value": 20}},
        "exits": {
            "outside": {"target": "emerald_crystal_falls_middle", "type": "direction"}
        }
    }

    rooms["emerald_crystal_falls_top"] = {
        "id": "emerald_crystal_falls_top",
        "name": "Crystal Falls - Summit",
        "description": "The top of the waterfall, where a wide river tumbles over a crystal-encrusted "
                       "cliff edge. The view is breathtaking — the entire island stretches below in a "
                       "patchwork of green jungle, glowing grotto, and misty ruins.",
        "coordinates": [cx + 1, cy + 10],
        "location_type": "wilderness",
        "items": {"summit_crystal": {"quantity": 1, "value": 32}},
        "exits": {
            "down": {"target": "emerald_crystal_falls_middle", "type": "direction"},
            "west": {"target": "emerald_crystal_river_source", "type": "direction"}
        }
    }

    rooms["emerald_crystal_river_source"] = {
        "id": "emerald_crystal_river_source",
        "name": "Crystal River Source",
        "description": "A sacred spring bubbles up from a crack in crystal-veined rock, the source "
                       "of the waterfall's river. The water is perfectly pure and glows faintly blue. "
                       "Druids believe this spring is the island's living heart.",
        "coordinates": [cx, cy + 10],
        "location_type": "wilderness",
        "items": {"pure_spring_water": {"quantity": 1, "value": 26}, "source_crystal": {"quantity": 1, "value": 38}},
        "exits": {
            "east": {"target": "emerald_crystal_falls_top", "type": "direction"},
            "north": {"target": "emerald_crystal_prismatic_cave", "type": "direction"}
        }
    }

    rooms["emerald_crystal_falls_grotto"] = {
        "id": "emerald_crystal_falls_grotto",
        "name": "Mist Grotto",
        "description": "A shallow grotto carved by spray from the waterfall. Rainbow mist hangs "
                       "permanently in the air. Delicate crystal flowers have grown from the mineral-rich "
                       "deposits, their petals tinkling in the breeze like tiny bells.",
        "coordinates": [cx + 3, cy + 9],
        "location_type": "wilderness",
        "items": {"crystal_flower": {"quantity": 2, "value": 18}},
        "exits": {
            "south": {"target": "emerald_crystal_falls_base", "type": "direction"},
            "east": {"target": "emerald_crystal_rainbow_bridge", "type": "direction"}
        }
    }

    # --- Overgrown Ruins (8 rooms) ---

    rooms["emerald_ruins_approach"] = {
        "id": "emerald_ruins_approach",
        "name": "Ruins Approach",
        "description": "Crumbling stone columns, strangled by vines, line a once-grand avenue. "
                       "This civilization predates the druids by millennia. The paving stones are "
                       "cracked by roots but the craftsmanship is unmistakable.",
        "coordinates": [cx + 1, cy - 1],
        "location_type": "wilderness",
        "items": {"ancient_stone_chip": {"quantity": 2, "value": 8}},
        "exits": {
            "south": {"target": "emerald_beast_ancient_hollow", "type": "direction"},
            "north": {"target": "emerald_ruins_gate", "type": "direction"}
        }
    }

    rooms["emerald_ruins_gate"] = {
        "id": "emerald_ruins_gate",
        "name": "Ruined Gate",
        "description": "A massive stone archway, half-collapsed and overgrown with strangler figs. "
                       "Faded carvings depict a civilization that worshipped nature spirits long before "
                       "the druids arrived. Beyond lies a complex of vine-choked buildings.",
        "coordinates": [cx + 1, cy - 2],
        "location_type": "wilderness",
        "items": {},
        "exits": {
            "south": {"target": "emerald_ruins_approach", "type": "direction"},
            "north": {"target": "emerald_ruins_courtyard", "type": "direction"},
            "east": {"target": "emerald_ruins_watchtower", "type": "direction"}
        }
    }

    rooms["emerald_ruins_courtyard"] = {
        "id": "emerald_ruins_courtyard",
        "name": "Overgrown Courtyard",
        "description": "A wide courtyard where trees have burst through the flagstones. "
                       "A dry fountain in the center has been colonized by flowering vines. "
                       "Crumbling statues of forgotten nature gods peer from the undergrowth.",
        "coordinates": [cx + 1, cy - 3],
        "location_type": "wilderness",
        "items": {"ancient_idol_fragment": {"quantity": 1, "value": 25}},
        "exits": {
            "south": {"target": "emerald_ruins_gate", "type": "direction"},
            "west": {"target": "emerald_ruins_library", "type": "direction"},
            "east": {"target": "emerald_ruins_temple_exterior", "type": "direction"},
            "north": {"target": "emerald_ruins_inner_sanctum", "type": "direction"}
        }
    }

    rooms["emerald_ruins_watchtower"] = {
        "id": "emerald_ruins_watchtower",
        "name": "Ruined Watchtower",
        "description": "A crumbling stone tower wrapped in creeping ivy. The upper floors have "
                       "collapsed, but the ground level is still accessible. Arrow slits offer "
                       "views of the surrounding jungle. Old weapon racks hold corroded bronze blades.",
        "coordinates": [cx + 2, cy - 2],
        "location_type": "wilderness",
        "items": {"corroded_bronze_blade": {"quantity": 1, "value": 14}},
        "exits": {
            "west": {"target": "emerald_ruins_gate", "type": "direction"}
        }
    }

    rooms["emerald_ruins_library"] = {
        "id": "emerald_ruins_library",
        "name": "Ruined Library",
        "description": "Shelves of petrified wood still hold stone tablets inscribed with a forgotten "
                       "language. Moss has crept over everything, but some tablets remain legible. "
                       "A druid scholar sits cross-legged, carefully translating the ancient text.",
        "coordinates": [cx, cy - 3],
        "location_type": "wilderness",
        "npcs": ["druid_scholar"],
        "items": {"stone_tablet": {"quantity": 1, "value": 30}, "translation_notes": {"quantity": 1, "value": 18}},
        "exits": {
            "east": {"target": "emerald_ruins_courtyard", "type": "direction"},
            "south": {"target": "emerald_ruins_sealed_vault", "type": "direction"}
        }
    }

    rooms["emerald_ruins_temple_exterior"] = {
        "id": "emerald_ruins_temple_exterior",
        "name": "Temple Exterior",
        "description": "The largest structure in the ruins — a stepped pyramid smothered in jungle growth. "
                       "Massive roots grip the stonework like claws. A dark entrance gapes at the base, "
                       "leading into the temple interior. Druidic warning totems flank the entrance.",
        "coordinates": [cx + 2, cy - 3],
        "location_type": "wilderness",
        "items": {},
        "exits": {
            "west": {"target": "emerald_ruins_courtyard", "type": "direction"},
            "enter": {"target": "emerald_ruins_temple_interior", "type": "named", "display": "Enter the Temple"}
        }
    }

    rooms["emerald_ruins_temple_interior"] = {
        "id": "emerald_ruins_temple_interior",
        "name": "Temple Interior",
        "description": "The inside of the pyramid is surprisingly intact. Phosphorescent moss lights "
                       "carved walls depicting the rise and fall of the pre-druid civilization. A spiral "
                       "staircase descends deeper into the earth, toward the ancient sanctum.",
        "coordinates": [cx + 2, cy - 4],
        "location_type": "wilderness",
        "items": {"phosphorescent_moss": {"quantity": 2, "value": 10}, "carved_wall_rubbing": {"quantity": 1, "value": 22}},
        "exits": {
            "outside": {"target": "emerald_ruins_temple_exterior", "type": "direction"},
            "down": {"target": "emerald_ancient_sanctum", "type": "direction"},
            "descend": {"target": "emerald_ancient_sanctum", "type": "named", "display": "Descend to Ancient Sanctum"}
        }
    }

    rooms["emerald_ruins_inner_sanctum"] = {
        "id": "emerald_ruins_inner_sanctum",
        "name": "Inner Ruins",
        "description": "The deepest part of the surface ruins. Collapsed walls frame a mosaic floor "
                       "depicting the island before the jungle claimed it — a thriving city of stone "
                       "and crystal. Nature has reclaimed everything, but the beauty endures.",
        "coordinates": [cx + 1, cy - 4],
        "location_type": "wilderness",
        "items": {"mosaic_fragment": {"quantity": 1, "value": 20}, "crystal_shard_ancient": {"quantity": 1, "value": 26}},
        "exits": {
            "south": {"target": "emerald_ruins_courtyard", "type": "direction"},
            "west": {"target": "emerald_ruins_collapsed_wing", "type": "direction"}
        }
    }

    rooms["emerald_ancient_sanctum"] = {
        "id": "emerald_ancient_sanctum",
        "name": "Ancient Sanctum - Dungeon Entrance",
        "description": "Deep beneath the ruined temple, a vast chamber opens up. Living roots and "
                       "glowing crystal formations frame a titanic stone door covered in druidic wards. "
                       "Beyond lies the Verdant Sanctum — a living dungeon where nature itself "
                       "guards secrets older than civilization.",
        "coordinates": [cx + 2, cy - 5],
        "location_type": "wilderness",
        "items": {},
        "exits": {
            "up": {"target": "emerald_ruins_temple_interior", "type": "direction"},
            "enter": {
                "target": "FIXED_DUNGEON",
                "type": "fixed_dungeon",
                "dungeon_id": "verdant_sanctum",
                "transition_text": "You press your hand against the warded door. The druidic symbols flare green and the stone grinds open, releasing a gust of warm, earth-scented air. Roots pull aside like curtains, revealing the living depths of the Verdant Sanctum..."
            }
        }
    }

    # =========================================================================
    # EMERALD ISLE EXPANSION - New rooms doubling island size
    # =========================================================================

    # --- Expanded Docks (+3 rooms) ---

    rooms["emerald_dock_fishers_pier"] = {
        "id": "emerald_dock_fishers_pier",
        "name": "Fisher's Pier",
        "description": "A narrow pier of living wood juts into the emerald shallows. Druid fishers "
                       "sit cross-legged, their lines made of braided vine disappearing into water "
                       "teeming with iridescent fish. Woven baskets of fresh catch line the pier. "
                       "A pelican familiar watches from a post, occasionally snatching a fish.",
        "coordinates": [cx - 1, cy - 1],
        "location_type": "dock",
        "items": {"iridescent_fish": {"quantity": 2, "value": 10}, "vine_fishing_line": {"quantity": 1, "value": 8}},
        "exits": {
            "east": {"target": "emerald_dock_cargo", "type": "direction"},
            "south": {"target": "emerald_dock_tide_cave", "type": "direction"}
        }
    }

    rooms["emerald_dock_tide_cave"] = {
        "id": "emerald_dock_tide_cave",
        "name": "Tidal Cave",
        "description": "A sea cave carved into the cliff beneath the docks, accessible only at low "
                       "tide. The walls are encrusted with luminous sea anemones and the floor is a "
                       "mirror of standing water. Crates of old salvage are stacked against one wall — "
                       "likely washed in from some distant shipwreck.",
        "coordinates": [cx - 1, cy - 2],
        "location_type": "wilderness",
        "items": {"salvaged_compass": {"quantity": 1, "value": 18}, "sea_anemone": {"quantity": 2, "value": 6}},
        "exits": {
            "north": {"target": "emerald_dock_fishers_pier", "type": "direction"}
        }
    }

    rooms["emerald_dock_tidal_ledge"] = {
        "id": "emerald_dock_tidal_ledge",
        "name": "Tidal Ledge",
        "description": "A natural rock shelf extending from the lookout platform. Tide pools teem "
                       "with strange crustaceans and starfish in colors not found on the mainland. "
                       "A collection of drift-glass — sea-tumbled fragments of old bottles — sparkles "
                       "in the sunlight. The view of the reef barrier is spectacular.",
        "coordinates": [cx + 2, cy],
        "location_type": "wilderness",
        "items": {"drift_glass": {"quantity": 3, "value": 5}, "strange_starfish": {"quantity": 1, "value": 12}},
        "exits": {
            "west": {"target": "emerald_dock_lookout", "type": "direction"}
        }
    }

    # --- Expanded Druid Village (+10 rooms) ---

    rooms["emerald_village_herbalist"] = {
        "id": "emerald_village_herbalist",
        "name": "Herbalist's Greenhouse",
        "description": "A dome of woven branches and living leaves, warmed by enchanted sunstones. "
                       "Rows of potted plants from every climate grow in perfect harmony. The herbalist, "
                       "an elderly woman with moss-green eyes, tends to seedlings that seem to lean "
                       "toward her touch. Shelves hold labeled jars of dried herbs and tinctures.",
        "coordinates": [cx - 2, cy + 3],
        "location_type": "building",
        "items": {"healing_herb": {"quantity": 3, "value": 10}, "growth_tonic": {"quantity": 1, "value": 22}},
        "exits": {
            "east": {"target": "emerald_village_healer", "type": "direction"}
        }
    }

    rooms["emerald_village_library"] = {
        "id": "emerald_village_library",
        "name": "Druid Library",
        "description": "Built into the hollow of an ancient tree, this library uses shelf-fungus as "
                       "natural bookcases. Scrolls of bark-paper and bound codices of pressed leaves "
                       "contain centuries of druidic knowledge. A reading nook offers hammock-seats "
                       "suspended over a softly glowing root system. The librarian is an awakened owl.",
        "coordinates": [cx - 2, cy + 4],
        "location_type": "building",
        "items": {"bark_scroll": {"quantity": 1, "value": 15}, "druid_codex": {"quantity": 1, "value": 35}},
        "exits": {
            "south": {"target": "emerald_village_herbalist", "type": "direction"},
            "east": {"target": "emerald_village_inn", "type": "direction"}
        }
    }

    rooms["emerald_village_meditation"] = {
        "id": "emerald_village_meditation",
        "name": "Meditation Garden",
        "description": "A perfectly circular clearing carpeted with soft moss. Stepping stones spiral "
                       "inward to a central boulder worn smooth by generations of meditating druids. "
                       "Wind chimes of bone and crystal hang from the surrounding branches. The air "
                       "here feels thick with peace — even the insects move slowly.",
        "coordinates": [cx, cy + 6],
        "location_type": "wilderness",
        "items": {},
        "exits": {
            "south": {"target": "emerald_village_lookout", "type": "direction"},
            "east": {"target": "emerald_village_seed_vault", "type": "direction"}
        }
    }

    rooms["emerald_village_seed_vault"] = {
        "id": "emerald_village_seed_vault",
        "name": "Seed Vault",
        "description": "A cool underground chamber accessed through a root-woven trapdoor. Hundreds "
                       "of clay jars line the walls, each containing seeds from species across the world. "
                       "Some jars glow, others frost over, and a few vibrate gently. A preservation "
                       "enchantment keeps everything in perfect stasis. This is the druids' greatest treasure.",
        "coordinates": [cx + 1, cy + 6],
        "location_type": "building",
        "items": {"rare_seed_pouch": {"quantity": 1, "value": 40}},
        "exits": {
            "west": {"target": "emerald_village_meditation", "type": "direction"}
        }
    }

    rooms["emerald_village_treehouse_dorm"] = {
        "id": "emerald_village_treehouse_dorm",
        "name": "Treehouse Dormitory",
        "description": "A cluster of small sleeping pods grown into the canopy, connected by rope "
                       "bridges and vine ladders. Each pod is a cozy nest of woven leaves and soft "
                       "moss. Apprentice druids sleep here, their dreams shaped by the tree's own "
                       "ancient memories. Glowbugs serve as nightlights.",
        "coordinates": [cx - 2, cy + 5],
        "location_type": "building",
        "items": {},
        "exits": {
            "east": {"target": "emerald_village_stables", "type": "direction"}
        }
    }

    rooms["emerald_village_animal_clinic"] = {
        "id": "emerald_village_animal_clinic",
        "name": "Animal Infirmary",
        "description": "A large open-air shelter where injured forest creatures are nursed back to "
                       "health. A three-legged fox sleeps on a mossy bed. A hawk with a splinted wing "
                       "watches from a perch. The druid veterinarian hums softly while bandaging a "
                       "badger's paw with poultices of healing leaves.",
        "coordinates": [cx - 1, cy + 2],
        "location_type": "building",
        "items": {"healing_poultice": {"quantity": 2, "value": 12}},
        "exits": {
            "east": {"target": "emerald_village_gate", "type": "direction"},
            "north": {"target": "emerald_village_workshop", "type": "direction"}
        }
    }

    rooms["emerald_village_council_grove"] = {
        "id": "emerald_village_council_grove",
        "name": "Council Grove",
        "description": "A ring of ancient trees whose branches have grown together to form a natural "
                       "amphitheater. Stone seats carved with animal totems face a central speaking "
                       "stump. This is where the druid circle gathers to debate and make decisions. "
                       "Offerings of fruit and flowers are left at the base of each tree.",
        "coordinates": [cx + 2, cy + 4],
        "location_type": "settlement",
        "items": {},
        "exits": {
            "south": {"target": "emerald_village_training", "type": "direction"},
            "west": {"target": "emerald_elder_house", "type": "direction"}
        }
    }

    rooms["emerald_village_moonwell"] = {
        "id": "emerald_village_moonwell",
        "name": "Moonwell",
        "description": "A natural pool fed by an underground spring, perfectly circular, that reflects "
                       "moonlight even during the day. The water surface shows visions to those with "
                       "the gift — flickering images of distant places and possible futures. Silver "
                       "coins glint at the bottom, offerings from generations of seekers.",
        "coordinates": [cx + 2, cy + 5],
        "location_type": "wilderness",
        "items": {"moonwater_vial": {"quantity": 1, "value": 30}},
        "exits": {
            "west": {"target": "emerald_village_east_bridge", "type": "direction"},
            "south": {"target": "emerald_village_council_grove", "type": "direction"}
        }
    }

    rooms["emerald_village_root_cellar"] = {
        "id": "emerald_village_root_cellar",
        "name": "Root Cellar",
        "description": "A cool underground room woven from living roots, used to store preserved "
                       "foods. Bundles of dried mushrooms, smoked fish, jarred honey, and fermented "
                       "berry wine line shelves of shelf-fungus. The root walls pulse faintly with "
                       "the tree's heartbeat. A heavy sweetness fills the air.",
        "coordinates": [cx - 1, cy + 1],
        "location_type": "building",
        "items": {"berry_wine": {"quantity": 2, "value": 8}, "jarred_honey": {"quantity": 1, "value": 12}},
        "exits": {
            "up": {"target": "emerald_village_workshop", "type": "direction"}
        }
    }

    rooms["emerald_village_apprentice_quarters"] = {
        "id": "emerald_village_apprentice_quarters",
        "name": "Apprentice Quarters",
        "description": "A communal space where young druids study and practice. Chalk circles on "
                       "the floor mark practice areas for simple growth spells. A board displays "
                       "daily assignments. Several apprentices sit in a circle, concentrating on "
                       "making a flower bloom — with mixed results.",
        "coordinates": [cx + 2, cy + 2],
        "location_type": "building",
        "items": {"practice_wand": {"quantity": 1, "value": 8}},
        "exits": {
            "west": {"target": "emerald_village_garden", "type": "direction"},
            "north": {"target": "emerald_village_training", "type": "direction"}
        }
    }

    # --- Expanded Rainforest (+10 rooms) ---

    rooms["emerald_rain_spider_canopy"] = {
        "id": "emerald_rain_spider_canopy",
        "name": "Spider Silk Canopy",
        "description": "The trees here are connected by vast webs of golden spider silk, strong "
                       "enough to walk on. Enormous orb-weavers the size of dogs tend their webs, "
                       "paying little attention to visitors. The silk catches the light like spun "
                       "gold. Druids harvest it carefully for enchanted textiles.",
        "coordinates": [cx + 4, cy + 7],
        "location_type": "wilderness",
        "items": {"golden_spider_silk": {"quantity": 1, "value": 35}},
        "exits": {
            "west": {"target": "emerald_rain_hollow_log", "type": "direction"},
            "north": {"target": "emerald_rain_quicksand_bog", "type": "direction"},
            "south": {"target": "emerald_rain_canopy_nest", "type": "direction"}
        }
    }

    rooms["emerald_rain_quicksand_bog"] = {
        "id": "emerald_rain_quicksand_bog",
        "name": "Quicksand Bog",
        "description": "A treacherous stretch where the ground looks solid but isn't. Warning stakes "
                       "driven by druids mark the safe path between patches of liquid earth. A half- "
                       "swallowed statue — clearly ancient — reaches one stone arm above the mire. "
                       "Bubbles of swamp gas burst with faint phosphorescent light.",
        "coordinates": [cx + 4, cy + 8],
        "location_type": "wilderness",
        "items": {},
        "exits": {
            "south": {"target": "emerald_rain_spider_canopy", "type": "direction"},
            "west": {"target": "emerald_rain_monkey_temple", "type": "direction"}
        }
    }

    rooms["emerald_rain_monkey_temple"] = {
        "id": "emerald_rain_monkey_temple",
        "name": "Monkey Temple",
        "description": "A small ruined shrine overrun by a troop of clever monkeys who treat it as "
                       "their kingdom. They've arranged shiny objects on the altar as offerings and "
                       "wear fragments of old jewelry. Their leader — a grizzled silver-back with "
                       "one blind eye — watches from the crumbling pediment with unsettling intelligence.",
        "coordinates": [cx + 3, cy + 8],
        "location_type": "wilderness",
        "items": {"shiny_trinket": {"quantity": 2, "value": 8}, "old_ring": {"quantity": 1, "value": 20}},
        "exits": {
            "east": {"target": "emerald_rain_quicksand_bog", "type": "direction"},
            "south": {"target": "emerald_rain_canopy_walk", "type": "direction"}
        }
    }

    rooms["emerald_rain_firefly_hollow"] = {
        "id": "emerald_rain_firefly_hollow",
        "name": "Firefly Hollow",
        "description": "A bowl-shaped depression in the forest where thousands of fireflies gather "
                       "at all hours, creating a permanent constellation of drifting golden light. "
                       "The hollow is eerily quiet — no bird calls, no insect drone — just the soft "
                       "pulse of living light. It feels sacred, or at least something demands silence.",
        "coordinates": [cx + 5, cy + 5],
        "location_type": "wilderness",
        "items": {"firefly_jar": {"quantity": 1, "value": 15}},
        "exits": {
            "west": {"target": "emerald_rain_ancient_tree", "type": "direction"}
        }
    }

    rooms["emerald_rain_serpent_den"] = {
        "id": "emerald_rain_serpent_den",
        "name": "Serpent's Den",
        "description": "A tangle of exposed roots creates a warren of tunnels beneath a massive tree. "
                       "Shed snakeskins — some impossibly long — drape from branches. A low hissing "
                       "resonates from deep within. The druids mark this area with warning totems: "
                       "the great serpent who nests here is old, venomous, and deeply territorial.",
        "coordinates": [cx + 5, cy + 4],
        "location_type": "wilderness",
        "items": {"shed_snakeskin": {"quantity": 1, "value": 18}},
        "exits": {
            "north": {"target": "emerald_rain_firefly_hollow", "type": "direction"},
            "west": {"target": "emerald_rain_jungle_floor", "type": "direction"}
        }
    }

    rooms["emerald_rain_river_crossing"] = {
        "id": "emerald_rain_river_crossing",
        "name": "River Crossing",
        "description": "A wide, shallow river cuts through the forest, its bed paved with smooth "
                       "stones that glow faintly green. Stepping stones provide a path across, but "
                       "the current is deceptively strong. Fish with translucent skin dart between "
                       "the stones. A rope bridge offers a safer but longer crossing upstream.",
        "coordinates": [cx + 3, cy + 3],
        "location_type": "wilderness",
        "items": {},
        "exits": {
            "north": {"target": "emerald_rain_fern_valley", "type": "direction"},
            "south": {"target": "emerald_beast_thicket", "type": "direction"}
        }
    }

    rooms["emerald_rain_giant_fern"] = {
        "id": "emerald_rain_giant_fern",
        "name": "Giant Fern Clearing",
        "description": "Ferns here grow to impossible sizes — their fronds fifteen feet across, "
                       "creating a canopy below the canopy. The filtered light is deep green and "
                       "dreamlike. Insects the size of birds buzz between the frond-tips. The ground "
                       "is carpeted in tiny white flowers that close when you step near them.",
        "coordinates": [cx + 5, cy + 6],
        "location_type": "wilderness",
        "items": {"giant_fern_frond": {"quantity": 1, "value": 10}},
        "exits": {
            "west": {"target": "emerald_rain_canopy_nest", "type": "direction"},
            "south": {"target": "emerald_rain_firefly_hollow", "type": "direction"}
        }
    }

    rooms["emerald_rain_canopy_observatory"] = {
        "id": "emerald_rain_canopy_observatory",
        "name": "Canopy Observatory",
        "description": "A druid-built platform at the very top of the tallest tree, above even the "
                       "canopy. For the first time, you can see the sky. The rainforest stretches "
                       "endlessly in every direction, a sea of green with the crystal waterfall "
                       "glinting to the north. Mist clings to valleys. Bird flocks wheel below you.",
        "coordinates": [cx + 5, cy + 7],
        "location_type": "building",
        "items": {},
        "exits": {
            "down": {"target": "emerald_rain_giant_fern", "type": "direction"}
        }
    }

    rooms["emerald_rain_fallen_titan"] = {
        "id": "emerald_rain_fallen_titan",
        "name": "Fallen Titan Tree",
        "description": "A tree so massive that its fall created a clearing a hundred yards wide. "
                       "Its trunk — wider than a house — lies on its side, colonized by an entire "
                       "ecosystem of moss, ferns, mushrooms, and small animals. You can walk along "
                       "the top like a road, or explore the cave-like spaces beneath its bulk.",
        "coordinates": [cx + 2, cy + 9],
        "location_type": "wilderness",
        "items": {"titan_bark": {"quantity": 1, "value": 22}},
        "exits": {
            "south": {"target": "emerald_rain_waterfall_path", "type": "direction"},
            "east": {"target": "emerald_rain_druid_recluse", "type": "direction"}
        }
    }

    rooms["emerald_rain_druid_recluse"] = {
        "id": "emerald_rain_druid_recluse",
        "name": "Recluse Druid's Camp",
        "description": "A small camp belonging to a druid who left the village years ago to live "
                       "alone in the deep forest. A hammock hangs between two trees, and a fire pit "
                       "holds warm coals. Carved wooden animals line a shelf — each one enchanted "
                       "to move when no one watches. The recluse herself is rarely here.",
        "coordinates": [cx + 3, cy + 9],
        "location_type": "wilderness",
        "items": {"enchanted_carving": {"quantity": 1, "value": 25}},
        "exits": {
            "west": {"target": "emerald_rain_fallen_titan", "type": "direction"}
        }
    }

    # --- Expanded Mushroom Grotto (+8 rooms) ---

    rooms["emerald_grotto_spore_nursery"] = {
        "id": "emerald_grotto_spore_nursery",
        "name": "Spore Nursery",
        "description": "A warm, humid chamber where druids cultivate rare fungal species. Beds of "
                       "composted leaf-litter host tiny mushrooms in every color. Spore clouds drift "
                       "lazily through the amber light. Labels written in druidic script identify "
                       "each species — some marked with skull symbols for the poisonous ones.",
        "coordinates": [cx - 2, cy + 5],
        "location_type": "building",
        "items": {"rare_spore_sample": {"quantity": 1, "value": 20}},
        "exits": {
            "north": {"target": "emerald_grotto_echo_chamber", "type": "direction"},
            "east": {"target": "emerald_grotto_deep_roots", "type": "direction"},
            "south": {"target": "emerald_grotto_toadstool_throne", "type": "direction"}
        }
    }

    rooms["emerald_grotto_toadstool_throne"] = {
        "id": "emerald_grotto_toadstool_throne",
        "name": "Toadstool Throne",
        "description": "A massive toadstool — ten feet across — dominates this chamber like a "
                       "natural throne. Its cap is mottled red and gold, and the stem is carved with "
                       "ancient symbols. Legend says the first druid of the island sat here and spoke "
                       "with the forest's spirit. The air tastes of old magic and earth.",
        "coordinates": [cx - 2, cy + 4],
        "location_type": "wilderness",
        "items": {},
        "exits": {
            "north": {"target": "emerald_grotto_spore_nursery", "type": "direction"},
            "east": {"target": "emerald_sanctum_spirit_pool", "type": "direction"},
            "south": {"target": "emerald_grotto_biolum_tunnel", "type": "direction"}
        }
    }

    rooms["emerald_grotto_biolum_tunnel"] = {
        "id": "emerald_grotto_biolum_tunnel",
        "name": "Bioluminescent Tunnel",
        "description": "A long natural passage where every surface glows. The walls are coated in "
                       "bioluminescent fungus that shifts between blue, green, and violet. The effect "
                       "is mesmerizing — like walking through a living aurora. Dripping water creates "
                       "a gentle percussion. Small blind cave fish swim in the floor channels.",
        "coordinates": [cx - 2, cy + 3],
        "location_type": "wilderness",
        "items": {"glowing_moss_sample": {"quantity": 1, "value": 14}},
        "exits": {
            "north": {"target": "emerald_grotto_toadstool_throne", "type": "direction"},
            "east": {"target": "emerald_grotto_mycelium_heart", "type": "direction"}
        }
    }

    rooms["emerald_grotto_mycelium_heart"] = {
        "id": "emerald_grotto_mycelium_heart",
        "name": "Mycelium Heart",
        "description": "The central node of the island's underground fungal network. Thousands of "
                       "white threads converge here, pulsing with faint light in rhythmic waves. "
                       "Druids believe this mycelium connects every tree on the island, allowing them "
                       "to share water and warnings. Touching the threads fills your mind with "
                       "distant whispers of rustling leaves.",
        "coordinates": [cx - 1, cy + 3],
        "location_type": "wilderness",
        "items": {"mycelium_strand": {"quantity": 1, "value": 30}},
        "exits": {
            "west": {"target": "emerald_grotto_biolum_tunnel", "type": "direction"},
            "north": {"target": "emerald_village_healer", "type": "direction"}
        }
    }

    rooms["emerald_grotto_shroomling_nest"] = {
        "id": "emerald_grotto_shroomling_nest",
        "name": "Shroomling Nest",
        "description": "Tiny mushroom creatures — shroomlings — have built a miniature village in "
                       "this alcove. Houses of stacked pebbles, bridges of twigs, and a central "
                       "meeting circle of pebbles arranged in a spiral. The shroomlings peer at you "
                       "with bead-like eyes, neither fearful nor aggressive, just curious.",
        "coordinates": [cx - 3, cy + 7],
        "location_type": "wilderness",
        "items": {"tiny_mushroom_house": {"quantity": 1, "value": 6}},
        "exits": {
            "east": {"target": "emerald_grotto_shroomlight_hall", "type": "direction"}
        }
    }

    rooms["emerald_grotto_cap_bridge"] = {
        "id": "emerald_grotto_cap_bridge",
        "name": "Mushroom Cap Bridge",
        "description": "Giant mushroom caps grow from the cavern walls on both sides, meeting in "
                       "the middle to form a natural bridge over a dark chasm. The caps are springy "
                       "underfoot and bounce slightly with each step. Looking down reveals nothing — "
                       "the chasm is seemingly bottomless, and a cold draft rises from below.",
        "coordinates": [cx - 3, cy + 6],
        "location_type": "wilderness",
        "items": {},
        "exits": {
            "north": {"target": "emerald_grotto_shroomling_nest", "type": "direction"},
            "east": {"target": "emerald_grotto_echo_chamber", "type": "direction"}
        }
    }

    rooms["emerald_grotto_underground_lake"] = {
        "id": "emerald_grotto_underground_lake",
        "name": "Underground Lake",
        "description": "A vast subterranean lake stretches into darkness, its surface perfectly still "
                       "and black as obsidian. Tiny points of bioluminescent light dot the ceiling "
                       "like stars, creating a mirror image on the water. A small wooden boat is "
                       "tied to a natural pier. The silence here is absolute and deeply unsettling.",
        "coordinates": [cx - 3, cy + 5],
        "location_type": "wilderness",
        "items": {},
        "exits": {
            "north": {"target": "emerald_grotto_cap_bridge", "type": "direction"},
            "east": {"target": "emerald_grotto_spore_nursery", "type": "direction"}
        }
    }

    rooms["emerald_grotto_mushroom_market"] = {
        "id": "emerald_grotto_mushroom_market",
        "name": "Mushroom Market",
        "description": "A small cavern where druid foragers trade fungal harvests. Tables of flat "
                       "stone display varieties of edible, medicinal, and magical mushrooms. A "
                       "cheerful druid with a mushroom-cap hat weighs portions on a hanging scale. "
                       "Price tags are written on bark chips. The smell is earthy and rich.",
        "coordinates": [cx, cy + 8],
        "location_type": "settlement",
        "items": {"healing_mushroom": {"quantity": 2, "value": 12}, "mind_cap": {"quantity": 1, "value": 28}},
        "exits": {
            "south": {"target": "emerald_grotto_spore_tunnel", "type": "direction"}
        }
    }

    # --- Expanded Druid Sanctum (+6 rooms) ---

    rooms["emerald_sanctum_library_deep"] = {
        "id": "emerald_sanctum_library_deep",
        "name": "Inner Sanctum Library",
        "description": "A hidden chamber within the sanctum where the druids' most precious texts "
                       "are kept. Scrolls of living bark that rewrite themselves with the seasons. "
                       "A tome bound in feathers that reads aloud when opened. The oldest text "
                       "is a stone slab in a language no living druid can decipher, but the plants "
                       "in its presence grow twice as fast.",
        "coordinates": [cx - 5, cy + 5],
        "location_type": "building",
        "items": {"feather_tome": {"quantity": 1, "value": 45}},
        "exits": {
            "east": {"target": "emerald_sanctum_inner_ring", "type": "direction"}
        }
    }

    rooms["emerald_sanctum_star_platform"] = {
        "id": "emerald_sanctum_star_platform",
        "name": "Star-Gazing Platform",
        "description": "A high platform above the canopy, reached by a spiral staircase of living "
                       "wood. At night, druids observe the stars to guide planting and ritual timing. "
                       "The platform is inscribed with a permanent star chart inlaid with silver. "
                       "During the day, you can see the entire island spread below you.",
        "coordinates": [cx - 5, cy + 6],
        "location_type": "building",
        "items": {"star_chart_fragment": {"quantity": 1, "value": 20}},
        "exits": {
            "south": {"target": "emerald_sanctum_library_deep", "type": "direction"},
            "east": {"target": "emerald_sanctum_sacred_grove", "type": "direction"}
        }
    }

    rooms["emerald_sanctum_crystal_seed_vault"] = {
        "id": "emerald_sanctum_crystal_seed_vault",
        "name": "Crystal Seed Vault",
        "description": "Seeds of extinct and legendary plants are preserved here in individual "
                       "crystal capsules, each enchanted to maintain stasis indefinitely. The seeds "
                       "glow with their own inner light — a world-tree seed burns golden, a midnight "
                       "rose seed pulses black-purple. This is the druids' ultimate insurance policy.",
        "coordinates": [cx - 5, cy + 4],
        "location_type": "building",
        "items": {},
        "exits": {
            "north": {"target": "emerald_sanctum_library_deep", "type": "direction"},
            "east": {"target": "emerald_sanctum_ley_nexus", "type": "direction"}
        }
    }

    rooms["emerald_sanctum_spirit_chamber"] = {
        "id": "emerald_sanctum_spirit_chamber",
        "name": "Spirit Communication Chamber",
        "description": "A round room with walls of polished wood, where druids commune with nature "
                       "spirits. Incense of sage and cedar fills the air. Sitting in the center "
                       "circle, you can hear distant voices — the murmur of the trees, the whisper "
                       "of the wind, the slow pulse of the earth itself. It's overwhelming and "
                       "beautiful and terrifying all at once.",
        "coordinates": [cx - 3, cy + 4],
        "location_type": "building",
        "items": {"spirit_incense": {"quantity": 2, "value": 15}},
        "exits": {
            "north": {"target": "emerald_sanctum_outer_ring", "type": "direction"},
            "west": {"target": "emerald_sanctum_crystal_seed_vault", "type": "direction"}
        }
    }

    rooms["emerald_sanctum_living_wood_corridor"] = {
        "id": "emerald_sanctum_living_wood_corridor",
        "name": "Living Wood Corridor",
        "description": "A passageway where the walls, floor, and ceiling are all formed of living "
                       "wood that slowly shifts and grows. Faces appear and fade in the grain. "
                       "Branches reach out as if to touch you, then retract. The corridor breathes — "
                       "expanding and contracting with a rhythm like a sleeping creature.",
        "coordinates": [cx - 4, cy + 3],
        "location_type": "wilderness",
        "items": {},
        "exits": {
            "north": {"target": "emerald_sanctum_inner_ring", "type": "direction"},
            "east": {"target": "emerald_sanctum_ley_nexus", "type": "direction"},
            "south": {"target": "emerald_sanctum_root_of_ages", "type": "direction"}
        }
    }

    rooms["emerald_sanctum_root_of_ages"] = {
        "id": "emerald_sanctum_root_of_ages",
        "name": "Root of Ages",
        "description": "The terminus of the sanctum — a titanic root as wide as a road, plunging "
                       "straight down into the earth. Its surface is carved with a continuous record "
                       "of the island's history, from the first seed to the present day. The carving "
                       "continues to grow, adding new lines at the edge. Touching the root floods "
                       "you with memories that aren't yours — centuries compressed into heartbeats.",
        "coordinates": [cx - 4, cy + 2],
        "location_type": "wilderness",
        "items": {"root_shaving": {"quantity": 1, "value": 35}},
        "exits": {
            "north": {"target": "emerald_sanctum_living_wood_corridor", "type": "direction"}
        }
    }

    # --- Expanded Beast Wilds (+8 rooms) ---

    rooms["emerald_beast_stampede_plain"] = {
        "id": "emerald_beast_stampede_plain",
        "name": "Stampede Plain",
        "description": "A rare open area in the jungle where herds of large herbivores graze on "
                       "tough elephant grass. The ground is trampled flat and rutted with hoofprints. "
                       "When startled, these beasts stampede with earth-shaking force. Druids have "
                       "placed warning totems at the edges. You can feel vibrations through your feet.",
        "coordinates": [cx + 3, cy],
        "location_type": "wilderness",
        "items": {},
        "exits": {
            "north": {"target": "emerald_beast_den", "type": "direction"},
            "west": {"target": "emerald_beast_nesting_grounds", "type": "direction"},
            "east": {"target": "emerald_beast_boundary_markers", "type": "direction"}
        }
    }

    rooms["emerald_beast_boundary_markers"] = {
        "id": "emerald_beast_boundary_markers",
        "name": "Territorial Boundary",
        "description": "Trees here are scarred with deep claw marks — territorial warnings from "
                       "the island's apex predators. Druid totems mark a boundary between the "
                       "relatively safe outer wilds and the truly dangerous inner territory. "
                       "Beyond this point, even experienced druids travel in pairs.",
        "coordinates": [cx + 4, cy],
        "location_type": "wilderness",
        "items": {"claw_mark_casting": {"quantity": 1, "value": 16}},
        "exits": {
            "west": {"target": "emerald_beast_stampede_plain", "type": "direction"},
            "north": {"target": "emerald_beast_ravine", "type": "direction"},
            "south": {"target": "emerald_beast_graveyard", "type": "direction"}
        }
    }

    rooms["emerald_beast_graveyard"] = {
        "id": "emerald_beast_graveyard",
        "name": "Beast Graveyard",
        "description": "A clearing where dying animals come to pass on. Immense skeletons of "
                       "creatures that haven't existed for centuries lie half-buried in moss. "
                       "The newest remains still have scraps of hide. The air is heavy with "
                       "reverence — even predators don't hunt here. It's an unspoken truce ground.",
        "coordinates": [cx + 4, cy - 1],
        "location_type": "wilderness",
        "items": {"ancient_fang": {"quantity": 1, "value": 28}, "beast_bone": {"quantity": 2, "value": 6}},
        "exits": {
            "north": {"target": "emerald_beast_boundary_markers", "type": "direction"}
        }
    }

    rooms["emerald_beast_alpha_cave"] = {
        "id": "emerald_beast_alpha_cave",
        "name": "Alpha's Cave",
        "description": "A deep cave that serves as the lair of the island's alpha predator — a "
                       "creature of terrifying size with bioluminescent markings. The cave floor "
                       "is littered with shattered bone and shed scales. Claw gouges in the stone "
                       "walls are inches deep. The beast is out hunting, but it could return at any moment.",
        "coordinates": [cx + 2, cy - 1],
        "location_type": "wilderness",
        "items": {"alpha_scale": {"quantity": 1, "value": 40}},
        "exits": {
            "north": {"target": "emerald_beast_alpha_territory", "type": "direction"}
        }
    }

    rooms["emerald_beast_watering_hole_deep"] = {
        "id": "emerald_beast_watering_hole_deep",
        "name": "Deep Watering Hole",
        "description": "A second, hidden pool fed by underground streams. The water is crystal clear, "
                       "and the bottom is visible twenty feet down — a trove of dropped antlers, "
                       "lost tusks, and mineral-crusted bones from millennia of animal visitors. "
                       "Dragonflies with four-inch wingspans patrol the surface.",
        "coordinates": [cx + 1, cy + 1],
        "location_type": "wilderness",
        "items": {"mineral_tusk": {"quantity": 1, "value": 22}},
        "exits": {
            "east": {"target": "emerald_beast_watering_hole", "type": "direction"},
            "north": {"target": "emerald_village_animal_clinic", "type": "direction"}
        }
    }

    rooms["emerald_beast_predator_den"] = {
        "id": "emerald_beast_predator_den",
        "name": "Predator's Second Den",
        "description": "A shallow overhang where a pack of jungle raptors has made its home. "
                       "Feathers and broken eggshells litter the ground. The pack is small but "
                       "fiercely coordinated — they hunt in pairs, communicate with clicks and "
                       "whistles, and show tool-use behavior that unsettles even experienced druids.",
        "coordinates": [cx + 5, cy + 3],
        "location_type": "wilderness",
        "items": {"raptor_feather": {"quantity": 2, "value": 14}},
        "exits": {
            "west": {"target": "emerald_rain_predator_trail", "type": "direction"},
            "south": {"target": "emerald_beast_hunting_grounds", "type": "direction"}
        }
    }

    rooms["emerald_beast_trainer_camp"] = {
        "id": "emerald_beast_trainer_camp",
        "name": "Beast Trainer's Camp",
        "description": "A druid beast-handler has set up a semi-permanent camp at the edge of the "
                       "wilds. Cages of woven green-wood hold injured animals being rehabilitated. "
                       "A taming circle drawn in chalk marks the training area. The handler — muscles "
                       "covered in scars and tattoos — feeds raw meat to a juvenile raptor on a leash.",
        "coordinates": [cx + 3, cy + 2],
        "location_type": "settlement",
        "npcs": ["beast_handler"],
        "items": {"beast_treat": {"quantity": 3, "value": 5}, "taming_whistle": {"quantity": 1, "value": 25}},
        "exits": {
            "north": {"target": "emerald_rain_river_crossing", "type": "direction"},
            "east": {"target": "emerald_beast_thicket", "type": "direction"},
            "south": {"target": "emerald_beast_den", "type": "direction"}
        }
    }

    rooms["emerald_beast_raptor_clearing"] = {
        "id": "emerald_beast_raptor_clearing",
        "name": "Raptor Clearing",
        "description": "Claw marks on every tree, feathers caught in undergrowth, and the acrid "
                       "smell of raptor musk. This is a feeding ground — fresh carcasses of smaller "
                       "animals are partially consumed. The raptors aren't here now, but the scattered "
                       "remains suggest they'll return soon. Your instincts scream to leave.",
        "coordinates": [cx + 5, cy + 2],
        "location_type": "wilderness",
        "items": {},
        "exits": {
            "west": {"target": "emerald_beast_hunting_grounds", "type": "direction"},
            "south": {"target": "emerald_beast_predator_den", "type": "direction"}
        }
    }

    # --- Expanded Crystal Waterfall (+6 rooms) ---

    rooms["emerald_crystal_prismatic_cave"] = {
        "id": "emerald_crystal_prismatic_cave",
        "name": "Prismatic Cave",
        "description": "A cave where natural crystal formations split incoming light into permanent "
                       "rainbows that dance across every surface. The crystals hum at different "
                       "frequencies — some audible, some felt as vibrations in your bones. Druids "
                       "come here to attune themselves with the island's crystal lattice.",
        "coordinates": [cx, cy + 11],
        "location_type": "wilderness",
        "items": {"prism_crystal": {"quantity": 1, "value": 35}},
        "exits": {
            "south": {"target": "emerald_crystal_river_source", "type": "direction"},
            "east": {"target": "emerald_crystal_ice_formation", "type": "direction"}
        }
    }

    rooms["emerald_crystal_ice_formation"] = {
        "id": "emerald_crystal_ice_formation",
        "name": "Ice Crystal Formation",
        "description": "Despite the tropical climate, this section of cave is freezing cold. Ice "
                       "crystals grow from the walls in impossible fractal patterns, their edges "
                       "razor-sharp. Your breath mists. The cold radiates from a single massive "
                       "crystal in the center that druids say fell from the moon centuries ago.",
        "coordinates": [cx + 1, cy + 11],
        "location_type": "wilderness",
        "items": {"lunar_ice_shard": {"quantity": 1, "value": 45}},
        "exits": {
            "west": {"target": "emerald_crystal_prismatic_cave", "type": "direction"}
        }
    }

    rooms["emerald_crystal_rainbow_bridge"] = {
        "id": "emerald_crystal_rainbow_bridge",
        "name": "Rainbow Bridge",
        "description": "A natural arch of crystallized water vapor spans a misty gorge. The bridge "
                       "is solid enough to walk on but entirely transparent — you can see through it "
                       "to the waterfall mist swirling a hundred feet below. Rainbows arc through "
                       "the spray, making the bridge shimmer with color. It's terrifying and beautiful.",
        "coordinates": [cx + 4, cy + 9],
        "location_type": "wilderness",
        "items": {},
        "exits": {
            "west": {"target": "emerald_crystal_falls_grotto", "type": "direction"},
            "east": {"target": "emerald_crystal_pool_cavern", "type": "direction"}
        }
    }

    rooms["emerald_crystal_pool_cavern"] = {
        "id": "emerald_crystal_pool_cavern",
        "name": "Crystal Pool Cavern",
        "description": "Behind the waterfall's mist, a hidden cavern holds a pool of water so "
                       "clear it's invisible until you touch it. The cavern walls are encrusted "
                       "with crystal formations that amplify sound — a whisper becomes a chorus. "
                       "Druids use this as a healing pool; the mineral-rich water mends wounds.",
        "coordinates": [cx + 5, cy + 9],
        "location_type": "wilderness",
        "items": {"crystal_water_flask": {"quantity": 1, "value": 28}},
        "exits": {
            "west": {"target": "emerald_crystal_rainbow_bridge", "type": "direction"}
        }
    }

    rooms["emerald_crystal_falls_peak"] = {
        "id": "emerald_crystal_falls_peak",
        "name": "Waterfall's Peak",
        "description": "The absolute summit above the crystal waterfall. A flat rock platform "
                       "offers a dizzying view of the water cascading down hundreds of feet into "
                       "the mist below. Eagles nest on the cliff face. The wind is fierce up here, "
                       "and spray coats everything in a fine mist that catches the light.",
        "coordinates": [cx + 1, cy + 12],
        "location_type": "wilderness",
        "items": {"eagle_feather": {"quantity": 1, "value": 18}},
        "exits": {
            "south": {"target": "emerald_crystal_falls_top", "type": "direction"}
        }
    }

    rooms["emerald_crystal_mist_path"] = {
        "id": "emerald_crystal_mist_path",
        "name": "Mist-Shrouded Path",
        "description": "A narrow path cut into the cliff face behind the waterfall. You're walking "
                       "through the falling water itself — a curtain of crystalline droplets. The "
                       "roar is deafening, the mist drenching. Through gaps in the water-curtain, "
                       "you catch fragments of the jungle far below, dreamlike and distorted.",
        "coordinates": [cx + 2, cy + 10],
        "location_type": "wilderness",
        "items": {},
        "exits": {
            "south": {"target": "emerald_crystal_falls_base", "type": "direction"},
            "north": {"target": "emerald_crystal_falls_peak", "type": "direction"}
        }
    }

    # --- Expanded Overgrown Ruins (+5 rooms) ---

    rooms["emerald_ruins_collapsed_wing"] = {
        "id": "emerald_ruins_collapsed_wing",
        "name": "Collapsed Wing",
        "description": "An entire section of the ancient complex has fallen in on itself. Massive "
                       "stone blocks lie at angles, creating a maze of narrow passages between them. "
                       "Vines have woven through the rubble, stabilizing some sections while slowly "
                       "pulling others apart. Fragments of painted murals are barely visible.",
        "coordinates": [cx, cy - 4],
        "location_type": "wilderness",
        "items": {"mural_fragment": {"quantity": 1, "value": 20}},
        "exits": {
            "east": {"target": "emerald_ruins_inner_sanctum", "type": "direction"},
            "south": {"target": "emerald_ruins_forgotten_throne", "type": "direction"}
        }
    }

    rooms["emerald_ruins_forgotten_throne"] = {
        "id": "emerald_ruins_forgotten_throne",
        "name": "Forgotten Throne Room",
        "description": "A grand hall, its ceiling long since collapsed to open sky. A throne of "
                       "green marble sits on a raised dais, a small tree growing from its seat. "
                       "Whoever ruled here did so in an age the druids can't recall. The craftsmanship "
                       "exceeds anything on the mainland. The throne hums when you approach it.",
        "coordinates": [cx, cy - 5],
        "location_type": "wilderness",
        "items": {"throne_gem": {"quantity": 1, "value": 50}},
        "exits": {
            "north": {"target": "emerald_ruins_collapsed_wing", "type": "direction"},
            "east": {"target": "emerald_ruins_guardian_corridor", "type": "direction"}
        }
    }

    rooms["emerald_ruins_guardian_corridor"] = {
        "id": "emerald_ruins_guardian_corridor",
        "name": "Guardian Statue Corridor",
        "description": "A long hallway lined with stone statues of armored warriors. Each statue "
                       "holds a different weapon and wears a different expression. Their eyes — inlaid "
                       "with crystal — seem to follow you. One statue at the far end has been "
                       "shattered from the inside, as if something broke out of it.",
        "coordinates": [cx + 1, cy - 5],
        "location_type": "wilderness",
        "items": {"guardian_crystal_eye": {"quantity": 1, "value": 35}},
        "exits": {
            "west": {"target": "emerald_ruins_forgotten_throne", "type": "direction"},
            "east": {"target": "emerald_ancient_sanctum", "type": "direction"}
        }
    }

    rooms["emerald_ruins_sealed_vault"] = {
        "id": "emerald_ruins_sealed_vault",
        "name": "Sealed Vault",
        "description": "Behind the library, a vault door of solid greenstone remains sealed with "
                       "ancient magic. Druidic wards and older, unknown symbols cover its surface. "
                       "The door is warm to the touch. Through a crack in the seal, golden light "
                       "spills out, and you can hear a faint, rhythmic pulse — like a heartbeat.",
        "coordinates": [cx, cy - 4],
        "location_type": "wilderness",
        "items": {},
        "exits": {
            "north": {"target": "emerald_ruins_library", "type": "direction"}
        }
    }

    rooms["emerald_ruins_overgrown_observatory"] = {
        "id": "emerald_ruins_overgrown_observatory",
        "name": "Ruined Observatory",
        "description": "A domed building whose roof has partially fallen away. Inside, a massive "
                       "bronze armillary sphere — corroded green but still functional — tracks "
                       "celestial movements. The ancient builders were astronomers. Vine-covered "
                       "lens mounts suggest they had telescopes that put modern ones to shame.",
        "coordinates": [cx + 3, cy - 3],
        "location_type": "wilderness",
        "items": {"ancient_lens": {"quantity": 1, "value": 40}},
        "exits": {
            "west": {"target": "emerald_ruins_temple_exterior", "type": "direction"}
        }
    }

    # --- Fey Hollow (New Sub-region, 16 rooms) ---

    rooms["emerald_fey_shimmer_path"] = {
        "id": "emerald_fey_shimmer_path",
        "name": "Shimmer Path",
        "description": "The air here sparkles with drifting motes of golden light. The path underfoot "
                       "is carpeted in clover, and every few steps the surroundings seem to shift "
                       "subtly — a tree that was on your left is now on your right. The border between "
                       "the beast wilds and the Fey Hollow is thin, and reality here is negotiable.",
        "coordinates": [cx + 5, cy + 1],
        "location_type": "wilderness",
        "items": {},
        "exits": {
            "west": {"target": "emerald_beast_ravine", "type": "direction"},
            "east": {"target": "emerald_fey_pixie_ring", "type": "direction"},
            "south": {"target": "emerald_fey_glamour_garden", "type": "direction"}
        }
    }

    rooms["emerald_fey_pixie_ring"] = {
        "id": "emerald_fey_pixie_ring",
        "name": "Pixie Ring",
        "description": "A perfect circle of toadstools, each one glowing a different color, marks "
                       "a fey crossing point. Tiny winged figures — pixies — dart between the caps, "
                       "trailing ribbons of light. Their laughter sounds like tiny bells. They seem "
                       "friendly but mischievous, tugging at your hair and hiding your belongings.",
        "coordinates": [cx + 6, cy + 1],
        "location_type": "wilderness",
        "items": {"pixie_dust": {"quantity": 1, "value": 30}},
        "exits": {
            "west": {"target": "emerald_fey_shimmer_path", "type": "direction"},
            "east": {"target": "emerald_fey_illusion_maze", "type": "direction"},
            "north": {"target": "emerald_fey_wisp_marsh", "type": "direction"}
        }
    }

    rooms["emerald_fey_illusion_maze"] = {
        "id": "emerald_fey_illusion_maze",
        "name": "Illusion Maze",
        "description": "Hedges of flowering bushes form a maze — but it's not the hedges that are "
                       "tricky, it's the illusions. Paths appear and vanish. Walls turn transparent "
                       "then solid. Your own reflection walks beside you going the wrong direction. "
                       "The pixies find your confusion hilarious.",
        "coordinates": [cx + 7, cy + 1],
        "location_type": "wilderness",
        "items": {},
        "exits": {
            "west": {"target": "emerald_fey_pixie_ring", "type": "direction"},
            "north": {"target": "emerald_fey_crystal_glade", "type": "direction"},
            "east": {"target": "emerald_fey_thorn_gate", "type": "direction"}
        }
    }

    rooms["emerald_fey_thorn_gate"] = {
        "id": "emerald_fey_thorn_gate",
        "name": "Thorn Gate",
        "description": "A massive archway of interwoven thorns, each one as long as a dagger and "
                       "glistening with some iridescent substance. This is the formal entrance to "
                       "the Fey Court proper. Two tiny guards in acorn-cap helmets stand at attention "
                       "on the thorns, their spears (actually rose thorns) pointed at you.",
        "coordinates": [cx + 8, cy + 1],
        "location_type": "wilderness",
        "items": {},
        "exits": {
            "west": {"target": "emerald_fey_illusion_maze", "type": "direction"},
            "east": {"target": "emerald_fey_court", "type": "direction"}
        }
    }

    rooms["emerald_fey_court"] = {
        "id": "emerald_fey_court",
        "name": "Fey Court",
        "description": "A clearing of impossible beauty. The grass is silver, the flowers sing softly, "
                       "and a miniature palace of crystallized dewdrops sits atop a mushroom the size "
                       "of a house. The Fey Queen — no larger than your hand but radiating authority — "
                       "holds court here. Sprites, pixies, and brownies attend her. Time moves "
                       "differently; minutes here may be hours outside.",
        "coordinates": [cx + 9, cy + 1],
        "location_type": "settlement",
        "items": {"fey_blessing_token": {"quantity": 1, "value": 60}},
        "exits": {
            "west": {"target": "emerald_fey_thorn_gate", "type": "direction"},
            "north": {"target": "emerald_fey_treasure_hollow", "type": "direction"},
            "south": {"target": "emerald_fey_enchanted_spring", "type": "direction"}
        }
    }

    rooms["emerald_fey_wisp_marsh"] = {
        "id": "emerald_fey_wisp_marsh",
        "name": "Will-o'-Wisp Marsh",
        "description": "A boggy area where will-o'-wisps bob and weave between dead trees. Their "
                       "blue-white light is beautiful but treacherous — each wisp tries to lure you "
                       "deeper into the mire. The ground squelches and sucks at your boots. Faint "
                       "music plays from no discernible source, a melancholy waltz.",
        "coordinates": [cx + 6, cy + 2],
        "location_type": "wilderness",
        "items": {"wisp_lantern": {"quantity": 1, "value": 22}},
        "exits": {
            "south": {"target": "emerald_fey_pixie_ring", "type": "direction"},
            "east": {"target": "emerald_fey_crystal_glade", "type": "direction"}
        }
    }

    rooms["emerald_fey_crystal_glade"] = {
        "id": "emerald_fey_crystal_glade",
        "name": "Crystal Glade",
        "description": "Every plant in this glade has crystallized — leaves of thin amethyst, stems "
                       "of emerald, flowers of ruby. They still grow, impossibly, shedding crystal "
                       "petals that chime on the ground. The effect of ancient fey magic, the druids "
                       "say. The glade is heartbreakingly beautiful and slightly dangerous — the "
                       "crystal thorns are razor-sharp.",
        "coordinates": [cx + 7, cy + 2],
        "location_type": "wilderness",
        "items": {"crystal_petal": {"quantity": 2, "value": 16}},
        "exits": {
            "west": {"target": "emerald_fey_wisp_marsh", "type": "direction"},
            "south": {"target": "emerald_fey_illusion_maze", "type": "direction"},
            "east": {"target": "emerald_fey_mirror_pool", "type": "direction"}
        }
    }

    rooms["emerald_fey_mirror_pool"] = {
        "id": "emerald_fey_mirror_pool",
        "name": "Mirror Pool",
        "description": "A perfectly still pool that reflects not what is, but what could be. Peering "
                       "in, you see yourself as you might become — older, wiser, scarred or crowned. "
                       "The visions shift with each glance. Coins at the bottom suggest others have "
                       "tried to buy favorable futures. The fey watch you watching yourself.",
        "coordinates": [cx + 8, cy + 2],
        "location_type": "wilderness",
        "items": {"mirror_shard": {"quantity": 1, "value": 25}},
        "exits": {
            "west": {"target": "emerald_fey_crystal_glade", "type": "direction"},
            "south": {"target": "emerald_fey_thorn_gate", "type": "direction"}
        }
    }

    rooms["emerald_fey_treasure_hollow"] = {
        "id": "emerald_fey_treasure_hollow",
        "name": "Treasure Hollow",
        "description": "A hollow beneath a great root where the fey hoard their treasures — which "
                       "are not gold and gems but 'interesting things.' A collection of buttons, "
                       "a lock of child's hair, a bottle of laughter, a pressed four-leaf clover, "
                       "and a music box that plays a song no one remembers. The fey value sentiment "
                       "over silver.",
        "coordinates": [cx + 9, cy + 2],
        "location_type": "building",
        "items": {"bottle_of_laughter": {"quantity": 1, "value": 35}, "enchanted_music_box": {"quantity": 1, "value": 45}},
        "exits": {
            "south": {"target": "emerald_fey_court", "type": "direction"}
        }
    }

    rooms["emerald_fey_glamour_garden"] = {
        "id": "emerald_fey_glamour_garden",
        "name": "Glamour Garden",
        "description": "A garden where appearance and reality are deliberately different. Flowers "
                       "that look like butterflies, butterflies that look like flowers. A fountain "
                       "that appears to flow upward. A sundial whose shadow points at your deepest "
                       "desire. The fey gardener — a brownie in a tiny apron — tends plants that "
                       "only exist if you believe in them.",
        "coordinates": [cx + 5, cy],
        "location_type": "wilderness",
        "items": {"glamour_seed": {"quantity": 1, "value": 20}},
        "exits": {
            "north": {"target": "emerald_fey_shimmer_path", "type": "direction"},
            "east": {"target": "emerald_fey_changeling_hollow", "type": "direction"}
        }
    }

    rooms["emerald_fey_changeling_hollow"] = {
        "id": "emerald_fey_changeling_hollow",
        "name": "Changeling Hollow",
        "description": "A cozy burrow where changelings — fey who can take any form — live in a "
                       "state of perpetual identity crisis. The walls are lined with mirrors and "
                       "masks. One changeling wears your face, another your companion's. They mean "
                       "no harm; they're just practicing. It's deeply unsettling regardless.",
        "coordinates": [cx + 6, cy],
        "location_type": "building",
        "items": {"changeling_mask": {"quantity": 1, "value": 28}},
        "exits": {
            "west": {"target": "emerald_fey_glamour_garden", "type": "direction"},
            "north": {"target": "emerald_fey_pixie_ring", "type": "direction"}
        }
    }

    rooms["emerald_fey_enchanted_spring"] = {
        "id": "emerald_fey_enchanted_spring",
        "name": "Enchanted Spring",
        "description": "A spring of water that tastes like whatever you most need — whether that's "
                       "water, wine, medicine, or courage. The spring is guarded by a ancient willow "
                       "tree whose roots form a protective cage around it. Drinking too much is "
                       "unwise; the fey always collect debts, eventually.",
        "coordinates": [cx + 9, cy],
        "location_type": "wilderness",
        "items": {"enchanted_water": {"quantity": 1, "value": 30}},
        "exits": {
            "north": {"target": "emerald_fey_court", "type": "direction"}
        }
    }

    rooms["emerald_fey_moth_cathedral"] = {
        "id": "emerald_fey_moth_cathedral",
        "name": "Moth Cathedral",
        "description": "An enormous hollow tree whose interior is carpeted with luna moths, their "
                       "wings creating a shimmering green tapestry on every surface. When disturbed, "
                       "they take flight in a storm of soft wings, revealing carved pillars beneath — "
                       "this was once a fey place of worship. The moths return to their positions "
                       "with mathematical precision.",
        "coordinates": [cx + 7, cy],
        "location_type": "wilderness",
        "items": {"luna_moth_wing": {"quantity": 1, "value": 18}},
        "exits": {
            "west": {"target": "emerald_fey_changeling_hollow", "type": "direction"},
            "north": {"target": "emerald_fey_illusion_maze", "type": "direction"}
        }
    }

    rooms["emerald_fey_dream_bower"] = {
        "id": "emerald_fey_dream_bower",
        "name": "Dream Bower",
        "description": "A canopy of woven flowers forms a natural bedroom where sleeping brings "
                       "vivid, prophetic dreams. Cushions of cloud-moss and blankets of spider silk "
                       "invite rest. A tiny sign in fey script warns: 'Dream true, dream deep, "
                       "but guard what secrets dream-selves keep.' Many who sleep here wake with "
                       "knowledge they shouldn't have.",
        "coordinates": [cx + 8, cy],
        "location_type": "building",
        "items": {"dream_pillow": {"quantity": 1, "value": 22}},
        "exits": {
            "west": {"target": "emerald_fey_moth_cathedral", "type": "direction"},
            "north": {"target": "emerald_fey_mirror_pool", "type": "direction"}
        }
    }

    # --- Petrified Grove (New Sub-region, 10 rooms) ---

    rooms["emerald_petrified_approach"] = {
        "id": "emerald_petrified_approach",
        "name": "Petrified Approach",
        "description": "The jungle thins and the ground turns gray and chalky. Ahead, the trees "
                       "have turned to stone — perfect replicas in granite and marble, every leaf "
                       "and branch preserved. The silence here is unnatural; nothing living grows. "
                       "Even the air feels old and heavy, as if time itself has slowed.",
        "coordinates": [cx, cy - 6],
        "location_type": "wilderness",
        "items": {},
        "exits": {
            "north": {"target": "emerald_ruins_forgotten_throne", "type": "direction"},
            "south": {"target": "emerald_petrified_sentinel_row", "type": "direction"}
        }
    }

    rooms["emerald_petrified_sentinel_row"] = {
        "id": "emerald_petrified_sentinel_row",
        "name": "Stone Sentinel Row",
        "description": "Two rows of petrified trees face each other across a stone path, creating "
                       "a grand avenue. But these trees — look closer — were once creatures. Enormous "
                       "serpents, coiled mid-strike. Giant birds, wings spread. Deer, leaping. All "
                       "turned to perfect stone. Whatever did this was powerful and angry.",
        "coordinates": [cx, cy - 7],
        "location_type": "wilderness",
        "items": {"stone_feather": {"quantity": 1, "value": 16}},
        "exits": {
            "north": {"target": "emerald_petrified_approach", "type": "direction"},
            "south": {"target": "emerald_petrified_altar", "type": "direction"},
            "east": {"target": "emerald_petrified_clearing", "type": "direction"}
        }
    }

    rooms["emerald_petrified_altar"] = {
        "id": "emerald_petrified_altar",
        "name": "Petrification Altar",
        "description": "A stone altar carved with eyes — hundreds of staring eyes. This is the "
                       "source of the petrification magic. The altar pulses with a grey light that "
                       "makes your skin tingle. Offerings of flowers placed here turn to stone within "
                       "seconds. The druids have placed warning wards, but the altar's magic seeps "
                       "through them slowly.",
        "coordinates": [cx, cy - 8],
        "location_type": "wilderness",
        "items": {"petrified_flower": {"quantity": 2, "value": 10}},
        "exits": {
            "north": {"target": "emerald_petrified_sentinel_row", "type": "direction"},
            "east": {"target": "emerald_petrified_basilisk_approach", "type": "direction"}
        }
    }

    rooms["emerald_petrified_clearing"] = {
        "id": "emerald_petrified_clearing",
        "name": "Petrified Clearing",
        "description": "A wide clearing where a battle was frozen mid-action. Stone warriors face "
                       "stone beasts in poses of combat — swords raised, jaws agape, arrows mid- "
                       "flight (suspended on stone threads). It's a snapshot of a war that happened "
                       "so long ago that no one remembers the sides or the cause.",
        "coordinates": [cx + 1, cy - 7],
        "location_type": "wilderness",
        "items": {"petrified_arrow": {"quantity": 1, "value": 12}, "stone_sword_hilt": {"quantity": 1, "value": 18}},
        "exits": {
            "west": {"target": "emerald_petrified_sentinel_row", "type": "direction"},
            "south": {"target": "emerald_petrified_basilisk_approach", "type": "direction"}
        }
    }

    rooms["emerald_petrified_basilisk_approach"] = {
        "id": "emerald_petrified_basilisk_approach",
        "name": "Basilisk Approach",
        "description": "The stone ground here is scarred with deep gouges from enormous claws. The "
                       "petrified trees are shattered — smashed through by something massive moving "
                       "between them. Fresh stone dust on the ground suggests the creature is still "
                       "active. A warning totem lies toppled, its message unreadable.",
        "coordinates": [cx + 1, cy - 8],
        "location_type": "wilderness",
        "items": {},
        "exits": {
            "north": {"target": "emerald_petrified_clearing", "type": "direction"},
            "west": {"target": "emerald_petrified_altar", "type": "direction"},
            "south": {"target": "emerald_petrified_basilisk_lair", "type": "direction"}
        }
    }

    rooms["emerald_petrified_basilisk_lair"] = {
        "id": "emerald_petrified_basilisk_lair",
        "name": "Basilisk's Lair",
        "description": "A vast cavern, its entrance framed by shattered stone trees. Inside, a "
                       "nest of crushed rock holds enormous eggs — each one stone, of course. The "
                       "basilisk is here: a creature the size of a horse, lizard-like, with eyes "
                       "that glow with grey light. It watches you with ancient, patient malice. "
                       "Don't. Look. Directly. At it.",
        "coordinates": [cx + 1, cy - 9],
        "location_type": "wilderness",
        "items": {"basilisk_scale": {"quantity": 1, "value": 55}},
        "exits": {
            "north": {"target": "emerald_petrified_basilisk_approach", "type": "direction"},
            "east": {"target": "emerald_petrified_treasure_cache", "type": "direction"}
        }
    }

    rooms["emerald_petrified_treasure_cache"] = {
        "id": "emerald_petrified_treasure_cache",
        "name": "Petrified Treasure Cache",
        "description": "Deep in the back of the basilisk's lair, the remains of its victims have "
                       "accumulated over centuries. Stone adventurers clutch stone treasure that was "
                       "once real gold. But some items — enchanted ones — resisted the petrification. "
                       "A sword still gleams. A ring still glows. A potion bottle is still liquid.",
        "coordinates": [cx + 2, cy - 9],
        "location_type": "wilderness",
        "items": {"enchanted_ring": {"quantity": 1, "value": 65}, "preserved_potion": {"quantity": 1, "value": 30}},
        "exits": {
            "west": {"target": "emerald_petrified_basilisk_lair", "type": "direction"}
        }
    }

    rooms["emerald_petrified_puzzle_stones"] = {
        "id": "emerald_petrified_puzzle_stones",
        "name": "Puzzle Stones",
        "description": "A circle of standing stones, each carved with a different animal, surrounds "
                       "a central pedestal. The stones can be rotated, and their alignment seems to "
                       "control the flow of petrification magic. Druids believe solving the puzzle "
                       "could reverse the curse — but getting it wrong intensifies it.",
        "coordinates": [cx - 1, cy - 7],
        "location_type": "wilderness",
        "items": {},
        "exits": {
            "east": {"target": "emerald_petrified_sentinel_row", "type": "direction"},
            "south": {"target": "emerald_petrified_weeping_stones", "type": "direction"}
        }
    }

    rooms["emerald_petrified_weeping_stones"] = {
        "id": "emerald_petrified_weeping_stones",
        "name": "Weeping Stones",
        "description": "Stone trees in this section 'weep' — water seeps through cracks in the "
                       "petrified wood, running down the trunks like tears. The water pools at the "
                       "base of each tree in small stone basins. Druids say the trees' spirits are "
                       "still alive inside the stone, mourning their imprisonment.",
        "coordinates": [cx - 1, cy - 8],
        "location_type": "wilderness",
        "items": {"stone_tear": {"quantity": 2, "value": 15}},
        "exits": {
            "north": {"target": "emerald_petrified_puzzle_stones", "type": "direction"},
            "east": {"target": "emerald_petrified_altar", "type": "direction"}
        }
    }

    rooms["emerald_petrified_memorial"] = {
        "id": "emerald_petrified_memorial",
        "name": "Druid Memorial",
        "description": "A recent addition to the grove — a circle of carved wooden posts placed "
                       "by modern druids to honor those who were petrified trying to break the curse. "
                       "Each post bears a name, a date, and a small portrait. Flowers — still living, "
                       "protected by powerful wards — grow in pots at the base of each memorial.",
        "coordinates": [cx - 1, cy - 6],
        "location_type": "wilderness",
        "items": {},
        "exits": {
            "south": {"target": "emerald_petrified_puzzle_stones", "type": "direction"},
            "east": {"target": "emerald_petrified_approach", "type": "direction"}
        }
    }


def generate_stormbreak_island(rooms):
    """Generate Island 3: Stormbreak Reef - Storm-battered volcanic reef island (~75 rooms)."""

    cx, cy = 10, 55  # Center coordinates

    # =========================================================================
    # STORMBREAK REEF - Storm-Battered Volcanic Reef Island (Level 15+)
    # Sub-regions: Docks, Reef Town, Shipwreck Graveyard, Storm Cliffs,
    #              Coral Labyrinth, Lightning Spire, Kraken's Reach, Storm Forge
    # =========================================================================

    # --- Stormbreak Docks (3 rooms) ---

    rooms["stormbreak_docks"] = {
        "id": "stormbreak_docks",
        "name": "Stormbreak Reef - Storm Dock",
        "description": "A battered stone dock slick with rain and sea spray. Iron chains anchor "
                       "the pier to jagged volcanic rock as waves crash relentlessly against the "
                       "moorings. Thunder rumbles overhead and lightning forks across a sky that "
                       "never clears.",
        "coordinates": [cx, cy - 2],
        "location_type": "dock",
        "items": {},
        "exits": {
            "board mainland": {
                "target": "harbor_east_dock",
                "type": "boat_travel",
                "island_id": "stormbreak_reef",
                "display": "Return to Grand Harbor",
                "unlock_cost": 0,
                "fare_cost": 0,
                "min_level": 1,
                "transition_text": "You board the ironclad return vessel. The crew raises storm shields\nas the ship battles through towering waves. After four harrowing\ndays, the calm waters of Grand Harbor finally appear on the horizon..."
            },
            "north": {"target": "stormbreak_town_gate", "type": "direction"},
            "east": {"target": "stormbreak_cargo_shelter", "type": "direction"},
            "south": {"target": "stormbreak_lighthouse", "type": "direction"}
        }
    }

    rooms["stormbreak_cargo_shelter"] = {
        "id": "stormbreak_cargo_shelter",
        "name": "Cargo Shelter",
        "description": "A reinforced stone shelter protects cargo from the relentless storms. "
                       "Waterproof tarps cover crates of imported goods, and iron hooks hold "
                       "everything in place against the howling wind. Salvaged ship timber "
                       "props up the walls.",
        "coordinates": [cx + 1, cy - 2],
        "location_type": "dock",
        "items": {"storm_tarp": {"quantity": 1, "value": 10}, "iron_hook": {"quantity": 2, "value": 8}},
        "exits": {
            "west": {"target": "stormbreak_docks", "type": "direction"},
            "east": {"target": "stormbreak_dock_breakwater", "type": "direction"}
        }
    }

    rooms["stormbreak_lighthouse"] = {
        "id": "stormbreak_lighthouse",
        "name": "Stormbreak Lighthouse",
        "description": "A squat, heavily fortified lighthouse built from black volcanic stone. "
                       "Its storm-crystal beacon cuts through the perpetual tempest, guiding "
                       "ships to safe harbor. The keeper's quarters below are filled with "
                       "nautical charts and weather instruments.",
        "coordinates": [cx, cy - 3],
        "location_type": "building",
        "items": {"nautical_chart": {"quantity": 1, "value": 20}, "storm_lantern": {"quantity": 1, "value": 15}},
        "exits": {
            "north": {"target": "stormbreak_docks", "type": "direction"},
            "south": {"target": "stormbreak_kraken_shallows", "type": "direction"}
        }
    }

    # --- Reef Town (15 rooms) ---

    rooms["stormbreak_town_gate"] = {
        "id": "stormbreak_town_gate",
        "name": "Reef Town Gate",
        "description": "A sturdy gate built from salvaged ship hulls marks the entrance to "
                       "Reef Town. Barnacle-encrusted timbers form an archway, and storm-shutters "
                       "can be sealed during the worst tempests. The sound of hammers and voices "
                       "drifts from within.",
        "coordinates": [cx, cy - 1],
        "location_type": "settlement",
        "items": {},
        "exits": {
            "south": {"target": "stormbreak_docks", "type": "direction"},
            "north": {"target": "stormbreak_town_center", "type": "direction"},
            "west": {"target": "stormbreak_town_tavern", "type": "direction"},
            "east": {"target": "stormbreak_town_workshop", "type": "direction"}
        }
    }

    rooms["stormbreak_town_tavern"] = {
        "id": "stormbreak_town_tavern",
        "name": "The Drowned Anchor Tavern",
        "description": "A rowdy tavern built from the overturned hull of a galleon. Ship lanterns "
                       "swing from the curved ceiling and the bar is fashioned from a captain's "
                       "wheel mounted on kegs. Sailors swap tales of storms and sea monsters "
                       "over mugs of grog.",
        "coordinates": [cx - 1, cy - 1],
        "location_type": "building",
        "items": {"storm_grog": {"quantity": 2, "value": 6}, "salted_fish": {"quantity": 3, "value": 4}},
        "exits": {
            "east": {"target": "stormbreak_town_gate", "type": "direction"},
            "north": {"target": "stormbreak_town_inn", "type": "direction"}
        }
    }

    rooms["stormbreak_town_workshop"] = {
        "id": "stormbreak_town_workshop",
        "name": "Salvage Workshop",
        "description": "A cluttered workshop where shipwreck salvage is repaired and repurposed. "
                       "Tools hang from every surface and half-rebuilt mechanisms litter the "
                       "workbenches. The smell of tar and rust hangs thick in the damp air.",
        "coordinates": [cx + 1, cy - 1],
        "location_type": "building",
        "items": {"salvage_tools": {"quantity": 1, "value": 15}, "ship_nails": {"quantity": 5, "value": 3}},
        "exits": {
            "west": {"target": "stormbreak_town_gate", "type": "direction"},
            "north": {"target": "stormbreak_town_market", "type": "direction"},
            "east": {"target": "stormbreak_town_lookout", "type": "direction"}
        }
    }

    rooms["stormbreak_town_lookout"] = {
        "id": "stormbreak_town_lookout",
        "name": "Town Lookout Post",
        "description": "A raised platform overlooking the reef and the churning sea beyond. "
                       "A spotter scans the horizon through rain-streaked glass for approaching "
                       "ships or dangerous storm surges. Signal flags snap violently in the gale.",
        "coordinates": [cx + 2, cy - 1],
        "location_type": "building",
        "items": {"signal_flag": {"quantity": 1, "value": 8}},
        "exits": {
            "west": {"target": "stormbreak_town_workshop", "type": "direction"},
            "north": {"target": "stormbreak_town_storage", "type": "direction"}
        }
    }

    rooms["stormbreak_town_inn"] = {
        "id": "stormbreak_town_inn",
        "name": "The Storm's Eye Inn",
        "description": "A cozy inn insulated with thick sailcloth and driftwood paneling. "
                       "Despite the constant rumble of thunder outside, the interior is warm "
                       "and dry. Hammocks sway gently in a room that feels like a ship's quarters.",
        "coordinates": [cx - 1, cy],
        "location_type": "building",
        "items": {"warm_blanket": {"quantity": 1, "value": 10}},
        "exits": {
            "south": {"target": "stormbreak_town_tavern", "type": "direction"},
            "east": {"target": "stormbreak_town_center", "type": "direction"},
            "north": {"target": "stormbreak_town_healer", "type": "direction"},
            "west": {"target": "stormbreak_graveyard_entrance", "type": "direction"}
        }
    }

    rooms["stormbreak_town_center"] = {
        "id": "stormbreak_town_center",
        "name": "Reef Town Center",
        "description": "The heart of Reef Town, a cobbled square sheltered by overlapping ship "
                       "sails stretched between masts driven into the ground. A storm-bell tower "
                       "rises from the center, and residents bustle between workshops and homes "
                       "built from salvaged wreckage.",
        "coordinates": [cx, cy],
        "location_type": "settlement",
        "npcs": ["reef_town_crier"],
        "items": {},
        "exits": {
            "south": {"target": "stormbreak_town_gate", "type": "direction"},
            "north": {"target": "stormbreak_town_elder", "type": "direction"},
            "east": {"target": "stormbreak_town_market", "type": "direction"},
            "west": {"target": "stormbreak_town_inn", "type": "direction"}
        }
    }

    rooms["stormbreak_town_market"] = {
        "id": "stormbreak_town_market",
        "name": "Stormbreak Market",
        "description": "An open-air market sheltered beneath oilskin canopies. Merchants sell "
                       "storm crystals, salvaged treasures, and reef-harvested goods. The stalls "
                       "are bolted to the ground to resist the ever-present wind.\n\n"
                       "A weathered trader beckons: 'Browse my wares with SHOP commands!'",
        "coordinates": [cx + 1, cy],
        "location_type": "settlement",
        "shop": True,
        "items": {"storm_crystal_shard": {"quantity": 2, "value": 18}, "reef_pearl": {"quantity": 1, "value": 25}},
        "exits": {
            "south": {"target": "stormbreak_town_workshop", "type": "direction"},
            "west": {"target": "stormbreak_town_center", "type": "direction"},
            "north": {"target": "stormbreak_town_smithy", "type": "direction"},
            "east": {"target": "stormbreak_town_storage", "type": "direction"}
        }
    }

    rooms["stormbreak_town_storage"] = {
        "id": "stormbreak_town_storage",
        "name": "Town Storage Cellar",
        "description": "A deep cellar carved into volcanic rock, sheltered from even the worst "
                       "storms. Barrels of preserved food, coils of rope, and emergency supplies "
                       "line the walls. This is where the town stores its reserves for when the "
                       "tempests are truly dire.",
        "coordinates": [cx + 2, cy],
        "location_type": "building",
        "items": {"preserved_rations": {"quantity": 3, "value": 5}, "sturdy_rope": {"quantity": 1, "value": 12}},
        "exits": {
            "south": {"target": "stormbreak_town_lookout", "type": "direction"},
            "west": {"target": "stormbreak_town_market", "type": "direction"},
            "north": {"target": "stormbreak_town_barracks", "type": "direction"},
            "east": {"target": "stormbreak_coral_entrance", "type": "direction"}
        }
    }

    rooms["stormbreak_town_healer"] = {
        "id": "stormbreak_town_healer",
        "name": "Storm Healer's Hut",
        "description": "A sturdy hut where the island healer treats lightning burns, coral cuts, "
                       "and storm-battered sailors. Jars of luminous salve and bundles of sea-kelp "
                       "poultices hang from the rafters. The healer hums an old sailor's prayer.",
        "coordinates": [cx - 1, cy + 1],
        "location_type": "building",
        "npcs": ["storm_healer"],
        "items": {"lightning_salve": {"quantity": 2, "value": 20}, "kelp_poultice": {"quantity": 3, "value": 10}},
        "exits": {
            "south": {"target": "stormbreak_town_inn", "type": "direction"},
            "east": {"target": "stormbreak_town_elder", "type": "direction"},
            "north": {"target": "stormbreak_town_well", "type": "direction"}
        }
    }

    rooms["stormbreak_town_elder"] = {
        "id": "stormbreak_town_elder",
        "name": "Elder's Hall",
        "description": "The largest building in Reef Town, constructed from the reinforced stern "
                       "of a massive warship. Inside, the Storm Elder governs the island from a "
                       "throne of coral and driftwood. Maps of the reef and storm charts cover "
                       "every wall.",
        "coordinates": [cx, cy + 1],
        "location_type": "building",
        "npcs": ["storm_elder"],
        "items": {"reef_map": {"quantity": 1, "value": 30}},
        "exits": {
            "south": {"target": "stormbreak_town_center", "type": "direction"},
            "west": {"target": "stormbreak_town_healer", "type": "direction"},
            "east": {"target": "stormbreak_town_smithy", "type": "direction"},
            "north": {"target": "stormbreak_town_north", "type": "direction"}
        }
    }

    rooms["stormbreak_town_smithy"] = {
        "id": "stormbreak_town_smithy",
        "name": "Thunderstrike Smithy",
        "description": "A forge that harnesses lightning strikes through copper rods on the roof. "
                       "The smith shapes storm-tempered metal into weapons and tools. Sparks fly "
                       "constantly, and the ring of hammer on anvil competes with the thunder above.",
        "coordinates": [cx + 1, cy + 1],
        "location_type": "building",
        "npcs": ["storm_smith"],
        "items": {"storm_iron_ingot": {"quantity": 1, "value": 35}, "copper_rod": {"quantity": 2, "value": 12}},
        "exits": {
            "south": {"target": "stormbreak_town_market", "type": "direction"},
            "west": {"target": "stormbreak_town_elder", "type": "direction"},
            "north": {"target": "stormbreak_town_shrine", "type": "direction"},
            "east": {"target": "stormbreak_town_barracks", "type": "direction"}
        }
    }

    rooms["stormbreak_town_barracks"] = {
        "id": "stormbreak_town_barracks",
        "name": "Storm Guard Barracks",
        "description": "The barracks of the island's Storm Guard, elite warriors trained to "
                       "fight in hurricane-force winds. Racks of weatherproof armor and "
                       "lightning-resistant shields line the walls. A training yard outside "
                       "echoes with the clash of weapons.",
        "coordinates": [cx + 2, cy + 1],
        "location_type": "building",
        "items": {"storm_shield_fragment": {"quantity": 1, "value": 22}},
        "exits": {
            "south": {"target": "stormbreak_town_storage", "type": "direction"},
            "west": {"target": "stormbreak_town_smithy", "type": "direction"},
            "east": {"target": "stormbreak_town_training_yard", "type": "direction"}
        }
    }

    rooms["stormbreak_town_well"] = {
        "id": "stormbreak_town_well",
        "name": "Stormwater Well",
        "description": "A deep well that collects rainwater filtered through volcanic rock. "
                       "The water here is tinged with minerals that give it a faintly electric "
                       "taste. Residents say drinking it steadies the nerves during the worst "
                       "storms.",
        "coordinates": [cx - 1, cy + 2],
        "location_type": "settlement",
        "items": {"stormwater_flask": {"quantity": 1, "value": 8}},
        "exits": {
            "south": {"target": "stormbreak_town_healer", "type": "direction"},
            "east": {"target": "stormbreak_town_north", "type": "direction"}
        }
    }

    rooms["stormbreak_town_north"] = {
        "id": "stormbreak_town_north",
        "name": "Reef Town - North End",
        "description": "The northern edge of Reef Town where the buildings thin out and rugged "
                       "terrain takes over. Storm-bent trees cling to rocky soil, and the wind "
                       "howls through gaps in the wreckage walls. Paths lead deeper into the "
                       "island's wild interior.",
        "coordinates": [cx, cy + 2],
        "location_type": "settlement",
        "items": {},
        "exits": {
            "south": {"target": "stormbreak_town_elder", "type": "direction"},
            "west": {"target": "stormbreak_town_well", "type": "direction"},
            "east": {"target": "stormbreak_town_shrine", "type": "direction"},
            "north": {"target": "stormbreak_cliffs_path", "type": "direction"}
        }
    }

    rooms["stormbreak_town_shrine"] = {
        "id": "stormbreak_town_shrine",
        "name": "Shrine of the Tempest",
        "description": "A small stone shrine dedicated to the storm spirits. Lightning-shaped "
                       "carvings adorn the walls, and offerings of storm glass and coral sit "
                       "on the altar. Flickering blue light plays across the ceiling during "
                       "strikes.",
        "coordinates": [cx + 1, cy + 2],
        "location_type": "building",
        "items": {"storm_glass_offering": {"quantity": 1, "value": 15}, "tempest_charm": {"quantity": 1, "value": 28}},
        "exits": {
            "south": {"target": "stormbreak_town_smithy", "type": "direction"},
            "west": {"target": "stormbreak_town_north", "type": "direction"},
            "east": {"target": "stormbreak_town_prayer_garden", "type": "direction"}
        }
    }

    # --- Shipwreck Graveyard (12 rooms) ---

    rooms["stormbreak_graveyard_entrance"] = {
        "id": "stormbreak_graveyard_entrance",
        "name": "Shipwreck Graveyard - Entrance",
        "description": "The path descends to a storm-lashed shore littered with wrecked vessels. "
                       "Broken masts jut from the sand like skeletal fingers, and the groaning "
                       "of twisted metal echoes above the crashing waves. The air stinks of "
                       "brine and rot.",
        "coordinates": [cx - 2, cy],
        "location_type": "wilderness",
        "items": {},
        "exits": {
            "east": {"target": "stormbreak_town_inn", "type": "direction"},
            "west": {"target": "stormbreak_graveyard_beach", "type": "direction"},
            "south": {"target": "stormbreak_graveyard_anchor_yard", "type": "direction"}
        }
    }

    rooms["stormbreak_graveyard_beach"] = {
        "id": "stormbreak_graveyard_beach",
        "name": "Wreck-Strewn Beach",
        "description": "A wide beach buried under shattered hulls and tangled rigging. Waves "
                       "roll in carrying fresh debris from the reef. Crabs scuttle between "
                       "rusting anchors, and the rain hammers down on exposed decking. The "
                       "remains of a dozen ships stretch in every direction.",
        "coordinates": [cx - 3, cy],
        "location_type": "wilderness",
        "items": {"rusty_anchor_chain": {"quantity": 1, "value": 8}, "waterlogged_timber": {"quantity": 3, "value": 3}},
        "exits": {
            "east": {"target": "stormbreak_graveyard_entrance", "type": "direction"},
            "west": {"target": "stormbreak_graveyard_ghost_ship", "type": "direction"},
            "north": {"target": "stormbreak_graveyard_hull", "type": "direction"},
            "south": {"target": "stormbreak_graveyard_salvage", "type": "direction"}
        }
    }

    rooms["stormbreak_graveyard_anchor_yard"] = {
        "id": "stormbreak_graveyard_anchor_yard",
        "name": "Anchor Yard",
        "description": "A muddy clearing where massive anchors have been dragged and stacked "
                       "by past salvage crews. Iron chains coil like sleeping serpents across "
                       "the ground. Some anchors bear the crests of ships lost centuries ago.",
        "coordinates": [cx - 2, cy - 1],
        "location_type": "wilderness",
        "items": {"ancient_ship_crest": {"quantity": 1, "value": 20}},
        "exits": {
            "north": {"target": "stormbreak_graveyard_entrance", "type": "direction"},
            "west": {"target": "stormbreak_graveyard_salvage", "type": "direction"}
        }
    }

    rooms["stormbreak_graveyard_salvage"] = {
        "id": "stormbreak_graveyard_salvage",
        "name": "Salvage Shore",
        "description": "The richest pickings on the graveyard shore. Salvagers have set up "
                       "makeshift workstations to strip usable materials from the wrecks. "
                       "Piles of bronze fittings, glass lenses, and water-stained maps "
                       "wait to be sorted.",
        "coordinates": [cx - 3, cy - 1],
        "location_type": "wilderness",
        "items": {"bronze_fitting": {"quantity": 2, "value": 12}, "salvaged_compass": {"quantity": 1, "value": 18}},
        "exits": {
            "east": {"target": "stormbreak_graveyard_anchor_yard", "type": "direction"},
            "north": {"target": "stormbreak_graveyard_beach", "type": "direction"},
            "west": {"target": "stormbreak_graveyard_below_deck", "type": "direction"}
        }
    }

    rooms["stormbreak_graveyard_hull"] = {
        "id": "stormbreak_graveyard_hull",
        "name": "Shattered Hull",
        "description": "The split-open hull of an enormous merchant vessel looms overhead. "
                       "You can walk through the exposed ribs of the ship like a cathedral "
                       "of rotting wood. Barnacles coat every surface and crabs nest in the "
                       "dark recesses.",
        "coordinates": [cx - 3, cy + 1],
        "location_type": "wilderness",
        "items": {"barnacle_cluster": {"quantity": 2, "value": 5}, "ship_rib_timber": {"quantity": 1, "value": 10}},
        "exits": {
            "south": {"target": "stormbreak_graveyard_beach", "type": "direction"},
            "west": {"target": "stormbreak_graveyard_rotting_bow", "type": "direction"},
            "north": {"target": "stormbreak_graveyard_tide_wreck", "type": "direction"}
        }
    }

    rooms["stormbreak_graveyard_rotting_bow"] = {
        "id": "stormbreak_graveyard_rotting_bow",
        "name": "Rotting Bow Section",
        "description": "The prow of a once-proud warship tilts at a steep angle, half-buried "
                       "in volcanic sand. Tattered sail fragments whip in the wind. A faded "
                       "nameplate reads something illegible beneath layers of corrosion.",
        "coordinates": [cx - 4, cy + 1],
        "location_type": "wilderness",
        "items": {"corroded_nameplate": {"quantity": 1, "value": 14}},
        "exits": {
            "east": {"target": "stormbreak_graveyard_hull", "type": "direction"},
            "south": {"target": "stormbreak_graveyard_ghost_ship", "type": "direction"},
            "west": {"target": "stormbreak_graveyard_figurehead", "type": "direction"},
            "north": {"target": "stormbreak_graveyard_crows_nest", "type": "direction"}
        }
    }

    rooms["stormbreak_graveyard_ghost_ship"] = {
        "id": "stormbreak_graveyard_ghost_ship",
        "name": "The Ghost Ship",
        "description": "A hauntingly intact galleon sits upright in the shallows, its deck "
                       "still mostly level. Faint phosphorescent light glows from the portholes "
                       "and the ship's bell rings on its own in the wind. Sailors say the crew "
                       "never left.",
        "coordinates": [cx - 4, cy],
        "location_type": "wilderness",
        "items": {"ghost_lantern": {"quantity": 1, "value": 30}, "spectral_coin": {"quantity": 3, "value": 15}},
        "exits": {
            "east": {"target": "stormbreak_graveyard_beach", "type": "direction"},
            "north": {"target": "stormbreak_graveyard_rotting_bow", "type": "direction"},
            "south": {"target": "stormbreak_graveyard_below_deck", "type": "direction"},
            "west": {"target": "stormbreak_graveyard_wreck_deep", "type": "direction"}
        }
    }

    rooms["stormbreak_graveyard_below_deck"] = {
        "id": "stormbreak_graveyard_below_deck",
        "name": "Below Deck - Flooded Hold",
        "description": "The lower deck of the ghost ship is half-flooded with dark seawater. "
                       "Cargo crates bob in the murky water and strange bioluminescent fish "
                       "dart between submerged timbers. Something large shifts in the deeper "
                       "water at the stern.",
        "coordinates": [cx - 4, cy - 1],
        "location_type": "wilderness",
        "items": {"waterlogged_chest": {"quantity": 1, "value": 25}, "bioluminescent_scale": {"quantity": 2, "value": 12}},
        "exits": {
            "east": {"target": "stormbreak_graveyard_salvage", "type": "direction"},
            "north": {"target": "stormbreak_graveyard_ghost_ship", "type": "direction"},
            "west": {"target": "stormbreak_tidal_caves_entrance", "type": "direction"}
        }
    }

    rooms["stormbreak_graveyard_crows_nest"] = {
        "id": "stormbreak_graveyard_crows_nest",
        "name": "Toppled Crow's Nest",
        "description": "A crow's nest from a fallen mast lies on its side among the wreckage. "
                       "The spotter's platform still holds a cracked telescope and a logbook "
                       "sealed in waxed leather. From here you can see the full extent of the "
                       "graveyard stretching along the coast.",
        "coordinates": [cx - 4, cy + 2],
        "location_type": "wilderness",
        "items": {"cracked_telescope": {"quantity": 1, "value": 16}, "waxed_logbook": {"quantity": 1, "value": 22}},
        "exits": {
            "south": {"target": "stormbreak_graveyard_rotting_bow", "type": "direction"},
            "east": {"target": "stormbreak_graveyard_tide_wreck", "type": "direction"}
        }
    }

    rooms["stormbreak_graveyard_figurehead"] = {
        "id": "stormbreak_graveyard_figurehead",
        "name": "Figurehead Grotto",
        "description": "A sheltered alcove where dozens of carved wooden figureheads have been "
                       "gathered — mermaids, sea serpents, storm gods — all weathered and "
                       "salt-bleached. Locals consider this place sacred, a memorial to the "
                       "lost ships.",
        "coordinates": [cx - 5, cy + 2],
        "location_type": "wilderness",
        "items": {"carved_figurehead": {"quantity": 1, "value": 35}},
        "exits": {
            "east": {"target": "stormbreak_graveyard_rotting_bow", "type": "direction"},
            "south": {"target": "stormbreak_graveyard_debris_field", "type": "direction"}
        }
    }

    rooms["stormbreak_graveyard_wreck_deep"] = {
        "id": "stormbreak_graveyard_wreck_deep",
        "name": "Deep Wreck - Submerged Hulks",
        "description": "The water deepens here, and the wrecks are almost entirely submerged. "
                       "Only mast-tips and rusted crow cages break the surface. The current is "
                       "treacherous and the water dark with stirred sediment. Treasure hunters "
                       "dive here at great risk.",
        "coordinates": [cx - 5, cy],
        "location_type": "wilderness",
        "items": {"sunken_doubloon": {"quantity": 2, "value": 20}},
        "exits": {
            "east": {"target": "stormbreak_graveyard_ghost_ship", "type": "direction"},
            "north": {"target": "stormbreak_graveyard_debris_field", "type": "direction"}
        }
    }

    rooms["stormbreak_graveyard_debris_field"] = {
        "id": "stormbreak_graveyard_debris_field",
        "name": "Debris Field",
        "description": "An impassable tangle of broken masts, shredded sails, and splintered "
                       "planking stretching across the shallows. The debris shifts and groans "
                       "with every wave. Seabirds nest atop the wreckage, screeching when "
                       "disturbed.",
        "coordinates": [cx - 5, cy + 1],
        "location_type": "wilderness",
        "items": {"driftwood_plank": {"quantity": 2, "value": 4}, "sea_glass": {"quantity": 3, "value": 6}},
        "exits": {
            "north": {"target": "stormbreak_graveyard_figurehead", "type": "direction"},
            "south": {"target": "stormbreak_graveyard_wreck_deep", "type": "direction"}
        }
    }

    rooms["stormbreak_graveyard_tide_wreck"] = {
        "id": "stormbreak_graveyard_tide_wreck",
        "name": "Tide-Revealed Wreck",
        "description": "At low tide, the skeleton of an ancient vessel emerges from the sand. "
                       "Its construction is unlike any modern ship — curved bone-like ribs and "
                       "a hull of interlocking stone plates. Whatever this vessel was, it was "
                       "not built by human hands.",
        "coordinates": [cx - 3, cy + 2],
        "location_type": "wilderness",
        "items": {"strange_hull_plate": {"quantity": 1, "value": 40}, "bone_rib_fragment": {"quantity": 1, "value": 18}},
        "exits": {
            "south": {"target": "stormbreak_graveyard_hull", "type": "direction"},
            "west": {"target": "stormbreak_graveyard_crows_nest", "type": "direction"},
            "north": {"target": "stormbreak_graveyard_flotsam_shore", "type": "direction"}
        }
    }

    # --- Storm Cliffs (12 rooms) ---

    rooms["stormbreak_cliffs_path"] = {
        "id": "stormbreak_cliffs_path",
        "name": "Storm Cliffs - Path",
        "description": "A steep, rain-slicked path climbs from the town toward the exposed "
                       "cliffs above. The wind intensifies with every step, carrying stinging "
                       "salt spray. Jagged volcanic rock juts from the hillside like broken "
                       "teeth.",
        "coordinates": [cx, cy + 3],
        "location_type": "wilderness",
        "items": {},
        "exits": {
            "south": {"target": "stormbreak_town_north", "type": "direction"},
            "north": {"target": "stormbreak_cliffs_overlook", "type": "direction"},
            "east": {"target": "stormbreak_cliffs_east", "type": "direction"},
            "west": {"target": "stormbreak_cliffs_west", "type": "direction"}
        }
    }

    rooms["stormbreak_cliffs_east"] = {
        "id": "stormbreak_cliffs_east",
        "name": "Eastern Cliffside",
        "description": "The eastern cliff face drops sheer into boiling surf far below. Wind-carved "
                       "pillars of basalt stand like sentinels along the edge. Lightning strikes "
                       "the tallest pillar with alarming regularity, leaving it black and smoking.",
        "coordinates": [cx + 1, cy + 3],
        "location_type": "wilderness",
        "items": {"lightning_scorched_rock": {"quantity": 1, "value": 12}},
        "exits": {
            "west": {"target": "stormbreak_cliffs_path", "type": "direction"},
            "north": {"target": "stormbreak_cliffs_whirlpool", "type": "direction"},
            "east": {"target": "stormbreak_cliffs_nest", "type": "direction"}
        }
    }

    rooms["stormbreak_cliffs_west"] = {
        "id": "stormbreak_cliffs_west",
        "name": "Western Cliffside",
        "description": "The western cliffs are riddled with caves carved by millennia of storms. "
                       "Howling wind creates an eerie whistle as it passes through the hollowed "
                       "rock. Tide pools glimmer in the crevices, filled with strange marine life.",
        "coordinates": [cx - 1, cy + 3],
        "location_type": "wilderness",
        "items": {"tide_pool_specimen": {"quantity": 1, "value": 10}},
        "exits": {
            "east": {"target": "stormbreak_cliffs_path", "type": "direction"},
            "north": {"target": "stormbreak_cliffs_thunder_cave", "type": "direction"},
            "west": {"target": "stormbreak_cliffs_ravine", "type": "direction"}
        }
    }

    rooms["stormbreak_cliffs_ravine"] = {
        "id": "stormbreak_cliffs_ravine",
        "name": "Wind-Carved Ravine",
        "description": "A deep ravine cut by centuries of hurricane-force winds channeling "
                       "through the rock. The walls are smooth as glass and hum with a low "
                       "vibration in the gale. Mineral deposits in the stone glitter with "
                       "faint electrical charge.",
        "coordinates": [cx - 2, cy + 3],
        "location_type": "wilderness",
        "items": {"charged_mineral": {"quantity": 1, "value": 15}},
        "exits": {
            "east": {"target": "stormbreak_cliffs_west", "type": "direction"},
            "north": {"target": "stormbreak_forge_entrance", "type": "direction"}
        }
    }

    rooms["stormbreak_cliffs_overlook"] = {
        "id": "stormbreak_cliffs_overlook",
        "name": "Storm Overlook",
        "description": "A windswept plateau offering a terrifying view of the perpetual tempest. "
                       "Lightning illuminates the churning sea in brilliant flashes, and thunder "
                       "shakes the very rock beneath your feet. You can see the entire island "
                       "from this exposed vantage point.",
        "coordinates": [cx, cy + 4],
        "location_type": "wilderness",
        "items": {"storm_crystal": {"quantity": 1, "value": 30}},
        "exits": {
            "south": {"target": "stormbreak_cliffs_path", "type": "direction"},
            "north": {"target": "stormbreak_cliffs_peak", "type": "direction"},
            "east": {"target": "stormbreak_cliffs_whirlpool", "type": "direction"},
            "west": {"target": "stormbreak_cliffs_thunder_cave", "type": "direction"}
        }
    }

    rooms["stormbreak_cliffs_thunder_cave"] = {
        "id": "stormbreak_cliffs_thunder_cave",
        "name": "Thunder Cave",
        "description": "A deep cave where the acoustics amplify every thunderclap into a "
                       "deafening roar. The walls vibrate with each boom, and stalactites "
                       "of crystallized salt hang from the ceiling. Bats cluster in terrified "
                       "knots in the deepest alcoves.",
        "coordinates": [cx - 1, cy + 4],
        "location_type": "wilderness",
        "items": {"salt_stalactite": {"quantity": 1, "value": 14}, "thunder_stone": {"quantity": 1, "value": 22}},
        "exits": {
            "east": {"target": "stormbreak_cliffs_overlook", "type": "direction"},
            "south": {"target": "stormbreak_cliffs_west", "type": "direction"},
            "north": {"target": "stormbreak_cliffs_wind_tunnel", "type": "direction"}
        }
    }

    rooms["stormbreak_cliffs_whirlpool"] = {
        "id": "stormbreak_cliffs_whirlpool",
        "name": "Whirlpool Overlook",
        "description": "The cliff edge here overlooks a massive permanent whirlpool in the reef "
                       "below. Ships caught in its pull are never seen again. The roar of the "
                       "spinning water is hypnotic, and spray reaches all the way up to the "
                       "clifftop.",
        "coordinates": [cx + 1, cy + 4],
        "location_type": "wilderness",
        "items": {"whirlpool_pearl": {"quantity": 1, "value": 35}},
        "exits": {
            "west": {"target": "stormbreak_cliffs_overlook", "type": "direction"},
            "south": {"target": "stormbreak_cliffs_east", "type": "direction"},
            "north": {"target": "stormbreak_cliffs_ledge", "type": "direction"},
            "east": {"target": "stormbreak_cliffs_arch", "type": "direction"}
        }
    }

    rooms["stormbreak_cliffs_nest"] = {
        "id": "stormbreak_cliffs_nest",
        "name": "Storm Petrel Nesting Grounds",
        "description": "Thousands of storm petrels nest in the craggy eastern cliffs, seemingly "
                       "unbothered by the eternal tempest. Their dark feathers shimmer with "
                       "static electricity. Broken eggshells crunch underfoot, and the birds "
                       "screech warnings at intruders.",
        "coordinates": [cx + 2, cy + 3],
        "location_type": "wilderness",
        "items": {"storm_petrel_feather": {"quantity": 3, "value": 8}},
        "exits": {
            "west": {"target": "stormbreak_cliffs_east", "type": "direction"},
            "north": {"target": "stormbreak_cliffs_arch", "type": "direction"}
        }
    }

    rooms["stormbreak_cliffs_arch"] = {
        "id": "stormbreak_cliffs_arch",
        "name": "Lightning Arch",
        "description": "A natural stone arch spans a gap between two cliff sections, its peak "
                       "blackened by countless lightning strikes. Electricity visibly arcs across "
                       "the stone during the worst storms. Crossing it requires nerve and perfect "
                       "timing.",
        "coordinates": [cx + 2, cy + 4],
        "location_type": "wilderness",
        "items": {"lightning_glass": {"quantity": 1, "value": 25}},
        "exits": {
            "south": {"target": "stormbreak_cliffs_nest", "type": "direction"},
            "west": {"target": "stormbreak_cliffs_whirlpool", "type": "direction"},
            "east": {"target": "stormbreak_cliffs_arch_bridge", "type": "direction"}
        }
    }

    rooms["stormbreak_cliffs_peak"] = {
        "id": "stormbreak_cliffs_peak",
        "name": "Storm Peak",
        "description": "The highest point of the Storm Cliffs, where the wind is so fierce "
                       "you must crouch to avoid being swept away. Lightning strikes the peak "
                       "constantly, and the rock glows with residual charge. A narrow path "
                       "continues along the ridgeline in both directions.",
        "coordinates": [cx, cy + 5],
        "location_type": "wilderness",
        "items": {"charged_storm_crystal": {"quantity": 1, "value": 45}},
        "exits": {
            "south": {"target": "stormbreak_cliffs_overlook", "type": "direction"},
            "east": {"target": "stormbreak_cliffs_ledge", "type": "direction"},
            "west": {"target": "stormbreak_cliffs_wind_tunnel", "type": "direction"}
        }
    }

    rooms["stormbreak_cliffs_ledge"] = {
        "id": "stormbreak_cliffs_ledge",
        "name": "Precarious Ledge",
        "description": "A narrow ledge of volcanic rock juts out over a dizzying drop. The "
                       "stone is warm to the touch and vibrates with deep geothermal energy. "
                       "To the east, a towering volcanic spire pierces the storm clouds, its "
                       "tip constantly wreathed in lightning.",
        "coordinates": [cx + 1, cy + 5],
        "location_type": "wilderness",
        "items": {},
        "exits": {
            "west": {"target": "stormbreak_cliffs_peak", "type": "direction"},
            "south": {"target": "stormbreak_cliffs_whirlpool", "type": "direction"},
            "east": {"target": "stormbreak_spire_base", "type": "direction"}
        }
    }

    rooms["stormbreak_cliffs_wind_tunnel"] = {
        "id": "stormbreak_cliffs_wind_tunnel",
        "name": "Wind Tunnel",
        "description": "A perfectly cylindrical tunnel bored through the cliff by millennia of "
                       "focused wind. The air screams through at incredible speed, and anything "
                       "not secured is immediately ripped away. Strange wind-carved formations "
                       "line the walls like frozen waves.",
        "coordinates": [cx - 1, cy + 5],
        "location_type": "wilderness",
        "items": {"wind_carved_stone": {"quantity": 1, "value": 16}},
        "exits": {
            "east": {"target": "stormbreak_cliffs_peak", "type": "direction"},
            "south": {"target": "stormbreak_cliffs_thunder_cave", "type": "direction"}
        }
    }

    # --- Coral Labyrinth (10 rooms) ---

    rooms["stormbreak_coral_entrance"] = {
        "id": "stormbreak_coral_entrance",
        "name": "Coral Labyrinth - Entrance",
        "description": "The reef gives way to a bewildering maze of razor-sharp coral formations "
                       "rising from tide pools. The coral grows in impossible spirals and arches, "
                       "taller than a person. One wrong step could slice through boot leather.",
        "coordinates": [cx + 3, cy],
        "location_type": "wilderness",
        "items": {},
        "exits": {
            "west": {"target": "stormbreak_town_storage", "type": "direction"},
            "north": {"target": "stormbreak_coral_north_fork", "type": "direction"},
            "south": {"target": "stormbreak_coral_south_fork", "type": "direction"}
        }
    }

    rooms["stormbreak_coral_north_fork"] = {
        "id": "stormbreak_coral_north_fork",
        "name": "Northern Coral Fork",
        "description": "The labyrinth branches northward into a passage of towering brain coral "
                       "and fan formations that wave hypnotically in the current. Tiny luminous "
                       "fish dart through gaps in the coral wall, leaving trails of soft blue light.",
        "coordinates": [cx + 3, cy + 1],
        "location_type": "wilderness",
        "items": {"luminous_coral_fragment": {"quantity": 1, "value": 15}},
        "exits": {
            "south": {"target": "stormbreak_coral_entrance", "type": "direction"},
            "east": {"target": "stormbreak_coral_tidepool", "type": "direction"}
        }
    }

    rooms["stormbreak_coral_south_fork"] = {
        "id": "stormbreak_coral_south_fork",
        "name": "Southern Coral Fork",
        "description": "The southern passage dips downward, and seawater floods in at high "
                       "tide. Anemones in vivid purples and oranges carpet the coral walls. "
                       "Hermit crabs the size of fists scuttle through the shallow pools.",
        "coordinates": [cx + 3, cy - 1],
        "location_type": "wilderness",
        "items": {"vivid_anemone": {"quantity": 2, "value": 10}},
        "exits": {
            "north": {"target": "stormbreak_coral_entrance", "type": "direction"},
            "east": {"target": "stormbreak_coral_underwater", "type": "direction"}
        }
    }

    rooms["stormbreak_coral_tidepool"] = {
        "id": "stormbreak_coral_tidepool",
        "name": "Glowing Tidepool",
        "description": "A large tidal pool sheltered by overhanging coral. The water glows with "
                       "bioluminescent plankton, casting shimmering blue-green light on the "
                       "surrounding walls. Starfish and sea urchins cluster on the pool's edges.",
        "coordinates": [cx + 4, cy + 1],
        "location_type": "wilderness",
        "items": {"bioluminescent_vial": {"quantity": 1, "value": 20}, "reef_starfish": {"quantity": 1, "value": 8}},
        "exits": {
            "west": {"target": "stormbreak_coral_north_fork", "type": "direction"},
            "south": {"target": "stormbreak_coral_east_passage", "type": "direction"},
            "east": {"target": "stormbreak_coral_chamber", "type": "direction"}
        }
    }

    rooms["stormbreak_coral_east_passage"] = {
        "id": "stormbreak_coral_east_passage",
        "name": "Coral East Passage",
        "description": "A narrow winding passage through walls of stag-horn coral. The razor "
                       "edges catch clothing and skin alike. Puddles of trapped seawater reflect "
                       "lightning from above, creating a strobe effect in the tight corridor.",
        "coordinates": [cx + 4, cy],
        "location_type": "wilderness",
        "items": {"staghorn_coral": {"quantity": 1, "value": 12}},
        "exits": {
            "north": {"target": "stormbreak_coral_tidepool", "type": "direction"},
            "south": {"target": "stormbreak_coral_underwater", "type": "direction"},
            "east": {"target": "stormbreak_coral_deep", "type": "direction"}
        }
    }

    rooms["stormbreak_coral_underwater"] = {
        "id": "stormbreak_coral_underwater",
        "name": "Underwater Passage",
        "description": "The coral passage dips below the waterline, requiring a breath-held "
                       "dive to navigate. The submerged tunnel is lit by glowing coral polyps "
                       "and schools of electric eels that pulse with blue light.",
        "coordinates": [cx + 4, cy - 1],
        "location_type": "wilderness",
        "items": {"electric_eel_scale": {"quantity": 1, "value": 18}},
        "exits": {
            "north": {"target": "stormbreak_coral_east_passage", "type": "direction"},
            "west": {"target": "stormbreak_coral_south_fork", "type": "direction"},
            "east": {"target": "stormbreak_coral_grotto", "type": "direction"}
        }
    }

    rooms["stormbreak_coral_deep"] = {
        "id": "stormbreak_coral_deep",
        "name": "Deep Coral Cavern",
        "description": "The coral formations here are ancient and enormous, forming a natural "
                       "cathedral. Pillars of fused coral rise from floor to ceiling, encrusted "
                       "with crystallized salt. The acoustics amplify the ocean's heartbeat "
                       "into a rhythmic boom.",
        "coordinates": [cx + 5, cy],
        "location_type": "wilderness",
        "items": {"ancient_coral": {"quantity": 1, "value": 28}},
        "exits": {
            "west": {"target": "stormbreak_coral_east_passage", "type": "direction"},
            "north": {"target": "stormbreak_coral_chamber", "type": "direction"},
            "east": {"target": "stormbreak_coral_pearl_bed", "type": "direction"}
        }
    }

    rooms["stormbreak_coral_chamber"] = {
        "id": "stormbreak_coral_chamber",
        "name": "Crystal Coral Chamber",
        "description": "A breathtaking natural chamber where coral has fused with volcanic "
                       "crystal. The walls shimmer with embedded gems, and the air hums with "
                       "a faint electrical resonance. This place feels sacred — untouched by "
                       "the storms above.",
        "coordinates": [cx + 5, cy + 1],
        "location_type": "wilderness",
        "items": {"coral_crystal_gem": {"quantity": 1, "value": 40}},
        "exits": {
            "south": {"target": "stormbreak_coral_deep", "type": "direction"},
            "west": {"target": "stormbreak_coral_tidepool", "type": "direction"}
        }
    }

    rooms["stormbreak_coral_grotto"] = {
        "id": "stormbreak_coral_grotto",
        "name": "Hidden Coral Grotto",
        "description": "A secret grotto accessible only through the underwater passage. Air "
                       "pockets in the ceiling keep it breathable. The walls are lined with "
                       "rare black coral, and a freshwater spring bubbles up through the "
                       "reef floor.",
        "coordinates": [cx + 5, cy - 1],
        "location_type": "wilderness",
        "items": {"black_coral": {"quantity": 1, "value": 45}, "freshwater_pearl": {"quantity": 2, "value": 20}},
        "exits": {
            "west": {"target": "stormbreak_coral_underwater", "type": "direction"},
            "east": {"target": "stormbreak_coral_grotto_deep", "type": "direction"}
        }
    }

    rooms["stormbreak_coral_pearl_bed"] = {
        "id": "stormbreak_coral_pearl_bed",
        "name": "Pearl Bed",
        "description": "The deepest reach of the coral labyrinth opens into a sandy-bottomed "
                       "chamber filled with giant oysters. Some shells are agape, revealing "
                       "lustrous pearls of unusual size. Lightning-pattern veins run through "
                       "the pearls, making them uniquely valuable.",
        "coordinates": [cx + 6, cy],
        "location_type": "wilderness",
        "items": {"lightning_pearl": {"quantity": 1, "value": 55}, "giant_oyster_shell": {"quantity": 1, "value": 12}},
        "exits": {
            "west": {"target": "stormbreak_coral_deep", "type": "direction"},
            "south": {"target": "stormbreak_coral_oyster_beds", "type": "direction"}
        }
    }

    # --- Lightning Spire (10 rooms) ---

    rooms["stormbreak_spire_base"] = {
        "id": "stormbreak_spire_base",
        "name": "Lightning Spire - Base",
        "description": "The base of an enormous volcanic spire that towers above the island. "
                       "The black rock is warm to the touch and crackles with static discharge. "
                       "Veins of copper ore run through the stone, acting as natural lightning "
                       "conductors.",
        "coordinates": [cx + 2, cy + 5],
        "location_type": "wilderness",
        "items": {"copper_ore_vein": {"quantity": 1, "value": 18}},
        "exits": {
            "west": {"target": "stormbreak_cliffs_ledge", "type": "direction"},
            "north": {"target": "stormbreak_spire_path", "type": "direction"}
        }
    }

    rooms["stormbreak_spire_path"] = {
        "id": "stormbreak_spire_path",
        "name": "Spire Ascent Path",
        "description": "A treacherous path spirals upward around the volcanic spire. Sections "
                       "of the trail are scorched black by lightning strikes, and the air "
                       "tingles with ozone. Small crystals embedded in the rock glow between "
                       "strikes.",
        "coordinates": [cx + 2, cy + 6],
        "location_type": "wilderness",
        "items": {"ozone_crystal": {"quantity": 1, "value": 16}},
        "exits": {
            "south": {"target": "stormbreak_spire_base", "type": "direction"},
            "north": {"target": "stormbreak_spire_ascent", "type": "direction"},
            "east": {"target": "stormbreak_spire_crystal_cave", "type": "direction"}
        }
    }

    rooms["stormbreak_spire_crystal_cave"] = {
        "id": "stormbreak_spire_crystal_cave",
        "name": "Storm Crystal Cave",
        "description": "A cave in the side of the spire filled with clusters of storm crystals "
                       "that pulse with trapped lightning. The crystals hum and spark, casting "
                       "erratic shadows. Miners once harvested here, but the danger proved "
                       "too great.",
        "coordinates": [cx + 3, cy + 6],
        "location_type": "wilderness",
        "items": {"raw_storm_crystal": {"quantity": 2, "value": 30}, "crystal_shard": {"quantity": 3, "value": 10}},
        "exits": {
            "west": {"target": "stormbreak_spire_path", "type": "direction"},
            "north": {"target": "stormbreak_spire_charged_field", "type": "direction"}
        }
    }

    rooms["stormbreak_spire_charged_field"] = {
        "id": "stormbreak_spire_charged_field",
        "name": "Charged Field",
        "description": "An open terrace on the spire where the air itself is visibly charged. "
                       "Hair stands on end, metal objects spark, and ball lightning drifts "
                       "lazily across the rocky ground. The view is spectacular and terrifying "
                       "in equal measure.",
        "coordinates": [cx + 3, cy + 7],
        "location_type": "wilderness",
        "items": {"ball_lightning_essence": {"quantity": 1, "value": 40}},
        "exits": {
            "south": {"target": "stormbreak_spire_crystal_cave", "type": "direction"},
            "west": {"target": "stormbreak_spire_ascent", "type": "direction"}
        }
    }

    rooms["stormbreak_spire_ascent"] = {
        "id": "stormbreak_spire_ascent",
        "name": "Upper Ascent",
        "description": "The path narrows as it climbs higher, cutting through solid volcanic "
                       "rock. Copper veins in the walls glow red-hot after each lightning "
                       "strike. The thunder is so loud here it rattles teeth, and the wind "
                       "threatens to peel you off the mountainside.",
        "coordinates": [cx + 2, cy + 7],
        "location_type": "wilderness",
        "items": {"heated_copper_nugget": {"quantity": 1, "value": 22}},
        "exits": {
            "south": {"target": "stormbreak_spire_path", "type": "direction"},
            "east": {"target": "stormbreak_spire_charged_field", "type": "direction"},
            "north": {"target": "stormbreak_spire_observation", "type": "direction"}
        }
    }

    rooms["stormbreak_spire_observation"] = {
        "id": "stormbreak_spire_observation",
        "name": "Storm Observation Platform",
        "description": "A flat platform carved into the spire, once used by storm-watchers to "
                       "study the eternal tempest. Ruined instruments and broken lenses litter "
                       "the ancient stone. From here, you can see lightning strikes across the "
                       "entire island simultaneously.",
        "coordinates": [cx + 2, cy + 8],
        "location_type": "wilderness",
        "items": {"storm_watcher_lens": {"quantity": 1, "value": 28}},
        "exits": {
            "south": {"target": "stormbreak_spire_ascent", "type": "direction"},
            "east": {"target": "stormbreak_spire_conduit", "type": "direction"}
        }
    }

    rooms["stormbreak_spire_conduit"] = {
        "id": "stormbreak_spire_conduit",
        "name": "Lightning Conduit",
        "description": "A vertical shaft through the spire that acts as a natural lightning "
                       "rod. Bolts of electricity cascade down the walls in blinding displays. "
                       "Ancient runes carved into the stone seem designed to channel and store "
                       "the energy.",
        "coordinates": [cx + 3, cy + 8],
        "location_type": "wilderness",
        "items": {"conduit_rune_stone": {"quantity": 1, "value": 35}},
        "exits": {
            "west": {"target": "stormbreak_spire_observation", "type": "direction"},
            "north": {"target": "stormbreak_spire_lightning_rod", "type": "direction"}
        }
    }

    rooms["stormbreak_spire_lightning_rod"] = {
        "id": "stormbreak_spire_lightning_rod",
        "name": "The Lightning Rod",
        "description": "Near the spire's peak, an enormous natural crystal protrudes from the "
                       "rock, acting as a lightning rod for the entire island. It glows with "
                       "perpetual charge, and touching it would mean instant death. The energy "
                       "here is overwhelming.",
        "coordinates": [cx + 3, cy + 9],
        "location_type": "wilderness",
        "items": {"lightning_rod_fragment": {"quantity": 1, "value": 50}},
        "exits": {
            "south": {"target": "stormbreak_spire_conduit", "type": "direction"},
            "west": {"target": "stormbreak_spire_summit_approach", "type": "direction"}
        }
    }

    rooms["stormbreak_spire_summit_approach"] = {
        "id": "stormbreak_spire_summit_approach",
        "name": "Summit Approach",
        "description": "The final stretch before the spire's summit. The path is barely wide "
                       "enough for one person, and the drop on either side is hundreds of "
                       "feet. Static electricity makes every metal object buzz and spark.",
        "coordinates": [cx + 2, cy + 9],
        "location_type": "wilderness",
        "items": {},
        "exits": {
            "east": {"target": "stormbreak_spire_lightning_rod", "type": "direction"},
            "north": {"target": "stormbreak_spire_summit", "type": "direction"}
        }
    }

    rooms["stormbreak_spire_summit"] = {
        "id": "stormbreak_spire_summit",
        "name": "Spire Summit - Eye of the Storm",
        "description": "The very peak of the Lightning Spire, where you stand inside the eye "
                       "of the eternal storm. For a brief radius around the summit, the air "
                       "is perfectly calm and clear, while a wall of howling wind and lightning "
                       "circles endlessly. An ancient altar of fused crystal sits at the center.",
        "coordinates": [cx + 2, cy + 10],
        "location_type": "wilderness",
        "items": {"eye_of_storm_crystal": {"quantity": 1, "value": 75}, "storm_altar_shard": {"quantity": 1, "value": 40}},
        "exits": {
            "south": {"target": "stormbreak_spire_summit_approach", "type": "direction"},
            "north": {"target": "stormbreak_spire_pinnacle", "type": "direction"}
        }
    }

    # --- Kraken's Reach (8 rooms) ---

    rooms["stormbreak_kraken_shallows"] = {
        "id": "stormbreak_kraken_shallows",
        "name": "Kraken's Reach - Shallows",
        "description": "South of the lighthouse, the reef descends into dark, churning waters. "
                       "The shallows here are littered with crushed ship timbers and enormous "
                       "sucker marks scar the rocks. Something vast lurks in the depths beyond.",
        "coordinates": [cx, cy - 4],
        "location_type": "wilderness",
        "items": {"sucker_marked_timber": {"quantity": 1, "value": 10}},
        "exits": {
            "north": {"target": "stormbreak_lighthouse", "type": "direction"},
            "south": {"target": "stormbreak_kraken_reef", "type": "direction"},
            "west": {"target": "stormbreak_kraken_sea_cave", "type": "direction"}
        }
    }

    rooms["stormbreak_kraken_reef"] = {
        "id": "stormbreak_kraken_reef",
        "name": "Kraken's Reef",
        "description": "A jagged reef where the water suddenly drops to abyssal depths. Massive "
                       "tentacle marks are gouged into the coral, and the water churns with "
                       "unnatural currents. Fishermen refuse to cast nets anywhere near this place.",
        "coordinates": [cx, cy - 5],
        "location_type": "wilderness",
        "items": {"kraken_ink_residue": {"quantity": 1, "value": 22}},
        "exits": {
            "north": {"target": "stormbreak_kraken_shallows", "type": "direction"},
            "west": {"target": "stormbreak_kraken_deep_water", "type": "direction"},
            "east": {"target": "stormbreak_kraken_coral_shelf", "type": "direction"}
        }
    }

    rooms["stormbreak_kraken_sea_cave"] = {
        "id": "stormbreak_kraken_sea_cave",
        "name": "Sea Cave",
        "description": "A half-submerged cave carved into the volcanic rock. The tide surges "
                       "in and out, bringing debris from the deep. Strange clicking sounds echo "
                       "from the darkness, and the walls are covered in claw marks too large "
                       "for any known creature.",
        "coordinates": [cx - 1, cy - 4],
        "location_type": "wilderness",
        "items": {"deep_sea_shell": {"quantity": 1, "value": 14}, "cave_pearl": {"quantity": 1, "value": 18}},
        "exits": {
            "east": {"target": "stormbreak_kraken_shallows", "type": "direction"},
            "south": {"target": "stormbreak_kraken_deep_water", "type": "direction"}
        }
    }

    rooms["stormbreak_kraken_deep_water"] = {
        "id": "stormbreak_kraken_deep_water",
        "name": "Deep Water Channel",
        "description": "A deep channel between the reef and the open ocean. The water is ink-dark "
                       "and bitterly cold. Enormous shadows pass beneath the surface, and the "
                       "sound of something breathing — impossibly large — echoes from below.",
        "coordinates": [cx - 1, cy - 5],
        "location_type": "wilderness",
        "items": {"deep_water_kelp": {"quantity": 2, "value": 8}},
        "exits": {
            "east": {"target": "stormbreak_kraken_reef", "type": "direction"},
            "north": {"target": "stormbreak_kraken_sea_cave", "type": "direction"},
            "south": {"target": "stormbreak_kraken_abyss", "type": "direction"}
        }
    }

    rooms["stormbreak_kraken_coral_shelf"] = {
        "id": "stormbreak_kraken_coral_shelf",
        "name": "Coral Shelf",
        "description": "A broad shelf of ancient coral extending over the abyss. The coral here "
                       "has been crushed and rebuilt countless times by massive impacts. Broken "
                       "weapons and armor from swallowed ships are embedded in the growth.",
        "coordinates": [cx + 1, cy - 5],
        "location_type": "wilderness",
        "items": {"embedded_weapon_hilt": {"quantity": 1, "value": 25}, "crushed_coral": {"quantity": 2, "value": 8}},
        "exits": {
            "west": {"target": "stormbreak_kraken_reef", "type": "direction"},
            "south": {"target": "stormbreak_kraken_trench", "type": "direction"}
        }
    }

    rooms["stormbreak_kraken_abyss"] = {
        "id": "stormbreak_kraken_abyss",
        "name": "The Abyss Edge",
        "description": "The ocean floor falls away into an unfathomable trench. Bioluminescent "
                       "creatures drift up from the darkness like living stars. The water pressure "
                       "is crushing, and an overwhelming sense of something ancient and hungry "
                       "watching from below makes your skin crawl.",
        "coordinates": [cx - 1, cy - 6],
        "location_type": "wilderness",
        "items": {"abyssal_pearl": {"quantity": 1, "value": 50}, "deep_sea_fang": {"quantity": 1, "value": 30}},
        "exits": {
            "north": {"target": "stormbreak_kraken_deep_water", "type": "direction"},
            "east": {"target": "stormbreak_kraken_lair", "type": "direction"}
        }
    }

    rooms["stormbreak_kraken_lair"] = {
        "id": "stormbreak_kraken_lair",
        "name": "Kraken's Lair - Dungeon Entrance",
        "description": "A vast underwater cavern at the edge of the abyss, its walls scarred by "
                       "the passage of something colossal. Enormous tentacle impressions line "
                       "the stone floor, and the water pulses with a rhythmic heartbeat. A yawning "
                       "passage descends into the Tempest Depths — a living dungeon where storm "
                       "and sea converge in darkness.",
        "coordinates": [cx, cy - 6],
        "location_type": "wilderness",
        "items": {"kraken_scale": {"quantity": 1, "value": 60}},
        "exits": {
            "west": {"target": "stormbreak_kraken_abyss", "type": "direction"},
            "east": {"target": "stormbreak_kraken_trench", "type": "direction"},
            "enter": {
                "target": "FIXED_DUNGEON",
                "type": "fixed_dungeon",
                "dungeon_id": "tempest_depths",
                "transition_text": "You dive into the yawning passage. The water grows colder and darker\nas you descend. Lightning flickers in the depths below, illuminating\nmassive stone corridors carved by ancient currents. The Tempest Depths\nawait, where storm and sea are one..."
            }
        }
    }

    rooms["stormbreak_kraken_trench"] = {
        "id": "stormbreak_kraken_trench",
        "name": "Abyssal Trench",
        "description": "A narrow trench cutting through the reef, so deep that light barely "
                       "reaches the bottom. Thermal vents blast scalding water upward, and "
                       "strange eyeless fish swim in the superheated plumes. The trench walls "
                       "glitter with mineral deposits.",
        "coordinates": [cx + 1, cy - 6],
        "location_type": "wilderness",
        "items": {"thermal_vent_crystal": {"quantity": 1, "value": 35}, "trench_mineral": {"quantity": 2, "value": 15}},
        "exits": {
            "west": {"target": "stormbreak_kraken_lair", "type": "direction"},
            "north": {"target": "stormbreak_kraken_coral_shelf", "type": "direction"}
        }
    }

    # --- Storm Forge (5 rooms) ---

    rooms["stormbreak_forge_entrance"] = {
        "id": "stormbreak_forge_entrance",
        "name": "Storm Forge - Entrance",
        "description": "A cave mouth in the ravine wall crackles with residual energy. Scorch "
                       "marks radiate outward like a starburst, and the stone underfoot is "
                       "fused smooth. The air inside shimmers with heat and ozone — this is "
                       "a natural forge powered by the island's eternal lightning.",
        "coordinates": [cx - 2, cy + 4],
        "location_type": "wilderness",
        "items": {"fused_stone_fragment": {"quantity": 1, "value": 14}},
        "exits": {
            "south": {"target": "stormbreak_cliffs_ravine", "type": "direction"},
            "north": {"target": "stormbreak_forge_chamber", "type": "direction"}
        }
    }

    rooms["stormbreak_forge_chamber"] = {
        "id": "stormbreak_forge_chamber",
        "name": "Forge Chamber",
        "description": "The main chamber of the Storm Forge, where natural lightning channels "
                       "through copper veins in the ceiling to strike a massive volcanic anvil. "
                       "The heat is intense, and the air crackles with power. Ancient smithing "
                       "tools of unknown make hang from the walls.",
        "coordinates": [cx - 2, cy + 5],
        "location_type": "building",
        "items": {"volcanic_anvil_chip": {"quantity": 1, "value": 25}, "ancient_tongs": {"quantity": 1, "value": 30}},
        "exits": {
            "south": {"target": "stormbreak_forge_entrance", "type": "direction"},
            "east": {"target": "stormbreak_forge_anvil", "type": "direction"},
            "north": {"target": "stormbreak_forge_crystal_store", "type": "direction"}
        }
    }

    rooms["stormbreak_forge_anvil"] = {
        "id": "stormbreak_forge_anvil",
        "name": "Lightning Anvil",
        "description": "The heart of the forge — an anvil of solidified magma sits beneath a "
                       "natural chimney that channels lightning directly onto its surface. The "
                       "metal shaped here is imbued with storm energy. Half-finished blades "
                       "glow with inner light.",
        "coordinates": [cx - 1, cy + 5],
        "location_type": "building",
        "items": {"storm_forged_blade_blank": {"quantity": 1, "value": 60}, "lightning_quenched_steel": {"quantity": 1, "value": 45}},
        "exits": {
            "west": {"target": "stormbreak_forge_chamber", "type": "direction"},
            "east": {"target": "stormbreak_forge_tempering_hall", "type": "direction"}
        }
    }

    rooms["stormbreak_forge_crystal_store"] = {
        "id": "stormbreak_forge_crystal_store",
        "name": "Crystal Storehouse",
        "description": "A cool side-chamber where charged storm crystals are stored in iron-banded "
                       "chests lined with insulating cork. The crystals hum softly, their inner "
                       "lightning frozen in amber-like clarity. These are the raw materials for "
                       "storm-forged equipment.",
        "coordinates": [cx - 2, cy + 6],
        "location_type": "building",
        "items": {"stored_storm_crystal": {"quantity": 2, "value": 35}, "insulating_cork": {"quantity": 1, "value": 10}},
        "exits": {
            "south": {"target": "stormbreak_forge_chamber", "type": "direction"},
            "east": {"target": "stormbreak_forge_crucible", "type": "direction"}
        }
    }

    rooms["stormbreak_forge_crucible"] = {
        "id": "stormbreak_forge_crucible",
        "name": "Storm Crucible",
        "description": "The deepest chamber of the forge contains a crucible of volcanic glass "
                       "suspended over a magma vent. Storm crystals are melted here and infused "
                       "into molten metal. The resulting alloy — stormsteel — is among the most "
                       "powerful materials in the known world.",
        "coordinates": [cx - 1, cy + 6],
        "location_type": "building",
        "items": {"stormsteel_ingot": {"quantity": 1, "value": 80}, "volcanic_glass_crucible_chip": {"quantity": 1, "value": 20}},
        "exits": {
            "west": {"target": "stormbreak_forge_crystal_store", "type": "direction"},
            "north": {"target": "stormbreak_forge_quenching_pool", "type": "direction"}
        }
    }



    # === STORMBREAK ISLAND EXPANSION ===

    # --- Expanded Docks (+3 rooms) ---

    rooms["stormbreak_dock_breakwater"] = {
        "id": "stormbreak_dock_breakwater",
        "name": "Storm Breakwater",
        "description": "A massive seawall of reinforced stone and coral blocks extending from "
                       "the eastern dock. Chains thick as a man's arm anchor floating barriers "
                       "that absorb the worst of incoming waves. Spray constantly washes over "
                       "the walkway, making footing treacherous.",
        "coordinates": [cx + 2, cy - 2],
        "location_type": "dock",
        "items": {"iron_chain_link": {"quantity": 2, "value": 12}, "coral_block": {"quantity": 1, "value": 8}},
        "exits": {
            "west": {"target": "stormbreak_cargo_shelter", "type": "direction"},
            "east": {"target": "stormbreak_dock_net_loft", "type": "direction"}
        }
    }

    rooms["stormbreak_dock_net_loft"] = {
        "id": "stormbreak_dock_net_loft",
        "name": "Net Loft",
        "description": "A raised platform built above the high-water mark where fishermen mend "
                       "their nets. Dozens of nets in various states of repair hang from drying "
                       "racks, some woven with storm-resistant fibers that shimmer faintly blue. "
                       "The smell of salt and tar is overwhelming.",
        "coordinates": [cx + 3, cy - 2],
        "location_type": "dock",
        "items": {"storm_net": {"quantity": 1, "value": 18}, "tar_bucket": {"quantity": 1, "value": 5}},
        "exits": {
            "west": {"target": "stormbreak_dock_breakwater", "type": "direction"},
            "south": {"target": "stormbreak_dock_tide_pool", "type": "direction"}
        }
    }

    rooms["stormbreak_dock_tide_pool"] = {
        "id": "stormbreak_dock_tide_pool",
        "name": "Dock Tide Pools",
        "description": "Rocky tide pools at the base of the breakwater teem with colorful marine "
                       "life. Anemones, starfish, and small crabs inhabit the shallow pools, while "
                       "deeper ones hold stranger creatures — eels that crackle with static "
                       "electricity and hermit crabs wearing storm-glass shells.",
        "coordinates": [cx + 3, cy - 3],
        "location_type": "wilderness",
        "items": {"electric_eel": {"quantity": 1, "value": 22}, "storm_glass_shell": {"quantity": 1, "value": 15}},
        "exits": {
            "north": {"target": "stormbreak_dock_net_loft", "type": "direction"}
        }
    }

    # --- Expanded Reef Town (+10 rooms) ---

    rooms["stormbreak_town_training_yard"] = {
        "id": "stormbreak_town_training_yard",
        "name": "Storm Guard Training Yard",
        "description": "An open-air training ground where the Storm Guard practice fighting in "
                       "howling winds. Training dummies are mounted on springs that whip them "
                       "around unpredictably, and sand-filled bags swing on chains. The ground "
                       "is deliberately kept muddy to simulate storm conditions.",
        "coordinates": [cx + 3, cy + 1],
        "location_type": "building",
        "items": {"training_sword": {"quantity": 1, "value": 12}, "wind_resistance_cloak": {"quantity": 1, "value": 30}},
        "exits": {
            "west": {"target": "stormbreak_town_barracks", "type": "direction"},
            "east": {"target": "stormbreak_town_armory", "type": "direction"},
            "north": {"target": "stormbreak_town_storm_cellar", "type": "direction"}
        }
    }

    rooms["stormbreak_town_armory"] = {
        "id": "stormbreak_town_armory",
        "name": "Reef Town Armory",
        "description": "A fortified stone building housing the island's weapons and armor. "
                       "Racks of storm-forged blades, lightning-resistant shields, and gale-proof "
                       "helms line the walls. A grizzled quartermaster keeps meticulous inventory "
                       "of every piece.",
        "coordinates": [cx + 4, cy + 1],
        "location_type": "building",
        "items": {"storm_guard_helm": {"quantity": 1, "value": 35}, "gale_shield": {"quantity": 1, "value": 40}},
        "exits": {
            "west": {"target": "stormbreak_town_training_yard", "type": "direction"},
            "north": {"target": "stormbreak_town_watchtower", "type": "direction"}
        }
    }

    rooms["stormbreak_town_watchtower"] = {
        "id": "stormbreak_town_watchtower",
        "name": "Eastern Watchtower",
        "description": "A squat stone tower on the eastern edge of town, designed to withstand "
                       "the fiercest hurricanes. From the top, guards can spot approaching ships "
                       "and incoming storm fronts. A complex system of flags and light signals "
                       "allows communication with the lighthouse.",
        "coordinates": [cx + 4, cy + 2],
        "location_type": "building",
        "items": {"signal_flags": {"quantity": 1, "value": 10}, "spyglass": {"quantity": 1, "value": 25}},
        "exits": {
            "south": {"target": "stormbreak_town_armory", "type": "direction"}
        }
    }

    rooms["stormbreak_town_prayer_garden"] = {
        "id": "stormbreak_town_prayer_garden",
        "name": "Prayer Garden",
        "description": "A walled garden behind the shrine where devotees of the storm spirits "
                       "come to meditate. Wind chimes made of storm glass create haunting melodies, "
                       "and carefully tended lightning flowers bloom in patterns that mirror the "
                       "storm clouds above. A peace pervades despite the howling winds.",
        "coordinates": [cx + 2, cy + 2],
        "location_type": "building",
        "items": {"lightning_flower": {"quantity": 2, "value": 18}, "storm_glass_chime": {"quantity": 1, "value": 22}},
        "exits": {
            "west": {"target": "stormbreak_town_shrine", "type": "direction"},
            "north": {"target": "stormbreak_town_upper_market", "type": "direction"}
        }
    }

    rooms["stormbreak_town_storm_cellar"] = {
        "id": "stormbreak_town_storm_cellar",
        "name": "Community Storm Cellar",
        "description": "A deep underground bunker where the entire town shelters during the worst "
                       "tempests. Reinforced with iron beams and volcanic stone, it holds emergency "
                       "supplies, bedding, and a small shrine. Scratch marks on the walls count "
                       "the hours of countless storms endured.",
        "coordinates": [cx + 3, cy + 2],
        "location_type": "building",
        "items": {"emergency_rations": {"quantity": 3, "value": 5}, "storm_blanket": {"quantity": 1, "value": 8}},
        "exits": {
            "south": {"target": "stormbreak_town_training_yard", "type": "direction"},
            "west": {"target": "stormbreak_town_prayer_garden", "type": "direction"}
        }
    }

    rooms["stormbreak_town_library"] = {
        "id": "stormbreak_town_library",
        "name": "Storm Scholar's Library",
        "description": "A cramped but well-stocked library built into a natural cave at the "
                       "north end of town. Shelves of waterproofed books contain centuries of "
                       "storm observations, tidal charts, and folklore about the eternal tempest. "
                       "A scholar mutters to herself while cross-referencing lightning patterns.",
        "coordinates": [cx, cy + 3],
        "location_type": "building",
        "items": {"storm_almanac": {"quantity": 1, "value": 20}, "tidal_chart": {"quantity": 1, "value": 15}},
        "exits": {
            "south": {"target": "stormbreak_town_north", "type": "direction"},
            "east": {"target": "stormbreak_town_fishmonger", "type": "direction"},
            "west": {"target": "stormbreak_town_chandlery", "type": "direction"}
        }
    }

    rooms["stormbreak_town_fishmonger"] = {
        "id": "stormbreak_town_fishmonger",
        "name": "Fishmonger's Stall",
        "description": "An open-air market stall where the day's catch is displayed on ice slabs "
                       "cut from the frozen upper peaks. Storm-touched fish with bioluminescent "
                       "scales fetch premium prices. The fishmonger shouts prices over the wind, "
                       "her voice carrying with practiced ease.",
        "coordinates": [cx + 1, cy + 3],
        "location_type": "settlement",
        "items": {"storm_fish": {"quantity": 2, "value": 12}, "bioluminescent_fillet": {"quantity": 1, "value": 20}},
        "exits": {
            "west": {"target": "stormbreak_town_library", "type": "direction"},
            "east": {"target": "stormbreak_town_upper_market", "type": "direction"}
        }
    }

    rooms["stormbreak_town_upper_market"] = {
        "id": "stormbreak_town_upper_market",
        "name": "Upper Market",
        "description": "The northern marketplace where traders sell goods too delicate for the "
                       "wind-blasted main square. Covered stalls with storm-shutters display "
                       "jewelry, potions, and imported luxuries. A money-changer's booth sits "
                       "in the most sheltered corner.",
        "coordinates": [cx + 2, cy + 3],
        "location_type": "settlement",
        "items": {"storm_potion": {"quantity": 1, "value": 25}, "reef_pearl_necklace": {"quantity": 1, "value": 35}},
        "exits": {
            "west": {"target": "stormbreak_town_fishmonger", "type": "direction"},
            "south": {"target": "stormbreak_town_prayer_garden", "type": "direction"}
        }
    }

    rooms["stormbreak_town_chandlery"] = {
        "id": "stormbreak_town_chandlery",
        "name": "Chandler's Workshop",
        "description": "A workshop specializing in candles, ropes, and ship supplies essential "
                       "for storm-battered vessels. The chandler crafts special storm-wicks that "
                       "burn even in hurricane-force winds, charging premium prices for the "
                       "island's signature innovation.",
        "coordinates": [cx - 1, cy + 3],
        "location_type": "building",
        "items": {"storm_wick_candle": {"quantity": 2, "value": 10}, "weather_rope": {"quantity": 1, "value": 15}},
        "exits": {
            "east": {"target": "stormbreak_town_library", "type": "direction"},
            "south": {"target": "stormbreak_town_well", "type": "direction"}
        }
    }

    rooms["stormbreak_town_scouts_lodge"] = {
        "id": "stormbreak_town_scouts_lodge",
        "name": "Storm Scouts' Lodge",
        "description": "A gathering place for the island's scouts — hardy individuals who venture "
                       "into the wild interior to map safe routes and track storm patterns. Maps "
                       "cover every wall, and a large sand-table in the center models the island's "
                       "terrain with remarkable detail.",
        "coordinates": [cx - 2, cy + 3],
        "location_type": "building",
        "items": {"scout_map": {"quantity": 1, "value": 18}, "storm_compass": {"quantity": 1, "value": 28}},
        "exits": {
            "east": {"target": "stormbreak_town_chandlery", "type": "direction"}
        }
    }

    # --- Expanded Shipwreck Graveyard (+8 rooms) ---

    rooms["stormbreak_graveyard_flotsam_shore"] = {
        "id": "stormbreak_graveyard_flotsam_shore",
        "name": "Flotsam Shore",
        "description": "A stretch of beach north of the graveyard where fresh wreckage washes "
                       "ashore after every major storm. Planks, barrels, and personal belongings "
                       "litter the sand. Scavengers pick through the debris at low tide, "
                       "occasionally finding valuables.",
        "coordinates": [cx - 3, cy + 3],
        "location_type": "wilderness",
        "items": {"washed_up_compass": {"quantity": 1, "value": 15}, "salvage_plank": {"quantity": 2, "value": 4}},
        "exits": {
            "south": {"target": "stormbreak_graveyard_tide_wreck", "type": "direction"},
            "west": {"target": "stormbreak_graveyard_barnacle_cavern", "type": "direction"}
        }
    }

    rooms["stormbreak_graveyard_barnacle_cavern"] = {
        "id": "stormbreak_graveyard_barnacle_cavern",
        "name": "Barnacle Cavern",
        "description": "A sea cave whose walls are completely encrusted with barnacles and "
                       "mussels. At high tide, water fills the cavern to waist height. Strange "
                       "echo effects make it sound like the barnacles are whispering. Sailors "
                       "say the cave remembers the voices of the drowned.",
        "coordinates": [cx - 4, cy + 3],
        "location_type": "wilderness",
        "items": {"whispering_barnacle": {"quantity": 1, "value": 20}, "cave_mussel": {"quantity": 3, "value": 4}},
        "exits": {
            "east": {"target": "stormbreak_graveyard_flotsam_shore", "type": "direction"},
            "west": {"target": "stormbreak_graveyard_drowned_chapel", "type": "direction"}
        }
    }

    rooms["stormbreak_graveyard_drowned_chapel"] = {
        "id": "stormbreak_graveyard_drowned_chapel",
        "name": "Drowned Chapel",
        "description": "The ruins of a chapel that once served the crews of ships moored in "
                       "this bay. Now half-submerged and overgrown with kelp, its stone pews "
                       "and altar still stand. Votive candles in waterproof holders still burn, "
                       "tended by someone — or something — unseen.",
        "coordinates": [cx - 5, cy + 3],
        "location_type": "wilderness",
        "items": {"votive_candle": {"quantity": 2, "value": 8}, "waterproof_prayer_book": {"quantity": 1, "value": 22}},
        "exits": {
            "east": {"target": "stormbreak_graveyard_barnacle_cavern", "type": "direction"},
            "south": {"target": "stormbreak_graveyard_anchor_yard", "type": "direction"}
        }
    }

    rooms["stormbreak_graveyard_anchor_yard"] = {
        "id": "stormbreak_graveyard_anchor_yard",
        "name": "Anchor Yard",
        "description": "A clearing littered with dozens of rusty anchors of every size and "
                       "design. Some are ancient, their flukes worn smooth by centuries of tide. "
                       "Others are recent, torn from ships in the last storm season. The anchors "
                       "form an eerie sculpture garden of maritime loss.",
        "coordinates": [cx - 6, cy + 2],
        "location_type": "wilderness",
        "items": {"ancient_anchor_chain": {"quantity": 1, "value": 18}, "corroded_anchor_fluke": {"quantity": 1, "value": 10}},
        "exits": {
            "north": {"target": "stormbreak_graveyard_drowned_chapel", "type": "direction"},
            "south": {"target": "stormbreak_graveyard_hull_breach", "type": "direction"}
        }
    }

    rooms["stormbreak_graveyard_hull_breach"] = {
        "id": "stormbreak_graveyard_hull_breach",
        "name": "Breached Hull",
        "description": "The split hull of an enormous galleon lies on its side like a beached "
                       "whale. The breach in its hull is large enough to walk through, revealing "
                       "a cavernous interior filled with silt and rusted equipment. Fish swim "
                       "through the upper decks at high tide.",
        "coordinates": [cx - 6, cy + 1],
        "location_type": "wilderness",
        "items": {"galleon_timber": {"quantity": 1, "value": 12}, "rusted_cutlass": {"quantity": 1, "value": 15}},
        "exits": {
            "north": {"target": "stormbreak_graveyard_anchor_yard", "type": "direction"},
            "south": {"target": "stormbreak_graveyard_salvager_camp", "type": "direction"}
        }
    }

    rooms["stormbreak_graveyard_salvager_camp"] = {
        "id": "stormbreak_graveyard_salvager_camp",
        "name": "Salvager's Camp",
        "description": "A semi-permanent camp set up by professional salvagers who work the "
                       "graveyard during calm periods. Tents are staked deep into the ground, "
                       "and diving equipment hangs from makeshift racks. A fire pit holds the "
                       "remains of last night's meal.",
        "coordinates": [cx - 6, cy],
        "location_type": "settlement",
        "items": {"diving_helmet": {"quantity": 1, "value": 30}, "salvage_manifest": {"quantity": 1, "value": 10}},
        "exits": {
            "north": {"target": "stormbreak_graveyard_hull_breach", "type": "direction"},
            "south": {"target": "stormbreak_graveyard_ghost_quarters", "type": "direction"}
        }
    }

    rooms["stormbreak_graveyard_ghost_quarters"] = {
        "id": "stormbreak_graveyard_ghost_quarters",
        "name": "Ghost Quarters",
        "description": "The officers' quarters of a ghostly frigate, eerily preserved despite "
                       "decades of exposure. The captain's desk still holds charts and a half-written "
                       "letter. At night, lanterns are said to flicker with pale blue light and "
                       "footsteps echo across empty decks.",
        "coordinates": [cx - 6, cy - 1],
        "location_type": "wilderness",
        "items": {"ghost_captain_letter": {"quantity": 1, "value": 35}, "phantom_lantern": {"quantity": 1, "value": 25}},
        "exits": {
            "north": {"target": "stormbreak_graveyard_salvager_camp", "type": "direction"},
            "east": {"target": "stormbreak_graveyard_sunken_vault", "type": "direction"}
        }
    }

    rooms["stormbreak_graveyard_sunken_vault"] = {
        "id": "stormbreak_graveyard_sunken_vault",
        "name": "Sunken Treasure Vault",
        "description": "Deep beneath the ghost quarters, a reinforced strongroom has been "
                       "exposed by erosion. Its iron door hangs open, revealing a chamber that "
                       "once held a fortune. Most treasure has been looted, but hidden compartments "
                       "in the walls may still hold secrets.",
        "coordinates": [cx - 7, cy - 1],
        "location_type": "wilderness",
        "items": {"hidden_doubloon_cache": {"quantity": 1, "value": 50}, "rusted_lock_mechanism": {"quantity": 1, "value": 12}},
        "exits": {
            "west": {"target": "stormbreak_graveyard_ghost_quarters", "type": "direction"}
        }
    }

    # --- Expanded Coral Labyrinth (+6 rooms) ---

    rooms["stormbreak_coral_grotto_deep"] = {
        "id": "stormbreak_coral_grotto_deep",
        "name": "Deep Grotto",
        "description": "Beyond the hidden grotto, the coral formations grow larger and more "
                       "elaborate. Columns of living coral reach from floor to ceiling, creating "
                       "a natural cathedral. Bioluminescent organisms embedded in the coral cast "
                       "the chamber in shifting blue and green light.",
        "coordinates": [cx + 6, cy - 2],
        "location_type": "wilderness",
        "items": {"luminous_coral_shard": {"quantity": 1, "value": 30}, "cathedral_coral_piece": {"quantity": 1, "value": 22}},
        "exits": {
            "west": {"target": "stormbreak_coral_grotto", "type": "direction"},
            "north": {"target": "stormbreak_coral_oyster_beds", "type": "direction"},
            "east": {"target": "stormbreak_coral_crystal_cave", "type": "direction"}
        }
    }

    rooms["stormbreak_coral_oyster_beds"] = {
        "id": "stormbreak_coral_oyster_beds",
        "name": "Giant Oyster Beds",
        "description": "Vast beds of enormous oysters carpet the sandy floor of this underwater "
                       "chamber. Each oyster is the size of a serving platter, and some contain "
                       "pearls shot through with electric-blue veins. The oysters snap shut with "
                       "surprising force when disturbed.",
        "coordinates": [cx + 6, cy - 1],
        "location_type": "wilderness",
        "items": {"giant_storm_pearl": {"quantity": 1, "value": 45}, "oyster_meat": {"quantity": 2, "value": 8}},
        "exits": {
            "north": {"target": "stormbreak_coral_pearl_bed", "type": "direction"},
            "south": {"target": "stormbreak_coral_grotto_deep", "type": "direction"},
            "east": {"target": "stormbreak_coral_luminous_chamber", "type": "direction"}
        }
    }

    rooms["stormbreak_coral_luminous_chamber"] = {
        "id": "stormbreak_coral_luminous_chamber",
        "name": "Luminous Chamber",
        "description": "A spherical chamber within the reef that glows with intense "
                       "bioluminescence. Every surface is covered with light-producing organisms "
                       "that pulse in synchronized waves. The light is bright enough to read by, "
                       "and the effect is hypnotically beautiful.",
        "coordinates": [cx + 7, cy - 1],
        "location_type": "wilderness",
        "items": {"bioluminescent_polyp": {"quantity": 2, "value": 18}, "light_coral_fragment": {"quantity": 1, "value": 25}},
        "exits": {
            "west": {"target": "stormbreak_coral_oyster_beds", "type": "direction"},
            "south": {"target": "stormbreak_coral_crystal_cave", "type": "direction"},
            "east": {"target": "stormbreak_coral_reef_throne", "type": "direction"}
        }
    }

    rooms["stormbreak_coral_crystal_cave"] = {
        "id": "stormbreak_coral_crystal_cave",
        "name": "Crystal Cave",
        "description": "Where coral meets volcanic rock, a cave of natural crystal formations "
                       "has grown. Storm energy channeled through the reef has caused the crystals "
                       "to develop in impossible geometric patterns. They ring like bells when "
                       "touched, each producing a different note.",
        "coordinates": [cx + 7, cy - 2],
        "location_type": "wilderness",
        "items": {"singing_crystal": {"quantity": 1, "value": 35}, "geometric_crystal_cluster": {"quantity": 1, "value": 28}},
        "exits": {
            "west": {"target": "stormbreak_coral_grotto_deep", "type": "direction"},
            "north": {"target": "stormbreak_coral_luminous_chamber", "type": "direction"}
        }
    }

    rooms["stormbreak_coral_anemone_garden"] = {
        "id": "stormbreak_coral_anemone_garden",
        "name": "Anemone Garden",
        "description": "A mesmerizing garden of giant sea anemones in every color imaginable. "
                       "Their tentacles sway in the current like flowers in a breeze. Some "
                       "anemones have formed symbiotic relationships with electric eels, creating "
                       "a dazzling but dangerous display of living light.",
        "coordinates": [cx + 7, cy],
        "location_type": "wilderness",
        "items": {"anemone_extract": {"quantity": 1, "value": 20}, "electric_symbiote": {"quantity": 1, "value": 30}},
        "exits": {
            "south": {"target": "stormbreak_coral_luminous_chamber", "type": "direction"},
            "west": {"target": "stormbreak_coral_pearl_bed", "type": "direction"}
        }
    }

    rooms["stormbreak_coral_reef_throne"] = {
        "id": "stormbreak_coral_reef_throne",
        "name": "Reef Throne",
        "description": "At the heart of the expanded coral labyrinth sits a natural formation "
                       "resembling a throne, grown from living coral over untold centuries. Local "
                       "legend says the reef itself is sentient, and whoever sits the throne can "
                       "communicate with the coral mind. The water here is warm and still.",
        "coordinates": [cx + 8, cy - 1],
        "location_type": "wilderness",
        "items": {"throne_coral_fragment": {"quantity": 1, "value": 50}, "reef_mind_pearl": {"quantity": 1, "value": 60}},
        "exits": {
            "west": {"target": "stormbreak_coral_luminous_chamber", "type": "direction"}
        }
    }

    # --- Expanded Lightning Spire (+6 rooms) ---

    rooms["stormbreak_spire_pinnacle"] = {
        "id": "stormbreak_spire_pinnacle",
        "name": "Spire Pinnacle",
        "description": "Above the summit's eye, impossible as it seems, a narrow spire of "
                       "fused volcanic glass rises into the storm wall itself. Lightning strikes "
                       "it constantly, the energy flowing down channels carved by elemental forces. "
                       "Standing here feels like being at the center of creation.",
        "coordinates": [cx + 2, cy + 11],
        "location_type": "wilderness",
        "items": {"fused_glass_shard": {"quantity": 1, "value": 40}, "storm_essence": {"quantity": 1, "value": 55}},
        "exits": {
            "south": {"target": "stormbreak_spire_summit", "type": "direction"},
            "west": {"target": "stormbreak_spire_storm_conduit", "type": "direction"},
            "east": {"target": "stormbreak_spire_lightning_rod_chamber", "type": "direction"},
            "north": {"target": "stormbreak_spire_cloud_walk", "type": "direction"}
        }
    }

    rooms["stormbreak_spire_storm_conduit"] = {
        "id": "stormbreak_spire_storm_conduit",
        "name": "Storm Conduit",
        "description": "A channel carved into the spire's western face where storm energy flows "
                       "like water. Arcs of lightning cascade down the groove, pooling in natural "
                       "basins carved into the rock. The air tastes of ozone and raw power. "
                       "Ancient runes line the conduit, suggesting deliberate construction.",
        "coordinates": [cx + 1, cy + 11],
        "location_type": "wilderness",
        "items": {"conduit_rune_rubbing": {"quantity": 1, "value": 25}, "pooled_lightning_vial": {"quantity": 1, "value": 45}},
        "exits": {
            "east": {"target": "stormbreak_spire_pinnacle", "type": "direction"},
            "north": {"target": "stormbreak_spire_observation_deck", "type": "direction"}
        }
    }

    rooms["stormbreak_spire_lightning_rod_chamber"] = {
        "id": "stormbreak_spire_lightning_rod_chamber",
        "name": "Lightning Rod Chamber",
        "description": "A natural chamber containing an enormous crystal that acts as a lightning "
                       "rod for the entire spire. The crystal is three times the height of a person "
                       "and glows with captured storm energy. Cables of copper and stormsteel "
                       "connect it to the forge far below.",
        "coordinates": [cx + 3, cy + 11],
        "location_type": "wilderness",
        "items": {"lightning_rod_crystal_chip": {"quantity": 1, "value": 50}, "stormsteel_cable_strand": {"quantity": 1, "value": 30}},
        "exits": {
            "west": {"target": "stormbreak_spire_pinnacle", "type": "direction"}
        }
    }

    rooms["stormbreak_spire_cloud_walk"] = {
        "id": "stormbreak_spire_cloud_walk",
        "name": "Cloud Walk",
        "description": "A narrow path that seems to extend into the clouds themselves. The stone "
                       "gives way to a bridge of solidified storm energy — translucent and crackling "
                       "with static. Below is nothing but churning cloud and flashes of lightning. "
                       "Each step sends ripples through the energy bridge.",
        "coordinates": [cx + 2, cy + 12],
        "location_type": "wilderness",
        "items": {"solidified_storm_crystal": {"quantity": 1, "value": 40}},
        "exits": {
            "south": {"target": "stormbreak_spire_pinnacle", "type": "direction"},
            "west": {"target": "stormbreak_spire_observation_deck", "type": "direction"},
            "north": {"target": "stormbreak_spire_storm_nexus", "type": "direction"}
        }
    }

    rooms["stormbreak_spire_observation_deck"] = {
        "id": "stormbreak_spire_observation_deck",
        "name": "Storm Observation Deck",
        "description": "A platform built by some ancient civilization for observing the eternal "
                       "storm from within. Instruments of unknown design track lightning patterns, "
                       "wind speeds, and atmospheric pressure. Some still function, their dials "
                       "spinning and clicking with mechanical precision.",
        "coordinates": [cx + 1, cy + 12],
        "location_type": "wilderness",
        "items": {"ancient_barometer": {"quantity": 1, "value": 35}, "storm_tracking_lens": {"quantity": 1, "value": 28}},
        "exits": {
            "south": {"target": "stormbreak_spire_storm_conduit", "type": "direction"},
            "east": {"target": "stormbreak_spire_cloud_walk", "type": "direction"}
        }
    }

    rooms["stormbreak_spire_storm_nexus"] = {
        "id": "stormbreak_spire_storm_nexus",
        "name": "Storm Nexus",
        "description": "The highest reachable point of the Lightning Spire — a platform where "
                       "all storm energy converges. Lightning from every direction strikes this "
                       "point simultaneously, creating a pillar of continuous electrical discharge. "
                       "Within the chaos, strange geometric patterns are visible, suggesting an "
                       "intelligence behind the storm.",
        "coordinates": [cx + 2, cy + 13],
        "location_type": "wilderness",
        "items": {"nexus_crystal": {"quantity": 1, "value": 80}, "storm_pattern_map": {"quantity": 1, "value": 45}},
        "exits": {
            "south": {"target": "stormbreak_spire_cloud_walk", "type": "direction"},
            "north": {"target": "stormbreak_maelstrom_path", "type": "direction"}
        }
    }

    # --- Expanded Storm Cliffs (+6 rooms) ---

    rooms["stormbreak_cliffs_arch_bridge"] = {
        "id": "stormbreak_cliffs_arch_bridge",
        "name": "Arch Bridge Crossing",
        "description": "Beyond the lightning arch, a precarious bridge of storm-fused stone "
                       "connects to an isolated cliff section. The bridge is barely wide enough "
                       "for one person and has no railings. Wind howls through the gap below, "
                       "carrying the sound of crashing waves.",
        "coordinates": [cx + 3, cy + 4],
        "location_type": "wilderness",
        "items": {"wind_worn_stone": {"quantity": 1, "value": 8}},
        "exits": {
            "west": {"target": "stormbreak_cliffs_arch", "type": "direction"},
            "east": {"target": "stormbreak_cliffs_sea_cave", "type": "direction"},
            "north": {"target": "stormbreak_cliffs_cliff_roost", "type": "direction"}
        }
    }

    rooms["stormbreak_cliffs_cliff_roost"] = {
        "id": "stormbreak_cliffs_cliff_roost",
        "name": "Storm Raptor Roost",
        "description": "A sheltered ledge high on the cliff face where massive storm raptors "
                       "nest. The birds are the size of eagles with feathers that crackle with "
                       "static electricity. Their nests are woven from copper wire and seagrass, "
                       "and eggs inside glow with inner lightning.",
        "coordinates": [cx + 3, cy + 5],
        "location_type": "wilderness",
        "items": {"storm_raptor_feather": {"quantity": 1, "value": 30}, "copper_nest_wire": {"quantity": 2, "value": 8}},
        "exits": {
            "south": {"target": "stormbreak_cliffs_arch_bridge", "type": "direction"},
            "east": {"target": "stormbreak_cliffs_cliff_shrine", "type": "direction"}
        }
    }

    rooms["stormbreak_cliffs_sea_cave"] = {
        "id": "stormbreak_cliffs_sea_cave",
        "name": "Thundering Sea Cave",
        "description": "A deep cave carved into the cliff base by millennia of wave action. "
                       "Each wave crashes in with thunderous force, sending spray fifty feet "
                       "into the air. At the back of the cave, the water is calmer, and strange "
                       "formations of salt crystal grow in impossible spirals.",
        "coordinates": [cx + 4, cy + 4],
        "location_type": "wilderness",
        "items": {"spiral_salt_crystal": {"quantity": 1, "value": 22}, "thunder_stone": {"quantity": 1, "value": 18}},
        "exits": {
            "west": {"target": "stormbreak_cliffs_arch_bridge", "type": "direction"},
            "east": {"target": "stormbreak_cliffs_smugglers_path", "type": "direction"},
            "north": {"target": "stormbreak_cliffs_cliff_shrine", "type": "direction"}
        }
    }

    rooms["stormbreak_cliffs_cliff_shrine"] = {
        "id": "stormbreak_cliffs_cliff_shrine",
        "name": "Cliff Face Shrine",
        "description": "Carved directly into the cliff face by ancient hands, this shrine "
                       "depicts a figure calming the waves with outstretched arms. Offerings "
                       "of storm glass and coral have been placed in niches around the carving. "
                       "During lightning storms, the figure seems to glow from within.",
        "coordinates": [cx + 4, cy + 5],
        "location_type": "wilderness",
        "items": {"cliff_shrine_offering": {"quantity": 1, "value": 20}, "ancient_carving_rubbing": {"quantity": 1, "value": 15}},
        "exits": {
            "south": {"target": "stormbreak_cliffs_sea_cave", "type": "direction"},
            "west": {"target": "stormbreak_cliffs_cliff_roost", "type": "direction"},
            "east": {"target": "stormbreak_cliffs_cliff_hollow", "type": "direction"}
        }
    }

    rooms["stormbreak_cliffs_smugglers_path"] = {
        "id": "stormbreak_cliffs_smugglers_path",
        "name": "Smuggler's Path",
        "description": "A hidden trail along the cliff base, partially submerged at high tide. "
                       "Iron rings hammered into the rock once held smuggler's boats. The path "
                       "winds through narrow gaps between boulders, invisible from above. "
                       "Contraband markings are scratched into the rock at intervals.",
        "coordinates": [cx + 5, cy + 4],
        "location_type": "wilderness",
        "items": {"smuggler_mark_stone": {"quantity": 1, "value": 12}, "hidden_cache_key": {"quantity": 1, "value": 20}},
        "exits": {
            "west": {"target": "stormbreak_cliffs_sea_cave", "type": "direction"},
            "north": {"target": "stormbreak_cliffs_cliff_hollow", "type": "direction"}
        }
    }

    rooms["stormbreak_cliffs_cliff_hollow"] = {
        "id": "stormbreak_cliffs_cliff_hollow",
        "name": "Cliff Hollow",
        "description": "A large natural cavity within the cliff itself, accessible through "
                       "a crack in the rock face. The hollow is surprisingly spacious and dry, "
                       "with natural shelves formed by layered stone. Evidence suggests someone "
                       "once lived here — a hearth, storage alcoves, and carved steps.",
        "coordinates": [cx + 5, cy + 5],
        "location_type": "wilderness",
        "items": {"hermit_journal": {"quantity": 1, "value": 22}, "carved_stone_bowl": {"quantity": 1, "value": 10}},
        "exits": {
            "west": {"target": "stormbreak_cliffs_cliff_shrine", "type": "direction"},
            "south": {"target": "stormbreak_cliffs_smugglers_path", "type": "direction"}
        }
    }

    # --- Expanded Storm Forge (+5 rooms) ---

    rooms["stormbreak_forge_quenching_pool"] = {
        "id": "stormbreak_forge_quenching_pool",
        "name": "Storm Quenching Pool",
        "description": "A deep pool of water charged with storm energy, used to quench "
                       "newly forged stormsteel. The water glows faintly blue and crackles "
                       "when metal is plunged into it. The resulting temper is said to make "
                       "the metal nearly indestructible. Steam rises constantly.",
        "coordinates": [cx - 1, cy + 7],
        "location_type": "building",
        "items": {"charged_quenching_water": {"quantity": 1, "value": 25}, "quenched_stormsteel_strip": {"quantity": 1, "value": 40}},
        "exits": {
            "south": {"target": "stormbreak_forge_crucible", "type": "direction"},
            "west": {"target": "stormbreak_forge_alloy_workshop", "type": "direction"},
            "east": {"target": "stormbreak_forge_gallery", "type": "direction"}
        }
    }

    rooms["stormbreak_forge_tempering_hall"] = {
        "id": "stormbreak_forge_tempering_hall",
        "name": "Tempering Hall",
        "description": "A long hall where finished storm-forged weapons and armor undergo "
                       "their final tempering process. Items are hung from chains and slowly "
                       "rotated through zones of heat and cold. Master smiths inspect each piece "
                       "with obsessive attention to detail.",
        "coordinates": [cx, cy + 6],
        "location_type": "building",
        "items": {"tempered_storm_blade": {"quantity": 1, "value": 55}, "master_smith_tools": {"quantity": 1, "value": 30}},
        "exits": {
            "west": {"target": "stormbreak_forge_anvil", "type": "direction"},
            "north": {"target": "stormbreak_forge_gallery", "type": "direction"}
        }
    }

    rooms["stormbreak_forge_gallery"] = {
        "id": "stormbreak_forge_gallery",
        "name": "Forge Gallery",
        "description": "A display hall showcasing the finest works ever produced by the Storm "
                       "Forge. Legendary weapons behind crystal cases glow with inner storm light. "
                       "Each piece has a nameplate telling its history. The gallery also serves "
                       "as a showroom for wealthy buyers.",
        "coordinates": [cx, cy + 7],
        "location_type": "building",
        "items": {"gallery_catalog": {"quantity": 1, "value": 15}, "display_storm_crystal": {"quantity": 1, "value": 20}},
        "exits": {
            "south": {"target": "stormbreak_forge_tempering_hall", "type": "direction"},
            "west": {"target": "stormbreak_forge_quenching_pool", "type": "direction"},
            "north": {"target": "stormbreak_forge_testing_range", "type": "direction"}
        }
    }

    rooms["stormbreak_forge_alloy_workshop"] = {
        "id": "stormbreak_forge_alloy_workshop",
        "name": "Alloy Workshop",
        "description": "A specialized workshop where experimental alloys are developed. Crucibles "
                       "of different metals bubble over volcanic vents while apprentice smiths "
                       "take careful notes. A chalkboard on the wall tracks the properties of "
                       "dozens of experimental stormsteel variants.",
        "coordinates": [cx - 2, cy + 7],
        "location_type": "building",
        "items": {"experimental_alloy_sample": {"quantity": 1, "value": 35}, "alloy_recipe_scroll": {"quantity": 1, "value": 25}},
        "exits": {
            "east": {"target": "stormbreak_forge_quenching_pool", "type": "direction"},
            "south": {"target": "stormbreak_forge_crystal_store", "type": "direction"}
        }
    }

    rooms["stormbreak_forge_testing_range"] = {
        "id": "stormbreak_forge_testing_range",
        "name": "Weapon Testing Range",
        "description": "An open area behind the forge where newly crafted weapons are tested "
                       "against reinforced targets. Dummies of iron and volcanic stone bear the "
                       "scars of countless tests. A measuring apparatus tracks the lightning "
                       "discharge of each strike.",
        "coordinates": [cx - 1, cy + 8],
        "location_type": "building",
        "items": {"testing_target_fragment": {"quantity": 1, "value": 8}, "discharge_meter": {"quantity": 1, "value": 22}},
        "exits": {
            "south": {"target": "stormbreak_forge_gallery", "type": "direction"}
        }
    }

    # === NEW SUB-REGION: Tidal Caves (18 rooms) ===

    rooms["stormbreak_tidal_caves_entrance"] = {
        "id": "stormbreak_tidal_caves_entrance",
        "name": "Tidal Caves Entrance",
        "description": "A yawning cave mouth in the western cliffs, half-hidden by curtains of "
                       "hanging seaweed. The tide surges in and out, revealing and concealing the "
                       "entrance on a six-hour cycle. The walls inside are smoothly carved by "
                       "millennia of water action.",
        "coordinates": [cx - 5, cy - 1],
        "location_type": "wilderness",
        "items": {"cave_seaweed": {"quantity": 2, "value": 4}, "tidal_marker_stone": {"quantity": 1, "value": 8}},
        "exits": {
            "east": {"target": "stormbreak_graveyard_below_deck", "type": "direction"},
            "south": {"target": "stormbreak_tidal_caves_passage", "type": "direction"}
        }
    }

    rooms["stormbreak_tidal_caves_passage"] = {
        "id": "stormbreak_tidal_caves_passage",
        "name": "Tidal Passage",
        "description": "A winding passage that plunges deeper into the cliff. Tide marks on the "
                       "walls show water levels at different times — some alarmingly high. "
                       "Phosphorescent algae provides dim greenish light. The sound of dripping "
                       "water echoes endlessly.",
        "coordinates": [cx - 5, cy - 2],
        "location_type": "wilderness",
        "items": {"phosphorescent_algae": {"quantity": 1, "value": 10}},
        "exits": {
            "north": {"target": "stormbreak_tidal_caves_entrance", "type": "direction"},
            "west": {"target": "stormbreak_tidal_caves_pool", "type": "direction"},
            "south": {"target": "stormbreak_tidal_caves_spring", "type": "direction"}
        }
    }

    rooms["stormbreak_tidal_caves_pool"] = {
        "id": "stormbreak_tidal_caves_pool",
        "name": "Still Pool Chamber",
        "description": "A chamber dominated by a perfectly still pool of crystal-clear water. "
                       "The pool is deeper than it appears — seemingly bottomless. Strange shapes "
                       "move in its depths, just at the edge of perception. The surface acts as "
                       "a perfect mirror, reflecting the cave ceiling.",
        "coordinates": [cx - 6, cy - 2],
        "location_type": "wilderness",
        "items": {"mirror_pool_water": {"quantity": 1, "value": 15}, "depth_stone": {"quantity": 1, "value": 18}},
        "exits": {
            "east": {"target": "stormbreak_tidal_caves_passage", "type": "direction"},
            "west": {"target": "stormbreak_tidal_caves_crystal_grotto", "type": "direction"},
            "south": {"target": "stormbreak_tidal_caves_mushroom_chamber", "type": "direction"}
        }
    }

    rooms["stormbreak_tidal_caves_crystal_grotto"] = {
        "id": "stormbreak_tidal_caves_crystal_grotto",
        "name": "Underground Crystal Grotto",
        "description": "A breathtaking cavern where massive crystal formations have grown in "
                       "the mineral-rich water. Amethyst, quartz, and a strange blue mineral "
                       "unique to these caves create a dazzling display. The crystals hum "
                       "faintly, resonating with the island's storm energy.",
        "coordinates": [cx - 7, cy - 2],
        "location_type": "wilderness",
        "items": {"cave_amethyst": {"quantity": 1, "value": 30}, "blue_storm_mineral": {"quantity": 1, "value": 40}},
        "exits": {
            "east": {"target": "stormbreak_tidal_caves_pool", "type": "direction"},
            "south": {"target": "stormbreak_tidal_caves_deep", "type": "direction"},
            "west": {"target": "stormbreak_tidal_caves_ancient_shrine", "type": "direction"}
        }
    }

    rooms["stormbreak_tidal_caves_deep"] = {
        "id": "stormbreak_tidal_caves_deep",
        "name": "Deep Tidal Caves",
        "description": "The caves plunge to their deepest point here, far below sea level. "
                       "The air is thick and warm from geothermal activity. Strange eyeless "
                       "fish swim in the streams, and albino crabs scuttle across rocks. "
                       "The ceiling drips with mineral formations shaped like frozen waterfalls.",
        "coordinates": [cx - 7, cy - 3],
        "location_type": "wilderness",
        "items": {"eyeless_cave_fish": {"quantity": 1, "value": 12}, "mineral_stalactite": {"quantity": 1, "value": 18}},
        "exits": {
            "north": {"target": "stormbreak_tidal_caves_crystal_grotto", "type": "direction"},
            "east": {"target": "stormbreak_tidal_caves_mushroom_chamber", "type": "direction"},
            "west": {"target": "stormbreak_tidal_caves_dripping_hall", "type": "direction"}
        }
    }

    rooms["stormbreak_tidal_caves_mushroom_chamber"] = {
        "id": "stormbreak_tidal_caves_mushroom_chamber",
        "name": "Mushroom Chamber",
        "description": "A warm, humid cavern where giant cave mushrooms grow in profusion. "
                       "Some are taller than a person, their caps glowing with soft purple "
                       "bioluminescence. The air is thick with spores that create a dreamy, "
                       "calming effect. Careful — some species are hallucinogenic.",
        "coordinates": [cx - 6, cy - 3],
        "location_type": "wilderness",
        "items": {"giant_cave_mushroom": {"quantity": 2, "value": 10}, "glowing_mushroom_cap": {"quantity": 1, "value": 22}},
        "exits": {
            "north": {"target": "stormbreak_tidal_caves_pool", "type": "direction"},
            "west": {"target": "stormbreak_tidal_caves_deep", "type": "direction"},
            "south": {"target": "stormbreak_tidal_caves_echo_chamber", "type": "direction"}
        }
    }

    rooms["stormbreak_tidal_caves_spring"] = {
        "id": "stormbreak_tidal_caves_spring",
        "name": "Underground Spring",
        "description": "A freshwater spring bubbles up from deep underground, filling a natural "
                       "basin before flowing away through cracks in the rock. The water is warm "
                       "and mineral-rich, leaving colorful deposits on the surrounding stone. "
                       "Small cave flowers bloom in the moisture.",
        "coordinates": [cx - 5, cy - 3],
        "location_type": "wilderness",
        "items": {"mineral_spring_water": {"quantity": 1, "value": 12}, "cave_flower": {"quantity": 2, "value": 8}},
        "exits": {
            "north": {"target": "stormbreak_tidal_caves_passage", "type": "direction"},
            "south": {"target": "stormbreak_tidal_caves_narrow_squeeze", "type": "direction"},
            "west": {"target": "stormbreak_tidal_caves_mushroom_chamber", "type": "direction"}
        }
    }

    rooms["stormbreak_tidal_caves_narrow_squeeze"] = {
        "id": "stormbreak_tidal_caves_narrow_squeeze",
        "name": "Narrow Squeeze",
        "description": "The passage narrows to barely shoulder-width, forcing travelers to "
                       "squeeze sideways through the gap. The walls are smooth and slippery "
                       "with moisture. Strange scratching sounds come from deeper within — "
                       "perhaps cave crabs, or something less familiar.",
        "coordinates": [cx - 5, cy - 4],
        "location_type": "wilderness",
        "items": {"slippery_stone": {"quantity": 1, "value": 5}},
        "exits": {
            "north": {"target": "stormbreak_tidal_caves_spring", "type": "direction"},
            "west": {"target": "stormbreak_tidal_caves_echo_chamber", "type": "direction"}
        }
    }

    rooms["stormbreak_tidal_caves_echo_chamber"] = {
        "id": "stormbreak_tidal_caves_echo_chamber",
        "name": "Echo Chamber",
        "description": "A perfectly spherical cavern where every sound is amplified and reflected "
                       "a hundred times. Even whispering creates a cacophony. The acoustics are "
                       "so perfect that some believe the chamber was carved deliberately by an "
                       "ancient civilization for ritual purposes.",
        "coordinates": [cx - 6, cy - 4],
        "location_type": "wilderness",
        "items": {"echo_stone": {"quantity": 1, "value": 25}, "resonance_crystal": {"quantity": 1, "value": 20}},
        "exits": {
            "east": {"target": "stormbreak_tidal_caves_narrow_squeeze", "type": "direction"},
            "north": {"target": "stormbreak_tidal_caves_mushroom_chamber", "type": "direction"},
            "west": {"target": "stormbreak_tidal_caves_underground_lake", "type": "direction"}
        }
    }

    rooms["stormbreak_tidal_caves_underground_lake"] = {
        "id": "stormbreak_tidal_caves_underground_lake",
        "name": "Underground Lake",
        "description": "The echo chamber opens onto an underground lake of breathtaking beauty. "
                       "The water is perfectly clear, revealing a sandy bottom dotted with "
                       "glowing crystals. A stone pier extends into the lake, and a small boat "
                       "is tied to its end — left by some previous explorer.",
        "coordinates": [cx - 7, cy - 4],
        "location_type": "wilderness",
        "items": {"underwater_crystal": {"quantity": 1, "value": 35}, "abandoned_oar": {"quantity": 1, "value": 8}},
        "exits": {
            "east": {"target": "stormbreak_tidal_caves_echo_chamber", "type": "direction"},
            "north": {"target": "stormbreak_tidal_caves_deep", "type": "direction"},
            "west": {"target": "stormbreak_tidal_caves_fossil_wall", "type": "direction"}
        }
    }

    rooms["stormbreak_tidal_caves_fossil_wall"] = {
        "id": "stormbreak_tidal_caves_fossil_wall",
        "name": "Fossil Wall",
        "description": "An exposed cliff face within the cave reveals thousands of ancient "
                       "fossils — sea creatures from an age before the eternal storm. Giant "
                       "ammonites, prehistoric fish, and creatures with no modern equivalent "
                       "are preserved in exquisite detail in the stone.",
        "coordinates": [cx - 8, cy - 4],
        "location_type": "wilderness",
        "items": {"ancient_ammonite_fossil": {"quantity": 1, "value": 30}, "prehistoric_fish_fossil": {"quantity": 1, "value": 22}},
        "exits": {
            "east": {"target": "stormbreak_tidal_caves_underground_lake", "type": "direction"},
            "north": {"target": "stormbreak_tidal_caves_dripping_hall", "type": "direction"}
        }
    }

    rooms["stormbreak_tidal_caves_dripping_hall"] = {
        "id": "stormbreak_tidal_caves_dripping_hall",
        "name": "Dripping Hall",
        "description": "A long gallery where water drips from thousands of stalactites in a "
                       "never-ending rain. Over eons, the drops have carved perfect bowls into "
                       "the floor, each filled with mineral-rich water of a different color. "
                       "The sound is strangely musical, like a natural rain-stick orchestra.",
        "coordinates": [cx - 8, cy - 3],
        "location_type": "wilderness",
        "items": {"colored_mineral_water": {"quantity": 2, "value": 10}, "musical_stalactite": {"quantity": 1, "value": 18}},
        "exits": {
            "south": {"target": "stormbreak_tidal_caves_fossil_wall", "type": "direction"},
            "north": {"target": "stormbreak_tidal_caves_ancient_shrine", "type": "direction"}
        }
    }

    rooms["stormbreak_tidal_caves_ancient_shrine"] = {
        "id": "stormbreak_tidal_caves_ancient_shrine",
        "name": "Ancient Tidal Shrine",
        "description": "Deep within the caves, an ancient shrine carved from the living rock "
                       "honors some forgotten deity of the tides. The altar is adorned with "
                       "shells and pearl offerings that glow with inner light. Water flows "
                       "around the shrine in channels that form a perfect spiral pattern.",
        "coordinates": [cx - 8, cy - 2],
        "location_type": "wilderness",
        "items": {"tidal_shrine_blessing": {"quantity": 1, "value": 40}, "spiral_shell_offering": {"quantity": 1, "value": 25}},
        "exits": {
            "south": {"target": "stormbreak_tidal_caves_dripping_hall", "type": "direction"},
            "east": {"target": "stormbreak_tidal_caves_crystal_grotto", "type": "direction"},
            "north": {"target": "stormbreak_tidal_caves_bioluminescent", "type": "direction"}
        }
    }

    rooms["stormbreak_tidal_caves_bioluminescent"] = {
        "id": "stormbreak_tidal_caves_bioluminescent",
        "name": "Bioluminescent Gallery",
        "description": "A passage where every surface is coated with bioluminescent organisms. "
                       "The walls glow in waves of blue, green, and purple, responding to sound "
                       "and movement. Walking through feels like moving through a living aurora. "
                       "The beauty is otherworldly and humbling.",
        "coordinates": [cx - 8, cy - 1],
        "location_type": "wilderness",
        "items": {"bioluminescent_sample": {"quantity": 1, "value": 20}, "living_light_vial": {"quantity": 1, "value": 28}},
        "exits": {
            "south": {"target": "stormbreak_tidal_caves_ancient_shrine", "type": "direction"},
            "north": {"target": "stormbreak_tidal_caves_hermit", "type": "direction"}
        }
    }

    rooms["stormbreak_tidal_caves_hermit"] = {
        "id": "stormbreak_tidal_caves_hermit",
        "name": "Hermit's Refuge",
        "description": "A surprisingly comfortable cave dwelling where a hermit has made their "
                       "home for decades. Woven mats, drying herbs, and a small library of "
                       "hand-copied books fill the space. The hermit claims to hear the voice "
                       "of the storm and records its messages in coded journals.",
        "coordinates": [cx - 8, cy],
        "location_type": "settlement",
        "items": {"hermit_coded_journal": {"quantity": 1, "value": 35}, "cave_herb_bundle": {"quantity": 2, "value": 8}},
        "exits": {
            "south": {"target": "stormbreak_tidal_caves_bioluminescent", "type": "direction"},
            "east": {"target": "stormbreak_tidal_caves_treasure", "type": "direction"}
        }
    }

    rooms["stormbreak_tidal_caves_treasure"] = {
        "id": "stormbreak_tidal_caves_treasure",
        "name": "Hidden Treasure Chamber",
        "description": "The deepest and most secret chamber of the tidal caves. Behind a "
                       "waterfall of underground water, a natural vault holds treasures "
                       "accumulated over centuries — pirate gold, storm crystals, and artifacts "
                       "from civilizations lost to the eternal tempest.",
        "coordinates": [cx - 7, cy],
        "location_type": "wilderness",
        "items": {"pirate_gold_hoard": {"quantity": 1, "value": 75}, "lost_civilization_artifact": {"quantity": 1, "value": 60}},
        "exits": {
            "west": {"target": "stormbreak_tidal_caves_hermit", "type": "direction"}
        }
    }

    # === NEW SUB-REGION: Maelstrom Overlook (10 rooms) ===

    rooms["stormbreak_maelstrom_path"] = {
        "id": "stormbreak_maelstrom_path",
        "name": "Maelstrom Path",
        "description": "Beyond the storm nexus, a path of solidified lightning energy leads "
                       "north toward an area of impossible meteorological activity. The wind "
                       "here changes direction every few seconds, and rain falls upward as "
                       "often as down. Each step forward requires fighting the chaotic gales.",
        "coordinates": [cx + 2, cy + 14],
        "location_type": "wilderness",
        "items": {"chaos_wind_sample": {"quantity": 1, "value": 20}},
        "exits": {
            "south": {"target": "stormbreak_spire_storm_nexus", "type": "direction"},
            "east": {"target": "stormbreak_maelstrom_ridge", "type": "direction"},
            "west": {"target": "stormbreak_maelstrom_storm_garden", "type": "direction"},
            "north": {"target": "stormbreak_maelstrom_overlook", "type": "direction"}
        }
    }

    rooms["stormbreak_maelstrom_ridge"] = {
        "id": "stormbreak_maelstrom_ridge",
        "name": "Maelstrom Ridge",
        "description": "A razor-thin ridge of volcanic rock overlooking the maelstrom below. "
                       "From here you can see the ocean churning in an enormous whirlpool, "
                       "its eye glowing with eerie green light. Ships caught in its pull are "
                       "dragged down in minutes — their wreckage never seen again.",
        "coordinates": [cx + 3, cy + 14],
        "location_type": "wilderness",
        "items": {"maelstrom_fragment": {"quantity": 1, "value": 30}},
        "exits": {
            "west": {"target": "stormbreak_maelstrom_path", "type": "direction"},
            "north": {"target": "stormbreak_maelstrom_viewpoint", "type": "direction"},
            "east": {"target": "stormbreak_maelstrom_watchtower", "type": "direction"}
        }
    }

    rooms["stormbreak_maelstrom_viewpoint"] = {
        "id": "stormbreak_maelstrom_viewpoint",
        "name": "Maelstrom Viewpoint",
        "description": "The best vantage point to observe the great maelstrom. An abandoned "
                       "research station clings to the cliff edge, its instruments still "
                       "recording data. Notebooks left behind describe the maelstrom as a "
                       "'wound in the ocean' that has been spinning since before recorded history.",
        "coordinates": [cx + 3, cy + 15],
        "location_type": "wilderness",
        "items": {"maelstrom_research_notes": {"quantity": 1, "value": 25}, "oceanographic_instrument": {"quantity": 1, "value": 30}},
        "exits": {
            "south": {"target": "stormbreak_maelstrom_ridge", "type": "direction"},
            "west": {"target": "stormbreak_maelstrom_overlook", "type": "direction"},
            "east": {"target": "stormbreak_maelstrom_crystal_field", "type": "direction"}
        }
    }

    rooms["stormbreak_maelstrom_overlook"] = {
        "id": "stormbreak_maelstrom_overlook",
        "name": "The Maelstrom Overlook",
        "description": "A broad platform of volcanic glass directly above the maelstrom's center. "
                       "The ground vibrates with the whirlpool's rotation, and spray from below "
                       "creates a permanent rainbow even in the storm's darkness. This is the "
                       "most awe-inspiring and terrifying vista on the island.",
        "coordinates": [cx + 2, cy + 15],
        "location_type": "wilderness",
        "items": {"maelstrom_glass": {"quantity": 1, "value": 45}, "storm_rainbow_prism": {"quantity": 1, "value": 35}},
        "exits": {
            "south": {"target": "stormbreak_maelstrom_path", "type": "direction"},
            "east": {"target": "stormbreak_maelstrom_viewpoint", "type": "direction"},
            "west": {"target": "stormbreak_maelstrom_vortex_edge", "type": "direction"},
            "north": {"target": "stormbreak_maelstrom_wind_tunnel", "type": "direction"}
        }
    }

    rooms["stormbreak_maelstrom_vortex_edge"] = {
        "id": "stormbreak_maelstrom_vortex_edge",
        "name": "Vortex Edge",
        "description": "The very edge of the cliff where the maelstrom's updraft meets the "
                       "storm's downdraft. The collision creates a wall of violent turbulence. "
                       "Objects thrown into the vortex are flung in random directions. Ancient "
                       "chains embedded in the rock suggest someone once tried to anchor "
                       "something here.",
        "coordinates": [cx + 1, cy + 15],
        "location_type": "wilderness",
        "items": {"vortex_chain_link": {"quantity": 1, "value": 15}, "turbulence_crystal": {"quantity": 1, "value": 30}},
        "exits": {
            "east": {"target": "stormbreak_maelstrom_overlook", "type": "direction"},
            "south": {"target": "stormbreak_maelstrom_storm_garden", "type": "direction"}
        }
    }

    rooms["stormbreak_maelstrom_storm_garden"] = {
        "id": "stormbreak_maelstrom_storm_garden",
        "name": "Storm Garden",
        "description": "Against all odds, a garden thrives at the edge of the maelstrom. "
                       "Plants here have evolved to feed on storm energy rather than sunlight. "
                       "Electric flowers bloom in crackling displays, and vine-like conductors "
                       "channel lightning into the soil. A reclusive gardener tends this "
                       "impossible Eden.",
        "coordinates": [cx + 1, cy + 14],
        "location_type": "wilderness",
        "items": {"electric_bloom": {"quantity": 2, "value": 18}, "storm_vine_cutting": {"quantity": 1, "value": 22}},
        "exits": {
            "east": {"target": "stormbreak_maelstrom_path", "type": "direction"},
            "north": {"target": "stormbreak_maelstrom_vortex_edge", "type": "direction"}
        }
    }

    rooms["stormbreak_maelstrom_watchtower"] = {
        "id": "stormbreak_maelstrom_watchtower",
        "name": "Maelstrom Watchtower",
        "description": "A ruined watchtower from an era when someone attempted to study and "
                       "control the maelstrom. Its upper floors have been sheared off by wind, "
                       "but the base remains solid. Inside, ancient machinery of unknown purpose "
                       "still ticks and whirs, powered by the ambient storm energy.",
        "coordinates": [cx + 4, cy + 14],
        "location_type": "building",
        "items": {"ancient_storm_gear": {"quantity": 1, "value": 30}, "maelstrom_control_fragment": {"quantity": 1, "value": 40}},
        "exits": {
            "west": {"target": "stormbreak_maelstrom_ridge", "type": "direction"},
            "north": {"target": "stormbreak_maelstrom_crystal_field", "type": "direction"}
        }
    }

    rooms["stormbreak_maelstrom_crystal_field"] = {
        "id": "stormbreak_maelstrom_crystal_field",
        "name": "Crystal Field",
        "description": "A field of storm crystals that have grown naturally in the extreme "
                       "conditions near the maelstrom. The crystals range from palm-sized to "
                       "taller than a person, arranged in concentric circles around a central "
                       "formation. They pulse with light in a rhythm that matches the "
                       "maelstrom's rotation.",
        "coordinates": [cx + 4, cy + 15],
        "location_type": "wilderness",
        "items": {"maelstrom_crystal": {"quantity": 1, "value": 55}, "pulsing_storm_geode": {"quantity": 1, "value": 35}},
        "exits": {
            "west": {"target": "stormbreak_maelstrom_viewpoint", "type": "direction"},
            "south": {"target": "stormbreak_maelstrom_watchtower", "type": "direction"}
        }
    }

    rooms["stormbreak_maelstrom_wind_tunnel"] = {
        "id": "stormbreak_maelstrom_wind_tunnel",
        "name": "Wind Tunnel",
        "description": "A natural tunnel through the rock where wind accelerates to incredible "
                       "speeds. The tunnel creates a sustained roar that can be heard for miles. "
                       "At intervals, the wind reverses direction without warning. Ropes along "
                       "the walls provide handholds for the brave or foolish.",
        "coordinates": [cx + 3, cy + 16],
        "location_type": "wilderness",
        "items": {"wind_tunnel_stone": {"quantity": 1, "value": 15}, "gale_rope": {"quantity": 1, "value": 10}},
        "exits": {
            "south": {"target": "stormbreak_maelstrom_viewpoint", "type": "direction"},
            "west": {"target": "stormbreak_maelstrom_eye", "type": "direction"}
        }
    }

    rooms["stormbreak_maelstrom_eye"] = {
        "id": "stormbreak_maelstrom_eye",
        "name": "Eye of the Maelstrom",
        "description": "The final, impossible destination — a platform suspended directly above "
                       "the maelstrom's eye. The water spirals hundreds of feet below, glowing "
                       "with an otherworldly green light. The air here is perfectly still and "
                       "warm, a pocket of impossible calm. In the center, a pedestal of pure "
                       "storm crystal holds an artifact of immense power.",
        "coordinates": [cx + 2, cy + 16],
        "location_type": "wilderness",
        "items": {"maelstrom_eye_crystal": {"quantity": 1, "value": 100}, "storm_sovereign_token": {"quantity": 1, "value": 80}},
        "exits": {
            "east": {"target": "stormbreak_maelstrom_wind_tunnel", "type": "direction"},
            "south": {"target": "stormbreak_maelstrom_overlook", "type": "direction"}
        }
    }


def generate_cinderforge_island(rooms):
    """Generate Island 4: Cinderforge Isle - Volcanic forges and obsidian wastes (~75 rooms)."""

    cx, cy = -50, 30  # Center coordinates

    # =========================================================================
    # CINDERFORGE ISLE - Volcanic Island (Level 20+)
    # Sub-regions: Docks, Cinder Village, Lava Fields, Obsidian Canyons,
    #              Ancient Forges, Ash Wastes, Volcano Core, Slag Pits
    # =========================================================================

    # --- Cinderforge Docks (3 rooms) ---

    rooms["cinder_docks"] = {
        "id": "cinder_docks",
        "name": "Cinderforge Isle - Ember Dock",
        "description": "A dock of heat-blackened basalt juts into steaming waters that bubble with "
                       "volcanic vents. The air shimmers with intense heat and the stone itself is "
                       "warm underfoot. Ash drifts like grey snow from a sky stained orange by the "
                       "distant volcano's glow.",
        "coordinates": [cx, cy - 4],
        "location_type": "dock",
        "items": {},
        "exits": {
            "board mainland": {
                "target": "harbor_east_dock",
                "type": "boat_travel",
                "island_id": "cinderforge_isle",
                "display": "Return to Grand Harbor",
                "unlock_cost": 0,
                "fare_cost": 0,
                "min_level": 1,
                "transition_text": "You board the fireproof vessel. The crew douses the hull with seawater\nas the ship pulls away from the smouldering dock. The volcanic glow\nfades behind you, and after five days the calm waters of Grand Harbor\nwelcome you home..."
            },
            "north": {"target": "cinder_docks_cargo", "type": "direction"},
            "east": {"target": "cinder_docks_beacon", "type": "direction"}
        }
    }

    rooms["cinder_docks_cargo"] = {
        "id": "cinder_docks_cargo",
        "name": "Fireproof Cargo Hold",
        "description": "A squat warehouse built from double-thick basalt blocks lined with asbesite mortar. "
                       "Crates of obsidian ingots, fire-resistant cloth, and sealed barrels of volcanic "
                       "mineral water are stacked on iron shelving. The floor is warm to the touch.",
        "coordinates": [cx, cy - 3],
        "location_type": "dock",
        "items": {"fire_resistant_cloth": {"quantity": 2, "value": 18}, "volcanic_mineral_water": {"quantity": 1, "value": 12}},
        "exits": {
            "south": {"target": "cinder_docks", "type": "direction"},
            "north": {"target": "cinder_village_path", "type": "direction"}
        }
    }

    rooms["cinder_docks_beacon"] = {
        "id": "cinder_docks_beacon",
        "name": "Fire Beacon Tower",
        "description": "A tall tower of black iron and volcanic stone, topped with a brazier of "
                       "ever-burning magma crystal. The beacon guides ships through the ash-choked "
                       "waters surrounding the island. From the top you can see the volcano's "
                       "glowing caldera dominating the island interior.",
        "coordinates": [cx + 1, cy - 4],
        "location_type": "building",
        "items": {"magma_crystal_shard": {"quantity": 1, "value": 25}},
        "exits": {
            "west": {"target": "cinder_docks", "type": "direction"},
            "east": {"target": "cinder_docks_watchtower", "type": "direction"}
        }
    }

    # --- Cinder Village (15 rooms) ---

    rooms["cinder_village_path"] = {
        "id": "cinder_village_path",
        "name": "Scorched Path to Village",
        "description": "A road of fused volcanic glass winds uphill from the docks through fields "
                       "of hardened lava. Heat-tolerant scrub and fire ferns line the path. The air "
                       "tastes of sulfur and cinders crunch underfoot with every step.",
        "coordinates": [cx, cy - 2],
        "location_type": "wilderness",
        "items": {},
        "exits": {
            "south": {"target": "cinder_docks_cargo", "type": "direction"},
            "north": {"target": "cinder_village_gate", "type": "direction"}
        }
    }

    rooms["cinder_village_gate"] = {
        "id": "cinder_village_gate",
        "name": "Cinder Village Gate",
        "description": "A massive gate of riveted iron and obsidian blocks guards the entrance to "
                       "Cinder Village. Dwarven runes of protection glow faintly along the archway, "
                       "warding against lava surges. Guards in heat-treated armour nod as you pass.",
        "coordinates": [cx, cy - 1],
        "location_type": "settlement",
        "items": {},
        "exits": {
            "south": {"target": "cinder_village_path", "type": "direction"},
            "north": {"target": "cinder_village_center", "type": "direction"},
            "east": {"target": "cinder_village_barracks", "type": "direction"},
            "west": {"target": "cinder_village_stable", "type": "direction"}
        }
    }

    rooms["cinder_village_center"] = {
        "id": "cinder_village_center",
        "name": "Cinder Village - Central Square",
        "description": "The heart of Cinder Village is a wide plaza paved with hexagonal basalt tiles. "
                       "A fountain of cooled lava stands in the centre, now flowing with fresh water "
                       "pumped from deep artesian wells. Volcanic stone buildings surround the square, "
                       "their windows glowing with forge-light.",
        "coordinates": [cx, cy],
        "location_type": "settlement",
        "items": {},
        "exits": {
            "south": {"target": "cinder_village_gate", "type": "direction"},
            "north": {"target": "cinder_village_elder", "type": "direction"},
            "east": {"target": "cinder_village_market", "type": "direction"},
            "west": {"target": "cinder_village_inn", "type": "direction"},
            "northeast": {"target": "cinder_village_smithy", "type": "direction"},
            "northwest": {"target": "cinder_village_shrine", "type": "direction"}
        }
    }

    rooms["cinder_village_elder"] = {
        "id": "cinder_village_elder",
        "name": "Elder's Hall",
        "description": "A domed hall of polished obsidian where the village elder holds council. "
                       "Tapestries woven with fire-silk depict the island's history — the great eruption, "
                       "the arrival of the dwarven forge-masters, and the founding of the village. "
                       "A throne of cooled magma sits on a raised dais.",
        "coordinates": [cx, cy + 1],
        "location_type": "building",
        "npcs": ["cinder_elder"],
        "items": {"fire_silk_tapestry_scrap": {"quantity": 1, "value": 30}},
        "exits": {
            "south": {"target": "cinder_village_center", "type": "direction"},
            "east": {"target": "cinder_village_library", "type": "direction"},
            "north": {"target": "cinder_village_overlook", "type": "direction"}
        }
    }

    rooms["cinder_village_library"] = {
        "id": "cinder_village_library",
        "name": "Ashen Archive",
        "description": "A library built into a natural lava tube, its shelves carved directly from "
                       "the stone walls. Books here are bound in fire-resistant dragon-leather and "
                       "the pages are thin sheets of hammered copper. Dwarven scholars study ancient "
                       "forge techniques by the light of magma lamps.",
        "coordinates": [cx + 1, cy + 1],
        "location_type": "building",
        "items": {"copper_page_scroll": {"quantity": 1, "value": 20}, "forge_technique_manual": {"quantity": 1, "value": 35}},
        "exits": {
            "west": {"target": "cinder_village_elder", "type": "direction"}
        }
    }

    rooms["cinder_village_overlook"] = {
        "id": "cinder_village_overlook",
        "name": "Village Overlook",
        "description": "A stone terrace at the highest point of the village offering a panoramic view "
                       "of the island. To the north, lava fields glow orange beneath pillars of smoke. "
                       "East lie the obsidian canyons, glinting like dark mirrors. The volcano's peak "
                       "looms above everything, trailing a banner of ash.",
        "coordinates": [cx, cy + 2],
        "location_type": "settlement",
        "items": {},
        "exits": {
            "south": {"target": "cinder_village_elder", "type": "direction"},
            "north": {"target": "cinder_lava_edge", "type": "direction"},
            "east": {"target": "cinder_obsidian_rim", "type": "direction"},
            "west": {"target": "cinder_ash_border", "type": "direction"}
        }
    }

    rooms["cinder_village_market"] = {
        "id": "cinder_village_market",
        "name": "Cinder Market",
        "description": "An open-air market sheltered under iron-framed canopies of fire-proof canvas. "
                       "Vendors sell obsidian tools, volcanic spices, heat salves, and ingots of rare "
                       "metals pulled from the earth. The haggling is loud and the air smells of "
                       "roasted sulfur-nuts and smoked fish.",
        "coordinates": [cx + 1, cy],
        "location_type": "settlement",
        "shop": True,
        "items": {"heat_salve": {"quantity": 3, "value": 15}, "volcanic_spice_pouch": {"quantity": 2, "value": 10}},
        "exits": {
            "west": {"target": "cinder_village_center", "type": "direction"},
            "east": {"target": "cinder_village_apothecary", "type": "direction"}
        }
    }

    rooms["cinder_village_apothecary"] = {
        "id": "cinder_village_apothecary",
        "name": "Ember Apothecary",
        "description": "A narrow shop crammed with shelves of bubbling phials and jars of crystallised "
                       "minerals. The apothecary — a wizened woman with soot-stained hands — brews "
                       "potions using volcanic reagents. Fire-resistance draughts are her specialty.",
        "coordinates": [cx + 2, cy],
        "location_type": "building",
        "items": {"fire_resistance_draught": {"quantity": 2, "value": 25}, "volcanic_salts": {"quantity": 1, "value": 12}},
        "exits": {
            "west": {"target": "cinder_village_market", "type": "direction"}
        }
    }

    rooms["cinder_village_inn"] = {
        "id": "cinder_village_inn",
        "name": "The Molten Hearth Inn",
        "description": "A sturdy inn built around a natural hot spring. Rooms are warm but comfortable, "
                       "heated from below by geothermal vents. The common room serves spiced magma-ale "
                       "and chargrilled ash-boar. Travellers and forge-workers relax in the steaming pools.",
        "coordinates": [cx - 1, cy],
        "location_type": "building",
        "items": {"magma_ale": {"quantity": 2, "value": 8}, "chargrilled_ash_boar": {"quantity": 1, "value": 14}},
        "exits": {
            "east": {"target": "cinder_village_center", "type": "direction"},
            "west": {"target": "cinder_village_healer", "type": "direction"},
            "upstairs": {"target": "cinder_village_inn_room", "type": "named", "display": "Inn Room"}
        }
    }

    rooms["cinder_village_inn_room"] = {
        "id": "cinder_village_inn_room",
        "name": "Molten Hearth - Guest Room",
        "description": "A small stone-walled room with a bed of woven fire-fern fronds. A window "
                       "of smoked glass looks out over the glowing lava fields. The floor is "
                       "pleasantly warm from the geothermal vents below.",
        "coordinates": [cx - 1, cy + 1],
        "location_type": "building",
        "items": {},
        "exits": {
            "downstairs": {"target": "cinder_village_inn", "type": "named", "display": "Back to Inn"}
        }
    }

    rooms["cinder_village_smithy"] = {
        "id": "cinder_village_smithy",
        "name": "Ironvein Smithy",
        "description": "A master forge run by a dwarven smith whose family has worked this island's "
                       "metals for generations. The anvil glows red-hot without a fire — it sits above "
                       "a natural magma vent. Weapons and armour of extraordinary quality line the walls.",
        "coordinates": [cx + 1, cy + 1],
        "location_type": "building",
        "items": {"obsidian_dagger": {"quantity": 1, "value": 40}, "volcanic_steel_ingot": {"quantity": 1, "value": 30}},
        "exits": {
            "southwest": {"target": "cinder_village_center", "type": "direction"}
        }
    }

    rooms["cinder_village_shrine"] = {
        "id": "cinder_village_shrine",
        "name": "Shrine of the Ember God",
        "description": "A small temple hewn from a single block of red obsidian. An eternal flame "
                       "burns on the altar, fed by a natural gas vent. Offerings of polished "
                       "volcanic glass and fire opals surround the flame. Pilgrims whisper prayers "
                       "to the Ember God for protection from eruptions.",
        "coordinates": [cx - 1, cy + 1],
        "location_type": "building",
        "items": {"fire_opal_offering": {"quantity": 1, "value": 35}},
        "exits": {
            "southeast": {"target": "cinder_village_center", "type": "direction"}
        }
    }

    rooms["cinder_village_healer"] = {
        "id": "cinder_village_healer",
        "name": "Ashweaver's Clinic",
        "description": "A low stone building where the village healer treats burns, smoke inhalation, "
                       "and the strange fevers that come from prolonged exposure to volcanic fumes. "
                       "Bundles of heat-resistant medicinal moss hang from the ceiling. A basin of "
                       "cooled mineral water stands ready for emergencies.",
        "coordinates": [cx - 2, cy],
        "location_type": "building",
        "items": {"medicinal_ash_moss": {"quantity": 2, "value": 15}, "cooling_salve": {"quantity": 1, "value": 20}},
        "exits": {
            "east": {"target": "cinder_village_inn", "type": "direction"},
            "west": {"target": "cinder_village_herb_garden", "type": "direction"}
        }
    }

    rooms["cinder_village_barracks"] = {
        "id": "cinder_village_barracks",
        "name": "Ember Guard Barracks",
        "description": "The garrison of the Ember Guard — soldiers trained to fight in extreme heat "
                       "and volcanic terrain. Their armour is forged from a special heat-dispersing "
                       "alloy. Weapon racks hold obsidian-tipped spears and shields coated in "
                       "fireite enamel.",
        "coordinates": [cx + 1, cy - 1],
        "location_type": "building",
        "items": {"obsidian_spear_tip": {"quantity": 1, "value": 22}},
        "exits": {
            "west": {"target": "cinder_village_gate", "type": "direction"},
            "east": {"target": "cinder_village_training_ground", "type": "direction"}
        }
    }

    rooms["cinder_village_stable"] = {
        "id": "cinder_village_stable",
        "name": "Firedrake Stable",
        "description": "A cavernous stable where the villagers keep domesticated firedrakes — "
                       "small, lizard-like creatures used as pack animals. Their scales shimmer "
                       "with residual heat and they snort little plumes of smoke. The stable is "
                       "built over a warm vent to keep them comfortable.",
        "coordinates": [cx - 1, cy - 1],
        "location_type": "building",
        "items": {"firedrake_scale": {"quantity": 2, "value": 18}},
        "exits": {
            "east": {"target": "cinder_village_gate", "type": "direction"}
        }
    }

    # --- Lava Fields (12 rooms) ---

    rooms["cinder_lava_edge"] = {
        "id": "cinder_lava_edge",
        "name": "Lava Field Edge",
        "description": "The village ends abruptly where the living rock begins. Ahead, a vast field "
                       "of cooling lava stretches toward the volcano. Rivers of molten orange cut "
                       "through crusts of black stone. The heat is staggering and the air dances "
                       "with thermal distortions.",
        "coordinates": [cx, cy + 3],
        "location_type": "wilderness",
        "items": {},
        "exits": {
            "south": {"target": "cinder_village_overlook", "type": "direction"},
            "north": {"target": "cinder_lava_river_bank", "type": "direction"},
            "east": {"target": "cinder_lava_cooling_shelf", "type": "direction"},
            "west": {"target": "cinder_lava_steam_vent", "type": "direction"}
        }
    }

    rooms["cinder_lava_river_bank"] = {
        "id": "cinder_lava_river_bank",
        "name": "Magma River Bank",
        "description": "You stand on a ridge of solidified lava overlooking a slow-moving river of "
                       "molten rock. The magma glows a deep cherry-red, its surface crusting over "
                       "before cracking apart to reveal fresh orange beneath. The heat radiates "
                       "upward in visible waves.",
        "coordinates": [cx, cy + 4],
        "location_type": "wilderness",
        "items": {"cooled_magma_chunk": {"quantity": 2, "value": 10}},
        "exits": {
            "south": {"target": "cinder_lava_edge", "type": "direction"},
            "north": {"target": "cinder_lava_crossing", "type": "direction"},
            "east": {"target": "cinder_lava_fire_geyser", "type": "direction"}
        }
    }

    rooms["cinder_lava_cooling_shelf"] = {
        "id": "cinder_lava_cooling_shelf",
        "name": "Cooling Lava Shelf",
        "description": "A broad shelf of recently cooled lava, its surface wrinkled like frozen fabric. "
                       "Cracks glow orange beneath your feet, and small jets of superheated gas hiss "
                       "from fissures. Mineral crystals have formed in the cooling pockets, glittering "
                       "like embedded jewels.",
        "coordinates": [cx + 1, cy + 3],
        "location_type": "wilderness",
        "items": {"volcanic_crystal": {"quantity": 1, "value": 22}, "sulfur_chunk": {"quantity": 2, "value": 8}},
        "exits": {
            "west": {"target": "cinder_lava_edge", "type": "direction"},
            "north": {"target": "cinder_lava_fire_geyser", "type": "direction"}
        }
    }

    rooms["cinder_lava_fire_geyser"] = {
        "id": "cinder_lava_fire_geyser",
        "name": "Fire Geyser Field",
        "description": "Columns of superheated steam and fire blast skyward at irregular intervals "
                       "from vents in the volcanic crust. The ground trembles constantly and a deep "
                       "rumbling echoes from below. The geysers leave behind rings of crystallised "
                       "minerals in brilliant oranges and yellows.",
        "coordinates": [cx + 1, cy + 4],
        "location_type": "wilderness",
        "items": {"geyser_crystal_ring": {"quantity": 1, "value": 28}},
        "exits": {
            "south": {"target": "cinder_lava_cooling_shelf", "type": "direction"},
            "west": {"target": "cinder_lava_river_bank", "type": "direction"},
            "north": {"target": "cinder_lava_pillars", "type": "direction"}
        }
    }

    rooms["cinder_lava_steam_vent"] = {
        "id": "cinder_lava_steam_vent",
        "name": "Steam Vent Cluster",
        "description": "A cluster of massive steam vents roars like a chorus of angry dragons. "
                       "Plumes of white-hot vapour shoot thirty feet into the air, obscuring vision "
                       "and drenching everything in mineral-laden moisture. The ground is slick "
                       "with condensed volcanic minerals.",
        "coordinates": [cx - 1, cy + 3],
        "location_type": "wilderness",
        "items": {"condensed_mineral_deposit": {"quantity": 1, "value": 15}},
        "exits": {
            "east": {"target": "cinder_lava_edge", "type": "direction"},
            "north": {"target": "cinder_lava_bubble_pool", "type": "direction"}
        }
    }

    rooms["cinder_lava_bubble_pool"] = {
        "id": "cinder_lava_bubble_pool",
        "name": "Bubbling Lava Pools",
        "description": "Several pools of sluggish lava bubble and pop like thick porridge. Each "
                       "burst sends tiny globules of molten rock arcing through the air in glowing "
                       "parabolas. The pools are rimmed with colourful mineral crusts — bright "
                       "yellows, deep reds, and shimmering copper-greens.",
        "coordinates": [cx - 1, cy + 4],
        "location_type": "wilderness",
        "items": {"lava_glass_bead": {"quantity": 3, "value": 12}},
        "exits": {
            "south": {"target": "cinder_lava_steam_vent", "type": "direction"},
            "east": {"target": "cinder_lava_crossing", "type": "direction"},
            "north": {"target": "cinder_lava_charred_grove", "type": "direction"}
        }
    }

    rooms["cinder_lava_crossing"] = {
        "id": "cinder_lava_crossing",
        "name": "Lava Flow Crossing",
        "description": "A precarious path of cooled lava pillars forms a natural bridge across a "
                       "wide magma channel. Each pillar is barely wide enough to stand on, and the "
                       "molten river below casts an eerie upward glow. One misstep would be fatal.",
        "coordinates": [cx, cy + 5],
        "location_type": "wilderness",
        "items": {},
        "exits": {
            "south": {"target": "cinder_lava_river_bank", "type": "direction"},
            "west": {"target": "cinder_lava_bubble_pool", "type": "direction"},
            "north": {"target": "cinder_lava_plateau", "type": "direction"},
            "east": {"target": "cinder_lava_pillars", "type": "direction"}
        }
    }

    rooms["cinder_lava_pillars"] = {
        "id": "cinder_lava_pillars",
        "name": "Basalt Pillar Forest",
        "description": "Dozens of hexagonal basalt columns rise from the lava field like stone "
                       "trees. Some tower fifty feet high, their tops flat enough to stand on. "
                       "Lava flows between them in slow orange rivers. The columns ring with a "
                       "low harmonic tone as heat expands the stone.",
        "coordinates": [cx + 1, cy + 5],
        "location_type": "wilderness",
        "items": {"basalt_column_chip": {"quantity": 1, "value": 10}},
        "exits": {
            "south": {"target": "cinder_lava_fire_geyser", "type": "direction"},
            "west": {"target": "cinder_lava_crossing", "type": "direction"},
            "north": {"target": "cinder_lava_scorched_ridge", "type": "direction"}
        }
    }

    rooms["cinder_lava_charred_grove"] = {
        "id": "cinder_lava_charred_grove",
        "name": "Charred Grove",
        "description": "The petrified remains of a forest consumed by an ancient eruption. Trees of "
                       "solid stone stand frozen mid-combustion, their bark replaced by volcanic glass. "
                       "Between them, small fire-ferns have colonised the ash, their fronds glowing "
                       "faintly with absorbed geothermal heat.",
        "coordinates": [cx - 1, cy + 5],
        "location_type": "wilderness",
        "items": {"petrified_wood": {"quantity": 1, "value": 18}, "fire_fern_frond": {"quantity": 2, "value": 8}},
        "exits": {
            "south": {"target": "cinder_lava_bubble_pool", "type": "direction"},
            "west": {"target": "cinder_lava_deadwood", "type": "direction"}
        }
    }

    rooms["cinder_lava_plateau"] = {
        "id": "cinder_lava_plateau",
        "name": "Ember Plateau",
        "description": "A high flat expanse of solidified lava offers a commanding view of the lava "
                       "fields spreading south and the volcano's slope rising to the north. Embers "
                       "drift on updrafts and the stone still radiates warmth from deep below. "
                       "Ancient dwarven trail-markers point toward the forge district.",
        "coordinates": [cx, cy + 6],
        "location_type": "wilderness",
        "items": {"dwarven_trail_marker": {"quantity": 1, "value": 14}},
        "exits": {
            "south": {"target": "cinder_lava_crossing", "type": "direction"},
            "north": {"target": "cinder_forge_gate", "type": "direction"},
            "east": {"target": "cinder_lava_scorched_ridge", "type": "direction"}
        }
    }

    rooms["cinder_lava_scorched_ridge"] = {
        "id": "cinder_lava_scorched_ridge",
        "name": "Scorched Ridge",
        "description": "A jagged ridge of fused rock marks the boundary between the lava fields and "
                       "the obsidian canyons. The rock here is a swirl of black glass and red stone, "
                       "twisted by unimaginable heat. The ridge offers a narrow but passable route "
                       "between the two regions.",
        "coordinates": [cx + 1, cy + 6],
        "location_type": "wilderness",
        "items": {"fused_glass_shard": {"quantity": 1, "value": 16}},
        "exits": {
            "south": {"target": "cinder_lava_pillars", "type": "direction"},
            "west": {"target": "cinder_lava_plateau", "type": "direction"},
            "east": {"target": "cinder_obsidian_entrance", "type": "direction"},
            "north": {"target": "cinder_lava_uplands", "type": "direction"}
        }
    }

    # --- Obsidian Canyons (10 rooms) ---

    rooms["cinder_obsidian_rim"] = {
        "id": "cinder_obsidian_rim",
        "name": "Obsidian Canyon Rim",
        "description": "The ground drops away sharply into a canyon of pure obsidian. The walls "
                       "are glass-smooth and reflect distorted images of the fiery sky. Far below, "
                       "a river of molten rock carves ever deeper into the volcanic glass. The rim "
                       "is razor-sharp — even touching it draws blood.",
        "coordinates": [cx + 2, cy + 2],
        "location_type": "wilderness",
        "items": {"obsidian_shard": {"quantity": 2, "value": 14}},
        "exits": {
            "west": {"target": "cinder_village_overlook", "type": "direction"},
            "north": {"target": "cinder_obsidian_descent", "type": "direction"},
            "east": {"target": "cinder_obsidian_overlook", "type": "direction"}
        }
    }

    rooms["cinder_obsidian_overlook"] = {
        "id": "cinder_obsidian_overlook",
        "name": "Glass Precipice",
        "description": "A jutting shelf of obsidian extends over the canyon like a dark balcony. "
                       "The glass is so clear you can see veins of trapped gas and mineral inclusions "
                       "within the rock beneath your feet. Below, the canyon splits into multiple "
                       "branches, each darker than the last.",
        "coordinates": [cx + 3, cy + 2],
        "location_type": "wilderness",
        "items": {"volcanic_glass_lens": {"quantity": 1, "value": 20}},
        "exits": {
            "west": {"target": "cinder_obsidian_rim", "type": "direction"},
            "north": {"target": "cinder_obsidian_narrow", "type": "direction"}
        }
    }

    rooms["cinder_obsidian_descent"] = {
        "id": "cinder_obsidian_descent",
        "name": "Canyon Descent",
        "description": "A steep switchback trail carved into the obsidian canyon wall leads down "
                       "into the depths. The walls close in as you descend, reflecting your torchlight "
                       "in a thousand dark mirrors. The air grows hotter with each step down.",
        "coordinates": [cx + 2, cy + 3],
        "location_type": "wilderness",
        "items": {},
        "exits": {
            "south": {"target": "cinder_obsidian_rim", "type": "direction"},
            "north": {"target": "cinder_obsidian_floor", "type": "direction"},
            "east": {"target": "cinder_obsidian_narrow", "type": "direction"}
        }
    }

    rooms["cinder_obsidian_narrow"] = {
        "id": "cinder_obsidian_narrow",
        "name": "Razor Narrows",
        "description": "The canyon narrows to barely shoulder-width, its walls of flawless obsidian "
                       "pressing close on both sides. Every surface is sharp enough to slice through "
                       "leather. Strange harmonic sounds echo through the passage as wind is forced "
                       "through the constriction.",
        "coordinates": [cx + 3, cy + 3],
        "location_type": "wilderness",
        "items": {"razor_obsidian_fragment": {"quantity": 1, "value": 18}},
        "exits": {
            "south": {"target": "cinder_obsidian_overlook", "type": "direction"},
            "west": {"target": "cinder_obsidian_descent", "type": "direction"},
            "north": {"target": "cinder_obsidian_crystal_cave", "type": "direction"}
        }
    }

    rooms["cinder_obsidian_floor"] = {
        "id": "cinder_obsidian_floor",
        "name": "Canyon Floor",
        "description": "The bottom of the obsidian canyon is a wide corridor of black glass. "
                       "A thin stream of superheated water runs along a channel in the center, "
                       "steaming and mineral-rich. The walls rise vertically on both sides, "
                       "their surfaces carved with ancient dwarven mining marks.",
        "coordinates": [cx + 2, cy + 4],
        "location_type": "wilderness",
        "items": {"heated_mineral_water_vial": {"quantity": 1, "value": 14}},
        "exits": {
            "south": {"target": "cinder_obsidian_descent", "type": "direction"},
            "east": {"target": "cinder_obsidian_crystal_cave", "type": "direction"},
            "north": {"target": "cinder_obsidian_mirror_hall", "type": "direction"}
        }
    }

    rooms["cinder_obsidian_crystal_cave"] = {
        "id": "cinder_obsidian_crystal_cave",
        "name": "Obsidian Crystal Cave",
        "description": "A natural cavern where obsidian has formed into enormous crystal structures. "
                       "Blades of volcanic glass three feet long sprout from the walls and ceiling "
                       "like a frozen explosion. Light refracts through them in dazzling patterns "
                       "of deep purple and midnight black.",
        "coordinates": [cx + 3, cy + 4],
        "location_type": "wilderness",
        "items": {"obsidian_crystal_blade": {"quantity": 1, "value": 40}, "volcanic_glass_prism": {"quantity": 1, "value": 25}},
        "exits": {
            "south": {"target": "cinder_obsidian_narrow", "type": "direction"},
            "west": {"target": "cinder_obsidian_floor", "type": "direction"}
        }
    }

    rooms["cinder_obsidian_mirror_hall"] = {
        "id": "cinder_obsidian_mirror_hall",
        "name": "Mirror Hall",
        "description": "A long section of canyon where the walls have been polished to a perfect "
                       "mirror finish by ancient lava flows. Your reflection stretches and distorts "
                       "in the curved surfaces, creating unsettling doppelgangers that seem to move "
                       "independently. The effect is deeply disorienting.",
        "coordinates": [cx + 2, cy + 5],
        "location_type": "wilderness",
        "items": {"mirror_obsidian_disc": {"quantity": 1, "value": 22}},
        "exits": {
            "south": {"target": "cinder_obsidian_floor", "type": "direction"},
            "north": {"target": "cinder_obsidian_vein", "type": "direction"}
        }
    }

    rooms["cinder_obsidian_vein"] = {
        "id": "cinder_obsidian_vein",
        "name": "Exposed Mineral Vein",
        "description": "A massive vein of raw metals cuts through the obsidian walls — iron, copper, "
                       "and traces of gold run in parallel bands through the volcanic glass. Ancient "
                       "dwarven picks still embedded in the rock show this vein was once heavily mined. "
                       "Some metal still glints, unclaimed.",
        "coordinates": [cx + 2, cy + 6],
        "location_type": "wilderness",
        "items": {"raw_iron_chunk": {"quantity": 2, "value": 12}, "trace_gold_ore": {"quantity": 1, "value": 35}},
        "exits": {
            "south": {"target": "cinder_obsidian_mirror_hall", "type": "direction"},
            "west": {"target": "cinder_obsidian_entrance", "type": "direction"},
            "east": {"target": "cinder_obsidian_deep_canyon", "type": "direction"}
        }
    }

    rooms["cinder_obsidian_entrance"] = {
        "id": "cinder_obsidian_entrance",
        "name": "Canyon Exit - Forge Road",
        "description": "The obsidian canyon opens onto a broad road of fitted basalt blocks leading "
                       "north toward the Ancient Forges. Dwarven road-markers carved with hammer "
                       "and anvil motifs line the path. The canyon's razor walls give way to "
                       "heat-blackened volcanic slopes.",
        "coordinates": [cx + 2, cy + 7],
        "location_type": "wilderness",
        "items": {},
        "exits": {
            "east": {"target": "cinder_obsidian_vein", "type": "direction"},
            "west": {"target": "cinder_lava_scorched_ridge", "type": "direction"},
            "north": {"target": "cinder_forge_approach", "type": "direction"}
        }
    }

    # --- Ancient Forges (12 rooms) ---

    rooms["cinder_forge_gate"] = {
        "id": "cinder_forge_gate",
        "name": "Gate of the Ancient Forges",
        "description": "A colossal archway of black iron and carved basalt marks the entrance to "
                       "the Ancient Forge complex. Dwarven runes of making and binding cover every "
                       "surface, still faintly glowing with residual enchantment. The sound of "
                       "distant hammering echoes from within, though the forges have been abandoned "
                       "for centuries.",
        "coordinates": [cx, cy + 7],
        "location_type": "building",
        "items": {},
        "exits": {
            "south": {"target": "cinder_lava_plateau", "type": "direction"},
            "north": {"target": "cinder_forge_main_hall", "type": "direction"},
            "east": {"target": "cinder_forge_approach", "type": "direction"},
            "west": {"target": "cinder_forge_guard_post", "type": "direction"}
        }
    }

    rooms["cinder_forge_approach"] = {
        "id": "cinder_forge_approach",
        "name": "Forge Approach Road",
        "description": "A wide paved road leads between the obsidian canyons and the forge complex. "
                       "Broken carts and scattered tools suggest this was once a busy supply route. "
                       "Ruts worn deep into the basalt paving show centuries of heavy ore-wagon traffic.",
        "coordinates": [cx + 1, cy + 7],
        "location_type": "wilderness",
        "items": {"rusted_dwarven_tool": {"quantity": 1, "value": 8}},
        "exits": {
            "west": {"target": "cinder_forge_gate", "type": "direction"},
            "south": {"target": "cinder_obsidian_entrance", "type": "direction"}
        }
    }

    rooms["cinder_forge_guard_post"] = {
        "id": "cinder_forge_guard_post",
        "name": "Forge Guard Post",
        "description": "A fortified watchtower that once protected the forge entrance from raiders "
                       "and lava surges. The armoured shutters still work, and racks of defensive "
                       "equipment — fire-shields, heat-resistant chain, and obsidian-tipped bolts — "
                       "remain in surprisingly good condition.",
        "coordinates": [cx - 1, cy + 7],
        "location_type": "building",
        "items": {"fire_shield": {"quantity": 1, "value": 35}, "obsidian_bolt": {"quantity": 3, "value": 10}},
        "exits": {
            "east": {"target": "cinder_forge_gate", "type": "direction"},
            "west": {"target": "cinder_forge_outpost", "type": "direction"}
        }
    }

    rooms["cinder_forge_main_hall"] = {
        "id": "cinder_forge_main_hall",
        "name": "Grand Forge Hall",
        "description": "An enormous vaulted hall carved from the living rock of the volcano. "
                       "Dozens of cold forge-pits line the walls, each large enough to smelt a "
                       "ship's anchor. The ceiling is blackened by millennia of smoke and the "
                       "floor is paved with heat-proof dwarven alloy tiles.",
        "coordinates": [cx, cy + 8],
        "location_type": "building",
        "items": {"dwarven_alloy_tile": {"quantity": 1, "value": 20}},
        "exits": {
            "south": {"target": "cinder_forge_gate", "type": "direction"},
            "north": {"target": "cinder_forge_master_anvil", "type": "direction"},
            "east": {"target": "cinder_forge_east_wing", "type": "direction"},
            "west": {"target": "cinder_forge_west_wing", "type": "direction"}
        }
    }

    rooms["cinder_forge_east_wing"] = {
        "id": "cinder_forge_east_wing",
        "name": "Weaponsmith Wing",
        "description": "The eastern wing was dedicated to weapon-crafting. Grinding wheels, "
                       "quenching troughs, and precision anvils fill the chamber. Weapon moulds "
                       "for swords, axes, and hammers line the walls. Some still contain solidified "
                       "metal, frozen mid-pour when the forges were abandoned.",
        "coordinates": [cx + 1, cy + 8],
        "location_type": "building",
        "items": {"ancient_sword_mould": {"quantity": 1, "value": 28}, "solidified_steel_casting": {"quantity": 1, "value": 16}},
        "exits": {
            "west": {"target": "cinder_forge_main_hall", "type": "direction"},
            "east": {"target": "cinder_forge_smelter", "type": "direction"},
            "north": {"target": "cinder_forge_enchant_room", "type": "direction"}
        }
    }

    rooms["cinder_forge_west_wing"] = {
        "id": "cinder_forge_west_wing",
        "name": "Armoursmith Wing",
        "description": "The western wing focused on armour and shield crafting. Enormous hammering "
                       "machines — powered by geothermal steam — stand silent but intact. Sheets "
                       "of partially worked metal hang from overhead racks, and a half-finished "
                       "suit of masterwork plate armour sits on a fitting mannequin.",
        "coordinates": [cx - 1, cy + 8],
        "location_type": "building",
        "items": {"masterwork_plate_fragment": {"quantity": 1, "value": 45}, "geothermal_steam_valve": {"quantity": 1, "value": 15}},
        "exits": {
            "east": {"target": "cinder_forge_main_hall", "type": "direction"},
            "north": {"target": "cinder_forge_ore_store", "type": "direction"}
        }
    }

    rooms["cinder_forge_master_anvil"] = {
        "id": "cinder_forge_master_anvil",
        "name": "Master Anvil Chamber",
        "description": "At the heart of the forge complex sits the Master Anvil — a monolithic "
                       "block of enchanted meteoric iron set into the floor above a controlled "
                       "magma vent. Runes spiral across its surface, still pulsing with dormant "
                       "power. Items struck upon it were said to gain magical properties.",
        "coordinates": [cx, cy + 9],
        "location_type": "building",
        "items": {"meteoric_iron_flake": {"quantity": 1, "value": 50}},
        "exits": {
            "south": {"target": "cinder_forge_main_hall", "type": "direction"},
            "east": {"target": "cinder_forge_enchant_room", "type": "direction"},
            "west": {"target": "cinder_forge_ore_store", "type": "direction"},
            "north": {"target": "cinder_forge_deep_shaft", "type": "direction"}
        }
    }

    rooms["cinder_forge_enchant_room"] = {
        "id": "cinder_forge_enchant_room",
        "name": "Enchantment Chamber",
        "description": "A circular chamber lined with rune-carved pillars of obsidian. This is "
                       "where finished weapons and armour received their magical enchantments. "
                       "A ritual circle is etched into the floor, its channels still stained "
                       "with residual magical reagents. The air tingles with latent power.",
        "coordinates": [cx + 1, cy + 9],
        "location_type": "building",
        "items": {"enchantment_reagent_dust": {"quantity": 1, "value": 30}, "rune_carved_pillar_chip": {"quantity": 1, "value": 18}},
        "exits": {
            "south": {"target": "cinder_forge_east_wing", "type": "direction"},
            "west": {"target": "cinder_forge_master_anvil", "type": "direction"}
        }
    }

    rooms["cinder_forge_ore_store"] = {
        "id": "cinder_forge_ore_store",
        "name": "Ore Vault",
        "description": "A massive storage vault where raw ores were kept before smelting. Iron-banded "
                       "bins still hold quantities of iron ore, copper, tin, and rarer metals. A few "
                       "bins are locked with dwarven puzzle-locks, their contents unknown but presumably "
                       "valuable given the security.",
        "coordinates": [cx - 1, cy + 9],
        "location_type": "building",
        "items": {"iron_ore": {"quantity": 3, "value": 8}, "rare_metal_nugget": {"quantity": 1, "value": 40}},
        "exits": {
            "south": {"target": "cinder_forge_west_wing", "type": "direction"},
            "east": {"target": "cinder_forge_master_anvil", "type": "direction"}
        }
    }

    rooms["cinder_forge_deep_shaft"] = {
        "id": "cinder_forge_deep_shaft",
        "name": "Deep Mining Shaft",
        "description": "A vertical shaft descends into the volcano's root, its walls reinforced "
                       "with dwarven girders. A rusted but functional ore-lift mechanism hangs over "
                       "the abyss. The mine below was the source of the island's rarest metals, "
                       "but something disturbed the deeper tunnels and the miners never returned.",
        "coordinates": [cx, cy + 10],
        "location_type": "building",
        "items": {"dwarven_mining_pick": {"quantity": 1, "value": 22}},
        "exits": {
            "south": {"target": "cinder_forge_master_anvil", "type": "direction"},
            "north": {"target": "cinder_forge_abandoned_tunnel", "type": "direction"}
        }
    }

    rooms["cinder_forge_abandoned_tunnel"] = {
        "id": "cinder_forge_abandoned_tunnel",
        "name": "Abandoned Mine Tunnel",
        "description": "A collapsed tunnel deep beneath the forges. Dwarven supports have buckled "
                       "under volcanic pressure and rubble blocks most passages. Scorch marks on "
                       "the walls suggest something other than lava caused the destruction. A single "
                       "narrow passage continues deeper into the mountain.",
        "coordinates": [cx, cy + 11],
        "location_type": "wilderness",
        "items": {"scorched_dwarven_helmet": {"quantity": 1, "value": 25}},
        "exits": {
            "south": {"target": "cinder_forge_deep_shaft", "type": "direction"},
            "north": {"target": "cinder_volcano_approach", "type": "direction"}
        }
    }

    rooms["cinder_forge_smelter"] = {
        "id": "cinder_forge_smelter",
        "name": "Grand Smelter",
        "description": "An industrial-scale smelting facility built directly over a magma channel. "
                       "Enormous stone crucibles could process tons of ore at once, heated by diverted "
                       "lava flows. The cooling system — an ingenious network of water channels fed "
                       "from underground rivers — still trickles faintly.",
        "coordinates": [cx + 2, cy + 8],
        "location_type": "building",
        "items": {"refined_volcanic_steel": {"quantity": 1, "value": 38}},
        "exits": {
            "west": {"target": "cinder_forge_east_wing", "type": "direction"},
            "east": {"target": "cinder_forge_testing_ground", "type": "direction"}
        }
    }

    # --- Ash Wastes (10 rooms) ---

    rooms["cinder_ash_border"] = {
        "id": "cinder_ash_border",
        "name": "Ash Waste Border",
        "description": "The landscape changes abruptly from volcanic rock to deep drifts of grey "
                       "ash. Wind whips the fine powder into stinging clouds that reduce visibility "
                       "to a few metres. The remains of a stone fence mark where the village once "
                       "tried to hold back the advancing ash fields.",
        "coordinates": [cx - 2, cy + 2],
        "location_type": "wilderness",
        "items": {},
        "exits": {
            "east": {"target": "cinder_village_overlook", "type": "direction"},
            "north": {"target": "cinder_ash_dunes", "type": "direction"},
            "west": {"target": "cinder_ash_collapsed_tower", "type": "direction"}
        }
    }

    rooms["cinder_ash_dunes"] = {
        "id": "cinder_ash_dunes",
        "name": "Ash Dunes",
        "description": "Rolling dunes of fine volcanic ash stretch to the horizon like a grey desert. "
                       "The wind sculpts them into constantly shifting shapes. Occasionally, the tip "
                       "of a buried structure — a chimney, an arch — pokes through the surface, "
                       "hinting at a civilisation swallowed by eruptions.",
        "coordinates": [cx - 2, cy + 3],
        "location_type": "wilderness",
        "items": {"buried_artifact_shard": {"quantity": 1, "value": 18}},
        "exits": {
            "south": {"target": "cinder_ash_border", "type": "direction"},
            "north": {"target": "cinder_ash_bone_field", "type": "direction"},
            "east": {"target": "cinder_ash_storm_path", "type": "direction"}
        }
    }

    rooms["cinder_ash_storm_path"] = {
        "id": "cinder_ash_storm_path",
        "name": "Cinder Storm Path",
        "description": "A narrow trail through the worst of the ash wastes. Cinder storms — "
                       "violent winds carrying burning embers and volcanic grit — sweep through "
                       "unpredictably. The path is marked by iron stakes driven into the bedrock, "
                       "connected by chains for travellers to cling to in zero visibility.",
        "coordinates": [cx - 1, cy + 3],
        "location_type": "wilderness",
        "items": {"iron_trail_stake": {"quantity": 1, "value": 10}},
        "exits": {
            "west": {"target": "cinder_ash_dunes", "type": "direction"},
            "north": {"target": "cinder_ash_ruins", "type": "direction"}
        }
    }

    rooms["cinder_ash_collapsed_tower"] = {
        "id": "cinder_ash_collapsed_tower",
        "name": "Collapsed Watchtower",
        "description": "The remains of a stone watchtower, half-buried in ash and tilted at a "
                       "precarious angle. The upper floors have collapsed but the ground level "
                       "provides shelter from the cinder storms. Old signal equipment and a "
                       "cracked warning bell still hang from the surviving walls.",
        "coordinates": [cx - 3, cy + 2],
        "location_type": "wilderness",
        "items": {"cracked_signal_bell": {"quantity": 1, "value": 14}, "old_signal_flag": {"quantity": 1, "value": 6}},
        "exits": {
            "east": {"target": "cinder_ash_border", "type": "direction"},
            "north": {"target": "cinder_ash_graveyard", "type": "direction"}
        }
    }

    rooms["cinder_ash_bone_field"] = {
        "id": "cinder_ash_bone_field",
        "name": "Bone Field",
        "description": "A grim expanse where the ash has eroded to reveal a layer of fossilised "
                       "bones — the remains of creatures caught in an ancient pyroclastic flow. "
                       "Some bones are enormous, belonging to beasts long extinct. Others are "
                       "disturbingly humanoid, frozen in poses of desperate flight.",
        "coordinates": [cx - 2, cy + 4],
        "location_type": "wilderness",
        "items": {"ancient_fossil_bone": {"quantity": 1, "value": 22}, "petrified_tooth": {"quantity": 1, "value": 15}},
        "exits": {
            "south": {"target": "cinder_ash_dunes", "type": "direction"},
            "east": {"target": "cinder_ash_ruins", "type": "direction"},
            "north": {"target": "cinder_ash_sulfur_flat", "type": "direction"}
        }
    }

    rooms["cinder_ash_ruins"] = {
        "id": "cinder_ash_ruins",
        "name": "Ashen Ruins",
        "description": "The partially excavated remains of a pre-eruption settlement. Stone walls "
                       "emerge from the ash like broken teeth. Inside the ruined buildings, everyday "
                       "objects — cookware, tools, toys — are preserved under thick layers of "
                       "volcanic debris, a snapshot of life interrupted.",
        "coordinates": [cx - 1, cy + 4],
        "location_type": "wilderness",
        "items": {"preserved_cooking_pot": {"quantity": 1, "value": 12}, "ancient_dwarven_toy": {"quantity": 1, "value": 20}},
        "exits": {
            "south": {"target": "cinder_ash_storm_path", "type": "direction"},
            "west": {"target": "cinder_ash_bone_field", "type": "direction"},
            "north": {"target": "cinder_ash_sinkhole", "type": "direction"}
        }
    }

    rooms["cinder_ash_graveyard"] = {
        "id": "cinder_ash_graveyard",
        "name": "Ashen Graveyard",
        "description": "A cemetery where the dead were interred in stone sarcophagi to protect them "
                       "from the volcanic soil. Many lids have been displaced by ground shifts, "
                       "revealing empty interiors — the bodies long since crumbled to ash. "
                       "Tombstones of heat-fused glass bear dwarven epitaphs.",
        "coordinates": [cx - 3, cy + 3],
        "location_type": "wilderness",
        "items": {"glass_tombstone_fragment": {"quantity": 1, "value": 16}},
        "exits": {
            "south": {"target": "cinder_ash_collapsed_tower", "type": "direction"},
            "east": {"target": "cinder_ash_sulfur_flat", "type": "direction"},
            "west": {"target": "cinder_ash_deep_wastes", "type": "direction"}
        }
    }

    rooms["cinder_ash_sulfur_flat"] = {
        "id": "cinder_ash_sulfur_flat",
        "name": "Sulfur Flats",
        "description": "A barren plain encrusted with bright yellow sulfur deposits. The ground "
                       "crunches and cracks underfoot, releasing noxious fumes. Pools of sulfuric "
                       "acid bubble in shallow depressions, their edges ringed with crystal "
                       "formations of startling beauty despite the toxic environment.",
        "coordinates": [cx - 2, cy + 5],
        "location_type": "wilderness",
        "items": {"sulfur_crystal": {"quantity": 2, "value": 12}, "acid_resistant_stone": {"quantity": 1, "value": 18}},
        "exits": {
            "south": {"target": "cinder_ash_bone_field", "type": "direction"},
            "west": {"target": "cinder_ash_graveyard", "type": "direction"},
            "east": {"target": "cinder_ash_sinkhole", "type": "direction"}
        }
    }

    rooms["cinder_ash_sinkhole"] = {
        "id": "cinder_ash_sinkhole",
        "name": "Cinder Sinkhole",
        "description": "A massive circular sinkhole where the ground collapsed into a lava tube "
                       "below. The walls reveal geological layers — ash, obsidian, pumice, and "
                       "ancient soil — like a cross-section of the island's violent history. A "
                       "precarious ledge spirals down into darkness and oppressive heat.",
        "coordinates": [cx - 1, cy + 5],
        "location_type": "wilderness",
        "items": {"pumice_stone": {"quantity": 2, "value": 6}},
        "exits": {
            "south": {"target": "cinder_ash_ruins", "type": "direction"},
            "west": {"target": "cinder_ash_sulfur_flat", "type": "direction"},
            "north": {"target": "cinder_slag_entrance", "type": "direction"}
        }
    }

    # --- Volcano Core (8 rooms) ---

    rooms["cinder_volcano_approach"] = {
        "id": "cinder_volcano_approach",
        "name": "Volcano Approach",
        "description": "The ground slopes steeply upward toward the volcano's caldera. The rock "
                       "is hot enough to burn through thin boots and the air is thick with toxic "
                       "fumes. Ancient warning stones carved with dwarven skulls line the path — "
                       "DO NOT PROCEED is written in a dozen languages.",
        "coordinates": [cx, cy + 12],
        "location_type": "wilderness",
        "items": {},
        "exits": {
            "south": {"target": "cinder_forge_abandoned_tunnel", "type": "direction"},
            "north": {"target": "cinder_volcano_outer_rim", "type": "direction"},
            "east": {"target": "cinder_volcano_fumarole", "type": "direction"},
            "west": {"target": "cinder_volcano_crystal_vent", "type": "direction"}
        }
    }

    rooms["cinder_volcano_outer_rim"] = {
        "id": "cinder_volcano_outer_rim",
        "name": "Volcano Outer Rim",
        "description": "You stand on the crumbling outer rim of the volcano's caldera. Below, a "
                       "vast bowl of molten rock churns and heaves, casting everything in hellish "
                       "orange light. The heat is almost unbearable and volcanic bombs — chunks of "
                       "molten rock — arc overhead with terrifying frequency.",
        "coordinates": [cx, cy + 13],
        "location_type": "wilderness",
        "items": {"volcanic_bomb_fragment": {"quantity": 1, "value": 20}},
        "exits": {
            "south": {"target": "cinder_volcano_approach", "type": "direction"},
            "west": {"target": "cinder_volcano_crystal_vent", "type": "direction"},
            "east": {"target": "cinder_volcano_lava_tube", "type": "direction"},
            "north": {"target": "cinder_volcano_inner_descent", "type": "direction"}
        }
    }

    rooms["cinder_volcano_fumarole"] = {
        "id": "cinder_volcano_fumarole",
        "name": "Fumarole Vents",
        "description": "A field of active fumaroles blasts superheated volcanic gases from deep "
                       "within the earth. The vents are ringed with deposits of pure elemental "
                       "sulfur and rare volcanic minerals. The noise is deafening — a constant "
                       "roar of escaping pressure from the mountain's depths.",
        "coordinates": [cx + 1, cy + 12],
        "location_type": "wilderness",
        "items": {"pure_sulfur_deposit": {"quantity": 1, "value": 16}, "rare_volcanic_mineral": {"quantity": 1, "value": 30}},
        "exits": {
            "west": {"target": "cinder_volcano_approach", "type": "direction"},
            "north": {"target": "cinder_volcano_lava_tube", "type": "direction"}
        }
    }

    rooms["cinder_volcano_lava_tube"] = {
        "id": "cinder_volcano_lava_tube",
        "name": "Ancient Lava Tube",
        "description": "A natural tunnel formed by flowing lava millennia ago. The tube is wide "
                       "enough to march an army through, its walls glazed smooth as glass. Stalactites "
                       "of cooled lava hang from the ceiling like stone fangs. The deeper you go, "
                       "the hotter and brighter it becomes.",
        "coordinates": [cx + 1, cy + 13],
        "location_type": "wilderness",
        "items": {"lava_stalactite_shard": {"quantity": 1, "value": 18}},
        "exits": {
            "south": {"target": "cinder_volcano_fumarole", "type": "direction"},
            "west": {"target": "cinder_volcano_outer_rim", "type": "direction"},
            "north": {"target": "cinder_volcano_magma_chamber", "type": "direction"}
        }
    }

    rooms["cinder_volcano_inner_descent"] = {
        "id": "cinder_volcano_inner_descent",
        "name": "Inner Caldera Descent",
        "description": "A treacherous path carved into the inner wall of the caldera spirals "
                       "downward toward the magma chamber. The rock glows dull red with conducted "
                       "heat and the air shimmers like a mirage. Dwarven reinforcing bolts are "
                       "driven into the path at intervals — someone intended to reach the bottom.",
        "coordinates": [cx, cy + 14],
        "location_type": "wilderness",
        "items": {"dwarven_reinforcing_bolt": {"quantity": 1, "value": 14}},
        "exits": {
            "south": {"target": "cinder_volcano_outer_rim", "type": "direction"},
            "east": {"target": "cinder_volcano_magma_chamber", "type": "direction"}
        }
    }

    rooms["cinder_volcano_magma_chamber"] = {
        "id": "cinder_volcano_magma_chamber",
        "name": "Magma Chamber",
        "description": "An enormous cavern filled with a lake of churning magma. The heat is "
                       "beyond extreme — metal glows and leather chars. Islands of solidified "
                       "rock float on the molten surface, colliding and breaking apart in slow "
                       "motion. The chamber pulses with the volcano's heartbeat.",
        "coordinates": [cx + 1, cy + 14],
        "location_type": "wilderness",
        "items": {"magma_core_crystal": {"quantity": 1, "value": 55}},
        "exits": {
            "south": {"target": "cinder_volcano_lava_tube", "type": "direction"},
            "west": {"target": "cinder_volcano_inner_descent", "type": "direction"},
            "north": {"target": "cinder_volcano_heart", "type": "direction"}
        }
    }

    rooms["cinder_volcano_heart"] = {
        "id": "cinder_volcano_heart",
        "name": "Heart of the Volcano",
        "description": "The deepest, hottest point of the volcano — a chamber where raw elemental "
                       "fire meets the bones of the earth. A column of pure magma rises from a "
                       "fissure in the floor, feeding the caldera above. Embedded in the far wall "
                       "is a doorway of heat-warped dwarven metal, sealed with runes of containment. "
                       "Something immensely powerful lurks beyond.",
        "coordinates": [cx, cy + 15],
        "location_type": "wilderness",
        "items": {"heart_of_flame_ember": {"quantity": 1, "value": 75}},
        "exits": {
            "south": {"target": "cinder_volcano_magma_chamber", "type": "direction"},
            "enter": {
                "target": "FIXED_DUNGEON",
                "type": "fixed_dungeon",
                "dungeon_id": "molten_crucible",
                "transition_text": "You break the ancient seals and force open the dwarven door. A blast\nof superheated air roars outward. Beyond lies the Molten Crucible —\na dwarven mega-forge built around a core of living magma, now\ncorrupted and guarded by fire elementals and forge-wraiths..."
            }
        }
    }

    rooms["cinder_volcano_crystal_vent"] = {
        "id": "cinder_volcano_crystal_vent",
        "name": "Crystal Vent Grotto",
        "description": "A side chamber where volcanic gases have crystallised into spectacular "
                       "formations. Needles of selenite, clusters of fire opal, and veins of "
                       "pure elemental crystal line every surface. The grotto is dangerously "
                       "unstable — cracks spider-web through the floor.",
        "coordinates": [cx - 1, cy + 13],
        "location_type": "wilderness",
        "items": {"selenite_needle": {"quantity": 1, "value": 28}, "raw_fire_opal": {"quantity": 1, "value": 45}},
        "exits": {
            "east": {"target": "cinder_volcano_outer_rim", "type": "direction"},
            "south": {"target": "cinder_volcano_approach", "type": "direction"},
            "west": {"target": "cinder_volcano_crystal_caves", "type": "direction"}
        }
    }

    # --- Slag Pits (5 rooms) ---

    rooms["cinder_slag_entrance"] = {
        "id": "cinder_slag_entrance",
        "name": "Slag Pit Entrance",
        "description": "A chasm opens in the ashen ground, revealing layers of industrial waste "
                       "from the ancient forges. Rivers of metallic residue have solidified into "
                       "strange striated patterns of iron, copper, and unknown alloys. The air "
                       "has a sharp metallic tang that coats the tongue.",
        "coordinates": [cx - 1, cy + 6],
        "location_type": "wilderness",
        "items": {},
        "exits": {
            "south": {"target": "cinder_ash_sinkhole", "type": "direction"},
            "north": {"target": "cinder_slag_metallic_pools", "type": "direction"},
            "east": {"target": "cinder_slag_crystal_shelf", "type": "direction"}
        }
    }

    rooms["cinder_slag_metallic_pools"] = {
        "id": "cinder_slag_metallic_pools",
        "name": "Metallic Pools",
        "description": "Pools of liquid metal shimmer in shallow basins carved by centuries of "
                       "runoff from the forges above. Mercury, molten tin, and stranger metals "
                       "swirl in mesmerizing patterns. The pools are toxic but contain valuable "
                       "deposits of refined metals along their crusted edges.",
        "coordinates": [cx - 1, cy + 7],
        "location_type": "wilderness",
        "items": {"refined_tin_nugget": {"quantity": 2, "value": 14}, "mercury_vial": {"quantity": 1, "value": 22}},
        "exits": {
            "south": {"target": "cinder_slag_entrance", "type": "direction"},
            "east": {"target": "cinder_slag_waste_heap", "type": "direction"}
        }
    }

    rooms["cinder_slag_crystal_shelf"] = {
        "id": "cinder_slag_crystal_shelf",
        "name": "Crystallised Slag Shelf",
        "description": "A ledge where molten slag has cooled into spectacular crystal formations. "
                       "Unlike natural crystals, these are geometric impossibilities — perfect cubes "
                       "of iron, spirals of copper, and fractal patterns of mixed alloys. The dwarven "
                       "smelting process created something unexpectedly beautiful in its waste.",
        "coordinates": [cx, cy + 6],
        "location_type": "wilderness",
        "items": {"iron_crystal_cube": {"quantity": 1, "value": 30}, "copper_spiral": {"quantity": 1, "value": 24}},
        "exits": {
            "west": {"target": "cinder_slag_entrance", "type": "direction"},
            "north": {"target": "cinder_slag_waste_heap", "type": "direction"}
        }
    }

    rooms["cinder_slag_waste_heap"] = {
        "id": "cinder_slag_waste_heap",
        "name": "Industrial Waste Heap",
        "description": "Mountains of discarded slag, broken crucibles, and failed castings form "
                       "a jagged landscape of industrial refuse. Despite appearances, valuable "
                       "materials can be salvaged — rejected pieces that didn't meet dwarven "
                       "standards would be masterwork anywhere else.",
        "coordinates": [cx, cy + 7],
        "location_type": "wilderness",
        "items": {"rejected_dwarven_blade": {"quantity": 1, "value": 35}, "broken_crucible_shard": {"quantity": 2, "value": 8}},
        "exits": {
            "south": {"target": "cinder_slag_crystal_shelf", "type": "direction"},
            "west": {"target": "cinder_slag_metallic_pools", "type": "direction"},
            "north": {"target": "cinder_slag_toxic_seep", "type": "direction"}
        }
    }

    rooms["cinder_slag_toxic_seep"] = {
        "id": "cinder_slag_toxic_seep",
        "name": "Toxic Seep",
        "description": "The lowest point of the slag pits, where toxic runoff collects in a "
                       "stagnant pool of iridescent metallic sludge. Despite the danger, rare "
                       "precipitates form along the edges — purified metals that only extreme "
                       "toxicity can produce. Alchemists pay fortunes for these samples.",
        "coordinates": [cx, cy + 8],
        "location_type": "wilderness",
        "items": {"toxic_precipitate_sample": {"quantity": 1, "value": 45}, "iridescent_slag_chunk": {"quantity": 1, "value": 20}},
        "exits": {
            "south": {"target": "cinder_slag_waste_heap", "type": "direction"}
        }
    }



    # === CINDERFORGE ISLAND EXPANSION ===

    # --- Expanded Docks (+3 rooms) ---

    rooms["cinder_docks_watchtower"] = {
        "id": "cinder_docks_watchtower",
        "name": "Ember Watchtower",
        "description": "A stone watchtower built atop a volcanic outcrop overlooking the dock. "
                       "Its fire signal can be seen for miles, warning ships of lava flows that "
                       "sometimes reach the harbor. The heat-resistant glass windows offer a "
                       "commanding view of the approach.",
        "coordinates": [cx + 2, cy - 4],
        "location_type": "building",
        "items": {"fire_signal_oil": {"quantity": 1, "value": 12}, "heat_glass_lens": {"quantity": 1, "value": 20}},
        "exits": {
            "west": {"target": "cinder_docks_beacon", "type": "direction"},
            "north": {"target": "cinder_docks_lava_pier", "type": "direction"}
        }
    }

    rooms["cinder_docks_lava_pier"] = {
        "id": "cinder_docks_lava_pier",
        "name": "Lava Pier",
        "description": "An obsidian pier extending into a channel where a small lava flow meets "
                       "the sea, sending up permanent clouds of steam. Fishermen cast heat-resistant "
                       "lines near the thermal vents where unique fire-adapted fish gather. "
                       "The basalt surface is uncomfortably warm to the touch.",
        "coordinates": [cx + 2, cy - 3],
        "location_type": "dock",
        "items": {"lava_fishing_line": {"quantity": 1, "value": 15}, "thermal_fish": {"quantity": 1, "value": 18}},
        "exits": {
            "south": {"target": "cinder_docks_watchtower", "type": "direction"},
            "north": {"target": "cinder_docks_steam_market", "type": "direction"}
        }
    }

    rooms["cinder_docks_steam_market"] = {
        "id": "cinder_docks_steam_market",
        "name": "Steam Market",
        "description": "A small marketplace that has grown up around the steam vents near the "
                       "dock. Vendors cook food directly on hot stones and sell fire-resistant "
                       "goods to arriving travelers. The perpetual steam provides natural cover, "
                       "making this a popular spot for discreet transactions.",
        "coordinates": [cx + 2, cy - 2],
        "location_type": "settlement",
        "items": {"steam_cooked_fish": {"quantity": 2, "value": 6}, "fire_resistant_gloves": {"quantity": 1, "value": 18}},
        "exits": {
            "south": {"target": "cinder_docks_lava_pier", "type": "direction"}
        }
    }

    # --- Expanded Cinder Village (+5 rooms) ---

    rooms["cinder_village_training_ground"] = {
        "id": "cinder_village_training_ground",
        "name": "Ember Guard Training Ground",
        "description": "A volcanic clearing where Ember Guards train to fight in extreme heat. "
                       "Obsidian training dummies are heated until they glow, simulating combat "
                       "with fire elementals. The ground is scorched black from years of "
                       "fire-based drills.",
        "coordinates": [cx + 2, cy - 1],
        "location_type": "building",
        "items": {"training_obsidian_shard": {"quantity": 1, "value": 10}, "heat_combat_manual": {"quantity": 1, "value": 15}},
        "exits": {
            "west": {"target": "cinder_village_barracks", "type": "direction"},
            "north": {"target": "cinder_village_lookout", "type": "direction"}
        }
    }

    rooms["cinder_village_lookout"] = {
        "id": "cinder_village_lookout",
        "name": "Village Lookout Post",
        "description": "A raised platform at the eastern edge of the village offering views of "
                       "the obsidian canyons beyond. Guards stationed here watch for both monster "
                       "incursions and unexpected lava flows. Signal horns hang from iron brackets.",
        "coordinates": [cx + 2, cy],
        "location_type": "building",
        "items": {"signal_horn": {"quantity": 1, "value": 12}},
        "exits": {
            "south": {"target": "cinder_village_training_ground", "type": "direction"},
            "west": {"target": "cinder_village_apothecary", "type": "direction"}
        }
    }

    rooms["cinder_village_herb_garden"] = {
        "id": "cinder_village_herb_garden",
        "name": "Volcanic Herb Garden",
        "description": "A terraced garden built on cooled lava flows where medicinal plants "
                       "adapted to volcanic soil thrive. Ash moss, fire ferns, and ember sage "
                       "grow in carefully tended beds. The healer tends these plants daily, "
                       "harvesting ingredients for remedies.",
        "coordinates": [cx - 3, cy],
        "location_type": "wilderness",
        "items": {"ember_sage": {"quantity": 2, "value": 12}, "volcanic_soil_sample": {"quantity": 1, "value": 8}},
        "exits": {
            "east": {"target": "cinder_village_healer", "type": "direction"},
            "north": {"target": "cinder_village_hot_spring", "type": "direction"}
        }
    }

    rooms["cinder_village_hot_spring"] = {
        "id": "cinder_village_hot_spring",
        "name": "Villagers' Hot Spring",
        "description": "A natural hot spring heated by volcanic activity, used by villagers for "
                       "bathing and relaxation. The mineral-rich water is said to have healing "
                       "properties. Steam rises from the surface, and the surrounding rocks are "
                       "encrusted with colorful mineral deposits.",
        "coordinates": [cx - 3, cy + 1],
        "location_type": "settlement",
        "items": {"mineral_bath_salt": {"quantity": 2, "value": 8}, "volcanic_mineral_crystal": {"quantity": 1, "value": 22}},
        "exits": {
            "south": {"target": "cinder_village_herb_garden", "type": "direction"}
        }
    }

    rooms["cinder_village_old_mine"] = {
        "id": "cinder_village_old_mine",
        "name": "Abandoned Village Mine",
        "description": "An old mine shaft at the village's northern edge, sealed off after a "
                       "collapse decades ago. The timbers are charred but still standing, and "
                       "a warm draft rises from below. Villagers say strange sounds echo from "
                       "the depths on quiet nights.",
        "coordinates": [cx - 1, cy + 2],
        "location_type": "building",
        "items": {"old_mining_pick": {"quantity": 1, "value": 10}, "collapsed_mine_stone": {"quantity": 1, "value": 5}},
        "exits": {
            "south": {"target": "cinder_village_overlook", "type": "direction"}
        }
    }

    # --- Expanded Lava Fields (+6 rooms) ---

    rooms["cinder_lava_deadwood"] = {
        "id": "cinder_lava_deadwood",
        "name": "Deadwood Expanse",
        "description": "A forest of petrified trees killed by ancient lava flows. The stone "
                       "trunks stand like gray sentinels, some still showing the texture of "
                       "bark and branches. Ash drifts between them like snow, and the silence "
                       "is absolute.",
        "coordinates": [cx - 2, cy + 5],
        "location_type": "wilderness",
        "items": {"petrified_branch": {"quantity": 1, "value": 15}, "stone_bark": {"quantity": 1, "value": 10}},
        "exits": {
            "east": {"target": "cinder_lava_charred_grove", "type": "direction"},
            "west": {"target": "cinder_lava_cinder_lake", "type": "direction"},
            "south": {"target": "cinder_lava_ember_pit", "type": "direction"}
        }
    }

    rooms["cinder_lava_cinder_lake"] = {
        "id": "cinder_lava_cinder_lake",
        "name": "Cinder Lake",
        "description": "A lake of dark water colored by volcanic ash, its surface perpetually "
                       "covered with a thin layer of floating cinders. Despite its foreboding "
                       "appearance, hardy fish thrive in the warm, mineral-rich water. Steam "
                       "rises where underwater vents heat the depths.",
        "coordinates": [cx - 3, cy + 5],
        "location_type": "wilderness",
        "items": {"cinder_lake_fish": {"quantity": 1, "value": 12}, "floating_pumice": {"quantity": 2, "value": 4}},
        "exits": {
            "east": {"target": "cinder_lava_deadwood", "type": "direction"},
            "south": {"target": "cinder_lava_hot_mud", "type": "direction"}
        }
    }

    rooms["cinder_lava_ember_pit"] = {
        "id": "cinder_lava_ember_pit",
        "name": "Ember Pit",
        "description": "A shallow depression where embers never fully die, glowing red and "
                       "orange beneath a crust of gray ash. Stepping too hard cracks the crust, "
                       "releasing blasts of heat. Fire salamanders bask in the warmth, their "
                       "scales shimmering like molten glass.",
        "coordinates": [cx - 2, cy + 4],
        "location_type": "wilderness",
        "items": {"fire_salamander_scale": {"quantity": 1, "value": 25}, "eternal_ember": {"quantity": 1, "value": 18}},
        "exits": {
            "north": {"target": "cinder_lava_deadwood", "type": "direction"},
            "west": {"target": "cinder_lava_hot_mud", "type": "direction"},
            "east": {"target": "cinder_lava_bubble_pool", "type": "direction"}
        }
    }

    rooms["cinder_lava_hot_mud"] = {
        "id": "cinder_lava_hot_mud",
        "name": "Boiling Mud Flats",
        "description": "A field of bubbling mud heated by underground magma. The mud ranges from "
                       "warm to lethally hot — experienced guides know which patches are safe. "
                       "The air reeks of sulfur. Some medicinal clay is harvested from the cooler "
                       "edges.",
        "coordinates": [cx - 3, cy + 4],
        "location_type": "wilderness",
        "items": {"medicinal_mud": {"quantity": 1, "value": 15}, "sulfur_crystal": {"quantity": 1, "value": 12}},
        "exits": {
            "north": {"target": "cinder_lava_cinder_lake", "type": "direction"},
            "east": {"target": "cinder_lava_ember_pit", "type": "direction"}
        }
    }

    rooms["cinder_lava_uplands"] = {
        "id": "cinder_lava_uplands",
        "name": "Volcanic Uplands",
        "description": "Higher ground above the main lava fields, offering commanding views "
                       "of the rivers of molten rock below. The terrain is rugged but walkable, "
                       "with outcrops of volcanic glass catching the firelight. Warm updrafts "
                       "carry ash and the smell of brimstone.",
        "coordinates": [cx + 1, cy + 7],
        "location_type": "wilderness",
        "items": {"volcanic_glass_chunk": {"quantity": 1, "value": 15}, "brimstone_fragment": {"quantity": 1, "value": 10}},
        "exits": {
            "south": {"target": "cinder_lava_scorched_ridge", "type": "direction"},
            "east": {"target": "cinder_lava_thermal_vista", "type": "direction"}
        }
    }

    rooms["cinder_lava_thermal_vista"] = {
        "id": "cinder_lava_thermal_vista",
        "name": "Thermal Vista Point",
        "description": "The highest point of the lava fields, where you can see the full scope "
                       "of Cinderforge's volcanic landscape. Rivers of lava, obsidian canyons, "
                       "and the great volcano itself spread before you like a painting in fire "
                       "and shadow. A stone cairn marks this as a place of significance.",
        "coordinates": [cx + 2, cy + 7],
        "location_type": "wilderness",
        "items": {"thermal_vista_sketch": {"quantity": 1, "value": 8}},
        "exits": {
            "west": {"target": "cinder_lava_uplands", "type": "direction"}
        }
    }

    # --- Expanded Obsidian Canyons (+6 rooms) ---

    rooms["cinder_obsidian_deep_canyon"] = {
        "id": "cinder_obsidian_deep_canyon",
        "name": "Deep Obsidian Canyon",
        "description": "Beyond the mineral vein, the canyon plunges deeper into the earth. "
                       "The obsidian walls become perfectly glass-like, reflecting distorted "
                       "images. Veins of gold and copper gleam in the volcanic glass. The air "
                       "grows warmer with each step deeper.",
        "coordinates": [cx + 3, cy + 6],
        "location_type": "wilderness",
        "items": {"deep_obsidian_shard": {"quantity": 1, "value": 28}, "copper_vein_sample": {"quantity": 1, "value": 15}},
        "exits": {
            "west": {"target": "cinder_obsidian_vein", "type": "direction"},
            "north": {"target": "cinder_obsidian_echo_gallery", "type": "direction"},
            "east": {"target": "cinder_obsidian_lava_bridge", "type": "direction"}
        }
    }

    rooms["cinder_obsidian_echo_gallery"] = {
        "id": "cinder_obsidian_echo_gallery",
        "name": "Echo Gallery",
        "description": "A long corridor of perfectly smooth obsidian that creates extraordinary "
                       "echoes. Every footstep reverberates for seconds, and whispers carry "
                       "from one end to the other with crystal clarity. Ancient writings on the "
                       "walls suggest this was once a place of ceremony.",
        "coordinates": [cx + 3, cy + 7],
        "location_type": "wilderness",
        "items": {"obsidian_inscription_rubbing": {"quantity": 1, "value": 20}, "echo_crystal": {"quantity": 1, "value": 18}},
        "exits": {
            "south": {"target": "cinder_obsidian_deep_canyon", "type": "direction"},
            "west": {"target": "cinder_obsidian_entrance", "type": "direction"}
        }
    }

    rooms["cinder_obsidian_lava_bridge"] = {
        "id": "cinder_obsidian_lava_bridge",
        "name": "Obsidian Lava Bridge",
        "description": "A natural bridge of obsidian spans a deep fissure filled with sluggishly "
                       "flowing lava. The bridge is barely wide enough for one person, and the "
                       "heat from below makes the air shimmer. Crossing requires steady nerves "
                       "and careful steps.",
        "coordinates": [cx + 4, cy + 6],
        "location_type": "wilderness",
        "items": {"heat_mirage_crystal": {"quantity": 1, "value": 22}},
        "exits": {
            "west": {"target": "cinder_obsidian_deep_canyon", "type": "direction"},
            "east": {"target": "cinder_obsidian_crystal_chamber", "type": "direction"}
        }
    }

    rooms["cinder_obsidian_crystal_chamber"] = {
        "id": "cinder_obsidian_crystal_chamber",
        "name": "Obsidian Crystal Chamber",
        "description": "A spherical chamber where obsidian has crystallized into enormous "
                       "geometric formations — perfect cubes, pyramids, and prisms of volcanic "
                       "glass. Light enters through a crack above, creating a dazzling display "
                       "of reflections that paint the walls with fire.",
        "coordinates": [cx + 5, cy + 6],
        "location_type": "wilderness",
        "items": {"obsidian_prism": {"quantity": 1, "value": 35}, "light_crystal": {"quantity": 1, "value": 20}},
        "exits": {
            "west": {"target": "cinder_obsidian_lava_bridge", "type": "direction"},
            "north": {"target": "cinder_obsidian_underground_river", "type": "direction"}
        }
    }

    rooms["cinder_obsidian_underground_river"] = {
        "id": "cinder_obsidian_underground_river",
        "name": "Underground Lava River",
        "description": "A massive underground cavern where a river of molten lava flows through "
                       "a channel carved into the obsidian bedrock. The light from the lava casts "
                       "the entire chamber in hellish orange-red. A narrow ledge follows the "
                       "river upstream.",
        "coordinates": [cx + 5, cy + 7],
        "location_type": "wilderness",
        "items": {"lava_river_stone": {"quantity": 1, "value": 18}, "obsidian_river_glass": {"quantity": 1, "value": 25}},
        "exits": {
            "south": {"target": "cinder_obsidian_crystal_chamber", "type": "direction"},
            "west": {"target": "cinder_obsidian_ancient_altar", "type": "direction"}
        }
    }

    rooms["cinder_obsidian_ancient_altar"] = {
        "id": "cinder_obsidian_ancient_altar",
        "name": "Ancient Obsidian Altar",
        "description": "At the deepest point of the expanded canyon, an altar of polished "
                       "obsidian stands before a wall carved with depictions of fire worship. "
                       "The altar radiates unnatural heat, and offerings placed upon it smolder "
                       "and then vanish. This was clearly a place of great power.",
        "coordinates": [cx + 4, cy + 7],
        "location_type": "wilderness",
        "items": {"obsidian_altar_shard": {"quantity": 1, "value": 45}, "fire_worship_glyph": {"quantity": 1, "value": 30}},
        "exits": {
            "east": {"target": "cinder_obsidian_underground_river", "type": "direction"},
            "south": {"target": "cinder_obsidian_lava_bridge", "type": "direction"}
        }
    }

    # --- Expanded Ancient Forges (+5 rooms) ---

    rooms["cinder_forge_testing_ground"] = {
        "id": "cinder_forge_testing_ground",
        "name": "Weapon Testing Ground",
        "description": "A reinforced chamber east of the smelter where newly forged weapons "
                       "are tested against volcanic stone targets. Scars from countless impacts "
                       "pit the walls. A master at arms evaluates each weapon's balance, edge, "
                       "and heat resistance.",
        "coordinates": [cx + 3, cy + 8],
        "location_type": "building",
        "items": {"test_target_fragment": {"quantity": 1, "value": 8}, "arms_master_notes": {"quantity": 1, "value": 15}},
        "exits": {
            "west": {"target": "cinder_forge_smelter", "type": "direction"},
            "north": {"target": "cinder_forge_trophy_hall", "type": "direction"}
        }
    }

    rooms["cinder_forge_trophy_hall"] = {
        "id": "cinder_forge_trophy_hall",
        "name": "Forge Trophy Hall",
        "description": "A display hall showcasing the legendary weapons crafted in Cinderforge's "
                       "history. Behind glass cases of heat-resistant crystal, blades of black "
                       "obsidian and glowing red stormsteel rest on velvet cushions. Each piece "
                       "has a nameplate telling tales of the heroes who wielded them.",
        "coordinates": [cx + 3, cy + 9],
        "location_type": "building",
        "items": {"forge_legend_book": {"quantity": 1, "value": 20}, "display_crystal_shard": {"quantity": 1, "value": 12}},
        "exits": {
            "south": {"target": "cinder_forge_testing_ground", "type": "direction"}
        }
    }

    rooms["cinder_forge_outpost"] = {
        "id": "cinder_forge_outpost",
        "name": "Western Forge Outpost",
        "description": "A fortified outpost west of the main forge complex, guarding against "
                       "incursions from the ash wastes. A small garrison maintains a constant "
                       "watch, and emergency supplies are stockpiled in fireproof containers. "
                       "A signal fire on the roof can summon reinforcements.",
        "coordinates": [cx - 2, cy + 7],
        "location_type": "building",
        "items": {"outpost_rations": {"quantity": 2, "value": 5}, "signal_fire_kit": {"quantity": 1, "value": 15}},
        "exits": {
            "east": {"target": "cinder_forge_guard_post", "type": "direction"},
            "south": {"target": "cinder_forge_coal_pit", "type": "direction"}
        }
    }

    rooms["cinder_forge_coal_pit"] = {
        "id": "cinder_forge_coal_pit",
        "name": "Volcanic Coal Pit",
        "description": "A deep pit where volcanic coal is mined for the forges. The coal here "
                       "burns twice as hot as normal coal, making it essential for working "
                       "volcanic metals. Miners work in shifts, the heat so intense that each "
                       "shift lasts only an hour.",
        "coordinates": [cx - 2, cy + 6],
        "location_type": "wilderness",
        "items": {"volcanic_coal": {"quantity": 3, "value": 8}, "mining_canary_cage": {"quantity": 1, "value": 10}},
        "exits": {
            "north": {"target": "cinder_forge_outpost", "type": "direction"},
            "east": {"target": "cinder_forge_rail_track", "type": "direction"}
        }
    }

    rooms["cinder_forge_rail_track"] = {
        "id": "cinder_forge_rail_track",
        "name": "Ore Cart Rail Track",
        "description": "A network of iron rail tracks connecting the coal pit to the forges. "
                       "Small carts loaded with volcanic coal and raw ore rattle along the "
                       "tracks, pushed by apprentices. The rails glow faintly from the heat "
                       "of the loads they carry.",
        "coordinates": [cx - 1, cy + 6],
        "location_type": "building",
        "items": {"ore_cart_wheel": {"quantity": 1, "value": 8}, "iron_rail_spike": {"quantity": 2, "value": 4}},
        "exits": {
            "west": {"target": "cinder_forge_coal_pit", "type": "direction"},
            "north": {"target": "cinder_forge_guard_post", "type": "direction"}
        }
    }

    # --- Expanded Ash Wastes (+7 rooms) ---

    rooms["cinder_ash_deep_wastes"] = {
        "id": "cinder_ash_deep_wastes",
        "name": "Deep Ash Wastes",
        "description": "The ash wastes deepen here, the gray powder drifting to knee height "
                       "in places. Visibility drops to mere feet during ash storms. Tracks in "
                       "the ash suggest something large patrols this desolate region. The "
                       "silence is oppressive and absolute.",
        "coordinates": [cx - 4, cy + 3],
        "location_type": "wilderness",
        "items": {"ash_sample_jar": {"quantity": 1, "value": 5}, "deep_waste_map": {"quantity": 1, "value": 15}},
        "exits": {
            "east": {"target": "cinder_ash_graveyard", "type": "direction"},
            "south": {"target": "cinder_ash_fossil_ridge", "type": "direction"},
            "north": {"target": "cinder_ash_wind_corridor", "type": "direction"}
        }
    }

    rooms["cinder_ash_fossil_ridge"] = {
        "id": "cinder_ash_fossil_ridge",
        "name": "Fossil Ridge",
        "description": "A ridge of exposed rock where ancient fossils emerge from beneath the "
                       "ash. The remains of creatures from before the volcanic age are preserved "
                       "in exquisite detail — giant insects, primitive reptiles, and plants that "
                       "no longer exist.",
        "coordinates": [cx - 4, cy + 2],
        "location_type": "wilderness",
        "items": {"ancient_insect_fossil": {"quantity": 1, "value": 22}, "pre_volcanic_fern_fossil": {"quantity": 1, "value": 18}},
        "exits": {
            "north": {"target": "cinder_ash_deep_wastes", "type": "direction"},
            "east": {"target": "cinder_ash_collapsed_tower", "type": "direction"},
            "south": {"target": "cinder_ash_buried_village", "type": "direction"}
        }
    }

    rooms["cinder_ash_buried_village"] = {
        "id": "cinder_ash_buried_village",
        "name": "Buried Village",
        "description": "The remains of a village buried by a catastrophic eruption centuries ago. "
                       "Rooftops poke through the ash like gravestones, and entering through "
                       "upper windows reveals rooms frozen in time — meals on tables, tools by "
                       "workbenches, all preserved under ash.",
        "coordinates": [cx - 4, cy + 1],
        "location_type": "wilderness",
        "items": {"preserved_meal": {"quantity": 1, "value": 10}, "buried_village_relic": {"quantity": 1, "value": 30}},
        "exits": {
            "north": {"target": "cinder_ash_fossil_ridge", "type": "direction"},
            "east": {"target": "cinder_ash_crypt_entrance", "type": "direction"}
        }
    }

    rooms["cinder_ash_crypt_entrance"] = {
        "id": "cinder_ash_crypt_entrance",
        "name": "Ash Crypt Entrance",
        "description": "A doorway descending into the earth, its stone frame carved with warnings "
                       "in a forgotten language. The stairs within are coated in fine ash, and "
                       "footprints show that something frequently comes and goes. A foul wind "
                       "rises from below.",
        "coordinates": [cx - 3, cy + 1],
        "location_type": "wilderness",
        "items": {"crypt_warning_inscription": {"quantity": 1, "value": 15}},
        "exits": {
            "west": {"target": "cinder_ash_buried_village", "type": "direction"},
            "south": {"target": "cinder_ash_crypt_depths", "type": "direction"}
        }
    }

    rooms["cinder_ash_crypt_depths"] = {
        "id": "cinder_ash_crypt_depths",
        "name": "Ash Crypt Depths",
        "description": "The crypt extends deep under the ash wastes, its walls lined with "
                       "sealed urns containing the ashes of the dead. The air is dry and hot, "
                       "and strange markings glow faintly on the walls. An altar at the far "
                       "end holds offerings of obsidian and fire opals.",
        "coordinates": [cx - 3, cy],
        "location_type": "wilderness",
        "items": {"crypt_urn": {"quantity": 1, "value": 20}, "crypt_fire_opal": {"quantity": 1, "value": 35}},
        "exits": {
            "north": {"target": "cinder_ash_crypt_entrance", "type": "direction"}
        }
    }

    rooms["cinder_ash_wind_corridor"] = {
        "id": "cinder_ash_wind_corridor",
        "name": "Wind Corridor",
        "description": "Channeled between two ridges of volcanic rock, the wind here reaches "
                       "gale force, carrying cutting particles of ash and obsidian. Travel is "
                       "only possible during brief lulls. The constant scouring has polished "
                       "the rock to a glass-like smoothness.",
        "coordinates": [cx - 4, cy + 4],
        "location_type": "wilderness",
        "items": {"wind_polished_stone": {"quantity": 1, "value": 12}, "obsidian_dust": {"quantity": 2, "value": 6}},
        "exits": {
            "south": {"target": "cinder_ash_deep_wastes", "type": "direction"},
            "east": {"target": "cinder_ash_bone_field", "type": "direction"},
            "north": {"target": "cinder_ash_sentinel_stone", "type": "direction"}
        }
    }

    rooms["cinder_ash_sentinel_stone"] = {
        "id": "cinder_ash_sentinel_stone",
        "name": "Sentinel Stone",
        "description": "A massive standing stone, black as obsidian, reaching twice the height "
                       "of a person. It stands alone in the ash wastes like a sentinel. Ancient "
                       "runes carved into its surface glow red during volcanic eruptions. Some "
                       "believe it is a waymarker left by the island's first inhabitants.",
        "coordinates": [cx - 4, cy + 5],
        "location_type": "wilderness",
        "items": {"sentinel_rune_rubbing": {"quantity": 1, "value": 25}, "volcanic_obsidian_chip": {"quantity": 1, "value": 10}},
        "exits": {
            "south": {"target": "cinder_ash_wind_corridor", "type": "direction"}
        }
    }

    # --- Expanded Volcano Core (+4 rooms) ---

    rooms["cinder_volcano_crystal_caves"] = {
        "id": "cinder_volcano_crystal_caves",
        "name": "Crystal Caves",
        "description": "Accessed through a crack in the volcano's western face, these caves "
                       "are a wonderland of fire crystals. Formations of ruby-red, amber, and "
                       "molten-gold crystals grow from every surface. The deepest crystals pulse "
                       "with volcanic heat, warm to the touch.",
        "coordinates": [cx - 2, cy + 13],
        "location_type": "wilderness",
        "items": {"ruby_fire_crystal": {"quantity": 1, "value": 40}, "amber_lava_crystal": {"quantity": 1, "value": 30}},
        "exits": {
            "east": {"target": "cinder_volcano_crystal_vent", "type": "direction"},
            "west": {"target": "cinder_volcano_hidden_chamber", "type": "direction"},
            "south": {"target": "cinder_volcano_geode_gallery", "type": "direction"}
        }
    }

    rooms["cinder_volcano_hidden_chamber"] = {
        "id": "cinder_volcano_hidden_chamber",
        "name": "Hidden Volcanic Chamber",
        "description": "A perfectly sealed chamber within the volcano, untouched for millennia. "
                       "The walls are smooth obsidian, and the air is thick with sulfur. At the "
                       "center, a pedestal of volcanic glass holds an artifact that radiates "
                       "intense heat — the Ember Heart.",
        "coordinates": [cx - 3, cy + 13],
        "location_type": "wilderness",
        "items": {"ember_heart_fragment": {"quantity": 1, "value": 75}, "sealed_chamber_air": {"quantity": 1, "value": 20}},
        "exits": {
            "east": {"target": "cinder_volcano_crystal_caves", "type": "direction"}
        }
    }

    rooms["cinder_volcano_geode_gallery"] = {
        "id": "cinder_volcano_geode_gallery",
        "name": "Geode Gallery",
        "description": "A passage through the volcano where enormous geodes have been split "
                       "open by tectonic forces, revealing crystalline interiors of breathtaking "
                       "beauty. Each geode is a different color — amethyst, citrine, obsidian, "
                       "and a fiery red crystal found nowhere else.",
        "coordinates": [cx - 2, cy + 12],
        "location_type": "wilderness",
        "items": {"fire_geode_half": {"quantity": 1, "value": 35}, "citrine_cluster": {"quantity": 1, "value": 22}},
        "exits": {
            "north": {"target": "cinder_volcano_crystal_caves", "type": "direction"},
            "east": {"target": "cinder_volcano_approach", "type": "direction"}
        }
    }

    rooms["cinder_volcano_steam_vents"] = {
        "id": "cinder_volcano_steam_vents",
        "name": "Steam Vent Network",
        "description": "A maze of volcanic steam vents on the volcano's eastern slope. Jets of "
                       "superheated steam blast from cracks in the rock at unpredictable intervals. "
                       "Navigating requires patience and careful observation of pressure "
                       "patterns. The steam carries dissolved minerals that leave colorful "
                       "deposits on the surrounding rock.",
        "coordinates": [cx + 2, cy + 14],
        "location_type": "wilderness",
        "items": {"steam_deposit_sample": {"quantity": 1, "value": 15}, "volcanic_steam_flask": {"quantity": 1, "value": 12}},
        "exits": {
            "west": {"target": "cinder_volcano_inner_descent", "type": "direction"}
        }
    }

    # === NEW SUB-REGION: Ember Tunnels (18 rooms) ===

    rooms["cinder_tunnel_entrance"] = {
        "id": "cinder_tunnel_entrance",
        "name": "Ember Tunnel Entrance",
        "description": "A yawning tunnel mouth exhaling hot air from the island's volcanic heart. "
                       "The walls glow faintly with embedded embers, providing dim but steady "
                       "illumination. Ancient pick marks show this tunnel was widened by miners "
                       "long ago.",
        "coordinates": [cx + 1, cy + 11],
        "location_type": "wilderness",
        "items": {"ember_wall_chip": {"quantity": 1, "value": 10}},
        "exits": {
            "west": {"target": "cinder_forge_abandoned_tunnel", "type": "direction"},
            "east": {"target": "cinder_tunnel_crossroads", "type": "direction"}
        }
    }

    rooms["cinder_tunnel_crossroads"] = {
        "id": "cinder_tunnel_crossroads",
        "name": "Tunnel Crossroads",
        "description": "A junction where four tunnels meet in a domed chamber. The ceiling is "
                       "high enough to echo, and directional markers are carved into the walls, "
                       "though centuries of heat have warped them almost beyond recognition. "
                       "A faint draft comes from the eastern passage.",
        "coordinates": [cx + 2, cy + 11],
        "location_type": "wilderness",
        "items": {"directional_marker_stone": {"quantity": 1, "value": 8}},
        "exits": {
            "west": {"target": "cinder_tunnel_entrance", "type": "direction"},
            "east": {"target": "cinder_tunnel_lava_flow", "type": "direction"},
            "north": {"target": "cinder_tunnel_mushroom_farm", "type": "direction"},
            "south": {"target": "cinder_tunnel_mine_shaft", "type": "direction"}
        }
    }

    rooms["cinder_tunnel_lava_flow"] = {
        "id": "cinder_tunnel_lava_flow",
        "name": "Lava Flow Tunnel",
        "description": "A tunnel following the path of an ancient lava flow. The solidified "
                       "magma forms smooth, rope-like patterns on the floor. In places, the "
                       "rock is still warm, and thin streams of molten rock seep through "
                       "cracks in the walls.",
        "coordinates": [cx + 3, cy + 11],
        "location_type": "wilderness",
        "items": {"pahoehoe_sample": {"quantity": 1, "value": 12}, "lava_seep_vial": {"quantity": 1, "value": 18}},
        "exits": {
            "west": {"target": "cinder_tunnel_crossroads", "type": "direction"},
            "east": {"target": "cinder_tunnel_sulfur_cavern", "type": "direction"},
            "north": {"target": "cinder_tunnel_crystal_pocket", "type": "direction"}
        }
    }

    rooms["cinder_tunnel_sulfur_cavern"] = {
        "id": "cinder_tunnel_sulfur_cavern",
        "name": "Sulfur Cavern",
        "description": "A cavern coated in brilliant yellow sulfur crystals. The air is thick "
                       "with acrid fumes that burn the eyes and throat. Despite the hostile "
                       "conditions, rare fire beetles thrive here, their carapaces gleaming "
                       "with sulfuric deposits.",
        "coordinates": [cx + 4, cy + 11],
        "location_type": "wilderness",
        "items": {"sulfur_crystal_cluster": {"quantity": 1, "value": 20}, "fire_beetle_carapace": {"quantity": 1, "value": 25}},
        "exits": {
            "west": {"target": "cinder_tunnel_lava_flow", "type": "direction"},
            "north": {"target": "cinder_tunnel_thermal_shaft", "type": "direction"}
        }
    }

    rooms["cinder_tunnel_mushroom_farm"] = {
        "id": "cinder_tunnel_mushroom_farm",
        "name": "Underground Mushroom Farm",
        "description": "In a cooler section of the tunnels, someone has cultivated a thriving "
                       "mushroom farm. Giant fire-cap mushrooms grow in beds of volcanic soil, "
                       "their caps glowing dull red. A hermit farmer tends them, trading rare "
                       "varieties for supplies from above.",
        "coordinates": [cx + 2, cy + 12],
        "location_type": "settlement",
        "items": {"fire_cap_mushroom": {"quantity": 3, "value": 8}, "volcanic_soil_compost": {"quantity": 1, "value": 10}},
        "exits": {
            "south": {"target": "cinder_tunnel_crossroads", "type": "direction"},
            "east": {"target": "cinder_tunnel_crystal_pocket", "type": "direction"},
            "north": {"target": "cinder_tunnel_hot_spring", "type": "direction"}
        }
    }

    rooms["cinder_tunnel_crystal_pocket"] = {
        "id": "cinder_tunnel_crystal_pocket",
        "name": "Crystal Pocket",
        "description": "A natural pocket in the volcanic rock filled with stunning crystal "
                       "formations. Fire opals, garnets, and a rare volcanic diamond catch the "
                       "light from glowing embers in the walls. Miners once fought fiercely over "
                       "claims to pockets like this.",
        "coordinates": [cx + 3, cy + 12],
        "location_type": "wilderness",
        "items": {"volcanic_diamond_rough": {"quantity": 1, "value": 60}, "fire_garnet": {"quantity": 2, "value": 20}},
        "exits": {
            "south": {"target": "cinder_tunnel_lava_flow", "type": "direction"},
            "west": {"target": "cinder_tunnel_mushroom_farm", "type": "direction"},
            "east": {"target": "cinder_tunnel_thermal_shaft", "type": "direction"}
        }
    }

    rooms["cinder_tunnel_thermal_shaft"] = {
        "id": "cinder_tunnel_thermal_shaft",
        "name": "Thermal Shaft",
        "description": "A vertical shaft where hot air rushes upward with tremendous force. "
                       "The shaft connects deep volcanic chambers to the surface, creating a "
                       "natural chimney effect. Ledges spiral around the shaft's interior, "
                       "providing a dizzying path downward.",
        "coordinates": [cx + 4, cy + 12],
        "location_type": "wilderness",
        "items": {"thermal_draft_crystal": {"quantity": 1, "value": 18}},
        "exits": {
            "south": {"target": "cinder_tunnel_sulfur_cavern", "type": "direction"},
            "west": {"target": "cinder_tunnel_crystal_pocket", "type": "direction"},
            "north": {"target": "cinder_tunnel_lava_lake", "type": "direction"}
        }
    }

    rooms["cinder_tunnel_mine_shaft"] = {
        "id": "cinder_tunnel_mine_shaft",
        "name": "Old Mine Shaft",
        "description": "A reinforced mine shaft descending at a steep angle into the earth. "
                       "Rusted iron tracks for ore carts line the floor, and timbers blackened "
                       "by age and heat shore up the ceiling. The deepest levels were abandoned "
                       "when they broke through into a magma pocket.",
        "coordinates": [cx + 2, cy + 10],
        "location_type": "wilderness",
        "items": {"rusted_ore_cart": {"quantity": 1, "value": 12}, "mine_shaft_map": {"quantity": 1, "value": 15}},
        "exits": {
            "north": {"target": "cinder_tunnel_crossroads", "type": "direction"},
            "east": {"target": "cinder_tunnel_collapsed_gallery", "type": "direction"},
            "west": {"target": "cinder_forge_deep_shaft", "type": "direction"}
        }
    }

    rooms["cinder_tunnel_collapsed_gallery"] = {
        "id": "cinder_tunnel_collapsed_gallery",
        "name": "Collapsed Gallery",
        "description": "A once-grand mining gallery partially collapsed by seismic activity. "
                       "Rubble fills half the chamber, but the remaining space reveals walls "
                       "studded with valuable ore. Unstable ground and occasional tremors make "
                       "lingering here dangerous.",
        "coordinates": [cx + 3, cy + 10],
        "location_type": "wilderness",
        "items": {"exposed_ore_vein": {"quantity": 1, "value": 25}, "unstable_rock_sample": {"quantity": 1, "value": 5}},
        "exits": {
            "west": {"target": "cinder_tunnel_mine_shaft", "type": "direction"},
            "north": {"target": "cinder_tunnel_lava_flow", "type": "direction"}
        }
    }

    rooms["cinder_tunnel_hot_spring"] = {
        "id": "cinder_tunnel_hot_spring",
        "name": "Underground Hot Spring",
        "description": "A beautiful underground hot spring fed by volcanic water sources. The "
                       "water is clear and tinged blue by dissolved minerals. Steam fills the "
                       "chamber, and the temperature is pleasantly warm. Miners once used this "
                       "as a rest area during long shifts.",
        "coordinates": [cx + 2, cy + 13],
        "location_type": "wilderness",
        "items": {"mineral_hot_water": {"quantity": 1, "value": 10}, "volcanic_bath_crystal": {"quantity": 1, "value": 15}},
        "exits": {
            "south": {"target": "cinder_tunnel_mushroom_farm", "type": "direction"},
            "east": {"target": "cinder_tunnel_forge_remnant", "type": "direction"},
            "west": {"target": "cinder_volcano_crystal_vent", "type": "direction"}
        }
    }

    rooms["cinder_tunnel_forge_remnant"] = {
        "id": "cinder_tunnel_forge_remnant",
        "name": "Ancient Forge Remnant",
        "description": "The remains of a forge even older than the ones above — built directly "
                       "into the volcanic rock. The anvil is carved from a single piece of "
                       "obsidian, and the furnace uses raw magma channeled from below. Whatever "
                       "civilization built this was far more advanced than expected.",
        "coordinates": [cx + 3, cy + 13],
        "location_type": "wilderness",
        "items": {"ancient_obsidian_anvil_chip": {"quantity": 1, "value": 40}, "proto_forge_blueprint": {"quantity": 1, "value": 30}},
        "exits": {
            "west": {"target": "cinder_tunnel_hot_spring", "type": "direction"},
            "north": {"target": "cinder_tunnel_magma_window", "type": "direction"}
        }
    }

    rooms["cinder_tunnel_lava_lake"] = {
        "id": "cinder_tunnel_lava_lake",
        "name": "Underground Lava Lake",
        "description": "The tunnels open onto a vast underground lake of molten lava. The heat "
                       "is staggering, and the air shimmers with thermal distortion. Islands of "
                       "cooled rock float on the surface, slowly melting. The cavern ceiling "
                       "glows red from reflected light.",
        "coordinates": [cx + 4, cy + 13],
        "location_type": "wilderness",
        "items": {"lava_lake_stone": {"quantity": 1, "value": 20}, "floating_obsidian": {"quantity": 1, "value": 25}},
        "exits": {
            "south": {"target": "cinder_tunnel_thermal_shaft", "type": "direction"},
            "west": {"target": "cinder_tunnel_forge_remnant", "type": "direction"},
            "north": {"target": "cinder_tunnel_fire_spirit_den", "type": "direction"}
        }
    }

    rooms["cinder_tunnel_magma_window"] = {
        "id": "cinder_tunnel_magma_window",
        "name": "Magma Window",
        "description": "A viewing chamber with a wall of heat-resistant crystal looking directly "
                       "into a flowing magma channel. The crystal is some unknown material — "
                       "completely transparent and cool to the touch despite the hellish view "
                       "beyond. An ancient observation post for studying volcanism.",
        "coordinates": [cx + 3, cy + 14],
        "location_type": "wilderness",
        "items": {"magma_window_crystal_chip": {"quantity": 1, "value": 50}, "volcanic_observation_notes": {"quantity": 1, "value": 20}},
        "exits": {
            "south": {"target": "cinder_tunnel_forge_remnant", "type": "direction"},
            "east": {"target": "cinder_tunnel_fire_spirit_den", "type": "direction"}
        }
    }

    rooms["cinder_tunnel_fire_spirit_den"] = {
        "id": "cinder_tunnel_fire_spirit_den",
        "name": "Fire Spirit Den",
        "description": "The deepest chamber of the ember tunnels, where fire spirits are said "
                       "to dwell. The air itself seems alive with dancing flames that move with "
                       "purpose and intelligence. The temperature fluctuates wildly — freezing "
                       "one moment, searing the next. An altar of pure flame burns eternally "
                       "at the center.",
        "coordinates": [cx + 4, cy + 14],
        "location_type": "wilderness",
        "items": {"fire_spirit_essence": {"quantity": 1, "value": 80}, "eternal_flame_ember": {"quantity": 1, "value": 60}},
        "exits": {
            "south": {"target": "cinder_tunnel_lava_lake", "type": "direction"},
            "west": {"target": "cinder_tunnel_magma_window", "type": "direction"}
        }
    }

    rooms["cinder_tunnel_ember_shrine"] = {
        "id": "cinder_tunnel_ember_shrine",
        "name": "Ember Shrine",
        "description": "A sacred shrine hidden deep within the tunnel network, dedicated to the "
                       "primordial fire that burns at the island's core. Offerings of obsidian "
                       "and fire opals surround an altar that is always warm to the touch. "
                       "Pilgrims from the village occasionally make the dangerous journey here.",
        "coordinates": [cx + 1, cy + 10],
        "location_type": "building",
        "items": {"ember_shrine_blessing": {"quantity": 1, "value": 30}, "pilgrim_fire_opal": {"quantity": 1, "value": 35}},
        "exits": {
            "east": {"target": "cinder_tunnel_mine_shaft", "type": "direction"},
            "north": {"target": "cinder_tunnel_entrance", "type": "direction"}
        }
    }

    # === NEW SUB-REGION: Cinderspine Ridge (13 rooms) ===

    rooms["cinder_ridge_base"] = {
        "id": "cinder_ridge_base",
        "name": "Cinderspine Ridge Base",
        "description": "The base of a jagged volcanic ridge that runs like a spine across the "
                       "island's northern reaches. The rock here is a mix of obsidian and pumice, "
                       "creating a striking black-and-white landscape. A trail of volcanic glass "
                       "shards marks the path upward.",
        "coordinates": [cx - 1, cy + 8],
        "location_type": "wilderness",
        "items": {"pumice_stone": {"quantity": 2, "value": 4}, "volcanic_glass_trail_marker": {"quantity": 1, "value": 8}},
        "exits": {
            "south": {"target": "cinder_forge_gate", "type": "direction"},
            "north": {"target": "cinder_ridge_lower_slope", "type": "direction"},
            "east": {"target": "cinder_ridge_east_approach", "type": "direction"}
        }
    }

    rooms["cinder_ridge_east_approach"] = {
        "id": "cinder_ridge_east_approach",
        "name": "Eastern Approach",
        "description": "An approach to the ridge from the east, skirting the edges of the ash "
                       "wastes. The contrast between the dark ridge and the gray ash creates "
                       "an otherworldly landscape. Cinder cones dot the terrain, some still "
                       "venting wisps of steam.",
        "coordinates": [cx, cy + 8],
        "location_type": "wilderness",
        "items": {"cinder_cone_sample": {"quantity": 1, "value": 10}},
        "exits": {
            "west": {"target": "cinder_ridge_base", "type": "direction"},
            "south": {"target": "cinder_forge_main_hall", "type": "direction"}
        }
    }

    rooms["cinder_ridge_lower_slope"] = {
        "id": "cinder_ridge_lower_slope",
        "name": "Lower Ridge Slope",
        "description": "The lower slopes of the Cinderspine Ridge, where tough volcanic grasses "
                       "and fire-resistant shrubs cling to the rock. The footing is treacherous "
                       "on the loose scree, and small avalanches of pumice are a constant "
                       "hazard.",
        "coordinates": [cx - 1, cy + 9],
        "location_type": "wilderness",
        "items": {"volcanic_scrub": {"quantity": 1, "value": 4}, "scree_sample": {"quantity": 1, "value": 5}},
        "exits": {
            "south": {"target": "cinder_ridge_base", "type": "direction"},
            "north": {"target": "cinder_ridge_switchback", "type": "direction"},
            "east": {"target": "cinder_ridge_hot_vent", "type": "direction"}
        }
    }

    rooms["cinder_ridge_hot_vent"] = {
        "id": "cinder_ridge_hot_vent",
        "name": "Ridgeside Hot Vent",
        "description": "A cluster of volcanic vents on the ridge's eastern face, blasting "
                       "superheated air in rhythmic pulses. The surrounding rock is stained "
                       "bright yellow and orange by mineral deposits. Small fire lizards bask "
                       "near the warmest vents.",
        "coordinates": [cx, cy + 9],
        "location_type": "wilderness",
        "items": {"fire_lizard_scale": {"quantity": 1, "value": 15}, "vent_mineral_deposit": {"quantity": 1, "value": 12}},
        "exits": {
            "west": {"target": "cinder_ridge_lower_slope", "type": "direction"},
            "north": {"target": "cinder_ridge_lookout", "type": "direction"}
        }
    }

    rooms["cinder_ridge_switchback"] = {
        "id": "cinder_ridge_switchback",
        "name": "Ridge Switchback Trail",
        "description": "A zigzagging trail carved into the ridge face, providing the only safe "
                       "route to the upper reaches. Each switchback offers expanding views of "
                       "the volcanic landscape below. Cairns of balanced obsidian mark the path.",
        "coordinates": [cx - 1, cy + 10],
        "location_type": "wilderness",
        "items": {"obsidian_cairn_stone": {"quantity": 1, "value": 8}},
        "exits": {
            "south": {"target": "cinder_ridge_lower_slope", "type": "direction"},
            "north": {"target": "cinder_ridge_summit_path", "type": "direction"},
            "east": {"target": "cinder_ridge_lookout", "type": "direction"}
        }
    }

    rooms["cinder_ridge_lookout"] = {
        "id": "cinder_ridge_lookout",
        "name": "Ridge Lookout",
        "description": "A natural platform partway up the ridge offering panoramic views in all "
                       "directions. The obsidian canyons, lava fields, ash wastes, and volcano "
                       "are all visible from here. On clear days, other islands can be spotted "
                       "on the horizon.",
        "coordinates": [cx, cy + 10],
        "location_type": "wilderness",
        "items": {"panoramic_sketch": {"quantity": 1, "value": 10}},
        "exits": {
            "south": {"target": "cinder_ridge_hot_vent", "type": "direction"},
            "west": {"target": "cinder_ridge_switchback", "type": "direction"}
        }
    }

    rooms["cinder_ridge_summit_path"] = {
        "id": "cinder_ridge_summit_path",
        "name": "Summit Path",
        "description": "The final approach to the ridge summit, a knife-edge of rock with "
                       "precipitous drops on both sides. The wind is ferocious at this altitude, "
                       "carrying flecks of volcanic ash. Chains have been hammered into the rock "
                       "to provide handholds for the brave.",
        "coordinates": [cx - 1, cy + 11],
        "location_type": "wilderness",
        "items": {"summit_chain_link": {"quantity": 1, "value": 8}},
        "exits": {
            "south": {"target": "cinder_ridge_switchback", "type": "direction"},
            "north": {"target": "cinder_ridge_summit", "type": "direction"},
            "east": {"target": "cinder_ridge_eagle_nest", "type": "direction"}
        }
    }

    rooms["cinder_ridge_eagle_nest"] = {
        "id": "cinder_ridge_eagle_nest",
        "name": "Fire Eagle's Nest",
        "description": "A massive nest of charred branches and volcanic glass built on a ledge "
                       "just below the ridge summit. The fire eagles — magnificent birds with "
                       "ember-tipped feathers — soar on the volcanic thermals. Their abandoned "
                       "feathers are prized for their heat resistance.",
        "coordinates": [cx, cy + 11],
        "location_type": "wilderness",
        "items": {"fire_eagle_feather": {"quantity": 1, "value": 35}, "volcanic_glass_nest_piece": {"quantity": 1, "value": 15}},
        "exits": {
            "west": {"target": "cinder_ridge_summit_path", "type": "direction"}
        }
    }

    rooms["cinder_ridge_summit"] = {
        "id": "cinder_ridge_summit",
        "name": "Cinderspine Summit",
        "description": "The highest point of the Cinderspine Ridge, offering a breathtaking "
                       "view of the entire island. The volcano looms to the north, lava rivers "
                       "snake across the landscape below, and the sea glitters on the horizon. "
                       "An ancient stone marker bears inscriptions in a lost language.",
        "coordinates": [cx - 1, cy + 12],
        "location_type": "wilderness",
        "items": {"summit_stone_inscription": {"quantity": 1, "value": 30}, "cinderspine_peak_crystal": {"quantity": 1, "value": 45}},
        "exits": {
            "south": {"target": "cinder_ridge_summit_path", "type": "direction"},
            "north": {"target": "cinder_ridge_descent", "type": "direction"},
            "west": {"target": "cinder_ridge_wind_carved", "type": "direction"}
        }
    }

    rooms["cinder_ridge_wind_carved"] = {
        "id": "cinder_ridge_wind_carved",
        "name": "Wind-Carved Cavern",
        "description": "A cavern carved into the ridge by millennia of wind erosion. The walls "
                       "are sculpted into flowing curves and abstract shapes, polished smooth "
                       "by centuries of abrasion. The wind moans through the cavern's natural "
                       "channels, creating an eerie symphony.",
        "coordinates": [cx - 2, cy + 12],
        "location_type": "wilderness",
        "items": {"wind_carved_stone": {"quantity": 1, "value": 18}, "wind_flute_stone": {"quantity": 1, "value": 22}},
        "exits": {
            "east": {"target": "cinder_ridge_summit", "type": "direction"}
        }
    }

    rooms["cinder_ridge_descent"] = {
        "id": "cinder_ridge_descent",
        "name": "Northern Descent",
        "description": "The far side of the Cinderspine Ridge descends toward the volcano core "
                       "region. The descent is steep and covered in loose volcanic debris. From "
                       "here, the volcano's caldera is clearly visible, its rim glowing with "
                       "inner fire.",
        "coordinates": [cx - 1, cy + 13],
        "location_type": "wilderness",
        "items": {"volcanic_debris_sample": {"quantity": 1, "value": 8}},
        "exits": {
            "south": {"target": "cinder_ridge_summit", "type": "direction"},
            "east": {"target": "cinder_volcano_crystal_vent", "type": "direction"},
            "north": {"target": "cinder_ridge_fire_shrine", "type": "direction"}
        }
    }

    rooms["cinder_ridge_fire_shrine"] = {
        "id": "cinder_ridge_fire_shrine",
        "name": "Ridgetop Fire Shrine",
        "description": "At the ridge's northern terminus, a small shrine sits at the edge of "
                       "the volcanic zone. An eternal flame burns in a bowl of volcanic glass, "
                       "tended by no one yet never extinguishing. Offerings left by brave "
                       "climbers surround it — obsidian tokens, fire opals, and carved prayers.",
        "coordinates": [cx - 1, cy + 14],
        "location_type": "building",
        "items": {"eternal_shrine_flame_ember": {"quantity": 1, "value": 40}, "climber_prayer_token": {"quantity": 1, "value": 15}},
        "exits": {
            "south": {"target": "cinder_ridge_descent", "type": "direction"}
        }
    }


def generate_dreadmist_isle(rooms):
    """Generate Island 5: Dreadmist Isle - Fog-shrouded undead Gothic horror island (~75 rooms)."""

    cx, cy = -60, -10  # Center coordinates

    # =========================================================================
    # DREADMIST ISLE - Gothic Horror Island (Level 25+)
    # Sub-regions: Docks, Village, Haunted Forest, Cursed Graveyard,
    #              Spectral Marsh, Ruined Castle, Necropolis, Dark Ritual Sites
    # =========================================================================

    # --- Dreadmist Docks (3 rooms) ---

    rooms["dreadmist_docks"] = {
        "id": "dreadmist_docks",
        "name": "Dreadmist Isle - Bone Shore Dock",
        "description": "A decrepit dock of salt-blackened wood extends into murky waters choked with "
                       "perpetual fog. The pale sand is littered with bleached bones and washed-up "
                       "coffin lids. An eerie silence smothers everything, broken only by the distant "
                       "tolling of a bell no one seems to ring.",
        "coordinates": [cx, cy - 4],
        "location_type": "dock",
        "items": {},
        "exits": {
            "board mainland": {
                "target": "harbor_west_dock",
                "type": "boat_travel",
                "island_id": "dreadmist_isle",
                "display": "Return to Grand Harbor",
                "unlock_cost": 0,
                "fare_cost": 0,
                "min_level": 1,
                "transition_text": "You board the black-sailed vessel. The whispering fog parts reluctantly\nas the ship creeps away from the cursed shore. After six days of\nuneasy silence, the lanterns of Grand Harbor finally pierce the gloom..."
            },
            "north": {"target": "dreadmist_village_path", "type": "direction"},
            "east": {"target": "dreadmist_docks_cargo_wharf", "type": "direction"},
            "west": {"target": "dreadmist_docks_lantern_tower", "type": "direction"}
        }
    }

    rooms["dreadmist_docks_cargo_wharf"] = {
        "id": "dreadmist_docks_cargo_wharf",
        "name": "Cargo Wharf",
        "description": "A crumbling stone wharf stacked with mouldering crates and tar-sealed coffins. "
                       "Whatever cargo arrives here is unloaded quickly — the dock workers refuse to "
                       "linger after dark. Chains rattle in the fog with no wind to stir them.",
        "coordinates": [cx + 1, cy - 4],
        "location_type": "dock",
        "items": {"tarnished_lantern": {"quantity": 1, "value": 12}, "sealed_coffin_nail": {"quantity": 3, "value": 5}},
        "exits": {
            "west": {"target": "dreadmist_docks", "type": "direction"},
            "east": {"target": "dreadmist_docks_bone_pier", "type": "direction"}
        }
    }

    rooms["dreadmist_docks_lantern_tower"] = {
        "id": "dreadmist_docks_lantern_tower",
        "name": "Lantern Tower",
        "description": "A crooked tower of moss-covered stone, its beacon a sickly green flame that "
                       "burns without fuel. The light barely penetrates the eternal fog, casting "
                       "twisted shadows across the shore. Scratches on the inner walls suggest "
                       "someone — or something — was once trapped inside.",
        "coordinates": [cx - 1, cy - 4],
        "location_type": "building",
        "items": {"ghost_flame_shard": {"quantity": 1, "value": 20}},
        "exits": {
            "east": {"target": "dreadmist_docks", "type": "direction"},
            "west": {"target": "dreadmist_fogbound_cliffs_path", "type": "direction"}
        }
    }

    # --- Dreadmist Village (15 rooms) ---

    rooms["dreadmist_village_path"] = {
        "id": "dreadmist_village_path",
        "name": "Fog-Choked Path",
        "description": "A narrow dirt road winds uphill from the docks through gnarled, leafless trees. "
                       "Faint spectral lights drift between the trunks. The fog is so thick you can "
                       "barely see your own feet, and the air smells of damp earth and decay.",
        "coordinates": [cx, cy - 3],
        "location_type": "wilderness",
        "items": {},
        "exits": {
            "south": {"target": "dreadmist_docks", "type": "direction"},
            "north": {"target": "dreadmist_village_gate", "type": "direction"}
        }
    }

    rooms["dreadmist_village_gate"] = {
        "id": "dreadmist_village_gate",
        "name": "Dreadmist Village Gate",
        "description": "A wrought-iron gate flanked by crumbling stone pillars topped with gargoyle "
                       "skulls marks the entrance to Dreadmist Village. Rusted chains dangle from "
                       "the hinges and a ward-glyph carved into the archway glows faintly, keeping "
                       "the worst of the undead at bay — for now.",
        "coordinates": [cx, cy - 2],
        "location_type": "settlement",
        "items": {},
        "exits": {
            "south": {"target": "dreadmist_village_path", "type": "direction"},
            "north": {"target": "dreadmist_village_center", "type": "direction"},
            "east": {"target": "dreadmist_village_smith", "type": "direction"},
            "west": {"target": "dreadmist_village_well", "type": "direction"}
        }
    }

    rooms["dreadmist_village_center"] = {
        "id": "dreadmist_village_center",
        "name": "Dreadmist Village - Center Square",
        "description": "The heart of Dreadmist Village is a cobblestone square perpetually shrouded in "
                       "grey mist. A cracked fountain depicts a weeping angel whose stone tears have "
                       "left green stains down her face. Lanterns burn with pale blue fire outside "
                       "shuttered buildings, and the few villagers move quickly, eyes downcast.",
        "coordinates": [cx, cy - 1],
        "location_type": "settlement",
        "items": {},
        "exits": {
            "south": {"target": "dreadmist_village_gate", "type": "direction"},
            "north": {"target": "dreadmist_village_elder", "type": "direction"},
            "east": {"target": "dreadmist_village_market", "type": "direction"},
            "west": {"target": "dreadmist_village_inn", "type": "direction"}
        }
    }

    rooms["dreadmist_village_elder"] = {
        "id": "dreadmist_village_elder",
        "name": "Elder Morvaine's Hall",
        "description": "A gloomy timber hall where Elder Morvaine presides over the beleaguered village. "
                       "Shelves of ancient tomes and warding talismans line the walls. A fire burns in "
                       "the hearth but gives off no warmth — only a cold, flickering light that makes "
                       "the shadows dance like living things.",
        "coordinates": [cx, cy],
        "location_type": "building",
        "npcs": ["elder_morvaine"],
        "items": {"warding_talisman": {"quantity": 1, "value": 30}, "tome_of_the_dead": {"quantity": 1, "value": 45}},
        "exits": {
            "south": {"target": "dreadmist_village_center", "type": "direction"},
            "north": {"target": "dreadmist_village_crypt_keeper", "type": "direction"},
            "east": {"target": "dreadmist_village_shrine", "type": "direction"},
            "west": {"target": "dreadmist_village_chapel", "type": "direction"}
        }
    }

    rooms["dreadmist_village_market"] = {
        "id": "dreadmist_village_market",
        "name": "Dreadmist Market",
        "description": "A covered market where gaunt vendors hawk their grim wares by candlelight. "
                       "Stalls sell funeral supplies, protective charms, silver weapons, and vials of "
                       "holy water. Business is conducted in hushed whispers, as if speaking too loudly "
                       "might attract unwanted attention from beyond the grave.",
        "coordinates": [cx + 1, cy - 1],
        "location_type": "settlement",
        "shop": True,
        "items": {"holy_water_vial": {"quantity": 3, "value": 18}, "silver_dagger": {"quantity": 1, "value": 35}},
        "exits": {
            "west": {"target": "dreadmist_village_center", "type": "direction"},
            "east": {"target": "dreadmist_village_apothecary", "type": "direction"}
        }
    }

    rooms["dreadmist_village_apothecary"] = {
        "id": "dreadmist_village_apothecary",
        "name": "The Pallid Remedy",
        "description": "A cramped apothecary shop reeking of embalming fluid and dried herbs. Jars of "
                       "pickled organs, bundles of wolfsbane, and phials of glowing ectoplasm line the "
                       "shelves. The apothecary — a woman with hollow eyes and bone-white hair — brews "
                       "remedies against curses, poisons, and spectral afflictions.",
        "coordinates": [cx + 2, cy - 1],
        "location_type": "building",
        "items": {"anti_curse_tonic": {"quantity": 2, "value": 22}, "wolfsbane_bundle": {"quantity": 1, "value": 15}},
        "exits": {
            "west": {"target": "dreadmist_village_market", "type": "direction"}
        }
    }

    rooms["dreadmist_village_inn"] = {
        "id": "dreadmist_village_inn",
        "name": "The Hollow Lantern Inn",
        "description": "A sagging two-storey inn whose windows are boarded from the inside. The common "
                       "room is dimly lit by candles stuck in skulls, and the ale tastes faintly of "
                       "grave dirt. Nervous travellers clutch silver talismans while the innkeeper "
                       "warns guests never to open their windows after midnight.",
        "coordinates": [cx - 1, cy - 1],
        "location_type": "building",
        "items": {"grave_dirt_ale": {"quantity": 2, "value": 6}, "tallow_candle": {"quantity": 3, "value": 3}},
        "exits": {
            "east": {"target": "dreadmist_village_center", "type": "direction"},
            "west": {"target": "dreadmist_village_healer", "type": "direction"},
            "upstairs": {"target": "dreadmist_village_inn_room", "type": "named", "display": "Inn Room"}
        }
    }

    rooms["dreadmist_village_inn_room"] = {
        "id": "dreadmist_village_inn_room",
        "name": "Hollow Lantern - Guest Room",
        "description": "A small room with a straw mattress, a crucifix nailed above the door, and "
                       "salt lines poured across the windowsill. The wallpaper peels in long strips "
                       "revealing older, stranger patterns beneath. You can rest here, though the "
                       "scratching sounds in the walls make sleep difficult.",
        "coordinates": [cx - 1, cy],
        "location_type": "building",
        "items": {},
        "exits": {
            "downstairs": {"target": "dreadmist_village_inn", "type": "named", "display": "Back to Inn"}
        }
    }

    rooms["dreadmist_village_healer"] = {
        "id": "dreadmist_village_healer",
        "name": "Sister Adela's Hospice",
        "description": "A candlelit hospice run by Sister Adela, a stern priestess of the light. "
                       "Patients lie on cots surrounded by protective wards etched into the floor. "
                       "She treats wounds both physical and spiritual — many villagers suffer from "
                       "nightmares, possession, and the slow wasting curse of the fog.",
        "coordinates": [cx - 2, cy - 1],
        "location_type": "building",
        "npcs": ["sister_adela"],
        "items": {"blessed_bandage": {"quantity": 2, "value": 20}, "smelling_salts": {"quantity": 1, "value": 10}},
        "exits": {
            "east": {"target": "dreadmist_village_inn", "type": "direction"},
            "west": {"target": "dreadmist_village_herb_plot", "type": "direction"}
        }
    }

    rooms["dreadmist_village_shrine"] = {
        "id": "dreadmist_village_shrine",
        "name": "Shrine of Last Light",
        "description": "A small stone shrine dedicated to the last vestiges of holy power on the island. "
                       "A single candle that never burns out sits on the altar, surrounded by prayers "
                       "scratched into copper plates. Villagers leave offerings here, begging for "
                       "protection against the encroaching darkness.",
        "coordinates": [cx + 1, cy],
        "location_type": "building",
        "items": {"eternal_candle_wax": {"quantity": 1, "value": 25}, "copper_prayer_plate": {"quantity": 2, "value": 8}},
        "exits": {
            "west": {"target": "dreadmist_village_elder", "type": "direction"}
        }
    }

    rooms["dreadmist_village_smith"] = {
        "id": "dreadmist_village_smith",
        "name": "Grimhelm's Forge",
        "description": "A blacksmith's forge where the anvil rings with a mournful tone. Grimhelm, a "
                       "scarred giant of a man, specialises in silver-edged weapons and iron-banded "
                       "coffins. Sparks fly from the forge like tiny dying stars, and every blade he "
                       "crafts is etched with protective runes against the undead.",
        "coordinates": [cx + 1, cy - 2],
        "location_type": "building",
        "npcs": ["grimhelm"],
        "items": {"silver_tipped_bolt": {"quantity": 5, "value": 10}, "runed_iron_band": {"quantity": 1, "value": 28}},
        "exits": {
            "west": {"target": "dreadmist_village_gate", "type": "direction"},
            "east": {"target": "dreadmist_castle_road", "type": "direction"}
        }
    }

    rooms["dreadmist_village_well"] = {
        "id": "dreadmist_village_well",
        "name": "The Whispering Well",
        "description": "An ancient stone well at the western edge of the village. Villagers say voices "
                       "rise from its depths at night — the pleas of souls drowned long ago. The water "
                       "is drinkable but tastes of iron and sorrow. A frayed rope and dented bucket "
                       "hang from a rotting crossbeam.",
        "coordinates": [cx - 1, cy - 2],
        "location_type": "settlement",
        "items": {"iron_tainted_water": {"quantity": 1, "value": 2}},
        "exits": {
            "east": {"target": "dreadmist_village_gate", "type": "direction"},
            "west": {"target": "dreadmist_marsh_trail", "type": "direction"}
        }
    }

    rooms["dreadmist_village_chapel"] = {
        "id": "dreadmist_village_chapel",
        "name": "Chapel of Fading Grace",
        "description": "A crumbling chapel whose stained-glass windows depict scenes of a great battle "
                       "between the living and the dead. Most panes are shattered, letting the fog creep "
                       "in. The pews are splintered and the altar is cracked, but a faint holy glow "
                       "still clings to the stone — the last ember of divine protection.",
        "coordinates": [cx - 2, cy],
        "location_type": "building",
        "items": {"shattered_stained_glass": {"quantity": 2, "value": 12}, "faded_prayer_book": {"quantity": 1, "value": 15}},
        "exits": {
            "east": {"target": "dreadmist_village_elder", "type": "direction"},
            "west": {"target": "dreadmist_village_graveyard_path", "type": "direction"}
        }
    }

    rooms["dreadmist_village_crypt_keeper"] = {
        "id": "dreadmist_village_crypt_keeper",
        "name": "Crypt Keeper's Hovel",
        "description": "A ramshackle dwelling belonging to Old Morteus, the village crypt keeper. Bones, "
                       "shovels, and embalming tools clutter every surface. Morteus knows more about "
                       "the dead of this island than any living soul, and his rheumy eyes have seen "
                       "things that would shatter a lesser mind.",
        "coordinates": [cx, cy + 1],
        "location_type": "building",
        "npcs": ["old_morteus"],
        "items": {"grave_keeper_key": {"quantity": 1, "value": 10}, "embalming_fluid": {"quantity": 2, "value": 14}},
        "exits": {
            "south": {"target": "dreadmist_village_elder", "type": "direction"},
            "north": {"target": "dreadmist_village_overlook", "type": "direction"}
        }
    }

    rooms["dreadmist_village_overlook"] = {
        "id": "dreadmist_village_overlook",
        "name": "Village Overlook",
        "description": "A raised stone platform at the northern edge of the village offering a bleak "
                       "panorama. To the west, the haunted forest writhes with spectral light. East, "
                       "the cursed graveyard's tombstones stretch to the horizon. Northward, the land "
                       "sinks into darkness where the ancient necropolis lies hidden.",
        "coordinates": [cx, cy + 2],
        "location_type": "settlement",
        "items": {},
        "exits": {
            "south": {"target": "dreadmist_village_crypt_keeper", "type": "direction"},
            "west": {"target": "dreadmist_haunted_edge", "type": "direction"},
            "east": {"target": "dreadmist_graveyard_gate", "type": "direction"},
            "north": {"target": "dreadmist_dark_crossroads", "type": "direction"}
        }
    }

    # --- Haunted Forest (12 rooms) ---

    rooms["dreadmist_haunted_edge"] = {
        "id": "dreadmist_haunted_edge",
        "name": "Edge of the Haunted Forest",
        "description": "The treeline looms before you like a wall of skeletal fingers. Dead branches "
                       "claw at the grey sky and the ground is carpeted with black, rotting leaves. "
                       "A faint wailing drifts from deep within, and spectral lights bob between "
                       "the twisted trunks.",
        "coordinates": [cx - 2, cy + 2],
        "location_type": "wilderness",
        "items": {"rotting_bark": {"quantity": 2, "value": 3}},
        "exits": {
            "east": {"target": "dreadmist_village_overlook", "type": "direction"},
            "west": {"target": "dreadmist_haunted_dead_grove", "type": "direction"},
            "north": {"target": "dreadmist_haunted_bone_glade", "type": "direction"}
        }
    }

    rooms["dreadmist_haunted_dead_grove"] = {
        "id": "dreadmist_haunted_dead_grove",
        "name": "Dead Grove",
        "description": "A grove of petrified trees stands in perfect rows, as if planted by some "
                       "long-dead gardener. The bark has turned to stone and the branches are frozen "
                       "mid-sway. Between the trunks, shadows move independently of any light source, "
                       "and the temperature drops sharply with each step deeper.",
        "coordinates": [cx - 3, cy + 2],
        "location_type": "wilderness",
        "items": {"petrified_wood_shard": {"quantity": 1, "value": 15}},
        "exits": {
            "east": {"target": "dreadmist_haunted_edge", "type": "direction"},
            "west": {"target": "dreadmist_haunted_twisted_oaks", "type": "direction"},
            "north": {"target": "dreadmist_haunted_wisp_trail", "type": "direction"}
        }
    }

    rooms["dreadmist_haunted_wisp_trail"] = {
        "id": "dreadmist_haunted_wisp_trail",
        "name": "Wisp Trail",
        "description": "A narrow path illuminated by drifting spectral wisps — pale orbs of ghostly "
                       "light that float just out of reach. Following them leads deeper into the forest, "
                       "but the wise know they lure the unwary to their doom. The ground squelches "
                       "underfoot with every step.",
        "coordinates": [cx - 3, cy + 3],
        "location_type": "wilderness",
        "items": {"wisp_essence": {"quantity": 1, "value": 22}},
        "exits": {
            "south": {"target": "dreadmist_haunted_dead_grove", "type": "direction"},
            "west": {"target": "dreadmist_haunted_spectral_clearing", "type": "direction"},
            "north": {"target": "dreadmist_haunted_ghostly_pond", "type": "direction"},
            "east": {"target": "dreadmist_haunted_bone_glade", "type": "direction"}
        }
    }

    rooms["dreadmist_haunted_twisted_oaks"] = {
        "id": "dreadmist_haunted_twisted_oaks",
        "name": "Twisted Oaks",
        "description": "Massive oak trees have been warped into grotesque shapes by some dark influence, "
                       "their trunks spiralling like wrung cloth. Faces seem to press outward from the "
                       "bark — mouths open in silent screams. A low, rhythmic groaning emanates from "
                       "deep within the wood of the largest tree.",
        "coordinates": [cx - 4, cy + 2],
        "location_type": "wilderness",
        "items": {"cursed_acorn": {"quantity": 2, "value": 8}},
        "exits": {
            "east": {"target": "dreadmist_haunted_dead_grove", "type": "direction"},
            "north": {"target": "dreadmist_haunted_spectral_clearing", "type": "direction"},
            "west": {"target": "dreadmist_haunted_hollow_tree", "type": "direction"}
        }
    }

    rooms["dreadmist_haunted_spectral_clearing"] = {
        "id": "dreadmist_haunted_spectral_clearing",
        "name": "Spectral Clearing",
        "description": "A circular clearing where the fog thins just enough to reveal a ring of "
                       "mushrooms glowing with pale violet light. Translucent figures drift through "
                       "the air — ghosts trapped in an eternal dance. The grass within the fairy ring "
                       "is frost-white despite no cold in the air.",
        "coordinates": [cx - 4, cy + 3],
        "location_type": "wilderness",
        "items": {"ghost_mushroom": {"quantity": 3, "value": 12}, "spectral_dust": {"quantity": 1, "value": 18}},
        "exits": {
            "south": {"target": "dreadmist_haunted_twisted_oaks", "type": "direction"},
            "east": {"target": "dreadmist_haunted_wisp_trail", "type": "direction"},
            "west": {"target": "dreadmist_haunted_cursed_grove", "type": "direction"},
            "north": {"target": "dreadmist_haunted_weeping_willows", "type": "direction"}
        }
    }

    rooms["dreadmist_haunted_weeping_willows"] = {
        "id": "dreadmist_haunted_weeping_willows",
        "name": "Weeping Willows",
        "description": "A cluster of enormous willow trees whose trailing branches drip with a viscous, "
                       "dark sap that smells of funeral incense. The branches sway and reach toward "
                       "passers-by, and soft sobbing sounds echo from somewhere within the canopy. "
                       "The ground is soft and gives way to shallow, dark water.",
        "coordinates": [cx - 4, cy + 4],
        "location_type": "wilderness",
        "items": {"mourning_sap": {"quantity": 2, "value": 14}},
        "exits": {
            "south": {"target": "dreadmist_haunted_spectral_clearing", "type": "direction"},
            "east": {"target": "dreadmist_haunted_ghostly_pond", "type": "direction"},
            "west": {"target": "dreadmist_haunted_dark_thicket", "type": "direction"},
            "north": {"target": "dreadmist_haunted_heart", "type": "direction"}
        }
    }

    rooms["dreadmist_haunted_cursed_grove"] = {
        "id": "dreadmist_haunted_cursed_grove",
        "name": "Cursed Grove",
        "description": "Every tree in this grove is branded with necrotic sigils that pulse with a "
                       "faint sickly glow. The ground is black and nothing grows — even fungi shun "
                       "this place. Animals caught within the grove have been turned to bone, their "
                       "skeletons posed in lifelike positions as if death came in an instant.",
        "coordinates": [cx - 5, cy + 3],
        "location_type": "wilderness",
        "items": {"necrotic_sigil_rubbing": {"quantity": 1, "value": 20}},
        "exits": {
            "east": {"target": "dreadmist_haunted_spectral_clearing", "type": "direction"},
            "south": {"target": "dreadmist_haunted_hollow_tree", "type": "direction"},
            "north": {"target": "dreadmist_haunted_dark_thicket", "type": "direction"}
        }
    }

    rooms["dreadmist_haunted_hollow_tree"] = {
        "id": "dreadmist_haunted_hollow_tree",
        "name": "The Hollow Tree",
        "description": "A colossal dead tree, easily thirty feet across, stands split open like a "
                       "wound. Inside the hollow trunk is a cramped space littered with old bones, "
                       "tattered cloth, and scratched symbols. Something once lived — or hid — here. "
                       "Claw marks score the inner walls from floor to the gap in the canopy above.",
        "coordinates": [cx - 5, cy + 2],
        "location_type": "wilderness",
        "items": {"tattered_spirit_cloth": {"quantity": 1, "value": 16}, "bone_charm": {"quantity": 1, "value": 10}},
        "exits": {
            "east": {"target": "dreadmist_haunted_twisted_oaks", "type": "direction"},
            "north": {"target": "dreadmist_haunted_cursed_grove", "type": "direction"}
        }
    }

    rooms["dreadmist_haunted_ghostly_pond"] = {
        "id": "dreadmist_haunted_ghostly_pond",
        "name": "Ghostly Pond",
        "description": "A still, mirror-black pond reflects a sky that doesn't match the one above — "
                       "the reflection shows stars and a blood-red moon even in daylight. Pale hands "
                       "occasionally break the surface before sinking back. Drinking the water is said "
                       "to grant visions of death, though whose death is uncertain.",
        "coordinates": [cx - 3, cy + 4],
        "location_type": "wilderness",
        "items": {"void_water_vial": {"quantity": 1, "value": 25}},
        "exits": {
            "south": {"target": "dreadmist_haunted_wisp_trail", "type": "direction"},
            "west": {"target": "dreadmist_haunted_weeping_willows", "type": "direction"}
        }
    }

    rooms["dreadmist_haunted_dark_thicket"] = {
        "id": "dreadmist_haunted_dark_thicket",
        "name": "Dark Thicket",
        "description": "An impenetrable tangle of thorn-covered vines and dead branches forms a "
                       "natural labyrinth. The thorns are unnaturally sharp and seem to move on their "
                       "own, closing paths behind you. Scraps of clothing and old bones hang snagged "
                       "in the barbs — remnants of those who couldn't find their way out.",
        "coordinates": [cx - 5, cy + 4],
        "location_type": "wilderness",
        "items": {"bloodthorn_vine": {"quantity": 2, "value": 11}},
        "exits": {
            "south": {"target": "dreadmist_haunted_cursed_grove", "type": "direction"},
            "east": {"target": "dreadmist_haunted_weeping_willows", "type": "direction"}
        }
    }

    rooms["dreadmist_haunted_bone_glade"] = {
        "id": "dreadmist_haunted_bone_glade",
        "name": "Bone Glade",
        "description": "A long, narrow clearing where the trees part to reveal ground carpeted in "
                       "weathered bones. Skulls of humans, animals, and less identifiable creatures "
                       "are arranged in concentric circles. At the centre, a single black candle "
                       "burns with a flame that bends toward the north, always north.",
        "coordinates": [cx - 2, cy + 3],
        "location_type": "wilderness",
        "items": {"black_wax_candle": {"quantity": 1, "value": 18}, "bone_fragment": {"quantity": 3, "value": 5}},
        "exits": {
            "south": {"target": "dreadmist_haunted_edge", "type": "direction"},
            "west": {"target": "dreadmist_haunted_wisp_trail", "type": "direction"}
        }
    }

    rooms["dreadmist_haunted_heart"] = {
        "id": "dreadmist_haunted_heart",
        "name": "Heart of the Haunted Forest",
        "description": "The deepest point of the forest — a clearing where a massive, ancient tree "
                       "stands alone, its bark white as bone and its branches heavy with hanging "
                       "nooses of spectral chain. The tree pulses with a visible heartbeat of dark "
                       "energy. This is the source of the forest's corruption, a conduit of death.",
        "coordinates": [cx - 4, cy + 5],
        "location_type": "wilderness",
        "items": {"heart_tree_splinter": {"quantity": 1, "value": 40}, "spectral_chain_link": {"quantity": 1, "value": 30}},
        "exits": {
            "south": {"target": "dreadmist_haunted_weeping_willows", "type": "direction"},
            "north": {"target": "dreadmist_haunted_shadow_glade", "type": "direction"}
        }
    }

    # --- Cursed Graveyard (10 rooms) ---

    rooms["dreadmist_graveyard_gate"] = {
        "id": "dreadmist_graveyard_gate",
        "name": "Graveyard Gate",
        "description": "A towering iron gate bearing the inscription 'HERE LIE THE FORSAKEN' in "
                       "letters of tarnished silver. The gate hangs permanently ajar, its lock rusted "
                       "away centuries ago. Beyond, endless rows of crooked tombstones disappear into "
                       "the fog like teeth in a monstrous jaw.",
        "coordinates": [cx + 3, cy + 2],
        "location_type": "wilderness",
        "items": {},
        "exits": {
            "west": {"target": "dreadmist_village_overlook", "type": "direction"},
            "east": {"target": "dreadmist_graveyard_entrance", "type": "direction"},
            "north": {"target": "dreadmist_graveyard_central", "type": "direction"}
        }
    }

    rooms["dreadmist_graveyard_entrance"] = {
        "id": "dreadmist_graveyard_entrance",
        "name": "Graveyard Entrance Path",
        "description": "A gravel path crunches underfoot as it winds between leaning tombstones and "
                       "collapsed grave markers. Many graves have been disturbed — earth piled beside "
                       "open holes, coffin lids splintered from the inside. The air is thick with the "
                       "smell of turned earth and something far worse.",
        "coordinates": [cx + 4, cy + 2],
        "location_type": "wilderness",
        "items": {"grave_dust": {"quantity": 2, "value": 8}},
        "exits": {
            "west": {"target": "dreadmist_graveyard_gate", "type": "direction"},
            "east": {"target": "dreadmist_graveyard_bone_pit", "type": "direction"},
            "north": {"target": "dreadmist_graveyard_tombstones", "type": "direction"}
        }
    }

    rooms["dreadmist_graveyard_central"] = {
        "id": "dreadmist_graveyard_central",
        "name": "Central Graveyard",
        "description": "The oldest section of the graveyard, where moss-covered headstones bear dates "
                       "from centuries past. A cracked stone angel stands vigil over a mass grave, her "
                       "wings broken and her face worn smooth by time. At night, faint green lights "
                       "rise from the earth like escaping souls.",
        "coordinates": [cx + 3, cy + 3],
        "location_type": "wilderness",
        "items": {"ancient_headstone_fragment": {"quantity": 1, "value": 12}},
        "exits": {
            "south": {"target": "dreadmist_graveyard_gate", "type": "direction"},
            "east": {"target": "dreadmist_graveyard_tombstones", "type": "direction"}
        }
    }

    rooms["dreadmist_graveyard_tombstones"] = {
        "id": "dreadmist_graveyard_tombstones",
        "name": "Field of Tombstones",
        "description": "An endless expanse of tombstones stretching in every direction, many tilted "
                       "at drunken angles or toppled entirely. Names and epitaphs have been scratched "
                       "out on some, replaced with warnings: 'DO NOT DISTURB', 'STILL HUNGRY'. "
                       "Skeletal hands occasionally claw up through the soft earth.",
        "coordinates": [cx + 4, cy + 3],
        "location_type": "wilderness",
        "items": {"cracked_tombstone": {"quantity": 1, "value": 6}, "death_shroud": {"quantity": 1, "value": 18}},
        "exits": {
            "south": {"target": "dreadmist_graveyard_entrance", "type": "direction"},
            "west": {"target": "dreadmist_graveyard_central", "type": "direction"},
            "east": {"target": "dreadmist_graveyard_mausoleum", "type": "direction"},
            "north": {"target": "dreadmist_graveyard_grave_keeper", "type": "direction"}
        }
    }

    rooms["dreadmist_graveyard_bone_pit"] = {
        "id": "dreadmist_graveyard_bone_pit",
        "name": "Bone Pit",
        "description": "A vast pit filled with the bones of thousands, tossed here without ceremony "
                       "during some ancient plague or massacre. The bones are piled twenty feet deep "
                       "and shift constantly, as if something moves beneath. Occasionally a skull "
                       "rolls to the edge and stares outward with empty, accusing sockets.",
        "coordinates": [cx + 5, cy + 2],
        "location_type": "wilderness",
        "items": {"plague_era_skull": {"quantity": 1, "value": 10}, "bone_meal": {"quantity": 2, "value": 4}},
        "exits": {
            "west": {"target": "dreadmist_graveyard_entrance", "type": "direction"},
            "north": {"target": "dreadmist_graveyard_mausoleum", "type": "direction"}
        }
    }

    rooms["dreadmist_graveyard_mausoleum"] = {
        "id": "dreadmist_graveyard_mausoleum",
        "name": "Grand Mausoleum",
        "description": "A massive stone mausoleum carved with weeping gargoyles and death motifs. "
                       "The iron doors are scratched from the inside and hang slightly open, revealing "
                       "darkness within. Cold air seeps out, carrying the scent of ancient dust and "
                       "something unspeakably old. Names of a noble family are engraved above the lintel.",
        "coordinates": [cx + 5, cy + 3],
        "location_type": "wilderness",
        "items": {"mausoleum_key_fragment": {"quantity": 1, "value": 22}, "noble_death_mask": {"quantity": 1, "value": 35}},
        "exits": {
            "west": {"target": "dreadmist_graveyard_tombstones", "type": "direction"},
            "south": {"target": "dreadmist_graveyard_bone_pit", "type": "direction"},
            "east": {"target": "dreadmist_graveyard_ossuary", "type": "direction"},
            "north": {"target": "dreadmist_graveyard_open_crypts", "type": "direction"}
        }
    }

    rooms["dreadmist_graveyard_ossuary"] = {
        "id": "dreadmist_graveyard_ossuary",
        "name": "Ossuary",
        "description": "An underground chamber whose walls, ceiling, and pillars are constructed "
                       "entirely from human bones arranged in macabre decorative patterns. Femurs "
                       "form arches, skulls create chandeliers, and ribcages are woven into the walls "
                       "like brickwork. A faint whispering fills the chamber, as if the bones remember.",
        "coordinates": [cx + 6, cy + 3],
        "location_type": "wilderness",
        "items": {"skull_candelabra": {"quantity": 1, "value": 28}},
        "exits": {
            "west": {"target": "dreadmist_graveyard_mausoleum", "type": "direction"},
            "north": {"target": "dreadmist_graveyard_sunken_tombs", "type": "direction"}
        }
    }

    rooms["dreadmist_graveyard_grave_keeper"] = {
        "id": "dreadmist_graveyard_grave_keeper",
        "name": "Grave Keeper's Shack",
        "description": "A tilting wooden shack at the graveyard's highest point, surrounded by the "
                       "freshest graves. The grave keeper left long ago — or perhaps became one of "
                       "the residents below. Tools still hang on the walls: shovels, picks, and a "
                       "collection of numbered stakes used to mark the newly dead.",
        "coordinates": [cx + 4, cy + 4],
        "location_type": "building",
        "items": {"grave_shovel": {"quantity": 1, "value": 8}, "numbered_grave_stake": {"quantity": 3, "value": 3}},
        "exits": {
            "south": {"target": "dreadmist_graveyard_tombstones", "type": "direction"},
            "east": {"target": "dreadmist_graveyard_open_crypts", "type": "direction"}
        }
    }

    rooms["dreadmist_graveyard_open_crypts"] = {
        "id": "dreadmist_graveyard_open_crypts",
        "name": "Open Crypts",
        "description": "A row of crypts built into a low hillside, their stone doors smashed open. "
                       "Inside each crypt, stone sarcophagi have been pried apart. Some are empty, "
                       "their occupants walking elsewhere. Others contain only scraps of burial cloth "
                       "and the remnants of grave goods picked clean by looters or worse.",
        "coordinates": [cx + 5, cy + 4],
        "location_type": "wilderness",
        "items": {"burial_cloth_scrap": {"quantity": 2, "value": 5}, "crypt_dust": {"quantity": 1, "value": 9}},
        "exits": {
            "south": {"target": "dreadmist_graveyard_mausoleum", "type": "direction"},
            "west": {"target": "dreadmist_graveyard_grave_keeper", "type": "direction"},
            "east": {"target": "dreadmist_graveyard_sunken_tombs", "type": "direction"}
        }
    }

    rooms["dreadmist_graveyard_sunken_tombs"] = {
        "id": "dreadmist_graveyard_sunken_tombs",
        "name": "Sunken Tombs",
        "description": "The easternmost edge of the graveyard, where the ground has collapsed into a "
                       "network of flooded burial chambers. Murky water fills the sunken tombs to "
                       "waist height, and coffins float half-submerged like rotting boats. The stench "
                       "is overwhelming, and bubbles rise from the depths hinting at movement below.",
        "coordinates": [cx + 6, cy + 4],
        "location_type": "wilderness",
        "items": {"waterlogged_burial_urn": {"quantity": 1, "value": 15}, "drowned_man_ring": {"quantity": 1, "value": 30}},
        "exits": {
            "west": {"target": "dreadmist_graveyard_open_crypts", "type": "direction"},
            "south": {"target": "dreadmist_graveyard_ossuary", "type": "direction"},
            "east": {"target": "dreadmist_graveyard_forgotten_plot", "type": "direction"}
        }
    }

    # --- Spectral Marsh (10 rooms) ---

    rooms["dreadmist_marsh_trail"] = {
        "id": "dreadmist_marsh_trail",
        "name": "Marsh Trail",
        "description": "A rickety boardwalk of grey, waterlogged planks leads away from the village "
                       "into a vast marshland. The fog is thickest here, reducing visibility to mere "
                       "feet. The boards groan and shift underfoot, and the stagnant water on either "
                       "side is black as ink.",
        "coordinates": [cx - 2, cy - 2],
        "location_type": "wilderness",
        "items": {},
        "exits": {
            "east": {"target": "dreadmist_village_well", "type": "direction"},
            "west": {"target": "dreadmist_marsh_foggy_banks", "type": "direction"}
        }
    }

    rooms["dreadmist_marsh_foggy_banks"] = {
        "id": "dreadmist_marsh_foggy_banks",
        "name": "Foggy Banks",
        "description": "The boardwalk ends here at a muddy bank shrouded in fog so dense it feels "
                       "solid. Reeds and cattails stand motionless despite a wind you can hear but "
                       "not feel. Will-o'-wisps drift lazily over the water, and occasionally a "
                       "face seems to form in the fog before dissolving.",
        "coordinates": [cx - 3, cy - 2],
        "location_type": "wilderness",
        "items": {"marsh_reed": {"quantity": 3, "value": 3}, "fog_essence": {"quantity": 1, "value": 16}},
        "exits": {
            "east": {"target": "dreadmist_marsh_trail", "type": "direction"},
            "west": {"target": "dreadmist_marsh_drowned_ruins", "type": "direction"},
            "south": {"target": "dreadmist_marsh_stagnant_pool", "type": "direction"}
        }
    }

    rooms["dreadmist_marsh_stagnant_pool"] = {
        "id": "dreadmist_marsh_stagnant_pool",
        "name": "Stagnant Pool",
        "description": "A wide, motionless pool of dark water covered in a film of grey-green scum. "
                       "Bubbles of marsh gas rise and pop with tiny flashes of pale light. The water "
                       "is warm to the touch despite the chill air, and a sweet, cloying smell rises "
                       "from its surface — the smell of slow decay.",
        "coordinates": [cx - 3, cy - 3],
        "location_type": "wilderness",
        "items": {"stagnant_water_sample": {"quantity": 1, "value": 5}, "marsh_gas_vial": {"quantity": 1, "value": 12}},
        "exits": {
            "north": {"target": "dreadmist_marsh_foggy_banks", "type": "direction"},
            "west": {"target": "dreadmist_marsh_wisp_fen", "type": "direction"},
            "south": {"target": "dreadmist_marsh_bog_hollow", "type": "direction"}
        }
    }

    rooms["dreadmist_marsh_drowned_ruins"] = {
        "id": "dreadmist_marsh_drowned_ruins",
        "name": "Drowned Ruins",
        "description": "The crumbling remains of a stone settlement half-swallowed by the marsh. "
                       "Walls jut from the water at odd angles and doorways lead into flooded rooms "
                       "where the furniture still sits submerged. Whatever village once stood here was "
                       "consumed by the swamp, its inhabitants lost to the dark waters.",
        "coordinates": [cx - 4, cy - 2],
        "location_type": "wilderness",
        "items": {"drowned_relic": {"quantity": 1, "value": 20}, "waterlogged_journal": {"quantity": 1, "value": 14}},
        "exits": {
            "east": {"target": "dreadmist_marsh_foggy_banks", "type": "direction"},
            "south": {"target": "dreadmist_marsh_wisp_fen", "type": "direction"},
            "west": {"target": "dreadmist_marsh_ghost_bridge", "type": "direction"}
        }
    }

    rooms["dreadmist_marsh_wisp_fen"] = {
        "id": "dreadmist_marsh_wisp_fen",
        "name": "Will-o'-Wisp Fen",
        "description": "Dozens of spectral lights dance above the black water here, casting an eerie "
                       "glow over the twisted landscape. The wisps cluster around a half-sunken altar "
                       "stone, circling it like moths around a flame. Those who follow the wisps too "
                       "deep are never seen again — only their boots are found, stuck in the mud.",
        "coordinates": [cx - 4, cy - 3],
        "location_type": "wilderness",
        "items": {"wisp_lantern": {"quantity": 1, "value": 24}, "sunken_altar_chip": {"quantity": 1, "value": 10}},
        "exits": {
            "north": {"target": "dreadmist_marsh_drowned_ruins", "type": "direction"},
            "east": {"target": "dreadmist_marsh_stagnant_pool", "type": "direction"},
            "south": {"target": "dreadmist_marsh_sunken_village", "type": "direction"},
            "west": {"target": "dreadmist_marsh_dead_mangroves", "type": "direction"}
        }
    }

    rooms["dreadmist_marsh_sunken_village"] = {
        "id": "dreadmist_marsh_sunken_village",
        "name": "Sunken Village",
        "description": "The skeletal remains of a fishing village protrude from the marsh — rooftops "
                       "barely above water level, chimneys like tombstones. Nets still hang from "
                       "rotting poles and a church steeple tilts at a sickening angle. At night, "
                       "lights appear in the submerged windows and the sound of singing drifts up.",
        "coordinates": [cx - 4, cy - 4],
        "location_type": "wilderness",
        "items": {"sunken_church_bell_fragment": {"quantity": 1, "value": 18}, "rotting_fishing_net": {"quantity": 1, "value": 4}},
        "exits": {
            "north": {"target": "dreadmist_marsh_wisp_fen", "type": "direction"},
            "east": {"target": "dreadmist_marsh_bog_hollow", "type": "direction"}
        }
    }

    rooms["dreadmist_marsh_bog_hollow"] = {
        "id": "dreadmist_marsh_bog_hollow",
        "name": "Bog Hollow",
        "description": "A deep depression in the marsh where the water is particularly dark and still. "
                       "Perfectly preserved bodies have been found in bogs like these — ancient dead "
                       "tanned by the peat into leathery mummies. You can see shapes beneath the "
                       "surface that might be logs, might be bodies, might be something worse.",
        "coordinates": [cx - 3, cy - 4],
        "location_type": "wilderness",
        "items": {"peat_preserved_hand": {"quantity": 1, "value": 15}, "bog_iron_nugget": {"quantity": 2, "value": 7}},
        "exits": {
            "north": {"target": "dreadmist_marsh_stagnant_pool", "type": "direction"},
            "west": {"target": "dreadmist_marsh_sunken_village", "type": "direction"}
        }
    }

    rooms["dreadmist_marsh_ghost_bridge"] = {
        "id": "dreadmist_marsh_ghost_bridge",
        "name": "Ghost Bridge",
        "description": "A stone bridge arches over a wide channel of marsh water, but the bridge is "
                       "only half-real — its stones flicker and shimmer like a mirage. Those who step "
                       "on it find it solid enough, but looking down reveals the ghostly reflection of "
                       "a different bridge in a different time, crowded with fleeing figures.",
        "coordinates": [cx - 5, cy - 2],
        "location_type": "wilderness",
        "items": {"phantom_stone_chip": {"quantity": 1, "value": 20}},
        "exits": {
            "east": {"target": "dreadmist_marsh_drowned_ruins", "type": "direction"},
            "south": {"target": "dreadmist_marsh_dead_mangroves", "type": "direction"}
        }
    }

    rooms["dreadmist_marsh_dead_mangroves"] = {
        "id": "dreadmist_marsh_dead_mangroves",
        "name": "Dead Mangroves",
        "description": "A forest of dead mangrove trees rises from the marsh, their roots forming a "
                       "tangled cage above and below the waterline. The bark is white and peeling, "
                       "and strange barnacle-like growths cover the lower trunks — growths that have "
                       "tiny, tooth-filled mouths that snap at anything that passes too close.",
        "coordinates": [cx - 5, cy - 3],
        "location_type": "wilderness",
        "items": {"biting_barnacle": {"quantity": 2, "value": 9}, "dead_mangrove_root": {"quantity": 1, "value": 6}},
        "exits": {
            "north": {"target": "dreadmist_marsh_ghost_bridge", "type": "direction"},
            "east": {"target": "dreadmist_marsh_wisp_fen", "type": "direction"},
            "south": {"target": "dreadmist_marsh_depths", "type": "direction"}
        }
    }

    rooms["dreadmist_marsh_depths"] = {
        "id": "dreadmist_marsh_depths",
        "name": "Marsh Depths",
        "description": "The deepest, most treacherous part of the spectral marsh — a place where the "
                       "water is chest-deep and the fog forms into solid, grasping shapes. A massive "
                       "stone head, remnant of some forgotten colossus, rises from the mire, its eyes "
                       "aglow with green fire. Dark power radiates from this place like heat from coals.",
        "coordinates": [cx - 5, cy - 4],
        "location_type": "wilderness",
        "items": {"colossus_eye_gem": {"quantity": 1, "value": 45}, "marsh_wraith_essence": {"quantity": 1, "value": 30}},
        "exits": {
            "north": {"target": "dreadmist_marsh_dead_mangroves", "type": "direction"},
            "west": {"target": "dreadmist_marsh_drowned_temple", "type": "direction"}
        }
    }

    # --- Ruined Castle (12 rooms) ---

    rooms["dreadmist_castle_road"] = {
        "id": "dreadmist_castle_road",
        "name": "Castle Road",
        "description": "A cracked flagstone road climbs toward the looming silhouette of a ruined "
                       "castle. Broken statues of knights line the road, their heads missing or turned "
                       "backward. Dead ivy clings to the stonework and the wind carries a low, "
                       "mournful howl from the castle's empty towers.",
        "coordinates": [cx + 3, cy - 3],
        "location_type": "wilderness",
        "items": {"broken_knight_helm": {"quantity": 1, "value": 14}},
        "exits": {
            "west": {"target": "dreadmist_village_smith", "type": "direction"},
            "east": {"target": "dreadmist_castle_gate", "type": "direction"},
            "north": {"target": "dreadmist_castle_west_wing", "type": "direction"}
        }
    }

    rooms["dreadmist_castle_gate"] = {
        "id": "dreadmist_castle_gate",
        "name": "Ruined Castle Gate",
        "description": "The shattered remains of a once-magnificent gatehouse. The portcullis has been "
                       "torn from its tracks and lies twisted on the ground. Scorch marks and deep "
                       "claw gouges scar the stone walls. Whatever breached this gate did so with "
                       "terrible force, and the defenders never stood a chance.",
        "coordinates": [cx + 4, cy - 3],
        "location_type": "wilderness",
        "items": {"bent_portcullis_bar": {"quantity": 1, "value": 10}},
        "exits": {
            "west": {"target": "dreadmist_castle_road", "type": "direction"},
            "north": {"target": "dreadmist_castle_courtyard", "type": "direction"},
            "east": {"target": "dreadmist_castle_collapsed_tower", "type": "direction"}
        }
    }

    rooms["dreadmist_castle_courtyard"] = {
        "id": "dreadmist_castle_courtyard",
        "name": "Castle Courtyard",
        "description": "A once-grand courtyard now overgrown with thorny black roses and pale, "
                       "luminous fungi. A dried-up fountain at the centre is filled with old bones "
                       "instead of water. Doorways lead deeper into the castle's wings, and a wide "
                       "staircase ascends to the great hall above.",
        "coordinates": [cx + 4, cy - 2],
        "location_type": "wilderness",
        "items": {"black_rose": {"quantity": 2, "value": 12}, "luminous_fungus": {"quantity": 1, "value": 8}},
        "exits": {
            "south": {"target": "dreadmist_castle_gate", "type": "direction"},
            "north": {"target": "dreadmist_castle_great_hall", "type": "direction"},
            "west": {"target": "dreadmist_castle_west_wing", "type": "direction"},
            "east": {"target": "dreadmist_castle_dark_corridor", "type": "direction"}
        }
    }

    rooms["dreadmist_castle_great_hall"] = {
        "id": "dreadmist_castle_great_hall",
        "name": "Great Hall",
        "description": "The castle's great hall stretches before you, its vaulted ceiling lost in "
                       "shadow. A massive banquet table runs the length of the room, still set with "
                       "tarnished silver and rotting food — as if the feast was interrupted centuries "
                       "ago. Portraits on the walls depict a noble family whose eyes seem to track "
                       "your movement.",
        "coordinates": [cx + 4, cy - 1],
        "location_type": "wilderness",
        "items": {"tarnished_silver_goblet": {"quantity": 2, "value": 18}, "rotting_feast_plate": {"quantity": 1, "value": 5}},
        "exits": {
            "south": {"target": "dreadmist_castle_courtyard", "type": "direction"},
            "east": {"target": "dreadmist_castle_throne_room", "type": "direction"},
            "west": {"target": "dreadmist_castle_armory", "type": "direction"},
            "north": {"target": "dreadmist_castle_dungeon_stairs", "type": "direction"}
        }
    }

    rooms["dreadmist_castle_collapsed_tower"] = {
        "id": "dreadmist_castle_collapsed_tower",
        "name": "Collapsed Tower",
        "description": "The eastern tower has partially collapsed, its upper floors spilling into a "
                       "heap of rubble. Broken furniture and shattered masonry litter the ground. "
                       "Through gaps in the debris, you can see the remains of a study — books, "
                       "instruments, and a cracked crystal ball still sitting on a tilted desk.",
        "coordinates": [cx + 5, cy - 3],
        "location_type": "wilderness",
        "items": {"cracked_crystal_ball": {"quantity": 1, "value": 25}, "ruined_spellbook": {"quantity": 1, "value": 20}},
        "exits": {
            "west": {"target": "dreadmist_castle_gate", "type": "direction"},
            "north": {"target": "dreadmist_castle_dark_corridor", "type": "direction"}
        }
    }

    rooms["dreadmist_castle_west_wing"] = {
        "id": "dreadmist_castle_west_wing",
        "name": "West Wing",
        "description": "The castle's west wing is in surprisingly intact condition, though covered in "
                       "dust and cobwebs thick as curtains. Servants' quarters line the hallway, their "
                       "doors hanging open to reveal small rooms frozen in time. A child's doll sits "
                       "on a bed, its glass eyes watching the corridor.",
        "coordinates": [cx + 3, cy - 2],
        "location_type": "wilderness",
        "items": {"haunted_glass_doll": {"quantity": 1, "value": 16}, "ancient_servant_key": {"quantity": 1, "value": 10}},
        "exits": {
            "south": {"target": "dreadmist_castle_road", "type": "direction"},
            "east": {"target": "dreadmist_castle_courtyard", "type": "direction"},
            "north": {"target": "dreadmist_castle_armory", "type": "direction"}
        }
    }

    rooms["dreadmist_castle_dark_corridor"] = {
        "id": "dreadmist_castle_dark_corridor",
        "name": "Dark Corridor",
        "description": "A long, narrow corridor where the torches have long since burned out. The "
                       "walls are lined with suits of armour that creak and shift when you're not "
                       "looking directly at them. Your footsteps echo strangely, returning a half-beat "
                       "late as if something walks behind you, matching your pace.",
        "coordinates": [cx + 5, cy - 2],
        "location_type": "wilderness",
        "items": {"rusted_gauntlet": {"quantity": 1, "value": 12}},
        "exits": {
            "west": {"target": "dreadmist_castle_courtyard", "type": "direction"},
            "south": {"target": "dreadmist_castle_collapsed_tower", "type": "direction"},
            "north": {"target": "dreadmist_castle_throne_room", "type": "direction"},
            "east": {"target": "dreadmist_castle_tower_peak", "type": "direction"}
        }
    }

    rooms["dreadmist_castle_throne_room"] = {
        "id": "dreadmist_castle_throne_room",
        "name": "Throne Room",
        "description": "A cavernous throne room dominated by a massive throne of black iron and bone. "
                       "Tattered banners bearing a skull-and-crown sigil hang from the walls. The "
                       "throne's armrests are carved into skeletal hands, and a dark stain spreads "
                       "across the floor before it — the remnant of some terrible, ancient deed.",
        "coordinates": [cx + 5, cy - 1],
        "location_type": "wilderness",
        "items": {"skull_crown_sigil": {"quantity": 1, "value": 35}, "dark_iron_throne_shard": {"quantity": 1, "value": 28}},
        "exits": {
            "west": {"target": "dreadmist_castle_great_hall", "type": "direction"},
            "south": {"target": "dreadmist_castle_dark_corridor", "type": "direction"}
        }
    }

    rooms["dreadmist_castle_armory"] = {
        "id": "dreadmist_castle_armory",
        "name": "Castle Armory",
        "description": "Racks of ancient weapons line the walls — swords corroded by time, shields "
                       "split down the middle, and crossbows whose strings have rotted away. A few "
                       "pieces remain in remarkable condition, protected by faint enchantments that "
                       "still flicker along the steel. A weapon stand holds a blade of polished silver.",
        "coordinates": [cx + 3, cy - 1],
        "location_type": "wilderness",
        "items": {"enchanted_silver_blade": {"quantity": 1, "value": 50}, "corroded_shield": {"quantity": 1, "value": 8}},
        "exits": {
            "east": {"target": "dreadmist_castle_great_hall", "type": "direction"},
            "south": {"target": "dreadmist_castle_west_wing", "type": "direction"}
        }
    }

    rooms["dreadmist_castle_dungeon_stairs"] = {
        "id": "dreadmist_castle_dungeon_stairs",
        "name": "Dungeon Stairway",
        "description": "A spiralling stone staircase descends into absolute darkness beneath the "
                       "castle. The walls are slick with moisture and the steps are worn smooth by "
                       "centuries of use. Chains hang from iron rings set into the walls, and the "
                       "sounds of dripping water and distant moaning rise from below.",
        "coordinates": [cx + 4, cy],
        "location_type": "wilderness",
        "items": {"rusty_manacle": {"quantity": 1, "value": 7}},
        "exits": {
            "south": {"target": "dreadmist_castle_great_hall", "type": "direction"},
            "north": {"target": "dreadmist_castle_dungeon", "type": "direction"}
        }
    }

    rooms["dreadmist_castle_dungeon"] = {
        "id": "dreadmist_castle_dungeon",
        "name": "Castle Dungeon",
        "description": "A cold, dripping dungeon of iron cells and torture implements. Skeletons "
                       "in rusted shackles slump against the walls, some still wearing the remains "
                       "of fine clothing — political prisoners, perhaps, forgotten by the world above. "
                       "One cell at the far end is sealed with silver chains and covered in ward-glyphs.",
        "coordinates": [cx + 4, cy + 1],
        "location_type": "wilderness",
        "items": {"prisoner_locket": {"quantity": 1, "value": 15}, "silver_shackle_key": {"quantity": 1, "value": 22}},
        "exits": {
            "south": {"target": "dreadmist_castle_dungeon_stairs", "type": "direction"},
            "north": {"target": "dreadmist_castle_torture_chamber", "type": "direction"}
        }
    }

    rooms["dreadmist_castle_tower_peak"] = {
        "id": "dreadmist_castle_tower_peak",
        "name": "Tower Peak",
        "description": "The highest point of the surviving tower offers a dizzying view over the fog-"
                       "shrouded island. From here you can see the haunted forest writhing to the west, "
                       "the graveyard sprawling to the northeast, and the spectral marsh glowing faintly "
                       "to the southwest. A cold wind howls through the broken battlements.",
        "coordinates": [cx + 6, cy - 2],
        "location_type": "wilderness",
        "items": {"windswept_banner_scrap": {"quantity": 1, "value": 10}},
        "exits": {
            "west": {"target": "dreadmist_castle_dark_corridor", "type": "direction"},
            "east": {"target": "dreadmist_castle_secret_passage", "type": "direction"}
        }
    }

    # --- Necropolis (8 rooms, includes dark crossroads) ---

    rooms["dreadmist_dark_crossroads"] = {
        "id": "dreadmist_dark_crossroads",
        "name": "Dark Crossroads",
        "description": "A desolate junction where three dirt roads meet under a gallows tree. Three "
                       "skeletal corpses swing from the branches, their empty eye sockets staring in "
                       "different directions — north toward the necropolis, east toward the ritual "
                       "sites, and south back to the village. The road north descends into darkness.",
        "coordinates": [cx, cy + 3],
        "location_type": "wilderness",
        "items": {"gallows_rope": {"quantity": 1, "value": 8}},
        "exits": {
            "south": {"target": "dreadmist_village_overlook", "type": "direction"},
            "north": {"target": "dreadmist_necropolis_entrance", "type": "direction"},
            "east": {"target": "dreadmist_ritual_path", "type": "direction"}
        }
    }

    rooms["dreadmist_necropolis_entrance"] = {
        "id": "dreadmist_necropolis_entrance",
        "name": "Necropolis Entrance",
        "description": "A yawning cave mouth carved to resemble a giant screaming skull — the entrance "
                       "to the Necropolis, the underground city of the dead. Steps cut into living rock "
                       "descend into a darkness that swallows torchlight. The air rising from below is "
                       "ice-cold and carries the scent of ancient dust and embalming spice.",
        "coordinates": [cx, cy + 4],
        "location_type": "wilderness",
        "items": {"necropolis_map_scrap": {"quantity": 1, "value": 15}},
        "exits": {
            "south": {"target": "dreadmist_dark_crossroads", "type": "direction"},
            "north": {"target": "dreadmist_necropolis_avenue", "type": "direction"}
        }
    }

    rooms["dreadmist_necropolis_avenue"] = {
        "id": "dreadmist_necropolis_avenue",
        "name": "Avenue of the Dead",
        "description": "A wide underground boulevard lined with towering stone sarcophagi standing "
                       "upright like sentinels. Ghostly blue-flame torches burn in iron sconces, "
                       "illuminating carved reliefs depicting the history of a death-obsessed "
                       "civilisation. The avenue stretches into the depths of the earth, branching "
                       "into side passages and burial halls.",
        "coordinates": [cx, cy + 5],
        "location_type": "wilderness",
        "items": {"death_torch": {"quantity": 1, "value": 18}, "sarcophagus_relief_rubbing": {"quantity": 1, "value": 14}},
        "exits": {
            "south": {"target": "dreadmist_necropolis_entrance", "type": "direction"},
            "west": {"target": "dreadmist_necropolis_catacombs", "type": "direction"},
            "east": {"target": "dreadmist_necropolis_ossuary_hall", "type": "direction"},
            "north": {"target": "dreadmist_necropolis_heart", "type": "direction"}
        }
    }

    rooms["dreadmist_necropolis_catacombs"] = {
        "id": "dreadmist_necropolis_catacombs",
        "name": "Catacombs of Whispers",
        "description": "A labyrinthine network of narrow tunnels lined floor to ceiling with niches "
                       "containing the remains of the dead. Thousands of skulls stare from alcoves "
                       "as you pass, and whispers seem to emanate from every wall — the murmured "
                       "memories of the entombed, endlessly repeating their final words.",
        "coordinates": [cx - 1, cy + 5],
        "location_type": "wilderness",
        "items": {"whispering_skull": {"quantity": 1, "value": 22}, "catacomb_dust": {"quantity": 2, "value": 6}},
        "exits": {
            "east": {"target": "dreadmist_necropolis_avenue", "type": "direction"},
            "north": {"target": "dreadmist_necropolis_tomb_king", "type": "direction"},
            "south": {"target": "dreadmist_catacombs_entrance", "type": "direction"}
        }
    }

    rooms["dreadmist_necropolis_ossuary_hall"] = {
        "id": "dreadmist_necropolis_ossuary_hall",
        "name": "Ossuary Hall",
        "description": "A grand vaulted chamber where the bones of the dead have been arranged into "
                       "elaborate architectural structures — pillars of femurs, arches of ribcages, "
                       "and a massive chandelier of skulls that hangs from the ceiling. Despite the "
                       "macabre decor, the hall has a solemn, cathedral-like grandeur.",
        "coordinates": [cx + 1, cy + 5],
        "location_type": "wilderness",
        "items": {"bone_chandelier_crystal": {"quantity": 1, "value": 30}},
        "exits": {
            "west": {"target": "dreadmist_necropolis_avenue", "type": "direction"},
            "north": {"target": "dreadmist_necropolis_soul_well", "type": "direction"}
        }
    }

    rooms["dreadmist_necropolis_tomb_king"] = {
        "id": "dreadmist_necropolis_tomb_king",
        "name": "Tomb of the Lich King",
        "description": "A sealed burial chamber built for a ruler of the dead. The stone sarcophagus "
                       "at its centre is covered in chains of enchanted silver, each link inscribed "
                       "with binding runes. The chains have weakened over the centuries and several "
                       "have snapped. Whatever sleeps within stirs restlessly.",
        "coordinates": [cx - 1, cy + 6],
        "location_type": "wilderness",
        "items": {"broken_binding_chain": {"quantity": 1, "value": 35}, "lich_king_seal": {"quantity": 1, "value": 50}},
        "exits": {
            "south": {"target": "dreadmist_necropolis_catacombs", "type": "direction"},
            "east": {"target": "dreadmist_necropolis_heart", "type": "direction"}
        }
    }

    rooms["dreadmist_necropolis_soul_well"] = {
        "id": "dreadmist_necropolis_soul_well",
        "name": "The Soul Well",
        "description": "A deep shaft in the earth from which a column of ghostly energy spirals "
                       "upward like a slow-motion tornado. Faces form and dissolve in the spectral "
                       "light — the harvested souls of the dead, trapped in an endless cycle. The "
                       "well feeds the necropolis with dark energy, sustaining its undead inhabitants.",
        "coordinates": [cx + 1, cy + 6],
        "location_type": "wilderness",
        "items": {"soul_fragment": {"quantity": 1, "value": 40}, "well_water_of_souls": {"quantity": 1, "value": 25}},
        "exits": {
            "south": {"target": "dreadmist_necropolis_ossuary_hall", "type": "direction"},
            "west": {"target": "dreadmist_necropolis_heart", "type": "direction"}
        }
    }

    rooms["dreadmist_necropolis_heart"] = {
        "id": "dreadmist_necropolis_heart",
        "name": "Heart of the Necropolis",
        "description": "The deepest chamber of the Necropolis — a vast cavern where the ceiling "
                       "disappears into darkness above. At its centre stands a black altar pulsing "
                       "with necrotic energy, surrounded by a circle of standing bones. A doorway "
                       "of shadow and green flame shimmers in the far wall, leading to something "
                       "ancient and terrible beyond.",
        "coordinates": [cx, cy + 6],
        "location_type": "wilderness",
        "items": {"necrotic_heart_shard": {"quantity": 1, "value": 60}},
        "exits": {
            "south": {"target": "dreadmist_necropolis_avenue", "type": "direction"},
            "west": {"target": "dreadmist_necropolis_tomb_king", "type": "direction"},
            "east": {"target": "dreadmist_necropolis_soul_well", "type": "direction"},
            "enter": {
                "target": "FIXED_DUNGEON",
                "type": "fixed_dungeon",
                "dungeon_id": "halls_of_the_damned",
                "transition_text": "You step through the doorway of shadow and green flame. Reality\ntwists around you as you enter the Halls of the Damned — an endless\nlabyrinth of death and torment ruled by an ancient lich whose power\nhas grown unchecked for millennia..."
            }
        }
    }

    # --- Dark Ritual Sites (5 rooms) ---

    rooms["dreadmist_ritual_path"] = {
        "id": "dreadmist_ritual_path",
        "name": "Ritual Path",
        "description": "A trail of scorched earth leads away from the crossroads toward a cluster of "
                       "dark ritual sites. The ground is blackened and cracked, and nothing grows for "
                       "ten feet on either side of the path. Faint symbols glow in the dirt — wards "
                       "left by past practitioners, or perhaps warnings from their victims.",
        "coordinates": [cx + 1, cy + 3],
        "location_type": "wilderness",
        "items": {"scorched_ward_stone": {"quantity": 1, "value": 12}},
        "exits": {
            "west": {"target": "dreadmist_dark_crossroads", "type": "direction"},
            "east": {"target": "dreadmist_ritual_standing_stones", "type": "direction"},
            "north": {"target": "dreadmist_ritual_sacrificial_altar", "type": "direction"}
        }
    }

    rooms["dreadmist_ritual_standing_stones"] = {
        "id": "dreadmist_ritual_standing_stones",
        "name": "Cursed Standing Stones",
        "description": "A circle of seven massive standing stones, each carved with profane symbols "
                       "that hurt the eyes to look at. The stones hum with subsonic energy, and the "
                       "air between them shimmers like a heat mirage. The ground within the circle is "
                       "glass-smooth, fused by some cataclysmic release of dark power.",
        "coordinates": [cx + 2, cy + 3],
        "location_type": "wilderness",
        "items": {"profane_stone_chip": {"quantity": 2, "value": 15}, "fused_ground_shard": {"quantity": 1, "value": 20}},
        "exits": {
            "west": {"target": "dreadmist_ritual_path", "type": "direction"},
            "north": {"target": "dreadmist_ritual_blood_circle", "type": "direction"}
        }
    }

    rooms["dreadmist_ritual_blood_circle"] = {
        "id": "dreadmist_ritual_blood_circle",
        "name": "Blood Circle",
        "description": "A wide circle drawn in what appears to be permanently fresh blood — it never "
                       "dries, never fades, and steams faintly in the cold air. Candles of black wax "
                       "burn at five equidistant points around the circumference. At the circle's "
                       "centre, a depression in the stone holds a pool of dark liquid that reflects "
                       "no light.",
        "coordinates": [cx + 2, cy + 4],
        "location_type": "wilderness",
        "items": {"blood_circle_candle": {"quantity": 2, "value": 14}, "void_blood_vial": {"quantity": 1, "value": 30}},
        "exits": {
            "south": {"target": "dreadmist_ritual_standing_stones", "type": "direction"},
            "west": {"target": "dreadmist_ritual_sacrificial_altar", "type": "direction"},
            "north": {"target": "dreadmist_ritual_dark_obelisk", "type": "direction"}
        }
    }

    rooms["dreadmist_ritual_sacrificial_altar"] = {
        "id": "dreadmist_ritual_sacrificial_altar",
        "name": "Sacrificial Altar",
        "description": "A massive stone altar stained dark with centuries of blood sacrifice. Grooves "
                       "channel the blood into a basin below where it pools and occasionally bubbles. "
                       "Iron manacles are bolted to each corner and the stone surface is scratched with "
                       "desperate claw marks. The malevolence here is palpable, pressing against your "
                       "mind like a weight.",
        "coordinates": [cx + 1, cy + 4],
        "location_type": "wilderness",
        "items": {"sacrificial_dagger": {"quantity": 1, "value": 38}, "blood_basin_residue": {"quantity": 1, "value": 18}},
        "exits": {
            "south": {"target": "dreadmist_ritual_path", "type": "direction"},
            "east": {"target": "dreadmist_ritual_blood_circle", "type": "direction"}
        }
    }

    rooms["dreadmist_ritual_dark_obelisk"] = {
        "id": "dreadmist_ritual_dark_obelisk",
        "name": "The Dark Obelisk",
        "description": "A towering obelisk of obsidian glass rises from the earth, its surface covered "
                       "in shifting runes that rearrange themselves as you watch. The obelisk pulses "
                       "with a deep, rhythmic thrum that you feel in your bones. At its base, offerings "
                       "of bone and shadow have been left by necromancers who worship the power it "
                       "channels from beyond the veil.",
        "coordinates": [cx + 2, cy + 5],
        "location_type": "wilderness",
        "items": {"obelisk_shard": {"quantity": 1, "value": 45}, "shadow_offering": {"quantity": 1, "value": 22}},
        "exits": {
            "south": {"target": "dreadmist_ritual_blood_circle", "type": "direction"},
            "east": {"target": "dreadmist_ritual_shadow_sanctum", "type": "direction"}
        }
    }



    # === DREADMIST ISLE EXPANSION ===

    # --- Expanded Docks (+3 rooms) ---

    rooms["dreadmist_docks_bone_pier"] = {
        "id": "dreadmist_docks_bone_pier",
        "name": "Bone Pier",
        "description": "An extension of the dock built from the ribcages and keels of wrecked "
                       "ships. The pale wood has been bleached by salt and time until it "
                       "resembles bone. At night, phosphorescent barnacles make the pier glow "
                       "with an unsettling green light.",
        "coordinates": [cx + 2, cy - 4],
        "location_type": "dock",
        "items": {"bone_pier_splinter": {"quantity": 1, "value": 8}, "phosphorescent_barnacle": {"quantity": 2, "value": 10}},
        "exits": {
            "west": {"target": "dreadmist_docks_cargo_wharf", "type": "direction"},
            "north": {"target": "dreadmist_docks_smuggler_cave", "type": "direction"}
        }
    }

    rooms["dreadmist_docks_smuggler_cave"] = {
        "id": "dreadmist_docks_smuggler_cave",
        "name": "Smuggler's Sea Cave",
        "description": "A sea cave behind the docks once used by smugglers to move contraband. "
                       "Iron rings are hammered into the walls for tying boats, and hidden "
                       "alcoves in the rock once held valuable cargo. The cave floods at high "
                       "tide, adding danger to discretion.",
        "coordinates": [cx + 2, cy - 3],
        "location_type": "wilderness",
        "items": {"smuggler_ring": {"quantity": 1, "value": 12}, "hidden_cache_remnant": {"quantity": 1, "value": 20}},
        "exits": {
            "south": {"target": "dreadmist_docks_bone_pier", "type": "direction"},
            "north": {"target": "dreadmist_docks_wreckers_cove", "type": "direction"}
        }
    }

    rooms["dreadmist_docks_wreckers_cove"] = {
        "id": "dreadmist_docks_wreckers_cove",
        "name": "Wrecker's Cove",
        "description": "A sheltered cove where wreckers — those who lure ships onto rocks with "
                       "false lights — once operated. The beach is littered with old ship timbers "
                       "and rusted equipment. A decrepit signal tower stands on the cliff above, "
                       "its false light long extinguished.",
        "coordinates": [cx + 2, cy - 2],
        "location_type": "wilderness",
        "items": {"wrecker_signal_lens": {"quantity": 1, "value": 18}, "wreck_timber": {"quantity": 2, "value": 4}},
        "exits": {
            "south": {"target": "dreadmist_docks_smuggler_cave", "type": "direction"}
        }
    }

    # --- Expanded Dreadmist Village (+5 rooms) ---

    rooms["dreadmist_village_herb_plot"] = {
        "id": "dreadmist_village_herb_plot",
        "name": "Cursed Herb Plot",
        "description": "A fenced garden behind the healer's hut where strange medicinal plants "
                       "grow in perpetual twilight. The herbs here thrive on the island's dark "
                       "energy — nightshade, wormwood, and a black flower that blooms only "
                       "during spectral visitations.",
        "coordinates": [cx - 3, cy - 1],
        "location_type": "wilderness",
        "items": {"shadowbloom": {"quantity": 1, "value": 25}, "cursed_wormwood": {"quantity": 2, "value": 10}},
        "exits": {
            "east": {"target": "dreadmist_village_healer", "type": "direction"},
            "north": {"target": "dreadmist_village_bone_fence", "type": "direction"}
        }
    }

    rooms["dreadmist_village_bone_fence"] = {
        "id": "dreadmist_village_bone_fence",
        "name": "Bone Fence Perimeter",
        "description": "The village's western boundary is marked by a fence made of stacked "
                       "animal bones and warding charms. Villagers believe it keeps the worst "
                       "spirits at bay. Bundles of dried herbs hang from every post, and "
                       "protective runes are carved into the bones.",
        "coordinates": [cx - 4, cy],
        "location_type": "settlement",
        "items": {"bone_warding_charm": {"quantity": 1, "value": 18}, "dried_protection_herbs": {"quantity": 1, "value": 10}},
        "exits": {
            "south": {"target": "dreadmist_village_herb_plot", "type": "direction"}
        }
    }

    rooms["dreadmist_village_graveyard_path"] = {
        "id": "dreadmist_village_graveyard_path",
        "name": "Path to the Village Graveyard",
        "description": "A somber path lined with guttering lanterns leads from the chapel to "
                       "the village's small graveyard. Headstones lean at odd angles, and fresh "
                       "flowers are placed daily on the newest graves. The path is well-worn by "
                       "mourners' feet.",
        "coordinates": [cx - 4, cy + 1],
        "location_type": "wilderness",
        "items": {"mourning_lantern": {"quantity": 1, "value": 8}, "memorial_flowers": {"quantity": 1, "value": 5}},
        "exits": {
            "east": {"target": "dreadmist_village_chapel", "type": "direction"},
            "north": {"target": "dreadmist_village_old_graveyard", "type": "direction"}
        }
    }

    rooms["dreadmist_village_old_graveyard"] = {
        "id": "dreadmist_village_old_graveyard",
        "name": "Old Village Graveyard",
        "description": "The original graveyard, centuries older than the current village. Many "
                       "headstones are unreadable, worn smooth by time and acid rain. Some "
                       "graves have been disturbed — whether by animals, treasure hunters, or "
                       "the restless dead is unclear.",
        "coordinates": [cx - 3, cy + 1],
        "location_type": "wilderness",
        "items": {"ancient_headstone_fragment": {"quantity": 1, "value": 12}, "grave_dirt": {"quantity": 1, "value": 5}},
        "exits": {
            "south": {"target": "dreadmist_village_graveyard_path", "type": "direction"},
            "east": {"target": "dreadmist_village_watchtower", "type": "direction"}
        }
    }

    rooms["dreadmist_village_watchtower"] = {
        "id": "dreadmist_village_watchtower",
        "name": "Village Watchtower",
        "description": "A rickety wooden watchtower on the village's northern edge, manned by "
                       "nervous volunteers who scan the mist for approaching threats. Ghost-ward "
                       "lanterns hang from the railing, and a warning bell can be heard across "
                       "the entire settlement.",
        "coordinates": [cx - 2, cy + 1],
        "location_type": "building",
        "items": {"ghost_ward_lantern": {"quantity": 1, "value": 15}, "warning_bell_clapper": {"quantity": 1, "value": 10}},
        "exits": {
            "west": {"target": "dreadmist_village_old_graveyard", "type": "direction"}
        }
    }

    # --- Expanded Haunted Forest (+8 rooms) ---

    rooms["dreadmist_haunted_shadow_glade"] = {
        "id": "dreadmist_haunted_shadow_glade",
        "name": "Shadow Glade",
        "description": "Beyond the heart of the forest, a glade where no light penetrates. "
                       "The trees here have grown so thick and twisted that they block all "
                       "illumination. Movement in the shadows suggests watching presences. "
                       "Even the bravest feel unwelcome here.",
        "coordinates": [cx - 4, cy + 6],
        "location_type": "wilderness",
        "items": {"shadow_bark": {"quantity": 1, "value": 22}, "dark_glade_moss": {"quantity": 1, "value": 12}},
        "exits": {
            "south": {"target": "dreadmist_haunted_heart", "type": "direction"},
            "west": {"target": "dreadmist_haunted_wraith_hollow", "type": "direction"},
            "north": {"target": "dreadmist_haunted_ancient_tree", "type": "direction"}
        }
    }

    rooms["dreadmist_haunted_wraith_hollow"] = {
        "id": "dreadmist_haunted_wraith_hollow",
        "name": "Wraith Hollow",
        "description": "A depression in the forest floor where cold mist pools and wraiths "
                       "are said to materialize on moonless nights. The temperature drops "
                       "sharply upon entering, and breath becomes visible. Ghostly wailing "
                       "echoes from every direction.",
        "coordinates": [cx - 5, cy + 6],
        "location_type": "wilderness",
        "items": {"wraith_mist_vial": {"quantity": 1, "value": 30}, "frozen_tear": {"quantity": 1, "value": 20}},
        "exits": {
            "east": {"target": "dreadmist_haunted_shadow_glade", "type": "direction"},
            "north": {"target": "dreadmist_haunted_spider_web", "type": "direction"}
        }
    }

    rooms["dreadmist_haunted_spider_web"] = {
        "id": "dreadmist_haunted_spider_web",
        "name": "Giant Spider Web",
        "description": "Enormous webs span between the dead trees, each strand thick as rope "
                       "and sticky as tar. The webs are woven in intricate geometric patterns "
                       "that seem almost deliberate. Wrapped cocoons hang from the upper "
                       "strands — some disturbingly human-shaped.",
        "coordinates": [cx - 5, cy + 7],
        "location_type": "wilderness",
        "items": {"spider_silk_strand": {"quantity": 1, "value": 20}, "web_wrapped_trinket": {"quantity": 1, "value": 15}},
        "exits": {
            "south": {"target": "dreadmist_haunted_wraith_hollow", "type": "direction"},
            "east": {"target": "dreadmist_haunted_ancient_tree", "type": "direction"}
        }
    }

    rooms["dreadmist_haunted_ancient_tree"] = {
        "id": "dreadmist_haunted_ancient_tree",
        "name": "Ancient Sentinel Tree",
        "description": "A tree of impossible age stands at the old forest's center — its trunk "
                       "wider than a house, its canopy lost in perpetual fog. Faces seem carved "
                       "into the bark, but they shift and change when you look away. A hollow "
                       "at its base leads into a root-walled chamber.",
        "coordinates": [cx - 4, cy + 7],
        "location_type": "wilderness",
        "items": {"sentinel_tree_bark": {"quantity": 1, "value": 35}, "shifting_face_rubbing": {"quantity": 1, "value": 20}},
        "exits": {
            "south": {"target": "dreadmist_haunted_shadow_glade", "type": "direction"},
            "west": {"target": "dreadmist_haunted_spider_web", "type": "direction"},
            "north": {"target": "dreadmist_haunted_root_chamber", "type": "direction"},
            "east": {"target": "dreadmist_haunted_will_o_wisp", "type": "direction"}
        }
    }

    rooms["dreadmist_haunted_root_chamber"] = {
        "id": "dreadmist_haunted_root_chamber",
        "name": "Root Chamber",
        "description": "Within the ancient tree's root system, a natural chamber has formed. "
                       "Roots thick as pillars form the walls, and the air smells of rich earth "
                       "and decay. Strange fungi grow in patterns that resemble text, as if the "
                       "tree is trying to communicate.",
        "coordinates": [cx - 4, cy + 8],
        "location_type": "wilderness",
        "items": {"root_chamber_mushroom": {"quantity": 2, "value": 12}, "tree_language_sample": {"quantity": 1, "value": 25}},
        "exits": {
            "south": {"target": "dreadmist_haunted_ancient_tree", "type": "direction"}
        }
    }

    rooms["dreadmist_haunted_will_o_wisp"] = {
        "id": "dreadmist_haunted_will_o_wisp",
        "name": "Will-o'-Wisp Trail",
        "description": "A meandering trail through the deep forest marked by floating lights "
                       "that bob and weave between the trees. The will-o'-wisps are beautiful "
                       "but treacherous — following them leads as often to danger as to "
                       "treasure. Their pale blue glow is the only light here.",
        "coordinates": [cx - 3, cy + 7],
        "location_type": "wilderness",
        "items": {"wisp_light_jar": {"quantity": 1, "value": 25}},
        "exits": {
            "west": {"target": "dreadmist_haunted_ancient_tree", "type": "direction"},
            "east": {"target": "dreadmist_haunted_fungal_ring", "type": "direction"}
        }
    }

    rooms["dreadmist_haunted_fungal_ring"] = {
        "id": "dreadmist_haunted_fungal_ring",
        "name": "Fairy Ring",
        "description": "A perfect circle of mushrooms in a clearing, the classic fairy ring of "
                       "folklore. The air within the circle shimmers faintly, and compasses spin "
                       "wildly. Local legend says stepping into the ring on the wrong night will "
                       "transport you to the realm of the dead.",
        "coordinates": [cx - 2, cy + 7],
        "location_type": "wilderness",
        "items": {"fairy_ring_mushroom": {"quantity": 1, "value": 18}, "spirit_realm_compass": {"quantity": 1, "value": 30}},
        "exits": {
            "west": {"target": "dreadmist_haunted_will_o_wisp", "type": "direction"},
            "south": {"target": "dreadmist_haunted_dark_thicket", "type": "direction"}
        }
    }

    rooms["dreadmist_haunted_gallows_tree"] = {
        "id": "dreadmist_haunted_gallows_tree",
        "name": "Gallows Tree",
        "description": "A dead oak with unnaturally horizontal branches from which frayed ropes "
                       "still hang. This was once a place of execution, and the ground beneath "
                       "is said to be cursed. Nothing grows within twenty paces of the tree, "
                       "and animals refuse to approach.",
        "coordinates": [cx - 3, cy + 6],
        "location_type": "wilderness",
        "items": {"gallows_rope_fragment": {"quantity": 1, "value": 15}, "cursed_acorn": {"quantity": 1, "value": 20}},
        "exits": {
            "south": {"target": "dreadmist_haunted_cursed_grove", "type": "direction"},
            "east": {"target": "dreadmist_haunted_shadow_glade", "type": "direction"}
        }
    }

    # --- Expanded Cursed Graveyard (+6 rooms) ---

    rooms["dreadmist_graveyard_forgotten_plot"] = {
        "id": "dreadmist_graveyard_forgotten_plot",
        "name": "Forgotten Burial Plot",
        "description": "An overgrown section of the graveyard where the oldest graves have been "
                       "neglected for generations. Headstones are cracked and illegible, some "
                       "have toppled entirely. Wild thorny roses have consumed entire plots, "
                       "their red blooms an unsettling contrast to the gray surroundings.",
        "coordinates": [cx + 7, cy + 4],
        "location_type": "wilderness",
        "items": {"forgotten_headstone": {"quantity": 1, "value": 10}, "blood_rose": {"quantity": 2, "value": 12}},
        "exits": {
            "west": {"target": "dreadmist_graveyard_sunken_tombs", "type": "direction"},
            "north": {"target": "dreadmist_graveyard_death_angel", "type": "direction"},
            "south": {"target": "dreadmist_graveyard_crypt_hall", "type": "direction"}
        }
    }

    rooms["dreadmist_graveyard_death_angel"] = {
        "id": "dreadmist_graveyard_death_angel",
        "name": "Death Angel Statue",
        "description": "A towering marble statue of a weeping angel stands at the center of "
                       "this section, its stone face streaked with dark stains that look like "
                       "tears of blood. Locals say the statue's pose changes when no one is "
                       "looking. Fresh flowers appear at its base despite no visitors.",
        "coordinates": [cx + 7, cy + 5],
        "location_type": "wilderness",
        "items": {"angel_tear_stone": {"quantity": 1, "value": 30}, "mysterious_flowers": {"quantity": 1, "value": 15}},
        "exits": {
            "south": {"target": "dreadmist_graveyard_forgotten_plot", "type": "direction"},
            "west": {"target": "dreadmist_graveyard_bone_orchard", "type": "direction"}
        }
    }

    rooms["dreadmist_graveyard_bone_orchard"] = {
        "id": "dreadmist_graveyard_bone_orchard",
        "name": "Bone Orchard",
        "description": "Dead trees grow from the graves here, their white branches resembling "
                       "skeletal arms reaching skyward. The trees seem to have grown from the "
                       "graves themselves, their roots entwined with coffins below. Eerie "
                       "creaking sounds come from the branches even without wind.",
        "coordinates": [cx + 6, cy + 5],
        "location_type": "wilderness",
        "items": {"bone_tree_branch": {"quantity": 1, "value": 18}, "grave_root": {"quantity": 1, "value": 12}},
        "exits": {
            "east": {"target": "dreadmist_graveyard_death_angel", "type": "direction"},
            "south": {"target": "dreadmist_graveyard_open_crypts", "type": "direction"}
        }
    }

    rooms["dreadmist_graveyard_crypt_hall"] = {
        "id": "dreadmist_graveyard_crypt_hall",
        "name": "Crypt Hall",
        "description": "An underground passage connecting several burial crypts beneath the "
                       "graveyard. The stone walls are carved with memorial inscriptions, and "
                       "iron doors mark the entrance to each family vault. Some doors stand "
                       "ajar, their locks rusted away.",
        "coordinates": [cx + 7, cy + 3],
        "location_type": "wilderness",
        "items": {"crypt_door_key": {"quantity": 1, "value": 20}, "memorial_inscription": {"quantity": 1, "value": 10}},
        "exits": {
            "north": {"target": "dreadmist_graveyard_forgotten_plot", "type": "direction"},
            "west": {"target": "dreadmist_graveyard_coffin_makers", "type": "direction"}
        }
    }

    rooms["dreadmist_graveyard_coffin_makers"] = {
        "id": "dreadmist_graveyard_coffin_makers",
        "name": "Coffin Maker's Workshop",
        "description": "A morbid workshop at the graveyard's edge where coffins are constructed. "
                       "Half-finished caskets line the walls, and the smell of pine and varnish "
                       "fills the air. The coffin maker works in silence, never speaking to "
                       "visitors, only gesturing toward a price list.",
        "coordinates": [cx + 6, cy + 3],
        "location_type": "building",
        "items": {"coffin_nail": {"quantity": 5, "value": 2}, "funeral_varnish": {"quantity": 1, "value": 10}},
        "exits": {
            "east": {"target": "dreadmist_graveyard_crypt_hall", "type": "direction"},
            "south": {"target": "dreadmist_graveyard_entrance", "type": "direction"}
        }
    }

    rooms["dreadmist_graveyard_mourners_bench"] = {
        "id": "dreadmist_graveyard_mourners_bench",
        "name": "Mourner's Bench",
        "description": "A stone bench surrounded by willow trees where mourners sit to grieve. "
                       "The willows weep actual drops of dark sap that stain the ground black. "
                       "A book of condolence lies chained to the bench, its pages filled with "
                       "messages to the dead.",
        "coordinates": [cx + 5, cy + 5],
        "location_type": "wilderness",
        "items": {"condolence_book_page": {"quantity": 1, "value": 8}, "weeping_willow_sap": {"quantity": 1, "value": 15}},
        "exits": {
            "south": {"target": "dreadmist_graveyard_mausoleum", "type": "direction"}
        }
    }

    # --- Expanded Spectral Marsh (+8 rooms) ---

    rooms["dreadmist_marsh_drowned_temple"] = {
        "id": "dreadmist_marsh_drowned_temple",
        "name": "Drowned Temple",
        "description": "The sunken ruins of an ancient temple rise from the deepest part of the "
                       "marsh. Only the upper columns and the peaked roof break the surface. "
                       "Diving down reveals partially intact chambers filled with mud-covered "
                       "artifacts and eerie submerged statues.",
        "coordinates": [cx - 6, cy - 4],
        "location_type": "wilderness",
        "items": {"drowned_temple_idol": {"quantity": 1, "value": 40}, "submerged_offering_bowl": {"quantity": 1, "value": 18}},
        "exits": {
            "east": {"target": "dreadmist_marsh_depths", "type": "direction"},
            "north": {"target": "dreadmist_marsh_corpse_garden", "type": "direction"},
            "south": {"target": "dreadmist_marsh_sinking_trail", "type": "direction"}
        }
    }

    rooms["dreadmist_marsh_corpse_garden"] = {
        "id": "dreadmist_marsh_corpse_garden",
        "name": "Corpse Garden",
        "description": "A horrifying stretch of marsh where bodies have been preserved in the "
                       "peat for centuries. The tannin-stained dead lie just below the surface, "
                       "their features eerily intact. Local tradition holds this was once a "
                       "sacrificial ground.",
        "coordinates": [cx - 6, cy - 3],
        "location_type": "wilderness",
        "items": {"bog_body_pendant": {"quantity": 1, "value": 30}, "preservation_peat": {"quantity": 1, "value": 12}},
        "exits": {
            "south": {"target": "dreadmist_marsh_drowned_temple", "type": "direction"},
            "east": {"target": "dreadmist_marsh_dead_mangroves", "type": "direction"},
            "north": {"target": "dreadmist_marsh_floating_island", "type": "direction"}
        }
    }

    rooms["dreadmist_marsh_floating_island"] = {
        "id": "dreadmist_marsh_floating_island",
        "name": "Floating Island",
        "description": "A mat of vegetation thick enough to walk on drifts slowly across the "
                       "marsh surface. Small bushes and even a twisted tree grow on it. The "
                       "island's position changes daily, making it an unreliable landmark but "
                       "a useful hiding place.",
        "coordinates": [cx - 6, cy - 2],
        "location_type": "wilderness",
        "items": {"floating_moss": {"quantity": 1, "value": 8}, "drifting_plant_root": {"quantity": 1, "value": 10}},
        "exits": {
            "south": {"target": "dreadmist_marsh_corpse_garden", "type": "direction"},
            "east": {"target": "dreadmist_marsh_ghost_bridge", "type": "direction"}
        }
    }

    rooms["dreadmist_marsh_sinking_trail"] = {
        "id": "dreadmist_marsh_sinking_trail",
        "name": "Sinking Trail",
        "description": "A treacherous path where the ground slowly sinks underfoot. Each step "
                       "must be carefully chosen to avoid being swallowed by the mud. Wooden "
                       "planks and poles mark a safe route, but some have shifted or rotted "
                       "away.",
        "coordinates": [cx - 6, cy - 5],
        "location_type": "wilderness",
        "items": {"marsh_walking_stick": {"quantity": 1, "value": 8}, "sinking_trail_plank": {"quantity": 1, "value": 5}},
        "exits": {
            "north": {"target": "dreadmist_marsh_drowned_temple", "type": "direction"},
            "east": {"target": "dreadmist_marsh_gas_pockets", "type": "direction"}
        }
    }

    rooms["dreadmist_marsh_gas_pockets"] = {
        "id": "dreadmist_marsh_gas_pockets",
        "name": "Gas Pocket Flats",
        "description": "A section of marsh where pockets of swamp gas bubble to the surface "
                       "in great bursts. The gas is flammable and foul-smelling, and occasional "
                       "spontaneous ignition creates brief pillars of blue-green fire. Breathing "
                       "here requires covering your nose and mouth.",
        "coordinates": [cx - 5, cy - 5],
        "location_type": "wilderness",
        "items": {"swamp_gas_vial": {"quantity": 1, "value": 15}, "gas_ignition_stone": {"quantity": 1, "value": 10}},
        "exits": {
            "west": {"target": "dreadmist_marsh_sinking_trail", "type": "direction"},
            "north": {"target": "dreadmist_marsh_depths", "type": "direction"},
            "east": {"target": "dreadmist_marsh_bone_bridge", "type": "direction"}
        }
    }

    rooms["dreadmist_marsh_bone_bridge"] = {
        "id": "dreadmist_marsh_bone_bridge",
        "name": "Bone Bridge",
        "description": "A bridge constructed entirely from bones — both human and animal — "
                       "spans a deep channel in the marsh. The construction is incredibly "
                       "intricate, each bone fitted precisely without mortar. Who built it and "
                       "why remains one of the island's darkest mysteries.",
        "coordinates": [cx - 4, cy - 5],
        "location_type": "wilderness",
        "items": {"bridge_bone_fragment": {"quantity": 1, "value": 12}, "bone_joiner_paste": {"quantity": 1, "value": 18}},
        "exits": {
            "west": {"target": "dreadmist_marsh_gas_pockets", "type": "direction"},
            "north": {"target": "dreadmist_marsh_sunken_village", "type": "direction"}
        }
    }

    rooms["dreadmist_marsh_lantern_field"] = {
        "id": "dreadmist_marsh_lantern_field",
        "name": "Lantern Field",
        "description": "Dozens of old lanterns hang from poles stuck into the marsh mud, each "
                       "burning with a different colored flame. No one maintains them, yet they "
                       "never go out. The lights create paths through the fog that some say lead "
                       "to treasure, while others insist they lead to doom.",
        "coordinates": [cx - 4, cy - 4],
        "location_type": "wilderness",
        "items": {"spectral_lantern": {"quantity": 1, "value": 25}, "colored_flame_wick": {"quantity": 1, "value": 12}},
        "exits": {
            "east": {"target": "dreadmist_marsh_bog_hollow", "type": "direction"},
            "south": {"target": "dreadmist_marsh_bone_bridge", "type": "direction"}
        }
    }

    rooms["dreadmist_marsh_hag_hut"] = {
        "id": "dreadmist_marsh_hag_hut",
        "name": "Marsh Hag's Hut",
        "description": "A dilapidated hut built on stilts over the stagnant water. Strings of "
                       "dried herbs, animal skulls, and glass bottles hang from the eaves. The "
                       "marsh hag who lives here is ancient and feared — she trades in curses, "
                       "cures, and information that no one else possesses.",
        "coordinates": [cx - 3, cy - 5],
        "location_type": "settlement",
        "items": {"hag_curse_bottle": {"quantity": 1, "value": 35}, "dried_skull_charm": {"quantity": 1, "value": 20}},
        "exits": {
            "north": {"target": "dreadmist_marsh_stagnant_pool", "type": "direction"}
        }
    }

    # --- Expanded Ruined Castle (+6 rooms) ---

    rooms["dreadmist_castle_secret_passage"] = {
        "id": "dreadmist_castle_secret_passage",
        "name": "Secret Passage",
        "description": "A hidden corridor behind the tower peak's wall, accessible through a "
                       "false stone panel. The passage is narrow and dusty, with cobwebs thick "
                       "enough to feel like curtains. It connects the tower to chambers that "
                       "should not exist according to the castle's known layout.",
        "coordinates": [cx + 7, cy - 2],
        "location_type": "building",
        "items": {"secret_passage_map": {"quantity": 1, "value": 20}, "false_panel_stone": {"quantity": 1, "value": 8}},
        "exits": {
            "west": {"target": "dreadmist_castle_tower_peak", "type": "direction"},
            "south": {"target": "dreadmist_castle_hidden_library", "type": "direction"}
        }
    }

    rooms["dreadmist_castle_hidden_library"] = {
        "id": "dreadmist_castle_hidden_library",
        "name": "Hidden Library",
        "description": "A library concealed within the castle walls, its existence unknown to "
                       "most. Shelves of grimoires, forbidden texts, and necromantic research "
                       "fill the room. This was clearly a place of dark study — the lord of "
                       "this castle had interests beyond governance.",
        "coordinates": [cx + 7, cy - 3],
        "location_type": "building",
        "items": {"forbidden_grimoire": {"quantity": 1, "value": 45}, "necromantic_notes": {"quantity": 1, "value": 30}},
        "exits": {
            "north": {"target": "dreadmist_castle_secret_passage", "type": "direction"},
            "west": {"target": "dreadmist_castle_collapsed_tower", "type": "direction"}
        }
    }

    rooms["dreadmist_castle_torture_chamber"] = {
        "id": "dreadmist_castle_torture_chamber",
        "name": "Torture Chamber",
        "description": "A grim chamber deep beneath the castle filled with rusted instruments "
                       "of cruelty. Iron maidens, racks, and chains line the walls. Dark stains "
                       "on the floor tell of the suffering that occurred here. The air carries "
                       "an unshakeable chill that no torch can dispel.",
        "coordinates": [cx + 4, cy + 2],
        "location_type": "building",
        "items": {"rusted_shackle": {"quantity": 1, "value": 8}, "dungeon_key_ring": {"quantity": 1, "value": 18}},
        "exits": {
            "south": {"target": "dreadmist_castle_dungeon", "type": "direction"},
            "east": {"target": "dreadmist_castle_crypt_entrance", "type": "direction"}
        }
    }

    rooms["dreadmist_castle_crypt_entrance"] = {
        "id": "dreadmist_castle_crypt_entrance",
        "name": "Castle Crypt Entrance",
        "description": "A doorway descending into the castle's family crypt. Stone sarcophagi "
                       "line the walls of the passage, each bearing the carved likeness of a "
                       "past lord or lady. Some sarcophagi are cracked, and scratching sounds "
                       "come from within.",
        "coordinates": [cx + 5, cy + 2],
        "location_type": "building",
        "items": {"sarcophagus_fragment": {"quantity": 1, "value": 15}, "lord_signet_ring": {"quantity": 1, "value": 30}},
        "exits": {
            "west": {"target": "dreadmist_castle_torture_chamber", "type": "direction"},
            "south": {"target": "dreadmist_castle_royal_crypt", "type": "direction"}
        }
    }

    rooms["dreadmist_castle_royal_crypt"] = {
        "id": "dreadmist_castle_royal_crypt",
        "name": "Royal Crypt",
        "description": "The final resting place of the castle's ruling family, an ornate chamber "
                       "with vaulted ceilings and faded murals depicting their lineage. The "
                       "central sarcophagus — the lord's — has been opened, its stone lid "
                       "pushed aside. The body within is missing.",
        "coordinates": [cx + 5, cy + 1],
        "location_type": "building",
        "items": {"empty_sarcophagus_dust": {"quantity": 1, "value": 5}, "royal_crown_fragment": {"quantity": 1, "value": 40}},
        "exits": {
            "north": {"target": "dreadmist_castle_crypt_entrance", "type": "direction"}
        }
    }

    rooms["dreadmist_castle_ruined_garden"] = {
        "id": "dreadmist_castle_ruined_garden",
        "name": "Ruined Castle Garden",
        "description": "Once a formal garden, now a tangle of dead hedges and overgrown paths. "
                       "A broken fountain stands at the center, its basin filled with dark water. "
                       "Stone benches lie toppled, and the remains of ornamental statues are "
                       "barely recognizable under layers of moss and decay.",
        "coordinates": [cx + 3, cy - 4],
        "location_type": "wilderness",
        "items": {"broken_fountain_piece": {"quantity": 1, "value": 10}, "dead_garden_rose": {"quantity": 1, "value": 8}},
        "exits": {
            "south": {"target": "dreadmist_castle_road", "type": "direction"}
        }
    }

    # --- Expanded Dark Ritual Sites (+4 rooms) ---

    rooms["dreadmist_ritual_shadow_sanctum"] = {
        "id": "dreadmist_ritual_shadow_sanctum",
        "name": "Shadow Sanctum",
        "description": "Beyond the dark obelisk, a sanctum of pure darkness. Light sources dim "
                       "and fail within its boundaries. The ground is inscribed with a massive "
                       "pentagram of silver that glows faintly, the only illumination. Something "
                       "powerful was summoned here — perhaps something that never left.",
        "coordinates": [cx + 3, cy + 5],
        "location_type": "wilderness",
        "items": {"silver_pentagram_fragment": {"quantity": 1, "value": 40}, "shadow_essence": {"quantity": 1, "value": 35}},
        "exits": {
            "west": {"target": "dreadmist_ritual_dark_obelisk", "type": "direction"},
            "north": {"target": "dreadmist_ritual_summoning_pit", "type": "direction"},
            "south": {"target": "dreadmist_ritual_bone_circle", "type": "direction"}
        }
    }

    rooms["dreadmist_ritual_summoning_pit"] = {
        "id": "dreadmist_ritual_summoning_pit",
        "name": "Summoning Pit",
        "description": "A deep pit ringed with iron stakes and binding runes. The pit descends "
                       "further than should be possible — torches dropped in fall for several "
                       "seconds before the light vanishes. The runes pulse with dark energy, "
                       "suggesting the binding is still active.",
        "coordinates": [cx + 3, cy + 6],
        "location_type": "wilderness",
        "items": {"binding_rune_stone": {"quantity": 1, "value": 35}, "iron_binding_stake": {"quantity": 1, "value": 20}},
        "exits": {
            "south": {"target": "dreadmist_ritual_shadow_sanctum", "type": "direction"}
        }
    }

    rooms["dreadmist_ritual_bone_circle"] = {
        "id": "dreadmist_ritual_bone_circle",
        "name": "Bone Circle",
        "description": "A circle of standing bones — femurs and tibias driven into the ground "
                       "like fence posts — surrounds a flat stone altar. Dark stains coat the "
                       "altar's surface, and the air tastes of iron. This is where lesser "
                       "rituals were performed in service to the greater summoning.",
        "coordinates": [cx + 3, cy + 4],
        "location_type": "wilderness",
        "items": {"ritual_bone_post": {"quantity": 1, "value": 15}, "altar_blood_stone": {"quantity": 1, "value": 22}},
        "exits": {
            "north": {"target": "dreadmist_ritual_shadow_sanctum", "type": "direction"},
            "west": {"target": "dreadmist_ritual_blood_circle", "type": "direction"}
        }
    }

    rooms["dreadmist_ritual_spirit_well"] = {
        "id": "dreadmist_ritual_spirit_well",
        "name": "Spirit Well",
        "description": "A stone well not drawing water but spirits. Ghostly wisps drift upward "
                       "from its depths, dissipating in the cold air. Dropping objects in "
                       "produces no sound of impact. The well is said to connect to the "
                       "underworld itself.",
        "coordinates": [cx + 1, cy + 5],
        "location_type": "wilderness",
        "items": {"spirit_well_water": {"quantity": 1, "value": 30}, "underworld_whisper_stone": {"quantity": 1, "value": 25}},
        "exits": {
            "south": {"target": "dreadmist_ritual_sacrificial_altar", "type": "direction"},
            "east": {"target": "dreadmist_ritual_dark_obelisk", "type": "direction"}
        }
    }

    # === NEW SUB-REGION: Whispering Catacombs (18 rooms) ===

    rooms["dreadmist_catacombs_entrance"] = {
        "id": "dreadmist_catacombs_entrance",
        "name": "Catacombs Entrance",
        "description": "A yawning entrance in the earth, framed by carved stone skulls. Steps "
                       "descend into darkness, and a cold draft carries the whisper of countless "
                       "voices. This is the entrance to the Whispering Catacombs — the ancient "
                       "burial complex beneath the island.",
        "coordinates": [cx - 1, cy + 6],
        "location_type": "wilderness",
        "items": {"skull_frame_chip": {"quantity": 1, "value": 10}},
        "exits": {
            "north": {"target": "dreadmist_necropolis_catacombs", "type": "direction"},
            "south": {"target": "dreadmist_catacombs_gallery", "type": "direction"}
        }
    }

    rooms["dreadmist_catacombs_gallery"] = {
        "id": "dreadmist_catacombs_gallery",
        "name": "Gallery of the Dead",
        "description": "A long corridor with niches carved into both walls, each holding a "
                       "skeletal occupant. Some are arranged in poses — sitting, reading, or "
                       "praying — as if death were merely a pause in their activities. Plaques "
                       "identify each occupant, though some names have been deliberately defaced.",
        "coordinates": [cx - 1, cy + 7],
        "location_type": "wilderness",
        "items": {"defaced_name_plaque": {"quantity": 1, "value": 12}, "arranged_skeleton_trinket": {"quantity": 1, "value": 15}},
        "exits": {
            "south": {"target": "dreadmist_catacombs_entrance", "type": "direction"},
            "north": {"target": "dreadmist_catacombs_crossroads", "type": "direction"},
            "east": {"target": "dreadmist_catacombs_candle_hall", "type": "direction"}
        }
    }

    rooms["dreadmist_catacombs_candle_hall"] = {
        "id": "dreadmist_catacombs_candle_hall",
        "name": "Candle Hall",
        "description": "A chamber illuminated by hundreds of candles, each representing a soul "
                       "interred in the catacombs. When a candle dies, the corresponding spirit "
                       "is said to move on. Some candles have burned for centuries without "
                       "shortening. Others flicker and sputter, on the verge of going out.",
        "coordinates": [cx, cy + 7],
        "location_type": "wilderness",
        "items": {"eternal_candle": {"quantity": 1, "value": 20}, "soul_candle_wax": {"quantity": 2, "value": 8}},
        "exits": {
            "west": {"target": "dreadmist_catacombs_gallery", "type": "direction"},
            "east": {"target": "dreadmist_catacombs_echo_tomb", "type": "direction"}
        }
    }

    rooms["dreadmist_catacombs_echo_tomb"] = {
        "id": "dreadmist_catacombs_echo_tomb",
        "name": "Echo Tomb",
        "description": "A circular chamber where the whispers of the catacombs concentrate. "
                       "Standing at the center, you can hear fragments of speech from the dead "
                       "— names, pleas, confessions. The effect is deeply unsettling, yet some "
                       "mediums seek this place to communicate with specific spirits.",
        "coordinates": [cx + 1, cy + 7],
        "location_type": "wilderness",
        "items": {"echo_tomb_recording": {"quantity": 1, "value": 25}, "spirit_voice_crystal": {"quantity": 1, "value": 30}},
        "exits": {
            "west": {"target": "dreadmist_catacombs_candle_hall", "type": "direction"}
        }
    }

    rooms["dreadmist_catacombs_crossroads"] = {
        "id": "dreadmist_catacombs_crossroads",
        "name": "Catacomb Crossroads",
        "description": "A junction where four passages meet beneath a domed ceiling painted "
                       "with faded depictions of death and judgment. Directional carvings mark "
                       "each passage — a skull for north, a weeping face for south, an open "
                       "hand for east, and a closed fist for west.",
        "coordinates": [cx - 1, cy + 8],
        "location_type": "wilderness",
        "items": {"crossroads_direction_stone": {"quantity": 1, "value": 10}},
        "exits": {
            "south": {"target": "dreadmist_catacombs_gallery", "type": "direction"},
            "north": {"target": "dreadmist_catacombs_noble_tombs", "type": "direction"},
            "east": {"target": "dreadmist_catacombs_bone_chapel", "type": "direction"},
            "west": {"target": "dreadmist_catacombs_flooded_passage", "type": "direction"}
        }
    }

    rooms["dreadmist_catacombs_bone_chapel"] = {
        "id": "dreadmist_catacombs_bone_chapel",
        "name": "Bone Chapel",
        "description": "A chapel constructed entirely from human bones — skulls form the walls, "
                       "femurs the pillars, and ribcages the ceiling vaults. A bone altar stands "
                       "at the front, and bone chandeliers hang overhead. Despite the macabre "
                       "construction, the craftsmanship is extraordinary.",
        "coordinates": [cx, cy + 8],
        "location_type": "wilderness",
        "items": {"bone_chapel_fragment": {"quantity": 1, "value": 22}, "bone_chandelier_piece": {"quantity": 1, "value": 18}},
        "exits": {
            "west": {"target": "dreadmist_catacombs_crossroads", "type": "direction"},
            "north": {"target": "dreadmist_catacombs_reliquary", "type": "direction"}
        }
    }

    rooms["dreadmist_catacombs_reliquary"] = {
        "id": "dreadmist_catacombs_reliquary",
        "name": "Reliquary",
        "description": "A secure chamber housing the sacred relics of the island's dead. Glass "
                       "cases hold finger bones of saints, preserved hearts in jars, and holy "
                       "symbols that glow with faint divine light. The relics are said to keep "
                       "the worst undead at bay.",
        "coordinates": [cx, cy + 9],
        "location_type": "wilderness",
        "items": {"holy_relic_shard": {"quantity": 1, "value": 40}, "preserved_saint_bone": {"quantity": 1, "value": 30}},
        "exits": {
            "south": {"target": "dreadmist_catacombs_bone_chapel", "type": "direction"}
        }
    }

    rooms["dreadmist_catacombs_flooded_passage"] = {
        "id": "dreadmist_catacombs_flooded_passage",
        "name": "Flooded Passage",
        "description": "This section of the catacombs has flooded with brackish water, "
                       "submerging the lower burial niches. The water is knee-deep and ice cold, "
                       "with an oily sheen on the surface. Something occasionally disturbs the "
                       "water from below.",
        "coordinates": [cx - 2, cy + 8],
        "location_type": "wilderness",
        "items": {"submerged_burial_goods": {"quantity": 1, "value": 18}, "oily_water_sample": {"quantity": 1, "value": 5}},
        "exits": {
            "east": {"target": "dreadmist_catacombs_crossroads", "type": "direction"},
            "north": {"target": "dreadmist_catacombs_drowned_crypt", "type": "direction"},
            "west": {"target": "dreadmist_catacombs_forgotten_alcove", "type": "direction"}
        }
    }

    rooms["dreadmist_catacombs_drowned_crypt"] = {
        "id": "dreadmist_catacombs_drowned_crypt",
        "name": "Drowned Crypt",
        "description": "A crypt completely submerged in water, its sarcophagi only visible as "
                       "dark shapes below the surface. Bubbles occasionally rise from the "
                       "coffins, and a ghostly luminescence illuminates the water from within. "
                       "Diving here is extremely dangerous.",
        "coordinates": [cx - 2, cy + 9],
        "location_type": "wilderness",
        "items": {"drowned_crypt_gem": {"quantity": 1, "value": 30}, "ghostly_luminescence_vial": {"quantity": 1, "value": 20}},
        "exits": {
            "south": {"target": "dreadmist_catacombs_flooded_passage", "type": "direction"}
        }
    }

    rooms["dreadmist_catacombs_forgotten_alcove"] = {
        "id": "dreadmist_catacombs_forgotten_alcove",
        "name": "Forgotten Alcove",
        "description": "A small chamber that was sealed shut for centuries until the flooding "
                       "weakened its wall. Inside, a single ornate sarcophagus bears the crest "
                       "of a royal family that history has forgotten. The seal was broken "
                       "recently — by something from within.",
        "coordinates": [cx - 3, cy + 8],
        "location_type": "wilderness",
        "items": {"unknown_royal_crest": {"quantity": 1, "value": 35}, "broken_seal_fragment": {"quantity": 1, "value": 15}},
        "exits": {
            "east": {"target": "dreadmist_catacombs_flooded_passage", "type": "direction"},
            "north": {"target": "dreadmist_catacombs_whispering_wall", "type": "direction"}
        }
    }

    rooms["dreadmist_catacombs_whispering_wall"] = {
        "id": "dreadmist_catacombs_whispering_wall",
        "name": "The Whispering Wall",
        "description": "A wall of smooth stone that vibrates with the collected whispers of "
                       "every soul buried in the catacombs. Pressing your ear against it reveals "
                       "a chorus of voices — some speaking languages long dead. The wall is warm "
                       "to the touch, as if something lives within.",
        "coordinates": [cx - 3, cy + 9],
        "location_type": "wilderness",
        "items": {"whispering_wall_stone": {"quantity": 1, "value": 25}, "dead_language_rubbing": {"quantity": 1, "value": 20}},
        "exits": {
            "south": {"target": "dreadmist_catacombs_forgotten_alcove", "type": "direction"},
            "east": {"target": "dreadmist_catacombs_guardian_hall", "type": "direction"}
        }
    }

    rooms["dreadmist_catacombs_guardian_hall"] = {
        "id": "dreadmist_catacombs_guardian_hall",
        "name": "Guardian's Hall",
        "description": "A chamber guarded by statues of armored warriors, their stone swords "
                       "pointed toward the entrance. Beyond them, a passage leads to the deepest "
                       "level of the catacombs. Locals say the guardians animate at night to "
                       "prevent the dead from escaping.",
        "coordinates": [cx - 2, cy + 9],
        "location_type": "wilderness",
        "items": {"guardian_sword_chip": {"quantity": 1, "value": 20}, "animated_stone_dust": {"quantity": 1, "value": 15}},
        "exits": {
            "west": {"target": "dreadmist_catacombs_whispering_wall", "type": "direction"},
            "south": {"target": "dreadmist_catacombs_flooded_passage", "type": "direction"},
            "north": {"target": "dreadmist_catacombs_deep_sanctum", "type": "direction"}
        }
    }

    rooms["dreadmist_catacombs_noble_tombs"] = {
        "id": "dreadmist_catacombs_noble_tombs",
        "name": "Noble Family Tombs",
        "description": "The section reserved for the island's noble families. Each family has "
                       "a private chamber sealed with carved doors depicting their house sigil. "
                       "The wealthiest tombs have doors of silver and gold, though most have "
                       "been plundered. One remains sealed and untouched.",
        "coordinates": [cx - 1, cy + 9],
        "location_type": "wilderness",
        "items": {"noble_sigil_door_piece": {"quantity": 1, "value": 25}, "plundered_tomb_gold": {"quantity": 1, "value": 20}},
        "exits": {
            "south": {"target": "dreadmist_catacombs_crossroads", "type": "direction"},
            "west": {"target": "dreadmist_catacombs_guardian_hall", "type": "direction"}
        }
    }

    rooms["dreadmist_catacombs_deep_sanctum"] = {
        "id": "dreadmist_catacombs_deep_sanctum",
        "name": "Deep Sanctum",
        "description": "The deepest and most sacred chamber of the catacombs, where the island's "
                       "most powerful dead are entombed. The air itself seems to resist intrusion, "
                       "growing colder and heavier with each step. At the center, an obsidian "
                       "coffin radiates an aura of immense dark power.",
        "coordinates": [cx - 2, cy + 10],
        "location_type": "wilderness",
        "items": {"deep_sanctum_crystal": {"quantity": 1, "value": 60}, "obsidian_coffin_shard": {"quantity": 1, "value": 45}},
        "exits": {
            "south": {"target": "dreadmist_catacombs_guardian_hall", "type": "direction"}
        }
    }

    # === NEW SUB-REGION: Fogbound Cliffs (15 rooms) ===

    rooms["dreadmist_fogbound_cliffs_path"] = {
        "id": "dreadmist_fogbound_cliffs_path",
        "name": "Fogbound Cliff Path",
        "description": "A narrow path along the island's western cliffs, perpetually shrouded "
                       "in thick fog. The cliff edge is invisible until you're right upon it, "
                       "making navigation perilous. The fog muffles sound, creating an eerie "
                       "silence broken only by waves far below.",
        "coordinates": [cx - 2, cy - 4],
        "location_type": "wilderness",
        "items": {"fog_condensation_vial": {"quantity": 1, "value": 8}},
        "exits": {
            "east": {"target": "dreadmist_docks_lantern_tower", "type": "direction"},
            "north": {"target": "dreadmist_fogbound_overlook", "type": "direction"},
            "south": {"target": "dreadmist_fogbound_sea_stairs", "type": "direction"}
        }
    }

    rooms["dreadmist_fogbound_overlook"] = {
        "id": "dreadmist_fogbound_overlook",
        "name": "Fogbound Overlook",
        "description": "On rare occasions when the fog briefly thins, this promontory offers "
                       "a glimpse of the churning sea below. Mostly, however, you stand above "
                       "an infinite gray void. Iron railings have been installed, though half "
                       "have rusted away.",
        "coordinates": [cx - 2, cy - 3],
        "location_type": "wilderness",
        "items": {"rusted_railing_piece": {"quantity": 1, "value": 5}, "cliff_moss": {"quantity": 1, "value": 8}},
        "exits": {
            "south": {"target": "dreadmist_fogbound_cliffs_path", "type": "direction"},
            "north": {"target": "dreadmist_fogbound_wind_cave", "type": "direction"},
            "west": {"target": "dreadmist_fogbound_ghost_lighthouse", "type": "direction"}
        }
    }

    rooms["dreadmist_fogbound_ghost_lighthouse"] = {
        "id": "dreadmist_fogbound_ghost_lighthouse",
        "name": "Ghost Lighthouse",
        "description": "A ruined lighthouse on a cliff promontory, its light long dead. Yet "
                       "sailors report seeing a spectral beam sweeping the fog on dark nights. "
                       "Inside, the mechanism is rusted solid, but the lens still glows faintly "
                       "with trapped soul-light.",
        "coordinates": [cx - 3, cy - 3],
        "location_type": "building",
        "items": {"soul_light_lens": {"quantity": 1, "value": 35}, "lighthouse_keeper_journal": {"quantity": 1, "value": 18}},
        "exits": {
            "east": {"target": "dreadmist_fogbound_overlook", "type": "direction"},
            "north": {"target": "dreadmist_fogbound_hermit_cave", "type": "direction"}
        }
    }

    rooms["dreadmist_fogbound_wind_cave"] = {
        "id": "dreadmist_fogbound_wind_cave",
        "name": "Wind Cave",
        "description": "A cave in the cliff face where wind creates haunting musical tones. "
                       "The local legend says the cave sings laments for the drowned. The "
                       "acoustics are remarkable — whispers carry from one end to the other "
                       "with perfect clarity.",
        "coordinates": [cx - 2, cy - 2],
        "location_type": "wilderness",
        "items": {"wind_cave_crystal": {"quantity": 1, "value": 18}, "singing_stone": {"quantity": 1, "value": 15}},
        "exits": {
            "south": {"target": "dreadmist_fogbound_overlook", "type": "direction"},
            "west": {"target": "dreadmist_fogbound_hermit_cave", "type": "direction"},
            "east": {"target": "dreadmist_marsh_trail", "type": "direction"}
        }
    }

    rooms["dreadmist_fogbound_hermit_cave"] = {
        "id": "dreadmist_fogbound_hermit_cave",
        "name": "Hermit's Sea Cave",
        "description": "A sea cave where a hermit mystic has lived for decades, studying the "
                       "island's supernatural phenomena. Journals and sketches cover every wall, "
                       "documenting ghost sightings, spectral patterns, and theories about the "
                       "island's curse.",
        "coordinates": [cx - 3, cy - 2],
        "location_type": "settlement",
        "items": {"mystic_journal": {"quantity": 1, "value": 25}, "ghost_pattern_chart": {"quantity": 1, "value": 20}},
        "exits": {
            "east": {"target": "dreadmist_fogbound_wind_cave", "type": "direction"},
            "south": {"target": "dreadmist_fogbound_ghost_lighthouse", "type": "direction"},
            "north": {"target": "dreadmist_fogbound_tidal_shelf", "type": "direction"}
        }
    }

    rooms["dreadmist_fogbound_sea_stairs"] = {
        "id": "dreadmist_fogbound_sea_stairs",
        "name": "Sea Stairs",
        "description": "Ancient stone stairs carved into the cliff face, descending toward the "
                       "sea. They're slippery with spray and algae, and partially submerged at "
                       "high tide. At the bottom, a small landing provides access to sea caves "
                       "only reachable by water.",
        "coordinates": [cx - 2, cy - 5],
        "location_type": "wilderness",
        "items": {"sea_stair_shell": {"quantity": 2, "value": 4}, "tidal_algae": {"quantity": 1, "value": 6}},
        "exits": {
            "north": {"target": "dreadmist_fogbound_cliffs_path", "type": "direction"},
            "south": {"target": "dreadmist_fogbound_sea_cave", "type": "direction"}
        }
    }

    rooms["dreadmist_fogbound_sea_cave"] = {
        "id": "dreadmist_fogbound_sea_cave",
        "name": "Lower Sea Cave",
        "description": "A cave at the base of the cliffs, accessible only at low tide. The walls "
                       "are carved with ancient maritime symbols and prayers for safe passage. "
                       "A pool in the center is unnaturally still, its surface acting as a "
                       "mirror that sometimes shows things that aren't there.",
        "coordinates": [cx - 2, cy - 6],
        "location_type": "wilderness",
        "items": {"mirror_pool_reflection": {"quantity": 1, "value": 20}, "maritime_prayer_carving": {"quantity": 1, "value": 12}},
        "exits": {
            "north": {"target": "dreadmist_fogbound_sea_stairs", "type": "direction"},
            "west": {"target": "dreadmist_fogbound_shipwreck_beach", "type": "direction"}
        }
    }

    rooms["dreadmist_fogbound_shipwreck_beach"] = {
        "id": "dreadmist_fogbound_shipwreck_beach",
        "name": "Shipwreck Beach",
        "description": "A narrow beach at the cliff base littered with the remains of ships "
                       "that didn't survive the approach. Broken masts, shattered hulls, and "
                       "scattered cargo create a maze of maritime wreckage. Crabs and seabirds "
                       "pick through the debris.",
        "coordinates": [cx - 3, cy - 6],
        "location_type": "wilderness",
        "items": {"ship_captain_compass": {"quantity": 1, "value": 22}, "wrecked_hull_plank": {"quantity": 2, "value": 4}},
        "exits": {
            "east": {"target": "dreadmist_fogbound_sea_cave", "type": "direction"},
            "north": {"target": "dreadmist_fogbound_smuggler_stash", "type": "direction"}
        }
    }

    rooms["dreadmist_fogbound_smuggler_stash"] = {
        "id": "dreadmist_fogbound_smuggler_stash",
        "name": "Smuggler's Stash",
        "description": "A hidden alcove in the cliffs where smugglers stored their most valuable "
                       "contraband. Wooden chests and barrels are tucked into natural niches, "
                       "some still sealed. The location is nearly impossible to find without "
                       "knowing exactly where to look.",
        "coordinates": [cx - 3, cy - 5],
        "location_type": "wilderness",
        "items": {"smuggler_chest": {"quantity": 1, "value": 35}, "sealed_contraband_barrel": {"quantity": 1, "value": 25}},
        "exits": {
            "south": {"target": "dreadmist_fogbound_shipwreck_beach", "type": "direction"},
            "north": {"target": "dreadmist_fogbound_ghost_lighthouse", "type": "direction"}
        }
    }

    rooms["dreadmist_fogbound_tidal_shelf"] = {
        "id": "dreadmist_fogbound_tidal_shelf",
        "name": "Tidal Shelf",
        "description": "A flat rock shelf exposed at low tide, covered with tide pools and "
                       "stranded sea creatures. At night, the shelf is said to be visited by "
                       "the ghosts of drowned sailors who walk the rocks searching for a way "
                       "back to shore.",
        "coordinates": [cx - 3, cy - 1],
        "location_type": "wilderness",
        "items": {"ghost_sailor_token": {"quantity": 1, "value": 20}, "tidal_pool_creature": {"quantity": 1, "value": 10}},
        "exits": {
            "south": {"target": "dreadmist_fogbound_hermit_cave", "type": "direction"},
            "east": {"target": "dreadmist_fogbound_skull_cave", "type": "direction"},
            "north": {"target": "dreadmist_fogbound_wailing_point", "type": "direction"}
        }
    }

    rooms["dreadmist_fogbound_skull_cave"] = {
        "id": "dreadmist_fogbound_skull_cave",
        "name": "Skull Cave",
        "description": "A cave whose entrance is naturally shaped like a screaming skull. "
                       "Inside, phosphorescent fungi cast everything in a sickly green glow. "
                       "Niches in the walls hold actual skulls — hundreds of them — arranged "
                       "in neat rows. A shrine to death occupies the deepest alcove.",
        "coordinates": [cx - 2, cy - 1],
        "location_type": "wilderness",
        "items": {"skull_cave_fungus": {"quantity": 1, "value": 12}, "death_shrine_offering": {"quantity": 1, "value": 22}},
        "exits": {
            "west": {"target": "dreadmist_fogbound_tidal_shelf", "type": "direction"}
        }
    }

    rooms["dreadmist_fogbound_wailing_point"] = {
        "id": "dreadmist_fogbound_wailing_point",
        "name": "Wailing Point",
        "description": "The northernmost point of the fogbound cliffs, where wind and wave "
                       "combine to create a sound uncannily like human wailing. The effect is "
                       "so convincing that search parties have been dispatched to rescue what "
                       "turned out to be nothing but wind and rock.",
        "coordinates": [cx - 4, cy + 2],
        "location_type": "wilderness",
        "items": {"wailing_wind_stone": {"quantity": 1, "value": 15}, "cliff_crystal": {"quantity": 1, "value": 18}},
        "exits": {
            "south": {"target": "dreadmist_fogbound_tidal_shelf", "type": "direction"},
            "east": {"target": "dreadmist_fogbound_mist_garden", "type": "direction"}
        }
    }

    rooms["dreadmist_fogbound_mist_garden"] = {
        "id": "dreadmist_fogbound_mist_garden",
        "name": "Mist Garden",
        "description": "A natural garden thriving in the constant fog and salt spray. Strange "
                       "plants that exist nowhere else grow here — ghost orchids that are "
                       "translucent, fog-drinker vines that absorb moisture from the air, and "
                       "death's cap mushrooms with an eerie blue glow.",
        "coordinates": [cx - 2, cy],
        "location_type": "wilderness",
        "items": {"ghost_orchid": {"quantity": 1, "value": 28}, "fog_drinker_vine": {"quantity": 1, "value": 18}},
        "exits": {
            "west": {"target": "dreadmist_fogbound_wailing_point", "type": "direction"}
        }
    }



def generate_wyrmscale_island(rooms):
    """Generate Island 6: Wyrmscale Isle - Dragon-dominated volcanic island (~75 rooms)."""

    cx, cy = -45, -50  # Center coordinates

    # =========================================================================
    # WYRMSCALE ISLE - Dragon Island (Level 30+)
    # Sub-regions: Docks, Wyrm Village, Dragonbone Wastes, Wyrmfire Peaks,
    #              Scale Forest, Hatchery, Elder Wyrm's Domain, Dragonbone Forge
    # =========================================================================

    # --- Wyrmscale Docks (3 rooms) ---

    rooms["wyrm_docks"] = {
        "id": "wyrm_docks",
        "name": "Wyrmscale Isle - Dragon's Landing",
        "description": "A dock of scorched basalt juts into waters stained orange by volcanic runoff. "
                       "Massive claw marks gouge the stone, and the charred remains of a previous dock "
                       "smoulder nearby. Overhead, winged silhouettes circle lazily against a sky choked "
                       "with ash and ember.",
        "coordinates": [cx, cy - 6],
        "location_type": "dock",
        "items": {},
        "exits": {
            "board mainland": {
                "target": "harbor_west_dock",
                "type": "boat_travel",
                "island_id": "wyrmscale_isle",
                "display": "Return to Grand Harbor",
                "unlock_cost": 0,
                "fare_cost": 0,
                "min_level": 1,
                "transition_text": "You board the dragon-scale plated vessel. The crew keeps a wary eye\non the circling shapes above as the ship pulls away from the scorched\ndock. After seven days of tense sailing, the familiar lights of Grand\nHarbor appear on the horizon..."
            },
            "north": {"target": "wyrm_docks_path", "type": "direction"},
            "east": {"target": "wyrm_docks_cargo", "type": "direction"},
            "west": {"target": "wyrm_docks_watchtower", "type": "direction"}
        }
    }

    rooms["wyrm_docks_cargo"] = {
        "id": "wyrm_docks_cargo",
        "name": "Fireproof Cargo Hold",
        "description": "A bunker-like warehouse carved into the cliff face, its walls lined with thick "
                       "dragonscale tiles to withstand stray blasts of fire. Crates of obsidian ore, "
                       "bundles of fireproof cloth, and sealed amphorae of drake oil are stacked on "
                       "iron racks bolted to the floor.",
        "coordinates": [cx + 1, cy - 6],
        "location_type": "dock",
        "items": {"drake_oil_amphora": {"quantity": 1, "value": 22}, "fireproof_cloth": {"quantity": 2, "value": 15}},
        "exits": {
            "west": {"target": "wyrm_docks", "type": "direction"},
            "east": {"target": "wyrm_docks_tide_pools", "type": "direction"}
        }
    }

    rooms["wyrm_docks_watchtower"] = {
        "id": "wyrm_docks_watchtower",
        "name": "Dragon Watch Tower",
        "description": "A squat iron tower topped with a smouldering signal brazier. Sentries in "
                       "scale-mail armour scan the skies through slitted visors, tracking the flight "
                       "paths of the island's dragon inhabitants. A horn of blackened bone hangs by "
                       "the door — three blasts means a dragon is attacking the docks.",
        "coordinates": [cx - 1, cy - 6],
        "location_type": "building",
        "items": {"signal_horn_shard": {"quantity": 1, "value": 18}},
        "exits": {
            "east": {"target": "wyrm_docks", "type": "direction"},
            "west": {"target": "wyrm_docks_signal_cove", "type": "direction"}
        }
    }

    # --- Wyrm Village (15 rooms) ---

    rooms["wyrm_docks_path"] = {
        "id": "wyrm_docks_path",
        "name": "Scorched Ascent",
        "description": "A winding path of fused volcanic glass climbs steeply from the docks into "
                       "the interior. The rock on either side is scarred with blast marks and littered "
                       "with shed dragon scales the size of dinner plates. The air tastes of sulfur "
                       "and hot iron.",
        "coordinates": [cx, cy - 5],
        "location_type": "wilderness",
        "items": {"shed_dragon_scale": {"quantity": 2, "value": 12}},
        "exits": {
            "south": {"target": "wyrm_docks", "type": "direction"},
            "north": {"target": "wyrm_village_gate", "type": "direction"}
        }
    }

    rooms["wyrm_village_gate"] = {
        "id": "wyrm_village_gate",
        "name": "Wyrmscale Village Gate",
        "description": "A gate forged from interlocking dragon bones arches over the path, reinforced "
                       "with bands of dark iron. The skulls of two lesser drakes are mounted on the "
                       "pillars, their empty eye sockets flickering with enchanted flame. Guards with "
                       "scale-pattern tattoos wave you through with spears tipped in dragontooth.",
        "coordinates": [cx, cy - 4],
        "location_type": "settlement",
        "items": {},
        "exits": {
            "south": {"target": "wyrm_docks_path", "type": "direction"},
            "north": {"target": "wyrm_village_center", "type": "direction"},
            "east": {"target": "wyrm_village_barracks", "type": "direction"},
            "west": {"target": "wyrm_village_stable", "type": "direction"}
        }
    }

    rooms["wyrm_village_center"] = {
        "id": "wyrm_village_center",
        "name": "Wyrm Village - Central Square",
        "description": "The heart of the dragonkin settlement is a wide plaza paved with hexagonal "
                       "scales of volcanic stone. A fountain carved in the shape of a coiled wyrm "
                       "spouts steaming water from its jaws. Scaled warriors mingle with merchants "
                       "beneath awnings of tanned dragon-wing membrane.",
        "coordinates": [cx, cy - 3],
        "location_type": "settlement",
        "items": {},
        "exits": {
            "south": {"target": "wyrm_village_gate", "type": "direction"},
            "north": {"target": "wyrm_village_elder", "type": "direction"},
            "east": {"target": "wyrm_village_market", "type": "direction"},
            "west": {"target": "wyrm_village_inn", "type": "direction"},
            "northeast": {"target": "wyrm_village_smithy", "type": "direction"},
            "northwest": {"target": "wyrm_village_shrine", "type": "direction"}
        }
    }

    rooms["wyrm_village_elder"] = {
        "id": "wyrm_village_elder",
        "name": "Elder Drakenthis's Hall",
        "description": "A grand hall built within the ribcage of a colossal ancient dragon. The curved "
                       "bones form natural arches overhead, and the floor is tiled with polished dragon "
                       "scales. Elder Drakenthis — an ancient dragonkin with silver-grey scales — sits "
                       "on a throne of fused obsidian, dispensing wisdom and justice.",
        "coordinates": [cx, cy - 2],
        "location_type": "building",
        "npcs": ["elder_drakenthis"],
        "items": {"wyrm_elder_blessing_scroll": {"quantity": 1, "value": 45}, "ancient_scale_fragment": {"quantity": 1, "value": 35}},
        "exits": {
            "south": {"target": "wyrm_village_center", "type": "direction"},
            "east": {"target": "wyrm_village_library", "type": "direction"},
            "north": {"target": "wyrm_village_overlook", "type": "direction"}
        }
    }

    rooms["wyrm_village_market"] = {
        "id": "wyrm_village_market",
        "name": "Wyrm Bazaar",
        "description": "An open-air market sheltered under canopies of stretched dragon-wing leather. "
                       "Vendors sell dragon-scale armour pieces, fireproof potions, obsidian blades, "
                       "and exotic meats smoked over dragonfire. The haggling is fierce and conducted "
                       "partly in Draconic, with many gestures and the occasional puff of smoke.",
        "coordinates": [cx + 1, cy - 3],
        "location_type": "settlement",
        "shop": True,
        "items": {"fireproof_potion": {"quantity": 3, "value": 20}, "smoked_drake_meat": {"quantity": 2, "value": 10}},
        "exits": {
            "west": {"target": "wyrm_village_center", "type": "direction"},
            "east": {"target": "wyrm_village_apothecary", "type": "direction"}
        }
    }

    rooms["wyrm_village_apothecary"] = {
        "id": "wyrm_village_apothecary",
        "name": "The Ember Remedy",
        "description": "A cramped shop thick with the scent of burned herbs and dragon bile. Shelves "
                       "hold phials of wyrm-blood tonic, drake-venom antidote, and salves made from "
                       "powdered dragon horn. The apothecary — a wiry dragonkin with cracked amber "
                       "scales — mutters Draconic incantations over each remedy.",
        "coordinates": [cx + 2, cy - 3],
        "location_type": "building",
        "items": {"wyrm_blood_tonic": {"quantity": 2, "value": 25}, "drake_venom_antidote": {"quantity": 1, "value": 18}},
        "exits": {
            "west": {"target": "wyrm_village_market", "type": "direction"}
        }
    }

    rooms["wyrm_village_inn"] = {
        "id": "wyrm_village_inn",
        "name": "The Smouldering Claw Inn",
        "description": "A tavern carved from a massive lava tube, its walls blackened by centuries of "
                       "dragonfire. The common room is lit by braziers of slow-burning ember-stone, and "
                       "the ale is served warm — everything here is warm. Dragonkin warriors swap tales "
                       "of hunts and raids over platters of charred boar.",
        "coordinates": [cx - 1, cy - 3],
        "location_type": "building",
        "items": {"ember_ale": {"quantity": 2, "value": 8}, "charred_boar_rib": {"quantity": 1, "value": 6}},
        "exits": {
            "east": {"target": "wyrm_village_center", "type": "direction"},
            "west": {"target": "wyrm_village_healer", "type": "direction"}
        }
    }

    rooms["wyrm_village_healer"] = {
        "id": "wyrm_village_healer",
        "name": "Dragon's Breath Healery",
        "description": "A round hut of heat-resistant stone where an elderly dragonkin healer tends to "
                       "burn wounds and claw marks. Poultices of aloe and ground fire-opal line the "
                       "shelves, and a small drake curls by the hearth, its breath keeping the healing "
                       "herbs at the perfect temperature for drying.",
        "coordinates": [cx - 2, cy - 3],
        "location_type": "building",
        "npcs": ["wyrm_healer"],
        "items": {"fire_opal_poultice": {"quantity": 2, "value": 20}, "burn_salve": {"quantity": 3, "value": 12}},
        "exits": {
            "east": {"target": "wyrm_village_inn", "type": "direction"}
        }
    }

    rooms["wyrm_village_smithy"] = {
        "id": "wyrm_village_smithy",
        "name": "Wyrmfire Smithy",
        "description": "A forge that uses captured dragonfire instead of coal. The heat is staggering, "
                       "and the smith — a massive dragonkin with arms like tree trunks — hammers "
                       "obsidian-edged blades on an anvil of meteoric iron. Weapons here are tempered "
                       "in drake blood and quenched in volcanic spring water.",
        "coordinates": [cx + 1, cy - 2],
        "location_type": "building",
        "items": {"obsidian_blade_blank": {"quantity": 1, "value": 30}, "meteoric_iron_ingot": {"quantity": 1, "value": 40}},
        "exits": {
            "southwest": {"target": "wyrm_village_center", "type": "direction"}
        }
    }

    rooms["wyrm_village_shrine"] = {
        "id": "wyrm_village_shrine",
        "name": "Shrine of the First Wyrm",
        "description": "A sacred grotto where a massive dragon skull — ancient beyond reckoning — is "
                       "enshrined on a pedestal of volcanic glass. Offerings of polished scales, fire "
                       "opals, and dragon teeth are arranged before it. The dragonkin come here to pay "
                       "homage to the progenitor of all wyrms.",
        "coordinates": [cx - 1, cy - 2],
        "location_type": "building",
        "items": {"fire_opal_offering": {"quantity": 1, "value": 35}, "wyrm_prayer_bead": {"quantity": 2, "value": 14}},
        "exits": {
            "southeast": {"target": "wyrm_village_center", "type": "direction"}
        }
    }

    rooms["wyrm_village_barracks"] = {
        "id": "wyrm_village_barracks",
        "name": "Scaleguard Barracks",
        "description": "A fortified building where the village's warriors live and train. Racks of "
                       "dragon-scale shields and obsidian spears line the walls. A training yard out "
                       "back is scorched black from sparring with live fire. The Scaleguard captain "
                       "keeps discipline tight — threats from the wilds are constant.",
        "coordinates": [cx + 1, cy - 4],
        "location_type": "building",
        "items": {"scale_shield_fragment": {"quantity": 1, "value": 22}, "obsidian_spear_tip": {"quantity": 1, "value": 18}},
        "exits": {
            "west": {"target": "wyrm_village_gate", "type": "direction"}
        }
    }

    rooms["wyrm_village_stable"] = {
        "id": "wyrm_village_stable",
        "name": "Drake Stable",
        "description": "A pen of reinforced iron bars where domesticated lesser drakes are kept. The "
                       "creatures snort puffs of smoke and eye newcomers with predatory intelligence. "
                       "Dragonkin riders saddle and feed their mounts here, using chunks of raw ore "
                       "and fire-charred meat.",
        "coordinates": [cx - 1, cy - 4],
        "location_type": "building",
        "items": {"drake_saddle_strap": {"quantity": 1, "value": 16}, "fire_charred_meat": {"quantity": 2, "value": 8}},
        "exits": {
            "east": {"target": "wyrm_village_gate", "type": "direction"}
        }
    }

    rooms["wyrm_village_library"] = {
        "id": "wyrm_village_library",
        "name": "Hall of Dragon Lore",
        "description": "A cavern lined with shelves of scrolls and tablets inscribed in Draconic script. "
                       "The texts chronicle the history of dragons on the island — their wars, their "
                       "alliances, and the pact that allows the dragonkin to live among them. A great "
                       "mural depicts the Elder Wyrm in all its terrible glory.",
        "coordinates": [cx + 2, cy - 2],
        "location_type": "building",
        "items": {"draconic_scroll": {"quantity": 1, "value": 28}, "dragon_lore_tablet": {"quantity": 1, "value": 32}},
        "exits": {
            "west": {"target": "wyrm_village_elder", "type": "direction"},
            "east": {"target": "wyrm_village_scroll_vault", "type": "direction"}
        }
    }

    rooms["wyrm_village_armory"] = {
        "id": "wyrm_village_armory",
        "name": "Wyrmscale Armory",
        "description": "A vault of dragon-scale armour and weapons forged from dragonbone. Suits of "
                       "interlocking scale-mail hang from iron mannequins, each set fitted for a "
                       "different warrior caste. The quartermaster inspects each piece with obsessive "
                       "care — poorly maintained gear gets you killed on this island.",
        "coordinates": [cx + 2, cy - 4],
        "location_type": "building",
        "items": {"wyrmscale_gauntlet": {"quantity": 1, "value": 38}, "dragonbone_arrowhead": {"quantity": 3, "value": 14}},
        "exits": {
            "west": {"target": "wyrm_village_barracks", "type": "direction"}
        }
    }

    rooms["wyrm_village_training_yard"] = {
        "id": "wyrm_village_training_yard",
        "name": "Scaleguard Training Yard",
        "description": "An open-air yard of scorched volcanic stone where dragonkin warriors spar with "
                       "obsidian weapons and practice formations against drake-shaped targets. The ground "
                       "is scarred with blast marks from live-fire drills, and a rack of battered training "
                       "shields stands against the barracks wall.",
        "coordinates": [cx + 1, cy - 5],
        "location_type": "building",
        "items": {"training_obsidian_blade": {"quantity": 1, "value": 18}, "battered_scale_shield": {"quantity": 1, "value": 14}},
        "exits": {
            "south": {"target": "wyrm_village_barracks", "type": "direction"},
            "west": {"target": "wyrm_docks_path", "type": "direction"}
        }
    }

    rooms["wyrm_village_watchtower"] = {
        "id": "wyrm_village_watchtower",
        "name": "Village Watchtower",
        "description": "A tall tower of reinforced dragonbone and iron rising above the village rooftops. "
                       "From the top, sentries scan the skies and surrounding terrain for threats — wild "
                       "drakes, volcanic eruptions, and the occasional territorial dispute between adult "
                       "dragons. A signal drum sits ready for emergencies.",
        "coordinates": [cx - 2, cy - 4],
        "location_type": "building",
        "items": {"watchtower_spyglass": {"quantity": 1, "value": 24}},
        "exits": {
            "east": {"target": "wyrm_village_stable", "type": "direction"}
        }
    }

    rooms["wyrm_village_overlook"] = {
        "id": "wyrm_village_overlook",
        "name": "Dragon's Eye Overlook",
        "description": "A high terrace of volcanic glass offering a panoramic view of the island. "
                       "To the west, bleached dragonbone formations rise from the wastes. To the east, "
                       "volcanic peaks trail plumes of black smoke. The scale forest glimmers in the "
                       "north, and the faint glow of the hatchery pulsates beyond the ridgeline.",
        "coordinates": [cx, cy - 1],
        "location_type": "settlement",
        "items": {},
        "exits": {
            "south": {"target": "wyrm_village_elder", "type": "direction"},
            "west": {"target": "wyrm_wastes_edge", "type": "direction"},
            "east": {"target": "wyrm_peaks_trail", "type": "direction"},
            "north": {"target": "wyrm_forest_border", "type": "direction"}
        }
    }

    # --- Dragonbone Wastes (12 rooms) ---

    rooms["wyrm_wastes_edge"] = {
        "id": "wyrm_wastes_edge",
        "name": "Edge of the Dragonbone Wastes",
        "description": "The landscape shifts abruptly to a desolate expanse of sun-bleached bone and "
                       "ash-grey sand. Enormous ribcages of fallen dragons arch overhead like natural "
                       "cathedrals. The wind moans through hollow bones, creating an unearthly dirge "
                       "that never ceases.",
        "coordinates": [cx - 2, cy - 1],
        "location_type": "wilderness",
        "items": {"bleached_dragon_rib": {"quantity": 1, "value": 20}},
        "exits": {
            "east": {"target": "wyrm_village_overlook", "type": "direction"},
            "west": {"target": "wyrm_wastes_bone_arch", "type": "direction"},
            "north": {"target": "wyrm_wastes_scale_field", "type": "direction"},
            "south": {"target": "wyrm_wastes_skull_hollow", "type": "direction"}
        }
    }

    rooms["wyrm_wastes_bone_arch"] = {
        "id": "wyrm_wastes_bone_arch",
        "name": "Bone Arch Passage",
        "description": "Two titanic dragon spines curve together to form a natural archway over the path. "
                       "Smaller bones crunch underfoot like gravel, and the smell of ancient calcium and "
                       "dust fills the air. Scavenger birds with scales instead of feathers perch on the "
                       "vertebrae, watching with unblinking reptilian eyes.",
        "coordinates": [cx - 3, cy - 1],
        "location_type": "wilderness",
        "items": {"dragon_vertebra_chunk": {"quantity": 1, "value": 16}},
        "exits": {
            "east": {"target": "wyrm_wastes_edge", "type": "direction"},
            "north": {"target": "wyrm_wastes_graveyard", "type": "direction"},
            "west": {"target": "wyrm_wastes_fossil_cave", "type": "direction"}
        }
    }

    rooms["wyrm_wastes_skull_hollow"] = {
        "id": "wyrm_wastes_skull_hollow",
        "name": "Skull Hollow",
        "description": "The hollowed-out skull of an enormous ancient dragon serves as a natural shelter. "
                       "Its eye sockets are large enough to walk through, and its jaws still hold teeth "
                       "longer than swords. Dragonkin pilgrims have left offerings of scales and gems "
                       "inside the cranium.",
        "coordinates": [cx - 2, cy - 2],
        "location_type": "wilderness",
        "items": {"ancient_dragon_tooth": {"quantity": 1, "value": 42}, "pilgrim_scale_offering": {"quantity": 1, "value": 15}},
        "exits": {
            "north": {"target": "wyrm_wastes_edge", "type": "direction"}
        }
    }

    rooms["wyrm_wastes_scale_field"] = {
        "id": "wyrm_wastes_scale_field",
        "name": "Dragon Scale Field",
        "description": "A vast field carpeted in shed dragon scales of every colour — obsidian black, "
                       "iron grey, ember red, and rare flashes of iridescent gold. The scales clatter "
                       "in the wind like ceramic tiles. Some are large enough to use as shields, and "
                       "dragonkin gatherers pick through them for crafting materials.",
        "coordinates": [cx - 2, cy],
        "location_type": "wilderness",
        "items": {"iridescent_dragon_scale": {"quantity": 1, "value": 48}, "iron_dragon_scale": {"quantity": 2, "value": 18}},
        "exits": {
            "south": {"target": "wyrm_wastes_edge", "type": "direction"},
            "west": {"target": "wyrm_wastes_spine_ridge", "type": "direction"},
            "north": {"target": "wyrm_wastes_claw_gorge", "type": "direction"},
            "east": {"target": "wyrm_forge_entrance", "type": "direction"}
        }
    }

    rooms["wyrm_wastes_graveyard"] = {
        "id": "wyrm_wastes_graveyard",
        "name": "Dragon Graveyard",
        "description": "An ancient sacred site where dragons come to die. Complete skeletons lie in "
                       "peaceful poses, their bones slowly petrifying into stone. The ground hums with "
                       "residual draconic magic, and faint spectral shapes of dragons drift between "
                       "the remains like fog.",
        "coordinates": [cx - 3, cy],
        "location_type": "wilderness",
        "items": {"petrified_dragonbone": {"quantity": 1, "value": 38}, "spectral_scale_dust": {"quantity": 1, "value": 26}},
        "exits": {
            "south": {"target": "wyrm_wastes_bone_arch", "type": "direction"},
            "north": {"target": "wyrm_wastes_ossuary", "type": "direction"},
            "east": {"target": "wyrm_wastes_spine_ridge", "type": "direction"}
        }
    }

    rooms["wyrm_wastes_spine_ridge"] = {
        "id": "wyrm_wastes_spine_ridge",
        "name": "Spine Ridge",
        "description": "A ridge formed by the partially-buried spine of a dragon so massive it defies "
                       "comprehension. Each vertebra is the size of a house, rising from the earth like "
                       "a mountainous serpent. The wind howls between the bony projections, and the "
                       "view from the top stretches across the entire wasteland.",
        "coordinates": [cx - 3, cy + 1],
        "location_type": "wilderness",
        "items": {"colossal_vertebra_shard": {"quantity": 1, "value": 30}},
        "exits": {
            "south": {"target": "wyrm_wastes_graveyard", "type": "direction"},
            "east": {"target": "wyrm_wastes_scale_field", "type": "direction"},
            "north": {"target": "wyrm_wastes_marrow_pool", "type": "direction"}
        }
    }

    rooms["wyrm_wastes_fossil_cave"] = {
        "id": "wyrm_wastes_fossil_cave",
        "name": "Fossil Cave",
        "description": "A cavern whose walls are embedded with the fossilized remains of prehistoric "
                       "dragons — species that went extinct millennia ago. Their stone bones protrude "
                       "from the rock in twisted poses, preserved mid-flight or mid-roar. Scholars "
                       "would pay a fortune to study this place.",
        "coordinates": [cx - 4, cy - 1],
        "location_type": "wilderness",
        "items": {"prehistoric_dragon_fossil": {"quantity": 1, "value": 55}, "fossil_amber_shard": {"quantity": 1, "value": 22}},
        "exits": {
            "east": {"target": "wyrm_wastes_bone_arch", "type": "direction"},
            "west": {"target": "wyrm_wastes_petrified_nest", "type": "direction"}
        }
    }

    rooms["wyrm_wastes_claw_gorge"] = {
        "id": "wyrm_wastes_claw_gorge",
        "name": "Claw Gorge",
        "description": "A deep gorge carved by the death throes of an ancient dragon whose petrified "
                       "claws still protrude from the canyon walls. The bottom is littered with bone "
                       "fragments and crystallized dragon blood that glows faintly red in the shadows. "
                       "Something nests in the deeper crevices — you hear scratching.",
        "coordinates": [cx - 2, cy + 1],
        "location_type": "wilderness",
        "items": {"crystallized_dragon_blood": {"quantity": 1, "value": 40}, "petrified_claw_tip": {"quantity": 1, "value": 24}},
        "exits": {
            "south": {"target": "wyrm_wastes_scale_field", "type": "direction"},
            "west": {"target": "wyrm_wastes_marrow_pool", "type": "direction"}
        }
    }

    rooms["wyrm_wastes_marrow_pool"] = {
        "id": "wyrm_wastes_marrow_pool",
        "name": "Marrow Pool",
        "description": "A shallow depression where ancient dragon marrow has seeped from cracked bones "
                       "and pooled into a viscous, glowing liquid. The substance radiates warmth and "
                       "faint draconic magic. Dragonkin alchemists carefully harvest it in small vials, "
                       "as it is a potent reagent for fire-based enchantments.",
        "coordinates": [cx - 3, cy + 2],
        "location_type": "wilderness",
        "items": {"dragon_marrow_vial": {"quantity": 2, "value": 35}},
        "exits": {
            "south": {"target": "wyrm_wastes_spine_ridge", "type": "direction"},
            "east": {"target": "wyrm_wastes_claw_gorge", "type": "direction"}
        }
    }

    rooms["wyrm_wastes_ossuary"] = {
        "id": "wyrm_wastes_ossuary",
        "name": "Dragon Ossuary",
        "description": "A vast underground chamber where dragonkin have arranged the bones of their "
                       "most revered dragons into intricate patterns and monuments. Skulls are mounted "
                       "on pillars, ribcages woven into walls, and wing-bones form chandeliers. Candles "
                       "of dragon tallow burn with a steady blue flame.",
        "coordinates": [cx - 4, cy],
        "location_type": "wilderness",
        "items": {"dragon_tallow_candle": {"quantity": 2, "value": 12}, "ossuary_relic": {"quantity": 1, "value": 45}},
        "exits": {
            "south": {"target": "wyrm_wastes_graveyard", "type": "direction"}
        }
    }

    rooms["wyrm_wastes_scorched_basin"] = {
        "id": "wyrm_wastes_scorched_basin",
        "name": "Scorched Basin",
        "description": "A wide depression in the wastes where an ancient dragon's death throes unleashed "
                       "a final, devastating blast of fire. The basin floor is smooth volcanic glass, "
                       "and the surrounding bone formations are charred black. Heat still radiates "
                       "from the centre, and nothing grows here — not even the hardiest scrub.",
        "coordinates": [cx - 4, cy + 1],
        "location_type": "wilderness",
        "items": {"death_blast_glass": {"quantity": 1, "value": 32}, "charred_bone_fragment": {"quantity": 2, "value": 10}},
        "exits": {
            "east": {"target": "wyrm_wastes_spine_ridge", "type": "direction"},
            "west": {"target": "wyrm_wastes_ash_fields", "type": "direction"}
        }
    }

    rooms["wyrm_wastes_tooth_spire"] = {
        "id": "wyrm_wastes_tooth_spire",
        "name": "Wyrm Tooth Spire",
        "description": "A single enormous dragon tooth — taller than a castle tower — stands alone on "
                       "the wasteland like a monolith. Its surface is carved with Draconic runes that "
                       "glow faintly at dusk. Dragonkin believe it belongs to the first dragon that "
                       "ever lived, and touching it is said to grant visions of the past.",
        "coordinates": [cx - 2, cy - 3],
        "location_type": "wilderness",
        "items": {"wyrm_tooth_rune_rubbing": {"quantity": 1, "value": 28}, "ancient_enamel_chip": {"quantity": 1, "value": 18}},
        "exits": {
            "north": {"target": "wyrm_wastes_skull_hollow", "type": "direction"}
        }
    }

    # --- Wyrmfire Peaks (10 rooms) ---

    rooms["wyrm_peaks_trail"] = {
        "id": "wyrm_peaks_trail",
        "name": "Wyrmfire Peaks Trail",
        "description": "A steep trail of black volcanic rock winds upward into the smoking peaks. The "
                       "temperature rises with every step, and the stone underfoot is uncomfortably "
                       "warm. Rivulets of lava glow orange in cracks along the path, and the air "
                       "shimmers with heat distortion.",
        "coordinates": [cx + 2, cy - 1],
        "location_type": "wilderness",
        "items": {},
        "exits": {
            "west": {"target": "wyrm_village_overlook", "type": "direction"},
            "north": {"target": "wyrm_peaks_fire_vent", "type": "direction"},
            "east": {"target": "wyrm_peaks_obsidian_cliff", "type": "direction"}
        }
    }

    rooms["wyrm_peaks_fire_vent"] = {
        "id": "wyrm_peaks_fire_vent",
        "name": "Fire Vent Plateau",
        "description": "A flat expanse of cracked basalt riddled with volcanic vents that periodically "
                       "blast jets of superheated gas and flame into the air. The eruptions follow a "
                       "pattern that the dragonkin have learned to navigate, but the unwary are quickly "
                       "roasted. Dragon nests are built around the warmest vents.",
        "coordinates": [cx + 2, cy],
        "location_type": "wilderness",
        "items": {"volcanic_vent_crystal": {"quantity": 1, "value": 32}, "heat_resistant_ore": {"quantity": 1, "value": 20}},
        "exits": {
            "south": {"target": "wyrm_peaks_trail", "type": "direction"},
            "north": {"target": "wyrm_peaks_dragon_nest", "type": "direction"},
            "east": {"target": "wyrm_peaks_lava_bridge", "type": "direction"},
            "west": {"target": "wyrm_forge_entrance", "type": "direction"}
        }
    }

    rooms["wyrm_peaks_obsidian_cliff"] = {
        "id": "wyrm_peaks_obsidian_cliff",
        "name": "Obsidian Cliff Face",
        "description": "A sheer cliff of natural obsidian glass, black as midnight and razor-sharp. "
                       "The surface reflects distorted images of the volcanic landscape. Dragon claw "
                       "marks score the glass where wyrms have landed and launched from its edge. At "
                       "the base, obsidian shards litter the ground like dark daggers.",
        "coordinates": [cx + 3, cy - 1],
        "location_type": "wilderness",
        "items": {"obsidian_shard": {"quantity": 3, "value": 14}, "volcanic_glass_mirror": {"quantity": 1, "value": 28}},
        "exits": {
            "west": {"target": "wyrm_peaks_trail", "type": "direction"},
            "north": {"target": "wyrm_peaks_lava_bridge", "type": "direction"}
        }
    }

    rooms["wyrm_peaks_lava_bridge"] = {
        "id": "wyrm_peaks_lava_bridge",
        "name": "Lava Bridge Crossing",
        "description": "A natural bridge of cooled lava spans a chasm of flowing magma. The bridge is "
                       "barely wide enough for two people and radiates blistering heat from below. "
                       "Dragons soar through the rising thermals, and the orange glow from the chasm "
                       "illuminates everything in hellish light.",
        "coordinates": [cx + 3, cy],
        "location_type": "wilderness",
        "items": {"cooled_lava_chunk": {"quantity": 1, "value": 15}},
        "exits": {
            "south": {"target": "wyrm_peaks_obsidian_cliff", "type": "direction"},
            "west": {"target": "wyrm_peaks_fire_vent", "type": "direction"},
            "north": {"target": "wyrm_peaks_caldera_rim", "type": "direction"}
        }
    }

    rooms["wyrm_peaks_dragon_nest"] = {
        "id": "wyrm_peaks_dragon_nest",
        "name": "Dragon Nesting Ledge",
        "description": "A wide rocky ledge high on the volcanic peak where adult dragons have built "
                       "nests of obsidian slabs, volcanic rock, and their own shed scales. Enormous "
                       "eggs the size of boulders sit in heated depressions. The parent dragons are "
                       "fiercely territorial — approaching too closely invites a blast of dragonfire.",
        "coordinates": [cx + 2, cy + 1],
        "location_type": "wilderness",
        "items": {"cracked_dragon_eggshell": {"quantity": 1, "value": 50}, "nest_scale_lining": {"quantity": 1, "value": 22}},
        "exits": {
            "south": {"target": "wyrm_peaks_fire_vent", "type": "direction"},
            "east": {"target": "wyrm_peaks_caldera_rim", "type": "direction"},
            "north": {"target": "wyrm_peaks_summit_path", "type": "direction"}
        }
    }

    rooms["wyrm_peaks_caldera_rim"] = {
        "id": "wyrm_peaks_caldera_rim",
        "name": "Caldera Rim",
        "description": "The rim of the island's primary volcano. Below, a lake of molten lava churns "
                       "and bubbles, casting orange light onto the smoke-stained clouds overhead. The "
                       "heat is nearly unbearable. Dragons circle the caldera, riding the thermals, "
                       "and their roars echo off the volcanic walls like thunder.",
        "coordinates": [cx + 3, cy + 1],
        "location_type": "wilderness",
        "items": {"volcanic_gas_crystal": {"quantity": 1, "value": 36}},
        "exits": {
            "south": {"target": "wyrm_peaks_lava_bridge", "type": "direction"},
            "west": {"target": "wyrm_peaks_dragon_nest", "type": "direction"},
            "north": {"target": "wyrm_peaks_ember_cave", "type": "direction"}
        }
    }

    rooms["wyrm_peaks_summit_path"] = {
        "id": "wyrm_peaks_summit_path",
        "name": "Summit Path",
        "description": "A treacherous path zigzagging up the volcano's flank toward the summit. The "
                       "rock is loose and unstable, and occasional tremors send cascades of gravel "
                       "tumbling downward. The air is thin and scorching, tasting of ash and brimstone. "
                       "Dragon silhouettes pass between you and the smoke-veiled sun.",
        "coordinates": [cx + 2, cy + 2],
        "location_type": "wilderness",
        "items": {"brimstone_chunk": {"quantity": 2, "value": 14}},
        "exits": {
            "south": {"target": "wyrm_peaks_dragon_nest", "type": "direction"},
            "east": {"target": "wyrm_peaks_ember_cave", "type": "direction"}
        }
    }

    rooms["wyrm_peaks_ember_cave"] = {
        "id": "wyrm_peaks_ember_cave",
        "name": "Ember Cave",
        "description": "A cave whose walls glow with veins of molten rock, casting everything in a "
                       "perpetual amber light. The floor is covered in a thick layer of warm ash, and "
                       "the air is heavy with sulfurous fumes. Deep within, something large breathes "
                       "with a slow, rhythmic rumble that shakes loose ash from the ceiling.",
        "coordinates": [cx + 3, cy + 2],
        "location_type": "wilderness",
        "items": {"ember_cave_crystal": {"quantity": 1, "value": 44}, "molten_vein_sample": {"quantity": 1, "value": 28}},
        "exits": {
            "south": {"target": "wyrm_peaks_caldera_rim", "type": "direction"},
            "west": {"target": "wyrm_peaks_summit_path", "type": "direction"}
        }
    }

    rooms["wyrm_peaks_magma_chamber"] = {
        "id": "wyrm_peaks_magma_chamber",
        "name": "Magma Chamber",
        "description": "A colossal underground chamber where magma wells up from deep beneath the "
                       "island. Rivers of lava flow sluggishly between islands of cooled rock. The "
                       "heat is almost lethal, and the light is blinding orange-white. Ancient dragon "
                       "carvings on the walls depict this place as the birthplace of dragonfire itself.",
        "coordinates": [cx + 4, cy],
        "location_type": "wilderness",
        "items": {"magma_heart_stone": {"quantity": 1, "value": 60}, "ancient_dragon_carving": {"quantity": 1, "value": 35}},
        "exits": {
            "west": {"target": "wyrm_peaks_lava_bridge", "type": "direction"},
            "east": {"target": "wyrm_peaks_caldera_rim", "type": "direction"}
        }
    }

    # --- Scale Forest (10 rooms) ---

    rooms["wyrm_forest_border"] = {
        "id": "wyrm_forest_border",
        "name": "Scale Forest Border",
        "description": "The vegetation here transitions from sparse scrub to a bizarre forest of "
                       "petrified dragon scales grown to the size of trees. They jut from the ground "
                       "at odd angles, their surfaces shimmering with iridescent patterns. The canopy "
                       "of overlapping scale-trees filters the light into a kaleidoscope of colour.",
        "coordinates": [cx, cy],
        "location_type": "wilderness",
        "items": {"petrified_scale_bark": {"quantity": 1, "value": 18}},
        "exits": {
            "south": {"target": "wyrm_village_overlook", "type": "direction"},
            "north": {"target": "wyrm_forest_crystal_grove", "type": "direction"},
            "west": {"target": "wyrm_forge_entrance", "type": "direction"},
            "east": {"target": "wyrm_forest_patrol_path", "type": "direction"}
        }
    }

    rooms["wyrm_forest_crystal_grove"] = {
        "id": "wyrm_forest_crystal_grove",
        "name": "Crystal Grove",
        "description": "A clearing where petrified scales have crystallized into towering formations "
                       "of translucent mineral. Sunlight refracts through them, casting prismatic "
                       "rainbows across the forest floor. The crystals hum faintly with residual "
                       "draconic magic, and touching them sends tingles up your arm.",
        "coordinates": [cx, cy + 1],
        "location_type": "wilderness",
        "items": {"dragon_crystal_prism": {"quantity": 1, "value": 42}, "resonant_scale_crystal": {"quantity": 1, "value": 30}},
        "exits": {
            "south": {"target": "wyrm_forest_border", "type": "direction"},
            "north": {"target": "wyrm_forest_deepwood", "type": "direction"},
            "east": {"target": "wyrm_forest_dragonkin_camp", "type": "direction"},
            "west": {"target": "wyrm_forest_mossy_hollow", "type": "direction"}
        }
    }

    rooms["wyrm_forest_patrol_path"] = {
        "id": "wyrm_forest_patrol_path",
        "name": "Dragonkin Patrol Path",
        "description": "A well-worn trail through the scale forest used by dragonkin warriors on "
                       "regular patrol. Claw marks on the crystallized trees mark territory boundaries. "
                       "The patrol scouts for trespassers, wild drakes, and signs of the elder wyrm's "
                       "movements. Boot prints and scale-imprints overlap in the soft ash.",
        "coordinates": [cx + 1, cy],
        "location_type": "wilderness",
        "items": {"patrol_marker_flag": {"quantity": 1, "value": 8}},
        "exits": {
            "west": {"target": "wyrm_forest_border", "type": "direction"},
            "north": {"target": "wyrm_forest_dragonkin_camp", "type": "direction"}
        }
    }

    rooms["wyrm_forest_dragonkin_camp"] = {
        "id": "wyrm_forest_dragonkin_camp",
        "name": "Dragonkin Patrol Camp",
        "description": "A small fortified camp nestled among the giant scale-trees. Tents of tanned "
                       "dragon-wing leather surround a central firepit where dragon-charcoal burns "
                       "with a smokeless blue flame. Warriors sharpen their weapons and swap stories "
                       "of encounters with the wild drakes that roam the forest.",
        "coordinates": [cx + 1, cy + 1],
        "location_type": "settlement",
        "items": {"dragon_charcoal": {"quantity": 2, "value": 10}, "patrol_ration_pack": {"quantity": 1, "value": 6}},
        "exits": {
            "south": {"target": "wyrm_forest_patrol_path", "type": "direction"},
            "west": {"target": "wyrm_forest_crystal_grove", "type": "direction"},
            "north": {"target": "wyrm_forest_wild_drake_den", "type": "direction"}
        }
    }

    rooms["wyrm_forest_mossy_hollow"] = {
        "id": "wyrm_forest_mossy_hollow",
        "name": "Mossy Hollow",
        "description": "A damp depression in the forest floor where moisture collects and thick moss "
                       "grows over fallen scale-trees. Bioluminescent fungi shaped like tiny dragon "
                       "heads glow pale green in the shadows. The air is cool here — a rare relief "
                       "from the island's oppressive heat.",
        "coordinates": [cx - 1, cy + 1],
        "location_type": "wilderness",
        "items": {"dragon_head_fungus": {"quantity": 3, "value": 12}, "damp_moss_clump": {"quantity": 1, "value": 5}},
        "exits": {
            "east": {"target": "wyrm_forest_crystal_grove", "type": "direction"},
            "north": {"target": "wyrm_forest_deepwood", "type": "direction"}
        }
    }

    rooms["wyrm_forest_deepwood"] = {
        "id": "wyrm_forest_deepwood",
        "name": "Scale Forest Deepwood",
        "description": "The heart of the scale forest, where the petrified scale-trees grow so dense "
                       "and tall they block out the sky entirely. The gloom is broken only by the "
                       "bioluminescent glow of dragon-fungi and the occasional flash of a drake's "
                       "eyes reflecting light. The forest floor crunches with centuries of shed scales.",
        "coordinates": [cx, cy + 2],
        "location_type": "wilderness",
        "items": {"ancient_scale_shard": {"quantity": 1, "value": 26}},
        "exits": {
            "south": {"target": "wyrm_forest_crystal_grove", "type": "direction"},
            "east": {"target": "wyrm_forest_wild_drake_den", "type": "direction"},
            "north": {"target": "wyrm_elder_border", "type": "direction"},
            "west": {"target": "wyrm_forest_petrified_clearing", "type": "direction"}
        }
    }

    rooms["wyrm_forest_wild_drake_den"] = {
        "id": "wyrm_forest_wild_drake_den",
        "name": "Wild Drake Den",
        "description": "A tangle of fallen scale-trees and volcanic boulders that wild drakes have "
                       "claimed as their lair. The ground is scorched in patches from their breath, "
                       "and the bones of their prey are scattered about. Hissing and growling echoes "
                       "from deeper within — the drakes do not welcome visitors.",
        "coordinates": [cx + 1, cy + 2],
        "location_type": "wilderness",
        "items": {"wild_drake_fang": {"quantity": 1, "value": 32}, "scorched_prey_bones": {"quantity": 1, "value": 8}},
        "exits": {
            "south": {"target": "wyrm_forest_dragonkin_camp", "type": "direction"},
            "west": {"target": "wyrm_forest_deepwood", "type": "direction"}
        }
    }

    rooms["wyrm_forest_petrified_clearing"] = {
        "id": "wyrm_forest_petrified_clearing",
        "name": "Petrified Clearing",
        "description": "A circular clearing where every tree, plant, and creature has been turned to "
                       "stone by the breath of an ancient dragon. Petrified birds hang in mid-flight, "
                       "and a stone deer leaps eternally over a frozen stream. The effect is hauntingly "
                       "beautiful and deeply unsettling.",
        "coordinates": [cx - 1, cy + 2],
        "location_type": "wilderness",
        "items": {"petrified_bird": {"quantity": 1, "value": 20}, "stone_flower": {"quantity": 2, "value": 14}},
        "exits": {
            "east": {"target": "wyrm_forest_deepwood", "type": "direction"},
            "south": {"target": "wyrm_forest_mossy_hollow", "type": "direction"}
        }
    }

    rooms["wyrm_forest_amber_pool"] = {
        "id": "wyrm_forest_amber_pool",
        "name": "Amber Resin Pool",
        "description": "A natural pool filled with golden amber resin that has seeped from the "
                       "crystallized scale-trees over centuries. Small insects and dragon scales are "
                       "preserved within the amber like ancient jewels. The dragonkin harvest it for "
                       "use in enchanting and preservation rituals.",
        "coordinates": [cx - 1, cy + 3],
        "location_type": "wilderness",
        "items": {"dragon_amber_nugget": {"quantity": 2, "value": 22}, "amber_preserved_scale": {"quantity": 1, "value": 34}},
        "exits": {
            "east": {"target": "wyrm_elder_border", "type": "direction"},
            "south": {"target": "wyrm_forest_petrified_clearing", "type": "direction"}
        }
    }

    rooms["wyrm_forest_scale_canopy"] = {
        "id": "wyrm_forest_scale_canopy",
        "name": "Scale Canopy Platform",
        "description": "A platform built high in the overlapping canopy of giant scale-trees, accessed "
                       "by a ladder of dragonbone rungs. From here you can see across the entire forest "
                       "and beyond — the volcanic peaks to the east, the bone wastes to the west, and "
                       "the dark entrance to the Elder Wyrm's domain to the north.",
        "coordinates": [cx, cy + 3],
        "location_type": "wilderness",
        "items": {"scale_canopy_map": {"quantity": 1, "value": 16}},
        "exits": {
            "down": {"target": "wyrm_forest_deepwood", "type": "direction"},
            "north": {"target": "wyrm_forest_ancient_hollow", "type": "direction"}
        }
    }

    # --- Hatchery (10 rooms) ---

    rooms["wyrm_hatchery_entrance"] = {
        "id": "wyrm_hatchery_entrance",
        "name": "Hatchery Entrance",
        "description": "A cave mouth ringed with dragon teeth driven into the rock like a fence. The "
                       "air that wafts from within is hot, humid, and smells of sulfur and iron. "
                       "Dragonkin attendants guard the entrance, allowing only those with permission "
                       "to enter the sacred breeding grounds.",
        "coordinates": [cx + 2, cy + 3],
        "location_type": "wilderness",
        "items": {},
        "exits": {
            "south": {"target": "wyrm_forest_wild_drake_den", "type": "direction"},
            "north": {"target": "wyrm_hatchery_incubation_hall", "type": "direction"},
            "east": {"target": "wyrm_hatchery_guard_post", "type": "direction"}
        }
    }

    rooms["wyrm_hatchery_guard_post"] = {
        "id": "wyrm_hatchery_guard_post",
        "name": "Hatchery Guard Post",
        "description": "A fortified position carved into the rock beside the hatchery entrance. "
                       "Elite dragonkin warriors stand watch here, armed with obsidian halberds and "
                       "wearing heat-treated scale armour. Their duty is to protect the unhatched "
                       "dragons — the future of the island.",
        "coordinates": [cx + 3, cy + 3],
        "location_type": "building",
        "items": {"obsidian_halberd_shard": {"quantity": 1, "value": 28}},
        "exits": {
            "west": {"target": "wyrm_hatchery_entrance", "type": "direction"}
        }
    }

    rooms["wyrm_hatchery_incubation_hall"] = {
        "id": "wyrm_hatchery_incubation_hall",
        "name": "Incubation Hall",
        "description": "A long cavern where dragon eggs are arranged in rows on heated stone cradles. "
                       "Each egg is the size of a barrel, their shells mottled with swirling colours "
                       "that pulse with internal light. Dragonkin attendants monitor the temperature "
                       "and turn the eggs at precise intervals dictated by ancient tradition.",
        "coordinates": [cx + 2, cy + 4],
        "location_type": "wilderness",
        "items": {"dragon_egg_shard": {"quantity": 1, "value": 38}, "incubation_tong": {"quantity": 1, "value": 15}},
        "exits": {
            "south": {"target": "wyrm_hatchery_entrance", "type": "direction"},
            "east": {"target": "wyrm_hatchery_warm_pool", "type": "direction"},
            "north": {"target": "wyrm_hatchery_nursery", "type": "direction"},
            "west": {"target": "wyrm_hatchery_egg_vault", "type": "direction"}
        }
    }

    rooms["wyrm_hatchery_warm_pool"] = {
        "id": "wyrm_hatchery_warm_pool",
        "name": "Incubation Pools",
        "description": "Natural hot springs have been channelled into shallow pools where aquatic "
                       "dragon eggs are submerged. The water glows a soft volcanic orange, and tiny "
                       "bubbles rise continuously from vents in the pool floor. Half-formed dragon "
                       "shapes are visible through the translucent shells.",
        "coordinates": [cx + 3, cy + 4],
        "location_type": "wilderness",
        "items": {"volcanic_spring_water_vial": {"quantity": 2, "value": 18}, "aquatic_egg_membrane": {"quantity": 1, "value": 30}},
        "exits": {
            "west": {"target": "wyrm_hatchery_incubation_hall", "type": "direction"}
        }
    }

    rooms["wyrm_hatchery_egg_vault"] = {
        "id": "wyrm_hatchery_egg_vault",
        "name": "Egg Vault",
        "description": "A heavily guarded chamber deep within the hatchery where the rarest and most "
                       "valuable dragon eggs are stored. The eggs here belong to the elder bloodlines — "
                       "ancient lineages of immense power. Each egg rests in a cradle of enchanted "
                       "obsidian that maintains the perfect temperature.",
        "coordinates": [cx + 1, cy + 4],
        "location_type": "wilderness",
        "items": {"elder_bloodline_scale": {"quantity": 1, "value": 55}, "enchanted_obsidian_shard": {"quantity": 1, "value": 34}},
        "exits": {
            "east": {"target": "wyrm_hatchery_incubation_hall", "type": "direction"}
        }
    }

    rooms["wyrm_hatchery_nursery"] = {
        "id": "wyrm_hatchery_nursery",
        "name": "Drake Nursery",
        "description": "A spacious cavern where newly hatched drakelings tumble and play under the "
                       "watchful eyes of dragonkin nurses. The tiny dragons snap at each other, "
                       "breathe puffs of smoke, and chase glowing insects. The nursery floor is "
                       "padded with layers of shed scales to cushion clumsy landings.",
        "coordinates": [cx + 2, cy + 5],
        "location_type": "wilderness",
        "items": {"drakeling_shed_scale": {"quantity": 3, "value": 8}, "nursery_feeding_trough": {"quantity": 1, "value": 10}},
        "exits": {
            "south": {"target": "wyrm_hatchery_incubation_hall", "type": "direction"},
            "north": {"target": "wyrm_hatchery_feeding_grounds", "type": "direction"},
            "east": {"target": "wyrm_hatchery_bonding_cave", "type": "direction"}
        }
    }

    rooms["wyrm_hatchery_bonding_cave"] = {
        "id": "wyrm_hatchery_bonding_cave",
        "name": "Bonding Cave",
        "description": "A quiet, dimly lit cave where dragonkin undergo the sacred bonding ritual with "
                       "young drakes. The walls are carved with ancient Draconic prayers, and a circle "
                       "of dragon teeth on the floor marks the ritual space. When the bond takes hold, "
                       "both drake and rider share senses — a connection that lasts a lifetime.",
        "coordinates": [cx + 3, cy + 5],
        "location_type": "wilderness",
        "items": {"bonding_ritual_tooth": {"quantity": 1, "value": 40}, "draconic_prayer_etching": {"quantity": 1, "value": 22}},
        "exits": {
            "west": {"target": "wyrm_hatchery_nursery", "type": "direction"},
            "east": {"target": "wyrm_hatchery_elder_nest", "type": "direction"}
        }
    }

    rooms["wyrm_hatchery_feeding_grounds"] = {
        "id": "wyrm_hatchery_feeding_grounds",
        "name": "Feeding Grounds",
        "description": "A fenced area where young drakes learn to hunt live prey released by their "
                       "handlers. The ground is scorched, scratched, and littered with bones. Juvenile "
                       "drakes — each the size of a large dog — practice their flame breath on targets "
                       "of stone and iron, filling the air with smoke and excited shrieks.",
        "coordinates": [cx + 2, cy + 6],
        "location_type": "wilderness",
        "items": {"juvenile_drake_scale": {"quantity": 2, "value": 16}, "practice_target_iron": {"quantity": 1, "value": 10}},
        "exits": {
            "south": {"target": "wyrm_hatchery_nursery", "type": "direction"},
            "west": {"target": "wyrm_hatchery_maturation_den", "type": "direction"}
        }
    }

    rooms["wyrm_hatchery_maturation_den"] = {
        "id": "wyrm_hatchery_maturation_den",
        "name": "Maturation Den",
        "description": "A series of individual cave chambers where adolescent drakes go through their "
                       "growth surges. The caves are sized to accommodate their rapid expansion, with "
                       "walls scored by restless claws. Each den is heated by a dedicated lava channel, "
                       "and the roars of growing dragons echo through the stone constantly.",
        "coordinates": [cx + 1, cy + 6],
        "location_type": "wilderness",
        "items": {"adolescent_drake_horn": {"quantity": 1, "value": 36}, "lava_channel_stone": {"quantity": 1, "value": 14}},
        "exits": {
            "east": {"target": "wyrm_hatchery_feeding_grounds", "type": "direction"},
            "west": {"target": "wyrm_hatchery_abandoned_den", "type": "direction"}
        }
    }

    # --- Elder Wyrm's Domain (8 rooms) ---

    rooms["wyrm_elder_border"] = {
        "id": "wyrm_elder_border",
        "name": "Border of the Elder's Domain",
        "description": "The forest thins abruptly and the ground turns to blackened, cracked earth. "
                       "Warning totems of dragon skulls and obsidian blades mark the boundary of the "
                       "Elder Wyrm's territory. The air is thick with draconic power — a pressure "
                       "that makes your ears pop and your skin prickle. Even the dragonkin tread "
                       "carefully beyond this point.",
        "coordinates": [cx, cy + 3],
        "location_type": "wilderness",
        "items": {"warning_totem_fragment": {"quantity": 1, "value": 20}},
        "exits": {
            "south": {"target": "wyrm_forest_deepwood", "type": "direction"},
            "north": {"target": "wyrm_elder_scorched_path", "type": "direction"}
        }
    }

    rooms["wyrm_elder_scorched_path"] = {
        "id": "wyrm_elder_scorched_path",
        "name": "Scorched Processional",
        "description": "A wide path of glass-smooth rock, fused by centuries of dragonfire into a "
                       "permanent roadway. It leads straight toward the Elder Wyrm's lair, flanked "
                       "by pillars of dragonbone carved with the names of every Elder Wyrm that has "
                       "ruled the island. The most recent name still glows with inner fire.",
        "coordinates": [cx, cy + 4],
        "location_type": "wilderness",
        "items": {"dragonbone_name_plate": {"quantity": 1, "value": 30}},
        "exits": {
            "south": {"target": "wyrm_elder_border", "type": "direction"},
            "north": {"target": "wyrm_elder_gate", "type": "direction"},
            "east": {"target": "wyrm_elder_bone_shrine", "type": "direction"},
            "west": {"target": "wyrm_elder_offering_circle", "type": "direction"}
        }
    }

    rooms["wyrm_elder_bone_shrine"] = {
        "id": "wyrm_elder_bone_shrine",
        "name": "Shrine of Fallen Elders",
        "description": "A solemn monument built from the bones of previous Elder Wyrms. Each skeleton "
                       "is arranged in a regal pose, wings spread wide, as if ready to take flight "
                       "once more. Dragonkin leave offerings of fire opals and dragon blood at the "
                       "base of each monument. The bones still radiate faint warmth.",
        "coordinates": [cx + 1, cy + 4],
        "location_type": "wilderness",
        "items": {"elder_wyrm_bone_relic": {"quantity": 1, "value": 52}, "fire_opal_gem": {"quantity": 1, "value": 38}},
        "exits": {
            "west": {"target": "wyrm_elder_scorched_path", "type": "direction"}
        }
    }

    rooms["wyrm_elder_offering_circle"] = {
        "id": "wyrm_elder_offering_circle",
        "name": "Offering Circle",
        "description": "A ritual circle of volcanic glass where the dragonkin bring tribute to appease "
                       "the Elder Wyrm. Piles of gold, gems, enchanted weapons, and rare scales are "
                       "heaped within the circle. The offerings are collected by the Elder Wyrm itself, "
                       "who swoops down at dusk to claim what is owed.",
        "coordinates": [cx - 1, cy + 4],
        "location_type": "wilderness",
        "items": {"tribute_gold_bar": {"quantity": 1, "value": 65}, "enchanted_scale_offering": {"quantity": 1, "value": 40}},
        "exits": {
            "east": {"target": "wyrm_elder_scorched_path", "type": "direction"}
        }
    }

    rooms["wyrm_elder_gate"] = {
        "id": "wyrm_elder_gate",
        "name": "Gate of the Elder Wyrm",
        "description": "An immense gate forged from a single piece of meteoric iron, shaped into the "
                       "likeness of two dragons facing each other with jaws agape. The heat emanating "
                       "from beyond is stifling, and the reverberations of a massive heartbeat pulse "
                       "through the iron. Beyond lies the Elder Wyrm's inner sanctum.",
        "coordinates": [cx, cy + 5],
        "location_type": "wilderness",
        "items": {},
        "exits": {
            "south": {"target": "wyrm_elder_scorched_path", "type": "direction"},
            "north": {"target": "wyrm_elder_antechamber", "type": "direction"},
            "east": {"target": "wyrm_elder_guardian_post", "type": "direction"},
            "west": {"target": "wyrm_elder_trophy_hall", "type": "direction"}
        }
    }

    rooms["wyrm_elder_guardian_post"] = {
        "id": "wyrm_elder_guardian_post",
        "name": "Elder's Guardian Post",
        "description": "The last checkpoint before the Elder Wyrm's lair. The most powerful dragonkin "
                       "warriors are stationed here, clad in armour forged from the shed scales of the "
                       "Elder Wyrm itself. They answer only to the Elder and will destroy anything that "
                       "threatens their ancient master.",
        "coordinates": [cx + 1, cy + 5],
        "location_type": "building",
        "items": {"elder_scale_armour_shard": {"quantity": 1, "value": 48}},
        "exits": {
            "west": {"target": "wyrm_elder_gate", "type": "direction"}
        }
    }

    rooms["wyrm_elder_trophy_hall"] = {
        "id": "wyrm_elder_trophy_hall",
        "name": "Elder's Trophy Hall",
        "description": "A cavern filled with the Elder Wyrm's personal hoard of trophies — the "
                       "weapons and armour of would-be dragonslayers who challenged the beast and "
                       "lost. Enchanted swords, runed shields, and the banners of fallen kingdoms "
                       "hang from the walls as grim warnings to any who would dare to follow.",
        "coordinates": [cx - 1, cy + 5],
        "location_type": "wilderness",
        "items": {"fallen_hero_blade": {"quantity": 1, "value": 58}, "dragonslayer_banner_scrap": {"quantity": 1, "value": 25}},
        "exits": {
            "east": {"target": "wyrm_elder_gate", "type": "direction"}
        }
    }

    rooms["wyrm_elder_antechamber"] = {
        "id": "wyrm_elder_antechamber",
        "name": "Elder Wyrm's Antechamber",
        "description": "The final passage before the Elder Wyrm's cavern. The walls are polished "
                       "smooth by the passage of an enormous body, and claw marks deeper than a "
                       "man is tall score the floor. The heat is beyond natural, and the rhythmic "
                       "breathing of something colossal vibrates in your chest.",
        "coordinates": [cx, cy + 6],
        "location_type": "wilderness",
        "items": {"elder_wyrm_claw_mark_cast": {"quantity": 1, "value": 35}},
        "exits": {
            "south": {"target": "wyrm_elder_gate", "type": "direction"},
            "north": {"target": "wyrm_elder_cavern", "type": "direction"}
        }
    }

    rooms["wyrm_elder_cavern"] = {
        "id": "wyrm_elder_cavern",
        "name": "Cavern of the Elder Wyrm",
        "description": "A cavern of staggering proportions — the ceiling vanishes into smoke and shadow "
                       "hundreds of feet above, and the floor is a lake of cooled lava cracked with "
                       "glowing fissures. At the centre, atop a mountain of gold and dragon bones, "
                       "sleeps the Elder Wyrm — an ancient dragon whose scales are the colour of "
                       "volcanic lightning. A shimmering portal of dragonfire pulses in the far wall, "
                       "leading deeper into the wyrm's sanctum.",
        "coordinates": [cx, cy + 7],
        "location_type": "wilderness",
        "items": {"elder_wyrm_shed_scale": {"quantity": 1, "value": 80}, "volcanic_lightning_shard": {"quantity": 1, "value": 60}},
        "exits": {
            "south": {"target": "wyrm_elder_antechamber", "type": "direction"},
            "enter": {
                "target": "FIXED_DUNGEON",
                "type": "fixed_dungeon",
                "dungeon_id": "wyrms_sanctum",
                "transition_text": "You step through the portal of dragonfire. Reality warps as the\nflames consume the air around you, reshaping the world into a realm\nof pure draconic power — the Wyrm's Sanctum, where the oldest and\nmost terrible of dragons has hoarded power since before memory..."
            }
        }
    }

    # --- Dragonbone Forge (5 rooms) ---

    rooms["wyrm_forge_entrance"] = {
        "id": "wyrm_forge_entrance",
        "name": "Dragonbone Forge Entrance",
        "description": "A fortified entrance built into the cliffside, framed by two massive dragon "
                       "femurs. The roar of the forge within echoes outward, accompanied by waves of "
                       "intense heat. A sign in Draconic script reads: 'Only those of the flame may "
                       "enter.' Sparks and ash drift from within like fiery snow.",
        "coordinates": [cx - 1, cy],
        "location_type": "building",
        "items": {},
        "exits": {
            "east": {"target": "wyrm_forest_border", "type": "direction"},
            "south": {"target": "wyrm_wastes_scale_field", "type": "direction"},
            "west": {"target": "wyrm_peaks_fire_vent", "type": "direction"},
            "north": {"target": "wyrm_forge_main_hall", "type": "direction"}
        }
    }

    rooms["wyrm_forge_main_hall"] = {
        "id": "wyrm_forge_main_hall",
        "name": "Dragonbone Forge - Main Hall",
        "description": "The central forge chamber, dominated by an enormous anvil carved from a single "
                       "dragon skull. Living dragonfire is channelled from volcanic vents through stone "
                       "conduits to feed the forge. Master smiths hammer dragonbone weapons and scale "
                       "armour, each piece taking months to complete and imbued with draconic essence.",
        "coordinates": [cx - 1, cy + 1],
        "location_type": "building",
        "items": {"dragonbone_hammer": {"quantity": 1, "value": 55}, "raw_dragonbone_ingot": {"quantity": 1, "value": 38}},
        "exits": {
            "south": {"target": "wyrm_forge_entrance", "type": "direction"},
            "east": {"target": "wyrm_forge_scale_workshop", "type": "direction"},
            "north": {"target": "wyrm_forge_quenching_pool", "type": "direction"},
            "west": {"target": "wyrm_forge_material_vault", "type": "direction"}
        }
    }

    rooms["wyrm_forge_scale_workshop"] = {
        "id": "wyrm_forge_scale_workshop",
        "name": "Scale-Working Workshop",
        "description": "A specialised workshop where dragon scales are cleaned, shaped, and fitted "
                       "into armour. The scales are incredibly tough — only dragonfire can soften them "
                       "enough to work. Finished pieces gleam with an iridescent sheen and are light "
                       "as leather but stronger than steel.",
        "coordinates": [cx, cy + 1],
        "location_type": "building",
        "items": {"worked_dragon_scale_plate": {"quantity": 1, "value": 48}, "scale_working_tools": {"quantity": 1, "value": 22}},
        "exits": {
            "west": {"target": "wyrm_forge_main_hall", "type": "direction"}
        }
    }

    rooms["wyrm_forge_quenching_pool"] = {
        "id": "wyrm_forge_quenching_pool",
        "name": "Dragonblood Quenching Pool",
        "description": "A deep pool of preserved dragon blood mixed with volcanic mineral water, used "
                       "to quench freshly forged dragonbone weapons. The liquid is dark red with an "
                       "oily sheen, and it hisses violently when hot metal contacts it. Weapons "
                       "quenched here are said to hunger for battle.",
        "coordinates": [cx - 1, cy + 2],
        "location_type": "building",
        "items": {"dragonblood_quench_vial": {"quantity": 1, "value": 42}},
        "exits": {
            "south": {"target": "wyrm_forge_main_hall", "type": "direction"},
            "north": {"target": "wyrm_forge_rune_chamber", "type": "direction"}
        }
    }

    rooms["wyrm_forge_material_vault"] = {
        "id": "wyrm_forge_material_vault",
        "name": "Material Vault",
        "description": "A heavily locked vault where the rarest forging materials are stored — "
                       "elder dragon scales, meteoric iron, volcanic diamonds, and vials of distilled "
                       "dragonfire. Each material is worth a small fortune, and the vault master keeps "
                       "meticulous records of every gram used.",
        "coordinates": [cx - 2, cy + 1],
        "location_type": "building",
        "items": {"volcanic_diamond": {"quantity": 1, "value": 70}, "distilled_dragonfire_vial": {"quantity": 1, "value": 58}},
        "exits": {
            "east": {"target": "wyrm_forge_main_hall", "type": "direction"}
        }
    }



    # === WYRMSCALE ISLE EXPANSION ===

    # --- Expanded Docks (+3 rooms) ---

    rooms["wyrm_docks_tide_pools"] = {
        "id": "wyrm_docks_tide_pools",
        "name": "Dragon Tide Pools",
        "description": "Rocky pools at the base of the dock cliffs where volcanic heat warms "
                       "the seawater. Dragon hatchlings sometimes come here to hunt fire-crabs "
                       "and lava eels. The water steams and bubbles, and the pools glow with "
                       "mineral colours — orange, red, and deep amber.",
        "coordinates": [cx + 2, cy - 6],
        "location_type": "wilderness",
        "items": {"fire_crab_shell": {"quantity": 1, "value": 15}, "lava_eel_scale": {"quantity": 1, "value": 12}},
        "exits": {
            "west": {"target": "wyrm_docks_cargo", "type": "direction"},
            "north": {"target": "wyrm_docks_dragon_perch", "type": "direction"}
        }
    }

    rooms["wyrm_docks_dragon_perch"] = {
        "id": "wyrm_docks_dragon_perch",
        "name": "Dragon Landing Perch",
        "description": "A massive stone ledge carved from the cliff face, scored with claw marks "
                       "from centuries of dragon landings. The ledge is wide enough for a full-grown "
                       "wyrm to rest its wings. Chains and harnesses hang from iron rings set into "
                       "the rock for securing cargo to dragon riders.",
        "coordinates": [cx + 2, cy - 5],
        "location_type": "wilderness",
        "items": {"dragon_harness_chain": {"quantity": 1, "value": 20}, "claw_scored_stone": {"quantity": 1, "value": 8}},
        "exits": {
            "south": {"target": "wyrm_docks_tide_pools", "type": "direction"}
        }
    }

    rooms["wyrm_docks_signal_cove"] = {
        "id": "wyrm_docks_signal_cove",
        "name": "Signal Cove",
        "description": "A sheltered cove west of the watchtower where signal fires are lit "
                       "to guide dragon riders home. The cove walls are blackened by centuries "
                       "of smoke, and a stockpile of dragonfire kindling stands ready. During "
                       "the nesting season, the smoke keeps wild drakes at bay.",
        "coordinates": [cx - 2, cy - 6],
        "location_type": "wilderness",
        "items": {"dragonfire_kindling": {"quantity": 2, "value": 8}, "signal_smoke_powder": {"quantity": 1, "value": 15}},
        "exits": {
            "east": {"target": "wyrm_docks_watchtower", "type": "direction"}
        }
    }

    # --- Expanded Village (+5 rooms) ---

    rooms["wyrm_village_scroll_vault"] = {
        "id": "wyrm_village_scroll_vault",
        "name": "Scroll Vault",
        "description": "A fireproof chamber deep within the rock behind the library, containing "
                       "the most ancient and valuable dragon lore. The scrolls here are written "
                       "on dragonhide and inscribed with letters of gold. Guards of the Dragon "
                       "Order watch over them day and night.",
        "coordinates": [cx + 3, cy - 2],
        "location_type": "building",
        "items": {"ancient_dragonhide_scroll": {"quantity": 1, "value": 50}, "gold_letter_fragment": {"quantity": 1, "value": 25}},
        "exits": {
            "west": {"target": "wyrm_village_library", "type": "direction"},
            "north": {"target": "wyrm_village_meditation", "type": "direction"}
        }
    }

    rooms["wyrm_village_meditation"] = {
        "id": "wyrm_village_meditation",
        "name": "Dragon Meditation Chamber",
        "description": "A serene cave heated by a gentle volcanic vent, where dragon riders "
                       "come to meditate and strengthen their mental bond with their drakes. "
                       "The walls are inscribed with calming Draconic mantras, and the warm "
                       "air carries the scent of sulphur and dragonflower incense.",
        "coordinates": [cx + 3, cy - 1],
        "location_type": "building",
        "items": {"dragonflower_incense": {"quantity": 1, "value": 15}, "meditation_crystal": {"quantity": 1, "value": 22}},
        "exits": {
            "south": {"target": "wyrm_village_scroll_vault", "type": "direction"}
        }
    }

    rooms["wyrm_village_hatchling_pen"] = {
        "id": "wyrm_village_hatchling_pen",
        "name": "Village Hatchling Pen",
        "description": "An enclosed area in the village where newly bonded hatchlings are raised. "
                       "The pen is ringed with fire-resistant stone and warmed by buried lava "
                       "channels. Young drakes play and practice breathing fire under the watchful "
                       "eyes of experienced dragon keepers.",
        "coordinates": [cx + 2, cy - 5],
        "location_type": "settlement",
        "items": {"hatchling_scale": {"quantity": 2, "value": 10}, "dragon_keeper_whistle": {"quantity": 1, "value": 18}},
        "exits": {
            "south": {"target": "wyrm_village_stable", "type": "direction"}
        }
    }

    rooms["wyrm_village_wyvern_roost"] = {
        "id": "wyrm_village_wyvern_roost",
        "name": "Wyvern Roost",
        "description": "A series of stone platforms built high above the village where messenger "
                       "wyverns nest. Smaller and more agile than true dragons, the wyverns carry "
                       "messages and small parcels between the island and the mainland. Their "
                       "nests are lined with shed dragon scales.",
        "coordinates": [cx + 2, cy - 3],
        "location_type": "building",
        "items": {"wyvern_feather": {"quantity": 1, "value": 15}, "messenger_harness": {"quantity": 1, "value": 12}},
        "exits": {
            "south": {"target": "wyrm_village_market", "type": "direction"}
        }
    }

    rooms["wyrm_village_draconic_court"] = {
        "id": "wyrm_village_draconic_court",
        "name": "Draconic Court",
        "description": "An open-air court where disputes between dragon riders are settled "
                       "according to ancient Draconic law. A throne of fused dragon teeth "
                       "serves as the judge's seat, and the walls display the tapestried "
                       "history of every major ruling. Justice here is swift and final.",
        "coordinates": [cx + 2, cy - 1],
        "location_type": "building",
        "items": {"draconic_law_scroll": {"quantity": 1, "value": 30}, "judgment_scale": {"quantity": 1, "value": 20}},
        "exits": {
            "south": {"target": "wyrm_village_elder", "type": "direction"}
        }
    }

    # --- Expanded Dragonbone Wastes (+8 rooms) ---

    rooms["wyrm_wastes_petrified_nest"] = {
        "id": "wyrm_wastes_petrified_nest",
        "name": "Petrified Dragon Nest",
        "description": "A dragon's nest turned entirely to stone over millennia. The eggs "
                       "within are perfect stone replicas, each perfectly preserved. Some "
                       "believe the unhatched dragon spirits still inhabit them, waiting for "
                       "conditions that will never come.",
        "coordinates": [cx - 5, cy - 1],
        "location_type": "wilderness",
        "items": {"petrified_egg": {"quantity": 1, "value": 45}, "nest_stone_fragment": {"quantity": 1, "value": 15}},
        "exits": {
            "east": {"target": "wyrm_wastes_fossil_cave", "type": "direction"},
            "south": {"target": "wyrm_wastes_ancient_battlefield", "type": "direction"},
            "north": {"target": "wyrm_wastes_tar_pit", "type": "direction"}
        }
    }

    rooms["wyrm_wastes_ancient_battlefield"] = {
        "id": "wyrm_wastes_ancient_battlefield",
        "name": "Ancient Dragon Battlefield",
        "description": "A vast field strewn with the bones of hundreds of dragons, the site "
                       "of a catastrophic battle between rival wyrm clans. Skeletons lie "
                       "intertwined, frozen in combat. The ground is glazed with ancient "
                       "dragonfire, creating patches of obsidian glass.",
        "coordinates": [cx - 5, cy],
        "location_type": "wilderness",
        "items": {"battlefield_dragon_fang": {"quantity": 1, "value": 35}, "obsidian_battle_glass": {"quantity": 1, "value": 20}},
        "exits": {
            "north": {"target": "wyrm_wastes_petrified_nest", "type": "direction"},
            "east": {"target": "wyrm_wastes_ash_fields", "type": "direction"}
        }
    }

    rooms["wyrm_wastes_ash_fields"] = {
        "id": "wyrm_wastes_ash_fields",
        "name": "Ash Fields",
        "description": "Endless plains of grey-white ash — the cremated remains of dragons "
                       "who chose the ancient tradition of funeral pyres. Walking through "
                       "raises clouds that sting the eyes and coat everything. Occasionally, "
                       "an intact dragon skeleton emerges from the drifts.",
        "coordinates": [cx - 5, cy + 1],
        "location_type": "wilderness",
        "items": {"dragon_ash": {"quantity": 2, "value": 8}, "pyre_remnant": {"quantity": 1, "value": 12}},
        "exits": {
            "east": {"target": "wyrm_wastes_scorched_basin", "type": "direction"},
            "west": {"target": "wyrm_wastes_ancient_battlefield", "type": "direction"},
            "north": {"target": "wyrm_wastes_bone_garden", "type": "direction"}
        }
    }

    rooms["wyrm_wastes_bone_garden"] = {
        "id": "wyrm_wastes_bone_garden",
        "name": "Bone Garden",
        "description": "Dragon bones have been arranged into towering sculptures by an unknown "
                       "artist — or perhaps by the dragons themselves. Ribcages form arches, "
                       "skulls are stacked into pyramids, and wing bones create fan-like "
                       "displays. The effect is both beautiful and deeply unsettling.",
        "coordinates": [cx - 5, cy + 2],
        "location_type": "wilderness",
        "items": {"bone_sculpture_piece": {"quantity": 1, "value": 20}, "arranged_dragon_claw": {"quantity": 1, "value": 18}},
        "exits": {
            "south": {"target": "wyrm_wastes_ash_fields", "type": "direction"}
        }
    }

    rooms["wyrm_wastes_tar_pit"] = {
        "id": "wyrm_wastes_tar_pit",
        "name": "Dragon Tar Pit",
        "description": "A bubbling pit of black tar where several dragons met their end, "
                       "their bones gradually being pulled beneath the surface. The tar "
                       "preserves everything perfectly — some bones pulled from it still bear "
                       "traces of scale colouration despite being thousands of years old.",
        "coordinates": [cx - 5, cy - 2],
        "location_type": "wilderness",
        "items": {"tar_preserved_scale": {"quantity": 1, "value": 28}, "tar_sample": {"quantity": 1, "value": 10}},
        "exits": {
            "south": {"target": "wyrm_wastes_petrified_nest", "type": "direction"},
            "east": {"target": "wyrm_wastes_earthquake_rift", "type": "direction"}
        }
    }

    rooms["wyrm_wastes_earthquake_rift"] = {
        "id": "wyrm_wastes_earthquake_rift",
        "name": "Earthquake Rift",
        "description": "A massive crack in the earth opened by a seismic event, revealing "
                       "layers of dragon bones dating back thousands of years. Each stratum "
                       "tells a different chapter of draconic history. Heat rises from the "
                       "depths, suggesting volcanic activity far below.",
        "coordinates": [cx - 4, cy - 2],
        "location_type": "wilderness",
        "items": {"rift_bone_layer": {"quantity": 1, "value": 22}, "geological_sample": {"quantity": 1, "value": 12}},
        "exits": {
            "west": {"target": "wyrm_wastes_tar_pit", "type": "direction"},
            "south": {"target": "wyrm_wastes_fossil_cave", "type": "direction"}
        }
    }

    rooms["wyrm_wastes_wyrmling_graveyard"] = {
        "id": "wyrm_wastes_wyrmling_graveyard",
        "name": "Wyrmling Graveyard",
        "description": "A heartbreaking section of the wastes where young dragons that didn't "
                       "survive their first year are laid to rest. The bones are small and "
                       "delicate, some barely larger than a dog. Dragon mothers visit this "
                       "place during the mourning season, their keening echoing for miles.",
        "coordinates": [cx - 3, cy + 2],
        "location_type": "wilderness",
        "items": {"wyrmling_bone": {"quantity": 1, "value": 15}, "mourning_dragon_tear": {"quantity": 1, "value": 35}},
        "exits": {
            "west": {"target": "wyrm_wastes_bone_garden", "type": "direction"},
            "south": {"target": "wyrm_wastes_spine_ridge", "type": "direction"}
        }
    }

    rooms["wyrm_wastes_horn_monument"] = {
        "id": "wyrm_wastes_horn_monument",
        "name": "Horn Monument",
        "description": "A towering monument constructed from dragon horns, each one donated "
                       "by a dragon upon its death. The horns spiral upward in a double helix, "
                       "creating a structure visible from across the island. Inside the helix, "
                       "the acoustics amplify any sound into a dragon-like roar.",
        "coordinates": [cx - 2, cy + 2],
        "location_type": "wilderness",
        "items": {"monument_horn_fragment": {"quantity": 1, "value": 22}, "acoustic_horn": {"quantity": 1, "value": 30}},
        "exits": {
            "west": {"target": "wyrm_wastes_wyrmling_graveyard", "type": "direction"}
        }
    }

    # --- Expanded Wyrmfire Peaks (+6 rooms) ---

    rooms["wyrm_peaks_caldera_rim"] = {
        "id": "wyrm_peaks_caldera_rim",
        "name": "Caldera Rim",
        "description": "The knife-edge rim of the great caldera, where you can look down into "
                       "the volcano's heart. Rivers of lava flow far below, and the heat shimmers "
                       "make the opposite rim dance and distort. Dragon nests dot the caldera "
                       "walls, their occupants riding the superheated thermals.",
        "coordinates": [cx + 5, cy],
        "location_type": "wilderness",
        "items": {"caldera_obsidian": {"quantity": 1, "value": 25}, "thermal_crystal": {"quantity": 1, "value": 30}},
        "exits": {
            "west": {"target": "wyrm_peaks_magma_chamber", "type": "direction"},
            "north": {"target": "wyrm_peaks_obsidian_cascade", "type": "direction"},
            "south": {"target": "wyrm_peaks_fire_altar", "type": "direction"}
        }
    }

    rooms["wyrm_peaks_obsidian_cascade"] = {
        "id": "wyrm_peaks_obsidian_cascade",
        "name": "Obsidian Cascade",
        "description": "A frozen waterfall of volcanic glass — lava that cooled mid-flow into "
                       "a spectacular formation of black glass sheets. The obsidian catches "
                       "firelight and reflects it in rainbow fragments. Dragon smiths harvest "
                       "the purest glass for weapon-making.",
        "coordinates": [cx + 5, cy + 1],
        "location_type": "wilderness",
        "items": {"pure_obsidian_shard": {"quantity": 1, "value": 35}, "rainbow_glass_fragment": {"quantity": 1, "value": 18}},
        "exits": {
            "south": {"target": "wyrm_peaks_caldera_rim", "type": "direction"},
            "west": {"target": "wyrm_peaks_steam_vents", "type": "direction"}
        }
    }

    rooms["wyrm_peaks_steam_vents"] = {
        "id": "wyrm_peaks_steam_vents",
        "name": "Steam Vent Field",
        "description": "A field of active geothermal vents that blast superheated steam into "
                       "the air at irregular intervals. The steam creates a permanent cloud "
                       "above this section, and the mineral deposits around each vent form "
                       "colourful crystalline towers.",
        "coordinates": [cx + 4, cy + 1],
        "location_type": "wilderness",
        "items": {"vent_crystal": {"quantity": 1, "value": 20}, "steam_mineral_deposit": {"quantity": 1, "value": 12}},
        "exits": {
            "east": {"target": "wyrm_peaks_obsidian_cascade", "type": "direction"}
        }
    }

    rooms["wyrm_peaks_fire_altar"] = {
        "id": "wyrm_peaks_fire_altar",
        "name": "Fire Altar",
        "description": "An ancient altar carved from a single block of fire-agate, perpetually "
                       "burning with a flame that has never been extinguished. Dragons come here "
                       "to rekindle their inner fire when it wanes with age. The altar's flame "
                       "changes colour based on the dragon's elemental alignment.",
        "coordinates": [cx + 5, cy - 1],
        "location_type": "wilderness",
        "items": {"fire_agate_chip": {"quantity": 1, "value": 40}, "eternal_ember": {"quantity": 1, "value": 50}},
        "exits": {
            "north": {"target": "wyrm_peaks_caldera_rim", "type": "direction"},
            "west": {"target": "wyrm_peaks_pyroclast_cave", "type": "direction"}
        }
    }

    rooms["wyrm_peaks_pyroclast_cave"] = {
        "id": "wyrm_peaks_pyroclast_cave",
        "name": "Pyroclast Cave",
        "description": "A cave formed by a pyroclastic flow — superheated gas and ash that "
                       "solidified into a tubular passage. The walls are smooth and glassy, "
                       "streaked with metallic minerals. Small lava tubes branch off in every "
                       "direction, creating a natural labyrinth.",
        "coordinates": [cx + 4, cy - 1],
        "location_type": "wilderness",
        "items": {"pyroclast_shell": {"quantity": 1, "value": 18}, "metallic_mineral_vein": {"quantity": 1, "value": 22}},
        "exits": {
            "east": {"target": "wyrm_peaks_fire_altar", "type": "direction"},
            "north": {"target": "wyrm_peaks_dragon_tomb", "type": "direction"}
        }
    }

    rooms["wyrm_peaks_dragon_tomb"] = {
        "id": "wyrm_peaks_dragon_tomb",
        "name": "Dragon King's Tomb",
        "description": "Deep within the peaks, a massive burial chamber holds the remains of "
                       "the Dragon King — the first and greatest wyrm to rule the island. "
                       "The skeleton is enormous, filling the entire cavern. Its eye sockets "
                       "still glow with residual power, and offerings surround the skull.",
        "coordinates": [cx + 4, cy],
        "location_type": "wilderness",
        "items": {"dragon_king_scale": {"quantity": 1, "value": 75}, "royal_offering": {"quantity": 1, "value": 35}},
        "exits": {
            "south": {"target": "wyrm_peaks_pyroclast_cave", "type": "direction"}
        }
    }

    # --- Expanded Scale Forest (+6 rooms) ---

    rooms["wyrm_forest_ancient_hollow"] = {
        "id": "wyrm_forest_ancient_hollow",
        "name": "Ancient Hollow",
        "description": "A massive scale-tree so old that its trunk has hollowed into a "
                       "cathedral-like space. Dragon clans once held councils here, and the "
                       "inner walls are carved with draconic histories spanning millennia. "
                       "The tree still lives, its canopy the highest point in the forest.",
        "coordinates": [cx, cy + 4],
        "location_type": "wilderness",
        "items": {"ancient_tree_sap": {"quantity": 1, "value": 20}, "council_carving_rubbing": {"quantity": 1, "value": 25}},
        "exits": {
            "south": {"target": "wyrm_forest_scale_canopy", "type": "direction"},
            "east": {"target": "wyrm_forest_mushroom_grotto", "type": "direction"},
            "west": {"target": "wyrm_forest_firefly_glade", "type": "direction"}
        }
    }

    rooms["wyrm_forest_mushroom_grotto"] = {
        "id": "wyrm_forest_mushroom_grotto",
        "name": "Mushroom Grotto",
        "description": "A damp hollow where bioluminescent mushrooms grow to enormous size, "
                       "fed by the mineral-rich volcanic soil. The mushrooms glow in shades "
                       "of dragon-fire orange and lava red. Some are edible and highly prized "
                       "for their ability to temporarily grant fire resistance.",
        "coordinates": [cx + 1, cy + 4],
        "location_type": "wilderness",
        "items": {"fire_resistance_mushroom": {"quantity": 2, "value": 18}, "bioluminescent_cap": {"quantity": 1, "value": 12}},
        "exits": {
            "west": {"target": "wyrm_forest_ancient_hollow", "type": "direction"}
        }
    }

    rooms["wyrm_forest_firefly_glade"] = {
        "id": "wyrm_forest_firefly_glade",
        "name": "Firefly Glade",
        "description": "A woodland clearing where fire-fireflies — insects that produce tiny "
                       "flames instead of light — dance in mesmerizing swarms. The effect is "
                       "like standing in a sea of floating candles. Young drakes love to play "
                       "here, snapping at the fireflies with tiny gouts of flame.",
        "coordinates": [cx - 1, cy + 4],
        "location_type": "wilderness",
        "items": {"fire_firefly_jar": {"quantity": 1, "value": 15}, "drake_play_feather": {"quantity": 1, "value": 8}},
        "exits": {
            "east": {"target": "wyrm_forest_ancient_hollow", "type": "direction"},
            "south": {"target": "wyrm_forest_crystal_spring", "type": "direction"}
        }
    }

    rooms["wyrm_forest_crystal_spring"] = {
        "id": "wyrm_forest_crystal_spring",
        "name": "Crystal Spring",
        "description": "A volcanic spring bubbling up through a bed of colourful crystals. "
                       "The water is warm, mineral-rich, and slightly effervescent. Dragons "
                       "drink from this spring, and the minerals in the water strengthen their "
                       "scales. Locals believe it can cure scale-rot in bonded drakes.",
        "coordinates": [cx - 1, cy + 3],
        "location_type": "wilderness",
        "items": {"crystal_spring_water": {"quantity": 1, "value": 18}, "spring_crystal": {"quantity": 1, "value": 22}},
        "exits": {
            "north": {"target": "wyrm_forest_firefly_glade", "type": "direction"}
        }
    }

    rooms["wyrm_forest_drake_trail"] = {
        "id": "wyrm_forest_drake_trail",
        "name": "Wild Drake Trail",
        "description": "A trail through the deep forest marked by claw marks and scorched "
                       "bark — the territorial markers of wild drakes. Following the trail "
                       "is dangerous but rewarding, as it passes through areas rich in rare "
                       "plants and minerals that drakes instinctively avoid.",
        "coordinates": [cx - 1, cy + 2],
        "location_type": "wilderness",
        "items": {"drake_territory_mark": {"quantity": 1, "value": 10}, "rare_forest_herb": {"quantity": 1, "value": 20}},
        "exits": {
            "east": {"target": "wyrm_forest_petrified_clearing", "type": "direction"},
            "north": {"target": "wyrm_forest_crystal_spring", "type": "direction"}
        }
    }

    rooms["wyrm_forest_scorchwood_circle"] = {
        "id": "wyrm_forest_scorchwood_circle",
        "name": "Scorchwood Circle",
        "description": "A circle of trees permanently set alight by dragonfire — they burn "
                       "but never consume. The perpetual fire creates a warm, lit clearing "
                       "in the deep forest. Dragon riders use this as a waypoint and signal "
                       "marker during night patrols.",
        "coordinates": [cx - 2, cy + 3],
        "location_type": "wilderness",
        "items": {"everburning_branch": {"quantity": 1, "value": 25}, "scorchwood_coal": {"quantity": 1, "value": 10}},
        "exits": {
            "east": {"target": "wyrm_forest_amber_pool", "type": "direction"}
        }
    }

    # --- Expanded Hatchery (+5 rooms) ---

    rooms["wyrm_hatchery_elder_nest"] = {
        "id": "wyrm_hatchery_elder_nest",
        "name": "Elder Broodmother's Nest",
        "description": "The private nesting chamber of the eldest broodmother — a dragon so "
                       "old she can no longer fly. Her nest is built from the shed scales of "
                       "every dragon she has helped raise, creating a shimmering mound of "
                       "colours. She watches over the hatchery with ancient wisdom.",
        "coordinates": [cx + 4, cy + 5],
        "location_type": "wilderness",
        "items": {"broodmother_scale": {"quantity": 1, "value": 55}, "ancient_nest_down": {"quantity": 1, "value": 20}},
        "exits": {
            "west": {"target": "wyrm_hatchery_bonding_cave", "type": "direction"},
            "south": {"target": "wyrm_hatchery_incubation_pool", "type": "direction"}
        }
    }

    rooms["wyrm_hatchery_incubation_pool"] = {
        "id": "wyrm_hatchery_incubation_pool",
        "name": "Volcanic Incubation Pool",
        "description": "A natural hot spring where dragon eggs are placed for volcanic "
                       "incubation. The mineral-rich water keeps the eggs at the perfect "
                       "temperature and infuses the developing hatchlings with elemental "
                       "energy. Attendants monitor temperature constantly.",
        "coordinates": [cx + 4, cy + 4],
        "location_type": "wilderness",
        "items": {"incubation_mineral": {"quantity": 1, "value": 18}, "volcanic_egg_water": {"quantity": 1, "value": 15}},
        "exits": {
            "north": {"target": "wyrm_hatchery_elder_nest", "type": "direction"}
        }
    }

    rooms["wyrm_hatchery_abandoned_den"] = {
        "id": "wyrm_hatchery_abandoned_den",
        "name": "Abandoned Maturation Den",
        "description": "A den abandoned after a cave-in partially collapsed the entrance. "
                       "Inside, the personal effects of a dragon that never returned remain "
                       "untouched — a hoard of shiny objects, claw-sharpening stones, and "
                       "the remnants of its last meal. A melancholy place.",
        "coordinates": [cx, cy + 6],
        "location_type": "wilderness",
        "items": {"abandoned_hoard_trinket": {"quantity": 1, "value": 22}, "claw_sharpening_stone": {"quantity": 1, "value": 12}},
        "exits": {
            "east": {"target": "wyrm_hatchery_maturation_den", "type": "direction"},
            "north": {"target": "wyrm_hatchery_wild_nest", "type": "direction"}
        }
    }

    rooms["wyrm_hatchery_wild_nest"] = {
        "id": "wyrm_hatchery_wild_nest",
        "name": "Wild Drake Nest",
        "description": "A nest built by an unbonded wild drake that refuses to leave the "
                       "hatchery area. The dragon keepers tolerate her presence because she "
                       "protects the young. Her nest is messier than the managed ones — "
                       "built from branches, bones, and stolen tools.",
        "coordinates": [cx, cy + 7],
        "location_type": "wilderness",
        "items": {"wild_drake_feather": {"quantity": 1, "value": 15}, "stolen_tool": {"quantity": 1, "value": 8}},
        "exits": {
            "south": {"target": "wyrm_hatchery_abandoned_den", "type": "direction"}
        }
    }

    rooms["wyrm_hatchery_training_circle"] = {
        "id": "wyrm_hatchery_training_circle",
        "name": "Flight Training Circle",
        "description": "A cleared area surrounded by tall poles and rope nets where young "
                       "dragons learn to fly. Padded landing zones and safety nets catch "
                       "failed attempts. The air above buzzes with juvenile winged forms "
                       "practicing takeoffs, landings, and aerial manoeuvres.",
        "coordinates": [cx + 3, cy + 6],
        "location_type": "wilderness",
        "items": {"training_net_rope": {"quantity": 1, "value": 8}, "flight_training_pole": {"quantity": 1, "value": 10}},
        "exits": {
            "west": {"target": "wyrm_hatchery_bonding_cave", "type": "direction"},
            "north": {"target": "wyrm_hatchery_elder_nest", "type": "direction"}
        }
    }

    # --- Expanded Dragonbone Forge (+4 rooms) ---

    rooms["wyrm_forge_rune_chamber"] = {
        "id": "wyrm_forge_rune_chamber",
        "name": "Rune Chamber",
        "description": "A sealed chamber where enchantment runes are inscribed onto finished "
                       "dragonbone weapons. The air crackles with residual magic, and the walls "
                       "are covered with formulae and diagrams. A master enchanter works here, "
                       "her hands glowing with draconic power.",
        "coordinates": [cx - 1, cy + 3],
        "location_type": "building",
        "items": {"rune_inscription_tool": {"quantity": 1, "value": 30}, "draconic_power_crystal": {"quantity": 1, "value": 25}},
        "exits": {
            "south": {"target": "wyrm_forge_quenching_pool", "type": "direction"},
            "east": {"target": "wyrm_forge_bone_sorting", "type": "direction"}
        }
    }

    rooms["wyrm_forge_bone_sorting"] = {
        "id": "wyrm_forge_bone_sorting",
        "name": "Bone Sorting Hall",
        "description": "A long hall where dragonbones are sorted by type, age, and quality. "
                       "Master sorters can identify a bone's origin species, age at death, "
                       "and elemental alignment by touch alone. The best bones are reserved "
                       "for master-grade weapons.",
        "coordinates": [cx, cy + 3],
        "location_type": "building",
        "items": {"sorted_bone_sample": {"quantity": 1, "value": 15}, "bone_quality_gauge": {"quantity": 1, "value": 20}},
        "exits": {
            "west": {"target": "wyrm_forge_rune_chamber", "type": "direction"}
        }
    }

    rooms["wyrm_forge_apprentice_hall"] = {
        "id": "wyrm_forge_apprentice_hall",
        "name": "Apprentice's Hall",
        "description": "Where young smiths learn the art of dragonbone forging. Workbenches "
                       "line the walls, each with a small practice anvil and a set of basic "
                       "tools. The apprentices' first attempts — misshapen daggers and crooked "
                       "arrowheads — hang from a display board as motivation.",
        "coordinates": [cx - 2, cy + 2],
        "location_type": "building",
        "items": {"apprentice_dagger": {"quantity": 1, "value": 10}, "practice_bone_blank": {"quantity": 1, "value": 8}},
        "exits": {
            "east": {"target": "wyrm_forge_quenching_pool", "type": "direction"}
        }
    }

    rooms["wyrm_forge_dragon_bellows"] = {
        "id": "wyrm_forge_dragon_bellows",
        "name": "Dragon Bellows Chamber",
        "description": "Rather than mechanical bellows, the forge uses a captive volcanic vent "
                       "channelled through dragonbone pipes. The result is a blast of heat that "
                       "surpasses any conventional forge. The temperature here is extreme — "
                       "only dragon-scaled smiths can work for more than minutes at a time.",
        "coordinates": [cx - 2, cy + 1],
        "location_type": "building",
        "items": {"dragonbone_pipe_section": {"quantity": 1, "value": 22}, "volcanic_vent_stone": {"quantity": 1, "value": 15}},
        "exits": {
            "east": {"target": "wyrm_forge_main_hall", "type": "direction"}
        }
    }

    # === NEW SUB-REGION: Dragon's Graveyard (18 rooms) ===

    rooms["wyrm_graveyard_entrance"] = {
        "id": "wyrm_graveyard_entrance",
        "name": "Dragon's Graveyard Entrance",
        "description": "Two massive dragon skulls, jaws open, form a gateway into the sacred "
                       "Dragon's Graveyard — where wyrms go to die. Only the most trusted "
                       "dragonkin are permitted entry. The atmosphere is solemn, and even "
                       "the wind seems to hush as you pass between the skulls.",
        "coordinates": [cx - 6, cy - 3],
        "location_type": "wilderness",
        "items": {"graveyard_gate_scale": {"quantity": 1, "value": 18}},
        "exits": {
            "east": {"target": "wyrm_wastes_tar_pit", "type": "direction"},
            "west": {"target": "wyrm_graveyard_avenue", "type": "direction"}
        }
    }

    rooms["wyrm_graveyard_avenue"] = {
        "id": "wyrm_graveyard_avenue",
        "name": "Avenue of Fallen Wyrms",
        "description": "A processional avenue lined with complete dragon skeletons, each "
                       "positioned as if sleeping. Name plates in Draconic identify each — "
                       "legendary wyrms whose deeds shaped the island's history. Fresh flowers "
                       "are placed by dragon riders who honour their ancestors' bonded companions.",
        "coordinates": [cx - 7, cy - 3],
        "location_type": "wilderness",
        "items": {"fallen_wyrm_nameplate": {"quantity": 1, "value": 22}, "memorial_flower_wreath": {"quantity": 1, "value": 10}},
        "exits": {
            "east": {"target": "wyrm_graveyard_entrance", "type": "direction"},
            "north": {"target": "wyrm_graveyard_elder_circle", "type": "direction"},
            "south": {"target": "wyrm_graveyard_bone_field", "type": "direction"},
            "west": {"target": "wyrm_graveyard_mourning_pool", "type": "direction"}
        }
    }

    rooms["wyrm_graveyard_elder_circle"] = {
        "id": "wyrm_graveyard_elder_circle",
        "name": "Elder Dragon Circle",
        "description": "A ring of the largest dragon skeletons on the island, each an Elder "
                       "Wyrm that lived for centuries. Their skulls face inward, creating a "
                       "council-like arrangement. Legend says the spirits of these elders still "
                       "convene here on the solstice to judge the living.",
        "coordinates": [cx - 7, cy - 2],
        "location_type": "wilderness",
        "items": {"elder_wyrm_tooth": {"quantity": 1, "value": 45}, "spirit_council_stone": {"quantity": 1, "value": 30}},
        "exits": {
            "south": {"target": "wyrm_graveyard_avenue", "type": "direction"},
            "east": {"target": "wyrm_graveyard_hoard_garden", "type": "direction"},
            "north": {"target": "wyrm_graveyard_wind_tomb", "type": "direction"}
        }
    }

    rooms["wyrm_graveyard_hoard_garden"] = {
        "id": "wyrm_graveyard_hoard_garden",
        "name": "Hoard Garden",
        "description": "When a dragon dies, its hoard is scattered across its grave. Over "
                       "centuries, coins, gems, and precious metals have been absorbed into "
                       "the soil, creating a garden where gold flowers and gem-fruit trees "
                       "grow — a bizarre and beautiful treasure garden.",
        "coordinates": [cx - 6, cy - 2],
        "location_type": "wilderness",
        "items": {"gold_flower": {"quantity": 1, "value": 35}, "gem_fruit": {"quantity": 1, "value": 28}},
        "exits": {
            "west": {"target": "wyrm_graveyard_elder_circle", "type": "direction"},
            "south": {"target": "wyrm_graveyard_entrance", "type": "direction"}
        }
    }

    rooms["wyrm_graveyard_bone_field"] = {
        "id": "wyrm_graveyard_bone_field",
        "name": "Bone Field",
        "description": "An open field where the bones of lesser dragons have accumulated over "
                       "ages. The ground is a carpet of white — ribcages, vertebrae, and claws "
                       "in every direction. Walking requires stepping on bones, creating an "
                       "eerie crunching sound with every step.",
        "coordinates": [cx - 7, cy - 4],
        "location_type": "wilderness",
        "items": {"bone_field_vertebra": {"quantity": 2, "value": 8}, "claw_fragment": {"quantity": 1, "value": 12}},
        "exits": {
            "north": {"target": "wyrm_graveyard_avenue", "type": "direction"},
            "west": {"target": "wyrm_graveyard_skull_cave", "type": "direction"},
            "south": {"target": "wyrm_graveyard_scale_monument", "type": "direction"}
        }
    }

    rooms["wyrm_graveyard_skull_cave"] = {
        "id": "wyrm_graveyard_skull_cave",
        "name": "Skull Cave",
        "description": "A cave formed from the partially buried skull of an impossibly large "
                       "dragon — one far bigger than any recorded in known history. You enter "
                       "through the eye socket, and the interior has been used as a shrine. "
                       "What creature could have been this large?",
        "coordinates": [cx - 8, cy - 4],
        "location_type": "wilderness",
        "items": {"mega_dragon_bone": {"quantity": 1, "value": 60}, "skull_cave_offering": {"quantity": 1, "value": 20}},
        "exits": {
            "east": {"target": "wyrm_graveyard_bone_field", "type": "direction"},
            "north": {"target": "wyrm_graveyard_guardian_bones", "type": "direction"}
        }
    }

    rooms["wyrm_graveyard_guardian_bones"] = {
        "id": "wyrm_graveyard_guardian_bones",
        "name": "Guardian Bones",
        "description": "Two dragon skeletons arranged in a standing, alert posture on either "
                       "side of a narrow passage. Whether they died in this position or were "
                       "arranged post-mortem is debated. They seem to guard whatever lies "
                       "beyond with eternal vigilance.",
        "coordinates": [cx - 8, cy - 3],
        "location_type": "wilderness",
        "items": {"guardian_bone_scale": {"quantity": 1, "value": 25}, "standing_dragon_rib": {"quantity": 1, "value": 15}},
        "exits": {
            "south": {"target": "wyrm_graveyard_skull_cave", "type": "direction"},
            "east": {"target": "wyrm_graveyard_mourning_pool", "type": "direction"}
        }
    }

    rooms["wyrm_graveyard_mourning_pool"] = {
        "id": "wyrm_graveyard_mourning_pool",
        "name": "Mourning Pool",
        "description": "A clear pool fed by underground springs, surrounded by dragon bones. "
                       "Living dragons come here to mourn their dead — they drink from the "
                       "pool and sing low, mournful songs that resonate in the bones around "
                       "them. The acoustics create a haunting harmony.",
        "coordinates": [cx - 8, cy - 2],
        "location_type": "wilderness",
        "items": {"mourning_pool_water": {"quantity": 1, "value": 18}, "resonating_bone": {"quantity": 1, "value": 22}},
        "exits": {
            "south": {"target": "wyrm_graveyard_guardian_bones", "type": "direction"},
            "east": {"target": "wyrm_graveyard_avenue", "type": "direction"},
            "north": {"target": "wyrm_graveyard_spirit_hollow", "type": "direction"}
        }
    }

    rooms["wyrm_graveyard_spirit_hollow"] = {
        "id": "wyrm_graveyard_spirit_hollow",
        "name": "Spirit Hollow",
        "description": "A deep depression where dragon spirits are said to linger before "
                       "passing on. On clear nights, translucent forms of dragons can be "
                       "seen soaring above the hollow, reliving their final flights. The "
                       "experience of watching is both beautiful and deeply sorrowful.",
        "coordinates": [cx - 8, cy - 1],
        "location_type": "wilderness",
        "items": {"spirit_scale": {"quantity": 1, "value": 35}, "spectral_wing_feather": {"quantity": 1, "value": 25}},
        "exits": {
            "south": {"target": "wyrm_graveyard_mourning_pool", "type": "direction"},
            "east": {"target": "wyrm_graveyard_wind_tomb", "type": "direction"}
        }
    }

    rooms["wyrm_graveyard_wind_tomb"] = {
        "id": "wyrm_graveyard_wind_tomb",
        "name": "Wind Tomb",
        "description": "A tomb carved into a cliff face, open to the sky and wind. Dragons "
                       "who died in flight are brought here — their bodies arranged with wings "
                       "spread on natural wind channels so the breeze perpetually flows over "
                       "them, symbolizing eternal flight.",
        "coordinates": [cx - 7, cy - 1],
        "location_type": "wilderness",
        "items": {"wind_tomb_feather": {"quantity": 1, "value": 20}, "flight_symbol_stone": {"quantity": 1, "value": 15}},
        "exits": {
            "south": {"target": "wyrm_graveyard_elder_circle", "type": "direction"},
            "west": {"target": "wyrm_graveyard_spirit_hollow", "type": "direction"},
            "east": {"target": "wyrm_graveyard_crystal_tomb", "type": "direction"}
        }
    }

    rooms["wyrm_graveyard_crystal_tomb"] = {
        "id": "wyrm_graveyard_crystal_tomb",
        "name": "Crystal Tomb",
        "description": "A dragon entombed in a massive crystal formation — volcanic minerals "
                       "flowed over the body and crystallized, preserving the wyrm perfectly. "
                       "Through the clear crystal, every scale, claw, and tooth is visible "
                       "in pristine condition, frozen in eternal beauty.",
        "coordinates": [cx - 6, cy - 1],
        "location_type": "wilderness",
        "items": {"crystal_tomb_shard": {"quantity": 1, "value": 40}, "preserved_dragon_scale": {"quantity": 1, "value": 50}},
        "exits": {
            "west": {"target": "wyrm_graveyard_wind_tomb", "type": "direction"}
        }
    }

    rooms["wyrm_graveyard_scale_monument"] = {
        "id": "wyrm_graveyard_scale_monument",
        "name": "Scale Monument",
        "description": "A towering pillar constructed entirely from dragon scales donated by "
                       "living dragons in memory of the dead. Each scale is inscribed with a "
                       "name in Draconic. Adding a scale is a sacred act of remembrance. The "
                       "monument catches sunlight and scatters rainbow light across the graveyard.",
        "coordinates": [cx - 7, cy - 5],
        "location_type": "wilderness",
        "items": {"memorial_scale": {"quantity": 1, "value": 20}, "rainbow_light_crystal": {"quantity": 1, "value": 18}},
        "exits": {
            "north": {"target": "wyrm_graveyard_bone_field", "type": "direction"},
            "east": {"target": "wyrm_graveyard_fossil_wall", "type": "direction"}
        }
    }

    rooms["wyrm_graveyard_fossil_wall"] = {
        "id": "wyrm_graveyard_fossil_wall",
        "name": "Fossil Wall",
        "description": "A natural cliff face where dragon fossils are embedded in the rock "
                       "in layers — a geological record of dragon evolution spanning millions "
                       "of years. The oldest fossils, at the bottom, show creatures barely "
                       "recognizable as dragons. The newest match modern species exactly.",
        "coordinates": [cx - 6, cy - 5],
        "location_type": "wilderness",
        "items": {"evolution_fossil": {"quantity": 1, "value": 35}, "geological_layer_sample": {"quantity": 1, "value": 15}},
        "exits": {
            "west": {"target": "wyrm_graveyard_scale_monument", "type": "direction"}
        }
    }

    rooms["wyrm_graveyard_silence_chamber"] = {
        "id": "wyrm_graveyard_silence_chamber",
        "name": "Chamber of Silence",
        "description": "A natural cavern deep in the graveyard where all sound is absorbed. "
                       "Not even shouting produces an echo. The silence is absolute and "
                       "profound — dragon riders visit when their grief is too loud for words. "
                       "The walls are smooth obsidian that reflects nothing.",
        "coordinates": [cx - 6, cy - 4],
        "location_type": "wilderness",
        "items": {"silence_stone": {"quantity": 1, "value": 25}, "void_obsidian": {"quantity": 1, "value": 20}},
        "exits": {
            "north": {"target": "wyrm_graveyard_hoard_garden", "type": "direction"},
            "south": {"target": "wyrm_graveyard_fossil_wall", "type": "direction"}
        }
    }

    rooms["wyrm_graveyard_first_dragon"] = {
        "id": "wyrm_graveyard_first_dragon",
        "name": "Tomb of the First Dragon",
        "description": "The eldest and most sacred tomb in the graveyard — that of the First "
                       "Dragon, the progenitor of all dragonkind on this island. The skeleton "
                       "is small by modern standards but perfectly formed. Its bones glow with "
                       "a soft golden light, and the air around it is always warm.",
        "coordinates": [cx - 8, cy],
        "location_type": "wilderness",
        "items": {"first_dragon_scale": {"quantity": 1, "value": 80}, "golden_bone_fragment": {"quantity": 1, "value": 50}},
        "exits": {
            "south": {"target": "wyrm_graveyard_spirit_hollow", "type": "direction"}
        }
    }

    # === NEW SUB-REGION: Stormscale Cliffs (15 rooms) ===

    rooms["wyrm_stormscale_path"] = {
        "id": "wyrm_stormscale_path",
        "name": "Stormscale Cliff Path",
        "description": "A windswept path along the island's eastern cliffs where storms from "
                       "the open ocean batter the rock. The cliffs are streaked with mineral "
                       "deposits that flash like dragon scales in lightning. Only the hardiest "
                       "dragons nest here, those attuned to storm and lightning.",
        "coordinates": [cx + 5, cy - 2],
        "location_type": "wilderness",
        "items": {"stormscale_deposit": {"quantity": 1, "value": 15}},
        "exits": {
            "west": {"target": "wyrm_peaks_lava_bridge", "type": "direction"},
            "north": {"target": "wyrm_stormscale_lookout", "type": "direction"},
            "south": {"target": "wyrm_stormscale_thunder_cave", "type": "direction"}
        }
    }

    rooms["wyrm_stormscale_lookout"] = {
        "id": "wyrm_stormscale_lookout",
        "name": "Storm Lookout",
        "description": "A fortified observation post on the cliff edge where weather watchers "
                       "track approaching storms. Storm dragons — a rare subspecies with scales "
                       "that crackle with electricity — are spotted from here during tempests, "
                       "riding the lightning between cloudbanks.",
        "coordinates": [cx + 5, cy - 1],
        "location_type": "building",
        "items": {"storm_spyglass": {"quantity": 1, "value": 22}, "weather_chart": {"quantity": 1, "value": 10}},
        "exits": {
            "south": {"target": "wyrm_stormscale_path", "type": "direction"},
            "west": {"target": "wyrm_stormscale_lightning_rod", "type": "direction"}
        }
    }

    rooms["wyrm_stormscale_lightning_rod"] = {
        "id": "wyrm_stormscale_lightning_rod",
        "name": "Lightning Rod Tower",
        "description": "A tall metal tower designed to attract and channel lightning. Dragonbone "
                       "conductors route the energy into a storage matrix beneath the tower. "
                       "The stored lightning powers forges and enchanting equipment across the "
                       "island. During storms, the tower glows blue-white.",
        "coordinates": [cx + 4, cy - 1],
        "location_type": "building",
        "items": {"lightning_crystal": {"quantity": 1, "value": 35}, "conductor_fragment": {"quantity": 1, "value": 18}},
        "exits": {
            "east": {"target": "wyrm_stormscale_lookout", "type": "direction"},
            "south": {"target": "wyrm_stormscale_charged_cave", "type": "direction"}
        }
    }

    rooms["wyrm_stormscale_thunder_cave"] = {
        "id": "wyrm_stormscale_thunder_cave",
        "name": "Thunder Cave",
        "description": "A sea cave where waves create booming sounds that reverberate through "
                       "the cliff. The acoustics are so powerful that the sound can be felt in "
                       "your chest. Storm dragons use the cave's resonance as part of their "
                       "mating display, adding their roars to the thunder.",
        "coordinates": [cx + 5, cy - 3],
        "location_type": "wilderness",
        "items": {"thunder_stone": {"quantity": 1, "value": 20}, "resonance_crystal": {"quantity": 1, "value": 15}},
        "exits": {
            "north": {"target": "wyrm_stormscale_path", "type": "direction"},
            "west": {"target": "wyrm_stormscale_nest_wall", "type": "direction"}
        }
    }

    rooms["wyrm_stormscale_nest_wall"] = {
        "id": "wyrm_stormscale_nest_wall",
        "name": "Storm Drake Nest Wall",
        "description": "A sheer cliff face pockmarked with nesting caves, each home to a "
                       "storm dragon. The drakes enter and exit at speed, crackling with "
                       "electrical energy. Their eggs glow with an inner light, and the "
                       "hatchlings' first breath is always a bolt of lightning.",
        "coordinates": [cx + 4, cy - 3],
        "location_type": "wilderness",
        "items": {"storm_drake_eggshell": {"quantity": 1, "value": 30}, "lightning_feather": {"quantity": 1, "value": 22}},
        "exits": {
            "east": {"target": "wyrm_stormscale_thunder_cave", "type": "direction"},
            "north": {"target": "wyrm_stormscale_charged_cave", "type": "direction"},
            "south": {"target": "wyrm_stormscale_tidal_roost", "type": "direction"}
        }
    }

    rooms["wyrm_stormscale_charged_cave"] = {
        "id": "wyrm_stormscale_charged_cave",
        "name": "Charged Cave",
        "description": "A cave where the very rock is charged with electrical energy. Static "
                       "makes hair stand on end and metal objects spark when touched. The walls "
                       "are veined with conductive minerals that channel lightning deep into the "
                       "earth. Small arcs of electricity dance continuously.",
        "coordinates": [cx + 4, cy - 2],
        "location_type": "wilderness",
        "items": {"charged_mineral_vein": {"quantity": 1, "value": 25}, "static_crystal": {"quantity": 1, "value": 18}},
        "exits": {
            "north": {"target": "wyrm_stormscale_lightning_rod", "type": "direction"},
            "south": {"target": "wyrm_stormscale_nest_wall", "type": "direction"},
            "east": {"target": "wyrm_stormscale_cliff_bridge", "type": "direction"}
        }
    }

    rooms["wyrm_stormscale_cliff_bridge"] = {
        "id": "wyrm_stormscale_cliff_bridge",
        "name": "Cliff Bridge",
        "description": "A dramatic natural stone arch spanning a deep chasm in the cliffs. "
                       "The bridge is narrow and the wind fierce — crossing requires courage "
                       "and steady footing. Dragons use the updrafts from the chasm for "
                       "effortless soaring, spiralling past in breathtaking displays.",
        "coordinates": [cx + 5, cy - 2],
        "location_type": "wilderness",
        "items": {"bridge_stone_chip": {"quantity": 1, "value": 8}, "chasm_wind_crystal": {"quantity": 1, "value": 15}},
        "exits": {
            "west": {"target": "wyrm_stormscale_charged_cave", "type": "direction"},
            "east": {"target": "wyrm_stormscale_sea_pillar", "type": "direction"}
        }
    }

    rooms["wyrm_stormscale_sea_pillar"] = {
        "id": "wyrm_stormscale_sea_pillar",
        "name": "Sea Pillar",
        "description": "A towering pillar of rock standing alone in the sea, separated from "
                       "the cliffs by a narrow gap. Only accessible by dragon or by a very "
                       "brave jump. The pillar's flat top is used as a dragon launch platform "
                       "for long-distance flights across the ocean.",
        "coordinates": [cx + 6, cy - 2],
        "location_type": "wilderness",
        "items": {"sea_pillar_stone": {"quantity": 1, "value": 12}, "launch_platform_scale": {"quantity": 1, "value": 18}},
        "exits": {
            "west": {"target": "wyrm_stormscale_cliff_bridge", "type": "direction"}
        }
    }

    rooms["wyrm_stormscale_tidal_roost"] = {
        "id": "wyrm_stormscale_tidal_roost",
        "name": "Tidal Roost",
        "description": "A low cliff shelf that floods at high tide, accessible only during "
                       "low water. Sea dragons — a rare aquatic variant — rest here between "
                       "deep ocean hunts. Their scales are blue-green and barnacle-encrusted, "
                       "and they smell of saltwater and kelp.",
        "coordinates": [cx + 4, cy - 4],
        "location_type": "wilderness",
        "items": {"sea_dragon_scale": {"quantity": 1, "value": 35}, "barnacle_cluster": {"quantity": 1, "value": 10}},
        "exits": {
            "north": {"target": "wyrm_stormscale_nest_wall", "type": "direction"},
            "west": {"target": "wyrm_stormscale_kelp_cave", "type": "direction"}
        }
    }

    rooms["wyrm_stormscale_kelp_cave"] = {
        "id": "wyrm_stormscale_kelp_cave",
        "name": "Kelp Cave",
        "description": "A sea cave draped with enormous kelp fronds that create a green "
                       "curtain across the entrance. Inside, tide pools house strange "
                       "bioluminescent creatures that the sea dragons feed upon. The cave "
                       "is damp and smells strongly of the ocean.",
        "coordinates": [cx + 3, cy - 4],
        "location_type": "wilderness",
        "items": {"giant_kelp_frond": {"quantity": 1, "value": 10}, "bioluminescent_fish": {"quantity": 1, "value": 18}},
        "exits": {
            "east": {"target": "wyrm_stormscale_tidal_roost", "type": "direction"}
        }
    }

    rooms["wyrm_stormscale_wind_altar"] = {
        "id": "wyrm_stormscale_wind_altar",
        "name": "Wind Altar",
        "description": "A high cliff altar where storm dragons are blessed before their first "
                       "flight. The altar stone is struck by lightning so frequently that it has "
                       "partially melted into a glass-smooth surface. Prayers inscribed on it "
                       "glow during storms.",
        "coordinates": [cx + 3, cy - 3],
        "location_type": "wilderness",
        "items": {"wind_blessing_stone": {"quantity": 1, "value": 25}, "melted_altar_glass": {"quantity": 1, "value": 20}},
        "exits": {
            "east": {"target": "wyrm_stormscale_nest_wall", "type": "direction"},
            "north": {"target": "wyrm_stormscale_eyrie", "type": "direction"}
        }
    }

    rooms["wyrm_stormscale_eyrie"] = {
        "id": "wyrm_stormscale_eyrie",
        "name": "Storm Dragon Eyrie",
        "description": "The highest nesting site on the Stormscale Cliffs, home to the oldest "
                       "and most powerful storm dragon on the island. Its nest is built from "
                       "shattered ship masts and lightning-fused metal. The dragon itself is "
                       "rarely seen — only the thunderclap of its wingbeats announces its arrival.",
        "coordinates": [cx + 3, cy - 2],
        "location_type": "wilderness",
        "items": {"storm_elder_scale": {"quantity": 1, "value": 55}, "lightning_fused_iron": {"quantity": 1, "value": 35}},
        "exits": {
            "south": {"target": "wyrm_stormscale_wind_altar", "type": "direction"},
            "east": {"target": "wyrm_stormscale_charged_cave", "type": "direction"}
        }
    }

    rooms["wyrm_stormscale_weather_cave"] = {
        "id": "wyrm_stormscale_weather_cave",
        "name": "Weather Reading Cave",
        "description": "A cave used by the island's weather readers — scholars who predict "
                       "storms by studying dragon behaviour and volcanic patterns. Their "
                       "instruments line the walls: barometers, wind gauges, and crystal "
                       "spheres that change colour with atmospheric pressure.",
        "coordinates": [cx + 6, cy - 3],
        "location_type": "building",
        "items": {"weather_crystal_sphere": {"quantity": 1, "value": 22}, "storm_barometer": {"quantity": 1, "value": 15}},
        "exits": {
            "west": {"target": "wyrm_stormscale_thunder_cave", "type": "direction"}
        }
    }



def generate_abyssal_reach(rooms):
    """Generate Island 7: The Abyssal Reach - Eldritch deep-ocean abyss island (~73 rooms)."""

    cx, cy = 15, -60  # Center coordinates

    # =========================================================================
    # THE ABYSSAL REACH - Eldritch Abyss Island (Level 40+, Tier 7)
    # A partially-submerged gateway to the deep ocean abyss. Lovecraftian
    # horror, impossible geometry, deep-sea creatures, alien ruins, and
    # madness-inducing architecture.
    # Sub-regions: Abyssal Docks, Abyssal Outpost, Sunken Ruins,
    #              Pressure Depths, Madness Reef, Deep One City,
    #              The Threshold, Eldritch Shores
    # =========================================================================

    # --- Abyssal Docks (3 rooms) ---

    rooms["abyssal_docks"] = {
        "id": "abyssal_docks",
        "name": "The Abyssal Reach - Void-Touched Dock",
        "description": "A dock of black coral and petrified bone extends over water so dark it reflects "
                       "nothing — not the sky, not the dock, not you. The planks vibrate with a subsonic "
                       "hum that rattles your teeth, and the air tastes of ozone and ancient brine.",
        "coordinates": [cx, cy - 7],
        "location_type": "dock",
        "items": {},
        "exits": {
            "board mainland": {
                "target": "harbor_west_dock",
                "type": "boat_travel",
                "island_id": "abyssal_depths",
                "display": "Return to Grand Harbor",
                "unlock_cost": 0,
                "fare_cost": 0,
                "min_level": 1,
                "transition_text": "You board the void-touched vessel. Reality snaps back into focus\nas the ship pulls away from the impossible shore. The journey home\nfeels like waking from a dream you can't quite remember. After what\nmight be days or centuries, Grand Harbor's lanterns pierce the dark..."
            },
            "north": {"target": "abyssal_outpost_gate", "type": "direction"},
            "east": {"target": "abyssal_docks_cargo", "type": "direction"},
            "west": {"target": "abyssal_docks_beacon", "type": "direction"}
        }
    }

    rooms["abyssal_docks_cargo"] = {
        "id": "abyssal_docks_cargo",
        "name": "Cargo Platform",
        "description": "A listing platform of fused stone and chitin where sealed containers of an unknown "
                       "alloy are stacked in patterns that hurt to look at directly. The crates weep a dark "
                       "ichor that evaporates before hitting the ground, and the labels are in no human script.",
        "coordinates": [cx + 1, cy - 7],
        "location_type": "dock",
        "items": {"void_sealed_crate": {"quantity": 1, "value": 35}, "abyssal_ichor_vial": {"quantity": 2, "value": 18}},
        "exits": {
            "west": {"target": "abyssal_docks", "type": "direction"},
            "east": {"target": "abyssal_docks_sunken_wharf", "type": "direction"}
        }
    }

    rooms["abyssal_docks_beacon"] = {
        "id": "abyssal_docks_beacon",
        "name": "Void Beacon",
        "description": "A spiralling tower of fused obsidian and pale bone, crowned with a light that burns "
                       "a colour your mind refuses to name. The beacon pulses in a rhythm that almost matches "
                       "your heartbeat — almost, but not quite, and the difference is maddening.",
        "coordinates": [cx - 1, cy - 7],
        "location_type": "building",
        "items": {"void_prism_shard": {"quantity": 1, "value": 28}},
        "exits": {
            "east": {"target": "abyssal_docks", "type": "direction"},
            "west": {"target": "abyssal_shores_black_beach", "type": "direction"}
        }
    }

    # --- Eldritch Shores (6 rooms) ---

    rooms["abyssal_shores_black_beach"] = {
        "id": "abyssal_shores_black_beach",
        "name": "Black Sand Beach",
        "description": "Sand the colour of crushed charcoal stretches along a coastline that curves in "
                       "directions that shouldn't exist. The tide comes in as spirals rather than waves, "
                       "depositing things that glitter with alien geometries and smell of distant stars.",
        "coordinates": [cx - 2, cy - 7],
        "location_type": "wilderness",
        "items": {"black_pearl": {"quantity": 1, "value": 30}, "star_touched_shell": {"quantity": 2, "value": 15}},
        "exits": {
            "east": {"target": "abyssal_docks_beacon", "type": "direction"},
            "west": {"target": "abyssal_shores_tide_pools", "type": "direction"},
            "south": {"target": "abyssal_shores_anomaly", "type": "direction"}
        }
    }

    rooms["abyssal_shores_tide_pools"] = {
        "id": "abyssal_shores_tide_pools",
        "name": "Impossible Tide Pools",
        "description": "Pools of water that are deeper than they should be — some appear inches deep but "
                       "contain entire ecosystems of bioluminescent creatures spiralling downward into "
                       "impossible depths. Your reflection in the water moves a half-second behind you.",
        "coordinates": [cx - 3, cy - 7],
        "location_type": "wilderness",
        "items": {"abyssal_anemone": {"quantity": 2, "value": 12}, "depth_water_vial": {"quantity": 1, "value": 20}},
        "exits": {
            "east": {"target": "abyssal_shores_black_beach", "type": "direction"},
            "north": {"target": "abyssal_shores_wreckage", "type": "direction"},
            "west": {"target": "abyssal_shores_lighthouse", "type": "direction"}
        }
    }

    rooms["abyssal_shores_lighthouse"] = {
        "id": "abyssal_shores_lighthouse",
        "name": "Broken Lighthouse",
        "description": "A lighthouse twisted by enormous force, its stone spiral now corkscrewing in the "
                       "wrong direction. The lantern room at the top emits a beam of pure darkness that "
                       "somehow illuminates things better left unseen on the horizon.",
        "coordinates": [cx - 4, cy - 7],
        "location_type": "building",
        "items": {"darklight_lens_fragment": {"quantity": 1, "value": 35}},
        "exits": {
            "east": {"target": "abyssal_shores_tide_pools", "type": "direction"},
            "west": {"target": "abyssal_shores_void_beach", "type": "direction"}
        }
    }

    rooms["abyssal_shores_wreckage"] = {
        "id": "abyssal_shores_wreckage",
        "name": "Dimensional Wreckage",
        "description": "The shattered remains of ships that never sailed any earthly sea. Hulls of crystallised "
                       "thought, masts of frozen lightning, and sails woven from solidified screams litter the "
                       "shore. Some wreckage phases in and out of visibility, never fully present.",
        "coordinates": [cx - 3, cy - 6],
        "location_type": "wilderness",
        "items": {"reality_splinter": {"quantity": 1, "value": 45}, "frozen_lightning_spar": {"quantity": 1, "value": 30}},
        "exits": {
            "south": {"target": "abyssal_shores_tide_pools", "type": "direction"},
            "east": {"target": "abyssal_shores_driftwood_grove", "type": "direction"}
        }
    }

    rooms["abyssal_shores_driftwood_grove"] = {
        "id": "abyssal_shores_driftwood_grove",
        "name": "Alien Driftwood Grove",
        "description": "Trees of petrified coral and mineral-encrusted driftwood from a thousand drowned "
                       "worlds stand rooted in the black sand. Their branches grow in fractal patterns that "
                       "make your eyes water, and faint whispers emanate from the wood in unspoken tongues.",
        "coordinates": [cx - 2, cy - 6],
        "location_type": "wilderness",
        "items": {"fractal_driftwood": {"quantity": 2, "value": 14}, "petrified_coral_branch": {"quantity": 1, "value": 22}},
        "exits": {
            "west": {"target": "abyssal_shores_wreckage", "type": "direction"},
            "east": {"target": "abyssal_outpost_supply_depot", "type": "direction"}
        }
    }

    rooms["abyssal_shores_anomaly"] = {
        "id": "abyssal_shores_anomaly",
        "name": "Shore Anomaly",
        "description": "A section of beach where the sand flows upward in slow spirals and gravity operates "
                       "at odd angles. Flotsam from elsewhere hangs frozen in mid-air — a child's toy from a "
                       "world that never was, a book written in colours, a clock counting backwards to zero.",
        "coordinates": [cx - 2, cy - 8],
        "location_type": "wilderness",
        "items": {"gravity_displaced_stone": {"quantity": 1, "value": 40}, "otherworld_trinket": {"quantity": 1, "value": 25}},
        "exits": {
            "north": {"target": "abyssal_shores_black_beach", "type": "direction"},
            "west": {"target": "abyssal_shores_rift_pool", "type": "direction"}
        }
    }

    # --- Abyssal Outpost (14 rooms) ---

    rooms["abyssal_outpost_gate"] = {
        "id": "abyssal_outpost_gate",
        "name": "Abyssal Outpost Gate",
        "description": "A fortified gateway of deep-sea iron and warded obsidian marks the entrance to "
                       "humanity's last outpost on the Reach. Guards in sealed pressure-suits eye you "
                       "through visors inscribed with sanity-preserving runes. Beyond, dim lanterns flicker.",
        "coordinates": [cx, cy - 6],
        "location_type": "settlement",
        "items": {},
        "exits": {
            "south": {"target": "abyssal_docks", "type": "direction"},
            "north": {"target": "abyssal_outpost_courtyard", "type": "direction"},
            "east": {"target": "abyssal_outpost_healer", "type": "direction"},
            "west": {"target": "abyssal_outpost_supply_depot", "type": "direction"}
        }
    }

    rooms["abyssal_outpost_healer"] = {
        "id": "abyssal_outpost_healer",
        "name": "Field Healer's Station",
        "description": "A reinforced tent reeking of medicinal salts and void-ward incense. The healer — a "
                       "gaunt woman with silver-etched pupils — treats wounds of both body and mind. Jars of "
                       "glowing salve line the shelves, each labelled with warnings about prolonged exposure.",
        "coordinates": [cx + 1, cy - 6],
        "location_type": "building",
        "items": {"void_ward_salve": {"quantity": 2, "value": 25}, "sanity_tincture": {"quantity": 1, "value": 35}},
        "exits": {
            "west": {"target": "abyssal_outpost_gate", "type": "direction"}
        }
    }

    rooms["abyssal_outpost_supply_depot"] = {
        "id": "abyssal_outpost_supply_depot",
        "name": "Supply Depot",
        "description": "A squat bunker of riveted iron plates, half-buried in the black ground. Crates of "
                       "rations, void-proofed equipment, and sealed containers of breathable air are stacked "
                       "to the ceiling. The quartermaster counts everything twice — things go missing here.\n\n"
                       "The quartermaster grunts: 'Need gear? Use SHOP commands. Don't touch what ain't paid for.'",
        "coordinates": [cx - 1, cy - 6],
        "location_type": "building",
        "shop": True,
        "items": {"sealed_ration_pack": {"quantity": 3, "value": 10}, "void_proofed_rope": {"quantity": 1, "value": 18}},
        "exits": {
            "east": {"target": "abyssal_outpost_gate", "type": "direction"},
            "west": {"target": "abyssal_shores_driftwood_grove", "type": "direction"}
        }
    }

    rooms["abyssal_outpost_courtyard"] = {
        "id": "abyssal_outpost_courtyard",
        "name": "Outpost Courtyard",
        "description": "The central yard of the outpost, paved with warded flagstones that glow faintly "
                       "blue underfoot. Soldiers, scholars, and survivors gather around a perpetual fire "
                       "that burns without fuel. The sky above is wrong — too many stars, in constellations "
                       "no astronomer has ever charted.",
        "coordinates": [cx, cy - 5],
        "location_type": "settlement",
        "items": {},
        "exits": {
            "south": {"target": "abyssal_outpost_gate", "type": "direction"},
            "north": {"target": "abyssal_outpost_war_room", "type": "direction"},
            "east": {"target": "abyssal_outpost_barracks", "type": "direction"},
            "west": {"target": "abyssal_outpost_tavern", "type": "direction"},
            "northeast": {"target": "abyssal_outpost_lookout", "type": "direction"}
        }
    }

    rooms["abyssal_outpost_barracks"] = {
        "id": "abyssal_outpost_barracks",
        "name": "Outpost Barracks",
        "description": "Rows of iron bunks bolted to the floor, each fitted with restraints for sleepers "
                       "who might walk in their nightmares. The walls are scratched with tally marks and "
                       "desperate prayers. A notice reads: 'Sleep in pairs. Report all dreams to Command.'",
        "coordinates": [cx + 1, cy - 5],
        "location_type": "building",
        "items": {"iron_bunk_restraint": {"quantity": 1, "value": 8}},
        "exits": {
            "west": {"target": "abyssal_outpost_courtyard", "type": "direction"},
            "east": {"target": "abyssal_outpost_armory", "type": "direction"},
            "north": {"target": "abyssal_outpost_training_yard", "type": "direction"}
        }
    }

    rooms["abyssal_outpost_armory"] = {
        "id": "abyssal_outpost_armory",
        "name": "Void-Warded Armory",
        "description": "Weapons of deep-sea iron and armour etched with sanity glyphs hang on racks behind "
                       "warded glass. Each piece is designed not just to kill, but to resist the reality-warping "
                       "effects of the Reach. The armourer mutters constantly, counting each item over and over.",
        "coordinates": [cx + 2, cy - 5],
        "location_type": "building",
        "items": {"void_warded_blade": {"quantity": 1, "value": 65}, "pressure_helm": {"quantity": 1, "value": 50}},
        "exits": {
            "west": {"target": "abyssal_outpost_barracks", "type": "direction"},
            "east": {"target": "abyssal_outpost_vault", "type": "direction"}
        }
    }

    rooms["abyssal_outpost_training_yard"] = {
        "id": "abyssal_outpost_training_yard",
        "name": "Training Yard",
        "description": "A yard of packed black earth where soldiers drill against training dummies shaped "
                       "like the things that crawl from the deep. Instructors shout techniques for fighting "
                       "in altered gravity and maintaining formation when geometry itself becomes hostile.",
        "coordinates": [cx + 1, cy - 4],
        "location_type": "settlement",
        "items": {"training_blade_abyssal": {"quantity": 1, "value": 12}},
        "exits": {
            "south": {"target": "abyssal_outpost_barracks", "type": "direction"}
        }
    }

    rooms["abyssal_outpost_tavern"] = {
        "id": "abyssal_outpost_tavern",
        "name": "The Drowned Anchor",
        "description": "A tavern built from salvaged ship timbers and sealed with pitch. The drinks here "
                       "are potent enough to drown the whispers, and that's the point. Veterans sit in "
                       "shadowed corners, eyes haunted, nursing cups of something that glows faintly violet.",
        "coordinates": [cx - 1, cy - 5],
        "location_type": "building",
        "items": {"void_still_spirits": {"quantity": 2, "value": 15}, "drowned_anchor_mug": {"quantity": 1, "value": 8}},
        "exits": {
            "east": {"target": "abyssal_outpost_courtyard", "type": "direction"},
            "north": {"target": "abyssal_outpost_mess_hall", "type": "direction"},
            "west": {"target": "abyssal_outpost_shrine", "type": "direction"}
        }
    }

    rooms["abyssal_outpost_shrine"] = {
        "id": "abyssal_outpost_shrine",
        "name": "Shrine of the Steadfast Mind",
        "description": "A small chapel reinforced with silver and cold iron, dedicated to no specific god "
                       "but to the concept of mental fortitude itself. Candles of rendered deep-sea fat burn "
                       "with a steady, calming light. Soldiers come here to pray before descending further.",
        "coordinates": [cx - 2, cy - 5],
        "location_type": "building",
        "items": {"steadfast_mind_candle": {"quantity": 2, "value": 20}, "silver_ward_token": {"quantity": 1, "value": 30}},
        "exits": {
            "east": {"target": "abyssal_outpost_tavern", "type": "direction"},
            "west": {"target": "abyssal_outpost_ritual_circle", "type": "direction"}
        }
    }

    rooms["abyssal_outpost_mess_hall"] = {
        "id": "abyssal_outpost_mess_hall",
        "name": "Mess Hall",
        "description": "A long, low room where soldiers eat in tense silence. The food is bland by design — "
                       "anything with too much flavour might be contaminated by the Reach's influence. A cook "
                       "stirs a vast pot of grey stew, whispering the recipe like a protective incantation.",
        "coordinates": [cx - 1, cy - 4],
        "location_type": "building",
        "items": {"bland_ration_stew": {"quantity": 3, "value": 5}},
        "exits": {
            "south": {"target": "abyssal_outpost_tavern", "type": "direction"},
            "west": {"target": "abyssal_outpost_market", "type": "direction"}
        }
    }

    rooms["abyssal_outpost_war_room"] = {
        "id": "abyssal_outpost_war_room",
        "name": "War Room",
        "description": "A fortified chamber with maps that redraw themselves as the Reach shifts. Pins and "
                       "strings mark known safe routes, creature sightings, and zones of total reality failure. "
                       "The command desk is bolted to the floor — not against storms, but against gravity shifts.",
        "coordinates": [cx, cy - 4],
        "location_type": "building",
        "items": {"shifting_map_fragment": {"quantity": 1, "value": 22}},
        "exits": {
            "south": {"target": "abyssal_outpost_courtyard", "type": "direction"},
            "east": {"target": "abyssal_outpost_commander", "type": "direction"},
            "north": {"target": "abyssal_depths_descent", "type": "direction"}
        }
    }

    rooms["abyssal_outpost_commander"] = {
        "id": "abyssal_outpost_commander",
        "name": "Commander's Quarters",
        "description": "The private chambers of Commander Voss, a woman who has served three tours on the "
                       "Reach and still retains most of her sanity. Her walls are covered in sketches of "
                       "things she's seen — things she draws so she doesn't have to remember them.",
        "coordinates": [cx + 1, cy - 3],
        "location_type": "building",
        "items": {"commander_voss_sketches": {"quantity": 1, "value": 15}},
        "exits": {
            "west": {"target": "abyssal_outpost_war_room", "type": "direction"},
            "east": {"target": "abyssal_outpost_observation", "type": "direction"}
        }
    }

    rooms["abyssal_outpost_lookout"] = {
        "id": "abyssal_outpost_lookout",
        "name": "Lookout Tower",
        "description": "A tall iron tower with reinforced viewing slits. From here you can see the impossible "
                       "geography of the Reach — the way the horizon curves upward, the patches of ocean that "
                       "flow vertically, and the distant city-shapes that shouldn't exist beneath the waves.",
        "coordinates": [cx + 2, cy - 4],
        "location_type": "building",
        "items": {"void_spyglass": {"quantity": 1, "value": 40}},
        "exits": {
            "southwest": {"target": "abyssal_outpost_courtyard", "type": "direction"},
            "east": {"target": "abyssal_reef_entrance", "type": "direction"}
        }
    }

    rooms["abyssal_outpost_market"] = {
        "id": "abyssal_outpost_market",
        "name": "Salvage Market",
        "description": "Not a proper market but a collection of blankets and crates where soldiers trade "
                       "salvage from expeditions into the Reach. Alien artefacts, deep-sea crystals, and "
                       "fragments of pre-human technology change hands at inflated prices. Everything is "
                       "examined for curses before sale.",
        "coordinates": [cx - 2, cy - 4],
        "location_type": "building",
        "items": {"deep_crystal_chunk": {"quantity": 1, "value": 38}, "alien_artefact_fragment": {"quantity": 1, "value": 50}},
        "exits": {
            "east": {"target": "abyssal_outpost_mess_hall", "type": "direction"},
            "west": {"target": "abyssal_ruins_entrance", "type": "direction"}
        }
    }

    # --- Sunken Ruins (12 rooms) ---

    rooms["abyssal_ruins_entrance"] = {
        "id": "abyssal_ruins_entrance",
        "name": "Sunken Ruins - Cyclopean Gateway",
        "description": "A gateway of blocks so massive no human civilisation could have placed them, each "
                       "stone carved with spiralling glyphs that move in your peripheral vision. The "
                       "architecture is wrong — angles that should be right angles aren't, and the doorways "
                       "are shaped for bodies not quite human.",
        "coordinates": [cx - 3, cy - 4],
        "location_type": "wilderness",
        "items": {"cyclopean_stone_chip": {"quantity": 2, "value": 15}},
        "exits": {
            "east": {"target": "abyssal_outpost_market", "type": "direction"},
            "west": {"target": "abyssal_ruins_passage", "type": "direction"},
            "north": {"target": "abyssal_ruins_mural_chamber", "type": "direction"}
        }
    }

    rooms["abyssal_ruins_passage"] = {
        "id": "abyssal_ruins_passage",
        "name": "Narrow Passage",
        "description": "A corridor that narrows and widens with no architectural logic, its walls slick "
                       "with bioluminescent slime that pulses in time with your breathing. The ceiling is "
                       "covered in thousands of tiny carvings — a star map millions of years out of date.",
        "coordinates": [cx - 4, cy - 4],
        "location_type": "wilderness",
        "items": {"bioluminescent_slime": {"quantity": 2, "value": 10}},
        "exits": {
            "east": {"target": "abyssal_ruins_entrance", "type": "direction"},
            "north": {"target": "abyssal_ruins_grand_hall", "type": "direction"}
        }
    }

    rooms["abyssal_ruins_grand_hall"] = {
        "id": "abyssal_ruins_grand_hall",
        "name": "Grand Hall of the Ancients",
        "description": "A hall of staggering proportions with pillars carved from single pieces of deep-sea "
                       "basalt. The ceiling vanishes into darkness above, and the floor is a mosaic depicting "
                       "creatures that make your mind ache to comprehend. Sound behaves strangely — your "
                       "footsteps echo before you take them.",
        "coordinates": [cx - 4, cy - 3],
        "location_type": "wilderness",
        "items": {"ancient_mosaic_tile": {"quantity": 1, "value": 25}, "basalt_pillar_fragment": {"quantity": 1, "value": 18}},
        "exits": {
            "south": {"target": "abyssal_ruins_passage", "type": "direction"},
            "east": {"target": "abyssal_ruins_mural_chamber", "type": "direction"},
            "west": {"target": "abyssal_ruins_library", "type": "direction"},
            "north": {"target": "abyssal_ruins_cyclopean_stair", "type": "direction"}
        }
    }

    rooms["abyssal_ruins_mural_chamber"] = {
        "id": "abyssal_ruins_mural_chamber",
        "name": "Chamber of Alien Murals",
        "description": "The walls are covered floor-to-ceiling with murals painted in pigments that glow "
                       "with their own light. They depict the history of a civilisation that thrived beneath "
                       "the ocean millions of years before humanity — their rise, their communion with things "
                       "from between the stars, and their terrible transformation.",
        "coordinates": [cx - 3, cy - 3],
        "location_type": "wilderness",
        "items": {"glowing_pigment_vial": {"quantity": 1, "value": 30}, "mural_rubbing": {"quantity": 1, "value": 22}},
        "exits": {
            "west": {"target": "abyssal_ruins_grand_hall", "type": "direction"},
            "south": {"target": "abyssal_ruins_entrance", "type": "direction"},
            "north": {"target": "abyssal_ruins_collapsed_wing", "type": "direction"}
        }
    }

    rooms["abyssal_ruins_collapsed_wing"] = {
        "id": "abyssal_ruins_collapsed_wing",
        "name": "Collapsed Wing",
        "description": "A section of the ruins where reality has partially given way. Walls phase between "
                       "solid and transparent, revealing impossible spaces beyond — rooms stacked inside "
                       "rooms, corridors that loop on themselves, and chambers where direction has no meaning.",
        "coordinates": [cx - 3, cy - 2],
        "location_type": "wilderness",
        "items": {"phase_shifted_brick": {"quantity": 1, "value": 32}},
        "exits": {
            "south": {"target": "abyssal_ruins_mural_chamber", "type": "direction"},
            "west": {"target": "abyssal_ruins_cyclopean_stair", "type": "direction"}
        }
    }

    rooms["abyssal_ruins_cyclopean_stair"] = {
        "id": "abyssal_ruins_cyclopean_stair",
        "name": "Cyclopean Stairway",
        "description": "A staircase built for beings three times your height, each step carved from a "
                       "single block of green-black stone. The stairs ascend and descend simultaneously "
                       "depending on which direction you look. Gravity is a suggestion here, not a law.",
        "coordinates": [cx - 4, cy - 2],
        "location_type": "wilderness",
        "items": {"non_euclidean_compass": {"quantity": 1, "value": 38}},
        "exits": {
            "south": {"target": "abyssal_ruins_grand_hall", "type": "direction"},
            "east": {"target": "abyssal_ruins_collapsed_wing", "type": "direction"},
            "west": {"target": "abyssal_ruins_observatory", "type": "direction"},
            "north": {"target": "abyssal_ruins_throne_room", "type": "direction"}
        }
    }

    rooms["abyssal_ruins_library"] = {
        "id": "abyssal_ruins_library",
        "name": "Drowned Library",
        "description": "Shelves of waterlogged tomes stretch into the gloom, their pages made from pressed "
                       "kelp and inked in squid-black fluid. Some books open themselves as you pass, displaying "
                       "diagrams of anatomies that have no earthly analogue. The knowledge here predates stone.",
        "coordinates": [cx - 5, cy - 3],
        "location_type": "wilderness",
        "items": {"elder_tome_fragment": {"quantity": 1, "value": 42}, "kelp_page_scroll": {"quantity": 2, "value": 16}},
        "exits": {
            "east": {"target": "abyssal_ruins_grand_hall", "type": "direction"},
            "north": {"target": "abyssal_ruins_observatory", "type": "direction"}
        }
    }

    rooms["abyssal_ruins_observatory"] = {
        "id": "abyssal_ruins_observatory",
        "name": "Abyssal Observatory",
        "description": "A domed chamber whose ceiling is a lens of polished crystal, focusing the light of "
                       "stars that don't exist in our sky. The ancient ones charted routes between worlds from "
                       "this room. Brass instruments of alien design still track celestial bodies you cannot see.",
        "coordinates": [cx - 5, cy - 2],
        "location_type": "wilderness",
        "items": {"star_lens_fragment": {"quantity": 1, "value": 48}, "alien_astrolabe": {"quantity": 1, "value": 55}},
        "exits": {
            "south": {"target": "abyssal_ruins_library", "type": "direction"},
            "east": {"target": "abyssal_ruins_cyclopean_stair", "type": "direction"},
            "north": {"target": "abyssal_ruins_temple", "type": "direction"}
        }
    }

    rooms["abyssal_ruins_temple"] = {
        "id": "abyssal_ruins_temple",
        "name": "Sunken Temple",
        "description": "A temple whose altar is a living coral formation that pulses with bioluminescence. "
                       "The walls depict worship of something vast coiled in the deepest trench — not a god "
                       "exactly, but something older. Offerings of gold and bone are fused into the altar's "
                       "surface, absorbed over millennia.",
        "coordinates": [cx - 5, cy - 1],
        "location_type": "wilderness",
        "items": {"coral_altar_fragment": {"quantity": 1, "value": 36}, "fused_offering_gold": {"quantity": 1, "value": 28}},
        "exits": {
            "south": {"target": "abyssal_ruins_observatory", "type": "direction"},
            "east": {"target": "abyssal_ruins_throne_room", "type": "direction"}
        }
    }

    rooms["abyssal_ruins_throne_room"] = {
        "id": "abyssal_ruins_throne_room",
        "name": "Throne of the Drowned King",
        "description": "A vast chamber dominated by a throne carved from a single nautilus shell the size "
                       "of a house. Something sits on it — not alive, not dead, but preserved in a state "
                       "between. Its crown is made of living barnacles that click and whisper in a language "
                       "that was old when the continents were one.",
        "coordinates": [cx - 4, cy - 1],
        "location_type": "wilderness",
        "items": {"drowned_king_barnacle": {"quantity": 1, "value": 52}, "nautilus_throne_chip": {"quantity": 1, "value": 34}},
        "exits": {
            "south": {"target": "abyssal_ruins_cyclopean_stair", "type": "direction"},
            "west": {"target": "abyssal_ruins_temple", "type": "direction"},
            "east": {"target": "abyssal_ruins_archive", "type": "direction"},
            "north": {"target": "abyssal_ruins_obelisk_chamber", "type": "direction"}
        }
    }

    rooms["abyssal_ruins_archive"] = {
        "id": "abyssal_ruins_archive",
        "name": "Archive of Sunken Memory",
        "description": "Crystal spheres the size of skulls line alcoves in the walls, each containing a "
                       "preserved memory from the ancient civilisation. Touch one and you experience fragments "
                       "of alien sensation — swimming through pressure that would crush steel, singing in "
                       "frequencies that shatter stone, seeing in spectrums beyond light.",
        "coordinates": [cx - 3, cy - 1],
        "location_type": "wilderness",
        "items": {"memory_sphere": {"quantity": 1, "value": 58}, "archive_crystal_dust": {"quantity": 2, "value": 12}},
        "exits": {
            "west": {"target": "abyssal_ruins_throne_room", "type": "direction"},
            "east": {"target": "abyssal_ruins_memory_well", "type": "direction"}
        }
    }

    rooms["abyssal_ruins_obelisk_chamber"] = {
        "id": "abyssal_ruins_obelisk_chamber",
        "name": "Chamber of the Black Obelisk",
        "description": "At the heart of the ruins stands a featureless black obelisk that absorbs all light. "
                       "It hums at a frequency that makes your vision blur and your thoughts fragment. Those "
                       "who study it too long begin to understand things they shouldn't — and can never forget.",
        "coordinates": [cx - 4, cy],
        "location_type": "wilderness",
        "items": {"obelisk_resonance_stone": {"quantity": 1, "value": 62}},
        "exits": {
            "south": {"target": "abyssal_ruins_throne_room", "type": "direction"},
            "north": {"target": "abyssal_ruins_void_altar", "type": "direction"}
        }
    }

    # --- Pressure Depths (10 rooms) ---

    rooms["abyssal_depths_descent"] = {
        "id": "abyssal_depths_descent",
        "name": "The Descent",
        "description": "A spiralling passage bored through living rock descends into the ocean floor itself. "
                       "Ancient enchantments maintain a bubble of breathable air, though the pressure makes "
                       "your ears ring. Bioluminescent organisms cling to the walls, lighting the way in "
                       "sickly blue-green.",
        "coordinates": [cx, cy - 3],
        "location_type": "wilderness",
        "items": {"pressure_crystal": {"quantity": 1, "value": 20}},
        "exits": {
            "south": {"target": "abyssal_outpost_war_room", "type": "direction"},
            "north": {"target": "abyssal_depths_crushing_corridor", "type": "direction"}
        }
    }

    rooms["abyssal_depths_crushing_corridor"] = {
        "id": "abyssal_depths_crushing_corridor",
        "name": "Crushing Corridor",
        "description": "The weight of the ocean above presses down with tangible force. The ancient wards "
                       "that keep the water at bay flicker visibly, and in those moments you can feel the "
                       "full crushing pressure of the abyss. The corridor walls are scored with claw marks "
                       "from things that came up from below.",
        "coordinates": [cx, cy - 2],
        "location_type": "wilderness",
        "items": {"pressure_ward_rune": {"quantity": 1, "value": 28}},
        "exits": {
            "south": {"target": "abyssal_depths_descent", "type": "direction"},
            "north": {"target": "abyssal_depths_crystal_cave", "type": "direction"},
            "west": {"target": "abyssal_depths_bioluminescent_grove", "type": "direction"},
            "east": {"target": "abyssal_depths_thermal_vent", "type": "direction"}
        }
    }

    rooms["abyssal_depths_bioluminescent_grove"] = {
        "id": "abyssal_depths_bioluminescent_grove",
        "name": "Bioluminescent Grove",
        "description": "A forest of giant tube worms and luminous kelp grows in the perpetual dark, creating "
                       "an otherworldly garden of pulsing blues, greens, and violets. Jellyfish the size of "
                       "carriages drift between the fronds, their translucent bodies revealing organs that "
                       "glow like trapped stars.",
        "coordinates": [cx - 1, cy - 2],
        "location_type": "wilderness",
        "items": {"luminous_kelp_strand": {"quantity": 2, "value": 14}, "tube_worm_extract": {"quantity": 1, "value": 24}},
        "exits": {
            "east": {"target": "abyssal_depths_crushing_corridor", "type": "direction"}
        }
    }

    rooms["abyssal_depths_thermal_vent"] = {
        "id": "abyssal_depths_thermal_vent",
        "name": "Thermal Vent Field",
        "description": "Columns of superheated water blast upward from fissures in the ocean floor, creating "
                       "shimmering curtains of heat. Strange ecosystems thrive here — albino crabs with too "
                       "many eyes, worms that feed on pure minerals, and bacterial mats that glow like molten "
                       "copper. The heat is almost unbearable.",
        "coordinates": [cx + 1, cy - 2],
        "location_type": "wilderness",
        "items": {"thermal_vent_mineral": {"quantity": 2, "value": 18}, "heat_resistant_crab_shell": {"quantity": 1, "value": 22}},
        "exits": {
            "west": {"target": "abyssal_depths_crushing_corridor", "type": "direction"},
            "east": {"target": "abyssal_depths_magma_seep", "type": "direction"}
        }
    }

    rooms["abyssal_depths_crystal_cave"] = {
        "id": "abyssal_depths_crystal_cave",
        "name": "Abyssal Crystal Cave",
        "description": "A cavern studded with crystals that have grown for millions of years under crushing "
                       "pressure. They sing when disturbed — not a pleasant sound but a discordant wail that "
                       "resonates with something primal in your brain. Some crystals contain shadows of "
                       "creatures frozen mid-movement, trapped aeons ago.",
        "coordinates": [cx, cy - 1],
        "location_type": "wilderness",
        "items": {"pressure_grown_crystal": {"quantity": 1, "value": 45}, "shadow_trapped_gem": {"quantity": 1, "value": 55}},
        "exits": {
            "south": {"target": "abyssal_depths_crushing_corridor", "type": "direction"},
            "west": {"target": "abyssal_depths_leviathan_bones", "type": "direction"},
            "east": {"target": "abyssal_depths_abyssopelagic_plain", "type": "direction"},
            "north": {"target": "abyssal_depths_trenches", "type": "direction"}
        }
    }

    rooms["abyssal_depths_leviathan_bones"] = {
        "id": "abyssal_depths_leviathan_bones",
        "name": "Leviathan Boneyard",
        "description": "The skeletal remains of creatures so vast that individual ribs form archways you "
                       "could sail a ship through. These leviathans died before mammals existed, and their "
                       "bones have calcified into structures that smaller creatures now inhabit. The skull "
                       "of the largest still radiates a faint psychic pressure.",
        "coordinates": [cx - 1, cy - 1],
        "location_type": "wilderness",
        "items": {"leviathan_bone_shard": {"quantity": 1, "value": 48}, "calcified_marrow": {"quantity": 1, "value": 32}},
        "exits": {
            "east": {"target": "abyssal_depths_crystal_cave", "type": "direction"}
        }
    }

    rooms["abyssal_depths_abyssopelagic_plain"] = {
        "id": "abyssal_depths_abyssopelagic_plain",
        "name": "Abyssopelagic Plain",
        "description": "A vast flat expanse of deep-sea sediment that stretches to the limits of vision in "
                       "every direction. Nothing should live here, but pale shapes drift across the plain — "
                       "things that evolved in total darkness, with no eyes but far too many mouths. The "
                       "silence is so complete it becomes a sound of its own.",
        "coordinates": [cx + 1, cy - 1],
        "location_type": "wilderness",
        "items": {"deep_sediment_sample": {"quantity": 2, "value": 12}, "eyeless_predator_tooth": {"quantity": 1, "value": 28}},
        "exits": {
            "west": {"target": "abyssal_depths_crystal_cave", "type": "direction"}
        }
    }

    rooms["abyssal_depths_trenches"] = {
        "id": "abyssal_depths_trenches",
        "name": "The Sunless Trenches",
        "description": "Chasms so deep that light itself seems to die before reaching the bottom. The walls "
                       "are carved with symbols that predate the ruins above — older, more primal, and far "
                       "more disturbing. Something enormous moves in the deepest part of the trench, displaced "
                       "water surging upward in rhythmic pulses.",
        "coordinates": [cx, cy],
        "location_type": "wilderness",
        "items": {"trench_stone": {"quantity": 1, "value": 35}, "primordial_glyph_rubbing": {"quantity": 1, "value": 42}},
        "exits": {
            "south": {"target": "abyssal_depths_crystal_cave", "type": "direction"},
            "east": {"target": "abyssal_depths_hydrothermal_spire", "type": "direction"},
            "north": {"target": "abyssal_depths_void_chasm", "type": "direction"}
        }
    }

    rooms["abyssal_depths_hydrothermal_spire"] = {
        "id": "abyssal_depths_hydrothermal_spire",
        "name": "Hydrothermal Spire",
        "description": "A natural chimney of mineral deposits towers upward, spewing superheated water laced "
                       "with metals that don't appear on any periodic table. The spire is colonised by creatures "
                       "that feed on impossible chemistry — their shells shimmer with iridescent alloys that "
                       "no forge could replicate.",
        "coordinates": [cx + 1, cy],
        "location_type": "wilderness",
        "items": {"impossible_alloy_flake": {"quantity": 1, "value": 58}, "spire_mineral_cluster": {"quantity": 1, "value": 30}},
        "exits": {
            "west": {"target": "abyssal_depths_trenches", "type": "direction"},
            "east": {"target": "abyssal_depths_crystal_forest", "type": "direction"}
        }
    }

    rooms["abyssal_depths_void_chasm"] = {
        "id": "abyssal_depths_void_chasm",
        "name": "Void Chasm",
        "description": "The deepest point of the Reach — a chasm that doesn't end at rock but opens into "
                       "something else entirely. Looking down, you see not darkness but a faint light from "
                       "impossibly far below, as if another sky exists beneath the ocean floor. The air here "
                       "hums with the dreams of sleeping gods.",
        "coordinates": [cx, cy + 1],
        "location_type": "wilderness",
        "items": {"void_chasm_echo_stone": {"quantity": 1, "value": 65}},
        "exits": {
            "south": {"target": "abyssal_depths_trenches", "type": "direction"},
            "north": {"target": "abyssal_city_gate", "type": "direction"}
        }
    }

    # --- Madness Reef (10 rooms) ---

    rooms["abyssal_reef_entrance"] = {
        "id": "abyssal_reef_entrance",
        "name": "Madness Reef - Outer Edge",
        "description": "The coral here grows in patterns that defy biology — spirals within spirals, fractals "
                       "that hurt to trace, and formations that seem to spell out words in a language your "
                       "brain almost understands. A low buzzing fills the water, and your thoughts begin to "
                       "feel... crowded.",
        "coordinates": [cx + 3, cy - 4],
        "location_type": "wilderness",
        "items": {"fractal_coral_sample": {"quantity": 2, "value": 16}},
        "exits": {
            "west": {"target": "abyssal_outpost_lookout", "type": "direction"},
            "east": {"target": "abyssal_reef_whispering_coral", "type": "direction"},
            "south": {"target": "abyssal_reef_hallucination_pool", "type": "direction"}
        }
    }

    rooms["abyssal_reef_whispering_coral"] = {
        "id": "abyssal_reef_whispering_coral",
        "name": "Whispering Coral Fields",
        "description": "Fields of coral that produce sound — a constant murmur of voices speaking just below "
                       "the threshold of comprehension. The longer you listen, the more certain you become that "
                       "the voices are saying your name. Some explorers have sat here for days, listening, "
                       "until they forgot how to leave.",
        "coordinates": [cx + 4, cy - 4],
        "location_type": "wilderness",
        "items": {"whispering_coral_polyp": {"quantity": 1, "value": 28}, "echo_pearl": {"quantity": 1, "value": 35}},
        "exits": {
            "west": {"target": "abyssal_reef_entrance", "type": "direction"},
            "south": {"target": "abyssal_reef_mind_grotto", "type": "direction"},
            "east": {"target": "abyssal_reef_whisper_coral", "type": "direction"}
        }
    }

    rooms["abyssal_reef_hallucination_pool"] = {
        "id": "abyssal_reef_hallucination_pool",
        "name": "Hallucination Pool",
        "description": "A still pool of water that shows you things that aren't there — or perhaps things "
                       "that are there but normally invisible. Other versions of yourself stare back from "
                       "the surface, making different choices, wearing different scars. Not all of them "
                       "are alive.",
        "coordinates": [cx + 3, cy - 3],
        "location_type": "wilderness",
        "items": {"mirror_water_vial": {"quantity": 1, "value": 32}},
        "exits": {
            "north": {"target": "abyssal_reef_entrance", "type": "direction"},
            "east": {"target": "abyssal_reef_mind_grotto", "type": "direction"},
            "south": {"target": "abyssal_reef_singing_stones", "type": "direction"}
        }
    }

    rooms["abyssal_reef_mind_grotto"] = {
        "id": "abyssal_reef_mind_grotto",
        "name": "Mind-Warping Grotto",
        "description": "A cave where the walls are covered in a living organism that reacts to thought. "
                       "Think of fire and the walls glow red; think of fear and they sprout thorns. The "
                       "organism feeds on psychic energy, and the more you think, the hungrier it gets. "
                       "Veterans advise meditating on nothing.",
        "coordinates": [cx + 4, cy - 3],
        "location_type": "wilderness",
        "items": {"psychic_organism_sample": {"quantity": 1, "value": 40}, "thought_reactive_stone": {"quantity": 1, "value": 26}},
        "exits": {
            "north": {"target": "abyssal_reef_whispering_coral", "type": "direction"},
            "west": {"target": "abyssal_reef_hallucination_pool", "type": "direction"},
            "east": {"target": "abyssal_reef_spiral_formation", "type": "direction"},
            "south": {"target": "abyssal_reef_eye_cluster", "type": "direction"}
        }
    }

    rooms["abyssal_reef_spiral_formation"] = {
        "id": "abyssal_reef_spiral_formation",
        "name": "Spiral Formation",
        "description": "A massive coral structure grown in a perfect logarithmic spiral that extends hundreds "
                       "of feet in every direction. Walking along it gives you vertigo — not from height, but "
                       "from the growing certainty that the spiral continues inward forever and that something "
                       "waits at its impossible centre.",
        "coordinates": [cx + 5, cy - 3],
        "location_type": "wilderness",
        "items": {"spiral_core_fragment": {"quantity": 1, "value": 45}},
        "exits": {
            "west": {"target": "abyssal_reef_mind_grotto", "type": "direction"},
            "south": {"target": "abyssal_reef_mirror_cave", "type": "direction"}
        }
    }

    rooms["abyssal_reef_singing_stones"] = {
        "id": "abyssal_reef_singing_stones",
        "name": "Singing Stones",
        "description": "Formations of mineralised coral that resonate with the ocean currents, producing "
                       "an eerie, atonal music. The songs change with the tides and sometimes arrange "
                       "themselves into melodies that shouldn't be possible from random vibration. Those "
                       "who transcribe the music report it contains mathematical proofs.",
        "coordinates": [cx + 3, cy - 2],
        "location_type": "wilderness",
        "items": {"singing_stone_chip": {"quantity": 2, "value": 18}, "transcribed_reef_song": {"quantity": 1, "value": 34}},
        "exits": {
            "north": {"target": "abyssal_reef_hallucination_pool", "type": "direction"},
            "east": {"target": "abyssal_reef_eye_cluster", "type": "direction"}
        }
    }

    rooms["abyssal_reef_eye_cluster"] = {
        "id": "abyssal_reef_eye_cluster",
        "name": "Eye Cluster",
        "description": "A formation of bioluminescent polyps that have evolved to look exactly like eyes — "
                       "thousands of them, covering every surface, all tracking your movement in perfect "
                       "synchronisation. They blink in patterns that convey meaning, though understanding "
                       "that meaning costs something you can't quite identify.",
        "coordinates": [cx + 4, cy - 2],
        "location_type": "wilderness",
        "items": {"eye_polyp_specimen": {"quantity": 1, "value": 38}},
        "exits": {
            "north": {"target": "abyssal_reef_mind_grotto", "type": "direction"},
            "west": {"target": "abyssal_reef_singing_stones", "type": "direction"},
            "east": {"target": "abyssal_reef_mirror_cave", "type": "direction"},
            "south": {"target": "abyssal_reef_fractured_reality", "type": "direction"}
        }
    }

    rooms["abyssal_reef_mirror_cave"] = {
        "id": "abyssal_reef_mirror_cave",
        "name": "Mirror Cave",
        "description": "A cave whose walls are coated in a naturally occurring substance that reflects "
                       "perfectly — too perfectly. Your reflection moves independently, mimicking actions "
                       "you haven't taken yet. Sometimes it mouths words. Sometimes it points at things "
                       "behind you that aren't there when you turn around.",
        "coordinates": [cx + 5, cy - 2],
        "location_type": "wilderness",
        "items": {"mirror_substance_scraping": {"quantity": 1, "value": 42}},
        "exits": {
            "north": {"target": "abyssal_reef_spiral_formation", "type": "direction"},
            "west": {"target": "abyssal_reef_eye_cluster", "type": "direction"},
            "south": {"target": "abyssal_reef_madness_heart", "type": "direction"}
        }
    }

    rooms["abyssal_reef_fractured_reality"] = {
        "id": "abyssal_reef_fractured_reality",
        "name": "Fractured Reality Zone",
        "description": "A region where the boundary between what is real and what is imagined has worn "
                       "thin entirely. Objects exist in multiple states simultaneously — a rock that is "
                       "also a fish that is also a memory of rain. Your own hands look unfamiliar. The "
                       "reef here grows in geometries that have no names in any human language.",
        "coordinates": [cx + 4, cy - 1],
        "location_type": "wilderness",
        "items": {"reality_fragment": {"quantity": 1, "value": 55}, "probability_crystal": {"quantity": 1, "value": 48}},
        "exits": {
            "north": {"target": "abyssal_reef_eye_cluster", "type": "direction"},
            "east": {"target": "abyssal_reef_madness_heart", "type": "direction"}
        }
    }

    rooms["abyssal_reef_madness_heart"] = {
        "id": "abyssal_reef_madness_heart",
        "name": "Heart of Madness",
        "description": "The centre of the reef, where the whispers become screams and the fractals become "
                       "faces. A massive brain-shaped coral formation pulses with its own heartbeat, connected "
                       "to the entire reef by neural-like tendrils. This is not coral — it is a single vast "
                       "organism, and it has been dreaming for millennia. It is starting to wake up.",
        "coordinates": [cx + 5, cy - 1],
        "location_type": "wilderness",
        "items": {"madness_heart_resonator": {"quantity": 1, "value": 72}, "neural_coral_strand": {"quantity": 1, "value": 38}},
        "exits": {
            "north": {"target": "abyssal_reef_mirror_cave", "type": "direction"},
            "west": {"target": "abyssal_reef_fractured_reality", "type": "direction"},
            "south": {"target": "abyssal_reef_ancient_growth", "type": "direction"}
        }
    }

    # --- Deep One City (10 rooms) ---

    rooms["abyssal_city_gate"] = {
        "id": "abyssal_city_gate",
        "name": "Deep One City - Threshold Gate",
        "description": "An archway of living coral and fused bone marks the entrance to a city that should "
                       "not exist. The architecture is simultaneously organic and geometric — buildings that "
                       "grew rather than were built, streets that follow the logic of tide patterns rather "
                       "than human planning. Shapes move in the windows.",
        "coordinates": [cx, cy + 2],
        "location_type": "wilderness",
        "items": {},
        "exits": {
            "south": {"target": "abyssal_depths_void_chasm", "type": "direction"},
            "north": {"target": "abyssal_city_plaza", "type": "direction"}
        }
    }

    rooms["abyssal_city_plaza"] = {
        "id": "abyssal_city_plaza",
        "name": "Central Plaza of the Deep Ones",
        "description": "A vast open space paved with tiles of polished nautilus shell. At its centre stands "
                       "a fountain that flows upward, defying gravity, its water cycling through colours that "
                       "don't exist above the surface. The Deep Ones — fish-like humanoids with bulging eyes "
                       "and webbed claws — watch you from doorways with alien curiosity.",
        "coordinates": [cx, cy + 3],
        "location_type": "wilderness",
        "items": {"nautilus_tile": {"quantity": 2, "value": 16}, "inverted_fountain_water": {"quantity": 1, "value": 30}},
        "exits": {
            "south": {"target": "abyssal_city_gate", "type": "direction"},
            "east": {"target": "abyssal_city_market", "type": "direction"},
            "west": {"target": "abyssal_city_temple", "type": "direction"},
            "north": {"target": "abyssal_city_palace", "type": "direction"}
        }
    }

    rooms["abyssal_city_temple"] = {
        "id": "abyssal_city_temple",
        "name": "Temple of the Drowned God",
        "description": "A cathedral of coral and bone dedicated to something that sleeps in the deepest "
                       "trenches. The Deep Ones worship here in eerie unison, their croaking chants creating "
                       "harmonics that vibrate in your chest. The altar is a living mouth — offerings placed "
                       "upon it are slowly consumed.",
        "coordinates": [cx - 1, cy + 3],
        "location_type": "wilderness",
        "items": {"drowned_god_idol": {"quantity": 1, "value": 52}, "chant_inscription_tablet": {"quantity": 1, "value": 28}},
        "exits": {
            "east": {"target": "abyssal_city_plaza", "type": "direction"},
            "north": {"target": "abyssal_city_spawning_pools", "type": "direction"},
            "west": {"target": "abyssal_city_coral_library", "type": "direction"}
        }
    }

    rooms["abyssal_city_market"] = {
        "id": "abyssal_city_market",
        "name": "Deep One Bazaar",
        "description": "A market where the Deep Ones trade in materials unrecognisable to surface dwellers — "
                       "compressed darkness, bottled pressure, crystallised sonar, and cuts of meat from "
                       "creatures that have never seen light. They accept gold, though they seem more "
                       "interested in trading for memories and dreams.",
        "coordinates": [cx + 1, cy + 3],
        "location_type": "wilderness",
        "items": {"compressed_darkness_vial": {"quantity": 1, "value": 44}, "crystallised_sonar": {"quantity": 1, "value": 36}},
        "exits": {
            "west": {"target": "abyssal_city_plaza", "type": "direction"},
            "north": {"target": "abyssal_city_barracks", "type": "direction"},
            "east": {"target": "abyssal_city_deep_bazaar", "type": "direction"}
        }
    }

    rooms["abyssal_city_spawning_pools"] = {
        "id": "abyssal_city_spawning_pools",
        "name": "Spawning Pools",
        "description": "Terraced pools of warm, mineral-rich water where the Deep Ones reproduce. Eggs "
                       "the size of fists cluster on every surface, their translucent shells revealing "
                       "the developing creatures within — things that start as fish and gradually, "
                       "disturbingly, develop more humanoid features as they grow.",
        "coordinates": [cx - 1, cy + 4],
        "location_type": "wilderness",
        "items": {"deep_one_egg_casing": {"quantity": 2, "value": 20}, "spawning_pool_water": {"quantity": 1, "value": 15}},
        "exits": {
            "south": {"target": "abyssal_city_temple", "type": "direction"},
            "east": {"target": "abyssal_city_palace", "type": "direction"},
            "north": {"target": "abyssal_city_archives", "type": "direction"},
            "west": {"target": "abyssal_city_oracle", "type": "direction"}
        }
    }

    rooms["abyssal_city_palace"] = {
        "id": "abyssal_city_palace",
        "name": "Palace of the Elder Deep One",
        "description": "A structure of impossible beauty and wrongness — walls of living pearl that breathe, "
                       "floors of compressed bioluminescence, and ceilings that display the dreams of the "
                       "palace's inhabitants. The Elder Deep One is ancient beyond reckoning, its body more "
                       "coral than flesh, its mind a vast cold intelligence.",
        "coordinates": [cx, cy + 4],
        "location_type": "wilderness",
        "items": {"living_pearl_fragment": {"quantity": 1, "value": 62}, "elder_deep_one_scale": {"quantity": 1, "value": 48}},
        "exits": {
            "south": {"target": "abyssal_city_plaza", "type": "direction"},
            "west": {"target": "abyssal_city_spawning_pools", "type": "direction"},
            "east": {"target": "abyssal_city_barracks", "type": "direction"},
            "north": {"target": "abyssal_city_observation_dome", "type": "direction"}
        }
    }

    rooms["abyssal_city_barracks"] = {
        "id": "abyssal_city_barracks",
        "name": "Deep One Barracks",
        "description": "The military quarter of the Deep One city, where warrior-caste creatures rest in "
                       "water-filled alcoves between patrols. Their weapons are grown from hardened coral "
                       "and sharpened bone, and their armour is their own thickened skin, scarified in "
                       "patterns that denote rank and kills.",
        "coordinates": [cx + 1, cy + 4],
        "location_type": "wilderness",
        "items": {"deep_one_coral_blade": {"quantity": 1, "value": 42}, "bone_spur_dagger": {"quantity": 1, "value": 28}},
        "exits": {
            "south": {"target": "abyssal_city_market", "type": "direction"},
            "west": {"target": "abyssal_city_palace", "type": "direction"},
            "north": {"target": "abyssal_city_forge", "type": "direction"}
        }
    }

    rooms["abyssal_city_archives"] = {
        "id": "abyssal_city_archives",
        "name": "Deep One Archives",
        "description": "Records kept not in books but in living organisms — sea slugs whose colour patterns "
                       "encode information, anemones that replay sounds when touched, and jellyfish whose "
                       "bioluminescent displays show scenes from millennia past. The Deep Ones have never "
                       "forgotten anything. They remember the time before the sun.",
        "coordinates": [cx - 1, cy + 5],
        "location_type": "wilderness",
        "items": {"memory_sea_slug": {"quantity": 1, "value": 44}, "archive_anemone": {"quantity": 1, "value": 30}},
        "exits": {
            "south": {"target": "abyssal_city_spawning_pools", "type": "direction"},
            "east": {"target": "abyssal_city_observation_dome", "type": "direction"}
        }
    }

    rooms["abyssal_city_observation_dome"] = {
        "id": "abyssal_city_observation_dome",
        "name": "Observation Dome",
        "description": "A dome of transparent organic crystal at the city's highest point, offering a view "
                       "of the surrounding abyss. From here you can see the full extent of the Deep One city "
                       "sprawling below, and beyond it, the impossible geography of the Threshold — where "
                       "reality itself begins to dissolve into something alien and vast.",
        "coordinates": [cx, cy + 5],
        "location_type": "wilderness",
        "items": {"organic_crystal_lens": {"quantity": 1, "value": 50}},
        "exits": {
            "south": {"target": "abyssal_city_palace", "type": "direction"},
            "west": {"target": "abyssal_city_archives", "type": "direction"},
            "east": {"target": "abyssal_city_forge", "type": "direction"},
            "north": {"target": "abyssal_threshold_path", "type": "direction"}
        }
    }

    rooms["abyssal_city_forge"] = {
        "id": "abyssal_city_forge",
        "name": "Abyssal Forge",
        "description": "The Deep Ones forge weapons and tools using hydrothermal vents as furnaces and the "
                       "pressure of the ocean as their hammer. The resulting alloys are impossibly strong — "
                       "metal that flows like water but strikes like stone. The forge-master is the oldest "
                       "Deep One you've seen, its body more machine than organism.",
        "coordinates": [cx + 1, cy + 5],
        "location_type": "wilderness",
        "items": {"abyssal_alloy_ingot": {"quantity": 1, "value": 68}, "pressure_forged_blade": {"quantity": 1, "value": 72}},
        "exits": {
            "south": {"target": "abyssal_city_barracks", "type": "direction"},
            "west": {"target": "abyssal_city_observation_dome", "type": "direction"}
        }
    }

    # --- The Threshold (8 rooms) ---

    rooms["abyssal_threshold_path"] = {
        "id": "abyssal_threshold_path",
        "name": "Path to the Threshold",
        "description": "Beyond the Deep One city, the ocean floor slopes upward into a ridge of crystallised "
                       "void-matter. The water here is neither warm nor cold — it is absent of temperature "
                       "entirely. Your thoughts echo as if your skull has become a cathedral. Ahead, reality "
                       "visibly frays at the edges.",
        "coordinates": [cx, cy + 6],
        "location_type": "wilderness",
        "items": {"void_matter_crystal": {"quantity": 1, "value": 52}},
        "exits": {
            "south": {"target": "abyssal_city_observation_dome", "type": "direction"},
            "north": {"target": "abyssal_threshold_warped_stairs", "type": "direction"}
        }
    }

    rooms["abyssal_threshold_warped_stairs"] = {
        "id": "abyssal_threshold_warped_stairs",
        "name": "Warped Staircase",
        "description": "A staircase that exists in multiple dimensions simultaneously — each step is in a "
                       "slightly different version of reality, and climbing them gives you glimpses of worlds "
                       "layered on top of your own. Some steps lead up, some lead sideways through time, and "
                       "one step leads to a place that is only darkness and breathing.",
        "coordinates": [cx, cy + 7],
        "location_type": "wilderness",
        "items": {"dimensional_step_stone": {"quantity": 1, "value": 45}},
        "exits": {
            "south": {"target": "abyssal_threshold_path", "type": "direction"},
            "west": {"target": "abyssal_threshold_antechamber", "type": "direction"},
            "east": {"target": "abyssal_threshold_obelisk", "type": "direction"},
            "north": {"target": "abyssal_threshold_void_maw", "type": "direction"}
        }
    }

    rooms["abyssal_threshold_antechamber"] = {
        "id": "abyssal_threshold_antechamber",
        "name": "Antechamber of Unmaking",
        "description": "A room where objects lose their definitions. Walls become suggestions, floors become "
                       "opinions, and your own body feels like a theory rather than a fact. The architects of "
                       "this space understood that reality is just a consensus, and in this room, that "
                       "consensus has broken down.",
        "coordinates": [cx - 1, cy + 7],
        "location_type": "wilderness",
        "items": {"unmade_substance": {"quantity": 1, "value": 55}, "consensus_shard": {"quantity": 1, "value": 42}},
        "exits": {
            "east": {"target": "abyssal_threshold_warped_stairs", "type": "direction"},
            "north": {"target": "abyssal_threshold_altar", "type": "direction"},
            "west": {"target": "abyssal_threshold_mirror_hall", "type": "direction"}
        }
    }

    rooms["abyssal_threshold_obelisk"] = {
        "id": "abyssal_threshold_obelisk",
        "name": "Obelisk of the Outer Dark",
        "description": "A second black obelisk, twin to the one in the ruins but larger and more powerful. "
                       "This one doesn't just absorb light — it absorbs meaning. Words spoken near it lose "
                       "their definitions. Concepts unravel. Staring at it, you begin to forget what 'up' "
                       "means, what 'self' means, what 'is' means.",
        "coordinates": [cx + 1, cy + 7],
        "location_type": "wilderness",
        "items": {"outer_dark_resonance_shard": {"quantity": 1, "value": 68}},
        "exits": {
            "west": {"target": "abyssal_threshold_warped_stairs", "type": "direction"},
            "north": {"target": "abyssal_threshold_convergence", "type": "direction"},
            "east": {"target": "abyssal_threshold_probability_room", "type": "direction"}
        }
    }

    rooms["abyssal_threshold_void_maw"] = {
        "id": "abyssal_threshold_void_maw",
        "name": "The Void Maw",
        "description": "A chamber shaped like the inside of an enormous mouth — ridged with teeth-like "
                       "formations of crystallised void-stuff. The throat leads downward into nothing, "
                       "or perhaps everything. The boundary between the Reach and whatever lies beyond "
                       "is paper-thin here. You can feel it pressing against your sanity.",
        "coordinates": [cx, cy + 8],
        "location_type": "wilderness",
        "items": {"void_tooth_crystal": {"quantity": 1, "value": 60}},
        "exits": {
            "south": {"target": "abyssal_threshold_warped_stairs", "type": "direction"},
            "west": {"target": "abyssal_threshold_altar", "type": "direction"},
            "east": {"target": "abyssal_threshold_convergence", "type": "direction"},
            "north": {"target": "abyssal_threshold_gate", "type": "direction"}
        }
    }

    rooms["abyssal_threshold_altar"] = {
        "id": "abyssal_threshold_altar",
        "name": "Altar of Final Offering",
        "description": "An altar of fused bone and void-crystal where the ancients made their last offerings "
                       "before crossing the Threshold. The altar still functions — place something upon it and "
                       "it is unmade at the molecular level, its essence drawn into the beyond. Scratched into "
                       "its base: 'What is given cannot be ungiven.'",
        "coordinates": [cx - 1, cy + 8],
        "location_type": "wilderness",
        "items": {"altar_bone_fragment": {"quantity": 1, "value": 48}, "void_crystal_offering_bowl": {"quantity": 1, "value": 55}},
        "exits": {
            "south": {"target": "abyssal_threshold_antechamber", "type": "direction"},
            "east": {"target": "abyssal_threshold_void_maw", "type": "direction"},
            "west": {"target": "abyssal_threshold_eye_chamber", "type": "direction"}
        }
    }

    rooms["abyssal_threshold_convergence"] = {
        "id": "abyssal_threshold_convergence",
        "name": "Point of Convergence",
        "description": "A place where multiple realities overlap, creating a kaleidoscope of existence. "
                       "You can see echoes of yourself in other timelines — some triumphant, some broken, "
                       "some transformed into things that are no longer human. All paths lead here. All "
                       "paths lead away. The distinction has ceased to matter.",
        "coordinates": [cx + 1, cy + 8],
        "location_type": "wilderness",
        "items": {"convergence_prism": {"quantity": 1, "value": 65}, "timeline_echo_strand": {"quantity": 1, "value": 50}},
        "exits": {
            "south": {"target": "abyssal_threshold_obelisk", "type": "direction"},
            "west": {"target": "abyssal_threshold_void_maw", "type": "direction"},
            "east": {"target": "abyssal_threshold_screaming_passage", "type": "direction"}
        }
    }

    rooms["abyssal_threshold_gate"] = {
        "id": "abyssal_threshold_gate",
        "name": "The Gate Beyond",
        "description": "The end of reality as you understand it. A massive gateway of impossible geometry — "
                       "its frame curves in directions that don't exist in three-dimensional space. Beyond "
                       "it lies the Void Beyond, a place of cosmic horror and absolute power. The gate "
                       "breathes. The gate watches. The gate has been waiting for you specifically.",
        "coordinates": [cx, cy + 9],
        "location_type": "wilderness",
        "items": {"gate_fragment": {"quantity": 1, "value": 80}},
        "exits": {
            "south": {"target": "abyssal_threshold_void_maw", "type": "direction"},
            "west": {"target": "abyssal_threshold_null_zone", "type": "direction"},
            "east": {"target": "abyssal_threshold_anchor_point", "type": "direction"},
            "enter": {
                "target": "FIXED_DUNGEON",
                "type": "fixed_dungeon",
                "dungeon_id": "void_beyond",
                "transition_text": "You step through the gate. Reality screams, then falls silent.\nThe Void Beyond opens before you — an infinite expanse of darkness\npunctuated by the dreams of dead gods and the geometry of madness.\nYou are no longer in your world. You may never truly return..."
            }
        }
    }



    # === ABYSSAL REACH EXPANSION ===

    # --- Expanded Docks (+3 rooms) ---

    rooms["abyssal_docks_sunken_wharf"] = {
        "id": "abyssal_docks_sunken_wharf",
        "name": "Sunken Wharf",
        "description": "A partially submerged extension of the dock, its timbers waterlogged and "
                       "encrusted with bioluminescent barnacles. Crates of salvaged deep-sea "
                       "artifacts sit half-submerged in the dark water. The wharf sinks a little "
                       "deeper each year, as if the abyss is slowly swallowing it.",
        "coordinates": [cx + 2, cy - 7],
        "location_type": "dock",
        "items": {"bioluminescent_barnacle": {"quantity": 2, "value": 12}, "sunken_salvage": {"quantity": 1, "value": 22}},
        "exits": {
            "west": {"target": "abyssal_docks_cargo", "type": "direction"},
            "east": {"target": "abyssal_docks_diving_platform", "type": "direction"},
            "south": {"target": "abyssal_docks_bell_cage", "type": "direction"}
        }
    }

    rooms["abyssal_docks_diving_platform"] = {
        "id": "abyssal_docks_diving_platform",
        "name": "Deep Diving Platform",
        "description": "A reinforced platform from which divers descend into the abyss wearing "
                       "pressure suits of void-warded metal. Winch mechanisms and air pumps line "
                       "the edges, and a board lists divers who descended and never returned — "
                       "the list is disturbingly long.",
        "coordinates": [cx + 3, cy - 7],
        "location_type": "building",
        "items": {"pressure_suit_fragment": {"quantity": 1, "value": 30}, "diver_memorial_token": {"quantity": 1, "value": 15}},
        "exits": {
            "west": {"target": "abyssal_docks_sunken_wharf", "type": "direction"}
        }
    }

    rooms["abyssal_docks_bell_cage"] = {
        "id": "abyssal_docks_bell_cage",
        "name": "Diving Bell Cage",
        "description": "A storage area for the iron diving bells used to explore the deep. "
                       "Each bell is inscribed with protective runes and lined with void-ward "
                       "crystal. Some bells have returned crushed by impossible pressures. "
                       "Others came back empty, their occupants simply... gone.",
        "coordinates": [cx + 2, cy - 6],
        "location_type": "building",
        "items": {"void_ward_crystal": {"quantity": 1, "value": 35}, "crushed_bell_fragment": {"quantity": 1, "value": 18}},
        "exits": {
            "north": {"target": "abyssal_docks_sunken_wharf", "type": "direction"}
        }
    }

    # --- Expanded Shores (+4 rooms) ---

    rooms["abyssal_shores_void_beach"] = {
        "id": "abyssal_shores_void_beach",
        "name": "Void Beach",
        "description": "A stretch of black sand that seems to absorb all light. The sand is "
                       "warm despite no sun reaching this place, and objects placed on it slowly "
                       "sink as if the beach is alive. Strange tide patterns bring up artifacts "
                       "from civilizations that never existed on this world.",
        "coordinates": [cx - 5, cy - 7],
        "location_type": "wilderness",
        "items": {"void_sand": {"quantity": 1, "value": 15}, "impossible_artifact": {"quantity": 1, "value": 40}},
        "exits": {
            "east": {"target": "abyssal_shores_lighthouse", "type": "direction"},
            "south": {"target": "abyssal_shores_echo_cave", "type": "direction"}
        }
    }

    rooms["abyssal_shores_echo_cave"] = {
        "id": "abyssal_shores_echo_cave",
        "name": "Echo Cave",
        "description": "A cave where sounds arrive before they're made — you hear your own "
                       "footsteps a moment before you take them. The temporal distortion is "
                       "mild here but deeply disorienting. Researchers have measured the time "
                       "displacement at exactly 2.7 seconds.",
        "coordinates": [cx - 5, cy - 6],
        "location_type": "wilderness",
        "items": {"temporal_echo_crystal": {"quantity": 1, "value": 35}, "time_displaced_shell": {"quantity": 1, "value": 20}},
        "exits": {
            "north": {"target": "abyssal_shores_void_beach", "type": "direction"}
        }
    }

    rooms["abyssal_shores_rift_pool"] = {
        "id": "abyssal_shores_rift_pool",
        "name": "Reality Rift Pool",
        "description": "A tide pool that opens into a rift in reality itself. The water "
                       "sometimes shows reflections of alien skies with multiple moons. "
                       "Objects dropped in occasionally come back changed — coins return "
                       "bearing the faces of unknown rulers.",
        "coordinates": [cx - 3, cy - 8],
        "location_type": "wilderness",
        "items": {"rift_water": {"quantity": 1, "value": 30}, "altered_coin": {"quantity": 1, "value": 25}},
        "exits": {
            "east": {"target": "abyssal_shores_anomaly", "type": "direction"},
            "west": {"target": "abyssal_shores_tentacle_grotto", "type": "direction"}
        }
    }

    rooms["abyssal_shores_tentacle_grotto"] = {
        "id": "abyssal_shores_tentacle_grotto",
        "name": "Tentacle Grotto",
        "description": "A sea cave where enormous tentacles — each thicker than a man — "
                       "slowly wave from crevices in the rock. They seem passive, merely "
                       "feeling the water currents, but their sheer size implies a creature "
                       "of terrifying proportions hidden in the rock.",
        "coordinates": [cx - 4, cy - 8],
        "location_type": "wilderness",
        "items": {"tentacle_sucker": {"quantity": 1, "value": 20}, "grotto_mucus_sample": {"quantity": 1, "value": 12}},
        "exits": {
            "east": {"target": "abyssal_shores_rift_pool", "type": "direction"}
        }
    }

    # --- Expanded Outpost (+6 rooms) ---

    rooms["abyssal_outpost_vault"] = {
        "id": "abyssal_outpost_vault",
        "name": "Containment Vault",
        "description": "A heavily warded chamber where artifacts too dangerous to handle are "
                       "stored. Three layers of void-ward crystal separate each shelf, and "
                       "warning glyphs pulse red whenever the contained objects attempt to "
                       "exert their influence. Some items visibly strain against their bonds.",
        "coordinates": [cx + 3, cy - 5],
        "location_type": "building",
        "items": {"containment_crystal": {"quantity": 1, "value": 40}, "warning_glyph_stone": {"quantity": 1, "value": 22}},
        "exits": {
            "west": {"target": "abyssal_outpost_armory", "type": "direction"},
            "north": {"target": "abyssal_outpost_quarantine", "type": "direction"}
        }
    }

    rooms["abyssal_outpost_quarantine"] = {
        "id": "abyssal_outpost_quarantine",
        "name": "Quarantine Chamber",
        "description": "Where returners from deep expeditions are held until cleared of "
                       "eldritch contamination. The chamber is lined with mirror-bright metal "
                       "that reveals any otherworldly taint. Some occupants have been here for "
                       "months, their contamination stubbornly refusing to fade.",
        "coordinates": [cx + 3, cy - 6],
        "location_type": "building",
        "items": {"quarantine_mirror_shard": {"quantity": 1, "value": 25}, "contamination_test_kit": {"quantity": 1, "value": 15}},
        "exits": {
            "south": {"target": "abyssal_outpost_vault", "type": "direction"}
        }
    }

    rooms["abyssal_outpost_observation"] = {
        "id": "abyssal_outpost_observation",
        "name": "Abyss Observation Post",
        "description": "A reinforced chamber with a single window of void-warded glass looking "
                       "directly into the abyss. The view shows nothing but darkness — yet "
                       "observers report seeing movement, patterns, and once, unmistakably, "
                       "an eye that looked back.",
        "coordinates": [cx + 2, cy - 3],
        "location_type": "building",
        "items": {"void_glass_shard": {"quantity": 1, "value": 35}, "observation_log": {"quantity": 1, "value": 18}},
        "exits": {
            "west": {"target": "abyssal_outpost_commander", "type": "direction"},
            "south": {"target": "abyssal_outpost_signal_tower", "type": "direction"}
        }
    }

    rooms["abyssal_outpost_signal_tower"] = {
        "id": "abyssal_outpost_signal_tower",
        "name": "Darklight Signal Tower",
        "description": "A tower equipped with darklight — inverse light that illuminates the "
                       "void without attracting the things that dwell in it. The darklight "
                       "signal can be seen from other outposts, enabling communication across "
                       "the abyss. The operator works in absolute silence.",
        "coordinates": [cx + 2, cy - 2],
        "location_type": "building",
        "items": {"darklight_emitter": {"quantity": 1, "value": 30}, "signal_code_book": {"quantity": 1, "value": 18}},
        "exits": {
            "north": {"target": "abyssal_outpost_observation", "type": "direction"}
        }
    }

    rooms["abyssal_outpost_ritual_circle"] = {
        "id": "abyssal_outpost_ritual_circle",
        "name": "Warding Ritual Circle",
        "description": "A permanent ritual circle where the outpost's protective wards are "
                       "maintained through daily ceremonies. Silver channels in the floor "
                       "carry sanctified oil in complex patterns. If the rituals stop for even "
                       "a day, the wards begin to weaken and things start to notice.",
        "coordinates": [cx - 3, cy - 5],
        "location_type": "building",
        "items": {"sanctified_oil": {"quantity": 1, "value": 22}, "ritual_circle_silver": {"quantity": 1, "value": 30}},
        "exits": {
            "east": {"target": "abyssal_outpost_shrine", "type": "direction"},
            "west": {"target": "abyssal_outpost_meditation", "type": "direction"}
        }
    }

    rooms["abyssal_outpost_meditation"] = {
        "id": "abyssal_outpost_meditation",
        "name": "Mind Ward Chamber",
        "description": "A chamber specifically designed to shield minds from the abyss's "
                       "corrosive influence. The walls are lined with lead and psychic "
                       "dampening crystals. Residents are required to spend one hour daily "
                       "here to maintain their sanity. Some spend much longer.",
        "coordinates": [cx - 4, cy - 5],
        "location_type": "building",
        "items": {"psychic_dampener": {"quantity": 1, "value": 35}, "sanity_anchor_stone": {"quantity": 1, "value": 28}},
        "exits": {
            "east": {"target": "abyssal_outpost_ritual_circle", "type": "direction"}
        }
    }

    # --- Expanded Sunken Ruins (+6 rooms) ---

    rooms["abyssal_ruins_void_altar"] = {
        "id": "abyssal_ruins_void_altar",
        "name": "Void Altar",
        "description": "An altar of black stone that seems to drink light. Above it, space "
                       "itself is torn — a permanent window into the void between worlds. "
                       "The tear pulses with alien colours that have no name in any human "
                       "language. Standing near it brings visions of impossible geometries.",
        "coordinates": [cx - 4, cy + 1],
        "location_type": "wilderness",
        "items": {"void_altar_fragment": {"quantity": 1, "value": 55}, "nameless_colour_crystal": {"quantity": 1, "value": 40}},
        "exits": {
            "south": {"target": "abyssal_ruins_obelisk_chamber", "type": "direction"},
            "east": {"target": "abyssal_ruins_processional", "type": "direction"}
        }
    }

    rooms["abyssal_ruins_processional"] = {
        "id": "abyssal_ruins_processional",
        "name": "Processional Way",
        "description": "A wide corridor lined with statues of robed figures processing toward "
                       "the void altar. Each statue is slightly different from the last — more "
                       "elongated, more alien — as if depicting a transformation. The final "
                       "statue barely resembles anything human.",
        "coordinates": [cx - 3, cy + 1],
        "location_type": "wilderness",
        "items": {"transformation_statue_chip": {"quantity": 1, "value": 25}, "processional_tile": {"quantity": 1, "value": 12}},
        "exits": {
            "west": {"target": "abyssal_ruins_void_altar", "type": "direction"},
            "east": {"target": "abyssal_ruins_resonance_hall", "type": "direction"}
        }
    }

    rooms["abyssal_ruins_resonance_hall"] = {
        "id": "abyssal_ruins_resonance_hall",
        "name": "Resonance Hall",
        "description": "A domed chamber where sounds create visible ripples in reality. "
                       "Speaking certain words — inscribed on the walls in an alien script — "
                       "causes the ripples to solidify into brief glimpses of other dimensions. "
                       "The effect is addictive and deeply dangerous.",
        "coordinates": [cx - 2, cy + 1],
        "location_type": "wilderness",
        "items": {"resonance_key_word": {"quantity": 1, "value": 35}, "solidified_ripple": {"quantity": 1, "value": 28}},
        "exits": {
            "west": {"target": "abyssal_ruins_processional", "type": "direction"}
        }
    }

    rooms["abyssal_ruins_memory_well"] = {
        "id": "abyssal_ruins_memory_well",
        "name": "Memory Well",
        "description": "A circular well that doesn't contain water but memories — the preserved "
                       "thoughts of the ruins' original inhabitants. Lowering a crystal into the "
                       "well fills it with alien perspectives and knowledge that the human mind "
                       "was never designed to contain.",
        "coordinates": [cx - 2, cy - 1],
        "location_type": "wilderness",
        "items": {"memory_crystal": {"quantity": 1, "value": 45}, "alien_perspective_shard": {"quantity": 1, "value": 30}},
        "exits": {
            "west": {"target": "abyssal_ruins_archive", "type": "direction"},
            "south": {"target": "abyssal_ruins_mosaic_floor", "type": "direction"}
        }
    }

    rooms["abyssal_ruins_mosaic_floor"] = {
        "id": "abyssal_ruins_mosaic_floor",
        "name": "Mosaic Floor Chamber",
        "description": "A chamber whose floor is an enormous mosaic depicting a map of "
                       "something — but not any geography that exists on this world. Cities "
                       "with impossible architecture, seas of colours that hurt to look at, "
                       "and a vast dark space at the center that might be the abyss itself.",
        "coordinates": [cx - 2, cy],
        "location_type": "wilderness",
        "items": {"mosaic_tile": {"quantity": 1, "value": 20}, "impossible_city_fragment": {"quantity": 1, "value": 35}},
        "exits": {
            "north": {"target": "abyssal_ruins_memory_well", "type": "direction"}
        }
    }

    rooms["abyssal_ruins_singing_pillars"] = {
        "id": "abyssal_ruins_singing_pillars",
        "name": "Singing Pillars",
        "description": "Twelve pillars of crystal that emit a continuous harmonic tone — a "
                       "frequency that can be felt in the bones. The tone changes when the "
                       "alignment of the abyss shifts, serving as an early warning system "
                       "for dimensional incursions. Currently, the tone is rising.",
        "coordinates": [cx - 5, cy],
        "location_type": "wilderness",
        "items": {"singing_pillar_shard": {"quantity": 1, "value": 30}, "harmonic_frequency_stone": {"quantity": 1, "value": 22}},
        "exits": {
            "east": {"target": "abyssal_ruins_obelisk_chamber", "type": "direction"}
        }
    }

    # --- Expanded Pressure Depths (+6 rooms) ---

    rooms["abyssal_depths_magma_seep"] = {
        "id": "abyssal_depths_magma_seep",
        "name": "Abyssal Magma Seep",
        "description": "Where volcanic magma meets the crushing depths, creating a surreal "
                       "landscape of solidified lava pillars and superheated water. The "
                       "temperature extremes support unique organisms — tube worms the size "
                       "of trees and crabs with carapaces of living metal.",
        "coordinates": [cx + 2, cy - 1],
        "location_type": "wilderness",
        "items": {"living_metal_crab_shell": {"quantity": 1, "value": 40}, "magma_seep_crystal": {"quantity": 1, "value": 25}},
        "exits": {
            "west": {"target": "abyssal_depths_thermal_vent", "type": "direction"},
            "east": {"target": "abyssal_depths_chimney_forest", "type": "direction"}
        }
    }

    rooms["abyssal_depths_chimney_forest"] = {
        "id": "abyssal_depths_chimney_forest",
        "name": "Black Smoker Forest",
        "description": "A forest of hydrothermal chimneys, each belching plumes of superheated "
                       "mineral-rich water into the abyss. The chimneys are encrusted with "
                       "strange metallic deposits and inhabited by organisms that feed on "
                       "chemicals instead of light. Life here is alien and ancient.",
        "coordinates": [cx + 3, cy - 1],
        "location_type": "wilderness",
        "items": {"black_smoker_mineral": {"quantity": 1, "value": 22}, "chemosynthetic_organism": {"quantity": 1, "value": 30}},
        "exits": {
            "west": {"target": "abyssal_depths_magma_seep", "type": "direction"}
        }
    }

    rooms["abyssal_depths_crystal_forest"] = {
        "id": "abyssal_depths_crystal_forest",
        "name": "Crystal Forest",
        "description": "Impossibly large crystals grow from the seafloor like trees, some "
                       "reaching fifty feet tall. They emit a low hum and glow with internal "
                       "light in shades of violet and ultraviolet. The crystals are not natural "
                       "— they're the dormant form of abyssal entities, dreaming in mineral.",
        "coordinates": [cx + 2, cy],
        "location_type": "wilderness",
        "items": {"dreaming_crystal": {"quantity": 1, "value": 50}, "crystal_hum_resonator": {"quantity": 1, "value": 30}},
        "exits": {
            "west": {"target": "abyssal_depths_hydrothermal_spire", "type": "direction"},
            "south": {"target": "abyssal_depths_living_reef", "type": "direction"},
            "east": {"target": "abyssal_depths_worm_tunnels", "type": "direction"}
        }
    }

    rooms["abyssal_depths_living_reef"] = {
        "id": "abyssal_depths_living_reef",
        "name": "Living Reef",
        "description": "Not coral but something else — a reef built from bio-metallic organisms "
                       "that are individually tiny but collectively form a structure of "
                       "staggering complexity. The reef communicates through bioluminescent "
                       "pulses, and it seems to be aware of visitors.",
        "coordinates": [cx + 2, cy + 1],
        "location_type": "wilderness",
        "items": {"bio_metallic_sample": {"quantity": 1, "value": 35}, "conscious_reef_pulse": {"quantity": 1, "value": 25}},
        "exits": {
            "north": {"target": "abyssal_depths_crystal_forest", "type": "direction"}
        }
    }

    rooms["abyssal_depths_worm_tunnels"] = {
        "id": "abyssal_depths_worm_tunnels",
        "name": "Abyssal Worm Tunnels",
        "description": "A network of tunnels bored through the rock by enormous abyssal worms. "
                       "The tunnel walls are smooth and lined with a hardened mucus that glows "
                       "faintly blue. Some tunnels are freshly carved; the worms are still "
                       "active somewhere in the rock.",
        "coordinates": [cx + 3, cy],
        "location_type": "wilderness",
        "items": {"worm_mucus_sample": {"quantity": 1, "value": 18}, "tunnel_bore_stone": {"quantity": 1, "value": 12}},
        "exits": {
            "west": {"target": "abyssal_depths_crystal_forest", "type": "direction"},
            "south": {"target": "abyssal_depths_pressure_chamber", "type": "direction"}
        }
    }

    rooms["abyssal_depths_pressure_chamber"] = {
        "id": "abyssal_depths_pressure_chamber",
        "name": "Extreme Pressure Chamber",
        "description": "A natural chamber at such extreme depth that the water pressure distorts "
                       "light itself. Objects appear warped and colours shift toward the ultraviolet. "
                       "Only specially warded individuals can survive here, and even they "
                       "report a crushing sensation in their minds.",
        "coordinates": [cx + 3, cy + 1],
        "location_type": "wilderness",
        "items": {"pressure_warped_metal": {"quantity": 1, "value": 35}, "deep_pressure_diamond": {"quantity": 1, "value": 50}},
        "exits": {
            "north": {"target": "abyssal_depths_worm_tunnels", "type": "direction"},
            "south": {"target": "abyssal_trench_entrance", "type": "direction"}
        }
    }

    # --- Expanded Madness Reef (+6 rooms) ---

    rooms["abyssal_reef_whisper_coral"] = {
        "id": "abyssal_reef_whisper_coral",
        "name": "Whisper Coral Formation",
        "description": "A coral formation that whispers — literally. Each polyp produces tiny "
                       "sounds that combine into comprehensible speech. The coral speaks in an "
                       "ancient language, repeating phrases that scholars believe are warnings: "
                       "'Do not listen. Do not remember. Do not look down.'",
        "coordinates": [cx + 6, cy - 4],
        "location_type": "wilderness",
        "items": {"whisper_coral_fragment": {"quantity": 1, "value": 35}, "warning_polyp": {"quantity": 1, "value": 20}},
        "exits": {
            "west": {"target": "abyssal_reef_whispering_coral", "type": "direction"},
            "south": {"target": "abyssal_reef_bioluminescent_hall", "type": "direction"}
        }
    }

    rooms["abyssal_reef_bioluminescent_hall"] = {
        "id": "abyssal_reef_bioluminescent_hall",
        "name": "Bioluminescent Hall",
        "description": "A passage through the reef illuminated by billions of bioluminescent "
                       "organisms, creating a display of shifting colours that rivals any "
                       "aurora. The light patterns seem to carry meaning — a visual language "
                       "that the reef's organisms use to communicate.",
        "coordinates": [cx + 6, cy - 3],
        "location_type": "wilderness",
        "items": {"bioluminescent_vial": {"quantity": 1, "value": 18}, "visual_language_sample": {"quantity": 1, "value": 25}},
        "exits": {
            "north": {"target": "abyssal_reef_whisper_coral", "type": "direction"},
            "south": {"target": "abyssal_reef_symbiont_cave", "type": "direction"}
        }
    }

    rooms["abyssal_reef_symbiont_cave"] = {
        "id": "abyssal_reef_symbiont_cave",
        "name": "Symbiont Cave",
        "description": "A cave inhabited by organisms that bond with visitors, creating temporary "
                       "symbiotic relationships. The symbionts are small, translucent creatures "
                       "that attach to skin and grant enhanced perception of the abyss — at the "
                       "cost of sharing their host's memories.",
        "coordinates": [cx + 6, cy - 2],
        "location_type": "wilderness",
        "items": {"symbiont_creature": {"quantity": 1, "value": 35}, "memory_share_crystal": {"quantity": 1, "value": 28}},
        "exits": {
            "north": {"target": "abyssal_reef_bioluminescent_hall", "type": "direction"},
            "south": {"target": "abyssal_reef_gravity_pool", "type": "direction"}
        }
    }

    rooms["abyssal_reef_gravity_pool"] = {
        "id": "abyssal_reef_gravity_pool",
        "name": "Inverted Gravity Pool",
        "description": "A section of the reef where gravity is inverted — water falls upward "
                       "and objects placed in the pool float to the ceiling. The phenomenon "
                       "is caused by a dimensional weak point, and the boundary between normal "
                       "and inverted gravity is dangerously unstable.",
        "coordinates": [cx + 6, cy - 1],
        "location_type": "wilderness",
        "items": {"gravity_stone": {"quantity": 1, "value": 40}, "inverted_water_vial": {"quantity": 1, "value": 22}},
        "exits": {
            "north": {"target": "abyssal_reef_symbiont_cave", "type": "direction"},
            "south": {"target": "abyssal_reef_predator_zone", "type": "direction"}
        }
    }

    rooms["abyssal_reef_predator_zone"] = {
        "id": "abyssal_reef_predator_zone",
        "name": "Predator Zone",
        "description": "An area of the reef dominated by apex predators — creatures adapted "
                       "to the abyss's extreme conditions. Glass-jawed fish with teeth like "
                       "needles, cephalopods that change not just colour but shape, and "
                       "something large that is only ever glimpsed at the edge of light.",
        "coordinates": [cx + 6, cy],
        "location_type": "wilderness",
        "items": {"predator_tooth": {"quantity": 1, "value": 25}, "shape_changing_ink": {"quantity": 1, "value": 30}},
        "exits": {
            "north": {"target": "abyssal_reef_gravity_pool", "type": "direction"},
            "west": {"target": "abyssal_reef_ancient_growth", "type": "direction"}
        }
    }

    rooms["abyssal_reef_ancient_growth"] = {
        "id": "abyssal_reef_ancient_growth",
        "name": "Ancient Growth",
        "description": "The oldest section of the reef — organisms here have been growing "
                       "continuously for millions of years. The structures are impossibly "
                       "complex, fractal patterns repeating at every scale. Scientists believe "
                       "the reef may be a single organism of planet-spanning intelligence.",
        "coordinates": [cx + 5, cy],
        "location_type": "wilderness",
        "items": {"ancient_growth_core": {"quantity": 1, "value": 50}, "fractal_shell": {"quantity": 1, "value": 30}},
        "exits": {
            "east": {"target": "abyssal_reef_predator_zone", "type": "direction"},
            "north": {"target": "abyssal_reef_madness_heart", "type": "direction"}
        }
    }

    # --- Expanded Deep One City (+6 rooms) ---

    rooms["abyssal_city_deep_bazaar"] = {
        "id": "abyssal_city_deep_bazaar",
        "name": "Deep One Bazaar",
        "description": "A market square in the alien city where Deep Ones trade goods from "
                       "the abyss and the surface. Stalls display impossible wares — living "
                       "jewellery, whispering shells, and bottled memories. The currency is "
                       "not gold but secrets whispered into specially prepared crystals.",
        "coordinates": [cx + 2, cy + 3],
        "location_type": "settlement",
        "items": {"living_jewel": {"quantity": 1, "value": 45}, "bottled_memory": {"quantity": 1, "value": 35}},
        "exits": {
            "west": {"target": "abyssal_city_market", "type": "direction"},
            "south": {"target": "abyssal_city_breeding_chamber", "type": "direction"}
        }
    }

    rooms["abyssal_city_breeding_chamber"] = {
        "id": "abyssal_city_breeding_chamber",
        "name": "Breeding Chamber",
        "description": "A vast chamber where Deep One larvae develop, tended by ancient brood "
                       "mothers. The larvae are translucent and disturbingly intelligent, "
                       "watching visitors with unblinking compound eyes. The pool water is "
                       "thick with nutrients and glows a sickly green.",
        "coordinates": [cx + 2, cy + 4],
        "location_type": "wilderness",
        "items": {"larvae_observation_notes": {"quantity": 1, "value": 15}, "brood_water_sample": {"quantity": 1, "value": 22}},
        "exits": {
            "north": {"target": "abyssal_city_deep_bazaar", "type": "direction"},
            "south": {"target": "abyssal_city_artifact_vault", "type": "direction"}
        }
    }

    rooms["abyssal_city_oracle"] = {
        "id": "abyssal_city_oracle",
        "name": "Oracle Chamber",
        "description": "The chamber of the Deep One Oracle — a being so old it has become "
                       "partially merged with the city's architecture. Its body stretches "
                       "through multiple rooms, but its consciousness is centred here. It "
                       "speaks in riddles that take decades to decipher.",
        "coordinates": [cx - 2, cy + 4],
        "location_type": "building",
        "items": {"oracle_riddle_stone": {"quantity": 1, "value": 50}, "merged_architecture_piece": {"quantity": 1, "value": 35}},
        "exits": {
            "east": {"target": "abyssal_city_spawning_pools", "type": "direction"},
            "south": {"target": "abyssal_city_dream_pool", "type": "direction"}
        }
    }

    rooms["abyssal_city_artifact_vault"] = {
        "id": "abyssal_city_artifact_vault",
        "name": "Artifact Vault",
        "description": "A secured vault where the Deep Ones store their most powerful and "
                       "dangerous artifacts. Each item is suspended in a sphere of solidified "
                       "void, accessible only through specific mental frequencies. The contents "
                       "represent millions of years of collection from across dimensions.",
        "coordinates": [cx + 2, cy + 5],
        "location_type": "building",
        "items": {"void_sphere_shard": {"quantity": 1, "value": 55}, "dimensional_artifact": {"quantity": 1, "value": 65}},
        "exits": {
            "north": {"target": "abyssal_city_breeding_chamber", "type": "direction"}
        }
    }

    rooms["abyssal_city_coral_library"] = {
        "id": "abyssal_city_coral_library",
        "name": "Coral Library",
        "description": "Knowledge stored not in books but in living coral formations. Each "
                       "branch contains a complete library, readable by touch through the "
                       "coral's bioelectric pulses. The library grows continually, adding "
                       "new knowledge absorbed from the thoughts of nearby minds.",
        "coordinates": [cx - 2, cy + 3],
        "location_type": "building",
        "items": {"knowledge_coral_branch": {"quantity": 1, "value": 40}, "bioelectric_reader": {"quantity": 1, "value": 25}},
        "exits": {
            "east": {"target": "abyssal_city_temple", "type": "direction"}
        }
    }

    rooms["abyssal_city_dream_pool"] = {
        "id": "abyssal_city_dream_pool",
        "name": "Communal Dream Pool",
        "description": "A pool where Deep Ones enter a shared dream state, their sleeping "
                       "minds networking into a hive consciousness. Visitors who enter the "
                       "pool experience fragments of this shared dream — alien memories, "
                       "cosmic vistas, and the overwhelming presence of something vast.",
        "coordinates": [cx - 2, cy + 5],
        "location_type": "wilderness",
        "items": {"dream_pool_water": {"quantity": 1, "value": 35}, "hive_mind_crystal": {"quantity": 1, "value": 45}},
        "exits": {
            "north": {"target": "abyssal_city_oracle", "type": "direction"}
        }
    }

    # --- Expanded Threshold (+6 rooms) ---

    rooms["abyssal_threshold_mirror_hall"] = {
        "id": "abyssal_threshold_mirror_hall",
        "name": "Mirror Hall",
        "description": "A corridor lined with mirrors that don't reflect this reality. Each "
                       "mirror shows a different dimension — some beautiful, some horrifying, "
                       "some too alien to comprehend. Occasionally, something in a mirror seems "
                       "to notice you looking.",
        "coordinates": [cx - 2, cy + 7],
        "location_type": "wilderness",
        "items": {"dimensional_mirror_shard": {"quantity": 1, "value": 45}, "alien_reflection": {"quantity": 1, "value": 30}},
        "exits": {
            "east": {"target": "abyssal_threshold_antechamber", "type": "direction"}
        }
    }

    rooms["abyssal_threshold_probability_room"] = {
        "id": "abyssal_threshold_probability_room",
        "name": "Probability Chamber",
        "description": "A room where probability itself breaks down. Coins land on their edge. "
                       "Dice show numbers that don't exist. Dropped objects sometimes fall up. "
                       "The laws of physics here are merely suggestions, and reality seems to "
                       "be choosing between multiple valid states at once.",
        "coordinates": [cx + 2, cy + 7],
        "location_type": "wilderness",
        "items": {"impossibility_coin": {"quantity": 1, "value": 40}, "probability_shard": {"quantity": 1, "value": 30}},
        "exits": {
            "west": {"target": "abyssal_threshold_obelisk", "type": "direction"}
        }
    }

    rooms["abyssal_threshold_null_zone"] = {
        "id": "abyssal_threshold_null_zone",
        "name": "Null Zone",
        "description": "A space where nothing exists — not darkness, not void, but the complete "
                       "absence of existence itself. You can feel the boundaries of reality "
                       "straining against the nothingness. It's said that the Threshold entity "
                       "sleeps somewhere beyond the null — or perhaps the null IS the entity.",
        "coordinates": [cx - 1, cy + 9],
        "location_type": "wilderness",
        "items": {"null_fragment": {"quantity": 1, "value": 60}, "existence_anchor": {"quantity": 1, "value": 45}},
        "exits": {
            "east": {"target": "abyssal_threshold_gate", "type": "direction"}
        }
    }

    rooms["abyssal_threshold_screaming_passage"] = {
        "id": "abyssal_threshold_screaming_passage",
        "name": "Screaming Passage",
        "description": "A passage where the fabric of reality is so thin that the sounds of "
                       "other dimensions bleed through. The result is a constant cacophony of "
                       "screams, whispers, music, and sounds that the human ear was never "
                       "designed to process. Sanity slips quickly here.",
        "coordinates": [cx + 2, cy + 8],
        "location_type": "wilderness",
        "items": {"dimensional_echo_crystal": {"quantity": 1, "value": 35}, "reality_fabric_thread": {"quantity": 1, "value": 28}},
        "exits": {
            "west": {"target": "abyssal_threshold_convergence", "type": "direction"}
        }
    }

    rooms["abyssal_threshold_eye_chamber"] = {
        "id": "abyssal_threshold_eye_chamber",
        "name": "Chamber of the Eye",
        "description": "A domed chamber with a ceiling that is, unmistakably, an enormous eye. "
                       "It blinks slowly — once every few minutes — and its gaze follows movement. "
                       "The eye belongs to something on the other side of the Threshold, watching "
                       "our reality with unknowable curiosity or hunger.",
        "coordinates": [cx - 2, cy + 8],
        "location_type": "wilderness",
        "items": {"eye_tear": {"quantity": 1, "value": 55}, "gaze_ward_stone": {"quantity": 1, "value": 40}},
        "exits": {
            "east": {"target": "abyssal_threshold_altar", "type": "direction"}
        }
    }

    rooms["abyssal_threshold_anchor_point"] = {
        "id": "abyssal_threshold_anchor_point",
        "name": "Reality Anchor Point",
        "description": "One of several anchor points that tether this section of reality to "
                       "the normal world. The anchor is a pillar of crystal driven deep into "
                       "bedrock, humming with stabilizing energy. If the anchors fail, this "
                       "entire area would slip through the Threshold into the beyond.",
        "coordinates": [cx + 1, cy + 9],
        "location_type": "wilderness",
        "items": {"anchor_crystal_chip": {"quantity": 1, "value": 48}, "stabilizing_rune": {"quantity": 1, "value": 32}},
        "exits": {
            "west": {"target": "abyssal_threshold_gate", "type": "direction"}
        }
    }

    # === NEW SUB-REGION: Abyssal Trenches (18 rooms) ===

    rooms["abyssal_trench_entrance"] = {
        "id": "abyssal_trench_entrance",
        "name": "Trench Entrance",
        "description": "The mouth of the deepest ocean trench on the Reach, plunging downward "
                       "into absolute darkness. The water here is as cold as it gets, and "
                       "the pressure would crush an unprotected body instantly. Void-ward "
                       "enchantments are mandatory beyond this point.",
        "coordinates": [cx + 3, cy + 2],
        "location_type": "wilderness",
        "items": {"trench_water_sample": {"quantity": 1, "value": 12}},
        "exits": {
            "north": {"target": "abyssal_depths_pressure_chamber", "type": "direction"},
            "east": {"target": "abyssal_trench_upper_shelf", "type": "direction"}
        }
    }

    rooms["abyssal_trench_upper_shelf"] = {
        "id": "abyssal_trench_upper_shelf",
        "name": "Upper Trench Shelf",
        "description": "A ledge partway down the trench wall where explorers rest before "
                       "descending further. Equipment caches are bolted to the rock, and "
                       "pressure gauges monitor the crushing environment. Bioluminescent "
                       "organisms drift past like stars in reverse.",
        "coordinates": [cx + 4, cy + 2],
        "location_type": "wilderness",
        "items": {"equipment_cache_tool": {"quantity": 1, "value": 18}, "pressure_gauge": {"quantity": 1, "value": 12}},
        "exits": {
            "west": {"target": "abyssal_trench_entrance", "type": "direction"},
            "south": {"target": "abyssal_trench_mid_descent", "type": "direction"},
            "east": {"target": "abyssal_trench_fossil_layer", "type": "direction"}
        }
    }

    rooms["abyssal_trench_mid_descent"] = {
        "id": "abyssal_trench_mid_descent",
        "name": "Mid-Trench Descent",
        "description": "Halfway down the trench, a point of no return for most expeditions. "
                       "The darkness is total without artificial light, and the cold penetrates "
                       "even the best warming enchantments. Strange clicking sounds echo from "
                       "below — something is aware of your presence.",
        "coordinates": [cx + 4, cy + 3],
        "location_type": "wilderness",
        "items": {"deep_darkness_vial": {"quantity": 1, "value": 20}, "warming_charm_fragment": {"quantity": 1, "value": 15}},
        "exits": {
            "north": {"target": "abyssal_trench_upper_shelf", "type": "direction"},
            "south": {"target": "abyssal_trench_narrow_passage", "type": "direction"},
            "west": {"target": "abyssal_trench_side_cave", "type": "direction"},
            "east": {"target": "abyssal_trench_bone_current", "type": "direction"}
        }
    }

    rooms["abyssal_trench_fossil_layer"] = {
        "id": "abyssal_trench_fossil_layer",
        "name": "Deep Fossil Layer",
        "description": "The trench wall here is embedded with fossils of creatures that predate "
                       "all known life — organisms from before the current age of the world. "
                       "Some fossils don't match any evolutionary tree. Others appear to be "
                       "technology, not biology, fossilized into stone.",
        "coordinates": [cx + 5, cy + 2],
        "location_type": "wilderness",
        "items": {"pre_world_fossil": {"quantity": 1, "value": 45}, "fossilized_technology": {"quantity": 1, "value": 55}},
        "exits": {
            "west": {"target": "abyssal_trench_upper_shelf", "type": "direction"}
        }
    }

    rooms["abyssal_trench_side_cave"] = {
        "id": "abyssal_trench_side_cave",
        "name": "Trench Side Cave",
        "description": "A cave carved into the trench wall by some unknown force. Inside, the "
                       "pressure is inexplicably lower, creating a habitable pocket. The cave "
                       "walls are inscribed with symbols that predate all known civilizations — "
                       "someone or something lived here, in the deep, long ago.",
        "coordinates": [cx + 3, cy + 3],
        "location_type": "wilderness",
        "items": {"ancient_inscription_rubbing": {"quantity": 1, "value": 30}, "pressure_pocket_stone": {"quantity": 1, "value": 20}},
        "exits": {
            "east": {"target": "abyssal_trench_mid_descent", "type": "direction"}
        }
    }

    rooms["abyssal_trench_narrow_passage"] = {
        "id": "abyssal_trench_narrow_passage",
        "name": "Narrowing Passage",
        "description": "The trench narrows dramatically here, the walls close enough to touch "
                       "on both sides. The rock is unusually warm and pulsates faintly — as if "
                       "you're passing through the throat of a living thing. The pulsation "
                       "matches a slow, steady heartbeat.",
        "coordinates": [cx + 4, cy + 4],
        "location_type": "wilderness",
        "items": {"pulsating_stone": {"quantity": 1, "value": 25}, "trench_narrow_crystal": {"quantity": 1, "value": 15}},
        "exits": {
            "north": {"target": "abyssal_trench_mid_descent", "type": "direction"},
            "south": {"target": "abyssal_trench_deep_shelf", "type": "direction"},
            "west": {"target": "abyssal_trench_pressure_gate", "type": "direction"}
        }
    }

    rooms["abyssal_trench_pressure_gate"] = {
        "id": "abyssal_trench_pressure_gate",
        "name": "Pressure Gate",
        "description": "A natural formation where opposing currents create a barrier of extreme "
                       "pressure. Passing through requires either immense physical fortitude or "
                       "specialized void-warding. The gate seems to filter — some things pass "
                       "through easily while others are crushed to powder.",
        "coordinates": [cx + 3, cy + 4],
        "location_type": "wilderness",
        "items": {"pressure_barrier_fragment": {"quantity": 1, "value": 35}, "gate_current_crystal": {"quantity": 1, "value": 20}},
        "exits": {
            "east": {"target": "abyssal_trench_narrow_passage", "type": "direction"}
        }
    }

    rooms["abyssal_trench_deep_shelf"] = {
        "id": "abyssal_trench_deep_shelf",
        "name": "Deep Trench Shelf",
        "description": "A wider ledge deep in the trench where the impossible becomes mundane. "
                       "Objects float without support. Light bends around corners. Time "
                       "occasionally stutters. At this depth, the boundary between the world "
                       "and the void beyond is paper-thin.",
        "coordinates": [cx + 5, cy + 4],
        "location_type": "wilderness",
        "items": {"reality_thin_crystal": {"quantity": 1, "value": 40}, "time_stutter_stone": {"quantity": 1, "value": 35}},
        "exits": {
            "north": {"target": "abyssal_trench_narrow_passage", "type": "direction"},
            "east": {"target": "abyssal_trench_leviathan_lair", "type": "direction"},
            "south": {"target": "abyssal_trench_bottom", "type": "direction"}
        }
    }

    rooms["abyssal_trench_leviathan_lair"] = {
        "id": "abyssal_trench_leviathan_lair",
        "name": "Leviathan's Lair",
        "description": "An enormous cavern in the trench wall, large enough to house a "
                       "creature of impossible size. Claw marks score the walls — each "
                       "gouge ten feet deep and fifty long. A warm current flows from "
                       "within, carrying a scent like ozone and ancient decay. The "
                       "leviathan is not here now. But it was, recently.",
        "coordinates": [cx + 6, cy + 4],
        "location_type": "wilderness",
        "items": {"leviathan_scale": {"quantity": 1, "value": 75}, "lair_detritus": {"quantity": 1, "value": 20}},
        "exits": {
            "west": {"target": "abyssal_trench_deep_shelf", "type": "direction"},
            "east": {"target": "abyssal_trench_crystallized_time", "type": "direction"}
        }
    }

    rooms["abyssal_trench_crystallized_time"] = {
        "id": "abyssal_trench_crystallized_time",
        "name": "Crystallized Time Pocket",
        "description": "A chamber where time itself has crystallized into solid form — amber-like "
                       "formations that contain frozen moments. Some crystals show ancient events: "
                       "the birth of the abyss, the arrival of the first Deep Ones, and something "
                       "vast and terrible that happened at the beginning of all things.",
        "coordinates": [cx + 7, cy + 4],
        "location_type": "wilderness",
        "items": {"crystallized_time": {"quantity": 1, "value": 80}, "frozen_moment": {"quantity": 1, "value": 55}},
        "exits": {
            "west": {"target": "abyssal_trench_leviathan_lair", "type": "direction"},
            "south": {"target": "abyssal_trench_abyssal_core", "type": "direction"},
            "north": {"target": "abyssal_wake_tidal_surge", "type": "direction"}
        }
    }

    rooms["abyssal_trench_bottom"] = {
        "id": "abyssal_trench_bottom",
        "name": "Trench Bottom",
        "description": "The absolute bottom of the deepest trench. The pressure is beyond "
                       "measurement, the darkness beyond total. Yet there is light here — "
                       "a faint, pulsing glow from something embedded in the trench floor. "
                       "Whatever it is, it's been here since before the world had a name.",
        "coordinates": [cx + 5, cy + 5],
        "location_type": "wilderness",
        "items": {"trench_floor_crystal": {"quantity": 1, "value": 80}, "primordial_sediment": {"quantity": 1, "value": 40}},
        "exits": {
            "north": {"target": "abyssal_trench_deep_shelf", "type": "direction"},
            "east": {"target": "abyssal_trench_origin_point", "type": "direction"},
            "west": {"target": "abyssal_trench_glowing_garden", "type": "direction"}
        }
    }

    rooms["abyssal_trench_origin_point"] = {
        "id": "abyssal_trench_origin_point",
        "name": "The Origin Point",
        "description": "At the deepest point of the trench, buried in sediment that has lain "
                       "undisturbed for aeons, is a perfect sphere of crystallized void. "
                       "Scholars theorize it's a seed — the nucleus from which the abyss grew. "
                       "Or perhaps it's a plug, holding back something far worse.",
        "coordinates": [cx + 6, cy + 5],
        "location_type": "wilderness",
        "items": {"crystallized_void_sphere": {"quantity": 1, "value": 100}, "origin_sediment": {"quantity": 1, "value": 50}},
        "exits": {
            "west": {"target": "abyssal_trench_bottom", "type": "direction"},
            "south": {"target": "abyssal_trench_deep_shrine", "type": "direction"}
        }
    }

    rooms["abyssal_trench_bone_current"] = {
        "id": "abyssal_trench_bone_current",
        "name": "Bone Current",
        "description": "An underwater current that carries bleached bones from somewhere "
                       "unknown. The bones belong to creatures of every imaginable species — "
                       "and some from no species known to science. They drift past in an "
                       "endless procession, a river of death flowing through the deep.",
        "coordinates": [cx + 5, cy + 3],
        "location_type": "wilderness",
        "items": {"unknown_species_bone": {"quantity": 1, "value": 30}, "bone_current_sample": {"quantity": 1, "value": 15}},
        "exits": {
            "west": {"target": "abyssal_trench_mid_descent", "type": "direction"},
            "east": {"target": "abyssal_trench_silence_zone", "type": "direction"}
        }
    }

    rooms["abyssal_trench_silence_zone"] = {
        "id": "abyssal_trench_silence_zone",
        "name": "Absolute Silence Zone",
        "description": "A section of the trench where sound cannot exist. Vibrations are "
                       "absorbed by an unknown force, creating perfect silence. Even your own "
                       "heartbeat is inaudible. Communication requires written messages or "
                       "telepathy. The silence is so complete it becomes a physical sensation.",
        "coordinates": [cx + 6, cy + 3],
        "location_type": "wilderness",
        "items": {"silence_stone": {"quantity": 1, "value": 35}, "sound_absorbing_mineral": {"quantity": 1, "value": 22}},
        "exits": {
            "west": {"target": "abyssal_trench_bone_current", "type": "direction"},
            "south": {"target": "abyssal_trench_echo_tomb", "type": "direction"}
        }
    }

    rooms["abyssal_trench_glowing_garden"] = {
        "id": "abyssal_trench_glowing_garden",
        "name": "Abyssal Garden",
        "description": "Impossibly, a garden grows at the bottom of the trench. Strange "
                       "plants with crystalline leaves and bioluminescent flowers thrive in "
                       "the darkness, fed by deep-earth minerals and void energy. The garden "
                       "is tended by organisms that are part plant, part mineral, part void.",
        "coordinates": [cx + 4, cy + 5],
        "location_type": "wilderness",
        "items": {"void_flower": {"quantity": 1, "value": 45}, "crystal_leaf": {"quantity": 1, "value": 30}},
        "exits": {
            "east": {"target": "abyssal_trench_bottom", "type": "direction"}
        }
    }

    rooms["abyssal_trench_deep_shrine"] = {
        "id": "abyssal_trench_deep_shrine",
        "name": "Deep Shrine",
        "description": "A shrine built by unknown hands at trench depth — dedicated to "
                       "something that dwells below even this. The shrine is made of a metal "
                       "that doesn't corrode in saltwater, inscribed with prayers in a language "
                       "that predates all known civilizations.",
        "coordinates": [cx + 6, cy + 6],
        "location_type": "wilderness",
        "items": {"incorruptible_metal_shard": {"quantity": 1, "value": 55}, "ancient_prayer_stone": {"quantity": 1, "value": 35}},
        "exits": {
            "north": {"target": "abyssal_trench_origin_point", "type": "direction"},
            "west": {"target": "abyssal_trench_echo_tomb", "type": "direction"}
        }
    }

    rooms["abyssal_trench_echo_tomb"] = {
        "id": "abyssal_trench_echo_tomb",
        "name": "Echo Tomb",
        "description": "A natural chamber where the dying thoughts of creatures that perished "
                       "in the trench have been preserved in the rock. Touching the walls "
                       "transmits their final moments — terror, wonder, acceptance. Among "
                       "the echoes, one stands out: a calm voice saying 'It's beautiful.'",
        "coordinates": [cx + 5, cy + 6],
        "location_type": "wilderness",
        "items": {"echo_stone": {"quantity": 1, "value": 30}, "final_thought_crystal": {"quantity": 1, "value": 25}},
        "exits": {
            "east": {"target": "abyssal_trench_deep_shrine", "type": "direction"},
            "north": {"target": "abyssal_trench_silence_zone", "type": "direction"}
        }
    }

    rooms["abyssal_trench_abyssal_core"] = {
        "id": "abyssal_trench_abyssal_core",
        "name": "Abyssal Core",
        "description": "The theoretical center of the abyss's influence — a chamber where "
                       "the void bleeds into reality constantly. The walls shift between solid "
                       "and intangible. Gravity changes direction every few minutes. Here, the "
                       "abyss is not something you observe — it observes you.",
        "coordinates": [cx + 7, cy + 5],
        "location_type": "wilderness",
        "items": {"abyssal_core_fragment": {"quantity": 1, "value": 90}, "void_bleed_essence": {"quantity": 1, "value": 60}},
        "exits": {
            "north": {"target": "abyssal_trench_crystallized_time", "type": "direction"},
            "south": {"target": "abyssal_wake_spawning_den", "type": "direction"},
            "east": {"target": "abyssal_wake_tentacle_wall", "type": "direction"}
        }
    }

    # === NEW SUB-REGION: Leviathan's Wake (12 rooms) ===

    rooms["abyssal_wake_tidal_surge"] = {
        "id": "abyssal_wake_tidal_surge",
        "name": "Tidal Surge Chamber",
        "description": "A chamber carved by the passage of something enormous — the wake left "
                       "by a leviathan. Powerful currents still flow through, capable of dragging "
                       "an unwary explorer into the depths. The walls are scored with friction "
                       "marks from the creature's passage.",
        "coordinates": [cx + 7, cy + 3],
        "location_type": "wilderness",
        "items": {"leviathan_friction_residue": {"quantity": 1, "value": 30}, "surge_current_crystal": {"quantity": 1, "value": 22}},
        "exits": {
            "south": {"target": "abyssal_trench_crystallized_time", "type": "direction"},
            "north": {"target": "abyssal_wake_maelstrom", "type": "direction"},
            "east": {"target": "abyssal_wake_debris_field", "type": "direction"}
        }
    }

    rooms["abyssal_wake_maelstrom"] = {
        "id": "abyssal_wake_maelstrom",
        "name": "Wake Maelstrom",
        "description": "A permanent whirlpool created by the leviathan's passage, still spinning "
                       "after centuries. Debris from across the abyss collects in its center — "
                       "an accidental museum of deep-sea artifacts. The maelstrom's eye is "
                       "eerily calm, a pocket of stillness in the chaos.",
        "coordinates": [cx + 7, cy + 2],
        "location_type": "wilderness",
        "items": {"maelstrom_artifact": {"quantity": 1, "value": 40}, "whirlpool_core_water": {"quantity": 1, "value": 25}},
        "exits": {
            "south": {"target": "abyssal_wake_tidal_surge", "type": "direction"},
            "east": {"target": "abyssal_wake_sensory_pool", "type": "direction"},
            "north": {"target": "abyssal_wake_ancient_skeleton", "type": "direction"}
        }
    }

    rooms["abyssal_wake_debris_field"] = {
        "id": "abyssal_wake_debris_field",
        "name": "Debris Field",
        "description": "A vast field of debris left in the leviathan's wake — shattered ships, "
                       "broken equipment, and the remains of creatures that got too close. "
                       "Among the wreckage are artifacts from civilizations unknown to the "
                       "surface world, carried from the deepest abyss.",
        "coordinates": [cx + 8, cy + 3],
        "location_type": "wilderness",
        "items": {"unknown_civilization_artifact": {"quantity": 1, "value": 55}, "shattered_hull_plate": {"quantity": 1, "value": 18}},
        "exits": {
            "west": {"target": "abyssal_wake_tidal_surge", "type": "direction"},
            "south": {"target": "abyssal_wake_bone_graveyard", "type": "direction"}
        }
    }

    rooms["abyssal_wake_bone_graveyard"] = {
        "id": "abyssal_wake_bone_graveyard",
        "name": "Bone Graveyard",
        "description": "Where the leviathan's meals come to rest — an enormous field of bones "
                       "from creatures of every size. Some skulls are as large as houses, their "
                       "species impossible to identify. The bones are slowly being consumed by "
                       "specialized organisms that break them down into minerals.",
        "coordinates": [cx + 8, cy + 4],
        "location_type": "wilderness",
        "items": {"giant_skull_fragment": {"quantity": 1, "value": 35}, "bone_mineral_deposit": {"quantity": 1, "value": 22}},
        "exits": {
            "north": {"target": "abyssal_wake_debris_field", "type": "direction"}
        }
    }

    rooms["abyssal_wake_spawning_den"] = {
        "id": "abyssal_wake_spawning_den",
        "name": "Leviathan Spawning Den",
        "description": "A vast cavern where leviathans breed — enormous eggs the size of "
                       "boulders line the walls in organic cradles. Most eggs are empty, their "
                       "occupants long departed, but some still pulse with life. The warmth "
                       "here is intense, maintained by volcanic vents specific to this chamber.",
        "coordinates": [cx + 7, cy + 6],
        "location_type": "wilderness",
        "items": {"leviathan_egg_fragment": {"quantity": 1, "value": 70}, "spawning_warmth_crystal": {"quantity": 1, "value": 35}},
        "exits": {
            "north": {"target": "abyssal_trench_abyssal_core", "type": "direction"},
            "east": {"target": "abyssal_wake_feeding_ground", "type": "direction"}
        }
    }

    rooms["abyssal_wake_tentacle_wall"] = {
        "id": "abyssal_wake_tentacle_wall",
        "name": "Tentacle Wall",
        "description": "A living wall of enormous tentacles that spans the entire width of "
                       "the trench. The tentacles belong to an entity embedded in the rock "
                       "itself — too large to comprehend, using its appendages to filter "
                       "nutrients from the water. Passage requires navigating between them.",
        "coordinates": [cx + 8, cy + 5],
        "location_type": "wilderness",
        "items": {"wall_tentacle_sample": {"quantity": 1, "value": 40}, "filtered_nutrient_crystal": {"quantity": 1, "value": 25}},
        "exits": {
            "west": {"target": "abyssal_trench_abyssal_core", "type": "direction"},
            "south": {"target": "abyssal_wake_feeding_ground", "type": "direction"}
        }
    }

    rooms["abyssal_wake_feeding_ground"] = {
        "id": "abyssal_wake_feeding_ground",
        "name": "Feeding Ground",
        "description": "The leviathan's primary feeding area — a region where upwelling "
                       "currents bring dense concentrations of organisms from the deep. "
                       "The water here is thick with life, creating a soup of bioluminescence. "
                       "The leviathan visits regularly, its approach heralded by a deep rumble.",
        "coordinates": [cx + 8, cy + 6],
        "location_type": "wilderness",
        "items": {"feeding_ground_plankton": {"quantity": 1, "value": 18}, "deep_upwelling_sample": {"quantity": 1, "value": 30}},
        "exits": {
            "north": {"target": "abyssal_wake_tentacle_wall", "type": "direction"},
            "west": {"target": "abyssal_wake_spawning_den", "type": "direction"}
        }
    }

    rooms["abyssal_wake_sensory_pool"] = {
        "id": "abyssal_wake_sensory_pool",
        "name": "Sensory Pool",
        "description": "A pool of ultra-dense water that amplifies all senses to supernatural "
                       "levels. Immersion grants temporary awareness of every living thing "
                       "within miles — including things you'd rather not know about. The "
                       "enhanced perception is overwhelming and potentially maddening.",
        "coordinates": [cx + 8, cy + 2],
        "location_type": "wilderness",
        "items": {"sensory_amplification_water": {"quantity": 1, "value": 35}, "awareness_crystal": {"quantity": 1, "value": 28}},
        "exits": {
            "west": {"target": "abyssal_wake_maelstrom", "type": "direction"}
        }
    }

    rooms["abyssal_wake_ancient_skeleton"] = {
        "id": "abyssal_wake_ancient_skeleton",
        "name": "Ancient Leviathan Skeleton",
        "description": "The complete skeleton of a leviathan that died millennia ago, still "
                       "resting on the trench floor. The bones are as large as buildings, and "
                       "an entire ecosystem has grown within the ribcage. Explorers have mapped "
                       "the skeleton and estimate the creature was over a mile long.",
        "coordinates": [cx + 7, cy + 1],
        "location_type": "wilderness",
        "items": {"ancient_leviathan_bone": {"quantity": 1, "value": 60}, "ribcage_ecosystem_sample": {"quantity": 1, "value": 30}},
        "exits": {
            "south": {"target": "abyssal_wake_maelstrom", "type": "direction"},
            "east": {"target": "abyssal_wake_current_channel", "type": "direction"},
            "north": {"target": "abyssal_wake_ritual_platform", "type": "direction"}
        }
    }

    rooms["abyssal_wake_current_channel"] = {
        "id": "abyssal_wake_current_channel",
        "name": "Deep Current Channel",
        "description": "A natural channel carved by a powerful deep-sea current that flows "
                       "perpetually in one direction. The current carries nutrients, organisms, "
                       "and occasionally artifacts from unknown depths. Swimming against it is "
                       "impossible; going with it is exhilarating and terrifying.",
        "coordinates": [cx + 8, cy + 1],
        "location_type": "wilderness",
        "items": {"current_carried_artifact": {"quantity": 1, "value": 35}, "deep_current_sample": {"quantity": 1, "value": 18}},
        "exits": {
            "west": {"target": "abyssal_wake_ancient_skeleton", "type": "direction"}
        }
    }

    rooms["abyssal_wake_ritual_platform"] = {
        "id": "abyssal_wake_ritual_platform",
        "name": "Sunken Ritual Platform",
        "description": "A perfectly flat stone platform on the trench floor, clearly artificial. "
                       "Ritual channels are carved into its surface in patterns that make the "
                       "eyes water. This platform was used to summon — or communicate with — "
                       "the leviathans. It may still function.",
        "coordinates": [cx + 7, cy],
        "location_type": "wilderness",
        "items": {"ritual_platform_stone": {"quantity": 1, "value": 45}, "summoning_channel_dust": {"quantity": 1, "value": 30}},
        "exits": {
            "south": {"target": "abyssal_wake_ancient_skeleton", "type": "direction"},
            "east": {"target": "abyssal_wake_eye_of_the_deep", "type": "direction"}
        }
    }

    rooms["abyssal_wake_eye_of_the_deep"] = {
        "id": "abyssal_wake_eye_of_the_deep",
        "name": "Eye of the Deep",
        "description": "The endpoint of the leviathan's wake — a vast circular depression in "
                       "the seafloor where the creature rests. The depression is hundreds of "
                       "yards across and perfectly smooth, polished by the leviathan's body over "
                       "millennia. In the very center, a single enormous eye stares upward from "
                       "beneath the rock. It is not sleeping. It is waiting.",
        "coordinates": [cx + 8, cy],
        "location_type": "wilderness",
        "items": {"deep_eye_tear": {"quantity": 1, "value": 85}, "polished_resting_stone": {"quantity": 1, "value": 40}},
        "exits": {
            "west": {"target": "abyssal_wake_ritual_platform", "type": "direction"}
        }
    }


def generate_all_islands(rooms):
    """Generate all island rooms including Grand Harbor."""
    generate_grand_harbor(rooms)
    generate_sunstone_atoll(rooms)
    generate_emerald_isle(rooms)
    generate_stormbreak_island(rooms)
    generate_cinderforge_island(rooms)
    generate_dreadmist_isle(rooms)
    generate_wyrmscale_island(rooms)
    generate_abyssal_reach(rooms)
