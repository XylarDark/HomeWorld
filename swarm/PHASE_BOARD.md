# PHASE BOARD — Conductor only writes status rows

**Current phase:** **HR3-C** (branch protection real) — **UNLOCKED / IN PROGRESS**  
**Flight fallback armed:** YES — scripted glide along CRUMB_*/GLIDE_SPLINE + portal both ways (Lead: FALLBACK FLIGHT 2026-09-16)  
**Active owners:** **CND** (Conductor) + cloud agent (HR3-C planning)  
**Blocked by:** Lead **`APPROVE HR3-C`** before implementation PR — [15_HR3_A_PLUS.md](../Docs/15_HR3_A_PLUS.md) § HR3-C. HR3-A/B **APPROVED**. VP-A **APPROVED** (hard-fail ABP). **VP-B PARKED** pending HR3.

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

## POST-AUDIT (Docs/05–10 + HR track)

MVP vertical slice and post-audit product wrap are **CLOSED**. **Harness Refine (HR-A…D + HR-B2) is CLOSED.** **Product next-phase (NP-A…E) is CLOSED / COMPLETE.** **HR2 track CLOSED / COMPLETE** — HR2-A/B/C all **APPROVED**; Lead **`APPROVE HR2-C`**, 2026-09-17 ET. **VP strategy APPROVED** — Lead **`APPROVE VP STRATEGY`**, 2026-09-17 ET. **VP-A APPROVED** — Lead **`APPROVE VP-A`**, 2026-09-17 ET (hard-fail accepted). **HR3 strategy APPROVED** — Lead **`APPROVE HR3 STRATEGY`**, 2026-09-17 ET. **HR3-A APPROVED** — Lead **`APPROVE HR3-A`**, 2026-09-17 ET. **HR3-B APPROVED** — Lead **`APPROVE HR3-B`**, 2026-09-17 ET. Active: **HR3-C UNLOCKED / IN PROGRESS** (await **`APPROVE HR3-C`**). **VP-B PARKED** pending HR3.

| Track | Doc / phase | Status | Gate / handoff |
|---|---|---|---|
| Docs/05 | UE import first pass | **CLOSED** | [05_UE_IMPORT_FIRST_PASS.md](../Docs/05_UE_IMPORT_FIRST_PASS.md) |
| Docs/06 | VS_MVP dress | **CLOSED** | [06_VS_MVP_DRESS.md](../Docs/06_VS_MVP_DRESS.md) |
| Docs/07 | Vertical slice sign-off | **CLOSED** | [07_VERTICAL_SLICE_SIGN OFF.md](../Docs/07_VERTICAL_SLICE_SIGN%20OFF.md) |
| Docs/08–10 | Audit WAVEs + post-audit wrap | **CLOSED** | [08_AUDIT_SIGN_OFF.md](../Docs/08_AUDIT_SIGN_OFF.md), [10_POST_AUDIT_WRAP.md](../Docs/10_POST_AUDIT_WRAP.md) |
| Docs/11 | Product next-phase strategy | **APPROVED** | [11_NEXT_PHASE_STRATEGY.md](../Docs/11_NEXT_PHASE_STRATEGY.md) |
| Docs/11 | Swarm & harness refine | **CLOSED** | [11_SWARM_HARNESS_REFINE.md](../Docs/11_SWARM_HARNESS_REFINE.md) |
| **HR-A…B2, HR-D** | Harness refine | **APPROVED** | See Docs/11a–11e |
| **NP-A…E** | Product next-phase | **CLOSED** | NP-A…E **APPROVED** — Lead **`APPROVE NP-E`**, 2026-09-17 ET |
| **Docs/13** | Harness Refine 2 strategy | **APPROVED** | [13_HR2_HARNESS_REFINE.md](../Docs/13_HR2_HARNESS_REFINE.md) — Lead **`APPROVE HR2 STRATEGY`**, 2026-09-17 ET |
| **HR2-A** | Doctor signal (UE host) | **APPROVED** | [13a_HR2_A_HANDOFF.md](../Docs/13a_HR2_A_HANDOFF.md) — Lead **`APPROVE HR2-A`**, 2026-09-17 ET |
| **HR2-B** | Cold-clone submodule | **APPROVED** | [13b_HR2_B_COLD_CLONE.md](../Docs/13b_HR2_B_COLD_CLONE.md) — Lead **`APPROVE HR2-B`**, 2026-09-17 ET |
| **HR2-C** | C++ CI gate (build-win64) | **APPROVED** | [13c_HR2_C_CI_GATE.md](../Docs/13c_HR2_C_CI_GATE.md), [handoffs/HR2_C_CI_GATE.md](../Docs/handoffs/HR2_C_CI_GATE.md) — Lead **`APPROVE HR2-C`**, 2026-09-17 ET |
| **HR2 track** | Harness Refine 2 | **CLOSED / COMPLETE** | [13_HR2_HARNESS_REFINE.md](../Docs/13_HR2_HARNESS_REFINE.md) — no HR2-D |
| **Docs/14** | Verify & Polish strategy | **APPROVED** | [14_VP_VERIFY_POLISH.md](../Docs/14_VP_VERIFY_POLISH.md) — Lead **`APPROVE VP STRATEGY`**, 2026-09-17 ET |
| **VP-A** | PIE evidence | **APPROVED** | [handoffs/VP_A_PIE.md](../Docs/handoffs/VP_A_PIE.md) — Lead **`APPROVE VP-A`**, 2026-09-17 ET; hard-fail accepted |
| **VP-B** | Smoke & character risk | **PARKED** | Pending HR3 — resume after HR3 track (+ HR3-B preflight recommended) |
| **Docs/15** | Harness Refine 3 (A+) | **APPROVED** | [15_HR3_A_PLUS.md](../Docs/15_HR3_A_PLUS.md) — Lead **`APPROVE HR3 STRATEGY`**, 2026-09-17 ET |
| **HR3-A** | Windows exec reliability | **APPROVED** | [handoffs/HR3_A_WINDOWS_EXEC.md](../Docs/handoffs/HR3_A_WINDOWS_EXEC.md) — Lead **`APPROVE HR3-A`**, 2026-09-17 ET; parent→DESKTOP proven; executors FAIL |
| **HR3-B** | UE preflight fails loud | **APPROVED** | [handoffs/HR3_B_UE_PREFLIGHT.md](../Docs/handoffs/HR3_B_UE_PREFLIGHT.md) — Lead **`APPROVE HR3-B`**, 2026-09-17 ET; evidence PR #60 (`9d7ffaf`) |
| **HR3-C** | Branch protection real | **UNLOCKED / IN PROGRESS** | [15_HR3_A_PLUS.md](../Docs/15_HR3_A_PLUS.md) § HR3-C; handoffs/HR3_C_BRANCH_PROTECTION.md (pending) |
| **HR3-D** | DESKTOP evidence + re-verify | **LOCKED** | handoffs/HR3_D_EVIDENCE_LANE.md (pending) |
| **VP-C** | Playability polish | **LOCKED** | handoffs/VP_C_POLISH.md (pending) |
| **VP-D** | Bootstrap & branch protection | **LOCKED** | handoffs/VP_D_BOOTSTRAP_CI.md (pending) |

**Current track:** **HR3-B APPROVED** — **HR3-C UNLOCKED / IN PROGRESS** (await Lead **`APPROVE HR3-C`**). VP-A **APPROVED**; **VP-B PARKED**; VP-C/D **LOCKED**. Product NP **CLOSED**. HR2 **CLOSED / COMPLETE**.

---

## Open tasks

| ID | Phase | Owner | Write path | Due artifact |
|---|---|---|---|---|
| HR3-C-gate | HR3-C | Lead | Docs/handoffs/ | Lead **`APPROVE HR3-C`** → unlock HR3-C implementation PR |
| VP-B-resume | VP-B | DESKTOP | Docs/handoffs/ | **PARKED** — resume after HR3 (ABP skeleton + NightMix smoke) |

## Open defects

| ID | Phase | Owner | Blocker | File |
|---|---|---|---|---|
| — | — | — | — | — |
