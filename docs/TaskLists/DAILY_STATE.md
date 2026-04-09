# Daily State

**Purpose:** This file is read at session start and updated at session end so you can ask "what did we do yesterday and what do we need to do today?" and get a clear answer. The agent updates it automatically when a session ends.

**Current focus:** Seventy-third task list **complete**. All T1–T10 done. First pending = none (user generates next list).

---

## Yesterday (last session)

What was completed or in progress in the previous session.

- Development environment upgrade: [docs/Setup/DEV_ENV_MATRIX.md](../Setup/DEV_ENV_MATRIX.md), `.vscode/extensions.json`, MCP_SETUP configuration audit, CI_SETUP runner/UE_EDITOR notes, KNOWN_ERRORS for Check-AutomationPrereqs; Safe-Build verified on this machine.

---

## Today

What we need to do today. Work from [CURRENT_TASK_LIST.md](CURRENT_TASK_LIST.md) and [ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md](ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md).

- **All T1–T10 complete.** No first pending task. Generate a new task list per [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md); then run `.\Tools\Start-AllAgents-InNewWindow.ps1` when ready. Phase 4 (Steam Demo store draft) skipped; next focus = assets, polish, or [NEXT_30_DAY_WINDOW.md](NEXT_30_DAY_WINDOW.md).

---

## Tomorrow

Preview of next focus.

- **After list 73:** Generate next list per [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md); then run `.\Tools\Start-AllAgents-InNewWindow.ps1`. Phase 4 skipped; next focus per [NEXT_30_DAY_WINDOW.md](NEXT_30_DAY_WINDOW.md) (assets, polish, deferred, etc.).

---

**How this is updated:** At the end of each task session, the agent (1) appends to [SESSION_LOG.md](../SESSION_LOG.md), (2) updates this file: **Yesterday** = what was done this session; **Today** = first pending task id from [CURRENT_TASK_LIST.md](CURRENT_TASK_LIST.md) (T1–T10); **Tomorrow** = next task id; (3) sets completed task status in CURRENT_TASK_LIST.md.
