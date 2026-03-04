# Daily State

**Purpose:** This file is read at session start and updated at session end so you can ask "what did we do yesterday and what do we need to do today?" and get a clear answer. The agent updates it automatically when a session ends.

**Current focus:** Eighth task list complete (all T1–T10 done). Next = generate new 10-task list.

---

## Yesterday (last session)

What was completed or in progress in the previous session.

- **T10 (eighth list) completed.** ACCOMPLISHMENTS_OVERVIEW §4: eighth-cycle row updated (all T1–T10 completed; Next = generate new list + run Start-AllAgents-InNewWindow.ps1). PROJECT_STATE_AND_TASK_LIST §4: list complete; next step = generate list per HOW_TO_GENERATE_TASK_LIST then run Start-AllAgents. T10 status set to completed in CURRENT_TASK_LIST.

---

## Today

What we need to do today. Work from [CURRENT_TASK_LIST.md](CURRENT_TASK_LIST.md) and [ACCOMPLISHMENTS_OVERVIEW.md](ACCOMPLISHMENTS_OVERVIEW.md).

- **Generate new 10-task list** — All T1–T10 complete. Generate the next list per [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md) (read [TASK_LIST_REPEATS_LOG.md](TASK_LIST_REPEATS_LOG.md) and ACCOMPLISHMENTS_OVERVIEW §4 to avoid duplicating completed work). Then run `.\Tools\Start-AllAgents-InNewWindow.ps1` for the next cycle.

---

## Tomorrow

Preview of next focus.

- **Run next automation cycle** — After the new list is generated, run Start-AllAgents-InNewWindow.ps1; agent will pick first pending task from the new list.

---

**How this is updated:** At the end of each task session, the agent (1) appends to [SESSION_LOG.md](../SESSION_LOG.md), (2) updates this file: **Yesterday** = what was done this session; **Today** = first pending task id from [CURRENT_TASK_LIST.md](CURRENT_TASK_LIST.md) (T1–T10); **Tomorrow** = next task id; (3) sets completed task status in CURRENT_TASK_LIST.md.
