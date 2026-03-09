# Phased approach to 100% MVP completion (asset-ready gate)

**Purpose:** Get from **~78–85% MVP** to **100% MVP** in clear phases so you can **start adding assets** with a stable, verified baseline. Each phase has a gate; after Phase 4 you are at "100% MVP" and **asset-ready**.

**Current state:** See [MVP_FULL_SCOPE_10_LISTS.md](MVP_FULL_SCOPE_10_LISTS.md) § List 64 (current state vs Lists 55–64) and the [MVP completeness percentage](MVP_FULL_SCOPE_10_LISTS.md#list-64-mvp-full-scope-verification-current-state-and-gaps) assessment. Gaps: packaged build not run; tutorial + Week 1 playtest single-session runs deferred; demo sign-off deferred; full agentic Path 2 (family BUILD branch) deferred.

**Definition of 100% for this plan:** All **run/verify** and **sign-off** items below are done. **Full agentic Path 2** (family agent claims and completes build order via State Tree) is **optional for the asset-ready gate** — you can add it later without blocking asset work. Path 1 (place wall, complete build order, simulate SO activation) remains the MVP bar for "agentic building" for asset-ready.

---

## Phase 1: Run and verify (integration + pre-demo)

**Goal:** Execute the integration runs and pre-demo checklist so the vertical slice is **verified in PIE**, not just documented.

| Step | What to do | Where to document | Gate |
|------|------------|-------------------|------|
| 1.1 | Open DemoMap, PCG generated, start PIE. Run `pie_test_runner.py` (Editor or MCP); read `Saved/pie_test_results.json`. | [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md) §3 or SESSION_LOG | Pass/fail per check in results |
| 1.2 | **Tutorial loop single-session:** In one PIE session, run the 13-step sequence per [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § Pre-demo verification and [MVP_TUTORIAL_PLAN.md](MVP_TUTORIAL_PLAN.md) (hw.Meal.Breakfast → hw.LoveTask.Complete → hw.GameWithChild.Complete → gather → hw.Meal.Lunch → hw.Meal.Dinner → hw.GoToBed → spectral/combat → hw.GrantBossReward → hw.AstralDeath → hw.TutorialEnd). | SESSION_LOG or VERTICAL_SLICE_CHECKLIST §3 | Which steps completed; any deferred/failed |
| 1.3 | **Week 1 playtest single-session:** Run Week 1 playtest (crash → scout → boss → claim home) per CONSOLE_COMMANDS § Pre-demo and [DAY5_PLAYTEST_SIGNOFF.md](../tasks/DAY5_PLAYTEST_SIGNOFF.md) § T1. | SESSION_LOG or DAY5_PLAYTEST_SIGNOFF § T1 result | Pass/fail per beat; 2–5 min stability |
| 1.4 | **Pre-demo checklist:** Complete VERTICAL_SLICE_CHECKLIST §3 items (level, character, moment, corner, stability). Tick or note each. | VERTICAL_SLICE_CHECKLIST.md §3 | All items checked or explicitly deferred with reason |

**Phase 1 gate:** All four steps run; outcomes written to the docs above. No blocker to proceed if some steps are "partial" — document and continue; fix critical failures before Phase 2.

**Phase 1 gate — List 66 (2026-03-08):** All four steps (1.1–1.4) run; outcomes documented in [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md) §3 (1.1, 1.2, 1.4), [DAY5_PLAYTEST_SIGNOFF.md](../tasks/DAY5_PLAYTEST_SIGNOFF.md) § T1 (1.3), and [SESSION_LOG.md](../SESSION_LOG.md). All steps deferred this round (Editor/MCP not connected); no critical failure to fix before Phase 2 — procedures for when Editor is available are in place. Proceed to Phase 2 (Packaged build run) or re-run Phase 1 in PIE when Editor is connected.

**Entry point:** [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md#pre-demo-verification-entry-point) links §3 run sequence and all `hw.*` commands.

---

## Before starting the next phase (agent checklist)

When the user says **"start agents on next phase"** (or you are about to create the next list and run the loop):

1. **Read session files** to verify the previous phase actually completed and what was deferred:
   - **SESSION_LOG.md** — read the **last 1–2 dated entries** to see what the previous list completed (e.g. "T1–T2 completed; smoke-test deferred"; "packaged build run" vs "deferred").
   - **DAILY_STATE.md** — confirm "Today" / "Yesterday" match the current list and that the previous list is marked complete (or note any pending).
   - **CURRENT_TASK_LIST.md** — if the previous list is still in place, check which tasks are `completed` vs `pending`/`blocked` so you don't advance on an incomplete list.
2. **Optional:** If `Saved/Logs/automation_tasks_complete.md` or `Saved/Logs/automation_exit_alert.md` exists (when not gitignored), read it for loop exit reason and last round.
3. **Then** create the next list (or confirm the next list is correct), update PROJECT_STATE and DAILY_STATE, and run `.\Tools\Start-AllAgents-InNewWindow.ps1`. If the previous phase had critical deferrals (e.g. packaged build never run, Phase 1 PIE runs all deferred), you can note that in the new list's context or inform the user.

This ensures we advance on **verified outcomes** from the session files, not only on the phased plan.

---

## Phase 2: Packaged build run and smoke-test

**Goal:** Run **Package Game** (or project package script); document outcome. Optional: launch packaged exe and load map or main menu (smoke-test).

| Step | What to do | Where to document | Gate |
|------|------------|-------------------|------|
| 2.1 | Close Editor. Run packaged build (e.g. [Package-HomeWorld.bat](../../Package-HomeWorld.bat) or RunUAT; see [KNOWN_ERRORS.md](../KNOWN_ERRORS.md) Package-HomeWorld if Stage fails). | SESSION_LOG or KNOWN_ERRORS | Build completes or failure + workaround documented |
| 2.2 | If build succeeds: optional smoke-test — launch `Saved\StagedBuilds\HomeWorld\WindowsNoEditor\...\HomeWorld.exe`, load main menu or DemoMap. | SESSION_LOG or VERTICAL_SLICE_CHECKLIST §3 | Packaged exe runs (or "deferred" with reason) |

**Phase 2 gate:** Packaged build has been run and outcome (success or documented failure) is recorded. Smoke-test is optional but recommended for "100% MVP."

**Phase 2 gate — List 67 (2026-03-08):** Packaged build run and outcome recorded (T1 completed); smoke-test deferred (T2 — no packaged exe at StagedBuilds this cycle). Phase 2 gate met. Proceed to Phase 3 (Demo sign-off) or re-run packaged build when ready (see [STEAM_EA_STORE_CHECKLIST.md](STEAM_EA_STORE_CHECKLIST.md) § Current status, § Packaged build retry).

**Reference:** List 55 scope; [KNOWN_ERRORS.md](../KNOWN_ERRORS.md) (Package-HomeWorld, MissingExecutable).

---

## Phase 3: Demo sign-off

**Goal:** **Demo sign-off** for the vertical slice: confirm the slice is showable; optional 1–3 min recording.

| Step | What to do | Where to document | Gate |
|------|------------|-------------------|------|
| 3.1 | Confirm chosen **moment** (e.g. Claim homestead) and **corner** (e.g. Homestead compound) per [PROTOTYPE_SCOPE.md](PROTOTYPE_SCOPE.md). Spot-check in PIE. | VERTICAL_SLICE_CHECKLIST §3 | Moment + corner confirmed |
| 3.2 | Sign off: "Vertical slice is demo-ready" or list remaining polish. Optional: record 1–3 min user-led demo. | VERTICAL_SLICE_CHECKLIST §3 or SESSION_LOG | Sign-off or deferred reason recorded |

**Phase 3 gate:** Demo sign-off (or explicit deferral) is documented. No blocker for asset work if you defer recording — sign-off that the slice is **ready to show** is enough for 100% gate.

**Phase 3 gate — List 68 (2026-03-08):** Phase 3.1 (moment Claim homestead, corner Homestead compound) and Phase 3.2 (demo sign-off: slice ready to show; optional 1–3 min recording deferred) are documented in [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md) §3 (T1/T2 sixty-eighth list). Phase 3 gate met. Proceed to Phase 4 (100% MVP asset-ready gate) or re-run PIE spot-check when Editor is available.

---

## Phase 4: 100% MVP — asset-ready gate

**Goal:** Declare **100% MVP** and **asset-ready**. Update project docs so the next step is clearly "add assets."

| Step | What to do | Where to document | Gate |
|------|------------|-------------------|------|
| 4.1 | Update [PROJECT_STATE_AND_TASK_LIST.md](PROJECT_STATE_AND_TASK_LIST.md) or [ACCOMPLISHMENTS_OVERVIEW.md](ACCOMPLISHMENTS_OVERVIEW.md) with **MVP 100% complete** and **Asset-ready** note. | PROJECT_STATE_AND_TASK_LIST §1 or ACCOMPLISHMENTS_OVERVIEW | One-line "MVP 100%; asset-ready" |
| 4.2 | Add a short **Asset-ready checklist** (optional): "Before adding new assets: DemoMap open, PCG generated, PIE stable, CONSOLE_COMMANDS § Pre-demo is the entry point for verification." | This doc or [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md) §3 | Future you (or agents) know how to re-verify after adding assets |
| 4.3 | If you deferred **full agentic Path 2** (family BUILD branch): add a single line to [AUTOMATION_GAPS.md](../AUTOMATION_GAPS.md) or PROJECT_STATE §2: "Full agentic Path 2 (State Tree BUILD) is post–100% MVP; add when ready." | AUTOMATION_GAPS or PROJECT_STATE §2 | No confusion that Path 2 is required for asset-ready |

**Asset-ready checklist (re-verify after adding assets):** Before adding new assets (or after large asset/level changes): DemoMap open, PCG generated, PIE stable; [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § Pre-demo is the entry point for verification (run §3 steps + `pie_test_runner` when needed).

**Phase 4 gate:** Docs state MVP 100% and asset-ready. You can start adding assets (meshes, materials, VFX, levels, Blueprint art) on top of this baseline.

**Phase 4 gate — List 69 (2026-03-08):** MVP 100%; asset-ready. Phase 4.1–4.3 completed: MVP 100% asset-ready note in [PROJECT_STATE_AND_TASK_LIST.md](PROJECT_STATE_AND_TASK_LIST.md) §1 and [ACCOMPLISHMENTS_OVERVIEW.md](ACCOMPLISHMENTS_OVERVIEW.md); asset-ready checklist in this doc and [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § Pre-demo; Path 2 deferred note in PROJECT_STATE §2. You can start adding assets. Next lists per [NEXT_30_DAY_WINDOW.md](NEXT_30_DAY_WINDOW.md) or user-defined.

---

## Summary: phase order and time

| Phase | Focus | Typical effort | Gate |
|-------|--------|----------------|------|
| **1** | Run and verify (integration + pre-demo) | 1–2 sessions (Editor + PIE) | Tutorial + Week 1 + pre-demo run and documented |
| **2** | Packaged build + smoke-test | 1 session (Editor closed; build ~30+ min) | Packaged build run and outcome documented |
| **3** | Demo sign-off | 1 short session | Sign-off or deferral documented |
| **4** | 100% MVP / asset-ready | 1 short doc update | "MVP 100%; asset-ready" in project state |

**Total:** Roughly **3–5 focused sessions** (depending on packaged build success and how many retries). After Phase 4, **start adding assets**; re-run Phase 1 (pre-demo checklist) after large asset or level changes to keep the slice verified.

---

## What "asset-ready" means

- **Stable baseline:** PIE runs; pre-demo checklist has been executed and documented; packaged build has been run (or failure documented).
- **Single entry point:** [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § Pre-demo verification is the place to re-verify after you add assets (run §3 steps + pie_test_runner when needed).
- **No blocking work:** Full agentic Path 2 (State Tree BUILD branch) and optional polish (e.g. 1–3 min recording) do **not** block "asset-ready." You can add them in a later phase while already adding assets.

---

## Links

- **Pre-demo and commands:** [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) § Pre-demo verification  
- **Checklist:** [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md) §3  
- **Tutorial steps:** [MVP_TUTORIAL_PLAN.md](MVP_TUTORIAL_PLAN.md)  
- **Week 1 playtest:** [DAY5_PLAYTEST_SIGNOFF.md](../tasks/DAY5_PLAYTEST_SIGNOFF.md) § T1  
- **Current state and gaps:** [MVP_FULL_SCOPE_10_LISTS.md](MVP_FULL_SCOPE_10_LISTS.md) § List 64  
- **Packaged build:** [KNOWN_ERRORS.md](../KNOWN_ERRORS.md) (Package-HomeWorld)  
- **Next lists after 100%:** [NEXT_30_DAY_WINDOW.md](NEXT_30_DAY_WINDOW.md) (Harden & demo, Deferred, Act 2 prep, Steam EA)
