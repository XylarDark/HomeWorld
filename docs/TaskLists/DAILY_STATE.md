# Daily State

**Purpose:** This file is read at session start and updated at session end so you can ask "what did we do yesterday and what do we need to do today?" and get a clear answer. The agent updates it automatically when a session ends.

**Current focus:** DevEnvTemplate fully adopted locally (gitlink `2997a3d`, skills, human-use, sync/doctor scripts). Next: commit/push adoption if not already; generate next task list when ready.

---

## Yesterday (last session)

- Full DevEnvTemplate adoption: gitlink `2997a3d`, `.gitmodules`, core skills localized, skills-extras + `docs/human-use/`, AGENTS.md layer table + accepted declines, doctor/sync verified.
- Blender Lab MCP connected (official `blender-mcp.exe`, not PyPI).

---

## Today

- Confirm adoption commit is on `main` if desired.
- Optional: Editor batch import + PIE verification; generate next task list per [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md).

---

## Tomorrow

- Assets / polish / next task list; optional later migration of retired always-on Cursor rules into AGENTS.md + skills.

---

**How this is updated:** At the end of each task session, the agent (1) appends to [SESSION_LOG.md](../SESSION_LOG.md), (2) updates this file: **Yesterday** = what was done this session; **Today** = first pending task id from [CURRENT_TASK_LIST.md](CURRENT_TASK_LIST.md) (T1–T10); **Tomorrow** = next task id; (3) sets completed task status in CURRENT_TASK_LIST.md.
