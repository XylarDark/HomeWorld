# Run tests and fix failures

Execute the test suite and systematically fix any failures until all pass.

## Steps

1. **Run Python automation tests**
   - In Editor: Tools > Test Automation (runs `Content/Python/tests/test_*.py`).
   - Or via MCP: `execute_python_script("pie_test_runner.py")`, then read `Saved/pie_test_results.json` for PIE validation.
   - Optionally run level-load tests: `test_level_loader.py`, `test_level_pie_flow.py` from Test Automation.

2. **Analyze failures**
   - Categorize: flaky, broken, or new failures.
   - Check if failures relate to recent changes.
   - See `docs/KNOWN_ERRORS.md` for recorded issues in the same area.

3. **Fix one at a time**
   - Address the most critical or blocking failure first.
   - Re-run tests after each fix.
   - Do not change tests themselves unless the test is wrong (e.g. outdated expectation); fix the implementation.

## Success

All selected tests pass. If a test is deferred or skipped, document why (e.g. in SESSION_LOG or the task doc).
