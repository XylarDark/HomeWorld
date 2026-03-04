# Automation readiness

**Short answer:** The development environment is set up for programming and testing both inside and outside the Editor. The fully automated 30-day loop is ready to run once the prerequisites below are met. A few gaps (CI doc paths, readiness checklist) were closed so CI passes and "ready to go" is clearly defined.

---

## What is in place

| Area | Status | Notes |
|------|--------|--------|
| **Programming outside Editor** | Ready | C++ build (Build-HomeWorld.bat, RunFullBuild.ps1), host Python (run_ue_automation.py, run_automation_cycle.py), configs in Content/Python. |
| **Programming inside Editor** | Ready | MCP execute_python_script, init_unreal.py on load, Content/Python scripts; manual steps documented where API has no access. |
| **Testing outside Editor** | Ready | run_ue_automation.py (Smoke group; Editor launches and exits); CI validate.yml (lint, JSON, docs, C++ pairing). Optional ci.yml for full build on self-hosted runner. |
| **Testing inside Editor** | Ready | PythonAutomationTest (test_*.py), pie_test_runner.py, validate_assets.py; run via MCP or Tools > Execute Python Script when Editor is open. |
| **Fully automated loop** | Ready | RunAutomationLoop.ps1 + NEXT_SESSION_PROMPT.md + CURRENT_TASK_LIST.md (10-task list). Requires Cursor Agent CLI. The loop auto-launches the Editor before the first round when UE_EDITOR is set; use `-NoLaunchEditor` to skip. See docs/workflow/HOW_TO_GENERATE_TASK_LIST.md. |

---

## Prerequisites to run the loop

These are **not** completed by the repo; you must do them on your machine. Use the task list below and optionally run `.\Tools\Check-AutomationPrereqs.ps1` to verify.

### Before you start — task list

Complete these in order before running the automation loop:

| # | Task | How to complete | Verify |
|---|------|-----------------|--------|
| 1 | **Install Cursor Agent CLI** | **Windows:** In PowerShell run `irm 'https://cursor.com/install?win32=true' | iex`, then **close and reopen your terminal** so PATH is updated. If `agent` is still not found, run the loop with `-AgentPath "C:\path\to\agent.exe"` (see [Cursor CLI docs](https://cursor.com/docs/cli/overview)). | In PowerShell: `agent --version` (or `agent -h`). Should run without "not found". |
| 2 | **Authenticate the CLI** | Run **`agent login`** once in a terminal and complete the browser flow, **or** set the **`CURSOR_API_KEY`** environment variable (get a key from [Cursor Dashboard](https://cursor.com/settings)) for headless/scripted use. | Run `.\Tools\Check-AutomationPrereqs.ps1` or try `agent -p "echo ok"` (should not ask for login if already authenticated). |
| 3 | **Set UE_EDITOR** | Set the environment variable to your UnrealEditor.exe path. Example (PowerShell, current session): `$env:UE_EDITOR = "C:\Program Files\Epic Games\UE_5.7\Engine\Binaries\Win64\UnrealEditor.exe"`. To set permanently: System Properties → Environment Variables → New (user or system) → Name: `UE_EDITOR`, Value: full path to UnrealEditor.exe. | Run `.\Tools\Check-AutomationPrereqs.ps1` (recommended). It uses **Test-UE_EDITORSet** from Tools/Common-Automation.ps1 so the path is never passed when unset. Never call `Test-Path -LiteralPath $env:UE_EDITOR` without a null check; see docs/KNOWN_ERRORS.md. |
| 4 | **Editor for MCP (when needed)** | Set `UE_EDITOR` to UnrealEditor.exe (step 3). The loop **auto-launches** the Editor before the first round when it is not running and waits for MCP (port 55557). Or start the Editor yourself before the loop. Use `-NoLaunchEditor` to run without the Editor. | Editor opens automatically when loop starts (if not already running), or you start it; Cursor MCP connected. |

After all four are done, run `.\Tools\RunAutomationLoop.ps1` from the project root (Editor auto-launches when UE_EDITOR is set; use `-NoLaunchEditor` to skip).

---

## Gaps that were closed (this pass)

- **CI validate.yml** — Required docs were updated to existing files: `docs/workflow/README.md`, `docs/workflow/30_DAY_SCHEDULE.md`, `docs/workflow/MVP_AND_ROADMAP_STRATEGY.md` instead of removed/non-existent `docs/TASKLIST.md` and `ROADMAP.md`, so CI passes.
- **Readiness checklist** — README-Automation.md now has an "Is the environment ready?" section and an "Automation readiness checklist" so you can confirm setup before running the loop.
- **Gaps and limitations** — Documented in README-Automation.md (Editor not auto-started, CI build optional, manual steps for no-API actions).

---

## Rare / one-time human intervention

- **Eliminated by automation (when used):** PCG graph assignment and optional Tag/MeshList params (ApplyPCGSetup commandlet); PCG no-API steps via Editor + auto-clicker ([pcg_apply_manual_steps.py](../Content/Python/gui_automation/pcg_apply_manual_steps.py) with refs from [capture_pcg_refs.py](../Content/Python/gui_automation/capture_pcg_refs.py)); DemoMap creation when `template_level_path` is set in demo_map_config.json (ensure_demo_map creates from template).
- **Editor-driven GUI automation:** You can open the Editor, use an auto-clicker (PyAutoGUI) with reference images to navigate and click the right UI elements in order, and optionally take screenshots to validate. Use this when no API exists or when it is the better solution. See [FULL_AUTOMATION_RESEARCH.md](FULL_AUTOMATION_RESEARCH.md) and the "Editor-driven GUI automation" section in the rare-intervention plan.
- **One-time by design:** UE_EDITOR env, first-time plugin enable/restart, CI self-hosted runner setup.
- **One-time per asset (acceptable unless automated):** AnimGraph structure (per ABP), State Tree structure (per ST), MEC representation mesh in Details—documented in task docs; use Editor + auto-clicker or commandlet when available.

## Remaining limitations (by design)

- The loop auto-launches the Unreal Editor before the first round when `UE_EDITOR` is set and the Editor is not running. Set `UE_EDITOR` to your UnrealEditor.exe path. Use `-NoLaunchEditor` to run without the Editor.
- Full build and UE automation in CI require a self-hosted Windows runner with UE 5.7 (ci.yml).
- Some Editor actions have no Python/MCP API; use the C++ commandlet (e.g. ApplyPCGSetup for graph assignment), Editor + auto-clicker with refs, or one-time manual setup. See docs/PCG_VARIABLES_NO_ACCESS.md and task docs.

See [README-Automation.md](../README-Automation.md) for commands and [docs/AUTOMATION_LOOP_UNTIL_DONE.md](AUTOMATION_LOOP_UNTIL_DONE.md) for loop behavior.
