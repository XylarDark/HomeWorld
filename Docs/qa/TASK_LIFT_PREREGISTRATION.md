# Task-lift preregistration

**Written before any taste-beat data exists.** 2026-10-01. The whole point of this
file is that it was written *before* the numbers, so the decision rule cannot be
fitted to whatever comes back.

## What is being claimed

The harness layer (`AGENTS.md`, `.cursor/`, `.agents/`, `swarm/`, `UserHarness`,
`START_HERE.md`) changes what the agent produces on **art design and game mechanic
work** — the two domains the human owns outright.

## What is NOT being claimed

- **Not** that the harness improves general capability.
- **Not** that the harness improves code, architecture, or harness refactoring.
  Those moved to agent-owned on 2026-10-01 and are out of scope here.
- **Not** that a null result means the harness is useless. Four tasks cannot
  establish absence of effect. A null means *this benchmark did not detect one*.

## The hard limit of this experiment — read before quoting anything

Two limits are structural and no amount of repetition fixes them.

**1. The canon is reachable from both arms.** `ABLATE_PATHS` removes the harness
but **not** `Docs/`. `Docs/02_ART_BIBLE.md` and the T0 beat packets are on disk in
the ablated worktree too. So this measures whether the harness **points an agent at**
the recorded canon, not whether the canon was available. Those are different
questions and this experiment only answers the first.

**2. Four tasks × one trial has close to zero statistical power.** The realistic
goal is to detect a *large* effect and to produce an unambiguous list of per-check
failures. It is not capable of measuring a small one, and no result from it should
be described as a harness effect size.

## Decision rule — fixed in advance

Let `d` = (conformance with harness) − (conformance without), computed over
**paired tasks only** (a task counts only when both arms produced a valid run).
Let `b` = the same difference on **completion**, the control.

| Condition | Verdict |
|---|---|
| `b` < 0 | **INVALID.** The harness arm completed the task less often. The conformance delta means nothing. Report and stop. |
| `d` ≥ 0.25 **and** `b` ≥ 0 | **Large effect detected.** Act on the per-check failures. |
| 0 ≤ `d` < 0.25 | **Inconclusive.** Do not quote a number in either direction. |
| `d` < 0 | **Harness arm scored worse.** Treat as a defect to investigate, not as a finding to celebrate. |

Pre-committing to `d ≥ 0.25` matters: choosing the threshold after seeing the data
is the cheapest way to manufacture a result, because any non-null number can be
called "large" if you are allowed to define large afterwards.

**On a null:** the honest output is "this benchmark did not detect an effect", not
"the harness does not help". The second sentence is a claim the experiment cannot
support, and writing it is how a smoke test gets quoted as evidence.

## The control set is not the benchmark

`scripts/task-lift/tasks.json` (chores: known-errors entry, UE 5.8 rule,
PowerShell helper, commit message) is a **sanity set**. Both arms already do those
jobs, so it measures whether the instrument still works — nothing more. It is at
ceiling by construction.

`scripts/task-lift/tasks-taste.json` (art master spec, shot brief, asset naming,
T0 beat packet) is the **benchmark**. Each is drawn from the locked canon, where
knowing the recorded decision is the difference between a right and a wrong
artifact.

Run the sanity set if you want to know the instrument is sound. Quote the taste set
if you want to know anything about the harness.

## Before any run

- [ ] `npm run tasklift:control` — sanity controls at 100%
- [ ] `node scripts/task-lift-control.js --manifest scripts/task-lift/tasks-taste.json` — taste controls at 100%
- [ ] `npm run tasklift:test` — green
- [ ] Provider healthy. A 402 or 429 voids runs; it is not a finding.
- [ ] Record the commit. Results only compare within one commit.

## The run itself

```
npm run tasklift:run:taste
```

`--run` is required. The runner refuses to spend agent sessions without it, because
the previous default was to run them — asking for a report cost eight sessions.

Budget note: 4 tasks × 2 conditions = 8 agent sessions per trial. The recommended
first honest run is `--trials 2` (16 sessions) once the provider is healthy.

---

# Results log (appended after data — do not edit the decision rule above)

## Run 1 — 2026-10-01, all 4 taste tasks, `opencode/space-bunny-free`, 1 trial, 8 sessions

**7 measured, 1 void** (`mechanic-beat-packet` / `without` — the session aborted with
`Session interrupted: shutdown`). Paired tasks: **3**; dropped: `mechanic-beat-packet`.

| Measure | With | Without | Delta |
|---|---|---|---|
| Task completion (control) | 100% | 100% | 0pp |
| Convention conformance | 88.9% | 96.3% | **−7.4pp** |

**Verdict against the rule fixed above:** `b = 0` (so not INVALID), `d = −0.074`, which
lands in **"Harness arm scored worse — treat as a defect to investigate, not as a
finding to celebrate."**

**What that does and does not mean.** It does **not** mean the harness is harmful.
n = 3 paired tasks at 1 trial, and the delta is driven by **three individual checks**:

- `art-master-spec` — **without** failed *"avoids the rejected look language"*: the
  ablated arm used photoreal / scan language where the harness arm did not. This is
  the one failure that points the harness's way, and it is the only check on that task
  that separates the arms.
- `art-shot-brief` — **with** failed *"pairs the shrine light against the cabin key"*
  and *"the shrine is a handmade spirit cue, not a tech gate"*. Both require a
  specific recorded term or a banned-term absence.
- The dropped task's 10 failures are all `void` — the agent never wrote the file.

**The most likely explanation is still the check, not the harness.** The two
`art-shot-brief` checks are the same shape as the two flaws already found and fixed
in this instrument: `pairs the shrine light against the cabin key` requires the
literal phrase `Cabin amber`, so an answer that says "the cabin's warm window light"
fails on wording while knowing the canon perfectly. `handmade spirit cue, not a tech
gate` is a banned-term check that can still be tripped by a *correct* answer that names
the neon portal while rejecting it — the `unless` negation guard was added to the
**material** check but not to the **shot** check.

**Therefore the next step is auditing the remaining taste checks for phrasing
sensitivity, not drawing a conclusion about the harness.** Two prior instances of this
exact defect were each found only by running the thing.

**Control outcome:** completion was identical at 100% in both arms, so the conformance
delta is not explained by the harness arm doing less work — which is what the control
exists to rule out, and it did its job.

**Still unrun:** `--trials 2`, the `docs-only` third arm, and any significance test.
The benchmark has one trial per cell and no power.
