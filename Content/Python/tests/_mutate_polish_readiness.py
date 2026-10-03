"""Mutation-check the polish readiness gate: do the tests actually kill fail-open edits?

A guard suite that cannot fail is not a guard. Each mutation below is a plausible
future edit that would make the gate report GREEN without measuring anything.
Each must be killed by the test suite. Any SURVIVED mutation is a hole.

Run: py <this file>   (from repo root)
"""

import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "Content" / "Python" / "polish_readiness.py"
TESTS = ROOT / "Content" / "Python" / "tests" / "test_polish_readiness.py"

MUTATIONS = [
    ("empty gate reads GREEN",
     r"if not self\.checks:\s*\n\s*return MISSING",
     "return GREEN"),
    ("all-MISSING gate reads GREEN",
     r"if any\(c\.state in \(FAIL, MISSING, STALE\) for c in self\.checks\):\s*\n\s*return RED",
     "return GREEN"),
    ("a waiver silently counts as a pass",
     r"\(waived if rec else open_hits\)\.append\(f\)",
     "waived.append(f)"),
    ("a missing artifact reports PASS",
     r"return Check\(cid, \"G-ENV\", requirement, src, \"no artifact\", \"0 findings\",\s*\n\s*MISSING,",
     "return Check(cid, \"G-ENV\", requirement, src, \"no artifact\", \"0 findings\",\n                     PASS,"),
    ("a stale waiver is ignored",
     r'(stale waiver\(s\))", "0 findings",\s*\n\s*STALE,',
     r'\1", "0 findings",\n            PASS,'),
    ("BOM handling regresses to plain utf-8",
     r'encoding=\"utf-8-sig\"\) as fh:', 'encoding="utf-8") as fh:'),
    ("a malformed report is treated as an empty one",
     r"except \(OSError, ValueError\):\s*\n\s*return None",
     "except (OSError, ValueError):\n        return {}"),
    ("traversal bounds become exclusive",
     r"if not \(lo <= float\(val\) <= hi\):",
     "if not (lo < float(val) < hi):"),
    ("an unmeasured traversal reads as zero and passes",
     r"if not isinstance\(val, \(int, float\)\):",
     "if False:"),
]


def run(tests_path: Path) -> tuple[bool, str]:
    """Return (tests_failed, last summary line). `tests_failed` is the kill signal."""
    p = subprocess.run([sys.executable, "-m", "pytest", str(tests_path), "-q"],
                       cwd=ROOT, capture_output=True, text=True)
    out = p.stdout + p.stderr
    failed = p.returncode != 0
    tail = out.strip().splitlines()[-1] if out.strip() else "?"
    # An error during collection is not the same evidence as an assertion
    # failure. A mutation that merely breaks the syntax has not been tested at
    # all - it has been skipped - and counting that as a kill would be the same
    # fail-open mistake this whole harness exists to catch.
    if "error" in tail and "failed" not in tail:
        return False, f"COLLECTION ERROR (not a behavioural kill): {tail}"
    return failed, tail


def _test_source_repointing_at_repo() -> str:
    """Re-point the loaded module's paths back at the real repo.

    The copied script resolves ROOT from its own location, so every repo artifact
    becomes unreachable from the temp copy. Two tests assert against the real
    greybox report, so without this the control would fail on clean source and
    abort — or, if the control were weakened to get past it, the harness would
    silently stop testing coverage.
    """
    src = TESTS.read_text(encoding="utf-8")
    shim = f'''
# --- harness shim: re-point at the real repo -------------------------------
_repo = Path(r"{ROOT.as_posix()}")
pr.ROOT = _repo
pr.GRAYBOX_REPORT = _repo / "Docs" / "qa" / "graybox_spec_report.json"
pr.AUTOMATION_RESULT = _repo / "Saved" / "automation_run_result.json"
pr.WAIVERS_FILE = _repo / "Docs" / "qa" / "polish_waivers.json"
pr.BASELINE_FILE = _repo / "Docs" / "qa" / "POLISH_BASELINE.json"
pr.ASSET_BOARD_FILE = _repo / "Docs" / "qa" / "POLISH_ASSET_BOARD.json"
pr.TRAVERSAL_BUDGET = _repo / "Docs" / "qa" / "TRAVERSAL_BUDGET.json"
pr.HUMAN_PLAYTEST_FILE = _repo / "Docs" / "qa" / "POLISH_HUMAN_PLAYTEST.json"
pr.FEEL_CANON = _repo / "Docs" / "canon" / "FEEL.md"
pr.MASTERS_DIR = _repo / "Content" / "HomeWorld" / "Materials" / "Masters"
pr.EXPORT_MANIFEST = _repo / "AssetCreation" / "Exports" / "MVP_EXPORT_MANIFEST.md"
# --- end shim ---------------------------------------------------------------
'''
    anchor = "_spec.loader.exec_module(pr)"
    if anchor not in src:
        raise SystemExit("harness shim: import anchor not found in the test module")
    return src.replace(anchor, anchor + "\n" + shim)


def main() -> int:
    original = SRC.read_text(encoding="utf-8")
    test_src = _test_source_repointing_at_repo()
    survivors: list[str] = []

    with tempfile.TemporaryDirectory() as td:
        tdir = Path(td)
        mut_src = tdir / "polish_readiness.py"
        mut_tests = tdir / "test_polish_readiness.py"

        # Control: the unmutated copy must pass, or "killed" proves nothing.
        mut_src.write_text(original, encoding="utf-8")
        rel = mut_src.as_posix()
        mut_tests.write_text(
            test_src.replace('ROOT / "Content" / "Python" / "polish_readiness.py"',
                             f'Path(r"{rel}")'),
            encoding="utf-8")
        failed, tail = run(mut_tests)
        if failed:
            print(f"{'CONTROL (unmutated)':<52} {'UNEXPECTED FAIL':<20} {tail}")
            print("\nCONTROL FAILED - the suite does not pass on clean source, so a "
                  "mutation being killed would mean nothing.")
            return 2
        print(f"{'CONTROL (unmutated)':<52} {'PASS':<20} {tail}")

        for name, pattern, replacement in MUTATIONS:
            new, n = re.subn(pattern, replacement, original)
            if n == 0:
                survivors.append(f"{name} (PATTERN DID NOT MATCH - mutation not applied)")
                print(f"{name:<52} {'NOT APPLIED':<20} pattern did not match")
                continue
            mut_src.write_text(new, encoding="utf-8")
            killed, tail = run(mut_tests)
            verdict = "killed" if killed else "SURVIVED"
            if not killed:
                survivors.append(name)
            print(f"{name:<52} {verdict:<20} {tail[:60]}")

    print()
    if survivors:
        print(f"SURVIVED {len(survivors)} mutation(s):")
        for s in survivors:
            print(f"  - {s}")
        return 1
    print(f"all {len(MUTATIONS)} fail-open mutations killed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())