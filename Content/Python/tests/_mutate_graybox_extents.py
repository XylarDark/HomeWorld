"""Mutation-verify test_graybox_containment_extents.py.

Two directions, because the invariant has two failure modes and a one-sided check
misses half of them:

    HALF-READING  the data are treated as already-halved, so the box is too tight
                   and a module sitting comfortably inside gets flagged.
    LOOSENED      someone widens the box so the flagging stops, and now nothing
                   outside the assembly is caught either.

The suite is a matched pair, so both are scored against the test that names the
failure, and a mutation that only trips the other half is reported as such rather
than counted as a kill.

Run standalone:

    python Content/Python/tests/_mutate_graybox_extents.py

Same three traps as _mutate_graybox_aliases.py: a regex matching nothing is a
HARNESS BUG and not a survivor; survival is read from the run and never assumed.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
TEST = os.path.join(HERE, "test_graybox_containment_extents.py")
READER = os.path.join(REPO, "Content", "Python", "graybox_spec_reader.py")

_HALF_X = r"        half_x = ASSEMBLY_FOOTPRINTS\.get\(volume\.assembly, \(4\.0, 4\.0\)\)\[0\] \* 0\.5"

# (name, regex, replacement, test expected to fail, expected_outcome)
#
# The two failure modes need opposite edits, and getting them the wrong way round
# is easy: `* 0.5` is what makes the box SMALLER, so deleting it widens the
# containment check rather than tightening it. The first version of M1 did exactly
# that - named "box twice too tight", actually doubled the box - and killed the
# wrong half of the pair. The data edit below is the real "reader trusted the
# comment" failure; the `* 1.0` edit is the "loosened constant" failure.
MUTATIONS = [
    (
        "M1: the footprint data are corrected to half-extents (box too tight)",
        r'    "SM_Island_Hero": \(21\.0, 14\.0\),',
        '    "SM_Island_Hero": (10.5, 7.0),',
        "test_a_module_inside_the_island_footprint_is_not_flagged",
        "killed",
    ),
    (
        "M2: the containment box is doubled so nothing outside is ever caught",
        _HALF_X,
        "        half_x = ASSEMBLY_FOOTPRINTS.get(volume.assembly, (4.0, 4.0))[0] * 1.0",
        "test_a_module_outside_the_island_footprint_is_still_flagged",
        "killed",
    ),
    (
        "M3: POSITION_TOLERANCE_M is dropped from the containment comparison",
        r"        outside_x = abs\(actual_origin\[0\] - ax\) > half_x \+ POSITION_TOLERANCE_M",
        "        outside_x = abs(actual_origin[0] - ax) > half_x",
        None,
        "survivor",
    ),
]


def _run_suite():
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", TEST, "-q", "--no-header",
         "-p", "no:cacheprovider"],
        cwd=REPO, capture_output=True, text=True,
    )
    return proc.returncode, proc.stdout + proc.stderr


SURVIVOR_NOTES = {
    "M3": (
        "The tolerance is 0.25 m and the fixture points sit 0.75 m clear of the "
        "boundary on both sides, so dropping it moves nothing. It is deliberate "
        "that no test pins the exact tolerance value: a test that did would fail "
        "whenever the tolerance is retuned, and a retuned tolerance is a normal "
        "edit. The boundary tests use points chosen to stay correct across any "
        "sane tolerance, which is what makes them about the halving."
    ),
}


def main():
    backup = tempfile.mkdtemp(prefix="mutate_extents_")
    shutil.copy2(READER, os.path.join(backup, "reader.py"))
    original = open(READER, "r", encoding="utf-8").read()

    try:
        code, out = _run_suite()
        if code != 0:
            print("HARNESS BUG: the suite is not green before mutating.")
            print(out[-3000:])
            return 1
        print("baseline: suite green\n")

        killed = survived = 0
        for name, pattern, replacement, test, expected in MUTATIONS:
            mutated, count = re.subn(pattern, replacement, original)
            if count != 1:
                print("HARNESS BUG: %s\n  regex matched %d times, expected 1"
                      % (name, count))
                return 1

            with open(READER, "w", encoding="utf-8") as handle:
                handle.write(mutated)

            code, out = _run_suite()
            # Greedy \S* so the capture is the LAST :: segment, which is the test
            # name in both layouts pytest emits:
            #   bare function : file.py::test_name
            #   unittest      : file.py::ClassName::test_name
            # The previous `[^\s:]*::(\w+)` captured the class instead of the method
            # for unittest modules, so a mutation that DID kill the expected test was
            # scored as a survivor - a false "the test no longer bites" reading.
            failed = set(re.findall(r"FAILED \S*::(\w+)", out))
            detected = bool(failed) if test is None else test in failed

            print("%-4s %s" % ("KILLED" if detected else "SURVIVED", name))
            if test:
                print("       expected to kill: %s" % test)
                print("       actually failed : %s"
                      % (", ".join(sorted(failed)) or "(none)"))
            else:
                print("       no test is expected to kill this:")
                print("         %s" % SURVIVOR_NOTES.get(name.split(":")[0], "?"))

            if expected == "killed" and not detected:
                print("       *** HARNESS BUG: expected KILLED, got SURVIVED ***")
                return 1
            if expected == "survivor" and detected:
                print("       *** HARNESS BUG: expected SURVIVOR, got KILLED ***")
                return 1

            killed += detected
            survived += not detected

        print("\n%d killed, %d survived (of %d)" % (killed, survived, len(MUTATIONS)))
        return 0
    finally:
        shutil.copy2(os.path.join(backup, "reader.py"), READER)
        shutil.rmtree(backup, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
