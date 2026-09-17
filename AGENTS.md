# HomeWorld – Agent context

## MVP canon (read first)

| Path | Role |
|------|------|
| **[START_HERE.md](START_HERE.md)** | Swarm entry — Human Lead gates, Conductor boot |
| **`Docs/`** (capital D) | **Signed MVP product canon** — GDD, art bible, export table, audit WAVEs ([Docs/README.md](Docs/README.md)) |
| **`docs/`** (lowercase) | UE 5.7 engineering — setup, PCG, automation, known errors ([docs/README.md](docs/README.md)) |

**Do not treat** [VisionBoard/MVP/](VisionBoard/MVP/README.md) or [docs/Automation/AGENT_COMPANY.md](docs/Automation/AGENT_COMPANY.md) as MVP product canon — see quarantine pointers there. Long-horizon theme/stack: [VisionBoard/Core/VISION.md](VisionBoard/Core/VISION.md).

---

**Project:** HomeWorld — Unreal Engine 5.7 game (Open World / World Partition). Targets UE 5.7 (compatible with 5.7.x, including 5.7.3). Theme: "Love as Epic Quest"; Act 1 focus is lone wanderer (explore → fight → build). **Lock:** Engine 5.7 only; platform PC + Steam Early Access; do not add engine or platform variants without team decision.

**Programmatic by default:** Prefer C++ (and Python automation) over Blueprints. New gameplay systems, movement, input, abilities, and core logic are implemented in C++; Blueprint is for content, level design, and designer overrides only. For abilities: implement logic in a C++ ability subclass (e.g. `UHomeWorldInteractAbility`) and reparent the GA_* Blueprint to that class so no Blueprint graph wiring is required. See [docs/CONVENTIONS.md](docs/CONVENTIONS.md) for the code-first checklist and C++ vs Blueprint split.

**Code:** C++ lives in `Source/HomeWorld/`. Default pawn: `AHomeWorldCharacter`; default game mode: `AHomeWorldGameMode`. Both use Enhanced Input for movement and look.

**Stack (enabled plugins):** Enhanced Input, PCG, Gameplay Abilities, Steam Sockets, Day Sequence. For Week 2 family agents, enable UE 5.7 recommended Mass Entity + Mass AI, StateTree, ZoneGraph, SmartObjects (see [docs/SETUP.md](docs/SETUP.md)). Config in `Config/`; project layout and rules in `.cursor/rules/` (Unreal C++, Blueprint, project).

**MCP-first development:** When the Unreal Editor is running and MCP tools are connected (unrealMCP), prefer live Editor manipulation via MCP over writing scripts or giving manual instructions. See `.cursor/rules/09-mcp-workflow.mdc` and [docs/Setup/MCP_SETUP.md](docs/Setup/MCP_SETUP.md). For using external LLMs to generate Editor automation scripts, see [docs/Automation/EXTERNAL_AI_AUTOMATION.md](docs/Automation/EXTERNAL_AI_AUTOMATION.md).

**Parallel plugin:** When the agent sees a need for web search, URL extraction, deep research, or list enrichment, it recommends you run the matching command (`/parallel-search`, `/parallel-extract`, `/parallel-research`, `/parallel-enrich`) and paste the result; the agent then interprets and integrates.

**Industry standards (MVP):** [docs/IndustryStandards/INDUSTRY_STANDARDS_FOR_MVP_WORLD_AND_CHARACTERS.md](docs/IndustryStandards/INDUSTRY_STANDARDS_FOR_MVP_WORLD_AND_CHARACTERS.md) — industry-standard approaches for game world, 2D→character, and characters/monsters with MVP commit decisions.

**Session ops (not MVP GDD):** **Swarm/Conductor:** resume from latest [Docs/handoffs/SESSION_HANDOFF_*.md](Docs/handoffs/) + [docs/SESSION_SUMMARY.md](docs/SESSION_SUMMARY.md) + [swarm/PHASE_BOARD.md](swarm/PHASE_BOARD.md) at session start (not full SESSION_LOG by default). **Do not rewrite all SESSION_SUMMARY history** — append only ([swarm/SWARM_OPS.md](swarm/SWARM_OPS.md) §13). **Legacy task lists (quarantine):** [docs/TaskLists/DAILY_STATE.md](docs/TaskLists/DAILY_STATE.md), [docs/SESSION_LOG.md](docs/SESSION_LOG.md). **Product canon** for the signed slice is **`Docs/`** (see [Docs/08_AUDIT_UPGRADE_STRATEGY.md](Docs/08_AUDIT_UPGRADE_STRATEGY.md)). Pre-swarm 30-day lists and VisionBoard/MVP gap docs are **quarantine** — do not treat as GDD.

**Daily workflow:** **Swarm/HS track:** read latest `Docs/handoffs/SESSION_HANDOFF_*.md` + SESSION_SUMMARY + PHASE_BOARD; append SESSION_SUMMARY at end (no full rewrite). **Legacy:** DAILY_STATE + append SESSION_LOG.

**Feature development (policy):** When developing a **new feature**, research Epic/UE docs and best practices first; **follow tutorials first**, then expand. See .cursor/rules/07-ai-agent-behavior.mdc (Feature development: research and tutorials first).

**Compound Engineering plugin:** The plugin is installed; **recommending its commands when appropriate is policy**. When a task is a good use case for a plugin workflow (plan, review, changelog, docs lookup, etc.), recommend the corresponding slash command instead of doing that workflow yourself. The situation-to-command mapping is in [.cursor/rules/10-compound-engineering.mdc](.cursor/rules/10-compound-engineering.mdc). Use **context7** MCP for up-to-date library/framework docs when relevant. Optional one-time: run `/setup` in Cursor to configure review agents for this project.

## DevEnvTemplate (adopted layers)

HomeWorld vendors [DevEnvTemplate/](DevEnvTemplate/) as a **gitlink** (pinned SHA — registry: [config/devenv-template-pin.json](config/devenv-template-pin.json)) and adopts these layers:

| Layer | Status |
| ----- | ------ |
| **Agent context** | `.agents/skills/` (core), `.agents/skills-extras/` (opt-in catalog), stack rules `21-unreal-engine.mdc` / `22-unreal-editor-ui.mdc` |
| **Operational memory** | `docs/KNOWN_ERRORS.md`, `docs/Automation/AUTOMATION_GAPS.md` (canonical), `docs/operational/automation-gaps.md` (pointer), `docs/DOCS_LAYOUT.md`, `docs/human-use/` (steer / taste / test; [cursor-cannot](docs/human-use/cursor-cannot/README.md)) |
| **Doctor** | Nested under `DevEnvTemplate/` (not `.devenv/`); `npm run doctor` / `doctor:build` / `sync` from repo root |

**Accepted declines (do not re-litigate every session):**

- Keep HomeWorld **always-applied** Cursor rules (`00–20`, `ue57-*`, etc.) until a dedicated migration to AGENTS.md + skills; template retires those for *new* adoptions only.
- Do **not** require Node 24+ on the host for day-to-day UE work; doctor may warn `EBADENGINE` under Node 22 — accepted for now.
- Do **not** vendor a second checkout under `.devenv/`; `DevEnvTemplate/` is the doctor root.
- Do **not** add ESLint / TypeScript unit-test gates for the game host; doctor “Node stack” criticals for missing TS/ESLint/JS tests are **accepted declines** (this repo is UE 5.7 + Python automation). Full matrix: [docs/Setup/DOCTOR_POLICY.md](docs/Setup/DOCTOR_POLICY.md).
- Automation gaps for game systems stay in [docs/Automation/AUTOMATION_GAPS.md](docs/Automation/AUTOMATION_GAPS.md), not the template stub.

The human **steers**, **makes taste**, and **tests**; the agent executes. See
[docs/human-use/OWNERSHIP.md](docs/human-use/OWNERSHIP.md). Do not invent a human
decision or a product listed under [cursor-cannot](docs/human-use/cursor-cannot/README.md).

Refresh layers: `npm run sync` (dry-run) then `npm run sync:apply`. Details: [docs/Setup/CURSOR_DEV.md](docs/Setup/CURSOR_DEV.md).

## MVP lookdev swarm (on demand)

Blender-first MVP production kit: canon in **`Docs/`**, kits in **`Lib/`**, coordination in **`swarm/`**. **Start:** [START_HERE.md](START_HERE.md) → Conductor chat → phase gates (`APPROVE P0` … `APPROVE P7`). **Process:** [swarm/SWARM_OPS.md](swarm/SWARM_OPS.md) (Human Use, evidence gates, explicit-path git staging, KNOWN_ERRORS / AUTOMATION_GAPS). Specialists in [`.cursor/agents/`](.cursor/agents/) load **on demand** when Conductor spawns a role — not always-on; separate from the UE automation company unless explicitly invoked.

## Dev environment setup

1. Install UE 5.7, clone this repo, init DevEnvTemplate: `git submodule update --init --recursive DevEnvTemplate` → `npm run doctor:build` once → `npm run doctor:ue` (UE host exit code; see [docs/Setup/CURSOR_DEV.md](docs/Setup/CURSOR_DEV.md), [Docs/13b_HR2_B_COLD_CLONE.md](Docs/13b_HR2_B_COLD_CLONE.md)).
2. Run `Setup-MCP.bat` (one-time MCP bridge install).
3. **Build → Editor → MCP chain:** Run `.\Tools\Safe-Build.ps1` (closes Editor if needed, then builds — see [docs/Setup/BUILD_POLICY.md](docs/Setup/BUILD_POLICY.md)).
4. Open Unreal Editor (`HomeWorld.uproject`), restart Cursor, verify MCP green dot (port 55557 — [docs/Setup/MCP_SETUP.md](docs/Setup/MCP_SETUP.md)).
5. See [docs/SETUP.md](docs/SETUP.md) for the full checklist. **Cloud agents:** no UE/MCP on Linux VM — see [docs/Setup/WINDOWS_BRIDGE.md](docs/Setup/WINDOWS_BRIDGE.md).

**Enhanced Input** is applied automatically when the Editor loads (`Content/Python/init_unreal.py`). You do not need to run `setup_enhanced_input.py` unless movement still fails (troubleshooting).

## Commands

Exact invocations the agent should use (see [docs/SETUP.md](docs/SETUP.md) and [docs/PCG/PCG_SETUP.md](docs/PCG/PCG_SETUP.md) for more):

### Build → Editor → MCP (canonical agent chain)

| Step | Action | Doc |
|------|--------|-----|
| 1 | **`.\Tools\Safe-Build.ps1`** from repo root (closes Editor if running, then builds) | [BUILD_POLICY.md](docs/Setup/BUILD_POLICY.md), [EDITOR_BUILD_PROTOCOL.md](docs/Editor/EDITOR_BUILD_PROTOCOL.md) |
| 2 | Open **Unreal Editor** (`HomeWorld.uproject`) | [SETUP.md](docs/SETUP.md) |
| 3 | Restart Cursor; confirm **MCP green dot** (UnrealMCP port 55557) | [MCP_SETUP.md](docs/Setup/MCP_SETUP.md) |
| 4 | Use MCP tools or `execute_python_script` for Editor work | [09-mcp-workflow.mdc](.cursor/rules/09-mcp-workflow.mdc) |

**Agents and automation:** Always use **Safe-Build**, never `Build-HomeWorld.bat` directly. **Humans** with Editor already closed may use `Build-HomeWorld.bat` (Safe-Build wraps it). **Cloud agents** (no UE): open PR → optional self-hosted `ci.yml` for C++ → Windows **DESKTOP-21CT3H0** for Editor/MCP — [WINDOWS_BRIDGE.md](docs/Setup/WINDOWS_BRIDGE.md).

- **C++ build (agents):** **`.\Tools\Safe-Build.ps1`** only — see chain above.
- **Python script in Editor:** From project root, `py "Content/Python/<script>.py"`; or via MCP: `execute_python_script("<script>.py")` (paths relative to `Content/Python/`).
- **Python tests:** Editor: Tools > Test Automation (discovers `Content/Python/tests/test_*.py`).
- **PIE validation:** MCP `execute_python_script("pie_test_runner.py")`, then read `Saved/pie_test_results.json`.
- **Host automation:** Set `UE_EDITOR` to UnrealEditor.exe, then from project root run `py Content/Python/run_ue_automation.py`; optional `capture_editor_screenshot.py` for screenshots (requires PyAutoGUI). See [docs/Automation/FULL_AUTOMATION_RESEARCH.md](docs/Automation/FULL_AUTOMATION_RESEARCH.md) (Implementation Phase 2).
- **VS_MVP slice setup:** Primary playable path is **VS_MVP** (`/Game/HomeWorld/Maps/VS_MVP/`). Run `bootstrap_project.py` or `batch_import_asset_creation.py` + `place_vs_mvp_markers.py` (Editor or MCP). Legacy DemoMap/Homestead maps were **removed WAVE F** — see [Docs/08_AUDIT_SIGN_OFF.md](Docs/08_AUDIT_SIGN_OFF.md).
- **MVP swarm (product direction):** [swarm/SWARM_OPS.md](swarm/SWARM_OPS.md) + Conductor — [START_HERE.md](START_HERE.md). Pre-swarm agent-company loop **removed WAVE F** — stub at [docs/Automation/AGENT_COMPANY.md](docs/Automation/AGENT_COMPANY.md).
- **Refine rules and strategy from runs:** All agent runs (main, fix, loop-breaker) and errors are recorded in Saved/Logs/agent_run_history.ndjson and automation_errors.log. Use them to update .cursor/rules, KNOWN_ERRORS.md, and development strategy over time. See [docs/Automation/AUTOMATION_REFINEMENT.md](docs/Automation/AUTOMATION_REFINEMENT.md).
- **Cost/token tracking:** Run history includes `model` per run for cost attribution; optional `tokens`/`cost` when the CLI or a tracker exposes usage. Use Cursor billing or external trackers until then. See [docs/Automation/AUTOMATION_COST_TRACKING.md](docs/Automation/AUTOMATION_COST_TRACKING.md).
- **Editor Output Log (Fixer/Guardian):** On main-loop failure the Watcher captures Saved/Logs/editor_output_full.txt (unfiltered) and editor_output_filtered.txt (development-relevant). Fixer reads the filtered log by default; **if previous fix round(s) did not resolve the issue, read the unfiltered log** (editor_output_full.txt) so the filter cannot hide the error. See [docs/Automation/AUTOMATION_EDITOR_LOG.md](docs/Automation/AUTOMATION_EDITOR_LOG.md).
- **Project commands:** Reusable workflows in `.cursor/commands/` are available via `/` in chat (e.g. `/run-tests-and-fix`, `/create-pr`, `/review-changes`).
- **Project skills:** Domain skills in `.cursor/skills/` (e.g. pcg-validate, ue57-api-check) are available via `/` in chat. **Primary slice:** VS_MVP + Docs/04 import — see [Maps/VS_MVP/README.md](Maps/VS_MVP/README.md). Legacy demo-map/homestead skills reference removed WAVE F assets.
- **UE 5.7 API/plugin work:** Before changing C++, Blueprint, PCG, or plugin code, check [.cursor/rules/unreal-cpp.mdc](.cursor/rules/unreal-cpp.mdc) (pitfalls table) and [docs/KNOWN_ERRORS.md](docs/KNOWN_ERRORS.md). For **PCG graph or node changes**, also check [docs/PCG/PCG_BEST_PRACTICES.md](docs/PCG/PCG_BEST_PRACTICES.md) and [docs/PCG/PCG_VARIABLES_NO_ACCESS.md](docs/PCG/PCG_VARIABLES_NO_ACCESS.md). See [docs/UE/UE57_TECH.md](docs/UE/UE57_TECH.md) for the full UE 5.7 tech entry point.
- **Unreal Engine information (all):** Use **only UE 5.7–specific sources** for API, Editor UI, plugins, and docs (Epic 5.7 docs, docs/UE/UE57_TECH.md, docs/UE57_EDITOR_UI.md, KNOWN_ERRORS). Do not rely on training data or other engine versions. See [.cursor/rules/ue57-sources.mdc](.cursor/rules/ue57-sources.mdc). Editor UI: [ue57-editor-ui.mdc](.cursor/rules/ue57-editor-ui.mdc), [docs/UE/UE57_EDITOR_UI.md](docs/UE/UE57_EDITOR_UI.md).
- **Full automation stack:** Programmatic + GUI automation (key clickers, screenshotters, orchestration) and tool catalog: [docs/Automation/FULL_AUTOMATION_RESEARCH.md](docs/Automation/FULL_AUTOMATION_RESEARCH.md).
- **Active coordination (post-audit):** [swarm/SWARM_OPS.md](swarm/SWARM_OPS.md) + Conductor — [START_HERE.md](START_HERE.md). Cloud-agent packets: [swarm/CLOUD_AGENT_PACKET.md](swarm/CLOUD_AGENT_PACKET.md). Harness refine: [Docs/11_SWARM_HARNESS_REFINE.md](Docs/11_SWARM_HARNESS_REFINE.md).
- **Quarantine — pre-swarm agent loop:** `Start-AllAgents*`, `run_automation_cycle.py`, start-automation-cycle command — **removed WAVE F**. History only: [docs/Automation/AGENT_COMPANY.md](docs/Automation/AGENT_COMPANY.md), [.cursor/rules/19-automation-cycle.mdc](.cursor/rules/19-automation-cycle.mdc). Do not resurrect deleted Tools.
- **Host automation (MCP):** Prefer MCP `execute_python_script` on **Windows Editor**; see [docs/Automation/FULL_AUTOMATION_RESEARCH.md](docs/Automation/FULL_AUTOMATION_RESEARCH.md). Cloud agents: [docs/Setup/WINDOWS_BRIDGE.md](docs/Setup/WINDOWS_BRIDGE.md).

## Boundaries

- **Never:** Commit secrets, API keys, or `.env`; edit `Plugins/UnrealMCP/` or `Saved/` (they are not project code); change engine version (UE 5.7 only) or target platform (PC + Steam Early Access) without a team decision.
- **Ask first:** CI/schema changes (`.github/workflows/`, JSON schema files), adding or upgrading dependencies, or broad refactors that touch many modules.
- **Game content:** Automation preserves existing content; create-if-missing, update-in-place. See [.cursor/rules/18-game-development-principles.mdc](.cursor/rules/18-game-development-principles.mdc).
- **Combat and night encounters:** **Placeholder only** until a full vision board pass on combat mechanics — placeholder abilities, UI, and spawn stubs are fine; avoid deep combat system work. **We do not kill foes** — combat **strips them of their sin** and **converts them to their "loved" version**; converted monsters can become **vendors**, **helpers**, **quest givers**, or **homestead pets/workers**. **Combat variety:** Defend (waves at home) = defenses + **ranged** or **ground AOE**; planetoid (away from home) = **combos** + **single-target**; end-game = use either style in either situation. Night encounters: waves at home + packs on planetoid + bosses at key points; goal = limited time per night, clear planetoid in one night. **Planetoid and homestead:** Homestead lands on planetoid, you venture out; complete planetoid → move to another. See [VisionBoard/Core/VISION.md](VisionBoard/Core/VISION.md) § Day and night, § Combat variety.

## Testing

- **Automated (Python):** `PythonAutomationTest` plugin is enabled. Tests in `Content/Python/tests/` (named `test_*.py`) are auto-discovered. Run via Editor: Tools > Test Automation.
- **PIE tests:** `Content/Python/pie_test_runner.py` validates character spawn, ground contact, animation, and PCG. Run via MCP: `execute_python_script("pie_test_runner.py")`, then read `Saved/pie_test_results.json`.
- **Level loading and tests:** Level load + World Partition streaming can make tests flaky. Smart level loader and latent tests are implemented (see [docs/Testing/LEVEL_TESTING_PLAN.md](docs/Testing/LEVEL_TESTING_PLAN.md)). Optional PIE full-flow test: `test_level_pie_flow.py` (Tools > Test Automation).
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

[docs/SETUP.md](docs/SETUP.md) (includes validation checklist). [docs/SPEC_AND_PLAN.md](docs/SPEC_AND_PLAN.md) (plan-first and where to save plans). Cursor rules ship with the repo in `.cursor/rules/` — they are loaded automatically when the project is opened in Cursor. Key rules: `unreal-cpp.mdc` (C++ conventions + UE 5.7 API pitfalls), `08-project-context.mdc` (HomeWorld overview), `09-mcp-workflow.mdc` (MCP-first priorities), `19-docs-directory-structure.mdc` (place new docs in correct docs/ subdir per [docs/DOCS_LAYOUT.md](docs/DOCS_LAYOUT.md)), `20-full-automation-no-manual-steps.mdc` (full autonomy: no manual steps for the user; log gaps to [docs/Automation/AUTOMATION_GAPS.md](docs/Automation/AUTOMATION_GAPS.md)), `automation-standards.mdc` (Editor UI automation is the **default** when we have the ability to interact with the Editor UI automatically; manual is fallback only; if a step cannot be automated, log to AUTOMATION_GAPS.md). Always check [docs/KNOWN_ERRORS.md](docs/KNOWN_ERRORS.md) before making changes. **Full automation:** The agent does not expect or request manual work mid-session; use GUI automation (PyAutoGUI, ref images) where APIs are missing, and log any remaining gaps to [docs/Automation/AUTOMATION_GAPS.md](docs/Automation/AUTOMATION_GAPS.md) for future solution sessions.

- **Session continuity:** **Swarm/Conductor:** resume from `Docs/handoffs/SESSION_HANDOFF_*.md` + `docs/SESSION_SUMMARY.md` + `swarm/PHASE_BOARD.md` at start; append SESSION_SUMMARY at end (do not rewrite history). **Legacy UE task lists:** SESSION_LOG + DAILY_STATE. See `.cursor/rules/07-ai-agent-behavior.mdc` (Session Continuity) · [swarm/SWARM_OPS.md](swarm/SWARM_OPS.md) §13.
