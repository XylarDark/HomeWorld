# HomeWorld automation

One-command build, test, and cycle orchestration. Use with Cursor and (optionally) in-editor AI Assistant.

## Is the environment ready?

**Programming and testing (outside Editor):** Yes. C++ build (`Build-HomeWorld.bat`, `RunFullBuild.ps1`), host Python (`run_ue_automation.py`, `run_automation_cycle.py`), and CI (`.github/workflows/validate.yml` and optional `ci.yml`) cover repo-level work. Set `UE_EDITOR` for headless test runs.

**Programming and testing (inside Editor):** Yes. With the Editor open and MCP connected, run scripts via MCP (`execute_python_script`), PIE validation (`pie_test_runner.py` → `Saved/pie_test_results.json`), asset validation (`validate_assets.py`), and PythonAutomationTest (Tools > Test Automation). The agent uses these when the cycle involves Editor work.

**Fully automated 30-day loop:** Ready once the checklist below is done. To **start all agents** (Developer + Fixer + Guardian) in one command, use **`.\Tools\Start-AllAgents.ps1`** — it installs the CLI if missing, auto-launches the Editor when `UE_EDITOR` is set, and runs the Watcher so the Fixer and Guardian engage on failure. For the loop only (no watcher), use `.\Tools\Start-AutomationSession.ps1`. Use `-NoLaunchEditor` to skip launching the Editor.

### Automation readiness checklist

- [ ] UE 5.7 installed; project builds (`Build-HomeWorld.bat`).
- [ ] `UE_EDITOR` set (for host scripts and orchestrator).
- [ ] Cursor Agent CLI installed and authenticated (`agent login` or `CURSOR_API_KEY`) for RunAutomationLoop.
- [ ] For loop with Editor tasks: set `UE_EDITOR` to UnrealEditor.exe so the loop can auto-launch the Editor before the first round; or start the Editor yourself. Use `-NoLaunchEditor` to run without the Editor.
- [ ] Required docs and state files exist: `docs/workflow/30_DAY_IMPLEMENTATION_STATUS.md`, `docs/workflow/NEXT_SESSION_PROMPT.md` (created/updated by the agent).

## Commands (run from project root)

| Command | Purpose |
|---------|---------|
| **`.\Tools\Start-AllAgents.ps1`** | **Start the full agent company** — install CLI if needed, auto-launch Editor when UE_EDITOR set, run Developer + Fixer + Guardian via Watcher. One script to put all agents to work. |
| `.\Tools\Safe-Build.ps1` | Build with Editor–build protocol (closes Editor if running, retries on Editor-related failure); use instead of Build-HomeWorld.bat for autonomous runs |
| `.\Tools\RunFullBuild.ps1` | Full build (RunUAT BuildGraph or Build-HomeWorld.bat) |
| `.\Tools\RunFullBuild.ps1 -Clean` | Clean + build |
| `.\Tools\RunFullBuild.ps1 -Platform Win64 -Test` | Build and run editor tests |
| `.\Tools\RunTests.ps1` | Run UE automation tests (Smoke group); requires `UE_EDITOR` env |
| `.\Tools\CleanProject.ps1` | Remove Binaries, Intermediate, DerivedDataCache |
| `.\Tools\CleanProject.ps1 -IncludeSaved -Confirm` | Also remove Saved/Logs; prompt before delete |
| `py Content/Python/run_automation_cycle.py --task N` | Orchestrator: build → scripts (from config) → run_ue_automation; updates CYCLE_STATE |
| `py Content/Python/run_automation_cycle.py --no-build --launch-and-wait` | Start Editor and wait for MCP port 55557 |
| `py Content/Python/run_automation_cycle.py --close-editor` | Gracefully close Editor (taskkill without /f) |
| `.\Tools\Guard-AutomationLoop.ps1` | **Guardian (loop-breaker):** Check logs for a repeating failure loop; if detected, run the Guardian agent to resolve or write Saved/Logs/automation_loop_breaker_report.md. Use -CheckOnly to only detect. Logs to Saved/Logs/guardian.log. |
| `.\Tools\Watch-AutomationAndFix.ps1` | **Watcher:** Run the automation loop; on failure, start the **Fixer**; if the same failure repeats, invoke the **Guardian**. Logs to Saved/Logs/watcher.log. See [docs/AGENT_COMPANY.md](docs/AGENT_COMPANY.md). |
| `.\Tools\Run-RefinerAgent.ps1` | **Refiner:** Read run history and errors; update rules and strategy (KNOWN_ERRORS, .cursor/rules, AGENTS.md) so the same failures don't recur. Run on-demand or after a Guardian report. Logs to Saved/Logs/refiner.log. |
| `.\Tools\Start-AutomationSession.ps1` | **One-command start:** Install Cursor Agent CLI if not on PATH, then run the automation loop. Use when you want to "start an automation session" without manually installing the CLI. |
| `.\Tools\RunAutomationLoop.ps1` | Fully automatic loop: run Cursor agent until all days in 30_DAY_IMPLEMENTATION_STATUS are done (requires Cursor Agent CLI on PATH; see "Cursor Agent CLI" below) |
| `.\Tools\RunAutomationLoop.ps1 -NoLaunchEditor` | Same as above, but do not auto-launch the Editor (run headless or start the Editor yourself). By default the loop auto-launches the Editor when `UE_EDITOR` is set. |

## Daily workflow (Cursor → git push → CI)

1. **In Cursor:** Start automation cycle: "Start automation cycle. Desires: [your goals]." Agent generates CYCLE_TASKLIST, inits CYCLE_STATE, runs first task.
2. **Continue:** Say "Continue" to run the next task or retry.
3. **Headless run:** For script-only tasks, run `py Content/Python/run_automation_cycle.py --task N` (set `UE_EDITOR` and close Editor first).
4. **Git push:** Push to main/master; CI runs (see .github/workflows). validate.yml runs lint and doc checks; ci.yml (if added) can run build/test on a self-hosted runner with UE installed.

## In-editor AI Assistant + Cursor

- **Cursor:** Use for code, scripts, docs, and MCP-driven Editor control (when Editor is open and MCP connected). Start automation cycle from Cursor.
- **In-editor AI Assistant:** Use for quick Editor-only questions and UI steps inside Unreal. For repeatable automation, prefer Cursor + MCP or Python scripts so they are versioned and scriptable.

## Troubleshooting

- **Build fails / Editor in use:** Use **`.\Tools\Safe-Build.ps1`** instead of `Build-HomeWorld.bat`; it closes the Editor if running and retries once on Editor-related failure. See [docs/EDITOR_BUILD_PROTOCOL.md](docs/EDITOR_BUILD_PROTOCOL.md).
- **UE_EDITOR not set:** Set to your UnrealEditor.exe path, e.g. `C:\Program Files\Epic Games\UE_5.7\Engine\Binaries\Win64\UnrealEditor.exe`.
- **RunTests / run_ue_automation fail:** Ensure Editor is closed and `UE_EDITOR` points to the correct engine. Check `Saved/automation_run_result.json` and Build-HomeWorld.log.
- **LFS / large .uasset:** Use `git lfs install` and ensure .uasset/.umap are tracked (see .gitattributes). Pull with LFS before build.
- **RunAutomationLoop: agent exited with -1073740791 / "usage limit for Opus" / "Assertion failed":** The Cursor Agent hit an API usage limit (e.g. Opus) or the CLI crashed. **Fix:** In Cursor settings, switch the default model to a different one (e.g. not Opus), or set a Spend Limit so the agent can continue. Your usage resets on your billing cycle. Then re-run `.\Tools\RunAutomationLoop.ps1`.
- **Terminal crashed but is the agent still running?** Check **Saved/automation_last_activity.json** (recent timestamp = likely still in a round) and **Saved/Logs/automation_loop.log** for progress. In Task Manager, look for **agent** or **node**. To report failures: paste **Saved/Logs/automation_errors.log** into chat so the agent can fix them (or fix them yourself).
- **Refine rules and strategy from runs:** All runs (main, fix, loop-breaker) are recorded in **Saved/Logs/agent_run_history.ndjson**. Use it with automation_errors.log and automation_loop_breaker_report.md to update .cursor/rules, KNOWN_ERRORS.md, and development strategy. See [docs/AUTOMATION_REFINEMENT.md](docs/AUTOMATION_REFINEMENT.md).

## Example Cursor prompts

- "Implement a new gameplay feature using UE 5.7 best practices."
- "Start the automatic development cycle. Desires: Complete Day 7 resource nodes and Day 8 polish from the 30-day schedule."
- "Run full automation cycle for task 1 (headless)."
- "Fix PCG no-access steps: add a GUI automation script or document the one-time manual steps."

## Cursor Agent CLI (for fully automatic loop)

To run the 30-day automation loop without manually pasting "Continue" each session, use the Cursor Agent CLI and the loop-runner script:

1. **Install Cursor Agent CLI** — Follow [Cursor CLI docs](https://cursor.com/docs/cli/overview). On Windows, install per Cursor’s instructions (e.g. from Cursor settings or the install script referenced in the docs).
2. **Authenticate** — Run `agent login` once in a terminal, or set the `CURSOR_API_KEY` environment variable for headless/scripted use. Get an API key from the [Cursor Dashboard](https://cursor.com/settings).
3. **Run the loop** — From project root: `.\Tools\RunAutomationLoop.ps1`. The script reads the prompt from `docs/workflow/NEXT_SESSION_PROMPT.md`, runs the agent with `-p -f --approve-mcps --workspace`, then checks `docs/workflow/30_DAY_IMPLEMENTATION_STATUS.md`; if any day is still `pending`, it runs the agent again. **The Editor is auto-launched** before the first round when `UE_EDITOR` is set; use `-NoLaunchEditor` to skip. See [docs/AUTOMATION_LOOP_UNTIL_DONE.md](docs/AUTOMATION_LOOP_UNTIL_DONE.md).

## First-time / next manual steps

1. Enable plugins in Editor (Edit > Plugins): PythonScriptPlugin, PCG, UnrealMCP, PythonAutomationTest (already in .uproject; confirm enabled).
2. Set `UE_EDITOR` (and optionally `HOMEWORLD_PROJECT`) for host scripts.
3. Run one Python script in Editor (e.g. Tools > Execute Python Script > validate_assets.py) and check `Saved/asset_validation_result.json`.
4. Run `.\Tools\RunTests.ps1` once with Editor closed to verify automation test path.

## Python stubs / autocomplete

For Cursor/VSCode autocomplete of the `unreal` module: use the Python interpreter embedded in UE (see Edit > Editor Preferences > Python) or generate/obtain .pyi stubs for the Unreal Python API and point your IDE to them. Epic does not ship a full .pyi; community stubs or introspection from the Editor can be used.

## Gaps and limitations

- **Editor auto-launch:** The loop auto-launches the Unreal Editor before the first round when `UE_EDITOR` is set and the Editor is not running, then waits for MCP (port 55557). Set `UE_EDITOR` to your UnrealEditor.exe path. Use `-NoLaunchEditor` to run without the Editor (e.g. headless).
- **CI build/test:** Full build and UE automation tests run only when a self-hosted Windows runner with UE 5.7 is configured (ci.yml). validate.yml runs on every push (lint, JSON, docs, C++ pairing) without UE.
- **No-API Editor actions:** PCG graph assignment is automated via the ApplyPCGSetup commandlet (and optional Tag/MeshList params); DemoMap can be created from template when `template_level_path` is set. For Get Landscape Data By Tag and mesh list, use one-time manual setup, or Editor + auto-clicker (pcg_apply_manual_steps.py with refs from capture_pcg_refs.py). See docs/PCG_VARIABLES_NO_ACCESS.md and docs/AUTOMATION_READINESS.md.

## See also

- [docs/AUTOMATION_LOOP_UNTIL_DONE.md](docs/AUTOMATION_LOOP_UNTIL_DONE.md) — Fully automatic loop with Cursor CLI and RunAutomationLoop.ps1.
- [docs/FULL_AUTOMATION_RESEARCH.md](docs/FULL_AUTOMATION_RESEARCH.md) — Orchestrator, GUI automation, cycle state.
- [.cursor/commands/start-automation-cycle.md](.cursor/commands/start-automation-cycle.md) — How to start and continue the cycle.
- [.cursor/rules/19-automation-cycle.mdc](.cursor/rules/19-automation-cycle.mdc) — Cycle steps and loop guards.
