# Editor–build protocol (automatic)

Builds must not stall because the Unreal Editor is open. This protocol is applied automatically by the tools below; the agent does not assume the user will close the Editor.

## Why this exists

- Building the Editor target (HomeWorldEditor) while the Editor is running fails with **Live Coding** or **Exit code: 6** (module locked).
- Autonomous development has no human to "close the Editor and try again," so closing and retrying must be automatic.

## Protocol (automatic)

1. **Before any C++ build:** If `UnrealEditor.exe` is running, close it (graceful `taskkill`), then wait until the process has exited (up to 90s).
2. **Run the build** (e.g. `Build-HomeWorld.bat`).
3. **If build fails and the failure is Editor-related** (Build-HomeWorld.log contains "Live Coding", "Unable to build while", "Exit code: 6", or Editor/lock wording): Force-close the Editor (`taskkill /f`), wait for exit, then **retry the build once**.
4. **Optional:** If the workflow needs the Editor after the build (e.g. next step uses MCP), launch the Editor and wait for port 55557 after a successful build.

## What to use

| Scenario | Use |
|----------|-----|
| **Agent or script runs a C++ build** | Run **`.\Tools\Safe-Build.ps1`** from project root instead of `Build-HomeWorld.bat`. Safe-Build closes the Editor if running, runs the build, and retries once on Editor-related failure. |
| **Orchestrator (build + scripts + tests)** | Run **`py Content/Python/run_automation_cycle.py`** (without `--no-build`). It now closes the Editor before building and retries once on Editor-related failure. |
| **Only need to close the Editor** | `py Content/Python/run_automation_cycle.py --close-editor` (or Safe-Build.ps1 is not for "close only" — use the Python script). |

## Safe-Build.ps1 options

- **Default:** Close Editor if running → build → on Editor-related failure, force-close and retry once. Exit code = build exit code.
- **`-LaunchEditorAfter`:** After a successful build, if this script had closed the Editor, launch it again and wait for MCP port 55557 (requires `UE_EDITOR` set). Use when the next step needs the Editor (e.g. MCP-driven round).

## Agent instructions

- When you need to **build C++**, run **`.\Tools\Safe-Build.ps1`** (or `py Content/Python/run_automation_cycle.py` with build). Do not run `Build-HomeWorld.bat` directly and then assume the user will close the Editor if it fails.
- If you already use `run_automation_cycle.py` for a full cycle (build + scripts/tests), no change — it now applies the protocol automatically.
- To **open the Editor** for MCP: the loop auto-launches it before the first round when `UE_EDITOR` is set, or use `run_automation_cycle.py --no-build --launch-and-wait`. To **close the Editor** before a build: use `run_automation_cycle.py --close-editor` or let Safe-Build / run_automation_cycle do it.

## References

- KNOWN_ERRORS.md: "Build HomeWorldEditor fails: Live Coding active"
- run_automation_cycle.py: `wait_for_editor_exit`, `force_close_editor`, `build_failure_likely_editor_related`, and build block with auto-close and retry
