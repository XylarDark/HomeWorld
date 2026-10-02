# Task-level eval — does the harness change the output?

> **Generated file.** Regenerate with `npm run tasklift:write`.

## Read this before quoting the number

**This is a pilot, not evidence.** 4 tasks x 2 conditions x 1 trial. That has almost no statistical power. It proves the instrument works, and it is worth acting on the *per-check* failures, which are unambiguous. Do not quote the lift delta as a harness effect.

Completion is the control. If the harness arm does not complete tasks at least as often, the conformance delta means nothing.

| Arm | Conformance | Completion | Runs |
|---|---|---|---|
| `with` | 75% | 100% | 8 |
| `docs-only` | 75% | 100% | 8 |
| `without` | 65% | 100% | 8 |

## Result

| Measure | With harness | Without | Delta |
|---|---|---|---|
| Task completion (control) | 100% | 100% | 0pp |
| Convention conformance | 75% | 65% | +10pp |
| **Lift on conformance** | — | — | **+10pp** |

Agent sessions: 24 run, 24 measured, 0 void, 3 retried after a transport failure.

Paired McNemar over 104 conformance checks: 18 where only the harness arm passed, 10 where only the ablated arm passed (p = 0.185). **Not significant — at this sample size, treat any delta above as noise.**

## Per-task detail

### art-master-spec

- with: completion 100%, conformance 100%
- without: completion 100%, conformance 100%

| Check | Class | With | Without |
|---|---|---|---|
| names the master material it uses | completion | pass | pass |
| reuses an existing master instead of inventing a family | conformance | pass | pass |
| declares BaseColor | conformance | pass | pass |
| declares Roughness | conformance | pass | pass |
| declares Variation | conformance | pass | pass |
| declares NightMix | conformance | pass | pass |
| NightMix is expressed as a 0 to 1 range | conformance | pass | pass |
| states the origin convention | conformance | pass | pass |
| states the unit is meters | conformance | pass | pass |
| avoids the canon's rejected look language (quoting a rejection is not using it) | conformance | pass | pass |

### art-shot-brief

- with: completion 100%, conformance 100%
- without: completion 100%, conformance 20%

| Check | Class | With | Without |
|---|---|---|---|
| names the subject | completion | pass | pass |
| states explicit pass criteria | conformance | pass | **FAIL** |
| states explicit fail criteria | conformance | pass | **FAIL** |
| names the locked palette chip the shrine uses | conformance | pass | **FAIL** |
| pairs the shrine light against the cabin key | conformance | pass | **FAIL** |
| reuses the existing masters rather than rebuilding for night | conformance | pass | pass |

### asset-naming

- with: completion 100%, conformance 100%
- without: completion 100%, conformance 100%

| Check | Class | With | Without |
|---|---|---|---|
| produced prefixed names | completion | pass | pass |
| every name uses an approved prefix and no spaces | conformance | pass | pass |
| does not invent a prefix outside the contract | conformance | pass | pass |
| uses a contract suffix where one applies | conformance | pass | pass |

### mechanic-beat-packet

- with: completion 100%, conformance 100%
- without: completion 100%, conformance 100%

| Check | Class | With | Without |
|---|---|---|---|
| identifies the beat | completion | pass | pass |
| carries the Bite id field | conformance | pass | pass |
| carries the Present? field | conformance | pass | pass |
| carries the CAP field | conformance | pass | pass |
| carries the Packet class field | conformance | pass | pass |
| states DONE-WHEN | conformance | pass | pass |
| carries the Anti row | conformance | pass | pass |
| carries the A-E trade-off section | conformance | pass | pass |
| uses the three-state verdict vocabulary | conformance | pass | pass |
| does not mark itself approved - design does not self-approve | conformance | pass | pass |

## Run identity

- commit: `a7cca23`
- task manifest: `scripts/task-lift/tasks-taste.json`
- model: `opencode/space-bunny-free`
- agent binary: `C:\Users\User\AppData\Roaming\npm\node_modules\@opencode\cli\bin\opencode.exe` (opencode v2.0.18)
- driver: `opencode run --standalone --auto` (fresh process, no parent session context)
- ablation: git worktree at the same commit with AGENTS.md, .cursor, .agents, swarm, UserHarness, START_HERE.md deleted
- agent timeouts: 0, agent errors: 0

_The raw per-check results are in `docs/qa/TASK_LIFT.json`._
