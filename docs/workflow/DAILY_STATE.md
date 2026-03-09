# Daily State

**Purpose:** This file is read at session start and updated at session end so you can ask "what did we do yesterday and what do we need to do today?" and get a clear answer. The agent updates it automatically when a session ends.

**Current focus:** Seventy-first task list — **Assets + Steam Demo Phase 1 (Asset workflow and tooling)**. First pending = T7 (Phase 1 gate — document completion).

---

## Yesterday (last session)

What was completed or in progress in the previous session.

- List 71 (Phase 1 Asset workflow): T6 completed — Phase 1 entry point and phased doc link: added "Phased execution" pointer in NEXT_30_DAY_WINDOW to ASSETS_AND_STEAM_DEMO_PHASED_APPROACH; added Phase 1 gate outcome (List 71) to phased doc. ASSET_WORKFLOW_AND_STEAM_DEMO already referenced phased approach.

---

## Today

What we need to do today. Work from [CURRENT_TASK_LIST.md](CURRENT_TASK_LIST.md) and [ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md](ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md).

- **First pending: T7** — Phase 1 gate — document completion. Then T8–T10 (Docs and cycle, Verification, Buffer).

---

## Tomorrow

Preview of next focus.

- After list 71: Phase 2 (Image-to-3D deferred pass) or Phase 3 (Steam Demo packaged build + smoke test) per [ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md](ASSETS_AND_STEAM_DEMO_PHASED_APPROACH.md); or **Preparing assets** / **Steam Demo prep** per [NEXT_30_DAY_WINDOW.md](NEXT_30_DAY_WINDOW.md). Act 2 prep is not in current scope.

---

**How this is updated:** At the end of each task session, the agent (1) appends to [SESSION_LOG.md](../SESSION_LOG.md), (2) updates this file: **Yesterday** = what was done this session; **Today** = first pending task id from [CURRENT_TASK_LIST.md](CURRENT_TASK_LIST.md) (T1–T10); **Tomorrow** = next task id; (3) sets completed task status in CURRENT_TASK_LIST.md.
