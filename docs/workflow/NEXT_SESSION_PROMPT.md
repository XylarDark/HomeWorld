# Next session prompt

**Eighth task list is active (MVP-focused).** Work on the first **pending** task (T1) from [CURRENT_TASK_LIST.md](CURRENT_TASK_LIST.md).

---

**At session start:** Read [DAILY_STATE.md](DAILY_STATE.md), [CURRENT_TASK_LIST.md](CURRENT_TASK_LIST.md), and [SESSION_LOG.md](../SESSION_LOG.md). Work only on **T1-T10**; do not add T11 or new task sections—document new work in SESSION_LOG or [AUTOMATION_GAPS.md](../AUTOMATION_GAPS.md). Work on the first **pending** task (T1: PIE pre-demo checklist). Complete one task per round. **When you complete a task, you MUST update CURRENT_TASK_LIST.md:** set only that task's **status** to `completed`; do not change any other task's status. Then update SESSION_LOG and DAILY_STATE at session end.

**Canonical workflow:** Fetch task → implement → decide build/Editor → validate in Editor (MCP, PIE, pie_test_runner) when applicable → debug until success → finish → **update CURRENT_TASK_LIST.md status** → fetch next. When C++ or Build.cs change, the loop runs Safe-Build after the round. Exit non-zero on validation failure so Fixer runs.

**When all T1-T10 are complete:** Generate the next 10-task list per [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md). When generating the list, read [TASK_LIST_REPEATS_LOG.md](TASK_LIST_REPEATS_LOG.md) and ACCOMPLISHMENTS_OVERVIEW §4 to avoid duplicating completed work. Then run `.\Tools\Start-AllAgents-InNewWindow.ps1` for the next cycle.
