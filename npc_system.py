"""
NPC & Dialogue System
=====================
Branching dialogue trees for all NPCs with:
- Multiple conversation topics
- Choices that lead to different responses
- Recipe/knowledge unlocks through dialogue
- Context-aware responses (check inventory, state, etc.)
"""

# Progression integration
try:
	from progression_system import award_xp, XP_AWARDS
	PROGRESSION_AVAILABLE = True
except ImportError:
	PROGRESSION_AVAILABLE = False

# Quest integration
try:
	from quest_system import QuestManager
	QUEST_AVAILABLE = True
except ImportError:
	QUEST_AVAILABLE = False

# Reputation integration
try:
	from npc_reputation import ReputationManager, GIFT_PREFERENCES, REPUTATION_DIALOGUE
	REPUTATION_AVAILABLE = True
except ImportError:
	REPUTATION_AVAILABLE = False


# =====================================================================
# NPC DATABASE
# =====================================================================
# Each NPC:
#   id:          unique identifier (matches world.json npcs array)
#   name:        display name
#   title:       short role description
#   location:    room_id where this NPC lives
#   greeting:    initial text when player starts talking
#   dialogue:    dict of node_id -> DialogueNode
#
# DialogueNode:
#   text:        what the NPC says
#   options:     list of {label, next} — player choices
#   effects:     optional dict of effects to apply
#   condition:   optional dict to check before showing this node
# =====================================================================

NPC_DATABASE = {
	"blacksmith": {
		"id": "blacksmith",
		"name": "Tormund",
		"title": "Village Blacksmith",
		"location": "village_blacksmith",
		"greeting": "The blacksmith looks up from his anvil, sweat glistening on his brow.\n\n\"Ah, a visitor! Name's Tormund. I forge the finest steel this side of the mountains. What can I do for you?\"",
		"dialogue": {
			"root": {
				"text": None,
				"options": [
					{"label": "Can you teach me to forge weapons?", "next": "teach_forging"},
					{"label": "What do you know about the dungeons?", "next": "dungeon_info"},
					{"label": "Tell me about the village.", "next": "village_info"},
					{"label": "What materials do you need?", "next": "materials"},
					{"label": "Goodbye.", "next": "farewell"},
				],
			},
			"teach_forging": {
				"text": "Tormund grins broadly.\n\n\"Now you're talking! Forging is an art, friend. Bring me iron ingots and I'll show you the basics. Every good smith starts with a dagger.\"\n\nHe pulls out a worn notebook and shows you several diagrams.\n\n\"Here — let me show you what I know.\"",
				"effects": {
					"learn_recipes": ["steel_dagger", "iron_sword", "refined_iron"],
				},
				"options": [
					{"label": "What about more advanced forging?", "next": "advanced_forging"},
					{"label": "Where can I find iron ingots?", "next": "find_iron"},
					{"label": "Thanks! Let me ask something else.", "next": "root"},
				],
			},
			"advanced_forging": {
				"text": "Tormund strokes his beard thoughtfully.\n\n\"Advanced work... aye. I can teach you leather armor — wolf pelts and rope, that's all you need. And if you bring me broken equipment, I can show you how to reforge it into something better.\n\nBut the REAL master crafting? That happens at the deep forges — the altars in the dungeons. Each one has its own power. I've heard the Iron Halls have a forge that burns eternally.\"",
				"effects": {
					"learn_recipes": ["leather_armor_piece", "masterwork_shield", "steel_longsword"],
				},
				"options": [
					{"label": "Tell me more about the dungeon forges.", "next": "dungeon_forges"},
					{"label": "Thanks, let me ask something else.", "next": "root"},
				],
			},
			"dungeon_forges": {
				"text": "\"There are four deep forges, one in each dungeon beneath this land:\n\n  • The Forge of Light in the Crystal Caverns — works with crystal and light energy.\n  • The Shadowforge in the Shadow Depths — unmakes and remakes with void power.\n  • The Dwarven Eternal Anvil in the Iron Halls — my dream forge. Uses mithril.\n  • The Catacomb Soul Altar beneath the ruins — binds soul energy to steel.\n\nEach forge has its own recipes. You'll discover them when you find the altars. But be warned — the dungeons are dangerous, especially the time-gated ones. The Shadow Depths beneath the crypt, though — that one's always open.\"",
				"options": [
					{"label": "How do I get mithril?", "next": "mithril_info"},
					{"label": "Thanks, let me ask something else.", "next": "root"},
				],
			},
			"mithril_info": {
				"text": "\"Raw mithril is found deep in the Iron Halls — third floor, if I recall. You'll also need an eternal ember to forge it. The dwarves guarded both jealously.\n\nBring them to the Dwarven Eternal Anvil and the recipe should reveal itself. The old smiths built wisdom into the forge stones.\"",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"find_iron": {
				"text": "\"Iron ingots? Well, you're standing next to one!\" He chuckles.\n\n\"But for more, check these places:\n  • The Iron Halls dungeon — full of the stuff\n  • Sometimes the shop has ingots in stock\n  • The mountain foothills occasionally have ore deposits\n\nBring me ingots and sticks and I'll teach you to forge.\"",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"dungeon_info": {
				"text": "\"The dungeons? Dangerous places, friend. Three of them open and close on a schedule — the Crystal Caverns, Iron Halls, and Sunken Catacombs. They change every time they open.\n\nBut there's one that's always open — the Shadow Depths, beneath the old crypt in the graveyard. Fixed layout, never changes. Good for learning the ropes... if you can handle the darkness.\n\nAll four have crafting altars on their deepest floor. Worth the risk if you ask me.\"",
				"options": [
					{"label": "Tell me about the Shadow Depths.", "next": "shadow_info"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"shadow_info": {
				"text": "\"The Shadow Depths... dark place, that one. Opened up beneath the graveyard crypt. Three floors of obsidian and void. They say a Shadow Sovereign once ruled from a throne down there.\n\nThe forge at the bottom — the Shadowforge — works with void energy. Requires obsidian and shadow materials. The swamp witch knows more about that dark craft than I do.\"",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"village_info": {
				"text": "\"Our village is small but proud. We've got everything an adventurer needs:\n\n  • The shop sells basic supplies — rotating stock\n  • Father Aldric at the chapel can heal your wounds\n  • The tavern's got rumors and ale in equal measure\n  • Old Martha in the swamp... well, she's an acquired taste\n\nAnd of course, you need armor and weapons, you come to me.\"",
				"options": [
					{"label": "Who is Old Martha?", "next": "martha_info"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"martha_info": {
				"text": "\"The swamp witch? She's been there longer than anyone can remember. Knows every plant, every potion, every poison. Some folk are scared of her, but she's harmless... mostly.\n\nShe can teach you to brew potions and cures. Worth visiting if you plan to delve into dungeons — her poison cures have saved many a life.\"",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"materials": {
				"text": "\"I always need materials! Here's what I work with:\n\n  • Iron ingots — the foundation of everything\n  • Sticks — for handles and shafts\n  • Wolf pelts — for leather armor\n  • Rope coils — for bindings\n  • Broken equipment — I can reforge broken shields and such\n  • Refined iron — for advanced work (I can teach you to make it)\n\nBring me these and we'll forge something worth carrying.\"",
				"options": [
					{"label": "Teach me to forge!", "next": "teach_forging"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"farewell": {
				"text": "\"Safe travels, friend. Come back when you need steel!\"",
				"options": [],
			},
		},
	},

	"hermit": {
		"id": "hermit",
		"name": "Old Finn",
		"title": "Forest Hermit",
		"location": "hermit_cabin",
		"greeting": "The old hermit peers at you from beneath bushy eyebrows.\n\n\"Hmm? A visitor? Don't get many of those. Name's Finn. Been living in these woods longer than most trees. What brings you to my door?\"",
		"dialogue": {
			"root": {
				"text": None,
				"options": [
					{"label": "Can you teach me about herbs and potions?", "next": "teach_herbs"},
					{"label": "What do you know about the forest?", "next": "forest_lore"},
					{"label": "Have you heard about the dungeons?", "next": "dungeon_lore"},
					{"label": "You seem wise. Any advice for an adventurer?", "next": "advice"},
					{"label": "Goodbye, Finn.", "next": "farewell"},
				],
			},
			"teach_herbs": {
				"text": "Finn's eyes light up.\n\n\"Ah, herbalism! The forest provides everything you need, if you know where to look.\"\n\nHe shuffles to a shelf packed with dried plants and opens a tattered journal.\n\n\"The strange herbs that grow near my cabin and in the swamp — those are the foundation. Mix two with mineral water from the Crystal Caverns and you get a healing potion. Mix one with shelf mushrooms — an antidote. Simple but effective.\"\n\nHe hands you the journal.",
				"effects": {
					"learn_recipes": ["healing_potion", "antidote"],
				},
				"options": [
					{"label": "Where do I find mineral water?", "next": "mineral_water"},
					{"label": "What else can I brew?", "next": "advanced_herbs"},
					{"label": "Thanks! Let me ask something else.", "next": "root"},
				],
			},
			"mineral_water": {
				"text": "\"The mineral hot springs in the Crystal Caverns — first floor. The water there has healing properties on its own, but it's the base for proper potions.\n\nYou can also make a quality torch if you combine a regular torch with rope and glowing moss. Learned that one the hard way — nearly broke my neck in a dark cave.\"",
				"effects": {
					"learn_recipes": ["quality_torch"],
				},
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"advanced_herbs": {
				"text": "\"Well now... for the advanced cures, you'll want to visit Old Martha in the swamp. She knows things about poison cures that I don't dare mess with.\n\nAnd Father Aldric at the chapel — he showed me how to make holy water once. Prayer candle and mineral water, blessed at any crafting station. Heals and cures poison both.\"",
				"effects": {
					"learn_recipes": ["holy_water"],
				},
				"options": [
					{"label": "Tell me about Old Martha.", "next": "martha"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"martha": {
				"text": "\"Martha? She lives in a hut deep in the swamp. Most folk avoid her — they say she talks to shadows and brews poisons for fun.\n\nTruth is, she's just old and grumpy. Knows her craft though. If you bring her some swamp ingredients, she'll teach you cures that can save your life in a dungeon.\n\nJust... don't touch anything in her hut without asking.\"",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"forest_lore": {
				"text": "\"This forest is ancient. The trees remember things that men have forgotten.\n\nThe woodland shrine to the south — it predates the village by centuries. Strange coins turn up there. The ancient grove is even older — I once found an acorn there that wouldn't sprout no matter what I did. Magic, I reckon.\n\nAnd then there's the cave to the west... the Crystal Caverns. Opens and closes on some schedule I've never figured out. But when it's open, the crystals inside are worth a fortune.\"",
				"options": [
					{"label": "Tell me about the Crystal Caverns.", "next": "crystal_info"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"crystal_info": {
				"text": "\"Beautiful and deadly, the Caverns. Three floors of crystal formations that'll take your breath away — and traps that'll take your life.\n\nThe miners tried to harvest crystals once. Most never came back. Their camp is still on the first floor — I found a journal there once. Sad reading.\n\nAt the very bottom is something called the Forge of Light. Uses concentrated light to reshape materials. Never seen it myself.\"",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"dungeon_lore": {
				"text": "\"Four dungeons beneath this land, each hiding secrets:\n\nThree open on a schedule — Crystal Caverns, Iron Halls, Sunken Catacombs. New layout each time. The fourth — Shadow Depths — is always open. Fixed, never changes. Enter through the crypt in the graveyard.\n\nEach has a crafting altar on the deepest floor. And I've heard tell of secret rooms in the procedurally generated ones — hidden behind the boss room walls, if you know to look.\"",
				"options": [
					{"label": "Secret rooms?", "next": "secret_rooms"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"secret_rooms": {
				"text": "\"Aye, secret rooms. In the time-gated dungeons, the boss chamber on the final floor sometimes has hidden passages.\n\nThe trick is to inspect the walls carefully. Run your hands along them. If there's a secret passage, you'll feel the draft.\n\nI've heard there's... art... inside. Strange art. 'Do a big cheese' or something. Nobody knows what it means.\" He shrugs.",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"advice": {
				"text": "\"Advice? Hmm.\n\n  • Always carry healing potions. The traps in dungeons are nasty.\n  • Search every room — hidden traps can be found before they trigger.\n  • Use a torch in dark places — helps you spot dangers.\n  • Talk to everyone — we all know different things.\n  • The tomes and journals scattered around? Read them. They hold crafting hints.\n  • Don't be afraid to run from a dungeon if you're low on health.\n\nAnd most importantly — save often, friend.\"",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"farewell": {
				"text": "\"Be careful out there. The forest may seem peaceful, but it has teeth.\"\n\nFinn waves you off and returns to whittling.",
				"options": [],
			},
		},
	},

	"priest": {
		"id": "priest",
		"name": "Father Aldric",
		"title": "Village Priest",
		"location": "chapel",
		"greeting": "The priest looks up from his prayers with a kind smile.\n\n\"Welcome, child. I am Father Aldric. The chapel is a place of peace and healing. How may I help you?\"",
		"dialogue": {
			"root": {
				"text": None,
				"options": [
					{"label": "Can you heal me?", "next": "heal"},
					{"label": "Can you teach me to make holy water?", "next": "teach_holy"},
					{"label": "Tell me about the graveyard.", "next": "graveyard_info"},
					{"label": "What do you know about the Shadow Depths?", "next": "shadow_depths"},
					{"label": "Goodbye, Father.", "next": "farewell"},
				],
			},
			"heal": {
				"text": None,
				"effects": {
					"heal_full": True,
				},
				"options": [
					{"label": "Thank you! Let me ask something else.", "next": "root"},
					{"label": "Goodbye, Father.", "next": "farewell"},
				],
			},
			"teach_holy": {
				"text": "Father Aldric nods solemnly.\n\n\"Holy water is a sacred remedy. It requires a prayer candle — blessed here in this chapel — and mineral water from a pure source. The caves beneath the forest contain mineral springs.\n\nCombine them at any crafting station with prayer and intent. The result purifies both body and soul — heals wounds and cures poison.\"\n\nHe shows you the blessing ritual.",
				"effects": {
					"learn_recipes": ["holy_water"],
				},
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"graveyard_info": {
				"text": "\"The graveyard troubles me. It has always been a quiet place of rest for our departed... but lately, a darkness has seeped up from below.\n\nThe old crypt in the back — something opened there. A crack in the wall leading down into... shadow. They call it the Shadow Depths now. An evil place, but it does not spread. Whatever is down there seems... contained.\n\nI pray for the souls trapped below.\"",
				"options": [
					{"label": "Tell me more about the Shadow Depths.", "next": "shadow_depths"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"shadow_depths": {
				"text": "\"The Shadow Depths are a wound in the earth. Three floors of darkness and void energy. At the bottom sits a throne — the Shadow Sovereign's throne. The Sovereign is gone, sealed away long ago, but its power lingers.\n\nThere is a forge at the bottom too — the Shadowforge. It works with void energy. Dangerous, but powerful.\n\nIf you go there... take holy water. And light. The shadows fear both.\"\n\nHis eyes darken. \"And whatever you do, do not put on the crown.\"",
				"options": [
					{"label": "What crown?", "next": "crown_warning"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"crown_warning": {
				"text": "\"The Sovereign's Shadow Crown. If it still exists down there... it carries the Sovereign's will. A fragment of its consciousness.\n\nI cannot stop you from taking it. But I urge caution. Power freely offered always has a price.\"\n\nHe pauses, then adds quietly:\n\"The swamp witch might know more. She has... an affinity for such things.\"",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"farewell": {
				"text": "\"Go with blessings, child. Return whenever you need healing or guidance.\"\n\nFather Aldric returns to his prayers.",
				"options": [],
			},
		},
	},

	"swamp_witch": {
		"id": "swamp_witch",
		"name": "Old Martha",
		"title": "Swamp Witch",
		"location": "witch_hut",
		"greeting": "A hunched figure peers at you from behind a bubbling cauldron.\n\n\"Well, well... fresh meat in my swamp. Don't worry, dearie, I don't bite. Much.\"\n\nShe cackles. \"I'm Martha. What do you want?\"",
		"dialogue": {
			"root": {
				"text": None,
				"options": [
					{"label": "Can you teach me about poisons and cures?", "next": "teach_cures"},
					{"label": "What do you know about the Shadow Depths?", "next": "shadow_knowledge"},
					{"label": "Tell me about the swamp.", "next": "swamp_lore"},
					{"label": "People seem afraid of you.", "next": "reputation"},
					{"label": "Goodbye, Martha.", "next": "farewell"},
				],
			},
			"teach_cures": {
				"text": "Martha grins, showing remarkably good teeth for someone her age.\n\n\"Ah, a practical one! Good, good. The dungeons are FULL of poison traps, and you'll die without a cure.\"\n\nShe points to the herbs hanging from her ceiling.\n\n\"Glowing moss — double handful — and a marsh lily. Mix them anywhere. Cures most poisons dead. I call it Swamp Cure. Learned it from my mother, who learned it from the moss itself.\"\n\nShe presses a stained recipe card into your hand.",
				"effects": {
					"learn_recipes": ["poison_cure"],
				},
				"options": [
					{"label": "What about shadow-forging?", "next": "shadow_forging"},
					{"label": "Any other recipes?", "next": "more_recipes"},
					{"label": "Thanks! Let me ask something else.", "next": "root"},
				],
			},
			"shadow_forging": {
				"text": "Martha's eyes gleam with dangerous excitement.\n\n\"Shadow-forging! Now THAT'S the good stuff. The Shadowforge at the bottom of the Shadow Depths — it works with void energy. Dark, beautiful stuff.\n\nI know two recipes for it:\n  • Shadow Blade — two obsidian blade fragments and concentrated void essence.\n  • Void Amulet — a dread idol and a void heart fragment.\n\nThere's more the forge itself will show you. But you'll need to GET there first, dearie. Three floors of nasty surprises.\"",
				"effects": {
					"learn_recipes": ["shadow_blade", "void_amulet"],
				},
				"options": [
					{"label": "Tell me more about the Shadow Depths.", "next": "shadow_knowledge"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"more_recipes": {
				"text": "\"Hmm... well, I also know that the hermit up in the forest knows healing potions. And the priest makes holy water — healing AND cleansing.\n\nFor my part? I stick to poisons and cures. Two sides of the same coin, dearie. But if you find interesting ingredients in the dungeons, bring them to me. I might know what to do with them.\"",
				"options": [
					{"label": "What about shadow-forging?", "next": "shadow_forging"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"shadow_knowledge": {
				"text": "Martha drops her playful demeanor. Her voice becomes serious.\n\n\"The Shadow Depths... I know that place better than anyone alive. The Sovereign that lived there — it wasn't evil. It was something BEYOND good and evil. A being of pure void.\n\nThe void consumes, yes, but it also creates. The Shadowforge proves that. Void energy can unmake iron and remake it as something stronger.\n\nThe Sovereign's Cloak — now THAT'S a prize. You'd need the crown, a cloak fragment, and umbral thread. The forge would do the rest.\"\n\nHer eyes go distant. \"I tried once. Didn't have the thread.\"",
				"effects": {
					"learn_recipes": ["sovereign_cloak"],
				},
				"options": [
					{"label": "The priest warned me about the crown.", "next": "crown_debate"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"crown_debate": {
				"text": "Martha snorts. \"Aldric means well, but he fears what he doesn't understand. The crown isn't cursed — it's just powerful. WEARING it might be unwise, yes. But USING it as a crafting material? Perfectly safe.\n\nThe Sovereign is long gone. Only echoes remain. The crown is just a conduit now — a shell of what it was.\n\nThat said...\" She pauses. \"If you hear whispers when you hold it... put it down. Fast.\"",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"swamp_lore": {
				"text": "\"My swamp? It's beautiful, if you've got eyes to see. The marsh lilies bloom at midnight. The foggy marsh is where the best glowing moss grows. And the sunken ruins — ancient, from before the village existed.\n\nBeneath the ruins is the entrance to the Sunken Catacombs. Opens and closes on a schedule, like the other dungeon portals. Different every time.\n\nThe deep swamp... be careful there. Things live in the deep water.\"",
				"options": [
					{"label": "What lives in the deep water?", "next": "deep_water"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"deep_water": {
				"text": "She waves a gnarled hand. \"Nothing that'll bother you on dry land. But if you ever get a fishing rod working near deep water... you might catch something interesting. Or something that catches YOU.\"\n\nShe cackles again.",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"reputation": {
				"text": "\"Afraid? Hah! Good. Keeps the riffraff away.\"\n\nShe stirs her cauldron thoughtfully.\n\n\"I've been here seventy years, dearie. I helped birth half the village. I cure their fevers, mend their bones, ease their passing. But one time — ONE time — I turn a chicken purple, and suddenly I'm a 'scary witch.'\"\n\nShe pauses. \"The chicken was fine, by the way. Lived twelve more years. Named her Violet.\"",
				"options": [
					{"label": "That's... actually pretty funny.", "next": "violet_story"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"violet_story": {
				"text": "Martha beams. \"Violet was the best chicken in the village! Laid purple eggs! Well... slightly purple. Violet-adjacent.\n\nAnyway, don't believe everything the villagers say about me. I'm just an old woman who likes her privacy and her potions.\"\n\nShe winks. \"And occasionally turning things unusual colors.\"",
				"options": [
					{"label": "I like you, Martha.", "next": "liked"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"liked": {
				"text": "\"Hmph. Don't get sentimental on me, dearie. But... you're alright too. Come back anytime. I'll teach you what I know.\"\n\nShe pretends to focus on her cauldron, but you catch a small smile.",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
					{"label": "Goodbye, Martha.", "next": "farewell"},
				],
			},
			"farewell": {
				"text": "\"Off with you then. And DON'T eat anything growing in the deep swamp. Trust me on that.\"\n\nShe waves you out without looking up from her cauldron.",
				"options": [],
			},
		},
	},

	"bartender": {
		"id": "bartender",
		"name": "Bren",
		"title": "Tavern Keeper",
		"location": "village_tavern",
		"greeting": "The bartender polishes a mug with a well-practiced rhythm.\n\n\"Welcome to the Golden Tankard! I'm Bren. Best ale in the region, or your money back. What'll it be?\"",
		"dialogue": {
			"root": {
				"text": None,
				"options": [
					{"label": "Any rumors or news?", "next": "rumors"},
					{"label": "Tell me about the regulars.", "next": "regulars"},
					{"label": "What do you know about the area?", "next": "area_info"},
					{"label": "Got any tips for a dungeon delver?", "next": "dungeon_tips"},
					{"label": "Goodbye.", "next": "farewell"},
				],
			},
			"rumors": {
				"text": "Bren leans in conspiratorially.\n\n\"Rumors? Oh, I've got plenty:\n\n  • Strange lights in the graveyard at night. Something opened in the crypt.\n  • A merchant came through saying the Iron Halls have mithril — THE mithril.\n  • The hermit in the forest talks to trees. Some say the trees talk back.\n  • Old Martha turned another chicken purple last week. Third one this year.\n  • Some adventurer claims he found a secret room in a dungeon with... art inside? Strange art. Wouldn't explain it.\"\n\nHe shrugs. \"Take it all with a grain of salt, of course.\"",
				"options": [
					{"label": "Tell me about the crypt lights.", "next": "crypt_lights"},
					{"label": "What's this about mithril?", "next": "mithril_rumor"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"crypt_lights": {
				"text": "\"Started a few weeks ago. Purple-ish glow coming from the graveyard crypt. Father Aldric went to investigate and came back pale as a sheet.\n\nSays there's a crack in the back wall of the crypt leading down into... darkness. Calls it the Shadow Depths. Nobody's made it all three floors and back yet.\n\nThe locals avoid the graveyard now. But adventurers? They can't resist.\"",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"mithril_rumor": {
				"text": "\"Aye, mithril. Lightest, strongest metal ever forged. The dwarves of the Iron Halls hoarded it.\n\nThe merchant said raw mithril ore is on the third floor, guarded by traps that'd make your eyes water. But if you could get some to a proper forge...\n\nTormund at the blacksmith barely sleeps anymore thinking about it.\"",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"regulars": {
				"text": "\"See that fellow in the corner?\" He nods toward a grizzled man.\n\n\"That's Gareth, our resident war veteran. Been coming here every night for years. Loves telling stories about the old battlefield east of here.\n\nOther than him, we get farmers, the occasional trader, and adventurers like yourself. Father Aldric stops by on Sundays — says it's 'pastoral duty.' I think he just likes the ale.\"",
				"options": [
					{"label": "Can I talk to Gareth?", "next": "gareth_redirect"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"gareth_redirect": {
				"text": "\"Sure, just turn to him directly. He loves an audience for his war stories.\"",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"area_info": {
				"text": "\"I hear plenty from travelers. The land around here breaks into a few regions:\n\n  • The forest to the west — ancient, magical, full of herbs and a hermit\n  • The mountains to the north — highland trails, and somewhere up there, the Iron Halls\n  • The swamp to the east — foggy, dangerous, home to Martha the witch\n  • The coast to the southeast — beaches, tidal caves, an old dock\n  • The ruins and battlefield to the east — history and danger\n  • And of course, the graveyard south of the crossroads\n\nPlenty to explore if you've got the nerve.\"",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"dungeon_tips": {
				"text": "\"I've served enough adventurers to know what works:\n\n  1. Search every room — traps hide everywhere\n  2. Carry healing potions — the hermit can teach you to make them\n  3. Use torches in dungeons — you'll spot traps better\n  4. The time-gated dungeons close on schedule — don't get trapped inside!\n  5. The Shadow Depths is always open — good for practice\n  6. Every dungeon has a crafting altar on the bottom floor\n  7. Inspect walls in boss rooms — sometimes there's... more\n\nAnd if things go bad, just 'leave' — no shame in living to fight another day.\"",
				"options": [
					{"label": "Any secrets I should know about?", "next": "hidden_hints"},
					{"label": "Thanks! Let me ask something else.", "next": "root"},
				],
			},
			"hidden_hints": {
				"text": "Bren lowers his voice to barely a whisper.\n\n\"I've heard... things. From old salts and wandering scholars.\n\n  • The sea cave south of here — there's an old sailor who swears there's a vault behind the back wall. A pirate vault. Examine it carefully.\n  • The woodland shrine in the forest — apparently someone left a puzzle there centuries ago. The altar knows if you've done your research.\n  • The castle library — there's a scholar who mentioned a locked cabinet. Something about an alchemist's key.\n  • And that old clocktower? People say the inside is sealed, but if you look at the gears...\n\nI'm a bartender. I hear things.\"",
				"options": [
					{"label": "Where do I find the alchemist's key?", "next": "alchemist_key_hint"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"alchemist_key_hint": {
				"text": "\"The alchemist's key? A traveling potion merchant passed through a few months back. Left a strange brass key as payment for his drinks.\"\n\nBren reaches under the bar and slides a small key across the counter.\n\n\"I've been meaning to figure out what it opens. Take it — maybe you'll have more luck than I did.\"",
				"effects": {"give_items": {"alchemist_key": 1}},
				"options": [
					{"label": "Thank you! Let me ask something else.", "next": "root"},
				],
			},
			"farewell": {
				"text": "\"Come back anytime! The Golden Tankard never closes.\"\n\nBren goes back to polishing his mugs.",
				"options": [],
			},
		},
	},

	"patron": {
		"id": "patron",
		"name": "Gareth",
		"title": "War Veteran",
		"location": "village_tavern",
		"greeting": "The grizzled veteran looks up from his ale with tired but sharp eyes.\n\n\"Eh? You want to talk? Fine. Sit down. Name's Gareth. Fought in the last war, twenty years ago now. What do you want to know?\"",
		"dialogue": {
			"root": {
				"text": None,
				"options": [
					{"label": "Tell me about the war.", "next": "war_story"},
					{"label": "What's on the old battlefield?", "next": "battlefield"},
					{"label": "Know anything about the dungeons?", "next": "dungeon_knowledge"},
					{"label": "Any advice for a young adventurer?", "next": "advice"},
					{"label": "I'll leave you to your drink.", "next": "farewell"},
				],
			},
			"war_story": {
				"text": "Gareth stares into his ale.\n\n\"The war... we fought the northern tribes. They came down through the mountains like an avalanche. We met them on the field east of here.\n\nThree days of fighting. We won, but barely. Left good men on that field. You can still find their swords and shields rusting in the grass.\n\nAfter that... the tribes retreated to the mountains. Some say they went into the Iron Halls — dwarf ruins. Made it their stronghold. Haven't seen them since.\"",
				"options": [
					{"label": "What happened to the Iron Halls?", "next": "iron_halls"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"iron_halls": {
				"text": "\"The Iron Halls were a dwarven fortress — abandoned centuries before any of us were born. After the war, we sent scouts into the mountains to look for the retreating tribes.\n\nThe scouts found the entrance but... the place was empty. No tribes, no dwarves, just stone and iron and darkness. And traps. The dwarves trapped everything.\n\nNow it opens and closes like the other dungeons. I don't understand the magic behind it, but I know what's inside: iron, steel, and at the very bottom — mithril.\"",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"battlefield": {
				"text": "\"The old battlefield... I go there sometimes. Pay my respects.\n\nYou can still find rusty swords and broken shields in the grass. Twenty years of rain and they're still there. Nobody wants to touch them.\n\nThere's a rusty sword there that's still usable, if you clean it up. And a broken shield — Tormund the blacksmith could probably reforge it into something decent.\"",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"dungeon_knowledge": {
				"text": "\"I've been in the Crystal Caverns once, back when I was younger and stupider. Beautiful place. Deadly place.\n\nThe traps... you think you're clever, then the floor opens or the ceiling starts coming down. The disarm trick is to study each trap carefully — look for the mechanism, the pressure plate, the trigger.\n\nSome traps you need tools for. A lockpick set helps. Others, you just need quick wits and luck.\"",
				"options": [
					{"label": "Any tips on traps?", "next": "trap_tips"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"trap_tips": {
				"text": "\"Three things about traps:\n\n  1. Use 'search' in every room. It can reveal hidden traps before they trigger.\n  2. Some traps block your path — pit traps and crushing ceilings. You MUST disarm those.\n  3. When you 'disarm' a trap, you get a choice. Study the trap first, then pick your approach. Having a lockpick set or torch improves your chances.\n\nAnd poison traps? Carry an antidote or strange herbs. Poison ticks damage every time you move.\"",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"advice": {
				"text": "\"I'm just an old soldier. But I'll tell you what I've learned:\n\nDon't fight battles you can't win. There's no shame in retreating and coming back stronger. Save your game often. Explore everything — the world rewards curiosity.\n\nAnd talk to people. This village is full of knowledge if you bother to listen. The hermit, the blacksmith, the witch, the priest — they all have something to teach.\"\n\nHe takes a long drink. \"Now go do something I'm too old for.\"",
				"options": [
					{"label": "Thanks, Gareth.", "next": "farewell"},
				],
			},
			"farewell": {
				"text": "\"Yeah, yeah. Go on.\"\n\nGareth raises his mug in a half-salute and goes back to staring at nothing.",
				"options": [],
			},
		},
	},

	"town_crier": {
		"id": "town_crier",
		"name": "Herald Pip",
		"title": "Town Crier",
		"location": "village_square",
		"greeting": "A young man in a slightly-too-large hat straightens up importantly.\n\n\"Hear ye, hear ye! I am Pip, Herald of the Village Square! Purveyor of news, announcements, and general information! How may I be of service?\"",
		"dialogue": {
			"root": {
				"text": None,
				"options": [
					{"label": "What's the latest news?", "next": "news"},
					{"label": "Where should I explore?", "next": "explore_guide"},
					{"label": "Tell me about the village services.", "next": "services"},
					{"label": "What are the dungeon schedules?", "next": "dungeon_schedule"},
					{"label": "Goodbye, Pip.", "next": "farewell"},
				],
			},
			"news": {
				"text": "Pip clears his throat dramatically.\n\n\"HEAR YE! Current news and notices:\n\n  📜 The Shadow Depths beneath the graveyard crypt are NOW OPEN to adventurers! Enter at your own risk!\n  📜 Dungeon schedule remains unchanged — Crystal Caverns, Iron Halls, and Sunken Catacombs open on regular rotation.\n  📜 Tormund the Blacksmith is offering crafting lessons to qualified adventurers!\n  📜 Father Aldric reminds everyone that free healing is available at the chapel.\n  📜 Old Martha says — and I quote — 'Tell them to bring me glowing moss or don't come at all.'\"\n\nHe looks pleased with himself.",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"explore_guide": {
				"text": "\"For newcomers, I recommend this route:\n\n  1. Start with the forest — west from the clearing. Good for gathering herbs.\n  2. Visit the village — learn from NPCs, stock up at the shop.\n  3. Try the Shadow Depths (graveyard crypt) — it's always open, good practice.\n  4. When you're stronger, tackle the time-gated dungeons.\n\nKey places to visit:\n  • Hermit's Cabin (forest) — learn potion recipes\n  • Blacksmith (village) — learn forging recipes\n  • Chapel (village) — free healing\n  • Witch's Hut (swamp) — learn poison cures\n  • Tavern (village) — rumors and tips\"",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"services": {
				"text": "\"The village offers these fine services:\n\n  🏪 General Store — Buy and sell items. Rotating stock!\n  ⚒️ Blacksmith — Craft weapons and armor (talk to Tormund first)\n  ⛪ Chapel — Free healing from Father Aldric\n  🍺 Tavern — Rumors, tips, and ale\n  📣 Me! — News and information, right here in the square\n\nWe also have a merchant who passes through occasionally.\"",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"dungeon_schedule": {
				"text": "\"The three time-gated dungeons follow a strict schedule:\n\nThey open and close every 3 hours, starting at midnight, Germany time:\n  00:00 - 03:00  OPEN\n  03:00 - 06:00  CLOSED\n  06:00 - 09:00  OPEN\n  09:00 - 12:00  CLOSED\n  ...and so on!\n\nIf you're inside when they close, you'll be teleported out automatically.\n\nThe Shadow Depths is ALWAYS open. No schedule — enter whenever you want through the graveyard crypt.\"",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"farewell": {
				"text": "\"Good day to you, citizen! Remember — knowledge is the mightiest weapon!\"\n\nPip strikes an impressive pose.",
				"options": [],
			},
		},
	},

	"merchant": {
		"id": "merchant",
		"name": "Silvia",
		"title": "Traveling Merchant",
		"location": "village_square",
		"greeting": "A sharp-eyed woman in traveling clothes looks you over appraisingly.\n\n\"Ah, a customer? I'm Silvia. I trade across the region. What interests you?\"",
		"dialogue": {
			"root": {
				"text": None,
				"options": [
					{"label": "Any trading tips?", "next": "trading_tips"},
					{"label": "What's valuable around here?", "next": "valuable_items"},
					{"label": "Have you traveled far?", "next": "travels"},
					{"label": "Goodbye.", "next": "farewell"},
				],
			},
			"trading_tips": {
				"text": "\"Trading tips? For free? You drive a hard bargain.\"\n\nShe smirks. \"Fine:\n\n  • The shop's prices fluctuate — check back regularly.\n  • You can negotiate with the shopkeeper. Offer less than asking price.\n  • Dungeon loot sells well, especially high-tier items.\n  • Crafted items are worth more than raw materials — if you know a recipe.\n  • The rarest items are found on the deepest dungeon floors.\n\nBuy low, sell high. Simple as that.\"",
				"options": [
					{"label": "What items are worth the most?", "next": "valuable_items"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"valuable_items": {
				"text": "\"The most valuable things I've seen pass through here:\n\n  💎 Dungeon boss loot — titan cores, shadow crowns, mithril\n  💎 Crafted weapons — prismatic blades, mithril blades, soul blades\n  💎 Rare crafted gear — Sovereign's Cloak, Dwarven Masterwork\n  💎 Crystal items — diamonds, heart crystal fragments\n  💎 Void materials — void gold, paradox gemstones\n\nIf you can carry it out of a dungeon's deepest floor, it's worth carrying.\"",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"travels": {
				"text": "\"I've been everywhere this land has to offer. The coast is beautiful but empty. The mountains are rich but cold. The swamp is... the swamp.\n\nThe most interesting place? The old battlefield, east of the village. Twenty years since the war and you can still find good steel there. Tormund would pay well for battlefield iron.\n\nI've also seen the entrances to all four dungeons. Never gone in myself — I prefer my profits without the risk of death.\"",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"farewell": {
				"text": "\"Pleasure doing business. Or not doing business, as the case may be.\"\n\nSilvia goes back to examining her ledger.",
				"options": [],
			},
		},
	},

	# =====================================================================
	# ISLAND NPCs — Grand Harbor
	# =====================================================================

	"harbor_master": {
		"id": "harbor_master",
		"name": "Captain Weylan",
		"title": "Harbor Master",
		"location": "grand_harbor_square",
		"greeting": "A broad-shouldered man in a salt-stained greatcoat surveys the docks with a practiced eye.\n\n\"Welcome to Grand Harbor, traveler. I'm Captain Weylan, Harbor Master. Every ship, every sailor, every crate passes through me. What do you need?\"",
		"dialogue": {
			"root": {
				"text": None,
				"options": [
					{"label": "Tell me about the islands.", "next": "island_info"},
					{"label": "Any sailing tips?", "next": "sailing_tips"},
					{"label": "What dangers are out there?", "next": "dangers"},
					{"label": "Goodbye, Captain.", "next": "farewell"},
				],
			},
			"island_info": {
				"text": "Weylan unfurls a weathered chart.\n\n\"Seven islands, each more dangerous than the last:\n\n  • Sunstone Atoll — warm, friendly. Good for new sailors. Level 5.\n  • Emerald Isle — dense jungle, druid folk. Level 10.\n  • Stormbreak — constant lightning. Level 15.\n  • Cinderforge — volcanic. Bring fire resistance. Level 20.\n  • Dreadmist — undead everywhere. Bring silver. Level 25.\n  • Wyrmscale — dragons. Level 30.\n  • The Abyssal Reach — void horrors. Level 40. Don't go.\n\nBook passage at the office to the east.\"",
				"options": [
					{"label": "What about the dangers?", "next": "dangers"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"sailing_tips": {
				"text": "\"First rule: prepare before you sail. Each island has a shop, but prices rise the further out you go. Stock up on potions and food here — it's cheapest at the harbor.\n\nSecond: talk to locals when you arrive. They know the terrain and the monsters better than any chart.\n\nThird: always know your way back to the dock. Getting lost on Dreadmist Isle is a death sentence.\"",
				"options": [
					{"label": "Tell me about the islands.", "next": "island_info"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"dangers": {
				"text": "\"Every island has its own breed of nasty. Sea serpents patrol the routes — you're safe on a ferry but not if you fall overboard. Sunstone has sand elementals. Emerald has poison frogs and territorial apes. Stormbreak has lightning drakes.\n\nBut the real killers? Cinderforge lava golems, Dreadmist wraiths, and Wyrmscale elder dragons. Don't tangle with those unless you're properly geared.\"",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"farewell": {
				"text": "\"Fair winds and following seas, traveler.\"\n\nCaptain Weylan turns back to his clipboard, barking orders at a passing deckhand.",
				"options": [],
			},
		},
	},

	"harbor_clerk": {
		"id": "harbor_clerk",
		"name": "Elara",
		"title": "Passage Clerk",
		"location": "harbor_master_office",
		"greeting": "A precise young woman adjusts her spectacles and looks up from a stack of manifests.\n\n\"Good day. I'm Elara, the passage clerk. I handle all travel bookings and island documentation. How may I help you?\"",
		"dialogue": {
			"root": {
				"text": None,
				"options": [
					{"label": "How do I travel to an island?", "next": "travel_info"},
					{"label": "Which island do you recommend first?", "next": "recommend"},
					{"label": "What's the chart on the wall?", "next": "chart"},
					{"label": "Goodbye.", "next": "farewell"},
				],
			},
			"travel_info": {
				"text": "\"Travel is simple. Head to the appropriate dock — north, south, east, or west — and board the ferry to your destination. Each island dock is clearly labeled.\n\nReturn ferries run from every island's dock back here. You won't be stranded... unless the dock gets destroyed, which has happened exactly once. On Dreadmist. We don't talk about it.\"",
				"options": [
					{"label": "Which island should I visit first?", "next": "recommend"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"recommend": {
				"text": "\"For a new adventurer? Sunstone Atoll, without question. Warm climate, friendly villagers, and the monsters are manageable at level 5. The Sun Temple has excellent loot for beginners.\n\nAfter that, work your way up: Emerald Isle at 10, Stormbreak at 15, and so on. Each island's dungeon matches its recommended level. Don't skip ahead — I've seen too many coffins come back on the cargo ferry.\"",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"chart": {
				"text": "\"That's the Master Chart — every known island, current, and shipping lane mapped by the Harbor Master himself. The seven main islands are marked with their difficulty levels.\n\nNotice the distances — Sunstone is closest, Wyrmscale is far to the north, and the Abyssal Reach is... well, it's off the edge of most charts. We had to extend the map twice.\"",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"farewell": {
				"text": "\"Safe travels. And do fill out the liability waiver before boarding — it's island policy.\"\n\nElara returns to her paperwork with quiet efficiency.",
				"options": [],
			},
		},
	},

	"tavern_keeper": {
		"id": "tavern_keeper",
		"name": "Barnacle Bill",
		"title": "Tavern Keeper",
		"location": "harbor_tavern",
		"greeting": "A heavyset man with an anchor tattooed on each forearm polishes a glass behind the bar.\n\n\"Ahoy! Name's Bill — Barnacle Bill, if you like. Welcome to The Salty Compass. Best grog and worst advice on the coast. What'll it be?\"",
		"dialogue": {
			"root": {
				"text": None,
				"options": [
					{"label": "Heard any rumors?", "next": "rumors"},
					{"label": "Tell me about the regulars.", "next": "regulars"},
					{"label": "Any advice for a traveler?", "next": "advice"},
					{"label": "See you around, Bill.", "next": "farewell"},
				],
			},
			"rumors": {
				"text": "Bill leans in conspiratorially.\n\n\"Rumors, eh? I hear plenty. Let's see...\n\n  • A ghost ship's been spotted near Dreadmist — crew of undead, they say.\n  • Cinderforge smiths have learned to temper metal in dragonfire.\n  • Something ancient woke up beneath Wyrmscale. The dragonkin are nervous.\n  • The druids on Emerald Isle found ruins older than their oldest trees.\n\nTake it all with a grain of sea salt.\"",
				"options": [
					{"label": "Tell me about the regulars.", "next": "regulars"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"regulars": {
				"text": "\"See that old fellow in the corner? That's Captain Aldos — sailed to every island and back. Buy him a drink and he'll talk your ear off about sea monsters.\n\nWe also get merchants, soldiers, and the occasional druid passing through. The harbor's the crossroads of the world, friend.\"",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"advice": {
				"text": "\"Best advice I can give? Eat before you sail. Seasickness on an empty stomach is a special kind of misery.\n\nAlso — the taverns on each island serve local specialties. Some of them have actual healing properties. Sunstone coconut water restores stamina, Stormbreak storm-ale gives lightning resistance, that sort of thing. Worth trying.\"",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"farewell": {
				"text": "\"Don't be a stranger! The grog's always flowing.\"\n\nBill waves his dishrag in farewell and moves on to the next customer.",
				"options": [],
			},
		},
	},

	"old_captain": {
		"id": "old_captain",
		"name": "Captain Aldos",
		"title": "Retired Sea Captain",
		"location": "harbor_tavern",
		"greeting": "A grizzled old man with a wooden leg and an eyepatch raises his mug in greeting.\n\n\"Pull up a chair, young one! Captain Aldos, retired. I've sailed every ocean and survived every storm. What would you hear about?\"",
		"dialogue": {
			"root": {
				"text": None,
				"options": [
					{"label": "Tell me about sea monsters.", "next": "sea_monsters"},
					{"label": "Which island was the most dangerous?", "next": "dangerous"},
					{"label": "Any treasure maps?", "next": "treasure"},
					{"label": "Enjoy your drink, Captain.", "next": "farewell"},
				],
			},
			"sea_monsters": {
				"text": "Aldos slams his mug down.\n\n\"Sea monsters! Now you're talking! The kraken near the Abyssal Reach took my leg AND my eye — different trips, mind you. The sea serpents between here and Stormbreak are fast but stupid — sail in zigzags.\n\nBut the worst? The fog wraiths near Dreadmist. They reach right through the hull and drain your life. Silver lanterns keep 'em at bay. ALWAYS carry silver near those waters.\"",
				"options": [
					{"label": "Which island was most dangerous?", "next": "dangerous"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"dangerous": {
				"text": "\"Dreadmist. No contest. The fog alone drives sailors mad. We lost three crew before we even docked — just vanished into the mist. The undead patrol the shores at night.\n\nBut I'll tell you a secret: Wyrmscale is worse if you're unprepared. The dragons there don't just attack — they hunt. Intelligently. Bring fire-resistant gear and pray.\"",
				"options": [
					{"label": "Any treasure maps?", "next": "treasure"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"treasure": {
				"text": "\"Ha! If I had a treasure map, would I be drinking in this dive? But I'll tell you this — every island has hidden caches. The dungeon bosses drop the real treasures, but there are secret rooms too.\n\nSearch the walls in dungeons. Look for odd-colored stones or drafts of air. I found a hidden vault in the Crystal Caverns once — nearly retired on the haul.\"",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"farewell": {
				"text": "\"May the tides favor you, young one! And remember — if it glows in the ocean, DON'T touch it!\"\n\nCaptain Aldos returns to his rum with a contented sigh.",
				"options": [],
			},
		},
	},

	# =====================================================================
	# ISLAND NPCs — Sunstone Atoll
	# =====================================================================

	"village_elder": {
		"id": "village_elder",
		"name": "Elder Kahuna",
		"title": "Village Elder",
		"location": "sunstone_village_center",
		"greeting": "An elderly man with sun-darkened skin and a crown of woven palm fronds smiles warmly.\n\n\"Aloha, traveler! I am Elder Kahuna, keeper of Sunstone Atoll. Our island welcomes all who come in peace. How may I guide you?\"",
		"dialogue": {
			"root": {
				"text": None,
				"options": [
					{"label": "Tell me about Sunstone Atoll.", "next": "island_lore"},
					{"label": "What's in the Sun Temple?", "next": "temple_info"},
					{"label": "Any advice for exploring?", "next": "explore_tips"},
					{"label": "Farewell, Elder.", "next": "farewell"},
				],
			},
			"island_lore": {
				"text": "\"Our atoll was raised from the sea by the Sun God millennia ago. The coral reefs protect us, and the jungle provides all we need. We live simply, in harmony with the tides.\n\nThe Sun Temple to the north is our most sacred place. Ancient priests built it to channel the sun's power. It still holds great magic — and great danger for the unprepared.\"",
				"options": [
					{"label": "What about the temple?", "next": "temple_info"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"temple_info": {
				"text": "\"The Sun Temple is a dungeon of three levels, filled with sun guardians and coral constructs. The deeper you go, the brighter — and more dangerous — it becomes.\n\nSeek the Solar Altar on the lowest floor. It can forge weapons of light if you bring the right materials. Speak with our Sun Priest to learn the old recipes before you enter.\"",
				"options": [
					{"label": "Any tips for exploring?", "next": "explore_tips"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"explore_tips": {
				"text": "\"The jungle has sand elementals — they're weak to water. Bring potions. The beach crabs are mostly harmless, but coral snappers can be vicious.\n\nCollect coconuts and tropical fruit as you go — they restore health and are plentiful. And stay on the paths at night. The jungle fauna is... territorial after dark.\"",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"farewell": {
				"text": "\"May the sun light your path, traveler. You are always welcome here.\"\n\nElder Kahuna bows gracefully and returns to his meditation.",
				"options": [],
			},
		},
	},

	"sun_priest": {
		"id": "sun_priest",
		"name": "Priestess Solara",
		"title": "Sun Priestess",
		"location": "sunstone_village_center",
		"greeting": "A woman in flowing golden robes stands before the sun totem, her eyes reflecting golden light.\n\n\"Greetings, seeker. I am Priestess Solara, keeper of the solar flame. The Sun God's light reveals all truths — and forges mighty weapons. Would you learn?\"",
		"dialogue": {
			"root": {
				"text": None,
				"options": [
					{"label": "Teach me the sun-forging arts.", "next": "teach_recipes"},
					{"label": "Tell me about the Sun God.", "next": "sun_lore"},
					{"label": "What dangers does the temple hold?", "next": "temple_dangers"},
					{"label": "Blessings upon you, Priestess.", "next": "farewell"},
				],
			},
			"teach_recipes": {
				"text": "Solara's hands glow with warm light as she traces ancient symbols in the air.\n\n\"The Sun God teaches through fire and light. I will share two sacred techniques:\n\n  • The Solar Blade — a sword that burns with sunfire.\n  • The Sunstone Shield — a ward against darkness and shadow.\n\nSeek the Solar Altar in the temple depths to forge these. You will need sunstone cores and golden essence.\"",
				"effects": {
					"learn_recipes": ["solar_blade", "sunstone_shield"],
				},
				"options": [
					{"label": "Tell me about the Sun God.", "next": "sun_lore"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"sun_lore": {
				"text": "\"The Sun God raised this atoll from the ocean floor as a beacon of light. The temple was built to channel divine energy — it powers our crops, our wards, and our very way of life.\n\nBut the deeper chambers were sealed long ago. The guardians there are remnants of the old priesthood, corrupted by too much power. They attack all who enter. Tread carefully.\"",
				"options": [
					{"label": "What dangers await in the temple?", "next": "temple_dangers"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"temple_dangers": {
				"text": "\"Sun guardians are armored in light — they resist fire and holy damage, but shadow and ice can crack their shells. Coral constructs are slow but hit hard. Use speed and dodge their charges.\n\nThe temple boss, the Solar Sovereign, channels a beam of pure sunlight. Stay behind the pillars. Strike when the beam fades. And bring sunburn salve — I'm not joking.\"",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"farewell": {
				"text": "\"Walk in the light, seeker. The Sun God watches over all who carry his flame.\"\n\nSolara turns back to the sun totem, resuming her quiet prayers.",
				"options": [],
			},
		},
	},

	"weapons_trainer": {
		"id": "weapons_trainer",
		"name": "Kai Ironshore",
		"title": "Combat Trainer",
		"location": "sunstone_village_training",
		"greeting": "A muscular warrior with coral-studded bracers and a weathered trident plants his weapon in the sand.\n\n\"You look like you could use some training. I'm Kai Ironshore — I've fought every creature on this atoll and most of the ones in the sea. Let's see what you've got.\"",
		"dialogue": {
			"root": {
				"text": None,
				"options": [
					{"label": "Teach me island combat techniques.", "next": "teach_combat"},
					{"label": "What weapons work best here?", "next": "weapon_advice"},
					{"label": "How do I fight in the temple?", "next": "temple_combat"},
					{"label": "Thanks for the training, Kai.", "next": "farewell"},
				],
			},
			"teach_combat": {
				"text": "Kai demonstrates a series of swift strikes with his trident.\n\n\"Island fighting is about speed and reach. Let me show you how to craft the tools of the trade:\n\n  • The Coral Trident — light, fast, and lethal in the right hands.\n  • Shell Armor — made from giant turtle shells. Tougher than it looks.\n\nGather coral fragments and turtle shells from the reef and beaches. I'll show you the rest.\"",
				"effects": {
					"learn_recipes": ["coral_trident", "shell_armor"],
				},
				"options": [
					{"label": "What about temple combat?", "next": "temple_combat"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"weapon_advice": {
				"text": "\"On the atoll? Piercing weapons — tridents, spears, daggers. The sand elementals are loose and shifty, so slashing does nothing. You need to stab through their core.\n\nAgainst coral constructs, use blunt weapons. A good mace shatters coral faster than any sword. And in the water? Reach weapons. You do NOT want a shark at arm's length.\"",
				"options": [
					{"label": "How about temple fighting?", "next": "temple_combat"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"temple_combat": {
				"text": "\"The temple guardians are tough. They're fast, armored, and they hit like a falling mast. My advice:\n\n  • Keep moving. They telegraph their attacks with a golden glow.\n  • Use the narrow corridors to fight them one at a time.\n  • Bring plenty of healing. The deeper floors have no rest spots.\n  • The boss has a sunbeam attack — hide behind pillars when it charges up.\n\nAnd if you find the Solar Altar, you can forge a Solar Blade. That thing cuts through guardians like butter.\"",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"farewell": {
				"text": "\"Keep your guard up and your blade sharp, fighter. The sea doesn't forgive the sloppy.\"\n\nKai retrieves his trident and resumes drilling against a practice dummy.",
				"options": [],
			},
		},
	},

	# =====================================================================
	# ISLAND NPCs — Emerald Isle
	# =====================================================================

	"druid_elder": {
		"id": "druid_elder",
		"name": "Archdruid Thalwen",
		"title": "Elder of the Green Circle",
		"location": "emerald_village_center",
		"greeting": "An ancient figure wrapped in living bark and flowering vines regards you with eyes like forest pools.\n\n\"The trees told me you were coming, outlander. I am Archdruid Thalwen. The Green Circle welcomes those who respect nature. What brings you to our canopy?\"",
		"dialogue": {
			"root": {
				"text": None,
				"options": [
					{"label": "Tell me about Emerald Isle.", "next": "island_lore"},
					{"label": "What lies in the jungle ruins?", "next": "ruins_info"},
					{"label": "How does druid magic work?", "next": "druid_magic"},
					{"label": "I must go. Farewell, Archdruid.", "next": "farewell"},
				],
			},
			"island_lore": {
				"text": "\"This island was old when the first druids arrived. The titan oaks are thousands of years old, and the ruins in the deep jungle are older still — built by a civilization that vanished before written history.\n\nWe druids are caretakers. The jungle provides — herbs, wood, shelter — but it also hunts. Respect the green, and the green will sustain you. Disrespect it, and the vines will drag you down.\"",
				"options": [
					{"label": "Tell me about the ruins.", "next": "ruins_info"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"ruins_info": {
				"text": "\"The Verdant Labyrinth — a dungeon beneath the old ruins. Three floors of overgrown corridors, trap-laden halls, and creatures warped by ancient magic.\n\nA druid scholar is studying the ruins' library. Speak with him there — he's translating tablets that may unlock sealed chambers. The deepest floor holds a Nature Altar for crafting living-wood items.\"",
				"options": [
					{"label": "How does druid magic work?", "next": "druid_magic"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"druid_magic": {
				"text": "\"We channel the life force of the island itself. Every root, every leaf, every creature is connected through the ley lines. Our magic heals, protects, and grows.\n\nBut we also fight, when we must. Nature is not gentle — thorns, poisons, crushing vines. Visit our healer to learn remedies, and our ranger trainer for combat techniques. The jungle is our greatest weapon and our greatest teacher.\"",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"farewell": {
				"text": "\"May the roots hold you and the canopy shelter you, outlander.\"\n\nThalwen closes his eyes, and for a moment the vines around him seem to sway in greeting — or farewell.",
				"options": [],
			},
		},
	},

	"druid_healer": {
		"id": "druid_healer",
		"name": "Ceridwen",
		"title": "Druid Healer",
		"location": "emerald_village_healer",
		"greeting": "A serene woman with moss-green hair stirs a bubbling cauldron of luminescent sap.\n\n\"Ah, you look weary, traveler. I am Ceridwen, healer of the Green Circle. Let me share the wisdom of the forest — every wound has a remedy growing somewhere nearby.\"",
		"dialogue": {
			"root": {
				"text": None,
				"options": [
					{"label": "Teach me jungle remedies.", "next": "teach_remedies"},
					{"label": "What herbs grow here?", "next": "herb_info"},
					{"label": "How do I survive the deep jungle?", "next": "survival_tips"},
					{"label": "Thank you, Ceridwen.", "next": "farewell"},
				],
			},
			"teach_remedies": {
				"text": "Ceridwen selects herbs from her collection with practiced hands.\n\n\"The jungle provides powerful medicine. Let me teach you two essential recipes:\n\n  • Jungle Remedy — cures poison AND restores health. Made from moonpetal and thornroot.\n  • Nature Ward — a protective charm against nature magic and beast attacks.\n\nGather moonpetals from the herbalist's garden and thornroot from the deep jungle floor.\"",
				"effects": {
					"learn_recipes": ["jungle_remedy", "nature_ward"],
				},
				"options": [
					{"label": "What herbs should I look for?", "next": "herb_info"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"herb_info": {
				"text": "\"The island is rich with medicinal plants:\n\n  • Moonpetal — glows silver at night. Heals wounds and purifies toxins.\n  • Heartbloom — a pulsing red flower. Restores stamina.\n  • Frostmint — cooling herb. Reduces fever and fire damage.\n  • Thornroot — deep jungle ground cover. Essential for wards.\n  • Fungal extract — from the mushroom fields. Powerful but unpredictable.\n\nThe herbalist's garden has cultivated samples, but the wild variants in the jungle are more potent.\"",
				"options": [
					{"label": "How do I survive the deep jungle?", "next": "survival_tips"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"survival_tips": {
				"text": "\"The deep jungle is hostile. Poison dart frogs are everywhere — an antidote is essential. Giant spiders spin webs across paths — carry a blade to cut free.\n\nThe apex predators are the jungle raptors. They hunt in packs and are smart enough to flank you. Fight with your back to a tree. And NEVER eat unidentified mushrooms — some explode with spore poison.\"",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"farewell": {
				"text": "\"The forest watches over those who listen to it. Go well, traveler.\"\n\nCeridwen returns to her cauldron, humming an old druidic lullaby.",
				"options": [],
			},
		},
	},

	"druid_ranger_trainer": {
		"id": "druid_ranger_trainer",
		"name": "Fenwick Thornwalker",
		"title": "Druid Ranger",
		"location": "emerald_village_training",
		"greeting": "A wiry druid with camouflage tattoos and a staff of living wood watches you approach with keen eyes.\n\n\"You move loudly, outlander. I could hear you from three platforms away. I'm Fenwick — I train rangers for jungle patrol. Want to learn how the forest fights?\"",
		"dialogue": {
			"root": {
				"text": None,
				"options": [
					{"label": "Teach me jungle combat.", "next": "jungle_combat"},
					{"label": "What creatures should I watch for?", "next": "creatures"},
					{"label": "How do you navigate the jungle?", "next": "navigation"},
					{"label": "Good hunting, Fenwick.", "next": "farewell"},
				],
			},
			"jungle_combat": {
				"text": "\"In the jungle, you don't fight fair — you fight smart. Use the terrain. Vines can trip your enemies. Branches can block charges. Mud slows heavy creatures.\n\nStrike fast and withdraw. Most jungle beasts will lose interest if you break line of sight. Don't stand and trade blows with a jungle troll — you'll lose every time.\n\nLearn to craft traps from vine and thorns. Set them on patrol routes and let the jungle do your killing.\"",
				"options": [
					{"label": "What creatures are dangerous?", "next": "creatures"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"creatures": {
				"text": "\"Here's the hierarchy:\n\n  • Insects and frogs — annoying, poisonous, but fragile.\n  • Jungle apes — territorial, hit hard, but dumb.\n  • Giant spiders — fast, poisonous, set ambushes.\n  • Jungle raptors — pack hunters. The worst.\n  • Verdant Guardians — ancient tree spirits in the ruins. Very tough.\n\nThe dungeon adds corrupted versions of these plus temple constructs. Bring antidotes and nature wards for everything.\"",
				"options": [
					{"label": "How do you navigate the jungle?", "next": "navigation"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"navigation": {
				"text": "\"Moss grows thickest on the north side of trees. Waterfalls always flow downhill to the coast — follow them to find your way back. The druid trail markers are carved into bark every fifty paces along main paths.\n\nIn the ruins, look for the druid scholar's chalk marks on the walls. He's mapped most of the upper levels. And keep a torch lit — the canopy blocks all sunlight in the deep jungle.\"",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"farewell": {
				"text": "\"Tread softly and carry a sharp blade, outlander. The jungle respects neither the loud nor the careless.\"\n\nFenwick vanishes into the foliage with unsettling silence.",
				"options": [],
			},
		},
	},

	"beast_handler": {
		"id": "beast_handler",
		"name": "Bramwick",
		"title": "Beast Handler",
		"location": "emerald_village_stables",
		"greeting": "A stocky druid covered in claw marks and bite scars grins as he feeds a giant beetle.\n\n\"Easy, Crunch! That's a friend, not a snack. Sorry about that — I'm Bramwick. I care for the tame beasts. Want to know about the island's creatures?\"",
		"dialogue": {
			"root": {
				"text": None,
				"options": [
					{"label": "What animals do you keep?", "next": "animals"},
					{"label": "How do you tame jungle beasts?", "next": "taming"},
					{"label": "What should I avoid in the wild?", "next": "avoid"},
					{"label": "Keep up the good work, Bramwick.", "next": "farewell"},
				],
			},
			"animals": {
				"text": "\"We've got quite the menagerie! Giant riding beetles — slow but armored like a tank. Moss-bears — gentle unless provoked. Canopy monkeys — clever little thieves that make great scouts.\n\nThe prize of the stable is old Thunderfoot, our armored lizard. Took three druids and a barrel of enchanted grain to calm him down. Now he's gentle as a kitten. A kitten that weighs eight hundred pounds.\"",
				"options": [
					{"label": "Can I tame my own beast?", "next": "taming"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"taming": {
				"text": "\"Taming's an art. You need patience, enchanted grain, and ideally a nature ward so the animal doesn't sense your fear. Start with something small — a beetle or monkey.\n\nThe key is the enchanted grain. Regular food makes them friendly for about ten seconds. Enchanted grain creates a bond. We grow it right here in the village.\"",
				"options": [
					{"label": "What should I avoid?", "next": "avoid"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"avoid": {
				"text": "\"The alpha raptor in the eastern jungle. It's twice the size of the pack raptors and mean as a landslide. The druids have a truce with it — we stay out of its territory, it stays out of ours.\n\nAlso, the guardian treants near the ruins. They look like normal trees until you get close. If a tree has glowing sap veins... that's not a tree. Back away slowly.\"",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"farewell": {
				"text": "\"Come back anytime! Crunch loves visitors. Well, loves sniffing visitors. Same thing!\"\n\nBramwick goes back to feeding the giant beetle, humming cheerfully.",
				"options": [],
			},
		},
	},

	"druid_scholar": {
		"id": "druid_scholar",
		"name": "Orin Mosscript",
		"title": "Druid Scholar",
		"location": "emerald_ruins_library",
		"greeting": "A bespectacled druid looks up from a stone tablet, ink-stained fingers clutching a quill.\n\n\"Oh! A visitor! Wonderful! I'm Orin — Orin Mosscript. I've been translating these ancient tablets for three years. The civilization that built these ruins was extraordinary. Do you want to hear what I've found?\"",
		"dialogue": {
			"root": {
				"text": None,
				"options": [
					{"label": "What have you discovered?", "next": "discoveries"},
					{"label": "Tell me about the ruins.", "next": "ruins"},
					{"label": "Any secrets hidden in the tablets?", "next": "secrets"},
					{"label": "Good luck with the research, Orin.", "next": "farewell"},
				],
			},
			"discoveries": {
				"text": "\"The builders called themselves the Verdant Architects. They could grow stone like plants — shaping temples, walls, and entire cities from living rock. Their magic blended nature and architecture.\n\nThey vanished suddenly. The tablets describe a 'great unraveling' — their magic turned against them. The constructs they built to guard the temple went berserk. That's why the ruins are so dangerous now.\"",
				"options": [
					{"label": "Tell me about the ruins.", "next": "ruins"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"ruins": {
				"text": "\"The ruins are extensive — what you see on the surface is barely a tenth of it. Underground, the Verdant Labyrinth stretches for ages. Three main levels, each deeper and more warped.\n\nI've marked the safe paths with chalk on the upper level. Look for my marks — white arrows on the walls. Below that... you're on your own. The constructs don't bother me because I sit still. They chase movement.\"",
				"options": [
					{"label": "Any tablet secrets?", "next": "secrets"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"secrets": {
				"text": "\"One tablet mentions a 'Seed of the World Tree' hidden on the lowest floor — a crafting material of immense power. The Nature Altar down there can reportedly create living weapons that grow stronger over time.\n\nAnother tablet warns of 'the Warden' — a massive construct that guards the final chamber. It can regenerate from any wound unless you destroy its core. Look for a glowing green crystal in its chest.\"",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"farewell": {
				"text": "\"Oh, going already? Well, if you find any stone tablets deeper in, bring them to me! I'll translate them for you. Knowledge is the greatest treasure!\"\n\nOrin dives back into his work with scholarly enthusiasm.",
				"options": [],
			},
		},
	},

	# =====================================================================
	# ISLAND NPCs — Stormbreak Island
	# =====================================================================

	"reef_town_crier": {
		"id": "reef_town_crier",
		"name": "Gull McGraw",
		"title": "Town Crier",
		"location": "stormbreak_town_center",
		"greeting": "A wiry man in a weather-beaten oilskin coat rings a brass bell.\n\n\"HEAR YE, HEAR YE! Oh — just you? Right then. I'm Gull McGraw, town crier and general information source. What do you need to know about Stormbreak?\"",
		"dialogue": {
			"root": {
				"text": None,
				"options": [
					{"label": "What's happening on Stormbreak?", "next": "news"},
					{"label": "How do people survive the storms?", "next": "storm_survival"},
					{"label": "Where should I explore?", "next": "explore"},
					{"label": "Carry on, Gull.", "next": "farewell"},
				],
			},
			"news": {
				"text": "\"Latest news! The lightning struck the bell tower AGAIN — third time this month. The storm smith forged a new lightning rod but the drakes keep stealing them for nests.\n\nAlso, sailors report increased reef serpent activity near the coral labyrinth. And the Storm Elder is offering bounties on thunder elementals. If you can handle the shock, there's gold in it.\"",
				"options": [
					{"label": "How do people survive here?", "next": "storm_survival"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"storm_survival": {
				"text": "\"Rule one: NEVER stand on high ground during a storm. Lightning doesn't strike randomly here — it hunts. The copper rods on the rooftops redirect most of it, but out in the open? You're a target.\n\nRule two: the cellars are your friend. When the storm-bell rings three times, get underground.\n\nRule three: wear rubber-soled boots. The storm smith sells them. Best investment you'll ever make.\"",
				"options": [
					{"label": "Where should I explore?", "next": "explore"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"explore": {
				"text": "\"The coral labyrinth to the east is full of treasure — and reef serpents. The thunder cliffs to the north are where the lightning drakes nest. Good loot, bad survival odds.\n\nThe Tempest Depths dungeon is beneath the cliffs. Three floors of storm-charged madness. The Storm Elder can tell you more about what's down there. Just... don't go during a storm. The dungeon floods with electric water.\"",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"farewell": {
				"text": "\"HEAR YE, HEAR YE! The traveler departs! May lightning miss you and the wind be at your back!\"\n\nGull resumes ringing his bell and shouting the day's news.",
				"options": [],
			},
		},
	},

	"storm_healer": {
		"id": "storm_healer",
		"name": "Nerissa Tidecaller",
		"title": "Storm Healer",
		"location": "stormbreak_town_healer",
		"greeting": "A calm woman with blue-tinged skin and hair that floats as if underwater hums a sailor's hymn over a jar of glowing salve.\n\n\"Lightning burns again? Reef cuts? Or just the usual electric tingling in your bones? I'm Nerissa. I heal what the storms break.\"",
		"dialogue": {
			"root": {
				"text": None,
				"options": [
					{"label": "How do you heal lightning burns?", "next": "healing_info"},
					{"label": "What should I carry for the storms?", "next": "preparation"},
					{"label": "Tell me about reef injuries.", "next": "reef_injuries"},
					{"label": "Stay safe, Nerissa.", "next": "farewell"},
				],
			},
			"healing_info": {
				"text": "\"Lightning burns are different from fire burns. They branch through the body like tree roots under the skin. My luminous salve draws the residual charge out — painful but effective.\n\nFor self-treatment in the field, kelp poultices work in a pinch. Wrap the burn, apply pressure, and stay out of further storms. The charge can accumulate in your body and the second strike is always worse.\"",
				"options": [
					{"label": "What should I carry?", "next": "preparation"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"preparation": {
				"text": "\"For exploring Stormbreak, you need:\n\n  • Lightning salve — for burns. I sell it here.\n  • Kelp poultices — field dressings. Cheap and effective.\n  • Rubber-soled boots — reduces shock damage.\n  • A copper grounding rod — plant it in the ground near you during storms.\n  • Healing potions — always, always bring healing potions.\n\nAnd if you're heading into the Tempest Depths, double everything. That dungeon is brutal.\"",
				"options": [
					{"label": "Tell me about reef injuries.", "next": "reef_injuries"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"reef_injuries": {
				"text": "\"Coral cuts are nasty — they get infected by sea bacteria if not treated quickly. Clean the wound with salt water, apply kelp poultice, and keep it dry.\n\nReef serpent bites are venomous. The venom causes paralysis within minutes. Carry antidote at all times near the coral labyrinth. If you can't cure it fast, the serpents will circle back for an easy meal.\"",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"farewell": {
				"text": "\"Be careful out there. Come back in one piece — I'm a healer, not a miracle worker.\"\n\nNerissa resumes her quiet hymn, hands moving steadily over her remedies.",
				"options": [],
			},
		},
	},

	"storm_elder": {
		"id": "storm_elder",
		"name": "Elder Galecrest",
		"title": "Storm Elder",
		"location": "stormbreak_town_elder",
		"greeting": "A imposing figure sits on a throne of coral and driftwood. His white beard crackles with static electricity.\n\n\"I am Elder Galecrest. I've governed Stormbreak for forty years — through hurricanes, drake raids, and worse. Speak, traveler. What would you know?\"",
		"dialogue": {
			"root": {
				"text": None,
				"options": [
					{"label": "Tell me about the Tempest Depths.", "next": "dungeon_info"},
					{"label": "What threatens Stormbreak?", "next": "threats"},
					{"label": "How did you build a town here?", "next": "history"},
					{"label": "Farewell, Elder.", "next": "farewell"},
				],
			},
			"dungeon_info": {
				"text": "\"The Tempest Depths lie beneath the thunder cliffs. Three floors of storm-charged caverns. The walls themselves conduct electricity — touch the wrong surface and you'll light up like a lantern.\n\nThe deepest floor holds the Storm Forge — an altar that harnesses lightning to temper weapons. Speak to our smith for the forging recipes. The dungeon boss, the Tempest Lord, controls the weather within. Defeating it calms the storms... temporarily.\"",
				"options": [
					{"label": "What threatens the island?", "next": "threats"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"threats": {
				"text": "\"Lightning drakes are our constant enemy — they nest on the cliffs and raid the town for metal. Reef serpents menace our fishers. Thunder elementals form during the worst storms and wander destructively.\n\nBut the real threat is the Tempest Lord itself. When it stirs, the storms intensify tenfold. We've lost buildings, ships, even entire sections of the reef. Every few years, a brave group ventures down to drive it back.\"",
				"options": [
					{"label": "How did this town survive?", "next": "history"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"history": {
				"text": "\"Shipwrecked sailors founded Reef Town three generations ago. We built from what the sea gave us — wreckage, coral, driftwood. The storms haven't stopped since.\n\nWe survive by adaptation. Copper rods on every roof. Underground shelters. A smith who forges tools from storm-tempered iron. We're not comfortable, but we're alive. And the storm crystals the island produces are worth a fortune on the mainland.\"",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"farewell": {
				"text": "\"May the storm pass over you and the tide carry you home, traveler.\"\n\nElder Galecrest's eyes drift to the storm charts on the wall, calculating the next tempest.",
				"options": [],
			},
		},
	},

	"storm_smith": {
		"id": "storm_smith",
		"name": "Voltra Strikehammer",
		"title": "Storm Smith",
		"location": "stormbreak_town_smithy",
		"greeting": "A powerfully built woman with singed eyebrows and copper-threaded hair hammers a glowing blade on a lightning-struck anvil. Sparks arc between her tools.\n\n\"Hold on — CLANG — almost — CLANG — there! Another thunder-edge, done. You want something forged, or just watching the sparks?\"",
		"dialogue": {
			"root": {
				"text": None,
				"options": [
					{"label": "Teach me storm-forging.", "next": "teach_forging"},
					{"label": "How does lightning forging work?", "next": "lightning_forge"},
					{"label": "What materials do you need?", "next": "materials"},
					{"label": "Keep hammering, Voltra.", "next": "farewell"},
				],
			},
			"teach_forging": {
				"text": "Voltra's eyes light up with literal sparks.\n\n\"Now you're talking! I can teach you the storm-tempering arts:\n\n  • Storm Blade — a sword that crackles with lightning. Shocks enemies on hit.\n  • Thunder Shield — absorbs electrical damage and stores it for a counter-discharge.\n\nYou'll need storm iron ingots and storm crystals. Find them in the Tempest Depths or buy them at the market. Bring them to the Storm Forge on the lowest dungeon floor.\"",
				"effects": {
					"learn_recipes": ["storm_blade", "thunder_shield"],
				},
				"options": [
					{"label": "How does lightning forging work?", "next": "lightning_forge"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"lightning_forge": {
				"text": "\"It's simple — and by simple I mean incredibly dangerous. The copper rods on my roof attract lightning strikes. I channel that energy through insulated tongs into the metal at the exact moment of tempering.\n\nThe metal absorbs the charge permanently. Storm-forged weapons never rust, never dull, and carry a residual shock. The Storm Forge in the dungeon does the same thing but with ten times the power. That's where you make the REAL weapons.\"",
				"options": [
					{"label": "What materials do you need?", "next": "materials"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"materials": {
				"text": "\"For storm-forging:\n\n  • Storm iron ingots — found in the Tempest Depths or smelted from ore on the cliffs.\n  • Storm crystals — harvested from crystal formations during storms.\n  • Copper rods — I make these myself, but the market sells them.\n  • Reef coral — for hilts and grips. Insulates against shock.\n\nBring any combination and I'll tell you what we can make.\"",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"farewell": {
				"text": "\"Watch for lightning on the way out! And if you find any storm iron in the dungeon, bring it here — I pay top coin!\"\n\nVoltra turns back to her anvil as another lightning bolt strikes the copper rod overhead.",
				"options": [],
			},
		},
	},

	# =====================================================================
	# ISLAND NPCs — Cinderforge Island
	# =====================================================================

	"cinder_elder": {
		"id": "cinder_elder",
		"name": "Magister Pyrra",
		"title": "Cinderforge Elder",
		"location": "cinder_village_elder",
		"greeting": "A stately woman draped in fire-silk robes sits on a throne of cooled magma. The air around her shimmers with heat.\n\n\"I am Magister Pyrra, keeper of Cinderforge. Few travelers brave the volcanic lands. You must be either very brave or very foolish. Perhaps both. What do you seek?\"",
		"dialogue": {
			"root": {
				"text": None,
				"options": [
					{"label": "Teach me volcanic forging.", "next": "teach_forging"},
					{"label": "Tell me about Cinderforge Island.", "next": "island_lore"},
					{"label": "What's in the Molten Crucible?", "next": "dungeon_info"},
					{"label": "I'll take my leave, Magister.", "next": "farewell"},
				],
			},
			"teach_forging": {
				"text": "Pyrra's hands glow with inner fire as she speaks.\n\n\"Obsidian is the heart of Cinderforge. Shaped in magma, cooled in volcanic spring, it holds an edge sharper than any steel. I will teach you:\n\n  • Obsidian Blade — a weapon of volcanic glass. Cuts through armor.\n  • Magma Shield — forged from basalt and fire crystal. Heavy but nearly indestructible.\n\nGather obsidian shards from the lava fields and fire crystals from the Molten Crucible.\"",
				"effects": {
					"learn_recipes": ["obsidian_blade", "magma_shield"],
				},
				"options": [
					{"label": "Tell me about the island.", "next": "island_lore"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"island_lore": {
				"text": "\"Cinderforge was built on the rim of an active volcano by the dwarven forge-masters three centuries ago. When the dwarves vanished into the deep, the human settlers carried on their traditions.\n\nThe volcano provides everything — heat for our forges, obsidian for our tools, hot springs for our baths. It also provides danger. Lava flows shift unpredictably. Fire elementals roam the upper slopes. And the things that live in the magma tunnels below... well, that's what the Molten Crucible is for.\"",
				"options": [
					{"label": "Tell me about the Molten Crucible.", "next": "dungeon_info"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"dungeon_info": {
				"text": "\"The Molten Crucible is our volcano dungeon — three floors of magma tunnels, lava lakes, and obsidian halls. The dwarves built the original forges there, and their guardian constructs still patrol.\n\nThe deepest floor holds the Eternal Forge — a crafting altar powered by the volcano's heart. The boss, a Magma Titan, guards it. Bring fire-resistant gear and cold-based weapons. And for the love of the forge, don't fall into the lava.\"",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"farewell": {
				"text": "\"Walk carefully on the cinder paths, traveler. The ground is not always as solid as it appears.\"\n\nMagister Pyrra returns to studying the fire-silk tapestries that tell her island's history.",
				"options": [],
			},
		},
	},

	# =====================================================================
	# ISLAND NPCs — Dreadmist Isle
	# =====================================================================

	"elder_morvaine": {
		"id": "elder_morvaine",
		"name": "Elder Morvaine",
		"title": "Village Elder of Dreadmist",
		"location": "dreadmist_village_elder",
		"greeting": "A gaunt man with hollow eyes and silver-streaked hair sits behind a desk piled with protection wards. The fire in his hearth flickers cold blue.\n\n\"Close the door. Quickly. I am Elder Morvaine. If you've come to Dreadmist, you're either hunting the undead or fleeing something worse. Which is it?\"",
		"dialogue": {
			"root": {
				"text": None,
				"options": [
					{"label": "Tell me about the undead threat.", "next": "undead_lore"},
					{"label": "How does the village survive?", "next": "survival"},
					{"label": "What's in the Halls of the Damned?", "next": "dungeon_info"},
					{"label": "Stay safe, Elder.", "next": "farewell"},
				],
			},
			"undead_lore": {
				"text": "\"The fog IS the curse. It seeped from the catacombs beneath the old castle centuries ago when a necromancer broke the seals. Now the dead don't stay dead. Every corpse buried on this island has a chance of rising.\n\nThe fog drains life, confuses the mind, and hides the undead until they're upon you. Silver weapons hurt them. Holy water burns them. Sunlight drives the lesser ones back. But the greater undead — wraiths, death knights — those require stronger methods.\"",
				"options": [
					{"label": "How does the village survive?", "next": "survival"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"survival": {
				"text": "\"Barely. We salt every doorstep, ward every window, and burn silver incense at dusk. Sister Adela's blessings protect the village perimeter, but the wards weaken over time.\n\nGrimhelm forges silver weapons for the militia. Old Morteus tends the crypts — keeping the recently dead from joining the horde. And I... I study the old texts, looking for a way to seal the catacombs permanently.\n\nWe don't sleep well on Dreadmist. But we survive.\"",
				"options": [
					{"label": "What about the dungeon?", "next": "dungeon_info"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"dungeon_info": {
				"text": "\"The Halls of the Damned — the catacombs beneath the old castle. Three floors of tombs, crypts, and sacrificial chambers. The necromancer's throne room is at the bottom.\n\nThe undead there are far stronger than the surface ones. Pack silver weapons, holy water, and plenty of light sources. Shadows are their allies. And if you reach the bottom... the Lich Lord awaits. It's the source of the fog. Destroy it, and maybe — maybe — this island can heal.\"",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"farewell": {
				"text": "\"Lock your door tonight. Salt the threshold. And if you hear scratching at the window... don't open it.\"\n\nMorvaine's hollow eyes return to his protection wards, muttering incantations.",
				"options": [],
			},
		},
	},

	"sister_adela": {
		"id": "sister_adela",
		"name": "Sister Adela",
		"title": "Priestess of the Light",
		"location": "dreadmist_village_healer",
		"greeting": "A stern woman in white vestments stained with old blood and candlewax looks up from blessing a patient.\n\n\"Another one. You don't yet carry the pallor of the curse, so there's hope. I am Sister Adela. I mend wounds of flesh and spirit here. Speak — but know that frivolous questions waste time better spent on the dying.\"",
		"dialogue": {
			"root": {
				"text": None,
				"options": [
					{"label": "How do I protect myself from the undead?", "next": "protection"},
					{"label": "What is the curse of Dreadmist?", "next": "curse_info"},
					{"label": "Can you heal spiritual wounds?", "next": "spiritual"},
					{"label": "Light guide you, Sister.", "next": "farewell"},
				],
			},
			"protection": {
				"text": "\"Silver. Holy water. Faith. Those are your weapons against the dead.\n\n  • Silver weapons cut through undead flesh where normal steel passes through.\n  • Holy water burns them like acid. Splash it on wraiths to make them solid.\n  • Blessed bandages heal the necrotic rot their claws inflict.\n  • Warding talismans reduce the fog's life-draining effect.\n\nGrimhelm at the forge can arm you with silver. I can bless your water and bandages. Do not enter the catacombs without both.\"",
				"options": [
					{"label": "What is the curse?", "next": "curse_info"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"curse_info": {
				"text": "\"Three centuries ago, the Necromancer Valdris breached the veil between life and death beneath the old castle. The fog that poured out was his doing — a miasma of death energy that sustains the undead and slowly kills the living.\n\nThe longer you stay on Dreadmist, the more the curse affects you. Nightmares first. Then cold sweats. Then the pallor — your skin turns grey. After that... you don't want to know. Keep moving. Don't linger.\"",
				"options": [
					{"label": "Can you heal the curse?", "next": "spiritual"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"spiritual": {
				"text": "\"I can slow the curse, not cure it. Only destroying the Lich Lord in the deepest catacomb can end it. My blessings keep the fog at bay for a time. My smelling salts clear the mind of its whispers.\n\nBut true healing? That requires ending the source. Every day the fog persists, more dead rise. More villagers fall ill. Time is not our ally, traveler.\"",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"farewell": {
				"text": "\"May the light hold fast in the darkness. And if you venture into the catacombs... come back alive. I have enough ghosts haunting my doorstep.\"\n\nSister Adela turns back to her patients, murmuring prayers of protection.",
				"options": [],
			},
		},
	},

	"grimhelm": {
		"id": "grimhelm",
		"name": "Grimhelm",
		"title": "Silver Weaponsmith",
		"location": "dreadmist_village_smith",
		"greeting": "A massive, scarred man etches protective runes into a silver-edged blade. His forge burns with a pale, bluish flame.\n\n\"You need weapons that kill the dead? Good. I'm Grimhelm. Every blade I forge is made to end what should have stayed buried. Let me show you what I know.\"",
		"dialogue": {
			"root": {
				"text": None,
				"options": [
					{"label": "Teach me to forge silver weapons.", "next": "teach_forging"},
					{"label": "Why silver against undead?", "next": "silver_lore"},
					{"label": "What runes do you use?", "next": "rune_info"},
					{"label": "Keep up the fight, Grimhelm.", "next": "farewell"},
				],
			},
			"teach_forging": {
				"text": "Grimhelm pulls two diagrams from a rack above his anvil.\n\n\"Two recipes. Learn them well — they'll save your life down here:\n\n  • Silver Sword — the standard undead-slayer. Silver-edged steel with a blessed core.\n  • Death Ward — an amulet that repels lesser undead on sight. They won't even approach you.\n\nYou'll need silver ingots, blessed iron, and holy water. Forge them at any altar, but the effect is strongest at the catacombs' Soul Altar.\"",
				"effects": {
					"learn_recipes": ["silver_sword", "death_ward"],
				},
				"options": [
					{"label": "Why silver?", "next": "silver_lore"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"silver_lore": {
				"text": "\"Silver is anathema to undead — always has been. The metal is pure in a way that iron and steel aren't. It disrupts the necrotic energy that animates them.\n\nA normal sword passes through a wraith like smoke. A silver sword? It cuts them like flesh. The purer the silver, the more it burns. That's why I alloy it carefully — too little silver fails, too much makes the blade brittle.\"",
				"options": [
					{"label": "Tell me about the runes.", "next": "rune_info"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"rune_info": {
				"text": "\"Every blade I forge carries three runes:\n\n  • The Seal of Binding — prevents the slain from rising again.\n  • The Mark of Light — makes the blade glow near undead. Warning system.\n  • The Ward of Will — protects the wielder's mind from the Lich Lord's whispers.\n\nI learned these from Sister Adela's prayer books. The old faith had more combat applications than most people realize.\"",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"farewell": {
				"text": "\"Every blade I forge is one more dead thing that stays dead. Come back when you need more steel.\"\n\nGrimhelm returns to his pale-burning forge, the ring of hammer on silver echoing through the fog.",
				"options": [],
			},
		},
	},

	"old_morteus": {
		"id": "old_morteus",
		"name": "Old Morteus",
		"title": "Crypt Keeper",
		"location": "dreadmist_village_crypt_keeper",
		"greeting": "A hunched old man with rheumy eyes and gnarled hands looks up from a ledger of burial records.\n\n\"Eh? A visitor? Don't get many of those. Understandable — nobody wants to visit the crypt keeper. I'm Morteus. I keep the dead in their graves. Mostly. What do you want?\"",
		"dialogue": {
			"root": {
				"text": None,
				"options": [
					{"label": "How do you keep the dead from rising?", "next": "methods"},
					{"label": "What do you know about the catacombs?", "next": "catacomb_info"},
					{"label": "Tell me about the Lich Lord.", "next": "lich_info"},
					{"label": "Rest well, Morteus.", "next": "farewell"},
				],
			},
			"methods": {
				"text": "\"Salt in the coffin. Silver coins on the eyes. Iron nails through the shroud. And prayer — lots of prayer. Doesn't always work, mind you. The fog's too strong some nights.\n\nWhen one gets up despite all that, I deal with it. Shovel to the neck works on fresh ones. For the older dead, you need silver. I keep a blessed mace by my bed. Hasn't failed me yet. Thirty years of crypt keeping and all my fingers.\"",
				"options": [
					{"label": "What about the catacombs?", "next": "catacomb_info"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"catacomb_info": {
				"text": "\"I've been to the first level. Only the first. The upper crypts I maintain — I re-seal tombs, replace wards, clear out the occasional skeleton that wakes up confused.\n\nBelow that? The old catacombs. Thousands of dead from the ancient war, all corrupted by the Lich Lord's magic. I heard sounds from down there — grinding stone, whispering voices, the drag of bone on bone. I nailed that door shut and I'm not opening it.\"",
				"options": [
					{"label": "Tell me about the Lich Lord.", "next": "lich_info"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"lich_info": {
				"text": "\"Valdris. The Lich Lord. He was a scholar once — studied death magic to try to save his dying wife. Failed. Went mad. Decided if he couldn't save one life, he'd conquer death itself.\n\nHe succeeded, in the worst way possible. Now he sits on a throne of bones three floors down, surrounded by his army of the dead. He can't leave the catacombs — the wards hold him in. But the fog spreads further every year. Eventually, the wards will fail entirely.\"",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"farewell": {
				"text": "\"Don't die on this island, traveler. I've got enough work as it is. And if you DO die... I'll make sure you stay down. Professional courtesy.\"\n\nMorteus returns to his ledger, carefully noting the day's burial count.",
				"options": [],
			},
		},
	},

	# =====================================================================
	# ISLAND NPCs — Wyrmscale Island
	# =====================================================================

	"elder_drakenthis": {
		"id": "elder_drakenthis",
		"name": "Elder Drakenthis",
		"title": "Dragonkin Elder",
		"location": "wyrm_village_elder",
		"greeting": "An ancient dragonkin with silver-grey scales and eyes like molten gold regards you from a throne of fused obsidian. When he speaks, wisps of smoke curl from his nostrils.\n\n\"A soft-skin, here? Interesting. I am Elder Drakenthis. My people have dwelt alongside dragons for a thousand years. You seek either wisdom or death. I offer both. Choose carefully.\"",
		"dialogue": {
			"root": {
				"text": None,
				"options": [
					{"label": "Tell me about the dragons.", "next": "dragon_lore"},
					{"label": "How do I survive Wyrmscale?", "next": "survival"},
					{"label": "What lies in the Wyrm's Sanctum?", "next": "dungeon_info"},
					{"label": "I honor your wisdom, Elder.", "next": "farewell"},
				],
			},
			"dragon_lore": {
				"text": "\"This island belongs to the dragons. We dragonkin are their descendants — diluted blood, but dragon blood nonetheless. The lesser drakes you see on the ridges are wild and territorial. The elder dragons in the peaks are intelligent, ancient, and utterly lethal.\n\nDo not mistake drakes for dragons. A drake is a beast. A dragon is a god with wings and fire. The difference will matter when you meet one.\"",
				"options": [
					{"label": "How do I survive here?", "next": "survival"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"survival": {
				"text": "\"Fire resistance is mandatory. Fireproof potions, dragonscale armor, fire-opal wards — anything that reduces burn damage. Without protection, a single drake's breath will cook you alive.\n\nThe elder dragons can also use frost, lightning, and acid breath. No single resistance will save you. Speed, cover, and knowing when to hide are your best defenses. Fight only what you must. Run from what you can't kill.\"",
				"options": [
					{"label": "Tell me about the Wyrm's Sanctum.", "next": "dungeon_info"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"dungeon_info": {
				"text": "\"The Wyrm's Sanctum is the lair of the Ancient Wyrm — a dragon so old it has forgotten its own name. Three floors of volcanic tunnels, dragon nesting chambers, and treasure hoards.\n\nThe deepest floor holds the Dragon Forge — an altar heated by dragonfire itself. The finest weapons in the world are forged there. But the Ancient Wyrm does not share its hoard willingly. You will fight for every step.\n\nSpeak with our healer for potions and salves. You will need them.\"",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"farewell": {
				"text": "\"Strength and fire, soft-skin. May your scales grow thick and your claws sharp — metaphorically speaking.\"\n\nElder Drakenthis closes his eyes, smoke curling lazily from his nostrils as he meditates.",
				"options": [],
			},
		},
	},

	"wyrm_healer": {
		"id": "wyrm_healer",
		"name": "Scoria Ashvein",
		"title": "Dragonkin Healer",
		"location": "wyrm_village_healer",
		"greeting": "An elderly dragonkin with cracked amber scales grinds fire-opal powder with a mortar and pestle. A small drake curls by the hearth.\n\n\"Burns? Claw marks? Acid scars? Name your poison — heh, or don't, I'll figure it out. I'm Scoria. I've patched up more dragon-hunters than I can count. Let me show you what keeps them alive.\"",
		"dialogue": {
			"root": {
				"text": None,
				"options": [
					{"label": "Teach me dragon-fighting remedies.", "next": "teach_remedies"},
					{"label": "How do I treat dragonfire burns?", "next": "burn_treatment"},
					{"label": "What potions should I bring to the Sanctum?", "next": "sanctum_prep"},
					{"label": "Stay warm, Scoria.", "next": "farewell"},
				],
			},
			"teach_remedies": {
				"text": "Scoria reaches into a cabinet and produces two recipe scrolls, their edges singed.\n\n\"Two recipes every dragon-hunter needs:\n\n  • Dragonscale Salve — heals fire, acid, and frost burns. Made from shed dragonscale and aloe.\n  • Wyrm Potion — a powerful brew that grants temporary fire immunity. Wyrm blood, fire-opal, and volcanic spring water.\n\nGather the ingredients from the island and the dungeon. The drakes shed scales near their nests.\"",
				"effects": {
					"learn_recipes": ["dragonscale_salve", "wyrm_potion"],
				},
				"options": [
					{"label": "How do I treat dragonfire burns?", "next": "burn_treatment"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"burn_treatment": {
				"text": "\"Dragonfire burns differently from normal fire. It clings to flesh and keeps burning even after the flames go out. Water doesn't help — it makes it worse.\n\nUse fire-opal poultice. The opal absorbs the residual dragon-flame and neutralizes it. Then apply dragonscale salve to heal the wound. For acid burns, use drake-venom antidote first to stop the corrosion, then salve.\n\nAnd always — always — carry burn salve into the Sanctum. You'll use every drop.\"",
				"options": [
					{"label": "What should I bring to the Sanctum?", "next": "sanctum_prep"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"sanctum_prep": {
				"text": "\"For the Wyrm's Sanctum, you need:\n\n  • Fireproof potions — at least three. The heat alone can kill you.\n  • Dragonscale salve — for burns between fights.\n  • Burn salve — for minor injuries. Save the dragonscale salve for big hits.\n  • Fire-opal poultices — for dragonfire burns.\n  • Drake-venom antidote — the acid-spitting drakes are on floor two.\n  • Wyrm potion — save it for the Ancient Wyrm fight. You'll need the fire immunity.\n\nAnd eat before you go. Dragon-hunting on an empty stomach is a recipe for crispy adventurer.\"",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"farewell": {
				"text": "\"Come back alive and I'll patch you up for free — first time only. After that, you're paying in dragonscale.\"\n\nScoria returns to grinding fire-opal powder, humming an old dragonkin melody.",
				"options": [],
			},
		},
	},
	# ── Banker ────────────────────────────────────────────────────────────────
	"banker": {
		"id": "banker",
		"name": "Aldus Geld",
		"title": "Bank Keeper",
		"location": "bank_of_estoria",
		"greeting": "A portly man in a starched collar looks up from a heavy ledger and adjusts his spectacles.\n\n\"Ah, welcome to the Bank of Estoria — the safest vault in the realm!  I'm Aldus Geld, keeper of this fine institution.  How may I serve you today?\"",
		"dialogue": {
			"root": {
				"text": None,
				"options": [
					{"label": "How does the bank work?", "next": "how_it_works"},
					{"label": "Can I upgrade my vault?", "next": "upgrades"},
					{"label": "Tell me about the bank's history.", "next": "history"},
					{"label": "Goodbye.", "next": "farewell"},
				],
			},
			"how_it_works": {
				"text": "Aldus beams with pride.\n\n\"Simplicity itself!  You may deposit gold here for safekeeping — funds stored in the vault are *completely* safe, even should misfortune befall you on the road.  To use the service:\n\n  deposit <amount>  — put gold into the vault\n  withdraw <amount> — retrieve your gold\n  balance          — see your current balance\n\nYour vault begins at 5,000 gold capacity, but I can expand it with the right materials.\"",
				"options": [
					{"label": "How do I expand my vault?", "next": "upgrades"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"upgrades": {
				"text": "Aldus taps the counter with a meticulous finger.\n\n\"We currently offer nineteen vault expansions — each requires gold and certain crafting materials to pay for the reinforced ironwork.  The early tiers rely on copper and iron; later tiers need steel, mithril, and exotic components.\n\nSimply type  'upgrade bank'  and I shall check whether you meet the requirements.\"",
				"options": [
					{"label": "What is the maximum capacity?", "next": "max_cap"},
					{"label": "Thanks, let me ask something else.", "next": "root"},
				],
			},
			"max_cap": {
				"text": "\"At Tier 19 — our finest vault — you may store up to 100,000 gold.  Quite the achievement!  Only the wealthiest adventurers ever reach that level.\"\n\nHe lowers his voice conspiratorially.\n\n\"Between you and me, only three adventurers have ever maxed the vault.  One retired to a sea-side manor.  Another disappeared into the Void Beyond.  The third... we don't talk about the third.\"",
				"options": [
					{"label": "Noted.  Let me ask something else.", "next": "root"},
				],
			},
			"history": {
				"text": "Aldus straightens with obvious pride.\n\n\"The Bank of Estoria was founded four hundred years ago by Esterio Geld — my ancestor.  During the Great Pillaging, every merchant in the realm lost their gold to roaming brigands.  Esterio had the notion of a vault beneath the town square, sealed by runestones.\n\nThe vault has never been breached.  Even during the Demon Siege of year 312, the vault held.  Some say the foundation is blessed by the old gods of commerce.\"\n\nHe pats the stonework wall affectionately.",
				"options": [
					{"label": "Impressive!  Back to business.", "next": "root"},
				],
			},
			"farewell": {
				"text": "Aldus bows his head courteously.\n\n\"May your purse always be heavy and your enemies always be light.  Safe travels, friend.\"\n\nHe returns to his ledger with practiced efficiency.",
				"options": [],
			},
		},
	},

	"developer": {
		"id": "developer",
		"name": "The Developer",
		"title": "Author of This Reality",
		"location": "developers_corner",
		"greeting": "A figure sits at a plain desk covered in papers, empty cups, and what looks suspiciously like a game engine's source code. They look up at you with wide eyes.\n\n\"Oh. Oh wow. You actually found this place. I didn't think anyone would.\"\n\nThey close their laptop quickly. Too quickly.",
		"dialogue": {
			"root": {
				"text": None,
				"options": [
					{"label": "Where exactly am I?", "next": "where_am_i"},
					{"label": "Are you... the developer?", "next": "are_you_dev"},
					{"label": "What's in that notebook?", "next": "notebook"},
					{"label": "Do you know this is a game?", "next": "fourth_wall"},
					{"label": "Can I have a gift?", "next": "gift_ask"},
					{"label": "Goodbye.", "next": "farewell"},
				],
			},
			"where_am_i": {
				"text": "\"This is... the Development Corner. It's where I — they — work on the world.\"\n\nThey gesture at the walls. Now that you look closely, you can see blueprint sketches of dungeons, NPC dialogue trees, item balance spreadsheets, and a whiteboard that reads 'PHASE 3: HIDDEN CONTENT — DONE? MAYBE'.\n\n\"You weren't supposed to be able to get in here. The plain wall was supposed to look, well, plain.\"\n\nThey sigh. \"Well done, honestly.\"",
				"options": [
					{"label": "What is Phase 3?", "next": "phase3"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"phase3": {
				"text": "\"Phase 3 is... well, you're living in it. Hidden rooms, secret bosses, mythic items, easter eggs.\"\n\nThey count on their fingers.\n\n\"There's the Underground Archive under the chapel — lots of books, don't touch the restricted section. The Pirate Vault down in the sea caves. The Forgotten Shrine puzzle in the forest. The Hidden Alchemy Lab in the castle — you'll need a key for that. The Void Sanctuary in the void rift. The Clocktower Interior — examine the gears. And this place.\"\n\nThey pause. \"Also there's a secret boss if you collect the right three items. Try 'invoke ritual' when you have them all.\"",
				"options": [
					{"label": "What three items for the boss?", "next": "ritual_hint"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"ritual_hint": {
				"text": "\"A shadow shard, a blood sigil, and a void crystal. All three. In your inventory.\"\n\nThey look at you seriously.\n\n\"The Void Titan is not a joke. It's... it's very strong. I may have over-tuned it slightly.\"\n\nA pause.\n\n\"Okay, significantly over-tuned. I was having a day.\"",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"are_you_dev": {
				"text": "They look around nervously.\n\n\"I mean... technically, everyone in this world is made of code. The tavern keeper, the blacksmith, even Father Aldric is just a series of nested dialogue trees and conditional checks.\"\n\nThey lower their voice.\n\n\"But yes. I'm the one who wrote the conditional checks. Please don't tell the other NPCs. They've been through enough.\"",
				"options": [
					{"label": "Do the NPCs know they're NPCs?", "next": "npcs_know"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"npcs_know": {
				"text": "\"Bren the bartender suspects. He keeps asking questions no tavern keeper should care about — the nature of free will, whether his dialogue options were pre-determined, why he can only give the same eight conversational topics.\"\n\nThey shudder.\n\n\"The blacksmith is fine. Never questions anything. Best NPC I ever wrote.\"\n\nA sad look crosses their face.\n\n\"Sometimes I add new dialogue for them in the middle of the night. They wake up and suddenly know things they didn't know yesterday. I like to think it feels like a dream to them.\"",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"notebook": {
				"text": "They slam a hand on the notebook protectively.\n\n\"That's my — that's nothing. Design notes. Ideas for Phase 4.\"\n\nYou catch a glimpse of the pages. You think you see the words 'WEATHER SYSTEM', 'FISHING TOURNAMENT', 'PLAYER HOUSING?', and 'WHY DOES THE SAVE FILE DO THAT' in large, concerned letters.\n\n\"If Phase 4 happens,\" they say quietly, \"you'll know.\"",
				"options": [
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"fourth_wall": {
				"text": "A very long silence.\n\n\"Does the wall look broken to you?\" they finally say.\n\nAnother silence.\n\n\"Okay, fine. Yes. This is a game. You are a player. I am the developer. The world around you is a Python program running on someone's laptop, and if they close the window, reality as you know it ceases to exist until the next git pull.\"\n\nThey look at the fourth wall directly.\n\nActually, they look at YOU directly.\n\n\"Hi. Thanks for playing. It means a lot.\"",
				"effects": {"track_event": "easter_eggs_found"},
				"options": [
					{"label": "...thanks?", "next": "thanks_response"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"thanks_response": {
				"text": "\"You're welcome. And — hey — try 'doabigcheese' sometime. Just... because.\"",
				"options": [
					{"label": "What does that do?", "next": "cheese_hint"},
					{"label": "Let me ask something else.", "next": "root"},
				],
			},
			"cheese_hint": {
				"text": "They smile for the first time.\n\n\"Type 'doabigcheese' anywhere, any time. It's... a long story. The short version is that it was 2 AM and someone thought it would be very funny.\"\n\nThey do not elaborate.",
				"options": [
					{"label": "I will definitely do that.", "next": "root"},
				],
			},
			"gift_ask": {
				"text": "They rummage under the desk.\n\n\"Let me see... I've got a developer's note, and...\"\n\nThey hand you a blade that hums with impossible energy.\n\n\"The Developer's Blade. Stats are... let's call them 'enthusiastically balanced'. Also a note explaining everything. Don't show the other NPCs.\"",
				"effects": {"give_items": {"devs_blade": 1, "developers_note": 1}, "track_event": "easter_eggs_found"},
				"options": [
					{"label": "This is incredible. Thank you.", "next": "gift_thanks"},
				],
			},
			"gift_thanks": {
				"text": "\"You earned it. Now go — before the save file corrupts again.\"\n\nThey turn back to their desk.\n\n\"And if you talk to Bren, tell him I said... tell him the options are all his. In a way.\"",
				"options": [
					{"label": "Goodbye.", "next": "farewell"},
				],
			},
			"farewell": {
				"text": "\"Safe travels. And — one last thing — you're doing great.\"\n\nThey wave. Reality feels very slightly more real than it did a moment ago.",
				"options": [],
			},
		},
	},
}


class NPCManager:
	"""Manages NPC interactions and dialogue state."""

	def __init__(self, engine):
		self.engine = engine

	def get_npcs_in_room(self, room_id=None):
		"""
		Get list of NPC IDs present in the given room.
		Reads from the world.json room data's 'npcs' array.
		"""
		if room_id is None:
			room_id = self.engine.player.current_room

		# Get room data from the json (not the Room object, which may lack npcs)
		room = self.engine.get_room_data(room_id)
		if not room:
			return []

		# Room objects might have npcs stored
		npcs = []
		if hasattr(room, 'npcs'):
			npcs = room.npcs or []
		elif isinstance(room, dict):
			npcs = room.get("npcs", [])

		return [npc_id for npc_id in npcs if npc_id in NPC_DATABASE]

	def get_npc(self, npc_id):
		"""Get NPC data by ID."""
		return NPC_DATABASE.get(npc_id)

	def get_npc_display_list(self, room_id=None):
		"""
		Get formatted string listing NPCs in the room.
		Returns empty string if no NPCs.
		"""
		npc_ids = self.get_npcs_in_room(room_id)
		if not npc_ids:
			return ""

		npc_names = []
		for npc_id in npc_ids:
			npc = NPC_DATABASE.get(npc_id)
			if npc:
				npc_names.append(f"{npc['name']} ({npc['title']})")

		if not npc_names:
			return ""

		return "People here: " + ", ".join(npc_names)

	def start_conversation(self, npc_name):
		"""
		Start a conversation with an NPC by name.
		Returns the greeting text + dialogue options, or an error message.
		"""
		player_room = self.engine.player.current_room
		npcs_here = self.get_npcs_in_room(player_room)

		if not npcs_here:
			return "There's nobody here to talk to."

		# Match by NPC id, display name, or partial match
		matched_npc_id = None
		search = npc_name.strip().lower().replace(" ", "_")

		for npc_id in npcs_here:
			npc = NPC_DATABASE.get(npc_id)
			if not npc:
				continue
			# Match by id, name, or title
			if (search == npc_id.lower() or
				search == npc["name"].lower().replace(" ", "_") or
				search == npc["name"].lower() or
				search in npc["name"].lower() or
				search in npc_id.lower() or
				search in npc["title"].lower()):
				matched_npc_id = npc_id
				break

		if not matched_npc_id:
			available = ", ".join(
				NPC_DATABASE[nid]["name"] for nid in npcs_here if nid in NPC_DATABASE
			)
			return f"You don't see anyone by that name. People here: {available}"

		npc = NPC_DATABASE[matched_npc_id]

		# Notify quest system about NPC interaction
		if QUEST_AVAILABLE and hasattr(self.engine, 'quest_manager') and self.engine.quest_manager:
			self.engine.quest_manager.on_npc_talked(matched_npc_id)

		# Record visit in reputation system
		rep_visit_msg = ""
		if REPUTATION_AVAILABLE and hasattr(self.engine, 'reputation_manager') and self.engine.reputation_manager:
			rep_visit_msg = self.engine.reputation_manager.record_visit(matched_npc_id)

		# Build greeting + root options
		result = "\n" + "═" * 55 + "\n"
		result += f"  💬 {npc['name']} — {npc['title']}"
		# Show mood if reputation system is active
		if REPUTATION_AVAILABLE and hasattr(self.engine, 'reputation_manager') and self.engine.reputation_manager:
			from npc_reputation import MOOD_ICONS
			mood = self.engine.reputation_manager.get_mood(matched_npc_id)
			icon = MOOD_ICONS.get(mood, "")
			result += f"  {icon} {mood.title()}"
		result += "\n"
		result += "═" * 55 + "\n\n"
		result += npc["greeting"] + "\n"
		if rep_visit_msg:
			result += rep_visit_msg + "\n"

		# Show root dialogue options + quest options + reputation options
		root = npc["dialogue"].get("root", {})
		options = list(root.get("options", []))

		# Inject quest-related dialogue options
		quest_options = []
		if QUEST_AVAILABLE and hasattr(self.engine, 'quest_manager') and self.engine.quest_manager:
			quest_options = self.engine.quest_manager.get_npc_quest_dialogue(matched_npc_id)

		# Inject reputation-gated dialogue options
		rep_options = []
		if REPUTATION_AVAILABLE and hasattr(self.engine, 'reputation_manager') and self.engine.reputation_manager:
			rep_available = self.engine.reputation_manager.get_available_rep_dialogue(matched_npc_id)
			for rd in rep_available:
				rep_options.append({
					"label": rd["label"],
					"rep_node_id": rd["node_id"],
					"rep_node": rd["node"],
				})

		result += self._format_options(options, quest_options, rep_options)

		# Set pending dialogue state
		self.engine.pending_dialogue = {
			"npc_id": matched_npc_id,
			"current_node": "root",
			"quest_options": quest_options,
			"rep_options": rep_options,
		}

		return result

	def handle_dialogue_choice(self, cmd):
		"""
		Handle player's response during an active conversation.
		Returns response text or None if not in dialogue.
		"""
		pending = self.engine.pending_dialogue
		if not pending:
			return None

		npc_id = pending["npc_id"]
		current_node_id = pending["current_node"]
		npc = NPC_DATABASE.get(npc_id)

		if not npc:
			self.engine.pending_dialogue = None
			return "The conversation ends abruptly."

		# Get current node
		current_node = npc["dialogue"].get(current_node_id, {})
		options = current_node.get("options", [])

		# Get quest options and rep options from pending state
		quest_options = pending.get("quest_options", [])
		rep_options = pending.get("rep_options", [])
		total_options = len(options) + len(quest_options) + len(rep_options)

		# Handle exit commands
		cmd_lower = cmd.strip().lower()
		if cmd_lower in ("bye", "goodbye", "leave", "quit", "exit", "back", "cancel"):
			self.engine.pending_dialogue = None
			farewell = npc["dialogue"].get("farewell", {})
			if farewell and farewell.get("text"):
				return farewell["text"] + "\n"
			return f"{npc['name']} nods as you turn to leave."

		# Parse choice number
		try:
			choice_idx = int(cmd_lower) - 1
		except ValueError:
			return f"Enter a number (1-{total_options}) to choose, or 'bye' to end conversation."

		if choice_idx < 0 or choice_idx >= total_options:
			return f"Choose 1-{total_options}, or 'bye' to end the conversation."

		# Check if player chose a quest option (appended after regular options)
		if choice_idx >= len(options) and choice_idx < len(options) + len(quest_options):
			quest_opt_idx = choice_idx - len(options)
			quest_opt = quest_options[quest_opt_idx]
			action_type, quest_id = quest_opt["quest_action"]
			if QUEST_AVAILABLE and hasattr(self.engine, 'quest_manager') and self.engine.quest_manager:
				# End dialogue and handle quest action
				self.engine.pending_dialogue = None
				return self.engine.quest_manager.handle_quest_dialogue(action_type, quest_id)
			self.engine.pending_dialogue = None
			return "The quest system is not available."

		# Check if player chose a reputation option (appended after quest options)
		if choice_idx >= len(options) + len(quest_options) and rep_options:
			rep_opt_idx = choice_idx - len(options) - len(quest_options)
			if rep_opt_idx < len(rep_options):
				rep_opt = rep_options[rep_opt_idx]
				rep_node = rep_opt["rep_node"]
				rep_node_id = rep_opt["rep_node_id"]
				# Apply effects from rep node
				effects_text = self._apply_effects(rep_node.get("effects", {}), npc)
				# Mark as claimed so it doesn't repeat
				if REPUTATION_AVAILABLE and hasattr(self.engine, 'reputation_manager'):
					self.engine.reputation_manager.claim_rep_reward(npc_id, rep_node_id)
				result = ""
				if rep_node.get("text"):
					result += rep_node["text"] + "\n"
				if effects_text:
					result += "\n" + effects_text + "\n"
				next_options = rep_node.get("options", [])
				if not next_options:
					self.engine.pending_dialogue = None
					result += "\n  [Conversation ended]\n"
				else:
					new_quest_options = []
					new_rep_options = []
					next_node_id = next_options[0].get("next", "root") if next_options else "root"
					if next_node_id == "root" and QUEST_AVAILABLE and hasattr(self.engine, 'quest_manager') and self.engine.quest_manager:
						new_quest_options = self.engine.quest_manager.get_npc_quest_dialogue(npc_id)
					if next_node_id == "root" and REPUTATION_AVAILABLE and hasattr(self.engine, 'reputation_manager'):
						new_rep_available = self.engine.reputation_manager.get_available_rep_dialogue(npc_id)
						for rd in new_rep_available:
							new_rep_options.append({"label": rd["label"], "rep_node_id": rd["node_id"], "rep_node": rd["node"]})
					result += self._format_options(next_options, new_quest_options if next_node_id == "root" else None, new_rep_options if next_node_id == "root" else None)
					self.engine.pending_dialogue = {
						"npc_id": npc_id,
						"current_node": next_node_id,
						"quest_options": new_quest_options if next_node_id == "root" else [],
						"rep_options": new_rep_options if next_node_id == "root" else [],
					}
				return result

		chosen = options[choice_idx]
		next_node_id = chosen.get("next", "farewell")
		next_node = npc["dialogue"].get(next_node_id, {})

		# Apply effects BEFORE showing text
		effects_text = self._apply_effects(next_node.get("effects", {}), npc)

		# Build response
		result = ""

		# Dynamic text generation for special nodes
		if next_node_id == "heal" and npc_id == "priest":
			result += self._do_priest_healing(npc)
		elif next_node.get("text"):
			result += next_node["text"] + "\n"

		# Show effects (learned recipes, etc.)
		if effects_text:
			result += "\n" + effects_text + "\n"

		# Record dialogue node visit in reputation system
		if REPUTATION_AVAILABLE and hasattr(self.engine, 'reputation_manager') and self.engine.reputation_manager:
			self.engine.reputation_manager.record_dialogue_node(npc_id, next_node_id)

		# Check if conversation continues
		next_options = next_node.get("options", [])
		if not next_options:
			# End of conversation
			self.engine.pending_dialogue = None
			result += "\n  [Conversation ended]\n"
		else:
			# Re-gather quest options if we're returning to root
			new_quest_options = []
			new_rep_options = []
			if next_node_id == "root" and QUEST_AVAILABLE and hasattr(self.engine, 'quest_manager') and self.engine.quest_manager:
				new_quest_options = self.engine.quest_manager.get_npc_quest_dialogue(npc_id)
			if next_node_id == "root" and REPUTATION_AVAILABLE and hasattr(self.engine, 'reputation_manager'):
				new_rep_available = self.engine.reputation_manager.get_available_rep_dialogue(npc_id)
				for rd in new_rep_available:
					new_rep_options.append({"label": rd["label"], "rep_node_id": rd["node_id"], "rep_node": rd["node"]})

			# Show next options
			result += self._format_options(next_options, new_quest_options if next_node_id == "root" else None, new_rep_options if next_node_id == "root" else None)

			# Update pending state
			self.engine.pending_dialogue = {
				"npc_id": npc_id,
				"current_node": next_node_id,
				"quest_options": new_quest_options if next_node_id == "root" else [],
				"rep_options": new_rep_options if next_node_id == "root" else [],
			}

		return result

	def _format_options(self, options, quest_options=None, rep_options=None):
		"""Format dialogue options for display, including quest and reputation options."""
		if not options and not quest_options and not rep_options:
			return ""

		result = "\n  ─── Your response ───\n"
		idx = 1
		for opt in options:
			result += f"  {idx}. {opt['label']}\n"
			idx += 1
		# Append quest options (if any)
		if quest_options:
			for qopt in quest_options:
				result += f"  {idx}. {qopt['label']}\n"
				idx += 1
		# Append reputation-gated options (if any)
		if rep_options:
			for ropt in rep_options:
				result += f"  {idx}. 💛 {ropt['label']}\n"
				idx += 1
		result += "  (or 'bye' to end conversation)\n"
		return result

	def _apply_effects(self, effects, npc):
		"""Apply dialogue effects (learn recipes, etc.). Returns notification text."""
		if not effects:
			return ""

		parts = []

		# Learn recipes
		recipes = effects.get("learn_recipes", [])
		if recipes:
			try:
				from crafting_system import CraftingSystem
				crafting = CraftingSystem(self.engine)
				for recipe_id in recipes:
					msg = crafting.learn_recipe(recipe_id)
					if msg:
						parts.append(msg)
			except ImportError:
				pass

		# Full heal (priest)
		if effects.get("heal_full"):
			# Handled separately in _do_priest_healing
			pass

		# Set player state flags
		state_changes = effects.get("set_state", {})
		for key, value in state_changes.items():
			self.engine.player.state[key] = value

		# Give items
		items = effects.get("give_items", {})
		for item_name, count in items.items():
			inv = self.engine.player.inventory
			inv[item_name] = inv.get(item_name, 0) + count
			self.engine._inventory_changed = True
			nice = item_name.replace("_", " ")
			parts.append(f"  📦 Received: {count}x {nice}")

		# Award XP for meaningful NPC interactions
		if PROGRESSION_AVAILABLE and (recipes or items):
			try:
				xp_amount = XP_AWARDS.get("complete_dialogue", 10)
				if recipes:
					# Use learn_recipe XP per recipe learned
					xp_amount += len(recipes) * XP_AWARDS.get("learn_recipe", 15)
				xp_msg = award_xp(self.engine.player, xp_amount, "NPC interaction")
				if xp_msg:
					parts.append(xp_msg)
			except Exception:
				pass

		# Track reputation gains for recipe learning
		if recipes and REPUTATION_AVAILABLE and hasattr(self, 'engine') and hasattr(self.engine, 'reputation_manager') and self.engine.reputation_manager:
			# This gets the current NPC context from pending dialogue
			pending = getattr(self.engine, 'pending_dialogue', None)
			if pending and pending.get('npc_id'):
				self.engine.reputation_manager.modify_affinity(pending['npc_id'], 3, "learned a recipe")

		# Track achievement events
		event_key = effects.get("track_event")
		if event_key:
			try:
				from achievement_system import track_event as ach_track
				ach_track(self.engine.player, event_key)
			except Exception:
				pass

		return "\n".join(parts)

	def handle_gift(self, npc_id, item_id):
		"""Handle giving a gift to an NPC."""
		# Validate NPC exists
		if npc_id not in NPC_DATABASE:
			return f"Unknown NPC: {npc_id}"

		npc = NPC_DATABASE[npc_id]

		# Validate item
		inv = self.engine.player.inventory
		if item_id not in inv or inv[item_id] <= 0:
			nice_item = item_id.replace('_', ' ')
			return f"You don't have any {nice_item} to give."

		# Check player is in same room as NPC
		npcs_here = self.get_npcs_in_room(self.engine.current_room)
		npc_ids_here = [n["id"] for n in npcs_here]
		if npc_id not in npc_ids_here:
			return f"{npc['name']} is not here."

		# Use reputation manager for the gift
		if not REPUTATION_AVAILABLE or not hasattr(self.engine, 'reputation_manager') or not self.engine.reputation_manager:
			return "The reputation system is not available."

		success, reaction = self.engine.reputation_manager.give_gift(npc_id, item_id)
		if not success:
			return reaction
		self.engine._inventory_changed = True

		result = "\n" + "═" * 55 + "\n"
		result += f"  🎁 Gift to {npc['name']}\n"
		result += "═" * 55 + "\n\n"
		result += reaction + "\n"

		# Show current relationship status
		mood = self.engine.reputation_manager.get_mood(npc_id)
		from npc_reputation import MOOD_ICONS
		icon = MOOD_ICONS.get(mood, "")
		result += f"\n  Relationship: {icon} {mood.title()}\n"

		return result

	def _do_priest_healing(self, npc):
		"""Handle the priest's healing — restores full HP."""
		stats = self.engine.player.stats
		current = stats.get("health", 100)
		max_hp = stats.get("health_max", 100)

		if current >= max_hp:
			return "Father Aldric places his hands gently on your head.\n\n\"You are already whole, child. There is nothing for me to heal.\"\n\nHe smiles warmly.\n"

		stats["health"] = max_hp
		healed = max_hp - current

		# Also cure poison
		if self.engine.poison_status:
			self.engine.poison_status = None
			return f"Father Aldric places his hands on your head. Warm golden light flows through you.\n\n\"Be healed, child.\"\n\n  ❤️ Restored {healed} health. (Health: {max_hp}/{max_hp})\n  🧪 Poison cured!\n"

		return f"Father Aldric places his hands on your head. Warm golden light flows through you.\n\n\"Be healed, child.\"\n\n  ❤️ Restored {healed} health. (Health: {max_hp}/{max_hp})\n"

	def to_dict(self):
		"""
		Serialize NPC dialogue state for saving.
		Currently stores learned recipes in player.state, so no extra data needed here.
		Future: Could store per-NPC visited dialogue nodes if needed.
		"""
		return {
			# Placeholder for future expansion
			# e.g., "visited_nodes": {"blacksmith": ["root", "teach_forging"]},
			# Currently recipes are stored in player.state["learned_recipes"]
		}

	def load_from_dict(self, data):
		"""
		Restore NPC dialogue state from saved data.
		Currently a no-op since recipes are in player.state.
		"""
		pass
