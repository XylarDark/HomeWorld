# Contributing to HomeWorld

**Project root:** The repo root is the project root. All paths in docs and scripts (e.g. `HomeWorld.uproject`, `Build-HomeWorld.bat`) are relative to the clone root.

## Workflow

1. Create a branch from `main` (or `master`): e.g. `feature/week1-pcg-biome`, `fix/plugin-load`.
2. Make your changes. If you touch setup or config, run through the [docs/SETUP.md](docs/SETUP.md) validation section.
3. Ensure the project opens in Unreal Editor without errors.
4. Open a pull request to `main` (or `master`). Fill in the PR template.
5. After review (one approval from another team member when possible), merge.

## Scope and context

- **Roadmap:** [ROADMAP.md](ROADMAP.md) – phases, pillars, campaign.
- **Current tasks:** [docs/TASKLIST.md](docs/TASKLIST.md) – what to build first in the Editor; each task links to a detailed doc in docs/tasks/.
- **Stack:** [docs/STACK_PLAN.md](docs/STACK_PLAN.md) – recommended tech per layer.

## Before opening a PR

- Run the [docs/SETUP.md](docs/SETUP.md) validation section if your change affects setup, plugins, or config.
- Confirm the project loads in UE and your change doesn’t break the default flow.
- Validation is currently manual (checklist + play in Editor); there is no automated test suite yet. When you fix a build, lint, or runtime error, record it in [docs/KNOWN_ERRORS.md](docs/KNOWN_ERRORS.md) so the team doesn't repeat it (see `.cursor/rules` error-recurrence guidance).
