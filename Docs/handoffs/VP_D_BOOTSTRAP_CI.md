# VP-D Bootstrap & Branch Protection — Handoff

| Field | Value |
|-------|-------|
| **Phase** | VP-D |
| **Status** | **DRAFT IN PROGRESS** — unlocked after Lead **`APPROVE VP-C`**, 2026-09-17 ET |
| **Lead gate** | **`APPROVE VP-D`** before VP-D implementation PR merge / COMPLETE |
| **Spec** | [14_VP_VERIFY_POLISH.md](../14_VP_VERIFY_POLISH.md) § VP-D |
| **Baseline** | Main post–VP-C stamp (polish PR #69 @ `f88ece5`) |

---

## Summary

Prove fresh-clone → script chain on Windows (PA-05); document GitHub branch protection checks Lead must enable (HR3-C carry-forward). **Do not mark VP track CLOSED** until Lead **`APPROVE VP-D`**.

| Workstream | Residual | Owner |
|------------|----------|-------|
| **Bootstrap dry-run** | PA-05 | **DESKTOP** (Conductor parent) + **CLOUD** (runbook/docs) |
| **Branch protection checklist** | HR3-C carry-forward | **Lead** (GitHub Settings) + **CLOUD** (doc cross-links) |

---

## Scope (from Docs/14 § VP-D)

### PA-05 — Bootstrap dry-run (DESKTOP evidence TBD)

Cold or clean clone path on **DESKTOP-21CT3H0**:

1. **Clone** — fresh or clean working tree (no stale `Saved/` / local `.uasset` assumptions)
2. **Submodule init** — [13b_HR2_B_COLD_CLONE.md](../13b_HR2_B_COLD_CLONE.md): `git submodule update --init --recursive DevEnvTemplate`
3. **Doctor** — `npm run doctor:ue` (UE host signal; see [13a_HR2_A_HANDOFF.md](../13a_HR2_A_HANDOFF.md))
4. **Editor** — open `HomeWorld.uproject`; confirm Enhanced Input via `Content/Python/init_unreal.py`
5. **Bootstrap** — `bootstrap_project.py` (or documented chain: `batch_import_asset_creation.py` + `place_vs_mvp_markers.py` per [AGENTS.md](../../AGENTS.md))
6. **Idempotent re-run** — second pass must not duplicate actors/assets; log create/reuse/skip lines

**Evidence deliverable:** log excerpts in this handoff (timestamp, host, UE version, exit codes). **Conductor owns DESKTOP execution** — no invented logs in cloud stamp PRs.

| Step | Expected signal | Evidence |
|------|-----------------|----------|
| Submodule init | `git submodule status` — no `-` prefix on `DevEnvTemplate` | _TBD — DESKTOP_ |
| `npm run doctor:ue` | exit **0** or documented accepted warn | _TBD — DESKTOP_ |
| Editor open | project loads; no fatal plugin errors | _TBD — DESKTOP_ |
| `bootstrap_project.py` | idempotent success; VS_MVP markers present | _TBD — DESKTOP_ |
| Re-run bootstrap | skip/reuse logs; no duplicates | _TBD — DESKTOP_ |

If any step cannot be automated, log gap → [docs/Automation/AUTOMATION_GAPS.md](../../docs/Automation/AUTOMATION_GAPS.md).

### Branch protection — HR3-C **DEFERRED** unless Lead confirms apply

VP-D documents the checklist; **does not fake APPLIED**. HR3-C branch protection remains **DEFERRED** until Lead configures GitHub and confirms.

| Doc | Role |
|-----|------|
| [docs/Setup/CI_SETUP.md](../../docs/Setup/CI_SETUP.md) | Lead step-by-step — required checks `validate`, `python-lint`, `build-win64` on `main` |
| [15c_HR3_C_BRANCH_PROTECTION.md](../15c_HR3_C_BRANCH_PROTECTION.md) | HR3-C spec |
| [handoffs/HR3_C_BRANCH_PROTECTION.md](HR3_C_BRANCH_PROTECTION.md) | Handoff — status **DEFERRED** (Lead skip 2026-09-17 ET) |

**Required checks (when Lead applies):**

| Check | Workflow | When |
|-------|----------|------|
| **`validate`** | validate.yml | Every PR |
| **`python-lint`** | validate.yml | Every PR |
| **`build-win64`** | ci.yml | C++ path filters only |

Lead verify (admin PAT):

```bash
gh api repos/XylarDark/HomeWorld/branches/main/protection \
  --jq '{required_checks: .required_status_checks.contexts, strict: .required_status_checks.strict}'
```

- Empty `contexts` or **404** → protection **not configured** (HR3-C still **DEFERRED**)
- `contexts` includes all three checks → update [HR3_C_BRANCH_PROTECTION.md](HR3_C_BRANCH_PROTECTION.md) to **APPLIED** (Lead confirmation only)

---

## Done criteria (Docs/14)

- [ ] Fresh-clone dry-run log shows bootstrap chain success on DESKTOP or documented gap → [AUTOMATION_GAPS.md](../../docs/Automation/AUTOMATION_GAPS.md)
- [ ] CI_SETUP lists required status checks and Lead steps for `main` protection (cross-linked — already in HR3-C PR #62)
- [ ] Lead confirms branch protection configured (note in handoff — **no bot access**; do not claim **APPLIED** without Lead confirmation)

---

## DESKTOP evidence

_Not filed — Conductor owns DESKTOP bootstrap dry-run. No invented evidence in this stub._

---

## Hard rules

- **Docs/07 CLOSED** — no reopen
- **No `.uasset` / `.umap` commits**
- **Do not mark VP track CLOSED** until Lead **`APPROVE VP-D`**
- **HR3-C branch protection:** document checklist only; status **DEFERRED** unless Lead confirms apply in GitHub UI

---

*VP-D handoff stub — **DRAFT IN PROGRESS**. Unlocked by Lead **`APPROVE VP-C`**, 2026-09-17 ET. Next gate: Lead **`APPROVE VP-D`**.*
