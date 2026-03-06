# Cycle state

**Superseded:** The active loop uses **[CURRENT_TASK_LIST.md](CURRENT_TASK_LIST.md)** and **RunAutomationLoop.ps1** (status in CURRENT_TASK_LIST only). This file is kept for reference only.

---

Used by the automatic development cycle to avoid infinite loops. The agent reads this at the start of each iteration and updates it after implement/test/debug/finalize.

**Fields:**
- **current_task_index** — Which task in CYCLE_TASKLIST (1-based).
- **retry_count** — Number of failures for the current task this run.
- **last_error_summary** — Short fingerprint of the last failure (e.g. log line or error type) for same-failure guard.
- **last_outcome** — `pass` | `fail` | `blocked`
- **blocked_reason** — Set when task is marked blocked (e.g. after max retries).

**Loop guards:** Max 3 retries per task; if last_error_summary unchanged after a retry, count no-progress (after 2 no-progress, try different approach or mark blocked). Before retry, agent must state what changed (hypothesis, fix, or research).

---

- **current_task_index:** 1
- **retry_count:** 0
- **last_error_summary:** (none)
- **last_outcome:** (none)
- **blocked_reason:** (none)
