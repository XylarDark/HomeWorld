# PHASE BOARD — Conductor only writes status rows

**Current phase:** **Docs/29 Taste Profiler (TP) — CLOSED / COMPLETE** — Lead **`APPROVE TP-E`**, 2026-09-19 ET — [29_TASTE_PROFILER.md](../Docs/29_TASTE_PROFILER.md). Next: Lead-named track or Taste Gate (do not invent).

**Flight fallback armed:** YES — scripted glide along CRUMB_*/GLIDE_SPLINE + portal both ways (Lead: FALLBACK FLIGHT 2026-09-16)  
**Active owners:** **Conductor** (parent DESKTOP) / **DESKTOP-21CT3H0**
**Blocked by:** none — next track TBD (Taste Gate if inventing)
**Sign-off doc:** [Docs/17_HS_AUDIT_SIGN_OFF.md](../Docs/17_HS_AUDIT_SIGN_OFF.md) — **SIGNED OFF** Lead **`SIGN OFF HS AUDIT`**, 2026-09-17 ET.


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

MVP vertical slice and post-audit product wrap are **CLOSED**. **Harness Refine (HR-A…D + HR-B2) is CLOSED.** **Product next-phase (NP-A…E) is CLOSED / COMPLETE.** **HR2 track CLOSED / COMPLETE.** **HR3 track CLOSED / COMPLETE** — Lead **`APPROVE HR3-D`**, 2026-09-17 ET (HR3-C **DEFERRED**). **VP track CLOSED / COMPLETE** (VP-A re-verify **WAIVED**). **Docs/16 Playable Loop CLOSED / COMPLETE** — Lead **`APPROVE PL-D`**, 2026-09-17 ET. **Docs/17 HS Audit CLOSED / COMPLETE** — Lead **`SIGN OFF HS AUDIT`**, 2026-09-17 ET. **Docs/18 VP2 CLOSED / COMPLETE** — Lead **`APPROVE VP2-C STOP`**, 2026-09-17 ET. **Docs/19 D19 CLOSED / COMPLETE** — Lead **`APPROVE D19`**, 2026-09-17 ET. **Docs/20 UASSET CLOSED / COMPLETE**. **Docs/21 Reap & Sow CLOSED / COMPLETE** — Lead **`APPROVE RS-E`**, 2026-09-19 ET. **Docs/26 Night Feel CLOSED / COMPLETE** — Lead **`APPROVE NF-A`**, 2026-09-19 ET. **Docs/27 Night Feel Build CLOSED / COMPLETE** — Lead **`APPROVE NF2-E`**, 2026-09-19 ET. **Docs/28 Taste Gates CLOSED / COMPLETE** — Lead **`APPROVE TG-E`**, 2026-09-19 ET. **Docs/29 Taste Profiler CLOSED / COMPLETE** — Lead **`APPROVE TP-E`**, 2026-09-19 ET. Next: Lead-named track or Taste Gate (do not invent).

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
| **HS-E** | Character / bootstrap canon | CLOUD+Lead+DESKTOP | **APPROVED / CLOSED** | [17e_HS_CONTENT_BOOTSTRAP.md](../Docs/17e_HS_CONTENT_BOOTSTRAP.md) — Lead **`APPROVE HS-E`**, 2026-09-17 ET (PR #97); policy **KEEP-LOCAL**; handoff [HS_E_CONTENT_BOOTSTRAP.md](../Docs/handoffs/HS_E_CONTENT_BOOTSTRAP.md) |
| **HS-F** | Sign-off & re-grade | CLOUD+Lead | **SIGNED OFF / CLOSED** | [17_HS_AUDIT_SIGN_OFF.md](../Docs/17_HS_AUDIT_SIGN_OFF.md) — Lead **`SIGN OFF HS AUDIT`**, 2026-09-17 ET |
| **HS-G** | Conductor/DESKTOP ops diet | CLOUD+DESKTOP+Lead | **APPROVED / COMPLETE** | [17g_HS_G_OPS_DIET.md](../Docs/17g_HS_G_OPS_DIET.md) — Lead **`APPROVE HS-G`**, 2026-09-17 ET (evidence PASS, hang budget, compile hygiene) |
| **Docs/18** | Verify & Prove 2 (VP2) | CLOUD+DESKTOP+Lead | **CLOSED / COMPLETE** | [18_VERIFY_PROVE.md](../Docs/18_VERIFY_PROVE.md) — Lead **`APPROVE VP2-C STOP`**, 2026-09-17 ET; main `2ef961f` |
| **VP2-A** | DESKTOP prove | DESKTOP | **APPROVED / CLOSED** | [VP2_A_EVIDENCE.md](../Docs/handoffs/VP2_A_EVIDENCE.md) — **9/9 PASS** |
| **VP2-B** | Success-path fixes | CLOUD+DESKTOP | **APPROVED / CLOSED** | [VP2_B_FIX.md](../Docs/handoffs/VP2_B_FIX.md) — DESKTOP **9/9 PASS** |
| **VP2-C** | Optional follow-on | — | **STOP / CLOSED** | **C0 Stop** — no C1/C2 |
| **Docs/19** | Thin playability (D19) | CLOUD+DESKTOP+Lead | **CLOSED / COMPLETE** | [19_THIN_PLAYABILITY.md](../Docs/19_THIN_PLAYABILITY.md) — Lead **`APPROVE D19`**, 2026-09-17 ET (PR #107) |
| **D19-A** | Gather piles that stick | CLOUD+DESKTOP | **APPROVED / CLOSED** | DESKTOP: `GP_Gather_*`; `GATHER: RES_WOOD +1` / `harvest ok` |
| **D19-B** | Seed cheat | CLOUD+DESKTOP | **APPROVED / CLOSED** | DESKTOP: `hw.Gather.Seed` → `GATHER: RES_SEED +N` |
| **D19-C** | Success-path evidence filter | CLOUD | **APPROVED / CLOSED** | `evidence-grep.js --success-path`; tests green |
| **Docs/20** | UASSET allowlist + AI provenance | CLOUD+Lead | **APPROVED / COMPLETE** | [20_UASSET_AI_POLICY.md](../Docs/20_UASSET_AI_POLICY.md) — Lead **`APPROVE UASSET POLICY`**, 2026-09-17 ET (PR #108); allowlist **active** |
| **Docs/21** | Reap & Sow (RS) | CLOUD+DESKTOP+Lead | **CLOSED / COMPLETE** | [21_REAP_SOW.md](../Docs/21_REAP_SOW.md) — Lead **`APPROVE RS-E`**, 2026-09-19 ET |
| **RS-A** | Canon stamp | CLOUD | **APPROVED / CLOSED** | Lead **`APPROVE RS-A`**, 2026-09-19 ET |
| **RS-B** | Material triad | CLOUD+DESKTOP | **APPROVED / CLOSED** | Lead **`APPROVE RS-B`**, 2026-09-19 ET — [RS_B_MATERIALS.md](../Docs/handoffs/RS_B_MATERIALS.md) |
| **RS-C** | Animal den | CLOUD+DESKTOP | **APPROVED / CLOSED** | Lead **`APPROVE RS-C`**, 2026-09-19 ET — [RS_C_ANIMAL_DEN.md](../Docs/handoffs/RS_C_ANIMAL_DEN.md) |
| **RS-D** | Humanoid camp | CLOUD+DESKTOP | **APPROVED / CLOSED** | Lead **`APPROVE RS-D`**, 2026-09-19 ET — [RS_D_HUMANOID_CAMP.md](../Docs/handoffs/RS_D_HUMANOID_CAMP.md) |
| **RS-E** | Special cross-bonus | CLOUD+DESKTOP | **APPROVED / CLOSED** | Lead **`APPROVE RS-E`**, 2026-09-19 ET — [RS_E_SPECIAL.md](../Docs/handoffs/RS_E_SPECIAL.md) |
| **Docs/22** | UE 5.8 Upgrade (U58) | CLOUD+DESKTOP+Lead | **STRATEGY APPROVED / ACTIVE** | [22_UE58_UPGRADE.md](../Docs/22_UE58_UPGRADE.md) — Lead unlocked via upgrade plan implement, 2026-09-19 ET |
| **U58-A** | Strategy + engine pin | CLOUD | **APPROVED / CLOSED** | EngineAssociation 5.8 · AGENTS/STACK_PLAN/rules lock docs |
| **U58-B** | Tooling / CI / env paths | CLOUD | **APPROVED / CLOSED** | UE_5.7 → UE_5.8 defaults · runner label `ue58` |
| **U58-C** | First open + Safe-Build | DESKTOP | **APPROVED / CLOSED** | MassEntity removed; Safe-Build green |
| **U58-D** | UnrealMCP + automation | DESKTOP | **APPROVED / CLOSED** | MCP 55557 Listen; Python OK |
| **U58-E** | VS_MVP content / PIE smoke | DESKTOP | **APPROVED / CLOSED** | RS placement + `hw.RS.*` LogTemp PASS |
| **U58-F** | Docs/rules + close + PR | CLOUD+Lead | **APPROVED / CLOSED** | UE58_TECH · ue58-sources · track CLOSED |
| **Docs/23** | UE 5.8 Feature Adoption (U58F) | CLOUD+DESKTOP+Lead | **CLOSED** (PR #111) | [23_UE58_FEATURE_ADOPTION.md](../Docs/23_UE58_FEATURE_ADOPTION.md) |
| **Docs/24** | VS Night / Pine / Mesh (VNP) | CLOUD+DESKTOP+AD | **IMPLEMENTED** | [24_VS_NIGHT_PINE_MESH.md](../Docs/24_VS_NIGHT_PINE_MESH.md) |
| **Docs/25** | Workspace & Tooling Refine (WTR) | CLOUD+DESKTOP | **CLOSED** | [25_WORKSPACE_TOOLING_REFINE.md](../Docs/25_WORKSPACE_TOOLING_REFINE.md) |
| **WTR-A** | Strategy matrix | CLOUD | **DONE** | Docs/25 matrix |
| **WTR-B** | MCP capability matrix | CLOUD+DESKTOP | **DONE** | [U58F_F](../Docs/handoffs/U58F_F_MCP_DECISION.md) — UnrealMCP primary |
| **WTR-C** | Python / evidence harden | DESKTOP | **DONE** | pine import · CAM bind · keep_alive · PCG introspect |
| **WTR-D** | Lookdev tool refine | DESKTOP | **DONE** | PVE notes · PCG dup spike · Mesh CVars |
| **WTR-E** | Stability / Insights | DESKTOP | **DONE** | UE58_TECH playbook |
| **Docs/26** | Night Feel (taste → thin slice) | CLOUD+DESKTOP+AD+Lead | **CLOSED / COMPLETE** | [26_TASTE_NEXT.md](../Docs/26_TASTE_NEXT.md) — Lead **`APPROVE NF-A`**, 2026-09-19 ET |
| **NF-A** | Night feel thin slice | DESKTOP+AD | **APPROVED / CLOSED** | Lead **`APPROVE NF-A`**, 2026-09-19 ET |
| **Docs/27** | Night Feel Build (NF2) | CLOUD+DESKTOP+AD+Lead | **CLOSED / COMPLETE** | [27_NIGHT_FEEL_BUILD.md](../Docs/27_NIGHT_FEEL_BUILD.md) — Lead **`APPROVE NF2-E`**, 2026-09-19 ET |
| **NF2-A** | Soft form-swap feedback | DESKTOP | **APPROVED / CLOSED** | Lead **`APPROVE NF2-A`**, 2026-09-19 ET |
| **NF2-B** | Night lookdev + shots | DESKTOP+AD | **APPROVED / CLOSED** | Lead **`APPROVE NF2-B`**, 2026-09-19 ET |
| **NF2-C** | AD still review | AD | **APPROVED / CLOSED** | Lead **`APPROVE NF2-C`**, 2026-09-19 ET |
| **NF2-D** | Sound asset polish | DESKTOP | **APPROVED / CLOSED** | Lead **`APPROVE NF2-D`**, 2026-09-19 ET (glow-only accept) |
| **NF2-E** | Close track | Lead | **APPROVED / CLOSED** | Lead **`APPROVE NF2-E`**, 2026-09-19 ET |
| **VNP-N0** | Night plumbing smoke | DESKTOP | **DONE** | `u58f_night_look_smoke.py` |
| **VNP-N1** | VS_MVP night tune | DESKTOP+LIT | **DONE** | Fog / warm lights |
| **VNP-N2** | Shots 1/2/5 evidence | DESKTOP | **DONE** | Saved/VNP_Evidence |
| **VNP-P1** | PVE pine KEEP-LOCAL | DESKTOP | **DONE** | Saved/VNP_PVE_Pine OBJ |
| **VNP-P2** | AD pine gate | AD | **APPROVE** | [VNP_P2_AD_PINE_VERDICT.md](../Docs/handoffs/VNP_P2_AD_PINE_VERDICT.md) |
| **VNP-P3** | Allowlist import + PCG | DESKTOP | **PARTIAL** | OBJ staged; uasset pending Editor |
| **VNP-M1** | Mesh Terrain sandbox | DESKTOP | **DONE** | L_U58F_MeshTerrain |
| **VNP-M2** | Cliff spike (no Landscape replace) | DESKTOP | **SPIKE STAMPED** | KEEP-LOCAL |
| **U58F-A** | Strategy + matrix | CLOUD | **APPROVED** | Docs/23 · UE58_TECH capabilities table |
| **U58F-B** | PCG 5.8 workflow | CLOUD+DESKTOP | **APPROVED** | PCGBiomeCore/Primitives · `u58f_pcg_smoke.py` |
| **U58F-C** | PVE stylized pine | DESKTOP+AD | **PLUGIN ON / AD PENDING** | Plugin on · AD gate [U58F_C_PVE_PINE.md](../Docs/handoffs/U58F_C_PVE_PINE.md) |
| **U58F-D** | MegaLights + Fog SSS | DESKTOP | **APPROVED** | DefaultEngine.ini · `u58f_night_look_smoke.py` |
| **U58F-E** | Lumen Lite path | CLOUD | **APPROVED** | Medium GI/Reflections · DefaultScalability.ini |
| **U58F-F** | MCP decision | CLOUD | **APPROVED** | Keep UnrealMCP · [U58F_F_MCP_DECISION.md](../Docs/handoffs/U58F_F_MCP_DECISION.md) |
| **U58F-G** | Mesh Terrain spike | DESKTOP | **SPIKE READY** | Plugin on · sandbox only · [U58F_G_MESH_TERRAIN.md](../Docs/handoffs/U58F_G_MESH_TERRAIN.md) |

**Current track:** none active — Docs/29 **CLOSED** (Lead **`APPROVE TP-E`**). Next: Lead-named track or Taste Gate.

### Docs/29 Taste Profiler (TP)

| Phase | Focus | Host | Status | Evidence |
|-------|--------|------|--------|----------|
| **TP-A** | Research digest | CLOUD | **DONE** | [29_TASTE_PROFILER.md](../Docs/29_TASTE_PROFILER.md) |
| **TP-B** | Strategy matrix | CLOUD | **DONE** | Implement-plan unlock ≈ **`APPROVE TP STRATEGY`** |
| **TP-C** | Profile + skills | CLOUD | **DONE** | [taste-profile.md](../docs/human-use/taste-profile.md) · skills taste-profiler / taste-gate |
| **TP-D** | Dry-run prove | CLOUD | **DONE** | [TP_D_PROVE.md](../Docs/handoffs/TP_D_PROVE.md) — Lead **`APPROVE TP-D`**, 2026-09-19 ET |
| **TP-E** | Close Docs/29 | Lead | **DONE** | [TP_E_CLOSE.md](../Docs/handoffs/TP_E_CLOSE.md) — Lead **`APPROVE TP-E`**, 2026-09-19 ET |

### Docs/28 Taste Gates (TG)

| Phase | Focus | Host | Status | Evidence |
|-------|--------|------|--------|----------|
| **TG-A** | Research digest | CLOUD | **DONE** | [28_TASTE_GATES.md](../Docs/28_TASTE_GATES.md) |
| **TG-B** | Strategy matrix | CLOUD | **DONE** | Implement-plan unlock ≈ **`APPROVE TG STRATEGY`** |
| **TG-C** | Skill + human-use + rule | CLOUD | **DONE** | `.cursor/skills/taste-gate/` · [taste-gates.md](../docs/human-use/taste-gates.md) |
| **TG-D** | Dry-run prove | CLOUD | **DONE** | [TG_D_PROVE.md](../Docs/handoffs/TG_D_PROVE.md) — Lead **`APPROVE TG-D`**, 2026-09-19 ET |
| **TG-E** | Close Docs/28 | Lead | **DONE** | [TG_E_CLOSE.md](../Docs/handoffs/TG_E_CLOSE.md) — Lead **`APPROVE TG-E`**, 2026-09-19 ET |

---

## Open tasks

| ID | Phase | Host | Owner | Write path | Due artifact |
|---|---|---|---|---|---|
| TP-E-close | TP-E | Lead | Lead | Docs/29 · PHASE_BOARD | [TP_E_CLOSE.md](../Docs/handoffs/TP_E_CLOSE.md) — **APPROVED / CLOSED** Lead **`APPROVE TP-E`**, 2026-09-19 ET |
| TP-D-prove | TP-D | CLOUD+Lead | CND+Lead | Docs/handoffs + Saved/ | [TP_D_PROVE.md](../Docs/handoffs/TP_D_PROVE.md) — **APPROVED / CLOSED** Lead **`APPROVE TP-D`**, 2026-09-19 ET |
| TG-E-close | TG-E | Lead | Lead | Docs/28 · PHASE_BOARD | [TG_E_CLOSE.md](../Docs/handoffs/TG_E_CLOSE.md) — **APPROVED / CLOSED** Lead **`APPROVE TG-E`**, 2026-09-19 ET |
| TG-D-prove | TG-D | CLOUD+Lead | CND+Lead | Docs/handoffs + Saved/ | [TG_D_PROVE.md](../Docs/handoffs/TG_D_PROVE.md) — **APPROVED / CLOSED** Lead **`APPROVE TG-D`**, 2026-09-19 ET |
| VNP-N0 | VNP-N0 | DESKTOP | CND | Saved/ · Docs/24 | Night smoke JSON |
| VNP-N2 | VNP-N2 | DESKTOP | CND | Saved/ evidence | Shots 1/2/5 |
| VNP-P2 | VNP-P2 | AD | AD | Docs/handoffs | AD pine verdict |
| VNP-M1 | VNP-M1 | DESKTOP | CND | Maps/Sandbox KEEP-LOCAL | Mesh Terrain sandbox |
| U58F-C-pve | U58F-C | DESKTOP+AD | CND+AD | Docs/handoffs + Content/HomeWorld | [U58F_C_PVE_PINE.md](../Docs/handoffs/U58F_C_PVE_PINE.md) — **AD PENDING** |
| U58F-G-sandbox | U58F-G | DESKTOP | CND | Maps/Sandbox KEEP-LOCAL | [U58F_G_MESH_TERRAIN.md](../Docs/handoffs/U58F_G_MESH_TERRAIN.md) — spike ready |
| U58-A-pin | U58-A | CLOUD | CND | Docs/22 · HomeWorld.uproject · AGENTS · STACK_PLAN · rules | EngineAssociation 5.8 — **IN PROGRESS** |
| U58-B-paths | U58-B | CLOUD | CND | Tools/ · .github/ · docs/Setup/ | UE_5.7 → UE_5.8 defaults — **LOCKED** |
| U58-C-build | U58-C | DESKTOP | CND | Source/ · docs/KNOWN_ERRORS.md | Safe-Build on 5.8 — **LOCKED** |
| U58-D-mcp | U58-D | DESKTOP | CND | Plugins/UnrealMCP · AUTOMATION_GAPS | MCP green + pie — **LOCKED** |
| U58-E-smoke | U58-E | DESKTOP | CND | Maps/VS_MVP · Content/Python | VS_MVP PIE smoke — **LOCKED** |
| U58-F-docs | U58-F | CLOUD+Lead | CND+Lead | docs/UE/UE58_TECH · ue58-sources · PR | Close track — **LOCKED** |
| RS-E-special | RS-E | CLOUD+DESKTOP+Lead | CND+Lead | Source/ + Content/Python + Docs/handoffs/ | [RS_E_SPECIAL.md](../Docs/handoffs/RS_E_SPECIAL.md) · `hw.RS.*` · `place_vs_mvp_rs_special_site.py` — **APPROVED / CLOSED** Lead **`APPROVE RS-E`**, 2026-09-19 ET |
| RS-D-camp | RS-D | CLOUD+DESKTOP | CND | Content/Python + Docs/handoffs/ | [RS_D_HUMANOID_CAMP.md](../Docs/handoffs/RS_D_HUMANOID_CAMP.md) · `place_vs_mvp_rs_humanoid_camp.py` — **APPROVED / CLOSED** Lead **`APPROVE RS-D`**, 2026-09-19 ET |
| RS-C-den | RS-C | CLOUD+DESKTOP | CND | Content/Python + Docs/handoffs/ | [RS_C_ANIMAL_DEN.md](../Docs/handoffs/RS_C_ANIMAL_DEN.md) · `place_vs_mvp_rs_animal_den.py` — **APPROVED / CLOSED** Lead **`APPROVE RS-C`**, 2026-09-19 ET |
| RS-B-materials | RS-B | CLOUD+DESKTOP | CND | Content/Python + Docs/handoffs/ | [RS_B_MATERIALS.md](../Docs/handoffs/RS_B_MATERIALS.md) · `place_vs_mvp_rs_material_sites.py` — **APPROVED / CLOSED** Lead **`APPROVE RS-B`**, 2026-09-19 ET |
| RS-A-canon | RS-A | CLOUD+Lead | CND+Lead | Docs/ + VisionBoard/ | [01_GDD_MVP.md](../Docs/01_GDD_MVP.md) §3.1 · Vision pointer · [21_REAP_SOW.md](../Docs/21_REAP_SOW.md) — **APPROVED / CLOSED** Lead **`APPROVE RS-A`**, 2026-09-19 ET |
| RS-strategy | Docs/21 | CLOUD+Lead | CND+Lead | Docs/ | [21_REAP_SOW.md](../Docs/21_REAP_SOW.md) — **APPROVED** Lead **`APPROVE RS STRATEGY`**, 2026-09-19 ET |
| CD-A-stubs | CD-A | CLOUD+DESKTOP | CND | Source/ + Content/Python + Docs/handoffs/ | [CD_A_STUBS.md](../Docs/handoffs/CD_A_STUBS.md) · `place_vs_mvp_cd_stubs.py` · `MINIGAME:*` · `BOSS:PHASE_*` — **IN PROGRESS** Lead **`APPROVE CD STRATEGY`** granted; **`APPROVE CD-A`** pending |
| UASSET-policy | Docs/20 | CLOUD+Lead | CND+Lead | Docs/ + config/ + scripts/ | [20_UASSET_AI_POLICY.md](../Docs/20_UASSET_AI_POLICY.md) · [AI_ASSET_LOG.md](../Docs/AI_ASSET_LOG.md) — **APPROVED / CLOSED** Lead **`APPROVE UASSET POLICY`**, 2026-09-17 ET (PR #108) |
| HS-F-sign-off | HS-F | CLOUD+Lead | CND+Lead | Docs/ | [17_HS_AUDIT_SIGN_OFF.md](../Docs/17_HS_AUDIT_SIGN_OFF.md) — **CLOSED** Lead **`SIGN OFF HS AUDIT`**, 2026-09-17 ET |
| HS-E-bootstrap | HS-E | CLOUD+Lead+DESKTOP | CND+Lead | Docs/ | [17e_HS_CONTENT_BOOTSTRAP.md](../Docs/17e_HS_CONTENT_BOOTSTRAP.md) · [HS_E_CONTENT_BOOTSTRAP.md](../Docs/handoffs/HS_E_CONTENT_BOOTSTRAP.md) — **APPROVED / CLOSED** Lead **`APPROVE HS-E`**, 2026-09-17 ET (KEEP-LOCAL) |
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

| VP2-A-evidence | VP2-A | DESKTOP | CND | Docs/handoffs | [VP2_A_EVIDENCE.md](../Docs/handoffs/VP2_A_EVIDENCE.md) — **APPROVED / CLOSED** — Lead **`APPROVE VP2-A`**, 2026-09-17 ET (retry **9/9 PASS**; soft-reject caveats historical) |
| VP2-B-fix | VP2-B | CLOUD+DESKTOP | CND | Docs/handoffs + Source/ | [VP2_B_FIX.md](../Docs/handoffs/VP2_B_FIX.md) — **APPROVED / CLOSED** — Lead **`APPROVE VP2-B`**, 2026-09-17 ET (DESKTOP 9/9 success-path) |
