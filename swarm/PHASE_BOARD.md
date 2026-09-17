# PHASE BOARD — Conductor only writes status rows

**Current phase:** **HR2-A** (Doctor signal) — **IN PROGRESS** — await Lead **`APPROVE HR2-A`**  
**Flight fallback armed:** YES — scripted glide along CRUMB_*/GLIDE_SPLINE + portal both ways (Lead: FALLBACK FLIGHT 2026-09-16)  
**Active owners:** **CND** (Conductor) + cloud agent (HR2-A PR)  
**Blocked by:** Lead **`APPROVE HR2-A`** — [Docs/13a_HR2_A_HANDOFF.md](../Docs/13a_HR2_A_HANDOFF.md)

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

MVP vertical slice and post-audit product wrap are **CLOSED**. **Harness Refine (HR-A…D + HR-B2) is CLOSED.** **Product next-phase (NP-A…E) is CLOSED / COMPLETE** — Lead **`APPROVE NP-E`**, 2026-09-17 ET. **HR2 strategy APPROVED** — Lead **`APPROVE HR2 STRATEGY`**, 2026-09-17 ET. Active: **HR2-A IN PROGRESS**.

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
| **HR2-A** | Doctor signal (UE host) | **IN PROGRESS** | [13a_HR2_A_HANDOFF.md](../Docs/13a_HR2_A_HANDOFF.md) — await **`APPROVE HR2-A`** |
| **HR2-B** | Cold-clone submodule | **LOCKED** | Blocked until **`APPROVE HR2-A`** |
| **HR2-C** | C++ CI gate (build-win64) | **LOCKED** | Blocked until **`APPROVE HR2-B`** |

**Current track:** HR2-A **IN PROGRESS** — `npm run doctor:ue` implemented; Conductor stops for Lead **`APPROVE HR2-A`**. Product NP **CLOSED**.

---

## Open tasks

| ID | Phase | Owner | Write path | Due artifact |
|---|---|---|---|---|
| HR2-A-gate | HR2-A | Lead | Docs/ | **`APPROVE HR2-A`** → unlock HR2-B |

## Open defects

| ID | Phase | Owner | Blocker | File |
|---|---|---|---|---|
| — | — | — | — | — |
