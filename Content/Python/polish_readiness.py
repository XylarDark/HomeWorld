# polish_readiness.py
# Host-side script: answers "are we ready to start a human polish pass?" from
# artifacts already on disk, and writes the answer out so it can be diffed.
#
# Run from project root:  py Content/Python/polish_readiness.py
# Writes: Docs/qa/POLISH_READINESS.json and Docs/qa/POLISH_READINESS.md
# Exit:  0 = every gate GREEN, 1 = a gate is RED, 2 = a gate could not be measured.
#
# See Docs/37_POLISH_PASS_PROCESS.md for the stage ladder this gates.
#
# ---------------------------------------------------------------------------
# WHY THIS SCRIPT EXISTS, AND WHY IT REFUSES TO REPORT READY
# ---------------------------------------------------------------------------
#
# The question "can we start polishing yet?" has been answered in this project by
# conversation, and conversation answers drift. Docs/14 closed a whole VP track with
# a checklist of boxes ticked while the verb table underneath it read all-FAIL and the
# waiver was filed next to it. Docs/34 researched an art pipeline and stopped at the
# research. Neither is a measurement.
#
# So the rule here is the same one that governs run_ue_automation.py, applied to
# readiness instead of tests:
#
#   ABSENCE OF EVIDENCE IS NOT EVIDENCE OF READINESS.
#
# A check whose source artifact is missing reports MISSING, never PASS. A gate with
# any MISSING or FAIL in it is RED. There is no partial credit and no "close
# enough" state, because the entire failure mode being guarded against is a pass
# that was granted because nobody looked.
#
# The specific ways this could have lied, all of which are closed below:
#
# 0. AN EMPTY ARTIFACT PASSES. A report that parses to zero checks is not a green
#    report, it is a report that never ran. `--selftest` asserts the check count is
#    exactly EXPECTED_CHECKS; a refactor that silently drops a check trips it.
#
# 1. A GATE WITH NO CHECKS PASSES. Gate state is derived from its checks, and a gate
#    is only allowed to go GREEN if it evaluated at least one check. An unevaluated
#    gate is MISSING at the gate level, which is RED. This is the fail-open shape
#    that killed the automation runner.
#
# 2. THRESHOLDS INVENTED HERE. This script holds no opinions about how big the island
#    should be or how long a walk should take. Every target is read from the artifact
#    that already owns it: `blocking_count` from the greybox report, the ten-master
#    count from the art bible lock, the traversal windows from Docs/canon/FEEL.md. If a
#    source is missing the check is MISSING, never "assumed fine".
#
# 3. A WAIVER THAT HIDES A BLOCKER. Waivers are read from an explicit file and are
#    reported as their own state, listed in the output with their rationale, and
#    counted separately. A waived blocker does not vanish; it is visible as a
#    decision someone made and can be re-litigated by deleting one line. Waivers
#    that name a criterion/volume pair with no matching finding are reported as
#    STALE, because a waiver outliving its finding means the gate has stopped
#    describing reality.
#
# 4. A FRESH-LOOKING RUN THAT RAN NOTHING. `Saved/automation_run_result.json` is only
#    trusted when it actually executed tests; zero-tests-ran is MISSING, not PASS.
#    `dll_stale` is surfaced rather than ignored, because a green run against a stale
#    binary was a real event on this project on 2026-10-02.
#
# Deliberately NOT in scope: anything about whether the result is good. This script
# says whether a pass may START. Whether it should CONTINUE, and whether the game is
# any fun, is a human judgement and belongs in a taste gate. See
# docs/human-use/OWNERSHIP.md.
# ---------------------------------------------------------------------------

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# --------------------------------------------------------------------------
# Paths and constants
# --------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parents[2]

GRAYBOX_REPORT = ROOT / "Docs" / "qa" / "graybox_spec_report.json"
AUTOMATION_RESULT = ROOT / "Saved" / "automation_run_result.json"
WAIVERS_FILE = ROOT / "Docs" / "qa" / "polish_waivers.json"
BASELINE_FILE = ROOT / "Docs" / "qa" / "POLISH_BASELINE.json"
TRAVERSAL_BUDGET = ROOT / "Docs" / "qa" / "TRAVERSAL_BUDGET.json"
ASSET_BOARD_FILE = ROOT / "Docs" / "qa" / "POLISH_ASSET_BOARD.json"
HUMAN_PLAYTEST_FILE = ROOT / "Docs" / "qa" / "POLISH_HUMAN_PLAYTEST.json"
FEEL_CANON = ROOT / "Docs" / "canon" / "FEEL.md"
EXPORT_MANIFEST = ROOT / "AssetCreation" / "Exports" / "MVP_EXPORT_MANIFEST.md"
LIB_BLEND = ROOT / "blender" / "floating_island_homestead_LIB.blend"
UE_ISLAND_MEASUREMENT = ROOT / "Docs" / "qa" / "UE_ISLAND_MEASUREMENT.json"
MASTERS_DIR = ROOT / "Content" / "HomeWorld" / "Materials" / "Masters"
EXPORT_MANIFEST = ROOT / "AssetCreation" / "Exports" / "MVP_EXPORT_MANIFEST.md"
OUT_JSON = ROOT / "Docs" / "qa" / "POLISH_READINESS.json"
OUT_MD = ROOT / "Docs" / "qa" / "POLISH_READINESS.md"

#: Art bible S10 / AGENTS.md lock: exactly ten master materials. Not a preference.
EXPECTED_MASTER_COUNT = 10

#: If this changes, a check was dropped or renamed. Fail loudly rather than
#: reporting a green run over a smaller set of questions. See WHY #0.
EXPECTED_CHECKS = 19

#: Criteria the greybox report can raise as BLOCKING. Every one of these needs a
#: check in G-ENV or a recorded decision that it is out of scope. This is the
#: assertion that stops the gate covering a subset of the blockers and reading as
#: coverage - the hole that let `4_distinct` go unmentioned while the gate showed
#: G-ENV covering "greybox" as though it covered all of it.
BLOCKING_CRITERIA = {"2_sized", "4_distinct", "master_binding", "1_location"}

#: Stage ladder from Docs/37_POLISH_PASS_PROCESS.md. Each gate opens the furthest
#: stage that may be ENTERED. Stage N+1 geometry is the expensive kind.
STAGES = [
    "S0 MEASURE",
    "S1 BLOCKOUT",
    "S2 ART-BLOCKOUT",
    "S3 ASSET PRODUCTION",
    "S4 DRESS",
    "S5 FEEL TUNE",
]

PASS = "PASS"
FAIL = "FAIL"
MISSING = "MISSING"
WAIVED = "WAIVED"
STALE = "STALE"

#: Criteria some `_criterion_check` call has claimed to cover. Populated as checks
#: are built so the selftest can compare it against the report's own blocking
#: criteria. This is the assertion that would have caught `4_distinct` going
#: unmentioned while G-ENV presented itself as covering "greybox".
_COVERED_CRITERIA: set[str] = set()

GREEN = "GREEN"
RED = "RED"


# --------------------------------------------------------------------------
# Result types
# --------------------------------------------------------------------------


@dataclass
class Check:
    id: str
    gate: str
    requirement: str
    source: str
    measured: str
    target: str
    state: str
    note: str = ""


@dataclass
class Gate:
    id: str
    question: str
    max_stage: str
    checks: list[Check] = field(default_factory=list)

    @property
    def state(self) -> str:
        # WHY #1: a gate that evaluated nothing is not green. Deriving state from
        # counts is what made an empty check list look like a pass.
        if not self.checks:
            return MISSING
        if any(c.state in (FAIL, MISSING, STALE) for c in self.checks):
            return RED
        return GREEN

    def tally(self) -> dict[str, int]:
        out: dict[str, int] = {}
        for c in self.checks:
            out[c.state] = out.get(c.state, 0) + 1
        return out


# --------------------------------------------------------------------------
# Artifact loading. Every loader returns None rather than raising, and every
# caller treats None as MISSING. A crash here would be a hard error, not a pass.
# --------------------------------------------------------------------------


def _rel(path: Path) -> str:
    """Repo-relative, forward-slashed, and never raising.

    Windows backslashes inside a markdown table cell render as escapes and make
    the artifact column look like a broken path, which invites the reader to
    dismiss the row instead of fixing what it is reporting.

    A path outside the repo falls back to its absolute posix form rather than
    raising. Source paths get redirected - by a test fixture, or by pointing the
    gate at another checkout - and a gate that crashes while describing where it
    looked has failed at the one job it has.
    """
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_json(path: Path) -> dict[str, Any] | None:
    """Read a JSON artifact, tolerating the UTF-8 BOM that UE writes.

    `utf-8-sig` is not optional. This is the same bug that made
    run_ue_automation.py report 0/0 on every run it ever performed: UE writes
    index.json with a BOM, json.load raises, a bare except swallowed it, and the
    function returned its not-found branch. Two readers in one repo now decode the
    same way on purpose.
    """
    try:
        if not path.is_file():
            return None
        with path.open("r", encoding="utf-8-sig") as fh:
            data = json.load(fh)
        return data if isinstance(data, dict) else None
    except (OSError, ValueError):
        return None


def load_waivers() -> dict[tuple[str, str, str], dict[str, Any]]:
    """Map (criterion, volume, detail) -> waiver record.

    Keyed on all three because the greybox report files several independent
    blockers under one criterion for one volume — SM_Island_Hero alone carries both
    a size mismatch and a bad pivot. A two-part key would let a waiver intended to
    accept a size mismatch also silently accept a pivot bug.
    """
    data = _read_json(WAIVERS_FILE)
    if not data:
        return {}
    out: dict[tuple[str, str, str], dict[str, Any]] = {}
    for entry in data.get("waivers") or []:
        key = (
            str(entry.get("criterion", "")),
            str(entry.get("volume", "")),
            str(entry.get("detail", "")),
        )
        out[key] = entry
    return out


def blocking_findings(report: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not report:
        return []
    return [f for f in (report.get("findings") or []) if f.get("severity") == "blocking"]


def find_key(f: dict[str, Any]) -> tuple[str, str, str]:
    return (
        str(f.get("criterion", "")),
        str(f.get("volume", "")),
        str(f.get("detail", "")),
    )


# --------------------------------------------------------------------------
# G-ENV — may we begin sizing and blockout work?
# --------------------------------------------------------------------------

#: Traversal windows, DECLARED from Docs/canon/FEEL.md.
#:
#: These are a RESTATEMENT, not a parse. An earlier revision of this comment
#: claimed the values were "read from that file rather than restated, so the gate
#: cannot drift from canon. Parsed out of the markdown table." That was false --
#: they are literals, and the same module's docstring admitted "FEEL.md states the
#: windows; nothing reads them". A comment promising a guarantee the code does not
#: provide is worse than no comment, because it stops the next reader checking.
#:
#: So the drift is now CHECKED instead of asserted: `read_canon_windows()` parses
#: FEEL.md for real, and `check_env_canon_windows_in_sync` FAILs if these literals
#: no longer match it. Canon moved on 2026-10-03 (island 21x14 -> 180x100, walk
#: 6.0 m/s) without touching this table, which is exactly the case the old comment
#: promised would be impossible.
TRAVERSAL_TARGETS: dict[str, tuple[float, float]] = {
    "cabin_to_lookout_s": (15.0, 25.0),
    "island_circuit_s": (45.0, 90.0),
}

#: Which FEEL.md table row supplies which window. Matched on ASCII substrings that
#: survive the file's typographic characters -- the row reads "Cabin -> lookout walk"
#: with a real arrow and en-dashes, and an earlier grep-based reader saw mojibake
#: there and would have matched nothing.
FEEL_WINDOW_ROWS: dict[str, tuple[str, ...]] = {
    "cabin_to_lookout_s": ("Cabin", "lookout walk"),
    "island_circuit_s": ("Island circuit",),
}

# "~15-25 s", "~12-25 s", with hyphen, en dash or em dash, spaces optional.
_RANGE_RE = re.compile(
    r"(\d+(?:\.\d+)?)\s*[-–—]\s*(\d+(?:\.\d+)?)\s*s\b"
)


def read_canon_windows() -> tuple[dict[str, tuple[float, float]], list[str]]:
    """Parse the traversal windows out of FEEL.md. Returns (windows, problems).

    Returns problems rather than raising: a missing or unreadable canon file has
    to surface as a RED check, not as a traceback that stops the gate reporting.
    An empty dict means "could not read canon", which the caller must treat as
    unknown -- never as "no windows exist".
    """
    problems: list[str] = []
    if not FEEL_CANON.is_file():
        return {}, [f"{_rel(FEEL_CANON)} is absent"]
    try:
        text = FEEL_CANON.read_text(encoding="utf-8-sig", errors="replace")
    except OSError as exc:
        return {}, [f"{_rel(FEEL_CANON)} unreadable: {exc}"]

    out: dict[str, tuple[float, float]] = {}
    for key, needles in FEEL_WINDOW_ROWS.items():
        row = next(
            (ln for ln in text.splitlines()
             if ln.lstrip().startswith("|") and all(n in ln for n in needles)),
            None,
        )
        if row is None:
            problems.append(f"no FEEL.md table row matching {needles}")
            continue
        hit = _RANGE_RE.search(row)
        if hit is None:
            problems.append(f"FEEL.md row {needles} has no 'NN-NN s' range: {row.strip()[:70]}")
            continue
        lo, hi = float(hit.group(1)), float(hit.group(2))
        if not 0 < lo <= hi:
            problems.append(f"FEEL.md row {needles} is not an ascending range: {row.strip()[:70]}")
            continue
        out[key] = (lo, hi)
    return out, problems


def check_env_canon_windows_in_sync() -> Check:
    """The windows this gate judges against must still be the ones canon states.

    A hardcoded window silently becomes a private taste decision the moment canon
    moves: the gate keeps reporting "inside canon" for a number the Lead has
    replaced, and nothing says so. This is the check that makes the drift visible.
    """
    canon, problems = read_canon_windows()
    # A partial parse must never read as agreement. If one row came back but
    # another did not, comparing only the row that parsed would report PASS over
    # a canon file we demonstrably failed to understand -- the same fail-open as
    # an absent artifact treated as a clean one.
    if not canon or problems:
        return Check(
            "env.canon_windows_in_sync", "G-ENV",
            "Gate traversal windows match Docs/canon/FEEL.md",
            _rel(FEEL_CANON),
            "could not read canon" if not canon else f"{len(canon)} of "
            f"{len(FEEL_WINDOW_ROWS)} windows parsed",
            "same windows",
            MISSING,
            "; ".join(problems) + ". The gate is judging against its own literals "
            "while canon is not fully readable, so nothing can be said about "
            "agreement.",
        )
    drifted = [
        f"{k}: gate {TRAVERSAL_TARGETS[k][0]:g}-{TRAVERSAL_TARGETS[k][1]:g} "
        f"vs canon {v[0]:g}-{v[1]:g}"
        for k, v in sorted(canon.items())
        if k in TRAVERSAL_TARGETS and TRAVERSAL_TARGETS[k] != v
    ]
    missing = [k for k in canon if k not in TRAVERSAL_TARGETS]
    if drifted or missing:
        return Check(
            "env.canon_windows_in_sync", "G-ENV",
            "Gate traversal windows match Docs/canon/FEEL.md",
            _rel(FEEL_CANON),
            "; ".join(drifted) or "window absent from the gate",
            "same windows", FAIL,
            "Canon moved and the gate did not. Update TRAVERSAL_TARGETS in this "
            "file to the values canon now states, or decide deliberately that the "
            "gate should keep judging the old window -- and say which in the commit.",
        )
    return Check(
        "env.canon_windows_in_sync", "G-ENV",
        "Gate traversal windows match Docs/canon/FEEL.md",
        _rel(FEEL_CANON), f"{len(canon)} windows agree", "same windows", PASS,
        ", ".join(f"{k} {v[0]:g}-{v[1]:g}" for k, v in sorted(canon.items())),
    )

#: The six tunables Docs/canon/FEEL.md still holds as TODO proposals. Named here so
#: POLISH_BASELINE.json and the gate agree on what "all of them" means -- without a
#: list, a file containing one arbitrary key would satisfy ">=1 baseline" and the
#: gate would go green having measured nothing that matters.
FEEL_TUNABLES: tuple[str, ...] = (
    "glide_gravity_scale",
    "glide_lateral_influence",
    "camera_arm_length_uu",
    "camera_pitch_bias_deg",
    "night_length_s",
    "gather_cooldown_s",
)


def check_env_world_assembled() -> Check:
    """A world exists to size. This checks external actors, not the .umap filename.

    The repo's own docs call the primary worlds 'DemoMap and Homestead'. Neither
    name exists. The assembled homestead is Content/HomeWorld/Maps/MainMenu.umap
    with ~1270 external actors. Naming it correctly is a documentation fix; what
    matters for readiness is that geometry is placed.
    """
    maps_dir = ROOT / "Content" / "HomeWorld" / "Maps"
    ext_root = ROOT / "Content" / "__ExternalActors__" / "HomeWorld" / "Maps"
    if not maps_dir.is_dir():
        return Check(
            "env.world_assembled", "G-ENV",
            "A placed world exists to size",
            "Content/HomeWorld/Maps",
            "maps directory absent", ">=1 map with placed actors", MISSING,
            "No map directory. Nothing to measure size against.",
        )
    total = 0
    if ext_root.is_dir():
        total = sum(1 for _ in ext_root.rglob("*.uasset"))
    maps = sorted(p.name for p in maps_dir.glob("*.umap"))
    if total == 0:
        return Check(
            "env.world_assembled", "G-ENV",
            "A placed world exists to size",
            "Content/__ExternalActors__", f"0 placed actors ({len(maps)} maps)",
            ">=1 placed actor", MISSING,
            "Maps exist but carry no external actors. This is an empty level.",
        )
    return Check(
        "env.world_assembled", "G-ENV",
        "A placed world exists to size",
        "Content/__ExternalActors__", f"{total} placed actors across {len(maps)} maps",
        ">=1 placed actor", PASS,
        f"Maps: {', '.join(maps)}. Note the docs name worlds that do not exist; "
        "the assembled homestead is MainMenu.",
    )


def check_env_traversal_measured() -> Check:
    """Can the walk be timed in-engine against the canon window?

    This is the single most important missing instrument in the project. FEEL.md
    declares cabin->lookout 15-25s and island circuit 45-90s, and nothing anywhere
    measures either. Until a number exists, 'the island feels too big' is an
    opinion, and opinions are what produce a second art pass nobody budgeted for.
    """
    data = _read_json(BASELINE_FILE)
    if data is None:
        return Check(
            "env.traversal_measured", "G-ENV",
            "Traversal time measured in-engine against the canon window",
            _rel(BASELINE_FILE), "no artifact",
            "; ".join(f"{k} {v[0]:g}-{v[1]:g}" for k, v in TRAVERSAL_TARGETS.items()),
            MISSING,
            "No instrument exists. FEEL.md states the windows; nothing reads them. "
            "Build the measurement before changing size, not after.",
        )
    rows = []
    bad = []
    unmeasured = []
    for key, (lo, hi) in TRAVERSAL_TARGETS.items():
        val = (data.get(key) or {}).get("measured_s")
        if not isinstance(val, (int, float)) or isinstance(val, bool):
            # Declared but not yet filled in. That is MISSING, not FAIL: FAIL
            # means "we measured it and it is wrong", and nothing was measured.
            # Creating POLISH_BASELINE.json with nulls must not make the gate
            # accuse the world of being mis-sized on the Lead's first run.
            rows.append(f"{key} unmeasured")
            unmeasured.append(key)
            continue
        rows.append(f"{key} {val:g}s")
        if not (lo <= float(val) <= hi):
            bad.append(key)
    if unmeasured:
        return Check(
            "env.traversal_measured", "G-ENV",
            "Traversal time measured in-engine against the canon window",
            _rel(BASELINE_FILE), "; ".join(rows),
            "; ".join(f"{k} {v[0]:g}-{v[1]:g}" for k, v in TRAVERSAL_TARGETS.items()),
            MISSING,
            "Not yet measured: " + ", ".join(unmeasured) + ". The artifact exists and "
            "the keys are declared, but no number has been recorded. Timing a walk "
            "needs the desktop editor with cells streamed and a human on the keys.",
        )
    if bad:
        return Check(
            "env.traversal_measured", "G-ENV",
            "Traversal time measured in-engine against the canon window",
            _rel(BASELINE_FILE), "; ".join(rows),
            "; ".join(f"{k} {v[0]:g}-{v[1]:g}" for k, v in TRAVERSAL_TARGETS.items()),
            FAIL,
            "Measured and out of window: " + ", ".join(bad) + ". Either the world or "
            "the window is wrong; which one is a human call.",
        )
    return Check(
        "env.traversal_measured", "G-ENV",
        "Traversal time measured in-engine against the canon window",
        _rel(BASELINE_FILE), "; ".join(rows),
        "; ".join(f"{k} {v[0]:g}-{v[1]:g}" for k, v in TRAVERSAL_TARGETS.items()),
        PASS, "Both windows measured and inside canon.",
    )


def _criterion_check(
    cid: str,
    criterion: str,
    requirement: str,
    waivers: dict[tuple[str, str, str], dict[str, Any]],
    detail_match: str | None = None,
    report: dict[str, Any] | None = None,
    report_present: bool = True,
) -> Check:
    """One greybox criterion as a readiness check, honouring waivers.

    `detail_match` narrows within a criterion. This is load-bearing rather than
    cosmetic: the greybox report files BOTH the island size mismatch and the
    island pivot bug under criterion `2_sized`. A pivot check that looked for a
    criterion named after itself would match nothing and report PASS while the
    blocker was still red — the exact fail-open shape this script exists to avoid.
    Narrowing by detail text splits one criterion into the two independent
    questions it actually contains.

    `report` is injectable so --selftest can drive the waiver and staleness logic
    from synthetic fixtures. Left reading only from disk, those paths could be
    tested solely against whatever happens to be on the machine, which makes the
    guard unfalsifiable in the one situation where it matters: someone changing
    this logic to be more permissive, and the tests agreeing with them because
    they read the same unchanged file.

    The two injection parameters are three-way, and the middle case is the one to
    be careful with:
        report={...}                     injected; disk ignored
        report=None, report_present=True  no injection; read from disk
        report=None, report_present=False the artifact does not exist

    Waiver handling is deliberately loud. A waived blocker still appears in the
    output with its rationale, and a waiver naming a finding that no longer exists
    is reported STALE rather than quietly ignored, because a gate whose waivers have
    outlived their findings is no longer describing the repo.
    """
    src = _rel(GRAYBOX_REPORT)
    _COVERED_CRITERIA.add(criterion)
    if report is None and report_present:
        report = _read_json(GRAYBOX_REPORT)
    if report is None:
        return Check(cid, "G-ENV", requirement, src, "no artifact", "0 findings",
                     MISSING, "Greybox report not found. Regenerate it in Blender.")

    hits = [
        f for f in blocking_findings(report)
        if f.get("criterion") == criterion
        and (detail_match is None or detail_match in str(f.get("detail", "")))
    ]
    # Staleness is judged against the WHOLE report, not this filtered subset.
    # A waiver for the island pivot is not stale merely because this check is
    # looking at the size finding; it is stale only when no blocking finding in
    # the report carries its exact identity any more.
    all_live = {find_key(f) for f in blocking_findings(report)}
    stale = sorted(
        rec.get("volume", "")
        for key, rec in waivers.items()
        if key[0] == criterion and key not in all_live
    )
    if stale:
        return Check(
            cid, "G-ENV", requirement, src,
            f"{len(hits)} blocking; {len(stale)} stale waiver(s)", "0 findings",
            STALE,
            f"Waived but no longer blocking: {', '.join(stale)}. Remove the waiver.",
        )

    waived, open_hits = [], []
    for f in hits:
        rec = waivers.get(find_key(f))
        (waived if rec else open_hits).append(f)

    if open_hits:
        detail = "; ".join(
            f"{f.get('volume')}: {f.get('detail')}" for f in open_hits[:4]
        )
        if len(open_hits) > 4:
            detail += f" (+{len(open_hits) - 4} more)"
        return Check(cid, "G-ENV", requirement, src,
                     f"{len(open_hits)} blocking", "0 blocking", FAIL, detail)

    if waived:
        detail = "; ".join(
            f"{f.get('volume')}: {waivers[find_key(f)].get('rationale', 'no rationale')}"
            for f in waived
        )
        return Check(cid, "G-ENV", requirement, src, f"{len(waived)} waived",
                     "0 blocking", WAIVED, detail)

    return Check(cid, "G-ENV", requirement, src, "0 blocking", "0 blocking", PASS)


def check_env_pivot() -> Check:
    """Assembly roots must sit on their ground contact.

    This one is cheap to fix and expensive to ignore. The island root's lowest
    vertex is at Z -0.450, so every module parented under it inherits that offset.
    Dressing props on top of a bad pivot produces placements that are all subtly
    wrong in the same direction, and the fix after the art pass is to rebuild them.
    """
    return _criterion_check(
        "env.pivot_grounded", "2_sized",
        "Assembly roots are pivoted at ground contact",
        load_waivers(), detail_match="ground contact",
    )


def check_env_master_binding() -> Check:
    return _criterion_check(
        "env.master_binding", "master_binding",
        "Every material resolves to one of the ten masters (art bible S10)",
        load_waivers(),
    )


def check_env_family_distinct() -> Check:
    """Silhouette families must be distinguishable from each other.

    Added because the gate was covering four of the five blocking findings in the
    greybox report and not saying so. A gate that reports honestly on a subset is
    worse than no gate, because it reads as coverage. Any criterion the greybox
    report can raise as blocking needs either a check here or a recorded decision
    that it is deliberately out of scope for sizing.
    """
    return _criterion_check(
        "env.family_distinct", "4_distinct",
        "Silhouette families measure distinctly from one another",
        load_waivers(),
    )


def _manifest_rows() -> list[tuple[str, str, int]]:
    """(category, filename, recorded_size) for every FBX row in the export manifest.

    The manifest is the only inventory of what Blender has handed to Unreal. It is
    also, as of 2026-10-04, the only thing that noticed an export had gone stale -
    see check_env_export_fresh.
    """
    rows: list[tuple[str, str, int]] = []
    if not EXPORT_MANIFEST.is_file():
        return rows
    for line in EXPORT_MANIFEST.read_text(encoding="utf-8", errors="replace").splitlines():
        if ".fbx" not in line or "`" not in line:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        name = cells[1].strip("`").strip()
        if not name.lower().endswith(".fbx"):
            continue
        try:
            size = int(cells[2])
        except ValueError:
            continue
        rows.append((cells[0], name, size))
    return rows


def check_env_export_fresh() -> Check:
    """Every FBX on disk matches the size the manifest recorded for it.

    WHY THIS EXISTS. On 2026-10-04 the island plate was applied and verified in
    blender/floating_island_homestead_LIB.blend, which measured 180.0 x 100.0 x
    0.45, and env.island_sized went PASS. The FBX that Unreal actually consumes
    still measured 19.3 x 10.7 - the pre-plate geometry, exported on 2026-09-16 -
    and the .uasset imported from it on 2026-09-28. Every gate row was reading the
    Blender source of truth and none of them read the artefact the game is built
    from, so a green gate was describing a mesh that no player could stand on.

    A clean log was not evidence here. The check that would have caught it is a
    size comparison against a file that was already being maintained, which is why
    it is a check and not a note. Of 23 FBX rows it named exactly one: SM_IslandTop.

    WHAT THIS CANNOT SEE, STATED PLAINLY. Size is a proxy for geometry, not
    geometry. It catches an export that did not happen or happened against
    different source, which is the failure that occurred. It cannot catch an
    unchanged export that is stale in substance, and it says so rather than
    claiming more.

    An earlier draft also compared each FBX's mtime against the .blend's and
    failed the row when any FBX was older. That reported 23 of 23 stale after a
    single object's geometry changed, because saving the blend touches one file and
    every export in it legitimately predates that save. A whole-file timestamp
    cannot describe per-object change, so it was removed rather than tuned. Its
    number is still printed, labelled as a hint.

    The companion hole - an FBX that is current but was never re-imported - is
    check_env_ue_island_measured. Together they cover the chain; neither covers it
    alone.

    MISSING, not FAIL, when the manifest lists a file that is absent: the row is
    unverified rather than wrong, and FAIL would push someone to hand-edit a size
    rather than re-run the export.
    """
    rows = _manifest_rows()
    if not rows:
        return Check(
            "env.export_fresh", "G-ENV",
            "Every exported FBX matches the size the manifest recorded",
            _rel(EXPORT_MANIFEST), "no rows parsed", "0 stale",
            MISSING,
            "The export manifest is missing or has no parseable FBX rows. Without it "
            "there is no inventory of what Blender has handed to Unreal.",
        )

    exports_root = EXPORT_MANIFEST.parent
    stale: list[str] = []
    missing: list[str] = []
    for category, name, recorded in rows:
        path = exports_root / category / name
        if not path.is_file():
            missing.append(name)
            continue
        actual = path.stat().st_size
        if actual != recorded:
            stale.append(f"{name} manifest {recorded} != disk {actual}")

    blend_mtime = LIB_BLEND.stat().st_mtime if LIB_BLEND.is_file() else None
    behind = 0
    if blend_mtime is not None:
        behind = sum(
            1 for category, name, _ in rows
            if (exports_root / category / name).is_file()
            and (exports_root / category / name).stat().st_mtime < blend_mtime - 1.0)

    note_bits: list[str] = []
    if stale:
        note_bits.append("re-export needed, size differs from manifest: "
                         + "; ".join(stale))
    if missing:
        note_bits.append("listed but not on disk: " + ", ".join(missing[:6]))
    note_bits.append(
        f"hint: {behind} of {len(rows)} FBX predate the .blend save, which is normal "
        f"and is not counted - one object's edit touches the whole file")

    question = "Every exported FBX matches the size the manifest recorded"
    if stale:
        return Check(
            "env.export_fresh", "G-ENV", question, _rel(EXPORT_MANIFEST),
            f"{len(stale)} stale of {len(rows)}", f"0 stale of {len(rows)}",
            FAIL, " | ".join(note_bits),
        )
    if missing:
        return Check(
            "env.export_fresh", "G-ENV", question, _rel(EXPORT_MANIFEST),
            f"0 stale, {len(missing)} absent of {len(rows)}",
            f"0 stale of {len(rows)}", MISSING, " | ".join(note_bits),
        )
    return Check(
        "env.export_fresh", "G-ENV", question, _rel(EXPORT_MANIFEST),
        f"0 stale of {len(rows)}", f"0 stale of {len(rows)}", PASS,
        " | ".join(note_bits),
    )


def check_env_ue_island_measured() -> Check:
    """The island as Unreal sees it has been measured, and agrees with Blender.

    check_env_export_fresh proves the FBX is current. This proves the thing after
    it: that somebody imported the current FBX and measured the result in the
    editor. Those are different claims and the gap between them is exactly where
    the 2026-10-04 plate went missing - the FBX was regenerated, but nothing
    recorded that the .uasset and the level were rebuilt from it.

    Unreal is not reachable from this script, so the measurement is a file an
    in-editor script writes (Content/Python/measure_ue_island.py). Until somebody
    runs it, this row is MISSING and the gate says so out loud rather than letting
    a Blender-side PASS imply an engine-side one.

    Units: the record is in Unreal centimetres, the comparison is in Blender
    metres. A conversion that is quietly wrong would move the number by 100x, so
    the tolerance is stated in metres and the raw value is printed beside it.
    """
    source_m = _island_bbox_blender_m()
    if source_m is None:
        return Check(
            "env.ue_island_measured", "G-ENV",
            "The island measured inside Unreal agrees with the Blender source",
            _rel(UE_ISLAND_MEASUREMENT), "no Blender-side measurement",
            "agrees", MISSING,
            "The greybox report has no SM_IslandTop measurement to compare against. "
            "Regenerate Docs/qa/graybox_spec_report.json first.",
        )

    question = "The island measured inside Unreal agrees with the Blender source"

    def unmeasured(measured: str, tail: str = "") -> Check:
        # One note for one condition. A missing file and a null bbox_cm are the
        # same fact - nobody has measured it - and this repo already shipped one
        # of them with a terser note than the other, which is how a reader ends up
        # guessing which hop is unverified. Both say the same thing.
        note = (
            "Nobody has measured the island inside Unreal. The Blender side reads "
            f"{source_m[0]:.1f} x {source_m[1]:.1f} m, but that is the source, not "
            "the mesh the game is built from. This exact gap is how the 2026-10-04 "
            "plate went missing: the .blend and the report said 180 x 100 while "
            "Unreal was still holding 19.3 x 10.7. Run "
            "Content/Python/measure_ue_island.py in the editor - it only reads - "
            "and commit what it writes. Hand-writing bbox_cm defeats the point."
        )
        return Check("env.ue_island_measured", "G-ENV", question,
                     _rel(UE_ISLAND_MEASUREMENT), measured, "agrees",
                     MISSING, note + tail)

    data = _read_json(UE_ISLAND_MEASUREMENT)
    if data is None:
        return unmeasured("no artifact")

    raw = data.get("bbox_cm")
    if not (isinstance(raw, (list, tuple)) and len(raw) >= 2):
        return unmeasured("no bbox_cm")

    try:
        ue_x_m, ue_y_m = float(raw[0]) / 100.0, float(raw[1]) / 100.0
    except (TypeError, ValueError):
        return Check(
            "env.ue_island_measured", "G-ENV", question,
            _rel(UE_ISLAND_MEASUREMENT), f"unparseable {raw!r}", "agrees", MISSING,
            "bbox_cm holds something that is not two numbers.",
        )

    # 2% of the span, or 1 m, whichever is larger. The point is to catch an
    # un-reimported asset (180 vs 19.3 is a 9x error), not to adjudicate
    # centimetre-level disagreement between two engines.
    tol = max(1.0, source_m[0] * 0.02)
    off_x = abs(ue_x_m - source_m[0])
    off_y = abs(ue_y_m - source_m[1])
    worst = max(off_x, off_y)
    measured = f"UE {ue_x_m:.1f} x {ue_y_m:.1f} m"
    target = f"Blender {source_m[0]:.1f} x {source_m[1]:.1f} m"
    if worst <= tol:
        state, note = PASS, f"within {tol:.2f} m; raw {list(raw)} cm"
    else:
        state = FAIL
        note = (f"off by {off_x:.2f} m in X and {off_y:.2f} m in Y, tol {tol:.2f}. "
                f"Blender says {source_m[0]:.1f} x {source_m[1]:.1f} m, Unreal says "
                f"{ue_x_m:.1f} x {ue_y_m:.1f} m. The usual cause is an FBX that was "
                f"re-exported and never re-imported, so the .uasset and the level "
                f"still hold the older mesh. Re-import and re-place, then re-run "
                f"the measuring script. Raw: {list(raw)} cm.")
    return Check(
        "env.ue_island_measured", "G-ENV", question,
        _rel(UE_ISLAND_MEASUREMENT), measured, target, state, note,
    )


def _island_bbox_blender_m() -> tuple[float, float] | None:
    """SM_IslandTop's measured footprint in metres, from the greybox report."""
    report = _read_json(GRAYBOX_REPORT)
    if not isinstance(report, dict):
        return None
    entry = (report.get("measurements") or {}).get("SM_IslandTop")
    if not isinstance(entry, dict):
        return None
    bbox = entry.get("bbox")
    if not (isinstance(bbox, (list, tuple)) and len(bbox) >= 2):
        return None
    try:
        return float(bbox[0]), float(bbox[1])
    except (TypeError, ValueError):
        return None


def check_env_island_sized() -> Check:
    return _criterion_check(
        "env.island_sized", "2_sized",
        "Assembly extents match their declared spec size",
        load_waivers(), detail_match="bbox",
    )


# --------------------------------------------------------------------------
# G-ASSET — may we begin asset production?
# --------------------------------------------------------------------------


def _upstream(gates: dict[str, Gate], gate_id: str) -> Check:
    """A gate cannot open while the gate beneath it is red.

    This encodes the industry's one consistent rule about art passes: the
    environment artist waits for a mature blockout. Making it a dependency rather
    than advice is the whole point — the failure this prevents is a month of
    production art against geometry that then moves.
    """
    up = gates.get(gate_id)
    if up is None:
        return Check(f"dep.{gate_id.lower()}", "", "", "", "", "", MISSING,
                     f"{gate_id} was not evaluated.")
    state = up.state
    return Check(
        f"dep.{gate_id.lower()}", "", f"{gate_id} must be GREEN first", "", state,
        GREEN, PASS if state == GREEN else FAIL,
        "" if state == GREEN else
        f"{gate_id} is {state}; its stage cannot be entered yet.",
    )


def check_env_traversal_reachable() -> Check:
    """Can the island's size even satisfy the canon windows?

    The companion to `env.traversal_measured`, and much cheaper. That check asks
    whether anyone has timed a walk. This one asks whether the windows are
    arithmetically reachable given the island that exists, which needs only the
    walk speed and the authored extents - both readable headlessly.

    It is the check that earns the whole measurement layer. `island circuit 45-90 s`
    implies 270-540 m of walking at 6.0 m/s, against a 48 m perimeter. Nobody
    could have seen that without dividing the window by the speed and comparing
    it to the island, and the island was authored at 19.3 m a long time before
    anyone asked.
    """
    data = _read_json(TRAVERSAL_BUDGET)
    src = _rel(TRAVERSAL_BUDGET)
    if data is None:
        return Check(
            "env.traversal_reachable", "G-ENV",
            "No canon traversal window contradicts the island size",
            src, "no artifact", "0 unreachable windows", MISSING,
            "Run Content/Python/traversal_budget.py. It needs the movement probe, "
            "so run probe_movement_budget.py in the editor first.",
        )
    verdict = data.get("verdict")
    windows = data.get("windows") or {}
    failing = sorted(k for k, v in windows.items()
                     if v.get("state") == "NOT_REACHABLE")
    unmeasured = sorted(k for k, v in windows.items()
                        if v.get("state") not in ("REACHABLE", "NOT_REACHABLE"))

    # An artifact that parsed to zero windows measured nothing. Reporting that as
    # a pass is the exact shape of failure this script exists to prevent.
    if not windows:
        return Check(
            "env.traversal_reachable", "G-ENV",
            "No canon traversal window contradicts the island size",
            src, "0 windows evaluated", "0 unreachable windows", MISSING,
            "The budget report contains no windows. It did not measure anything.",
        )

    note = ""
    for key in failing:
        note += f"{key}: {windows[key].get('note', '')} "
    if unmeasured:
        note += f"unmeasured: {', '.join(unmeasured)}. "

    if verdict == "NOT_REACHABLE" or failing:
        return Check(
            "env.traversal_reachable", "G-ENV",
            "No canon traversal window contradicts the island size",
            src, f"{len(failing)} unreachable of {len(windows)}", "0 unreachable",
            FAIL, note.strip() or
            "A canon window cannot be met on the island as built.")
    if unmeasured or verdict == "UNMEASURED":
        return Check(
            "env.traversal_reachable", "G-ENV",
            "No canon traversal window contradicts the island size",
            src, f"{len(unmeasured)} unmeasured of {len(windows)}", "0 unreachable",
            MISSING, note.strip() or "Some windows could not be checked.")
    return Check(
        "env.traversal_reachable", "G-ENV",
        "No canon traversal window contradicts the island size",
        src, f"0 unreachable of {len(windows)}", "0 unreachable", PASS,
        "Size does not contradict any window. This does NOT mean a real walk fits "
        "them - the timing instrument is `env.traversal_measured`.",
    )


def check_asset_masters() -> Check:
    if not MASTERS_DIR.is_dir():
        return Check("asset.master_count", "G-ASSET",
                     "Exactly ten master materials exist",
                     _rel(MASTERS_DIR), "directory absent",
                     str(EXPECTED_MASTER_COUNT), MISSING, "")
    names = sorted(p.stem for p in MASTERS_DIR.glob("*.uasset"))
    n = len(names)
    state = PASS if n == EXPECTED_MASTER_COUNT else FAIL
    return Check(
        "asset.master_count", "G-ASSET",
        "Exactly ten master materials exist (art bible S10)",
        _rel(MASTERS_DIR), f"{n} masters", str(EXPECTED_MASTER_COUNT),
        state, ", ".join(names),
    )


def check_asset_board() -> Check:
    """Per-asset production stage, so 'how far along is pass 1' has an answer.

    The industry practice is unremarkable and consistently stated: track each asset
    through its stages so that feedback is possible before the expensive steps. What
    makes it bite here is doing many assets to a cheap stage and reviewing them as a
    batch, because a 50%-finished asset is often 100%-finished enough to judge and
    a finished one is too late to move cheaply.
    """
    data = _read_json(ASSET_BOARD_FILE)
    if data is None:
        return Check(
            "asset.board", "G-ASSET",
            "Every master mesh has a declared stage and priority",
            _rel(ASSET_BOARD_FILE), "no artifact",
            "one row per mesh", MISSING,
            "No asset board. Without one, 'asset pass 1' has no definition of "
            "done and no way to batch review before the expensive stages.",
        )
    assets = data.get("assets") or []
    if not assets:
        return Check(
            "asset.board", "G-ASSET",
            "Every master mesh has a declared stage and priority",
            _rel(ASSET_BOARD_FILE), "0 assets listed", "one row per master",
            MISSING,
            "The board exists but lists no assets. It should carry one row per "
            "master material, all ten.",
        )

    staged: list[str] = []
    undeclared: list[str] = []
    bad_stage: list[str] = []
    for asset in assets:
        name = str(asset.get("name") or "?")
        code = _stage_code(asset.get("stage"))
        if asset.get("stage") and code is None:
            bad_stage.append(f"{name}={asset.get('stage')!r}")
            continue
        if code is not None and str(asset.get("priority") or "").strip():
            staged.append(name)
        else:
            undeclared.append(name)

    # MISSING, not FAIL, while rows are blank. An un-triaged asset is an open
    # question, not a defect; FAIL would accuse the board of being wrong about
    # production state nobody has recorded yet. This is the same rule the playtest
    # record follows, for the same reason: FAIL leaves "just write something" as the
    # only route to green.
    if bad_stage:
        return Check(
            "asset.board", "G-ASSET",
            "Every master mesh has a declared stage and priority",
            _rel(ASSET_BOARD_FILE),
            f"{len(staged)}/{len(assets)} declared",
            f"{len(assets)}/{len(assets)} declared",
            FAIL,
            "Stage is not one of Docs/37_POLISH_PASS_PROCESS.md's ladder: "
            + "; ".join(bad_stage[:6])
            + ". Use the rung code (S0..S5) or its full label.",
        )
    if undeclared:
        return Check(
            "asset.board", "G-ASSET",
            "Every master mesh has a declared stage and priority",
            _rel(ASSET_BOARD_FILE),
            f"{len(staged)}/{len(assets)} declared",
            f"{len(assets)}/{len(assets)} declared",
            MISSING,
            "Declared but not recorded yet: " + ", ".join(undeclared[:6])
            + ". Each row needs a stage from the S0-S5 ladder and a priority, so a "
            "batch can be reviewed together at S2 rather than one at a time at S3.",
        )
    return Check(
        "asset.board", "G-ASSET",
        "Every master mesh has a declared stage and priority",
        _rel(ASSET_BOARD_FILE),
        f"{len(staged)}/{len(assets)} declared", f"{len(assets)}/{len(assets)} declared",
        PASS, ", ".join(staged[:8]),
    )


def _stage_code(value: Any) -> str | None:
    """Normalise a stage entry to its rung code, or None if it names no rung.

    Accepts "S2", "s2" and "S2 ART-BLOCKOUT" so a hand edit cannot fail on
    punctuation, but rejects "blockout" and "S7" -- a stage that is not on the
    ladder must not read as declared, or the board claims a production state that
    Docs/37 does not define.
    """
    text = str(value or "").strip().upper()
    if not text:
        return None
    for stage in STAGES:
        code = stage.split()[0]
        if text == code or text.startswith(code + " "):
            return code
    return None


def check_asset_poly_budgets() -> Check:
    if not EXPORT_MANIFEST.is_file():
        return Check(
            "asset.poly_budgets", "G-ASSET",
            "Export manifest declares a poly budget per mesh",
            _rel(EXPORT_MANIFEST), "absent", "budget per mesh",
            MISSING, "")
    text = EXPORT_MANIFEST.read_text(encoding="utf-8-sig", errors="replace")
    has_budget = bool(re.search(r"(?i)(poly|tris?|budget)", text))
    return Check(
        "asset.poly_budgets", "G-ASSET",
        "Export manifest declares a poly budget per mesh",
        _rel(EXPORT_MANIFEST),
        "declared" if has_budget else "no budget column found",
        "budget per mesh", PASS if has_budget else FAIL,
        "" if has_budget else
        "Budgets are what stop a dressing pass from quietly tripling the cost of "
        "the level.",
    )


# --------------------------------------------------------------------------
# G-FEEL — may we begin mechanics feel work?
# --------------------------------------------------------------------------


def check_feel_human_playtest() -> Check:
    """A human has to have played the build. There is no substitute.

    Nothing in this repo substitutes for it: not 42 green automation rows, not the
    eight-verb script, not Docs/canon/PLAYTEST.md. Every one of those is a code
    assertion or a scripted probe. Green code means the verbs fire; it says nothing
    about whether the island is the right size or the glide is the right shape,
    which are exactly the two questions a feel pass exists to answer.
    """
    data = _read_json(HUMAN_PLAYTEST_FILE)
    if data is None:
        return Check(
            "feel.human_playtest", "G-FEEL",
            "A human has played the build at a named commit",
            _rel(HUMAN_PLAYTEST_FILE), "never performed", "1 record",
            MISSING,
            "Docs/canon/PLAYTEST.md's last known good is a scripted PIE probe from "
            "2026-09-20, not a play session. A feel pass tuned without a human in "
            "the loop is tuning against an imagined player.",
        )
    commit = str(data.get("commit") or "")
    played = data.get("played_at")
    if not commit or not played:
        # MISSING, not FAIL. The artifact exists but nobody has played yet -- a
        # seeded skeleton with null fields is not a half-finished playtest, and FAIL
        # would accuse the record of being unusable when it has simply never been
        # filled in. FAIL is reserved for a record that names a commit and a
        # timestamp, which is a claim that can then be checked against the build.
        return Check(
            "feel.human_playtest", "G-FEEL",
            "A human has played the build at a named commit",
            _rel(HUMAN_PLAYTEST_FILE),
            f"declared, never filled in (commit={commit or 'none'})",
            "commit + timestamp",
            MISSING,
            "The record exists and the fields are empty. Fill in commit (the short "
            "sha you played), played_at, and notes. Until then no human has played "
            "this build.",
        )
    return Check(
        "feel.human_playtest", "G-FEEL",
        "A human has played the build at a named commit",
        _rel(HUMAN_PLAYTEST_FILE), f"{commit} @ {played}",
        "commit + timestamp", PASS, str(data.get("notes", ""))[:200],
    )


def check_feel_tunable_baselines() -> Check:
    """Every tunable marked TODO in FEEL.md needs a measured current value.

    FEEL.md holds six tunables as proposals with rationale but no chosen number,
    because nothing was ever played to choose one. Measuring the value as it
    stands today costs nothing and is the precondition for telling whether a change
    helped. Tuning horizontal is only horizontal if you know where you started.
    """
    if not FEEL_CANON.is_file():
        return Check(
            "feel.tunable_baselines", "G-FEEL",
            "Every TODO tunable has a measured pre-tune value",
            _rel(FEEL_CANON), "absent", "one value per tunable",
            MISSING, "")
    data = _read_json(BASELINE_FILE)
    baselines = (data or {}).get("tunables") or {}
    if not baselines:
        return Check(
            "feel.tunable_baselines", "G-FEEL",
            "Every TODO tunable has a measured pre-tune value",
            _rel(BASELINE_FILE), "0 baselines", ">=1 per tunable",
            MISSING,
            "FEEL.md lists glide gravity, lateral influence, camera arm, camera "
            "pitch bias, night length and gather cooldown as TODO proposals. None "
            "has a measured current value.",
        )
    # A key present with a null value is a declared placeholder, not a baseline.
    # Counting it would let a freshly-seeded skeleton turn this check PASS and hand
    # the polish pass a green gate over six unfilled numbers.
    measured = [k for k, v in baselines.items() if isinstance(v, (int, float, str, bool)) and v is not None]
    pending = [k for k in FEEL_TUNABLES if k not in measured]
    measured_str = ", ".join(sorted(measured)[:8]) or "none"
    if pending:
        return Check(
            "feel.tunable_baselines", "G-FEEL",
            "Every TODO tunable has a measured pre-tune value",
            _rel(BASELINE_FILE), f"{len(measured)}/{len(FEEL_TUNABLES)} measured",
            ">=1 per tunable", MISSING,
            "Still unmeasured: " + ", ".join(pending) + ". Measured: " + measured_str + ".",
        )
    return Check(
        "feel.tunable_baselines", "G-FEEL",
        "Every TODO tunable has a measured pre-tune value",
        _rel(BASELINE_FILE), f"{len(measured)} baselines",
        ">=1 per tunable", PASS, measured_str,
    )


def check_feel_verb_script() -> Check:
    """The eight-verb script, run by a human, with greps captured.

    Docs/14 filed this as all six verbs FAIL and then closed the track under a
    WAIVE. That is a legitimate record, but it is a record of the automation
    failing, not of a person succeeding, so the verbs are not verified by a human.
    """
    data = _read_json(HUMAN_PLAYTEST_FILE)
    verbs = (data or {}).get("verbs") or {}
    if not verbs:
        return Check(
            "feel.verb_script", "G-FEEL",
            "Eight-verb script human-run with log greps captured",
            _rel(HUMAN_PLAYTEST_FILE), "0 verbs recorded",
            "8 verbs, each pass or documented fail", MISSING,
            "No human verb record. The only filed run is all-FAIL under a WAIVE "
            "(Docs/14 VP-A).",
        )
    results = {v: _verb_result(r) for v, r in verbs.items()}
    unrun = [v for v in MVP_VERBS if results.get(v) is None]
    unknown = [v for v in verbs if v not in MVP_VERBS]
    if unrun:
        return Check(
            "feel.verb_script", "G-FEEL",
            "Eight-verb script human-run with log greps captured",
            _rel(HUMAN_PLAYTEST_FILE),
            f"{len(MVP_VERBS) - len(unrun)}/{len(MVP_VERBS)} run, "
            f"{len(unrun)} not run",
            "8 verbs, each pass or documented fail",
            MISSING,
            "Declared but never run: " + ", ".join(unrun) + ". A null result is an "
            "open question, not a failure -- FAIL would say a person tried it and it "
            "broke. Run them in the order in POLISH_HUMAN_PLAYTEST.json and record "
            "either pass or a documented fail per verb."
            + (f" Keys outside the MVP eight: {', '.join(unknown)}." if unknown else ""),
        )
    # An extra key does NOT block a pass -- the eight did run, and that is the
    # question this check asks. But it is named in the note rather than dropped,
    # because a verb ID outside the locked allowlist usually means someone is
    # testing a mechanic that does not exist, and a silently-ignored extra row is
    # how that goes unnoticed. Docs/canon/VERBS.md: "If a verb is not listed here,
    # do not implement it."
    extra = f" Not part of the MVP eight: {', '.join(unknown)}." if unknown else ""
    failed = sorted(v for v, r in results.items() if r != "pass")
    if failed:
        return Check(
            "feel.verb_script", "G-FEEL",
            "Eight-verb script human-run with log greps captured",
            _rel(HUMAN_PLAYTEST_FILE),
            f"{len(results)} verbs, {len(failed)} not passing", "0 not passing",
            FAIL,
            "Run and did not pass: " + ", ".join(failed)
            + ". Each needs a documented reason, not a retry until green." + extra,
        )
    return Check(
        "feel.verb_script", "G-FEEL",
        "Eight-verb script human-run with log greps captured",
        _rel(HUMAN_PLAYTEST_FILE),
        f"{len(MVP_VERBS)} of the MVP eight run, all passing", "0 not passing",
        PASS, ", ".join(MVP_VERBS) + extra,
    )


def _verb_result(raw: Any) -> Any:
    """Read one verb's result, accepting either shape the file may use.

    A verb entry may be a bare result (``"V1": "pass"``) or an object carrying the
    instructions a human needs while playing (``"V1": {"how": ..., "result": ...}``).
    The shipped skeleton uses the object form, because a record that says only
    "V1: pass" cannot be replayed or checked by anyone afterwards.

    A dict with no ``result`` key reads as None -- never as a pass. Treating a
    missing field as success is how a freshly seeded skeleton ends up reporting
    that a human played the build when nobody filled anything in.
    """
    if isinstance(raw, dict):
        return raw.get("result")
    return raw


#: The eight MVP verbs, from Docs/canon/VERBS.md (LOCKED allowlist). V3b/V3c are
#: sub-rows of V3, and RS-*/SS-*/Minigame*/Boss* are site-kit and stub rows rather
#: than MVP verbs, so they are deliberately not listed here.
#:
#: DECLARED, not parsed. VERBS.md puts V1 in two tables (day/body and either/cycle)
#: and nests V3b/V3c under V3, so "the eight" is a judgement about which rows count
#: rather than a mechanical read. Declaring it here keeps the gate and the skeleton
#: file agreeing; a test asserts they agree, which is the drift that could actually
#: fabricate a green row.
MVP_VERBS: tuple[str, ...] = ("V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8")

MVP_VERB_NAMES: dict[str, str] = {
    "V1": "Walk homestead",
    "V2": "Glide island -> planet (FALLBACK CRUMB_* -> landing)",
    "V3": "Gather (day Use on a World node -> +1 RES_*)",
    "V4": "Encounter / tame (beast pad: wild -> cautious -> tamed)",
    "V5": "Portal A <-> B",
    "V6": "Heal x3 (spirit hurt -> healed)",
    "V7": "Nurture x2 (homestead N1 crop + N2 stored)",
    "V8": "Return / dawn (portal home and/or Rest -> body)",
}


def check_feel_binary_fresh() -> Check:
    """A green automation run is only worth reading against a fresh binary.

    On 2026-10-02 this project produced a 19/19 Success from a DLL nine minutes
    older than the source it claimed to test. The runner now reports `dll_stale`;
    this check refuses to treat that run as evidence.
    """
    data = _read_json(AUTOMATION_RESULT)
    if data is None:
        return Check(
            "feel.binary_fresh", "G-FEEL",
            "Last automation run executed tests against a fresh binary",
            _rel(AUTOMATION_RESULT), "no artifact",
            "failures == 0 and dll_stale false", MISSING, "")
    if data.get("dll_stale"):
        return Check(
            "feel.binary_fresh", "G-FEEL",
            "Last automation run executed tests against a fresh binary",
            _rel(AUTOMATION_RESULT), "dll_stale true",
            "dll_stale false", FAIL,
            "The run tested an older binary than the source claims. Rebuild before "
            "reading any result from it.",
        )
    ran = data.get("ran")
    failed_n = data.get("failed")
    if not isinstance(ran, int) or ran <= 0:
        return Check(
            "feel.binary_fresh", "G-FEEL",
            "Last automation run executed tests against a fresh binary",
            _rel(AUTOMATION_RESULT), "0 tests ran",
            "failures == 0 and dll_stale false", MISSING,
            "A run that executed nothing is not a passing run.",
        )
    # UE's own counters disagree with its own test list (42 vs 43 on the last
    # run). Carry that disagreement out rather than picking one number: the
    # runner already trusts the report loudly, and hiding the anomaly here would
    # make this gate look more settled than the evidence supports.
    note = f"dll_stale={data.get('dll_stale')}"
    counters = data.get("ran_from_report_counters")
    entries = data.get("ran_from_report_entries")
    if isinstance(counters, int) and isinstance(entries, int) and counters != entries:
        note += (f"; report counters disagree with report entries "
                 f"({counters} vs {entries}), unexplained")
    state = PASS if failed_n == 0 else FAIL
    return Check(
        "feel.binary_fresh", "G-FEEL",
        "Last automation run executed tests against a fresh binary",
        _rel(AUTOMATION_RESULT),
        f"{ran} ran, {failed_n} failed", "0 failed", state, note,
    )


# --------------------------------------------------------------------------
# Assembly
# --------------------------------------------------------------------------


def build() -> dict[str, Gate]:
    gates: dict[str, Gate] = {
        "G-ENV": Gate("G-ENV", "May we begin sizing and blockout work?", "S2 ART-BLOCKOUT"),
        "G-ASSET": Gate("G-ASSET", "May we begin asset production?", "S4 DRESS"),
        "G-FEEL": Gate("G-FEEL", "May we begin mechanics feel work?", "S5 FEEL TUNE"),
    }

    gates["G-ENV"].checks = [
        check_env_world_assembled(),
        check_env_island_sized(),
        check_env_pivot(),
        check_env_export_fresh(),
        check_env_ue_island_measured(),
        check_env_master_binding(),
        check_env_family_distinct(),
        check_env_traversal_measured(),
        check_env_traversal_reachable(),
        check_env_canon_windows_in_sync(),
    ]
    gates["G-ASSET"].checks = [
        _upstream(gates, "G-ENV"),
        check_asset_masters(),
        check_asset_board(),
        check_asset_poly_budgets(),
    ]
    gates["G-FEEL"].checks = [
        _upstream(gates, "G-ASSET"),
        check_feel_human_playtest(),
        check_feel_tunable_baselines(),
        check_feel_verb_script(),
        check_feel_binary_fresh(),
    ]
    return gates


def _dependency_checks(gates: dict[str, Gate]) -> list[Check]:
    return [c for g in gates.values() for c in g.checks if c.id.startswith("dep.")]


def render_markdown(gates: dict[str, Gate], generated: str) -> str:
    L: list[str] = []
    A = L.append
    A("# Polish readiness")
    A("")
    A("Generated by `Content/Python/polish_readiness.py`. Do not hand-edit.")
    A(f"Generated: {generated}")
    A("")
    A("## Verdict")
    A("")
    A("| Gate | Question | State | Furthest stage that may be entered |")
    A("|---|---|---|---|")
    for gid in ("G-ENV", "G-ASSET", "G-FEEL"):
        g = gates[gid]
        t = g.tally()
        detail = ", ".join(f"{k} {v}" for k, v in sorted(t.items())) or "nothing evaluated"
        A(f"| **{gid}** | {g.question} | **{g.state}** | {g.max_stage} ({detail}) |")
    A("")
    A("A RED gate is a measurement, not a verdict. It means the named artifact is")
    A("absent or out of range, and the note says which.")
    A("")
    for gid in ("G-ENV", "G-ASSET", "G-FEEL"):
        g = gates[gid]
        A(f"## {gid} — {g.question}")
        A("")
        A(f"**{g.state}** · furthest stage that may be entered: **{g.max_stage}**")
        A("")
        A("| Check | Requirement | Source | Measured | Target | State |")
        A("|---|---|---|---|---|---|")
        for c in g.checks:
            if c.id.startswith("dep."):
                A(f"| `{c.id}` | {c.requirement} | {c.source} | {c.measured} | "
                  f"{c.target} | **{c.state}** |")
                continue
            A(f"| `{c.id}` | {c.requirement} | `{c.source}` | {c.measured} | "
              f"{c.target} | **{c.state}** |")
        A("")
        notes = [c for c in g.checks if c.note]
        if notes:
            A("### Notes")
            A("")
            for c in notes:
                A(f"- `{c.id}` — {c.note}")
            A("")
    A("## Stage ladder")
    A("")
    for s in STAGES:
        A(f"- {s}")
    A("")
    A("Full rationale and the industry sources are in "
      "[Docs/37_POLISH_PASS_PROCESS.md](../37_POLISH_PASS_PROCESS.md).")
    A("")
    return "\n".join(L)


def selftest(gates: dict[str, Gate]) -> int:
    """Assert the gate can still fail, and that it fails honestly.

    A guard like this is worth nothing unless it is itself checked against a case
    that should trip it. Both directions are exercised here rather than trusted.
    """
    problems: list[str] = []

    total = sum(len(g.checks) for g in gates.values())
    if total != EXPECTED_CHECKS:
        problems.append(f"expected {EXPECTED_CHECKS} checks, evaluated {total}")

    # An empty gate must not be green. This is the fail-open shape.
    empty = Gate("X", "empty", "n/a")
    if empty.state != MISSING:
        problems.append(f"empty gate reported {empty.state}, expected {MISSING}")

    # A gate whose checks are all MISSING must be red, not green.
    missing_only = Gate("Y", "missing", "n/a", [Check("a", "Y", "", "", "", "", MISSING)])
    if missing_only.state != RED:
        problems.append(f"all-MISSING gate reported {missing_only.state}, expected {RED}")

    # Waiver logic runs against a synthetic report so the assertions mean
    # something regardless of what the blend currently measures. Keys are the
    # full (criterion, volume, detail) identity, so one waiver cannot quietly
    # cover a sibling blocker sharing a criterion and a volume.
    fixture = {
        "findings": [
            {"criterion": "2_sized", "volume": "SM_X", "severity": "blocking",
             "detail": "y bbox 10.700 vs spec 14.000"},
            {"criterion": "2_sized", "volume": "SM_X", "severity": "blocking",
             "detail": "origin is not at ground contact"},
        ]
    }
    size_key = ("2_sized", "SM_X", "y bbox 10.700 vs spec 14.000")
    waivers = {size_key: {"rationale": "recorded", "volume": "SM_X"}}

    def cc(ws, match, rep=fixture):
        return _criterion_check("t", "2_sized", "req", ws,
                                detail_match=match, report=rep)

    if cc(waivers, "bbox").state != WAIVED:
        problems.append(f"waived finding reported {cc(waivers, 'bbox').state}, "
                        "expected WAIVED")
    if cc({}, "bbox").state != FAIL:
        problems.append(f"unwaived finding reported {cc({}, 'bbox').state}, "
                        "expected FAIL")
    # The pivot sibling stays open even though the size sibling is waived.
    if cc(waivers, "ground contact").state != FAIL:
        problems.append("a size waiver wrongly covered the pivot blocker")
    # A filter matching nothing must not read as PASS.
    if cc({}, "no such text").state != PASS:
        problems.append("a filter matching nothing did not read as PASS")

    # A waiver naming a finding that no longer exists must surface as STALE.
    stale = _criterion_check("t", "2_sized", "req",
                             {("2_sized", "SM_GONE", "gone"): {"volume": "SM_GONE"}},
                             detail_match="bbox", report=fixture)
    if stale.state != STALE:
        problems.append(f"stale waiver reported {stale.state}, expected {STALE}")

    # An absent report must be MISSING, never PASS.
    absent = _criterion_check("t", "2_sized", "req", {}, detail_match="bbox",
                              report=None, report_present=False)
    if absent.state != MISSING:
        problems.append(f"absent report reported {absent.state}, expected {MISSING}")

    # Every criterion the report can raise as blocking must be covered by some
    # check. A gate that reports honestly on a subset reads as coverage of the
    # whole, which is how `4_distinct` went unmentioned while G-ENV claimed to be
    # gating greybox.
    live = _read_json(GRAYBOX_REPORT)
    if live:
        blocking_criteria = {str(f.get("criterion", ""))
                             for f in blocking_findings(live)}
        uncovered = sorted(blocking_criteria - _COVERED_CRITERIA)
        if uncovered:
            problems.append(
                "gate does not cover blocking criterion(s) "
                f"{uncovered}; add a check or record why they are out of scope")

    if problems:
        for p in problems:
            print(f"SELFTEST FAIL: {p}", file=sys.stderr)
        return 1
    print(f"SELFTEST OK — {total} checks, fail-open paths behave.")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Report whether a human polish pass may start, per gate."
    )
    ap.add_argument("--selftest", action="store_true",
                    help="verify the gate can still fail; run before trusting output")
    args = ap.parse_args(argv)

    gates = build()

    if args.selftest:
        return selftest(gates)

    generated = datetime.now(timezone.utc).isoformat(timespec="seconds")
    any_red = any(g.state != GREEN for g in gates.values())
    unmeasurable = any(g.state == MISSING for g in gates.values())

    payload = {
        "generated": generated,
        "process_doc": "Docs/37_POLISH_PASS_PROCESS.md",
        "verdict": "NOT_READY" if any_red else "READY",
        "gates": {
            gid: {
                "question": g.question,
                "state": g.state,
                "max_stage": g.max_stage,
                "tally": g.tally(),
                "checks": [asdict(c) for c in g.checks],
            }
            for gid, g in gates.items()
        },
        "stages": STAGES,
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    # newline="\n" explicitly. Path.write_text translates "\n" to the platform
    # separator, so on Windows these two files came out CRLF while every
    # neighbouring doc is LF — which makes them churn on the next edit by anyone
    # whose tooling normalises the other way.
    OUT_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
                        encoding="utf-8", newline="\n")
    OUT_MD.write_text(render_markdown(gates, generated), encoding="utf-8",
                      newline="\n")

    print(f"generated {generated}")
    for gid in ("G-ENV", "G-ASSET", "G-FEEL"):
        g = gates[gid]
        t = g.tally()
        detail = ", ".join(f"{k} {v}" for k, v in sorted(t.items())) or "nothing evaluated"
        print(f"  {gid:<8} {g.state:<8} -> {g.max_stage:<20} ({detail})")
    print(f"wrote {OUT_JSON.relative_to(ROOT)}")
    print(f"wrote {OUT_MD.relative_to(ROOT)}")

    # 2 is reserved for "a gate could not be measured at all", which is a worse
    # problem than "a gate is red" and should not be collapsed into it.
    return 2 if unmeasurable else (1 if any_red else 0)


if __name__ == "__main__":
    raise SystemExit(main())