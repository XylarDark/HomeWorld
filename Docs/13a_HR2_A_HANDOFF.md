# Docs/13a — HR2-A Doctor Signal Handoff

| Field | Value |
|-------|-------|
| **Status** | **COMPLETE — awaiting Lead `APPROVE HR2-A`** |
| **Date** | 2026-09-17 |
| **Author** | Cloud Agent (HR2-A) |
| **Strategy** | [13_HR2_HARNESS_REFINE.md](13_HR2_HARNESS_REFINE.md) — Lead **`APPROVE HR2 STRATEGY`**, 2026-09-17 ET |
| **Strategy merge SHA** | `d10e7b575e25d87c8aea55ee6bf314b8288e38d2` (PR #47) |

---

## Gate

**Awaiting** Lead **`APPROVE HR2-A`** — do **not** start HR2-B until approved.

---

## Goal

Make `npm run doctor:ue` exit **0** on the UE game host when only [DOCTOR_POLICY](../docs/Setup/DOCTOR_POLICY.md) accepted declines remain; exit **1** when any new critical appears.

---

## Deliverables

| # | Item | Path |
|---|------|------|
| 1 | UE doctor wrapper | `scripts/doctor-ue.js` |
| 2 | Decline registry (machine-readable) | `config/doctor-ue-declines.json` |
| 3 | npm script | `package.json` → `doctor:ue` |
| 4 | Policy update | [docs/Setup/DOCTOR_POLICY.md](../docs/Setup/DOCTOR_POLICY.md) |
| 5 | Dev runbook | [docs/Setup/CURSOR_DEV.md](../docs/Setup/CURSOR_DEV.md) |

**Not in scope:** TypeScript, ESLint, Jest, rules diet, gameplay C++, `.uasset`.

---

## Before / after (cloud VM, submodule init + doctor:build)

Host: Linux cloud agent VM, DevEnvTemplate pin `2efd756`, Node 22.

| Command | Exit | Score | Criticals |
|---------|------|-------|-----------|
| `npm run doctor` | **1** | 77/100 | 5 (all policy declines) |
| `npm run doctor:ue` | **0** | 77/100 (same report) | 5 accepted → non-fatal |

### Raw doctor critical list

```
- TypeScript Not Configured
- ESLint Not Configured
- No JS Unit Tests Detected
- Secrets Handling Not Detected
- Always-Applied Rule Budget Exceeded
```

### doctor:ue summary (tail)

```
--- doctor:ue (UE host) ---
Raw doctor exit: 1
Critical total: 5
Accepted declines (non-fatal): 5
  ✓ TypeScript Not Configured
  ✓ ESLint Not Configured
  ✓ No JS Unit Tests Detected
  ✓ Secrets Handling Not Detected
  ✓ Always-Applied Rule Budget Exceeded
doctor:ue exit: 0 (only accepted declines remain)
```

**Windows:** Same class expected on DESKTOP-21CT3H0 after `git submodule update --init DevEnvTemplate` + `npm run doctor:build`. Lead may spot-check; cloud evidence satisfies HR2-A done criteria for automation hosts.

---

## How it works

1. `doctor:ue` runs the same DevEnvTemplate CLI as `npm run doctor` (stdio inherited).
2. Reads `.devenv/health-report.json` critical `message` fields.
3. Compares against `config/doctor-ue-declines.json` (synced with DOCTOR_POLICY table).
4. Exit **0** if every critical is in the decline set; exit **1** if any actionable critical remains.

Adding a new accepted decline: update **both** `config/doctor-ue-declines.json` and DOCTOR_POLICY.md.

---

## Done criteria (HR2-A)

- [x] `npm run doctor:ue` exits **0** on cloud when only accepted declines remain
- [x] Exit **1** path preserved for non-declined criticals (wrapper logic)
- [x] DOCTOR_POLICY + CURSOR_DEV document `doctor` vs `doctor:ue`
- [x] Decline registry is machine-readable single source for wrapper
- [ ] Lead **`APPROVE HR2-A`** → unlock HR2-B

---

*HR2-A complete — Conductor stops for Lead **`APPROVE HR2-A`**.*
