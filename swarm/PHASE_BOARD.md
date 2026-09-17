# PHASE BOARD — Conductor only writes status rows

**Current phase:** **HS-E** — Character / bootstrap canon (**IN PROGRESS**)

**Flight fallback armed:** YES — scripted glide along CRUMB_*/GLIDE_SPLINE + portal both ways (Lead: FALLBACK FLIGHT 2026-09-16)  
**Active owners:** **Lead** (`APPROVE HS-E`) / **Conductor** (docs+preflight) / **DESKTOP** (KEEP-LOCAL setup proof)
**Blocked by:** Lead policy **KEEP-LOCAL** recorded (`HS-E POLICY KEEP-LOCAL`, 2026-09-17 ET). Next gate **`APPROVE HS-E`**. Branch protection **DEFERRED**.


| Phase | Name | Owners | Status | Gate file | Handoffs |
|---|---|---|---|---|---|
| P0 | Canon freeze | CND DES AD | CLOSED | Docs/00_CANON.md | P0_DES_canon, P0_AD_shotlist, P0_CND_skeleton |
| P1 | GDD + graybox | DES WLD | CLOSED | Docs/01_GDD_MVP.md | P1_DES_gdd, P1_WLD_graybox |
| P2 | Materials + bible | AD TA | CLOSED | Docs/02_MATERIAL_SHEET.md | P2_AD_bible, P2_TA_masters |
| P3 | Homestead kit | ENV-H PROP LIT | CLOSED | Maps/Preview_Homestead_Night | P3_ENVH_kit, P3_PROP_kit, P3_LIT_night, P3_BLENDER_kit |
| P4 | Planet + transit | ENV-P WLD LIT | CLOSED | Maps/Preview_Lookout_To_Planet | P4_ENVP_forest, P4_WLD_transit, P4_LIT_day |
| P5 | Verbs + life | CHA PROP GP SYS | CLOSED | Docs/01_GDD_MVP.md verbs executed | P5_CHA_life, P5_PROP_verbs, P5_SYS_data, P5_GP_verbs, P5_CND_fallback_flight |
| P6 | Integrate | INT CND TA | CLOSED | Maps/VS_MVP | P6_INT_slice, P6_FIX_shot1, P6_QA_judge, P6_QA_rejudge |
| P7 | Sign-off | QA AD DES Lead | CLOSED | Docs/07_VERTICAL_SLICE_SIGN OFF.md | P7_Lead_signoff |

Status values: `LOCKED` `OPEN` `IN PROGRESS` `GATE FAILED` `CLOSED` `GATE READY`

---

## Host owner lane (HR3-D convention)

Every **active** post-audit / HR / VP row must name **who runs evidence**:

| Tag | Meaning |
|-----|---------|
| **CLOUD** | Cursor cloud agent (Linux VM) — docs, C++ source, CI; no MCP/PIE |
| **DESKTOP** | **DESKTOP-21CT3H0** — Conductor **parent** only ([HR3_A_WINDOWS_EXEC.md](../Docs/handoffs/HR3_A_WINDOWS_EXEC.md)); Task executors **FAIL** |
| **Lead** | Human — GitHub Settings, **`APPROVE *`** gates |

**DESKTOP Shell law (HS-B):** Conductor **parent** session only — never assign DESKTOP Shell / MCP / PIE to Cursor **Task** executors or cloud Linux VMs. Happy path: [WINDOWS_BRIDGE.md](../docs/Setup/WINDOWS_BRIDGE.md) · [SWARM_OPS.md](SWARM_OPS.md) §16. Re-verify rule: [HR3_D_EVIDENCE_LANE.md](../Docs/handoffs/HR3_D_EVIDENCE_LANE.md).

### Re-verify before polish (HS-D)

Prior **hard-fail** verb greps must be **re-proved** (or Lead **WAIVED** per prefix) before any downstream **polish / presentation** unlock:

1. Blocker-fix phase files evidence → Lead **`APPROVE`**.
2. DESKTOP owner (Conductor **parent**) re-runs the prior phase prefix checklist on current `main`; append **§ Re-verify** (keep original FAIL/WAIVE). Prefer `npm run evidence:grep -- --log Saved/Logs/HomeWorld.log`.
3. Conductor **refuses** polish unlock until all required prefixes **PASS** or Lead **WAIVED**.

Canonical history: **VP-A → VP-B → VP-A re-verify → VP-C**. Spec: [17d_HS_EVIDENCE.md](../Docs/17d_HS_EVIDENCE.md) · handoff [HS_D_EVIDENCE.md](../Docs/handoffs/HS_D_EVIDENCE.md) · ops [SWARM_OPS.md](SWARM_OPS.md) §4c. Silent skip forbidden.

---

## POST-AUDIT (Docs/05–10 + HR track)

MVP vertical slice and post-audit product wrap are **CLOSED**. **Harness Refine (HR-A…D + HR-B2) is CLOSED.** **Product next-phase (NP-A…E) is CLOSED / COMPLETE.** **HR2 track CLOSED / COMPLETE.** **HR3 track CLOSED / COMPLETE** — Lead **`APPROVE HR3-D`**, 2026-09-17 ET (HR3-C **DEFERRED**). **VP track CLOSED / COMPLETE** (VP-A re-verify **WAIVED**). **Docs/16 Playable Loop CLOSED / COMPLETE** — Lead **`APPROVE PL-D`**, 2026-09-17 ET. **Docs/17 HS Audit ACTIVE** — HS-A/B/D **CLOSED**; HS-C **DEFERRED**; **HS-E IN PROGRESS**.

| Track | Doc / phase | Host | Status | Gate / handoff |
|---|---|---|---|---|
| Docs/05 | UE import first pass | DESKTOP | **CLOSED** | [05_UE_IMPORT_FIRST_PASS.md](../Docs/05_UE_IMPORT_FIRST_PASS.md) |
| Docs/06 | VS_MVP dress | DESKTOP | **CLOSED** | [06_VS_MVP_DRESS.md](../Docs/06_VS_MVP_DRESS.md) |
| Docs/07 | Vertical slice sign-off | Lead | **CLOSED** | [07_VERTICAL_SLICE_SIGN OFF.md](../Docs/07_VERTICAL_SLICE_SIGN%20OFF.md) |
| Docs/08–10 | Audit WAVEs + post-audit wrap | CLOUD | **CLOSED** | [08_AUDIT_SIGN_OFF.md](../Docs/08_AUDIT_SIGN_OFF.md), [10_POST_AUDIT_WRAP.md](../Docs/10_POST_AUDIT_WRAP.md) |
| Docs/11 | Product next-phase strategy | CLOUD | **APPROVED** | [11_NEXT_PHASE_STRATEGY.md](../Docs/11_NEXT_PHASE_STRATEGY.md) |
| Docs/11 | Swarm & harness refine | CLOUD | **CLOSED** | [11_SWARM_HARNESS_REFINE.md](../Docs/11_SWARM_HARNESS_REFINE.md) |
| **HR-A…B2, HR-D** | Harness refine | CLOUD | **APPROVED** | See Docs/11a–11e |
| **NP-A…E** | Product next-phase | CLOUD+DESKTOP | **CLOSED** | NP-A…E **APPROVED** — Lead **`APPROVE NP-E`**, 2026-09-17 ET |
| **Docs/13** | Harness Refine 2 strategy | CLOUD | **APPROVED** | [13_HR2_HARNESS_REFINE.md](../Docs/13_HR2_HARNESS_REFINE.md) |
| **HR2-A** | Doctor signal (UE host) | CLOUD | **APPROVED** | [13a_HR2_A_HANDOFF.md](../Docs/13a_HR2_A_HANDOFF.md) |
| **HR2-B** | Cold-clone submodule | CLOUD | **APPROVED** | [13b_HR2_B_COLD_CLONE.md](../Docs/13b_HR2_B_COLD_CLONE.md) |
| **HR2-C** | C++ CI gate (build-win64) | CLOUD | **APPROVED** | [13c_HR2_C_CI_GATE.md](../Docs/13c_HR2_C_CI_GATE.md), [handoffs/HR2_C_CI_GATE.md](../Docs/handoffs/HR2_C_CI_GATE.md) |
| **HR2 track** | Harness Refine 2 | — | **CLOSED / COMPLETE** | [13_HR2_HARNESS_REFINE.md](../Docs/13_HR2_HARNESS_REFINE.md) |
| **Docs/14** | Verify & Polish strategy | CLOUD | **APPROVED** | [14_VP_VERIFY_POLISH.md](../Docs/14_VP_VERIFY_POLISH.md) |
| **VP-A** | PIE evidence | DESKTOP | **APPROVED** — **re-verify WAIVED** | [handoffs/VP_A_PIE.md](../Docs/handoffs/VP_A_PIE.md) § Re-verify — Lead **`WAIVE VP-A re-verify`**, 2026-09-17 ET |
| **VP-B** | Smoke & character risk | DESKTOP | **APPROVED / CLOSED** | [handoffs/VP_B_SMOKE_CHARACTER.md](../Docs/handoffs/VP_B_SMOKE_CHARACTER.md) — Lead **`APPROVE VP-B`**, 2026-09-17 ET; PA-03 **deferred accept** (mesh-only interim) |
| **Docs/15** | Harness Refine 3 (A+) | CLOUD | **APPROVED** | [15_HR3_A_PLUS.md](../Docs/15_HR3_A_PLUS.md) |
| **HR3-A** | Windows exec reliability | DESKTOP | **APPROVED** | [handoffs/HR3_A_WINDOWS_EXEC.md](../Docs/handoffs/HR3_A_WINDOWS_EXEC.md) |
| **HR3-B** | UE preflight fails loud | CLOUD+DESKTOP | **APPROVED** | [handoffs/HR3_B_UE_PREFLIGHT.md](../Docs/handoffs/HR3_B_UE_PREFLIGHT.md) — PR #60 |
| **HR3-C** | Branch protection | Lead | **DEFERRED / COMPLETE for track** | Lead skip 2026-09-17 ET — [handoffs/HR3_C_BRANCH_PROTECTION.md](../Docs/handoffs/HR3_C_BRANCH_PROTECTION.md) checklist PR #62; GitHub apply deferred |
| **HR3-D** | DESKTOP evidence + re-verify | CLOUD | **APPROVED** | [handoffs/HR3_D_EVIDENCE_LANE.md](../Docs/handoffs/HR3_D_EVIDENCE_LANE.md) — Lead **`APPROVE HR3-D`**, 2026-09-17 ET; PR #65 |
| **HR3 track** | Harness Refine 3 (A+) | — | **CLOSED / COMPLETE** | [15_HR3_A_PLUS.md](../Docs/15_HR3_A_PLUS.md) — HR3-C **DEFERRED**; harness **~A**, swarm **~A+** |
| **VP-C** | Playability polish | CLOUD+DESKTOP | **APPROVED / CLOSED** | [handoffs/VP_C_POLISH.md](../Docs/handoffs/VP_C_POLISH.md) — Lead **`APPROVE VP-C`**, 2026-09-17 ET |
| **VP-D** | Bootstrap dry-run | CLOUD+DESKTOP | **APPROVED / CLOSED** | [handoffs/VP_D_BOOTSTRAP_CI.md](../Docs/handoffs/VP_D_BOOTSTRAP_CI.md) — Lead **`APPROVE VP-D`**, 2026-09-17 ET; branch protection **DEFERRED** |
| **Docs/16 PL** | Playable Loop | CLOUD+DESKTOP+Lead | **CLOSED / COMPLETE** | [16_PLAYABLE_LOOP.md](../Docs/16_PLAYABLE_LOOP.md) — Lead **`APPROVE PL-D`**, 2026-09-17 ET; PL-B **WAIVED** |
| **Docs/17 HS** | Harness & Swarm Audit | CLOUD | **APPROVED / ACTIVE** | [17_HS_AUDIT_STRATEGY.md](../Docs/17_HS_AUDIT_STRATEGY.md) — Lead **`APPROVE HS STRATEGY`**, 2026-09-17 ET |
| **HS-A** | Inventory & debt ledger | CLOUD | **APPROVED / CLOSED** | [17a_HS_INVENTORY.md](../Docs/17a_HS_INVENTORY.md) — Lead **`APPROVE HS-A`**, 2026-09-17 ET (PR #88) |
| **HS-B** | Swarm ops tighten | CLOUD | **APPROVED / CLOSED** | [17b_HS_SWARM_OPS.md](../Docs/17b_HS_SWARM_OPS.md) — Lead **`APPROVE HS-B`**, 2026-09-17 ET |
| **HS-C** | CI as law | CLOUD+Lead | **DEFERRED / CLOSED** | Lead **`ACCEPT HS-C DEFER`**, 2026-09-17 ET — [17c](../Docs/17c_HS_CI_LAW.md) |
| **HS-D** | Evidence automation | CLOUD+DESKTOP | **APPROVED / CLOSED** | [17d_HS_EVIDENCE.md](../Docs/17d_HS_EVIDENCE.md) · [HS_D_EVIDENCE.md](../Docs/handoffs/HS_D_EVIDENCE.md) — Lead **`APPROVE HS-D`**, 2026-09-17 ET (PR #94) |
| **HS-E** | Character / bootstrap canon | CLOUD+Lead+DESKTOP | **IN PROGRESS** | [17e_HS_CONTENT_BOOTSTRAP.md](../Docs/17e_HS_CONTENT_BOOTSTRAP.md) — policy **KEEP-LOCAL** (Lead 2026-09-17 ET); PENDING **`APPROVE HS-E`**; handoff [HS_E_CONTENT_BOOTSTRAP.md](../Docs/handoffs/HS_E_CONTENT_BOOTSTRAP.md) |

**Current track:** **Docs/17 HS** — HS-A/B/D **CLOSED**; HS-C **DEFERRED**; **HS-E IN PROGRESS** (policy **KEEP-LOCAL**; PENDING **`APPROVE HS-E`**).

---

## Open tasks

| ID | Phase | Host | Owner | Write path | Due artifact |
|---|---|---|---|---|---|
| HS-E-bootstrap | HS-E | CLOUD+Lead+DESKTOP | CND+Lead | Docs/ | [17e_HS_CONTENT_BOOTSTRAP.md](../Docs/17e_HS_CONTENT_BOOTSTRAP.md) · [HS_E_CONTENT_BOOTSTRAP.md](../Docs/handoffs/HS_E_CONTENT_BOOTSTRAP.md) — **IN PROGRESS** policy **KEEP-LOCAL**; PENDING **`APPROVE HS-E`** |
| HS-D-evidence | HS-D | CLOUD+DESKTOP | CND | Docs/ + scripts/ | [17d_HS_EVIDENCE.md](../Docs/17d_HS_EVIDENCE.md) · [HS_D_EVIDENCE.md](../Docs/handoffs/HS_D_EVIDENCE.md) — **APPROVED / CLOSED** Lead **`APPROVE HS-D`**, 2026-09-17 ET |
| HS-B-swarm-ops | HS-B | CLOUD | CND | Docs/ + swarm/ | [17b_HS_SWARM_OPS.md](../Docs/17b_HS_SWARM_OPS.md) — **APPROVED / CLOSED** Lead **`APPROVE HS-B`**, 2026-09-17 ET |
| HS-A-inventory | HS-A | CLOUD | CND | Docs/ | [17a_HS_INVENTORY.md](../Docs/17a_HS_INVENTORY.md) — **APPROVED / CLOSED** Lead **`APPROVE HS-A`**, 2026-09-17 ET |
| PL-A-character | PL-A | DESKTOP+CLOUD | CND | Docs/handoffs/ | [PL_A_CHARACTER.md](../Docs/handoffs/PL_A_CHARACTER.md) — **APPROVED / CLOSED** — Lead **`APPROVE PL-A`**, 2026-09-17 ET |
| PL-B-pie | PL-B | Lead | Lead | Docs/handoffs/ | [PL_B_PIE.md](../Docs/handoffs/PL_B_PIE.md) — **WAIVED / CLOSED** — Lead **`WAIVE PL-B`**, 2026-09-17 ET |
| PL-D-presentation | PL-D | DESKTOP+Lead | CND+Lead | Docs/handoffs/ | [PL_D_PRESENTATION.md](../Docs/handoffs/PL_D_PRESENTATION.md) — **APPROVED / CLOSED** — Lead **`APPROVE PL-D`**, 2026-09-17 ET; PL track complete |
| PL-C-loop | PL-C | CLOUD+DESKTOP | CND | Docs/handoffs/ | [PL_C_LOOP_UX.md](../Docs/handoffs/PL_C_LOOP_UX.md) — **APPROVED / CLOSED** — Lead **`APPROVE PL-C`**, 2026-09-17 ET |
| VP-A-reverify | VP-A | Lead | Lead | Docs/handoffs/ | **WAIVED** — Lead **`WAIVE VP-A re-verify`**, 2026-09-17 ET; debt closes under **PL-B** |
| HR3-C-branch-protection | HR3-C | Lead | Lead | docs/Setup/ | **DEFERRED** — [HR3_C_BRANCH_PROTECTION.md](../Docs/handoffs/HR3_C_BRANCH_PROTECTION.md) |

## Deferred accept (VP-B — not open defects)

| ID | Phase | Decision | Reference |
|---|---|---|---|
| PA-03 | VP-B | **Deferred accept** — mesh-only interim; `ABP_HomeWorldCharacter` not assigned; `EDITOR_ABP_SKELETON` warning only; does **not** block VP-C planning/impl | [VP_B_SMOKE_CHARACTER.md](../Docs/handoffs/VP_B_SMOKE_CHARACTER.md) § ABP deferred accept |

## Open defects

| ID | Phase | Owner | Blocker | File |
|---|---|---|---|---|
| — | — | — | — | — |