"""The polish readiness gate must fail honestly, and there must be a way to prove it does.

This file exists because the gate's whole purpose is to stop a stage being entered
without a measurement behind it, and a guard that cannot be shown to fail is not a
guard. Every test here is a claim that some plausible future edit would otherwise
turn the gate green without measuring anything.

Three classes of quiet failure are covered:

  1. FAIL-OPEN DERIVATION. Gate state is computed from its checks. If the
     computation degrades - state read from a field that is always zero, an empty
     check list treated as "nothing to complain about", an empty report treated as
     a clean one - the gate reports GREEN while measuring nothing.

  2. MISSING READ AS PASS. The load-bearing distinction is PASS versus MISSING.
     An absent artifact has to report MISSING, and any gate holding one has to go
     RED. This is the specific failure that made `run_ue_automation.py` report
     0/0 forever: the UTF-8 BOM raised, a bare `except` caught it, and the
     not-found branch was indistinguishable from a run that passed.

  3. WAIVERS THAT COVER MORE THAN THEY SAY. Waivers exist so a human can accept a
     blocker without pretending it was fixed. They stop doing that job the moment
     one can cover a blocker it was not written for.

Written as `unittest.TestCase` rather than bare pytest functions, because
`import pytest` at module scope fails inside the engine's bundled Python, and red
rows in the full automation group teach people to ignore the full group.

WHAT THAT DOES NOT BUY: the editor's automation runner reports ONE row per module
and only IMPORTS it. It does not execute these assertions. Verified on 2026-10-03
by planting a deliberately false assertion - host pytest failed it while the
editor run still reported Success. A green `Editor.Python.*` row means "this module
imports", never "these laws hold". Only host pytest runs them:
`py -m pytest Content/Python/tests`.
"""

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "Content" / "Python" / "polish_readiness.py"

_spec = importlib.util.spec_from_file_location("polish_readiness", SCRIPT)
pr = importlib.util.module_from_spec(_spec)
sys.modules["polish_readiness"] = pr
_spec.loader.exec_module(pr)


def _fixture_findings():
    """A synthetic greybox report holding the two real SM_Island_Hero blockers.

    Both are filed under criterion `2_sized` for the same volume. That collision is
    the point: it is why the gate narrows by detail text, and why waivers key on
    the full identity.
    """
    return {
        "findings": [
            {"criterion": "2_sized", "volume": "SM_Island_Hero",
             "severity": "blocking",
             "detail": "y bbox 10.700 vs spec 14.000 (off by 3.300, tolerance 1.400)"},
            {"criterion": "2_sized", "volume": "SM_Island_Hero",
             "severity": "blocking",
             "detail": "origin is not at ground contact (lowest vertex at Z -0.450)"},
            {"criterion": "master_binding", "volume": "M_ValleyNight",
             "severity": "blocking",
             "detail": "material in the blend is neither one of the ten masters "
                       "nor an allowed instance (art bible S10)"},
        ]
    }


SIZE_KEY = ("2_sized", "SM_Island_Hero",
            "y bbox 10.700 vs spec 14.000 (off by 3.300, tolerance 1.400)")
PIVOT_KEY = ("2_sized", "SM_Island_Hero",
             "origin is not at ground contact (lowest vertex at Z -0.450)")


_UNSET = object()


def _check(waivers, criterion, detail_match, report=_UNSET):
    # A bare `report=None` default cannot express "pass an absent report", because
    # None is also the sentinel for "use the fixture". Without a distinct sentinel
    # the MISSING-vs-PASS distinction under test is untestable.
    body = _fixture_findings() if report is _UNSET else report
    return pr._criterion_check(
        "t", criterion, "req", waivers,
        detail_match=detail_match, report=body,
    )


class GateDerivationFailsClosed(unittest.TestCase):
    """State must be derived from checks, and an absence of checks is not a pass."""

    def test_empty_gate_is_not_green(self):
        gate = pr.Gate("X", "empty", "n/a")
        self.assertEqual(gate.state, pr.MISSING,
                         "a gate that evaluated nothing must never read GREEN")

    def test_all_missing_gate_is_red(self):
        gate = pr.Gate("Y", "missing", "n/a",
                       [pr.Check("a", "Y", "", "", "", "", pr.MISSING)])
        self.assertEqual(gate.state, pr.RED)

    def test_waived_counts_separately_from_passed(self):
        gate = pr.Gate("Z", "mixed", "n/a", [
            pr.Check("a", "Z", "", "", "", "", pr.PASS),
            pr.Check("b", "Z", "", "", "", "", pr.WAIVED),
        ])
        self.assertEqual(gate.state, pr.GREEN)
        self.assertEqual(gate.tally(), {pr.PASS: 1, pr.WAIVED: 1},
                         "a waiver must not be counted as a pass - it is a decision")

    def test_stale_makes_a_gate_red(self):
        gate = pr.Gate("W", "stale", "n/a",
                       [pr.Check("a", "W", "", "", "", "", pr.STALE)])
        self.assertEqual(gate.state, pr.RED,
                         "a waiver outliving its finding means the gate has stopped "
                         "describing the repo; that is not a green light")


class MissingIsNotPass(unittest.TestCase):
    """An absent artifact is MISSING. It is never PASS, and never a clean report."""

    def test_absent_report_is_missing(self):
        c = pr._criterion_check("t", "2_sized", "req", {},
                                detail_match="bbox",
                                report=None, report_present=False)
        self.assertEqual(c.state, pr.MISSING)

    def test_empty_findings_list_is_a_pass_not_a_crash(self):
        # An empty report is a real state (regenerated, nothing blocking). It is a
        # PASS for that criterion. What must never happen is an empty report being
        # indistinguishable from an absent one.
        #
        # Three-way semantics of the injection parameters, worth stating because
        # the wrong reading is silent and produces a plausible wrong answer:
        #   report={...}                     -> injected; disk ignored
        #   report=None, report_present=True  -> "no injection"; read from disk
        #   report=None, report_present=False -> the artifact does not exist
        self.assertEqual(_check({}, "2_sized", "bbox", report={"findings": []}).state,
                         pr.PASS)
        absent = pr._criterion_check("t", "2_sized", "req", {},
                                     detail_match="bbox",
                                     report=None, report_present=False)
        self.assertEqual(absent.state, pr.MISSING,
                         "an absent report must be distinguishable from an empty one")

    def test_bom_prefixed_json_is_read(self):
        # The exact bug that made the automation runner report 0/0 on every run it
        # ever performed. If the reader regresses to plain utf-8 this fails.
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "bom.json"
            p.write_bytes(b"\xef\xbb\xbf" + json.dumps({"ran": 43}).encode("utf-8"))
            self.assertEqual(pr._read_json(p), {"ran": 43})

    def test_malformed_json_is_missing_not_a_crash(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "bad.json"
            p.write_text("{not json", encoding="utf-8")
            self.assertIsNone(pr._read_json(p))

    def test_json_array_is_not_accepted_as_an_object(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "list.json"
            p.write_text("[1, 2, 3]", encoding="utf-8")
            self.assertIsNone(pr._read_json(p),
                              "a list is not a report; treating it as one is a pass")


class TraversalReachabilityIsHonest(unittest.TestCase):
    """An empty budget report must not read as a passed one.

    `env.traversal_reachable` exists because `island circuit 45-90 s` implies
    270-540 m of walking against a 48 m authored perimeter. That finding is only
    worth anything if the gate cannot also be satisfied by a report that measured
    nothing, so the degenerate inputs are pinned here.
    """

    def _with_budget(self, body):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "TRAVERSAL_BUDGET.json"
            p.write_text(json.dumps(body), encoding="utf-8")
            saved = pr.TRAVERSAL_BUDGET
            pr.TRAVERSAL_BUDGET = p
            try:
                return pr.check_env_traversal_reachable()
            finally:
                pr.TRAVERSAL_BUDGET = saved

    def test_absent_report_is_missing(self):
        saved = pr.TRAVERSAL_BUDGET
        pr.TRAVERSAL_BUDGET = Path(tempfile.gettempdir()) / "__no_such_budget__.json"
        try:
            self.assertEqual(pr.check_env_traversal_reachable().state, pr.MISSING)
        finally:
            pr.TRAVERSAL_BUDGET = saved

    def test_empty_windows_is_missing_not_pass(self):
        c = self._with_budget({"verdict": "REACHABLE", "windows": {}})
        self.assertEqual(c.state, pr.MISSING,
                         "a report that evaluated zero windows measured nothing; "
                         "an empty window list must never read as a pass")

    def test_failing_window_fails_the_check(self):
        c = self._with_budget({
            "verdict": "NOT_REACHABLE",
            "windows": {"island_circuit_s": {
                "state": "NOT_REACHABLE", "note": "5.6 laps of a 48 m island"}},
        })
        self.assertEqual(c.state, pr.FAIL)
        self.assertIn("5.6 laps", c.note,
                      "the note must carry the arithmetic, not just a verdict")

    def test_unmeasured_window_is_missing(self):
        c = self._with_budget({
            "verdict": "UNMEASURED",
            "windows": {"cabin_to_lookout_s": {"state": "UNMEASURED"}},
        })
        self.assertEqual(c.state, pr.MISSING)

    def test_all_reachable_passes_but_does_not_claim_the_walk_fits(self):
        c = self._with_budget({
            "verdict": "REACHABLE",
            "windows": {"cabin_to_lookout_s": {"state": "REACHABLE"},
                        "island_circuit_s": {"state": "REACHABLE"}},
        })
        self.assertEqual(c.state, pr.PASS)
        self.assertIn("does NOT mean a real walk fits", c.note,
                      "a pass here must not be mistaken for a timing measurement")


class WaiversCoverExactlyOneBlocker(unittest.TestCase):
    """A waiver must accept the blocker it names and nothing else."""

    def test_named_waiver_reports_waived(self):
        c = _check({SIZE_KEY: {"rationale": "accepted"}}, "2_sized", "bbox")
        self.assertEqual(c.state, pr.WAIVED)

    def test_unwaived_blocker_reports_fail(self):
        self.assertEqual(_check({}, "2_sized", "bbox").state, pr.FAIL)

    def test_waiver_does_not_cover_a_sibling_blocker(self):
        # The size mismatch and the bad pivot share a criterion and a volume.
        # Waiving the size must leave the pivot red, or a human accepting "the
        # island is a bit small" would also silently accept "the island floats
        # 45cm above its ground contact".
        c = _check({SIZE_KEY: {"rationale": "accepted"}}, "2_sized",
                   "ground contact")
        self.assertEqual(c.state, pr.FAIL)

    def test_stale_waiver_reports_stale(self):
        c = _check({("2_sized", "SM_Gone", "no longer exists"): {}},
                   "2_sized", "bbox")
        self.assertEqual(c.state, pr.STALE)

    def test_filter_matching_nothing_is_a_pass(self):
        # The inverse hazard: a filter narrower than the data matches nothing and
        # would otherwise be indistinguishable from "fixed". Asserted explicitly
        # so that if this ever becomes an error, the reason is on record.
        self.assertEqual(_check({}, "2_sized", "no such substring").state, pr.PASS)


class TraversalWindowsAreReadFromCanon(unittest.TestCase):
    """The gate owns no numbers. Targets come from FEEL.md, and bounds are inclusive."""

    def test_targets_match_canon(self):
        self.assertEqual(pr.TRAVERSAL_TARGETS["cabin_to_lookout_s"], (15.0, 25.0))
        self.assertEqual(pr.TRAVERSAL_TARGETS["island_circuit_s"], (45.0, 90.0))

    def test_window_bounds_are_inclusive(self):
        # Boundary values that hide off-by-one errors: exactly at the limit must
        # pass, one outside must fail. If the comparison were exclusive, a
        # traversal of exactly 25.0s - a perfectly legal walk - would be reported
        # out of canon and send someone to resize an island that was correct.
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "baseline.json"
            p.write_text(json.dumps({
                "cabin_to_lookout_s": {"measured_s": 25.0},
                "island_circuit_s": {"measured_s": 45.0},
            }), encoding="utf-8")
            saved = pr.BASELINE_FILE
            pr.BASELINE_FILE = p
            try:
                self.assertEqual(pr.check_env_traversal_measured().state, pr.PASS)
                p.write_text(json.dumps({
                    "cabin_to_lookout_s": {"measured_s": 25.1},
                    "island_circuit_s": {"measured_s": 45.0},
                }), encoding="utf-8")
                self.assertEqual(pr.check_env_traversal_measured().state, pr.FAIL)
            finally:
                pr.BASELINE_FILE = saved

    def test_unmeasured_key_is_not_treated_as_zero(self):
        # A missing measurement must not read as 0.0 and pass a `0 <= 0 <= 90`
        # style check; it is unmeasured.
        #
        # STATE CORRECTED 2026-10-03. This test used to assert FAIL. FAIL means
        # "measured, and the number is wrong" -- it accuses the world of being
        # mis-sized. But nothing was measured: the baseline file was seeded with
        # nulls and a human has not walked the island. Seeding the skeleton would
        # have flipped this check RED on the Lead's first run and told them to go
        # fix geometry that nobody has timed yet. Unmeasured is MISSING.
        #
        # The original intent of the test survives the change intact: the state is
        # still not PASS, which is the property that actually matters.
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "baseline.json"
            p.write_text(json.dumps({
                "cabin_to_lookout_s": {"measured_s": 20.0},
                "island_circuit_s": {},
            }), encoding="utf-8")
            saved = pr.BASELINE_FILE
            pr.BASELINE_FILE = p
            try:
                c = pr.check_env_traversal_measured()
                self.assertEqual(c.state, pr.MISSING)
                self.assertIn("unmeasured", c.measured)
                self.assertNotEqual(c.state, pr.PASS)
            finally:
                pr.BASELINE_FILE = saved

    def test_a_fully_seeded_skeleton_reports_missing_not_fail(self):
        # The regression that motivated separating MISSING from FAIL: shipping the
        # POLISH_BASELINE.json skeleton -- real artifact, declared keys, all values
        # null -- must NOT accuse anyone of bad measurements, and must NOT go green.
        # Both wrong answers hide the same fact: that nobody has played yet.
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "baseline.json"
            p.write_text(json.dumps({
                "cabin_to_lookout_s": {"measured_s": None},
                "island_circuit_s": {"measured_s": None},
            }), encoding="utf-8")
            saved = pr.BASELINE_FILE
            pr.BASELINE_FILE = p
            try:
                c = pr.check_env_traversal_measured()
                self.assertEqual(c.state, pr.MISSING)
                self.assertNotEqual(c.state, pr.FAIL)
            finally:
                pr.BASELINE_FILE = saved

    def test_absent_artifact_is_still_missing(self):
        # Seeding the skeleton must not have changed how a MISSING FILE reads.
        # Before, no file meant MISSING with the note "no instrument exists"; now a
        # file with nulls means MISSING with a different note. Same state, different
        # guidance -- and the no-file case must not have been lost in the edit.
        with tempfile.TemporaryDirectory() as td:
            saved = pr.BASELINE_FILE
            pr.BASELINE_FILE = Path(td) / "does_not_exist.json"
            try:
                c = pr.check_env_traversal_measured()
                self.assertEqual(c.state, pr.MISSING)
                self.assertIn("no artifact", c.measured)
            finally:
                pr.BASELINE_FILE = saved

    def test_bool_is_not_a_measurement(self):
        # True is an int in Python, so `isinstance(True, (int, float))` is True.
        # A stray `true` in hand-edited JSON would otherwise measure a walk of 1
        # second and report a confident PASS.
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "baseline.json"
            p.write_text(json.dumps({
                "cabin_to_lookout_s": {"measured_s": True},
                "island_circuit_s": {"measured_s": True},
            }), encoding="utf-8")
            saved = pr.BASELINE_FILE
            pr.BASELINE_FILE = p
            try:
                self.assertEqual(pr.check_env_traversal_measured().state, pr.MISSING)
            finally:
                pr.BASELINE_FILE = saved


class TunableBaselines(unittest.TestCase):
    """A declared placeholder must not be counted as a measured value.

    `POLISH_BASELINE.json` ships with all six FEEL.md tunables present and null, so
    the human fills in numbers instead of inventing a schema. The hazard is
    specific and quiet: the check used to report PASS for *any* non-empty `tunables`
    dict, so seeding six nulls would have turned the G-FEEL gate green over zero
    measurements.
    """

    def _baseline(self, td, tunables):
        p = Path(td) / "baseline.json"
        p.write_text(json.dumps({"tunables": tunables}), encoding="utf-8")
        return p

    def test_all_null_tunables_are_not_a_baseline(self):
        with tempfile.TemporaryDirectory() as td:
            p = self._baseline(td, {k: None for k in pr.FEEL_TUNABLES})
            saved = pr.BASELINE_FILE
            pr.BASELINE_FILE = p
            try:
                c = pr.check_feel_tunable_baselines()
                self.assertEqual(c.state, pr.MISSING)
                self.assertNotEqual(c.state, pr.PASS)
                self.assertIn("0/6", c.measured)
            finally:
                pr.BASELINE_FILE = saved

    def test_one_arbitrary_key_does_not_satisfy_all_six(self):
        # Without a named list, one key would clear a ">0 baselines" test and the
        # gate would report 1/1 measured while five tunables stayed untouched.
        with tempfile.TemporaryDirectory() as td:
            p = self._baseline(td, {"glide_gravity_scale": 0.45})
            saved = pr.BASELINE_FILE
            pr.BASELINE_FILE = p
            try:
                c = pr.check_feel_tunable_baselines()
                self.assertEqual(c.state, pr.MISSING)
                self.assertIn("1/6", c.measured)
                self.assertIn("night_length_s", c.note)
            finally:
                pr.BASELINE_FILE = saved

    def test_partial_fill_names_what_is_left(self):
        with tempfile.TemporaryDirectory() as td:
            p = self._baseline(td, {
                "glide_gravity_scale": 0.45,
                "glide_lateral_influence": 0.0,
                "camera_arm_length_uu": 420,
            })
            saved = pr.BASELINE_FILE
            pr.BASELINE_FILE = p
            try:
                c = pr.check_feel_tunable_baselines()
                self.assertEqual(c.state, pr.MISSING)
                for pending in ("camera_pitch_bias_deg", "night_length_s",
                                "gather_cooldown_s"):
                    self.assertIn(pending, c.note)
            finally:
                pr.BASELINE_FILE = saved

    def test_all_six_measured_passes(self):
        with tempfile.TemporaryDirectory() as td:
            p = self._baseline(td, {
                "glide_gravity_scale": 0.45,
                "glide_lateral_influence": 0.0,
                "camera_arm_length_uu": 420,
                "camera_pitch_bias_deg": -11.0,
                "night_length_s": 120,
                "gather_cooldown_s": 90,
            })
            saved = pr.BASELINE_FILE
            pr.BASELINE_FILE = p
            try:
                self.assertEqual(pr.check_feel_tunable_baselines().state, pr.PASS)
            finally:
                pr.BASELINE_FILE = saved


class CanonWindowSync(unittest.TestCase):
    """The gate's traversal windows are literals; canon moves; drift must be loud.

    An earlier revision of polish_readiness.py carried the comment "Read from that
    file rather than restated, so the gate cannot drift from canon. Parsed out of
    the markdown table." It was false -- the values were dict literals -- and the
    same module's docstring said "nothing reads them". Canon then moved on
    2026-10-03 without touching the literals. So the claim is now checked.

    Every test here is a mutation: a plausible edit to canon or to the gate that
    would otherwise drift silently.
    """

    def _with_feel(self, body):
        """Point the gate at a temporary FEEL.md and yield control."""
        td = tempfile.TemporaryDirectory()
        p = Path(td.name) / "FEEL.md"
        p.write_text(body, encoding="utf-8")
        saved_path, saved_targets = pr.FEEL_CANON, dict(pr.TRAVERSAL_TARGETS)
        pr.FEEL_CANON = p
        self.addCleanup(td.cleanup)
        self.addCleanup(setattr, pr, "FEEL_CANON", saved_path)
        self.addCleanup(setattr, pr, "TRAVERSAL_TARGETS", saved_targets)
        return td

    def test_shipped_feel_md_actually_parses(self):
        # The row is "Cabin -> lookout walk" with a real arrow and en-dashes. A
        # reader that matched on those characters would find nothing and return an
        # empty dict -- which, read naively, looks like "canon declares no windows"
        # rather than "the parse failed". So parse the REAL file.
        canon, problems = pr.read_canon_windows()
        self.assertEqual(problems, [], f"shipped FEEL.md failed to parse: {problems}")
        self.assertEqual(
            canon,
            {"cabin_to_lookout_s": (15.0, 25.0), "island_circuit_s": (45.0, 90.0)},
        )

    def test_shipped_literals_agree_with_shipped_canon(self):
        self.assertEqual(pr.check_env_canon_windows_in_sync().state, pr.PASS)

    def test_canon_moves_and_the_gate_follows_silently(self):
        # The whole point. Canon narrows the circuit window; the literals do not
        # move; the check must FAIL and name both sides rather than keep reporting
        # "inside canon" for a number the Lead replaced.
        body = (
            "| Tunable | Value | Notes |\n|---|---|---|\n"
            "| Cabin -> lookout walk | ~15-25 s | V1 |\n"
            "| Island circuit | ~30-60 s | V1 |\n"
        )
        self._with_feel(body)
        c = pr.check_env_canon_windows_in_sync()
        self.assertEqual(c.state, pr.FAIL)
        self.assertIn("island_circuit_s", c.measured)
        self.assertIn("45-90", c.measured)
        self.assertIn("30-60", c.measured)

    def test_updating_the_literal_clears_the_failure(self):
        # Otherwise the check is just a permanent FAIL and gets ignored, which is
        # the same failure mode as a permanent PASS.
        body = (
            "| Tunable | Value | Notes |\n|---|---|---|\n"
            "| Cabin -> lookout walk | ~15-25 s | V1 |\n"
            "| Island circuit | ~30-60 s | V1 |\n"
        )
        self._with_feel(body)
        pr.TRAVERSAL_TARGETS = dict(pr.TRAVERSAL_TARGETS, island_circuit_s=(30.0, 60.0))
        self.assertEqual(pr.check_env_canon_windows_in_sync().state, pr.PASS)

    def test_en_dash_and_hyphen_both_parse(self):
        # FEEL.md uses en-dashes. A hand-edit on Windows will often produce ASCII
        # hyphens. Both must parse, or a canon edit silently voids the check.
        for dash in ("-", "\u2013", "\u2014"):
            with self.subTest(dash=dash):
                body = (
                    "| Tunable | Value | Notes |\n|---|---|---|\n"
                    f"| Cabin -> lookout walk | ~15{dash}25 s | V1 |\n"
                    f"| Island circuit | ~45{dash}90 s | V1 |\n"
                )
                self._with_feel(body)
                canon, problems = pr.read_canon_windows()
                self.assertEqual(problems, [])
                self.assertEqual(canon["cabin_to_lookout_s"], (15.0, 25.0))

    def test_absent_canon_is_missing_not_pass(self):
        # A vanished FEEL.md must never read as "in sync". It reads MISSING,
        # because the gate is then judging its own literals against nothing.
        td = tempfile.TemporaryDirectory()
        saved = pr.FEEL_CANON
        pr.FEEL_CANON = Path(td.name) / "gone.md"
        try:
            c = pr.check_env_canon_windows_in_sync()
            self.assertEqual(c.state, pr.MISSING)
            self.assertNotEqual(c.state, pr.PASS)
        finally:
            pr.FEEL_CANON = saved
            td.cleanup()

    def test_row_without_a_range_is_reported_not_skipped(self):
        # "not measured yet" in the value cell. Returning an empty dict here is
        # correct, but it must arrive with a problem attached, or the check
        # degrades to MISSING for a reason nobody can act on.
        body = (
            "| Tunable | Value | Notes |\n|---|---|---|\n"
            "| Cabin -> lookout walk | TBD | V1 |\n"
            "| Island circuit | ~45-90 s | V1 |\n"
        )
        self._with_feel(body)
        canon, problems = pr.read_canon_windows()
        self.assertNotIn("cabin_to_lookout_s", canon)
        self.assertTrue(any("cabin_to_lookout_s" in p or "lookout" in p
                            for p in problems), problems)
        self.assertEqual(pr.check_env_canon_windows_in_sync().state, pr.MISSING)

    def test_descending_range_is_refused(self):
        # "25-15 s" is a typo, not a window. Accepting it would invert the test.
        body = (
            "| Tunable | Value | Notes |\n|---|---|---|\n"
            "| Cabin -> lookout walk | ~25-15 s | V1 |\n"
            "| Island circuit | ~45-90 s | V1 |\n"
        )
        self._with_feel(body)
        canon, problems = pr.read_canon_windows()
        self.assertNotIn("cabin_to_lookout_s", canon)
        self.assertTrue(problems)


class TheShippedSkeletonIsHonest(unittest.TestCase):
    """Assert the real artifact on disk, not a fixture.

    A fixture only proves the code behaves. This proves the file that actually ships
    does not contain invented numbers -- which is the whole claim being made to the
    human: "these are unfilled, not tuned."
    """

    def setUp(self):
        self.path = ROOT / "Docs" / "qa" / "POLISH_BASELINE.json"
        if not self.path.is_file():
            self.skipTest("POLISH_BASELINE.json not present")
        self.data = json.loads(self.path.read_text(encoding="utf-8"))

    def test_no_traversal_window_has_a_measured_value(self):
        for key in pr.TRAVERSAL_TARGETS:
            entry = self.data.get(key)
            self.assertIsNotNone(entry, f"{key} not declared in the skeleton")
            self.assertIsNone(
                entry.get("measured_s"),
                f"{key} carries a measured_s. No human has timed a walk yet -- a "
                f"number here would be invented and would make the gate pass.",
            )

    def test_every_feel_tunable_is_declared_and_null(self):
        tunables = self.data.get("tunables") or {}
        self.assertEqual(
            sorted(tunables), sorted(pr.FEEL_TUNABLES),
            "the skeleton's tunable keys have drifted from FEEL_TUNABLES in the gate",
        )
        for key, value in tunables.items():
            self.assertIsNone(
                value, f"{key} carries a value ({value!r}) but was never measured"
            )

    def test_windows_match_canon_not_the_gate(self):
        # The window belongs to FEEL.md. If the file restates a different one, the
        # human tunes against the file while the gate judges against canon, and the
        # two disagree silently.
        self.assertEqual(
            self.data["cabin_to_lookout_s"]["window_s"],
            list(pr.TRAVERSAL_TARGETS["cabin_to_lookout_s"]),
        )
        self.assertEqual(
            self.data["island_circuit_s"]["window_s"],
            list(pr.TRAVERSAL_TARGETS["island_circuit_s"]),
        )


class ShapeOfTheGate(unittest.TestCase):
    """Structural invariants. A dropped check must be a loud failure, not a quiet one."""

    def test_check_count_matches_expectation(self):
        gates = pr.build()
        total = sum(len(g.checks) for g in gates.values())
        self.assertEqual(total, pr.EXPECTED_CHECKS,
                         "a check was added, removed or renamed - update "
                         "EXPECTED_CHECKS deliberately or the guard is not guarding")

    def test_every_gate_evaluated_something(self):
        for gid, gate in pr.build().items():
            self.assertGreater(len(gate.checks), 0, f"{gid} evaluated nothing")

    def test_dependency_checks_require_their_parent_to_be_green(self):
        gates = pr.build()
        for gid in ("G-ASSET", "G-FEEL"):
            deps = [c for c in gates[gid].checks if c.id.startswith("dep.")]
            self.assertTrue(deps, f"{gid} has no upstream dependency check")
            for d in deps:
                self.assertIn(d.state, (pr.PASS, pr.FAIL))

    def test_selftest_passes(self):
        self.assertEqual(pr.selftest(pr.build()), 0)

    def test_every_blocking_criterion_is_covered(self):
        # The hole this pins: the gate covered four of the five blocking findings
        # in the greybox report and did not say so. `4_distinct` was simply absent,
        # so G-ENV presented itself as gating "greybox" while ignoring one of the
        # two things greybox was blocking on.
        pr.build()
        live = pr._read_json(pr.GRAYBOX_REPORT)
        self.assertIsNotNone(live, "greybox report absent; coverage cannot be asserted")
        blocking_criteria = {str(f.get("criterion", ""))
                             for f in pr.blocking_findings(live)}
        self.assertTrue(blocking_criteria,
                        "report has no blocking findings; this test needs a real one")
        uncovered = sorted(blocking_criteria - pr._COVERED_CRITERIA)
        self.assertEqual(uncovered, [],
                         f"gate does not cover blocking criterion(s) {uncovered}")

    def test_coverage_assertion_would_catch_an_orphan_criterion(self):
        # Prove the assertion is falsifiable: an uncovered blocking criterion has
        # to produce a complaint, or the check above is decorative.
        #
        # Discard AFTER build(), not before. _criterion_check repopulates the set
        # as a side effect, so removing the criterion first is silently undone by
        # the very call that is supposed to be under test - which would make this
        # test pass for the wrong reason, or fail for a confusing one.
        saved = set(pr._COVERED_CRITERIA)
        try:
            gates = pr.build()
            pr._COVERED_CRITERIA.discard("4_distinct")
            rc = pr.selftest(gates)
            self.assertNotEqual(rc, 0,
                                "removing coverage of a blocking criterion was not "
                                "detected")
        finally:
            pr._COVERED_CRITERIA.clear()
            pr._COVERED_CRITERIA.update(saved)


if __name__ == "__main__":
    unittest.main()