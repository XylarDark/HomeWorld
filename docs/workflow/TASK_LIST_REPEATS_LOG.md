# Task list repeats: causes and how we address them

**Purpose:** Log why the same or similar tasks appear across sessions and what we do (or can do) to reduce repeats. Use this when generating new task lists and when debugging "why did we run this again?"

**Last updated:** 2026-03-05

---

## 1. Why you see repeated tasks

### A. Status not persisted (loop re-runs same list)

**What happens:** The automation loop reads `CURRENT_TASK_LIST.md` each round. If the agent completes a task but **does not write** `- **status:** completed` for that task (or the file is reverted/lost), the next round still sees that task as pending. The loop then runs the same task again, or after 10 rounds the list still shows 10 pending and the loop would start round 11 on T1.

**Observed:** 2026-03-04 sixth-list run: loop completed 10 rounds (T1→T10) but after round 10 reported "pending tasks remain (10 of 10)" and started round 11 on T1. Root cause: `CURRENT_TASK_LIST.md` was not updated with `status: completed` for the tasks the agent had completed (or changes were not saved).

**References:** LAST_SESSION_AUDIT_AND_MVP_REMAINING.md §1 (Sixth-list automation run); SESSION_LOG entries 2026-03-05 (task list fix, max rounds).

---

### B. Re-verification by design (intentional repeats)

**What happens:** New task lists are generated with goals like "Re-run vertical slice pre-demo checklist" or "PIE-with-validation" so that a **later** run can re-verify the slice or run PIE tests. The same *type* of work (e.g. "run pie_test_runner with PIE") appears in multiple lists (e.g. second, third, sixth, seventh, eighth) because we want to confirm the slice or PIE flow still works after other changes.

**Observed:** Vertical slice checklist / PIE validation appears as T1 or T2 in several lists; portal LevelToOpen and State Tree Defend appear in multiple lists as "verify or document."

**References:** ACCOMPLISHMENTS_OVERVIEW §4 (cycle summaries); VERTICAL_SLICE_CHECKLIST §3 (verification outcomes per list).

---

### C. New list overlaps with previous list’s scope

**What happens:** When we generate a "new" 10-task list, we pull from ACCOMPLISHMENTS_OVERVIEW, NEXT_30_DAY_WINDOW, PROJECT_STATE, and AUTOMATION_GAPS. If the previous list did not have all tasks marked completed in the file (see A), or if the generator does not exclude already-done work, the new list can include tasks that are semantically the same as ones already completed (e.g. "SaveGame persistence," "portal verify," "docs polish").

**Observed:** Seventh and eighth lists both have PIE validation, portal, State Tree Defend, SaveGame, packaging, docs polish, buffer. Some of this is intentional (e.g. buffer every list); some is overlap because we keep re-verifying or the generator doesn’t explicitly skip "already done" items.

**References:** HOW_TO_GENERATE_TASK_LIST (sources); ACCOMPLISHMENTS_OVERVIEW §4.

---

### D. Gaps and deferred work reappear

**What happens:** AUTOMATION_GAPS and deferred features (e.g. portal LevelToOpen, State Tree Defend, full agentic building) don’t have a one-shot fix. So we add "verify or document" tasks in several lists to (1) try again with new scripts/APIs or (2) document current status. Those tasks look repeated because the *underlying* work (close the gap) isn’t done yet.

**Observed:** Portal (Gap 1) and State Tree (Gap 2) appear in multiple lists as "verify or document"; each cycle may add scripts or docs but the gap stays open until manual steps or new API is used.

**References:** AUTOMATION_GAPS.md; LAST_SESSION_AUDIT_AND_MVP_REMAINING §3.

---

## 2. How we address repeats

### Already in place

| Measure | What it does |
|--------|----------------|
| **Prompt: must update CURRENT_TASK_LIST** | RunAutomationLoop default prompt and NEXT_SESSION_PROMPT tell the agent: when you complete a task, you MUST update `docs/workflow/CURRENT_TASK_LIST.md` and set only that task’s `- **status:**` to `completed`. Reduces (A). |
| **Max 10 rounds per run** | RunAutomationLoop exits after 10 rounds even if the file still shows pending. Prevents infinite re-run of the same 10 tasks when status isn’t persisted. Reduces (A). |
| **Parser fix** | Task list parser uses `\z` (end of string) so it correctly counts pending in T1–T10. Avoids mis-counts that could cause early exit or wrong "next" task. |
| **ACCOMPLISHMENTS_OVERVIEW §4** | Each cycle’s outcome is summarized (e.g. "T1–T10 completed" or "T1 completed; T2–T10 pending"). When generating the *next* list, the generator should read this and avoid duplicating completed work unless re-verification is intended. Reduces (C). |

### When generating a new list (checklist)

To reduce unnecessary repeats when creating the next CURRENT_TASK_LIST:

1. **Read ACCOMPLISHMENTS_OVERVIEW §4** — Which cycle just finished? Which tasks were completed? Don’t add the same task again unless the goal is explicit **re-verification** (e.g. "Re-run vertical slice checklist after code changes").
2. **Read CURRENT_TASK_LIST.md** (before replacing) — If the file still has pending tasks, prefer **continuing** that list (or copying pending items into the new list) instead of discarding and re-adding similar goals.
3. **Re-verification vs new work** — If a task is "re-run X" or "re-verify Y," name it clearly (e.g. "Re-run vertical slice pre-demo checklist") so it’s obvious it’s intentional. For net-new work, prefer tasks that don’t duplicate §4 completed items.
4. **Gaps** — For AUTOMATION_GAPS items, "verify or document" is a valid repeat until the gap is closed; optionally add a note in the task (e.g. "Gap 1 still open; verify or document current status") so it’s clear why it’s there again.

---

## 3. Log of repeat-related changes (chronological)

| Date | Change | Purpose |
|------|--------|--------|
| 2026-03-05 | RunAutomationLoop default prompt: explicit "you MUST update CURRENT_TASK_LIST.md … set only that task's status to completed." | Reduce (A): agent must persist completion. |
| 2026-03-05 | NEXT_SESSION_PROMPT: same requirement; "update CURRENT_TASK_LIST.md status" in workflow. | Reduce (A). |
| 2026-03-05 | Max 10 rounds cap in RunAutomationLoop. | If (A) still happens, loop exits after 10 rounds instead of restarting from T1. |
| 2026-03-05 | Task list parser: `$` → `\z` in section regex. | Correct pending count so loop doesn’t exit early or mis-identify next task. |
| 2026-03-05 | TASK_LIST_REPEATS_LOG.md (this file) created. | Single place to log causes and mitigations; reference from HOW_TO_GENERATE_TASK_LIST. |

---

## 4. References

- **Task list generation:** [HOW_TO_GENERATE_TASK_LIST.md](HOW_TO_GENERATE_TASK_LIST.md) (sources; use ACCOMPLISHMENTS_OVERVIEW to avoid duplicating completed work).
- **Audit and MVP remaining:** [LAST_SESSION_AUDIT_AND_MVP_REMAINING.md](LAST_SESSION_AUDIT_AND_MVP_REMAINING.md).
- **Cycle outcomes:** [ACCOMPLISHMENTS_OVERVIEW.md](ACCOMPLISHMENTS_OVERVIEW.md) §4.
- **Gaps:** [AUTOMATION_GAPS.md](../AUTOMATION_GAPS.md).
