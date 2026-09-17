# Docs/15 — Harness Refine 3 (HR3): A+ Strategy

| Field | Value |
|-------|-------|
| **Status** | **APPROVED / ACTIVE** — Lead Luke Thompson, **`APPROVE HR3 STRATEGY`**, 2026-09-17 ET |
| **Gate** | **`APPROVE HR3 STRATEGY`** — **APPROVED** (Luke Thompson, 2026-09-17 ET) |
| **HR3-A evidence merge** | `27a1af4` (PR #58) |
| **HR3-B evidence merge** | `9d7ffaf` (PR #60) |
| **Date** | 2026-09-17 |
| **Baseline** | Main post-HR2 + VP-A evidence — HR2 **CLOSED**, VP strategy **APPROVED**, VP-A **APPROVED** (hard-fail ABP), VP-B **PARKED** for HR3 |
| **Harness grade (now)** | **~B** — doctor:ue truth, cold-clone CI, build-win64 path filters; no loud UE preflight, Windows exec tribal, branch protection advisory |
| **Swarm grade (now)** | **~B+** — gates, handoffs, DESKTOP evidence filed; re-verify and worker lane not closed-loop |
| **Author** | Conductor (HomeWorld) |
| **Prior HR track** | [13_HR2_HARNESS_REFINE.md](13_HR2_HARNESS_REFINE.md) — **CLOSED** |
| **Parallel product track** | [14_VP_VERIFY_POLISH.md](14_VP_VERIFY_POLISH.md) — **APPROVED**; VP-B **PARKED** pending HR3 |

---

## Gate

Lead **`APPROVE HR3 STRATEGY`** — **APPROVED** (Luke Thompson, 2026-09-17 ET).

Lead **`APPROVE HR3-A`** — **APPROVED** (Luke Thompson, 2026-09-17 ET). Evidence merge `27a1af4` (PR #58).

Lead **`APPROVE HR3-B`** — **APPROVED** (Luke Thompson, 2026-09-17 ET). Evidence merge `9d7ffaf` (PR #60).

**Next gate:** **`APPROVE HR3-D`** — DESKTOP evidence lane + re-verify.

**HR3-A APPROVED / COMPLETE**. **HR3-B APPROVED / COMPLETE**. **HR3-C DEFERRED / COMPLETE for track** — Lead **`APPROVE HR3-C deferred`**, 2026-09-17 ET (checklist PR #62; GitHub apply deferred). **HR3-D EVIDENCE FILED / AWAITING APPROVE HR3-D**. **VP-B PARKED** pending HR3 close (do not mark VP complete).

---

## Why HR3 (not more VP polish first)

HR2 delivered a **B- harness** (now **~B** after HR2-C merge) and unlocked product NP. VP strategy is **APPROVED**; VP-A evidence is **filed** with a **hard-fail** (ABP skeleton / empty mesh — no spawnable character). VP-B was **unlocked** but **PARKED** mid-fix so HR3 can land first — same pattern as pausing NP for HR.

Conductor blunt grade at VP-A close: **swarm B+ / harness B**. **A+** means **closed loops that fail loud before Lead sees them** — not another polish pass on symptoms.

| # | Residual | Impact | HR3 phase |
|---|----------|--------|-----------|
| 1 | **Windows agent exec reliability** — Shell on DESKTOP-21CT3H0 works for Conductor parent but not reliably for executors/workers (`machineId` routing tribal) | Swarm cannot own PIE/MCP without Lead-orchestrated Conductor | **HR3-A** |
| 2 | **No UE preflight that fails loud** — VP-A ran verb greps before catching ABP/empty-mesh class failures | Lead wastes phases on empty FORM: greps | **HR3-B** |
| 3 | **Branch protection advisory** — HR2-C documented required checks; GitHub UI not proven enforced | CI red is ignorable; C++ can merge on validate alone in practice | **HR3-C** |
| 4 | **DESKTOP evidence lane + no re-verify contract** — handoffs exist but board does not require re-prove of prior hard-fail greps after blocker fixes | Documented fail is forever; VP-B fix may not re-close VP-A loop | **HR3-D** |

**Explicitly OUT of HR3:** AnimGraph spike, rule-pack bloat, HR2 redo, Docs/07 reopen, combat/free-flight, product VP-C/D implementation, `.uasset`/`.umap` commits.

---

## ROI / grade targets

| Area | Now | After HR3 |
|------|-----|-----------|
| **Harness** | ~B | **A+** (preflight + Windows lane + branch protection) |
| **Swarm** | ~B+ | **A+** (DESKTOP lane + re-verify + handoff contract) |

**A+ definition:** Automation and swarm ops **fail non-zero / gate-block** on known blocker classes (MCP down, missing assets, ABP compile deps, map missing, PIE prerequisites) **before** verb greps or Lead phase review. DESKTOP work is **worker-routable** via one canonical lane. Branch protection is **real or explicitly deferred with ticket**. Blocker-fix phases **re-prove** prior hard-fail evidence before polish unlocks.

---

## Board status

| Track | Status |
|-------|--------|
| **Docs/11 HR-A…D + HR-B2** | **CLOSED** |
| **Product NP (Docs/11)** | **CLOSED** |
| **Docs/13 / HR2** | **CLOSED / COMPLETE** |
| **Docs/14 / VP strategy** | **APPROVED** |
| **VP-A** | **APPROVED** — hard-fail ABP evidence filed |
| **VP-B** | **PARKED** — pending HR3 (was unlocked mid-fix) |
| **Docs/15 / HR3 strategy** | **APPROVED** — Lead **`APPROVE HR3 STRATEGY`**, 2026-09-17 ET |
| **HR3-A** | **APPROVED / COMPLETE** — [handoffs/HR3_A_WINDOWS_EXEC.md](handoffs/HR3_A_WINDOWS_EXEC.md) |
| **HR3-B** | **APPROVED / COMPLETE** — [handoffs/HR3_B_UE_PREFLIGHT.md](handoffs/HR3_B_UE_PREFLIGHT.md) |
| **HR3-C** | **DEFERRED / COMPLETE for track** — [15c_HR3_C_BRANCH_PROTECTION.md](15c_HR3_C_BRANCH_PROTECTION.md), [handoffs/HR3_C_BRANCH_PROTECTION.md](handoffs/HR3_C_BRANCH_PROTECTION.md) — Lead skip 2026-09-17 ET; checklist PR #62 |
| **HR3-D** | **EVIDENCE FILED** — [handoffs/HR3_D_EVIDENCE_LANE.md](handoffs/HR3_D_EVIDENCE_LANE.md) |

---

## HR3 plan (Lead gates each phase)

Naming: **HR3-A … HR3-D** (Harness Refine 3 — A+ pass). Do **not** reuse HR2-*, NP-*, or VP-* phase ids for harness work.

### HR3-A — Windows agent exec reliability (was H1)

**Goal:** Executors/workers can reliably run Shell on **DESKTOP-21CT3H0** (`machineId`), not only Conductor parent. Document + prove one canonical Windows lane.

| Item | Spec |
|------|------|
| **Problem** | DESKTOP PIE/MCP work is tribal Conductor-only; cloud agents and spawned workers cannot route Shell to self-hosted worker hostname **DESKTOP-21CT3H0** consistently. |
| **Host** | Self-hosted worker **DESKTOP-21CT3H0** — see [WINDOWS_BRIDGE.md](../docs/Setup/WINDOWS_BRIDGE.md), [CLOUD_AGENT_PACKET.md](../swarm/CLOUD_AGENT_PACKET.md) |
| **Approach** | (a) Document canonical `machineId` / worker targeting for Cursor cloud agents and Conductor spawns; (b) prove worker → `machineId` → hostname **DESKTOP** with command output; (c) catalog known failure modes + fix or documented workaround that becomes the **happy path**. |
| **Evidence** | [handoffs/HR3_A_WINDOWS_EXEC.md](handoffs/HR3_A_WINDOWS_EXEC.md) — runbook, failure modes, proof excerpts |
| **Gate** | Lead **`APPROVE HR3-A`** — **APPROVED** (Luke Thompson, 2026-09-17 ET) |

**Why A+:** Without this, DESKTOP work is tribal Conductor-only — swarm can't own PIE/MCP.

**Done criteria:**

- [x] Runbook proves **parent** → `machineId` → hostname **DESKTOP-21CT3H0** — [handoffs/HR3_A_WINDOWS_EXEC.md](handoffs/HR3_A_WINDOWS_EXEC.md)
- [x] Known failure modes documented; happy path = **Conductor parent** (Task executors FAIL — do not assign DESKTOP Shell)
- [x] CLOUD_AGENT_PACKET / WINDOWS_BRIDGE cross-links updated
- [x] Handoff includes command output excerpts (hostname, machineId, tool availability)

---

### HR3-B — UE preflight that fails loud (was H2)

**Goal:** `npm run preflight:ue` (or extend `doctor:ue`) exits **non-zero** when: MCP 55557 down, required assets missing (BP mesh, ABP compile/skeleton deps), map missing, obvious PIE blockers. Catch the VP-A ABP/empty-mesh class of failure **before** verb greps.

| Item | Spec |
|------|------|
| **Problem** | VP-A DESKTOP run executed verb greps and filed hard-fail only after PIE — no automated gate for skeleton/mesh/map/MCP prerequisites. |
| **Checks (minimum)** | MCP port **55557** reachable; VS_MVP map path exists; character BP + ABP skeleton deps resolvable; bootstrap-critical assets present (script-defined list). |
| **Policy** | Document when to run: before VP PIE, before DESKTOP handoff PR, in CI where applicable (dry-run / skip-MCP mode on cloud). |
| **Evidence** | [handoffs/HR3_B_UE_PREFLIGHT.md](handoffs/HR3_B_UE_PREFLIGHT.md) — script + policy; DESKTOP dry-run exit codes (pass + deliberate fail cases) |
| **Gate** | Lead **`APPROVE HR3-B`** — **APPROVED** (Luke Thompson, 2026-09-17 ET) |

**Why A+:** Harness screams before Lead wastes a phase on empty FORM: greps.

**Done criteria:**

- [x] `npm run preflight:ue` (or documented equivalent) exits **non-zero** on each blocker class above — [handoffs/HR3_B_UE_PREFLIGHT.md](handoffs/HR3_B_UE_PREFLIGHT.md)
- [x] DESKTOP dry-run logs show pass + fail exit codes with clear messages — [handoffs/HR3_B_UE_PREFLIGHT.md](handoffs/HR3_B_UE_PREFLIGHT.md) § DESKTOP evidence
- [x] Policy doc: when required, who runs it (cloud vs DESKTOP owner) — [docs/Setup/UE_PREFLIGHT.md](../docs/Setup/UE_PREFLIGHT.md)
- [x] VP-A class failure (ABP skeleton) would have been caught by preflight — `EDITOR_ABP_SKELETON` + `--simulate-fail`

---

### HR3-C — Branch protection real (was H3)

**Goal:** Extend [CI_SETUP.md](../docs/Setup/CI_SETUP.md) with Lead checklist; document required checks **validate** + **python-lint** + **build-win64** (C++ paths per HR2-C). Evidence that settings were applied **OR** explicit Lead defer with ticket note — bot can't flip GitHub UI.

| Item | Spec |
|------|------|
| **Problem** | HR2-C made `build-win64` required in workflow/path filters; GitHub branch protection may still be advisory if Lead has not applied rules on `main`. |
| **Required checks** | `validate`, `python-lint`, `build-win64` (on C++ path changes per [13c_HR2_C_CI_GATE.md](13c_HR2_C_CI_GATE.md)) |
| **Deliverable** | [15c_HR3_C_BRANCH_PROTECTION.md](15c_HR3_C_BRANCH_PROTECTION.md), [handoffs/HR3_C_BRANCH_PROTECTION.md](handoffs/HR3_C_BRANCH_PROTECTION.md) + [CI_SETUP.md](../docs/Setup/CI_SETUP.md) updates |
| **Lead action** | Apply branch protection **OR** defer with dated ticket note in handoff (bot cannot configure GitHub UI) |
| **Gate** | Lead **`APPROVE HR3-C`** before implementation PR |

**Why A+:** CI stops being advisory.

**Done criteria:**

- [x] CI_SETUP Lead checklist complete (step-by-step for required checks)
- [x] Handoff shows evidence of applied settings **OR** explicit defer + ticket id — **DEFERRED** (Lead skip 2026-09-17 ET; GitHub apply not verified; checklist in CI_SETUP)
- [x] CI_POLICY and ci.yml remain aligned with HR2-C path list
- [x] Docs-only PRs still merge on validate alone (documented skipped-check behavior)

---

### HR3-D — DESKTOP evidence lane + auto re-verify (was S1)

**Goal:** Swarm ops: PHASE_BOARD names **cloud vs DESKTOP owner** per phase; handoff PR contract (host, greps, evidence path); after a blocker fix phase (e.g. VP-B), board requires **re-prove** of prior hard-fail greps (VP-A re-verify) before unlocking polish.

| Item | Spec |
|------|------|
| **Problem** | Evidence is filed once; blocker fixes do not automatically trigger re-verification; cloud vs DESKTOP ownership implicit. |
| **PHASE_BOARD** | Template column or row convention: owner **CLOUD** vs **DESKTOP** per active phase |
| **Handoff contract** | PR body / handoff md: host, grep prefixes, evidence path, pass/fail table |
| **Re-verify rule** | After VP-B (or any blocker-fix phase), **VP-A greps re-run** required before VP-C unlock |
| **Optional** | Thin routine/prompt for CI-fail wake — document only if routine cannot be created from repo |
| **Deliverable** | PHASE_BOARD template + [SWARM_OPS.md](../swarm/SWARM_OPS.md) / [CLOUD_AGENT_PACKET.md](../swarm/CLOUD_AGENT_PACKET.md) updates; [handoffs/HR3_D_EVIDENCE_LANE.md](handoffs/HR3_D_EVIDENCE_LANE.md) |
| **Gate** | Lead **`APPROVE HR3-D`** before implementation PR |

**Why A+:** Documented fail isn't forever; swarm re-closes the loop.

**Done criteria:**

- [x] PHASE_BOARD shows cloud vs DESKTOP owner for HR3 and VP phases — [swarm/PHASE_BOARD.md](../swarm/PHASE_BOARD.md) Host column
- [x] SWARM_OPS handoff contract documented (host, greps, evidence path) — [swarm/SWARM_OPS.md](../swarm/SWARM_OPS.md) §4a–4c
- [x] Re-verify rule: VP-B complete → VP-A greps re-prove before VP-C — [14_VP_VERIFY_POLISH.md](14_VP_VERIFY_POLISH.md) § Re-verify
- [x] Handoff doc includes example VP-A re-verify checklist — [handoffs/HR3_D_EVIDENCE_LANE.md](handoffs/HR3_D_EVIDENCE_LANE.md)

---

## Hard rules (every HR3 phase)

| Rule | Source |
|------|--------|
| **Docs/07 CLOSED** | Do not reopen vertical-slice sign-off |
| **FALLBACK FLIGHT armed** | No free-flight / flight HUD |
| **No `.uasset` / `.umap` commits** | Local Windows only |
| **Exactly 10 masters** | Docs/02 |
| **VP-B PARKED** | Resume VP-B after HR3 strategy (+ recommended HR3-B preflight) — do not mark VP track complete |
| **Lead APPROVE each HR3-* before implementation PR** | This doc |
| **Docs-only default for strategy + handoffs** | HR3-A/B/C/D implementation PRs may touch scripts, CI docs, swarm ops — no gameplay C++ unless explicitly scoped |
| **Stop for Lead APPROVE HR3 STRATEGY before HR3-A** | This PR is strategy only |

---

## Explicit OUT (HR3 track)

| Item | Reason |
|------|--------|
| AnimGraph spike | Product/content — not harness |
| Rule-pack bloat | HR-B2 already 15→3 always-on; no rules theater |
| HR2 redo | HR2 **CLOSED**; HR3 is A+ closure pass only |
| Docs/07 reopen | Lead **CLOSED** |
| Combat / free-flight | Placeholder policy; out of harness track |
| VP-C/D polish | **LOCKED** until VP-B + re-verify; HR3 enables, does not replace |
| Cloud UE / MCP on Linux VM | [WINDOWS_BRIDGE.md](../docs/Setup/WINDOWS_BRIDGE.md) — accepted architecture |
| `.uasset` commits | Local Windows only |

---

## Approval gate

| Step | Lead action | Unlocks |
|------|-------------|---------|
| 0 | **`APPROVE HR3 STRATEGY`** | HR3-A implementation planning |
| 1 | **`APPROVE HR3-A`** | HR3-A Windows exec reliability PR(s) |
| 2 | **`APPROVE HR3-B`** | HR3-B UE preflight PR(s) |
| 3 | **`APPROVE HR3-C`** | HR3-C branch protection PR(s) |
| 4 | **`APPROVE HR3-D`** | HR3-D evidence lane PR(s) |

Phases may run **sequentially** (recommended: A → B → C → D) or **parallel** after strategy approval if Lead directs — each phase still requires its own APPROVE before implementation.

```
Docs/15 / HR3 STRATEGY: APPROVED — Lead Luke Thompson, APPROVE HR3 STRATEGY, 2026-09-17 ET
HR3-A: APPROVED / COMPLETE — Lead APPROVE HR3-A, 2026-09-17 ET (evidence PR #58)
HR3-B: APPROVED / COMPLETE — Lead APPROVE HR3-B, 2026-09-17 ET (evidence PR #60)
HR3-C: DEFERRED / COMPLETE for track — Lead APPROVE HR3-C deferred, 2026-09-17 ET (PR #62)
HR3-D: EVIDENCE FILED — await APPROVE HR3-D
VP-B: PARKED pending HR3 close
```

---

## Relationship to prior docs

| Doc | Relationship |
|-----|--------------|
| [13_HR2_HARNESS_REFINE.md](13_HR2_HARNESS_REFINE.md) | HR2 **CLOSED** — HR3 is A+ pass on residual B/B+ friction |
| [14_VP_VERIFY_POLISH.md](14_VP_VERIFY_POLISH.md) | VP **APPROVED**; VP-A hard-fail drove HR3-B; VP-B **PARKED** |
| [11_SWARM_HARNESS_AUDIT.md](11_SWARM_HARNESS_AUDIT.md) | Baseline grades; HR3 targets A+ closed loops |
| [WINDOWS_BRIDGE.md](../docs/Setup/WINDOWS_BRIDGE.md) | DESKTOP-21CT3H0 — HR3-A canonical lane |
| [CI_SETUP.md](../docs/Setup/CI_SETUP.md) | HR3-C branch protection checklist |
| [13c_HR2_C_CI_GATE.md](13c_HR2_C_CI_GATE.md) | build-win64 path filters — HR3-C enforces on GitHub |
| [handoffs/VP_A_PIE.md](handoffs/VP_A_PIE.md) | VP-A hard-fail evidence — HR3-B must catch this class preflight |
| [swarm/SWARM_OPS.md](../swarm/SWARM_OPS.md) | HR3-D updates handoff + re-verify contract |

---

*Conductor prepared this file; HR3 strategy **APPROVED** 2026-09-17 ET — Lead **`APPROVE HR3 STRATEGY`**. HR3-A **APPROVED / COMPLETE**. HR3-B **APPROVED / COMPLETE**. HR3-C **DEFERRED / COMPLETE for track** — Lead **`APPROVE HR3-C deferred`**, 2026-09-17 ET (checklist PR #62; GitHub apply deferred). HR3-D **EVIDENCE FILED** — [handoffs/HR3_D_EVIDENCE_LANE.md](handoffs/HR3_D_EVIDENCE_LANE.md). VP-B **PARKED** until HR3-D close.*
