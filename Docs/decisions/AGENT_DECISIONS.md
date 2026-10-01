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

### DEC-0006 — `void` is the absence of a state, not a fourth state (2026-10-01)

- **Area:** code design
- **Decision:** Adopt one shared outcome vocabulary in `scripts/outcome.js`: `pass`,
  `soft_fail`, `closed_fail` for a subject that was actually measured, plus `void`
  for one that was not. `void` is excluded from the denominator, never scored 0.
- **Rationale:** Three tools had grown their own outcome words and a reader would
  reasonably assume they matched. They did not, and the mismatch had teeth: the void
  pilot reported eight runs that produced nothing as a conformance delta, because
  the only honest-sounding option was to call them failures. The alternative was to
  keep `pass`/`fail` and rely on prose warnings. Rejected — the warning would be in
  the report nobody reads, while the number would be in the report somebody quotes.
- **Evidence:** `scripts/outcome.js`; the `verdictFor` ordering rule is pinned by a
  test asserting an absent subject is `void` even when `pass: true`.
- **Reverses if:** Never by convenience. If `void` is ever mapped to `closed_fail`,
  the pilot bug returns.

### DEC-0007 — Verify the ablation, and ship a positive control (2026-10-01)

- **Area:** code design
- **Decision:** `buildWorktree` refuses to measure an arm whose harness surfaces
  survived the delete, and every task carries a `control` fixture that must score
  100% (`npm run tasklift:control`).
- **Rationale:** The alternative was to trust the ablation and read the number. Two
  silent failure modes sat behind that trust. If a delete half-fails, the "without
  harness" arm is a "with harness" arm in disguise, the arms agree, and the finding
  is "no effect" — biased toward the comfortable answer. If a check's pattern can
  never be satisfied, the eval reports a permanent shortfall that reads as "the
  harness does not help". Both produce a confident wrong number, which is the exact
  failure this instrument exists to avoid.
- **Evidence:** `verifyAblation`; `scoreControl`; the four control fixtures reach
  100% (8/8, 9/9, 6/6, 5/5). A test builds a throwaway tree with a surviving surface
  and asserts the check fails.
- **Reverses if:** Never. These only ever report a problem; they cannot manufacture a
  result.

### DEC-0008 — Tombstones exempt from the scope requirement, by `description:` only (2026-10-01)

- **Area:** code design
- **Decision:** The `globs:` conformance check becomes `declaresScope`: a live rule
  must declare globs, a rule whose `description:` self-declares as retired or
  quarantined is exempt (scored `soft_fail`, not a clean pass).
- **Rationale:** I first proposed *loosening* this check, on the grounds that 3 of 31
  rules lack `globs:` so a faithful copy of those would fail. Checking before acting
  showed all three are deliberate tombstones — `07-ai-agent-behavior` and
  `08-project-context` are `RETIRED P4`, `19-automation-cycle` is `QUARANTINE WAVE F`,
  all with `alwaysApply: false`. Loosening would have hidden three dead rules behind a
  passing check. Every live rule has `alwaysApply: false`, so `globs:` is the only
  trigger a new rule has; the check is correct and the exceptions are intentional.
- **Evidence:** `.cursor/rules/*.mdc` frontmatter — 31/31 `alwaysApply: false`,
  28/31 with `globs:`; the three without are the tombstones. Discriminate on
  `description:`, never body text, matching the rule `harness-coverage.js` already
  uses.
- **Reverses if:** A tombstone is ever revived, its `description:` stops declaring
  retirement and the check applies to it again. That is the intended behaviour.

### DEC-0009 — An unlogged boundary change fails; the DEC entry must be in the same commit (2026-10-01)

- **Area:** harness refactor
- **Decision:** `npm run decisions:check` exits non-zero when a commit touching a
  boundary surface ships without adding a `DEC-NNNN` entry **in that same commit**.
- **Rationale:** The 2026-10-01 reset made the written record the only evidence that
  an agent-owned decision was ever made, and a record nothing checks is a suggestion.
  The first version accepted an entry from any *later* commit and was rejected on
  inspection: one entry appended at the end of a branch excuses every unlogged change
  before it, which is decorative rather than enforcing. Scope is deliberately narrow —
  it checks that the reasoning was written down, not that it was good. Judging
  reasoning is a human taste call; recording it is mechanical.
- **Evidence:** `scripts/decision-log.js`; tests build a throwaway git repo and assert
  both the violation and the same-commit clearance, including that a later entry does
  **not** cover an earlier commit. Run against this repo's own history it flags three
  pre-rule commits, including my own `e937c9a`.
- **Reverses if:** The same-commit rule proves impractical in practice. Then amend or
  squash — do not weaken the check, or it stops catching the thing it exists for.
- **Baseline:** the rule applies from this commit forward. Commits made before it are
  backfilled here, not re-litigated.