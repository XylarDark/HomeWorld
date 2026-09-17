# PHASE BOARD — Conductor only writes status rows

**Current phase:** **PRODUCT NP TRACK CLOSED** — Lead **`APPROVE NP-E`** (Luke Thompson, 2026-09-17 ET)  
**Flight fallback armed:** YES — scripted glide along CRUMB_*/GLIDE_SPLINE + portal both ways (Lead: FALLBACK FLIGHT 2026-09-16)  
**Active owners:** **CND** (Conductor) — no open product NP phases  
**Blocked by:** —

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

MVP vertical slice and post-audit product wrap are **CLOSED**. **Harness Refine (HR-A…D + HR-B2) is CLOSED.** **Product next-phase (NP-A…E) is CLOSED / COMPLETE** — Lead **`APPROVE NP-E`**, 2026-09-17 ET.

| Track | Doc / phase | Status | Gate / handoff |
|---|---|---|---|
| Docs/05 | UE import first pass | **CLOSED** | [05_UE_IMPORT_FIRST_PASS.md](../Docs/05_UE_IMPORT_FIRST_PASS.md) |
| Docs/06 | VS_MVP dress | **CLOSED** | [06_VS_MVP_DRESS.md](../Docs/06_VS_MVP_DRESS.md) |
| Docs/07 | Vertical slice sign-off | **CLOSED** | [07_VERTICAL_SLICE_SIGN OFF.md](../Docs/07_VERTICAL_SLICE_SIGN%20OFF.md) |
| Docs/08–10 | Audit WAVEs + post-audit wrap | **CLOSED** | [08_AUDIT_SIGN_OFF.md](../Docs/08_AUDIT_SIGN_OFF.md), [10_POST_AUDIT_WRAP.md](../Docs/10_POST_AUDIT_WRAP.md) |
| Docs/11 | Product next-phase strategy | **APPROVED** | [11_NEXT_PHASE_STRATEGY.md](../Docs/11_NEXT_PHASE_STRATEGY.md) |
| Docs/11 | Swarm & harness refine | **CLOSED** | [11_SWARM_HARNESS_REFINE.md](../Docs/11_SWARM_HARNESS_REFINE.md) |
| **HR-A…B2, HR-D** | Harness refine | **APPROVED** | See Docs/11a–11e |
| **NP-A** | Inventory / gap map | **APPROVED** | [12a_NP_A_INVENTORY.md](../Docs/12a_NP_A_INVENTORY.md) |
| **NP-B** | Lookdev apply | **APPROVED** | [12b_NP_B_LOOKDEV.md](../Docs/12b_NP_B_LOOKDEV.md) |
| **NP-C** | Form + V1 polish | **APPROVED** | [12c_NP_C_FORM_V1.md](../Docs/12c_NP_C_FORM_V1.md) |
| **NP-D** | SYS V3–V4 gather + tame | **APPROVED** | [12d_NP_D_SYS_V3_V4.md](../Docs/12d_NP_D_SYS_V3_V4.md) — Lead **`APPROVE NP-D`**, 2026-09-17 ET |
| **NP-E** | Heal + nurture + persist | **APPROVED** | [12e_NP_E_SYS_V6_V8.md](../Docs/12e_NP_E_SYS_V6_V8.md), [handoffs/NP_E_SYS_V6_V8.md](../Docs/handoffs/NP_E_SYS_V6_V8.md) — Lead **`APPROVE NP-E`**, 2026-09-17 ET |

**Current track:** **PRODUCT NP TRACK CLOSED** — NP-A…E all **APPROVED**. Placement script fixes on main (`870f1d0`). No NP-F; no next product NP gate.

---

## Open tasks

| ID | Phase | Owner | Write path | Due artifact |
|---|---|---|---|---|
| — | — | — | — | Product NP track closed — no open NP tasks |

## Open defects

| ID | Phase | Owner | Blocker | File |
|---|---|---|---|---|
| — | — | — | — | — |
