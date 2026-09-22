# Docs/ — MVP swarm canon

This directory is **Blender-first MVP swarm canon**: GDD slices, art bible, material sheet, WAVE handoffs, and QA placeholders for the multi-agent production kit.

## Do not merge with `docs/`

| Path | Purpose |
|------|---------|
| **`Docs/`** (this tree) | MVP swarm operating system — canon, handoffs, shot list, kit-facing specs linked from `Lib/` |
| **`docs/`** (lowercase) | Unreal Engine 5.8 project documentation — setup, automation, PCG, task lists, known errors |

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
- **Harness Refine 3 — A+ strategy (APPROVED):** [15_HR3_A_PLUS.md](15_HR3_A_PLUS.md) — Lead **`APPROVE HR3 STRATEGY`**, 2026-09-17 ET
| [16_PLAYABLE_LOOP.md](16_PLAYABLE_LOOP.md) | Playable Loop (PL) — character + PIE + thin UX | **CLOSED / COMPLETE** |
| [17_HS_AUDIT_STRATEGY.md](17_HS_AUDIT_STRATEGY.md) | Harness & Swarm Audit (HS) — post–Docs/08 | **CLOSED / COMPLETE** |
| [17a_HS_INVENTORY.md](17a_HS_INVENTORY.md) | HS-A inventory & debt ledger | **CLOSED** |
| [17b_HS_SWARM_OPS.md](17b_HS_SWARM_OPS.md) | HS-B swarm ops tighten | **CLOSED** |
| [17c_HS_CI_LAW.md](17c_HS_CI_LAW.md) | HS-C CI as law | **DEFERRED / CLOSED** |
| [17d_HS_EVIDENCE.md](17d_HS_EVIDENCE.md) | HS-D evidence & re-verify | **CLOSED** |
| [17e_HS_CONTENT_BOOTSTRAP.md](17e_HS_CONTENT_BOOTSTRAP.md) | HS-E character / bootstrap canon — policy **KEEP-LOCAL** | **CLOSED** |
| [20_UASSET_AI_POLICY.md](20_UASSET_AI_POLICY.md) | UASSET allowlist + AI asset provenance | **APPROVED / COMPLETE** — Lead **`APPROVE UASSET POLICY`**, 2026-09-17 ET |
| [21_REAP_SOW.md](21_REAP_SOW.md) | Reap & Sow (day reap / night sow / dream combat / planet sites) | **CLOSED / COMPLETE** — Lead **`APPROVE RS-E`**, 2026-09-19 ET |
| [22_GATHER_CRAFT_IMPL.md](22_GATHER_CRAFT_IMPL.md) | Gather & Craft impl (site→RES, hearth recipes) | **CLOSED / COMPLETE** — Lead **`APPROVE GC-C`**, 2026-09-21 ET |
| [23_COMBAT_DREAM_IMPL.md](23_COMBAT_DREAM_IMPL.md) | Combat & Dream impl (minigame stubs, boss phase volume) | **CLOSED / COMPLETE** — Lead **`APPROVE CD-A`**, 2026-09-21 ET |
| [24_MOVEMENT_IMPL.md](24_MOVEMENT_IMPL.md) | Movement impl (traversal stubs, spirit blink, mount boost) | **CLOSED / COMPLETE** — Lead **`APPROVE MV-A`**, 2026-09-21 ET |
| [25_SPIRIT_STEALTH_IMPL.md](25_SPIRIT_STEALTH_IMPL.md) | Spirit Stealth impl (lit volumes, A2 alert stubs) | **CLOSED / COMPLETE** — Lead **`APPROVE SS-A`**, 2026-09-21 ET |
| [22_UE58_UPGRADE.md](22_UE58_UPGRADE.md) | UE 5.8 Upgrade (U58) — EngineAssociation + tooling cutover | **CLOSED / COMPLETE** — 2026-09-19 ET |
| [23_UE58_FEATURE_ADOPTION.md](23_UE58_FEATURE_ADOPTION.md) | UE 5.8 Feature Adoption (U58F) - PCG/PVE/MegaLights/Fog SSS/Lumen Lite | **CLOSED / COMPLETE** - 2026-09-19 ET |
| [24_VS_NIGHT_PINE_MESH.md](24_VS_NIGHT_PINE_MESH.md) | VS Night / Pine / Mesh (VNP) — MegaLights evidence, PVE pine, Mesh Terrain sandbox | **IMPLEMENTED** — 2026-09-19 ET |
| [25_WORKSPACE_TOOLING_REFINE.md](25_WORKSPACE_TOOLING_REFINE.md) | Workspace & Tooling Refine (WTR) — MCP matrix, evidence, stability | **CLOSED** — 2026-09-19 ET |
| [26_TASTE_NEXT.md](26_TASTE_NEXT.md) | Night Feel (NF) — taste gate + thin slice dusk/dawn | **CLOSED / COMPLETE** — Lead **`APPROVE NF-A`**, 2026-09-19 ET |
| [27_NIGHT_FEEL_BUILD.md](27_NIGHT_FEEL_BUILD.md) | Night Feel Build (NF2) — soft dusk/dawn feedback phases | **CLOSED / COMPLETE** — Lead **`APPROVE NF2-E`**, 2026-09-19 ET |
| [28_TASTE_GATES.md](28_TASTE_GATES.md) | Taste Gates (TG) — detect/queue/resume human taste limits | **CLOSED / COMPLETE** — Lead **`APPROVE TG-E`**, 2026-09-19 ET |
| [29_TASTE_PROFILER.md](29_TASTE_PROFILER.md) | Taste Profiler (TP) — durable profile + session promote | **CLOSED / COMPLETE** — Lead **`APPROVE TP-E`**, 2026-09-19 ET |
| [30_DEMO_SPINE.md](30_DEMO_SPINE.md) | Demo Spine (DS) — visible campfire → tent → cottage | **DS STRATEGY APPROVED** — Lead **`APPROVE DEMO-SPINE`**, 2026-09-21 ET; **DS-A IN PROGRESS** |
| [17_HS_AUDIT_SIGN_OFF.md](17_HS_AUDIT_SIGN_OFF.md) | HS-F sign-off & re-grade | **IN PROGRESS** (PENDING **`SIGN OFF HS AUDIT`**) |
- **HR3-C branch protection (PENDING LEAD APPLY):** [15c_HR3_C_BRANCH_PROTECTION.md](15c_HR3_C_BRANCH_PROTECTION.md) — Lead checklist in [docs/Setup/CI_SETUP.md](../docs/Setup/CI_SETUP.md); handoff [handoffs/HR3_C_BRANCH_PROTECTION.md](handoffs/HR3_C_BRANCH_PROTECTION.md)
- **Start swarm:** [../START_HERE.md](../START_HERE.md)
- **Master prompt:** [../HOMEWORLD_MASTER_PROMPT.md](../HOMEWORLD_MASTER_PROMPT.md)
- **Game canon brief:** [../HOMEWORLD_MVP_SWARM_BRIEF.md](../HOMEWORLD_MVP_SWARM_BRIEF.md)
- **Swarm ops:** [../swarm/SWARM_OPS.md](../swarm/SWARM_OPS.md)
- **Gather & craft bible (LOCKED):** [GATHER_CRAFT_BIBLE.md](GATHER_CRAFT_BIBLE.md) — impl [GATHER_CRAFT_IMPL_PROMPT.md](GATHER_CRAFT_IMPL_PROMPT.md)
- **UE project context:** [../AGENTS.md](../AGENTS.md) and [../docs/README.md](../docs/README.md)
| [18_VERIFY_PROVE.md](18_VERIFY_PROVE.md) | Verify & Prove (VP2) | **DRAFT** |
