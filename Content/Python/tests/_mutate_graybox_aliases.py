"""Mutation-verify test_graybox_report_aliases.py.

A test suite that cannot fail is not evidence. Each mutation below breaks ONE
specific guarantee of the alias-rendering fix and asserts the suite notices.

Run standalone:

    python Content/Python/tests/_mutate_graybox_aliases.py

THE THREE TRAPS THIS FILE AVOIDS

Recorded here because each one has already cost a session a false result:

  1. AN UNCOMPILABLE / UNIMPORTABLE MUTATION IS NOT EVIDENCE. If a regex matches
     nothing, the file is unchanged, the suite passes, and the mutation is scored
     a survivor for the wrong reason. Every mutation here must match exactly once
     or the run stops and reports HARNESS BUG.

  2. A MUTATION THAT BREAKS A DIFFERENT GUARANTEE IS NOT A RESULT. Each entry names
     the test it is expected to kill, so a mutation that kills the suite via some
     unrelated assertion is visible in the report rather than hidden in a count.

  3. A SURVIVOR MUST BE STATED, NOT SKIPPED. M5 is expected to survive and says so
     in its own docstring, with the reason. A silently dropped mutation is worse
     than a red one, because it reads as coverage.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
TEST = os.path.join(HERE, "test_graybox_report_aliases.py")
READER = os.path.join(REPO, "Content", "Python", "graybox_spec_reader.py")

# (name, regex, replacement, test expected to fail, expected_outcome)
MUTATIONS = [
    (
        "M1: the renderer stops resolving aliases and reads only the spec name",
        r"    row = measurements\.get\(name\)\n    if row is not None:\n"
        r"        return row, None\n\n    recorded = resolutions\.get\(name\)",
        "    return measurements.get(name), None\n\n    recorded = resolutions.get(name)",
        "test_resolved_spec_name_is_not_reported_absent",
        "killed",
    ),
    (
        "M2: alias halves are no longer filtered out of the rendered rows",
        r"        if name in spec_names or name in alias_only:\n            continue",
        "        if name in spec_names:\n            continue",
        "test_pure_alias_rows_do_not_double_count",
        "killed",
    ),
    (
        "M3: the row stops naming which object it resolved to",
        r'            origin = "%s \(via `%s`\)" % \(origin, resolved_as\)',
        "            pass",
        "test_resolved_spec_name_is_not_reported_absent",
        "killed",
    ),
    (
        "M4: a genuinely missing volume is rendered as present",
        r'            lines\.append\("\| `%s` \| \*\(absent\)\* \| — \|" % name\)',
        '            lines.append("| `%s` | *(non-mesh)* | — |" % name)',
        "test_genuinely_absent_volume_is_still_reported_absent",
        "killed",
    ),
    (
        "M5: run() stops recording what each spec module resolved to",
        r"            alias_resolutions\[volume\.name\] = matched_as\n",
        "",
        None,
        "survivor",
    ),
]


#: Why an expected survivor is a survivor. A mutation that is expected to survive and
#: gives no reason reads as an untested hole, which is the exact thing this file is
#: meant to rule out.
SURVIVOR_NOTES = {
    "M5": (
        "The renderer resolves through VOLUME_ALIASES itself when a report dict has "
        "no `alias_resolutions`, so dropping the recorded value changes the JSON "
        "evidence without changing the rendered table. That redundancy is deliberate: "
        "it is what lets an older report dict still render. The recording is therefore "
        "evidence, not the mechanism, and no unit test can be its killer - it needs "
        "Blender, because `run()` reads the live scene."
    ),
}


def _wrap(text):
    return textwrap.wrap(text, width=88)


def _run_suite():
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", TEST, "-q", "--no-header", "-p", "no:cacheprovider"],
        cwd=REPO,
        capture_output=True,
        text=True,
    )
    return proc.returncode, proc.stdout + proc.stderr


def main():
    backup = tempfile.mkdtemp(prefix="mutate_graybox_")
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
                print("  pattern: %r" % pattern)
                return 1

            with open(READER, "w", encoding="utf-8") as handle:
                handle.write(mutated)

            code, out = _run_suite()
            failed = set(re.findall(r"FAILED [^\s:]*::(\w+)", out))
            # Survival is read from the run, never assumed. A `test is None` entry
            # means "no test is expected to kill this", and the first version of this
            # harness scored that as `detected = True` by definition - which made a
            # declared survivor impossible to record as one, and would have reported
            # any mutation in this file as evidence it did not have.
            detected = bool(failed) if test is None else test in failed

            verdict = "KILLED" if detected else "SURVIVED"
            print("%-4s %s" % (verdict, name))
            if test:
                print("       expected to kill: %s" % test)
                print("       actually failed : %s" % (", ".join(sorted(failed)) or "(none)"))
            else:
                note = SURVIVOR_NOTES.get(name.split(":")[0], "(no reason recorded)")
                print("       no test is expected to kill this:")
                for line in _wrap(note):
                    print("         %s" % line)

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
