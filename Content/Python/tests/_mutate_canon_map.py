"""Mutation-verify test_canon_map.py.

A test suite that cannot fail is not evidence. Each mutation below breaks ONE
specific guarantee and asserts that the suite notices. Run standalone:

    python Content/Python/tests/_mutate_canon_map.py
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
TEST = os.path.join(HERE, "test_canon_map.py")
MAP = os.path.join(REPO, "Docs", "CANON_MAP.md")
MUSTS = os.path.join(REPO, "Docs", "handoffs", "T0_MECHANIC_INVENTORIES_V1.md")
HEADER = os.path.join(REPO, "Source", "HomeWorld", "HomeWorldCharacter.h")

# (name, file, regex, replacement, tests expected to fail)
MUTATIONS = [
    (
        "M1: #17 reverted to the false negative ('Found: Nothing')",
        MUSTS,
        r"### P1 \u2014 #17 Spirit-stealth \u2014 \*\*CLOSED[^\n]*",
        "### P1 \u2014 #17 Spirit-stealth \u2014 **N** Found: Nothing.",
        "test_m17_stealth_is_never_recorded_as_absent",
    ),
    (
        "M2: #17 row loses its APPROVE stamp",
        MAP,
        r"(\| \*\*#17\*\*[^\n]*?)\*\*CLOSED \u2014 `APPROVE SS-A` 2026-09-21\*\*",
        r"\1**CLOSED**",
        "test_m17_stealth_is_never_recorded_as_absent",
    ),
    (
        "M3: a lookup-table path is pointed at a file that does not exist",
        MAP,
        r"`Docs/VISION_BOARD\.md`",
        "`Docs/VISION_BOARD_TYPO.md`",
        "test_every_path_named_in_the_lookup_table_resolves",
    ),
    (
        "M4: an invented 11th master is named in the map",
        MAP,
        r"(## 2\. If you need X, read Y)",
        r"\1 `M_WaterRiver`",
        "test_lookup_table_names_only_canon_masters_and_resources",
    ),
    (
        "M5: a 7th resource is named in the map",
        MAP,
        r"(## 2\. If you need X, read Y)",
        r"\1 `RES_FERTILIZER`",
        "test_lookup_table_names_only_canon_masters_and_resources",
    ),
    (
        "M6: the soft-latch fail-open's code identifier is renamed out of the map",
        MAP,
        r"bSoftLatch",
        "bLenientFallback",
        "test_soft_latch_is_documented_as_a_defect_not_a_feature",
    ),
    (
        "M7: the SOFT_LATCH_ONLY log tag is dropped from the map",
        MAP,
        r"`SOFT_LATCH_ONLY`",
        "a log tag",
        "test_soft_latch_is_documented_as_a_defect_not_a_feature",
    ),
    (
        "M8: the strict counterpart is renamed, so evidence and courtesy get confused",
        MAP,
        r"SatisfiesFreedomGateStrict",
        "SatisfiesFreedomGate",
        "test_soft_latch_is_documented_as_a_defect_not_a_feature",
    ),
    # --- the two new tests: state agreement + "N while a hook is declared" -------------
    (
        "M9: #2 reverted to the false negative ('**N**') while its hook still exists",
        MAP,
        r"(\| #2 \|[^\n]*?)\*\*Logic done\*\*",
        r"\1**N**",
        "test_no_must_is_recorded_absent_while_a_t0_hook_is_declared",
    ),
    (
        "M10: the must list and the map disagree about #7 (map 'Logic done', heading 'Partial')",
        MUSTS,
        r"(### P1 \u2014 #7 Rune unlock[^\n]*?)\*\*Partial \(logic\), unbuilt \(level\)\*\*",
        r"\1**Partial**",
        "test_found_states_agree_between_map_and_canonical_must_list",
    ),
    (
        "M11: a must loses its heading, which would silently drop it from the comparison",
        MUSTS,
        r"### P2 \u2014 #13 Home portal[^\n]*\n",
        "",
        "test_found_states_agree_between_map_and_canonical_must_list",
    ),
    (
        "M12: every 'T0 #n' marker is renamed out of the header, emptying the declared set",
        HEADER,
        r"T0 #\d+",
        "T0 beat",
        "test_no_must_is_recorded_absent_while_a_t0_hook_is_declared",
    ),
    (
        "M13: #15's map cell downgrades 'Logic done' to 'Partial' against its own heading",
        MAP,
        r"(\| #15 \|[^\n]*?)\*\*Logic done \+ tested\*\*",
        r"\1**Partial**",
        "test_found_states_agree_between_map_and_canonical_must_list",
    ),
]


def run_suite():
    result = subprocess.run(
        [sys.executable, "-m", "pytest", TEST, "-q"],
        cwd=REPO,
        capture_output=True,
        text=True,
    )
    return result.stdout + result.stderr


def main():
    baseline = run_suite()
    if " failed" in baseline or "error" in baseline.lower():
        print("BASELINE IS NOT GREEN - fix the suite before trusting any mutation")
        print(baseline[-2000:])
        return 1
    print("baseline green")

    # Prove each mutation pattern actually matches something before trusting it.
    survivors = []
    for name, path, pattern, replacement, expected in MUTATIONS:
        with open(path, "r", encoding="utf-8") as handle:
            original = handle.read()
        mutated, count = re.subn(pattern, replacement, original)
        if count == 0:
            print(f"  SKIPPED (pattern matched nothing) {name}")
            survivors.append(name)
            continue
        backup = tempfile.mktemp(suffix=".md")
        shutil.copyfile(path, backup)
        try:
            with open(path, "w", encoding="utf-8", newline="") as handle:
                handle.write(mutated)
            output = run_suite()
            if expected in output and " failed" in output:
                print(f"  KILLED   {name}")
            else:
                print(f"  SURVIVED {name}  <-- test is vacuous")
                survivors.append(name)
        finally:
            shutil.copyfile(backup, path)
            os.unlink(backup)

    if survivors:
        print(f"\n{len(survivors)} SURVIVOR(S): the suite does not actually enforce these")
        return 1
    print("\nall mutations killed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())