# Build and validate (UE 5.7)

Compile the project and optionally run PIE validation. Use when verifying C++, plugin, or engine changes.

## Steps

1. **Close Editor / disable Live Coding**
   - Building while the Editor is running can fail with "Unable to build while Live Coding is active." Close the Editor or turn off Live Coding before building.

2. **Run the build**
   - From project root: `Build-HomeWorld.bat`
   - Check `Build-HomeWorld.log` for completion (look for "Exit code:" at the end). Non-zero exit = fix compile errors before continuing.

3. **Optional: PIE validation**
   - Open Editor, run PIE, then via MCP: `execute_python_script("pie_test_runner.py")`, and read `Saved/pie_test_results.json` for ground contact, character, PCG, etc.

4. **When touching C++ / PCG / plugins**
   - Before or after changes, check [.cursor/rules/unreal-cpp.mdc](../.cursor/rules/unreal-cpp.mdc) (pitfalls table) and [docs/KNOWN_ERRORS.md](../docs/KNOWN_ERRORS.md). See [docs/UE57_TECH.md](../docs/UE57_TECH.md) for the full UE 5.7 tech entry point.

## Success

Build completes with exit code 0. If you ran PIE validation, all requested checks in `pie_test_results.json` pass or are documented as deferred.
