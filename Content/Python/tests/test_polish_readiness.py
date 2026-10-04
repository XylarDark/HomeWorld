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

import datetime
import importlib.util
import json
import os
import sys
import tempfile
import time
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


class PlaytestRecordCannotBeFakedGreen(unittest.TestCase):
    """The playtest record is the one artifact no automation may stand in for.

    Both checks it feeds used to collapse "not run" into "failed". That is the wrong
    direction of error twice over: it accuses a person of breaking something they
    never tried, and -- far worse -- it leaves `"pass"` as the only alternative, so
    the cheapest way to a green G-FEEL becomes writing eight words of fiction.

    A null must read MISSING. That is the only state that is both true and actionable.

    Each test here is a mutation of the shipped file.
    """

    SHIPPED = ROOT / "Docs" / "qa" / "POLISH_HUMAN_PLAYTEST.json"

    def setUp(self):
        if not self.SHIPPED.is_file():
            self.skipTest("POLISH_HUMAN_PLAYTEST.json not present")
        self.saved = pr.HUMAN_PLAYTEST_FILE
        self.addCleanup(setattr, pr, "HUMAN_PLAYTEST_FILE", self.saved)

    def _use(self, body):
        td = tempfile.TemporaryDirectory()
        p = Path(td.name) / "POLISH_HUMAN_PLAYTEST.json"
        p.write_text(json.dumps(body), encoding="utf-8")
        pr.HUMAN_PLAYTEST_FILE = p
        self.addCleanup(td.cleanup)
        return p

    def _shipped(self):
        return json.loads(self.SHIPPED.read_text(encoding="utf-8"))

    # --- the shipped file ------------------------------------------------

    def test_shipped_record_reports_missing_not_fail(self):
        # FAIL here would read "a playtest was attempted and did not work". The
        # truth is nobody has played. The note has to say which.
        self._use(self._shipped())
        for check in (pr.check_feel_human_playtest(), pr.check_feel_verb_script()):
            with self.subTest(check=check.id):
                self.assertEqual(check.state, pr.MISSING)

    def test_shipped_record_declares_exactly_the_eight_mvp_verbs(self):
        # If the skeleton and the gate disagree about which eight, the human fills
        # in the file and the gate scores something else.
        self.assertEqual(sorted(self._shipped()["verbs"]), sorted(pr.MVP_VERBS))

    def test_shipped_record_contains_no_passing_verb(self):
        # The fabricated-green guard, on the real artifact. Any non-null result here
        # is a claim that a person played a build that has never been played.
        for verb, entry in self._shipped()["verbs"].items():
            with self.subTest(verb=verb):
                self.assertIsNone(
                    pr._verb_result(entry),
                    f"{verb} already carries a result. No human has played this "
                    f"build, so any value here would be invented.",
                )

    def test_shipped_record_names_no_commit(self):
        data = self._shipped()
        self.assertIn("commit", data)
        self.assertIsNone(data["commit"], "a commit here claims a play session")
        self.assertIsNone(data["played_at"])

    # --- the transitions -------------------------------------------------

    def test_a_filled_in_record_does_reach_pass(self):
        # A check that can never go green is decoration; it gets ignored and then it
        # stops catching anything. Prove the happy path actually works, in BOTH the
        # nested form the skeleton ships and the bare-string form.
        filled = {
            "commit": "f218fce", "played_at": "2026-10-04T02:00:00+00:00",
            "verbs": {v: {"how": "x", "result": "pass"} for v in pr.MVP_VERBS},
        }
        self._use(filled)
        self.assertEqual(pr.check_feel_human_playtest().state, pr.PASS)
        self.assertEqual(pr.check_feel_verb_script().state, pr.PASS)

        self._use({**filled, "verbs": {v: "pass" for v in pr.MVP_VERBS}})
        self.assertEqual(pr.check_feel_verb_script().state, pr.PASS)

    def test_one_documented_failure_fails_and_names_the_verb(self):
        verbs = {v: {"result": "pass"} for v in pr.MVP_VERBS}
        verbs["V2"] = {"result": "landed on the valley lip, not the field",
                       "note": "worth a ruling on the 75 m / 95 m delta"}
        self._use({"commit": "abc1234", "played_at": "2026-10-04", "verbs": verbs})
        c = pr.check_feel_verb_script()
        self.assertEqual(c.state, pr.FAIL)
        self.assertIn("V2", c.note)
        self.assertNotIn("V1,", c.note.split("Run and did not pass: ")[1])

    def test_a_verb_object_missing_its_result_is_unrun_not_pass(self):
        # The trap this form invites: seven verbs look filled, and someone adds an
        # eighth object but forgets `result`. Reading the object itself as a result
        # would score a dict != "pass" -> FAIL (wrong); reading it as present would
        # score PASS (worse). It must be MISSING.
        verbs = {v: {"result": "pass"} for v in pr.MVP_VERBS if v != "V7"}
        verbs["V7"] = {"how": "crop + stored", "note": "done, forgot the result"}
        self._use({"commit": "abc1234", "played_at": "2026-10-04", "verbs": verbs})
        c = pr.check_feel_verb_script()
        self.assertEqual(c.state, pr.MISSING)
        self.assertIn("V7", c.note)

    def test_seven_of_eight_is_not_eight(self):
        # The tempting forgery: run what is easy, record the rest as a blanket pass.
        verbs = {v: {"result": "pass"} for v in pr.MVP_VERBS if v != "V2"}
        self._use({"commit": "abc1234", "played_at": "2026-10-04", "verbs": verbs})
        c = pr.check_feel_verb_script()
        self.assertEqual(c.state, pr.MISSING)
        self.assertIn("V2", c.note)

    def test_a_record_without_a_timestamp_is_missing(self):
        # Commit alone is not enough to re-test against -- the binary moves.
        verbs = {v: {"result": "pass"} for v in pr.MVP_VERBS}
        self._use({"commit": "abc1234", "played_at": None, "verbs": verbs})
        self.assertEqual(pr.check_feel_human_playtest().state, pr.MISSING)

    def test_an_extra_verb_cannot_substitute_for_a_missing_one(self):
        # V9 is not in the locked allowlist, so marking it "pass" must not buy
        # coverage for V2. The eight are the eight.
        verbs = {v: {"result": "pass"} for v in pr.MVP_VERBS if v != "V2"}
        verbs["V9"] = {"result": "pass"}
        self._use({"commit": "abc1234", "played_at": "2026-10-04", "verbs": verbs})
        c = pr.check_feel_verb_script()
        self.assertEqual(c.state, pr.MISSING)
        self.assertIn("V2", c.note)

    def test_an_extra_verb_is_named_rather_than_dropped(self):
        # All eight ran, so PASS is honest -- but an ID outside the allowlist should
        # be surfaced, because it usually means a mechanic is being tested that
        # Docs/canon/VERBS.md does not contain.
        verbs = {v: {"result": "pass"} for v in pr.MVP_VERBS}
        verbs["V9"] = {"result": "pass"}
        self._use({"commit": "abc1234", "played_at": "2026-10-04", "verbs": verbs})
        c = pr.check_feel_verb_script()
        self.assertEqual(c.state, pr.PASS)
        self.assertIn("V9", c.note)
        # and the count reports the eight, not the nine
        self.assertIn("8", c.measured)
        self.assertNotIn("9", c.measured)


class PaDPlacementsAreReadFromTheSpecs(unittest.TestCase):
    """place_vs_mvp_pa_d.py must place from Lib/01_Homestead, not from itself.

    It used to hardcode the three cliff faces, the garden centre and the five fence
    segments directly under comments citing SM_Cliff.json and GARDEN_BLOCKING.md.
    A comment citing a file is a claim about that file, not a link to it, so a spec
    edit would silently not apply here.

    Three things have to hold at once, and each has already been broken once:

    1. PARITY. The rewrite must reproduce every coordinate it replaced. This is a
       placement script; "the refactor was tidy" is not evidence that nothing moved.
    2. THE REGEXES ACTUALLY MATCH. The first version of the number pattern was
       written with doubled backslashes (`\\d` in the source), which compiles to a
       pattern matching a literal backslash followed by 'd'. It raised loudly, which
       is the only reason it was caught - but the check that caught it was a manual
       run against the real spec file, which is exactly the kind of check that does
       not survive. Hence this.
    3. THE SPECS ARE TYPographic, NOT ASCII. GARDEN_BLOCKING.md writes its minus as
       U+2212 MINUS SIGN and its size separator as U+00D7. SM_Cliff.json is plain
       ASCII. A pattern written for one spelling silently finds nothing in the other,
       which is how a "wired to spec" change can read nothing at all.

    The script needs `unreal` and calls sys.exit without it, so it is imported with a
    stub. That is why there was no test for it before.
    """

    SCRIPT = ROOT / "Content" / "Python" / "place_vs_mvp_pa_d.py"
    CLIFF_SPEC = ROOT / "Lib" / "01_Homestead" / "SM_Cliff.json"
    GARDEN_SPEC = ROOT / "Lib" / "01_Homestead" / "GARDEN_BLOCKING.md"

    @classmethod
    def setUpClass(cls):
        import types

        stub = types.ModuleType("unreal")
        stub.log = lambda *a, **k: None
        saved = sys.modules.get("unreal")
        sys.modules["unreal"] = stub
        try:
            spec = importlib.util.spec_from_file_location("place_vs_mvp_pa_d", cls.SCRIPT)
            cls.pad = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(cls.pad)
        finally:
            if saved is None:
                sys.modules.pop("unreal", None)
            else:
                sys.modules["unreal"] = saved

    # -- 1. parity -------------------------------------------------------
    def test_cliff_faces_are_unchanged(self):
        self.assertEqual(
            self.pad.CLIFF_SPECS,
            (("SM_Cliff_LookoutFace", (7.5, -5.5, -4.0)),
             ("SM_Cliff_CabinFace", (-7.0, -4.5, -3.0)),
             ("SM_Cliff_Rear", (0.0, 5.0, -2.5))),
        )

    def test_garden_centre_and_planters_are_unchanged(self):
        self.assertEqual(self.pad.GARDEN_CENTER_BL, (-3.5, 0.5, 0.0))
        self.assertEqual(
            self.pad.PLANTER_SPECS,
            (("SM_Planter_A", (-4.1, 0.5, 0.0)),
             ("SM_Planter_B", (-3.5, 0.5, 0.0)),
             ("SM_Planter_C", (-2.9, 0.5, 0.0))),
        )

    def test_fence_segments_are_unchanged(self):
        self.assertEqual(
            self.pad.FENCE_SEGMENTS_BL,
            ((-5.5, 0.5, 0.0), (-3.5, 1.75, 0.0), (-1.5, 0.5, 0.0),
             (-3.5, -0.75, 0.0), (-4.5, 1.25, 0.0)),
        )

    def test_path_endpoints_are_unchanged(self):
        self.assertEqual(self.pad.PATH_START_BL, (-6.0, 1.0, 0.0))
        self.assertEqual(self.pad.PATH_END_BL, (7.0, -3.5, 0.0))

    # -- 2. the patterns match the real specs ---------------------------
    def test_the_patterns_match_the_real_spec_files(self):
        """Reads the shipped specs with the shipped patterns.

        This is the assertion the doubled-backslash bug would have failed. It is
        deliberately blunt: if a regex stops matching a spec that has not changed,
        the wiring is broken whether or not anything still parses.
        """
        cliff = json.loads(self.CLIFF_SPEC.read_text(encoding="utf-8-sig"))
        wanted = list(cliff["graybox_map"])
        self.assertEqual([name for name, _ in self.pad.CLIFF_SPECS], wanted,
                         "CLIFF_SPECS no longer follows graybox_map")

        garden_text = self.GARDEN_SPEC.read_text(encoding="utf-8-sig")
        row = next(ln for ln in garden_text.splitlines() if "Zone volume" in ln)
        self.assertTrue(self.pad._XYZ_RE.search(row),
                        "centre pattern does not match the shipped GARDEN_BLOCKING.md")
        self.assertTrue(self.pad._SIZE_RE.search(row),
                        "size pattern does not match the shipped GARDEN_BLOCKING.md")
        self.assertEqual(self.pad._read_garden_envelope(str(self.GARDEN_SPEC)),
                         ((-3.5, 0.5, 0.0), (4.0, 2.5, 0.6)))

    def test_the_shipped_garden_spec_is_typographic(self):
        """Guards assumption 3, so a future ASCII rewrite cannot pass unnoticed.

        If this ever starts failing because someone normalised the file to ASCII,
        that is fine - but the ASCII path must be proven to work too (below), not
        assumed.
        """
        text = self.GARDEN_SPEC.read_text(encoding="utf-8-sig")
        self.assertIn("\u2212", text, "spec no longer uses U+2212; re-check _to_float")
        self.assertIn("\u00d7", text, "spec no longer uses U+00D7; re-check _SIZE_RE")

    def test_both_spellings_of_every_symbol_parse(self):
        for minus in ("-", "\u2212"):
            for times in ("x", "\u00d7"):
                with self.subTest(minus=ascii(minus), times=ascii(times)):
                    text = ("| Zone volume | **4.0 %s 2.5 %s 0.6 m** at (%s3.5, 0.5, 0.0) |"
                            % (times, times, minus))
                    with tempfile.TemporaryDirectory() as td:
                        p = Path(td) / "g.md"
                        p.write_text(text, encoding="utf-8")
                        self.assertEqual(
                            self.pad._read_garden_envelope(str(p)),
                            ((-3.5, 0.5, 0.0), (4.0, 2.5, 0.6)))

    # -- 3. it is actually wired, not coincidentally equal ---------------
    def test_editing_the_spec_moves_the_fence(self):
        """The point of reading the spec. Four fence points are derived, so they must
        follow the envelope; before this they were five literals that merely agreed."""
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "g.md"
            p.write_text("| Zone volume | **8.0 \u00d7 2.5 \u00d7 0.6 m** at (\u22126.5, 0.5, 0.0) |",
                         encoding="utf-8")
            centre, size = self.pad._read_garden_envelope(str(p))
        self.assertEqual((centre, size), ((-6.5, 0.5, 0.0), (8.0, 2.5, 0.6)))
        half_x, half_y = size[0] / 2.0, size[1] / 2.0
        self.assertEqual(centre[0] - half_x, -10.5)
        self.assertEqual(centre[1] + half_y, 1.75)

    # -- 4. a broken source raises rather than silently placing nothing --
    def test_a_spec_missing_the_row_raises(self):
        for label, text in (
            ("no row", "# Garden\n\nNothing here.\n"),
            ("no size", "| Zone volume | at (-3.5, 0.5, 0.0) |\n"),
            ("no centre", "| Zone volume | **4.0 \u00d7 2.5 \u00d7 0.6 m** |\n"),
        ):
            with self.subTest(case=label), tempfile.TemporaryDirectory() as td:
                p = Path(td) / "g.md"
                p.write_text(text, encoding="utf-8")
                with self.assertRaises(ValueError):
                    self.pad._read_garden_envelope(str(p))

    def test_a_greybox_map_name_without_an_origin_is_named_not_invented(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "c.json"
            p.write_text(json.dumps({"graybox_map": ["SM_Cliff_Rear"],
                                     "modules": [{"name": "SM_Cliff_Rear"}]}),
                         encoding="utf-8")
            specs, missing = self.pad._read_cliff_specs(str(p))
        self.assertEqual(specs, ())
        self.assertEqual(missing, ["SM_Cliff_Rear"])

    def test_a_spec_with_no_greybox_map_raises(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "c.json"
            p.write_text(json.dumps({"graybox_map": [], "modules": []}), encoding="utf-8")
            with self.assertRaises(ValueError):
                self.pad._read_cliff_specs(str(p))


class TheExportChainCannotGoStale(unittest.TestCase):
    """The FBX Unreal consumes must be current, and somebody must have measured it.

    On 2026-10-04 the island plate was applied and verified in the .blend - it
    measured 180.0 x 100.0 x 0.45 and `env.island_sized` went PASS. The FBX that
    Unreal actually consumes still measured 19.3 x 10.7, exported on 2026-09-16,
    and the .uasset had been imported from it on 2026-09-28.

    Every gate row was reading the Blender source of truth. Not one read the
    artefact the game is built from, so the gate was green and a player would have
    stood on a 19 m island. This is the cleanest example in the repo of a green log
    being worth nothing, and it is why there are now two rows for the chain rather
    than none.

    Between them the two rows cover:

      env.export_fresh        the .blend -> FBX hop, via the manifest's file sizes.
      env.ue_island_measured  the FBX -> .uasset -> level hop, via an in-editor
                              measurement of the real thing.

    Neither alone is sufficient. A current FBX that was never re-imported passes the
    first and fails the second, which is the state this repo was actually in.

    MOST OF THIS CLASS IS MUTATION-TESTED GUARD. An independent review of the
    first version of these two checks found six ways to turn them green without
    measuring anything, so each of those holes has a test that fails when it is
    reopened. The bug this class exists to prevent is a gate that says PASS, and a
    test that only exercises the happy path does not prevent it.
    """

    def setUp(self):
        self.saved_manifest = pr.EXPORT_MANIFEST
        self.saved_record = pr.UE_ISLAND_MEASUREMENT
        self.addCleanup(setattr, pr, "EXPORT_MANIFEST", self.saved_manifest)
        self.addCleanup(setattr, pr, "UE_ISLAND_MEASUREMENT", self.saved_record)

    # -- helpers ---------------------------------------------------------
    def _use_manifest(self, rows):
        """rows: list of (category, filename, recorded_size). Returns the root.

        Each FBX is created at exactly `recorded_size` bytes, so a row can be made
        stale in either direction. Real exports here are ~15 kB and up and the check
        enforces a floor, so fixtures use realistic sizes unless a test is
        specifically about small ones.
        """
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        root = Path(td.name)
        lines = ["# manifest", "", "| Category | File | Bytes | Target |",
                 "|---|---|---|---|"]
        for category, name, recorded in rows:
            lines.append("| %s | `%s` | %d | %s |"
                         % (category, name, recorded, name))
            target = root / category
            target.mkdir(parents=True, exist_ok=True)
            (target / name).write_bytes(b"\0" * recorded)
        path = root / "MVP_EXPORT_MANIFEST.md"
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        pr.EXPORT_MANIFEST = path
        return root

    def _now_iso(self):
        return datetime.datetime.now(datetime.timezone.utc).isoformat(
            timespec="seconds")

    def _record(self, **over):
        """A record valid in every respect except whatever the test changes.

        Without this, every provenance test would also be testing the provenance of
        whatever ad-hoc dict that test happened to write, and a test named for a
        NaN would go red for an unrelated missing `level`.
        """
        body = {
            "measured_at": self._now_iso(),
            "level": "MainMenu",
            "asset": "SM_IslandTop",
            "actors_found": 1,
            "local_bbox_cm": [18000.0, 10000.0, 45.0],
            "non_unit_scale_actors": [],
        }
        body.update(over)
        return body

    def _use_record(self, body):
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        p = Path(td.name) / "UE_ISLAND_MEASUREMENT.json"
        p.write_text(json.dumps(body), encoding="utf-8")
        pr.UE_ISLAND_MEASUREMENT = p
        return p

    # -- env.export_fresh ------------------------------------------------
    def test_shipped_manifest_agrees_with_every_fbx_on_disk(self):
        """The real assertion about the real repo: rows parse, none stale, none
        unlisted.

        Two-sided on purpose. Comparing only against the manifest cannot notice an
        export that was added to disk and never recorded, which is the shape of the
        original failure - a file the inventory does not know about.
        """
        rows, rejected = pr._manifest_rows()
        self.assertEqual(rejected, [], "the shipped manifest has unreadable rows")
        self.assertGreaterEqual(len(rows), 20,
                                "manifest stopped parsing most of its rows")
        self.assertEqual(pr.check_env_export_fresh().state, pr.PASS)

    def test_a_size_mismatch_is_fail(self):
        self._use_manifest([("Homestead", "SM_IslandTop.fbx", 15692)])
        (pr.EXPORT_MANIFEST.parent / "Homestead" / "SM_IslandTop.fbx").write_bytes(
            b"\0" * 15676)
        c = pr.check_env_export_fresh()
        self.assertEqual(c.state, pr.FAIL)
        self.assertIn("SM_IslandTop.fbx", c.note)
        self.assertIn("15676", c.note)

    def test_an_export_that_grew_is_also_stale(self):
        """The comparison must be `!=`, not `<`.

        An export that gained geometry is the common case, and `if actual <
        recorded` - which reads as "an export cannot be smaller than the manifest
        says" - accepts every one of them silently. The first version of this test
        only made the file smaller, so that edit left the suite green.
        """
        self._use_manifest([("Homestead", "SM_IslandTop.fbx", 15692)])
        (pr.EXPORT_MANIFEST.parent / "Homestead" / "SM_IslandTop.fbx").write_bytes(
            b"\0" * 20000)
        c = pr.check_env_export_fresh()
        self.assertEqual(c.state, pr.FAIL)
        self.assertIn("20000", c.note)

    def test_an_export_on_disk_that_the_manifest_never_heard_of_is_fail(self):
        """The direction the first version could not see at all.

        It walked the manifest, so an FBX nobody recorded was not in the inventory.
        It could never be found stale, because as far as the gate was concerned it
        did not exist.
        """
        self._use_manifest([("Homestead", "SM_IslandTop.fbx", 15692)])
        stray = pr.EXPORT_MANIFEST.parent / "Homestead" / "SM_Smuggled.fbx"
        stray.write_bytes(b"\0" * 15692)
        c = pr.check_env_export_fresh()
        self.assertEqual(c.state, pr.FAIL)
        self.assertIn("SM_Smuggled.fbx", c.note)
        self.assertIn("not in the manifest", c.note)

    def test_a_malformed_export_row_is_fail_not_skipped(self):
        """A row the checker cannot read is an export it cannot watch.

        The first version skipped anything whose byte count would not parse, so
        three exports could disappear from the inventory while the row still said
        PASS - the parser's own fail-open, tolerated by a test that only ever
        counted rows.
        """
        root = self._use_manifest([("Homestead", "SM_IslandTop.fbx", 15692)])
        manifest = root / "MVP_EXPORT_MANIFEST.md"
        manifest.write_text(
            manifest.read_text(encoding="utf-8")
            + "| Homestead | `SM_Broken.fbx` | not-a-number | x |\n",
            encoding="utf-8")
        c = pr.check_env_export_fresh()
        self.assertEqual(c.state, pr.FAIL)
        self.assertIn("cannot read", c.note)

    def test_a_manifest_row_whose_path_escapes_the_export_tree_is_reported(self):
        """`../../..` in a category cell would otherwise stat a file outside
        AssetCreation/Exports and call it covered, while the real FBX it was meant
        to describe drops out of the inventory undetected."""
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        root = Path(td.name)
        (root / "Homestead").mkdir(parents=True, exist_ok=True)
        (root / "Homestead" / "SM_IslandTop.fbx").write_bytes(b"\0" * 15692)
        (root / "MVP_EXPORT_MANIFEST.md").write_text(
            "| C | F | B |\n|---|---|---|\n"
            "| Homestead | `SM_IslandTop.fbx` | 15692 | x |\n"
            "| ../../../../etc | `passwd.fbx` | 10 | x |\n",
            encoding="utf-8")
        pr.EXPORT_MANIFEST = root / "MVP_EXPORT_MANIFEST.md"
        rows, rejected = pr._manifest_rows()
        self.assertEqual([r[1] for r in rows], ["SM_IslandTop.fbx"])
        self.assertTrue(any("escapes" in r for r in rejected),
                        "a path outside the export tree must be reported")

    def test_a_zero_byte_export_is_fail_not_agreement(self):
        """A 0-byte file whose manifest row also said 0 was a clean PASS.

        Both sides agreed and both were empty. The smallest real export in the
        manifest is 15116 bytes, so a floor well under that is safe.
        """
        self._use_manifest([("Homestead", "SM_IslandTop.fbx", 0)])
        (pr.EXPORT_MANIFEST.parent / "Homestead" / "SM_IslandTop.fbx").write_bytes(b"")
        c = pr.check_env_export_fresh()
        self.assertEqual(c.state, pr.FAIL)
        self.assertIn("too small", c.note)

    def test_a_collision_proxy_row_is_not_an_export_row(self):
        """The manifest holds more than one table.

        Collision proxies read `UCX_SM_Cabin` | `5.5 x 4.5 x 5.5` |
        `Homestead/SM_Cabin.fbx`, and an export row's own Contents column mentions
        UCX names too. Reporting those as malformed export rows would be a false RED
        on a correct manifest, which is how a real gate gets ignored.
        """
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        root = Path(td.name)
        (root / "Homestead").mkdir(parents=True, exist_ok=True)
        (root / "Homestead" / "SM_Cabin.fbx").write_bytes(b"\0" * 81196)
        (root / "MVP_EXPORT_MANIFEST.md").write_text(
            "| Category | File | Bytes | Contents |\n|---|---|---|---|\n"
            "| Homestead | `SM_Cabin.fbx` | 81196 | SM_Cabin_* + UCX_SM_Cabin"
            " - (1680 tris; UCX 5.5x4.5x5.5) |\n"
            "| `UCX_SM_Cabin` | 5.5 x 4.5 x 5.5 | `Homestead/SM_Cabin.fbx` |\n",
            encoding="utf-8")
        pr.EXPORT_MANIFEST = root / "MVP_EXPORT_MANIFEST.md"
        rows, rejected = pr._manifest_rows()
        self.assertEqual([r[1] for r in rows], ["SM_Cabin.fbx"])
        self.assertEqual(rejected, [])
        self.assertEqual(pr.check_env_export_fresh().state, pr.PASS)

    def test_a_listed_but_absent_file_is_missing_not_fail(self):
        """FAIL here would push someone to hand-edit a size instead of exporting."""
        self._use_manifest([("Homestead", "SM_IslandTop.fbx", 15692)])
        (pr.EXPORT_MANIFEST.parent / "Homestead" / "SM_IslandTop.fbx").unlink()
        self.assertEqual(pr.check_env_export_fresh().state, pr.MISSING)

    def test_an_unparseable_manifest_is_missing(self):
        self._use_manifest([])
        pr.EXPORT_MANIFEST.write_text("# nothing here\n", encoding="utf-8")
        self.assertEqual(pr.check_env_export_fresh().state, pr.MISSING)

    def test_fbx_predating_the_blend_is_a_hint_not_a_failure(self):
        """Regression test for a false positive this check shipped with.

        The first version failed the row when any FBX was older than the .blend.
        After the plate was applied and the blend re-saved, that reported 23 of 23
        stale - because saving the blend touches one file and every export in it
        legitimately predates that save, whether or not their geometry moved.

        A whole-file timestamp cannot describe per-object change. The number is
        still printed so a human can see it; it must not decide the verdict.

        This constructs the condition on purpose. The first version of this test
        asserted against the live repo, where the blend happened to be newer than
        every export - so it passed whether or not the `behind` count was computed
        at all. Deleting the entire calculation left it green.
        """
        root = self._use_manifest([("Homestead", "SM_IslandTop.fbx", 15692)])
        blend = root / "lib.blend"
        blend.write_bytes(b"x")
        saved_blend = pr.LIB_BLEND
        pr.LIB_BLEND = blend
        self.addCleanup(setattr, pr, "LIB_BLEND", saved_blend)
        future = time.time() + 86400
        os.utime(blend, (future, future))
        c = pr.check_env_export_fresh()
        self.assertEqual(c.state, pr.PASS,
                         "an FBX older than the .blend is a hint, not a failure")
        self.assertIn("hint:", c.note)
        self.assertIn("1 of 1", c.note, "the hint must actually count something")
        self.assertIn("not counted", c.note)

    # -- env.ue_island_measured -----------------------------------------
    def test_shipped_record_is_not_yet_measured(self):
        """Nobody has measured the island in the editor yet, so the row reads
        MISSING - not PASS (nobody checked) and not FAIL (nobody claims it is
        wrong).

        Asserted against the live state rather than hard-coded to MISSING, so that
        doing the work does not turn the suite red and tempt someone into deleting
        the assertion. The first version hard-coded MISSING, which meant completing
        the task would have broken the very test guarding it.
        """
        shipped = ROOT / "Docs" / "qa" / "UE_ISLAND_MEASUREMENT.json"
        self.assertTrue(shipped.is_file(), "UE_ISLAND_MEASUREMENT.json missing")
        body = json.loads(shipped.read_text(encoding="utf-8"))
        self._use_record(body)
        c = pr.check_env_ue_island_measured()
        if body.get("local_bbox_cm") is None:
            self.assertEqual(c.state, pr.MISSING)
            self.assertIn("measure_ue_island.py", c.note)
        else:
            # Somebody measured it. The row now owes them a real verdict, and the
            # measurement has to be a real one.
            self.assertIn(c.state, (pr.PASS, pr.FAIL))
            self.assertIsNotNone(body.get("level"))
            self.assertIsNotNone(body.get("measured_at"))

    def test_the_real_pre_plate_size_would_fail(self):
        """The numbers this repo was actually in, fed back through the check.

        1930 x 1070 cm is what the 2026-09-28 .uasset held. If this ever reads PASS
        the comparison is broken, and that is the one thing this row exists to stop.
        """
        self._use_record(self._record(local_bbox_cm=[1930.0, 1070.0, 45.0]))
        c = pr.check_env_ue_island_measured()
        self.assertEqual(c.state, pr.FAIL)
        self.assertIn("180.0", c.target)
        self.assertIn("19.3", c.measured)
        self.assertIn("re-import", c.note)

    def test_a_matching_measurement_passes(self):
        self._use_record(self._record())
        self.assertEqual(pr.check_env_ue_island_measured().state, pr.PASS)

    def test_small_drift_within_tolerance_passes(self):
        """The point is to catch an un-reimported asset, not to adjudicate
        centimetre-level disagreement between two engines."""
        self._use_record(self._record(local_bbox_cm=[18040.0, 9980.0, 45.0]))
        self.assertEqual(pr.check_env_ue_island_measured().state, pr.PASS)

    def test_the_y_axis_is_checked_independently(self):
        """X correct, Y wrong. The first version had no such test.

        Removing `off_y` from the comparison left every test green, which is what a
        check with one untested axis looks like.
        """
        self._use_record(self._record(local_bbox_cm=[18000.0, 4000.0, 45.0]))
        c = pr.check_env_ue_island_measured()
        self.assertEqual(c.state, pr.FAIL)
        self.assertIn("in Y", c.note)

    def test_the_z_axis_is_checked_too(self):
        """A flattened island is the wrong island.

        Z was read from the source report and never compared, so a
        180 x 100 x 0.05 plate passed a row written for a 180 x 100 x 0.45 one.
        """
        self._use_record(self._record(local_bbox_cm=[18000.0, 10000.0, 5.0]))
        c = pr.check_env_ue_island_measured()
        self.assertEqual(c.state, pr.FAIL)
        self.assertIn("in Z", c.note)

    def test_nan_in_any_slot_is_missing_not_pass(self):
        """The nastiest one, and it was live.

        `max(off_x, off_y)` returns its first argument whenever the second is not
        greater, and `NaN > x` is always False - so a NaN in the Y slot was
        discarded by max() and the row reported PASS with the words "off by nan" in
        its own note. JSON accepts the bare literal, so a committed record can carry
        one.
        """
        for raw in ([float("nan"), 10000.0, 45.0],
                    [18000.0, float("nan"), 45.0],
                    [18000.0, 10000.0, float("inf")],
                    [18000.0, 10000.0, float("-inf")]):
            with self.subTest(raw=raw):
                self._use_record(self._record(local_bbox_cm=raw))
                c = pr.check_env_ue_island_measured()
                self.assertNotEqual(c.state, pr.PASS)
                self.assertIn("non-finite", c.measured + c.note)

    def test_a_unit_error_cannot_pass(self):
        """cm vs m is a 100x trap. 18000 cm is 180 m and agrees; 18000 m would be
        1.8 million cm."""
        self._use_record(
            self._record(local_bbox_cm=[1800000.0, 1000000.0, 4500.0]))
        self.assertEqual(pr.check_env_ue_island_measured().state, pr.FAIL)

    def test_non_numeric_and_boolean_values_are_missing(self):
        """Numbers written as strings, and Python bools, which are ints.

        A string that happens to parse is not a measurement, and True would
        otherwise become 1.0 cm.
        """
        for raw in (["18000", "10000", "45"], [True, False, True],
                    [18000.0, None, 45.0], [18000.0, {}, 45.0]):
            with self.subTest(raw=raw):
                self._use_record(self._record(local_bbox_cm=raw))
                c = pr.check_env_ue_island_measured()
                self.assertEqual(c.state, pr.MISSING)
                self.assertIn("unparseable", c.measured + c.note)

    def test_a_two_element_bbox_is_missing(self):
        self._use_record(self._record(local_bbox_cm=[18000.0, 10000.0]))
        self.assertEqual(pr.check_env_ue_island_measured().state, pr.MISSING)

    def test_a_world_bbox_record_is_rejected_not_compared(self):
        """bbox_cm is the actor's WORLD box; Blender reports object-space.

        Comparing them means failing any rotated island - wrong by construction,
        not by tolerance. An older record carrying only bbox_cm must be rejected
        with the reason, not quietly accepted.
        """
        self._use_record({
            "measured_at": self._now_iso(), "level": "MainMenu",
            "asset": "SM_IslandTop", "actors_found": 1,
            "bbox_cm": [18000.0, 10000.0, 45.0],
        })
        c = pr.check_env_ue_island_measured()
        self.assertNotEqual(c.state, pr.PASS)
        self.assertIn("local_bbox_cm", c.note)

    def test_an_actor_at_non_unit_scale_fails(self):
        """The right mesh at the wrong scale is still the wrong island.

        A 0.1-scaled 180 m plate is a 19 m plate, which is the exact number that
        started this.
        """
        self._use_record(self._record(
            local_bbox_cm=[1800.0, 1000.0, 45.0],
            non_unit_scale_actors=["SM_IslandTop"]))
        c = pr.check_env_ue_island_measured()
        self.assertEqual(c.state, pr.FAIL)
        self.assertIn("scaled", c.note)

    def test_a_record_naming_another_asset_fails(self):
        self._use_record(self._record(asset="SM_ResIsland"))
        c = pr.check_env_ue_island_measured()
        self.assertEqual(c.state, pr.FAIL)
        self.assertIn("SM_ResIsland", c.note)

    def test_a_record_from_an_unknown_level_fails(self):
        self._use_record(self._record(level="Sandbox_Preview"))
        c = pr.check_env_ue_island_measured()
        self.assertEqual(c.state, pr.FAIL)
        self.assertIn("Sandbox_Preview", c.note)

    def test_a_record_that_predates_the_export_fails(self):
        """A record written before the FBX was last exported describes the previous
        geometry, and nothing else about it looks wrong.

        This is the one legitimate use of a timestamp here: two whole files, each a
        complete build of the same thing. The retracted per-object mtime rule could
        not do this.
        """
        self._use_manifest([("Homestead", "SM_IslandTop.fbx", 15692)])
        fbx = pr.EXPORT_MANIFEST.parent / "Homestead" / "SM_IslandTop.fbx"
        future = time.time() + 86400
        os.utime(fbx, (future, future))
        self._use_record(self._record(measured_at="2026-01-01T00:00:00+00:00"))
        c = pr.check_env_ue_island_measured()
        self.assertEqual(c.state, pr.FAIL)
        self.assertIn("predates", c.note)

    def test_missing_provenance_is_missing(self):
        """A bare number is not evidence: no asset, no level, no time."""
        for field in ("asset", "level", "measured_at"):
            with self.subTest(field=field):
                body = self._record()
                body[field] = None
                self._use_record(body)
                c = pr.check_env_ue_island_measured()
                self.assertEqual(c.state, pr.MISSING)
                self.assertIn(field, c.measured + c.note)

    def test_a_null_bbox_is_missing(self):
        for body in ({}, {"local_bbox_cm": None}, {"local_bbox_cm": []},
                     {"local_bbox_cm": "wide"}):
            with self.subTest(body=body):
                self._use_record(body)
                self.assertEqual(pr.check_env_ue_island_measured().state,
                                 pr.MISSING)

    def test_a_missing_record_is_missing(self):
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        pr.UE_ISLAND_MEASUREMENT = Path(td.name) / "absent.json"
        c = pr.check_env_ue_island_measured()
        self.assertEqual(c.state, pr.MISSING)
        self.assertIn("19.3", c.note, "the note should say what nearly happened")

    def test_no_blender_measurement_is_missing_not_pass(self):
        """If the greybox report cannot be read there is nothing to compare, and
        that must not read as agreement."""
        self._use_record(self._record())
        saved = pr.GRAYBOX_REPORT
        pr.GRAYBOX_REPORT = Path(tempfile.gettempdir()) / "definitely-absent.json"
        self.addCleanup(setattr, pr, "GRAYBOX_REPORT", saved)
        self.assertEqual(pr.check_env_ue_island_measured().state, pr.MISSING)

class BlockedRowsMustNameAnAction(unittest.TestCase):
    """A red row that does not say what to do is a mood, not a work list.

    On 2026-10-04, 6 of the 8 substantive blocked rows stated a finding and no
    next step. Reading them told you what was wrong and nothing about what to do
    about it - which is the failure mode of a gate that only ever complains.

    The Lead's stated expectation is that the agent is never idle: always
    working, always asking a question that extracts information, or always
    pointing at the next concrete step. This class is that expectation made
    structural, so a later edit that drops an action is a failing test rather
    than a quietly less useful gate.

    Deliberately NOT required of PASS rows (there is nothing to do) and not of
    `dep.` rollups (a gate-level summary naming its own actions would duplicate
    its children).
    """

    #: Rows where an empty action is legitimate: agent-owned, still in progress.
    ALLOWED_EMPTY = frozenset()

    def _substantive_blocked(self):
        gates = pr.build()
        return [c for g in gates.values() for c in g.checks
                if c.state in (pr.FAIL, pr.MISSING, pr.STALE)
                and not c.id.startswith("dep.")
                and c.id not in self.ALLOWED_EMPTY]

    def test_every_blocked_row_carries_a_next_action(self):
        empty = [c.id for c in self._substantive_blocked()
                 if not (c.next_action or "").strip()]
        self.assertEqual(
            empty, [],
            "these rows are blocked and say nothing about what to do: "
            + ", ".join(empty))

    def test_the_shipped_repo_has_none_empty(self):
        """Assert against the real repo, so drift shows up immediately."""
        blocked = self._substantive_blocked()
        self.assertGreaterEqual(len(blocked), 5,
                                "the gate went quiet; that is as suspicious as a red row")
        for c in blocked:
            with self.subTest(check=c.id):
                self.assertTrue(c.next_action.strip())

    def test_an_action_must_be_actionable_not_a_restatement(self):
        """"Row is red" is not an action. Require a verb and some specificity.

        The bar is deliberately low - a length floor plus a leading capital -
        because the failure being guarded against is an empty string or a
        paraphrase, not weak prose.
        """
        for c in self._substantive_blocked():
            with self.subTest(check=c.id):
                action = c.next_action.strip()
                self.assertGreater(len(action), 40,
                                   f"{c.id}: action too short to be useful")
                self.assertTrue(
                    action[0].isupper() or action[0].isdigit(),
                    f"{c.id}: action should read as an instruction")

    def test_pass_rows_need_no_action(self):
        """Guards the other direction: a PASS carrying an action is noise."""
        gates = pr.build()
        noisy = [c.id for g in gates.values() for c in g.checks
                 if c.state == pr.PASS and c.next_action.strip()]
        self.assertEqual(noisy, [], "PASS rows should not be telling anyone to do work")

    def test_markdown_renders_a_what_to_do_section(self):
        """The action has to reach the human, not just the JSON."""
        gates = pr.build()
        md = pr.render_markdown(gates, "2026-10-04T00:00:00+00:00")
        self.assertIn("### What to do", md)
        self.assertIn("Next action", md)


class AssetBoardCannotBeFakedGreen(unittest.TestCase):
    """The board exists so a batch can be reviewed at S2, not one asset at S3.

    Its first implementation read `if a.get("stage")` -- truthy -- so a seeded
    skeleton of nulls counted as ten undeclared assets and reported FAIL. That is
    the same fabrication trap as the playtest record, and it pushes the writer
    toward typing anything rather than looking at anything.

    Also: a stage that is not on the ladder must not read as declared. "blockout"
    or "S7" is not a production state Docs/37 defines, and treating it as one would
    let the board assert a stage the process has never heard of.
    """

    SHIPPED = ROOT / "Docs" / "qa" / "POLISH_ASSET_BOARD.json"

    def setUp(self):
        if not self.SHIPPED.is_file():
            self.skipTest("POLISH_ASSET_BOARD.json not present")
        self.saved = pr.ASSET_BOARD_FILE
        self.addCleanup(setattr, pr, "ASSET_BOARD_FILE", self.saved)

    def _use(self, body):
        td = tempfile.TemporaryDirectory()
        p = Path(td.name) / "POLISH_ASSET_BOARD.json"
        p.write_text(json.dumps(body), encoding="utf-8")
        pr.ASSET_BOARD_FILE = p
        self.addCleanup(td.cleanup)
        return p

    def _shipped(self):
        return json.loads(self.SHIPPED.read_text(encoding="utf-8"))

    def test_shipped_board_reports_missing_not_fail(self):
        self._use(self._shipped())
        c = pr.check_asset_board()
        self.assertEqual(c.state, pr.MISSING)
        self.assertNotEqual(c.state, pr.FAIL)

    def test_shipped_board_carries_every_master_and_nothing_else(self):
        # The masters are read from Content/HomeWorld/Materials/Masters. A board
        # that quietly drops one would let the check go green over nine.
        on_disk = {p.stem for p in (ROOT / "Content" / "HomeWorld" / "Materials"
                                    / "Masters").glob("*.uasset")}
        listed = [a["name"] for a in self._shipped()["assets"]]
        self.assertEqual(len(on_disk), pr.EXPECTED_MASTER_COUNT)
        self.assertEqual(sorted(listed), sorted(on_disk))

    def test_shipped_board_has_no_stage_and_no_priority(self):
        for asset in self._shipped()["assets"]:
            with self.subTest(asset=asset["name"]):
                self.assertIsNone(asset["stage"], "a stage here is a production claim")
                self.assertIsNone(asset["priority"])

    def test_a_fully_declared_board_reaches_pass(self):
        # Otherwise this is decoration that can only ever be red.
        self._use({"assets": [{"name": "M_CliffRock", "stage": "S2",
                               "priority": 1}]})
        self.assertEqual(pr.check_asset_board().state, pr.PASS)

    def test_stage_accepts_the_code_or_the_full_label(self):
        # A hand edit failing on punctuation would be reported as an undeclared
        # asset, which reads as "nobody triaged this" and is simply wrong.
        for value in ("S2", "s2", "S2 ART-BLOCKOUT", " S2 "):
            with self.subTest(stage=value):
                self.assertEqual(pr._stage_code(value), "S2")

    def test_a_stage_off_the_ladder_is_rejected(self):
        for value in ("blockout", "S7", "done", "2"):
            with self.subTest(stage=value):
                self.assertIsNone(pr._stage_code(value))
        self._use({"assets": [{"name": "M_CliffRock", "stage": "blockout",
                               "priority": 1}]})
        c = pr.check_asset_board()
        self.assertEqual(c.state, pr.FAIL)
        self.assertIn("M_CliffRock", c.note)

    def test_a_stage_without_a_priority_is_still_undeclared(self):
        # The check's own question is "stage and priority". Priority is what makes
        # batching possible, so a stage alone must not complete a row.
        self._use({"assets": [{"name": "M_CliffRock", "stage": "S2",
                               "priority": None}]})
        c = pr.check_asset_board()
        self.assertEqual(c.state, pr.MISSING)
        self.assertIn("M_CliffRock", c.note)

    def test_seven_of_ten_is_not_ten(self):
        assets = [{"name": f"M_{i}", "stage": "S2", "priority": 1}
                  for i in range(7)]
        assets.append({"name": "M_CliffRock", "stage": None, "priority": None})
        self._use({"assets": assets})
        self.assertEqual(pr.check_asset_board().state, pr.MISSING)

    def test_a_board_listing_no_assets_is_missing(self):
        # Present-but-empty must not read as "everything is staged".
        self._use({"assets": []})
        self.assertEqual(pr.check_asset_board().state, pr.MISSING)


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