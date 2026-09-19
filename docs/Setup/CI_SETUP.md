# CI setup (self-hosted runner and alternatives)

**Policy summary:** When `validate.yml` vs `ci.yml` matters, docs-only PRs, and `[skip ci]` — see [CI_POLICY.md](CI_POLICY.md). **Cloud → Windows handoff:** [WINDOWS_BRIDGE.md](WINDOWS_BRIDGE.md).

This doc explains how to get **full Unreal Engine build and automation tests** running in CI. The repo has two workflows:

- **validate.yml** — Runs on every push on GitHub-hosted runners (Ubuntu). No UE required: lint, JSON checks, required docs, C++ header/source pairing. Always runs.
- **ci.yml** — Full Win64 build and optional automation tests. **Requires a self-hosted Windows runner** with Unreal Engine 5.8 installed.

---

## Self-hosted Windows runner (primary)

To run [.github/workflows/ci.yml](../.github/workflows/ci.yml) (build + tests), you need a Windows machine that will act as a GitHub Actions runner with UE 5.8 and the build toolchain installed.

### 1. Install prerequisites on the runner machine

- **Windows 10/11** (x64).
- **Visual Studio 2022** (or 2019) with **Desktop development with C++** and **Windows 10/11 SDK**. Same toolchain as your local UE 5.8 development.
- **Unreal Engine 5.8** — Install via Epic Games Launcher (or custom build) to a known path, e.g. `C:\Program Files\Epic Games\UE_5.8`.
- **Git** and **Git LFS** — Required for checkout and .uasset/.umap. Run `git lfs install` on the machine.

### 2. Clone the repo and register the runner

- Clone the HomeWorld repo (or ensure the runner will have access to it).
- In GitHub: **Settings → Actions → Runners → New self-hosted runner**. Follow the instructions for Windows (download, configure, install/run as service).
- When configuring the runner, add **labels** so ci.yml can select it. The workflow uses:
  - `runs-on: [self-hosted, windows, ue58]`
  So add at least: **windows**, **ue58** (and **self-hosted** is automatic). You can add these in the runner configuration or in the GitHub UI when adding the runner.

### 3. Set environment on the runner (optional but recommended)

For the **Run automation tests** step in ci.yml to run (Smoke group), the runner needs **UE_EDITOR** set so that [Tools/RunTests.ps1](../Tools/RunTests.ps1) (and [Content/Python/run_ue_automation.py](../Content/Python/run_ue_automation.py)) can launch the Editor headless. Options:

- **System or user env:** Set `UE_EDITOR` to the full path to `UnrealEditor.exe`, e.g. `C:\Program Files\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe`. Restart the runner service after changing env vars.
- **CI workflow:** You can set env in the workflow (e.g. from a secret or hardcoded path) and pass it to the step; the current ci.yml uses `${{ env.UE_EDITOR }}`, so define `env.UE_EDITOR` at job or workflow level if not set on the runner.

If `UE_EDITOR` is not set, the workflow still runs the build; the "Run automation tests" step will skip and log that tests were skipped.

**`UE_EDITOR` inside GitHub Actions:** [.github/workflows/ci.yml](../../.github/workflows/ci.yml) passes `UE_EDITOR: ${{ env.UE_EDITOR }}` into the test step. That value is only non-empty if you define **`env`** at the **workflow** or **job** level in `ci.yml`, or if your runner exposes it in a way Actions injects into `env` (varies by runner setup). If tests always skip, either set **`UE_EDITOR`** as a persistent **user or system** environment variable on the runner (restart the runner service after changes) or add a job-level default, for example:

```yaml
jobs:
  build-win64:
    runs-on: [self-hosted, windows, ue58]
    env:
      UE_EDITOR: 'C:\Program Files\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe'
```

Use your real engine path, or a repository variable / secret if paths differ per machine.

### Runner maintenance

- **Disk:** Periodically clear **Derived Data Cache** and old **Intermediate** folders if the runner disk fills or builds slow down. Typical locations: `%LOCALAPPDATA%\UnrealEngine\Common\DerivedDataCache`, and the repo’s `Intermediate/` / `Saved/` (safe to delete on the runner between runs if you accept longer next build).
- **Labels:** The job requires `runs-on: [self-hosted, windows, ue58]` — ensure the runner is registered with labels **windows** and **ue58** (plus self-hosted).
- **Engine path:** [ci.yml](../../.github/workflows/ci.yml) defaults **`UE_ENGINE`** to `C:\Program Files\Epic Games\UE_5.8` for the build step if unset; align installs or override `UE_ENGINE` on the runner.

### 4. What ci.yml does when a runner is available

1. Checkout with LFS.
2. Build Win64 Development (RunFullBuild.ps1 or Build-HomeWorld.bat).
3. Optionally run automation tests (RunTests.ps1 with Smoke group) if UE_EDITOR is set.
4. On failure, upload Build-HomeWorld.log as an artifact.

---

## Horde (Epic distributed builds)

For distributed or more advanced build pipelines, you can use [Epic Horde](https://dev.epicgames.com/documentation/en-us/unreal-engine/horde-build-automation-for-unreal-engine). The project has a minimal guide: [HORDE_LOCAL_SETUP.md](HORDE_LOCAL_SETUP.md). Horde uses its own agents and job templates; ci.yml could later be adapted to trigger Horde jobs instead of (or in addition to) inline build steps. For a single runner and standard GitHub Actions, the self-hosted runner above is sufficient.

---

## Hosted UE CI options (evaluate as needed)

If you prefer not to maintain a self-hosted Windows machine:

- **Speedrun CI** — [speedrun.ci](https://speedrun.ci/) — Commercial CI built for Unreal Engine; integrates with GitHub. Evaluate for pricing and feature fit.
- **Epic container images (UE 5.8)** — Epic’s [Container Deployments and Images](https://dev.epicgames.com/documentation/en-us/unreal-engine/container-deployments-and-images-for-unreal-editor-and-unreal-engine) (beta) provide UE in containers for cloud pipelines. Useful for deployment and custom runner images; not a drop-in “run ci.yml on GitHub-hosted runner” without a Windows-based runner or custom image.

These are optional; the primary path for HomeWorld is a self-hosted Windows runner with UE 5.8 as described above.

---

## Branch protection (Lead — GitHub repo settings)

**HR3-C (Docs/15c):** Branch protection is configured in **GitHub Settings**, not in this repo. Cloud agents **cannot** flip the branch-protection UI — Lead must apply the checklist below and confirm in [Docs/handoffs/HR3_C_BRANCH_PROTECTION.md](../../Docs/handoffs/HR3_C_BRANCH_PROTECTION.md).

**Policy:** [CI_POLICY.md](CI_POLICY.md) · **HR2-C path filters:** [Docs/13c_HR2_C_CI_GATE.md](../../Docs/13c_HR2_C_CI_GATE.md) · **HR3-C gate:** [Docs/15c_HR3_C_BRANCH_PROTECTION.md](../../Docs/15c_HR3_C_BRANCH_PROTECTION.md)

### Required status checks on `main`

| Status check (exact job name) | Workflow | Require? | When it applies |
|-------------------------------|----------|----------|-----------------|
| **`validate`** | [validate.yml](../../.github/workflows/validate.yml) | **Yes** | Every PR to `main` |
| **`python-lint`** | [validate.yml](../../.github/workflows/validate.yml) | **Yes** | Every PR to `main` |
| **`build-win64`** | [ci.yml](../../.github/workflows/ci.yml) | **Yes** | When PR touches **C++ path filters** (below); skipped on docs-only PRs |

**C++ path filters** (must stay in sync with `ci.yml` and [CI_POLICY.md](CI_POLICY.md)):

| Path pattern | Examples |
|--------------|----------|
| `Source/**` | `Source/HomeWorld/*.cpp`, `Source/HomeWorld/*.h` |
| `**/*.Build.cs` | `Source/HomeWorld/HomeWorld.Build.cs` |
| `*.uproject` | `HomeWorld.uproject` |
| `Plugins/**/Source/**` | Tracked plugin C++ (if any) |
| `.github/workflows/ci.yml` | CI workflow changes |

**Not in C++ filters:** `docs/**`, `Docs/**`, `Content/Python/**`, `Config/*.ini` (unless paired with C++ paths), `.cursor/**`, `swarm/**`.

### Lead checklist — enable branch protection for `main`

Complete these steps in the GitHub UI (**repo admin** required). Do **not** mark HR3-C done until Lead confirms each box.

#### 0. Prerequisites

- [ ] At least **one recent PR** has run Actions so check names appear in the picker (merge this HR3-C docs PR or any open PR first if the list is empty).
- [ ] Self-hosted runner **DESKTOP-21CT3H0** is online with labels `windows`, `ue58` when testing C++ PRs ([§ Self-hosted Windows runner](#self-hosted-windows-runner-primary) above).

#### 1. Open branch protection

1. Go to **https://github.com/XylarDark/HomeWorld/settings/branches**
2. Under **Branch protection rules**, click **Add rule** (or **Edit** an existing rule for `main`).
3. **Branch name pattern:** `main`

#### 2. Pull request requirements (recommended)

- [ ] **Require a pull request before merging** — enabled
- [ ] **Require approvals** — optional (team preference); minimum **1** if enabled
- [ ] **Dismiss stale pull request approvals when new commits are pushed** — optional
- [ ] **Require conversation resolution before merging** — optional

#### 3. Status checks (required)

- [ ] **Require status checks to pass before merging** — enabled
- [ ] **Require branches to be up to date before merging** — enabled (recommended)
- [ ] Search the status-check picker and add these **exact job names**:
  - [ ] **`validate`**
  - [ ] **`python-lint`**
  - [ ] **`build-win64`**

GitHub may show workflow context in the UI (e.g. `Validate / validate`). Select the entries whose **job name** matches the table above.

**Skipped checks (docs-only PRs):** [ci.yml](../../.github/workflows/ci.yml) uses path filters — docs-only PRs do **not** run `build-win64`. Enable **“Do not require status checks to pass for checks that were skipped”** (GitHub wording may vary: *allow merge when optional/skipped checks did not run*). Without this, docs PRs can be blocked waiting for a check that never runs.

If that option is unavailable on your plan, use **Lead merge policy** for docs-only PRs until path-scoped rulesets exist — see [CI_POLICY.md](CI_POLICY.md).

#### 4. Additional protections (recommended)

- [ ] **Do not allow bypassing the above settings** — enabled (admins included), or document who may bypass
- [ ] **Restrict who can push to matching branches** — optional; blocks direct pushes to `main`
- [ ] **Allow force pushes** — **disabled**
- [ ] **Allow deletions** — **disabled**

#### 5. Save and verify

1. Click **Create** or **Save changes**.
2. Open a **docs-only test PR** — expect **`validate`** + **`python-lint`** green; **`build-win64`** absent/skipped; merge allowed.
3. Open (or use) a **C++-touching PR** — expect all three checks; **`build-win64`** must be green on self-hosted Windows unless [Lead waiver](#lead-waiver-build-win64) applies.

#### 6. Lead confirmation (HR3-C evidence)

After applying settings, Lead updates [Docs/handoffs/HR3_C_BRANCH_PROTECTION.md](../../Docs/handoffs/HR3_C_BRANCH_PROTECTION.md):

- Status → **APPLIED** (or **DEFERRED** with ticket/note)
- Screenshot or API excerpt listing required checks on `main`
- Date and Lead stamp

**API verify (Lead / admin PAT only):** Cloud agent token returns **403** — Lead must run:

```bash
gh api repos/XylarDark/HomeWorld/branches/main/protection \
  --jq '{required_checks: .required_status_checks.contexts, strict: .required_status_checks.strict, enforce_admins: .enforce_admins.enabled}'
```

Expected `required_checks` includes `validate`, `python-lint`, and `build-win64` when HR3-C is **APPLIED**. Empty response or 404 means protection is **not** configured — do not claim enabled in PHASE_BOARD.

### Docs-only PR behavior

When a PR changes only paths **outside** the C++ filters, **`ci.yml` does not run**. With skipped-check handling enabled, merge requires only **`validate`** + **`python-lint`**. See [CI_POLICY.md](CI_POLICY.md) § Two workflows.

### Lead waiver (build-win64)

When the Windows runner is offline or Lead accepts merge risk without a CI build:

1. PR description contains exact text: **`Lead waiver: build-win64`**
2. **Or** GitHub label: **`lead-waiver-build-win64`**
3. **`validate`** + **`python-lint`** must still be green
4. Lead approves merge in review

`ci.yml` skips `build-win64` and runs `build-win64-waiver-notice`. Branch protection may still show `build-win64` as pending — Lead uses admin merge or temporary bypass per team policy. Full policy: [CI_POLICY.md](CI_POLICY.md) § Lead waiver.

---

## Summary

- **validate.yml** — No setup; runs on every push on GitHub-hosted runners.
- **ci.yml** — Requires a self-hosted Windows runner with UE 5.8, Visual Studio, and (for tests) `UE_EDITOR` set. Add labels `windows`, `ue58` to the runner. Runs only when C++ path filters match (HR2-C). See steps 1–4 above and [CI_POLICY.md](CI_POLICY.md).
