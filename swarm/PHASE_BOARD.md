# PHASE BOARD — Conductor only writes status rows

**Current phase:** **VP-B** (smoke & character risk) — **UNLOCKED / IN PROGRESS** (resume)  
**Flight fallback armed:** YES — scripted glide along CRUMB_*/GLIDE_SPLINE + portal both ways (Lead: FALLBACK FLIGHT 2026-09-16)  
**Active owners:** **CND** (Conductor parent on **DESKTOP**)  
**Blocked by:** None for VP-B start. **HR3 track CLOSED / COMPLETE** — Lead **`APPROVE HR3-D`**, 2026-09-17 ET (HR3-C **DEFERRED**). VP-A **APPROVED** (hard-fail ABP; **re-verify after VP-B** before VP-C). VP-C/D **LOCKED**.

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
| **DESKTOP** | **DESKTOP-21CT3H0** — Conductor **parent** only ([HR3_A_WINDOWS_EXEC.md](../Docs/handoffs/HR3_A_WINDOWS_EXEC.md)) |
| **Lead** | Human — GitHub Settings, **`APPROVE *`** gates |

Task executors are **not** DESKTOP owners. Re-verify rule: [HR3_D_EVIDENCE_LANE.md](../Docs/handoffs/HR3_D_EVIDENCE_LANE.md) · [SWARM_OPS.md](SWARM_OPS.md) §4.

---

## POST-AUDIT (Docs/05–10 + HR track)

MVP vertical slice and post-audit product wrap are **CLOSED**. **Harness Refine (HR-A…D + HR-B2) is CLOSED.** **Product next-phase (NP-A…E) is CLOSED / COMPLETE.** **HR2 track CLOSED / COMPLETE.** **HR3 track CLOSED / COMPLETE** — Lead **`APPROVE HR3-D`**, 2026-09-17 ET (HR3-C **DEFERRED**). **VP strategy APPROVED.** Active: **VP-B UNLOCKED / IN PROGRESS** (resume). VP-A re-verify required after VP-B before VP-C.

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
| **VP-A** | PIE evidence | DESKTOP | **APPROVED** | [handoffs/VP_A_PIE.md](../Docs/handoffs/VP_A_PIE.md) — hard-fail; **re-verify after VP-B** |
| **VP-B** | Smoke & character risk | DESKTOP | **UNLOCKED / IN PROGRESS** | ABP skeleton + NightMix smoke — resume after HR3 close |
| **Docs/15** | Harness Refine 3 (A+) | CLOUD | **APPROVED** | [15_HR3_A_PLUS.md](../Docs/15_HR3_A_PLUS.md) |
| **HR3-A** | Windows exec reliability | DESKTOP | **APPROVED** | [handoffs/HR3_A_WINDOWS_EXEC.md](../Docs/handoffs/HR3_A_WINDOWS_EXEC.md) |
| **HR3-B** | UE preflight fails loud | CLOUD+DESKTOP | **APPROVED** | [handoffs/HR3_B_UE_PREFLIGHT.md](../Docs/handoffs/HR3_B_UE_PREFLIGHT.md) — PR #60 |
| **HR3-C** | Branch protection | Lead | **DEFERRED / COMPLETE for track** | Lead skip 2026-09-17 ET — [handoffs/HR3_C_BRANCH_PROTECTION.md](../Docs/handoffs/HR3_C_BRANCH_PROTECTION.md) checklist PR #62; GitHub apply deferred |
| **HR3-D** | DESKTOP evidence + re-verify | CLOUD | **APPROVED** | [handoffs/HR3_D_EVIDENCE_LANE.md](../Docs/handoffs/HR3_D_EVIDENCE_LANE.md) — Lead **`APPROVE HR3-D`**, 2026-09-17 ET; PR #64 |
| **HR3 track** | Harness Refine 3 (A+) | — | **CLOSED / COMPLETE** | [15_HR3_A_PLUS.md](../Docs/15_HR3_A_PLUS.md) — HR3-C **DEFERRED**; harness **~A**, swarm **~A+** |
| **VP-C** | Playability polish | CLOUD+DESKTOP | **LOCKED** | Requires VP-A re-verify after VP-B — [14_VP_VERIFY_POLISH.md](../Docs/14_VP_VERIFY_POLISH.md) |
| **VP-D** | Bootstrap dry-run | CLOUD+DESKTOP | **LOCKED** | handoffs/VP_D_BOOTSTRAP_CI.md (pending) |

**Current track:** **HR3 CLOSED / COMPLETE** — Lead **`APPROVE HR3-D`**, 2026-09-17 ET. **VP-B UNLOCKED / IN PROGRESS** (resume). VP-A **APPROVED** — **re-verify after VP-B** before VP-C. VP-C/D **LOCKED**.

---

## Open tasks

| ID | Phase | Host | Owner | Write path | Due artifact |
|---|---|---|---|---|---|
| VP-B-smoke | VP-B | DESKTOP | CND parent | Docs/handoffs/ | **IN PROGRESS** — NightMix smoke + ABP skeleton fix; file `VP_B_SMOKE_CHARACTER.md` |
| VP-A-reverify | VP-A | DESKTOP | CND parent | Docs/handoffs/ | **LOCKED until VP-B** — re-run verb greps after VP-B; checklist in HR3_D handoff |

## Open defects

| ID | Phase | Owner | Blocker | File |
|---|---|---|---|---|
| PA-03 | VP-B | DESKTOP | ABP skeleton missing — blocks verb PIE | [VP_A_PIE.md](../Docs/handoffs/VP_A_PIE.md) |
