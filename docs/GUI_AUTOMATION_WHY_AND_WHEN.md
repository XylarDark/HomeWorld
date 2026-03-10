# GUI automation: default when available, manual as fallback

**Purpose:** We have tools that click on the Editor UI (PyAutoGUI-based scripts). **Policy:** When we have the ability to interact with the Editor UI automatically, that is the **default method**; manual steps are the fallback when GUI automation is unavailable or fails. This doc explains when to use GUI automation first and why manual is still documented (fallback and steps with no clicker).

---

## Why not always use UI clickers?

### 1. Ref images must be captured once — and we don't ship them

The clicker scripts find UI elements by **matching reference PNGs** to the screen (e.g. "Level To Open" field, "By Tag" dropdown, "Generate" button). Those ref images:

- Must be **captured on a machine where the Editor is open** and the UI is in the right state (e.g. portal selected, Details visible).
- Are **not in the repo** (or were never committed) because: (a) capture runs **host-side** with PyAutoGUI; (b) the agent/CI environment typically has **no display, no Editor, no PyAutoGUI**; (c) someone has to run the capture script once and commit the PNGs if we want them shared.

So the "manual" path is documented as the one that **always works** without requiring ref capture first. The clicker path is **optional**: "capture refs, then run the script."

### 2. Environment: clickers run host-side only

- **Agent/CI:** No Unreal Editor, no visible desktop, often no PyAutoGUI. The automation loop cannot run `set_portal_level_to_open.py` or `pcg_apply_manual_steps.py` there.
- **Your machine:** You can run the clicker scripts with the Editor focused, **after** installing PyAutoGUI (`pip install pyautogui`) and (for first use) capturing the ref images.

So we document manual steps so that **anyone** can complete setup even if they never run the clicker. If you invest in ref capture once, you can use the scripts for repeat runs.

### 3. Every manual step that can be clicker-driven has a GUI script

We have GUI automation for all of the following. Capture ref images once (see [REF_IMAGES_SETUP_TUTORIAL.md](REF_IMAGES_SETUP_TUTORIAL.md)), then run the apply script with the Editor focused.

| Manual task | GUI script | Ref images |
|-------------|------------|------------|
| Portal — Level To Open | `set_portal_level_to_open.py` | `refs/portal/` (capture: `capture_portal_refs.py`) |
| PCG — Get Landscape Data, mesh list, Generate | `pcg_apply_manual_steps.py` | `refs/` (capture: `capture_pcg_refs.py`) |
| State Tree — Night? / Defend branch | `state_tree_apply_defend_branch.py` | `refs/state_tree/` (capture: `capture_state_tree_refs.py`) |
| State Tree — BUILD branch | `state_tree_apply_build_branch.py` | `refs/state_tree_build/` (capture: `capture_state_tree_build_refs.py`) |
| New level (File → New Level → Empty Open World, Save As) | `new_level_from_ui.py` | `refs/new_level/` (capture: `capture_new_level_refs.py`) |
| Main menu (WBP_MainMenu — widget, parent class, four buttons) | `wbp_main_menu_from_ui.py` | `refs/wbp_main_menu/` (capture: `capture_wbp_main_menu_refs.py`) |
| Landscape — open mode / Sculpt (minimal) | `landscape_apply_basic.py` | `refs/landscape/` (capture: `capture_landscape_refs.py`) |
| Homestead plateau (spawn position via Details) | `homestead_plateau_from_ui.py` | `refs/homestead/` (capture: `capture_homestead_refs.py`; preferred: `place_homestead_spawn.py` config-driven, no refs) |

Steps that have **no clicker** (manual only):

- **Full planetoid terrain** (Sculpt / Erosion / Noise / spires) — no image-based way to drive Landscape tools; use [MANUAL_EDITOR_TUTORIAL.md](MANUAL_EDITOR_TUTORIAL.md) §8.
- **Purely creative choices** (e.g. exact homestead plateau placement by eye, paint layers, landmark placement) — designer-only; scripts can place from config, but fine-tuning is manual.

So for everything in the table above, use the GUI script when refs are available; for terrain and creative polish, manual is the only path.

### 4. Fragility

Ref-image matching can break if:

- **Resolution or DPI** changes (laptop vs monitor, scaling).
- **Editor theme or layout** changes (UE version update, different font size).
- **Language** (if any UI text is in the ref image).

When that happens, the script fails to find the element and you fall back to manual. Documenting manual steps ensures there is always a reliable path.

---

## When you *can* use UI clickers

Use them when:

1. You are on a **host** with the Editor open and PyAutoGUI installed.
2. The task has a **script** (portal, PCG, or State Tree Defend).
3. You have **reference images** for that script (captured once per ref README).

### How to enable the clicker path

1. **Install PyAutoGUI** (host): `pip install pyautogui`
2. **Get ref images** — Either capture them yourself (Editor in the right state, run the capture script for that feature), or **use refs already in the repo** if someone has committed them. Full steps: [REF_IMAGES_SETUP_TUTORIAL.md](REF_IMAGES_SETUP_TUTORIAL.md) (capture → crop → commit to repo).
3. **Run the apply script** with the Editor focused, from project root, e.g.:
   - `py Content/Python/gui_automation/set_portal_level_to_open.py`
   - `py Content/Python/gui_automation/pcg_apply_manual_steps.py`
   - `py Content/Python/gui_automation/state_tree_apply_defend_branch.py`
   - (and similarly for `state_tree_apply_build_branch.py`, `new_level_from_ui.py`, `wbp_main_menu_from_ui.py`, `landscape_apply_basic.py`, `homestead_plateau_from_ui.py`)

If refs are in the repo, you do not need to capture; just run the apply script. Manual steps remain the fallback when refs are missing or matching fails.

---

## Summary

| Question | Answer |
|----------|--------|
| **What is the default method for Editor UI steps?** | **GUI automation** when a script exists and refs are available. Use the clicker script first; manual is fallback only when GUI is unavailable or fails. See [.cursor/rules/automation-standards.mdc](../.cursor/rules/automation-standards.mdc) (Editor UI automation as default). |
| **Why document "manual" at all?** | As **fallback** when refs aren't in the repo or captured, PyAutoGUI isn't available, or matching failed. Also for steps with no clicker (full terrain sculpting, purely creative placement). |
| **When should I use the clicker?** | **By default** for any step in the table above when you're on a host with Editor + PyAutoGUI. Use refs from the repo if committed, or capture once per [REF_IMAGES_SETUP_TUTORIAL.md](REF_IMAGES_SETUP_TUTORIAL.md) and commit so others can use them; use manual only if the script isn't runnable or fails. |

See also: [REF_IMAGES_SETUP_TUTORIAL.md](REF_IMAGES_SETUP_TUTORIAL.md) (capture, crop, add refs to repo), [MANUAL_EDITOR_TUTORIAL.md](MANUAL_EDITOR_TUTORIAL.md), [AUTOMATION_GAPS.md](AUTOMATION_GAPS.md), [Content/Python/gui_automation/refs/README.md](../Content/Python/gui_automation/refs/README.md).
