# HomeWorld – Agent context

## MVP canon (read first)

| Path | Role |
|------|------|
| **[START_HERE.md](../START_HERE.md)** | Swarm entry — Human Lead gates, Conductor boot |
| **[Docs/VISION_BOARD.md](VISION_BOARD.md)** | **Product canon. Read before scoping. Do not restate it.** Theme and the long horizon stay in `VisionBoard/Core/VISION.md`. `VisionBoard/MVP/` is outside prototype scope. |
| **[Docs/CANON_MAP.md](CANON_MAP.md)** | **Start here when you need to find the answer to something.** A topic-keyed index over this tree, machine-checked so it cannot go stale |
| **`Docs/` and `docs/`** | **One directory.** Product files and engineering files are separated by the canon map and by subdirectory, not by spelling. Index: [Docs/README.md](README.md). Engineering index: [docs/README_ENGINEERING.md](README_ENGINEERING.md). |

> **`Docs/` and `docs/` are ONE directory on this machine, not two trees.** Windows is
> case-insensitive: both spellings enumerate the same files. Subdirectories separate topics.
> Prototype vision is only `Docs/VISION_BOARD.md`. Either casing resolves in a cross-reference.
> Do not sync the two spellings. There is nothing to sync. Settled by
> Lead 2026-10-02; [DEC-0029](decisions/AGENT_DECISIONS.md#dec-0029).

**Do not treat** [VisionBoard/MVP/](../VisionBoard/MVP/README.md) or [docs/Automation/AGENT_COMPANY.md](Automation/AGENT_COMPANY.md) as MVP product canon — see quarantine pointers there. Long-horizon theme/stack: [VisionBoard/Core/VISION.md](../VisionBoard/Core/VISION.md).

---

**Project:** HomeWorld — Unreal Engine 5.8 game (Open World / World Partition). Targets UE 5.8 (compatible with 5.8.x). Theme: "Love as Epic Quest"; family is present from the start, and the prototype includes the camp rescue. Day is for gathering; night is for tending in spirit form. **Lock:** Engine 5.8 only; platform PC + Steam Early Access; do not add engine or platform variants without team decision. **Review trigger (2026-09-30):** 5.8 is the last *planned* UE5 release and a UE6 timeline is public, so this lock has a visible expiry — it stays until a team decision, but reassess when UE6 enters planning, or when 5.8 features this project depends on are still Experimental past their stabilization window. Recorded in [Docs/handoffs/HR4_A_SKILL_EVAL.md](handoffs/HR4_A_SKILL_EVAL.md).

**Programmatic by default:** Prefer C++ (and Python automation) over Blueprints. New gameplay systems, movement, input, abilities, and core logic are implemented in C++; Blueprint is for content, level design, and designer overrides only. For abilities: implement logic in a C++ ability subclass (e.g. `UHomeWorldInteractAbility`) and reparent the GA_* Blueprint to that class so no Blueprint graph wiring is required. See [docs/CONVENTIONS.md](CONVENTIONS.md) for the code-first checklist and C++ vs Blueprint split.

**Code:** C++ lives in `Source/HomeWorld/`. Default pawn: `AHomeWorldCharacter`; default game mode: `AHomeWorldGameMode`. Both use Enhanced Input for movement and look.

**Stack (enabled plugins):** Enhanced Input, PCG, Gameplay Abilities, Steam Sockets, Day Sequence. For Week 2 family agents, enable UE 5.8 recommended MassGameplay + MassAI, StateTree, ZoneGraph, SmartObjects (see [docs/SETUP.md](SETUP.md)). Config in `Config/`; project layout and rules in `.cursor/rules/` (Unreal C++, Blueprint, project).

**Context discipline:** past ~60k tokens of conversation you are in what the Agentic Engineering material calls the **dumb zone** - instruction-following and recall both degrade. Above it: write state to a .md file, summarise open threads and next actions there, and start a fresh session from that file. Do not carry the context forward and hope. Split research across agents rather than deepening one thread.

**Steer gate:** You cannot take responsibility for a change you cannot explain, you cannot see the playtest, and you cannot decide taste. A clean log is not evidence. Before an edit that sets feel, scope, or done, load `.agents/skills/steer-gate/SKILL.md` and [Docs/handoffs/SLICE_SESSION.md](handoffs/SLICE_SESSION.md). Name the limitation, numbered options, then stop. Ownership map: [docs/human-use/OWNERSHIP.md](human-use/OWNERSHIP.md).


**MCP-first development:** When the Unreal Editor is running and MCP tools are connected (unrealMCP), prefer live Editor manipulation via MCP over writing scripts or giving manual instructions. See `.cursor/rules/09-mcp-workflow.mdc` and [docs/Setup/MCP_SETUP.md](Setup/MCP_SETUP.md). For using external LLMs to generate Editor automation scripts, see [docs/Automation/EXTERNAL_AI_AUTOMATION.md](Automation/EXTERNAL_AI_AUTOMATION.md).

**Parallelism:** research, read-only investigation and low-stakes maintenance may run alongside each other. **Writes serialise** - one significant change under review at a time. Two agents must not edit the same files in one tree, and an agent finding uncommitted tracked changes it did not make must stop and report rather than commit or stash them. Check with `npm run tree:check`.

**Industry standards (MVP):** [docs/IndustryStandards/INDUSTRY_STANDARDS_FOR_MVP_WORLD_AND_CHARACTERS.md](IndustryStandards/INDUSTRY_STANDARDS_FOR_MVP_WORLD_AND_CHARACTERS.md) — industry-standard approaches for game world, 2D→character, and characters/monsters with MVP commit decisions.

**Session ops (not MVP GDD):** **Swarm/Conductor:** resume from latest [Docs/handoffs/SESSION_HANDOFF_*.md](handoffs) + [docs/SESSION_NOW.md](SESSION_NOW.md) + [swarm/PHASE_BOARD.md](../swarm/PHASE_BOARD.md) at session start. Do not open [docs/history/SESSION_LOG.md](history/SESSION_LOG.md) to start. Append the next block to `SESSION_NOW.md` only ([swarm/SWARM_OPS.md](../swarm/SWARM_OPS.md) §13). **Legacy task lists (quarantine):** [docs/TaskLists/DAILY_STATE.md](TaskLists/DAILY_STATE.md). Open [docs/SESSION_LOG.md](SESSION_LOG.md) only when a past incident is named. It is not a start read. **Product canon** for the signed slice is **`Docs/`** (see [Docs/08_AUDIT_UPGRADE_STRATEGY.md](08_AUDIT_UPGRADE_STRATEGY.md)). Pre-swarm 30-day lists and VisionBoard/MVP gap docs are **quarantine** — do not treat as GDD.

**Uncle Bob names, already owned here.** Do not install [uncle-bob](https://github.com/robert-hoffmann/uncle-bob) and do not add `.ub-workflows/`. `ub-quality` is [AGENTS.md](../AGENTS.md) plus the rule that matches the file being edited. `ub-authoring` is the one-sentence `description` on each skill in [.agents/skills](../.agents/skills). `ub-workflow` is [Docs/context/SESSION_START.md](../Docs/context/SESSION_START.md): a named handoff, queue, or file stops; "what next" is the production read list; a multi-step slice is a handoff plus [docs/SESSION_NOW.md](SESSION_NOW.md). Swarm stays [START_HERE.md](../START_HERE.md). Their reviewed, flow, auto, and continuous modes are not used. Feel and test stay with Luke. `ub-governance` is [verification-evidence](../.agents/skills/verification-evidence/SKILL.md). Ordinary playtest evidence stays the queue result and the named log line. That skill opens only when a check could pass without measuring its subject.

**Daily workflow:** **Swarm/HS track:** read latest `Docs/handoffs/SESSION_HANDOFF_*.md` + `docs/SESSION_NOW.md` + PHASE_BOARD; append `SESSION_NOW.md` at end. **Legacy:** DAILY_STATE. Open `docs/SESSION_LOG.md` only when a past incident is named. It is not a start read.

**Feature development (policy):** When developing a **new feature**, research Epic/UE docs and best practices first; **follow tutorials first**, then expand.

**Research:** when a task needs current external facts, use the available research tooling and cite a primary source. Details in [docs/Automation/FULL_AUTOMATION_RESEARCH.md](Automation/FULL_AUTOMATION_RESEARCH.md). A request to check or optimize the harness opens `harness-check`.

## DevHarness (adopted layers)

HomeWorld vendors [UserHarness/](../UserHarness) as a **gitlink** to **DevHarness** (product rename 2026-09-19 — pinned SHA; registry: [Config/userharness-pin.json](../Config/userharness-pin.json)) and adopts these layers:

| Layer | Status |
| ----- | ------ |
| **Agent context** | `.agents/skills/` (core), `.agents/skills-extras/` (opt-in catalog), stack rules `21-unreal-engine.mdc` / `ue58-editor-ui.mdc` |
| **Architecture A–E** | `.agents/skills-extras/architecture-trade-offs-design-depth/` — opt-in copy of DET extras writer (blob `107a5118c95c1bf0b1b3d1755796632bff41b535`; [SYNC.md](../.agents/skills-extras/architecture-trade-offs-design-depth/SYNC.md)). Load before inventing boundaries/APIs; cite only, no fork |
| **Skill load** | Discoverable catalog is `.agents/skills/` only. `.cursor/skills/` is not a second catalog. Extras and A–E full are cite/copy-in only — never paste skill bodies here. |
| **Research prompts** | [Docs/handoffs/RESEARCH_PROMPT_CONTRACT.md](handoffs/RESEARCH_PROMPT_CONTRACT.md) — Conductor paste-ready ROLE/CONTEXT/CANON/ASK/NON-GOALS/DONE-WHEN/child Research. Design and studio lookups: one file per body, opened only while that research is the task. |
| **Operational memory** | `docs/KNOWN_ERRORS.md`, `docs/Automation/AUTOMATION_GAPS.md` (canonical), `docs/operational/automation-gaps.md` (pointer), `docs/DOCS_LAYOUT.md`, `docs/human-use/` (steer / taste / test; [cursor-cannot](human-use/cursor-cannot/README.md)) |
| **Doctor** | Nested under `UserHarness/` (not `.devenv/`); `npm run doctor` / `doctor:build` / `sync` from repo root |

### Loop engineering (`/loop-engineer`, global skill)

Two orchestration systems coexist. They are **nested, not alternatives**:

| Tool | Layer | Role |
| ---- | ----- | ---- |
| **GSD** | Architecture, top-down | Cursor commands: `/gsd-discuss-phase`, `/gsd-plan-phase`, `/gsd-execute-phase`, `/gsd-verify-work`. Plans a phase behind human gates. |
| **loop-engineer** | Implementation, bottom-up | Executes **one** goal to a machine-checkable stop condition. Never plans, never gates. |

**Run `/loop-engineer` only inside one already-gated GSD plan**, where the human decisions were taken at the gate and the loop has no new decision to make. Its own contract is "fully autonomous, never pause for user input, no plan-approval gate" — that is safe only while the decisions it could have made were already made.

Execute may use UnrealMCP on port 55557. Open `.agents/skills/ue-editor-ui/SKILL.md` only after a script logs `editor_ui: NEED_SLATE`. Verify for this repo is the existing editor check or pytest, not a GSD browser pass. Taste, test, and a new product phase stay human. GSD-3 stays idle until `swarm/PHASE_BOARD.md` names a bite.

**Non-goals — do not violate:**

- **Not the continuity layer.** It has no resume: every invocation starts a fresh loop, and `<LOOP_ID>_DONE/` is bookkeeping nothing reads back. Continuity stays in `swarm/PHASE_BOARD.md`, `Docs/handoffs/SESSION_HANDOFF_*.md`, `docs/SESSION_NOW.md`, and `.planning/STATE.md`. Never point `/loop-engineer` at a continuity task.
- **Never point it at a product decision.** The human owns taste and scope ([docs/human-use/OWNERSHIP.md](human-use/OWNERSHIP.md)); a loop that auto-skips past 3 verifier failures cannot ask.
- **Answer Q3 (auto-commit) `no` in a shared tree.** With `yes` it commits `PLAN.md` + `STATUS.md` per task, producing commits nobody staged by path.
- **Its budget is a turn counter, not a cost ceiling.** `MAX_TURNS` counts agent invocations only; there is no dollar/token limit. Set it deliberately per loop.
- **Subagents run sequentially in OpenCode** (upstream #14195, re-reported #29638), so wall-clock and cost per turn are higher than on a parallel platform.
- State lives in `loop-stack/<LOOP_ID>/`; cross-loop memory in `loop-stack/.global/MEMORY.md` (tracked). Goal output goes to the project directory, **never** inside `loop-stack/`.

**Accepted declines (do not re-litigate every session):**

- Harness always-on context lives in **`AGENTS.md` only** — Cursor rules are opt-in by glob or agent-requested (`alwaysApply: 0`, as of the P4 trim; see [.cursor/rules/README.md](../.cursor/rules/README.md)). Do not add an always-apply rule.
- Do **not** require Node 24+ on the host for day-to-day UE work; doctor may warn `EBADENGINE` under Node 22 — accepted for now.
- Do **not** vendor a second checkout under `.devenv/`; `UserHarness/` is the doctor root.
- Do **not** add ESLint / TypeScript unit-test gates for the game host; doctor “Node stack” criticals for missing TS/ESLint/JS tests are **accepted declines** (this repo is UE 5.8 + Python automation). Full matrix: [docs/Setup/DOCTOR_POLICY.md](Setup/DOCTOR_POLICY.md).
- Automation gaps for game systems stay in [docs/Automation/AUTOMATION_GAPS.md](Automation/AUTOMATION_GAPS.md), not the template stub.

The human makes **taste** (art design and game mechanic design), **tests** (what
"done" means, ship/no-ship, beat acceptance), and owns **isolation and permission
posture**. The agent owns architecture, code design, and harness refactoring, and
records those calls in [Docs/decisions/AGENT_DECISIONS.md](decisions/AGENT_DECISIONS.md).
See [docs/human-use/OWNERSHIP.md](human-use/OWNERSHIP.md) for the full map. Do
not invent a human decision or a product listed under
[cursor-cannot](human-use/cursor-cannot/README.md) — and do not ask for
approval on a boundary the agent owns, which is a bug in the ask, not caution.

Refresh layers: `npm run sync` (dry-run) then `npm run sync:apply`. Details: [docs/Setup/CURSOR_DEV.md](Setup/CURSOR_DEV.md).

## MVP lookdev swarm (on demand)

Blender-first MVP production kit: canon in **`Docs/`**, kits in **`Lib/`**, coordination in **`swarm/`**. **Start:** [START_HERE.md](../START_HERE.md) → Conductor chat → phase gates (`APPROVE P0` … `APPROVE P7`). **Process:** [swarm/SWARM_OPS.md](../swarm/SWARM_OPS.md) (Human Use, evidence gates, explicit-path git staging, KNOWN_ERRORS / AUTOMATION_GAPS). Specialists in [`.cursor/agents/`](../.cursor/agents/) load **on demand** when Conductor spawns a role — not always-on; separate from the UE automation company unless explicitly invoked.

**Mode detection (token efficiency):** At task start, choose **SWARM / NON-SWARM / HYBRID** and a **ModelClass** (Auto/Mid/Frontier/Explore) per [docs/human-use/SWARM_MODE_ROUTING.md](human-use/SWARM_MODE_ROUTING.md) (skill: `swarm-mode-routing`; research: [docs/Automation/SWARM_ROUTING_RESEARCH.md](Automation/SWARM_ROUTING_RESEARCH.md)). Default coding chats are NON-SWARM — do not auto-load Conductor kits.

## Dev environment setup

1. Install UE 5.8, clone this repo, init UserHarness: `git submodule update --init --recursive UserHarness` → `npm run doctor:build` once → `npm run doctor:ue` (UE host exit code; see [docs/Setup/CURSOR_DEV.md](Setup/CURSOR_DEV.md), [Docs/13b_HR2_B_COLD_CLONE.md](13b_HR2_B_COLD_CLONE.md)).
2. Run `Setup-MCP.bat` (one-time MCP bridge install).
3. **Build → Editor → MCP chain:** Run `.\Tools\Safe-Build.ps1` (closes Editor if needed, then builds — see [docs/Setup/BUILD_POLICY.md](Setup/BUILD_POLICY.md)).
4. Open Unreal Editor (`HomeWorld.uproject`), restart Cursor, verify MCP green dot (port 55557 — [docs/Setup/MCP_SETUP.md](Setup/MCP_SETUP.md)).
5. See [docs/SETUP.md](SETUP.md) for the full checklist. **Cloud agents:** no UE/MCP on Linux VM — see [docs/Setup/WINDOWS_BRIDGE.md](Setup/WINDOWS_BRIDGE.md).

**Enhanced Input** is applied automatically when the Editor loads (`Content/Python/init_unreal.py`). You do not need to run `setup_enhanced_input.py` unless movement still fails (troubleshooting).

## Commands

Exact invocations the agent should use (see [docs/SETUP.md](SETUP.md) and [docs/PCG/PCG_SETUP.md](PCG/PCG_SETUP.md) for more):

### Build → Editor → MCP (canonical agent chain)

| Step | Action | Doc |
|------|--------|-----|
| 1 | **`.\Tools\Safe-Build.ps1`** from repo root (closes Editor if running, then builds) | [BUILD_POLICY.md](Setup/BUILD_POLICY.md), [EDITOR_BUILD_PROTOCOL.md](Editor/EDITOR_BUILD_PROTOCOL.md) |
| 2 | Open **Unreal Editor** (`HomeWorld.uproject`) | [SETUP.md](SETUP.md) |
| 3 | Restart Cursor; confirm **MCP green dot** (UnrealMCP port 55557) | [MCP_SETUP.md](Setup/MCP_SETUP.md) |
| 4 | Use MCP tools or `execute_python_script` for Editor work | [09-mcp-workflow.mdc](../.cursor/rules/09-mcp-workflow.mdc) |

**Agents and automation:** Always use **Safe-Build**, never `Build-HomeWorld.bat` directly. **Humans** with Editor already closed may use `Build-HomeWorld.bat` (Safe-Build wraps it). **Cloud agents** (no UE): open PR → optional self-hosted `ci.yml` for C++ → Windows **DESKTOP-21CT3H0** for Editor/MCP — [WINDOWS_BRIDGE.md](Setup/WINDOWS_BRIDGE.md).

- **C++ build (agents):** **`.\Tools\Safe-Build.ps1`** only — see chain above.
- **Python script in Editor:** From project root, `py "Content/Python/<script>.py"`; or via MCP: `execute_python_script("<script>.py")` (paths relative to `Content/Python/`).
- **Python tests:** Editor: Tools > Test Automation (discovers `Content/Python/tests/test_*.py`).
- **PIE validation:** MCP `execute_python_script("pie_test_runner.py")`, then read `Saved/pie_test_results.json`.
- **In-editor quest sweep:** `.\Tools\RunTests.ps1 -Quest` (Editor open on UnrealMCP; loads `L_SizeTest`, one fresh PIE per stop). Results `Saved/quest_tests.json`; add quests in `Content/Python/quest_test_manifest.py`. See [Docs/qa/QUEST_TESTS.md](qa/QUEST_TESTS.md).
- **Host automation:** Set `UE_EDITOR` to the locked UE 5.8 editor path (`C:\Program Files\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe`), then from project root run `py Content/Python/run_ue_automation.py --filter <Prefix>`. Output is written to `Saved/automation_run_result.json`. Optional `capture_editor_screenshot.py` for screenshots (requires PyAutoGUI). See [docs/Automation/FULL_AUTOMATION_RESEARCH.md](Automation/FULL_AUTOMATION_RESEARCH.md) (Implementation Phase 2).
- **VS_MVP slice setup:** Primary playable path is **VS_MVP** (`/Game/HomeWorld/Maps/VS_MVP/`). Run `bootstrap_project.py` or `batch_import_asset_creation.py` + `place_vs_mvp_markers.py` (Editor or MCP). Legacy DemoMap/Homestead maps were **removed WAVE F** — see [Docs/08_AUDIT_SIGN_OFF.md](08_AUDIT_SIGN_OFF.md).
- **MVP swarm (product direction):** [swarm/SWARM_OPS.md](../swarm/SWARM_OPS.md) + Conductor — [START_HERE.md](../START_HERE.md). Pre-swarm agent-company loop **removed WAVE F** — stub at [docs/Automation/AGENT_COMPANY.md](Automation/AGENT_COMPANY.md).
- **Refine rules and strategy from runs:** All agent runs (main, fix, loop-breaker) and errors are recorded in Saved/Logs/agent_run_history.ndjson and automation_errors.log. Use them to update .cursor/rules, KNOWN_ERRORS.md, and development strategy over time. See [docs/Automation/AUTOMATION_REFINEMENT.md](Automation/AUTOMATION_REFINEMENT.md).
- **Cost/token tracking:** Run history includes `model` per run for cost attribution; optional `tokens`/`cost` when the CLI or a tracker exposes usage. Use Cursor billing or external trackers until then. See [docs/Automation/AUTOMATION_COST_TRACKING.md](Automation/AUTOMATION_COST_TRACKING.md).
- **Editor Output Log (Fixer/Guardian):** On main-loop failure the Watcher captures Saved/Logs/editor_output_full.txt (unfiltered) and editor_output_filtered.txt (development-relevant). Fixer reads the filtered log by default; **if previous fix round(s) did not resolve the issue, read the unfiltered log** (editor_output_full.txt) so the filter cannot hide the error. See [docs/Automation/AUTOMATION_EDITOR_LOG.md](Automation/AUTOMATION_EDITOR_LOG.md).
- **Project commands:** Reusable workflows in `.cursor/commands/` are available via `/` in chat (e.g. `/run-tests-and-fix`, `/create-pr`, `/review-changes`).
- **Project skills:** Domain skills in `.agents/skills/` (e.g. pcg-validate, **ue58-api-check**) are available via `/` in chat. **Primary slice:** VS_MVP + Docs/04 import — see [Maps/VS_MVP/README.md](../Maps/VS_MVP/README.md). Legacy demo-map/homestead skills reference removed WAVE F assets.
- **UE 5.8 API/plugin work:** Before changing C++, Blueprint, PCG, or plugin code, check [.cursor/rules/unreal-cpp.mdc](../.cursor/rules/unreal-cpp.mdc) (pitfalls table) and [docs/KNOWN_ERRORS.md](KNOWN_ERRORS.md). For **PCG graph or node changes**, also check [docs/PCG/PCG_BEST_PRACTICES.md](PCG/PCG_BEST_PRACTICES.md) and [docs/PCG/PCG_VARIABLES_NO_ACCESS.md](PCG/PCG_VARIABLES_NO_ACCESS.md). See [docs/UE/UE58_TECH.md](UE/UE58_TECH.md) for the full UE 5.8 tech entry point (5.7 history: [docs/UE/UE57_TECH.md](UE/UE57_TECH.md)).
- **Unreal Engine information (all):** Use **only UE 5.8–specific sources** for API, Editor UI, plugins, and docs (Epic 5.8 docs, docs/UE/UE58_TECH.md, docs/UE/UE58_EDITOR_UI.md when present, KNOWN_ERRORS). Do not rely on training data or other engine versions. See [.cursor/rules/ue58-sources.mdc](../.cursor/rules/ue58-sources.mdc). Editor UI: [ue58-editor-ui.mdc](../.cursor/rules/ue58-editor-ui.mdc).
- **Full automation stack:** Programmatic + GUI automation (key clickers, screenshotters, orchestration) and tool catalog: [docs/Automation/FULL_AUTOMATION_RESEARCH.md](Automation/FULL_AUTOMATION_RESEARCH.md).
- **Active coordination (post-audit):** [swarm/SWARM_OPS.md](../swarm/SWARM_OPS.md) + Conductor — [START_HERE.md](../START_HERE.md). Cloud-agent packets: [swarm/CLOUD_AGENT_PACKET.md](../swarm/CLOUD_AGENT_PACKET.md). Harness refine: [Docs/11_SWARM_HARNESS_REFINE.md](11_SWARM_HARNESS_REFINE.md).
- **Quarantine — pre-swarm agent loop:** `Start-AllAgents*`, `run_automation_cycle.py`, start-automation-cycle command — **removed WAVE F**. History only: [docs/Automation/AGENT_COMPANY.md](Automation/AGENT_COMPANY.md). Do not resurrect deleted Tools.
- **Host automation (MCP):** Prefer MCP `execute_python_script` on **Windows Editor**; see [docs/Automation/FULL_AUTOMATION_RESEARCH.md](Automation/FULL_AUTOMATION_RESEARCH.md). Cloud agents: [docs/Setup/WINDOWS_BRIDGE.md](Setup/WINDOWS_BRIDGE.md).

## Boundaries

- **Never:** Commit secrets, API keys, or `.env`; edit `Plugins/UnrealMCP/` or `Saved/` (they are not project code); change engine version (UE 5.8 only) or target platform (PC + Steam Early Access) without a team decision.
- **Agent-owned, decide then log** (was "Ask first" before 2026-10-01): CI/schema changes (`.github/workflows/`, JSON schema files), adding or upgrading dependencies, and broad refactors that touch many modules. Record each in [Docs/decisions/AGENT_DECISIONS.md](decisions/AGENT_DECISIONS.md) with the alternative you rejected. See [OWNERSHIP.md](human-use/OWNERSHIP.md#ownership-map).
- **Game content:** Automation preserves existing content; create-if-missing, update-in-place. See [.cursor/rules/18-game-development-principles.mdc](../.cursor/rules/18-game-development-principles.mdc).
- **Combat and night encounters:** Read [Docs/VISION_BOARD.md](VISION_BOARD.md). Do not restate it. Theme and the long horizon are in [VisionBoard/Core/VISION.md](../VisionBoard/Core/VISION.md).

## Testing

- **Automated (Python):** `PythonAutomationTest` plugin is enabled. Tests in `Content/Python/tests/` (named `test_*.py`) are auto-discovered. Run via Editor: Tools > Test Automation.
- **PIE tests:** `Content/Python/pie_test_runner.py` validates character spawn, ground contact, animation, and PCG. Run via MCP: `execute_python_script("pie_test_runner.py")`, then read `Saved/pie_test_results.json`.
- **Level loading and tests:** Level load + World Partition streaming can make tests flaky. Smart level loader and latent tests are implemented (see [docs/Testing/LEVEL_TESTING_PLAN.md](Testing/LEVEL_TESTING_PLAN.md)). Optional PIE full-flow test: `test_level_pie_flow.py` (Tools > Test Automation).
- **CI:** GitHub Actions (`.github/workflows/validate.yml`) — Python lint, JSON schema checks, C++ header/source pairing, doc freshness.

## Code style

- **C++:** PascalCase types, camelCase locals; Unreal prefixes (`A`, `U`, `F`, `E`, `I`). Include own header first. See `.cursor/rules/unreal-cpp.mdc`.
- **Python:** PEP 8, type hints, 4-space indent. UE scripts must be idempotent (check-before-create).
- **Commits:** Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`). Stage by explicit path — see [swarm/SWARM_OPS.md](../swarm/SWARM_OPS.md) and [PR and commit guidelines](#pr-and-commit-guidelines) below.
- **Feature debug instrumentation and log-driven validation:** When implementing features, include a **robust, log-driven way to validate** that they work (entry/exit, user-triggered actions, success/fail in logs). The user must not have to prompt for logging to confirm implementation.

## PR and commit guidelines

- Use Conventional Commits format for all commit messages.
- PowerShell shell: use `;` not `&&` for command chaining; use here-strings for multi-line commit messages.
- Pre-commit: lint, build check, no secrets, no `__pycache__` or temp JSON in tracked files.

## Security

- Never commit secrets, API keys, or `.env` files. Use `.env.example` for templates.
- `Saved/`, `Plugins/UnrealMCP/`, and `__pycache__/` are gitignored.
- Validate all external input at boundaries. See the [secure-coding](../.agents/skills/secure-coding/SKILL.md) skill.

## Setup and validation

[docs/SETUP.md](SETUP.md) (includes validation checklist). [docs/SPEC_AND_PLAN.md](SPEC_AND_PLAN.md) (plan-first and where to save plans). Cursor rules ship with the repo in `.cursor/rules/` — they are loaded automatically when the project is opened in Cursor. Key rules: `unreal-cpp.mdc` (C++ conventions + UE 5.8 API pitfalls), `09-mcp-workflow.mdc` (MCP-first priorities), `19-docs-directory-structure.mdc` (place new docs in correct docs/ subdir per [docs/DOCS_LAYOUT.md](DOCS_LAYOUT.md)), `20-full-automation-no-manual-steps.mdc` (full autonomy: no manual steps for the user; log gaps to [docs/Automation/AUTOMATION_GAPS.md](Automation/AUTOMATION_GAPS.md)), `automation-standards.mdc` (Editor UI automation is the **default** when we have the ability to interact with the Editor UI automatically; manual is fallback only; if a step cannot be automated, log to AUTOMATION_GAPS.md). Always check [docs/KNOWN_ERRORS.md](KNOWN_ERRORS.md) before making changes. **Full automation:** The agent does not expect or request manual work mid-session; use GUI automation (PyAutoGUI, ref images) where APIs are missing, and log any remaining gaps to [docs/Automation/AUTOMATION_GAPS.md](Automation/AUTOMATION_GAPS.md) for future solution sessions.

- **Session continuity:** **Swarm/Conductor:** resume from `Docs/handoffs/SESSION_HANDOFF_*.md` + `docs/SESSION_NOW.md` + `swarm/PHASE_BOARD.md` at start; append `SESSION_NOW.md` at end. Do not open `docs/history/SESSION_LOG.md` to start. **Legacy UE task lists:** DAILY_STATE. Open `docs/SESSION_LOG.md` only when a past incident is named. It is not a start read. · [swarm/SWARM_OPS.md](../swarm/SWARM_OPS.md) §13.
