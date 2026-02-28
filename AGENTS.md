# HomeWorld – Agent context

**Project:** HomeWorld — Unreal Engine 5.7 game (Open World / World Partition). Targets UE 5.7 (compatible with 5.7.x, including 5.7.3). Theme: "Love as Epic Quest"; Act 1 focus is lone wanderer (explore → fight → build). See [docs/workflow/VISION.md](docs/workflow/VISION.md) (theme, campaign, 7 sins/virtues, succession) and [docs/STACK_PLAN.md](docs/STACK_PLAN.md) for stack. **Lock:** Engine 5.7 only; platform PC + Steam Early Access; do not add engine or platform variants without team decision.

**Programmatic by default:** As much work as possible is done in C++. New gameplay systems, movement, input, and core logic go in C++; Blueprint is for content, level design, and designer overrides. See [docs/CONVENTIONS.md](docs/CONVENTIONS.md) for the code-first checklist and C++ vs Blueprint split.

**Code:** C++ lives in `Source/HomeWorld/`. Default pawn: `AHomeWorldCharacter`; default game mode: `AHomeWorldGameMode`. Both use Enhanced Input for movement and look.

**Stack (enabled plugins):** Enhanced Input, PCG, Gameplay Abilities, Steam Sockets, Day Sequence. For Week 2 family agents, enable UE 5.7 recommended Mass Entity + Mass AI, StateTree, ZoneGraph, SmartObjects (see [SETUP.md](docs/SETUP.md)). Config in `Config/`; project layout and rules in `.cursor/rules/` (Unreal C++, Blueprint, project).

**MCP-first development:** When the Unreal Editor is running and MCP tools are connected (unrealMCP), prefer live Editor manipulation via MCP over writing scripts or giving manual instructions. See `.cursor/rules/09-mcp-workflow.mdc` and [docs/MCP_SETUP.md](docs/MCP_SETUP.md). For using external LLMs to generate Editor automation scripts, see [docs/EXTERNAL_AI_AUTOMATION.md](docs/EXTERNAL_AI_AUTOMATION.md).

**Parallel plugin:** When the agent sees a need for web search, URL extraction, deep research, or list enrichment, it recommends you run the matching command (`/parallel-search`, `/parallel-extract`, `/parallel-research`, `/parallel-enrich`) and paste the result; the agent then interprets and integrates.

**Current tasks:** [docs/workflow/README.md](docs/workflow/README.md) — workflow index and task status; [docs/workflow/30_DAY_SCHEDULE.md](docs/workflow/30_DAY_SCHEDULE.md) — 30-day schedule; each task links to a detailed doc in `docs/tasks/`.

**Daily workflow:** At session start the agent reads [docs/workflow/DAILY_STATE.md](docs/workflow/DAILY_STATE.md) (yesterday / today). You can prompt e.g. "What did we do yesterday and what do we need to do today?" At session end the agent updates DAILY_STATE (what was done → yesterday; next day's tasks → today; tomorrow preview) and appends [docs/SESSION_LOG.md](docs/SESSION_LOG.md).

**Feature development (policy):** When developing a **new feature**, research Epic/UE docs and best practices first; **follow tutorials first**, then expand. See .cursor/rules/07-ai-agent-behavior.mdc (Feature development: research and tutorials first).

**Compound Engineering plugin:** The plugin is installed; **recommending its commands when appropriate is policy**. When a task is a good use case for a plugin workflow (plan, review, changelog, docs lookup, etc.), recommend the corresponding slash command instead of doing that workflow yourself. The situation-to-command mapping is in [.cursor/rules/10-compound-engineering.mdc](.cursor/rules/10-compound-engineering.mdc). Use **context7** MCP for up-to-date library/framework docs when relevant. Optional one-time: run `/setup` in Cursor to configure review agents for this project.

## Dev environment setup

1. Install UE 5.7, clone this repo, open `HomeWorld.uproject`.
2. Run `Setup-MCP.bat` (one-time MCP bridge install).
3. Run `Build-HomeWorld.bat` to compile C++ (requires Editor closed or Live Coding off).
4. Open Editor, restart Cursor, verify MCP green dot in status bar.
5. See [docs/SETUP.md](docs/SETUP.md) for the full checklist.

**Enhanced Input** is applied automatically when the Editor loads (`Content/Python/init_unreal.py`). You do not need to run `setup_enhanced_input.py` unless movement still fails (troubleshooting).

## Commands

Exact invocations the agent should use (see [docs/SETUP.md](docs/SETUP.md) and [docs/PCG_SETUP.md](docs/PCG_SETUP.md) for more):

- **C++ build:** `Build-HomeWorld.bat` (run with Editor closed or Live Coding off; check `Build-HomeWorld.log` for completion).
- **Python script in Editor:** From project root, `py "Content/Python/<script>.py"`; or via MCP: `execute_python_script("<script>.py")` (paths relative to `Content/Python/`).
- **Python tests:** Editor: Tools > Test Automation (discovers `Content/Python/tests/test_*.py`).
- **PIE validation:** MCP `execute_python_script("pie_test_runner.py")`, then read `Saved/pie_test_results.json`.
- **Project commands:** Reusable workflows in `.cursor/commands/` are available via `/` in chat (e.g. `/run-tests-and-fix`, `/create-pr`, `/review-changes`).
- **Project skills:** Domain skills in `.cursor/skills/` (e.g. homestead-setup, pcg-validate, ue57-api-check) are available via `/` in chat for Homestead map + PCG setup, PCG validation, and UE 5.7 API/plugin checks.
- **PCG Generate nothing:** Use the **pcg-validate** skill and [docs/PCG_SETUP.md](docs/PCG_SETUP.md) section "Generate produces nothing (checklist)"; check Output Log for **LogPCG** and **No surfaces found**.
- **UE 5.7 API/plugin work:** Before changing C++, Blueprint, PCG, or plugin code, check [.cursor/rules/unreal-cpp.mdc](.cursor/rules/unreal-cpp.mdc) (pitfalls table) and [docs/KNOWN_ERRORS.md](docs/KNOWN_ERRORS.md). For **PCG graph or node changes**, also check [docs/PCG_BEST_PRACTICES.md](docs/PCG_BEST_PRACTICES.md) and [docs/PCG_VARIABLES_NO_ACCESS.md](docs/PCG_VARIABLES_NO_ACCESS.md). See [docs/UE57_TECH.md](docs/UE57_TECH.md) for the full UE 5.7 tech entry point.

## Boundaries

- **Never:** Commit secrets, API keys, or `.env`; edit `Plugins/UnrealMCP/` or `Saved/` (they are not project code); change engine version (UE 5.7 only) or target platform (PC + Steam Early Access) without a team decision.
- **Ask first:** CI/schema changes (`.github/workflows/`, JSON schema files), adding or upgrading dependencies, or broad refactors that touch many modules.

## Testing

- **Automated (Python):** `PythonAutomationTest` plugin is enabled. Tests in `Content/Python/tests/` (named `test_*.py`) are auto-discovered. Run via Editor: Tools > Test Automation.
- **PIE tests:** `Content/Python/pie_test_runner.py` validates character spawn, ground contact, animation, and PCG. Run via MCP: `execute_python_script("pie_test_runner.py")`, then read `Saved/pie_test_results.json`.
- **Level loading and tests:** Level load + World Partition streaming can make tests flaky. Smart level loader and latent tests are implemented (see [docs/LEVEL_TESTING_PLAN.md](docs/LEVEL_TESTING_PLAN.md)). Optional PIE full-flow test: `test_level_pie_flow.py` (Tools > Test Automation).
- **CI:** GitHub Actions (`.github/workflows/validate.yml`) — Python lint, JSON schema checks, C++ header/source pairing, doc freshness.

## Code style

- **C++:** PascalCase types, camelCase locals; Unreal prefixes (`A`, `U`, `F`, `E`, `I`). Include own header first. See `.cursor/rules/unreal-cpp.mdc`.
- **Python:** PEP 8, type hints, 4-space indent. UE scripts must be idempotent (check-before-create). See `.cursor/rules/12-python.mdc`.
- **Commits:** Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`). See `.cursor/rules/04-git-workflow.mdc`.
- **Feature debug instrumentation:** When implementing new features, add minimal debug logs (entry/exit, key branches, critical values) so debugging can fast-track to runtime evidence. See `.cursor/rules/16-feature-debug-instrumentation.mdc`.

## PR and commit guidelines

- Use Conventional Commits format for all commit messages.
- PowerShell shell: use `;` not `&&` for command chaining; use here-strings for multi-line commit messages.
- Pre-commit: lint, build check, no secrets, no `__pycache__` or temp JSON in tracked files.

## Security

- Never commit secrets, API keys, or `.env` files. Use `.env.example` for templates.
- `Saved/`, `Plugins/UnrealMCP/`, and `__pycache__/` are gitignored.
- Validate all external input at boundaries. See `.cursor/rules/02-security.mdc`.

## Setup and validation

[docs/SETUP.md](docs/SETUP.md) (includes validation checklist). [docs/SPEC_AND_PLAN.md](docs/SPEC_AND_PLAN.md) (plan-first and where to save plans). Cursor rules ship with the repo in `.cursor/rules/` — they are loaded automatically when the project is opened in Cursor. Key rules: `unreal-cpp.mdc` (C++ conventions + UE 5.7 API pitfalls), `08-project-context.mdc` (HomeWorld overview), `09-mcp-workflow.mdc` (MCP-first priorities), `automation-standards.mdc` (variables-with-no-access procedure for Editor automation). Always check `docs/KNOWN_ERRORS.md` before making changes in areas where errors have been recorded. When adding automation for Editor/engine features, follow the "variables no access" procedure: identify required settings, verify automation access, document no-access items and manual steps (see `.cursor/rules/automation-standards.mdc` and e.g. `docs/PCG_VARIABLES_NO_ACCESS.md`).

- **Session continuity:** Read `docs/SESSION_LOG.md` at task start to load prior context. Append a summary at task end. See `.cursor/rules/07-ai-agent-behavior.mdc` (Session Continuity, AI Agent Checklist).
