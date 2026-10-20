# quest_tests.py
# Entry point for the in-editor opening quest sweep.
# Run via UnrealMCP: execute_python_script("quest_tests.py")
# Or from the shell: .\Tools\RunTests.ps1 -Quest
#
# The runner is tick-driven. This call arms it and returns; poll
# Saved/quest_tests_status.json for progress and Saved/quest_tests.json
# for the result. A second call while a run is active reports the active
# beat instead of starting another one.

import importlib

import quest_test_runner

if not quest_test_runner.is_running():
    # Unregister a stale tick from a previous session before reloading.
    quest_test_runner.shutdown()
    importlib.reload(quest_test_runner)

quest_test_runner.start()
