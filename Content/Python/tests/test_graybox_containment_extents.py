"""The assembly containment box is built from FULL extents. Pin that as behaviour.

`ASSEMBLY_FOOTPRINTS` is documented as full extents because `verify` halves each
axis before comparing - it asks how far a child module sits from its assembly's
centre, not how big the assembly is. That relationship is easy to break in the
direction that matters:

    "SM_Island_Hero is (21.0, 14.0) but the comment says half-extents, so the
     half-extent must be 10.5 x 7.0 - let me fix the data to match the comment."

Nobody would write that on purpose. What happens instead is someone wanting the
containment box to *reach* something, finding the box too small, and adjusting the
number that looks wrong. The comment is what they trust, so it has to be right, and
a correct comment is not enough on its own - this file pins the arithmetic.

The two tests are a matched pair on purpose. The first says a module 8 m out on an
island whose spec size is 21 m is INSIDE the footprint, which is only true if the
data are full extents (half of 21 is 10.5, and 8 < 10.5). The second says a module
12 m out is OUTSIDE, so the check still bites. A box that has been widened until
nothing fails would pass the first and fail the second; a check that stopped
checking would do the reverse. Only both together mean the number is doing work.
"""

import os
import sys

import pytest

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


def test_a_module_inside_the_island_footprint_is_not_flagged():
    """8 m from a 21 m island's centre is inside. Half-extent data would flag it."""
    findings = reader.verify(
        _child_module("SM_Node_8m_Out", 8.0), _measured_at("SM_Node_8m_Out", 8.0)
    )

    blocking = _blocking_location_findings(findings)

    assert not blocking, (
        "a module 8 m out is inside an island whose declared size is 21 m; it was "
        "flagged, so ASSEMBLY_FOOTPRINTS is being read as half-extents: %r" % (blocking,)
    )


def test_a_module_outside_the_island_footprint_is_still_flagged():
    """The other half of the pair: 12 m is past 21/2, so the check must still fire.

    Without this the test above could be satisfied by a containment box wide enough
    to accept anything - which is the failure a loosened constant produces, and the
    one that turns 1_location into a check that always passes.
    """
    findings = reader.verify(
        _child_module("SM_Node_12m_Out", 12.0), _measured_at("SM_Node_12m_Out", 12.0)
    )

    blocking = _blocking_location_findings(findings)

    assert blocking, (
        "a module 12 m from a 21 m island's centre is outside the footprint and must "
        "be reported - nothing was, so the containment check is not running"
    )


@pytest.mark.parametrize(
    "assembly, footprint, inside_x, outside_x",
    [
        ("SM_Island_Hero", (21.0, 14.0), 9.0, 12.0),
        ("SM_Cabin", (5.5, 4.5), 2.0, 3.5),
        ("SM_Garden_Beds", (4.0, 2.5), 1.5, 2.5),
    ],
)
def test_every_footprint_is_read_as_full_extents(assembly, footprint, inside_x, outside_x):
    """Same boundary arithmetic for all three assemblies, not just the island.

    Each `inside_x` is past the midpoint of its assembly's declared x size, so it
    fails only if the data are full extents; each `outside_x` is past half plus
    POSITION_TOLERANCE_M, so it fails only if the check is still live.
    """
    assert reader.ASSEMBLY_FOOTPRINTS[assembly] == pytest.approx(footprint)

    half = footprint[0] * 0.5 + reader.POSITION_TOLERANCE_M
    assert inside_x < half, "test setup: 'inside' point is not inside"
    assert outside_x > half, "test setup: 'outside' point is not outside"

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

    assert not inside, "%s: %r should sit inside" % (assembly, inside)
    assert outside, "%s: %r should sit outside" % (assembly, outside)
