# Editor polish tutorial — Get HomeWorld to a polished MVP state

**Purpose:** One place to implement **outstanding work in the Editor** so the vertical slice reaches a **polished MVP** state: pre-demo verification green, optional one-time manual steps done, and visual/UX polish applied. Use this after the automation runs (e.g. after the twenty-ninth list, run 3 of 4) or when you are ready to focus on in-Editor work.

**Prerequisites:** Project builds (run `Build-HomeWorld.bat` if needed). Unreal Editor 5.7, DemoMap or Homestead as primary level.

---

## Full analysis: what’s done vs what’s outstanding

### What’s done (automation / code)

- **29 full 10-task list cycles** (T1–T10 per list). Core loop (explore → fight → build), day/night & astral, conversion & roles, combat stubs, HUD, SaveGame, night encounters, family spawn/Defend design, homestead-on-planetoid stub, and documentation are in place.
- **Vertical slice locked:** **Moment** = Claim homestead (place with **P**); **Corner** = Homestead compound (DemoMap/Homestead with buildings + PCG).
- **Pre-demo tooling:** Step-by-step run sequence in [VERTICAL_SLICE_CHECKLIST.md](workflow/VERTICAL_SLICE_CHECKLIST.md) §3; [CONSOLE_COMMANDS.md](CONSOLE_COMMANDS.md) for `hw.*` commands and pre-demo entry point; `pie_test_runner.py` → `Saved/pie_test_results.json`; HUD metrics reference in §3.1; demo-readiness checklist in §3.2.
- **MVP polish guidance:** [MVP_GAP_ANALYSIS.md](workflow/MVP_GAP_ANALYSIS.md) §6 “What to do in Editor for polish” (lighting, LOD, asset placement, animation, UX/HUD, stability).

**Rough completion:** ~80% by weighted gap analysis; remaining ~20% is mostly **verification** (one full PIE pass of §3, 2–5 min stability), **optional one-time manual steps** (portal, State Tree Defend), and **in-Editor polish** (lighting, LOD, placement, animation, HUD).

### What’s outstanding (your Editor work)

| Category | What to do | Where it’s documented |
|----------|------------|------------------------|
| **Pre-demo verification** | One full PIE run: open DemoMap, PCG generated, start PIE, run `pie_test_runner.py`, inspect `Saved/pie_test_results.json`, optionally 2–5 min stability. | §3 step-by-step below; [VERTICAL_SLICE_CHECKLIST](workflow/VERTICAL_SLICE_CHECKLIST.md) §3 |
| **Portal → planetoid** (optional) | Set **Level To Open** on the portal actor to the planetoid map (e.g. `Planetoid_Pride`) so overlap opens the planetoid level. | [AUTOMATION_GAPS.md](AUTOMATION_GAPS.md) Gap 1 |
| **State Tree Defend branch** (optional) | Add Night? branch and Defend task to ST_FamilyGatherer so family switches to Defend at night. | [AUTOMATION_GAPS.md](AUTOMATION_GAPS.md) Gap 2 |
| **Lighting** | Lighting pass on DemoMap/Homestead: key light, fill, shadows; time-of-day preview if used. | MVP_GAP_ANALYSIS §6 |
| **LOD** | Check view distance for PCG/meshes; reduce pop-in where needed. | MVP_GAP_ANALYSIS §6 |
| **Asset placement** | Tweak PCG density, exclusion zones, or manual placement for homestead compound and key areas. | MVP_GAP_ANALYSIS §6 |
| **Animation** | Blend times, root motion, transitions in/out of combat or harvest. | MVP_GAP_ANALYSIS §6 |
| **UX / HUD** | HUD layout, readability, wave count, spiritual power, converted count; placeholder text/icons. | MVP_GAP_ANALYSIS §6; §3.1 |
| **Stability** | 2–5 min PIE: play moment + corner, no crash or major hitch; note repro steps for KNOWN_ERRORS. | MVP_GAP_ANALYSIS §6 |
| **Packaged build** (optional) | Run `Package-AfterClose.ps1` with Editor and game closed; document if Stage fails (files in use). | [KNOWN_ERRORS.md](KNOWN_ERRORS.md); STEAM_EA_STORE_CHECKLIST |

---

## Part 1: Pre-demo verification (get §3 green)

This is the single ordered sequence that makes the pre-demo checklist (§3) fully green. Entry point: [CONSOLE_COMMANDS.md](CONSOLE_COMMANDS.md) (Pre-demo verification) links to §3 and the command reference.

### Step-by-step

1. **Open Editor** — Launch Unreal Editor with the HomeWorld project.
2. **Open DemoMap (or Homestead)** — File → Open Level (or Content Browser) and open `/Game/HomeWorld/Maps/DemoMap` or the Homestead map.
3. **Ensure PCG is generated** — In the level, select the PCG Volume (or PCG actor). If needed, run **Generate** per [PCG_SETUP.md](PCG_SETUP.md). In Output Log, confirm there are no “no surfaces” or empty volume messages.
4. **Start PIE** — Click **Play** (or use MCP `start_pie` if connected). Wait until the game window is ready (level loaded, character spawned).
5. **Wait for level/pawn ready** — Allow ~5–10 seconds for level streaming and pawn possession (longer if World Partition is loading).
6. **Run pie_test_runner** — In Editor: **Tools → Execute Python Script** → `Content/Python/pie_test_runner.py`. (Or via MCP: `execute_python_script("pie_test_runner.py")`.) Results are written to **`Saved/pie_test_results.json`**.
7. **Inspect results** — On your machine, open **`Saved/pie_test_results.json`**. Confirm:
   - **Level:** level name, PCG actors present.
   - **Character:** spawned, on ground, capsule.
   - **Moment:** placement API, Place/Harvest if applicable.
   - **Corner:** PCG count (and spot-check in viewport).
   - **SaveGame** (if checks exist): phase, LoveLevel, spiritual power after `hw.Save` / `hw.Load`.
   - **Planetoid / HomesteadLandedOnPlanetoid** (if on planetoid/DemoMap): flag or note in results.
   For how to read each key and check name, see [CONSOLE_COMMANDS.md § Reading Saved/pie_test_results.json](CONSOLE_COMMANDS.md#reading-savedpie_test_resultsjson).
8. **Optional: stability** — Run PIE for 2–5 minutes; confirm no crash or repeated log errors. Spot-check the **Corner** (homestead compound) in the viewport.

### Demo readiness (§3.2)

When the following are done, the slice is **ready to show**:

- **Pre-demo §3 green** — All five §3 items checked (Level, Character, Moment, Corner, Stability) via the sequence above.
- **Moment: Claim homestead** — In PIE, key **P** (Place) spawns a building at cursor; no critical input or visual bugs.
- **Corner: Homestead compound** — Placed buildings, resource nodes, and PCG trees visible; no critical LOD pop-in or lighting artifacts.

Optional: record a 1–3 min clip (Take Recorder, Game Bar, or OBS) per VERTICAL_SLICE_CHECKLIST §4.

---

## Part 2: One-time manual steps (optional)

Do these only if you need **planetoid transition** or **family Defend behavior** for the slice. They are not required for “claim homestead + homestead compound” alone.

### 2.1 Portal: Level To Open (Gap 1)

**When:** You want the player to walk to the portal and open the planetoid level.

**Steps:**

1. Run your usual flow that places the portal (e.g. `ensure_demo_portal.py` or `place_portal_placeholder.py`).
2. In the level, **select the portal actor** (e.g. `HomeWorldDungeonEntrance` or `BP_PortalToPlanetoid`).
3. In **Details**, find **Dungeon** (or the relevant category) and set **Level To Open** to the planetoid map name (e.g. **`Planetoid_Pride`**).
4. Save the level. In PIE, walk to the portal and confirm the planetoid level loads on overlap.

**Alternative:** If you have the GUI automation ref image and PyAutoGUI set up, you can run `Content/Python/gui_automation/set_portal_level_to_open.py` per [AUTOMATION_GAPS.md](AUTOMATION_GAPS.md) Gap 1.

### 2.2 State Tree: Night? and Defend branch (Gap 2)

**When:** You want family agents to switch to Defend behavior at night.

**Steps:**

1. Open **ST_FamilyGatherer** in the State Tree editor (`/Game/HomeWorld/AI/ST_FamilyGatherer`).
2. Ensure the root is a **Selector**. Add a **Night?** branch as the **first** child (highest priority).
3. Set the branch **condition** to read Blackboard **IsNight** (Bool).
4. In that branch, add a **Defend** state with a task (e.g. **Move To** rally point or enemy).
5. In the State Tree **Blackboard**, add **IsNight** (Bool). Wire IsNight from game code (e.g. `UHomeWorldTimeOfDaySubsystem::GetIsNight()`). In PIE you can set night with **`hw.TimeOfDay.Phase 2`**.
6. **Compile** the State Tree and save.
7. **Validate:** PIE, run **`hw.TimeOfDay.Phase 2`** in the console; agents using ST_FamilyGatherer should switch to the Defend branch.

Full detail: [AUTOMATION_GAPS.md](AUTOMATION_GAPS.md) § Gap 2 and [DAY12_ROLE_PROTECTOR.md](tasks/DAY12_ROLE_PROTECTOR.md).

---

## Part 3: Editor polish checklist

Use this after pre-demo verification is green. Order is flexible; a practical order is: **stability first**, then **lighting/LOD and placement**, then **animation and UX** as needed.

### 3.1 Stability

- Run PIE for **2–5 minutes**.
- Play through the **moment** (claim homestead with **P**) and view the **corner** (homestead compound).
- Confirm **no crash** and no repeated errors in Output Log.
- If you see a reproducible hitch or crash, note the steps and add them to [KNOWN_ERRORS.md](KNOWN_ERRORS.md).

### 3.2 Lighting

- Open DemoMap (or Homestead).
- **Key light:** Directional light intensity, rotation, and color for time-of-day feel.
- **Fill / ambient:** Add or adjust fill/ambient so the homestead area reads clearly.
- **Shadows:** Shadow resolution and distance; fix obvious artifacts.
- If you use a **time-of-day** system, do a quick preview at Day/Dusk/Night/Dawn and adjust as needed.

### 3.3 LOD

- Check **view distance** for PCG and key static meshes (trees, rocks, buildings).
- Reduce **pop-in** where obvious (LOD screen size or draw distance).
- Prefer a single pass; only refine further if you notice issues during play.

### 3.4 Asset placement

- **PCG:** Tweak density, exclusion zones, or filters for the homestead compound and approach so the “corner” looks intentional.
- **Manual:** Place or adjust key actors (e.g. buildings, harvestables) so the compound reads as the hero area.
- Keep **create-if-missing, update-in-place**: don’t delete existing content; adjust in place.

### 3.5 Animation

- **Blend times:** Entry/exit of combat or harvest so transitions don’t feel abrupt.
- **Root motion:** If you use root motion, align with movement and camera.
- **Transitions:** In/out of place, harvest, or spirit abilities if they have dedicated animations.

### 3.6 UX / HUD

- **Layout:** Position and size of Phase, Spiritual, Love, Wave, Converted, Restored today, Meals with family, Dawn countdown, Astral HP, SpiritBurst/SpiritShield, day buff.
- **Readability:** Font size, contrast, and background so values are readable in play.
- **Placeholders:** Replace or document any placeholder text or icons; see [VERTICAL_SLICE_CHECKLIST.md §3.1](workflow/VERTICAL_SLICE_CHECKLIST.md) for the HUD metrics reference.

---

## Part 4: Reading Saved/pie_test_results.json

After running **`pie_test_runner.py`**, open **`Saved/pie_test_results.json`** on your machine.

- **`pie_was_running`** — Must be `true` for most checks to be meaningful.
- **`summary`** — e.g. `"25/35 passed"`; quick pass/fail.
- **`all_passed`** — `true` only when every check passed.
- **`checks`** — Array of objects with **name**, **passed**, **detail**. Use **detail** to see why a check failed (e.g. “PIE not running”, “No controlled pawn”).

**Check names** and what they verify (e.g. PIE active, Character spawned, On ground, Placement API, Place flow, Harvest flow, PCG actors, Save/Load persistence, Conversion test, etc.) are listed in [CONSOLE_COMMANDS.md § Reading Saved/pie_test_results.json](CONSOLE_COMMANDS.md#reading-savedpie_test_resultsjson). Use that table to interpret any failing check.

---

## Part 5: Packaged build (optional)

If you want a **packaged executable** for the slice:

1. **Close** Unreal Editor and any running HomeWorld game so no process holds Stage files.
2. Run **`.\Tools\Package-AfterClose.ps1`** (or your project’s packaging script).
3. If **Stage** fails with “files in use” or SafeCopyFile errors, document it in [KNOWN_ERRORS.md](KNOWN_ERRORS.md) and [STEAM_EA_STORE_CHECKLIST.md](workflow/STEAM_EA_STORE_CHECKLIST.md); retry later with everything closed.

Packaging is **not** required for a polished MVP in the Editor; PIE is sufficient for the pre-demo checklist and stability run.

---

## Quick reference

| Goal | Where to look |
|------|----------------|
| Pre-demo run sequence + commands | [CONSOLE_COMMANDS.md](CONSOLE_COMMANDS.md) (Pre-demo verification), [VERTICAL_SLICE_CHECKLIST.md](workflow/VERTICAL_SLICE_CHECKLIST.md) §3 |
| Interpret pie_test_results.json | [CONSOLE_COMMANDS.md § Reading Saved/pie_test_results.json](CONSOLE_COMMANDS.md#reading-savedpie_test_resultsjson) |
| hw.* commands in PIE | [CONSOLE_COMMANDS.md](CONSOLE_COMMANDS.md) (Commands, Key PIE-test usage) |
| Portal Level To Open | [AUTOMATION_GAPS.md](AUTOMATION_GAPS.md) Gap 1 |
| State Tree Defend branch | [AUTOMATION_GAPS.md](AUTOMATION_GAPS.md) Gap 2 |
| What to do in Editor (categories) | [MVP_GAP_ANALYSIS.md](workflow/MVP_GAP_ANALYSIS.md) §6 |
| HUD metrics (which line = which value) | [VERTICAL_SLICE_CHECKLIST.md §3.1](workflow/VERTICAL_SLICE_CHECKLIST.md) |
| Demo readiness sign-off | [VERTICAL_SLICE_CHECKLIST.md §3.2](workflow/VERTICAL_SLICE_CHECKLIST.md) |
| Known errors and workarounds | [KNOWN_ERRORS.md](KNOWN_ERRORS.md) |

---

**See also:** [VERTICAL_SLICE_CHECKLIST.md](workflow/VERTICAL_SLICE_CHECKLIST.md), [MVP_GAP_ANALYSIS.md](workflow/MVP_GAP_ANALYSIS.md), [AUTOMATION_GAPS.md](AUTOMATION_GAPS.md), [CONSOLE_COMMANDS.md](CONSOLE_COMMANDS.md).
