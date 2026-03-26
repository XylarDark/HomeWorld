# Reference images setup tutorial — GUI automation

**Purpose:** GUI clicker scripts (PyAutoGUI) locate Editor UI by matching reference PNGs. This tutorial explains how to **capture**, **save into the repo**, and **commit** those ref images so that (1) anyone with the repo can run the clickers without capturing themselves, and (2) we have a single source of truth for "what the UI looks like" when it was last verified.

**Policy:** When we have the ability to interact with the Editor UI automatically, GUI automation is the **default method**; manual is fallback when refs are missing, PyAutoGUI is unavailable, or matching fails. See [GUI_AUTOMATION_WHY_AND_WHEN.md](GUI_AUTOMATION_WHY_AND_WHEN.md) and [.cursor/rules/automation-standards.mdc](.cursor/rules/automation-standards.mdc).

---

## Getting started: add ref images to the repo in three steps

1. **Capture** — On a machine where the Unreal Editor is open and visible, run the capture script for the feature you need (see §4 and §7). Put the Editor in the right state (e.g. portal selected, Details → Level To Open visible), then run e.g. `py Content/Python/gui_automation/capture_portal_refs.py`. PNGs are saved under `Content/Python/gui_automation/refs/`.
2. **Crop (optional but recommended)** — Crop each PNG to just the UI element (e.g. the "Level To Open" field or the "Generate" button) so PyAutoGUI can match reliably. Replace the saved file.
3. **Commit to the repo** — Stage and commit the ref images so everyone (and any host that runs the clickers) can use them without capturing again:
   - `git add Content/Python/gui_automation/refs/`
   - `git commit -m "chore(gui): add ref images for <feature>"`
   - Push. Ref images are **not** in `.gitignore`; the repo is the source of truth.

After that, anyone who clones the repo can run the apply scripts (e.g. `set_portal_level_to_open.py`) on their host with the Editor focused—no per-machine capture needed, as long as resolution/DPI/theme are close enough for matching. If matching fails, fall back to [MANUAL_EDITOR_TUTORIAL.md](MANUAL_EDITOR_TUTORIAL.md).

---

## 1. Why ref images live in the repo

- **Clickers need refs:** Scripts in `Content/Python/gui_automation/` use `pyautogui.locateOnScreen(ref_path)` to find UI elements. Those PNGs must exist where the script expects them.
- **Capture is host-only:** The agent/CI environment usually has no display and no PyAutoGUI. So refs cannot be captured in CI; they are captured once on a machine where the Editor is open and in the right state, then **saved into the repo** so that:
  - Other developers (or the same machine later) can run the clicker without re-capturing.
  - The repo documents "this is the UI state we last validated against."
- **Where they live:** All ref images are under `Content/Python/gui_automation/refs/`, grouped by feature (e.g. `refs/portal/`, `refs/state_tree/`, `refs/new_level/`). These paths are **not** in `.gitignore`; commit them so the repo is self-contained.

---

## 2. Where ref images are stored

| Feature | Ref directory | Capture script | Apply script |
|--------|----------------|----------------|--------------|
| Portal (Level To Open) | `refs/portal/` | `capture_portal_refs.py` | `set_portal_level_to_open.py` |
| PCG (Forest / Planetoid) | `refs/` (root) | `capture_pcg_refs.py` | `pcg_apply_manual_steps.py` |
| State Tree (Night?/Defend) | `refs/state_tree/` | `capture_state_tree_refs.py` | `state_tree_apply_defend_branch.py` |
| State Tree (BUILD branch) | `refs/state_tree_build/` | `capture_state_tree_build_refs.py` | `state_tree_apply_build_branch.py` |
| New Level (File → New Level) | `refs/new_level/` | `capture_new_level_refs.py` | `new_level_from_ui.py` |
| Main menu (WBP_MainMenu) | `refs/wbp_main_menu/` | `capture_wbp_main_menu_refs.py` | `wbp_main_menu_from_ui.py` |
| Landscape (minimal) | `refs/landscape/` | `capture_landscape_refs.py` | `landscape_apply_basic.py` |
| Homestead spawn position | `refs/homestead/` | `capture_homestead_refs.py` | `homestead_plateau_from_ui.py` (optional) |

Run capture scripts **from the project root** with the Editor visible and in the state described for each ref (e.g. portal selected, Details open). Apply scripts also run from project root with the Editor focused.

---

## 3. Recommended environment (consistency and fragility)

Image matching can break when resolution, DPI, or theme changes. To improve reliability and allow refs to be shared:

- **Resolution:** Use a consistent resolution when capturing (e.g. 1920×1080 or your primary dev resolution). Document it in `refs/README.md` or this tutorial so others can match.
- **DPI / display scaling:** Prefer 100% scaling where possible. High DPI can change text/control sizes and break matching.
- **Theme:** Use the same Editor theme (e.g. default) when capturing. Different themes change colors and can affect `locateOnScreen` confidence.
- **Crop refs tightly:** After capture, crop each PNG to **just the UI element** (e.g. the "Level To Open" field, or the "Generate" button). Smaller, distinctive regions match more reliably than full-screen or large panels.
- **Confidence:** Scripts use a confidence value (e.g. 0.8). If matching fails after an engine or theme update, try lowering confidence slightly or re-capturing refs.

When matching fails (resolution/DPI/theme/UE version change), **fall back to manual** steps in [MANUAL_EDITOR_TUTORIAL.md](MANUAL_EDITOR_TUTORIAL.md); the doc makes that explicit.

---

## 4. How to capture refs (per feature)

### 4.1 Portal (Level To Open)

1. Run `place_portal_placeholder.py` in the Editor (or ensure portal exists). Select the portal actor (tag **Portal_To_Planetoid**).
2. In Details, expand **Dungeon** and ensure **Level To Open** is visible.
3. From project root: `py Content/Python/gui_automation/capture_portal_refs.py` (interactive) or `capture_portal_refs.py --auto` for a right-panel crop.
4. Optionally crop the saved image to just the "Level To Open" field; replace `refs/portal/level_to_open_field.png`.

See `Content/Python/gui_automation/refs/portal/README.md`.

### 4.2 PCG (Forest / Planetoid)

1. Open the Editor with the correct context (e.g. ForestIsland_PCG open, or PCG Volume selected in level).
2. From project root: `py Content/Python/gui_automation/capture_pcg_refs.py`.
3. For each ref name, position the Editor as prompted (Details panel, By Tag selector, tag field, mesh list, graph dropdown, Generate button) and press Enter to capture.
4. Optionally crop each PNG to the relevant element. Files go in `refs/` (root under gui_automation).

See `Content/Python/gui_automation/refs/README.md`.

### 4.3 State Tree (Night? / Defend)

1. Open **ST_FamilyGatherer** in the State Tree editor.
2. From project root: `py Content/Python/gui_automation/capture_state_tree_refs.py`. Use `--auto` for a single full-screen shot as `state_tree_editor.png`, or run without `--auto` to capture all refs interactively.
3. For each ref, position the Editor so the described region (add branch, condition IsNight, Defend task, Blackboard IsNight) is visible, then press Enter.
4. Optionally crop each image. Files go in `refs/state_tree/`.

See `Content/Python/gui_automation/refs/state_tree/README.md`.

### 4.4 State Tree (BUILD branch)

1. Open **ST_FamilyGatherer** in the State Tree editor (root or a branch selected where you will add BUILD).
2. From project root: `py Content/Python/gui_automation/capture_state_tree_build_refs.py`.
3. For each ref (add branch, BUILD-related condition/task, Move To, Claim Smart Object, etc.), position the Editor and press Enter.
4. Save to `refs/state_tree_build/`. Optionally crop each PNG.

See `Content/Python/gui_automation/refs/state_tree_build/README.md`.

### 4.5 New Level (File → New Level → Empty Open World)

1. Have the Editor focused with no level needing save, or save the current level first.
2. From project root: `py Content/Python/gui_automation/capture_new_level_refs.py`.
3. Capture: **File** menu open, **New Level** item, **Empty Open World** option, and **Save As** dialog (path field visible). Save to `refs/new_level/`.
4. Crop to the specific menu item or path field for better matching.

See `Content/Python/gui_automation/refs/new_level/README.md`.

### 4.6 Main menu (WBP_MainMenu)

1. Open Content Browser to **Content → HomeWorld → UI** (or where WBP_MainMenu will live). Optionally open an existing WBP_MainMenu for later refs.
2. From project root: `py Content/Python/gui_automation/capture_wbp_main_menu_refs.py`.
3. Capture refs for: right-click **User Interface → Widget Blueprint**, **Class Settings**, **Parent Class** dropdown (HomeWorldMainMenuWidget), Designer **Canvas Panel** / **Vertical Box**, **Button** (x4), and **On Clicked** binding targets (Play, Character, Options, Quit). Save to `refs/wbp_main_menu/`.
4. Crop each to the relevant control. Many refs = many steps; the apply script will skip steps whose ref is missing.

See `Content/Python/gui_automation/refs/wbp_main_menu/README.md`.

### 4.7 Landscape (minimal — open mode / Sculpt)

1. Open a level that has a Landscape (e.g. Planetoid_Pride).
2. From project root: `py Content/Python/gui_automation/capture_landscape_refs.py`.
3. Capture: **Landscape** mode or **Modes** panel with **Landscape** selected, and optionally **Sculpt** tool. Save to `refs/landscape/`.
4. Full terrain sculpting (canyons, erosion, noise) is not practical via ref-based automation; this ref set supports only "focus Landscape" and optionally "click Sculpt." Use manual for real terrain work.

See `Content/Python/gui_automation/refs/landscape/README.md`.

### 4.8 Homestead plateau (spawn position)

1. Open the planetoid level. Select the **Player Start** (or the actor whose position you want to set).
2. In Details, expand **Transform** and ensure **Location** is visible.
3. From project root: `py Content/Python/gui_automation/capture_homestead_refs.py`.
4. Capture the **Location** X/Y/Z fields (or a single ref that includes the first field). Save to `refs/homestead/`.

**Preferred:** Use the config-driven script `place_homestead_spawn.py` (Python/MCP) to place or move the Player Start at coordinates from config; no ref images required. Use the GUI script only when you want to set position via the Details panel.

See `Content/Python/gui_automation/refs/homestead/README.md`.

---

## 5. Committing ref images to the repo

Ref images **should be in the repo** so that GUI automation works for everyone without each person capturing on their own machine.

1. After capturing (and optionally cropping), ensure all new or updated PNGs are under `Content/Python/gui_automation/refs/` (including subdirs: `portal/`, `state_tree/`, `new_level/`, etc.).
2. **Do not** add `refs/` or `refs/*.png` to `.gitignore`. These paths are intended to be committed.
3. Stage and commit:
   - `git add Content/Python/gui_automation/refs/`
   - `git commit -m "chore(gui): add ref images for portal, PCG, state tree, new level, WBP, landscape, homestead"` (adjust message to the features you added).
4. Push so others (and any host that runs the clickers) have the refs. The automation loop does not capture refs; it only **uses** them when the script runs on a machine with a display and PyAutoGUI.

---

## 6. Host-only and fallback

- **Clickers are host-only:** They run only where the Editor is visible and PyAutoGUI is installed. CI/agent environments typically have no display, so they cannot run capture or clicker scripts. Documenting "run this on your machine" is expected.
- **Refs in repo = no per-machine capture:** Once refs are committed, anyone who clones the repo can run the apply scripts on their host without capturing again—as long as their resolution/DPI/theme are close enough for matching to succeed.
- **When matching fails:** If resolution, DPI, theme, or UE version changes and refs no longer match, **fall back to manual** steps in [MANUAL_EDITOR_TUTORIAL.md](MANUAL_EDITOR_TUTORIAL.md). Re-capture refs on the new setup and commit updated PNGs if you want to restore GUI automation for that environment.

---

## 7. Quick reference — capture commands (from project root)

```text
py Content/Python/gui_automation/capture_portal_refs.py [--auto]
py Content/Python/gui_automation/capture_pcg_refs.py
py Content/Python/gui_automation/capture_state_tree_refs.py [--auto]
py Content/Python/gui_automation/capture_state_tree_build_refs.py
py Content/Python/gui_automation/capture_new_level_refs.py
py Content/Python/gui_automation/capture_wbp_main_menu_refs.py
py Content/Python/gui_automation/capture_landscape_refs.py
py Content/Python/gui_automation/capture_homestead_refs.py
```

After capture, optionally crop each PNG to the relevant UI element, then commit under `Content/Python/gui_automation/refs/`.

---

## See also

- [MANUAL_EDITOR_TUTORIAL.md](MANUAL_EDITOR_TUTORIAL.md) — Manual fallback for every step; use when refs are missing or GUI automation fails.
- [GUI_AUTOMATION_WHY_AND_WHEN.md](GUI_AUTOMATION_WHY_AND_WHEN.md) — Policy: GUI automation default when available; manual fallback.
- [AUTOMATION_GAPS.md](AUTOMATION_GAPS.md) — Which gaps have GUI scripts and which remain manual-only.
- `Content/Python/gui_automation/refs/*/README.md` — Per-feature ref lists and capture notes.
