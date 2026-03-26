# Editor launch deep dive: why the Editor may open then close

**Purpose:** When automation launches the Unreal Editor (e.g. via `run_automation_cycle.py --launch-and-wait`) and the Editor appears to open then close, this doc explains likely causes and how to fix or diagnose them.

**Last updated:** 2026-03-09.

---

## 1. Root cause: missing EditorStartupMap (fixed by default)

### What was happening

- **Config:** `Config/DefaultEngine.ini` had `EditorStartupMap=/Game/HomeWorld/Maps/MainMenu.MainMenu`. If the MainMenu map did not exist, the Editor would **exit** with e.g. *"The map specified ... Could not be found. Exiting."*, causing MCP timeout and session failure.

### Current fix (reliable development + main menu on startup)

- **First launch:** `EditorStartupMap` is **DemoMap** in the repo so the Editor always opens (no "map not found" exit).
- **Main menu on startup:** When the Editor loads, `Content/Python/init_unreal.py` runs and calls `ensure_main_menu_map`: if the MainMenu map is missing, it is created from the template (e.g. Homestead). Once MainMenu exists, init_unreal updates `Config/DefaultEngine.ini` to set `EditorStartupMap=MainMenu`, so **the next time you open the project, the Editor opens on the main menu**.
- **GameDefaultMap** remains MainMenu for the game (Play / packaged).

### If you ever see Editor open-then-close again

1. **Capture Editor output:** Check `Saved/Logs/editor_launch_<timestamp>.log` for "Could not be found" or "Exiting".
2. **Ensure EditorStartupMap points to an existing map:** In `Config/DefaultEngine.ini`, set `EditorStartupMap` to `/Game/HomeWorld/Maps/DemoMap.DemoMap` or `/Game/HomeWorld/Maps/Homestead.Homestead`.
3. **Run with -NoLaunchEditor:** Start the Editor yourself, then run `.\Tools\Start-AllAgents-InNewWindow.ps1 -NoLaunchEditor`.

---

## 2. Other possible causes

| Cause | What to check | Fix |
|-------|----------------|-----|
| **Plugin / load failure** | Editor crash logs in `Saved/Logs/` (e.g. `UnrealEditor.log`, crash dumps). | Disable recently added plugins, fix missing modules, or run with minimal plugins. |
| **-UNATTENDED** | We use `-UNATTENDED` to avoid dialogs. It does **not** by itself close the Editor. | If a dialog is required (e.g. EULA, project upgrade), run once without automation and accept; or remove -UNATTENDED for a test run and capture output. |
| **Init script exit** | `Content/Python/init_unreal.py` runs when the Editor loads. It calls `sys.exit(0)` only when `import unreal` fails (i.e. not running inside Editor). | Inside the Editor, `import unreal` succeeds, so init_unreal should not exit the process. If you see otherwise in logs, add a guard or log before any exit. |
| **Out of memory / crash** | Check `Saved/Logs/` for crash or OOM. | Increase RAM, reduce project load, or disable heavy plugins for automation. |

---

## 3. Diagnostics: capturing Editor output

To see why the Editor exited, capture its stdout/stderr when launching:

- **Automation loop:** When you run `Start-AllAgents-InNewWindow.ps1` (or RunAutomationLoop), the loop calls `run_automation_cycle.py --launch-and-wait --capture-editor-log`, so Editor stdout/stderr are written to **`Saved/Logs/editor_launch_<timestamp>.log`**. After a failed run, open the latest file in that folder and search for "Could not be found", "Exiting", "Error", "Fatal", or "crash".
- **Manual run:** To capture when running the cycle script yourself: `python Content/Python/run_automation_cycle.py --no-build --launch-and-wait --capture-editor-log`. Same log path applies.
- **Manual test (no script):** From a command prompt, run:
  ```bat
  "C:\Program Files\Epic Games\UE_5.7\Engine\Binaries\Win64\UnrealEditor.exe" C:\path\to\HomeWorld\HomeWorld.uproject -UNATTENDED
  ```
  (Adjust paths.) Watch the console for the same messages.

---

## 4. References

- [KNOWN_ERRORS.md](KNOWN_ERRORS.md) — "Start-EditorAndWaitForMCP failed (exit 1)" and "Editor launch: missing MainMenu map".
- [AUTOMATION_READINESS.md](AUTOMATION_READINESS.md) — Workaround: open Editor manually, then run with `-NoLaunchEditor`.
- Epic forums: e.g. "The map specified on the commandline '...' Could not be found. Exiting" (Editor exits when startup map is missing).
- Project: `Content/Python/ensure_main_menu_map.py`, `Content/Python/main_menu_config.json`, `Config/DefaultEngine.ini`.
