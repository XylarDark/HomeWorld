# Docs/15c — HR3-C Branch protection (real checks on `main`)

| Field | Value |
|-------|-------|
| **Status** | **DEFERRED / COMPLETE for track** — Lead skip 2026-09-17 ET |
| **Date** | 2026-09-17 |
| **Author** | Cloud Agent (HR3-C) |
| **Strategy** | [15_HR3_A_PLUS.md](15_HR3_A_PLUS.md) — Lead **`APPROVE HR3 STRATEGY`**, 2026-09-17 ET |
| **Prior gate** | HR2-C **APPROVED** — [13c_HR2_C_CI_GATE.md](13c_HR2_C_CI_GATE.md); HR3-B evidence filed — [handoffs/HR3_B_UE_PREFLIGHT.md](handoffs/HR3_B_UE_PREFLIGHT.md) |
| **Related** | [docs/Setup/CI_SETUP.md](../docs/Setup/CI_SETUP.md) § Branch protection · [docs/Setup/CI_POLICY.md](../docs/Setup/CI_POLICY.md) |

---

## Gate

**DEFERRED** — Lead Luke Thompson typed **skip** on UI/API verify (2026-09-17 ET). Treat as **`APPROVE HR3-C deferred`**: checklist delivered (PR #62); GitHub apply not verified; checklist remains in [CI_SETUP.md](../docs/Setup/CI_SETUP.md) for later apply.

Cloud agents **cannot** enable branch protection. Checklist and verification notes filed; **do not block HR3-D**.

**Next gate:** Lead **`APPROVE HR3-D`** before HR3-D implementation PR. Re-apply branch protection in GitHub when ready → stamp handoff **APPLIED**.

---

## Goal

Make **`main`** merge policy **real** in GitHub: required status checks **`validate`**, **`python-lint`**, and **`build-win64`** (when C++ paths change per HR2-C), with docs-only PR behavior documented.

HR2-C wired workflow path filters and policy text; HR3-C makes the **GitHub settings steps** explicit so Lead can apply and verify without guessing.

---

## Required checks (canonical)

| Check | Workflow | Every PR? | Notes |
|-------|----------|-----------|-------|
| **`validate`** | [validate.yml](../.github/workflows/validate.yml) | Yes | Ubuntu hosted |
| **`python-lint`** | [validate.yml](../.github/workflows/validate.yml) | Yes | Ubuntu hosted; warnings-only ruff |
| **`build-win64`** | [ci.yml](../.github/workflows/ci.yml) | C++ paths only | Self-hosted `windows`/`ue57` — DESKTOP-21CT3H0 |

**C++ path filters** (sync with [CI_POLICY.md](../docs/Setup/CI_POLICY.md) and [13c_HR2_C_CI_GATE.md](13c_HR2_C_CI_GATE.md)):

- `Source/**`
- `**/*.Build.cs`
- `*.uproject`
- `Plugins/**/Source/**`
- `.github/workflows/ci.yml`

---

## Deliverables

| # | Item | Path |
|---|------|------|
| 1 | Step-by-step Lead checklist | [docs/Setup/CI_SETUP.md](../docs/Setup/CI_SETUP.md) § Branch protection |
| 2 | Policy alignment (path filters, waiver) | [docs/Setup/CI_POLICY.md](../docs/Setup/CI_POLICY.md) |
| 3 | Handoff + verification status | [handoffs/HR3_C_BRANCH_PROTECTION.md](handoffs/HR3_C_BRANCH_PROTECTION.md) |
| 4 | PHASE_BOARD row | [swarm/PHASE_BOARD.md](../swarm/PHASE_BOARD.md) |

**Not in scope:** Changing GitHub org/repo settings from the cloud VM; C++ gameplay; bootstrap dry-run (VP-D PA-05).

---

## Cloud agent verification (what we could prove)

| Check | Result | Notes |
|-------|--------|-------|
| `gh api …/branches/main/protection` | **403** — Resource not accessible by integration | Cloud agent token is not repo admin; **cannot confirm** protection enabled |
| Workflow job names | **`validate`**, **`python-lint`**, **`build-win64`** | Match checklist in CI_SETUP |
| Path filters in `ci.yml` | Match CI_POLICY / 13c table | HR2-C sync unchanged |
| Docs-only PR (this PR) | **`validate`** + **`python-lint`** only | `ci.yml` skipped — expected |

**Do not** mark HR3-C **APPLIED** until Lead API or UI confirms required checks on `main`.

---

## Done criteria (HR3-C)

- [x] CI_SETUP Lead checklist: Settings → Branches → `main` → required checks
- [x] Check names and C++ path list aligned with CI_POLICY and HR2-C
- [x] Handoff filed with **PENDING LEAD APPLY** and API 403 documented
- [x] Lead confirms in handoff — **DEFERRED** (skip 2026-09-17 ET; GitHub apply not verified)
- [x] Lead **`APPROVE HR3-C deferred`** — complete for track; unlock HR3-D
- [ ] Lead applies branch protection in GitHub UI (when ready) → stamp **APPLIED**

---

## Relationship to VP-D

[14_VP_VERIFY_POLISH.md](14_VP_VERIFY_POLISH.md) VP-D includes bootstrap dry-run (PA-05) **and** branch protection docs. **HR3-C** completes the **branch protection documentation** slice; VP-D bootstrap evidence remains separate (DESKTOP / Lead gate).

---

*HR3-C **DEFERRED / COMPLETE for track** — Lead **`APPROVE HR3-C deferred`**, 2026-09-17 ET. Checklist PR #62; GitHub apply deferred. HR3-D unlocked. Do not claim protection enabled without GitHub confirmation.*
