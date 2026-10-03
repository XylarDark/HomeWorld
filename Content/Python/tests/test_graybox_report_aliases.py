"""The report must not call a present object absent.

THE DEFECT

`VOLUME_ALIASES` exists because specs name *modules* while the blend authors some of
them as mirrored pairs - `SM_Cabin_Window_Frame_Front` and `_Side`,
`SM_Cabin_Porch_Post_L` and `_R`, the hero island top as `SM_IslandTop`. Its own
docstring states the rule it was written to enforce:

    Reporting "SM_Cabin_Window_Frame not present" when the blend holds
    SM_Cabin_Window_Frame_Front and _Side is a false finding that trains the
    Lead to ignore the report.

The VERIFIER honours that. `measure_scene` expands every alias, and `verify` walks
`resolve_alias` to find the first candidate that is actually there - so `1_location`
and `2_sized` are checked against the real authored mesh.

The MARKDOWN did not. `to_markdown` iterated the raw measurements dict, so it
emitted one `*(absent)*` row per spec name and, right beside it, the alias row
holding the geometry. The report said "not present" about a 19.3 x 10.7 m island
top while simultaneously verifying it. Half the fix was in place and the half the
Lead actually reads was not.

WHY THESE ARE UNIT TESTS AND NOT A BLENDER RUN

`to_markdown` is a pure function of the report dict, and the defect is entirely in
that rendering. The report it was fed is on disk in `Docs/qa/GRAYBOX_SPEC_REPORT.json`,
so the false row is observable without launching Blender - see
`test_the_committed_report_still_shows_the_false_finding`, which fails until the
report is regenerated. That test is the one that would have caught this in review.

Written as `unittest.TestCase` rather than bare pytest functions because
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

import json
import os
import sys
import unittest

_HERE = os.path.dirname(os.path.abspath(__file__))
# Absolute, walked up from __file__. A CWD-relative path here would make the
# committed-report test skip or fail depending on where pytest was invoked from -
# a test that quietly stops checking when run from the wrong directory is the same
# class of defect as the one it is written to catch.
_PY = os.path.dirname(_HERE)
if _PY not in sys.path:
    sys.path.insert(0, _PY)

import graybox_spec_reader as reader  # noqa: E402
from homeworld_graybox_spec import VOLUME_ALIASES, resolve_alias  # noqa: E402

_REPO_ROOT = os.path.dirname(os.path.dirname(_PY))
_COMMITTED_REPORT = os.path.join(_REPO_ROOT, "Docs", "qa", "GRAYBOX_SPEC_REPORT.json")


def _measurement(name, bbox=None, origin=(0.0, 0.0, 0.0)):
    """One measurements row, shaped like the real ones."""
    return {
        "name": name,
        "type": "MESH",
        "world_origin": list(origin),
        "bbox": list(bbox) if bbox else None,
    }


class GrayboxReportAliasesTest(unittest.TestCase):
    def test_resolved_spec_name_is_not_reported_absent(self):
        """The spec name resolves through its alias, so the row shows the geometry."""
        report = {
            "spec_ids": ["SM_Island_Hero"],
            "volume_names": ["SM_Island_Hero"],
            "alias_resolutions": {"SM_Island_Hero": "SM_IslandTop"},
            "measurements": {
                "SM_Island_Hero": None,
                "SM_IslandTop": _measurement("SM_IslandTop", bbox=[19.3, 10.7, 0.45]),
            },
        }

        markdown = reader.to_markdown(report)

        self.assertNotIn(
            "*(absent)*", markdown,
            "the spec name resolved to an authored object, so 'absent' is the false "
            "finding VOLUME_ALIASES was written to prevent",
        )
        self.assertIn("19.3000", markdown, "the resolved object's measured bbox must be shown")
        self.assertIn("SM_IslandTop", markdown, "the row must name the object it resolved to")
        self.assertTrue(
            any(
                line.startswith("| `SM_Island_Hero` |") and "via `SM_IslandTop`" in line
                for line in markdown.splitlines()
            ),
            "the row must say WHICH object was measured - a size with no source is how "
            "the next reader concludes the volume is the wrong object",
        )

    def test_genuinely_absent_volume_is_still_reported_absent(self):
        """The fix must not turn every missing volume into a pass."""
        report = {
            "spec_ids": ["SM_Cabin_Door"],
            "volume_names": ["SM_Cabin_Door"],
            "alias_resolutions": {},
            "measurements": {"SM_Cabin_Door": None},
        }

        markdown = reader.to_markdown(report)

        self.assertIn("*(absent)*", markdown)
        self.assertIn("SM_Cabin_Door", markdown)

    def test_alias_resolved_by_a_later_candidate(self):
        """Only the `_L`/`_Front` half exists; resolution must still find it.

        The mirrored pairs are not authored symmetrically in every case, so a fix that
        assumed the first alias is always present would pass the island test and fail
        here.
        """
        report = {
            "spec_ids": ["SM_Cabin_Porch_Post"],
            "volume_names": ["SM_Cabin_Porch_Post"],
            "alias_resolutions": {"SM_Cabin_Porch_Post": "SM_Cabin_Porch_Post_R"},
            "measurements": {
                "SM_Cabin_Porch_Post": None,
                "SM_Cabin_Porch_Post_L": None,
                "SM_Cabin_Porch_Post_R": _measurement(
                    "SM_Cabin_Porch_Post_R", bbox=[0.15, 0.15, 1.4]
                ),
            },
        }

        markdown = reader.to_markdown(report)

        self.assertNotIn("*(absent)*", markdown)
        self.assertIn("SM_Cabin_Porch_Post_R", markdown)

    def test_pure_alias_rows_do_not_double_count(self):
        """An alias half gets one row, on its spec volume - not a second row of its own.

        Otherwise the table counts `SM_Cabin_Porch_Post` twice, once absent and once
        sized, and a reader counting rows gets a different number of volumes than the
        spec actually names.
        """
        report = {
            "spec_ids": ["SM_Cabin_Porch_Post"],
            "volume_names": ["SM_Cabin_Porch_Post"],
            "alias_resolutions": {"SM_Cabin_Porch_Post": "SM_Cabin_Porch_Post_L"},
            "measurements": {
                "SM_Cabin_Porch_Post": None,
                "SM_Cabin_Porch_Post_L": _measurement(
                    "SM_Cabin_Porch_Post_L", bbox=[0.15, 0.15, 1.4]
                ),
            },
        }

        markdown = reader.to_markdown(report)

        rows = [
            line
            for line in markdown.splitlines()
            if line.startswith("| `SM_Cabin_Porch_Post") or line.startswith("| `SM_Cabin_Porch_Post_")
        ]
        self.assertEqual(
            len(rows), 1, "the alias half must not also get its own row: %r" % rows
        )

    def test_authored_object_that_is_not_a_spec_volume_is_still_listed(self):
        """A measured object no spec names is real geometry and must stay visible."""
        report = {
            "spec_ids": ["SM_Cabin_Door"],
            "volume_names": ["SM_Cabin_Door"],
            "alias_resolutions": {},
            "measurements": {
                "SM_Cabin_Door": _measurement("SM_Cabin_Door", bbox=[1.0, 0.1, 2.0]),
                "SM_Authored_Extra": _measurement("SM_Authored_Extra", bbox=[0.4, 0.4, 0.4]),
            },
        }

        markdown = reader.to_markdown(report)

        self.assertIn("SM_Authored_Extra", markdown)

    def test_a_declared_volume_that_is_also_an_alias_keeps_its_own_row(self):
        """Suppressing alias halves must never delete a volume the specs ask about.

        `SM_IslandTop` is reachable only as an alias of `SM_Island_Hero` today, so the
        collapsing logic is never exercised against a name that is *both* a declared
        volume and an alias half elsewhere. If a spec later declares it directly, the
        filter must let the row through rather than quietly dropping a volume from the
        report.
        """
        report = {
            "spec_ids": ["SM_Island_Hero", "SM_IslandTop"],
            "volume_names": ["SM_Island_Hero", "SM_IslandTop"],
            "alias_resolutions": {"SM_Island_Hero": "SM_IslandTop"},
            "measurements": {
                "SM_Island_Hero": None,
                "SM_IslandTop": _measurement("SM_IslandTop", bbox=[19.3, 10.7, 0.45]),
            },
        }

        markdown = reader.to_markdown(report)

        # Anchor on the row prefix, not a substring: the `SM_Island_Hero` row also
        # mentions SM_IslandTop in its "via" annotation, and counting that as a second
        # row is the mistake this assertion exists to catch in the other direction.
        rows = [
            line
            for line in markdown.splitlines()
            if line.startswith("| `SM_IslandTop` |")
        ]
        self.assertEqual(len(rows), 1, "a declared volume must keep its own row: %r" % rows)
        self.assertNotIn("*(absent)*", markdown)
        self.assertTrue(
            any(
                line.startswith("| `SM_Island_Hero` |") and "via `SM_IslandTop`" in line
                for line in markdown.splitlines()
            ),
            "the aliasing volume must still say what it resolved to",
        )

    def test_report_without_the_new_keys_still_renders(self):
        """`to_markdown` must keep working on a report dict written by an older run.

        The committed JSON on disk has no `volume_names` or `alias_resolutions`, and
        re-reading an old report is a normal thing to do while bisecting a report
        regression. A renderer that hard-fails on a missing key turns a rendering bug
        into an unreadable history.
        """
        report = {
            "spec_ids": ["SM_Cabin_Door"],
            "measurements": {
                "SM_Cabin_Door": _measurement("SM_Cabin_Door", bbox=[1.0, 0.1, 2.0])
            },
        }

        markdown = reader.to_markdown(report)

        self.assertIn("SM_Cabin_Door", markdown)
        self.assertIn("1.0000", markdown)

    def test_every_alias_table_key_is_a_real_volume(self):
        """An alias entry for a name no spec declares is dead weight.

        `VOLUME_ALIASES` is consulted by `measure_scene` and `verify`, so a key that
        matches no volume can never be reached - it reads like coverage and verifies
        nothing. Cheap lint, and it catches a spec being renamed out from under the
        table.
        """
        volumes = reader._all_volumes()
        declared = {volume.name for volume in volumes}

        orphans = sorted(name for name in VOLUME_ALIASES if name not in declared)

        self.assertFalse(
            orphans,
            "VOLUME_ALIASES has entries for names no spec declares: %r - they can never "
            "be reached, so they read as coverage and verify nothing" % (orphans,),
        )

    def test_alias_tuples_start_with_their_own_key(self):
        """The spec name must be first, or the 'best match first' contract is a lie.

        `resolve_alias` documents its result as 'best match first'. Every caller relies
        on the spec name being tried first, so a table that reorders it silently
        changes which object satisfies the volume.
        """
        wrong = sorted(
            name for name, aliases in VOLUME_ALIASES.items() if aliases[0] != name
        )

        self.assertFalse(wrong, "these alias tuples do not lead with their own key: %r" % wrong)

    @unittest.skipUnless(
        os.path.isfile(_COMMITTED_REPORT),
        "committed greybox report not present",
    )
    def test_the_committed_report_still_shows_the_false_finding(self):
        """The report the Lead is actually reading must not contain the defect.

        This is the test that matters on its own. Everything above pins the renderer in
        isolation; this one reads `Docs/qa/GRAYBOX_SPEC_REPORT.json` and asks whether a
        spec name with a measured alias is still rendered `*(absent)*`. It fails until
        the report is regenerated by a run that includes the renderer fix - which is the
        point, because shipping the fix without regenerating leaves the false finding in
        front of the Lead while the tests go green.
        """
        with open(_COMMITTED_REPORT, "r", encoding="utf-8") as handle:
            report = json.load(handle)

        measurements = report.get("measurements") or {}
        with open(
            os.path.join(_REPO_ROOT, "Docs", "qa", "GRAYBOX_SPEC_REPORT.md"),
            "r",
            encoding="utf-8",
        ) as handle:
            markdown = handle.read()

        unbacked = []
        for name, aliases in VOLUME_ALIASES.items():
            if measurements.get(name) is not None:
                continue
            satisfied_by = [
                alias for alias in resolve_alias(name) if measurements.get(alias)
            ]
            if not satisfied_by:
                continue
            row_prefix = "| `%s` |" % name
            for line in markdown.splitlines():
                if line.startswith(row_prefix) and "*(absent)*" in line:
                    unbacked.append((name, satisfied_by[0]))

        self.assertFalse(
            unbacked,
            "the committed report renders these as absent even though an authored "
            "object satisfies them: %r - regenerate it with the renderer fix"
            % (unbacked,),
        )


# No `if __name__ == "__main__": unittest.main()` here, deliberately. The editor's
# automation runner IMPORTS each module under Content/Python/tests/ with __name__
# set to "__main__", so that block executes during import: unittest discovers 0 tests,
# prints OK, then calls sys.exit() and raises SystemExit out of the import - which
# the runner reports as a Fail. Measured on 2026-10-03. Run these with pytest, or
# `python -m unittest`, both of which work without the block.