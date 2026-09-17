# CI policy — validate vs build-win64

**When to use this:** Opening a PR or choosing whether a change needs a Windows UE build.

---

## Two workflows

| Workflow | Runner | UE required | When it runs |
|----------|--------|-------------|--------------|
| **[validate.yml](../../.github/workflows/validate.yml)** | GitHub-hosted Ubuntu | No | Every push/PR to `main` / `master` |
| **[ci.yml](../../.github/workflows/ci.yml)** | Self-hosted `[self-hosted, windows, ue57]` | Yes (UE 5.7 + VS) | Push/PR when workflow triggers; needs **DESKTOP-21CT3H0** (or equivalent) online |

Full runner setup: [CI_SETUP.md](CI_SETUP.md). Cloud → Windows handoff: [WINDOWS_BRIDGE.md](WINDOWS_BRIDGE.md).

---

## What validate checks (DOCS_LAYOUT truth)

`validate.yml` verifies:

- `HomeWorld.uproject` valid JSON
- `Content/Python/*.json` valid
- **Required docs** at canonical paths (see [DOCS_LAYOUT.md](../DOCS_LAYOUT.md)) — not quarantine stubs under `docs/workflow/` or `docs/tasks/`
- C++ header/source pairing (warnings)
- **DevEnvTemplate pin + submodule** — gitlink matches [config/devenv-template-pin.json](../../config/devenv-template-pin.json); empty submodule dir is inited in CI ([scripts/verify-devenv-submodule.sh](../../scripts/verify-devenv-submodule.sh); HR2-B)
- Git hygiene (no `__pycache__`, temp JSON in root)

**Docs-only PRs:** `validate` + `python-lint` jobs are sufficient. No `ci.yml` / Win64 build required.

---

## When ci.yml (build-win64) matters

| Change type | validate | ci.yml build-win64 |
|-------------|----------|-------------------|
| Docs / markdown only | Required | Not required |
| Python Editor scripts (`Content/Python/`) | Required | Optional (run PIE/tests on Windows) |
| C++ (`Source/`, `*.Build.cs`) | Required | **Recommended** — cloud agents cannot Safe-Build locally |
| `.uasset` / `.umap` | N/A (never commit) | Windows Editor only |

If the self-hosted runner is offline, merge may proceed for docs-only work; C++ PRs should wait for green build or explicit Lead verification on **DESKTOP-21CT3H0**.

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
