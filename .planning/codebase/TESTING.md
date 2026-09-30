---
last_mapped_commit: 94158e9416cc44954f4fdb11e0de696e31836276
last_mapped_at: 2026-09-28
---
﻿# Testing

**Analysis Date:** 2026-09-28

## Frameworks

**Node (repo harness):**
- `node --test` via npm scripts
- `scripts/preflight-ue.test.js`
- `scripts/evidence-grep.test.js`
- `package.json`: `preflight:ue:test`, `evidence:grep:test`

**UE Python automation:**
- `Content/Python/tests/` — e.g. `test_project_setup.py`, `test_input_assets.py`, `test_pcg_forest.py`, `test_level_pie_flow.py`, `test_character.py`, material rule tests
- Requires Editor / Python plugin on DESKTOP

**UE automation (optional CI):**
- `.github/workflows/ci.yml` optional `Tools/RunTests.ps1 -Group Smoke` when `UE_EDITOR` set
- Primary CI gate: Win64 Development build on self-hosted `ue58` runner

**Validate workflow:**
- `.github/workflows/validate.yml` — docs/policy path (non-C++ PRs)

## Structure

| Layer | Location | Runs where |
|-------|----------|------------|
| Harness unit | `scripts/*.test.js` | Any Node ≥20 |
| Preflight | `npm run preflight:ue` | DESKTOP full; cloud `--assets-only` |
| Python Editor tests | `Content/Python/tests/` | DESKTOP Editor |
| PIE / verb evidence | logs + `evidence:grep` | DESKTOP Conductor parent |
| C++ build gate | `ci.yml` build-win64 | Self-hosted Windows UE 5.8 |

## Mocking / Fixtures

- Preflight supports `--simulate-fail=` for dry-run docs/tests
- Mannequins / Character content KEEP-LOCAL (`Content/Characters/` gitignored) — not a CI fixture

## Coverage Expectations

- New features must be log-validatable (instrumentation rule)
- Product Act gates require evidence paths on disk before Lead `APPROVE`
- GSD host scaffolding does **not** invent Nyquist/eval suites for Co product — leave Research EXIT untouched

---
*Testing analysis: 2026-09-28*
