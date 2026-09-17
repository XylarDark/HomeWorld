# Docs/13 — Harness Refine 2 (HR2) Strategy

| Field | Value |
|-------|-------|
| **Status** | **APPROVED** — Lead Luke Thompson, **`APPROVE HR2 STRATEGY`**, 2026-09-17 ET |
| **Date** | 2026-09-17 |
| **Strategy merge** | `d10e7b575e25d87c8aea55ee6bf314b8288e38d2` (PR #47) |
| **Baseline** | Main @ `54193ac` — post-NP audit + senior harness review |
| **Harness grade** | **B- (~3.8/5)** — past blocking threshold (HR-A…D + HR-B2 complete) |
| **Author** | Conductor (HomeWorld) |
| **Prior HR track** | [11_SWARM_HARNESS_REFINE.md](11_SWARM_HARNESS_REFINE.md) — **CLOSED** |
| **Audit input** | [11_SWARM_HARNESS_AUDIT.md](11_SWARM_HARNESS_AUDIT.md) (re-grade after HR-A…D) |

---

## Why HR2 (not another HR pass)

HR-A…D + HR-B2 delivered a **B- harness** and unlocked product NP. Senior harness review at `54193ac` confirms **no full HR redo** — only **high-ROI residual friction** remains:

| # | Residual | Impact |
|---|----------|--------|
| 1 | **Doctor truthfulness** — `npm run doctor` exits **1** with **5 criticals** on UE host; agents/humans must read [DOCTOR_POLICY.md](../docs/Setup/DOCTOR_POLICY.md) every time to know red is policy, not breakage. Rule budget critical persists despite **3** `alwaysApply: true` rules (doctor may count all **34** `.mdc` files). | False-negative signal; automation cannot trust exit code |
| 2 | **Cold-clone submodule** — empty `DevEnvTemplate/` without `git submodule update --init`; pin `2efd756` documented but not CI-enforced | Onboarding tribal knowledge; cloud snapshot fragility |
| 3 | **C++ CI gate (optional but recommended)** — `build-win64` is **recommended**, not **required**, on C++ path changes ([CI_POLICY.md](../docs/Setup/CI_POLICY.md)) | C++ can merge on Ubuntu `validate` alone without Windows build or Lead waiver |

**Explicitly OUT of HR2:** rules-diet theater, TS/ESLint/Jest to silence doctor, full HR-A…D redo, cloud UE fantasy (Editor/MCP on Linux VM).

---

## Board status

| Track | Status |
|-------|--------|
| **Docs/11 HR-A…D + HR-B2** | **CLOSED** |
| **Product NP (Docs/11_NEXT_PHASE_STRATEGY)** | **CLOSED** — NP work complete at audit baseline |
| **Docs/13 / HR2 strategy** | **APPROVED** — Lead **`APPROVE HR2 STRATEGY`**, 2026-09-17 ET |
| **HR2-A** | **APPROVED** — [13a_HR2_A_HANDOFF.md](13a_HR2_A_HANDOFF.md); Lead **`APPROVE HR2-A`**, 2026-09-17 ET |
| **HR2-B** | **IN PROGRESS** — [13b_HR2_B_COLD_CLONE.md](13b_HR2_B_COLD_CLONE.md); await Lead **`APPROVE HR2-B`** |
| **HR2-C** | **LOCKED** — blocked until **`APPROVE HR2-B`** |

---

## HR2 plan (Lead gates each phase)

Naming: **HR2-A … HR2-C** (Harness Refine 2). Do **not** reuse HR-A…D or NP phase ids.

### HR2-A — Doctor signal (UE host truthfulness)

**Goal:** Make `npm run doctor` exit code **meaningful** for the UE game host — agents and humans trust green/red without reading DOCTOR_POLICY every run.

| Item | Spec |
|------|------|
| **Problem** | Doctor scores against Node/TS app profile; 5 accepted-decline criticals (TS, ESLint, JS tests, secrets scanner, rule budget) force exit **1** despite **77/100** score and honest policy in [DOCTOR_POLICY.md](../docs/Setup/DOCTOR_POLICY.md). |
| **Approach (pick one or combine — implementation PR decides after gate)** | (a) **Host override config** — wire DevEnvTemplate doctor to read HomeWorld host profile that suppresses or downgrades accepted declines; (b) **`doctor:ue` script** — wrapper that runs doctor, maps known critical IDs to policy table, exits **0** when only accepted declines remain; (c) **Automate decline registry** — single machine-readable list (JSON or doctor config) synced from DOCTOR_POLICY so suppression is not hand-maintained in two places. |
| **Rule budget** | Investigate doctor count vs actual `alwaysApply: true` (3 vs 34 `.mdc`); fix miscount if template bug, or document + suppress if accepted. **No** mass rule delete to game the score. |
| **Evidence** | Before/after matrix: Lead **Windows DESKTOP** + **cloud VM** — `npm run doctor` exit code, critical list, score; excerpt in handoff doc. |
| **Deliverable** | `Docs/13a_HR2_A_DOCTOR_SIGNAL.md` + PR touching doctor config / wrapper / DOCTOR_POLICY cross-links |
| **Gate** | Lead **`APPROVE HR2-A`** before implementation PR |

**In scope:** Doctor exit semantics, host profile, accepted-decline automation, AGENTS.md / CURSOR_DEV.md command table update (`npm run doctor` vs `npm run doctor:ue`).

**Out of scope:** Adding TypeScript, ESLint, or Jest to satisfy template defaults; retiring all always-applied rules in one PR; bumping DevEnvTemplate pin solely for doctor (pin work is HR2-B if needed).

**Done criteria:**

- [ ] `npm run doctor` (or documented `doctor:ue`) exits **0** on Windows + cloud when only [DOCTOR_POLICY.md](../docs/Setup/DOCTOR_POLICY.md) accepted declines remain
- [ ] Exit **non-zero** still occurs for **new** criticals not in decline registry
- [ ] DOCTOR_POLICY and doctor config stay in sync (single source or explicit sync step)
- [ ] Handoff includes before/after command output excerpts

---

### HR2-B — Cold-clone submodule onboarding

**Goal:** One proven cold-clone path — `git submodule update --init`, pin SHA documented, optional CI guard — so `npm run doctor:build` works without tribal knowledge.

| Item | Spec |
|------|------|
| **Problem** | Fresh clone leaves empty `DevEnvTemplate/`; doctor fails until manual submodule init. Pin `2efd756` is in [CURSOR_DEV.md](../docs/Setup/CURSOR_DEV.md) but not enforced in CI. |
| **Pin hygiene** | Document canonical gitlink SHA in CURSOR_DEV + this strategy; optional bump only if HR2-B implementation needs template feature (not HR2-A doctor theater). |
| **One proven path** | Idempotent runbook: clone → `git submodule update --init --recursive DevEnvTemplate` → `npm run doctor:build` → `npm run doctor` (or `doctor:ue` post HR2-A). |
| **CI guard (optional)** | validate job step: `DevEnvTemplate/` non-empty; gitlink matches recorded SHA (or submodule status clean). Fails PR if submodule pointer drift without doc update. |
| **Evidence** | Fresh-clone dry-run log (cloud agent or CI artifact): empty → init → doctor:build success. |
| **Deliverable** | `Docs/13b_HR2_B_COLD_CLONE.md` + PR (validate.yml step, CURSOR_DEV runbook, AGENTS.md onboarding line) |
| **Gate** | Lead **`APPROVE HR2-B`** before implementation PR |

**In scope:** Submodule init runbook, pin documentation, CI non-empty / gitlink check, bootstrap pointer in AGENTS.md Setup section.

**Out of scope:** Vendoring template under `.devenv/` (accepted decline); second submodule beyond DevEnvTemplate; full environment snapshot rebuild.

**Done criteria:**

- [ ] Cold clone (no prior submodule) → documented commands → `doctor:build` succeeds on cloud VM
- [ ] CI fails or warns when `DevEnvTemplate/` is empty or gitlink ≠ documented pin without accompanying doc change
- [ ] No manual "ask in chat" steps — runbook is copy-paste complete

---

### HR2-C — C++ CI gate (build-win64 required)

**Goal:** PRs touching C++ paths **require** green `build-win64` (self-hosted Windows) or explicit Lead waiver — docs-only PRs stay validate-only.

| Item | Spec |
|------|------|
| **Problem** | [CI_POLICY.md](../docs/Setup/CI_POLICY.md) marks `build-win64` **recommended**; cloud agents cannot Safe-Build; C++ can merge on Ubuntu validate alone. |
| **Path filters** | Trigger required `build-win64` when PR changes: `Source/**`, `**/*.Build.cs`, `*.uproject`, `Plugins/**/Source/**` (if tracked). |
| **Policy update** | CI_POLICY.md: **Required** for C++ paths; waiver: Lead label or documented override in PR body (`Lead waiver: build-win64`). |
| **Workflow** | `.github/workflows/ci.yml` — path filters + required check for protected branch (or branch rule doc if GitHub settings out of repo). |
| **Docs-only** | No change — `validate.yml` only. |
| **Deliverable** | `Docs/13c_HR2_C_CI_GATE.md` + PR (ci.yml, CI_POLICY.md, optional branch protection note in CI_SETUP.md) |
| **Gate** | Lead **`APPROVE HR2-C`** before implementation PR |

**In scope:** ci.yml path filters, CI_POLICY required vs recommended table, waiver documentation, README/AGENTS pointer.

**Out of scope:** UE on GitHub-hosted Ubuntu; making validate run Safe-Build; requiring build-win64 for Python-only or docs-only PRs.

**Done criteria:**

- [ ] C++ touch PR without green `build-win64` is blocked (CI red or policy-enforced) unless Lead waiver documented
- [ ] Docs-only PR merges on validate alone
- [ ] CI_POLICY and ci.yml agree on path list
- [ ] Cloud agent packet updated: C++ PR expects Windows runner or waiver

---

## Hard rules (every HR2 phase)

| Rule | Source |
|------|--------|
| **Docs/07 CLOSED** | Do not reopen vertical-slice sign-off |
| **FALLBACK FLIGHT armed** | No free-flight / flight HUD |
| **No `.uasset` / `.umap` commits** | Local Windows only |
| **Exactly 10 masters** | Docs/02 |
| **No product VP/NP work in HR2 track** | Harness only — product NP CLOSED at HR2 entry |
| **Lead APPROVE each HR2-* before implementation PR** | This doc |
| **Docs-only default for strategy + handoffs** | HR2-A/B/C implementation PRs may touch doctor config, validate.yml, ci.yml, package.json scripts — no gameplay C++ unless explicitly part of HR2-C workflow files only |

---

## Explicit OUT (HR2 track)

| Item | Reason |
|------|--------|
| Another rules-diet theater | HR-B2 already 15→3 always-on; doctor may miscount — fix signal, not mass delete |
| TS / ESLint / Jest to silence doctor | Accepted decline — UE host is not Node app ([DOCTOR_POLICY.md](../docs/Setup/DOCTOR_POLICY.md)) |
| Full HR-A…D redo | CLOSED at B-; HR2 is surgical residual only |
| Cloud UE / MCP on Linux VM | [WINDOWS_BRIDGE.md](../docs/Setup/WINDOWS_BRIDGE.md) — accepted architecture |
| Product NP-A…E implementation | NP CLOSED; HR2 does not reopen lookdev/form/SYS verbs |
| Nanite/Lumen beauty gates | Off-slice |
| Reopening Docs/07 for free-flight | Lead CLOSED |

---

## Approval gate

| Step | Lead action | Unlocks |
|------|-------------|---------|
| 0 | **`APPROVE HR2 STRATEGY`** | HR2-A implementation planning |
| 1 | **`APPROVE HR2-A`** | HR2-A doctor signal PR(s) |
| 2 | **`APPROVE HR2-B`** | HR2-B cold-clone PR(s) |
| 3 | **`APPROVE HR2-C`** | HR2-C CI gate PR(s) |

Phases may run **sequentially** (recommended: A → B → C) or **parallel** after strategy approval if Lead directs — each phase still requires its own APPROVE before implementation.

```
Docs/13 / HR2 STRATEGY: APPROVED — Lead Luke Thompson, APPROVE HR2 STRATEGY, 2026-09-17 ET
HR2-A: APPROVED — Lead Luke Thompson, APPROVE HR2-A, 2026-09-17 ET
HR2-B: IN PROGRESS — cold-clone runbook + CI guard; await APPROVE HR2-B
HR2-C: LOCKED
```

---

## Relationship to prior docs

| Doc | Relationship |
|-----|--------------|
| [11_SWARM_HARNESS_REFINE.md](11_SWARM_HARNESS_REFINE.md) | HR1 track **CLOSED** — HR2 is post-NP residual pass only |
| [11_SWARM_HARNESS_AUDIT.md](11_SWARM_HARNESS_AUDIT.md) | B- (3.8) harness baseline; HR2 targets listed residual rows |
| [11e_HR_B2_HANDOFF.md](11e_HR_B2_HANDOFF.md) | Doctor declines + rules 15→3 — HR2-A extends with exit-code truth |
| [DOCTOR_POLICY.md](../docs/Setup/DOCTOR_POLICY.md) | Accepted declines — HR2-A makes machine-enforceable |
| [CURSOR_DEV.md](../docs/Setup/CURSOR_DEV.md) | Pin `2efd756`, init runbook — HR2-B adds CI proof |
| [CI_POLICY.md](../docs/Setup/CI_POLICY.md) | build-win64 recommended — HR2-C promotes to required on C++ paths |
| [11_NEXT_PHASE_STRATEGY.md](11_NEXT_PHASE_STRATEGY.md) | Product NP — **CLOSED**; HR2 does not replace NP handoffs |

---

*Conductor prepared this file; HR2 strategy **APPROVED** 2026-09-17 ET. HR2-A **APPROVED** 2026-09-17 ET. HR2-B in progress — **stop for Lead `APPROVE HR2-B`** before HR2-C.*
