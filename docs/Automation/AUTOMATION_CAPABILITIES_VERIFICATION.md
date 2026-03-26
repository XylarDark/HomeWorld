# Automation capabilities verification

**Purpose:** Confirm all project capabilities are accessible and referenced so agents use them. Update this doc when new tools or flows are added.

**Last verified:** 2026-03 (session).

---

## 1. Agent company and scripts

| Capability | Accessible | Utilized by | Notes |
|-------------|------------|-------------|--------|
| **Start-AllAgents.ps1** | Yes | User / AGENTS.md | One script to start Watcher (Developer + Fixer + Guardian). Installs CLI if missing, launches Editor when UE_EDITOR set. |
| **Watch-AutomationAndFix.ps1** | Yes | Start-AllAgents | Runs loop; on failure runs Fixer; on same failure again runs Guardian. |
| **RunAutomationLoop.ps1** | Yes | Watch, Start-AutomationSession | Reads NEXT_SESSION_PROMPT.md; after exit 0 runs Safe-Build if C++/Build.cs changed; uses Test-HasPendingTasks on CURRENT_TASK_LIST.md to continue; checks stop sentinel (Saved/Logs/agent_stop_requested) at round start. |
| **Guard-AutomationLoop.ps1** | Yes | Watch (when loop detected) | Reads automation_errors.log, automation_loop.log, watcher.log, **editor_output_full.txt**; writes automation_loop_breaker_report.md. |
| **Run-RefinerAgent.ps1** | Yes | User / AGENTS.md / Refiner role | Reads agent_run_history.ndjson, automation_errors.log, Guardian report; suggests Gap-Solver when gaps mentioned. |
| **Run-GapSolverAgent.ps1** | Yes | User / AGENTS.md / Refiner prompt | Implements solutions for docs/AUTOMATION_GAPS.md; referenced in Refiner prompt and automation-gap-solutions skill. |
| **Safe-Build.ps1** | Yes | RunAutomationLoop | Close Editor, build, retry once on Editor-related failure; -LaunchEditorAfter for post-build relaunch. |
| **Start-AutomationSession.ps1** | Yes | User / Start-AllAgents | Installs CLI if needed, then RunAutomationLoop. |

All of the above are documented in AGENTS.md Commands and in docs/AGENT_COMPANY.md.

---

## 2. Logs and Editor output

| Capability | Accessible | Utilized by | Notes |
|------------|------------|-------------|--------|
| **automation_errors.log** | Yes | Fixer, Guardian, Refiner | Written on non-zero exit; Fixer/Guardian prompts tell agent to read it. |
| **automation_loop.log** | Yes | Fixer, Guardian | Last 40 lines injected into Fixer prompt; Guardian gets excerpt. |
| **editor_output_full.txt** | Yes | Fixer (when unfixable), Guardian | Captured by Watch on failure from HomeWorld.log; Guardian always instructed to read it. |
| **editor_output_filtered.txt** | Yes | Fixer (default) | Produced by Content/Python/filter_editor_log.py; Fixer uses filtered first; safety rule: use full when fixRound >= 1. |
| **agent_run_history.ndjson** | Yes | Refiner, Append-AgentRunRecord | Written by RunAutomationLoop / Watch / Guard; Refiner reads last 60 lines. |
| **automation_loop_breaker_report.md** | Yes | Guardian (writes), Refiner (reads) | Guardian ensures it exists when loop unresolved. |

Capture: Watch-AutomationAndFix calls Invoke-CaptureEditorLog on every main-loop failure (before Fixer), then runs filter_editor_log.py. See docs/AUTOMATION_EDITOR_LOG.md.

---

## 3. Task list and prompts

| Capability | Accessible | Utilized by | Notes |
|------------|------------|-------------|--------|
| **CURRENT_TASK_LIST.md** | Yes | RunAutomationLoop (Test-HasPendingTasks), NEXT_SESSION_PROMPT, DAILY_STATE, AGENTS.md | Single 10-task list (T1–T10). Loop **exit condition**: continues while any task has `status: pending` or `status: in_progress`. Prompt says "first pending" from this list. See docs/workflow/HOW_TO_GENERATE_TASK_LIST.md and CURRENT_TASK_LIST_TEMPLATE.md. |
| **NEXT_SESSION_PROMPT.md** | Yes | RunAutomationLoop (Get-PromptText) | Default prompt file; contains workflow (fetch → implement → build/Editor → validate → debug → finish) and task source (CURRENT_TASK_LIST). |
| **DAILY_STATE.md** | Yes | Prompt, 07-ai-agent-behavior | Yesterday/Today/Tomorrow; Today = first pending task id from CURRENT_TASK_LIST (e.g. T4); agent reads at start and updates at end. |

**Loop vs task list:** The **stop condition** for RunAutomationLoop is "no pending or in_progress tasks in CURRENT_TASK_LIST.md." The loop also exits 0 at round start if **Saved/Logs/agent_stop_requested** exists (graceful stop), or on Ctrl+C (immediate stop). When the Guardian writes automation_loop_breaker_report.md and does not resolve the loop, the Watcher exits 1.

---

## 4. MCP and Editor

| Capability | Accessible | Utilized by | Notes |
|------------|------------|-------------|--------|
| **execute_python_script** (MCP) | Yes | 09-mcp-workflow, AGENTS.md, NEXT_SESSION_PROMPT | Prompt says to run validation e.g. execute_python_script('pie_test_runner.py'). |
| **pie_test_runner.py** | Yes | MCP, AGENTS.md, .cursor/commands/run-tests-and-fix | Writes Saved/pie_test_results.json. |
| **mcp_harness.py** | Yes | 09-mcp-workflow (Agent utility scripts) | Saved/mcp_request.json → MCP → Saved/mcp_response.json; commands: ping, asset_exists, get_actors, start_pie, stop_pie, etc. |
| **blueprint_inspector.py** | Yes | 09-mcp-workflow | Saved/blueprint_inspect_request.json → Saved/blueprint_inspect_result.json. |
| **capture_viewport.py** | Yes | 09-mcp-workflow | Saved/screenshot_result.json. |
| **layout_blueprint_nodes.py** | Yes | 09-mcp-workflow | Optional layout of Blueprint graph. |

Editor launch: RunAutomationLoop (and thus Watch) can auto-launch Editor before first round when UE_EDITOR is set; run_automation_cycle.py --launch-and-wait used for launch and MCP wait.

---

## 5. Build and validation in the cycle

| Capability | Accessible | Utilized by | Notes |
|------------|------------|-------------|--------|
| **Test-CppOrBuildFilesModified** | Yes | RunAutomationLoop | git status for Source/ and *.Build.cs; after exit 0, if true runs Safe-Build -LaunchEditorAfter. |
| **Safe-Build after round** | Yes | RunAutomationLoop | On build failure, exit 1 so Fixer runs; error appended to automation_errors.log. |
| **BuildBeforeFirstRound** | Yes | RunAutomationLoop -BuildBeforeFirstRound | Optional clean baseline build before first round. |

Documented in RunAutomationLoop header, docs/AUTOMATION_LOOP_UNTIL_DONE.md, and NEXT_SESSION_PROMPT (workflow + "loop will run a build after this round if C++ changed").

---

## 6. Rules and skills

| Capability | Accessible | Utilized by | Notes |
|------------|------------|-------------|--------|
| **09-mcp-workflow.mdc** | Yes | alwaysApply | MCP first, then Python, then GUI automation; log gaps to AUTOMATION_GAPS; agent utility scripts table. |
| **19-automation-gaps.mdc** | Yes | AGENTS.md (automation-gap-solutions) | When task touches a logged gap, use automation-gap-solutions skill; prefer programmatic then GUI then log. |
| **19-automation-cycle.mdc** | Yes | AGENTS.md (Automatic development cycle) | Follow when cycle is active. |
| **20-full-automation-no-manual-steps.mdc** | Yes | AGENTS.md Setup and validation | No manual steps for user; log gaps to AUTOMATION_GAPS. |
| **automation-gap-solutions** skill | Yes | AGENTS.md, Refiner prompt | Read AUTOMATION_GAPS, implement or document; portal, State Tree, PCG. |
| **demo-map-setup** skill | Yes | AGENTS.md | DemoMap + PCG. |
| **pcg-validate** skill | Yes | AGENTS.md, pcg-best-practices | When PCG Generate produces nothing. |
| **ue57-api-check** skill | Yes | AGENTS.md | Before C++/Python touching UE 5.7–sensitive APIs. |

---

## 7. Gaps and recommendations

- **Loop continuation:** Loop stops when CURRENT_TASK_LIST.md has no task with status pending or in_progress; optional stop sentinel (Saved/Logs/agent_stop_requested) for graceful exit. Resolved: single 10-task list drives the loop.
- **UE_EDITOR null:** Resolved. All scripts that check the Editor path use **Test-UE_EDITORSet** from Tools/Common-Automation.ps1 (or an explicit null check) so Test-Path is never called with null. See docs/KNOWN_ERRORS.md.
- **Editor log capture:** Requires Editor to have been run so HomeWorld.log exists; if the failure was before Editor launch, editor_output_full.txt may be missing or from a prior run. Fixer/Guardian prompts already say "if it exists."

---

## 8. Quick checklist for "are we using everything?"

- [ ] **Start agents:** Start-AllAgents.ps1 (or Watch-AutomationAndFix) — Developer, Fixer, Guardian.
- [ ] **Task source:** NEXT_SESSION_PROMPT points to CURRENT_TASK_LIST; DAILY_STATE has Today = first pending task id (e.g. T4).
- [ ] **Build:** Safe-Build runs after a successful round when C++/Build.cs changed; build failure invokes Fixer.
- [ ] **Validation:** Prompt tells Developer to run PIE/validation (e.g. pie_test_runner.py via MCP) when task requires it; exit non-zero to trigger Fixer.
- [ ] **Fixer:** Reads automation_errors.log, automation_loop.log, editor_output_filtered.txt (and editor_output_full.txt when fixRound >= 1).
- [ ] **Guardian:** Reads editor_output_full.txt and log excerpts; writes automation_loop_breaker_report.md.
- [ ] **Refiner:** Run on demand or after Guardian; reads run history and errors; suggests Gap-Solver when gaps mentioned.
- [ ] **Gap-Solver:** Run when AUTOMATION_GAPS or Guardian report mentions gaps; use automation-gap-solutions skill.
- [ ] **MCP:** execute_python_script for Editor scripts; mcp_harness for structured commands; pie_test_runner for PIE validation.

All of the above are wired in scripts, prompts, or rules. Use this doc to confirm nothing is missed when adding or changing automation.
