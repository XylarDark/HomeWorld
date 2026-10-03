# Copyright HomeWorld. All Rights Reserved.

"""The floating-island top datum must be able to FAIL.

The homestead is a floating island, so `origin: ground_contact` was an
assertion about a thing that does not exist there. It was replaced with a
top-surface datum check. A check that cannot fail is decoration, and
replacing a failing check with an un-failable one is exactly how a gate gets
quietly made weaker -- so this module proves the replacement has teeth.

Three ways to violate the datum are covered:

* the origin drifts off the declared plane,
* the mesh top stops reaching the plane,
* the origin cannot be measured at all.

Plus two scoping tests, because a datum that leaked onto every volume would
turn one island's criterion into a project-wide weakening.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

_PY = Path(__file__).resolve().parents[1]
if str(_PY) not in sys.path:
    sys.path.insert(0, str(_PY))

import graybox_spec_reader as R  # noqa: E402
import homeworld_graybox_spec as S  # noqa: E402


def _island_volume():
    """The floating island as the loader actually builds it from the spec."""
    for spec in S.load_all_specs():
        for volume in spec.volumes:
            if volume.name == "SM_Island_Hero":
                return volume
    raise AssertionError("SM_Island_Hero is not in the parsed specs")


def _blocking(measured):
    return [
        f
        for f in R.verify(_island_volume(), measured)
        if f.get("severity") == "blocking"
    ]


class TopDatumCanFail(unittest.TestCase):
    """Each case mutates the measurement into a state that must be caught."""

    def test_origin_off_the_declared_plane_fails(self):
        # Island dragged 0.5 m up: every socket is now half a metre off the
        # walkable surface. This is the bug the criterion exists to catch.
        findings = _blocking(
            {
                "type": "MESH",
                "bbox": [19.3, 10.7, 0.45],
                "tris": 60,
                "polys": 18,
                "materials": ["M_StylizedGrass"],
                "scale": [1.0, 1.0, 1.0],
                "scale_applied": True,
                "origin_z_world": 0.5,
                "lowest_vert_z_world": 0.05,
                "top_vert_z_world": 0.5,
                "pivot_is_ground_contact": False,
            }
        )
        self.assertTrue(
            any("world_top_z" in f["detail"] for f in findings),
            "an island origin 0.5 m off its declared datum must be blocking, "
            "got: %r" % (findings,),
        )

    def test_top_surface_not_reaching_the_plane_fails(self):
        # Origin correct, but the walkable surface itself sits below the datum
        # the sockets were placed against -- a silently sunk island.
        findings = _blocking(
            {
                "type": "MESH",
                "bbox": [19.3, 10.7, 0.45],
                "tris": 60,
                "polys": 18,
                "materials": ["M_StylizedGrass"],
                "scale": [1.0, 1.0, 1.0],
                "scale_applied": True,
                "origin_z_world": 0.0,
                "lowest_vert_z_world": -0.45,
                "top_vert_z_world": -0.30,
                "pivot_is_ground_contact": False,
            }
        )
        self.assertTrue(
            any("walkable top" in f["detail"] for f in findings),
            "an island whose top never reaches world_top_z must be blocking, "
            "got: %r" % (findings,),
        )

    def test_unmeasurable_origin_fails(self):
        # Absence of evidence is not evidence of readiness. If we cannot read
        # the origin we cannot claim the datum holds.
        findings = _blocking(
            {
                "type": "MESH",
                "bbox": [19.3, 10.7, 0.45],
                "tris": 60,
                "polys": 18,
                "materials": ["M_StylizedGrass"],
                "scale": [1.0, 1.0, 1.0],
                "scale_applied": True,
                "origin_z_world": None,
                "lowest_vert_z_world": None,
                "top_vert_z_world": None,
                "pivot_is_ground_contact": False,
            }
        )
        self.assertTrue(
            any("could not be measured" in f["detail"] for f in findings),
            "an unmeasurable floating origin must be blocking, got: %r"
            % (findings,),
        )

    def test_as_authored_passes(self):
        # The real authored measurements: origin on the plane, crust hanging
        # below it. No datum finding, and no ground-contact finding either.
        findings = _blocking(
            {
                "type": "MESH",
                "bbox": [19.3, 10.7, 0.45],
                "tris": 60,
                "polys": 18,
                "materials": ["M_StylizedGrass"],
                "scale": [1.0, 1.0, 1.0],
                "scale_applied": True,
                "origin_z_world": 0.0,
                "lowest_vert_z_world": -0.45,
                "top_vert_z_world": 0.0,
                "pivot_is_ground_contact": False,
            }
        )
        datum = [f for f in findings if "world_top_z" in f["detail"] or "walkable top" in f["detail"]]
        self.assertEqual([], datum, "the authored island must satisfy its own datum")
        self.assertEqual(
            [],
            [f for f in findings if "ground contact" in f["detail"]],
            "a floating island must not be held to a ground-contact criterion",
        )


class DatumIsScoped(unittest.TestCase):
    """A datum must not become a project-wide weakening."""

    def test_only_the_floating_island_carries_a_datum(self):
        dated = [
            (spec.id, v.name)
            for spec in S.load_all_specs()
            for v in spec.volumes
            if v.top_datum_z_m is not None
        ]
        self.assertEqual([("SM_IslandTop", "SM_Island_Hero")], dated)

    def test_ground_contact_still_asserted_for_grounded_volumes(self):
        grounded = sorted(
            v.name
            for spec in S.load_all_specs()
            for v in spec.volumes
            if v.pivot_is_ground_contact
        )
        self.assertIn("SM_Cliff_LookoutFace", grounded)
        self.assertIn("SM_Cliff_Rear", grounded)
        self.assertNotIn("SM_Island_Hero", grounded)

    def test_ground_contact_criterion_still_fires(self):
        """The old check must not have been deleted, only scoped away here."""
        cliff = None
        for spec in S.load_all_specs():
            for volume in spec.volumes:
                if volume.name == "SM_Cliff_Rear":
                    cliff = volume
        self.assertIsNotNone(cliff)
        self.assertTrue(cliff.pivot_is_ground_contact)
        findings = R.verify(
            cliff,
            {
                "type": "MESH",
                "bbox": [12.0, 2.0, 5.0],
                "tris": 60,
                "polys": 18,
                "materials": ["M_CliffRock"],
                "scale": [1.0, 1.0, 1.0],
                "scale_applied": True,
                "origin_z_world": 0.0,
                "lowest_vert_z_world": -1.5,
                "top_vert_z_world": 3.5,
                "pivot_is_ground_contact": False,
            },
        )
        self.assertTrue(
            any("ground contact" in f["detail"] for f in findings),
            "ground-contact volumes must still be held to ground contact",
        )


if __name__ == "__main__":
    unittest.main()