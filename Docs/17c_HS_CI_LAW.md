# Docs/17c — HS-C CI as law (branch protection)

| Field | Value |
|-------|-------|
| **Status** | **DEFERRED / CLOSED for track** — Lead **`ACCEPT HS-C DEFER`**, 2026-09-17 ET |
| **Date** | 2026-09-17 (ET) |
| **Author** | Conductor (HomeWorld) |
| **Parent plan** | [17_HS_AUDIT_STRATEGY.md](17_HS_AUDIT_STRATEGY.md) |
| **Prior gate** | [17b_HS_SWARM_OPS.md](17b_HS_SWARM_OPS.md) — Lead **`APPROVE HS-B`**, 2026-09-17 ET |
| **Baseline checklist** | [15c_HR3_C_BRANCH_PROTECTION.md](15c_HR3_C_BRANCH_PROTECTION.md) · [docs/Setup/CI_SETUP.md](../docs/Setup/CI_SETUP.md) § Branch protection · [docs/Setup/CI_POLICY.md](../docs/Setup/CI_POLICY.md) |

---

## Goal

Make **`main`** merge policy **real**: required status checks **`validate`**, **`python-lint`**, and **`build-win64`** (when C++ paths change per HR2-C) — **or** Lead stamps permanent **`ACCEPT HS-C DEFER`** with written risk (same honesty as HR3-C deferred, but closed for HS).

Cloud agents **cannot** flip GitHub branch protection. Lead applies in UI (or API with admin). Conductor verifies and stamps.

---

## Required checks (canonical)

| Check | Workflow | Every PR? |
|-------|----------|-----------|
| **`validate`** | validate.yml | Yes |
| **`python-lint`** | validate.yml | Yes |
| **`build-win64`** | ci.yml | C++ path filters only |

C++ filters: `Source/**`, `**/*.Build.cs`, `*.uproject`, `Plugins/**/Source/**`, `.github/workflows/ci.yml`.

---

## Lead paths

### A — Apply (preferred for A+ harness)

1. Open GitHub → **XylarDark/HomeWorld** → Settings → Branches → Branch protection for `main`.
2. Enable required status checks: `validate`, `python-lint`, `build-win64` (allow skip when path filter does not run build-win64 — follow CI_SETUP notes).
3. Reply in chat: **`HS-C APPLIED`** (or paste screenshot / settings confirm).
4. Conductor verifies (test PR or API read) → files handoff **APPLIED** → Lead **`APPROVE HS-C`**.

Full steps: [docs/Setup/CI_SETUP.md](../docs/Setup/CI_SETUP.md) § Branch protection · [15c_HR3_C_BRANCH_PROTECTION.md](15c_HR3_C_BRANCH_PROTECTION.md).

### B — Accept defer forever (HS close)

Reply **`ACCEPT HS-C DEFER`**. Conductor stamps permanent accept with risk: C++ can still merge on Ubuntu validate alone if humans ignore red checks. HS-C closes; HS-D unlocks.

---

## Risk if deferred

| Risk | Impact |
|------|--------|
| Required checks advisory only | Policy-honor merges; HR2-C path filters do not block alone |
| Docs-only still fine | validate/python-lint habit may remain |
| Harness grade ceiling | ~A not A+ on "CI as law" |

---

## Gate

Lead **`ACCEPT HS-C DEFER`** — **ACCEPTED** (Luke Thompson, 2026-09-17 ET).

**HS-C CLOSED for track** (permanent accept). Checklist remains in [CI_SETUP.md](../docs/Setup/CI_SETUP.md) / [15c](15c_HR3_C_BRANCH_PROTECTION.md) if Lead later applies. **HS-D UNLOCKED**.

### Written risk (accepted)

| Risk | Impact |
|------|--------|
| Required checks advisory only | Policy-honor merges; C++ can merge on Ubuntu `validate` alone if humans ignore red |
| Harness grade ceiling | ~A — not A+ on "CI as law" until GitHub settings applied |

---

*HS-C **DEFERRED / CLOSED** — Lead **`ACCEPT HS-C DEFER`**, 2026-09-17 ET.*
