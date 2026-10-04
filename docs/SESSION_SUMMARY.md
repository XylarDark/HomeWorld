## 2026-09-23 — PS-C-CAP-001 absolute ps_stills paths (cloud, rung-1)

- **Ticket PS-C-CAP-001:** HighResShot ladder **Bad input** when dest was basename/cwd-relative → orphan PNG, **0/7** gate. **Fix:** `capture_viewport._ensure_abs_dest`; `ps_placement_prove._resolve_still_path` + AL path guard under **`Saved/ps_stills/`**; KNOWN_ERRORS Cause→Avoid. Draft PR — DESKTOP re-prove `CAM_CabinClose` + full `ps_placement_prove.py`.

## 2026-09-23 — UE_BIBLE anti-ladder hard rules (cloud)

- **Docs-only:** [UE_BIBLE.md](../Docs/UE_BIBLE.md) §2b — Conductor/Lead harness locks (one repro before ladder PR, no third ladder, one Fix per root cause); Cause→Avoid table; HighResShot freeze + MRQ pointer. [PDF_CYCLE.md](../swarm/PDF_CYCLE.md) Host Pulse one-liner. Branch `cursor/ue-bible-anti-ladder-b3a5` — draft PR, not merged.

## 2026-09-23 — PS-C-3 fresh stills + gate/disk parity (cloud, post-#195)

- **Ticket PS-C-3:** DESKTOP scored **closed_fail** — **flaky capture** (5× PS_* `png_missing` + timeout) + **false metric proxy** (gate `file_exists` vs stale CAM mtimes). **Fix:** PS_* **console HighResShot abs then AL**; wait-deadline console/AL retry rounds; post-drive **final drain** + **`_audit_ps_stills_disk`**; gate **`stills_present_count` = disk-fresh**, **`gate_count_matches_disk`**. Epic screenshot doc + forum tick-wait cited in KNOWN_ERRORS. Draft **#196** — DESKTOP re-prove only.

## 2026-09-23 — Docs/33 Placement Stills (PS) strategy draft (cloud)

- **PS-0:** [33_PLACEMENT_STILLS.md](../Docs/33_PLACEMENT_STILLS.md) — homestead-only placement stills suite (metrics catalog, multi-angle cams, benchmark sources, PS-A…E gates ending **`APPROVE PS STRATEGY`**). Handoff [PS_STRATEGY.md](../Docs/handoffs/PS_STRATEGY.md). Reuses PA-E harness patterns (`pa_e_shotlist_common`, HARNESS_ARRANGE); no `.uasset` commits. PHASE_BOARD + Docs/README updated. **Pending Lead gate.**

## 2026-09-23 — PDF development cycle ops doc (cloud)

- Added [swarm/PDF_CYCLE.md](../swarm/PDF_CYCLE.md) (Design → Implement → Test → Fix companion to SWARM_OPS); Grok sidebar agents HomeWorld Design/Implement/Test/Fix + Conductor parent; tiny SWARM_OPS §0 pointer.

## 2026-09-22 — Harness P3 audit + universal tooling checklist (cloud)

- **P3:** [HARNESS_ARRANGE_TASKLIST.md](Automation/HARNESS_ARRANGE_TASKLIST.md) prove-script matrix; wired **`conductor_night_evidence_preflight`** + **`summarize_evidence_png_harness`** for NF2-B/VNP; NF2-B **`capture_outcome`** parity; viewport **`reload_pa_e_capture_python_modules`**. Exempt docstrings for host/utility/spikes. **automation-standards.mdc** v1.11 universal gap checklist; CAPTURE_REDUNDANCY P3 pointer. **DESKTOP re-prove** NF2-B / PA-E after merge.

## 2026-09-22 — PA-E harness P1: three-state + framing gate + conductor preflight (cloud)

- **P1 Lead-approved:** [pa_e_shotlist_common.py](../Content/Python/pa_e_shotlist_common.py) — **`capture_outcome`** (`pass`/`soft_fail`/`closed_fail`), **`finalize_shot_validation`** (luminance vs framing intent, Lead eyeball stamp), **`conductor_mrq_capture_preflight`** (Markers world reload, VNP module reload). MRQ [capture_shotlist_mrq.py](../Content/Python/capture_shotlist_mrq.py) wires preflight + guards; night gate prefers **`visible_sky_stack_ok`**. Docs: CAPTURE_REDUNDANCY, KNOWN_ERRORS, HARNESS P1. **DESKTOP re-prove required** after merge (cloud has no UE).

## 2026-09-22 — PA-E MRQ visible sky iteration (post-#178 FAIL)

- DESKTOP #178: PIE `stack_ok` but sky still void; **height_fog absent**. **Fix:** spawn/tune **ExponentialHeightFog** in PIE; atmo @ **world origin**; MRQ skylight **hemisphere fill** (skip early black recapture); warm-up **56/16**; full stack + recapture on Slate ticks during MRQ wait. Report **`visible_sky_stack_ok`**. Gap **OPEN** — DESKTOP re-prove top-band RGB.

## 2026-09-22 — PA-E MRQ PIE sky in render world (post-#177)

- Post-#177 DESKTOP: **`mrq_pie_night_stack.ok`** but sky still void black; geometry lit. **Fix:** world-aware `apply_mrq_pie_homestead_night_stack` + **`apply_mrq_pie_homestead_night_stack_in_render_world`** during MRQ wait; PIE deferred spawn; **AtmosphereSunLightIndex 0**; centroid sanitize; `r.SupportSkyAtmosphere 1` on job. Gap **OPEN** — DESKTOP re-prove sky band RGB.

## 2026-09-22 — PA-E MRQ PIE readable night sky (P0.1)

- Post-#175 DESKTOP: MRQ stills — cabin lit, **void black sky**. **Fix:** `apply_mrq_pie_homestead_night_stack` + per-shot `reapply_night_environment_for_mrq_shot` (`mrq_pie_shot=True`); MRQ exposure ConsoleVariableSetting. KNOWN_ERRORS + CAPTURE_REDUNDANCY. Gap **OPEN** — DESKTOP re-prove.

## 2026-09-22 — PA-E P0.2/P0.3 shot2 framing + pose_source (cloud, post-#175)

- **P0.2:** `SHOT2_WIDE_STANDOFF_UU` (650,-1150,650) + `SHOT2_LOOKAT_XY_BIAS_UU` — modest strafe off (400,-1400) to reduce left pine on wide cabin frame.
- **P0.3:** `resolve_camera_transform` aims/validates vs anchor look target (`_look_target_for_pose_meta`); reaim-only no longer overwrites **`wide_cabin_anchor`** / **`wide_hero_anchor`** with **`in_level_camera_aim_at_bounds`**. KNOWN_ERRORS one-liner.

## 2026-09-22 — PA-E DESKTOP prove miss log (TOKEN-LEAN policy)

- Lead: **TOKEN-LEAN** known errors — harness one-line Cause→Avoid + KNOWN_ERRORS index (`pa-e-*` keys); six DESKTOP rows minified; no long narratives in agent memory. [automation-standards.mdc](../.cursor/rules/automation-standards.mdc) v1.9, [CAPTURE_REDUNDANCY.md](Automation/CAPTURE_REDUNDANCY.md), [KNOWN_ERRORS.md](KNOWN_ERRORS.md) § Index.

## 2026-09-22 — PA-E Arrange bounds relocate + cliff exclude (cloud)

- Post-#171 DESKTOP: Arrange **`in_level_camera_aim_at_bounds`** only (wrong **Y** vs P6_FIX doc; cliff actors poisoned centroid). **Fix:** [pa_e_shotlist_common.py](../Content/Python/pa_e_shotlist_common.py) — **`homestead_bounds_relocate`** / doc fallback **`set_actor_location`**; exclude **Cliff** from aim needles; **`aim_ok`** requires **`forward_ray_hits_dress_aabb`**. KNOWN_ERRORS + CAPTURE_REDUNDANCY + HARNESS P0-8. Gap **OPEN** — DESKTOP re-prove framing.

## 2026-09-22 — PA-E assert harden + Arrange aim_bounds (cloud, post-#170)

- DESKTOP after **#170**: **`capture_pass: true`** with global mean ~8.7 but ~93% black pixels (center ~0); Shot1 ≈ Shot2 scrap on frame edge. **Fix:** [pa_e_shotlist_common.py](../Content/Python/pa_e_shotlist_common.py) — center-crop + L&gt;8/L&gt;1 fractions + shot-pair MSE/hash; per-shot **`aim_bounds`** (exclude edge Fence/Rock), ray vs dress AABB in Arrange; MRQ **`reapply_night_environment_for_mrq_shot`** per job. Viewport `_validate_png` delegates to shared assert. KNOWN_ERRORS + CAPTURE_REDUNDANCY + HARNESS_ARRANGE P0-6/7. **Policy:** Lead-correction → harness (compact gates in-repo, CAPTURE_REDUNDANCY practice #5). Gap **OPEN** — DESKTOP should see **`capture_pass: false`** until lit homestead framing.

## 2026-09-22 — PA-E MRQ shot sequencing + luminance without Editor PIL (cloud)

- Post-#169 DESKTOP: shot1 rendered; shot2 **`Render already in progress`** (finalize on PNG too early); **`pil_unavailable`** false FAIL on lit PNG; LogPython still doubled (`print`+`unreal.log`). Fixes: executor-finished + `!is_rendering()` gate, `INTER_SHOT_DRAIN`, `_in_tick`/`_MAIN_ENTRY_ACTIVE`, stdlib PNG luminance + host Python fallback, `{shot_id}_{frame_number}` output names. KNOWN_ERRORS.

## 2026-09-22 — PA-E MRQ executor delegate arity + re-entry lock (cloud)

- Post-#168 DESKTOP: Arrange `ready: true` but MRQ failed `OnMoviePipelineExecutorFinished: expected 2, got 3`; duplicate shot1 / doubled LogPython from nested pre-tick. [capture_shotlist_mrq.py](../Content/Python/capture_shotlist_mrq.py): 2-arg finished handler per Epic 5.8 API, `PREPARING` lock, `_ACTIVE_DRIVER` guard, report `executor_start_error`. KNOWN_ERRORS. Gap **OPEN** — DESKTOP `execute_python_script("capture_shotlist.py")` after gate ready.

## 2026-09-22 — P0 PA-E Harness Arrange gate (cloud)

- **Problem:** Capture Act/Assert ran without Arrange (Phase 2 without light stack; CAM label ≠ aim; `load_level` dropped TMP lights; diagnostic JSON wrote before `homestead_night_environment`).
- **Fix:** `arrange_pa_e_shotlist()` / `assert_environment_ready()` in [pa_e_shotlist_common.py](../Content/Python/pa_e_shotlist_common.py) → `Saved/pa_e_arrange_gate.json`; blocks [capture_shotlist_mrq.py](../Content/Python/capture_shotlist_mrq.py), [capture_shotlist_viewport.py](../Content/Python/capture_shotlist_viewport.py); TMP re-seed in [vnp_night_tune_and_evidence.py](../Content/Python/vnp_night_tune_and_evidence.py). Docs: CAPTURE_REDUNDANCY § P0 Arrange, [HARNESS_ARRANGE_TASKLIST.md](Automation/HARNESS_ARRANGE_TASKLIST.md), KNOWN_ERRORS, AUTOMATION_GAPS. Formal shotlist gap **OPEN** until DESKTOP lit stills.

## 2026-09-22 — Universal testing preconditions + explicit PA-E TOD (cloud, PR #167)

- Lead lock-in: verify content in level, camera aim, lighting/TOD/view mode, then capture/inspect — stamped in CAPTURE_REDUNDANCY + `automation-standards.mdc` v1.5. PA-E capture: explicit **Night phase 2** per `Docs/00_SHOTLIST.md` Shot 1–2 via `apply_pa_e_shotlist_time_of_day`; report `viewport_prep.time_of_day` (replaces undocumented bare `night_phase`).

## 2026-09-22 — PA-E Lead prove loop + centroid diagnostic (cloud, PR #167)

- **Hard rule:** near-black stills ⇒ **`closed_fail: false`**, **`prove_loop_status: in_progress`** — inventory → aim at homestead bounds → capture/inspect → bug-fix; not a closed FAIL while Lead sees lit geometry in viewport. [pa_e_shotlist_common.py](../Content/Python/pa_e_shotlist_common.py): `LEAD_PROVE_LOOP`, bounds-aim `resolve_camera_transform`, `summarize_capture_report`, `write_homestead_capture_diagnostic`. New [pa_e_homestead_capture_diagnostic.py](../Content/Python/pa_e_homestead_capture_diagnostic.py) for DESKTOP. MRQ report: `lead_prove_loop`, `homestead_diagnostic_path`. Docs: CAPTURE_REDUNDANCY 4-step bar, AUTOMATION_GAPS, KNOWN_ERRORS, DEFECT. Gap **OPEN** — DESKTOP lit stills + `ok: true`; no cloud PASS.

## 2026-09-22 — PA-E MRQ + Lead capture clarification (cloud)

- MRQ remains primary; **quality bar unchanged** — DESKTOP PASS requires **lit non-black homestead** stills (luminance gates), not file-exists-only. Near-black AL PNGs while Lead sees viewport content = **OPEN viewport capture bug** (pose/game-view/pilot/buffer). Hardened MRQ: CAM possessable binding, camera-cut preroll + `MoviePipelineAntiAliasingSetting` warm-up, deferred pass enabled, per-shot `editor_prep` diagnostics + report `desktop_conductor_checklist`. Docs: CAPTURE_REDUNDANCY prove bar, AUTOMATION_GAPS AL bug row, KNOWN_ERRORS, DEFECT.

## 2026-09-22 — PA-E MRQ one-frame shotlist capture (cloud, post-#166)

- Lead-approved rung-1 pivot after post-#166 DESKTOP: AL pretick wrote **black/near-black** PNGs (`ok: false`). Added [capture_shotlist_mrq.py](../Content/Python/capture_shotlist_mrq.py) + canonical [capture_shotlist.py](../Content/Python/capture_shotlist.py); [pa_e_shotlist_common.py](../Content/Python/pa_e_shotlist_common.py); enabled **MovieRenderPipeline** / **MovieRenderPipelineEditor** / **SequencerScripting** in `HomeWorld.uproject`. Updated CAPTURE_REDUNDANCY, AUTOMATION_GAPS, KNOWN_ERRORS. Gap **OPEN** — DESKTOP re-prove MRQ on **DESKTOP-21CT3H0** (Safe-Build after plugin enable); **no PASS claim**.

## 2026-09-22 — PA-E pretick wait probe + re-entry fix (cloud)

- Post-#165 DESKTOP (~15:01 ET): pretick responsive, **Shot1** ~38KB on disk, report **`file_missing`** (wait probe **`MIN_BYTES`**, nested **`POSED`** re-entry). [capture_shotlist_viewport.py](../Content/Python/capture_shotlist_viewport.py): **`PREPARING`** lock, **`_find_fresh_capture_path`** on timeout/final drain, **`MIN_BYTES`** validation-only. KNOWN_ERRORS + AUTOMATION_GAPS + CAPTURE_REDUNDANCY note. Gap **OPEN** — DESKTOP re-prove.

## 2026-09-22 — PA-E DESKTOP prove FAIL post-#163 (docs only, blocking wait)

- **`C:\dev\HomeWorld`**, ~14:45–14:53 ET after **#163** @ `d0d074d`: MCP **`capture_shotlist_viewport.py`** — level load OK; Shot 1+2 AutomationLibrary **`kwargs_delay_force_gv`**; **`task_done: false`** (~90s poll each); **no PNG** (~120s wait); Editor **Not Responding**; killed in **`final_drain`**; **no** **`pa_e_capture_report.json`**; **no** new **`Saved/Screenshots/PA_E/`** stills. Research logged: async HighResShot + **main-thread `time.sleep` poll** footgun → **`register_slate_pre_tick_callback`** (rung 1). Merged **#164** @ `aac7893`. KNOWN_ERRORS + AUTOMATION_GAPS + [DEFECT_PA_E](../Docs/qa/DEFECT_PA_E_shot_capture_automation.md). Gap **OPEN** — **no PASS claim**.

## 2026-09-22 — PA-E Slate pre-tick capture wait (cloud, #165)

- [capture_shotlist_viewport.py](../Content/Python/capture_shotlist_viewport.py): **rung-1 fix** for post-#163 failure — **`register_slate_pre_tick_callback`** state machine + keep_alive; no blocking sleep after `take_high_res_screenshot`. Report `primary_path: automation_library_slate_pretick`. [CAPTURE_REDUNDANCY.md](Automation/CAPTURE_REDUNDANCY.md) § Shotlist wait updated. Gap **OPEN** until DESKTOP re-proves **pretick** path (not “AL unproven forever”).

## 2026-09-22 — PA-E shotlist AutomationLibrary primary (cloud, rung 1)

- [capture_shotlist_viewport.py](../Content/Python/capture_shotlist_viewport.py): **proven-results-first** — **`AutomationLibrary.take_high_res_screenshot`** primary with Slate tick spacing (one request per shot, ~120s file wait, ~75s final drain); **retired** multi-form console **HighResShot** × **330s** ladder. [CAPTURE_REDUNDANCY.md](Automation/CAPTURE_REDUNDANCY.md) § Shotlist aligned; MRQ one-frame noted as next rung-1 option if AL fails. Gap **OPEN** — DESKTOP re-prove; no PASS claim.

## 2026-09-22 — Universal tooling practice suite (Lead lock-in, docs only)

- Lead lock-in for **any** automation gap: (1) Docs-first, (2) Proven-results first, (3) Research on dead-ends before SCOUT/BUILD/Lead ping, (4) Gated ladder — [CAPTURE_REDUNDANCY.md](Automation/CAPTURE_REDUNDANCY.md) (canonical universal doc; shotlist instance only); [AUTOMATION_GAPS.md](Automation/AUTOMATION_GAPS.md); [automation-standards.mdc](../.cursor/rules/automation-standards.mdc) v1.4. Capture arc cited only under Examples (non-exhaustive).

## 2026-09-22 — PA-E DESKTOP prove FAIL post-#159 (docs only)

- **`C:\dev\HomeWorld`**, ~12:51–13:01 ET after **#159**: console **HighResShot** logged for Shot 1/2 + viewport focus OK → **no PNG** (~120s each); AutomationLibrary fallback **`task_done: false`**, **`file_produced_by: null`**; MCP **600s timeout** during `final_drain`; **no** new **`pa_e_capture_report.json`**; **no** new **`Shot*.png`** under **`Saved/Screenshots/PA_E/`**. KNOWN_ERRORS + AUTOMATION_GAPS + [DEFECT_PA_E](../Docs/qa/DEFECT_PA_E_shot_capture_automation.md). Gap **OPEN**; pre-#161 rung-1 variants exhausted on that prove — **#161** adds doc-ordered ladder + **330s** wait; DESKTOP re-prove still required. **No PASS claim.**

## 2026-09-22 — PA-E DESKTOP prove FAIL post-#157 (docs only)

- **`C:\dev\HomeWorld`**, ~12:46 ET: **`Saved/pa_e_capture_report.json`** **`ok: false`** — **`AutomationEditorTask` stall**, **`file_missing`**, **`pil_available: false`**. Document-only append. Gap **OPEN**.

## 2026-09-22 — Epic doc-aligned HighResShot + AutomationLibrary (cloud, rung 1)

- [capture_shotlist_viewport.py](../Content/Python/capture_shotlist_viewport.py) / [capture_viewport.py](../Content/Python/capture_viewport.py): **`filename=` before resolution** console ladder with per-form **330s** file wait; `Saved/Screenshots/Windows`; `finish_loading_before_screenshot`, `delay` on `take_high_res_screenshot`, Lit via `set_editor_viewport_view_mode`; inter-shot Slate settle. Implements Lead **docs-first** policy ([#160](https://github.com/XylarDark/HomeWorld/pull/160) / [CAPTURE_REDUNDANCY.md](Automation/CAPTURE_REDUNDANCY.md) § Docs-first); FOCUSVIEWPORT unverified; KNOWN_ERRORS / AUTOMATION_GAPS / DEFECT_PA_E. Merged **#161** @ `89eaf94`. Gap **OPEN** — DESKTOP re-prove required.

## 2026-09-22 — Docs-first console/API policy (Lead lock-in, cloud)

- Lead policy: read official Epic/vendor docs before hardening console commands / Editor Python APIs — [docs/Automation/CAPTURE_REDUNDANCY.md](Automation/CAPTURE_REDUNDANCY.md) § Docs-first; [AUTOMATION_GAPS.md](Automation/AUTOMATION_GAPS.md) + research log; [.cursor/rules/automation-standards.mdc](../.cursor/rules/automation-standards.mdc). Motivating miss: **HighResShot** parameter order vs [Taking Screenshots](https://dev.epicgames.com/documentation/en-us/unreal-engine/taking-screenshots-in-unreal-engine). Merged **#160** (docs-only); script alignment in **#161**.

## 2026-09-22 — PA-E console HighResShot primary (cloud, rung 1)

- DESKTOP after #157: AutomationLibrary **AutomationEditorTask** stall → both shots `file_missing`. [capture_shotlist_viewport.py](../Content/Python/capture_shotlist_viewport.py): console **HighResShot** primary (multi cmd forms), viewport focus + Slate tick pump, AutomationLibrary fallback only; `file_produced_by` in report. [capture_viewport.py](../Content/Python/capture_viewport.py) same order. KNOWN_ERRORS + AUTOMATION_GAPS note. Gap **OPEN** — no DESKTOP PASS claim.

## 2026-09-22 — PA-E capture abspath + stale purge + luminance gate (cloud, rung 1)

- DESKTOP re-prove after #156 still FAIL (relative paths, Shot1 missing, Shot2 stale false-pass). [capture_shotlist_viewport.py](../Content/Python/capture_shotlist_viewport.py): `abspath(project_dir)`; purge PNGs before capture; PIL luminance required; mtime ≥ capture_since; multi game-view API attempts; AutomationEditorTask poll. KNOWN_ERRORS + AUTOMATION_GAPS note. Gap **OPEN** — no DESKTOP PASS claim.

## 2026-09-22 — PA-E capture absolute path + async drain (cloud, rung 1)

- [capture_shotlist_viewport.py](../Content/Python/capture_shotlist_viewport.py): absolute `Saved/Screenshots/PA_E/` for HighResShot; Engine Win64/PA_E copy fallbacks; 120s stable-size wait + final drain before keep_alive disarm. Supersedes conflicted PR #155. Gap **OPEN** — no DESKTOP PASS claim.

## 2026-09-22 — Capture redundancy ladder + shotlist viewport script (cloud)

- Lead policy: [docs/Automation/CAPTURE_REDUNDANCY.md](Automation/CAPTURE_REDUNDANCY.md) — **gated global ladder** (rung 1 built-in/repo; rung 2 **`APPROVE TOOL SCOUT`**; rung 3 **`APPROVE TOOL BUILD`**; no auto-install / no unprompted stacks); shotlist PA-E uses rung-1 script; ban host ImageGrab for shotlist PASS.
- [Content/Python/capture_shotlist_viewport.py](../Content/Python/capture_shotlist_viewport.py) — PA-E Shot 1/2 on `L_VS_MVP_Markers`, `Saved/pa_e_capture_report.json`, CopyToBox desktop copy.
- [DEFECT_PA_E](../Docs/qa/DEFECT_PA_E_shot_capture_automation.md) + AUTOMATION_GAPS PA-E row → ladder + script; gap **OPEN** until DESKTOP prove. **No shotlist PASS claim.**

## 2026-09-22 — PA-E close stamp (cloud, docs)

- Lead **`APPROVE PA-E`**, 2026-09-22 ET → [Docs/32_PROTOTYPE_ASSETS.md](../Docs/32_PROTOTYPE_ASSETS.md) **CLOSED / COMPLETE** (whole PA track); [Docs/handoffs/PA_E_SHOTS.md](../Docs/handoffs/PA_E_SHOTS.md) **APPROVED / CLOSED**; [PA_D_IMPORT_PLACE.md](../Docs/handoffs/PA_D_IMPORT_PLACE.md) **CLOSED**; `DECISIONS.md` row; thin README / PHASE_BOARD / SESSION_* updates. Place evidence **`C:\dev\HomeWorld\Saved\pa_d_place_report.json`** **accepted**. Formal Shot 1/2 stills **deferred/accepted** — **not** PASS from `HomeWorld_PA_E` ImageGrab. **No `.uasset`.**

## 2026-09-22 — SS-B close stamp + PA-E ImageGrab miss (cloud, docs)

- Lead **`APPROVE SS-B`** (2026-09-21 ET) → `Docs/31_SPIRIT_STEALTH_FEEL.md` **CLOSED / COMPLETE**; `Docs/handoffs/SS_B_STEALTH_FEEL.md` **APPROVED / CLOSED**; `Docs/canon/DECISIONS.md` row; thin README / PHASE_BOARD / SESSION_* updates. Supersedes conflicted PR #139. **DESKTOP** STEALTH PIE greps **deferred/accepted** — not stamped PASS. **No APPROVE PA-E.**
- Conductor remote PA-E Shot 1/2 host **ImageGrab** (2026-09-22 ET, Lead away): `Shot1_lookout.png` (~525KB) = Grok Bot chat/desktop; `Shot2_cabin_garden.png` (~376KB) = Editor chrome — not shotlist-grade. Strengthened KNOWN_ERRORS / AUTOMATION_GAPS / [DEFECT_PA_E_shot_capture_automation.md](../Docs/qa/DEFECT_PA_E_shot_capture_automation.md). Evidence folder `C:\Users\User\Desktop\HomeWorld_PA_E\`. **Stop grinding remote ImageGrab for PA-E**; Lead manual viewport stills.

## 2026-09-22 — SWARM_OPS §11 operational memory backfill (cloud)

- Docs-only: [docs/KNOWN_ERRORS.md](KNOWN_ERRORS.md) + [docs/Automation/AUTOMATION_GAPS.md](Automation/AUTOMATION_GAPS.md) entries for GC→PA DESKTOP failures (2026-09-20–22); [Docs/qa/DEFECT_PA_E_shot_capture_automation.md](../Docs/qa/DEFECT_PA_E_shot_capture_automation.md); [PA_D_IMPORT_PLACE.md](../Docs/handoffs/PA_D_IMPORT_PLACE.md) Blockers pointer. **No APPROVE PA-E**; Lead still manual Shot 1/2.

## 2026-09-22 — PA-D APPROVED + place script (cloud)

- Lead **`APPROVE PA-D`**, 2026-09-22 ET → [Docs/32_PROTOTYPE_ASSETS.md](../Docs/32_PROTOTYPE_ASSETS.md) **PA-D IN PROGRESS**; [Docs/handoffs/PA_D_IMPORT_PLACE.md](../Docs/handoffs/PA_D_IMPORT_PLACE.md) **APPROVED** (awaiting DESKTOP evidence). `DECISIONS.md` + `PHASE_BOARD` + `Docs/README` minimal update. **No `.uasset`**. PA track **not CLOSED** (PA-E locked).
- PR #145: `Content/Python/place_vs_mvp_pa_d.py` (cliffs, planters, fence, path stones + `place_vs_mvp_dress` refresh); `place_vs_mvp_dress.py` SM_Cabin exact + Pine S/M/L. DESKTOP run after batch_import.

## 2026-09-22 — PA-C tranche-2 land (cloud)

- Tranche-2 FBX in `AssetCreation/Exports/Homestead/`: upgraded `SM_Cabin.fbx`, `SM_Glider_Perch.fbx`; new path stones ×3, planters ×3, `SM_Garden_Fence_Seg.fbx`. [Docs/handoffs/PA_C_TRANCHE2.md](../Docs/handoffs/PA_C_TRANCHE2.md) · [PA_C_BLENDER.md](../Docs/handoffs/PA_C_BLENDER.md). **Docs/32** tranche-2 **DONE**; **PA-D OPEN** (no Lead **`APPROVE PA-D`**). No `.uasset`. PA track **not CLOSED** (optional island rim).

## 2026-09-22 — PA-C tranche-1 land (cloud)

- Lead **`APPROVE PA-C`**, 2026-09-22 ET → [Docs/32_PROTOTYPE_ASSETS.md](../Docs/32_PROTOTYPE_ASSETS.md) **PA-C IN PROGRESS** (tranche-1 cliffs+pines **DONE**); [Docs/handoffs/PA_C_BLENDER.md](../Docs/handoffs/PA_C_BLENDER.md) + [PA_C_TRANCHE1.md](../Docs/handoffs/PA_C_TRANCHE1.md). FBX: `SM_Cliff_{LookoutFace,CabinFace,Rear}.fbx` + upgraded `SM_Pine_Homestead.fbx` in `AssetCreation/Exports/Homestead/`. **No `.uasset`**. PA track **not CLOSED** (cabin→path→planters→fence→glider→rim remain).

## 2026-09-22 — PA-A gap audit APPROVED (cloud)

- Lead **`APPROVE PA-A`**, 2026-09-22 ET → [Docs/32_PROTOTYPE_ASSETS.md](../Docs/32_PROTOTYPE_ASSETS.md) **PA-A CLOSED / COMPLETE** · **PA-C OPEN / IN PROGRESS ready**; [Docs/handoffs/PA_A_GAP_AUDIT.md](../Docs/handoffs/PA_A_GAP_AUDIT.md) **APPROVED / CLOSED**. Gap table + Blender queue stamped. **PA track not CLOSED** (no PA-C approve / no PA-E).

## 2026-09-22 — PA STRATEGY APPROVED (cloud)

- Lead **`APPROVE PA STRATEGY — homestead kit only`**, 2026-09-22 ET → [Docs/32_PROTOTYPE_ASSETS.md](../Docs/32_PROTOTYPE_ASSETS.md) **PA STRATEGY APPROVED** · **PA-A OPEN**; [Docs/handoffs/PA_STRATEGY.md](../Docs/handoffs/PA_STRATEGY.md) **APPROVED / CLOSED** (strategy stamp). Scope: homestead kit only. PR #141. **PA-A gap audit not started.**

## 2026-09-22 — PA-0 prototype assets strategy (cloud, OPEN)

- PA-0 docs-only: kit plate + sidecar in `AssetCreation/RefImages/` and `Docs/refs/ai/` (superseded by approve stamp above).

## 2026-09-22 — SS-B HUD UE 5.8 compile fix (cloud)

- PR [#147](https://github.com/XylarDark/HomeWorld/pull/147): `HomeWorldHUD.cpp` — protected `Canvas` (lambda in `DrawHUD`), `DrawTile` + `BLEND_Translucent` + `SetDrawColor`, `bSpiritHiddenCue` rename. Rebased on main (PA-D #146). DESKTOP Safe-Build verify pending.

## 2026-09-22 — SS-B spirit stealth feel (cloud, IN PROGRESS)

- Lead **`APPROVE SS-B STRATEGY`** (2026-09-21 ET) → [Docs/31_SPIRIT_STEALTH_FEEL.md](../Docs/31_SPIRIT_STEALTH_FEEL.md) **SS-B STRATEGY APPROVED / SS-B IN PROGRESS**; [Docs/handoffs/SS_B_STEALTH_FEEL.md](../Docs/handoffs/SS_B_STEALTH_FEEL.md); `DECISIONS.md` SS-B strategy row. **SS-B not stamped APPROVED.**
- C++: stealth feel cues on `HomeWorldSpiritStealthComponent`, HUD alert bar, `HomeWorldSpiritNpcTorchCarrier`, `place_vs_mvp_ss_b_feel.py`. DESKTOP greps `STEALTH:*` + PIE feel pending.

## 2026-09-22 — DS-A track CLOSED (docs stamp, cloud)

- Lead **`APPROVE DS-A`** (2026-09-21 ET; chat truncated **`APPROVE DS-`**) → `Docs/30_DEMO_SPINE.md` **CLOSED / COMPLETE**; `Docs/handoffs/DS_A_VISIBLE_HEARTH.md` **APPROVED / CLOSED**; `Docs/canon/DECISIONS.md` row. DS-A on main `7d579f9` (PR #136). **PROVE-BATCH** DESKTOP walk/greps **deferred** — not stamped PASS. Next track Lead TBD.

## 2026-09-22 — SS-A spirit stealth stubs (cloud, IN PROGRESS)

- Lead **`SS-A`** → **`APPROVE SS STRATEGY`**; [Docs/25_SPIRIT_STEALTH_IMPL.md](../Docs/25_SPIRIT_STEALTH_IMPL.md) + [Docs/handoffs/SS_A_STEALTH_STUBS.md](../Docs/handoffs/SS_A_STEALTH_STUBS.md); `DECISIONS.md` SS strategy row. SS-A **not** stamped APPROVED.
- C++: `HomeWorldSpiritLitVolume`, `HomeWorldSpiritStealthComponent`, `place_vs_mvp_ss_stealth.py`, cheats `hw.Stealth.Status` / `hw.Stealth.ForceLit`. DESKTOP greps `STEALTH:*` pending.

## 2026-09-21 ET — MV-A track CLOSED (docs stamp, cloud)

- Lead **`APPROVE MV-A`** → `Docs/24_MOVEMENT_IMPL.md` **CLOSED / COMPLETE**; `Docs/handoffs/MV_A_TRAVERSAL.md` **APPROVED / CLOSED**; `Docs/canon/DECISIONS.md` row. MV-A on main `349d3e4` (PR #130). **SS-A** (spirit stealth) separate — not part of MV close. Next track TBD — not in this PR.

## 2026-09-22 ET — SPIRIT_STEALTH bible LOCKED (docs-only, cloud)

- Lead locks 2026-09-21 ET chat: spirit **hidden default**, torch reveal (NPC / campfire / spirit torch), found-out **A2 alert** (not crouch, not kidnap, not kill-on-detect); body vs spirit torch split.
- Added `Docs/SPIRIT_STEALTH_BIBLE.md`, `Docs/SPIRIT_STEALTH_IMPL_PROMPT.md`; amends `DAYNIGHT_BIBLE`, `MOVEMENT_BIBLE`, `Docs/canon/DECISIONS.md`, `DO_NOT.md`, `VERBS.md`; MV-A (#130) **excludes** SS-A — merged main `19d0ca6` (PR #131).

## 2026-09-22 ET — MV-A traversal stubs (cloud, IN PROGRESS)

- Lead **`MV-A`** chat → **`APPROVE MV STRATEGY`**; [Docs/24_MOVEMENT_IMPL.md](../Docs/24_MOVEMENT_IMPL.md) + [Docs/handoffs/MV_A_TRAVERSAL.md](../Docs/handoffs/MV_A_TRAVERSAL.md); `DECISIONS.md` MV strategy row (alongside SPIRIT_STEALTH lock). MV-A **not** stamped APPROVED (Lead closes later).
- C++: `HomeWorldTraversalComponent` (sprint, mantle/vault, spirit blink, mount boost, soft fall reset on one CMC); dusk blocks FALLBACK glide start; cheats `hw.Move.Mantle` / `hw.Move.Blink`. PR #130; DESKTOP Safe-Build + PIE prove pending.

## 2026-09-21 ET — SS-A track CLOSED (docs stamp, cloud)

- Lead **`APPROVE SS-A`** → `Docs/25_SPIRIT_STEALTH_IMPL.md` **CLOSED / COMPLETE**; `Docs/handoffs/SS_A_STEALTH_STUBS.md` **APPROVED / CLOSED**; `Docs/canon/DECISIONS.md` row. SS-A on main `7bc577f` (PR #133). Next: Lead-named track TBD — not in this PR.

## 2026-09-21 ET — CD-A track CLOSED (docs stamp, cloud)

- Lead **`APPROVE CD-A`** → `Docs/23_COMBAT_DREAM_IMPL.md` **CLOSED / COMPLETE**; `Docs/handoffs/CD_A_STUBS.md` **APPROVED / CLOSED**; `Docs/canon/DECISIONS.md` row. CD-A on main `50faeab` (PR #128). Next: **MV-A** TBD — not in this PR.

## 2026-09-21 ET — GC-C track CLOSED (docs stamp, cloud)

- Lead **`APPROVE GC-C`** → `Docs/22_GATHER_CRAFT_IMPL.md` **CLOSED / COMPLETE**; `Docs/handoffs/GC_C_PLACEHOLDERS.md` **APPROVED / CLOSED**; `Docs/canon/DECISIONS.md` row. GC on main `7061e18` (PR #126). Next: CD-A / MV-A TBD — not in this PR.

## 2026-09-21 ET — GC-C placeholder volumes (cloud)

- GC-C: `AHomeWorldGcPlaceholderVolume` + `EHomeWorldGcPlaceholderKind`; overlap logs `PLACEHOLDER:*`; cottage rooms gated on `IsCottageUnlocked()`; `place_vs_mvp_gc_placeholders.py` (`GP_PH_*`).
- Docs: GC-B **CLOSED** in `Docs/22` + `DECISIONS.md` (Lead **`APPROVE GC-B`** 2026-09-21 ET); GC-C **IN PROGRESS**; handoff `Docs/handoffs/GC_C_PLACEHOLDERS.md`. GC-C not stamped APPROVED — pending Lead **`APPROVE GC-C`**.

## 2026-09-21 ET — GC-B craft spine (cloud)

- GC-B: `UHomeWorldCraftSubsystem`, `AHomeWorldCraftStation`, interact + Stored-first spend; `place_vs_mvp_gc_craft.py` (`GP_Craft_Hub`); `hw.Craft.*` cheats.
- Docs: GC-A **CLOSED** in `Docs/22_GATHER_CRAFT_IMPL.md`; handoff `Docs/handoffs/GC_B_CRAFT_SPINE.md`; `DECISIONS.md` GC-A row. GC-B not stamped APPROVED.

## 2026-09-21 ET — GATHER_CRAFT bible locked (cloud)

- Added `Docs/GATHER_CRAFT_BIBLE.md` + `Docs/GATHER_CRAFT_IMPL_PROMPT.md` (Lead A1/B1/C1/D1 locks).
- Appended `Docs/canon/DECISIONS.md`; recipe rows + flint/grass aliases in `SCHEMA.md`; thin updates to `DO_NOT.md`, `VERBS.md`, `HOMESTEAD_BIBLE.md`, `canon/README.md`, `Docs/README.md`. Docs-only.

## 2026-09-20 ET — CAMERA_BIBLE locked (canon pointer)

Lead paste: added `Docs/CAMERA_BIBLE.md` (Galaxy identity / WoW orbit control / iso systems / FP intimacy). `Docs/canon/DECISIONS.md` row; `Docs/canon/README.md` + `FEEL.md` pointers. No gameplay code.

## 2026-09-19 ET — DevHarness Taste Profiler sync + HomeWorld pin

DevHarness PR #32 merged (`0eafcfb`): extras `taste-profiler` + profile templates; taste-gate read-first. HomeWorld pin bumped; Docs/29 CLOSED work committed with profile/skills.

## 2026-09-19 ET — APPROVE TP-E / Docs/29 CLOSED

Lead **`APPROVE TP-E`**, 2026-09-19 ET. Docs/29 Taste Profiler **CLOSED / COMPLETE** (TP-A…E). Profile + skills stay live. PHASE_BOARD: next track TBD — Lead names it or Taste Gate (do not invent). DevHarness sync = separate chore.

## 2026-09-19 ET — APPROVE TP-D / TP-E GATE READY

Lead **`APPROVE TP-D`**, 2026-09-19 ET. Dry-run prove accepted; session candidate promoted (Skip invent / product still TBD). Docs/29 **ACTIVE** — [TP_E_CLOSE.md](../Docs/handoffs/TP_E_CLOSE.md) **GATE READY**. PENDING Lead **`APPROVE TP-E`**.

## 2026-09-19 ET — Docs/29 Taste Profiler ACTIVE (TP-A…D)

Lead implement-plan unlocked Taste Profiler. Filed [29_TASTE_PROFILER.md](../Docs/29_TASTE_PROFILER.md); seeded [taste-profile.md](../docs/human-use/taste-profile.md); skills `taste-profiler` + taste-gate read-first; prove [TP_D_PROVE.md](../Docs/handoffs/TP_D_PROVE.md). PHASE_BOARD **ACTIVE**; PENDING Lead **`APPROVE TP-D`** then **`APPROVE TP-E`**.

## 2026-09-19 ET — DevHarness Taste Gates sync + HomeWorld pin

DevHarness PR #31 merged (`398ce0b`): extras skill `taste-gate` + `docs/human-use/taste-gates.md`. HomeWorld pin bumped; local `.agents/skills/taste-gate` activated. Docs/26–28 + NF2 ship in same HomeWorld push.

## 2026-09-19 ET — APPROVE TG-E / Docs/28 CLOSED

Lead **`APPROVE TG-E`**, 2026-09-19 ET. Docs/28 Taste Gates **CLOSED / COMPLETE** (TG-A…E). Harness remains: skill `taste-gate` + [taste-gates.md](../docs/human-use/taste-gates.md). PHASE_BOARD: next track TBD — Lead names it or Taste Gate (do not invent).

## 2026-09-19 ET — APPROVE TG-D / TG-E GATE READY

Lead **`APPROVE TG-D`**, 2026-09-19 ET. Dry-run prove accepted ([TG_D_PROVE.md](../Docs/handoffs/TG_D_PROVE.md)); queue entry resolved. Docs/28 still **ACTIVE** — [TG_E_CLOSE.md](../Docs/handoffs/TG_E_CLOSE.md) **GATE READY**. PENDING Lead **`APPROVE TG-E`** to close. Next product track still TBD (no invent).

## 2026-09-19 ET — Docs/28 Taste Gates ACTIVE (TG-A…D)

Lead unlocked Taste Gates research + implement-plan. Filed [28_TASTE_GATES.md](../Docs/28_TASTE_GATES.md) (research digest + strategy). Spike: skill `taste-gate`, [taste-gates.md](../docs/human-use/taste-gates.md), rule pointer in 07-ai-agent-behavior. Dry-run prove [TG_D_PROVE.md](../Docs/handoffs/TG_D_PROVE.md) + `Saved/taste_gates_pending.json`. PHASE_BOARD **ACTIVE**; PENDING Lead **`APPROVE TG-D`** then **`APPROVE TG-E`** to close. Park note superseded — track unparked to ACTIVE.

## 2026-09-19 ET — APPROVE NF2-E / Docs/27 CLOSED

Lead **`APPROVE NF2-E`**, 2026-09-19 ET. Docs/27 Night Feel Build **CLOSED / COMPLETE** (NF2-A…E). Soft form-swap glow + night lookdev shipped; sound assets deferred. PHASE_BOARD: next = **Taste Gates** harness research (parked) or Lead-named track.


## 2026-09-19 ET — APPROVE NF2-D

Lead **`APPROVE NF2-D`**, 2026-09-19 ET. Sound/particle assign deferred (glow-only). **NF2-E OPEN** — [NF2_E_CLOSE.md](../Docs/handoffs/NF2_E_CLOSE.md). PENDING Lead **`APPROVE NF2-E`** to close Docs/27 → Taste Gates research.


## 2026-09-19 ET — APPROVE NF2-C

Lead **`APPROVE NF2-C`**, 2026-09-19 ET. AD still review **CLOSED**. **NF2-D OPEN** — optional SoftFormSwapSound/particle assign ([NF2_D_SOUND_POLISH.md](../Docs/handoffs/NF2_D_SOUND_POLISH.md)).


## 2026-09-19 ET — APPROVE NF2-B

Lead **`APPROVE NF2-B`**, 2026-09-19 ET. Night lookdev **CLOSED** (partial PNG pack accepted). **NF2-C OPEN** — AD still review [NF2_C_AD_STILLS.md](../Docs/handoffs/NF2_C_AD_STILLS.md).


## 2026-09-19 ET — NF2-B implement GATE READY

Night lookdev Cmd batch: VS_MVP load, MegaLights/Fog SSS, cameras bound 1/2/5; `shot5_spirit.png` on disk; shot1/2 PNG gap logged. Handoff [NF2_B_NIGHT_LOOKDEV.md](../Docs/handoffs/NF2_B_NIGHT_LOOKDEV.md). PENDING Lead **`APPROVE NF2-B`**.


## 2026-09-19 ET — APPROVE NF2-A

Lead **`APPROVE NF2-A`**, 2026-09-19 ET. Soft form-swap feedback **CLOSED**. **NF2-B OPEN** (night lookdev + Shot 1/2/5 evidence). PHASE_BOARD Docs/27 ACTIVE.


## 2026-09-19 ET — PARKED: Taste Gates (post-Docs/27 research)

~~Parked~~ → **ACTIVE** 2026-09-19 — see Docs/28 block above. Original vision: harness detects taste limits and queries the human. Ground in [OWNERSHIP.md](../docs/human-use/OWNERSHIP.md).


## 2026-09-19 ET — Docs/27 Night Feel Build ACTIVE (NF2-A)

Lead asked to proceed with a new phase track. Filed [27_NIGHT_FEEL_BUILD.md](../Docs/27_NIGHT_FEEL_BUILD.md) (NF2-A…E) from Docs/26 taste canon. NF2-A: soft form-swap glow + `NF2:` logs in `HomeWorldCharacter`; handoff [NF2_A_FORM_SWAP.md](../Docs/handoffs/NF2_A_FORM_SWAP.md). PHASE_BOARD **ACTIVE**. PENDING Safe-Build + DESKTOP PIE greps → Lead **`APPROVE NF2-A`**.


## 2026-09-19 ET — APPROVE NF-A / Docs/26 CLOSED

Lead **`APPROVE NF-A`**, 2026-09-19 ET. Docs/26 Night Feel **CLOSED / COMPLETE**. Taste targets remain canon; VNP/WTR night evidence accepted as baseline; soft dusk/dawn VFX+audio sting backlog for explicit implement ask. PHASE_BOARD: next product track TBD.


## 2026-09-19 ET — Docs/26 Night Feel taste gate

Taste interview complete: night lookdev + “safe home above a living world” + dusk/dawn NightMix + soft VFX/audio; thin slice **NF-A**. Track **Docs/26 Night Feel** — [26_TASTE_NEXT.md](../Docs/26_TASTE_NEXT.md). PHASE_BOARD **OPEN**. PENDING implement + Lead **`APPROVE NF-A`**.


## 2026-09-19 ET — Docs/25 WTR implement (A–E)

Workspace & Tooling Refine on `feat/ue58-workspace-tooling`: Docs/25 matrix; [U58F_F](../Docs/handoffs/U58F_F_MCP_DECISION.md) Epic vs UnrealMCP capability matrix (**keep UnrealMCP**); pine `.uasset` via Cmd batch; evidence binds `CAM_Hero`/`CAM_CabinClose`/`CAM_PortalNight`; keep_alive pattern; PCG introspect 5.8 refresh; PVE/Mesh CVars notes; [UE58_TECH](../docs/UE/UE58_TECH.md) DESKTOP stability playbook. PHASE_BOARD WTR **CLOSING**.


## 2026-09-19 ET — APPROVE RS-E / Docs/21 CLOSED

Lead **`APPROVE RS-E`**, 2026-09-19 ET. Docs/21 Reap & Sow **CLOSED / COMPLETE** (RS-A…E). Special cross-bonus + `hw.RS.*` accepted. PHASE_BOARD: no active product phase — next track TBD (Lead gate). Do not reopen RS/VP2/D19.


## 2026-09-19 ET — RS-E implement (GATE READY)

RS-E special cross-bonus filed: [place_vs_mvp_rs_special_site.py](../Content/Python/place_vs_mvp_rs_special_site.py), PlayerState RS flags + `hw.RS.CollectDayBonus` / `CollectNightBonus` / `CrossBonusStatus`, [RS_E_SPECIAL.md](../Docs/handoffs/RS_E_SPECIAL.md). PHASE_BOARD **RS-E GATE READY** — PENDING Lead **`APPROVE RS-E`** (closes Docs/21).


## 2026-09-19 ET — APPROVE RS-D

Lead **`APPROVE RS-D`**, 2026-09-19 ET. Filed [place_vs_mvp_rs_humanoid_camp.py](../Content/Python/place_vs_mvp_rs_humanoid_camp.py) + [RS_D_HUMANOID_CAMP.md](../Docs/handoffs/RS_D_HUMANOID_CAMP.md) (`GP_RS_HumanoidCamp` / `_Dream` / `_Collect`). MCP offline — DESKTOP PIE deferred accept. **RS-E OPEN** (special cross-bonus; closes Docs/21 on **`APPROVE RS-E`**).


## 2026-09-19 ET — APPROVE RS-C

Lead **`APPROVE RS-C`**, 2026-09-19 ET. Filed [place_vs_mvp_rs_animal_den.py](../Content/Python/place_vs_mvp_rs_animal_den.py) + [RS_C_ANIMAL_DEN.md](../Docs/handoffs/RS_C_ANIMAL_DEN.md) (`GP_RS_AnimalDen` BeastPad + `GP_RS_AnimalDen_Dream` stub). MCP offline — DESKTOP PIE deferred accept. **RS-D OPEN** (humanoid camp).


## 2026-09-19 ET — APPROVE RS-B

Lead **`APPROVE RS-B`**, 2026-09-19 ET. Filed [place_vs_mvp_rs_material_sites.py](../Content/Python/place_vs_mvp_rs_material_sites.py) + [RS_B_MATERIALS.md](../Docs/handoffs/RS_B_MATERIALS.md) (`GP_RS_Tree/Rock/Flower` day piles + sow TargetPoints). Editor MCP offline — DESKTOP PIE deferred accept. **RS-C OPEN** (animal den).


## 2026-09-19 ET — APPROVE RS-A

Lead **`APPROVE RS-A`**, 2026-09-19 ET. Canon stamp **CLOSED**. **RS-B OPEN** (material triad: trees / rocks / flowers on VS_MVP path). PHASE_BOARD + Docs/21 updated. Next: implement RS-B then **`APPROVE RS-B`**.


## 2026-09-19 ET — APPROVE RS STRATEGY + RS-A canon filed

Lead **`APPROVE RS STRATEGY`**, 2026-09-19 ET. [Docs/21_REAP_SOW.md](../Docs/21_REAP_SOW.md) strategy **APPROVED**. **RS-A** canon stamp filed: [Docs/01_GDD_MVP.md](../Docs/01_GDD_MVP.md) fantasy + §3.1 site kit + dream combat; VisionBoard day/night product pointer. PHASE_BOARD **RS-A GATE READY** — PENDING Lead **`APPROVE RS-A`** (unlocks RS-B). No C++/Content.


## 2026-09-19 ET — Docs/21 Reap & Sow strategy DRAFT

Filed [Docs/21_REAP_SOW.md](../Docs/21_REAP_SOW.md): day = reap/collect, night = sow/nurture; astral combat = dream battles → heal/recruit; planet sites (trees, rocks, flowers, animal den, humanoid camp, special cross-bonus). Phases **RS-A…E** locked. PHASE_BOARD + Docs/README wired. **PENDING Lead `APPROVE RS STRATEGY`** — do not start RS-A until gate. No C++/Content this session.


## 2026-09-18 ET — Merge outstanding work into main + prune branches

Lead: merge all outstanding work into **main** and remove feature branches. PR #109 merged (VS_MVP markers). Allowlist extended (Docs/20 + `config/uasset-allowlist.json` + `.gitattributes`) for Meshes/Materials/Biomes/Harvestables/Dungeon + GA_Dodge/PrimaryAttack + khronos_box_scale_ref; committed + pushed (`bb8ce21`). **Mannequins** remain KEEP-LOCAL. Local feature branches deleted; **39** remote `cursor/*` / `docs/*` / content branches deleted. Repo branches: **main** only.


## 2026-09-17 ET — APPROVE UASSET POLICY

Lead **`APPROVE UASSET POLICY`**, 2026-09-17 ET. [Docs/20_UASSET_AI_POLICY.md](../Docs/20_UASSET_AI_POLICY.md) stamped **APPROVED / COMPLETE**; allowlist **active** (default KEEP-LOCAL elsewhere). PR #108 merged. No Content binaries. Next product track TBD (Lead gate).


## 2026-09-17 ET — Docs/20 UASSET/AI policy DRAFT

Lead requested UASSET allowlist + AI provenance policy. [Docs/20_UASSET_AI_POLICY.md](../Docs/20_UASSET_AI_POLICY.md) + [AI_ASSET_LOG.md](../Docs/AI_ASSET_LOG.md) filed; scoped `.gitattributes` LFS; `npm run check:uasset-allowlist`; swarm/setup pointers updated. PHASE_BOARD **IN PROGRESS** — PENDING **`APPROVE UASSET POLICY`**. No Content binaries in PR.


## 2026-09-17 ET — APPROVE HS-G

Lead Luke Thompson **`APPROVE HS-G`**, 2026-09-17 ET. [Docs/17g_HS_G_OPS_DIET.md](../Docs/17g_HS_G_OPS_DIET.md) stamped **APPROVED / COMPLETE**; PHASE_BOARD HS-G closed; Docs/17/18/17d pointers synced. PR #105 merged. VP2-A/B gate strings unchanged.


## 2026-09-17 ET — HS-G ops diet DRAFT

Lead requested optional residual mini-track. [Docs/17g_HS_G_OPS_DIET.md](../Docs/17g_HS_G_OPS_DIET.md) filed **DRAFT** — three Conductor/DESKTOP ops rules (evidence PASS, hang budget, compile hygiene). PHASE_BOARD + Docs/17/18/17d pointers. PENDING **`APPROVE HS-G`** — do not stamp in PR.


## 2026-09-17 ET — VP2-A evidence filed (0/9 MISSING)

DESKTOP: preflight PASS; PIE+Manny+ABP_Unarmed PASS; MCP interact automation crashed; evidence:grep 0/9 MISSING. Handoff VP2_A_EVIDENCE.md — PENDING **`APPROVE VP2-A`**.


## 2026-09-17 ET — APPROVE VP2 STRATEGY / VP2-A unlocked

Lead **`APPROVE VP2 STRATEGY`**. Docs/18 active; **VP2-A** DESKTOP evidence prove **IN PROGRESS**.


## 2026-09-17 ET — Docs/18 VP2 Verify & Prove DRAFT

Lead asked for next-track draft after HS sign-off. Docs/18 VP2 (prove loop with evidence:grep before features) filed DRAFT — await **`APPROVE VP2 STRATEGY`**.


## 2026-09-17 ET — SIGN OFF HS AUDIT / Docs/17 CLOSED

Lead **`SIGN OFF HS AUDIT`**. Harness **~A**, swarm **~A**. HS-A/B/D/E APPROVED; HS-C ACCEPT DEFER; HS-E KEEP-LOCAL. Next product track **TBD by Lead only**.


## 2026-09-17 ET — HS-F sign-off DRAFT (PENDING SIGN OFF HS AUDIT)

HS-F filing: [Docs/17_HS_AUDIT_SIGN_OFF.md](../Docs/17_HS_AUDIT_SIGN_OFF.md). Proposed grades harness **~A** / swarm **~A**. Do **not** claim **`SIGN OFF HS AUDIT`**. Next product track **TBD by Lead only**.


## 2026-09-17 ET — APPROVE HS-E / HS-F unlocked

Lead **`APPROVE HS-E`** (policy **KEEP-LOCAL**). Character/bootstrap closed ([Docs/17e](../Docs/17e_HS_CONTENT_BOOTSTRAP.md)). **HS-F** sign-off & re-grade **IN PROGRESS**.


## 2026-09-17 ET — HS-E POLICY KEEP-LOCAL (PENDING APPROVE HS-E)

Lead **`HS-E POLICY KEEP-LOCAL`**. Docs/17e + DESKTOP handoff + preflight Mannequins fail-loud. Status still **PENDING** **`APPROVE HS-E`**. Do not claim APPROVE. No `.uasset` commits.


## 2026-09-17 ET — APPROVE HS-D / HS-E unlocked

Lead **`APPROVE HS-D`**. Evidence automation closed ([Docs/17d](../Docs/17d_HS_EVIDENCE.md)). **HS-E** character/bootstrap canon **IN PROGRESS**.


## 2026-09-17 ET — ACCEPT HS-C DEFER / HS-D unlocked

Lead **`ACCEPT HS-C DEFER`**. Branch protection permanently deferred for HS (risk accepted). **HS-D** evidence & re-verify automation **IN PROGRESS**.


## 2026-09-17 ET — APPROVE HS-B / HS-C unlocked

Lead **`APPROVE HS-B`**. Swarm ops closed ([Docs/17b](../Docs/17b_HS_SWARM_OPS.md)). **HS-C** CI as law **IN PROGRESS** — apply branch protection or **`ACCEPT HS-C DEFER`**.


## 2026-09-17 ET — APPROVE HS-A / HS-B unlocked

Lead **`APPROVE HS-A`**. Inventory closed ([Docs/17a](../Docs/17a_HS_INVENTORY.md)). **HS-B** swarm ops tighten **IN PROGRESS**.


## 2026-09-17 ET — APPROVE HS STRATEGY / HS-A unlocked

Lead **`APPROVE HS STRATEGY`**. Docs/17 active; **HS-A** inventory & debt ledger **IN PROGRESS**.


## 2026-09-17 ET — Docs/17 HS Audit strategy DRAFT

Lead asked for post–Docs/08 harness/swarm audit (same shape as Docs/08 WAVEs). Drafted Docs/17 HS-A…F; awaiting **`APPROVE HS STRATEGY`**.


# Session summary (rolling)

## 2026-09-17 ET — APPROVE PL-D / Docs/16 PL track CLOSED

Lead **`APPROVE PL-D`**. Playable Loop **CLOSED / COMPLETE** (A APPROVED, B WAIVED, C APPROVED, D APPROVED). Shot 1 still + UE markers filed. Next product/harness track **TBD**.


## 2026-09-17 ET — PL-D Shot 1 evidence (pending APPROVE PL-D)

UE markers `CAM_Hero` + `VS_MARKER_Shot1_Lookout` confirmed on `L_VS_MVP_Markers`. Presentation still = existing `shot1_lookout.png` (P6_FIX). UE HighResShot black — not used. Awaiting Lead **`APPROVE PL-D`** to close PL track.


## 2026-09-17 ET — APPROVE PL-C / PL-D unlocked

Lead **`APPROVE PL-C`**. Store-transfer + inventory readout **CLOSED**. **PL-D OPEN** — optional Shot 1 from existing CAM/markers. Next: Lead **`APPROVE PL-D`** closes PL track.


## 2026-09-17 ET — WAIVE PL-B / PL-C unlocked

Lead **`WAIVE PL-B`** (Luke Thompson, away). Verb Alt+P greps **WAIVED** (no invented lines). **PL-C OPEN** — PA-07 store-transfer + thin inventory readout. Next: Lead **`APPROVE PL-C`**.


## 2026-09-17 ET — APPROVE PL-A / PL-B unlocked

Lead **`APPROVE PL-A`** (Luke Thompson). Manny substitute + preflight evidence **CLOSED**. **PL-B OPEN** — human Alt+P verb greps on `L_VS_MVP_Markers` (Docs/12c–12e prefixes). Keep [VP_A_PIE.md](../Docs/handoffs/VP_A_PIE.md) WAIVE record intact.


## 2026-09-17 ET — PL-A Manny substitute APPROVED

Lead approved **UE 5.7 template Mannequin** (`SKM_Manny_Simple` + `ABP_Unarmed`) as PL-A substitute for missing `SK_Man_Full_01`. Config paths updated; DESKTOP copies Mannequins locally (**no `.uasset` commits**). Next: MCP apply + `preflight:ue --require-editor`, then Lead **`APPROVE PL-A`**.


## 2026-09-17 ET — APPROVE PL STRATEGY / Docs/16

Lead **`APPROVE PL STRATEGY`**. Playable Loop track **ACTIVE**: PL-A character realization OPEN; PL-B/C/D LOCKED. Prior VP track CLOSED.


## 2026-09-17 ET — APPROVE VP-D / VP track CLOSED

Lead **`APPROVE VP-D`** (Luke Thompson). Docs/14 Verify & Polish **CLOSED / COMPLETE** (VP-A…D). Bootstrap evidence PR #72; stamp follow-up. Branch protection remains **DEFERRED** (HR3-C). Next track TBD.


**Purpose:** Short operational memory for **swarm / Conductor** sessions. Read this and [swarm/PHASE_BOARD.md](../swarm/PHASE_BOARD.md) at session start — **not** the full [SESSION_LOG.md](SESSION_LOG.md) unless you need a specific past incident.

**Policy:** Conductor (or the closing agent) maintains a **rolling last-30-days** summary here. When an entry is older than 30 days, move detail to SESSION_LOG only (do not delete SESSION_LOG history).

---

## How to use

| Session type | Read at start | Write at end |
|---|---|---|
| **MVP swarm / Conductor / HR track** | This file + `swarm/PHASE_BOARD.md` + relevant `Docs/handoffs/` | Append one dated bullet block here; update PHASE_BOARD if status changed |
| **UE engineering (Windows Editor)** | [TaskLists/DAILY_STATE.md](TaskLists/DAILY_STATE.md) + this file (optional) | Append [SESSION_LOG.md](SESSION_LOG.md); refresh DAILY_STATE if using task lists |
| **Cloud agent (docs-only PR)** | Task packet + [Docs/11_SWARM_HARNESS_REFINE.md](../Docs/11_SWARM_HARNESS_REFINE.md) HR section | PR evidence paths; Conductor updates this file after merge |

Full chronological history remains in **SESSION_LOG.md** (~850KB+). CI still requires SESSION_LOG to exist and be non-empty; this file is the **default entry point** for swarm continuity.

---

## Rolling log (newest first)

### 2026-09-17 — VP-C APPROVED (APPROVE VP-C stamp)

- Lead **`APPROVE VP-C`** (Luke Thompson, 2026-09-17 ET) — VP-C **APPROVED / CLOSED**; **VP-D IN PROGRESS** (unlocked).
- Polish PR #69 @ `f88ece5` (PA-04 M_Nurtured visual, PA-06 interact prompts; PA-07 deferred). HR3-C branch protection **DEFERRED** unless Lead applies.
- Docs stamped: [VP_C_POLISH.md](../Docs/handoffs/VP_C_POLISH.md), [VP_D_BOOTSTRAP_CI.md](../Docs/handoffs/VP_D_BOOTSTRAP_CI.md), [14_VP_VERIFY_POLISH.md](../Docs/14_VP_VERIFY_POLISH.md), [PHASE_BOARD.md](../swarm/PHASE_BOARD.md).
- **Next:** Conductor DESKTOP PA-05 bootstrap dry-run; Lead branch-protection checklist; Lead **`APPROVE VP-D`** when VP-D complete.

### 2026-09-17 — Lead WAIVE VP-A re-verify (start VP-C)

- Lead **`WAIVE VP-A re-verify`** (Luke Thompson, 2026-09-17 ET) — all required verb prefixes **WAIVED** for VP-C unlock per HR3-D.
- Honest automation **STILL FAIL** record retained in [VP_A_PIE.md](../Docs/handoffs/VP_A_PIE.md) § Re-verify; waiver stamp appended.
- [PHASE_BOARD.md](../swarm/PHASE_BOARD.md): VP-A-reverify → **WAIVED**; no longer blocks VP-C **COMPLETE** (Lead **`APPROVE VP-C`** still required).
- **Next:** Lead **`APPROVE VP-C`** when polish sign-off ready.

### 2026-09-17 — VP-A re-verify STILL FAIL + VP-C polish impl (pending APPROVE VP-C)

- **VP-A re-verify** on DESKTOP @ `0e4bca1`: verb greps **STILL FAIL** (0 gameplay lines all prefixes); MCP PIE `get_pie_worlds` count **0**, no PlayerController; `pie_test_runner` **3/40**. § Re-verify appended to [VP_A_PIE.md](../Docs/handoffs/VP_A_PIE.md).
- **VP-C impl (repo):** PA-04 `ApplyNurturedVisual` on nurture success/restore; PA-06 interact on-screen prompts + range hints; gather dress **no gap** (GP_N1/GP_N2 present); PA-07 store-transfer **deferred**. Handoff [VP_C_POLISH.md](../Docs/handoffs/VP_C_POLISH.md) — **IN PROGRESS / PENDING APPROVE VP-C** (not COMPLETE).
- [PHASE_BOARD.md](../swarm/PHASE_BOARD.md): VP-A-reverify → **STILL FAIL**; VP-C → **PENDING APPROVE VP-C**.
- **Next:** Lead **`APPROVE VP-C`**; human Alt+P PIE for verb greps or Lead **WAIVE** per prefix.

### 2026-09-17 — VP-B APPROVED (APPROVE VP-B stamp)

- Lead **`APPROVE VP-B`** (Luke Thompson, 2026-09-17 ET) — VP-B **APPROVED / CLOSED**; **VP-C IN PROGRESS** (planning/impl unlocked).
- PA-03 **deferred accept** under VP-B (mesh-only interim; not an open defect). **VP-D LOCKED**.
- **VP-A re-verify** on DESKTOP (CND parent) — **IN PROGRESS** / required before VP-C **COMPLETE** per [HR3_D_EVIDENCE_LANE.md](../Docs/handoffs/HR3_D_EVIDENCE_LANE.md). Do **not** mark VP-C **COMPLETE** until re-verify filed or Lead **WAIVED**.
- Docs stamped: [VP_B_SMOKE_CHARACTER.md](../Docs/handoffs/VP_B_SMOKE_CHARACTER.md), [14_VP_VERIFY_POLISH.md](../Docs/14_VP_VERIFY_POLISH.md), [PHASE_BOARD.md](../swarm/PHASE_BOARD.md); stub [VP_C_POLISH.md](../Docs/handoffs/VP_C_POLISH.md).
- **Next:** Conductor files VP-A re-verify on DESKTOP; VP-C implementation — Lead **`APPROVE VP-C`** before implementation PR merge.

### 2026-09-17 — VP-B DESKTOP evidence + NightMix MaterialLibrary fix

- **DESKTOP-21CT3H0** @ `5d09cf8`: preflight exit **0** (`mesh_only: true`); NightMix smoke **4/4** via `unreal.MaterialLibrary` (PA-02 fixed).
- Repo: `smoke_nightmix_phase.py` prefers `MaterialLibrary`, fallback `KismetMaterialLibrary`; handoff [VP_B_SMOKE_CHARACTER.md](../Docs/handoffs/VP_B_SMOKE_CHARACTER.md).
- [PHASE_BOARD.md](../swarm/PHASE_BOARD.md): VP-B **EVIDENCE COMPLETE — PENDING LEAD `APPROVE VP-B`**; VP-C **LOCKED**.
- **Next:** Lead **`APPROVE VP-B`** → VP-A re-verify → unlock VP-C.

### 2026-09-17 — VP-B mesh-only character + preflight (repo lane)

- Cloud agent VP-B: interim **mesh-only** spawn — `character_blueprint_config.json` → Engine `DefaultSkeletalMesh`, empty `anim_blueprint`; preflight + bootstrap scripts aligned (spawn > AnimGraph).
- Handoff: [Docs/handoffs/VP_B_SMOKE_CHARACTER.md](../Docs/handoffs/VP_B_SMOKE_CHARACTER.md); [PHASE_BOARD.md](../swarm/PHASE_BOARD.md) + [Docs/14](../Docs/14_VP_VERIFY_POLISH.md) → VP-B **IN PROGRESS** (HR3 **CLOSED**).
- **Next (DESKTOP):** `setup_character_blueprint.py` → `preflight_ue_editor.py` → `npm run preflight:ue -- --require-editor`; then NightMix smoke + VP-A re-grep.

### 2026-09-17 — HR3-D APPROVED (APPROVE HR3-D stamp)

- Lead **`APPROVE HR3-D`** (Luke Thompson, 2026-09-17 ET) — HR3-D **APPROVED / COMPLETE**; **HR3 track CLOSED / COMPLETE** (HR3-C **DEFERRED**).
- Evidence merge `9fe48d6` (PR #65). Grades: harness **~A** (C deferred = not pure A+ on CI-as-law), swarm **~A+**.
- Docs stamped: [HR3_D_EVIDENCE_LANE.md](../Docs/handoffs/HR3_D_EVIDENCE_LANE.md), [15_HR3_A_PLUS.md](../Docs/15_HR3_A_PLUS.md), [PHASE_BOARD.md](../swarm/PHASE_BOARD.md), [14_VP_VERIFY_POLISH.md](../Docs/14_VP_VERIFY_POLISH.md).

### 2026-09-17 — HR3-D DESKTOP evidence lane + re-verify (docs-only)

- Cloud agent HR3-D: [PHASE_BOARD.md](../swarm/PHASE_BOARD.md) **Host** column (**CLOUD** | **DESKTOP** | **Lead**); handoff PR contract in [SWARM_OPS.md](../swarm/SWARM_OPS.md) §4a–4c and [CLOUD_AGENT_PACKET.md](../swarm/CLOUD_AGENT_PACKET.md).
- Re-verify rule: **VP-B → VP-A greps re-prove → VP-C unlock** — [14_VP_VERIFY_POLISH.md](../Docs/14_VP_VERIFY_POLISH.md) § Re-verify; example checklist in [HR3_D_EVIDENCE_LANE.md](../Docs/handoffs/HR3_D_EVIDENCE_LANE.md).
- HR3-C **DEFERRED / COMPLETE for track** (Lead skip).

### 2026-09-17 — HR3-C DEFERRED (APPROVE HR3-C deferred stamp)

- Lead Luke Thompson typed **skip** on HR3-C branch-protection UI/API verify (2026-09-17 ET) — treat as **`APPROVE HR3-C deferred`**: checklist delivered (PR #62); GitHub apply not verified; do not block HR3-D.
- Docs stamped: [HR3_C_BRANCH_PROTECTION.md](../Docs/handoffs/HR3_C_BRANCH_PROTECTION.md), [15_HR3_A_PLUS.md](../Docs/15_HR3_A_PLUS.md), [15c_HR3_C_BRANCH_PROTECTION.md](../Docs/15c_HR3_C_BRANCH_PROTECTION.md), [PHASE_BOARD.md](../swarm/PHASE_BOARD.md).
- Branch protection apply remains in [CI_SETUP.md](Setup/CI_SETUP.md) for later.

### 2026-09-17 — HR3-C branch protection checklist (docs-only)

- Cloud agent HR3-C: expanded [docs/Setup/CI_SETUP.md](Setup/CI_SETUP.md) § Branch protection — step-by-step Lead checklist for **`validate`**, **`python-lint`**, **`build-win64`** on `main`; aligned with [CI_POLICY.md](Setup/CI_POLICY.md) and HR2-C path filters.
- Spec + handoff: [Docs/15c_HR3_C_BRANCH_PROTECTION.md](../Docs/15c_HR3_C_BRANCH_PROTECTION.md), [Docs/handoffs/HR3_C_BRANCH_PROTECTION.md](../Docs/handoffs/HR3_C_BRANCH_PROTECTION.md) — status **PENDING LEAD APPLY** (API `gh …/protection` → **403**; Lead must confirm in GitHub UI).
- [PHASE_BOARD.md](../swarm/PHASE_BOARD.md): HR3-C **EVIDENCE FILED — PENDING LEAD APPLY**.
- **Next:** Lead apply branch protection → stamp handoff **APPLIED** → **`APPROVE HR3-C`**. Do not claim protection enabled without GitHub confirmation.

### 2026-09-17 — HR3-B APPROVED (APPROVE HR3-B stamp)

- Lead **`APPROVE HR3-B`** (Luke Thompson, 2026-09-17 ET) — HR3-B **APPROVED / COMPLETE**; **HR3-C UNLOCKED / IN PROGRESS**.
- DESKTOP dry-run on **DESKTOP-21CT3H0** @ `9d7ffaf` (PR #60): `--skip-mcp --assets-only` exit **0**; `--simulate-fail=EDITOR_ABP_SKELETON` exit **1**; editor + `--require-editor` exit **1** (`EDITOR_ABP_SKELETON`, `EDITOR_BP_MESH_EMPTY`).
- Docs stamped: [HR3_B_UE_PREFLIGHT.md](../Docs/handoffs/HR3_B_UE_PREFLIGHT.md), [15_HR3_A_PLUS.md](../Docs/15_HR3_A_PLUS.md), [PHASE_BOARD.md](../swarm/PHASE_BOARD.md).
- **VP-B still PARKED** pending HR3. HR3-D **LOCKED**. No HR3-C implementation in stamp PR.
- **Next:** HR3-C planning (branch protection real) — Lead **`APPROVE HR3-C`** before implementation PR.

### 2026-09-17 — HR3-B UE preflight (cloud PR)

- Added `npm run preflight:ue` — [scripts/preflight-ue.js](../scripts/preflight-ue.js), [config/preflight-ue.json](../config/preflight-ue.json), [Content/Python/preflight_ue_editor.py](../Content/Python/preflight_ue_editor.py).
- Policy: [docs/Setup/UE_PREFLIGHT.md](Setup/UE_PREFLIGHT.md); handoff: [Docs/handoffs/HR3_B_UE_PREFLIGHT.md](../Docs/handoffs/HR3_B_UE_PREFLIGHT.md).
- CI: validate job runs `--skip-mcp --assets-only` + `preflight:ue:test`. Cross-links: DOCTOR_POLICY, WINDOWS_BRIDGE, CURSOR_DEV.
- **Next:** Lead **`APPROVE HR3-B`** after DESKTOP dry-run; then unlock HR3-C.

### 2026-09-17 — HR3-A APPROVED (APPROVE HR3-A stamp)

- Lead **`APPROVE HR3-A`** (Luke Thompson, 2026-09-17 ET) — HR3-A **APPROVED / COMPLETE**; **HR3-B UNLOCKED / IN PROGRESS**.
- Docs stamped: [handoffs/HR3_A_WINDOWS_EXEC.md](../Docs/handoffs/HR3_A_WINDOWS_EXEC.md), [15_HR3_A_PLUS.md](../Docs/15_HR3_A_PLUS.md), [PHASE_BOARD.md](../swarm/PHASE_BOARD.md). Evidence merge `27a1af4` (PR #58).
- **VP-B still PARKED** pending HR3. HR3-C/D **LOCKED**. No HR3-B implementation in stamp PR.
- **Next:** HR3-B planning (UE preflight fails loud) — Lead **`APPROVE HR3-B`** before implementation PR.

### 2026-09-17 — HR3-A Windows exec evidence filed (docs-only)

- [handoffs/HR3_A_WINDOWS_EXEC.md](../Docs/handoffs/HR3_A_WINDOWS_EXEC.md): **parent → machineId → DESKTOP-21CT3H0** proven; Task executors **FAIL** (no Shell/ListMachines/CallDynamicTool).
- Updated [WINDOWS_BRIDGE.md](Setup/WINDOWS_BRIDGE.md) § Canonical Windows agent lane; [CLOUD_AGENT_PACKET.md](../swarm/CLOUD_AGENT_PACKET.md) DESKTOP owner = Conductor parent.
- [PHASE_BOARD.md](../swarm/PHASE_BOARD.md): HR3-A **EVIDENCE FILED / AWAITING APPROVE HR3-A** (not COMPLETE until Lead stamp). **VP-B PARKED**.
- **Next:** Lead **`APPROVE HR3-A`** → unlock HR3-B (UE preflight). Do not assign DESKTOP Shell to Task executors.

### 2026-09-17 — HR3 strategy APPROVED (APPROVE HR3 STRATEGY stamp)

- Lead **`APPROVE HR3 STRATEGY`** (Luke Thompson, 2026-09-17 ET) — Docs/15 **APPROVED / ACTIVE**; **HR3-A UNLOCKED / IN PROGRESS**.
- Docs stamped: [15_HR3_A_PLUS.md](../Docs/15_HR3_A_PLUS.md), [PHASE_BOARD.md](../swarm/PHASE_BOARD.md). **VP-B PARKED** pending HR3. HR3-B/C/D **LOCKED**.
- **Next:** HR3-A planning (Windows exec runbook) — Lead **`APPROVE HR3-A`** before implementation PR. No HR3-A scripts in stamp PR.

### 2026-09-17 — HR3 A+ strategy (docs-only DRAFT)

- Delivered [Docs/15_HR3_A_PLUS.md](../Docs/15_HR3_A_PLUS.md) — **DRAFT**; phases HR3-A (Windows exec), HR3-B (UE preflight), HR3-C (branch protection), HR3-D (DESKTOP evidence + re-verify).
- [PHASE_BOARD.md](../swarm/PHASE_BOARD.md): current track **HR3 draft**; **VP-B PARKED** pending HR3; VP-A **APPROVED** (hard-fail ABP).
- Harness target **~B → A+**; swarm **~B+ → A+**. **No HR3-A…D implementation** in strategy PR.
- **Next:** Lead **`APPROVE HR3 STRATEGY`** → unlock HR3-A. Resume VP-B after HR3 (+ HR3-B preflight recommended).

### 2026-09-17 — VP-A APPROVED (APPROVE VP-A stamp)

- Lead **`APPROVE VP-A`** (Luke Thompson, 2026-09-17 ET) — VP-A **APPROVED**; VP-B was unlocked then **PARKED** for HR3.
- Evidence PR #54: verb PIE **hard-fail accepted** (PA-03 `ABP_HomeWorldCharacter` skeleton); re-verify greps after VP-B.
- Docs stamped: [handoffs/VP_A_PIE.md](../Docs/handoffs/VP_A_PIE.md), [14_VP_VERIFY_POLISH.md](../Docs/14_VP_VERIFY_POLISH.md), [PHASE_BOARD.md](../swarm/PHASE_BOARD.md).

### 2026-09-17 — VP-A PIE evidence filed (DESKTOP hard-fail)

- DESKTOP PIE run on **DESKTOP-21CT3H0** (2026-09-17 ~08:26–08:28 ET) via UnrealMCP @ repo `cb592fa`.
- [handoffs/VP_A_PIE.md](../Docs/handoffs/VP_A_PIE.md): scene inventory **PASS**; all verb prefixes **FAIL** (no spawnable character).
- Root cause: `ABP_HomeWorldCharacter` skeleton missing (`UE4_Mannequin_Skeleton`) — maps **PA-03 / VP-B**.
- [PHASE_BOARD.md](../swarm/PHASE_BOARD.md): VP-A **EVIDENCE FILED / AWAITING APPROVE VP-A** (not COMPLETE until Lead stamp).
- **Next:** Lead **`APPROVE VP-A`** → unlock **VP-B** (ABP skeleton + NightMix smoke) before verb PIE re-run.

### 2026-09-17 — VP strategy APPROVED (APPROVE VP STRATEGY stamp)

- Lead **`APPROVE VP STRATEGY`** (Luke Thompson, 2026-09-17 ET) — Docs/14 **APPROVED / ACTIVE**; VP-A **UNLOCKED / IN PROGRESS**.
- Docs stamped: [14_VP_VERIFY_POLISH.md](../Docs/14_VP_VERIFY_POLISH.md), [PHASE_BOARD.md](../swarm/PHASE_BOARD.md); stub [handoffs/VP_A_PIE.md](../Docs/handoffs/VP_A_PIE.md) pending DESKTOP evidence.
- Product NP **CLOSED**. HR2 **CLOSED**. VP-B/C/D **LOCKED** until their gates.
- **Next:** DESKTOP PIE evidence → Lead **`APPROVE VP-A`**. **Do not mark VP-A complete without evidence.**

### 2026-09-17 — VP Verify & Polish strategy (docs-only)

- Delivered [Docs/14_VP_VERIFY_POLISH.md](../Docs/14_VP_VERIFY_POLISH.md) — **DRAFT**; phases VP-A (PIE evidence), VP-B (smoke/ABP), VP-C (thin polish), VP-D (bootstrap + branch protection).
- [swarm/PHASE_BOARD.md](../swarm/PHASE_BOARD.md): HR2 track **CLOSED**; VP rows **LOCKED**; current track awaits Lead **`APPROVE VP STRATEGY`**.
- Post-NP audit residuals PA-01…PA-08 mapped to VP phases. **No VP-A…D implementation** in strategy PR.
- **Next:** Lead **`APPROVE VP STRATEGY`** → unlock VP-A on DESKTOP.

### 2026-09-17 — HR2 track CLOSED (APPROVE HR2-C)

- Lead **`APPROVE HR2-C`** (Luke Thompson, 2026-09-17 ET) — HR2-C **APPROVED**; HR2 track **CLOSED / COMPLETE** (HR2-A/B/C all approved).
- Docs stamped: [13_HR2_HARNESS_REFINE.md](../Docs/13_HR2_HARNESS_REFINE.md), [13c_HR2_C_CI_GATE.md](../Docs/13c_HR2_C_CI_GATE.md), [PHASE_BOARD.md](../swarm/PHASE_BOARD.md).
- **No HR2-D.** No new product phases without Lead direction.

### 2026-09-17 — HR2-C C++ CI gate (build-win64 required)

- Lead **`APPROVE HR2-B`** (Luke Thompson, 2026-09-17 ET) — HR2-B **APPROVED**; HR2-C unlocked.
- HR2-C: `ci.yml` path filters for C++ paths; `build-win64` **Required** (was recommended); Lead waiver documented; branch protection note in CI_SETUP.
- Deliverables: [Docs/13c_HR2_C_CI_GATE.md](../Docs/13c_HR2_C_CI_GATE.md), [Docs/handoffs/HR2_C_CI_GATE.md](../Docs/handoffs/HR2_C_CI_GATE.md).
- **Next:** Lead **`APPROVE HR2-C`** → HR2 track **CLOSED**. **Do not invent HR2-D.**

### 2026-09-17 — HR2-B cold-clone submodule onboarding

- Lead **`APPROVE HR2-A`** (Luke Thompson, 2026-09-17 ET) — HR2-A **APPROVED**; HR2-B unlocked.
- HR2-B: pin registry `config/devenv-template-pin.json`, CI guard `scripts/verify-devenv-submodule.sh` in validate.yml, runbook in CURSOR_DEV + AGENTS.md.
- Cloud evidence: empty `DevEnvTemplate/` → submodule init → `doctor:build` exit 0 → `doctor:ue` exit 0.
- Handoff: [Docs/13b_HR2_B_COLD_CLONE.md](../Docs/13b_HR2_B_COLD_CLONE.md). **Next:** Lead **`APPROVE HR2-B`** → unlock HR2-C. **Do not start HR2-C.**

### 2026-09-17 — HR2-A doctor signal (`doctor:ue`)

- Lead **`APPROVE HR2 STRATEGY`** (Luke Thompson, 2026-09-17 ET) — strategy merge `d10e7b5` (PR #47).
- HR2-A: `scripts/doctor-ue.js`, `config/doctor-ue-declines.json`, `npm run doctor:ue` — cloud before exit **1**, after exit **0** (77/100, 5 accepted declines).
- Handoff: [Docs/13a_HR2_A_HANDOFF.md](../Docs/13a_HR2_A_HANDOFF.md). **Next:** Lead **`APPROVE HR2-A`** → unlock HR2-B.

### 2026-09-17 — HR2 harness refine strategy (docs-only)

- Delivered [Docs/13_HR2_HARNESS_REFINE.md](../Docs/13_HR2_HARNESS_REFINE.md) — **DRAFT**; phases HR2-A (doctor signal), HR2-B (cold-clone submodule), HR2-C (C++ CI gate).
- [swarm/PHASE_BOARD.md](../swarm/PHASE_BOARD.md): HR2 rows **LOCKED**; product NP **CLOSED**; current track awaits Lead **`APPROVE HR2 STRATEGY`**.
- Baseline: harness **B- (~3.8/5)** @ `54193ac`; no HR2 implementation in this PR.
- **Next:** Lead **`APPROVE HR2 STRATEGY`** → unlock HR2-A.

### 2026-09-17 — Product NP track CLOSED (APPROVE NP-E)

- Lead **`APPROVE NP-E`** (Luke Thompson, 2026-09-17 ET) — NP-E **APPROVED**; product NP track **CLOSED / COMPLETE** (NP-A…E all approved).
- Placement scripts on main: PR #44 (`870f1d0`) — beast pad class replace + nurture enum fix.
- Docs stamped: [11_NEXT_PHASE_STRATEGY.md](../Docs/11_NEXT_PHASE_STRATEGY.md), [PHASE_BOARD.md](../swarm/PHASE_BOARD.md), [12e_NP_E_SYS_V6_V8.md](../Docs/12e_NP_E_SYS_V6_V8.md).
- **No NP-F.** No further product NP gates.

### 2026-09-17 — NP-E SYS V6–V8 + APPROVE NP-D stamp

- Lead **`APPROVE NP-D`** (Luke Thompson, 2026-09-17 ET) — NP-D **APPROVED**; NP-E unlocked and **COMPLETE**.
- NP-E: heal ×3 (`HEAL:`), nurture ×2 (`NURTURE:`), dawn persist (`DAWN:`) — [12e_NP_E_SYS_V6_V8.md](../Docs/12e_NP_E_SYS_V6_V8.md).
- Residual: `AHomeWorldBeastPad` C++ actor replaces unreliable Editor `add_component_by_class`.
- **Next:** Lead **`APPROVE NP-E`** → product NP track complete. Windows **Safe-Build** required after merge.

### 2026-09-17 — NP-D SYS V3–V4 + APPROVE NP-C stamp

- Lead **`APPROVE NP-C`** (Luke Thompson, 2026-09-17 ET) — NP-C **APPROVED**; NP-D unlocked.
- Resolved Docs/11 + SESSION_SUMMARY conflict markers; NP-A/B/C **APPROVED**; next gate **`APPROVE NP-D`**.
- NP-D: RES_* six-slot inventory, gather path, beast tame SM — [12d_NP_D_SYS_V3_V4.md](../Docs/12d_NP_D_SYS_V3_V4.md).
- **Next:** Lead **`APPROVE NP-D`** after PR merge + Windows Safe-Build → unlock NP-E.

### 2026-09-17 — NP-C form + V1 polish

- Lead **`APPROVE NP-B`** — lookdev apply signed off (Luke Thompson, 2026-09-17 ET).
- NP-C delivered: [12c_NP_C_FORM_V1.md](../Docs/12c_NP_C_FORM_V1.md) — GP_PlayerStart, form swap (FORM: logs), soft walk bounds, V2/V5 PIE runbook, NightMix smoke script.
- C++: `HomeWorldSoftBoundsComponent`, character form sync via `TimeOfDaySubsystem::OnPhaseChanged`.
- Python: `place_vs_mvp_gp.py`, `smoke_nightmix_phase.py`, `vs_mvp_walk_bounds.json`; bootstrap chain extended.

### 2026-09-17 — NP-B lookdev apply (Windows evidence)

- Lead **`APPROVE NP-A`** — NP-B unlocked (2026-09-17 ET).
- Windows DESKTOP-21CT3H0 @ HEAD `82c7eb2`: `assign_vs_mvp_materials` **Done** — 78 actors, 78 slots assigned, 0 missing/unmapped; 8 masters used (`M_BeastStylized` + `M_Nurtured` unused — expected).
- NightMix smoke residual (non-blocking). [Docs/12b_NP_B_LOOKDEV.md](../Docs/12b_NP_B_LOOKDEV.md) **APPROVED**.

### 2026-09-17 — NP-A inventory / gap map

- Lead **`APPROVE NP STRATEGY`** — product NP strategy **APPROVED** (Luke Thompson, 2026-09-17 ET).
- NP-A delivered: [Docs/12a_NP_A_INVENTORY.md](../Docs/12a_NP_A_INVENTORY.md) — KEEP/PRESENT/MISSING/DEFER vs Docs/03 + Docs/02; Windows mesh counts; content binary volatility call-out for NP-B.
- Windows inventory confirmed (`cmd dir`, HEAD ae7f649): ten masters + MPC + L_VS_MVP_Markers **PRESENT**; MI on DRESS_* **MISSING** → NP-B; ABP skeleton warning risk noted.
- **Next:** Lead **`APPROVE NP-A`** → unlock NP-B (no lookdev implementation until approved).

### 2026-09-17 — HR track CLOSED; product NP unlocked

- Lead **`APPROVE HR-B2`** then **`APPROVE HR-D`** — harness refine track **CLOSED** (Luke Thompson, 2026-09-17 ET).
- [Docs/11_NEXT_PHASE_STRATEGY.md](../Docs/11_NEXT_PHASE_STRATEGY.md) activated — NP-A…E **DRAFT** awaiting Lead **`APPROVE NP STRATEGY`**.
- **Next:** Lead **`APPROVE NP STRATEGY`** → unlock NP-A (no implementation until approved).

### 2026-09-17 — HR-B2 residual harness risks

- Lead deferred **`APPROVE HR-D`** → **HR-B2 first** — [Docs/11d_HR_D_DEFER.md](../Docs/11d_HR_D_DEFER.md).
- DevEnvTemplate pin `213673f` → **`2efd756`**; rules **15 → 3** always-on; [DOCTOR_POLICY.md](Setup/DOCTOR_POLICY.md) for accepted declines.
- Handoff: [Docs/11e_HR_B2_HANDOFF.md](../Docs/11e_HR_B2_HANDOFF.md). Product NP **PARKED**.
- **Next:** Lead **`APPROVE HR-B2`** → then **`APPROVE HR-D`**.

### 2026-09-17 — HR-D dry-run loop (cloud agent proof)

- Lead **`APPROVE HR-C`** — swarm ops refine signed off; HR-D dry-run unlocked.
- Cloud agent dry-run: docs-only PR #27 — no MCP, no Safe-Build, no `.uasset`.
- Deliverables: [Docs/handoffs/HR_D_DRY_RUN.md](../Docs/handoffs/HR_D_DRY_RUN.md), [Docs/11d_HR_D_HANDOFF.md](../Docs/11d_HR_D_HANDOFF.md); audit re-grade (combined **B- 3.9** vs baseline **C 2.8**).

### 2026-09-17 — HR-C swarm ops refine

- Lead **`APPROVE HR-B`** — harness tighten signed off (PR #25).
- HR-C delivered: POST-AUDIT `PHASE_BOARD`, cloud-agent handoff templates, dual-OS trim in workflow/rules, SESSION_SUMMARY policy.
- **Next:** Lead **`APPROVE HR-C`** → unlock HR-D dry-run.

### 2026-09-17 — HR-B harness tighten

- CI validate paths aligned to DOCS_LAYOUT (SH-01 fix); Windows bridge runbook; rules glob slimming (20→15 always-on).
- Handoff: [Docs/11b_HR_B_HANDOFF.md](../Docs/11b_HR_B_HANDOFF.md).

### 2026-09-17 — HR-A measures + Docs/11 approved

- Baseline doctor, rules token budget, dual-OS inventory — [Docs/11a_HR_MEASURES.md](../Docs/11a_HR_MEASURES.md).

### 2026-09-16 — Post-audit wrap + audit sign-off

- Docs/10 CLOSED (master graphs + NightMix); WAVE F archive; VS_MVP primary slice — [Docs/08_AUDIT_SIGN_OFF.md](../Docs/08_AUDIT_SIGN_OFF.md).

### 2026-09-17 — VP2-A DESKTOP prove retry (9/9 PASS)

- Conductor parent DESKTOP retry: `evidence:grep` → **9/9 PASS, 0 MISSING** (soft-reject paths documented).
- Filed [Docs/handoffs/VP2_A_EVIDENCE.md](../Docs/handoffs/VP2_A_EVIDENCE.md); [Docs/18_VERIFY_PROVE.md](../Docs/18_VERIFY_PROVE.md) board → **PENDING `APPROVE VP2-A`**.
- First-run contrast: **0/9** (MCP crash + LogTemp filter). VP2-B backlog captured (LogTemp, piles, MCP console play-world).
- PR #103 (docs-only; no `.uasset`/`.umap`).

### 2026-09-17 — VP2-B success-path fixes (Lead early unlock)

- Lead direction: VP2-B before VP2-A approve; **do not stamp `APPROVE VP2-A`**.
- C++: `HomeWorldPlayWorld` PIE fallback for MCP console cheats; CVar `hw.TimeOfDay.Phase` → `SetPhase`; `hw.TimeOfDay.SetPhase`; `PersistDawnSnapshot` world resolve; interact cone-proximity fallback.
- Python: `place_vs_mvp_resource_piles.py` (GP_Gather_* near homestead).
- Docs: [VP2_B_FIX.md](../Docs/handoffs/VP2_B_FIX.md), [18_VERIFY_PROVE.md](../Docs/18_VERIFY_PROVE.md), [PHASE_BOARD.md](../swarm/PHASE_BOARD.md) → VP2-B **IN PROGRESS**.
- Awaiting DESKTOP Safe-Build + re-prove; gate **`APPROVE VP2-B`**.

### 2026-09-17 — VP2 CLOSED (C0 Stop) + Safe-Build DLL guard

- Lead authorized Conductor **`APPROVE VP2-C STOP`** / **`CLOSE VP2`** after VP2-A+B on main `2ef961f`.
- Docs: [18_VERIFY_PROVE.md](../Docs/18_VERIFY_PROVE.md) track **CLOSED**; [PHASE_BOARD.md](../swarm/PHASE_BOARD.md) VP2 rows closed; no C1/C2 follow-on.
- Harness: `Tools/Safe-Build.ps1` asserts `Binaries/Win64/UnrealEditor-HomeWorld.dll` > 100 KB post-build (HS-G Bad Image / zero-byte DLL residual).

### 2026-09-17 — Docs/19 thin playability (D19-A/B/C impl)

- Lead **`APPROVE D19 STRATEGY`** 2026-09-17 ET — bot-shaped gather + seed + success-path evidence.
- Docs: [19_THIN_PLAYABILITY.md](../Docs/19_THIN_PLAYABILITY.md) **APPROVED**; [PHASE_BOARD.md](../swarm/PHASE_BOARD.md) → Docs/19 **IN PROGRESS** (VP2 stays CLOSED).
- D19-A: hardened `place_vs_mvp_resource_piles.py` — label re-apply, actor tags, dedupe, verify log.
- D19-B: `hw.Gather.Seed` console cheat → `RES_SEED` (mirrors Ore/Flowers).
- D19-C: `evidence-grep.js --success-path` + tests green (`npm run evidence:grep:test`).

### 2026-09-19 — Docs/19 CLOSED (Lead APPROVE D19)

- Lead **`APPROVE D19`** 2026-09-17 ET — D19-A/B/C after DESKTOP prove (PR #107).
- D19-A: `GP_Gather_*` spawn; `GATHER: RES_WOOD +1` / `harvest ok`; `HomeWorldResourcePile` non-Abstract.
- D19-B: `hw.Gather.Seed` → `GATHER: RES_SEED +N`.
- D19-C: `evidence-grep --success-path` PASS; Safe-Build ASCII/single-quote fixes on branch.
- Docs: [19_THIN_PLAYABILITY.md](../Docs/19_THIN_PLAYABILITY.md) **CLOSED / COMPLETE**; [PHASE_BOARD.md](../swarm/PHASE_BOARD.md) → no active product phase.

### 2026-09-19 — Docs/22 UE 5.8 Upgrade CLOSED

- Lead unlocked via upgrade plan implement; branch `chore/ue-5.8-upgrade`.
- U58-A: `EngineAssociation` **5.8**; AGENTS / STACK_PLAN / rules lock → 5.8.
- U58-B: Tools/CI/docs defaults `UE_5.7`→`UE_5.8`; runner label **`ue58`**.
- U58-C: Safe-Build green; removed **MassEntity** from `.uproject` (absent in Launcher 5.8); KNOWN_ERRORS entry.
- U58-D: UnrealMCP rebuilt; MCP port 55557 after ~9m first-open shader compile.
- U58-E: VS_MVP open + RS placement scripts; `hw.RS.CollectDayBonus` / `CrossBonusStatus` / `CollectNightBonus` LogTemp PASS.
- U58-F: [UE58_TECH.md](UE/UE58_TECH.md), `ue58-sources.mdc`, `ue58-api-check` skill; track **CLOSED**.

### 2026-09-19 — Docs/23 UE 5.8 Feature Adoption (U58F)

- Branch `feat/ue58-feature-adoption`; [23_UE58_FEATURE_ADOPTION.md](../Docs/23_UE58_FEATURE_ADOPTION.md).
- Enabled plugins: PCGBiomeCore, PCGPrimitives, ProceduralVegetationEditor, MeshTerrainMode.
- MegaLights + Fog SSS project CVars; Lumen Lite documented (Medium GI/Reflections).
- MCP: keep UnrealMCP ([U58F_F_MCP_DECISION.md](../Docs/handoffs/U58F_F_MCP_DECISION.md)).
- PVE pine + Mesh Terrain Landscape replace remain AD/WLD gated; smoke scripts under `Content/Python/u58f_*.py`.

---

*Maintained by Conductor; HR-C established this rolling policy.*

### 2026-09-19 — U58F DESKTOP smoke + PR #111

- Branch `feat/ue58-feature-adoption` merged to main (PR #111).
- Smokes **ok**: `u58f_pcg_smoke`, `u58f_pve_smoke`, `u58f_night_look_smoke`, `u58f_mesh_terrain_smoke`
- Remaining gates: Art Director PVE pine Content commit; Mesh Terrain sandbox KEEP-LOCAL (no VS_MVP Landscape replace)

### 2026-09-19 — Swarm mode routing protocol

- Added [docs/human-use/SWARM_MODE_ROUTING.md](human-use/SWARM_MODE_ROUTING.md) + skill `swarm-mode-routing`.
- Wired AGENTS.md, START_HERE, SWARM_OPS §0, agent-workflow, DOCS_LAYOUT.
- Note: self-hosted `build-win64` queue is merge hygiene, not a mode-routing blocker.

### 2026-09-19 — Merge outstanding to main

- Merged PR #111 (U58F) and PR #112 (swarm mode routing); feature remotes deleted.
- Docs/23 stamped **CLOSED**; PHASE_BOARD idle (post-U58F).

### 2026-09-19 — Swarm routing optimize (model class + research)

- Added [SWARM_ROUTING_RESEARCH.md](Automation/SWARM_ROUTING_RESEARCH.md); expanded [SWARM_MODE_ROUTING.md](human-use/SWARM_MODE_ROUTING.md) with ModelClass + progressive disclosure.
- Skill description triggers enriched; AD/QA/Conductor **Preferred model class**; token-efficient-context + SWARM_OPS linked.

### 2026-09-19 — Docs/24 VNP (night / pine / mesh)

- Branch eat/vs-night-pine-mesh; [24_VS_NIGHT_PINE_MESH.md](../Docs/24_VS_NIGHT_PINE_MESH.md).
- N0–N2: MegaLights/Fog SSS smoke + VS_MVP evidence Saved/VNP_Evidence/.
- P1–P2: stylized pine OBJ; AD **APPROVE** ([VNP_P2_AD_PINE_VERDICT.md](../Docs/handoffs/VNP_P2_AD_PINE_VERDICT.md)).
- P3: OBJ staged under Content/HomeWorld/Meshes/Environment/; uasset import pending Editor reconnect.
- M1–M2: Mesh Terrain sandbox created; no VS_MVP Landscape replace.

### 2026-09-20 — Docs/canon short pointer pack (cloud)

- Added `Docs/canon/` (12 files: `PILLARS`…`DECISIONS`, `README`) — Game Dev Partner canon pass; long canon unchanged.
- PR #115: combat framing A in `DECISIONS.md`; PLAYTEST next 2-min gather + `hw.Gather.Seed` test.

### 2026-09-20 — Camera bible FP amendment (cloud)

- Replaced `Docs/CAMERA_BIBLE.md` with Lead amendment: no dedicated FP; near framing = WoW orbit boom zoom; two presets (Orbit TP + Iso).
- Added `Docs/CAMERA_IMPL_PROMPT.md`; appended `DECISIONS.md`; aligned `Docs/canon/FEEL.md` + `README.md` pointers.

### 2026-09-21 — MOVEMENT bible locked (cloud)

- Added `Docs/MOVEMENT_BIBLE.md` + `Docs/MOVEMENT_IMPL_PROMPT.md` (Lead vision + Conductor NOW/LATER verbatim).
- Appended `Docs/canon/DECISIONS.md`; Related links in `Docs/canon/README.md`. No gameplay C++; `DO_NOT.md` unchanged (second CMC already listed).

### 2026-09-21 — DAYNIGHT bible locked (cloud)

- Added `Docs/DAYNIGHT_BIBLE.md` + `Docs/DAYNIGHT_IMPL_PROMPT.md` (Lead interview verbatim).
- Appended `Docs/canon/DECISIONS.md`; Related links in `Docs/canon/README.md`; `FEEL.md` night-length pointer. No gameplay C++.

### 2026-09-20 — Homestead bible LOCK (cloud)

- Added `Docs/HOMESTEAD_BIBLE.md` + `Docs/HOMESTEAD_IMPL_PROMPT.md` (Lead interview verbatim).
- Appended `Docs/canon/DECISIONS.md`; `Docs/canon/README.md` + `DO_NOT.md` pointers (edge glide, no invisible-wall bounds, NPC family not co-op MVP, named homestead recipes).

### 2026-09-21 — COMBAT_DREAM bible locked (cloud)

- Added `Docs/COMBAT_DREAM_BIBLE.md` + `Docs/COMBAT_DREAM_IMPL_PROMPT.md` (Lead A1/B/C/D locks).
- Amended combat framing A in `Docs/canon/DECISIONS.md`; updated `DO_NOT.md`, `VERBS.md`, `canon/README.md`. Docs-only; boss volume placement deferred to DESKTOP/Content track.

### 2026-09-21 — GC-A site→RES map (cloud)

- Lead **`APPROVE GC STRATEGY`** → `Docs/22_GATHER_CRAFT_IMPL.md`, handoff `Docs/handoffs/GC_A_SITE_RES.md`, `DECISIONS.md` strategy row.
- C++: `EHomeWorldGatherSiteKind`, pile `GatherSiteKind`, flint/grass flavor logs; Python `homeworld_gc_site_setup.py` + VS_MVP placement scripts. GC-B/C not in PR.

## 2026-09-22 — Split greybox keyart + ART bible (cloud)

- Lead approved adding `refs/keyart_homestead_planetside_split.jpg`; `Docs/02_ART_BIBLE.md` north stars now list night + split dual-zone refs. Docs/asset only.

## 2026-09-22 — DS-A visible demo spine (cloud)

- Lead **`APPROVE DEMO-SPINE`** → `Docs/30_DEMO_SPINE.md`, handoff `Docs/handoffs/DS_A_VISIBLE_HEARTH.md`, `DECISIONS.md` DS strategy row.
- C++: craft/placeholder DS-A visuals; `RevealDemoCottageShell` on `PROGRESS:COTTAGE_UNLOCK`. Python placement + `vs_mvp_ds_visual_helpers.py`. PR: feat(DS-A) visible hearth.

## 2026-09-21 — CD-A stubs (cloud)

- Lead **`APPROVE CD STRATEGY`** → [Docs/23_COMBAT_DREAM_IMPL.md](../Docs/23_COMBAT_DREAM_IMPL.md), handoff [Docs/handoffs/CD_A_STUBS.md](../Docs/handoffs/CD_A_STUBS.md), `DECISIONS.md` CD strategy row (Docs/22 GC **CLOSED** on main via #127).
- C++: minigame stubs (`MINIGAME:*`), boss placeholder volume (`BOSS:PHASE_*`, `BOSS:SEAL`), `place_vs_mvp_cd_stubs.py`, cheats `hw.Minigame.*` / `hw.Boss.Status`. **CD-A APPROVED** stamped in follow-on docs PR (Lead **`APPROVE CD-A`**, 2026-09-21 ET).

## 2026-09-22 — PA-D save before dress reload (cloud)

- **Fix:** `place_vs_mvp_pa_d.py` saves level after PA-D spawn and before `run_dress_refresh()` so `load_level` in dress does not wipe unsaved cliffs/planters/fence/path stones.
- **PR:** #149 (`cursor/pa-d-save-before-dress-1f4a`).

## 2026-09-22 — PA-E P2 industry harness (cloud)

- **P2:** Fixture lifecycle (`inventory` / `reseed` / optional editor `teardown`), centralized **`MRQ_LATENT_WAIT_CONTRACT`**, **`probe_mrq_tool_readiness`** in **`conductor_mrq_capture_preflight`**, **`artifact_stamps`** + **`PA_E_FRESH_PROVE`** purge gate in MRQ report.
- **Docs:** [HARNESS_ARRANGE_TASKLIST.md](Automation/HARNESS_ARRANGE_TASKLIST.md) P2 realigned (golden-image → gated SCOUT); CAPTURE_REDUNDANCY + KNOWN_ERRORS one-liners.
- **DESKTOP:** Re-prove `execute_python_script("capture_shotlist_mrq.py")` → `Saved/pa_e_capture_report.json` + Shot1/Shot2 under `Saved/Screenshots/PA_E/` (cloud cannot run UE).

## 2026-09-22 — PA-E shot1/2 camera pose (cloud, post-#172)

- **Fix:** `pa_e_shotlist_common.py` — shot1/2 use CAM_Hero / CAM_CabinClose **doc meters** + look_at **aim_bounds** dress centroid (extent offsets grazed AABB, fence on frame); **`distance_band_ok`** on **`aim_ok`**.
- **Fix:** `capture_shotlist_mrq.py` — MRQ via spawned **PA_E_MRQ_*** at Arrange loc/rot; purge stale possessable + Transform tracks; **add_possessable** only (no `find_binding_by_name` on CAM_*).
- **KNOWN_ERRORS:** relocate + ray hit ≠ visual PASS; possessable CAM_* + stale sequence Transform ≠ Arrange pose.
- **PR:** #174 `cursor/pa-e-camera-pose-framing-0534` (DESKTOP re-prove MRQ after merge).

## 2026-09-23 — DevHarness pin 8be4170 (cloud)

- Bump `DevEnvTemplate` to **`8be41708e3c1c0bf0b64b6bd4ba9b268d82a7bf0`** (DevHarness PR #33 harness practices).
- Pin registry + CURSOR_DEV + HR2-B canonical table; `automation-harness` guide + extras skills; host `automation-standards.mdc` cross-link only.
- PR: `cursor/bump-devharness-pin-8be4170-80e0` (draft).

## 2026-09-23 — PS-0 strategy approved + PS-A inventory (cloud)

- Lead **`APPROVE PS STRATEGY — homestead kit only`** — PS-0 **CLOSED**; PHASE_BOARD → **PS-A**; [PS_A_INVENTORY.md](../Docs/handoffs/PS_A_INVENTORY.md) (actors, cam map, thresholds, bounds schema).

## 2026-09-23 — PS-A closed / PS-B Arrange opened (cloud)

- Lead **`APPROVE PS-A`**, 2026-09-22 ET — inventory **CLOSED** (DESKTOP counts stamped); PHASE_BOARD → **PS-B**; [PS_B_ARRANGE.md](../Docs/handoffs/PS_B_ARRANGE.md) + `Content/Python/arrange_ps_homestead.py` (`Saved/ps_dress_bounds.json`, `Saved/ps_arrange_gate.json`). **`APPROVE PS-B`** pending DESKTOP Arrange prove + eyeball.

## 2026-09-23 — PS-B closed / PS-C metrics+stills opened (cloud)

- Lead **`APPROVE PS-B`**, 2026-09-22 ET — Arrange **CLOSED** (DESKTOP prove stamped in [PS_B_ARRANGE.md](../Docs/handoffs/PS_B_ARRANGE.md)); PHASE_BOARD → **PS-C**; [PS_C_METRICS.md](../Docs/handoffs/PS_C_METRICS.md) + `Content/Python/ps_placement_prove.py` (`Saved/ps_placement_metrics.json`, `Saved/ps_stills/`, `Saved/ps_c_prove_gate.json`). **`APPROVE PS-C`** pending DESKTOP prove.

## 2026-09-23 — PS-C prove harden after DESKTOP 71bb847 (cloud)

- DESKTOP first run: island max-Z proxy + relative screenshot path → mass closed_fail, 0/7 stills. Harden: multi line-trace, no island proxy, soft baseline, capture_viewport absolute HighResShot, PA-E MRQ PNG fallback for hero/cabin.

## 2026-09-23 — PS-C-1 slate stills harden (cloud)

- Ticket PS-C-1: MCP mid-prove FAppTime Ensure / 300s empty — stills path moved to **`register_slate_pre_tick_callback`** + **`vnp_editor_keep_alive`** (PA-E pretick pattern); **`capture_viewport.console_high_res_invoke_once`** + tick **`probe_png_ready`** (no blocking **`time.sleep`** in settle/wait). Gate written when async stills finish. KNOWN_ERRORS Cause→Avoid row. DESKTOP re-prove pending — no PASS claim.

## 2026-09-23 — Host Pulse console-kill stamp (cloud)

- Docs-only: [HOST_PULSE.md](../Docs/handoffs/HOST_PULSE.md) § Console-kill + Cause→Avoid; [PDF_CYCLE.md](../swarm/PDF_CYCLE.md) § Host Pulse pointer. PR **#193** draft `cursor/host-pulse-console-kill-b3a5`.

## 2026-09-23 — UE Project Bible (cloud, docs-only)

- Added [Docs/UE_BIBLE.md](../Docs/UE_BIBLE.md) — token-lean DESKTOP/MCP prove do/don’t (HOST_PULSE stall budgets, logging/console-kill, PS-C-1 Slate lessons, Conductor tables).
- [swarm/PDF_CYCLE.md](../swarm/PDF_CYCLE.md): Host Pulse ops summary + UE_BIBLE pointer. Branch `cursor/ue-project-bible-b3a5`; no Tools/Source/Content changes.

## 2026-09-23 — PS-C-2 stills driver completes (cloud)

- DESKTOP: gate frozen **`stills_in_progress: true`**, 0 PNGs — async slate callback never advanced after MCP return. Fix: module-level tick dispatcher + **`_drive_ps_c_stills_orchestrator`** (pump/tick until DONE, ≤300s); prove returns with **`stills_in_progress: false`** and updated gate; viewport focus before capture. KNOWN_ERRORS PS-C-2 row. No PASS claim.

## 2026-09-23 — PS-C-CAP-001 re-verify + PS-C-CAM-002 (cloud, PR #198)

- **Ticket A:** Manifest **`exists`/`file_exists`** aligned with canonical **`Saved/ps_stills/`** disk stat before write; **`_finish_all`** + **`_write_stills_manifest(..., act_since=)`** reconcile; gate still uses **`_audit_ps_stills_disk`** for fresh count.
- **Ticket B:** Stale **`ps_arrange_gate.json`** → **`_still_cam_labels_missing()`** forces **`arrange_ps_homestead`** re-run when prove cameras absent.
- **Boot:** Removed bogus **`MovieRenderPipelineEditor`** from **`HomeWorld.uproject`**; KNOWN_ERRORS Cause→Avoid rows. DESKTOP re-prove pending.
- **Design binding:** Prove 7 labels verified = **`PS_C_METRICS.md`** = PS-A map (no three-way mismatch); **`_prove_still_labels_drift_from_design`** blocks agent-invented cams.

## 2026-09-23 — PS-C-CAP-001 one-cam path canon (cloud, PR #198 `baef6e1`)

- DESKTOP **`cd7c258` ~11:38:** gate before **`CAM_CabinClose.png`**, **`settle_path` missing** while PNG on canonical disk — AL async vs non-unified poll path.
- Fix: **`_ps_c_canonical_still_path`** (AL ≡ settle ≡ manifest/gate); **`act_end`** only when **`paths_ready`**; gate defer poll before manifest; KNOWN_ERRORS row. Conductor: **one Act after PR** only; CAM-002 hold.

## 2026-09-23 — PS-C-CAP-001 one-cam sync writer (cloud, PR #198 `fd8aa8c`)

- DESKTOP **`98c7b36` ~12:09:** path canon OK; async driver + early **`act_end`** → settle **`exists:false`**, PNG same second as gate.
- Fix: **`_ps_c_one_cam_sync_capture_still`** + **`capture_viewport.wait_for_png_on_disk`** (single AL, render flush, no slate driver/defer). CAM-002 hold.


## 2026-10-02 - T0 #14/#15/#16 as code + doc consolidation (agent)

**Two false negatives found and fixed in one session, both the same defect class.**

`#17 Spirit-stealth` was recorded as `Found: Nothing` while it was LOCKED (2026-09-21),
implemented (`HomeWorldSpiritStealthComponent.{h,cpp}` + `HomeWorldSpiritLitVolume.h`) and CLOSED
under `APPROVE SS-A`. `#14` read `no guard/sleeper/soothe` while `TryAvoidNodeGuard` and
`TrySootheNodeSleeper` sat in the same component. Cause in both cases: **not missing docs, a missing
pointer.** The must list answers "what must be true"; "is it built?" lives in per-subsystem track
docs and nothing in the T0 track pointed at them. Same shape as the broken shrine - nothing named it.

Rule now enforced, not remembered: the `Found` column may say `N` only if no `APPROVE`-stamped
track doc claims the mechanic. `Docs/CANON_MAP.md` �3 is the cross-link; `test_canon_map.py`
asserts #17 cites its stamp and can never read `N` again.

**Structural findings.** `Docs/` and `docs/` are the SAME directory on this machine (identical
hashes, 441 md each) - the canon split asserted in `AGENTS.md` and `Docs/README.md` does not exist
on disk. `Docs/README.md` is a chronological wave log, so it answers "what did WAVE B do?" but not
"where is the camp-night rescue spec?".

**Camp night, as corrected by the Lead (Q25).** All THREE actors are calmed, not "avoid 1 + soothe 2":
the guard is eased awake->asleep, the two sleepers eased to *stay* asleep. The gate needs each
actor BOTH eased AND asleep. Consequences: avoiding the guard never opens the gate; a woken sleeper
closes it again and re-easing does not put them back to sleep; killed and converted both block it
(`EConvertedFoeRole` is what happens to foes you defeat - conflating it with care inverts the beat).

**Touch rule (#15), now code.** Allowed: `Soil`, `Lashings`, `ActorMind`. Refused: `ActorBody` -
a spirit has no hands. `ActorMind` is the exception that lets #14/#16 exist; `ActorBody` is what
keeps the beat about easing minds rather than dragging bodies. Every verdict logged.

**Fail-open contained.** The gate soft-latches when an actor is absent (kept: a reviewer is never
hard-blocked by missing content) but marks `bSoftLatch`. `SatisfiesFreedomGateStrict()` refuses
those and is the evidence half; the gameplay half logs `SOFT_LATCH_ONLY` so the difference is
visible instead of hidden in a return value. Before this, #14 could certify itself with zero actors
in the world.

**Evidence.** 17/17 T0 automation tests green headless on UE 5.8.2 (was 8, all 9 new camp tests
are world-free). `GetCalmedActorCount()` initially read 0 in two tests - correct behaviour, wrong
assertions: with no camp actors every ease soft-latches. Fixed by building the camp in those tests,
which also gives `FindCampActorInWorld` its first coverage at all. One assertion was outright wrong
(the "gate is three wide" check asked a fresh camp to already be complete). Mutation suite
`_mutate_camp_night.py`: M1 gate bypass, M2 ActorBody allowed, M3 eased-not-required, M4
converted-as-calm, M5 guard-ease-no-sleep, M6 actor lookup silently fails.

**Host test suite could not run at all** before this session - `pytest Content/Python/tests` aborted
during collection on 7 Editor-only files. `conftest.py` now detects them by scanning for a
module-level `import unreal` rather than listing them, and `test_host_collection.py` checks the
guard from a collected file (pytest does NOT collect test functions out of a conftest, so the first
self-check was dead code). 53 host tests green, up from zero runnable.

**Also:** `T0_M14_CAMP_NIGHT_GATE_PROVE.md` rewritten against the corrected beat, including a
`closed_fail` for a *silent* soft latch. `TryCampNight` rewired off the dead two-verb flow - it
would otherwise never have opened the new gate. Legacy verbs kept callable for Blueprint but marked
LEGACY.

**Still unbuilt:** the camp. No `NODE_GUARD`/`NODE_SLEEPER`/`NODE_CAPTIVE` in any `.umap`, so every
real run soft-latches. Blocks M8, M13, M14 and three prove scripts. Blocked on the camp image.

---

## 2026-10-02 - T0 must-list `Found` column: four more false negatives, and a real state check

**Asked:** "How are we on our canon docs health? Did we finish the consolidation and do we
have a single source of truth now?" - clarified to mean the **bible / vision**, not doc hygiene.

### The canon answer (the substance, not the indices)

The **vision axis is singular and consistent**: gather by day, tend by night; no kill-combat;
convert-not-kill; homestead non-combat. `VISION_BOARD.md` (V2b), `00_CANON.md`, `01_GDD_MVP.md`
and `canon/*` all agree on that. **But it reads as three bibles**, because the supersession was
never written down:

- `00_CANON.md` declares `LOCKED (P0)`; `canon/*.md` (12 files) declare `LOCKED`, last touched
  2026-09-21; `VISION_BOARD.md` declares `CANON for product work`, 2026-10-02.
- `canon/README.md:3` names `00_CANON.md` + `01_GDD_MVP.md` as the long sources of truth.
- **`VISION_BOARD.md` never once names `00_CANON.md` or `canon/`.**
- One load-bearing stale line: `canon/FANTASY.md:14` says the player is a
  *"Family co-op caretaker"*; VISION_BOARD §1 says *"You are **alone** and you have **lost
  something**"* + one rescued companion. It also contradicts its own `canon/DO_NOT.md:30`.

**Recorded as DEC-0029** (records the Lead's 2026-10-02 decision; takes no new one). NOT edited:
`FANTASY.md` / `canon/*` / `00_CANON.md` are Lead-LOCKED and "who the player is" is product
framing - human-owned. Escalated instead. `CANON_MAP.md` §0 now states the supersession at the
door.

### The `Found` column was stale for #1-#13 - a third batch of false negatives

The four `N`s were **grep misses, not absences**. `HomeWorldCharacter.h` declares a named `T0 #n`
hook for each, and for #2/#7/#8 the absence claim was contradicted by *passing* tests:

| # | row said | actually |
| --- | --- | --- |
| 2 | "No kettle/tea path" | `TryBrewNodeKettleTea` + `TryNodeKettleInteractInFront`; `HomeWorld.T0.M2.TeaGateOffWithoutBrew` passes |
| 7 | "`rune` = 0 hits" | `SetRuneGateUnlocked`; two-gate form; `M9.BothGatesGrantSpirit` passes |
| 8 | "`eject` = 0" | `TryCampDayEject` emits `NODE_DAY_CAMP`/`EJECT_HOME`/`TOD_DAY`/`FORM_BODY`/`CAM_T0_CAMP_DAY` (`HomeWorldCharacter.cpp:1915`) |
| 10 | "No reverse boot" | `StartGlideHome(bAllowNightPhase)` reusing the FALLBACK glide component (`HomeWorldCharacter.cpp:2010`) |

Also corrected: #1, #3, #4, #6, #9, #11, #12, #13 rows + the `#15` heading (still read
`**N (new, 2026-10-02)**` while its row said implemented). Every corrected `Found` row keeps
**logic** and **level** apart, exactly as #14's does: hooks exist, but **no `.umap` carries
`NODE_KETTLE` / `NODE_RUNE` / `NODE_DAY_CAMP` / `NODE_BED` / `NODE_PLANT_SLOT` /
`NODE_PORTAL_CAMP`**, so these have never run against a real world.

### CANON_MAP §6 was an overclaim - now made true

§6 claimed the suite checked that §3's `Found` values agree with the must list. **It did not** -
it only asserted must *numbers* appeared in both files, so the two documents could disagree on
every state and still pass. Same failure class as the stale rows. Two new tests fix it:

- `test_found_states_agree_between_map_and_canonical_must_list` - parses the real `Found` cell
  and the real heading, normalises both to one vocabulary (`N`/`Y`/`Partial`/`Logic done`/
  `CLOSED`) and compares. Pinned so a *deleted* heading cannot silently drop a must out of the
  comparison.
- `test_no_must_is_recorded_absent_while_a_t0_hook_is_declared` - greps `T0 #n` out of
  `HomeWorldCharacter.h` and fails if any such must is recorded `N`. This is the direct check on
  the four false negatives.

`_mutate_canon_map.py` extended M9-M13 for them. **13/13 mutations killed.** It earned its keep
twice: it caught a real ordering bug in the state vocabulary (`Partial (logic), unbuilt (level)`
must map to `LOGIC_DONE`, not `PARTIAL`), and it caught a typo of mine in the harness itself
(`agrees` vs `agree`) that had made three mutations look like survivors.

### Also in this commit
- Camp night as code: `HomeWorldCampNightTypes.{h,cpp}`, `HomeWorldCampNightTests.cpp` (9
  world-free tests), `HomeWorldSpiritStealthComponent` extended, `TryCampNight` rewired off the
  dead two-verb flow. **17/17 T0 automation tests green headless on UE 5.8.2.**
- Legacy verbs kept callable for BP, marked `LEGACY`. Soft latch contained via `bSoftLatch` +
  `SOFT_LATCH_ONLY`; `SatisfiesFreedomGateStrict()` is the evidence half.
- `CAMP.json` + `FIELD.json` both carry `spirit_touch`.

### Still blocked / not claimed
- **Camp geometry unbuilt** (`camp_named_objects: []`) - blocks M8, M13, M14 and three prove
  scripts. Blocked on the camp image (image work paused by the Lead).
- **6 beats `NO_VERDICT`** (M2, M3, M4, M6, M7, T0_default). **0 of 14 proven.**
- `APPROVE-T0-MECHANIC-INV` still unchecked while 13 PRs merged against it.
- M6 of `_mutate_camp_night.py` still unresolved; M2 repointed to `TYPES_CPP`.

### Durable lesson
> A `Found` column is a snapshot of whatever you happened to have open. Three times now a
> mechanic read as absent because no document pointed at the file holding it. The fix is not
> "look harder" - it is **two documents that must agree, machine-checked.**

---

## 2026-10-02 (session 2) - the camp exists, and the test that proves it was green for the wrong reason

Continuation of `11e8afb`. Lead answered three parked questions: correct `FANTASY.md` to the
Lone Wanderer, greybox the camp from `CAMP.json` now, and stop treating `Docs/` and `docs/`
as two trees.

### Landed
- **`AHomeWorldCampActor`** (`Source/HomeWorld/HomeWorldCampActor.{h,cpp}`). An `ACharacter`,
  not a greybox prop, because `CAMP.json` `rejects` lists that. Identity is carried by an
  actor **tag**; the editor-label branch is `#if WITH_EDITOR` and never runs at runtime.
- **Four actors placed** into `L_VS_MVP_Markers` by `Content/Python/t0_place_camp.py`
  (idempotent, `placed=0 reused=4`): `NODE_GUARD`, `NODE_SLEEPER_A`, `NODE_SLEEPER_B`,
  `NODE_CAPTIVE`. Every position derived from `CAMP.json` - trigger offsets and module
  offsets - not invented. Four UE 5.8 API bugs fixed along the way
  (`EditorLevelLibrary` deprecated, `set_actor_location` needs explicit `sweep`, enum by
  string, label stomping).
- **DEC-0029** - `Docs/VISION_BOARD.md` (V2b) is the operative vision for prototype scope;
  `00_CANON.md` / `canon/*` / `01_GDD_MVP.md` are an earlier cut, valid as Act 2+ background.
  `Docs/` and `docs/` are one directory on this case-insensitive filesystem.
- `FANTASY.md` protagonist corrected. `measured` in `CAMP.json` stays `null` on purpose.

### The finding worth keeping
A new test - `HomeWorld.T0.M14.PlacedActorsAreDiscovered` - asserts real placed actors are
found by tag alone and the strict gate opens. **18/18 T0 tests green.**

Then the mutation harness said otherwise:

- **M6 survived.** M6 disables the tag *and* object-name match in `FindCampActorInWorld`.
  It should have failed the new test. It didn't, because `SetActorLabel` had left every
  actor labelled `NODE_GUARD` / `NODE_SLEEPER`, and `FindCampActorInWorld` also matches the
  editor label - **a branch that is `#if WITH_EDITOR` and therefore does not exist in a
  packaged build.**
- So the test was green against a camp that soft-latches everywhere it actually ships.
  The three matching routes are editor label / tag / `GetName()`; only the last two survive
  a cook. A test that lets the editor label answer asks the wrong question and gets the
  right answer.
- Fix: `MakeRealCamp` now renames each actor to an opaque `CampGarrison_N`, which strips the
  label **and** the object name (`SetActorLabel` renames the object too), leaving the tag as
  the only route. It also places actors the way the script does - role change, then
  `RerunConstructionScripts`, **no** direct `RefreshCampIdentity()` call, because calling it
  explicitly would have masked a broken `OnConstruction`.
- **9/9 mutations killed**, restored tree re-verified green. Two harness bugs fixed on the
  way: M6's first form (`return nullptr;` at the top of the function) does not compile -
  it makes the body unreachable and UE treats C4702 as an error, so it was never scorable;
  and M2's pattern was one tab short, so it matched nothing and was correctly reported as a
  HARNESS BUG rather than scored.

### Durable lesson
> The green test and the shipped build are different questions. Ask which code path the test
> actually exercised, not which one the test name implies. `#if WITH_EDITOR` is a hole in
> every in-editor test suite.

### Not mine - left untouched and reported, not committed
34 untracked files predate this session (Sep 16 - Oct 1): 11 `Content/HomeWorld/Meshes/
Homestead/*.uasset` greybox props, `blender/floating_island_homestead_LIB.blend1`, and
`docs/` files from other streams (`decisions/DISAGREEMENTS.md`, `handoffs/TASTE_GATE_SCOPE_
R1-R4.md`, `qa/*`, `human-use/scope-refinement.md`). Committing another stream's work is
not mine to do.

## 2026-10-02 (session 3) - the gate that made six verbs unreachable, and a report that called six present volumes absent

### Landed

- `d4f4ed0` - the beat-node interactable gate now knows the seven beat-node tags. `ActorHasInteractableComponent`
  recognised only `AHomeWorldResourcePile`, `AHomeWorldCraftStation` and six named components, none of them a
  beat-node tag. A correctly tagged prop with a colliding collider was still rejected, and
  `FindInteractTargetInCone` did not rescue it because line 2668 re-checks the same gate. Placement was never
  going to fix those six beats. Added `namespace HomeWorldT0BeatNodes` with `TagsPerNode()` as the only place a
  tag is spelled, `AllTags()` derived by flattening it, and `TagsFor` / `ActorCarriesTagFor` /
  `ActorCarriesAnyBeatNodeTag` on top. Seven verbs dropped from about 17 lines of duplicated tag loop each to one
  call.
- `daaed6b` - `HomeWorldBeatNodeGateTests.cpp`: a 14-row table over **hardcoded** tag literals (reading them
  from the implementation's own table would make the test tautological), plus an end-to-end trace-to-verb test on
  #7 rune and #4 backpack because both are resource-free. Tag identity comes from the Actor **tag**, not
  `SetActorLabel` - the `WITH_EDITOR` label branch does not exist at runtime.
- `daaed6b` - extracted `HomeWorldTestWorld.h` (`FScopedWorld`, `SpawnCharacter`), replacing three
  byte-equivalent copies across the camp-night and day-gate tests. Note for anyone using it:
  `APawn::GetControlRotation()` returns `FRotator::ZeroRotator` with no controller, and a zero rotator points
  +X, so the fixture's aiming depends on that.
- `68f0dd4` - 11 `Found` cells in `Docs/handoffs/T0_MECHANIC_INVENTORIES_V1.md`. Nine read `Still unbuilt: no
  NODE_X in any .umap`, which reads as "place the prop and the beat closes". It would not have. Two were stale
  about the camp, which has had actors placed in `L_VS_MVP_Markers` since `4920c90`. None of the rewrites change a
  verdict - they only stop the doc naming the wrong blocker.
- `000927d` - the greybox report no longer calls six present volumes absent. `VOLUME_ALIASES` exists because the
  specs name *modules* while the blend authors some as mirrored pairs (`_Front`/`_Side`, `_L`/`_R`, the hero
  island as `SM_IslandTop`), and its own docstring says reporting one of those as not present "is a false
  finding that trains the Lead to ignore the report". The verifier honoured that - `measure_scene` expands every
  alias and `verify` walks `resolve_alias` before checking `1_location` and `2_sized`. `to_markdown` did not: it
  iterated the raw measurements dict, so it printed `*(absent)*` for the spec name and the geometry holding the
  real size two lines below. Half the fix was in place; the half anyone reads was not. Six rows now read as
  resolved with a `via` annotation naming the object measured, and the `2_sized` mismatch for `SM_Island_Hero`
  surfaces precisely (y 10.700 vs spec 14.000) instead of hiding behind "absent".
- `6e0b2e4` - `ASSEMBLY_FOOTPRINTS` was documented as "half-extents" while the containment check halves each axis
  first. The data are full extents. Comment only, no value and no behaviour changed, but a wrong comment on a
  tolerance constant is load-bearing: the comment is what a reader trusts when the number looks wrong. Provenance
  is now per entry, because the original claimed `overall_size_m` for all three and only the cabin has one.

### Verification - what is proven and what is not

- **The `NodeGate` fix is NOT verified.** `UnrealEditor-Cmd.exe HomeWorld.uproject -ExecCmds="Automation RunTests
  HomeWorld.T0; Quit" -unattended -NullRHI` logs `Ready to start automation` and then emits nothing: no report
  export, `Quit` never fires. The same command returned 16/16 green earlier the same day. Ruled out by
  measurement - it stalls with a filter matching zero tests, with and without `-NullRHI`, with an explicit clean
  map argument, with the asset registry cache deleted, on an idle box. Reading `AutomationCommandline.cpp`,
  `FWaitForInteractiveFrameRate` passes and `FindWorkers` / `HandleRefreshTimeout` never log, so the command queue
  is going empty rather than searching for a worker. Recorded in `docs/KNOWN_ERRORS.md`.
- **No green UE suite may be claimed from an earlier run.** The host Python suite is the only harness currently
  executable, and it is green at 70.
- So the beat-node gate fix is compile-verified and unit-tested but never executed. `HomeWorld.T0.NodeGate.*` is
  red-before / green-after on paper only. Stated plainly rather than rounded up.
- Two flag traps worth remembering: `-TestExit=` cannot contain spaces (`FParse::Value` stops at whitespace), so
  `-TestExit="Automation Test Queue Empty"` silently degrades to `TestExit: Automation` and exits at startup. And
  `-ExecutePythonScript` is run-and-exit - the editor quits when the script returns - so the `t0_m*_prove.py` PIE
  harness is unrunnable by construction. The space form of that flag is not parsed at all; the editor idles
  forever.

### The mutation harnesses earned their keep twice

- `_mutate_graybox_aliases.py` found dead code in my own first version of the alias fix: an `alias_only` check
  inside the spec-name loop that could never fire, because `alias_only` holds names that are *not* declared
  volumes. Removing it changed nothing; a second, subtler one followed, a subtraction subsumed by the next loop's
  own condition.
- The same harness then scored its own declared survivor as killed, because survival was computed from the test
  name instead of the run. `detected = test is None or test in failed` makes every `None` entry a guaranteed
  kill, so the file would have reported evidence it did not have.
- `_mutate_graybox_extents.py`'s first M1 removed `* 0.5`, which *widens* the containment box, while claiming to
  tighten it. It killed the mutation either way, but the wrong half of the matched pair. A harness that reports
  the kill it got as the kill it wanted will one day report a miss as a hit.
- Standing traps, all three still live: an uncompilable mutation is not evidence (UE treats C4702 unreachable
  code as an error, so `return nullptr;` at a function top can never be scored); a regex matching nothing must be
  reported as HARNESS BUG and scored a survivor, not skipped; adding a `case` that already exists fails to
  compile (C2196), so edit the existing return instead.

### Durable lesson

> A gate that is not reachable is not a missing prop, and a finding that is not true is worse than a missing
> check. Both halves of this session are the same shape: something downstream was reporting faithfully on a
> subject it had never actually looked at, and the report said so in words nobody questioned. The tell in each
> case was a doc that explained the intent correctly - the alias table's docstring, the must list's
> `Still unbuilt` clause - sitting next to code that did the opposite.

### Not mine - left untouched and reported, not committed

- `blender/floating_island_homestead_LIB.blend1` is untracked. The `.blend` itself is byte- and mtime-identical
  across the regeneration runs - the reader ran read-only with `place=False` - and neither was committed.
- `92e2dbc` (the Lead's porch exclusion) also edits `Content/Python/graybox_spec_reader.py`. Checked intact. It
  is also why the regenerated report's blocking count reads 5 and not 8: that commit removed three porch findings,
  not my renderer change, which cannot touch `findings`.
- Ruff reports 194 findings across `Content/Python/`. Pre-existing and in other files; the three I touched are
  clean.

### CORRECTION - the `### Landed` list above is wrong about `d4f4ed0`

Appended rather than edited, per the append-only rule, so the mistake stays on the record.

**`d4f4ed0` is not landed.** It is the tip of branch `keep/interact-gate` and is **not an ancestor of
`main`** (`git merge-base --is-ancestor d4f4ed0 HEAD` exits 1). On `main`,
`ActorHasInteractableComponent` still recognises only `AHomeWorldResourcePile`, `AHomeWorldCraftStation`
and six named components, and no beat-node tag, so all six affected verbs are unreachable in every world.
The "Landed" bullet above, and the nine must-list cells written in `68f0dd4` that said the gate "is now
fixed in `d4f4ed0`", were both false. Both now say so.

Two things made this survivable for a while and neither was checked:

- **The commit succeeded.** A commit that was created is not a commit that is reachable from the branch
  that ships. `d4f4ed0` resolved as a hash, and every subsequent command that referenced it succeeded -
  `git show`, `git log --all` - because those ask whether it exists, not whether `main` has it.
- **The checkpoint summary said "Landed".** I carried that forward and then wrote nine rows on its
  authority. A prior summary is a claim, not evidence, exactly like a test result that never ran.

The check is one command: `git merge-base --is-ancestor <sha> HEAD`. It costs nothing and it is the
difference between "the fix exists somewhere" and "the fix is in the branch we ship".

Two further consequences:

- `docs/KNOWN_ERRORS.md` gained its automation-harness-stall entry and its gate-defect entry **inside
  `d4f4ed0`**, so neither was on `main` either. Both are re-recorded on `main`.
- **The order of the whole session was wrong, not just one claim.** The six-verb blocker was found, fixed,
  tested, written up and treated as closed while `main` never received it. Every subsequent piece of work -
  the must-list correction, this summary, the `000927d` and `6e0b2e4` commits - was reasoned from the
  premise that `main` had the gate fix. It did not. Whether those commits are still correct is a question
  worth asking explicitly; on inspection they touch disjoint files (`Content/Python/`, `Docs/qa/`,
  `Docs/handoffs/`) and never depend on the C++ gate, so they stand, but that should have been checked when
  the premise broke rather than after.

**Not merged unilaterally.** `git merge-tree main keep/interact-gate` exits 0 and the two file sets are
disjoint from `87d42c8..main`, so the merge is mechanically clean. A branch named `keep/` may be parked on
purpose by someone who intends to review or rebase it, and this is not mine to decide. Flagged to the Lead
instead of merged.
### Correction and closure: the gate fix is landed, the build was broken, and the suite is green for the first time

Appended 2026-10-02. This supersedes the two entries above in one respect: the beat-node gate fix is
now on `main`, and `main` compiles and passes. What follows is the evidence, because the previous
entries in this file were written on evidence that turned out to be wrong twice.

**1. The harness was never broken. My diagnosis of it was.** The "stall" that was recorded here as an
environment regression was a PowerShell quoting fault of mine: `-ExecCmds="Automation RunTests ..."`
reached UE as the single word `Automation`, so `FParse::Value` truncated it and the deferred queue
idled with nothing queued. PR #277 fixed the invocation. A second, separate mistake: the runner reads
`UE_EDITOR` from the environment, and that variable pointed at UE 5.7 while the project lock is 5.8,
so runs were silently executing the wrong engine. With the engine correct, the quoting correct, and
`Automation RunTests HomeWorld.T0` (a name filter - `RunTest Group:` filters UE groups, not name
prefixes, and `Group:HomeWorld` matches nothing), UE loads 6615 tests and runs the group in seconds.

**2. The 19/19 green that drove every conclusion in this file was a stale DLL.** `Safe-Build.ps1` had
not been run after the NodeGate tests landed, so the automation was executing an older binary that
genuinely passed. The tell was available before the rebuild and is now in KNOWN_ERRORS: a 0.0117s
duration for a test that builds a `UWorld` and spawns fifteen actors, and 20 `Success` results with
zero `Fail` across 33 rotated logs. After a rebuild the same command reported
`NodeGate.AllBeatNodeTagsAreInteractable` **Fail** with 15 errors. A deliberate `AddError` that cannot
be satisfied was placed at the top of the test to establish that the harness surfaces errors at all;
it reported `Fail`, which makes the 14 row failures real rather than a silent-pass artefact.

**3. Landing the fix exposed that `main` did not compile.** Cherry-picking `d4f4ed0` conflicted only in
`docs/KNOWN_ERRORS.md` (resolved by keeping the branch's better quoting entry plus two new ones);
`HomeWorldCharacter.cpp` applied clean. But the build then failed with **53 errors across four files**,
three of which this work never touched. Cause: an edit made while removing the deliberate-failure probe
had deleted the function signature and opening brace of
`FBeatNodeTagsAreInteractableTest::RunTest`, leaving its body at namespace scope. In a UE unity build
the orphaned `FScopedWorld Scope(...)` collides with correctly-scoped `Scope` locals in its unity
siblings, so `C4459: declaration of 'Scope' hides global declaration` fired against
`HomeWorldCampNightTests.cpp`, `HomeWorldDayGateTests.cpp` and `HomeWorldFormGateTests.cpp` - all
pristine. That broken state was in `c2bff14` and was reported as done.

What located it was reading the **first** error in the log rather than the last: `error C2059: syntax
error: 'if'` at line 181, immediately after the orphaned statement. The C4459 lines dominate the log by
count and are pure downstream noise. `git diff daaed6b -- <file>` then showed the two deleted lines
immediately. Restored with `git checkout daaed6b -- <file>` rather than by hand-editing back to an
approximation, so the file is byte-identical to its baseline. `c2bff14` was local-only and never
pushed, so no shared branch carried it.

**4. Verified state at `df00858`.**
- `Safe-Build.ps1` exits 0 **against this commit**, confirmed twice: once incrementally, then after
  deleting `Binaries/Win64/UnrealEditor-HomeWorld.dll` to force a relink.
- Freshness proven, not assumed: DLL mtime `23:45:28`, newest source under test `23:43:26`. The binary
  is newer than every file in `Source/HomeWorld`.
- `Automation RunTests HomeWorld.T0` against that exact DLL: **19 succeeded, 0 failed, exit 0**, every
  test `err=0`, including both `NodeGate` tests.
- Host suite **70 passed**. Mutation harnesses 4 killed / 1 survived and 2 killed / 1 survived; the
  survivors were declared with reasons when those harnesses were written and have not changed.

**What this session's greens are and are not worth.** This 19/19 is the first full-suite result that a
build can vouch for, so prior T0 verdicts citing automation output are now re-runnable rather than
void - but they still need re-running before being called proven, and nothing here establishes that
the beats are *good*, only that the code runs and the asserted laws hold. No playtest was performed.

**Two questions still open, unchanged from before.** `SM_Island_Hero` is authored at 19.3x10.7 against a
spec of 21x14 (off by 3.3 with 1.4 tolerance); rescaling authored geometry is forbidden, so it is
either record-target-not-met or reconcile-the-spec, and that is a human call. And the must-list rows
for these beats should be revisited now that the fix is genuinely landed rather than re-cited from a
claim.
---

## 2026-10-03 - the fix is pushed, and the harness under it turned out to be the real story

**Land state.** `main` is clean and `origin/main` is level with it. Five commits, none of them
carrying a commit that fails to build:

| Commit | What |
|---|---|
| `031e711` | the beat-node interactable gate fix, applied to `main` as one commit rather than cherry-picked |
| `066ba61` | session record correcting the harness and stale-DLL conclusions (append-only) |
| `296e50f` | the nine must-list rows, which had been corrected to say the fix was parked |
| `a748271` | `run_ue_automation.py`: it had never once parsed a report |
| `c2c3d41` | two red rows in the full group that were never about the product |

`git merge-base --is-ancestor 031e711 origin/main` exits 0. Only `Source/HomeWorld/
HomeWorldCharacter.cpp` changed on the C++ side, and that commit is the one verified against
`Safe-Build.ps1`.

**The squash decision, made and recorded.** The three earlier commits were replaced by two rather
than pushed as-is, because `c2bff14` shipped a file with a deleted function signature and its body
at namespace scope. Nothing pushed carried it. `git log` history is now bisect-safe: every commit
on `main` compiles.

**`run_ue_automation.py` had never measured anything.** It is the file agents are pointed at
instead of reading the UE log. It reported `passed: 0, failed: 0` on every run ever, because UE
writes `index.json` with a UTF-8 BOM, `json.load` raised, the `except` clause caught it, and the
function returned its not-found branch. Read as `utf-8-sig` now. Four more defects in the same file
could each have produced a false green on its own - unchecked engine lock, a `--group` selector
matching no UE group judged by `failed == 0`, an uncleared report directory, and no DLL freshness
check - and all are now closed. Verified end to end rather than by inspection: `--filter
HomeWorld.T0` returns exit 0 on UE 5.8, and a 5.7 `UE_EDITOR` is refused before UE is launched.

**Running the full group for the first time found two reds, and they were not the product.** Both
were `import pytest` at module scope failing inside the engine's bundled Python. Converted to
`unittest.TestCase`; host pytest collects those natively so nothing was lost.

**But the conversion did not do what it looks like it does, and the positive control is the only
reason I know that.** A deliberately false assertion was planted in one of the two files: host
pytest failed it, and the editor run reported **Success**. The editor's Python automation runner
reports one row per module and only *imports* it. It does not execute `TestCase` methods and never
executed bare `test_*` functions either. So thirteen green `Editor.Python.*` rows assert nothing,
and `test_run_ue_automation.py` alone contributes one green row for twelve functions. **Host
`py -m pytest Content/Python/tests` is the only thing that runs the Python laws** - both file
docstrings now say so, and there is a KNOWN_ERRORS entry.

Two further traps came out of that work. A `__main__` guard calling `unittest.main()` fails these
modules, because the runner imports with `__name__` set to `"__main__"` and the block raises
`SystemExit` out of the import. And both mutation harnesses were matching `FAILED` lines with a
pattern that captures the class rather than the method for a unittest module, scoring a killed
mutation as SURVIVED - a false "the test no longer bites" reading, in the one tool whose job is to
catch exactly that.

**Final state, measured.**

- `Automation RunTests HomeWorld` (full group, first time ever run): **42 succeeded, 0 failed,
  43 listed, exit 0**, fresh DLL, UE 5.8, `dll_stale: false`.
- `Automation RunTests HomeWorld.T0`: 19 tests listed, 0 failed.
- Host suite: **81 passed + 3 subtests**.
- Mutation harnesses: **4 killed / 1 survived** and **2 killed / 1 survived** - unchanged from
  before the conversion, now with correct attribution.

**One measurement that is still unexplained.** UE's report counters disagree with UE's own list of
tests: `succeeded: 19` while listing 20 tests on T0, and 42 while listing 43 on the full group. The
runner now carries both numbers and warns rather than quietly preferring one. UE's exit code is 255
on a fully green run, so the report is trusted over the exit code, loudly. Neither is understood;
both are recorded rather than smoothed over.

**Still not established.** No playtest. 42 green means the code runs and the asserted laws hold.
It says nothing about whether the beats are any good, and the thirteen Python rows in that total
are import checks, not law checks. `SM_Island_Hero` remains the open human decision - authored
19.3x10.7 against a spec of 21x14, rescaling authored geometry forbidden, recommendation
record-target-not-met, raised with the Lead twice.
## 2026-10-03 (later) — polish readiness gate, and one line of arithmetic that fails

**Question put to me:** how ready are we to start the human polish pass on environment
size, asset pass 1, and mechanics feel 1; what is industry procedure for it; and set up
or reuse a pipeline that minimises rework. Directions given: work now, taste only via
interview, greybox tier only, never overwrite authored geometry, do not commit
`.blend`/`.uasset`, append-only to this file, temp files in the temp dir and deleted.

### The finding that matters most

`Docs/canon/FEEL.md` declares an island circuit window of 45-90 s. The character walks at
**600 cm/s (6.0 m/s)** — a number that had never been written down anywhere in the
project, because it is a C++ default on `ACharacter` sitting in a Blueprint CDO. The
island as authored is **19.3 x 10.7 m** (spec says 21 x 14, and that disagreement is
already a recorded waiver). As an ellipse that is a **48 m perimeter, an 8.0 s lap**.

The window's *floor* of 45 s therefore needs **270 m of walking against a 48 m lap: 5.6
laps**. A circuit that winds five times is not a circuit. Either the island is roughly
2.3x too small, or the window was a GDD guess never checked against the world, or the
circuit is meant to be partly flown on FALLBACK (12-25 s in the same table) and even then
needs 120 m against a 48 m lap. Only one can be true and it is not an engineering call.

This was knowable the moment walk speed and island size both existed. The island was
authored at 19.3 m long before anyone divided.

### What was built

- `Content/Python/polish_readiness.py` — 16 checks across three gates. Rule:
  **absence of evidence is not evidence of readiness.** MISSING is never PASS; exit 2 is
  reserved for "could not measure at all". Waivers key on the finding's full
  (criterion, volume, detail) identity because the greybox report files several
  independent blockers under one criterion for one volume. A waiver naming a finding that
  no longer exists reports STALE. `--selftest` asserts the gate can still fail.
- `Content/Python/probe_movement_budget.py` — extracts walk speed from the character
  CDO. Runs inside the editor via `-run=pythonscript`.
- `Content/Python/traversal_budget.py` — the feasibility check above. Reads `FEEL.md`'s
  windows by parsing them rather than restating them, so it cannot drift from canon.
- `Docs/37_POLISH_PASS_PROCESS.md` — the stage ladder, the three gates, the industry
  grounding, and the ownership boundary.
- 24 regression tests plus a mutation harness proving the tests can fail.

### Errors found in my own work before shipping (recorded because the pattern recurs)

1. The pivot check originally looked for a criterion named `2_sized_origin`, which does
   not exist — it matched nothing and would have reported **PASS with the blocker live**.
   The report files both the island size mismatch and the island pivot under `2_sized`,
   so the check now narrows by detail text.
2. `--selftest` could not test the waiver logic, because `_criterion_check` read the real
   report from disk and the synthetic waivers never matched it. The report is now
   injectable — left as-is, the guard was unfalsifiable in exactly the situation it
   exists for.
3. `_rel` crashed on a path outside the repo. A gate that crashes while describing where
   it looked has failed at its one job.
4. The gate covered **4 of the 5 blocking findings and did not say so**, while presenting
   itself as *the* greybox gate. `4_distinct` was simply absent. This is the worst one: a
   gate that reports honestly on a subset reads as coverage of the whole. Coverage is now
   asserted in selftest, and the assertion is itself tested for falsifiability.
5. `traversal_budget.py` compared a **point-to-point** distance against the island's
   **perimeter** and reported `cabin_to_lookout_s` NOT_REACHABLE with the note "arithmetic,
   not an opinion". A 150 m path across a 19 m island just means crossing it about eight
   times, which is an ordinary winding route. It would have sent someone to re-cut a
   perfectly good window. Only a **closed loop** is bounded by perimeter, so only that
   shape may be declared unreachable.
6. The spec lookup used `SM_IslandTop` where `ASSEMBLY_FOOTPRINTS` is keyed on the
   assembly root `SM_Island_Hero`, printing a literal "None m" in a credibility table.
7. The movement probe read several properties in one `try`, so one mis-named property
   (`max_walk_slope`, which is `walkable_floor_angle` in 5.8) discarded four good values
   and reported the walk speed as unreadable when it had been read successfully.

### Headline correction to a prior conclusion

An earlier note in this session said the world was not assembled because only two `.umap`
files exist and the docs call them DemoMap and Homestead. **That was wrong.** `MainMenu.umap`
carries **1,270 placed external actors** and built HLOD layers. The world is assembled and
is misnamed in documentation, which is a cheap documentation fix.

Also corrected: `Docs/CANON_MAP.md` claimed 8 blocking greybox findings; the report says 5.

### Still blocked, unchanged

- `SM_Island_Hero` — authored 19.3x10.7 vs spec 21x14, tolerance 1.4. Recorded as a
  waiver, explicitly **not** a resolution. Raised twice with the Lead, dismissed twice, not
  re-raising.
- **Mechanics feel 1 cannot start.** No human has ever played this build. 109 green Python
  tests and 43 green automation rows are code assertions; they say the verbs fire and
  nothing about whether the island is the right size or the glide the right shape.
- The circuit finding needs a human ruling. Waiving it is not available and should not be:
  two of the three numbers involved would still disagree while the report said the check
  passed.
- G-ENV remains RED on the island pivot, two materials outside the ten masters, silhouette
  distinctness, the circuit contradiction, and the absent timing instrument.

### Rules that follow

- A measurement instrument that needs the game running must not be built as if it does not.
  Report the missing instrument honestly and check what *can* be checked headlessly.
- World Partition geometry does not exist in a commandlet — a map reporting 0 meshes under
  `-run=pythonscript` is not an empty map.
- When a check narrows within a criterion, assert that the narrower filter matches
  something. A filter narrower than the data is indistinguishable from "fixed".
- Verify append-only records in bytes against `git show HEAD:<path>`, and print the byte
  counts from Python. Piping `git show` through PowerShell reported a 177 KB file as
  746 bytes.
---

## SESSION 2026-10-03 (afternoon) - the world was already built; two things hid it

Lead instruction, verbatim: the homestead is a **floating island**; you jump off
the edge toward the starting zone and *"no matter what you do while you are
travelling toward the ground, you will land in the field."* The drop exists to
convey relative size and speed. Numbers are the Lead's polish-pass work - build
the skeleton so everything exists to be adjusted.

### Two defects made the game unplayable and invisible

**1. Play went nowhere.** `UHomeWorldGameInstance` defaulted `GameMapPath` to
`/Game/HomeWorld/Maps/DemoMap`. That asset has never existed in Content.
Verified against the 5.8 asset registry: DemoMap `false`, Homestead `false`,
`L_VS_MVP_Markers` `true`, MainMenu `true`. `OpenLevel` to a missing map is a
silent no-op and nothing covered the menu's travel target. Now defaults to
`L_VS_MVP_Markers`, logs the choice, and resolves the target before travelling
so a future miss logs an Error naming the fix.

**2. The fall soft reset cancelled the drop.** `FallResetDropCm = 2200` (22 m)
and `FallResetSeconds = 2.75` against an authored **95 m / 9500 cm** drop to
`SM_Planet_GroundPlate` (top at Z -95.0, island walkable surface at Z 0).
22 m is 23% of the drop; the time limit is 62%. Walking off the rim teleported
the player back onto the rim, 73 m above the field. The net was written for
slipping off a small ledge and was never reconciled with an authored 95 m drop.
Added opt-in `bRespectDropCorridor` + `IsOverLandingGround()` (traces the fall
corridor for somewhere to land). **Default off**; the tuned values are
untouched because they are feel and they are the Lead's.

### The world was already in the project

`MainMenu.umap` (the GameDefaultMap) is 25 KB of World Partition plus 1,270
external actors of kit-bash rock/plank/brick. Grepping all 1,270 for
`SM_IslandTop`, `SM_Planet_GroundPlate`, `CRUMB_`, `SM_Cabin`, `SM_Lookout`,
`SM_LandingCircle` returns **MISSING on every one**. That reads exactly like
"the homestead was never placed."

It was placed. `L_VS_MVP_Markers.umap` (226 KB, not World Partition, so actors
are inline) holds **78 StaticMeshActors, 25 labelled TargetPoints
(GP_PlayerStart, GP_GlideStart, GP_PortalA/B, GP_SpiritWisp_A-C,
GP_Store_BERRY|FIBER|HERB|SEED|STONE|WOOD, GP_N1_Crop, GP_N2_Stored,
GP_BeastPad), the full CRUMB_* glide path + CRUMB_GlideSpline, 5 cameras,
6 StoreProps, 4 CampActors, 3 SpiritWisps, 2 NurtureTargets, 2 ShrinePortal
Triggers, 1 PlayerStart, 1 BeastPad**. Every gameplay class in Source/HomeWorld
is represented. The blend holds 437 objects including the 80x70 m field, 3
islets, 16 planet pines and hamlet roofs.

Lesson worth keeping: **do not conclude a map is unbuilt.** A World Partition
map's geometry lives in `__ExternalActors__`; grep the `.umap` alone is
meaningless, and an empty result can mean "different level", not "no level".
Recorded in KNOWN_ERRORS 2026-10-03.

### The island pivot was a wrong assertion, not wrong geometry

`SM_IslandTop.json` declared `"origin": "ground_contact"` while also declaring
`world_top_z: 0.0` and placing **all 10 sockets at z 0.0**. Those cannot both
hold: at ground contact the sockets would float 0.5 m above the walkable
surface. A floating island has no ground to contact, so the criterion was
about a surface that does not exist there.

Three sources agreed the top surface is the datum:
- Blender: origin (0,0,0), local Z -0.45..0.0
- UE 5.8 import: 19.3 x 10.7 x 0.45 m, local Z -45..0 cm
- Siblings: Lookout_Pad z=0, Glider_Perch z=0, PathStone z=0.02, beds z=0

So the geometry was correct and the check was wrong. Added `top_datum_z_m` read
from `world_top_z`; a declared datum means floating, so ground contact is no
longer asserted for it, and `verify()` instead asserts the origin sits at the
datum **and** the mesh reaches it - two independent blocking failure modes,
plus "origin unmeasurable is blocking" because absence of evidence is not
evidence. `measure_object` now reports `top_vert_z_world`. Ground-contact
volumes are untouched; a test asserts `SM_Cliff_LookoutFace`/`Rear` still hold.

**Criterion swap, not a gate loosening** - and proved to be: the new test drives
`verify()` with an origin 0.5 m off, a top that never reaches the plane, and an
unmeasurable origin, requiring a blocking finding each time, and asserts the
datum landed on exactly one volume.

Graybox report **5 blocking -> 4**. G-ENV FAIL 4 -> FAIL 3.

### A correction to our own KNOWN_ERRORS

An earlier entry claimed `EditorLevelLibrary.get_all_level_actors` "does not
exist in 5.8". **False.** Measured on `++UE5+Release-5.8-CL-56702186`:
`hasattr` True, the call returns a real Array. 56 call sites across
`Content/Python/*.py` use it; taken at face value that note justified rewriting
all 56 - a large, pointless, risky change to working scripts. Corrected in place.
**Rule established: "this API is gone" is a measurement claim. Probe it before
recording it.** A reader cannot tell a wrong entry from a right one by tone.

### Research requested by the Lead

`Docs/38_AI_AGENT_PRACTICE.md`. Headline: CraftBench-UE (arXiv 2609.23142)
measured that among on-time Blueprint submissions that passed asset checks,
**42.2% and 50.0% failed explicit runtime assertions**, and C++ beat Blueprint
by 30-43 points. That is our own positive-control finding in peer-reviewed form.
METR RCT: AI-allowed work took **19% longer** while developers believed 20%
faster - a ~40 point perception gap, so measure agent ROI with a clock. Epic
shipped a first-party MCP in UE 5.8 (`ModelContextProtocol` + `AllToolsets`,
with a Testing toolset) and an official Claude Code plugin. Stated gaps: no
primary source for Gauntlet-as-AI-gate, and no credible practitioner spec for
AI-driven Blender->UE blockout guardrails.

### State

- 116 pytest pass (was 109). `HomeWorld.T0` 19/19, build green on 5.8.
- Commits this session: `022bef5` fall/drop, `0a0938d` menu map, `ff619b0` island datum.
- **No .blend or .uasset touched or committed.** No feel value changed.

### Still human-owned, not agent-resolvable

`SM_Island_Hero` 19.3x10.7 vs spec 21x14 (raised twice, dismissed twice, not
re-raising). `M_FamilySilhouette` and `M_ValleyNight` outside the ten masters -
rebinding or adding them is a canon call. One `4_distinct` collision on
`SM_NODE_PLANT_SLOT_DAY_PLANTED`. `Docs/29_TASTE_PROFILER.md` exists and no taste
profile has ever been bootstrapped. And **no human has played this build**:
every green row above proves code runs and asserted laws hold, nothing about
whether the island reads or the glide feels.

## SESSION 2026-10-04 (early) - the island got its locked footprint, and four wrong claims got retracted

### The 180 x 100 plate is in, and the rim is generated rather than transported

`SM_IslandTop` now measures exactly **180.0 x 100.0 x 0.45 m** with the top face at
Z = 0 exactly, satisfying `Lib/01_Homestead/SM_IslandTop.md` outright. Topology is
preserved: 32 verts, 18 polys, 16-point rim. Nothing else in the scene moved - the
homestead core simply became interior to a larger island.

The rim is generated on the 90 x 50 ellipse, not carried over from the authored
19.3 x 10.7 outline. Two transports were tried and both were rejected on
measurement, which is why `AssetCreation/Blender/apply_island_plate.py` says so
plainly instead of claiming the authored silhouette was preserved:

1. Carrying each authored vertex's deviation-from-ellipse across gave k up to
   **1.81** and a **272 x 137** result - 92 m over on X.
2. Anisotropic scaling to exactly 180 x 100 is clean, but the authored shape
   pinches 24.6% inside the ellipse at its corners, so the locked 90 x 50 walk
   oval escaped the rim by **8.9%** at -100 deg. A circuit you can walk off the
   edge of is not a circuit.

So k is exactly **1.00** at the four axis directions and **1.05 / 1.10 / 1.15**
elsewhere. **0 of 16** values needed the clamp. Angles are on 5-degree steps and k
on 0.05 steps at the Lead's direction, so one number can be moved by hand in the
polish pass: edit `RIM`, re-run, read the `PLATE_` lines.

Two consequences reported rather than silently chosen, both feel judgements:

- **The bulges fall only in the X-dominant directions.** On a 2:1 ellipse the k
  ceiling collapses to ~1.01-1.02 within 20 deg of the minor axis, so near 70,
  110, 170, 250 and 285 deg only k = 1.00 fits. Irregularity near the Y axes
  would need k < 1, which would let the walk oval leave the island.
- **The walk oval is inscribed and touches the rim at four points** (+-90 X,
  +-50 Y). That is arithmetic, not choice: the Lead's footprint 180 x 100 and
  oval semi-axes 90 x 50 are the same numbers.

### Four retractions

Everything below was stated to the Lead earlier and was wrong. Each was caught by
a measurement, not by reasoning harder.

- **"The island circuit stays NOT_REACHABLE, 1.2 laps."** Wrong.
  `ellipse_perimeter_m()` takes **full extents** and halves internally; I fed it
  `(90, 50)`, the walk oval's semi-axes, instead of `(180, 100)`. At 180 x 100 the
  perimeter is **448.8 m**, a lap is **74.8 s** at 6.0 m/s, which is inside the
  45-90 s window. The verdict is **REACHABLE**. My original 448.8 m was right all
  along.
- **"An invented ninth verb should block PASS."** Wrong. If all eight ran, PASS is
  honest. The real defect was that the extra key was dropped in silence; it is now
  named in the note as non-blocking and the count reports eight.
- **"SM_Cliff.json carries no placements, so that citation is false."** Wrong. The
  three cliff origins are in `modules[].origin`. My search only matched keys
  containing `pos`/`loc`/`place`/`bl_`/`xyz`/`transform` and missed `origin`.
- **"There is mojibake on those lines."** Wrong. The bytes are clean UTF-8 with
  U+2014; the `?` was PowerShell console rendering. Same false conclusion as the
  FEEL.md en-dashes earlier.

The common shape: three of the four were **absence of evidence read as evidence**,
and the fourth was **a measurement claim made from the wrong input**. A narrow
search returning nothing is not a finding.

### The stale waiver was deleted, not re-issued

`Docs/qa/polish_waivers.json` held a `2_sized` waiver reading "y bbox 10.700 vs
spec 14.000". Its own un-waive condition had fired - "if the island is later
resized" - which is what happened. The finding it named no longer exists, so
keeping it could only ever read STALE. History is kept under `_waiver_history`.
There is nothing to replace it with: `2_sized` raises no findings at all now, so
the size question is settled by geometry rather than by a waiver.

### Gate movement, and what is still red because it is human work

Greybox blocking **5 -> 3**, and `2_sized` is **gone** rather than waived. The
remaining 3 are the art findings the Lead ruled stay RED. Gate G-ENV: FAIL **3 ->
2**, STALE **2 -> 0**, PASS **2 -> 5**; `island_sized`, `pivot_grounded` and
`traversal_reachable` all PASS.

Everything still RED is a person, not a task:

- `master_binding` (M_FamilySilhouette, M_ValleyNight), `family_distinct`
  (SM_NODE_PLANT_SLOT_DAY_PLANTED) - the art pass.
- `asset.board` **0/10 declared** - skeleton seeded, unfilled on purpose.
- `human_playtest`, `verb_script`, `tunable_baselines` - all MISSING. **No human
  has ever played this build.**

### Two new fail-opens, both found by tests written minutes after the code

- `asset.board` tested `if a.get("stage")`, and null is falsy, so a seeded board of
  nulls read **FAIL** instead of MISSING. Same trap as the playtest record: FAIL
  leaves "type anything" as the only route to green.
- The first version of the `place_vs_mvp_pa_d.py` number pattern was written with
  doubled backslashes (`\\d` in the source, matching a literal backslash) and
  matched nothing. Only a manual run against the real spec file caught it. It is
  now a permanent test, mutation-tested by re-introducing the bug.

`place_vs_mvp_pa_d.py` now **reads** `SM_Cliff.json` and `GARDEN_BLOCKING.md`
instead of restating them under comments that cited them, and raises rather than
falling back to a literal. The four edge-midpoint fence segments are derived from
the spec envelope, so editing the envelope moves the rail. Worth noting: the
Markdown specs are **typographic** where the JSON specs are ASCII - the garden
writes its minus as U+2212 and its size separator as U+00D7 - so a pattern written
for one spelling silently finds nothing in the other.

### State

Branch `main` at **a33ae07**, pushed and verified by ancestry. `polish` and
`origin/polish` untouched at `f218fce` / `9686e68`. Tests **165 pass** (was 134),
`--selftest` OK at 17 checks. Working tree clean.

The `.blend` was committed at the Lead's explicit direction, against the standing
"never commit `.blend`" rule: it is already tracked (5 prior commits, most recently
`ae8ab66` which shipped one with its report), and leaving it uncommitted makes the
committed report describe geometry nobody else has. Plate first, then the
instruments, then the measurements - three commits, so the geometry is reviewable
without the reports that depend on it.

### Still human-owned, not agent-resolvable

**No human has played this build.** `feel.human_playtest` and `feel.verb_script`
are MISSING, which is the honest reading - not FAIL, because nobody has tried. The
record reads MISSING so that "no one has played it" can never be recorded as "a
person played it and it failed", and so that typing something is never the cheapest
route to green.

**V2 is the row that decides whether 180 x 100 reads as an island.** Jump off the
edge and land in the field; that is the whole test. Also open: the six feel
tunables, the ten asset-board stages, and the three G-ENV art findings.


---

## 2026-10-04 (late) - The plate was in Blender and nowhere else

Lead asked whether everything agent-doable was done before the polish pass, and
for an interview to get what was needed from them. The first question was the
useful one. Answering it honestly meant asking what a player would actually stand
on, and the answer was: a 19.3 m island.

### What was found

`SM_IslandTop` measured 180.0000 x 100.0000 x 0.4500 in
`blender/floating_island_homestead_LIB.blend`, applied and committed earlier the
same day. `env.island_sized` said PASS. But
`AssetCreation/Exports/Homestead/SM_IslandTop.fbx` had been written 2026-09-16 and
still measured **19.3000 x 10.7000 x 0.4500** - 32 verts, the same topology and the
same Z datum as the plate, so unmistakably the older mesh - and
`Content/HomeWorld/Meshes/Homestead/SM_IslandTop.uasset` had been imported from it
on 2026-09-28.

Proved by importing the FBX into a clean Blender and measuring it, not inferred
from timestamps.

**The gate was not wrong. It was silent about the hop it never measured.** Every
check read the `.blend`, which is the authoring source of truth. No check read the
FBX, the `.uasset`, or the actor in the level. `env.world_assembled` counted 1270
external actors and measured no dimensions;
`Saved/automation_run_result.json` ran 20 tests and mentioned "island" zero times.

### What was done about it

1. **Re-exported** through `AssetCreation/Blender/export_to_asset_creation.py`,
   then verified by re-importing the written FBX: `[180.0000 100.0000 0.4500]`, 32
   verts, top_z 0. `apply_transforms_selected()` re-saved the `.blend` during the
   export; re-measuring showed nothing moved (loc 0/rot 0/scale 1, 32 verts /
   18 polys) so the `.blend` was reverted. Manifest row 15676 -> 15692 - the only
   stale row of 23.

2. **`env.export_fresh`** (new row) - parses every FBX row in
   `MVP_EXPORT_MANIFEST.md` and compares recorded size to disk. The `.blend -> FBX`
   hop.

3. **`env.ue_island_measured`** (new row) + **`Content/Python/measure_ue_island.py`**
   + seeded **`Docs/qa/UE_ISLAND_MEASUREMENT.json`** - the `FBX -> .uasset -> level`
   hop, which pure Python cannot reach. The script only reads (`get_actor_bounds`),
   spawns nothing and saves no level. Reads MISSING today: nobody has run it, and
   the note says so rather than letting a Blender PASS imply an engine PASS.

### Four retractions and one false positive

- **"The mtime rule works."** Wrong - it reported **23 of 23 stale** after one
  object's geometry changed, because saving the blend touches one file while every
  export in it legitimately predates that save. A whole-file timestamp cannot
  describe per-object change. Removed rather than tuned; the count is still printed
  as a hint, and `test_fbx_predating_the_blend_is_a_hint_not_a_failure` guards it.
- **"Two notes for two branches is fine."** Wrong - a missing record file and a null
  `bbox_cm` are the same fact and shipped with different notes. A test caught it;
  `unmeasured()` now serves both.
- **`Docs/` vs `docs/`** - `git status` printed the new record at
  `?? docs/qa/UE_ISLAND_MEASUREMENT.json`. Staged with capital D and confirmed with
  an `A` line in `git diff --cached --name-status`.
- **"The manifest is a stale whole."** Wrong - 22 of 23 rows were exact. Its accuracy
  is what makes it a usable detector.

### Evidence

Both mutations reproduced real numbers rather than invented ones, which is the only
reason to trust them:

| mutation | result |
|---|---|
| manifest back to 15676 | FAIL, `1 stale of 23`, `SM_IslandTop.fbx manifest 15676 != disk 15692` |
| record holding the real 2026-09-28 uasset size | FAIL, `UE 19.3 x 10.7 m` vs `Blender 180.0 x 100.0 m`, off by 160.70 / 89.30, tol 3.60 |
| shipped state | `env.export_fresh` PASS `0 stale of 23`; `env.ue_island_measured` MISSING `no bbox_cm` |

`EXPECTED_CHECKS` 17 -> 19. Tests 165 -> 178. `--selftest` OK at 19.
Gate: **G-ENV RED, FAIL 2 MISSING 2 PASS 6.** G-ASSET RED. G-FEEL RED. NOT_READY.

### State and what is owed

Commits `e08b756` (re-export) and `d80a6a6` (gate rows, script, skeleton, tests),
pushed to `main`, verified by `git merge-base --is-ancestor`, not by push output.
`polish` / `origin/polish` untouched at `f218fce` / `9686e68`.

**Still owed, and it is not agent-doable:** the `.uasset` re-import and the actor
re-place. Both are binary/content steps outside a commit, and the editor is not
reachable from this session (`unrealMCP` returns null, not an error - itself a
fail-open worth noting). Until somebody runs `measure_ue_island.py`, the plate is
authored but unproven in the game.

The rule that paid: **a measurement chain is only as good as its last link, and
every tool in this repo was reporting on the first.** When a check goes green, ask
what it did *not* measure. Recorded in `docs/KNOWN_ERRORS.md`.

---

## 2026-10-04 (evening) - Independent review of tonight's own gate work, and the research landing

### The headline

I ran an adversarial review of the two gate rows I had added earlier the same evening, as
`Docs/38_AI_AGENT_PRACTICE.md` §9 item 1 recommends. **It found six ways to turn both rows
green without measuring anything.** All six are closed, each with a test that fails if the
hole reopens. 178 -> 200 tests. Commit `84d7264`.

Two of the six are worth remembering:

- `max(off_x, off_y)` returned `off_x` whenever `off_y` was NaN, because `NaN > x` is
  always False. So **a NaN in the Y slot reported PASS**, with the words "off by nan" in the
  row's own note. `json` accepts the bare literal, so a committed record can carry one.
- The check compared Blender's **object-space** box against Unreal's **world-space** AABB.
  Any rotation of the island actor makes those disagree, so the row would have reported FAIL
  on a correctly placed island. Wrong by construction, not by tolerance - widening the
  tolerance would have concealed it.

The other four: the manifest parser silently skipped rows it could not read (three exports
could vanish from the inventory while the row said PASS); the inventory only ran one way, so
an export on disk that nobody recorded was invisible forever; a `../../..` in a manifest cell
stat'd a file outside the export tree; and a 0-byte FBX whose manifest row also said 0 was a
clean PASS because both sides agreed and both were empty.

`measure_ue_island.py` also had a defect worth its own entry: it opened the measurement record
with `"w"` and wrote only its own keys, so **the first person who did everything right deleted
the skeleton** - including the `19.3 x 10.7` diagnosis. It now preserves `_`-prefixed keys and
writes atomically, and any failure writes a `_status: FAILED` record rather than leaving the
gate to report MISSING with no trace that anyone had tried.

### Retraction: I mis-stated a repo rule to the Lead, and the Lead decided on it

I said re-importing `SM_IslandTop` produces a `.uasset` that "the no-commit rule keeps out of
history", and offered to lift that rule. **That was wrong.** `Config/uasset-allowlist.json`
already allowlists `Content/HomeWorld/Meshes`; `SM_IslandTop.uasset` is already tracked; it is
already LFS-backed with a present 78,829-byte object. No rule ever blocked it - a re-import is
simply a modified tracked file.

The Lead chose the "lift the rule" option on my false premise. The outcome they wanted (the fix
cannot be lost) is achieved automatically by existing policy, and the action item is simpler
and faster than I told them. Recorded in `docs/KNOWN_ERRORS.md` as its own class: *asserting a
repo rule from memory instead of reading the machine config.* A "the rules prevent X" claim is
a measurement claim about a config file.

Also worth recording from that check: this git stores LFS objects under `.git/lfs/objects`,
**not** `%LOCALAPPDATA%\lfs\objects`. The documented default briefly looked like a dangling
pointer.

### Research landed as canon

- `Docs/38_AI_AGENT_PRACTICE.md` §11 - round two, studio practice rather than papers. GDC 2026
  (~2,300 professionals): AI use is 81% research, 22% testing/debugging, **5% player-facing**;
  adoption 97% analytics vs 43% art/design; negative sentiment 18% -> 30% -> **52%**. So the
  split in `docs/human-use/OWNERSHIP.md` is the mainstream shape, not a doctrine we invented,
  and the sentiment trend says it is also the defensible one.
- `Docs/20_UASSET_AI_POLICY.md` §4A - **the Valve January 2026 rule, which until now existed
  only in chat.** Disclosure is required for AI content *shipped to and consumed by players*;
  tooling and workflow need none. So the exposure is **placeholders reaching players**, not the
  fact that we use agents - the reference cases (*Clair Obscur: Expedition 33*, *The Alters*)
  are both placeholder incidents.
- `Docs/decisions/AGENT_DECISIONS.md` DEC-0030 and DEC-0031 - the next-action invariant, and
  the decision to close the fail-opens rather than add a severity ladder.
- `Docs/CANON_MAP.md` - four new index rows; its advertised DEC range was stale (said 0028, the
  file had 0029) and is now correct at 0031.

### The restraint worth naming

The research says mature gates ship a rule as a **warning** and promote it to an error only
once clean. Our gate is binary. Adding a WARN tier and marking `master_binding` and
`family_distinct` WARN would have made all three gates readable - and would have quietly undone
the Lead's 2026-10-04 ruling that those two rows stay RED, by another name. **Capability
recorded, not applied.** It needs its own decision, stated as its own decision.

### Also fixed

- Every blocked gate row now carries an executable next action as a structural field, rendered
  as a "What to do" table, enforced by a test. All 8 substantive blocked rows have one.
- `Docs/qa/POLISH_BASELINE.json`: the two traversal notes pointed at a `_deferrals` key that
  was never written. It exists now.
- `Docs/qa/POLISH_READINESS.json` / `.md` regenerated. G-ENV FAIL 2 MISSING 2 PASS 6; G-ASSET
  RED; G-FEEL RED. Verdict unchanged: `NOT_READY`.

### State

`main` is clean and pushed. `polish` / `origin/polish` untouched. The `.uasset` has **not** been
re-imported - that still needs the editor, and is still the thing blocking the engine gap.

### Open questions for the Lead

1. **Which level is the shipping one?** `docs/KNOWN_ERRORS.md` answers this for the *homestead
   geometry* - `L_VS_MVP_Markers`, not `MainMenu` - and `measure_ue_island.py` defaults to it.
   But `env.ue_island_measured` deliberately does **not** enforce it: it accepts any real
   `.umap` and prints which one it measured. A measurement from the wrong level would still read
   PASS and say so in its measured column. Tightening that needs the ruling, not a guess.
2. **Is "polish" the right name for this stage?** Industry usage means the alpha -> beta
   transition; we have no human playtest, so we are at a vertical slice. Renaming touches every
   gate row id, both `Docs/qa/POLISH_*` files and four canon docs. Recorded in
   `Docs/38_AI_AGENT_PRACTICE.md` §11.4, not decided.
3. **Should the gate get a severity ladder?** See the restraint note above.

---

## 2026-10-04 — auditing the index, and the audit tool was the defect

Commit `a701b15`. Applies last commit's own advice — review the work minutes after writing it —
to the docs written the session before.

**Found, all three real:**
- `Docs/CANON_MAP.md` named `Docs/decisions/AGENT_DECISIONS.md` **twice in the same lookup
  table** with different ranges (0028 and 0031, the second row added by me). A reader cannot
  resolve a contradiction, so the fix was to delete my row, not to correct both. The surviving
  row now says **0035**, the true maximum, and notes the file's *order* is 0001-0026, 0033-0035,
  0027-0031.
- **DEC-0001 cited `docs/qa/TASK_LIFT.md`, which has never existed in git history** — not
  deleted, never added. The pilot write-up is `Docs/qa/TASK_LIFT_PREREGISTRATION.md`. Pointer
  corrected, with the dead path left in the note so the next grep finds the correction.
- The first pass at this audit **was itself wrong**. Grepping `^### DEC-` returned 0001-0026 then
  a jump to 0033-0035, and I concluded the numbering had gaps at 0027-0029 and 0032. All of
  those ids are present, as `##` level-2 headings. The audit tool could only see part of the file
  and reported the invisible part as absent — a **false RED on a correct file**, which is the
  exact defect the previous commit spent its effort removing from `polish_readiness.py`. The
  `3de567d` commit message carries the same wrong belief.

**Also checked and cleared:** nine other unresolved backticked paths were false positives from an
over-loose regex — engine include paths, an external GitHub slug, a SkillEvaluator package path,
and KNOWN_ERRORS cycle notes from March 2026 that predate this work.

**Gate unchanged:** G-ENV / G-ASSET / G-FEEL all RED, `NOT_READY`. 114 tests + 69 subtests pass.

**Handoff written:** `Docs/handoffs/SESSION_HANDOFF_POLISH_GATES.md` — fresh-chat entry point for
this slice, carrying the editor steps, the two deliberate REDs, the human-only rows, and the
repo traps.


### And the `git add` skip is finally diagnosed

Commit `0ff1a3b`. The trap that has cost a file twice is no longer folklore.
`git add <new file under Docs/> <existing path spelled docs/...>` stages **nothing**,
prints **nothing**, exits **0**. Cause: `core.ignorecase = true` plus one physical Windows
directory (`Docs/` and `docs/`, DEC-0029) serving **two index trees** - 324 tracked paths under
`Docs/`, 155 under `docs/`. A lowercase pathspec matches into the new file's own directory, so
the new file reads as already accounted for. Not a git bug; a configuration where two spellings
name one file and one name hides the other. Rule: add one path at a time, capital `Docs`, confirm
with `git diff --cached --name-status`.

`1afade3` hit this bug - it is why the handoff could not be committed the first time.

**Fresh-chat entry point for this slice: `Docs/handoffs/SESSION_HANDOFF_POLISH_GATES.md`.**
It carries the six editor steps that close the engine gap, the two G-ENV rows that stay RED on
purpose, the four open Lead decisions, and the repo traps.
