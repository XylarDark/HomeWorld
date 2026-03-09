# Current task list (10-task)

**Last updated:** 2026-03-02 (seventy-first list — **Assets + Steam Demo Phase 1: Asset workflow and tooling**). **Context:** [ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md](ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md) Phase 1 — lock asset workflow doc, document automation vs manual, optional script; gate = workflow §1 current and automation vs manual listed.

**Purpose:** Single ordered list that drives the automation loop. Agents fetch the first **pending** or **in_progress** task; update status when done. Loop exits when no task has status pending or in_progress.

**Convention:** `pending` | `in_progress` | `completed` | `blocked`

**Order:** T1–T7 = Phase 1 implementation (workflow, automation vs manual, optional script, follow-ups); T8 = Docs and cycle; T9 = Verification; T10 = Buffer.

---

## T1. Workflow §1 review and paths (Phase 1 step 1.1)

- **goal:** Ensure [ASSET_WORKFLOW_AND_STEAM_DEMO.md](../ASSET_WORKFLOW_AND_STEAM_DEMO.md) §1 (asset workflow) is current: tools table, recommended workflow (source → import → paths → placement → document manual). Add or align project-specific paths (e.g. `/Game/HomeWorld/Milady/`, Building, Maps) from [CONTENT_LAYOUT.md](../CONTENT_LAYOUT.md) so workflow §1 references the single source of truth for content paths.
- **success criteria:** ASSET_WORKFLOW_AND_STEAM_DEMO §1 complete; paths in §1 match or reference CONTENT_LAYOUT; workflow is the entry point for "how we add assets."
- **research_notes:** [ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md](ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md) Phase 1 step 1.1; [CONTENT_LAYOUT.md](../CONTENT_LAYOUT.md) (Milady, Building, Maps, Characters, PCG, etc.); [ASSET_WORKFLOW_AND_STEAM_DEMO.md](../ASSET_WORKFLOW_AND_STEAM_DEMO.md) §1.
- **steps_or_doc:** docs/ASSET_WORKFLOW_AND_STEAM_DEMO.md §1; docs/CONTENT_LAYOUT.md.
- **status:** completed

---

## T2. Automation vs manual list (Phase 1 step 1.2)

- **goal:** Document which asset steps are **automatable** (Python batch import, MCP placement, PCG config, EditorAssetLibrary) and which require **one-time or manual** steps (VRM4U import options, Meshy API key, DCC export presets, State Tree editing). Per [automation-standards](.cursor/rules/automation-standards.mdc): list "no access" items and the manual step for each. Place in ASSET_WORKFLOW_AND_STEAM_DEMO §1, or in MILADY_VARIABLES_NO_ACCESS / [KNOWN_ERRORS.md](../KNOWN_ERRORS.md) with a cross-reference from §1.
- **success criteria:** Clear automation vs manual list in workflow doc or linked doc; each "no access" item has manual step documented; Phase 1 gate 1.2 satisfied.
- **research_notes:** [ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md](ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md) Phase 1 step 1.2; .cursor/rules/automation-standards.mdc; [AUTOMATION_GAPS.md](../AUTOMATION_GAPS.md); [docs/PCG_VARIABLES_NO_ACCESS.md](../PCG_VARIABLES_NO_ACCESS.md) (pattern for no-access docs).
- **steps_or_doc:** docs/ASSET_WORKFLOW_AND_STEAM_DEMO.md §1; docs/AUTOMATION_GAPS.md; docs/KNOWN_ERRORS.md.
- **status:** completed

---

## T3. Optional — one repeatable asset step (Phase 1 step 1.3)

- **goal:** If useful, add or document **one idempotent script** (e.g. ensure content folders, or a minimal batch-import/placement pattern) in `Content/Python/` and reference it from the workflow doc. **Skip** if current scripts (e.g. ensure_milady_folders.py) already cover the pattern; then document in ASSET_WORKFLOW_AND_STEAM_DEMO §1 that "ensure_* folders" pattern is the reference and list existing scripts. Gate does not require new code.
- **success criteria:** Either (a) one new or updated script referenced from workflow §1, or (b) workflow §1 explicitly references existing ensure_* (or equivalent) scripts as the repeatable-asset-step pattern; T3 status set to completed.
- **research_notes:** [ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md](ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md) Phase 1 step 1.3; Content/Python/ensure_milady_folders.py; Content/Python/ensure_ui_folders.py; idempotency per 00-core-principles.mdc.
- **steps_or_doc:** docs/ASSET_WORKFLOW_AND_STEAM_DEMO.md §1; Content/Python/.
- **status:** completed

---

## T4. CONTENT_LAYOUT alignment with workflow paths

- **goal:** Ensure [CONTENT_LAYOUT.md](../CONTENT_LAYOUT.md) is consistent with the workflow §1 paths: all asset types (Milady, Building, Maps, Characters, PCG, etc.) used in the workflow doc are present in CONTENT_LAYOUT. If CONTENT_LAYOUT has paths not yet mentioned in ASSET_WORKFLOW_AND_STEAM_DEMO §1, add a short "Content paths" sentence or table row in §1 that points to CONTENT_LAYOUT as the single source of truth.
- **success criteria:** CONTENT_LAYOUT and workflow §1 paths aligned; workflow §1 points to CONTENT_LAYOUT for full path list; T4 status set to completed.
- **research_notes:** [CONTENT_LAYOUT.md](../CONTENT_LAYOUT.md); [ASSET_WORKFLOW_AND_STEAM_DEMO.md](../ASSET_WORKFLOW_AND_STEAM_DEMO.md) §1.
- **steps_or_doc:** docs/CONTENT_LAYOUT.md; docs/ASSET_WORKFLOW_AND_STEAM_DEMO.md §1.
- **status:** completed

---

## T5. CONVENTIONS or doc note for asset paths

- **goal:** If [CONVENTIONS.md](../CONVENTIONS.md) (or equivalent) exists, add or update a short note on **asset path / import convention** (e.g. new project content under `/Game/HomeWorld/` or a documented subfolder; LFS for .uasset/.umap). If CONVENTIONS does not exist or has no asset section, add a one-paragraph "Asset paths" subsection to ASSET_WORKFLOW_AND_STEAM_DEMO §1 that states the convention and links to CONTENT_LAYOUT.
- **success criteria:** Asset path convention is stated in CONVENTIONS or in workflow §1 with link to CONTENT_LAYOUT; T5 status set to completed.
- **research_notes:** [CONVENTIONS.md](../CONVENTIONS.md); [CONTENT_LAYOUT.md](../CONTENT_LAYOUT.md); [ASSET_WORKFLOW_AND_STEAM_DEMO.md](../ASSET_WORKFLOW_AND_STEAM_DEMO.md) §1.
- **steps_or_doc:** docs/CONVENTIONS.md; docs/ASSET_WORKFLOW_AND_STEAM_DEMO.md §1; docs/CONTENT_LAYOUT.md.
- **status:** completed

---

## T6. Phase 1 entry point and phased doc link

- **goal:** Ensure [NEXT_30_DAY_WINDOW.md](NEXT_30_DAY_WINDOW.md) and [ASSET_WORKFLOW_AND_STEAM_DEMO.md](../ASSET_WORKFLOW_AND_STEAM_DEMO.md) both point to [ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md](ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md) for phased execution. Add a "Phase 1 gate" outcome line to ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md § Phase 1 when T1–T2 (and optionally T3) are done (e.g. "Phase 1 gate — List 71: workflow §1 current, automation vs manual listed; gate met."). Do this as a placeholder or fill after T1–T2 complete; T6 can be updated in T8 or T9 if preferred.
- **success criteria:** NEXT_30_DAY_WINDOW and ASSET_WORKFLOW_AND_STEAM_DEMO reference the phased approach; Phase 1 section in phased doc has a gate-outcome note (can be "pending List 71" until T1–T2 done); T6 status set to completed.
- **research_notes:** [NEXT_30_DAY_WINDOW.md](NEXT_30_DAY_WINDOW.md); [ASSET_WORKFLOW_AND_STEAM_DEMO.md](../ASSET_WORKFLOW_AND_STEAM_DEMO.md); [ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md](ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md) Phase 1.
- **steps_or_doc:** docs/workflow/NEXT_30_DAY_WINDOW.md; docs/ASSET_WORKFLOW_AND_STEAM_DEMO.md; docs/workflow/ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md.
- **status:** completed

---

## T7. Phase 1 gate — document completion

- **goal:** Confirm Phase 1 steps 1.1 and 1.2 are complete (workflow §1 current, automation vs manual listed). Document in [ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md](ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md) Phase 1 section a one-line **Phase 1 gate — List 71** outcome (e.g. "Phase 1 gate met: workflow §1 complete and paths aligned; automation vs manual documented."). If either step was deferred, note it. Optionally add a short SESSION_LOG-style summary.
- **success criteria:** Phase 1 gate outcome recorded in phased approach doc (and optionally SESSION_LOG); T7 status set to completed.
- **research_notes:** [ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md](ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md) Phase 1 gate; [SESSION_LOG.md](../SESSION_LOG.md).
- **steps_or_doc:** docs/workflow/ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md; docs/SESSION_LOG.md.
- **status:** completed

---

## T8. Docs and cycle (combined)

- **goal:** In **one task**, do all of: (1) Ensure VERTICAL_SLICE_CHECKLIST §4 has a seventy-first-list deliverables row (Phase 1: asset workflow locked, automation vs manual, CONTENT_LAYOUT/CONVENTIONS alignment). (2) CONSOLE_COMMANDS or workflow doc updated if any new verification steps were added. (3) KNOWN_ERRORS or AUTOMATION_GAPS cycle note for list 71 (e.g. "Seventy-first list (Phase 1 Asset workflow): T1–T7 outcomes; workflow §1, automation vs manual, Phase 1 gate."). Success = all three done (or explicitly deferred).
- **success criteria:** Vertical slice §4 has seventy-first-list row; CONSOLE_COMMANDS/workflow current if needed; KNOWN_ERRORS or AUTOMATION_GAPS cycle note; T8 status set to completed.
- **research_notes:** [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md) §4; [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md); [KNOWN_ERRORS.md](../KNOWN_ERRORS.md); [AUTOMATION_GAPS.md](../AUTOMATION_GAPS.md).
- **steps_or_doc:** docs/workflow/VERTICAL_SLICE_CHECKLIST.md; docs/CONSOLE_COMMANDS.md; docs/KNOWN_ERRORS.md; docs/AUTOMATION_GAPS.md.
- **status:** pending

---

## T9. Verification (combined)

- **goal:** In **one task**, do all of: (1) If T1–T7 changed C++ or Build.cs, run Build-HomeWorld.bat and confirm build passes. (2) Review VERTICAL_SLICE_CHECKLIST §3–§4 and ASSET_WORKFLOW_AND_STEAM_DEMO for consistency; document outcome in SESSION_LOG or checklist. (3) Run validate_task_list.py and fix any schema issues; update DAILY_STATE "Today" if needed. Success = build green (if applicable), doc review done, list validated.
- **success criteria:** Build run and result logged if applicable; doc review done and noted; validate_task_list.py passed; DAILY_STATE updated if needed; T9 status set to completed.
- **research_notes:** Build-HomeWorld.bat; [VERTICAL_SLICE_CHECKLIST.md](VERTICAL_SLICE_CHECKLIST.md) §3–§4; [ASSET_WORKFLOW_AND_STEAM_DEMO.md](../ASSET_WORKFLOW_AND_STEAM_DEMO.md); [SESSION_LOG.md](../SESSION_LOG.md); Content/Python/validate_task_list.py; [DAILY_STATE.md](DAILY_STATE.md).
- **steps_or_doc:** Build-HomeWorld.bat; docs/workflow/VERTICAL_SLICE_CHECKLIST.md; docs/ASSET_WORKFLOW_AND_STEAM_DEMO.md; python Content/Python/validate_task_list.py; docs/workflow/DAILY_STATE.md.
- **status:** pending

---

## T10. Buffer: next list prep (ACCOMPLISHMENTS + PROJECT_STATE §4)

- **goal:** Update ACCOMPLISHMENTS_OVERVIEW §4 with seventy-first-list (Phase 1 Asset workflow) outcome and PROJECT_STATE_AND_TASK_LIST §4. Do NOT replace CURRENT_TASK_LIST (user does that after the loop). Set T1–T10 status to completed where done. **Next:** Per [ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md](ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md) — Phase 2 (Image-to-3D deferred pass), or Phase 3 (Steam Demo packaged build); generate next list per HOW_TO_GENERATE_TASK_LIST when ready.
- **success criteria:** ACCOMPLISHMENTS_OVERVIEW §4 has seventy-first-cycle row; PROJECT_STATE §4 says list 71 complete and points to Phase 2 or Phase 3; T10 status set to completed in CURRENT_TASK_LIST only.
- **research_notes:** [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md); [ACCOMPLISHMENTS_OVERVIEW.md](ACCOMPLISHMENTS_OVERVIEW.md); [PROJECT_STATE_AND_TASK_LIST.md](PROJECT_STATE_AND_TASK_LIST.md); [ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md](ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md).
- **steps_or_doc:** HOW_TO_GENERATE_TASK_LIST.md; ACCOMPLISHMENTS_OVERVIEW.md; PROJECT_STATE_AND_TASK_LIST.md; ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md.
- **status:** pending

---

**Order:** T1–T7 = Phase 1 (workflow §1, automation vs manual, optional script, CONTENT_LAYOUT/CONVENTIONS, entry point, Phase 1 gate). T8 = Docs and cycle. T9 = Verification. T10 = Buffer. **After list 71:** Phase 2 (image-to-3D deferred) or Phase 3 (packaged build + smoke test) per [ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md](ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md); run `.\Tools\Start-AllAgents-InNewWindow.ps1` when ready for next list.
