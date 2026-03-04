# Last session audit and MVP basics remaining

**Date:** 2026-03-05 (audit)

---

## 1. Last session audit (recent work)

### Automation / tooling fixes (this chat)

| What | Outcome |
|------|--------|
| **Task list parser** | Fixed: regex used `$` in multiline mode so section blocks stopped at every line end; changed to `\z` (end of string). Pending count was 0 despite 10 pending tasks; now correctly reports T1–T10. |
| **Unicode in RunAutomationLoop** | Fixed: en-dash/em-dash/arrow in strings caused PowerShell parse errors in some environments. Replaced with ASCII hyphen and `->`; used concatenation for interpolated strings with pipes. |
| **Max rounds cap** | Added: loop exits after 10 rounds so it never restarts from T1 when the task list is reset or not persisted. Prevents infinite re-run of same 10 tasks. |
| **Agent stop** | Stopped agent process and (when present) removed automation_loop.lock so a new run can start. |

### Sixth-list automation run (2026-03-04)

- **Run:** Start-AllAgents-InNewWindow; loop ran **10 rounds** (T1 → T10).
- **Per round:** Agent completed task, Safe-Build ran when C++/Build.cs changed, Editor relaunched; round_completed and build_validated logged.
- **After round 10:** Loop saw **“pending tasks remain (10 of 10)”** and started **round 11** on T1 again. Cause: task list file was not updated with `status: completed` for T1–T10 (or was reverted), so the parser still saw 10 pending.
- **Mitigation:** Max-round cap (10) now forces exit after 10 rounds so the plan does not restart indefinitely.

### Seventh list (current)

- **T1:** Completed. Vertical slice pre-demo checklist re-run; outcome documented (Editor/MCP not connected that run; procedure for full run when Editor available is in VERTICAL_SLICE_CHECKLIST §3).
- **T2–T10:** Pending. Next up: **T2 (PIE-with-validation)**.

---

## 2. MVP basics (from VISION and PROTOTYPE_SCOPE)

**MVP:** Smallest playable version that validates the core promise.  
**Vertical slice:** One moment + one corner at showable quality.  
**Gate:** Week 1 playtest = crash → scout → boss → claim home.  
**First playable loop:** Explore → fight → build.

**Locked choices:**

- **Moment:** Claim homestead (place first home with P after exploring/harvesting).
- **Corner:** Homestead compound (DemoMap/Homestead with buildings, resource nodes, PCG).

**Pre-demo checklist (VERTICAL_SLICE_CHECKLIST §3):**

1. **Level:** DemoMap (or Homestead) open; PCG generated.
2. **Character:** BP_HomeWorldCharacter; Enhanced Input; GAS (LMB, Shift, E, P).
3. **Moment:** Claim homestead playable in PIE (place with P works).
4. **Corner:** Homestead compound visible in viewport.
5. **Stability:** PIE 2–5 min without crash.

---

## 3. What’s done vs what’s left for MVP basics

### Done (artifacts and prior cycles)

| Area | Status |
|------|--------|
| **Level + PCG** | DemoMap/Homestead layout; ForestIsland_PCG; create_demo_from_scratch / create_pcg_forest. When Editor is open and PCG generated, checklist “Level” and “PCG” pass. |
| **Character + GAS** | BP_HomeWorldCharacter; Enhanced Input (init_unreal.py); GA_PrimaryAttack, Dodge, Interact, Place. Abilities granted via setup_gas_abilities. |
| **Moment (place)** | GA_Place, TryPlaceAtCursor; BuildPlacementSupport. Place-at-cursor (P) implemented. |
| **Harvest** | BP_HarvestableTree; TryHarvestInFront; GA_Interact. |
| **Pre-demo verification** | Multiple runs; Level + PCG pass when Editor/MCP used. Character/Moment/Corner/Stability require PIE + pie_test_runner; procedure documented; some runs had Editor disconnected so only “outcome documented”. |
| **Automation** | Loop, Watcher, Fixer, Guardian, single-instance guard, heartbeats, task list T1–T10 parsing, max 10 rounds. |

### Left before “all basics for MVP” are complete

| # | Item | How to close |
|---|------|--------------|
| 1 | **Pre-demo checklist with PIE** | With Editor open: open DemoMap, ensure PCG generated, **start PIE**, run `pie_test_runner.py` (MCP or Tools → Execute Python Script), inspect `Saved/pie_test_results.json` for character spawn, on ground, placement API, PCG count. Spot-check corner and 2–5 min stability. Matches **T2 (PIE-with-validation)**. |
| 2 | **Save/Load and Phase 2 in PIE** | Document or verify: `pie_test_runner` check_save_load_persistence and check_time_of_day_phase2 with PIE running; update DAY15 §4 and DAY12 §4. Part of T2. |
| 3 | **Portal DemoMap → planetoid (optional for MVP)** | Set LevelToOpen (Details or set_portal_level_to_open.py + ref image); PIE walk to portal (800,0,100) → planetoid loads. **T3**; AUTOMATION_GAPS Gap 1. |
| 4 | **State Tree Defend/Night (optional for MVP)** | One-time manual or GUI automation (refs) per AUTOMATION_GAPS Gap 2; then PIE + `hw.TimeOfDay.Phase 2` to see Defend. **T4 / T6**. |
| 5 | **SaveGame across PIE restart** | hw.Save, stop PIE, start PIE, hw.Load; or document. **T5**. |
| 6 | **Packaged build or checklist** | Run Package-HomeWorld.bat and smoke-test, or keep STEAM_EA_STORE_CHECKLIST updated (already done in sixth list). **T7**. |
| 7 | **Docs and buffer** | T8–T10: docs polish, AUTOMATION_GAPS update, ACCOMPLISHMENTS + PROJECT_STATE §4 for next list. |

**Strict MVP basics (must-have):** 1 and 2 — one full pass with PIE of the pre-demo checklist and PIE test results (and Save/Load / Phase 2) documented. That gives a verified “explore → fight → build” loop and showable slice.

**Nice-to-have for slice:** 3 (portal), 4 (Defend), 5 (SaveGame persistence), 6 (packaging), 7 (docs/buffer). These can be done in the current seventh list (T2–T10) or carried into the next list.

---

## 4. Current task list (seventh) — quick reference

| Id | Summary | Status |
|----|---------|--------|
| T1 | Re-run vertical slice pre-demo checklist | completed |
| T2 | PIE-with-validation: pie_test_runner with PIE running | pending |
| T3 | Portal LevelToOpen gap: verify or document | pending |
| T4 | State Tree Defend/Night gap: verify or document | pending |
| T5 | SaveGame/Load persistence across PIE restart | pending |
| T6 | Act 2 Defend at home (night phase) validate or doc | pending |
| T7 | Packaged build run or Steam EA checklist update | pending |
| T8 | Docs polish (KNOWN_ERRORS, CONVENTIONS, checklist) | pending |
| T9 | AUTOMATION_GAPS or refinement doc update | pending |
| T10 | Buffer: next list generation prep | pending |

**Next step:** Run agents (`.\Tools\Start-AllAgents-InNewWindow.ps1`) to work through T2–T10, or do **T2 manually**: start PIE, run `pie_test_runner.py`, review `Saved/pie_test_results.json`, and document outcome to close the core MVP basics check.

---

## 5. References

- [CURRENT_TASK_LIST.md](CURRENT_TASK_LIST.md) — full goals and success criteria.
- [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md) — §3 pre-demo checklist and verification notes.
- [PROTOTYPE_SCOPE.md](PROTOTYPE_SCOPE.md) — moment and corner locked.
- [VISION.md](VISION.md) — MVP and vertical slice definitions.
- [AUTOMATION_GAPS.md](../AUTOMATION_GAPS.md) — portal and State Tree gaps and workarounds.
