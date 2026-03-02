# Day 3: Placement API + Week 1 playtest — Plan

**Goal:** Complete Day 3 of the 30-day schedule: (1) verify GetPlacementHit / GetPlacementTransform work for build/placement, (2) run the Week 1 playtest (explore → fight → build) and confirm the loop is playable.

**Prerequisite:** Day 2 verified (GAS 3 skills, character, input). See [GAS_SURVIVOR_SKILLS.md](../docs/tasks/GAS_SURVIVOR_SKILLS.md) verification checklist.

**Reference:** [DAY3_PLACEMENT_AND_PLAYTEST.md](../docs/tasks/DAY3_PLACEMENT_AND_PLAYTEST.md), [VISION.md](../docs/workflow/VISION.md), [30_DAY_SCHEDULE.md](../docs/workflow/30_DAY_SCHEDULE.md).

---

## Already done (no rework)

- C++ **BuildPlacementSupport** with GetPlacementHit and GetPlacementTransform (trace from camera, return hit and placement transform).
- **pie_test_runner.py** includes a **Placement API** check that calls the API in PIE.
- **DAY3_PLACEMENT_AND_PLAYTEST.md** written with verification steps and Week 1 playtest checklist.
- Schedule and workflow README link to the Day 3 task doc.

---

## Plan: steps to execute

### Step 1 — Verify placement API (automated)

1. Open the project in Editor; open **DemoMap** (map with ground).
2. Start **Play in Editor (PIE)**.
3. Run **Tools → Execute Python Script** → `Content/Python/pie_test_runner.py` (or MCP: `execute_python_script("pie_test_runner.py")`).
4. Open **Saved/pie_test_results.json**.
5. **Success:** A check named **"Placement API"** exists and **passed** is **true**.  
   **If failed:** Note the **detail** (e.g. "BuildPlacementSupport not found" or "signature not supported"). C++ API is still valid; proceed to optional Blueprint verification in DAY3_PLACEMENT_AND_PLAYTEST.md §1.2, or accept and move to playtest.

**Outcome:** Placement API is verified (automated or Blueprint), or documented as limited from Python only.

---

### Step 2 — Optional: Blueprint placement preview (if you want in-editor feedback)

1. Create a Blueprint (e.g. **BP_PlacementTester**) or add to **BP_HomeWorldCharacter**.
2. On key press (e.g. **P**): call **Get Placement Transform** (Build Placement Support), pass world (e.g. from Get Player Controller → Get World) and Max Distance 10000.
3. If return is true, use **Out Transform** to **Draw Debug Sphere** at impact point or **Spawn Actor** (e.g. small cube) for 1 second then destroy.
4. PIE; press **P** while aiming at ground; confirm preview appears under crosshair.

**Outcome:** Optional; only if you want visible confirmation of placement trace in PIE.

---

### Step 3 — Pre-playtest setup

1. **Map:** DemoMap loaded; optionally run PCG Generate and load World Partition region if you want trees/rocks.
2. **GameMode:** Confirm level uses a GameMode that spawns **BP_HomeWorldCharacter** (or default pawn with GAS).
3. **Abilities:** If unsure, run **Tools → Execute Python Script** → `Content/Python/setup_gas_abilities.py` (idempotent).
4. **Build:** C++ built (e.g. **Build-HomeWorld.bat** with Editor closed). No blocking errors in Output Log on load.

**Outcome:** Level and character are ready for playtest.

---

### Step 4 — Week 1 playtest (in PIE)

Run a short session (2–5 minutes) and confirm:

| Check | Action |
|-------|--------|
| **Explore** | WASD moves, mouse looks; character on ground, no fall-through. |
| **Fight** | Left Mouse = Primary Attack (ability fires); Shift = Dodge. |
| **Interact** | E = Interact (ability fires). |
| **Placement** | If you added Step 2, press P and confirm preview at aim. |
| **Stability** | No crashes; no repeated errors in Output Log. |

**Outcome:** Explore → fight → build loop is playable (movement, attack, dodge, interact, placement API verified).

---

### Step 5 — Close Day 3 and update state

1. In **docs/workflow/30_DAY_SCHEDULE.md**, mark Day 3 items complete: change `- [ ]` to `- [x]` for both bullets.
2. In **docs/workflow/DAILY_STATE.md**:
   - **Yesterday:** Set to what was done this session (e.g. "Day 3: Placement API verified via pie_test_runner; Week 1 playtest (explore/fight/build) completed.").
   - **Today:** Set to Day 4 tasks (from 30_DAY_SCHEDULE).
   - **Tomorrow:** Set to Day 5 preview.
   - **Current day:** Set to **4**.
3. Append a short entry to **docs/SESSION_LOG.md** (date, Day 3 completion, any issues).

**Outcome:** Schedule and daily state reflect Day 3 complete; next session starts on Day 4.

---

## Success criteria (Day 3 complete when)

- [ ] Placement API verified (pie_test_runner **Placement API** pass, or Blueprint test, or documented limitation).
- [ ] Week 1 playtest done: explore, fight (LMB/Shift), interact (E), optional placement (P); no crashes.
- [ ] 30_DAY_SCHEDULE Day 3 checked off; DAILY_STATE and SESSION_LOG updated.

---

## Constraints and references

- **No new C++ or Blueprint content required** for Day 3 unless you add the optional Blueprint preview (Step 2).
- **PCG / 100+ static meshes:** Not required for Day 3; pie_test_runner may still report "PCG actors" fail on empty/small maps — that is optional for this day.
- **VISION gate:** Week 1 playtest validates "first playable loop"; full "crash → scout → boss → claim home" can be placeholder content and is the Week 1 sign-off before Homestead phase.

---

## File reference

| Item | Location |
|------|----------|
| Task doc | docs/tasks/DAY3_PLACEMENT_AND_PLAYTEST.md |
| Placement C++ | Source/HomeWorld/BuildPlacementSupport.h, .cpp |
| PIE tests | Content/Python/pie_test_runner.py |
| Schedule | docs/workflow/30_DAY_SCHEDULE.md |
| Daily state | docs/workflow/DAILY_STATE.md |
| Session log | docs/SESSION_LOG.md |
