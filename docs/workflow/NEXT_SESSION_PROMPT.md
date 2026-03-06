# Next session prompt

**Twenty-ninth task list is active (rapid prototyping).** Work on the first **pending** task (T1) from [CURRENT_TASK_LIST.md](CURRENT_TASK_LIST.md). Run 3 of 4 toward polished MVP per [MVP_GAP_ANALYSIS.md](MVP_GAP_ANALYSIS.md).

---

**At session start:** Read [DAILY_STATE.md](DAILY_STATE.md), [CURRENT_TASK_LIST.md](CURRENT_TASK_LIST.md), and [SESSION_LOG.md](../SESSION_LOG.md). Work only on **T1-T10**; do not add T11 or new task sections—document new work in SESSION_LOG or [AUTOMATION_GAPS.md](../AUTOMATION_GAPS.md). Work on the first **pending** task (T1: Pre-demo verification entry point — link §3 and CONSOLE_COMMANDS from one doc). Complete one task per round. **When you complete a task, you MUST update CURRENT_TASK_LIST.md:** set only that task's **status** to `completed`; do not change any other task's status. **If the task is about a deferred feature** (e.g. agentic building): also update [PROJECT_STATE_AND_TASK_LIST.md](PROJECT_STATE_AND_TASK_LIST.md) §2 **Deferred features** table (Last list/date or status) when outcome is still deferred so the next list generator has current status. Then update SESSION_LOG and DAILY_STATE at session end.

**Canonical workflow:** Fetch task → implement → decide build/Editor → validate in Editor (MCP, PIE, pie_test_runner) when applicable → debug until success → finish → **update CURRENT_TASK_LIST.md status** → fetch next. When C++ or Build.cs change, the loop runs Safe-Build after the round. Exit non-zero on validation failure so Fixer runs.

**When your task is T10 (buffer):** Update only ACCOMPLISHMENTS_OVERVIEW §4 and PROJECT_STATE_AND_TASK_LIST §4 and set **T10 status to completed** in CURRENT_TASK_LIST. Do **not** replace or regenerate CURRENT_TASK_LIST.md in this session (the user does that after the loop exits). **When all T1-T10 are complete** (after loop exits): user generates the next list per [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md), then runs `.\Tools\Start-AllAgents-InNewWindow.ps1`.
