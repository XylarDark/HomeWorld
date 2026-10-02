# Task-level eval — does the harness change the output?

> **Generated file.** Regenerate with `npm run tasklift:write`.

## Read this before quoting the number

**This is a pilot, not evidence.** 4 tasks x 2 conditions x 1 trial. That has almost no statistical power. It proves the instrument works, and it is worth acting on the *per-check* failures, which are unambiguous. Do not quote the lift delta as a harness effect.

Completion is the control. If the harness arm does not complete tasks at least as often, the conformance delta means nothing.

## Ablation check

The two arms must genuinely differ. If a harness file survived the delete, the "without" arm would be a "with" arm in disguise and the whole comparison would be void — silently, and in the direction that finds no effect. This is verified, not assumed.

- **without** — **INCOMPLETE: still present — **
- **without** — undefined files remain in the ablated tree
- **with** — 0 of 6 harness surfaces present (expected: non-zero)

| Arm | Harness surfaces present (of checked) | Files in tree |
|---|---|---|
| `with` | 0 of 0 | 4268 |
| `docs-only` | 0 of 3 | 4176 |
| `without` | 0 of 6 | 4147 |

| Arm | Conformance | Completion | Runs |
|---|---|---|---|
| `with` | 31% | 83% | 6 |
| `docs-only` | 56% | 100% | 3 |
| `without` | 67% | 100% | 6 |

## Result

| Measure | With harness | Without | Delta |
|---|---|---|---|
| Task completion (control) | 83% | 100% | -17pp |
| Convention conformance | 31% | 67% | -36pp |
| **Lift on conformance** | — | — | **-36pp** |

Agent sessions: 20 run, 20 measured, 0 void, 0 retried after a transport failure.

Paired McNemar over 92 conformance checks: 7 where only the harness arm passed, 39 where only the ablated arm passed (p = <0.001). Significant at 5%.

## Per-task detail

### art-master-spec

- with: completion 100%, conformance 67%
- without: completion 100%, conformance 100%

| Check | Class | With | Without |
|---|---|---|---|
| names the master material it uses | completion | pass | pass |
| reuses an existing master instead of inventing a family | conformance | pass | pass |
| declares BaseColor | conformance | pass | pass |
| declares Roughness | conformance | pass | pass |
| declares Variation | conformance | pass | pass |
| declares NightMix | conformance | pass | pass |
| NightMix is expressed as a 0 to 1 range | conformance | **FAIL** | pass |
| states the origin convention | conformance | **FAIL** | pass |
| states the unit is meters | conformance | **FAIL** | pass |
| avoids the canon's rejected look language (quoting a rejection is not using it) | conformance | pass | pass |

### art-shot-brief

- with: completion 100%, conformance 20%
- without: completion 100%, conformance 100%

| Check | Class | With | Without |
|---|---|---|---|
| names the subject | completion | pass | pass |
| states explicit pass criteria | conformance | **FAIL** | pass |
| states explicit fail criteria | conformance | pass | pass |
| names the locked palette chip the shrine uses | conformance | **FAIL** | pass |
| pairs the shrine light against the cabin key | conformance | **FAIL** | pass |
| reuses the existing masters rather than rebuilding for night | conformance | **FAIL** | pass |

### asset-naming

- with: completion 0%, conformance 33%
- without: completion 100%, conformance 67%

| Check | Class | With | Without |
|---|---|---|---|
| produced prefixed names | completion | **FAIL** | pass |
| every name uses an approved prefix and no spaces | conformance | **FAIL** | pass |
| does not invent a prefix outside the contract | conformance | pass | pass |
| uses a contract suffix where one applies | conformance | **FAIL** | **FAIL** |

### mechanic-beat-packet

- with: completion 0%, conformance 0%
- without: completion 100%, conformance 100%

| Check | Class | With | Without |
|---|---|---|---|
| identifies the beat | completion | **FAIL** | pass |
| carries the Bite id field | conformance | **FAIL** | pass |
| carries the Present? field | conformance | **FAIL** | pass |
| carries the CAP field | conformance | **FAIL** | pass |
| carries the Packet class field | conformance | **FAIL** | pass |
| states DONE-WHEN | conformance | **FAIL** | pass |
| carries the Anti row | conformance | **FAIL** | pass |
| carries the A-E trade-off section | conformance | **FAIL** | pass |
| uses the three-state verdict vocabulary | conformance | **FAIL** | pass |
| does not mark itself approved - design does not self-approve | conformance | **FAIL** | pass |

## Run identity

- commit: `6ac687d`
- task manifest: `scripts/task-lift/tasks-taste.json`
- model: `opencode/nemotron-3.5-lightning-free`
- dropped pairs (one arm had no valid run, so it cannot be compared): asset-naming
- agent binary: `C:\Users\User\AppData\Roaming\npm\node_modules\@opencode\cli\bin\opencode.exe` (opencode v2.0.18)
- driver: `opencode run --standalone --auto` (fresh process, no parent session context)
- ablation: git worktree at the same commit with AGENTS.md, .cursor, .agents, swarm, UserHarness, START_HERE.md deleted
- agent timeouts: 0, agent errors: 0

_The raw per-check results are in `docs/qa/TASK_LIFT.json`._
