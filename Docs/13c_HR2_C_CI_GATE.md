# Docs/13c — HR2-C C++ CI Gate (build-win64 required)

| Field | Value |
|-------|-------|
| **Status** | **APPROVED** — Lead Luke Thompson, **`APPROVE HR2-C`**, 2026-09-17 ET |
| **Date** | 2026-09-17 |
| **Author** | Cloud Agent (HR2-C) |
| **Strategy** | [13_HR2_HARNESS_REFINE.md](13_HR2_HARNESS_REFINE.md) — Lead **`APPROVE HR2 STRATEGY`**, 2026-09-17 ET |
| **Prior gate** | HR2-B **APPROVED** — Lead **`APPROVE HR2-B`**, 2026-09-17 ET |

---

## Gate

**APPROVED** — Lead Luke Thompson, **`APPROVE HR2-C`**, 2026-09-17 ET. HR2 track **CLOSED / COMPLETE**. **No HR2-D.**

---

## Goal

PRs touching C++ paths **require** green `build-win64` on the self-hosted Windows runner, or an explicit **Lead waiver**. Docs-only PRs remain **validate-only** (no UE build).

---

## C++ path filters (canonical — sync ci.yml ↔ CI_POLICY)

| Path pattern | Purpose |
|--------------|---------|
| `Source/**` | Game module C++ |
| `**/*.Build.cs` | Unreal build rules |
| `*.uproject` | Project descriptor / module list |
| `Plugins/**/Source/**` | Tracked plugin C++ (if any) |
| `.github/workflows/ci.yml` | Re-validate when build workflow changes |

**Out of scope for required build:** `docs/**`, `Docs/**`, `Content/Python/**`, config-only changes without C++ paths.

---

## Deliverables

| # | Item | Path |
|---|------|------|
| 1 | Workflow path filters + waiver skip | [.github/workflows/ci.yml](../.github/workflows/ci.yml) |
| 2 | Required vs validate-only policy | [docs/Setup/CI_POLICY.md](../docs/Setup/CI_POLICY.md) |
| 3 | Branch protection expectation | [docs/Setup/CI_SETUP.md](../docs/Setup/CI_SETUP.md) § Branch protection |
| 4 | Cloud agent packet | [swarm/CLOUD_AGENT_PACKET.md](../swarm/CLOUD_AGENT_PACKET.md) |
| 5 | Strategy stamp | [13_HR2_HARNESS_REFINE.md](13_HR2_HARNESS_REFINE.md) |

**Not in scope:** UE on GitHub-hosted Ubuntu; requiring `build-win64` for docs/Python-only PRs; gameplay C++ changes.

---

## Lead waiver escape hatch

When merge must proceed without a Windows build (runner offline, hotfix policy):

1. PR description contains exact text: **`Lead waiver: build-win64`**
2. **Or** label: **`lead-waiver-build-win64`**
3. **`validate` + `python-lint` must still be green**
4. Lead approves merge in review

`ci.yml` skips `build-win64` and runs `build-win64-waiver-notice` (ubuntu notice job).

---

## Branch protection (Lead action outside repo)

Lead configures GitHub **Settings → Branches** for `main`:

- **Required:** `validate`, `python-lint` (every PR)
- **Required:** `build-win64` when workflow runs (C++ paths)

See [CI_SETUP.md](../docs/Setup/CI_SETUP.md) § Branch protection for skipped-check behavior on docs-only PRs.

---

## Evidence

| Check | Result | Notes |
|-------|--------|-------|
| Path list in `ci.yml` | Matches CI_POLICY table | HR2-C sync |
| Docs-only PR | `validate` + `python-lint` only | `ci.yml` skipped via path filters |
| C++ PR | `validate` + `build-win64` required | Self-hosted `windows`/`ue57` |
| Waiver PR | Notice job; build skipped | Lead documented in PR body/label |
| Cloud agent packet | Updated | C++ PR → Windows runner or waiver |

This PR is **docs + ci.yml only** — no C++ gameplay changes. CI validate runs on merge.

---

## Done criteria (HR2-C)

- [x] C++ touch PR policy: green `build-win64` required unless Lead waiver documented
- [x] Docs-only PR merges on validate alone (`ci.yml` path filters)
- [x] CI_POLICY and ci.yml agree on path list
- [x] Cloud agent packet updated
- [x] Branch protection documented in CI_SETUP / CI_POLICY
- [x] Lead **`APPROVE HR2-C`** → HR2 track **CLOSED**

---

*HR2-C **APPROVED** 2026-09-17 ET — HR2 track **CLOSED / COMPLETE**. No HR2-D.*
