# Task list debugging: false negatives and overwrites

**Purpose:** Document how we tell whether "tasks not completed" is a **bug** (persistence/parser) vs **agent behavior** (e.g. overwriting the file), and what logging and checks we use to avoid false positives/negatives.

**Last updated:** 2026-03-04

---

## 1. Evidence from the 2026-03-04 run (tenth list)

From the automation loop output:

| After round | Log line | Pending count |
|-------------|----------|----------------|
| 1 | "pending tasks remain (9 of 10); next pending: T2" | 9 |
| 2 | "pending tasks remain (8 of 10); next pending: T3" | 8 |
| 3 | "pending tasks remain (7 of 10); ..." | 7 |
| ... | ... | ... |
| 9 | "pending tasks remain (1 of 10); next pending: T10" | 1 |
| 10 | "pending tasks remain (10 of 10); next pending: T1" | **10** |

**Conclusion:** The loop re-reads `CURRENT_TASK_LIST.md` from disk after each round. Rounds 1–9 each saw the expected **decrease** in pending count (agent had set that task to `completed`). After round 10, the pending count **increased** from 1 to 10. So:

- **No parser bug:** The parser and loop logic are correct; they reflect the file contents.
- **No "never persisted" bug:** Rounds 1–9 did persist (file was updated).
- **Round 10 agent overwrote the file:** The agent, when doing T10 (buffer: update ACCOMPLISHMENTS §4 and PROJECT_STATE §4), likely **replaced** `CURRENT_TASK_LIST.md` with a new or template version (e.g. "generate the next list") and left all statuses `pending`. So this is **agent behavior**, not a script bug.

**False negative:** We initially thought "tasks not set to completed" — in fact they were set for T1–T9, then round 10 undid that by overwriting the file.

**False positive risk:** We do not independently verify that the agent *did* the work for each task; we only observe that the file had one fewer pending task. So an agent could set status to `completed` without doing the work. Mitigation: success criteria in each task and SESSION_LOG/ACCOMPLISHMENTS; no automated content verification in the loop today.

---

## 2. Logging we have (and where it lives)

| Log | Location | What it tells us |
|-----|----------|------------------|
| **automation_loop.log** | Saved/Logs/ | Each round start (pending count), agent finish (exit code), "pending tasks remain (N of 10)". **Key for debugging:** if N goes 9→8→…→1 then 10, the file was overwritten after round 10. |
| **automation_events.log** | Saved/Logs/ | High-level events: task_started, round_completed, loop_exited_ok/fail. Confirms order of events. |
| **agent_run_history.ndjson** | Saved/Logs/ | One record per agent run (role, round, exit code, error summary). Does not record "which task" or "did file change"; use with loop log. |
| **automation_errors.log** | Saved/Logs/ | Errors only (non-zero exit, and now: task list overwrite warning). Check here when loop exits 1 after "overwrite detected". |
| **CURRENT_TASK_LIST.md** | docs/workflow/ | Source of truth. Loop reads it after each round. If an agent overwrites it, the next read sees the new content. |
| **SESSION_LOG.md** | docs/ | Agent is supposed to append per round; confirms what the agent claims it did (not machine-verified). |

**Saved/ is gitignored** — these logs are local. For remote debugging, capture `automation_loop.log` and `automation_errors.log` (or their tails) when reporting an issue.

---

## 3. Checks we added to reduce overwrites and false conclusions

### 3.1 Post-round consistency check (RunAutomationLoop.ps1)

After each successful round we compare:

- `pendingCountAtStart` = pending count at **start** of the round  
- `taskStateAfter.PendingCount` = pending count **after** the round (re-read from disk)

If **pending count increased** (`taskStateAfter.PendingCount -gt pendingCountAtStart`):

- We log a **WARNING** to the loop log and to **automation_errors.log**.
- We write a **loop_exited_fail** event.
- We call **Invoke-ExitStatusAlert** with reason "Task list overwrite detected" and **exit 1** so the Watcher/Fixer runs and the user sees the alert.

So we **detect** overwrites (or any regression in pending count) and **stop** the loop instead of running more rounds with a broken list.

### 3.2 T10 prompt clarification (default prompt + NEXT_SESSION_PROMPT)

- **Default prompt:** "If your task is T10 (buffer): update only ACCOMPLISHMENTS_OVERVIEW §4 and PROJECT_STATE_AND_TASK_LIST §4 and set T10 status to completed in CURRENT_TASK_LIST; do NOT replace or regenerate CURRENT_TASK_LIST.md (the user generates the next list after the loop exits)."
- **NEXT_SESSION_PROMPT:** Explicit "When your task is T10: ... Do **not** replace or regenerate CURRENT_TASK_LIST.md in this session."

This reduces the chance the T10 agent will "generate the next list" and overwrite the current file.

### 3.3 Max rounds cap (existing)

If the file is still wrong after 10 rounds, the loop exits 0 at 10 rounds and tells the user to fix CURRENT_TASK_LIST. Prevents infinite re-runs.

---

## 4. How to debug "tasks not completed" in future

1. **Check automation_loop.log** (or the terminal output): After each round, does "pending tasks remain (N of 10)" **decrease** (9, 8, 7, …) or **increase** or stay same?
   - **Decreases each time:** Agent is updating the file; if you still see "10 pending" at the end, something reverted the file later (e.g. round 10 overwrite) or you're looking at a different run.
   - **Increases after a round:** Overwrite or bad edit; consistency check will now exit 1 and log to automation_errors.log.
   - **Stays same after a round:** Agent exited 0 but did not set the task to completed (possible false positive for "task done").

2. **Check automation_errors.log:** Look for "Task list pending count INCREASED" or "overwrite detected".

3. **Check CURRENT_TASK_LIST.md** on disk: Are T1–T10 statuses `completed` or `pending`? If all pending after a "complete" run, the file was overwritten or never updated.

4. **Check SESSION_LOG.md:** What does the agent claim it did last round? Compare to what the loop log says (pending count).

---

## 5. Session validity: when to re-attempt vs treat as complete

### Ruling for the 2026-03-04 tenth-list run

**Evidence:**

1. **Loop log:** After rounds 1–9, pending count was 9, 8, 7, 6, 5, 4, 3, 2, 1. So the agent **did** update `CURRENT_TASK_LIST.md` (set that task’s status to `completed`) in each of those rounds. The **marking** (status) was working.
2. **After round 10:** Pending count went from 1 to 10. So round 10’s agent **overwrote** the file (e.g. wrote a new list with all `pending`). That is the **only** bug: agent behavior in round 10, not a bug in “how we mark things completed.”
3. **No parser or persistence bug:** The loop re-reads the file from disk each time; it correctly showed 9→8→…→1. The file was correct after rounds 1–9 and wrong only after round 10.

**Conclusion:** The tenth-list run is **valid**. The only failure was round 10 overwriting the task list. We do **not** re-attempt T1–T10 of the tenth list.

**Actions taken:** (1) Set all T1–T10 to `completed` in `CURRENT_TASK_LIST.md`. (2) Added tenth cycle to ACCOMPLISHMENTS_OVERVIEW §4. (3) Updated PROJECT_STATE_AND_TASK_LIST §3 and §4 to “tenth list complete” and “next = generate new list.” (4) Documented here so future sessions do not re-run the same tenth-list tasks.

### Policy for future “pending again” after a run

- If the **loop log** shows pending count **decreasing** each round (9, 8, 7, … 1) and then either (a) “no pending; exiting” or (b) next round shows **10 pending** again → treat as **valid run + overwrite in last round**. Fix the file (set completed), update ACCOMPLISHMENTS and PROJECT_STATE, and **do not** re-attempt the same list.
- If the loop log shows pending count **never decreasing** (always 10 after every round) → then investigate a real persistence or agent bug (agent not writing the file, or path/perms issue).

---

## 6. References

- [TASK_LIST_REPEATS_LOG.md](TASK_LIST_REPEATS_LOG.md) — Why tasks repeat; cause (A) = status not persisted / file overwritten.
- [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md) — When and how to generate the **next** list (after loop exits, not during T10).
- RunAutomationLoop.ps1 — Get-TaskListState (reads file), post-round consistency check, default prompt T10 clause.
- **Session validity:** §5 above — when to re-attempt vs treat as complete; ruling for the tenth-list run.
