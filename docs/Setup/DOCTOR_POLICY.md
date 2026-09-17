# Doctor policy — HomeWorld accepted declines

HomeWorld is a **Unreal Engine 5.7 game host** (C++, Python Editor automation, minimal root `package.json` for DevEnvTemplate doctor/sync only). The DevEnvTemplate doctor scores against a **Node/TS app** profile by default. Several **critical** findings are **accepted declines** — not bugs to fix by inventing a fake Node application.

**Canonical doctor commands:** [CURSOR_DEV.md](CURSOR_DEV.md) — `npm run doctor:build` (after pin bump or fresh clone), **`npm run doctor:ue`** (UE host — trust exit code), `npm run doctor` (raw template output).

**Decline registry (machine-readable):** [config/doctor-ue-declines.json](../../config/doctor-ue-declines.json) — keep in sync with the table below.

**HR-B2 evidence:** [Docs/11e_HR_B2_HANDOFF.md](../../Docs/11e_HR_B2_HANDOFF.md). **HR2-A:** [Docs/13a_HR2_A_HANDOFF.md](../../Docs/13a_HR2_A_HANDOFF.md). **HR3-B (game harness, not doctor):** [UE_PREFLIGHT.md](UE_PREFLIGHT.md) — `npm run preflight:ue` for MCP/assets/PIE blockers; keep separate from doctor declines.

---

## Accepted declines (critical → rationale)

| Doctor critical | Why it does not apply to HomeWorld | Where policy lives |
|-----------------|-------------------------------------|-------------------|
| **TypeScript Not Configured** | Game logic is **C++** (`Source/HomeWorld/`). Root `package.json` exists only for DevEnvTemplate CLI wrappers, not a TS product surface. | [AGENTS.md](../../AGENTS.md) DevEnvTemplate table |
| **ESLint Not Configured** | No JS/TS product codebase. Python lint runs in CI (`validate.yml` python-lint). Adding ESLint would be template cosplay, not game quality. | [AGENTS.md](../../AGENTS.md), `.github/workflows/validate.yml` |
| **No JS Unit Tests Detected** | Tests: **Python** (`Content/Python/tests/`), **UE Test Automation**, **PIE** (`pie_test_runner.py`). Doctor does not detect UE/Python test harness as “JS unit tests.” | [AGENTS.md](../../AGENTS.md) Testing section |
| **Secrets Handling Not Detected** | Secrets policy: no `.env` in repo; `.env.example` templates; OWASP rules in glob-scoped `02-security.mdc`; gitignore for `Saved/`, plugins. Doctor looks for Node-specific secret scanners. | [02-security.mdc](../../.cursor/rules/02-security.mdc), [AGENTS.md](../../AGENTS.md) Security |
| **Always-Applied Rule Budget Exceeded** | HomeWorld **keeps** session-wide rules (`07`, `08`, `20`) until dedicated AGENTS.md + skills migration. HR-B2 reduced always-on count **15 → 3** (307 lines; threshold 200). Remaining budget gap is **accepted** until incremental migration or Lead approves retiring `07`/`08` content to skills. | [Docs/11e_HR_B2_HANDOFF.md](../../Docs/11e_HR_B2_HANDOFF.md), [CURSOR_DEV.md](CURSOR_DEV.md) |

---

## Expected doctor outcome

| Command | Host | Expected exit | Notes |
|---------|------|---------------|-------|
| **`npm run doctor:ue`** | Cloud VM / Windows (after submodule init + `doctor:build`) | **0** when only accepted declines remain | **Preferred** for agents and CI hygiene checks on UE host |
| `npm run doctor` | Same | **1** (5 policy criticals) | Raw DevEnvTemplate signal — read this doc before interpreting |
| Either | Score | **77/100** (HR-B2 / HR2-A cloud baseline) | Warnings may remain; only **non-declined** criticals fail `doctor:ue` |

**Green raw doctor** on this host would require either (a) adopting a full Node/TS app stack (declined), or (b) reducing always-applied rules below 200 lines **and** template support for host-specific doctor ignore lists (not available at pin `2efd756`). Use **`doctor:ue`** instead.

---

## Node engine warning

Template prefers Node **24+**; HomeWorld allows Node **20+**. `EBADENGINE` on Node 22 is an **accepted decline** — doctor still runs.

---

## When to revisit

- After DevEnvTemplate adds **host override** config for gap suppression (track template `master`).
- After Lead approves retiring always-applied rules to `.agents/skills/` (would address rule budget).
- After HR-D dry-run if harness re-grade shows doctor friction blocking agents.

---

*HR-B2 — honest mitigation; HR2-A adds `doctor:ue` exit-code truth (no TS/ESLint/Jest cosplay).*
