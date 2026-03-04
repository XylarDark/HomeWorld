# Build and validate (UE 5.7)

Compile the project and optionally run PIE validation. Use when verifying C++, plugin, or engine changes.

## Steps

1. **Run the build (Editor–build protocol is automatic)**
   - From project root: **`.\Tools\Safe-Build.ps1`**
   - Safe-Build closes the Editor if running, runs the build, and retries once if the failure was Editor-related (Live Coding / Exit code 6). No manual close required. See [docs/EDITOR_BUILD_PROTOCOL.md](../docs/EDITOR_BUILD_PROTOCOL.md).
   - Check `Build-HomeWorld.log` for completion (look for "Exit code:" at the end). Non-zero exit = fix compile errors before continuing.

3. **Optional: PIE validation**
   - Open Editor, run PIE, then via MCP: `execute_python_script("pie_test_runner.py")`, and read `Saved/pie_test_results.json` for ground contact, character, PCG, etc.

4. **When touching C++ / PCG / plugins**
   - Before or after changes, check [.cursor/rules/unreal-cpp.mdc](../.cursor/rules/unreal-cpp.mdc) (pitfalls table) and [docs/KNOWN_ERRORS.md](../docs/KNOWN_ERRORS.md). See [docs/UE57_TECH.md](../docs/UE57_TECH.md) for the full UE 5.7 tech entry point.

## Success

Build completes with exit code 0. If you ran PIE validation, all requested checks in `pie_test_results.json` pass or are documented as deferred.
