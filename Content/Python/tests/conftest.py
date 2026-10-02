"""Pytest collection guard for Content/Python/tests.

WHY THIS FILE EXISTS

Running the host-side test suite used to be impossible, which is why individual
files had to be named one at a time. `pytest Content/Python/tests` aborted with an
INTERNALERROR during collection, before a single test ran:

    test_pie_test_runner.py  ->  import pie_test_runner  ->  import unreal
    ModuleNotFoundError: No module named 'unreal'
    SystemExit: 1

`unreal` only exists inside the Unreal Editor, so every Editor-only file in this
directory poisoned the whole host run. Seven files were affected once the first
layer was peeled back - the two PIE harnesses plus five that `import unreal`
directly.

DETECT, DO NOT ENUMERATE

The first version of this file hardcoded the two PIE filenames. That guards
exactly what was known at the time and nothing else, so the next Editor-only test
added would have broken the host suite again in exactly the same way. This version
scans for a module-level `import unreal` instead, which means a new Editor-only
test is handled without anyone remembering to come here.

Two files cannot be caught that way: `test_pie_test_runner.py` and
`test_level_pie_flow.py` import a *sibling script*, which is what imports `unreal`
and calls `sys.exit(1)`. Detecting that statically would need an import graph, so
those two stay listed explicitly with the reason recorded.

NONE OF THESE FILES ARE BROKEN. They are correct, and they are discovered by the
Editor's own PythonAutomationTest plugin (Tools > Test Automation), which runs them
in the process where `unreal` exists. `collect_ignore` affects host pytest only; the
Editor path is untouched.

This is the same class of defect as a geometry volume that no spec names: the check
could not run, so nothing was being checked.
"""

import os
import re

_HERE = os.path.dirname(os.path.abspath(__file__))

#: A module-level `unreal` import. Anchored at column 0 so an import nested inside a
#: function does not disqualify an otherwise host-runnable file.
_MODULE_LEVEL_UNREAL = re.compile(r"^(?:import\s+unreal\b|from\s+unreal\b)", re.MULTILINE)

#: Sibling-import cases: these pull in a script that hard-exits without `unreal`.
#: Listed with the reason because static detection cannot see through the import.
_SIBLING_IMPORT_CASES = {
    "test_pie_test_runner.py": "imports pie_test_runner, which does sys.exit(1) without unreal",
    "test_level_pie_flow.py": "imports pie_test_runner, which does sys.exit(1) without unreal",
}


def _requires_unreal(path):
    """True when importing this module on the host would need the Editor."""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            return bool(_MODULE_LEVEL_UNREAL.search(handle.read()))
    except OSError:
        return False


def _discover():
    ignored = []
    for name in sorted(os.listdir(_HERE)):
        if not name.endswith(".py"):
            continue
        full = os.path.join(_HERE, name)
        if not os.path.isfile(full):
            continue
        if name in _SIBLING_IMPORT_CASES or _requires_unreal(full):
            ignored.append(name)
    return ignored


#: Resolved against THIS file's directory, not the process CWD. pytest is normally
#: invoked from the repo root, so a bare relative name resolves to nothing and the
#: ignore list silently comes out empty - which is what happened the first time,
#: producing a green-looking config that guarded nothing.
collect_ignore = _discover()


def pytest_report_header(config):
    """Make the exclusions visible instead of silent.

    A guard that quietly hides files is indistinguishable from a guard that is
    filtering out real coverage, so the count is printed on every run.
    """
    return "editor-only modules not collected on host: {0}".format(
        ", ".join(collect_ignore) if collect_ignore else "none"
    )


# NOTE: a `test_` function defined here would never run - pytest does not collect
# test functions out of conftest.py. An earlier version of this file had exactly
# that, which meant the guard's self-check was dead code and the guard appeared to
# be checking itself while checking nothing. The real self-check lives in
# test_host_collection.py, which loads this module by path and asserts on it.