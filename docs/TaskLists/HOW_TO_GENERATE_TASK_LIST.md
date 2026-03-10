# How to generate the current task list

The automation loop is driven by **one task list**: `docs/workflow/CURRENT_TASK_LIST.md`. It must contain exactly **10 tasks** (T1–T10) with a consistent schema. The loop counts only T1–T10; do not add T11 or new task sections—document new work in SESSION_LOG or AUTOMATION_GAPS.md for the next list. This doc describes how to create or replace that list so agents have the best chance of one-shot success.

## Task list composition: dynamic by development phase (policy)

**Goal:** Maximize both **quality** and **quantity** of development depending on the current needs of the cycle. Avoid spending too many tokens on verification when we are in rapid prototyping; avoid skipping verification when we are hardening for demo or release.

**How to choose the split:** Read **PROJECT_STATE_AND_TASK_LIST.md §0 "Current development phase"**. It defines two phases and how many of the 10 tasks should be implementation vs verification. The task list generator **must** use that section to decide the split for the next list.

- **Rapid prototyping:** More **implementation** slots (e.g. 7–8 of 10). Testable feature/code work: implement a system, add an ability, wire a flow, fix a bug with a test. Success criteria must be testable (PIE, test pass, build, script run). Fewer verification slots (2–3): e.g. one PIE or build check, T10 buffer; optional docs/gaps. Use when adding features, exploring systems, building out MVP.
- **Prototype hardening:** Balanced or verification-heavy (e.g. 4–5 implementation, 5–6 verification). Verification = run PIE pre-demo checklist, run packaged build and smoke-test, document in VERTICAL_SLICE_CHECKLIST, update AUTOMATION_GAPS, polish KNOWN_ERRORS/CONVENTIONS, refinement from run history, buffer (ACCOMPLISHMENTS + PROJECT_STATE §4). T10 remains the buffer task (do not replace the task list). Use when preparing for demo, playtest, or release; or when stabilizing after a big push.

**When generating a new list:** (1) Read PROJECT_STATE_AND_TASK_LIST §0 and note **Current phase**. (2) Assign that many slots to **testable implementation** (fill first slots T1, T2, …). (3) Assign the remaining slots to **verification and support**. This keeps the list dynamic to our needs. **When to change phase:** Update PROJECT_STATE_AND_TASK_LIST §0 "Current phase" when the team shifts (e.g. "We're two weeks from a demo" → set to **Prototype hardening**; "We're adding the next feature set" → **Rapid prototyping**).

### Consolidate overhead so more slots are substantive (policy)

**Problem:** Many lists have used 4–5 tasks for small, recurring overhead (vertical slice §4 N-th deliverables, CONSOLE_COMMANDS refresh, KNOWN_ERRORS/AUTOMATION_GAPS cycle note, build verification, doc review, task list validation). That leaves only 3–4 slots for real implementation.

**Policy:** Consolidate so that **more of the 10 tasks are substantive work**:

- **One "Docs and cycle" task** (e.g. T8): Combine vertical slice §4 N-th-list deliverables, CONSOLE_COMMANDS or workflow doc update, and KNOWN_ERRORS/AUTOMATION_GAPS cycle note into a **single task**. Success = all three done (or explicitly deferred) in one go.
- **One "Verification" task** (e.g. T9): Combine build run (if C++/config changed), doc review (VERTICAL_SLICE_CHECKLIST §3–§4, CONSOLE_COMMANDS), and task list validation (validate_task_list.py, DAILY_STATE) into a **single task**. Success = build green, docs reviewed, list validated.
- **T10** remains the buffer task (ACCOMPLISHMENTS + PROJECT_STATE §4; do not replace CURRENT_TASK_LIST).

**Resulting shape (rapid prototyping):** T1–T7 = **implementation** (build/code/feature/test; each task should be a meaningful chunk of work). T8 = **Docs and cycle** (combined). T9 = **Verification** (combined). T10 = **Buffer**. That gives **7 implementation slots** instead of 3–4, so more work gets done per list. Use bigger, multi-step implementation tasks where it makes sense (e.g. "Implement X and add a test" or "Add feature A and wire it in B").

## Avoiding repeated tasks

If the same or similar tasks keep appearing across sessions, see **[TASK_LIST_REPEATS_LOG.md](TASK_LIST_REPEATS_LOG.md)** for causes (status not persisted, re-verification by design, overlap when generating new lists, gaps reappearing) and how we address them. When generating a new list: read **ACCOMPLISHMENTS_OVERVIEW §4** so you don't duplicate completed work unless you intend re-verification; prefer continuing or carrying over pending tasks instead of re-adding the same goals.

**Deferred features:** Read **PROJECT_STATE_AND_TASK_LIST.md §2 "Deferred features"**. Do **not** add another task that only "verify or document" a deferred feature (e.g. agentic building, death-to-spirit, SaveGame) if that feature was already verified or documented in the last 1–2 lists. Add a "deferred" task only if the goal is to **implement** the feature (e.g. full agentic building per DAY10 Option B) or to re-verify after major code changes. This prevents re-doing the same verification cycle.

---

## Sources to use

Gather detail from:

- **VISION.md** — theme, campaign, playtest gates, Act 1/2 scope.
- **ACCOMPLISHMENTS_OVERVIEW.md** — high-level record of all work accomplished; use with task list and vision to avoid duplicating and to inform next tasks. **Check §4** before adding a task that might already be completed in a prior cycle (see TASK_LIST_REPEATS_LOG).
- **AUTOMATION_GAPS.md** — known gaps, manual steps, and workarounds.
- **NEXT_30_DAY_WINDOW.md** — near-term priorities (N1–N4, etc.).
- **PROJECT_STATE_AND_TASK_LIST.md** — overall state and task context; **§0 "Current development phase"** is the single source of truth for how many tasks are implementation vs verification (read it first when building the list).
- **Existing task docs** in `docs/tasks/` (e.g. DAY5_PLAYTEST_SIGNOFF, DAY12_ROLE_PROTECTOR, DAY10_AGENTIC_BUILDING).
- **Epic/UE docs** and project docs (CONVENTIONS.md, KNOWN_ERRORS.md, PCG_SETUP.md, etc.) for APIs and pitfalls.

## Rule: maximize detail for one-shot success

Each of the 10 tasks should be filled with **research-backed detail**:

- **goal** — One or two sentences; what “done” means.
- **success_criteria** — Verifiable outcomes (e.g. “PIE shows X”, “File Y exists”, “Test Z passes”).
- **research_notes** — Key findings: APIs, doc links, known pitfalls, AUTOMATION_GAPS references. This is what lets the agent avoid re-researching and complete the task in one go.
- **steps_or_doc** — Bullet list or links to task docs, CONVENTIONS, KNOWN_ERRORS.
- **status** — `pending` | `in_progress` | `completed` | `blocked`. The loop continues while any task is `pending` or `in_progress`.

## Process

1. **Copy the template:** Copy `CURRENT_TASK_LIST_TEMPLATE.md` to `CURRENT_TASK_LIST.md` (or overwrite the existing `CURRENT_TASK_LIST.md`).
2. **Fill each slot T1–T10:** Read **PROJECT_STATE_AND_TASK_LIST.md §0** for the current development phase. Respect **Task list composition** above: assign that many slots to **testable implementation** (build/code/feature with testable success criteria), and the rest to **verification and support** (PIE checklist, packaged build, docs, AUTOMATION_GAPS, refinement, buffer). T10 is always the buffer task. For each task, paste or write goal, success_criteria, research_notes, and steps_or_doc from the sources above. Set **status** to `pending` for work to do, `completed` for already-done items, or `blocked` if blocked with a reason.
3. **Run the loop:** The automation loop reads `CURRENT_TASK_LIST.md`, fetches the first pending/in_progress task, and runs until the list has no pending/in_progress tasks (or until a stop sentinel or Guardian report).

No automated “research and fill” script is required; you (or a future generator) can fill the template manually or via script. The loop only needs the file to exist and to use the 10-task schema with **status** lines.

## Validation

Run the validator to ensure `CURRENT_TASK_LIST.md` is well-formed before starting the loop (or in CI):

```bash
python Content/Python/validate_task_list.py
```

The script checks that all T1–T10 sections exist, each task has **goal**, **success criteria**, **research_notes** (or **implementation_notes**), **steps_or_doc**, and **status**, and that each **status** is one of `pending`, `in_progress`, `completed`, or `blocked`. Exit code 0 if valid, 1 otherwise with a clear message for the first missing or invalid item.

## Derive from 30-day status

To derive a new 10-task list from the current 30-day implementation status and schedule:

1. Run: `python Content/Python/migrate_30day_to_task_list.py`
2. The script writes a draft to `Saved/Logs/current_task_list_draft.md` (it does not overwrite `CURRENT_TASK_LIST.md`).
3. Copy the draft to `docs/workflow/CURRENT_TASK_LIST.md` and add **research_notes** (and tune goal/success_criteria) as needed.
4. Run `python Content/Python/validate_task_list.py` to confirm the list is valid.

The mapping of day ranges to T1–T10 is in `docs/workflow/30DAY_TO_10TASK_MAPPING.json`. Use `--write` only if you intend to overwrite `CURRENT_TASK_LIST.md` from the script (not recommended for normal iteration).

## Replacing the list

To start a new window of work: replace `CURRENT_TASK_LIST.md` with a new 10-task list (from the template or from scratch). Ensure every task has a **status** line so `Test-HasPendingTasks` works correctly. The loop will then run on the new list until it is complete or stopped.
