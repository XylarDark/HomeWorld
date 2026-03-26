# Start automatic development cycle

Run the automatic development cycle: turn **desires** (feature goals) into a task list, then execute one cycle iteration (implement programmatic → editor → test → debug → finalize → update rules) for the current task. Follow [.cursor/rules/19-automation-cycle.mdc](.cursor/rules/19-automation-cycle.mdc) for steps and loop guards.

## First run (start cycle)

1. **Read desires** from the user message (and any linked file, e.g. a backlog or part of `docs/workflow/30_DAY_SCHEDULE.md`).

2. **Generate task list** — Ordered list of tasks; each with id, goal, success criteria, optional doc link, status. Write to **docs/workflow/CYCLE_TASKLIST.md**.

3. **Initialize cycle state** — Set **docs/workflow/CYCLE_STATE.md**: current_task_index = 1, retry_count = 0, last_error_summary = (none), last_outcome = (none), blocked_reason = (none).

4. **Run one full cycle** for task 1: implement programmatic work → implement editor work → perform test → if fail, perform debug (first principles, update CYCLE_STATE); if pass, finalize task (mark completed, update DAILY_STATE, SESSION_LOG, advance state). On any instructive failure, update KNOWN_ERRORS. Respect loop guards (max 3 retries, same-failure guard, progress requirement). If task is blocked, mark it and move on or stop.

5. **Persist state** and report: what was done, current task index, next step (e.g. "Run this command again with message 'Continue' for the next task").

## Continue (subsequent runs)

When the user says **"Continue"** (or runs this command with message "Continue"):

1. Read **docs/workflow/CYCLE_TASKLIST.md** and **docs/workflow/CYCLE_STATE.md**.

2. If the current task is **completed** or **blocked**, advance to the next task (increment current_task_index, reset retry_count). If no tasks remain with status pending or in_progress, report "Cycle done" and stop.

3. Run **one full cycle** for the current task (same steps as above), following 19-automation-cycle.mdc. Update CYCLE_TASKLIST and CYCLE_STATE after test/debug/finalize.

4. Report outcome and what to do next (e.g. "Continue" again or "Task N blocked: reason").

## Orchestrator option (headless vs open Editor for MCP)

- **Run full cycle headless:** For the current task, you can run the host orchestrator instead of doing Editor work via MCP: `py Content/Python/run_automation_cycle.py --task N` (from project root; requires UE_EDITOR). This runs build (if Editor not running), scripts from automation_cycle_config.json for that task, then run_ue_automation.py, and updates CYCLE_STATE. Use when the task is script-only and no interactive MCP is needed.
- **Open Editor for MCP:** To drive the Editor via MCP, run `py Content/Python/run_automation_cycle.py --no-build --launch-and-wait` (or have the user open the Editor manually). Then run the cycle steps (implement, test, etc.) using MCP tools. When done, run `py Content/Python/run_automation_cycle.py --close-editor` before the next build.

## One-command start (install CLI if needed, then loop)

If the user says **"start an automation session"** or **"start all agents"** (or wants one command that does everything): run **`.\Tools\Start-AllAgents.ps1`** from the project root. This installs the Cursor Agent CLI if needed, auto-launches the Editor when `UE_EDITOR` is set, and runs the full agent company (Developer + Fixer + Guardian via the Watcher). For the loop only without the watcher, use `.\Tools\Start-AutomationSession.ps1`. Use `-NoLaunchEditor` to skip launching the Editor.

## Loop until all 30 days are done

If the user wants the process to **never end until all 30-day tasks are implementation-complete**:

1. Read [docs/workflow/30_DAY_IMPLEMENTATION_STATUS.md](../docs/workflow/30_DAY_IMPLEMENTATION_STATUS.md) and work on the first day with status `pending` (or execute the plan in `.cursor/plans/` if the prompt references one).
2. When you finish or block a day, update that file (set day to `done` or `blocked`), update DAILY_STATE and SESSION_LOG.
3. Create a short implementation plan for the **next** pending day (goal, key steps, task doc link, success criteria) and save it to `.cursor/plans/dayN-<slug>.md` (e.g. `day7-resource-nodes.md`), or embed the plan steps in NEXT_SESSION_PROMPT. The next session should execute that plan.
4. At **session end**, write [docs/workflow/NEXT_SESSION_PROMPT.md](../docs/workflow/NEXT_SESSION_PROMPT.md) with the exact prompt to paste in a **new chat** to continue (e.g. reference the plan file or include the steps). The agent cannot start a new session by itself; the user (or external tooling) starts the next session and pastes that prompt. See [docs/Automation/AUTOMATION_LOOP_UNTIL_DONE.md](../docs/Automation/AUTOMATION_LOOP_UNTIL_DONE.md).

## Success

- Task list is in CYCLE_TASKLIST.md; state in CYCLE_STATE.md.
- Each iteration runs one cycle for one task, with no infinite loops (guards enforced).
- User can start with "Start automation cycle. Desires: …" and continue with "Continue" until the list is done or blocked.
- For 30-day loop: use 30_DAY_IMPLEMENTATION_STATUS and NEXT_SESSION_PROMPT so each new session continues where the last left off.
