# PHASE BOARD — Conductor only writes status rows

**Current phase:** **NP-B** (Product next-phase — lookdev apply)  
**Flight fallback armed:** YES — scripted glide along CRUMB_*/GLIDE_SPLINE + portal both ways (Lead: FALLBACK FLIGHT 2026-09-16)  
**Active owners:** **CND** (Conductor)  
**Blocked by:** — (await Lead **`APPROVE NP-B`** after Windows run evidence)

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

MVP vertical slice and post-audit product wrap are **CLOSED**. **Harness Refine (HR-A…D + HR-B2) is CLOSED.** Active work is **Product next-phase (NP-A…E)**.

| Track | Doc / phase | Status | Gate / handoff |
|---|---|---|---|
| Docs/05 | UE import first pass | **CLOSED** | [05_UE_IMPORT_FIRST_PASS.md](../Docs/05_UE_IMPORT_FIRST_PASS.md) |
| Docs/06 | VS_MVP dress | **CLOSED** | [06_VS_MVP_DRESS.md](../Docs/06_VS_MVP_DRESS.md) |
| Docs/07 | Vertical slice sign-off | **CLOSED** | [07_VERTICAL_SLICE_SIGN OFF.md](../Docs/07_VERTICAL_SLICE_SIGN%20OFF.md) |
| Docs/08–10 | Audit WAVEs + post-audit wrap | **CLOSED** | [08_AUDIT_SIGN_OFF.md](../Docs/08_AUDIT_SIGN_OFF.md), [10_POST_AUDIT_WRAP.md](../Docs/10_POST_AUDIT_WRAP.md) |
| Docs/11 | Product next-phase strategy | **APPROVED** | [11_NEXT_PHASE_STRATEGY.md](../Docs/11_NEXT_PHASE_STRATEGY.md) — Lead **`APPROVE NP STRATEGY`**, 2026-09-17 ET |
| Docs/11 | Swarm & harness refine | **CLOSED** | [11_SWARM_HARNESS_REFINE.md](../Docs/11_SWARM_HARNESS_REFINE.md) |
| **HR-A** | Measure & inventory | **APPROVED** | [11a_HR_MEASURES.md](../Docs/11a_HR_MEASURES.md) |
| **HR-B** | Harness tighten | **APPROVED** | [11b_HR_B_HANDOFF.md](../Docs/11b_HR_B_HANDOFF.md) |
| **HR-C** | Swarm ops refine | **APPROVED** | [11c_HR_C_HANDOFF.md](../Docs/11c_HR_C_HANDOFF.md) |
| **HR-D** | Prove (dry-run loop) | **APPROVED** | [11d_HR_D_HANDOFF.md](../Docs/11d_HR_D_HANDOFF.md) |
| **HR-B2** | Residual harness risks | **APPROVED** | [11e_HR_B2_HANDOFF.md](../Docs/11e_HR_B2_HANDOFF.md) |
| **NP-A** | Inventory / gap map | **APPROVED** | [12a_NP_A_INVENTORY.md](../Docs/12a_NP_A_INVENTORY.md) — Lead **`APPROVE NP-A`**, 2026-09-17 ET |
| **NP-B** | Lookdev apply | **COMPLETE — awaiting APPROVE NP-B** | [12b_NP_B_LOOKDEV.md](../Docs/12b_NP_B_LOOKDEV.md), [handoffs/NP_B_LOOKDEV.md](../Docs/handoffs/NP_B_LOOKDEV.md) |
| **NP-C…E** | Form + SYS verbs | **LOCKED** | Blocked until Lead **`APPROVE NP-B`** |

**Current track:** NP-A **APPROVED** (Lead **`APPROVE NP-A`**, 2026-09-17 ET). **NP-B COMPLETE** (script + docs) — await Windows evidence + Lead **`APPROVE NP-B`**.

---

## Open tasks

| ID | Phase | Owner | Write path | Due artifact |
|---|---|---|---|---|
| NP-B-run | NP-B | CND | Docs/handoffs/ | Run `assign_vs_mvp_materials.py` on DESKTOP; fill NP_B_LOOKDEV evidence |
| NP-B-gate | NP-B | Lead | Docs/ | **`APPROVE NP-B`** → unlock NP-C |

## Open defects

| ID | Phase | Owner | Blocker | File |
|---|---|---|---|---|
| — | — | — | — | — |
