# Agent decision log

Append-only record of decisions the **agent owns**.

## Why this file exists

Until 2026-10-01 the project stamped human approval on three jobs: **steer**,
**taste** and **test**. On 2026-10-01 the ownership model was narrowed by Lead
decision:

| Domain | Owner |
| ------ | ----- |
| **Art design** (art bible, palette, tone, shots, stills accept/reject) | **Human** |
| **Game mechanic design** (beats, inventories, mechanics canon) | **Human** |
| **Test** (what "done" means, rubrics, verify bar, ship/no-ship, beat acceptance) | **Human** |
| **Code design** (module boundaries, where new code goes, shared utils, extract-to-library) | **Agent** |
| **Architecture** (purpose, directory map, module depth, tradeoffs) | **Agent** |
| **Harness refactoring** (rules, skills, scripts, scorers, CI) | **Agent** |

Removing a stamp is not the same as removing the record. Before, an architecture
decision waited for a human and was then visible in the discussion. If it is now
agent-owned and *silent*, the decision is still invisible — just later, when
someone reads the diff and wonders why. So every agent-owned design decision gets
one row here: what was decided, why, and what would reverse it.

This log is **not** a taste profile. It records engineering decisions. Taste
decisions are stamped by the human and belong in
[taste-profile.md](../human-use/taste-profile.md).

## How to add a row

Append at the end. Do not renumber. Do not rewrite history — supersede with a
pointer.

```markdown
### DEC-NNNN — short title (YYYY-MM-DD)

- **Area:** code design | architecture | harness refactor
- **Decision:** one sentence, in the active voice. "Use X", not "we will use X".
- **Rationale:** why this and not the obvious alternative. Name the alternative.
- **Evidence:** the measurement, test, or file that justifies it. A number beats
  an opinion; if there is none, say so — "no evidence, agent judgement".
- **Reverses if:** the condition that would make this wrong. Cheap to state.
- **Supersedes:** DEC-NNNN, if any.
```

A decision that cannot state its alternative has not been made yet — it has been
skipped.

## Entries

### DEC-0001 — Harness lift is measured on conformance, with completion as the control (2026-10-01)

- **Area:** harness refactor
- **Decision:** Score agent output on two check classes. Measure lift on the
  `conformance` class only, and treat `completion` as a control that must not
  regress.
- **Rationale:** The alternative was a single pass/fail score per task. A harness
  could then "win" by making the agent emit more files and more prose, which is
  volume, not quality. Separating the classes means a conformance gain only counts
  if the agent still completed the task at least as often.
- **Evidence:** Design rationale; no measurement yet. The pilot that motivated it
  is in `scripts/task-lift.js` and `docs/qa/TASK_LIFT.md`.
- **Reverses if:** A real run shows conformance and completion move together with
  no trade-off, in which case one class is redundant and the manifest can shrink.

### DEC-0002 — Ablation removes harness files from the working tree (2026-10-01)

- **Area:** harness refactor
- **Decision:** The "without harness" arm is a separate `git worktree` at the same
  commit with `AGENTS.md`, `.cursor/`, `.agents/`, `swarm/` and `UserHarness`
  deleted, driven by a fresh `opencode run --standalone` process.
- **Rationale:** The alternative was prompting the agent not to read the rules.
  A prompt is a suggestion the agent may honour and the evaluator cannot verify,
  so the measurement would have compared the harness against nothing.
- **Evidence:** Enforced by `ABLATE_PATHS` in `scripts/task-lift.js` and pinned by
  a test.
- **Reverses if:** The three-arm design (adding a no-rules-but-docs arm) shows the
  `docs/` layer carries the same conventions, which would mean this arm
  under-attributes the rules layer specifically.

### DEC-0003 — Measure coverage by mention, and say so in the report (2026-10-01)

- **Area:** harness refactor
- **Decision:** `harness-coverage.js` scores a recorded failure as covered when any
  rule file contains a distinctive term from it, and states in every run that
  mention is a ceiling on coverage and never proof of prevention.
- **Rationale:** The alternative was a hand-curated map of failure to rule, which
  is accurate but is also unfalsifiable, goes stale silently, and cannot be
  re-run. Mention is deterministic, runs free, and over-reports rather than
  under-reports — the safe direction for a gap-finder.
- **Evidence:** 48 of 54 extractable failures covered; the 6 uncovered are listed
  as candidates for human read in `docs/qa/HARNESS_COVERAGE.md`.
- **Reverses if:** Human review finds the candidate list mostly false positives, in
  which case the term extractor needs narrowing before the number means anything.

### DEC-0004 — Product evidence is recorded separately from product acceptance (2026-10-01)
- **Area:** code design
- **Decision:** `scripts/t0-evidence.js` reports what each local prove artifact
  claims and hard-codes `accepted: false`. Acceptance is never inferred from a file.
- **Rationale:** The alternative was letting the ledger read the artifact's `pass`
  field as a verdict. Three artifacts self-report a pass and five self-report
  `provisional`, so the board's "MERGED / NOT PROVEN" and the artifacts' "pass"
  were both true and the contradiction was invisible. Acceptance is a **Test**
  job and stays human; conflating the two would have quietly deleted that stamp.
- **Evidence:** `docs/qa/T0_BEAT_EVIDENCE.md` — 0 of 14 accepted, 3 local passes,
  5 provisional, 6 with no verdict field.
- **Reverses if:** Never on the `accepted` field — that is a human Test stamp by
  decision. It may be revisited only if acceptance becomes machine-checkable.

### DEC-0005 — Harness and T0 run in parallel; the "harness only" horizon is superseded (2026-10-01)

- **Area:** architecture
- **Decision:** Treat the harness track and the T0 prototype track as two
  concurrent tracks. Drop the "horizon = harness only" note as a **bar on product
  work**; it remains accurate only as a description of the harness track's scope.
- **Rationale:** The board contradicted itself — L3 declared a Lead lock of
  "horizon = harness only" while listing T0 as the live product track stamped
  `APPROVE-PROTOTYPE-LIST` the same day. Two readings were available: the lock was
  superseded by the later T0 stamp, or the two tracks run in parallel. They differ
  only in whether the harness track needed permission to exist. The alternative
  reading — keep waiting for a Lead ruling — was rejected because it left a
  **harness** question parked on a human, which is precisely the class this project
  moved to the agent on 2026-10-01.
- **Evidence:** `swarm/PHASE_BOARD.md` L3 and L168; `APPROVE-PROTOTYPE-LIST`
  2026-09-27. `HR4_A_SKILL_EVAL.md` and `HR4_B_MDC_SCORE_AND_GATES.md` (both
  2026-09-30) restate "harness only"; read as scope, not as a bar.
- **Reverses if:** The Lead states a product-horizon lock again. It would then be a
  **product** decision, so it is stamped, not logged here.
- **Does not touch:** `T0-gaps-vs-inventories-stamp` (game mechanic canon) and
  `T0-prove-results` (Test: beat acceptance) stay human. This decision moved a
  harness question, not a product one.