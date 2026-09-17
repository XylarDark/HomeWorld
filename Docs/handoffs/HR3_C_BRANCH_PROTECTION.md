# HR3-C Branch protection — Handoff

| Field | Value |
|-------|-------|
| **Phase** | HR3-C |
| **Status** | **PENDING LEAD APPLY** — GitHub branch protection not confirmed by agent |
| **Lead gate** | Apply settings → stamp **APPLIED** (or **DEFERRED** + ticket) → **`APPROVE HR3-C`** |
| **Spec** | [15c_HR3_C_BRANCH_PROTECTION.md](../15c_HR3_C_BRANCH_PROTECTION.md) |
| **Checklist** | [docs/Setup/CI_SETUP.md](../../docs/Setup/CI_SETUP.md) § Branch protection |

---

## Summary

HR3-C documents **real** required status checks on `main`. Cloud agent delivered the Lead checklist; **Lead must configure GitHub Settings** (bot cannot).

| Required check | Workflow | When |
|----------------|----------|------|
| **`validate`** | validate.yml | Every PR |
| **`python-lint`** | validate.yml | Every PR |
| **`build-win64`** | ci.yml | C++ path filters only ([CI_POLICY.md](../../docs/Setup/CI_POLICY.md)) |

**C++ paths:** `Source/**`, `**/*.Build.cs`, `*.uproject`, `Plugins/**/Source/**`, `.github/workflows/ci.yml`

**Docs-only PRs:** Enable GitHub **skipped-check** handling so merge is not blocked when `build-win64` did not run — see CI_SETUP § Lead checklist step 3.

**Waiver:** `Lead waiver: build-win64` or label `lead-waiver-build-win64` — [CI_POLICY.md](../../docs/Setup/CI_POLICY.md) § Lead waiver.

---

## Cloud agent verification (2026-09-17)

| Method | Result |
|--------|--------|
| `gh api repos/XylarDark/HomeWorld/branches/main/protection` | **HTTP 403** — `Resource not accessible by integration` |
| Interpretation | Agent token lacks admin scope; **protection state unknown** — Lead must confirm in UI or with admin PAT |

**Lead verify command (admin):**

```bash
gh api repos/XylarDark/HomeWorld/branches/main/protection \
  --jq '{required_checks: .required_status_checks.contexts, strict: .required_status_checks.strict, enforce_admins: .enforce_admins.enabled}'
```

- **404** or empty `contexts` → protection **not configured**
- **`contexts`** includes `validate`, `python-lint`, `build-win64` → HR3-C **APPLIED** (update this handoff + PHASE_BOARD)

---

## Lead action checklist (short)

1. Open **https://github.com/XylarDark/HomeWorld/settings/branches**
2. Rule for **`main`**: require PR + status checks **`validate`**, **`python-lint`**, **`build-win64`**
3. Enable **do not require skipped checks** (docs-only PRs)
4. Save; test docs-only PR + C++ PR merge behavior
5. Update this file: status **APPLIED** + date + optional API JSON excerpt
6. Comment **`APPROVE HR3-C`** on the HR3-C PR (or Conductor chat)

### If deferring

Set status **DEFERRED**, add ticket/issue link and reason (e.g. waiting for first green `build-win64` on runner). Do **not** mark PHASE_BOARD HR3-C as APPLIED.

---

## Stamp

| When | Who | Action |
|------|-----|--------|
| 2026-09-17 | Cloud Agent | Checklist + handoff filed; API **403** — **PENDING LEAD APPLY** |
| _pending_ | Lead | GitHub settings applied → **APPLIED** |
| _pending_ | Lead | **`APPROVE HR3-C`** |
