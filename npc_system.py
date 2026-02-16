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
					{"label": "Thanks! Let me ask something else.", "next": "root"},
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
