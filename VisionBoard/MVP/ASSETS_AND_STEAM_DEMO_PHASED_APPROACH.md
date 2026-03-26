# Phased approach: Assets workflow, image-to-3D, and MVP deliverable (marketing-ready)

**Purpose:** Accomplish the work needed for the **MVP deliverable**: **marketing-ready** slice with **assets and visuals mandatory** for good-looking marketing material (screenshots, capsule, trailer). Phases 1–2 lock asset workflow and image-to-3D; Phase 3 (packaged build) is **optional for MVP**. **Phase 4 (store draft) is skipped** — when we ship on Steam, use [STEAM_EA_STORE_CHECKLIST](STEAM_EA_STORE_CHECKLIST.md) directly. — we do **not** require launching on Steam to call the MVP done. When we choose to ship, use the Steam checklist then.

**MVP deliverable = marketing-ready.** Assets and visuals are mandatory. Steam launch is not.

**Scope:** [ASSET_WORKFLOW_AND_STEAM_DEMO.md](../ASSET_WORKFLOW_AND_STEAM_DEMO.md), [NEXT_30_DAY_WINDOW.md](NEXT_30_DAY_WINDOW.md). **Act 2 prep is not in scope** (deferred).

**Task list linkage:** Each phase can be implemented as one or more 10-task lists in [CURRENT_TASK_LIST.md](CURRENT_TASK_LIST.md). See § "Mapping phases to task lists" below.

---

## Phase 1: Asset workflow and tooling (mandatory for MVP)

**Goal:** Lock the **asset generation workflow** and document what we can automate vs what stays manual. **Assets and visuals are mandatory for the MVP deliverable** (marketing material); this phase ensures we can add and iterate on assets consistently. No requirement to implement new scripts — document patterns, content paths, and manual steps so future asset work is consistent.

| Step | What to do | Where to document | Gate |
|------|------------|-------------------|------|
| 1.1 | **Workflow doc review:** Ensure [ASSET_WORKFLOW_AND_STEAM_DEMO.md](../ASSET_WORKFLOW_AND_STEAM_DEMO.md) §1 (asset workflow) is current: tools table, recommended workflow (source → import → paths → placement → document manual). Add any project-specific paths (e.g. `/Game/HomeWorld/Milady/`, Building, Maps) from [CONTENT_LAYOUT.md](../CONTENT_LAYOUT.md) if that doc exists. | ASSET_WORKFLOW_AND_STEAM_DEMO §1 | Workflow §1 complete and paths aligned |
| 1.2 | **Automation vs manual:** Document which asset steps are automatable (Python batch import, MCP placement, PCG config) and which require one-time or manual steps (VRM4U options, Meshy API key, DCC export presets). Per [automation-standards](.cursor/rules/automation-standards.mdc): list "no access" items and manual steps. | ASSET_WORKFLOW_AND_STEAM_DEMO §1 or MILADY_VARIABLES_NO_ACCESS / KNOWN_ERRORS | Clear automation vs manual list |
| 1.3 | **Optional — one repeatable asset step:** If useful, add or document one idempotent script (e.g. ensure content folders, or a minimal batch-import/placement pattern) in `Content/Python/` and reference it from the workflow doc. Skip if current scripts (e.g. ensure_milady_folders.py) already cover the pattern. | ASSET_WORKFLOW_AND_STEAM_DEMO §1 or Content/Python | Optional; gate does not require new code |

**Phase 1 gate:** Steps 1.1 and 1.2 done; workflow doc is the single entry point for "how we add assets." Optional 1.3 if it unblocks future work.

**Phase 1 gate — List 71:** Phase 1 gate met: workflow §1 complete and paths aligned; automation vs manual documented; ensure_* pattern referenced; CONTENT_LAYOUT and CONVENTIONS aligned; entry point and phased doc link in place. List 71 T1–T6 complete; no steps deferred.

---

## Phase 2: Image-to-3D (Milady) — research lock and deferred pass

**Goal:** Formalize the **deferred decision** for full "scan Milady image → 3D in-game" pipeline. Document that it is feasible (Meshy, Tripo/TripoSR) but deferred; optionally run **one manual path** (PNG → Meshy or Tripo → download GLB → VRM4U import) and record outcome so we have a known-good path when we resume.

| Step | What to do | Where to document | Gate |
|------|------------|-------------------|------|
| 2.1 | **Deferred pass doc:** In [ASSET_WORKFLOW_AND_STEAM_DEMO.md](../ASSET_WORKFLOW_AND_STEAM_DEMO.md) §2 and [MILADY_IMPORT_ROADMAP.md](../tasks/MILADY_IMPORT_ROADMAP.md) Phase 4, add an explicit note: "Image-to-3D (Milady) — feasible via Meshy or Tripo; **full pipeline deferred** to post–Steam Demo (or next asset sprint). Manual path: PNG → Meshy/Tripo → GLB → VRM4U import." | Both docs | Deferred decision recorded |
| 2.2 | **Optional — manual run:** If Meshy or Tripo (and VRM4U) are available: pick one Milady PNG, upload to Meshy or Tripo, download GLB, import in UE with VRM4U; note outcome (success, quality, any blockers) in SESSION_LOG or a short subsection of ASSET_WORKFLOW_AND_STEAM_DEMO §2. | SESSION_LOG or ASSET_WORKFLOW_AND_STEAM_DEMO §2 | Optional; gate does not require manual run |
| 2.3 | **Resume path:** Document "when resuming": implement Phase 4 (Meshy from UE) or Tripo path; document any "variables with no access" in MILADY_IMPORT_SETUP or MILADY_VARIABLES_NO_ACCESS. | ASSET_WORKFLOW_AND_STEAM_DEMO §2 or MILADY_IMPORT_ROADMAP | Resume steps clear |

**Phase 2 gate:** 2.1 and 2.3 done. Optional 2.2 (manual run) improves confidence but is not required for the gate.

**Phase 2 gate — List 72:** Phase 2 gate met: image-to-3D deferred; resume path documented.

---

## Phase 3: Packaged build and smoke test (optional for MVP)

**Goal:** Run the **packaged build** and **smoke test** so we have a distributable build (or a documented failure and workaround). **Not required for MVP deliverable** — MVP is marketing-ready (assets + visuals); this phase is for when we want a runnable exe for recording or future Steam distribution.

| Step | What to do | Where to document | Gate |
|------|------------|-------------------|------|
| 3.1 | **Packaged build:** Close Editor and any processes using project/Engine binaries. Run `.\Tools\Package-AfterClose.ps1` (or `-CleanStagedBuilds` if Stage failed before). Monitor `Package-HomeWorld.log` for exit code 0. See [workflow/STEAM_EA_STORE_CHECKLIST.md](STEAM_EA_STORE_CHECKLIST.md) § Packaged build retry and [KNOWN_ERRORS.md](../KNOWN_ERRORS.md) if Stage fails. | SESSION_LOG; STEAM_EA_STORE_CHECKLIST § Current status | Build run; outcome (success or documented failure) recorded |
| 3.2 | **Smoke test:** If packaged exe exists at `Saved\StagedBuilds\HomeWorld\WindowsNoEditor\HomeWorld\Binaries\Win64\HomeWorld.exe`, launch it; confirm level loads, character moves, no critical errors. | SESSION_LOG; STEAM_EA_STORE_CHECKLIST § Packaged build | Smoke test pass or "deferred" (no exe) with reason |

**Phase 3 gate:** 3.1 done (build run and outcome documented). 3.2 done when exe exists; otherwise document "smoke test deferred until packaged build succeeds."

**Phase 3 gate — List 73:** Phase 3 gate met: packaged build run, outcome recorded; smoke test deferred (no exe).

---

## Phase 4: Store draft — **SKIPPED**

**Status:** This phase has been removed from the plan. When we ship on Steam, use [STEAM_EA_STORE_CHECKLIST](../../docs/TaskLists/STEAM_EA_STORE_CHECKLIST.md) directly to draft store content and capsule/screenshots.

**Original goal (for reference):** Have a **store page draft** (title, short description, about, key features, capsule/screenshots plan) so when we **do** launch on Steam, store presence can be filled quickly. **Not required for MVP deliverable** — MVP = marketing-ready (assets + visuals); Steam launch is post-MVP. No Steamworks account or app creation required for this phase.

| Step | What to do | Where to document | Gate |
|------|------------|-------------------|------|
| 4.1 | **Store draft content:** Ensure [STEAM_EA_STORE_CHECKLIST.md](STEAM_EA_STORE_CHECKLIST.md) § Store page content (draft) has or is updated with: store title, short description, about/long description, key features, system requirements (draft). Use [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md) and [VISION.md](VISION.md) for tone and scope. | STEAM_EA_STORE_CHECKLIST § Store page content | Draft copy in checklist |
| 4.2 | **Capsule and screenshots plan:** Add a brief plan for capsule art (e.g. 616x353, 460x215) and in-game screenshots (e.g. vertical slice moment, Homestead corner). Can be a bullet list; actual assets can be created later. | STEAM_EA_STORE_CHECKLIST § Store page content or linked doc | Plan documented |

**Phase 4 gate:** Store draft (4.1) and capsule/screenshots plan (4.2) are in the checklist or linked; no blocker for future Steam launch. (MVP deliverable does not require Steam.)

---

## Phase 5: Consolidation and next-list prep

**Goal:** Record this phased block's outcomes and leave the project ready for the **next** task list (e.g. more assets, polish, or Steamworks setup when we choose to ship).

| Step | What to do | Where to document | Gate |
|------|------------|-------------------|------|
| 5.1 | **Vertical slice §4:** Add a row or subsection to [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md) §4 for "Assets + MVP deliverable (marketing-ready) phased block": Phase 1–3 outcomes (workflow locked, image-to-3D deferred, packaged build/smoke test status if run). Phase 4 (store draft) skipped.. | VERTICAL_SLICE_CHECKLIST §4 | §4 updated |
| 5.2 | **ACCOMPLISHMENTS_OVERVIEW and PROJECT_STATE:** Update [ACCOMPLISHMENTS_OVERVIEW.md](ACCOMPLISHMENTS_OVERVIEW.md) §4 with this block (e.g. "Assets + MVP deliverable phased approach: Phase 1–2 (workflow, assets/visuals) complete; Phase 3 optional for MVP; Phase 4 (store draft) skipped"). Update [PROJECT_STATE_AND_TASK_LIST.md](PROJECT_STATE_AND_TASK_LIST.md) §4 so "Next" points to next list per [NEXT_30_DAY_WINDOW.md](NEXT_30_DAY_WINDOW.md) (further assets, polish, or Steam when we ship). | Both docs | Accomplishments and next step clear |
| 5.3 | **DAILY_STATE and SESSION_LOG:** Set [DAILY_STATE.md](DAILY_STATE.md) Yesterday/Today to reflect completion of this block; Tomorrow = next list focus. Append [SESSION_LOG.md](../SESSION_LOG.md) with a short summary (phases completed, any deferrals). | DAILY_STATE; SESSION_LOG | Session continuity updated |

**Phase 5 gate:** 5.1–5.3 done; next 10-task list can be generated per [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md).

---

## Before starting the next phase (agent checklist)

When the user says **"start agents on next phase"** (or you are about to create the next list for this approach):

1. **Read session files** to verify the previous phase completed and what was deferred:
   - **SESSION_LOG.md** — last 1–2 dated entries: what the previous list completed (e.g. "Phase 1 done; workflow doc updated"; "Phase 3: packaged build deferred, Stage failed").
   - **DAILY_STATE.md** — Today/Yesterday match the current phase; previous list marked complete or pending.
   - **CURRENT_TASK_LIST.md** — which tasks are `completed` vs `pending`/`blocked` so we don’t advance on an incomplete list.
2. **Optional:** If `Saved/Logs/automation_tasks_complete.md` or similar exists, read for loop exit reason.
3. **Then** create the next list (or confirm it), update PROJECT_STATE and DAILY_STATE, and run `.\Tools\Start-AllAgents-InNewWindow.ps1`. If the previous phase had critical deferrals (e.g. packaged build never succeeded), note that in the new list context or inform the user.

This keeps advancement based on **verified outcomes** from session files.

---

## Mapping phases to task lists

Use this to turn phases into 10-task lists. Each phase can be **one list** or combined (e.g. Phase 1+2 in one list, Phase 3+4 in another). Follow [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md) (implementation vs verification split, T8 Docs and cycle, T9 Verification, T10 Buffer).

| Phase | Suggested T1–T7 (implementation) | T8 | T9 | T10 |
|-------|----------------------------------|-----|-----|-----|
| **1** | T1 Workflow §1 review and paths (1.1). T2 Automation vs manual list (1.2). T3 Optional script or doc (1.3). T4–T7 Buffer or small follow-ups (e.g. CONTENT_LAYOUT, CONVENTIONS). | Docs and cycle | Verification | Buffer |
| **2** | T1 Deferred pass in ASSET_WORKFLOW_AND_STEAM_DEMO + MILADY_IMPORT_ROADMAP (2.1). T2 Optional manual run and outcome (2.2). T3 Resume path doc (2.3). T4–T7 Buffer or Phase 1 follow-ups. | Docs and cycle | Verification | Buffer |
| **3** | T1 Run Package-AfterClose.ps1; document outcome (3.1). T2 Smoke test if exe exists (3.2). T3 Update STEAM_EA_STORE_CHECKLIST § Current status. T4–T7 Buffer or store draft start. | Docs and cycle | Verification | Buffer |
| **4 (skipped)** | — Phase 4 removed from plan. Use STEAM_EA_STORE_CHECKLIST when shipping. | — | — | — |
| **5** | T1 VERTICAL_SLICE_CHECKLIST §4 (5.1). T2 ACCOMPLISHMENTS_OVERVIEW + PROJECT_STATE §4 (5.2). T3 DAILY_STATE + SESSION_LOG (5.3). T4–T7 Buffer. | Docs and cycle | Verification | Buffer |

**Order:** Execute phases 1 → 2 → 3 → 5 (Phase 4 skipped). You can merge phases into fewer lists (e.g. List A = Phase 1+2, List B = Phase 3+4, List C = Phase 5) to reduce overhead.

---

## Success for this plan

- [ ] Phase 1 gate: Asset workflow doc current; automation vs manual documented.
- [ ] Phase 2 gate: Image-to-3D deferred pass and resume path documented.
- [ ] Phase 3 gate: Packaged build run and outcome documented; smoke test if exe exists.
- [x] Phase 4: **Skipped** (removed from plan).
- [ ] Phase 5 gate: VERTICAL_SLICE §4, ACCOMPLISHMENTS, PROJECT_STATE, DAILY_STATE, SESSION_LOG updated; next list can be generated.

**See also:** [ASSET_WORKFLOW_AND_STEAM_DEMO.md](../ASSET_WORKFLOW_AND_STEAM_DEMO.md), [NEXT_30_DAY_WINDOW.md](NEXT_30_DAY_WINDOW.md), [STEAM_EA_STORE_CHECKLIST.md](STEAM_EA_STORE_CHECKLIST.md), [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md).
