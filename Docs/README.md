# Docs/ — MVP swarm canon

This directory is **Blender-first MVP swarm canon**: GDD slices, art bible, material sheet, WAVE handoffs, and QA placeholders for the multi-agent production kit.

## Do not merge with `docs/`

| Path | Purpose |
|------|---------|
| **`Docs/`** (this tree) | MVP swarm operating system — canon, handoffs, shot list, kit-facing specs linked from `Lib/` |
| **`docs/`** (lowercase) | Unreal Engine 5.7 project documentation — setup, automation, PCG, task lists, known errors |

These are **intentionally separate**. On case-insensitive filesystems (macOS/Windows defaults), Git may only check out one of the two names locally — clone on Linux CI or use a case-sensitive volume if you need both trees simultaneously.

## Entry points

- **UE import first pass:** [05_UE_IMPORT_FIRST_PASS.md](05_UE_IMPORT_FIRST_PASS.md)
- **VS_MVP kit dress (post-audit):** [06_VS_MVP_DRESS.md](06_VS_MVP_DRESS.md)
- **Audit & upgrade strategy:** [08_AUDIT_UPGRADE_STRATEGY.md](08_AUDIT_UPGRADE_STRATEGY.md) — **COMPLETE** (Lead signed off)
- **WAVE A inventory:** [08a_INVENTORY.md](08a_INVENTORY.md)
- **WAVE B harness gap:** [08b_HARNESS_GAP.md](08b_HARNESS_GAP.md) — COMPLETE (PR #12)
- **WAVE C boot health:** [08c_BOOT_HEALTH.md](08c_BOOT_HEALTH.md) — COMPLETE (PR #13)
- **WAVE D content canon:** [08d_CONTENT_CANON.md](08d_CONTENT_CANON.md) — COMPLETE (PR #14 merged)
- **WAVE E upgrade pass:** [08e_UPGRADE_PASS.md](08e_UPGRADE_PASS.md) — COMPLETE (PR #15 merged)
- **WAVE F audit sign-off:** [08_AUDIT_SIGN_OFF.md](08_AUDIT_SIGN_OFF.md) — **SIGNED OFF** (PR #16 merged; Lead Luke Thompson, 2026-09-16 ET)
- **FALLBACK glide + portal runbook:** [09_FALLBACK_GLIDE.md](09_FALLBACK_GLIDE.md) — CRUMB scripted glide V2 + dual shrine portal
- **Post-audit wrap (CLOSED):** [10_POST_AUDIT_WRAP.md](10_POST_AUDIT_WRAP.md) — master graphs + NightMix
- **Swarm & harness audit (APPROVED):** [11_SWARM_HARNESS_AUDIT.md](11_SWARM_HARNESS_AUDIT.md) — Lead Luke Thompson, 2026-09-17 ET
- **Swarm & harness refine (CLOSED):** [11_SWARM_HARNESS_REFINE.md](11_SWARM_HARNESS_REFINE.md) — HR-A…D + HR-B2 approved (Lead Luke Thompson, 2026-09-17 ET)
- **HR-A measures (APPROVED):** [11a_HR_MEASURES.md](11a_HR_MEASURES.md) — baseline tables
- **HR-B harness tighten (APPROVED):** [11b_HR_B_HANDOFF.md](11b_HR_B_HANDOFF.md)
- **HR-C swarm ops refine (APPROVED):** [11c_HR_C_HANDOFF.md](11c_HR_C_HANDOFF.md) — Lead Luke Thompson, 2026-09-17 ET
- **HR-D prove dry-run (APPROVED):** [11d_HR_D_HANDOFF.md](11d_HR_D_HANDOFF.md) — Lead **`APPROVE HR-D`**, 2026-09-17 ET
- **HR-D defer stamp (CLOSED):** [11d_HR_D_DEFER.md](11d_HR_D_DEFER.md) — HR-B2 first, then HR-D approved
- **HR-B2 residual harness (APPROVED):** [11e_HR_B2_HANDOFF.md](11e_HR_B2_HANDOFF.md) — Lead **`APPROVE HR-B2`**, 2026-09-17 ET
- **Product next-phase (APPROVED):** [11_NEXT_PHASE_STRATEGY.md](11_NEXT_PHASE_STRATEGY.md) — Lead **`APPROVE NP STRATEGY`**, 2026-09-17 ET
- **NP-A inventory / gap map (APPROVED):** [12a_NP_A_INVENTORY.md](12a_NP_A_INVENTORY.md) — Lead **`APPROVE NP-A`**, 2026-09-17 ET
- **NP-B lookdev apply (APPROVED):** [12b_NP_B_LOOKDEV.md](12b_NP_B_LOOKDEV.md) — Lead **`APPROVE NP-B`**, 2026-09-17 ET
- **NP-C form + V1 polish (APPROVED):** [12c_NP_C_FORM_V1.md](12c_NP_C_FORM_V1.md) — Lead **`APPROVE NP-C`**, 2026-09-17 ET
- **NP-D SYS V3–V4 gather + tame (APPROVED):** [12d_NP_D_SYS_V3_V4.md](12d_NP_D_SYS_V3_V4.md) — Lead **`APPROVE NP-D`**, 2026-09-17 ET
- **NP-E heal + nurture + dawn persist (APPROVED):** [12e_NP_E_SYS_V6_V8.md](12e_NP_E_SYS_V6_V8.md) — Lead **`APPROVE NP-E`**, 2026-09-17 ET
- **Harness Refine 2 strategy (APPROVED):** [13_HR2_HARNESS_REFINE.md](13_HR2_HARNESS_REFINE.md) — Lead **`APPROVE HR2 STRATEGY`**, 2026-09-17 ET
- **HR2-A doctor signal (APPROVED):** [13a_HR2_A_HANDOFF.md](13a_HR2_A_HANDOFF.md) — Lead **`APPROVE HR2-A`**, 2026-09-17 ET
- **HR2-B cold-clone submodule (APPROVED):** [13b_HR2_B_COLD_CLONE.md](13b_HR2_B_COLD_CLONE.md) — Lead **`APPROVE HR2-B`**, 2026-09-17 ET
- **HR2-C C++ CI gate (APPROVED — HR2 track CLOSED):** [13c_HR2_C_CI_GATE.md](13c_HR2_C_CI_GATE.md) — Lead **`APPROVE HR2-C`**, 2026-09-17 ET
- **Verify & Polish strategy (APPROVED — VP-B PARKED):** [14_VP_VERIFY_POLISH.md](14_VP_VERIFY_POLISH.md) — Lead **`APPROVE VP STRATEGY`**, 2026-09-17 ET; VP-A **APPROVED**; VP-B **PARKED** pending HR3
- **Harness Refine 3 — A+ strategy (APPROVED — HR3-A IN PROGRESS):** [15_HR3_A_PLUS.md](15_HR3_A_PLUS.md) — Lead **`APPROVE HR3 STRATEGY`**, 2026-09-17 ET
- **Start swarm:** [../START_HERE.md](../START_HERE.md)
- **Master prompt:** [../HOMEWORLD_MASTER_PROMPT.md](../HOMEWORLD_MASTER_PROMPT.md)
- **Game canon brief:** [../HOMEWORLD_MVP_SWARM_BRIEF.md](../HOMEWORLD_MVP_SWARM_BRIEF.md)
- **Swarm ops:** [../swarm/SWARM_OPS.md](../swarm/SWARM_OPS.md)
- **UE project context:** [../AGENTS.md](../AGENTS.md) and [../docs/README.md](../docs/README.md)
