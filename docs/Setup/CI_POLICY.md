# CI policy — validate vs build-win64

**When to use this:** Opening a PR or choosing whether a change needs a Windows UE build.

**HR2-C (2026-09-17):** `build-win64` is **Required** when a PR touches C++ paths (see path list below). Docs-only PRs remain **validate-only**.

---

## Two workflows

| Workflow | Runner | UE required | When it runs |
|----------|--------|-------------|--------------|
| **[validate.yml](../../.github/workflows/validate.yml)** | GitHub-hosted Ubuntu | No | **Every** push/PR to `main` / `master` |
| **[ci.yml](../../.github/workflows/ci.yml)** | Self-hosted `[self-hosted, windows, ue58]` | Yes (UE 5.8 + VS) | Push/PR that touches **C++ path filters** (below); needs **DESKTOP-21CT3H0** (or equivalent) online |

Full runner setup: [CI_SETUP.md](CI_SETUP.md). Cloud → Windows handoff: [WINDOWS_BRIDGE.md](WINDOWS_BRIDGE.md). HR2-C deliverable: [Docs/13c_HR2_C_CI_GATE.md](../../Docs/13c_HR2_C_CI_GATE.md).

---

## C++ path filters (ci.yml ↔ CI_POLICY — must stay in sync)

When a PR changes **any** of these paths, **`build-win64` is required** (green on self-hosted Windows runner):

| Path pattern | Examples |
|--------------|----------|
| `Source/**` | `Source/HomeWorld/*.cpp`, `Source/HomeWorld/*.h` |
| `**/*.Build.cs` | `Source/HomeWorld/HomeWorld.Build.cs` |
| `*.uproject` | `HomeWorld.uproject` |
| `Plugins/**/Source/**` | Tracked plugin C++ (if any) |
| `.github/workflows/ci.yml` | CI workflow changes (re-validates build gate) |

**Not in C++ filters:** `docs/**`, `Docs/**`, `Content/Python/**`, `Config/*.ini` (unless paired with C++ paths), `.cursor/**`, `swarm/**`.

---

## What validate checks (DOCS_LAYOUT truth)

`validate.yml` verifies (runs on **all** PRs):

- `HomeWorld.uproject` valid JSON
- `Content/Python/*.json` valid
- **Required docs** at canonical paths (see [DOCS_LAYOUT.md](../DOCS_LAYOUT.md)) — not quarantine stubs under `docs/workflow/` or `docs/tasks/`
- C++ header/source pairing (warnings)
- **DevEnvTemplate pin + submodule** — gitlink matches [config/devenv-template-pin.json](../../config/devenv-template-pin.json); empty submodule dir is inited in CI ([scripts/verify-devenv-submodule.sh](../../scripts/verify-devenv-submodule.sh); HR2-B)
- Git hygiene (no `__pycache__`, temp JSON in root)

**Docs-only PRs:** `validate` + `python-lint` jobs are **sufficient**. `ci.yml` does **not** run (no C++ path changes). No Win64 build required.

---

## When ci.yml (build-win64) matters

| Change type | validate | ci.yml build-win64 |
|-------------|----------|-------------------|
| Docs / markdown only | **Required** | **Not required** (workflow skipped) |
| Python Editor scripts (`Content/Python/`) | **Required** | Optional (run PIE/tests on Windows) |
| C++ (`Source/`, `*.Build.cs`, `*.uproject`, plugin Source) | **Required** | **Required** — must be green before merge |
| `.uasset` / `.umap` | Allowlist only ([Docs/20_UASSET_AI_POLICY.md](../../Docs/20_UASSET_AI_POLICY.md)); default KEEP-LOCAL | Windows Editor + Git LFS for allowlisted paths |

If the self-hosted runner is offline, **do not merge** C++ PRs until `build-win64` is green or Lead documents a **waiver** (below).

---

## Lead waiver (build-win64 escape hatch)

When the Windows runner is unavailable or Lead accepts merge risk without a CI build:

1. Add to the **PR description** (exact phrase): `Lead waiver: build-win64`
2. **Or** apply GitHub label: `lead-waiver-build-win64`
3. Lead explicitly approves merge in review (Conductor / Human Lead)

The workflow skips `build-win64` when the waiver is present and posts a notice job. **Validate must still be green.** Waiver is for **build-win64 only** — not for skipping `validate` or committing `.uasset`.

---

## Branch protection (GitHub settings — Lead action)

**HR3-C (Docs/15c):** Repo settings are outside this tree. Lead applies the step-by-step checklist in [CI_SETUP.md](CI_SETUP.md) § Branch protection. Handoff status: [Docs/handoffs/HR3_C_BRANCH_PROTECTION.md](../../Docs/handoffs/HR3_C_BRANCH_PROTECTION.md) — cloud agents **cannot** confirm protection is enabled (API 403 without admin).

| Check | Required on `main` | Notes |
|-------|-------------------|-------|
| `validate` | **Yes** | Every PR — [validate.yml](../../.github/workflows/validate.yml) job `validate` |
| `python-lint` | **Yes** | Every PR — [validate.yml](../../.github/workflows/validate.yml) job `python-lint` |
| `build-win64` | **Yes** | When C++ path filters match — [ci.yml](../../.github/workflows/ci.yml) job `build-win64`; skipped on docs-only PRs |

**C++ path filters** (must match `ci.yml` and table above in § C++ path filters): `Source/**`, `**/*.Build.cs`, `*.uproject`, `Plugins/**/Source/**`, `.github/workflows/ci.yml`.

If GitHub blocks docs-only PRs because `build-win64` never ran, enable **“Do not require status checks for checks that were skipped”** in the branch rule, or enforce C++ gate via Lead review until path-scoped rulesets are available.

Details: [CI_SETUP.md](CI_SETUP.md) § Branch protection · Gate: [Docs/15c_HR3_C_BRANCH_PROTECTION.md](../../Docs/15c_HR3_C_BRANCH_PROTECTION.md).

---

## `[skip ci]` guidance

Use **`[skip ci]`** in the commit message **only** when:

- Typo/formatting in docs with zero functional change, **and**
- You accept that GitHub Actions will not run on that commit

**Do not** skip CI for:

- Changes to `validate.yml`, `ci.yml`, or required-doc paths
- C++ or Python automation changes
- Anything that needs lint or doc-path verification

Prefer normal commits so `validate` stays green on every merge.

---

## Related

- [BUILD_POLICY.md](BUILD_POLICY.md) — Safe-Build for agents
- [MCP_SETUP.md](MCP_SETUP.md) — Editor MCP after build
- [Docs/11a_HR_MEASURES.md](../../Docs/11a_HR_MEASURES.md) — SH-01 CI flake baseline
- [Docs/13c_HR2_C_CI_GATE.md](../../Docs/13c_HR2_C_CI_GATE.md) — HR2-C evidence and done criteria
