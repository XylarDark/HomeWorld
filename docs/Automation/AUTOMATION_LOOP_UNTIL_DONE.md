# Running the automation loop until the task list is done

**Goal:** Have the development cycle run session after session until every task in the **current task list** is completed (or the loop is stopped). The loop is driven by a single 10-task list; it exits only when that list has no pending/in_progress tasks, or when a stop sentinel or Guardian report applies. This doc explains what the agent can and cannot do, and what tooling you need.

---

## Loop driver and exit conditions

- **Single source of truth:** [CURRENT_TASK_LIST.md](workflow/CURRENT_TASK_LIST.md) (exactly 10 tasks, T1–T10) drives the loop. See [HOW_TO_GENERATE_TASK_LIST.md](workflow/HOW_TO_GENERATE_TASK_LIST.md) for how to create or replace this list from research.
- **Only T1–T10 count:** The loop counts pending/in_progress only for sections **T1** through **T10**. Do not add T11, T12, etc. If the agent discovers work that deserves a new task, it must document it in SESSION_LOG or [AUTOMATION_GAPS.md](AUTOMATION_GAPS.md) for the next task-list generation; it must not add new task sections to CURRENT_TASK_LIST. The CLI logs which task is being worked on (e.g. "Working on first pending task: T3 — …") so you can see progress.
- **Continuation:** The loop continues while the task list has **any** of T1–T10 with `status: pending` or `status: in_progress`. When all of T1–T10 are `completed` or only `blocked` (with no remaining work), the loop exits 0.
- **Exit conditions (only):**
  - **Task list complete** — No pending/in_progress tasks → exit 0.
  - **Stop sentinel** — At the start of each round, if the file **Saved/Logs/agent_stop_requested** exists, the loop logs "Stop requested" and exits 0. To request a graceful stop without killing the terminal, create that empty file; the loop will exit at the start of the next round.
  - **Hard cancel** — Ctrl+C in the terminal stops the loop immediately.
  - **Guardian report (cannot complete)** — When the Guardian writes automation_loop_breaker_report.md and does not resolve the loop, the Watcher exits 1; the loop does not start another round until you re-run.

### Audit: no early exit (task list must drive completion)

The loop must **not** exit 0 while CURRENT_TASK_LIST still has any task with `status: pending` or `status: in_progress`. Only these exits are valid:

| Outcome | Condition | Exit code | Who exits |
|--------|-----------|-----------|-----------|
| **Task list complete** | Test-HasPendingTasks is false (no pending/in_progress in CURRENT_TASK_LIST) | 0 | RunAutomationLoop |
| **User stop** | Saved/Logs/agent_stop_requested exists at round start | 0 | RunAutomationLoop |
| **Agent or build failure** | Agent exit non-zero, agent timeout, Safe-Build failed, or prerequisite missing | non-zero | RunAutomationLoop (Watcher then runs Fixer and re-runs loop) |
| **Guardian gave up** | Same failure repeated, Guardian wrote report, MaxFixRounds reached | 1 | Watch-AutomationAndFix |

Safeguards against early exit: (1) At each round start, the loop checks Test-HasPendingTasks; if false, it exits 0 without running the agent (task list already complete). (2) After each successful round, it re-reads CURRENT_TASK_LIST from disk and only continues the do-while when Test-HasPendingTasks is true. (3) The default prompt and NEXT_SESSION_PROMPT instruct the agent to complete **exactly one task** per round and set **only that task** to completed so the loop continues to the next pending task. (4) Round start and end log the number of pending/in_progress tasks so automation_loop.log shows why the loop continued or exited.

---

## Canonical workflow

The automation cycle follows this workflow:

1. **Fetch task** — Get the first **pending** or **in_progress** task from [CURRENT_TASK_LIST.md](workflow/CURRENT_TASK_LIST.md).
2. **Implement work** — Implement the task (code, scripts, assets, docs as needed).
3. **Decide if Editor must be opened / project must be built** — If the work touched C++ or Build.cs, the project must be built before validation (the loop runs Safe-Build after the round). If the work requires in-Editor or in-game validation, the Editor must be open (and optionally PIE running).
4. **Validate work in Editor** — When the task requires it, use Editor tools and/or game sessions (MCP, PIE, pie_test_runner.py, execute_python_script, etc.) to confirm the work functions correctly. The Developer must run validation when applicable and exit non-zero if validation fails so the Fixer runs (debug loop).
5. **Debug if necessary** — If validation or build fails, the loop exits non-zero and the Watcher runs the Fixer; the cycle repeats until a solution is found.
6. **Finish task** — Mark task done in CURRENT_TASK_LIST.md (set status to completed or blocked), update SESSION_LOG, DAILY_STATE, and NEXT_SESSION_PROMPT.
7. **Fetch next task** — Loop to step 1.

**Build in the loop:** After each successful agent round, the loop checks for modified files under `Source/` or any `*.Build.cs`. If any exist, it runs **Safe-Build -LaunchEditorAfter** (closes Editor, builds, relaunches Editor). If the build fails, the loop exits with code 1 so the Watcher runs the Fixer. See [Tools/RunAutomationLoop.ps1](../Tools/RunAutomationLoop.ps1).

---

## Can the agent start the next session by itself?

**No.** The agent runs inside a Cursor session. It cannot open a new chat or trigger a new session. Something external must start each new session and send a "Continue" (or equivalent) prompt.

So: **"Never end until all tasks are done"** requires either you to keep starting the next session (e.g. by pasting the recommended prompt) or an external process that triggers Cursor with that prompt.

---

## What we have in-repo (no external tooling)

1. **Current task list** — [CURRENT_TASK_LIST.md](workflow/CURRENT_TASK_LIST.md) is the single list that drives the loop (10 tasks, T1–T10). Agents fetch the first pending or in_progress task. The list uses status: `pending` | `in_progress` | `completed` | `blocked`. See [HOW_TO_GENERATE_TASK_LIST.md](workflow/HOW_TO_GENERATE_TASK_LIST.md) and [CURRENT_TASK_LIST_TEMPLATE.md](workflow/CURRENT_TASK_LIST_TEMPLATE.md) to create or replace the list.

2. **Recommended next prompt** — At the end of each session, the agent writes [NEXT_SESSION_PROMPT.md](workflow/NEXT_SESSION_PROMPT.md) with the **exact prompt** you (or a script) should use to start the next session. You open a new chat, paste that prompt, and the agent continues.

3. **"Continue" convention** — If you say **"Continue the automatic development cycle"** (or use the start-automation-cycle command with message "Continue"), the agent reads CURRENT_TASK_LIST and DAILY_STATE and runs one more cycle for the current task, then updates state and writes the next recommended prompt.

**Manual loop:**  
Session 1 → agent does task, writes NEXT_SESSION_PROMPT.md → you start Session 2, paste the prompt → … repeat until CURRENT_TASK_LIST has no pending/in_progress tasks (or you create Saved/Logs/agent_stop_requested or press Ctrl+C).

---

## Implementation-complete vs spec-complete

For "never end until all tasks are done," the agent treats **implementation** as the bar:

- **Implementation-complete** for a task = scripts run successfully where applicable, required assets/actors exist, and validation (e.g. PIE or test) passes or is explicitly deferred with a reason. Then set **status:** to `completed` in CURRENT_TASK_LIST.md (or `blocked` with reason).
- The loop reads [CURRENT_TASK_LIST.md](workflow/CURRENT_TASK_LIST.md) and continues while any task has `status: pending` or `status: in_progress`. The agent updates the task list at session end. The 30-day schedule and 30_DAY_IMPLEMENTATION_STATUS remain as legacy reference; the **loop driver** is the current task list only.

Legacy: 30_DAY_IMPLEMENTATION_STATUS was previously used; the loop driver is now CURRENT_TASK_LIST only.
---

## Fully automatic loop with Cursor CLI

The **Cursor Agent CLI** supports non-interactive, scriptable runs. You can drive a fully automatic loop with a wrapper script and no manual "Continue" pastes.

- **Invocation:** Run the agent with a prompt; use `-p` / `--print` for non-interactive mode (prints responses to console).
- **Auto-approval:** Use `-f` / `--force` to auto-approve commands and `--approve-mcps` to auto-approve MCP servers (e.g. Unreal MCP when the Editor is running).
- **Workspace:** Use `--workspace <project_root>` so the agent uses your project’s `.cursor/rules`, `AGENTS.md`, and `.cursor/mcp.json`.

**Loop runner pattern:** [Tools/RunAutomationLoop.ps1](../Tools/RunAutomationLoop.ps1): (1) at round start, if **Saved/Logs/agent_stop_requested** exists, exit 0; (2) read the prompt from [NEXT_SESSION_PROMPT.md](workflow/NEXT_SESSION_PROMPT.md) (or a default that references CURRENT_TASK_LIST and first pending task); (3) run the agent with that prompt; (4) when the agent exits with 0, if Source/ or *.Build.cs are modified, run Safe-Build -LaunchEditorAfter and exit 1 on build failure so the Fixer runs; (5) check [CURRENT_TASK_LIST.md](workflow/CURRENT_TASK_LIST.md) for any task with `status: pending` or `status: in_progress` (Test-HasPendingTasks); (6) if yes, repeat from (1); otherwise exit 0. The Developer is expected to validate in Editor when the task requires it (e.g. PIE, pie_test_runner) and exit non-zero on validation failure so the debug loop runs.

**One-command start:** [Tools/Start-AutomationSession.ps1](../Tools/Start-AutomationSession.ps1) installs the Cursor Agent CLI if it is not on PATH, then runs the loop. The Editor is **auto-launched** before the first round when `UE_EDITOR` is set. From project root run `.\Tools\Start-AutomationSession.ps1` (use `-NoLaunchEditor` to skip launching the Editor).

**Cloud Agents API:** The Cloud Agents API launches agents in Cursor’s cloud VM on a repo clone. It **cannot** attach to your local Unreal Editor or use a local-only Unreal MCP server. Use it only for repo-only or code-only tasks (e.g. refactors, docs). For Editor-dependent work (run Python in Editor, PIE, MCP), use the **local CLI** with the loop runner and the Editor running on your machine.

**Docs:** [Cursor CLI – Using Agent](https://cursor.com/docs/cli/using), [Parameters](https://cursor.com/docs/cli/reference/parameters).

**Windows / PowerShell:** The CLI on Windows uses PowerShell. Avoid piping agent output through `Select-Object -First N` or other truncating pipelines; that can cause hangs or "Connection failed" loops. Let the agent’s output run to completion or stream to a file.

**Prerequisites for the loop:** Cursor Agent CLI installed and authenticated (`agent login` or `CURSOR_API_KEY`). For Unreal tasks that need MCP, start the Unreal Editor (and ensure the MCP server is available) before running the loop.

**File logging (survives terminal crash):** The loop writes to:
- **Saved/Logs/automation_loop.log** — Timestamped progress (each round start, agent finished, exit code). Use to see what happened if the terminal closed or crashed.
- **Saved/Logs/automation_events.log** — High-level event stream (round completed, build validated/failed, Fixer/Guardian invoked, PIE validation). One line per event; same events are printed to the terminal when the loop or Watcher runs. **Get-AutomationStatus** (without `-Short`) shows the last 10 events.
- **Saved/automation_last_activity.json** — Last message and timestamp (and current round). If the timestamp is recent (e.g. within the last few minutes), the agent may still be running; if it’s old and no new round started, the process may have crashed or exited.
- **Saved/Logs/automation_errors.log** — Errors only (non-zero exit, usage limit hint). Paste this into chat to fix issues; over time you can use it so the agent can fix its own errors (e.g. “read automation_errors.log and apply fixes”).

**Is the agent still working?** Run **`.\Tools\Get-AutomationStatus.ps1`** anytime (from project root) to see: process running?, last activity time and message, last 10 high-level events (automation_events.log), last lines of automation_loop.log and watcher.log, and whether the task list has pending tasks. Use **`-Short`** for a one-screen summary only. Alternatively: (1) Check **Saved/automation_last_activity.json** — if `timestamp` is recent, the loop is likely still in a round. (2) In Task Manager, look for **agent** or **node** (Cursor CLI). (3) If the terminal is still open, see if new output appears.

**Agent timeout and heartbeat (Watcher accountability):** The loop runs each agent round with a **timeout** (default **90 minutes**; override with **`-AgentTimeoutMinutes`**). If the agent does not finish within that time, the loop treats it as **stalled**, logs the timeout, exits with code 1 so the **Fixer** runs. While the agent is running, the loop writes a **heartbeat every 1 minute** to: (1) automation_last_activity.json and automation_status_latest.txt, and (2) **Saved/Logs/automation_heartbeat.log**. Each heartbeat includes a **high-level overview**: **Since last heartbeat** (new automation_events.log and automation_loop.log lines, or “agent still working”) and **Next** (when agent exits: build if needed, next round with next pending task or exit, or Fixer on non-zero). This lets you see what work has been done since the last tick and what will happen next. **To see progress in chat:** ask "what's the agent doing?" or "automation status"; the agent will read automation_heartbeat.log and summarize. **In terminal:** run **`.\Tools\Get-AutomationStatus.ps1`** (shows heartbeat log tail) or tail **Saved/Logs/automation_heartbeat.log**.

**Stall protection:** By default the loop starts **Watch-HeartbeatStall.ps1** as a background process. If the heartbeat (or automation_last_activity.json) has not been updated for **15 minutes** (configurable via **`-StallThresholdMinutes`**) and an **agent** process is still running, the stall watcher **kills the agent** so the round ends and the loop can exit (then the Fixer can run). This avoids indefinite hangs when the agent or CLI is stuck. Log: **Saved/Logs/stall_watcher.log**. Use **`-NoStallProtection`** when running RunAutomationLoop to disable (e.g. for debugging). To stop a run manually: create **Saved/Logs/agent_stop_requested** (empty file) and kill the agent process; the loop will exit at the start of the next round (or immediately when the job ends).

**Live status file:** The loop writes **Saved/Logs/automation_status_latest.txt** at the start of each round with a one-line summary (timestamp, round, pending Y/N). For updates every 90 seconds during a round, run **`.\Tools\Update-AutomationStatusLive.ps1`** in a second terminal; it overwrites that file until the loop is no longer running. Tail the file to see current state without re-running a script: in PowerShell `Get-Content Saved\Logs\automation_status_latest.txt -Wait`, or in bash `tail -f Saved/Logs/automation_status_latest.txt`.

**Terminal capture and window policy:** When you start agents via **Start-AllAgents-InNewWindow.ps1** or **Start-AllAgents.bat**, the run uses **Run-AutomationWithCapture.ps1**: all stdout/stderr is teed to **Saved/Logs/automation_terminal_capture.log** so errors that only appear in the external terminal are captured. The Fixer and the chat agent read this file when diagnosing failures or when you ask for automation status. The agent window is run under **cmd /k** (or ends with "Press Enter to close"); **only you can terminate the terminal**—it never auto-closes on success or failure, so you can always see errors or success.

**Single-instance guard (avoid two CLIs):** Each run of **Start-AllAgents-InNewWindow.ps1** used to open a new window with no check for an already-running loop, so running "start agents" twice (e.g. from chat and from a shortcut) could start two loops that shared the same **CURRENT_TASK_LIST.md** and Editor, causing conflicting edits and odd counts (e.g. "10 pending" again after Round 10). The scripts now use a **lock file** (**Saved/Logs/automation_loop.lock**) that stores the PID of the process running the loop. Before opening a new window, **Start-AllAgents-InNewWindow.ps1** checks whether that PID is still running; if so, it prints a warning and **exits with code 1** without starting a second run (no second window is opened). **Which window to close** if you already have two: close the one that started **later** (the duplicate); keep the one that started first (or the one with the higher round number if you prefer to keep the more advanced run). After the loop exits (or you close its window), the lock is removed so you can start a new run. Helpers: **Get-AutomationLoopLockPath**, **Test-AutomationLoopRunning**, **Set-AutomationLoopLock**, **Remove-AutomationLoopLock** in [Tools/Common-Automation.ps1](../Tools/Common-Automation.ps1).

**When the loop exits:** It writes **Saved/Logs/automation_exit_alert.md** (and .json) with exit reason, round, last message, and a **"What we were unable to accomplish"** section (pending tasks, errors, and a reminder to document in SESSION_LOG/AUTOMATION_GAPS). The CLI also prints a prominent block at the end of each session: what was not accomplished, that it must be documented, and that the next run will include research and solution-making for these items. The Watcher shows the same style of alert when it exits after fix rounds or the Guardian. To get an update in the agentic chat, say **"Give me the automation update"** or **"Check automation exit"**; the agent will read the alert file and **automation_terminal_capture.log** and summarize (including any terminal-only errors).

**When all tasks are complete:** If the loop exits with "No pending tasks; done", it also writes **Saved/Logs/automation_tasks_complete.md**. The terminal **stays open**: at the end of every run (success or failure), **Start-AllAgents.ps1** shows "Press Enter to close this window" so you can read the output and confirm how the run ended. Use **`-NoPauseOnComplete`** when running headless or in CI to skip the pause. **Run automation only in a separate window:** use **`.\Tools\Start-AllAgents-InNewWindow.ps1`** from any terminal (opens a new window where the loop runs) or double-click **Start-AllAgents.bat** in the project root; never run the loop in the chat/integrated terminal. The agent will **automatically prepend a prominent alert** at the start of your next chat so you know to generate a new task list (see [HOW_TO_GENERATE_TASK_LIST.md](workflow/HOW_TO_GENERATE_TASK_LIST.md)) and run the new-window launcher when ready. You do not need to ask for this update.

**When a round completes (loop still running):** After each successful round, the loop writes **Saved/Logs/automation_last_completion.json** (timestamp, round, message). When you open the chat and the loop has not yet exited (no exit alert), the agent will **automatically prepend** "Latest automation: Round N completed at [time]; run Get-AutomationStatus to see if still running." So you are informed whenever something (a round) has completed, without asking.

**Slack/Discord alerts (opt-in):** To post a short message to Slack or Discord when the loop exits, create **Saved/Logs/automation_slack_webhook.txt** and put a single line in it: the Incoming Webhook URL (Slack or Discord). The loop will POST a JSON body with the exit summary when it exits. Do not commit this file or put webhook URLs in the repo. Remove the file to disable.

**Watcher (second agent to fix failures):** Run **`.\Tools\Watch-AutomationAndFix.ps1`** instead of `Start-AutomationSession.ps1` to have a supervisor that runs the main loop and, when it fails, starts a **fix agent** that reads `Saved/Logs/automation_errors.log` and the tail of `automation_loop.log`, applies fixes, and then the watcher re-runs the loop. Use `-MaxFixRounds 3` (default) to limit how many fix rounds before giving up; use `-NoRetryAfterFix` to run the fix agent once and then exit so you can re-run manually. Watcher activity is logged to **Saved/Logs/watcher.log**.

---

## Thresholds before we report to you (manual intervention)

We **do not** alert you after every failure. The following thresholds are in place so the system retries automatically before asking you to intervene:

| Trigger | Threshold | What happens before we report |
|--------|------------|-------------------------------|
| **Developer round fails** (build, validation, agent exit non-zero) | **3 fix rounds** (default) | Main loop fails → **Fixer** runs (fix round 1). Loop re-runs. If it fails again → Fixer runs (fix round 2). If it fails again → Fixer runs (fix round 3). After 3 fix rounds we invoke the **Guardian** and exit; then we **report**: read **Saved/Logs/automation_loop_breaker_report.md**. So you are only asked to intervene after **up to 3 automatic fix attempts**. Override with `-MaxFixRounds N` when starting the watcher. |
| **Agent stalls** (no heartbeat) | **15 minutes** (default) | Stall watcher kills the agent so the round ends; the loop exits non-zero and the **Fixer** runs. No direct report to you unless we then exhaust fix rounds (see above). Override with `-StallThresholdMinutes N` in RunAutomationLoop. |
| **Agent timeout** (single round too long) | **90 minutes** (default) | Loop kills the agent and exits non-zero; **Fixer** runs. No direct report to you unless we exhaust fix rounds. Override with `-AgentTimeoutMinutes N`. |
| **Max rounds per run** | **10 rounds** | Prevents infinite re-run of the same 10 tasks if the task list is not updated. Loop exits 0 and tells you to fix CURRENT_TASK_LIST or generate a new list. Light intervention: update task statuses or create the next list. |
| **Task list complete** | N/A (success) | We report success: **Saved/Logs/automation_tasks_complete.md** and exit alert. Your only action: generate the next task list (see [HOW_TO_GENERATE_TASK_LIST.md](workflow/HOW_TO_GENERATE_TASK_LIST.md) and [TASK_LIST_REPEATS_LOG.md](workflow/TASK_LIST_REPEATS_LOG.md)). |

**Summary:** You are asked to **manually intervene** only when (1) the Guardian has run and written **automation_loop_breaker_report.md** (after 3 fix rounds), or (2) the loop exited after 10 rounds without the task list being updated (fix CURRENT_TASK_LIST or generate a new list), or (3) you choose to generate a new task list after all tasks are complete.

**Guardian (third agent – loop-breaker):** If the main loop and **Fixer** are in a **repeating failure loop** (same error or same exit code), the **Guardian** agent resolves it or writes a report. The **watcher** automatically invokes it when the same failure happens twice in a row, or when `MaxFixRounds` is reached. You can also run **`.\Tools\Guard-AutomationLoop.ps1`** manually. Use **`-CheckOnly`** to only detect (exit 1 = loop detected). Guardian activity is logged to **Saved/Logs/guardian.log**. For the full role model (Developer, Fixer, Guardian, Refiner) and accountability, see [docs/AGENT_COMPANY.md](AGENT_COMPANY.md).

**Run history for refinement:** All agent runs (main, fix, loop-breaker) are recorded in **Saved/Logs/agent_run_history.ndjson**. Use it with automation_errors.log and automation_loop_breaker_report.md to update rules and development strategy over time. See [docs/AUTOMATION_REFINEMENT.md](AUTOMATION_REFINEMENT.md).

---

## Plan-per-task

At the end of each session, the agent creates a short implementation plan for the **next** pending task (from CURRENT_TASK_LIST) so the next session has a clear, executable plan.

- **Option A:** Save the plan to `.cursor/plans/<task-id>-<slug>.md` and set NEXT_SESSION_PROMPT.md to tell the next session to execute that plan file.
- **Option B:** Embed the plan steps (goal, key steps, task doc link, success criteria) inside NEXT_SESSION_PROMPT.md so the next session's prompt both identifies the task (e.g. T4) and lists the plan.

The default prompt in RunAutomationLoop.ps1 and the content of NEXT_SESSION_PROMPT.md instruct the agent to create and save (or embed) the plan for the next pending task after marking the current task done. See [.cursor/commands/start-automation-cycle.md](../.cursor/commands/start-automation-cycle.md).

---

## Scheduling (run agents on a schedule)

To run the agent company (Watcher + Developer + Fixer + Guardian) on a schedule (e.g. nightly or at 9am), use the OS scheduler; no code changes are required.

- **Windows:** Use **Task Scheduler**. Create a task that runs at the desired time (e.g. 9:00 AM daily). **Action:** Start a program; **Program:** `powershell.exe`; **Arguments:** `-NoProfile -ExecutionPolicy Bypass -File "C:\path\to\HomeWorld\Tools\Start-AllAgents.ps1"` (use your project root path). Set **Start in** to the project root (e.g. `C:\dev\HomeWorld`) so relative paths and Resolve-ProjectRoot work. Ensure the user is logged in (or run the task with "Run whether user is logged on or not" and set up any required env vars like `UE_EDITOR` and `CURSOR_API_KEY` in the task or a wrapper script).
- **macOS / Linux:** Use **cron**. Example: run at 9:00 AM daily: `0 9 * * * cd /path/to/HomeWorld && pwsh -NoProfile -File ./Tools/Start-AllAgents.ps1 >> Saved/Logs/scheduled_run.log 2>&1` (adjust shell if you use `powershell` or `bash` to invoke PowerShell). Ensure `UE_EDITOR` and `CURSOR_API_KEY` are set (e.g. in the cron environment or in a small wrapper script that sources them and then runs Start-AllAgents.ps1).

The loop runs until the task list has no pending/in_progress tasks, stop is requested, or the Guardian reports. For a **webhook trigger** (e.g. from SwarmClaw or CI), you would run the same command from a webhook-triggered script or service; that is not built into the repo.

---

## Other options (manual or semi-automatic)

| Option | Description |
|--------|-------------|
| **Scheduled task + manual paste** | A scheduled task or reminder that opens Cursor and shows you NEXT_SESSION_PROMPT.md so you can paste it and start the next session quickly. |
| **UI automation** | A tool (e.g. AutoHotkey, Sikuli, or similar) that opens Cursor, focuses the chat, and pastes the contents of NEXT_SESSION_PROMPT.md. Still requires Cursor to be running and the automation to know when the agent has finished. |
| **Compound / workflow plugins** | If you use a plugin that can "execute plan until done" across multiple steps or sessions, that could drive the loop; configuration would be in that plugin. |

---

## Automation development standards

When adding or changing automation scripts (Tools/*.ps1), follow these standards so scripts stay consistent and avoid known errors:

- **UE_EDITOR:** Never call `Test-Path -LiteralPath $env:UE_EDITOR` without ensuring UE_EDITOR is set (passing null causes ParameterBindingValidationException). Use **Test-UE_EDITORSet** from [Tools/Common-Automation.ps1](../Tools/Common-Automation.ps1) (dot-source the script).
- **Paths:** Do not pass null or empty to `Test-Path -LiteralPath`; guard with `if (-not $var) { ... }` or use shared helpers.
- **Shared helpers:** Dot-source Common-Automation.ps1 and use **Test-UE_EDITORSet**, **Resolve-ProjectRoot**, and **Get-AgentExe** so automation scripts stay DRY and consistent. Resolve-ProjectRoot returns project root (HOMEWORLD_PROJECT or parent of Tools). Get-AgentExe accepts optional -AgentPath and returns the Cursor Agent CLI path or $null.
- **Single responsibility:** Keep each script focused (loop, watch, guard, refiner, gap-solver, prereqs, build); add new scripts or shared modules rather than overloading one script.
- **Reference:** See [docs/KNOWN_ERRORS.md](KNOWN_ERRORS.md) for past errors and fixes; check before changing automation or UE_EDITOR usage.

---

## Summary

- **Agent cannot self-start a new session.** Something external (you or a script) must start the next session and send the continue prompt.
- **In-repo:** Use CURRENT_TASK_LIST.md and NEXT_SESSION_PROMPT.md so each session knows what to do and the next session can be started with one paste.
- **"Done" = no pending/in_progress tasks.** The loop runs until CURRENT_TASK_LIST.md has no task with status pending or in_progress, or until a stop sentinel (Saved/Logs/agent_stop_requested) or Guardian report. To stop gracefully without killing the terminal, create that file; to stop immediately, use Ctrl+C.
- **Fully automatic loop:** Use the Cursor Agent CLI with RunAutomationLoop.ps1: it invokes the CLI with the prompt from NEXT_SESSION_PROMPT.md and repeats until Test-HasPendingTasks is false. See "Fully automatic loop with Cursor CLI" above.
