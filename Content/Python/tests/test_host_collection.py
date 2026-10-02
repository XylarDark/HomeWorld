"""The collection guard reports on itself.

WHY THIS IS A SEPARATE FILE

conftest.py is where the guard lives, but pytest does NOT collect `test_`
functions out of a conftest - they never run. An earlier version of the guard
carried its own self-check as a `test_` function, which meant the guard looked
like it was checking itself while checking nothing at all. Dead assertions are
worse than absent ones, because they are counted when someone counts tests.

So the check lives here, in a file pytest genuinely collects, and it loads
conftest.py by path so it asserts on the real artifact rather than a copy of the
logic.

THE FAILURE BEING GUARDED

`pytest Content/Python/tests` aborted during collection with an INTERNALERROR and
zero tests run:

    test_pie_test_runner.py -> import pie_test_runner -> import unreal
    ModuleNotFoundError: No module named 'unreal'  /  SystemExit: 1

Seven Editor-only files were responsible. Detection is by scanning for a
module-level `import unreal`, not by a hardcoded list, so a newly added
Editor-only test is handled without anyone remembering to update the guard.
"""

import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
CONFTEST = os.path.join(HERE, "conftest.py")

#: Every Editor-only module known to exist in this directory, with why. Two import a
#: sibling script that hard-exits; the rest import `unreal` directly.
EXPECTED_EDITOR_ONLY = {
    "test_character.py": "module-level import unreal",
    "test_input_assets.py": "module-level import unreal",
    "test_level_loader.py": "module-level import unreal",
    "test_level_pie_flow.py": "imports pie_test_runner, which sys.exit(1)s without unreal",
    "test_pcg_forest.py": "module-level import unreal",
    "test_pie_test_runner.py": "imports pie_test_runner, which sys.exit(1)s without unreal",
    "test_project_setup.py": "module-level import unreal",
}


def _load_guard():
    spec = importlib.util.spec_from_file_location("_hw_tests_conftest", CONFTEST)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_every_known_editor_only_module_is_excluded():
    guard = _load_guard()
    excluded = set(guard.collect_ignore)
    missing = sorted(set(EXPECTED_EDITOR_ONLY) - excluded)
    assert not missing, (
        f"Editor-only modules no longer excluded: {missing}. Without them "
        "`pytest Content/Python/tests` aborts during collection and runs nothing. "
        "Update EXPECTED_EDITOR_ONLY only if these files genuinely became host-runnable."
    )


def test_the_exclusion_list_is_not_empty():
    """If detection ever returns nothing, the guard stopped guarding.

    A silently empty ignore list produces a green config that filters out no
    coverage and hides no Editor-only file - the original failure, wearing the
    costume of a fix.
    """
    guard = _load_guard()
    assert len(guard.collect_ignore) >= len(EXPECTED_EDITOR_ONLY), (
        f"guard detected {len(guard.collect_ignore)} Editor-only modules, expected at "
        f"least {len(EXPECTED_EDITOR_ONLY)}. The `import unreal` scan has regressed."
    )


def test_host_runnable_tests_are_not_excluded():
    """The guard must not over-collect: real host coverage has to survive.

    A guard that ignores everything would also 'fix' the collection error, by
    deleting the evidence it was supposed to protect.
    """
    guard = _load_guard()
    excluded = set(guard.collect_ignore)
    for name in ("test_canon_map.py", "test_homeworld_graybox_spec.py"):
        assert name not in excluded, (
            f"{name} runs fine on the host and must be collected; it is being excluded"
        )


def test_guard_is_self_describing():
    """Every exclusion carries a recorded reason, so it can be audited later."""
    guard = _load_guard()
    for name, reason in guard._SIBLING_IMPORT_CASES.items():
        assert reason.strip(), f"{name} is excluded with no recorded reason"