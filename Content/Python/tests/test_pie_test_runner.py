# test_pie_test_runner.py
# PythonAutomationTest: validates pie_test_runner check result contract (shape and types).
# Runs without PIE. Discovered by Editor: Tools > Test Automation.

import os
import sys

# Allow importing pie_test_runner from Content/Python
_script_dir = os.path.dirname(os.path.abspath(__file__))
_content_python = os.path.normpath(os.path.join(_script_dir, ".."))
if _content_python not in sys.path:
    sys.path.insert(0, _content_python)

import pie_test_runner
import importlib
importlib.reload(pie_test_runner)

REQUIRED_KEYS = ("name", "passed", "detail")


def test_check_pie_active_returns_result_shape():
    """pie_test_runner check functions return dict with name, passed, detail."""
    result = pie_test_runner.check_pie_active()
    assert isinstance(result, dict), "check_pie_active should return a dict"
    for key in REQUIRED_KEYS:
        assert key in result, "check result must have key %r" % key
    assert isinstance(result["name"], str), "name must be string"
    assert isinstance(result["passed"], bool), "passed must be bool"
    assert isinstance(result["detail"], str), "detail must be string"


def test_run_checks_returns_summary_and_checks_list():
    """run_checks() returns dict with summary, all_passed, checks (list of result dicts)."""
    # Use a single check (no PIE required) so shape is stable in Editor Test Automation
    result = pie_test_runner.run_checks(checks=[pie_test_runner.check_pie_active])
    assert isinstance(result, dict), "run_checks should return a dict"
    assert "summary" in result, "run_checks must have summary"
    assert "all_passed" in result, "run_checks must have all_passed"
    assert "checks" in result, "run_checks must have checks"
    assert isinstance(result["summary"], str), "summary must be string"
    assert isinstance(result["all_passed"], bool), "all_passed must be bool"
    assert isinstance(result["checks"], list), "checks must be a list"
    for item in result["checks"]:
        assert isinstance(item, dict), "each check result must be a dict"
        for key in REQUIRED_KEYS:
            assert key in item, "check result must have key %r" % key
