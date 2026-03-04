# Running the automation loop until all 30-day tasks are done

**Goal:** Have the development cycle run session after session until every task in the 30-day list is **implementation-complete** (not just specified). This doc explains what the agent can and cannot do, and what tooling you need.

---

## Can the agent start the next session by itself?

**No.** The agent runs inside a Cursor session. It cannot open a new chat or trigger a new session. Something external must start each new session and send a "Continue" (or equivalent) prompt.

So: **"Never end until all tasks are done"** requires either you to keep starting the next session (e.g. by pasting the recommended prompt) or an external process that triggers Cursor with that prompt.

---

## What we have in-repo (no external tooling)

1. **Cycle state and task list** — [CYCLE_TASKLIST.md](workflow/CYCLE_TASKLIST.md) and [CYCLE_STATE.md](workflow/CYCLE_STATE.md) tell the agent which task is current and what to do next. The agent updates these at the end of each iteration.

2. **Recommended next prompt** — At the end of each session, the agent writes [NEXT_SESSION_PROMPT.md](workflow/NEXT_SESSION_PROMPT.md) with the **exact prompt** you (or a script) should use to start the next session. You open a new chat, paste that prompt, and the agent continues.

3. **"Continue" convention** — If you say **"Continue the automatic development cycle"** (or use the start-automation-cycle command with message "Continue"), the agent reads CYCLE_TASKLIST and CYCLE_STATE and runs one more cycle for the current task, then updates state and writes the next recommended prompt.

**Manual loop:**  
Session 1 → agent does task 1, writes NEXT_SESSION_PROMPT.md → you start Session 2, paste the prompt → agent does task 2, writes NEXT_SESSION_PROMPT.md → … repeat until CYCLE_TASKLIST has no pending/in_progress tasks.

---

## Implementation-complete vs spec-complete

The 30-day schedule was marked [x] for the "test drive" so that **every day has a task doc**. Many of those days are **spec-complete** (goal and steps written) but not **implementation-complete** (scripts run in Editor, PIE passed, assets created, etc.).

For "never end until all tasks are done," we need the agent to treat **implementation** as the bar:

- **Implementation-complete** for a day = scripts run successfully where applicable, required assets/actors exist, and validation (e.g. PIE or test) passes or is explicitly deferred with a reason.
- The agent should use [30_DAY_SCHEDULE.md](workflow/30_DAY_SCHEDULE.md) plus [30_DAY_IMPLEMENTATION_STATUS.md](workflow/30_DAY_IMPLEMENTATION_STATUS.md) (see below) so it only marks a day done when implementation is done, and only then moves on.

We add **30_DAY_IMPLEMENTATION_STATUS.md** to record, per day, whether it is implementation-complete and what’s left. The agent reads it at session start and updates it at session end. That way the "loop until done" has a single source of truth for "what’s actually left to do."

---

## Fully automatic loop with Cursor CLI

The **Cursor Agent CLI** supports non-interactive, scriptable runs. You can drive a fully automatic loop with a wrapper script and no manual "Continue" pastes.

- **Invocation:** Run the agent with a prompt; use `-p` / `--print` for non-interactive mode (prints responses to console).
- **Auto-approval:** Use `-f` / `--force` to auto-approve commands and `--approve-mcps` to auto-approve MCP servers (e.g. Unreal MCP when the Editor is running).
- **Workspace:** Use `--workspace <project_root>` so the agent uses your project’s `.cursor/rules`, `AGENTS.md`, and `.cursor/mcp.json`.

**Loop runner pattern:** A script (e.g. [Tools/RunAutomationLoop.ps1](../Tools/RunAutomationLoop.ps1)) can: (1) read the prompt from [NEXT_SESSION_PROMPT.md](workflow/NEXT_SESSION_PROMPT.md) (or a default "Continue…" prompt), (2) run `agent -p -f --approve-mcps --workspace <project_root> "<prompt>"`, (3) when the agent exits, check [30_DAY_IMPLEMENTATION_STATUS.md](workflow/30_DAY_IMPLEMENTATION_STATUS.md) for any `pending`, (4) if pending, repeat from (1); otherwise exit. No built-in "run until condition" exists in the CLI; the outer script implements the loop.

**One-command start:** [Tools/Start-AutomationSession.ps1](../Tools/Start-AutomationSession.ps1) installs the Cursor Agent CLI if it is not on PATH, then runs the loop. The Editor is **auto-launched** before the first round when `UE_EDITOR` is set. From project root run `.\Tools\Start-AutomationSession.ps1` (use `-NoLaunchEditor` to skip launching the Editor).

**Cloud Agents API:** The Cloud Agents API launches agents in Cursor’s cloud VM on a repo clone. It **cannot** attach to your local Unreal Editor or use a local-only Unreal MCP server. Use it only for repo-only or code-only tasks (e.g. refactors, docs). For Editor-dependent work (run Python in Editor, PIE, MCP), use the **local CLI** with the loop runner and the Editor running on your machine.

**Docs:** [Cursor CLI – Using Agent](https://cursor.com/docs/cli/using), [Parameters](https://cursor.com/docs/cli/reference/parameters).

**Windows / PowerShell:** The CLI on Windows uses PowerShell. Avoid piping agent output through `Select-Object -First N` or other truncating pipelines; that can cause hangs or "Connection failed" loops. Let the agent’s output run to completion or stream to a file.

**Prerequisites for the loop:** Cursor Agent CLI installed and authenticated (`agent login` or `CURSOR_API_KEY`). For Unreal tasks that need MCP, start the Unreal Editor (and ensure the MCP server is available) before running the loop.

**File logging (survives terminal crash):** The loop writes to:
- **Saved/Logs/automation_loop.log** — Timestamped progress (each round start, agent finished, exit code). Use to see what happened if the terminal closed or crashed.
- **Saved/automation_last_activity.json** — Last message and timestamp (and current round). If the timestamp is recent (e.g. within the last few minutes), the agent may still be running; if it’s old and no new round started, the process may have crashed or exited.
- **Saved/Logs/automation_errors.log** — Errors only (non-zero exit, usage limit hint). Paste this into chat to fix issues; over time you can use it so the agent can fix its own errors (e.g. “read automation_errors.log and apply fixes”).

**Is the agent still working?** (1) Check **Saved/automation_last_activity.json** — if `timestamp` is recent, the loop is likely still in a round. (2) In Task Manager, look for a process named **agent** or **node** (Cursor CLI). (3) If the terminal is still open, see if new output appears. If the terminal crashed but the process is still running, the log files keep updating until the round finishes.

**Watcher (second agent to fix failures):** Run **`.\Tools\Watch-AutomationAndFix.ps1`** instead of `Start-AutomationSession.ps1` to have a supervisor that runs the main loop and, when it fails, starts a **fix agent** that reads `Saved/Logs/automation_errors.log` and the tail of `automation_loop.log`, applies fixes, and then the watcher re-runs the loop. Use `-MaxFixRounds 3` (default) to limit how many fix rounds before giving up; use `-NoRetryAfterFix` to run the fix agent once and then exit so you can re-run manually. Watcher activity is logged to **Saved/Logs/watcher.log**.

**Guardian (third agent – loop-breaker):** If the main loop and **Fixer** are in a **repeating failure loop** (same error or same exit code), the **Guardian** agent resolves it or writes a report. The **watcher** automatically invokes it when the same failure happens twice in a row, or when `MaxFixRounds` is reached. You can also run **`.\Tools\Guard-AutomationLoop.ps1`** manually. Use **`-CheckOnly`** to only detect (exit 1 = loop detected). Guardian activity is logged to **Saved/Logs/guardian.log**. For the full role model (Developer, Fixer, Guardian, Refiner) and accountability, see [docs/AGENT_COMPANY.md](AGENT_COMPANY.md).

**Run history for refinement:** All agent runs (main, fix, loop-breaker) are recorded in **Saved/Logs/agent_run_history.ndjson**. Use it with automation_errors.log and automation_loop_breaker_report.md to update rules and development strategy over time. See [docs/AUTOMATION_REFINEMENT.md](AUTOMATION_REFINEMENT.md).

---

## Plan-per-task

At the end of each session, the agent creates a short implementation plan for the **next** pending day (from 30_DAY_IMPLEMENTATION_STATUS) so the next session has a clear, executable plan instead of only a generic "work on first pending day" prompt.

- **Option A:** Save the plan to `.cursor/plans/dayN-<slug>.md` (e.g. `day7-resource-nodes.md`) and set NEXT_SESSION_PROMPT.md to tell the next session to execute that plan file.
- **Option B:** Embed the plan steps (goal, key steps, task doc link, success criteria) inside NEXT_SESSION_PROMPT.md so the next session's prompt both identifies the day and lists the plan.

The default prompt in RunAutomationLoop.ps1 and the content of NEXT_SESSION_PROMPT.md instruct the agent to create and save (or embed) the plan for the next pending day after marking the current day done. See [.cursor/commands/start-automation-cycle.md](../.cursor/commands/start-automation-cycle.md) ("Loop until all 30 days are done").

---

## Other options (manual or semi-automatic)

| Option | Description |
|--------|-------------|
| **Scheduled task + manual paste** | A scheduled task or reminder that opens Cursor and shows you NEXT_SESSION_PROMPT.md so you can paste it and start the next session quickly. |
| **UI automation** | A tool (e.g. AutoHotkey, Sikuli, or similar) that opens Cursor, focuses the chat, and pastes the contents of NEXT_SESSION_PROMPT.md. Still requires Cursor to be running and the automation to know when the agent has finished. |
| **Compound / workflow plugins** | If you use a plugin that can "execute plan until done" across multiple steps or sessions, that could drive the loop; configuration would be in that plugin. |

---

## Summary

- **Agent cannot self-start a new session.** Something external (you or a script) must start the next session and send the continue prompt.
- **In-repo:** Use CYCLE_TASKLIST, CYCLE_STATE, and NEXT_SESSION_PROMPT.md so each session knows what to do and the next session can be started with one paste.
- **"Done" = implementation-complete.** We track that in 30_DAY_IMPLEMENTATION_STATUS.md so the loop runs until every day is actually done, not just specified.
- **Fully automatic loop:** Use the Cursor Agent CLI with a loop-runner script (e.g. RunAutomationLoop.ps1) that invokes the CLI with the prompt from NEXT_SESSION_PROMPT.md and repeats until 30_DAY_IMPLEMENTATION_STATUS has no pending days. See "Fully automatic loop with Cursor CLI" above.
