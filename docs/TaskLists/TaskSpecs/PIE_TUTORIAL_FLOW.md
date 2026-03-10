# PIE tutorial flow — single-session verification

**Purpose:** One doc that defines the **PIE verification sequence** for the MVP tutorial (13 steps). Use it in a single PIE session to run the command order and confirm each step. No requirement to automate the full flow in one script; this doc with command sequence and confirmation steps suffices for verification.

**Related:** [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) (Pre-demo verification, all `hw.*` commands); [VERTICAL_SLICE_CHECKLIST.md](workflow/VERTICAL_SLICE_CHECKLIST.md) §3 (step-by-step run sequence); [MVP_TUTORIAL_PLAN.md](workflow/MVP_TUTORIAL_PLAN.md) (13-step loop, List scope).

---

## Prerequisites (before running the sequence)

1. **Open DemoMap** — File → Open Level → `/Game/HomeWorld/Maps/DemoMap` (or Homestead).
2. **Ensure PCG generated** — Select PCG Volume; Generate if needed; no "no surfaces" in Output Log.
3. **Start PIE** — Play; wait for level and pawn ready (~5–10 s).
4. **Optional:** Run `pie_test_runner.py` (MCP or Tools → Execute Python Script) and inspect `Saved/pie_test_results.json` for baseline (Level, Character, PCG). See [CONSOLE_COMMANDS § Reading Saved/pie_test_results.json](../CONSOLE_COMMANDS.md#reading-savedpie_test_resultsjson).

---

## Command sequence and how to confirm each step

Run these in order in one PIE session. **Confirm** = check HUD, Output Log, or (where noted) `pie_test_results.json`.

| Step | Beat | Command(s) | How to confirm |
|------|------|------------|----------------|
| **1** | Wake up in homestead | *(Start PIE; phase is Day by default.)* | HUD **Phase: Day**; player at spawn. Optional: `hw.TimeOfDay.Phase` (no arg) → 0 in Output Log. `pie_test_runner` has DemoMap morning + spawn check. |
| **2** | Have breakfast | **`hw.Meal.Breakfast`** | HUD **Restored today** ≥ 1, **Meals with family: N** (if Family-tagged actors exist), **Love** increased if family present. Set `hw.TimeOfDay.Phase 2` (night) → HUD **Day buff: active**. |
| **3** | Complete one love task with partner | **`hw.LoveTask.Complete`** | HUD **Love: N** increased; Output Log "love tasks today: 1" (or higher). |
| **4** | Play one game with child | **`hw.GameWithChild.Complete`** | HUD **Love: N** increased; Output Log "games with child today: 1". |
| **5** | Collect wood, ore, pick flowers | Harvest: face **BP_HarvestableTree** / **BP_HarvestableOre** / **BP_HarvestableFlower**, press **E**; or stubs: **`hw.Gather.Ore`**, **`hw.Gather.Flowers`** (wood via harvest or place_resource_nodes). Then **`hw.Goods`** | Output Log **"Harvest succeeded (Physical) - Wood +N"** (and Ore/Flowers if harvested); **`hw.Goods`** second line **Wood: N, Ore: N, Flowers: N**. HUD **Physical** count. |
| **6** | Have lunch | **`hw.Meal.Lunch`** (phase must be Day) | HUD **Restored today** ≥ 2 (after breakfast + lunch). |
| **7** | Have dinner | **`hw.Meal.Dinner`** (phase Day) | HUD **Restored today** ≥ 3, **Meals with family: N**. |
| **8** | Go to bed | **`hw.GoToBed`** or **`hw.TimeOfDay.Phase 2`** | HUD **Phase: Night**; optional: **`hw.SpiritBurst`** / **`hw.SpiritShield`** → Output Log "activated"; night encounter Wave 1 in Log. |
| **9** | Spectral self — go out | *(Already at night from step 8.)* **`hw.SpiritBurst`** or **`hw.SpiritShield`** | Output Log ability activation; Log "Night encounter Wave 1 — spawned placeholder". |
| **10** | Combat with encampment | *(Night active.)* | HUD **Wave 1** (or higher); Output Log "Night encounter Wave 1 — spawned placeholder" (Wave 2/3 when triggered). |
| **11** | Beat the boss | **`hw.GrantBossReward`** [*amount*] (e.g. `hw.GrantBossReward 100`) | Output Log "hw.GrantBossReward granted Wood +N"; **`hw.Goods`** or HUD shows Wood. |
| **12** | Night ends | **`hw.AstralDeath`** | HUD **Phase: Dawn** (or Day); player respawned at start. `pie_test_runner` has `check_astral_death`. |
| **13** | Wake up — family taken (tutorial end) | **`hw.TutorialEnd`** or **`hw.FamilyTaken`** | Output Log "Family taken — tutorial complete; inciting incident", "bTutorialComplete set". PlayerState `GetTutorialComplete() == true` (for Act 1 handoff). |

---

## Quick reference: command order only

For copy-paste in console (after PIE is running and phase is Day):

```
hw.Meal.Breakfast
hw.LoveTask.Complete
hw.GameWithChild.Complete
hw.Gather.Ore
hw.Gather.Flowers
hw.Meal.Lunch
hw.Meal.Dinner
hw.GoToBed
hw.SpiritBurst
hw.GrantBossReward 100
hw.AstralDeath
hw.TutorialEnd
```

*(Step 5 wood: harvest a tree with E or ensure trees placed via place_resource_nodes.py; step 9–10: confirm Wave 1 in HUD/Log after hw.GoToBed.)*

---

## Optional: script or partial automation

A script may run a subset of commands via the Editor (e.g. `execute_console_command` or Unreal Python) and parse Output Log or `pie_test_results.json`. This doc does not require full automation; the command sequence and confirmation table above are the verification definition. For automated checks, see `pie_test_runner.py` (e.g. check_astral_death, Love task complete, Game with child complete, Save/Load, GrantBossReward).

---

**See also:** [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § Pre-demo verification (entry point, Tutorial List 2–10 verification); [VERTICAL_SLICE_CHECKLIST.md](workflow/VERTICAL_SLICE_CHECKLIST.md) §3 (step-by-step run sequence); [MVP_TUTORIAL_PLAN.md](workflow/MVP_TUTORIAL_PLAN.md) (13-step loop, List scope).
