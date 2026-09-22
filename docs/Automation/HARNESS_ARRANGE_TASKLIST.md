# Harness Arrange gate — task list (Lead plan)

**P0 (this PR):** Blocking Arrange gate before PA-E capture Act/Assert.

**Habit:** Lead-correction → harness — proven misses (e.g. assert before Arrange, speckle false PASS) land as **code gates + one policy row** in [CAPTURE_REDUNDANCY.md](CAPTURE_REDUNDANCY.md) / [automation-standards.mdc](../../.cursor/rules/automation-standards.mdc); no chat-only checklist.

| ID | Task | Status |
|----|------|--------|
| P0-1 | Shared gate API `arrange_pa_e_shotlist` / `assert_environment_ready` in `pa_e_shotlist_common.py` | Done (PR) |
| P0-2 | Write `Saved/pa_e_arrange_gate.json`; block MRQ/AL when `ready: false` | Done (PR) |
| P0-3 | TMP night fixture re-seed after `load_level` (`vnp_night_tune_and_evidence.reseed_pa_e_tmp_night_fixtures`) | Done (PR) |
| P0-4 | Diagnostic single-write JSON (`level_loaded`, `homestead_night_environment`, `arrange_gate`) | Done (PR) |
| P0-5 | Docs: CAPTURE_REDUNDANCY, KNOWN_ERRORS, AUTOMATION_GAPS, automation-standards | Done (PR) |
| P0-6 | Assert harden: center-crop + bright-pixel fraction + shot-pair diversity (block global-mean speckle PASS) | Done (follow-up PR) |
| P0-7 | Arrange: per-shot `aim_bounds` centroids, ray vs dress AABB, MRQ per-shot night reapply note | Done (follow-up PR) |
| P0-8 | Arrange: bounds **relocate** CAM (not reaim-only); exclude Cliff from aim needles; ray required for `aim_ok` | Done (PR) |

**P1 (follow-up):** Three-state reports everywhere (`blocked` / `in_progress` / `pass`) with consistent `closed_fail` semantics across PIE harnesses and NF2-B evidence scripts. **Done on main (#180).**

**P2 (industry harness — PA-E / MRQ):** Fixture lifecycle, latent waits, plugin probe, artifact stamps (this track — **not** golden-image SCOUT).

| ID | Task | Status |
|----|------|--------|
| P2-1 | TMP + `PA_E_MRQ_*` fixture lifecycle helpers + report stamps (`reseed_pa_e_tmp_fixtures_for_capture`, `inventory_pa_e_session_fixtures`, optional `teardown_pa_e_session_fixtures`) | PR (cloud) |
| P2-2 | Central `MRQ_LATENT_WAIT_CONTRACT` (56/16 warm-up, PIE stack tick cadence, Slate pre-tick budgets); wait miss → `classify_mrq_wait_outcome` soft/closed fail | PR (cloud) |
| P2-3 | `probe_mrq_tool_readiness()` wired into `conductor_mrq_capture_preflight` (clear blocked reason, not import crash) | PR (cloud) |
| P2-4 | `artifact_stamps` in `pa_e_capture_report.json` (paths + mtimes); `PA_E_FRESH_PROVE=1` optional full purge only at prove start | PR (cloud) |

**P2-gated (Lead `APPROVE TOOL SCOUT` only):** Epic Screenshot Comparison / golden-image pipeline after trusted lit capture path — docs scout only until gate; **not** part of industry P2 PR.

**P3 (follow-up):** Full harness audit — every Editor Python “prove” script calls Arrange or documents why not (non-shotlist tests). **Done (PR).**

| Script | Gate | Notes |
|--------|------|--------|
| [capture_shotlist.py](../../Content/Python/capture_shotlist.py) | MRQ entry → `conductor_mrq_capture_preflight` + `arrange_pa_e_shotlist` + `reset_mrq_session_guards` | Canonical PA-E prove |
| [capture_shotlist_mrq.py](../../Content/Python/capture_shotlist_mrq.py) | Same (implements) | P2 fixtures / latent contract / artifact stamps |
| [capture_shotlist_viewport.py](../../Content/Python/capture_shotlist_viewport.py) | `reload_pa_e_capture_python_modules` + `arrange_pa_e_shotlist` (`require_mrq=False`) | AL diagnostic; **exempt** MRQ conductor preflight |
| [pa_e_homestead_capture_diagnostic.py](../../Content/Python/pa_e_homestead_capture_diagnostic.py) | `arrange_pa_e_shotlist` | Arrange-only steps 1–2; no capture |
| [nf2_b_night_lookdev_evidence.py](../../Content/Python/nf2_b_night_lookdev_evidence.py) | `conductor_night_evidence_preflight` + `arrange_pa_e_shotlist` + P1 `capture_outcome` | NF2-B parity (#180 note) |
| [vnp_night_tune_and_evidence.py](../../Content/Python/vnp_night_tune_and_evidence.py) | Same when Markers world | Shots 1/2/5; harness luminance only |
| [vnp_load_vs_mvp_and_evidence.py](../../Content/Python/vnp_load_vs_mvp_and_evidence.py) | load + preflight + arrange → VNP `main()` | Orchestrator |
| [capture_viewport.py](../../Content/Python/capture_viewport.py) | **Exempt** | Generic utility still; docstring |
| [capture_editor_screenshot.py](../../Content/Python/capture_editor_screenshot.py) | **Exempt** | Host PyAutoGUI; not Editor prove |
| [nf2_a_form_swap_evidence.py](../../Content/Python/nf2_a_form_swap_evidence.py) | **Exempt** | PIE log instructions JSON only |
| [preflight_ue_editor.py](../../Content/Python/preflight_ue_editor.py) | **Exempt** | HR3-B npm preflight |
| [_pl_d_capture2.py](../../Content/Python/_pl_d_capture2.py), [_pl_d_capture_shot1.py](../../Content/Python/_pl_d_capture_shot1.py) | **Exempt** | PL-D spikes |
| [wtr_pcg_nondestructive_spike.py](../../Content/Python/wtr_pcg_nondestructive_spike.py) | **Exempt** | WTR PCG spike optional PNG |

Shared API: `conductor_mrq_capture_preflight` (MRQ) · `conductor_night_evidence_preflight` (VNP/NF2) · `arrange_pa_e_shotlist` · `summarize_evidence_png_harness` in [pa_e_shotlist_common.py](../../Content/Python/pa_e_shotlist_common.py).

**References:** [CAPTURE_REDUNDANCY.md](CAPTURE_REDUNDANCY.md) § P0 Arrange gate · [pa_e_shotlist_common.py](../../Content/Python/pa_e_shotlist_common.py) · [Docs/00_SHOTLIST.md](../../Docs/00_SHOTLIST.md)
