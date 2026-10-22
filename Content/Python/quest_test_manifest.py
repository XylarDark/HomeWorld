# quest_test_manifest.py
# One entry per hw.Playtest.FastForward stop. This file is data: add a quest here,
# not in quest_test_runner.py.
#
# Adding a quest:
#   1. Add its stop and its `playtest_ff: ready for <name>` line in
#      Source/HomeWorld/HomeWorldCharacter.cpp (DebugFastForwardOpening).
#   2. Add any new state it needs to GetPlaytestStateJson() in the same file.
#   3. Add an entry below. Checks use the small vocabulary implemented in
#      quest_test_contract.py: eq, ne, le, ge, between, near, present, count_tag.
#      The host pytest suite validates every entry before a sweep starts.
#   4. Run: .\Tools\RunTests.ps1 -Quest -QuestOnly <id>
#
# The stop is BEFORE the named action. These are preconditions, not completions.
# The human pass tables in Docs/qa/TUTORIAL_PLAYTEST_QUEUE.md stay human.

"""The opening quest sweep, in chain order."""


def eq(path, value):
    return {"kind": "eq", "path": path, "value": value}


def ne(path, value):
    return {"kind": "ne", "path": path, "value": value}


def le(path, value):
    return {"kind": "le", "path": path, "value": value}


def ge(path, value):
    return {"kind": "ge", "path": path, "value": value}


def between(path, low, high):
    return {"kind": "between", "path": path, "low": low, "high": high}


def near(a, b, cm):
    return {"kind": "near", "a": a, "b": b, "cm": cm}


def present(path):
    return {"kind": "present", "path": path}


def count_tag(tag, value):
    return {"kind": "count_tag", "tag": tag, "value": value}


# How far the pawn may be from the beat's target and still count as placed there.
# The fast-forward asks for 180-260 cm (470 at the spring); this allows for the
# placement search nudging the pawn around a prop.
QUESTS = [
    {
        "id": "spirit",
        "stop": "spirit",
        "section": "Midday",
        "note": "E at the spirit",
        "checks": [
            eq("beat.ready_for", "spirit"),
            eq("quest.spirit_claimed", False),
            eq("actors.reveal.spirit_visible", True),
            le("beat.ready_distance", 300),
        ],
    },
    {
        "id": "herbs",
        "stop": "herbs",
        "section": "Midday",
        "note": "E at the east bed, draw the trace heart",
        "checks": [
            eq("beat.ready_for", "herbs"),
            eq("quest.spirit_claimed", True),
            eq("quest.herbs_gathered", 0),
            eq("actors.reveal.spirit_visible", False),
            le("beat.ready_distance", 300),
        ],
    },
    {
        "id": "backpack",
        "stop": "backpack",
        "section": "The backpack",
        "note": "E at the partner: the backpack",
        "checks": [
            eq("beat.ready_for", "backpack"),
            eq("quest.herbs_gathered", 20),
            eq("quest.herb_tenths", 20),
            eq("quest.herb_west", True),
            eq("quest.herb_east", True),
            eq("actors.reveal.partner_waiting", False),
            le("beat.ready_distance", 300),
        ],
    },
    {
        "id": "kettle",
        "stop": "kettle",
        "section": "Crafting stations",
        "note": "E at the counter: open, mix, then brew",
        "checks": [
            eq("beat.ready_for", "kettle"),
            eq("actors.reveal.partner_waiting", True),
            eq("quest.armor_gift", True),
            eq("quest.kettle_brewed", False),
            eq("quest.station_open", False),
            le("beat.ready_distance", 260),
            between("actors.counter.east_face", 980, 990),
            near("actors.partner.location", "actors.reveal.partner_stand", 80),
        ],
    },
    {
        "id": "station",
        "stop": "station",
        "section": "Crafting stations",
        "note": "E at the counter: open, then mix",
        "checks": [
            eq("beat.ready_for", "station"),
            eq("quest.kettle_brewed", True),
            eq("quest.station_open", False),
            eq("quest.mixed_herbs", 0),
            le("beat.ready_distance", 260),
            between("actors.counter.east_face", 980, 990),
            near("actors.partner.location", "actors.reveal.partner_stand", 80),
        ],
    },
    {
        "id": "dog",
        "stop": "dog",
        "section": "The dog",
        "note": "walk up slowly, draw the Grace trace, then E",
        "checks": [
            eq("beat.ready_for", "dog"),
            eq("quest.station_open", True),
            ge("quest.mixed_herbs", 1),
            eq("actors.dog.tamed", False),
            le("beat.ready_distance", 700),
            near("actors.partner.location", "actors.reveal.partner_stand", 80),
        ],
    },
    {
        "id": "fish",
        "stop": "fish",
        "section": "Fishing",
        "note": "E at the pond bank, one fish",
        "checks": [
            eq("beat.ready_for", "fish"),
            eq("actors.dog.tamed", True),
            eq("quest.fish_caught", False),
            eq("quest.mixed_herbs", 0),
            le("beat.ready_distance", 1200),
            near("actors.partner.location", "actors.reveal.partner_stand", 80),
        ],
    },
    {
        "id": "sleep",
        "stop": "sleep",
        "section": "Night on the island",
        "note": "E at the bed: sleep",
        "checks": [
            eq("beat.ready_for", "sleep"),
            eq("quest.fish_caught", True),
            eq("quest.night_spirit", False),
            le("beat.ready_distance", 260),
            near("actors.partner.location", "actors.reveal.partner_stand", 80),
        ],
    },
    {
        "id": "night",
        "stop": "",
        "section": "Night on the island",
        "note": "night is on, the bed is behind you",
        "checks": [
            eq("beat.ready_for", "night"),
            eq("quest.night_spirit", True),
            eq("actors.reveal.partner_waiting", True),
            count_tag("NODE_OPENING_WISP", 3),
            le("beat.ready_distance", 260),
            between("actors.counter.east_face", 980, 990),
            near("actors.partner.location", "actors.reveal.partner_stand", 80),
        ],
    },
    {
        "id": "collect",
        "stop": "collect",
        "section": "Night on the island",
        "note": "E at the wisp, click the heart",
        "checks": [
            eq("beat.ready_for", "collect"),
            eq("quest.night_spirit", True),
            eq("quest.wisps_collected", 0),
            eq("quest.wisps_carried", 0),
            count_tag("NODE_OPENING_WISP", 3),
            le("beat.ready_distance", 400),
            near("actors.partner.location", "actors.reveal.partner_stand", 80),
        ],
    },
    {
        "id": "heal",
        "stop": "heal",
        "section": "Wisp loop",
        "note": "E at the hot springs, the heal takes 20s",
        "checks": [
            eq("beat.ready_for", "heal"),
            eq("quest.night_spirit", True),
            eq("quest.wisps_carried", 3),
            eq("quest.wisps_healed", 0),
            le("beat.ready_distance", 520),
            near("actors.partner.location", "actors.reveal.partner_stand", 80),
        ],
    },
    {
        "id": "glider",
        "stop": "glider",
        "section": "The glider",
        "note": "E at the armory: craft the glider",
        "checks": [
            eq("beat.ready_for", "glider"),
            eq("quest.glider_crafted", False),
            eq("quest.dawn_wood", 1),
            eq("quest.dawn_silk", 1),
            eq("quest.dawn_metal", 1),
            eq("quest.night_spirit", False),
            le("beat.ready_distance", 300),
        ],
    },
    {
        "id": "delivery",
        "stop": "delivery",
        "section": "Delivery",
        "note": "E at the wood node: set the healed wisp",
        "checks": [
            eq("beat.ready_for", "delivery"),
            eq("quest.glider_crafted", False),
            eq("quest.delivery_wood", 0),
            eq("quest.wisps_healed", 1),
            eq("quest.night_spirit", False),
            count_tag("NODE_OPENING_DELIVERY", 1),
            le("beat.ready_distance", 300),
        ],
    },
    {
        "id": "daycamp",
        "stop": "daycamp",
        "section": "Day camp",
        "note": "walk into the clearing",
        "checks": [
            eq("beat.ready_for", "daycamp"),
            eq("quest.night_spirit", False),
            eq("quest.partner_away", False),
            eq("quest.day_camp_eject", False),
            le("beat.ready_distance", 400),
        ],
    },
    {
        "id": "dawnglide",
        "stop": "dawnglide",
        "section": "Dawn glide",
        "note": "the launch is yours",
        "checks": [
            eq("beat.ready_for", "dawnglide"),
            eq("quest.glider_crafted", True),
            eq("quest.night_spirit", False),
            eq("quest.descent_active", False),
            eq("quest.cloud_carried", 0),
            le("beat.ready_distance", 450),
        ],
    },
    {
        "id": "nightglide",
        "stop": "nightglide",
        "section": "Night glide",
        "note": "travel only, the launch is yours",
        "checks": [
            eq("beat.ready_for", "nightglide"),
            eq("quest.night_spirit", True),
            eq("quest.glider_crafted", True),
            eq("quest.descent_active", False),
            eq("quest.cloud_carried", 0),
            le("beat.ready_distance", 450),
        ],
    },
    {
        "id": "stealth",
        "stop": "stealth",
        "section": "Stealth",
        "note": "reach the guard",
        "checks": [
            eq("beat.ready_for", "stealth"),
            eq("quest.night_spirit", True),
            eq("quest.glider_crafted", True),
            eq("quest.guards_calm", 0),
            eq("quest.descent_active", False),
        ],
    },
    {
        "id": "ease",
        "stop": "ease",
        "section": "Ease",
        "note": "the wind-up is yours",
        "checks": [
            eq("beat.ready_for", "ease"),
            eq("quest.night_spirit", True),
            eq("quest.guards_calm", 0),
            count_tag("NODE_OPENING_EASE", 3),
        ],
    },
    {
        "id": "shrine",
        "stop": "shrine",
        "section": "Shrine",
        "note": "E at the shrine",
        "checks": [
            eq("beat.ready_for", "shrine"),
            eq("quest.night_spirit", True),
            eq("quest.guards_calm", 3),
            eq("quest.partner_walking", False),
            count_tag("NODE_OPENING_EASE", 3),
            count_tag("NODE_CAPTIVE", 1),
            count_tag("NODE_OPENING_SHRINE", 1),
        ],
    },
]


def by_id(quest_id):
    for quest in QUESTS:
        if quest["id"] == quest_id:
            return quest
    return None


def ids():
    return [quest["id"] for quest in QUESTS]
