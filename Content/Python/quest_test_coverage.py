# quest_test_coverage.py
# DECLARED coverage for the opening sweep: which C++ automation tests cover
# each beat, and which checks stay human-only.
#
# This is a declaration, not an inference. Nothing here is derived from test
# names: each row was read from the test body it points at (the BeastEncounter
# component, for example, is the bull system, not the opening dog - a name
# inference would have filed it under the wrong beat). The preflight and the
# coverage matrix (run_quest_tests_host.py --coverage) verify that every name
# below exists as an automation test in Source/HomeWorld, and warn when it has
# stopped existing.
#
# An empty `tests` list is a real finding and stays empty: it says the sweep
# state machine for that beat has no C++ automation behind it, so the matrix
# and the human pass table carry the whole weight. That is what the gap is
# supposed to look like in a tool: visible, not papered over.
#
# `human` lists the parts of the beat that only the human pass
# (Docs/qa/TUTORIAL_PLAYTEST_QUEUE.md) can judge - feel, sightline, wording,
# gesture - the things the night-wisp tests' own header calls "human checks".

"""Declared coverage rows for the opening quest sweep, in no particular order.

Keys must match manifest beat ids; values declare `tests` (C++ automation
test names, exact) and `human` (what only the human pass can judge).
"""

COVERAGE = {
    "spirit": {
        "tests": [
            # The reveal actor owns spirit_visible and partner_waiting, which is
            # what this beat's manifest checks read.
            "HomeWorld.Systems.Opening.ChildArrivesFirst",
            "HomeWorld.Systems.Opening.ChildRaceRoute",
            # The claimed-spirit fact feeds the displayed steps.
            "HomeWorld.Systems.Opening.QuestLog",
        ],
        "human": [
            "sightline of the spirit approach (can you not see it from over the hill?)",
            "the E prompt wording at the spirit",
        ],
    },
    "herbs": {
        "tests": [
            # The opening herb facts feed the displayed steps; the zone spec pins
            # where herb beds are allowed to sit at all.
            "HomeWorld.Systems.Opening.QuestLog",
            "HomeWorld.T0.ZoneGenerator.HerbSpacingAndPineCap",
        ],
        "human": [
            "trace-heart draw feel on the herb bed",
            "hover prompt while aiming at the bed",
        ],
    },
    "backpack": {
        "tests": [
            # Whole-way-through: placed prop, real trace, real latch.
            "HomeWorld.T0.NodeGate.BackpackBeatFiresFromTaggedProp",
            # The backpack's law (equip gates inventory) and its refusal gates.
            "HomeWorld.T0.M4.InventoryGatedByBackpack",
            "HomeWorld.T0.DayGates.RefuseAtDuskAndNight",
            "HomeWorld.Systems.Opening.QuestLog",
        ],
        "human": [
            "the gift beat wording when the partner hands it over",
        ],
    },
    "kettle": {
        "tests": [
            # Brew gate law and the pick -> brew chain touching the same verb.
            "HomeWorld.T0.M2.TeaGateOffWithoutBrew",
            "HomeWorld.T0.FL2.GardenPickThenTea",
            "HomeWorld.T0.DayGates.RefuseAtDuskAndNight",
            "HomeWorld.Systems.Opening.QuestLog",
            "HomeWorld.HomeLoop.KettleStillBrews",
            "HomeWorld.HomeLoop.OpeningSprintUntouched",
            "HomeWorld.HomeLoop.MistimeServes",
            "HomeWorld.HomeLoop.GreensHerbOffOpening",
        ],
        "human": [
            "counter hover and pour feel at the kettle",
        ],
    },
    "station": {
        "tests": [
            # Mixed-herb state is read by the quest log (feed the dog);
            # no test drives the counter open/mix state machine itself.
            "HomeWorld.Systems.Opening.QuestLog",
        ],
        "human": [
            "open-then-mix rhythm at the counter",
        ],
    },
    "dog": {
        "tests": [
            # The Grace trace: shape law, wrong-shape miss, spend on match, and
            # the input path that runs it.
            "HomeWorld.Systems.Stroke.GraceMatchesItsShape",
            "HomeWorld.Systems.Stroke.WrongShapeMisses",
            "HomeWorld.Systems.Stroke.HerbSpendsOnMatch",
            "HomeWorld.Systems.Stroke.PawnInputRunsTheHold",
            "HomeWorld.Systems.Opening.QuestLog",
        ],
        "human": [
            "Grace trace draw feel (the click gesture itself)",
            "slow-approach pacing while the dog watches",
        ],
    },
    "fish": {
        "tests": [
            # Only the quest-log fact so far; the pond catch has no automation.
            "HomeWorld.Systems.Opening.QuestLog",
        ],
        "human": [
            "the catch itself at the pond edge (E, one fish - no test drives it)",
        ],
    },
    "sleep": {
        "tests": [
            # The bed law at night and on Day, plus the bed-start latch the
            # night-loop tests assert in their setup.
            "HomeWorld.T0.M11.BedAtNightGrantsSpirit",
            "HomeWorld.T0.M11.DayBedStaysBody",
            "HomeWorld.Systems.Opening.NightWisp.DepositStartsHeal",
            "HomeWorld.Systems.Opening.QuestLog",
        ],
        "human": [
            "the form shift as the night starts (camera and breath)",
        ],
    },
    "night": {
        "tests": [
            # Night on, wisps spawned and tagged; the reveal partner waits.
            "HomeWorld.Systems.Opening.NightWisp.DepositStartsHeal",
            "HomeWorld.Systems.Opening.ChildArrivesFirst",
        ],
        "human": [
            "wisp glow readability from the bed",
            "the partner's night line wording",
        ],
    },
    "collect": {
        "tests": [
            # Carried-wisp accounting: the deposit tests pin what a carried
            # wisp is worth and what its absence costs.
            "HomeWorld.Systems.Opening.NightWisp.DepositStartsHeal",
            "HomeWorld.Systems.Opening.NightWisp.DepositNeedsWisp",
            "HomeWorld.Systems.Opening.NightWisp.DepositNeedsHerb",
        ],
        "human": [
            "the click-heart gesture on the aimed wisp",
        ],
    },
    "heal": {
        "tests": [
            # The full deposit state machine: start, herb precondition, wisp
            # precondition, and spring range.
            "HomeWorld.Systems.Opening.NightWisp.DepositStartsHeal",
            "HomeWorld.Systems.Opening.NightWisp.DepositNeedsHerb",
            "HomeWorld.Systems.Opening.NightWisp.DepositNeedsWisp",
            "HomeWorld.Systems.Opening.NightWisp.DepositNeedsSpringRange",
        ],
        "human": [
            "the 20s heal wait feel and the healed wisp's follow arc",
        ],
    },
}
