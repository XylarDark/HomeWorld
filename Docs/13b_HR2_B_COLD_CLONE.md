# Docs/13b — HR2-B Cold-Clone Submodule Onboarding

| Field | Value |
|-------|-------|
| **Status** | **APPROVED** — Lead Luke Thompson, **`APPROVE HR2-B`**, 2026-09-17 ET |
| **Date** | 2026-09-17 |
| **Author** | Cloud Agent (HR2-B) |
| **Strategy** | [13_HR2_HARNESS_REFINE.md](13_HR2_HARNESS_REFINE.md) — Lead **`APPROVE HR2 STRATEGY`**, 2026-09-17 ET |
| **Prior gate** | HR2-A **APPROVED** — Lead **`APPROVE HR2-A`**, 2026-09-17 ET |

---

## Gate

**APPROVED** — Lead Luke Thompson typed **`APPROVE HR2-B`** on 2026-09-17 ET. HR2-C unlocked.

---

## Goal

One proven cold-clone path: empty `DevEnvTemplate/` → submodule init → `doctor:build` → `doctor:ue`, with CI enforcing gitlink ↔ documented pin hygiene.

---

## Canonical pin (machine-readable)

| Field | Value |
|-------|-------|
| **Registry** | [config/devenv-template-pin.json](../config/devenv-template-pin.json) |
| **Full SHA** | `2efd7569a698e73a04279feaebaae1eb55c4e1c0` |
| **Short SHA** | `2efd756` |
| **Remote** | `https://github.com/XylarDark/DevEnvTemplate.git` |
| **Branch** | `master` |

Verify locally:

```bash
git ls-tree HEAD DevEnvTemplate          # commit must match pin JSON
git submodule status DevEnvTemplate      # prefix space = init OK; - = not init
```

**Pin bump policy:** When changing the gitlink, update **all** of: `.gitmodules` (if URL changes), `config/devenv-template-pin.json`, [docs/Setup/CURSOR_DEV.md](../docs/Setup/CURSOR_DEV.md), and this doc. CI fails if gitlink ≠ registry SHA.

---

## Idempotent cold-clone runbook

From repo root after `git clone` (no prior submodule init):

```bash
git submodule update --init --recursive DevEnvTemplate
npm run doctor:build    # once: install + build nested DevEnvTemplate
npm run doctor:ue       # UE host: exit 0 when only DOCTOR_POLICY declines remain
```

Re-runs are safe: submodule init is idempotent; `doctor:build` is a no-op when `dist/` is current.

**Node 22 `EBADENGINE`:** Accepted decline — see [DOCTOR_POLICY.md](../docs/Setup/DOCTOR_POLICY.md).

**Do not** vendor a second checkout under `.devenv/` — [AGENTS.md](../AGENTS.md) accepted decline.

Human-facing copy: [docs/Setup/CURSOR_DEV.md](../docs/Setup/CURSOR_DEV.md) § Init runbook.

---

## CI guard

[validate.yml](../.github/workflows/validate.yml) step **DevEnvTemplate pin + submodule (HR2-B)** runs [scripts/verify-devenv-submodule.sh](../scripts/verify-devenv-submodule.sh):

1. Gitlink SHA at `HEAD` must match `config/devenv-template-pin.json`.
2. `docs/Setup/CURSOR_DEV.md` must cite the full SHA.
3. If `DevEnvTemplate/` is empty, runs `git submodule update --init --recursive` (cold-clone simulation).
4. Checked-out submodule HEAD must match documented pin.

Fails PR when pointer drifts without registry/doc update. Does **not** run full `doctor:build` in CI (too slow); cold-clone evidence below covers that path.

---

## Deliverables

| # | Item | Path |
|---|------|------|
| 1 | Pin registry | `config/devenv-template-pin.json` |
| 2 | CI verify script | `scripts/verify-devenv-submodule.sh` |
| 3 | validate.yml step | `.github/workflows/validate.yml` |
| 4 | Runbook (human) | [docs/Setup/CURSOR_DEV.md](../docs/Setup/CURSOR_DEV.md) |
| 5 | Onboarding pointer | [AGENTS.md](../AGENTS.md) § Dev environment setup |
| 6 | CI policy note | [docs/Setup/CI_POLICY.md](../docs/Setup/CI_POLICY.md) |

**Not in scope:** Vendoring template; second submodule; pin bump for theater; TS/ESLint; HR2-C.

---

## Evidence — fresh-clone dry-run (cloud VM)

Host: Linux cloud agent VM, 2026-09-17, main @ HR2-B branch, Node 22. **Starting state:** `DevEnvTemplate/` empty (default post-clone).

| Step | Command | Exit | Notes |
|------|---------|------|-------|
| 0 | `ls DevEnvTemplate/` | — | Empty directory (only `.` / `..`) |
| 1 | `bash scripts/verify-devenv-submodule.sh` | **0** | Gitlink matched pin; submodule init; checkout `2efd756` |
| 2 | `npm run doctor:build` | **0** | `tsc --build` OK; 177 packages |
| 3 | `npm run doctor:ue` | **0** | 5 accepted declines; raw doctor exit 1 |

### verify-devenv-submodule.sh (excerpt)

```
Gitlink matches documented pin: 2efd756 (2efd7569a698e73a04279feaebaae1eb55c4e1c0)
CURSOR_DEV.md cites documented pin
DevEnvTemplate/ empty — running submodule init (cold-clone path)
Submodule path 'DevEnvTemplate': checked out '2efd7569a698e73a04279feaebaae1eb55c4e1c0'
Submodule checkout matches pin: 2efd7569a698e73a04279feaebaae1eb55c4e1c0
DevEnvTemplate submodule verification OK
```

### doctor:ue (tail)

```
--- doctor:ue (UE host) ---
Raw doctor exit: 1
Critical total: 5
Accepted declines (non-fatal): 5
doctor:ue exit: 0 (only accepted declines remain)
```

**Windows:** Same runbook on DESKTOP-21CT3H0; submodule may ship prebuilt `dist/` so `doctor:build` can be skipped when CLI already present.

---

## Done criteria (HR2-B)

- [x] Cold clone → documented commands → `doctor:build` succeeds on cloud VM
- [x] CI fails when gitlink ≠ documented pin (verify script)
- [x] CI inits empty submodule (cold-clone path in validate)
- [x] Runbook copy-paste complete in CURSOR_DEV + AGENTS.md
- [x] No manual "ask in chat" steps
- [x] Lead **`APPROVE HR2-B`** → unlock HR2-C

---

*HR2-B **APPROVED** 2026-09-17 ET — HR2-C unlocked.*
