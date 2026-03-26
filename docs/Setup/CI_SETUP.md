# CI setup (self-hosted runner and alternatives)

This doc explains how to get **full Unreal Engine build and automation tests** running in CI. The repo has two workflows:

- **validate.yml** — Runs on every push on GitHub-hosted runners (Ubuntu). No UE required: lint, JSON checks, required docs, C++ header/source pairing. Always runs.
- **ci.yml** — Full Win64 build and optional automation tests. **Requires a self-hosted Windows runner** with Unreal Engine 5.7 installed.

---

## Self-hosted Windows runner (primary)

To run [.github/workflows/ci.yml](../.github/workflows/ci.yml) (build + tests), you need a Windows machine that will act as a GitHub Actions runner with UE 5.7 and the build toolchain installed.

### 1. Install prerequisites on the runner machine

- **Windows 10/11** (x64).
- **Visual Studio 2022** (or 2019) with **Desktop development with C++** and **Windows 10/11 SDK**. Same toolchain as your local UE 5.7 development.
- **Unreal Engine 5.7** — Install via Epic Games Launcher (or custom build) to a known path, e.g. `C:\Program Files\Epic Games\UE_5.7`.
- **Git** and **Git LFS** — Required for checkout and .uasset/.umap. Run `git lfs install` on the machine.

### 2. Clone the repo and register the runner

- Clone the HomeWorld repo (or ensure the runner will have access to it).
- In GitHub: **Settings → Actions → Runners → New self-hosted runner**. Follow the instructions for Windows (download, configure, install/run as service).
- When configuring the runner, add **labels** so ci.yml can select it. The workflow uses:
  - `runs-on: [self-hosted, windows, ue57]`
  So add at least: **windows**, **ue57** (and **self-hosted** is automatic). You can add these in the runner configuration or in the GitHub UI when adding the runner.

### 3. Set environment on the runner (optional but recommended)

For the **Run automation tests** step in ci.yml to run (Smoke group), the runner needs **UE_EDITOR** set so that [Tools/RunTests.ps1](../Tools/RunTests.ps1) (and [Content/Python/run_ue_automation.py](../Content/Python/run_ue_automation.py)) can launch the Editor headless. Options:

- **System or user env:** Set `UE_EDITOR` to the full path to `UnrealEditor.exe`, e.g. `C:\Program Files\Epic Games\UE_5.7\Engine\Binaries\Win64\UnrealEditor.exe`. Restart the runner service after changing env vars.
- **CI workflow:** You can set env in the workflow (e.g. from a secret or hardcoded path) and pass it to the step; the current ci.yml uses `${{ env.UE_EDITOR }}`, so define `env.UE_EDITOR` at job or workflow level if not set on the runner.

If `UE_EDITOR` is not set, the workflow still runs the build; the "Run automation tests" step will skip and log that tests were skipped.

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
- **Epic container images (UE 5.7)** — Epic’s [Container Deployments and Images](https://dev.epicgames.com/documentation/en-us/unreal-engine/container-deployments-and-images-for-unreal-editor-and-unreal-engine) (beta) provide UE in containers for cloud pipelines. Useful for deployment and custom runner images; not a drop-in “run ci.yml on GitHub-hosted runner” without a Windows-based runner or custom image.

These are optional; the primary path for HomeWorld is a self-hosted Windows runner with UE 5.7 as described above.

---

## Summary

- **validate.yml** — No setup; runs on every push on GitHub-hosted runners.
- **ci.yml** — Requires a self-hosted Windows runner with UE 5.7, Visual Studio, and (for tests) `UE_EDITOR` set. Add labels `windows`, `ue57` to the runner. See steps 1–4 above.
