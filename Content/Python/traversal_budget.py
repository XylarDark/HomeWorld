# traversal_budget.py
# Host-side script: asks whether the traversal windows in Docs/canon/FEEL.md are
# physically reachable on the island that was actually built.
#
# Run from project root:  py Content/Python/traversal_budget.py
# Reads:  Saved/movement_probe.json       (walk speed, extracted from the character CDO)
#         Docs/qa/graybox_spec_report.json (authored island extents)
#         Docs/canon/FEEL.md               (the windows, parsed - not restated)
# Writes: Docs/qa/TRAVERSAL_BUDGET.json and Docs/qa/TRAVERSAL_BUDGET.md
# Exit:   0 = every window reachable, 1 = a window is not reachable, 2 = could not measure
#
# See Docs/37_POLISH_PASS_PROCESS.md for how this feeds the polish readiness gate.
#
# ---------------------------------------------------------------------------
# WHY THIS SCRIPT IS ARITHMETIC AND NOT A SIMULATION
# ---------------------------------------------------------------------------
#
# The obvious way to answer "is the island the right size?" is to time a walk.
# That needs the game running with World Partition cells streamed in and a pawn
# driven along a route - the desktop, a human, and a route nobody has drawn yet.
# None of that exists, so a timing instrument here would be a number produced by
# nobody's code about a walk nobody took. It would look like evidence.
#
# This script does the part that does not need the desktop, and it is the part
# that catches expensive mistakes early:
#
#     window_seconds x walk_speed  ==  the distance the window demands
#
# A traversal window is a distance budget wearing a stopwatch. Compare that
# distance against the island's authored perimeter and you learn whether the
# window and the geometry can both be true. If they cannot, no amount of play
# testing will reconcile them, and the person about to art-pass the island needs
# to know that BEFORE the art exists rather than after.
#
# What this does NOT establish, stated plainly so the number is not over-read:
#
#   - It uses the STRAIGHT-LINE minimum path length. A real route across uneven
#     ground is longer, so this is a lower bound on the walk and a lower bound on
#     the time. Reachability failures found here are therefore real. Absence of a
#     failure here proves nothing.
#   - It assumes constant walk speed on flat ground. Real traversal is slower
#     uphill, on slopes, and around obstacles. Accelerating from rest and the
#     44.77 deg walkable floor angle are both ignored.
#   - It says nothing about whether the result feels right. See Docs/28_TASTE_GATES.md.
#
# So this is a NECESSARY-CONDITION check, not a performance measurement. It can
# only ever fail the world, never pass it, and the report is worded to match.
#
# A NOTE ON THE PERIMETER MODEL. The island is modelled as an ellipse of the
# authored extents, and its perimeter uses Ramanujan's approximation. That is a
# reasonable shape for an island and a deliberately rough one for a route: it
# answers "how far is it around", not "where does the path go". Any real route
# is longer. The report says "ellipse perimeter", never "the path", because the
# distinction is the whole reason this check is a floor rather than a verdict.
# ---------------------------------------------------------------------------

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "Content" / "Python"))

MOVEMENT_PROBE = ROOT / "Saved" / "movement_probe.json"
GRAYBOX_REPORT = ROOT / "Docs" / "qa" / "graybox_spec_report.json"
FEEL_CANON = ROOT / "Docs" / "canon" / "FEEL.md"
OUT_JSON = ROOT / "Docs" / "qa" / "TRAVERSAL_BUDGET.json"
OUT_MD = ROOT / "Docs" / "qa" / "TRAVERSAL_BUDGET.md"

#: Which authored volume is the walkable island top. Read by name from the
#: greybox report's own measurements, not assumed - the report is the instrument
#: that measured it, and this script consumes that rather than re-deriving.
ISLAND_VOLUME = "SM_IslandTop"

#: Where the DECLARED size lives. Deliberately a different key, and the
#: distinction is not cosmetic.
#:
#: `SM_IslandTop` is the walkable surface mesh and the thing we time a lap around.
#: `SM_Island_Hero` is the assembly ROOT that the spec declares an overall size
#: for, and it is the volume the greybox report files the size and pivot findings
#: against. Asking ASSEMBLY_FOOTPRINTS for `SM_IslandTop` returns None - the
#: first version of this script did exactly that and printed "spec extents: None
#: m" in a table meant to establish credibility, which is worse than omitting it.
#: Root and surface coincide in this model because the island is one slab, so the
#: numbers are comparable; that is an assumption worth stating, not a fact.
SPEC_VOLUME = "SM_Island_Hero"

CM_PER_M = 100.0

REACHABLE = "REACHABLE"
NOT_REACHABLE = "NOT_REACHABLE"
UNMEASURED = "UNMEASURED"


def _read_json(path: Path) -> dict[str, Any] | None:
    """utf-8-sig: UE writes a BOM. See docs/KNOWN_ERRORS.md."""
    try:
        if not path.is_file():
            return None
        with path.open("r", encoding="utf-8-sig") as fh:
            data = json.load(fh)
        return data if isinstance(data, dict) else None
    except (OSError, ValueError):
        return None


def parse_windows(feel_md: str) -> dict[str, tuple[float, float]]:
    """Pull the traversal windows out of the FEEL.md table.

    Parsed rather than restated. FEEL.md owns these numbers; a copy in this file
    would drift silently the first time somebody tuned the window, and the drift
    would show up as this script disagreeing with canon while both looked right.

    Recognises rows of the form ``| Label | ~15-25 s | notes |`` and normalises
    the unicode the file actually uses - en dash, em dash, tilde, or plain hyphen.
    """
    windows: dict[str, tuple[float, float]] = {}
    wanted = {
        "cabin_to_lookout_s": r"cabin\s*(?:->|→|to)\s*lookout",
        "island_circuit_s": r"island\s+circuit",
    }
    for line in feel_md.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        label, value = cells[0], cells[1]
        for key, pattern in wanted.items():
            if key in windows or not re.search(pattern, label, re.I):
                continue
            nums = re.findall(r"\d+(?:\.\d+)?",
                              value.translate(str.maketrans(
                                  {"–": "-", "—": "-", "~": " "})))
            if len(nums) >= 2:
                lo, hi = sorted((float(nums[0]), float(nums[1])))
                windows[key] = (lo, hi)
    return windows


def ellipse_perimeter_m(a_m: float, b_m: float) -> float:
    """Ramanujan's perimeter approximation for an ellipse.

    a_m and b_m are SEMI-axes. The authored bboxes are full extents, and the
    halving here is the one place the script converts between the two
    conventions - ASSEMBLY_FOOTPRINTS in graybox_spec_reader.py documents that
    same relationship, and mixing the two up is the specific error its comment
    warns about.
    """
    a = a_m / 2.0
    b = b_m / 2.0
    if a <= 0 or b <= 0:
        return 0.0
    return math.pi * (3.0 * (a + b) - math.sqrt((3.0 * a + b) * (a + 3.0 * b)))


def build() -> dict[str, Any]:
    out: dict[str, Any] = {
        "generated": None,
        "inputs": {},
        "island": {},
        "windows": {},
        "verdict": None,
        "notes": [],
    }

    # --- walk speed --------------------------------------------------------
    probe = _read_json(MOVEMENT_PROBE)
    walk_cm_s: float | None = None
    if probe is None:
        out["notes"].append(
            f"{MOVEMENT_PROBE.name} absent - run probe_movement_budget.py inside "
            "the editor to extract the walk speed")
    else:
        raw = probe.get("walk_speed_cm_s")
        if isinstance(raw, (int, float)) and raw > 0:
            walk_cm_s = float(raw)
        else:
            out["notes"].append(
                f"{MOVEMENT_PROBE.name} carries no usable walk speed "
                f"(walk_speed_cm_s={raw!r}); its own errors: "
                f"{probe.get('errors')}")
        out["inputs"]["movement_probe_errors"] = probe.get("errors") or []
    out["inputs"]["walk_speed_cm_s"] = walk_cm_s
    out["inputs"]["walk_speed_ms"] = (
        round(walk_cm_s / CM_PER_M, 3) if walk_cm_s else None)

    # --- island geometry ---------------------------------------------------
    report = _read_json(GRAYBOX_REPORT)
    extents: tuple[float, float] | None = None
    if report is None:
        out["notes"].append(f"{GRAYBOX_REPORT.name} absent - cannot read island extents")
    else:
        m = (report.get("measurements") or {}).get(ISLAND_VOLUME)
        if not m or not m.get("bbox"):
            out["notes"].append(
                f"{ISLAND_VOLUME} not in the greybox report measurements")
        else:
            bbox = m["bbox"]
            extents = (float(bbox[0]), float(bbox[1]))
            out["island"]["volume"] = ISLAND_VOLUME
            out["island"]["authored_extents_m"] = [extents[0], extents[1]]
            out["island"]["pivot_is_ground_contact"] = m.get(
                "pivot_is_ground_contact")
            out["island"]["lowest_vert_z_world"] = m.get("lowest_vert_z_world")

    # --- spec size, from the same module the greybox gate uses -------------
    spec: tuple[float, float] | None = None
    try:
        import graybox_spec_reader as gsr  # noqa: PLC0415 - needs sys.path above
        spec = gsr.ASSEMBLY_FOOTPRINTS.get(SPEC_VOLUME)
    except Exception as exc:  # noqa: BLE001
        out["notes"].append(
            f"could not read ASSEMBLY_FOOTPRINTS: {type(exc).__name__}: {exc}")
    if spec is None:
        out["notes"].append(
            f"{SPEC_VOLUME} not in ASSEMBLY_FOOTPRINTS - the declared island size "
            "is unknown, so the authored extents below cannot be compared to spec")
    out["island"]["spec_volume"] = SPEC_VOLUME
    out["island"]["spec_extents_m"] = list(spec) if spec else None

    if extents:
        perim = ellipse_perimeter_m(extents[0], extents[1])
        out["island"]["ellipse_perimeter_m"] = round(perim, 1)
        if walk_cm_s:
            out["island"]["seconds_per_lap_walked"] = round(
                perim / (walk_cm_s / CM_PER_M), 1)

    # --- windows -----------------------------------------------------------
    windows: dict[str, tuple[float, float]] = {}
    if not FEEL_CANON.is_file():
        out["notes"].append(f"{FEEL_CANON.name} absent - no canon to check against")
    else:
        windows = parse_windows(FEEL_CANON.read_text(encoding="utf-8-sig"))
        for needed in ("cabin_to_lookout_s", "island_circuit_s"):
            if needed not in windows:
                out["notes"].append(
                    f"could not parse '{needed}' from FEEL.md - the gate needs it "
                    "and this script will not invent a window")

    # A window's SHAPE decides how it may be tested. A point-to-point journey and
    # a closed loop are different claims with different necessary conditions, and
    # testing them with the same comparison produces confident nonsense.
    #
    # The first version of this script compared every window's implied path length
    # against the island's ellipse perimeter and called the result "arithmetic,
    # not an opinion". For cabin->lookout that is simply the wrong comparison: a
    # 150 m path across a 19 m island means crossing it about eight times, which
    # is an ordinary winding route rather than a contradiction. It reported
    # NOT_REACHABLE and would have sent someone to re-cut a window that was fine.
    #
    #   POINT_TO_POINT - a path can be longer than the island without limit; it can
    #     weave. There is no upper bound from size alone, so the only defensible
    #     statement is the implied distance and how many crossings of the island's
    #     long axis it requires. Nothing here can fail.
    #
    #   CLOSED_LOOP - a circuit returns to its start, so its length is bounded by
    #     the perimeter. This is where size CAN contradict a window, and it is the
    #     only shape this script may declare NOT_REACHABLE.
    WINDOW_SHAPE = {
        "cabin_to_lookout_s": "POINT_TO_POINT",
        "island_circuit_s": "CLOSED_LOOP",
    }

    long_axis_m = extents[0] if extents else None
    perim = out["island"].get("ellipse_perimeter_m")
    worst: list[str] = []
    verdict = REACHABLE

    for key, (lo, hi) in windows.items():
        row: dict[str, Any] = {"window_s": [lo, hi],
                               "shape": WINDOW_SHAPE.get(key, "UNKNOWN")}
        if not walk_cm_s:
            row.update(state=UNMEASURED,
                       note="walk speed unmeasured; the window has no denominator")
            worst.append(key)
            out["windows"][key] = row
            continue

        demand_lo = lo * walk_cm_s / CM_PER_M
        demand_hi = hi * walk_cm_s / CM_PER_M
        row["implied_path_length_m"] = [round(demand_lo, 1), round(demand_hi, 1)]
        if perim:
            row["lap_walk_time_s"] = out["island"].get("seconds_per_lap_walked")
        if long_axis_m:
            row["crossings_of_long_axis_floor"] = round(demand_lo / long_axis_m, 1)

        shape = row["shape"]
        if shape == "POINT_TO_POINT":
            row["state"] = REACHABLE
            row["note"] = (
                f"needs {demand_lo:.0f}-{demand_hi:.0f} m of path, roughly "
                f"{demand_lo / long_axis_m:.0f}-{demand_hi / long_axis_m:.0f} "
                f"crossings of the island's {long_axis_m:.0f} m long axis. A "
                "winding route can satisfy this; island size does not contradict it")
        elif shape == "CLOSED_LOOP":
            row["laps_needed_for_window_floor"] = (
                round(demand_lo / perim, 1) if perim else None)
            if perim and demand_lo > perim:
                row["state"] = NOT_REACHABLE
                row["note"] = (
                    f"even the window's FLOOR ({lo:g} s) needs {demand_lo:.0f} m, but "
                    f"one lap of the island is {perim:.0f} m - "
                    f"{demand_lo / perim:.1f} laps. A circuit that winds is no longer "
                    "a circuit; one number here is wrong")
                verdict = NOT_REACHABLE
                worst.append(key)
            else:
                row["state"] = REACHABLE
                row["note"] = (
                    f"one lap is {perim:.0f} m / "
                    f"{out['island'].get('seconds_per_lap_walked')} s walked, so the "
                    f"{lo:g}-{hi:g} s window needs about "
                    f"{demand_lo / perim:.1f}-{demand_hi / perim:.1f} laps")
        else:
            row["state"] = UNMEASURED
            row["note"] = "no declared shape; this script will not guess one"
            worst.append(key)

        out["windows"][key] = row

    if verdict == REACHABLE and worst:
        verdict = UNMEASURED
    out["verdict"] = verdict
    out["windows_failing"] = worst
    if walk_cm_s and extents:
        out["notes"].append(
            "Necessary-condition check on a straight-line lower bound. A "
            "NOT_REACHABLE is real and needs a human ruling on which number is "
            "wrong. Every REACHABLE here is unfalsified by design - it means "
            "size does not contradict the window, not that the walk fits it.")
    return out


def render_md(data: dict[str, Any], generated: str) -> str:
    L: list[str] = []
    A = L.append
    A("# Traversal budget")
    A("")
    A("Generated by `Content/Python/traversal_budget.py`. Do not hand-edit.")
    A(f"Generated: {generated}")
    A("")
    A("## Verdict")
    A("")
    A(f"**{data['verdict']}**")
    A("")
    if data["verdict"] == NOT_REACHABLE:
        A("At least one canon window cannot be reached on the authored island. This")
        A("is arithmetic on measured numbers, not an opinion, and it needs a human")
        A("ruling on which number is wrong - see the note under each window.")
    elif data["verdict"] == UNMEASURED:
        A("Not measurable yet. The walk speed has not been extracted.")
    else:
        A("Every window is reachable in principle on the authored island. This does")
        A("not mean they are reachable in practice - see the limits below.")
    A("")
    A("## Inputs")
    A("")
    A("| Quantity | Value | Source |")
    A("|---|---|---|")
    ws = data["inputs"].get("walk_speed_ms")
    A(f"| Walk speed | {ws if ws is not None else '**unmeasured**'} m/s "
      f"({data['inputs'].get('walk_speed_cm_s')} cm/s) | character CDO, via "
      f"`probe_movement_budget.py` |")
    ext = data["island"].get("authored_extents_m")
    A(f"| Island extents, authored | {ext} m | `{ISLAND_VOLUME}` in the greybox report |")
    spec = data["island"].get("spec_extents_m")
    spec_txt = f"{spec} m" if spec else "**unknown**"
    A(f"| Island extents, spec | {spec_txt} | `{data['island'].get('spec_volume')}` "
      f"in `ASSEMBLY_FOOTPRINTS` |")
    perim = data["island"].get("ellipse_perimeter_m")
    A(f"| Ellipse perimeter | {perim} m | derived from authored extents |")
    lap = data["island"].get("seconds_per_lap_walked")
    A(f"| Seconds per lap, walked | {lap} s | perimeter / walk speed |")
    A("")
    A("## Windows")
    A("")
    A("| Window | Shape | Canon range | Implied path | State |")
    A("|---|---|---|---|---|")
    for key, row in data["windows"].items():
        imp = row.get("implied_path_length_m")
        A(f"| `{key}` | {row.get('shape', '-')} | "
          f"{row['window_s'][0]:g}-{row['window_s'][1]:g} s | "
          f"{f'{imp[0]:g}-{imp[1]:g} m' if imp else '-'} | "
          f"**{row.get('state', UNMEASURED)}** |")
    A("")
    A("A window's shape decides how it can be tested. A **point-to-point** journey")
    A("can weave indefinitely, so island size cannot contradict it and this script")
    A("never reports it as failing. A **closed loop** returns to its start, so its")
    A("length is bounded by the perimeter - that is the only shape where size and a")
    A("window can genuinely contradict each other.")
    A("")
    notes = [(k, v.get("note")) for k, v in data["windows"].items() if v.get("note")]
    if notes:
        A("### Per-window notes")
        A("")
        for k, n in notes:
            A(f"- `{k}` — {n}")
        A("")
    if data.get("notes"):
        A("### Diagnostics")
        A("")
        for n in data["notes"]:
            A(f"- {n}")
        A("")
    A("## What this does not establish")
    A("")
    A("- It uses a **straight-line lower bound**. Real routes are longer, so every")
    A("  failure reported here is real, and every pass proves nothing.")
    A("- It assumes **constant speed on flat ground**. Real traversal is slower")
    A("  uphill, at corners, and around obstacles.")
    A("- The perimeter is an **ellipse approximation**, not a path.")
    A("- It says nothing about whether a walk would feel good. That is a taste gate.")
    A("")
    A("Full rationale: [Docs/37_POLISH_PASS_PROCESS.md](../37_POLISH_PASS_PROCESS.md)")
    A("")
    return "\n".join(L)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Check FEEL.md traversal windows against the authored island.")
    ap.add_argument("--selftest", action="store_true",
                    help="verify the arithmetic against hand-checked cases")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()

    data = build()
    from datetime import datetime, timezone
    generated = datetime.now(timezone.utc).isoformat(timespec="seconds")
    data["generated"] = generated

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n",
                        encoding="utf-8", newline="\n")
    OUT_MD.write_text(render_md(data, generated), encoding="utf-8", newline="\n")

    print(f"generated {generated}  verdict={data['verdict']}")
    ws = data["inputs"].get("walk_speed_ms")
    print(f"  walk speed      {ws if ws is not None else 'UNMEASURED'} m/s")
    print(f"  island authored {data['island'].get('authored_extents_m')} m"
          f"   perimeter {data['island'].get('ellipse_perimeter_m')} m"
          f"   {data['island'].get('seconds_per_lap_walked')} s/lap")
    for key, row in data["windows"].items():
        print(f"  {key:<22} {row['window_s'][0]:g}-{row['window_s'][1]:g} s  "
              f"{row.get('state', UNMEASURED)}")
    print(f"wrote {OUT_JSON.relative_to(ROOT)}")
    print(f"wrote {OUT_MD.relative_to(ROOT)}")

    if data["verdict"] == UNMEASURED:
        return 2
    return 0 if data["verdict"] == REACHABLE else 1


def selftest() -> int:
    """Pin the arithmetic and the FEEL.md parser.

    The ellipse formula and the extents/semi-axes conversion are the two places
    a plausible-looking edit silently changes every number in the report. Both are
    checked against hand-computable values rather than against a previous run,
    so the test cannot agree with a regression by construction.
    """
    problems: list[str] = []

    # Ramanujan on a circle: semi-axis r -> 2*pi*r. Full extents = diameter.
    for r in (1.0, 5.0, 12.5):
        got = ellipse_perimeter_m(2 * r, 2 * r)
        want = 2 * math.pi * r
        if abs(got - want) > 0.01:
            problems.append(f"circle r={r}: got {got:.4f}, want {want:.4f}")
    # A known ellipse: semi-axes 2,1 -> Ramanujan gives ~9.6884.
    got = ellipse_perimeter_m(4.0, 2.0)
    if abs(got - 9.6884) > 0.001:
        problems.append(f"ellipse 4x2 full extents: got {got:.4f}, want 9.6884")
    # Degenerate input must not divide by zero or go negative.
    if ellipse_perimeter_m(0.0, 5.0) != 0.0:
        problems.append("degenerate extents did not return 0.0")

    # FEEL.md parsing, on the real shapes the file uses.
    sample = (
        "| Cabin → lookout walk | ~15–25 s | V1 |\n"
        "| Island circuit | ~45–90 s | V1 |\n"
        "| Gather channel | ~1.5–3 s | V3 |\n"
    )
    got = parse_windows(sample)
    if got.get("cabin_to_lookout_s") != (15.0, 25.0):
        problems.append(f"cabin window parsed as {got.get('cabin_to_lookout_s')}")
    if got.get("island_circuit_s") != (45.0, 90.0):
        problems.append(f"circuit window parsed as {got.get('island_circuit_s')}")
    if "gather_channel_s" in got:
        problems.append("parsed a window that is not traversal")
    # Reversed bounds in the source must be normalised, not propagated.
    rev = "| Island circuit | ~90–45 s | x |\n"
    if parse_windows(rev).get("island_circuit_s") != (45.0, 90.0):
        problems.append("reversed bounds were not normalised")
    # An unparseable window must be absent, never guessed.
    if parse_windows("| Island circuit | TBD | x |\n"):
        problems.append("invented a window from 'TBD'")

    # A point-to-point window must NEVER be reported NOT_REACHABLE on size
    # grounds, however long the implied path. This is the bug that shipped in the
    # first version: it compared a 150 m journey against a 48 m perimeter and
    # declared canon unreachable, which would have sent someone to re-cut a
    # perfectly good window.
    saved = (GRAYBOX_REPORT, FEEL_CANON, MOVEMENT_PROBE)
    import tempfile
    try:
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            (tmp / "graybox_spec_report.json").write_text(json.dumps({
                "measurements": {ISLAND_VOLUME: {
                    "bbox": [19.3, 10.7, 0.45],
                    "pivot_is_ground_contact": False,
                    "lowest_vert_z_world": -0.45}}}), encoding="utf-8")
            (tmp / "movement_probe.json").write_text(
                json.dumps({"walk_speed_cm_s": 600.0, "errors": []}), encoding="utf-8")
            (tmp / "FEEL.md").write_text(
                "| Cabin → lookout walk | ~15–25 s | V1 |\n"
                "| Island circuit | ~45–90 s | V1 |\n", encoding="utf-8")
            globals()["GRAYBOX_REPORT"] = tmp / "graybox_spec_report.json"
            globals()["FEEL_CANON"] = tmp / "FEEL.md"
            globals()["MOVEMENT_PROBE"] = tmp / "movement_probe.json"
            data = build()

        if data["windows"]["cabin_to_lookout_s"]["state"] == NOT_REACHABLE:
            problems.append("point-to-point window reported NOT_REACHABLE on size")
        if data["windows"]["island_circuit_s"]["state"] != NOT_REACHABLE:
            problems.append(
                "closed loop needing 4.7 laps of a 48 m island was not flagged; the "
                "loop bound is the one real necessary condition here")
        if data["verdict"] != NOT_REACHABLE:
            problems.append("overall verdict did not follow the failing loop")
    finally:
        globals()["GRAYBOX_REPORT"], globals()["FEEL_CANON"] = saved[0], saved[1]
        globals()["MOVEMENT_PROBE"] = saved[2]

    # Spec extents must come from the assembly root, not the walkable surface.
    # Looking up ISLAND_VOLUME in ASSEMBLY_FOOTPRINTS returns None and prints
    # "None m" in the credibility table.
    import graybox_spec_reader as _gsr
    if _gsr.ASSEMBLY_FOOTPRINTS.get(SPEC_VOLUME) is None:
        problems.append(f"{SPEC_VOLUME} absent from ASSEMBLY_FOOTPRINTS")
    if SPEC_VOLUME == ISLAND_VOLUME:
        problems.append(
            "spec volume and walkable volume are the same key; the greybox report "
            "files size findings against the assembly root, not the surface mesh")

    if problems:
        for p in problems:
            print(f"SELFTEST FAIL: {p}", file=sys.stderr)
        return 1
    print("SELFTEST OK — ellipse arithmetic and window parsing behave.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
