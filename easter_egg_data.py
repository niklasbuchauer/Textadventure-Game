"""Shared easter egg room content used by engine fallback and pygame overlay UI."""

import copy


DEFAULT_TILE_LEGEND = {
    "#": {"color": (78, 64, 46), "accent": (115, 92, 60)},
    ".": {"color": (31, 33, 36), "accent": (42, 44, 48)},
    "~": {"color": (28, 61, 90), "accent": (67, 117, 156)},
    "*": {"color": (97, 79, 38), "accent": (148, 126, 66)},
    "S": {"color": (102, 84, 57), "accent": (150, 124, 84)},
    "R": {"color": (83, 111, 128), "accent": (121, 171, 194)},
    "C": {"color": (127, 97, 46), "accent": (178, 147, 81)},
    "A": {"color": (125, 115, 93), "accent": (187, 174, 146)},
    "F": {"color": (154, 81, 48), "accent": (233, 146, 74)},
    "V": {"color": (92, 76, 131), "accent": (150, 124, 196)},
    "G": {"color": (116, 98, 56), "accent": (184, 159, 92)},
    "P": {"color": (134, 102, 57), "accent": (203, 170, 108)},
    "D": {"color": (82, 88, 96), "accent": (124, 134, 147)},
    "K": {"color": (88, 78, 57), "accent": (146, 131, 95)},
    "N": {"color": (96, 88, 72), "accent": (150, 140, 115)},
    "W": {"color": (72, 93, 106), "accent": (123, 160, 179)},
    "B": {"color": (111, 84, 60), "accent": (168, 130, 92)},
    "E": {"color": (93, 107, 102), "accent": (139, 170, 162)},
    "L": {"color": (123, 96, 67), "accent": (181, 146, 104)},
    "T": {"color": (120, 88, 66), "accent": (174, 133, 95)},
    "H": {"color": (96, 70, 44), "accent": (166, 116, 72)},
    "O": {"color": (101, 83, 121), "accent": (165, 141, 203)},
    "I": {"color": (85, 108, 112), "accent": (139, 178, 185)},
    "M": {"color": (76, 90, 98), "accent": (132, 158, 172)},
}


def _hotspot(hotspot_id, label, action_id, x, y, w=1, h=1):
    return {
        "id": hotspot_id,
        "label": label,
        "action_id": action_id,
        "x": x,
        "y": y,
        "w": w,
        "h": h,
    }


def _layout(grid, hotspots):
    return {
        "grid": list(grid),
        "legend": copy.deepcopy(DEFAULT_TILE_LEGEND),
        "hotspots": list(hotspots),
    }


EASTER_EGG_ROOM_DATA = {
    "underground_archive": {
        "title": "Underground Archive",
        "lore": (
            "Dust moves like ash in shafts of pale rune-light, and every breath tastes of paper, ink, and old stone. "
            "The archive is not arranged for comfort; it is arranged for survival, as if the people who built it expected the world above to fail.\n\n"
            "The room divides itself into aisles, writing stations, and guarded alcoves. Someone catalogued entire ages here, "
            "and someone else returned later to redact dangerous truths in a different hand."
        ),
        "interactions": [
            {
                "action_id": "inspect_stacks",
                "label": "Inspect Stacks",
                "type": "note",
                "text": (
                    "The shelving near the northern wall is sorted by expedition route, not by author. "
                    "Binders with brass tabs list weather, losses, and routes through collapsed districts.\n\n"
                    "Near the lower rows you find charred journals wrapped in wax cloth. "
                    "Three mention the same warning: 'Do not trust maps copied after the Third Collapse.'"
                ),
            },
            {
                "action_id": "study_runes",
                "label": "Study Runes",
                "type": "note",
                "text": (
                    "The runes carved into the floor lanes are not decorative. "
                    "They track movement and pulse faster when you step close to sealed cabinets.\n\n"
                    "A translator's margin note suggests the phrases alternate between inventory markers "
                    "and judicial language, implying this archive was both a library and a courtroom record."
                ),
            },
            {
                "action_id": "read_cartographer_table",
                "label": "Read Cartographer Table",
                "type": "note",
                "text": (
                    "A drafting table still holds layered transparent maps pinned by obsidian needles. "
                    "Each layer adds hidden tunnels, collapsed bridges, and safewatch posts.\n\n"
                    "The topmost overlay is unfinished but recent. "
                    "Whoever worked here last expected someone else to continue the map, and left room for your route."
                ),
            },
            {
                "action_id": "inspect_sealed_drawers",
                "label": "Inspect Sealed Drawers",
                "type": "note",
                "text": (
                    "The drawer fronts are stamped with courtroom sigils and sealed by wax cords hardened with mineral dust. "
                    "Inside, verdict ledgers list names, crimes, and exile destinations that no longer exist on public maps.\n\n"
                    "Several entries are scratched out and replaced with a single notation: 'Relocated under oath protection.'"
                ),
            },
            {
                "action_id": "review_warden_log",
                "label": "Review Warden Log",
                "type": "note",
                "text": (
                    "A narrow logbook by the exit tracks every person allowed to enter this archive over eighty-three years. "
                    "The handwriting grows shakier near the end but the rules never change.\n\n"
                    "The final entry is unsigned and reads: 'If you can read this, guard the index before you guard the vault.'"
                ),
            },
        ],
        "layout": _layout(
            [
                "################",
                "#SSSS..T..RRR..#",
                "#SSSS..T..RRR..#",
                "#....##....##..#",
                "#DD..##..NN##..#",
                "#DD......NN....#",
                "#....S....S....#",
                "#....S....S....#",
                "#.......I......#",
                "################",
            ],
            [
                _hotspot("stacks", "Inspect Stacks", "inspect_stacks", 1, 1, 4, 2),
                _hotspot("runes", "Study Runes", "study_runes", 10, 1, 3, 2),
                _hotspot("cartographer", "Read Cartographer Table", "read_cartographer_table", 6, 1, 1, 2),
                _hotspot("drawers", "Inspect Sealed Drawers", "inspect_sealed_drawers", 1, 4, 2, 2),
                _hotspot("warden", "Review Warden Log", "review_warden_log", 8, 4, 2, 2),
            ],
        ),
    },
    "pirate_vault": {
        "title": "Pirate Vault",
        "lore": (
            "Tar, salt, and wet rope perfume the chamber like a memory of a storm that never ended. "
            "Every chest is marked by crew symbols instead of names, and every symbol tells a story of mutiny, debt, or oath.\n\n"
            "The vault was built to flood on command. The old crew trusted neither the sea nor each other, "
            "so they designed the room to drown thieves before they reached the central ledger chest."
        ),
        "interactions": [
            {
                "action_id": "inspect_chests",
                "label": "Inspect Chests",
                "type": "note",
                "text": (
                    "The nearest chests are ranked by risk, not value. "
                    "One holds navigational astrolabes, another sealed writs from ports that denied pirate docking rights.\n\n"
                    "Several compartments are decoys filled with iron scrap to imitate weight. "
                    "The real stash is split so no single theft can cripple the crew."
                ),
            },
            {
                "action_id": "check_channels",
                "label": "Check Water Channels",
                "type": "note",
                "text": (
                    "A narrow grate reveals pressure channels that run beneath every aisle. "
                    "The overflow gates are counterweighted and still react when disturbed.\n\n"
                    "The mechanism is crude but ruthless: flood first, retrieve losses later. "
                    "No wonder the floor stones are scored by drag marks."
                ),
            },
            {
                "action_id": "study_route_board",
                "label": "Study Route Board",
                "type": "note",
                "text": (
                    "A wall board near the south passage maps interception routes around reefs and military patrol lines. "
                    "Pins mark successful raids in brass and failed attempts in blackened steel.\n\n"
                    "One unfinished line points inland, suggesting the crew planned land raids as their final campaign."
                ),
            },
            {
                "action_id": "inspect_captain_locker",
                "label": "Inspect Captain Locker",
                "type": "note",
                "text": (
                    "The captain's locker is less about wealth and more about leverage. "
                    "Inside are sealed letters, hostage contracts, and medallions from rival crews.\n\n"
                    "A private ledger records favors owed by governors, smugglers, and one frightened admiral."
                ),
            },
            {
                "action_id": "read_watch_log",
                "label": "Read Watch Log",
                "type": "note",
                "text": (
                    "The watch log tracks not only tides but temper. "
                    "Entries note arguments over shares, crew disappearances, and sudden lock changes in the vault.\n\n"
                    "Near the end, a quartermaster warns: 'If the channels open without order, the traitor is aboard.'"
                ),
            },
        ],
        "layout": _layout(
            [
                "################",
                "#CC..C...C..CC.#",
                "#CC..C...C..CC.#",
                "#....WWWW......#",
                "#..P.WWWW..T...#",
                "#....WWWW..T...#",
                "#..C.....C..N..#",
                "#..C.....C..N..#",
                "#......D.......#",
                "################",
            ],
            [
                _hotspot("chests", "Inspect Chests", "inspect_chests", 1, 1, 2, 2),
                _hotspot("channels", "Check Water Channels", "check_channels", 5, 3, 4, 3),
                _hotspot("routes", "Study Route Board", "study_route_board", 11, 4, 1, 2),
                _hotspot("captain", "Inspect Captain Locker", "inspect_captain_locker", 3, 4, 1, 1),
                _hotspot("watch", "Read Watch Log", "read_watch_log", 13, 6, 1, 2),
            ],
        ),
    },
    "forgotten_shrine_puzzle": {
        "title": "Forgotten Shrine",
        "lore": (
            "The shrine is quiet in the way deep water is quiet: no wind, no dust, no stray echo. "
            "Everything here was built around devotion and doubt in equal measure.\n\n"
            "The altar does not demand worship. It demands understanding. "
            "Every inscription and carved path tests whether you came for power or for truth."
        ),
        "interactions": [
            {
                "action_id": "approach_altar",
                "label": "Approach Altar",
                "type": "note",
                "text": (
                    "The altar stone is warm despite the chill in the chamber. "
                    "As your hand nears, shallow glyphs brighten and rearrange around your shadow.\n\n"
                    "One line resolves into a familiar challenge: 'Name the cost before naming the wish.'"
                ),
            },
            {
                "action_id": "read_inscriptions",
                "label": "Read Inscriptions",
                "type": "note",
                "text": (
                    "The wall text spirals from floor to ceiling in nested language layers. "
                    "The oldest lines discuss obligation; newer lines debate mercy and restraint.\n\n"
                    "A final clause repeats in each era's script: 'Only those who understand questions deserve hidden answers.'"
                ),
            },
            {
                "action_id": "observe_offering_bowls",
                "label": "Observe Offering Bowls",
                "type": "note",
                "text": (
                    "Bronze bowls ring the altar, each filled with different offerings: ash, clear water, thread, and uncut stone. "
                    "None are precious in coin, but each carries practical meaning.\n\n"
                    "The pattern suggests this shrine honored discipline over wealth, and memory over spectacle."
                ),
            },
            {
                "action_id": "inspect_pillar_marks",
                "label": "Inspect Pillar Marks",
                "type": "note",
                "text": (
                    "The support pillars are scored by deliberate blade cuts at shoulder height. "
                    "Pilgrims carved these marks while reciting vows, one cut for each binding promise.\n\n"
                    "Some cuts are deep and steady, others tremble. The stone preserves both confidence and fear."
                ),
            },
            {
                "action_id": "read_keeper_tablet",
                "label": "Read Keeper Tablet",
                "type": "note",
                "text": (
                    "A cracked slate tablet by the rear wall records names of shrine keepers and the questions they failed to answer. "
                    "Failure was not punished here; it was archived.\n\n"
                    "The last keeper wrote one private line in smaller script: 'The right answer arrived after I locked the door.'"
                ),
            },
        ],
        "layout": _layout(
            [
                "################",
                "#......*.......#",
                "#....*****.....#",
                "#...**AAA**....#",
                "#...**AAA**....#",
                "#....*****..N..#",
                "#..P......P.N..#",
                "#..P..T...P....#",
                "#......N.......#",
                "################",
            ],
            [
                _hotspot("altar", "Approach Altar", "approach_altar", 5, 3, 3, 2),
                _hotspot("inscriptions", "Read Inscriptions", "read_inscriptions", 12, 5, 1, 2),
                _hotspot("bowls", "Observe Offering Bowls", "observe_offering_bowls", 4, 2, 5, 4),
                _hotspot("pillars", "Inspect Pillar Marks", "inspect_pillar_marks", 2, 6, 1, 2),
                _hotspot("keeper", "Read Keeper Tablet", "read_keeper_tablet", 7, 7, 1, 1),
            ],
        ),
    },
    "hidden_alchemy_lab": {
        "title": "Hidden Alchemy Lab",
        "lore": (
            "This is a working laboratory, not a shrine to chaos. "
            "Stations are laid out by process order: wash, prep, distill, condense, stabilize, store.\n\n"
            "Soot marks and chalk notes show repeated iteration, not reckless improvisation. "
            "Whoever ran this lab treated alchemy like engineering with consequences."
        ),
        "interactions": [
            {
                "action_id": "inspect_flasks",
                "label": "Inspect Flasks",
                "type": "note",
                "text": (
                    "The vial rack is grouped by volatility instead of color. "
                    "Green labels mark stable reagents, amber marks reactive compounds, and red marks one-use catalysts.\n\n"
                    "Every stopper is numbered and cross-referenced with a usage ledger, suggesting strict batch control."
                ),
            },
            {
                "action_id": "check_furnace",
                "label": "Check Furnace",
                "type": "note",
                "text": (
                    "The furnace chamber is lined with layered brick and mica plates to retain heat with minimal fuel waste. "
                    "A brass regulator wheel controls airflow in quarter-turn increments.\n\n"
                    "Scratch marks around the regulator suggest this wheel was adjusted constantly during long distillation runs."
                ),
            },
            {
                "action_id": "inspect_distillation_line",
                "label": "Inspect Distillation Line",
                "type": "note",
                "text": (
                    "A row of copper stills runs along the west bench, connected by cooling coils that feed into labeled catch basins. "
                    "The setup separates heavy salts, aromatic oils, and clear solvents in stages.\n\n"
                    "Each stage includes pressure notes in neat handwriting, with warnings beside thresholds where glass failures occurred."
                ),
            },
            {
                "action_id": "read_prep_bench_notes",
                "label": "Read Prep Bench Notes",
                "type": "note",
                "text": (
                    "The central prep table is covered in chalk formulas and corrected ratios. "
                    "Someone iterated one restorative tonic twenty-two times, crossing out each unstable version.\n\n"
                    "The final note is practical and tired: 'Good medicine should survive bad hands.'"
                ),
            },
            {
                "action_id": "inspect_wash_station",
                "label": "Inspect Wash Station",
                "type": "note",
                "text": (
                    "A stone sink and drain rack sit near the entrance to keep contamination away from active mixtures. "
                    "Drying rods hold sterilized glassware in strict size order.\n\n"
                    "A carved warning over the basin reads: 'Rinse before reuse, or poison by habit.'"
                ),
            },
            {
                "action_id": "check_supply_crates",
                "label": "Check Supply Crates",
                "type": "note",
                "text": (
                    "Stacked crates contain charcoal, limestone, sulfur packets, and cloth-wrapped root bundles sorted by harvest date. "
                    "The inventory is disciplined enough to support months of uninterrupted work.\n\n"
                    "One crate is reserved for failed compounds, each sealed with a tag describing exactly what went wrong."
                ),
            },
        ],
        "layout": _layout(
            [
                "################",
                "#FFFF..BBBB..SS#",
                "#F..F..BBBB..SS#",
                "#....LLEELL....#",
                "#....LLEELL....#",
                "#..TTTTTT......#",
                "#..TTTTTT..VV..#",
                "#..WW....CC.VV.#",
                "#..WW....CC....#",
                "################",
            ],
            [
                _hotspot("furnace", "Check Furnace", "check_furnace", 1, 1, 4, 2),
                _hotspot("distill", "Inspect Distillation Line", "inspect_distillation_line", 6, 3, 4, 2),
                _hotspot("prep", "Read Prep Bench Notes", "read_prep_bench_notes", 2, 5, 6, 2),
                _hotspot("wash", "Inspect Wash Station", "inspect_wash_station", 2, 7, 2, 2),
                _hotspot("flasks", "Inspect Flasks", "inspect_flasks", 12, 6, 2, 2),
                _hotspot("crates", "Check Supply Crates", "check_supply_crates", 9, 7, 2, 2),
            ],
        ),
    },
    "void_sanctuary": {
        "title": "Void Sanctuary",
        "lore": (
            "Sound collapses in this chamber before it reaches the walls. "
            "Even your own steps arrive half a breath late, as if time bends around the sanctuary core.\n\n"
            "Crystals grow from nothing, then dissolve back into nothing, obeying rules no physicist has fully described. "
            "The place is calm, but it is never safe."
        ),
        "interactions": [
            {
                "action_id": "inspect_rift_crystals",
                "label": "Inspect Rift Crystals",
                "type": "note",
                "text": (
                    "The crystal lattice shifts between solid and translucent phases in a repeating cycle. "
                    "Each phase emits a different harmonic that you feel in your teeth before you hear it.\n\n"
                    "Relics linked to shadow, blood, and oath magic resonate immediately, confirming these crystals amplify intent as much as power."
                ),
            },
            {
                "action_id": "invoke_ritual",
                "label": "Invoke Ritual",
                "type": "command",
                "command": "invoke ritual",
                "success_text": "You begin the ritual sequence in the sanctuary.",
            },
            {
                "action_id": "read_anchor_plaque",
                "label": "Read Anchor Plaque",
                "type": "note",
                "text": (
                    "A plaque fixed into the stone ring lists anchor phrases used to return from deep ritual trance. "
                    "Each phrase is plain and practical, designed to be remembered under stress.\n\n"
                    "The final line is underlined repeatedly: 'Leave before the room begins answering back.'"
                ),
            },
            {
                "action_id": "inspect_focus_ring",
                "label": "Inspect Focus Ring",
                "type": "note",
                "text": (
                    "The central ring is scored with concentric calibration marks, suggesting many controlled experiments. "
                    "Whoever worked here adjusted standing position by inches to shape the ritual field.\n\n"
                    "Tiny inscriptions between marks record emotional states: fear, resolve, grief, clarity."
                ),
            },
            {
                "action_id": "review_observer_notes",
                "label": "Review Observer Notes",
                "type": "note",
                "text": (
                    "A set of observer notes sits in a weighted folio, each page documenting behavior during void exposure sessions. "
                    "The writer tracked pulse, speech latency, and memory drift.\n\n"
                    "One recurring annotation appears in every session: 'Participant reports hearing advice in their own voice.'"
                ),
            },
            {
                "action_id": "inspect_boundary_marks",
                "label": "Inspect Boundary Marks",
                "type": "note",
                "text": (
                    "Boundary sigils along the outer wall were carved, erased, and carved again with increasing depth. "
                    "The progression implies repeated containment failures followed by rapid corrections.\n\n"
                    "At the newest mark, the stone remains warm, as if the boundary was reinforced recently."
                ),
            },
        ],
        "layout": _layout(
            [
                "################",
                "#....O.....N...#",
                "#..VVVVVVV..N..#",
                "#.VV.....VV....#",
                "#.VV..OO.VV....#",
                "#.VV.....VV..I.#",
                "#..VVVVVVV.....#",
                "#....O.....T...#",
                "#..............#",
                "################",
            ],
            [
                _hotspot("rift", "Inspect Rift Crystals", "inspect_rift_crystals", 2, 2, 7, 5),
                _hotspot("ritual", "Invoke Ritual", "invoke_ritual", 12, 7, 1, 1),
                _hotspot("plaque", "Read Anchor Plaque", "read_anchor_plaque", 12, 1, 1, 2),
                _hotspot("focus", "Inspect Focus Ring", "inspect_focus_ring", 6, 4, 2, 1),
                _hotspot("observer", "Review Observer Notes", "review_observer_notes", 13, 5, 1, 1),
                _hotspot("boundary", "Inspect Boundary Marks", "inspect_boundary_marks", 5, 1, 1, 1),
            ],
        ),
    },
    "clocktower_interior": {
        "title": "Clocktower Interior",
        "lore": (
            "The clocktower interior is part engine room, part cathedral. "
            "Every movement is measured: pendulum sweep, gear transfer, release spring, bell impulse.\n\n"
            "The machinery is old but not decayed. It is maintained by someone meticulous enough to polish teeth on gears "
            "that no surface observer will ever see."
        ),
        "interactions": [
            {
                "action_id": "inspect_gears",
                "label": "Inspect Gears",
                "type": "note",
                "text": (
                    "The primary gears are etched with star coordinates and phase markers rather than simple numbers. "
                    "Rotation here tracks both local hour and seasonal sky position.\n\n"
                    "A maintenance etching on one spoke reads: 'Timekeeping fails first at the edges. Grease the perimeter twice.'"
                ),
            },
            {
                "action_id": "observe_pendulum",
                "label": "Observe Pendulum",
                "type": "note",
                "text": (
                    "The pendulum swings through a narrow window with almost no lateral drift. "
                    "Each pass triggers a fine relay chain that resets micro-errors in the upper gear stack.\n\n"
                    "Its weight is denser than lead and engraved with prayer-like timing intervals."
                ),
            },
            {
                "action_id": "inspect_service_walkway",
                "label": "Inspect Service Walkway",
                "type": "note",
                "text": (
                    "A grated walkway circles the inner chamber, with handholds polished by years of maintenance traffic. "
                    "Tools are still chained to posts in a fixed order by task.\n\n"
                    "The chain tags suggest a two-person crew once serviced this tower nightly."
                ),
            },
            {
                "action_id": "read_calibration_board",
                "label": "Read Calibration Board",
                "type": "note",
                "text": (
                    "A chalk board near the access hatch lists drift corrections for wind, temperature, and bell weight. "
                    "Each correction is dated and signed with initials.\n\n"
                    "The most recent line ends abruptly, as if the engineer was interrupted mid-calculation."
                ),
            },
            {
                "action_id": "inspect_signal_chimes",
                "label": "Inspect Signal Chimes",
                "type": "note",
                "text": (
                    "Secondary chimes are tuned to frequencies too high for crowd signaling but ideal for mechanical diagnostics. "
                    "A wrong tone would expose gear imbalance long before failure.\n\n"
                    "The frame still hums softly, indicating the system is active even when the main bell is silent."
                ),
            },
        ],
        "layout": _layout(
            [
                "################",
                "#..GGG..GGG....#",
                "#..GGG..GGG..K.#",
                "#....P....P..K.#",
                "#....P....P....#",
                "#..G..TT..G....#",
                "#..G..TT..G..N.#",
                "#......C.......#",
                "#..........I...#",
                "################",
            ],
            [
                _hotspot("gears", "Inspect Gears", "inspect_gears", 3, 1, 6, 2),
                _hotspot("pendulum", "Observe Pendulum", "observe_pendulum", 5, 3, 1, 2),
                _hotspot("walkway", "Inspect Service Walkway", "inspect_service_walkway", 3, 5, 6, 2),
                _hotspot("board", "Read Calibration Board", "read_calibration_board", 12, 6, 1, 1),
                _hotspot("chimes", "Inspect Signal Chimes", "inspect_signal_chimes", 12, 2, 1, 2),
            ],
        ),
    },
    "developers_corner": {
        "title": "Developer's Corner",
        "lore": (
            "This room looks lived in: half office, half workshop, equal parts ambition and triage. "
            "Design boards crowd one wall while cable runs and spare parts snake under the desk.\n\n"
            "Nothing here is arranged for show. It is arranged for momentum. "
            "Whoever built this corner worked late, iterated fast, and left breadcrumbs for curious players."
        ),
        "interactions": [
            {
                "action_id": "read_notes",
                "label": "Read Notes",
                "type": "note",
                "text": (
                    "Pinned notes span combat pacing, pet balance, and map readability complaints in blunt shorthand. "
                    "Many are crossed out only after a second column labeled 'player reality check.'\n\n"
                    "One sticky note simply says: 'If they found this room, reward curiosity forever.'"
                ),
            },
            {
                "action_id": "inspect_workstation",
                "label": "Inspect Workstation",
                "type": "note",
                "text": (
                    "The workstation monitor displays build logs beside a giant checklist. "
                    "Most tasks are technical, but one line is personal: 'Make the world feel worth revisiting.'\n\n"
                    "The famous crossed-out item remains: 'Hide this room better.'"
                ),
            },
            {
                "action_id": "read_bug_board",
                "label": "Read Bug Board",
                "type": "note",
                "text": (
                    "A whiteboard tracks old bugs with tiny postmortem notes beside each fix. "
                    "Many entries include player-reported context that shaped the final solution.\n\n"
                    "The board ends with a rule in block letters: 'Fix clarity before complexity.'"
                ),
            },
            {
                "action_id": "inspect_coffee_corner",
                "label": "Inspect Coffee Corner",
                "type": "note",
                "text": (
                    "A side table holds cold mugs, instant packets, and a timer that has been reset too many times to count. "
                    "There are no fancy tools here, just the fuel of long debugging nights.\n\n"
                    "A marker note on the kettle reads: 'Refill before shipping builds.'"
                ),
            },
            {
                "action_id": "review_milestone_journal",
                "label": "Review Milestone Journal",
                "type": "note",
                "text": (
                    "A stitched journal records milestone goals alongside what actually shipped. "
                    "The gap between plan and reality is honest, and often funny.\n\n"
                    "Final page, newest entry: 'Players keep finding better uses for systems than we designed. Keep that energy.'"
                ),
            },
            {
                "action_id": "inspect_reference_shelf",
                "label": "Inspect Reference Shelf",
                "type": "note",
                "text": (
                    "A shelf of dog-eared references covers UX, encounter design, and odd folklore books with folded corners. "
                    "Tabs mark pages about pacing and emotional payoff.\n\n"
                    "Between manuals sits a handwritten card: 'Worldbuilding is also systems design.'"
                ),
            },
        ],
        "layout": _layout(
            [
                "################",
                "#NNN....M..W...#",
                "#NNN....M..W...#",
                "#....DDDD......#",
                "#....DDDD..K...#",
                "#..T......K....#",
                "#..T..S...S..N.#",
                "#......N.......#",
                "#...........I..#",
                "################",
            ],
            [
                _hotspot("notes", "Read Notes", "read_notes", 1, 1, 3, 2),
                _hotspot("workstation", "Inspect Workstation", "inspect_workstation", 8, 1, 1, 2),
                _hotspot("bugs", "Read Bug Board", "read_bug_board", 12, 6, 1, 1),
                _hotspot("coffee", "Inspect Coffee Corner", "inspect_coffee_corner", 2, 5, 1, 2),
                _hotspot("milestones", "Review Milestone Journal", "review_milestone_journal", 12, 4, 1, 2),
                _hotspot("references", "Inspect Reference Shelf", "inspect_reference_shelf", 6, 6, 1, 1),
            ],
        ),
    },
    "default": {
        "title": "Secret Chamber",
        "lore": (
            "Ancient runes glow on the walls with a steady patience that outlived their makers. "
            "This chamber was hidden to preserve something, not simply to conceal it.\n\n"
            "The floor plan is plain but deliberate: a threshold, a center, and a record point. "
            "Someone expected visitors, but only the right kind."
        ),
        "interactions": [
            {
                "action_id": "inspect_chamber",
                "label": "Inspect Chamber",
                "type": "note",
                "text": (
                    "The stone blocks are fitted with unusual precision, and wear patterns show traffic flowing in a single loop. "
                    "Even hidden places collect routines.\n\n"
                    "A faint groove at the center suggests an object once sat here for generations before being removed."
                ),
            }
        ],
        "layout": _layout(
            [
                "################",
                "#..............#",
                "#....R.........#",
                "#...RRR....N...#",
                "#....R.........#",
                "#......T.......#",
                "#..............#",
                "#..............#",
                "#..............#",
                "################",
            ],
            [
                _hotspot("chamber", "Inspect Chamber", "inspect_chamber", 4, 2, 3, 3),
            ],
        ),
    },
}


def get_easter_egg_room_payload(room_id, room_name=None, room_desc=None):
    key = room_id if room_id in EASTER_EGG_ROOM_DATA else "default"
    source = EASTER_EGG_ROOM_DATA[key]
    payload = {
        "room_id": room_id,
        "title": source.get("title") or (room_name or "Secret Chamber"),
        "description": room_desc or "A hidden chamber.",
        "lore": source.get("lore", "A hidden place waits in silence."),
        "interactions": copy.deepcopy(source.get("interactions", [])),
        "layout": copy.deepcopy(source.get("layout", {})),
    }
    if room_name and payload["title"].lower() == "secret chamber":
        payload["title"] = room_name
    return payload


def get_easter_egg_fallback_text(payload):
    title = payload.get("title", "Secret Chamber")
    lore = payload.get("lore", "You enter a hidden place.")
    desc = payload.get("description", "A hidden chamber.")
    return (
        "\n" + "=" * 62 + "\n"
        + f"  SECRET ROOM: {title.upper()}\n"
        + "=" * 62 + "\n"
        + lore + "\n\n"
        + desc + "\n\n"
        + "An interactive room map window has opened.\n"
        + "Click room hotspots to interact, or type 'go back' to return."
    )
