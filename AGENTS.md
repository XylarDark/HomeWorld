# HomeWorld – Agent context

**Project:** HomeWorld — Unreal Engine 5.7 game (Open World / World Partition). Targets UE 5.7 (compatible with 5.7.x, including 5.7.3). Theme: "Love as Epic Quest"; Act 1 focus is lone wanderer (explore → fight → build). See [docs/workflow/VISION.md](docs/workflow/VISION.md) (theme, campaign, 7 sins/virtues, succession) and [docs/STACK_PLAN.md](docs/STACK_PLAN.md) for stack. **Lock:** Engine 5.7 only; platform PC + Steam Early Access; do not add engine or platform variants without team decision.

**Programmatic by default:** Prefer C++ (and Python automation) over Blueprints. New gameplay systems, movement, input, abilities, and core logic are implemented in C++; Blueprint is for content, level design, and designer overrides only. For abilities: implement logic in a C++ ability subclass (e.g. `UHomeWorldInteractAbility`) and reparent the GA_* Blueprint to that class so no Blueprint graph wiring is required. See [docs/CONVENTIONS.md](docs/CONVENTIONS.md) for the code-first checklist and C++ vs Blueprint split.

**Code:** C++ lives in `Source/HomeWorld/`. Default pawn: `AHomeWorldCharacter`; default game mode: `AHomeWorldGameMode`. Both use Enhanced Input for movement and look.

**Stack (enabled plugins):** Enhanced Input, PCG, Gameplay Abilities, Steam Sockets, Day Sequence. For Week 2 family agents, enable UE 5.7 recommended Mass Entity + Mass AI, StateTree, ZoneGraph, SmartObjects (see [SETUP.md](docs/SETUP.md)). Config in `Config/`; project layout and rules in `.cursor/rules/` (Unreal C++, Blueprint, project).

**MCP-first development:** When the Unreal Editor is running and MCP tools are connected (unrealMCP), prefer live Editor manipulation via MCP over writing scripts or giving manual instructions. See `.cursor/rules/09-mcp-workflow.mdc` and [docs/MCP_SETUP.md](docs/MCP_SETUP.md). For using external LLMs to generate Editor automation scripts, see [docs/EXTERNAL_AI_AUTOMATION.md](docs/EXTERNAL_AI_AUTOMATION.md).

**Parallel plugin:** When the agent sees a need for web search, URL extraction, deep research, or list enrichment, it recommends you run the matching command (`/parallel-search`, `/parallel-extract`, `/parallel-research`, `/parallel-enrich`) and paste the result; the agent then interprets and integrates.

**Current tasks:** [docs/workflow/README.md](docs/workflow/README.md) — workflow index; [docs/workflow/PROJECT_STATE_AND_TASK_LIST.md](docs/workflow/PROJECT_STATE_AND_TASK_LIST.md) — **project overview and task list** (work done + work not yet completed T1–T10); [docs/workflow/30_DAY_SCHEDULE.md](docs/workflow/30_DAY_SCHEDULE.md) — 30-day schedule; each task links to a detailed doc in `docs/tasks/`. **Task list policy:** When generating a new 10-task list, the split of implementation vs verification is **dynamic by development phase**. Read [docs/workflow/PROJECT_STATE_AND_TASK_LIST.md](docs/workflow/PROJECT_STATE_AND_TASK_LIST.md) §0 **Current development phase**: **Rapid prototyping** → more implementation (e.g. 7–8), fewer verification; **Prototype hardening** → balanced (e.g. 4–5 implementation, 5–6 verification). Maximize quality and quantity according to phase. See [docs/workflow/HOW_TO_GENERATE_TASK_LIST.md](docs/workflow/HOW_TO_GENERATE_TASK_LIST.md) § Task list composition.

**Daily workflow:** At session start the agent reads [docs/workflow/DAILY_STATE.md](docs/workflow/DAILY_STATE.md) (yesterday / today). You can prompt e.g. "What did we do yesterday and what do we need to do today?" At session end the agent updates DAILY_STATE (what was done → yesterday; next day's tasks → today; tomorrow preview) and appends [docs/SESSION_LOG.md](docs/SESSION_LOG.md).

**Feature development (policy):** When developing a **new feature**, research Epic/UE docs and best practices first; **follow tutorials first**, then expand. See .cursor/rules/07-ai-agent-behavior.mdc (Feature development: research and tutorials first).

**Compound Engineering plugin:** The plugin is installed; **recommending its commands when appropriate is policy**. When a task is a good use case for a plugin workflow (plan, review, changelog, docs lookup, etc.), recommend the corresponding slash command instead of doing that workflow yourself. The situation-to-command mapping is in [.cursor/rules/10-compound-engineering.mdc](.cursor/rules/10-compound-engineering.mdc). Use **context7** MCP for up-to-date library/framework docs when relevant. Optional one-time: run `/setup` in Cursor to configure review agents for this project.

## Dev environment setup

1. Install UE 5.7, clone this repo, open `HomeWorld.uproject`.
2. Run `Setup-MCP.bat` (one-time MCP bridge install).
3. Run `.\Tools\Safe-Build.ps1` to compile C++ (closes Editor automatically if needed; see docs/EDITOR_BUILD_PROTOCOL.md).
4. Open Editor, restart Cursor, verify MCP green dot in status bar.
5. See [docs/SETUP.md](docs/SETUP.md) for the full checklist.

**Enhanced Input** is applied automatically when the Editor loads (`Content/Python/init_unreal.py`). You do not need to run `setup_enhanced_input.py` unless movement still fails (troubleshooting).

## Commands

Exact invocations the agent should use (see [docs/SETUP.md](docs/SETUP.md) and [docs/PCG_SETUP.md](docs/PCG_SETUP.md) for more):

- **C++ build:** Use **`.\Tools\Safe-Build.ps1`** from project root so the Editor is closed automatically if running and build is retried once on Editor-related failure. Do not assume the user will close the Editor. See [docs/EDITOR_BUILD_PROTOCOL.md](docs/EDITOR_BUILD_PROTOCOL.md). Alternatively `py Content/Python/run_automation_cycle.py` (without `--no-build`) applies the same protocol.
- **Python script in Editor:** From project root, `py "Content/Python/<script>.py"`; or via MCP: `execute_python_script("<script>.py")` (paths relative to `Content/Python/`).
- **Python tests:** Editor: Tools > Test Automation (discovers `Content/Python/tests/test_*.py`).
- **PIE validation:** MCP `execute_python_script("pie_test_runner.py")`, then read `Saved/pie_test_results.json`.
- **Host automation:** Set `UE_EDITOR` to UnrealEditor.exe, then from project root run `py Content/Python/run_ue_automation.py`; optional `capture_editor_screenshot.py` for screenshots (requires PyAutoGUI). See [docs/FULL_AUTOMATION_RESEARCH.md](docs/FULL_AUTOMATION_RESEARCH.md) (Implementation Phase 2).
- **Demo map setup:** Primary demo map is **DemoMap** (`/Game/HomeWorld/Maps/DemoMap`). Run `create_demo_from_scratch.py` (Editor or MCP). Create map first via File → New Level → Empty Open World → Save As; see [docs/DEMO_MAP.md](docs/DEMO_MAP.md).
- **Agent company (roles and continuity):** Developer (main loop), Fixer (on failure), Guardian (loop-breaker), Refiner (rules/strategy from run history), **Gap-Solver** (implements solutions for logged automation gaps). They keep each other accountable so development continues through errors. See [docs/AGENT_COMPANY.md](docs/AGENT_COMPANY.md).
- **Start all agents ("start agents" in chat):** When the user says "start agents", "run automation", or "start the loop", run **`.\Tools\Start-AllAgents-InNewWindow.ps1`** (capture by default). This opens a new window that uses **Run-AutomationWithCapture.ps1**: all terminal output goes to **Saved/Logs/automation_terminal_capture.log** and the window stays open until the user closes it. Or tell them to double-click **Start-AllAgents.bat** in project root. Never run Start-AllAgents.ps1 in the chat/integrated terminal.
- **Automation exit update:** When the user asks for an **automation update**, **check automation exit**, **what happened with the agents**, or **give me the automation update**, read **Saved/Logs/automation_exit_alert.md** (or automation_exit_alert.json). If the file exists, summarize it for the user (exit reason, exit code, round, pending tasks, last message). If the file is missing or unreadable, run `.\Tools\Get-AutomationStatus.ps1` or read Saved/automation_last_activity.json and Saved/Logs/automation_loop.log tail and give a short status. The loop writes this alert file automatically whenever it exits (success, stop, or error).
- **Watcher (fix-on-failure):** Run **`.\Tools\Watch-AutomationAndFix.ps1`** to run the automation loop and, when it fails, start the **Fixer**; after **3 fix rounds** (default) the watcher invokes the **Guardian** and reports (Saved/Logs/automation_loop_breaker_report.md). See docs/AUTOMATION_LOOP_UNTIL_DONE.md (including **Thresholds before we report to you**).
- **Guardian (loop-breaker):** Run **`.\Tools\Guard-AutomationLoop.ps1`** to check for a repeating failure loop; if so, run the Guardian agent to resolve or write Saved/Logs/automation_loop_breaker_report.md. The watcher invokes this automatically when the same exit code recurs.
- **Refiner (rules from runs):** Run **`.\Tools\Run-RefinerAgent.ps1`** (or **refine-rules-from-runs** command) to process run history and update .cursor/rules, KNOWN_ERRORS.md, and strategy so the same failures don't recur.
- **Gap-Solver (implement gap solutions):** Run **`.\Tools\Run-GapSolverAgent.ps1`** (or **run-gap-solver** command) when a gap is logged in docs/AUTOMATION_GAPS.md or after a Guardian report that mentions gaps. The Gap-Solver implements programmatic or GUI-automation solutions and updates AUTOMATION_GAPS and GAP_SOLUTIONS_RESEARCH. See [docs/AGENT_COMPANY.md](docs/AGENT_COMPANY.md).
- **Refine rules and strategy from runs:** All agent runs (main, fix, loop-breaker) and errors are recorded in Saved/Logs/agent_run_history.ndjson and automation_errors.log. Use them to update .cursor/rules, KNOWN_ERRORS.md, and development strategy over time. See [docs/AUTOMATION_REFINEMENT.md](docs/AUTOMATION_REFINEMENT.md).
- **Cost/token tracking:** Run history includes `model` per run for cost attribution; optional `tokens`/`cost` when the CLI or a tracker exposes usage. Use Cursor billing or external trackers until then. See [docs/AUTOMATION_COST_TRACKING.md](docs/AUTOMATION_COST_TRACKING.md).
- **Editor Output Log (Fixer/Guardian):** On main-loop failure the Watcher captures Saved/Logs/editor_output_full.txt (unfiltered) and editor_output_filtered.txt (development-relevant). Fixer reads the filtered log by default; **if previous fix round(s) did not resolve the issue, read the unfiltered log** (editor_output_full.txt) so the filter cannot hide the error. See [docs/AUTOMATION_EDITOR_LOG.md](docs/AUTOMATION_EDITOR_LOG.md).
- **Project commands:** Reusable workflows in `.cursor/commands/` are available via `/` in chat (e.g. `/run-tests-and-fix`, `/create-pr`, `/review-changes`).
- **Project skills:** Domain skills in `.cursor/skills/` (e.g. demo-map-setup, homestead-setup, pcg-validate, ue57-api-check, **automation-gap-solutions**) are available via `/` in chat. **Primary demo map:** DemoMap and **create_demo_from_scratch.py**; see [docs/DEMO_MAP.md](docs/DEMO_MAP.md). Use **demo-map-setup** for DemoMap + PCG. For tasks touching logged automation gaps (Level Streaming/portal, State Tree, PCG no-access), use **automation-gap-solutions** skill and [.cursor/rules/19-automation-gaps.mdc](.cursor/rules/19-automation-gaps.mdc).
- **PCG Generate nothing:** Use the **pcg-validate** skill and [docs/PCG_SETUP.md](docs/PCG_SETUP.md) section "Generate produces nothing (checklist)"; check Output Log for **LogPCG** and **No surfaces found**. For a short, tutorial-aligned flow and volume sizing (DemoMap), see [docs/PCG_QUICK_SETUP.md](docs/PCG_QUICK_SETUP.md).
- **UE 5.7 API/plugin work:** Before changing C++, Blueprint, PCG, or plugin code, check [.cursor/rules/unreal-cpp.mdc](.cursor/rules/unreal-cpp.mdc) (pitfalls table) and [docs/KNOWN_ERRORS.md](docs/KNOWN_ERRORS.md). For **PCG graph or node changes**, also check [docs/PCG_BEST_PRACTICES.md](docs/PCG_BEST_PRACTICES.md) and [docs/PCG_VARIABLES_NO_ACCESS.md](docs/PCG_VARIABLES_NO_ACCESS.md). See [docs/UE57_TECH.md](docs/UE57_TECH.md) for the full UE 5.7 tech entry point.
- **Unreal Engine information (all):** Use **only UE 5.7–specific sources** for API, Editor UI, plugins, and docs (Epic 5.7 docs, docs/UE57_TECH.md, docs/UE57_EDITOR_UI.md, KNOWN_ERRORS). Do not rely on training data or other engine versions. See [.cursor/rules/ue57-sources.mdc](.cursor/rules/ue57-sources.mdc). Editor UI: [ue57-editor-ui.mdc](.cursor/rules/ue57-editor-ui.mdc), [docs/UE57_EDITOR_UI.md](docs/UE57_EDITOR_UI.md).
- **Full automation stack:** Programmatic + GUI automation (key clickers, screenshotters, orchestration) and tool catalog: [docs/FULL_AUTOMATION_RESEARCH.md](docs/FULL_AUTOMATION_RESEARCH.md).
- **Automatic development cycle:** Use the **start-automation-cycle** command (or prompt: "Start automation cycle. Desires: …"). **Agent task list (vision-aligned):** [docs/workflow/AGENT_TASK_LIST.md](docs/workflow/AGENT_TASK_LIST.md) — agents fetch the first pending task from this list. Task list (prior cycle): [docs/workflow/CYCLE_TASKLIST.md](docs/workflow/CYCLE_TASKLIST.md); state: [docs/workflow/CYCLE_STATE.md](docs/workflow/CYCLE_STATE.md). Say "Continue" to run the next task or retry. When the cycle is active, follow [.cursor/rules/19-automation-cycle.mdc](.cursor/rules/19-automation-cycle.mdc). See [docs/FULL_AUTOMATION_RESEARCH.md](docs/FULL_AUTOMATION_RESEARCH.md) §7.
- **Loop until all 30 days done:** The agent cannot start a new session by itself. To run session-after-session until every day is implementation-complete: each session writes [docs/workflow/NEXT_SESSION_PROMPT.md](docs/workflow/NEXT_SESSION_PROMPT.md); you (or external tooling) start the next chat and paste that prompt. The loop runs a C++ build after each successful round when Source/ or *.Build.cs are modified (build failure invokes the Fixer); the Developer must validate in Editor when the task requires it and exit non-zero on validation failure so the debug loop runs. Implementation status: [docs/workflow/30_DAY_IMPLEMENTATION_STATUS.md](docs/workflow/30_DAY_IMPLEMENTATION_STATUS.md). See [docs/AUTOMATION_LOOP_UNTIL_DONE.md](docs/AUTOMATION_LOOP_UNTIL_DONE.md).
- **Orchestrator (full-auto):** From project root run `py Content/Python/run_automation_cycle.py --task N` for build → scripts (from config) → run_ue_automation; use `--launch-and-wait` to start Editor and wait for MCP port 55557, `--close-editor` to close gracefully. See [README-Automation.md](README-Automation.md) and [docs/FULL_AUTOMATION_RESEARCH.md](docs/FULL_AUTOMATION_RESEARCH.md) §9.

## Boundaries

- **Never:** Commit secrets, API keys, or `.env`; edit `Plugins/UnrealMCP/` or `Saved/` (they are not project code); change engine version (UE 5.7 only) or target platform (PC + Steam Early Access) without a team decision.
- **Ask first:** CI/schema changes (`.github/workflows/`, JSON schema files), adding or upgrading dependencies, or broad refactors that touch many modules.
- **Game content:** Automation preserves existing content; create-if-missing, update-in-place. See [.cursor/rules/18-game-development-principles.mdc](.cursor/rules/18-game-development-principles.mdc).
- **Combat and night encounters:** **Placeholder only** until a full vision board pass on combat mechanics — placeholder abilities, UI, and spawn stubs are fine; avoid deep combat system work. **We do not kill foes** — combat **strips them of their sin** and **converts them to their "loved" version**; converted monsters can become **vendors**, **helpers**, **quest givers**, or **homestead pets/workers**. **Combat variety:** Defend (waves at home) = defenses + **ranged** or **ground AOE**; planetoid (away from home) = **combos** + **single-target**; end-game = use either style in either situation. Night encounters: waves at home + packs on planetoid + bosses at key points; goal = limited time per night, clear planetoid in one night. **Planetoid and homestead:** Homestead lands on planetoid, you venture out; complete planetoid → move to another. See [docs/workflow/VISION.md](docs/workflow/VISION.md) § Day and night, § Combat variety.

## Testing

- **Automated (Python):** `PythonAutomationTest` plugin is enabled. Tests in `Content/Python/tests/` (named `test_*.py`) are auto-discovered. Run via Editor: Tools > Test Automation.
- **PIE tests:** `Content/Python/pie_test_runner.py` validates character spawn, ground contact, animation, and PCG. Run via MCP: `execute_python_script("pie_test_runner.py")`, then read `Saved/pie_test_results.json`.
- **Level loading and tests:** Level load + World Partition streaming can make tests flaky. Smart level loader and latent tests are implemented (see [docs/LEVEL_TESTING_PLAN.md](docs/LEVEL_TESTING_PLAN.md)). Optional PIE full-flow test: `test_level_pie_flow.py` (Tools > Test Automation).
- **CI:** GitHub Actions (`.github/workflows/validate.yml`) — Python lint, JSON schema checks, C++ header/source pairing, doc freshness.

## Code style

- **C++:** PascalCase types, camelCase locals; Unreal prefixes (`A`, `U`, `F`, `E`, `I`). Include own header first. See `.cursor/rules/unreal-cpp.mdc`.
- **Python:** PEP 8, type hints, 4-space indent. UE scripts must be idempotent (check-before-create). See `.cursor/rules/12-python.mdc`.
- **Commits:** Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`). See `.cursor/rules/04-git-workflow.mdc`.
- **Feature debug instrumentation and log-driven validation:** When implementing features, include a **robust, log-driven way to validate** that they work (entry/exit, user-triggered actions, success/fail in logs). The user must not have to prompt for logging to confirm implementation. See `.cursor/rules/16-feature-debug-instrumentation.mdc`.

## PR and commit guidelines

- Use Conventional Commits format for all commit messages.
- PowerShell shell: use `;` not `&&` for command chaining; use here-strings for multi-line commit messages.
- Pre-commit: lint, build check, no secrets, no `__pycache__` or temp JSON in tracked files.

## Security

- Never commit secrets, API keys, or `.env` files. Use `.env.example` for templates.
- `Saved/`, `Plugins/UnrealMCP/`, and `__pycache__/` are gitignored.
- Validate all external input at boundaries. See `.cursor/rules/02-security.mdc`.

## Setup and validation

[docs/SETUP.md](docs/SETUP.md) (includes validation checklist). [docs/SPEC_AND_PLAN.md](docs/SPEC_AND_PLAN.md) (plan-first and where to save plans). Cursor rules ship with the repo in `.cursor/rules/` — they are loaded automatically when the project is opened in Cursor. Key rules: `unreal-cpp.mdc` (C++ conventions + UE 5.7 API pitfalls), `08-project-context.mdc` (HomeWorld overview), `09-mcp-workflow.mdc` (MCP-first priorities), `20-full-automation-no-manual-steps.mdc` (full autonomy: no manual steps for the user; log gaps to `docs/AUTOMATION_GAPS.md`), `automation-standards.mdc` (attempt MCP/Python/GUI automation; if a step cannot be automated, log to AUTOMATION_GAPS.md). Always check `docs/KNOWN_ERRORS.md` before making changes. **Full automation:** The agent does not expect or request manual work mid-session; use GUI automation (PyAutoGUI, ref images) where APIs are missing, and log any remaining gaps to `docs/AUTOMATION_GAPS.md` for future solution sessions.

- **Session continuity:** Read `docs/SESSION_LOG.md` at task start to load prior context. Append a summary at task end. See `.cursor/rules/07-ai-agent-behavior.mdc` (Session Continuity, AI Agent Checklist).
