"""The assembly containment box is built from FULL extents. Pin that as behaviour.

`ASSEMBLY_FOOTPRINTS` is documented as full extents because `verify` halves each
axis before comparing - it asks how far a child module sits from its assembly's
centre, not how big the assembly is. That relationship is easy to break in the
direction that matters:

    "SM_Island_Hero is (180.0, 100.0) but the comment says half-extents, so the
     half-extent must be 90.0 x 50.0 - let me fix the data to match the comment."

Nobody would write that on purpose. What happens instead is someone wanting the
containment box to *reach* something, finding the box too small, and adjusting the
number that looks wrong. The comment is what they trust, so it has to be right, and
a correct comment is not enough on its own - this file pins the arithmetic.

The two tests are a matched pair on purpose. The first says a module 89.5 m out on an
island whose spec size is 180 m is INSIDE the footprint, which is only true if the
data are full extents (half of 180 is 90, and 89.5 < 90). The second says a module
91 m out is OUTSIDE, so the check still bites. A box that has been widened until
nothing fails would pass the first and fail the second; a check that stopped
checking would do the reverse. Only both together mean the number is doing work.

Written as `unittest.TestCase` rather than bare pytest functions, because
`import pytest` at module scope made this file FAIL to import inside the engine's
bundled Python (no pytest there), and two red rows in the full automation group
teach people to ignore the full group. As a TestCase it imports cleanly under both
interpreters.

WHAT THAT DOES NOT BUY: the editor's automation runner reports ONE row per module
and only IMPORTS it. It does not execute the assertions - not for bare pytest
functions and not for unittest TestCases. Verified on 2026-10-03 by planting a
deliberately false assertion: host pytest failed it, and the editor run still
reported Success. So a green `Editor.Python.*` row means "this module imports",
never "these laws hold". The only thing that runs these laws is host pytest:
`py -m pytest Content/Python/tests`.
"""

import os
import sys
import unittest

_HERE = os.path.dirname(os.path.abspath(__file__))
_PY = os.path.dirname(_HERE)
if _PY not in sys.path:
    sys.path.insert(0, _PY)

import graybox_spec_reader as reader  # noqa: E402
from homeworld_graybox_spec import Volume  # noqa: E402


def _child_module(name, offset_x, assembly="SM_Island_Hero"):
    """A child of `assembly` sitting `offset_x` along x from its assembly origin.

    `origin_is_explicit=False` is what selects the containment branch: the spec
    gives no world origin for a sub-module, so the verifier cannot compare against
    one and must check it sits inside its parent instead.
    """
    return Volume(
        name=name,
        size_m=(0.4, 0.4, 0.4),
        origin=(0.0, 0.0, 0.0),
        family="heal",
        role="prop",
        spec_id="NODE_PLANT_SLOT",
        family_status="assigned",
        origin_is_explicit=False,
        assembly_origin=(0.0, 0.0, 0.0),
        assembly=assembly,
    )


def _measured_at(name, x):
    return {
        "name": name,
        "type": "MESH",
        "world_origin": [x, 0.0, 0.0],
        "bbox": [0.4, 0.4, 0.4],
        "parent": "SM_IslandTop",
    }


def _blocking_location_findings(findings):
    return [
        finding
        for finding in findings
        if finding["criterion"] == "1_location"
        and finding["severity"] == "blocking"
    ]


class GrayboxContainmentExtentsTest(unittest.TestCase):
    def test_a_module_inside_the_island_footprint_is_not_flagged(self):
        """89.5 m from a 180 m island's centre is inside. Half-extent data would flag it."""
        findings = reader.verify(
            _child_module("SM_Node_89_5m_Out", 89.5), _measured_at("SM_Node_89_5m_Out", 89.5)
        )

        blocking = _blocking_location_findings(findings)

        self.assertFalse(
            blocking,
            "a module 89.5 m out is inside an island whose declared size is 180 m; it was "
            "flagged, so ASSEMBLY_FOOTPRINTS is being read as half-extents: %r" % (blocking,),
        )

    def test_a_module_outside_the_island_footprint_is_still_flagged(self):
        """The other half of the pair: 91 m is past 180/2, so the check must still fire.

        Without this the test above could be satisfied by a containment box wide enough
        to accept anything - which is the failure a loosened constant produces, and the
        one that turns 1_location into a check that always passes.
        """
        findings = reader.verify(
            _child_module("SM_Node_91m_Out", 91.0), _measured_at("SM_Node_91m_Out", 91.0)
        )

        blocking = _blocking_location_findings(findings)

        self.assertTrue(
            blocking,
            "a module 91 m from a 180 m island's centre is outside the footprint and must "
            "be reported - nothing was, so the containment check is not running",
        )

    def test_every_footprint_is_read_as_full_extents(self):
        """Same boundary arithmetic for all three assemblies, not just the island.

        Each `inside_x` is past the midpoint of its assembly's declared x size, so it
        fails only if the data are full extents; each `outside_x` is past half plus
        POSITION_TOLERANCE_M, so it fails only if the check is still live.
        """
        cases = [
            ("SM_Island_Hero", (180.0, 100.0), 89.5, 91.0),
            ("SM_Cabin", (5.5, 4.5), 2.0, 3.5),
            ("SM_Garden_Beds", (4.0, 2.5), 1.5, 2.5),
        ]

        for assembly, footprint, inside_x, outside_x in cases:
            # subTest, so one assembly failing does not hide the other two. A loop
            # with bare asserts would report only the first failure and leave it
            # looking like the whole table agrees.
            with self.subTest(assembly=assembly):
                actual = tuple(reader.ASSEMBLY_FOOTPRINTS[assembly])
                self.assertEqual(len(actual), len(footprint), "footprint shape changed")
                for axis, (got, want) in enumerate(zip(actual, footprint)):
                    self.assertAlmostEqual(
                        got, want, places=6,
                        msg="%s axis %d: declared %r, expected %r"
                            % (assembly, axis, got, want),
                    )

                half = footprint[0] * 0.5 + reader.POSITION_TOLERANCE_M
                self.assertLess(inside_x, half, "test setup: 'inside' point is not inside")
                self.assertGreater(outside_x, half, "test setup: 'outside' point is not outside")

                inside = _blocking_location_findings(
                    reader.verify(
                        _child_module("SM_Inside", inside_x, assembly),
                        _measured_at("SM_Inside", inside_x),
                    )
                )
                outside = _blocking_location_findings(
                    reader.verify(
                        _child_module("SM_Outside", outside_x, assembly),
                        _measured_at("SM_Outside", outside_x),
                    )
                )

                self.assertFalse(inside, "%s: %r should sit inside" % (assembly, inside))
                self.assertTrue(outside, "%s: %r should sit outside" % (assembly, outside))


# No `if __name__ == "__main__": unittest.main()` here, deliberately. The editor's
# automation runner IMPORTS each module under Content/Python/tests/ with __name__
# set to "__main__", so that block executes during import: unittest discovers 0 tests
# against the importing module, prints OK, then calls sys.exit() and raises
# SystemExit out of the import - which the runner reports as a Fail. Measured on
# 2026-10-03. Run these with pytest, or `python -m unittest`, both of which work
# without the block.