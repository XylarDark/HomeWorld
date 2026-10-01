# HR4-B — Closing the `.mdc` measurement gap, and hardening two gates

| Field | Value |
|-------|-------|
| **Date** | 2026-09-30 |
| **Phase** | HR4-B · harness/bot (Lead lock 2026-09-27: horizon = harness only) |
| **Follows** | [HR4_A_SKILL_EVAL.md](HR4_A_SKILL_EVAL.md) |
| **Scope** | Make the 31 `.cursor/rules/*.mdc` measurable with the *real* scorer; close two unverified gates. No product or engine change. |

---

## Finding 1 — the `.mdc` corpus is now measurable (was a hard FAIL)

HR4-A left this open:

```
$ skillevaluator quality-check .cursor/rules
QUALITY | FAIL | 1 errors
```

An Agent Skill is a directory with a `SKILL.md`; a Cursor rule is a `.mdc`
file. Rather than re-implement the rubric — which would produce numbers that
*look* comparable but are not the same measurement — `scripts/score-mdc-rules.js`
materializes each rule into a throwaway Agent Skill under a temp dir and lets
the **actual `skillevaluator` binary** score it. The repo is never modified.

```
npm run rules:score            # human table
npm run rules:score:test       # 18 unit tests, no scorer required
npm run rules:score -- --json Saved/rules_score.json --strict
```

### Result — 31/31 scored, 0 unscored

Scores below are **SkillEvaluator 0.4.0**, recorded in the report as
`scorerVersion` + `rubricComparable` so any future run can tell whether its
numbers are comparable.

| Metric | Value |
|---|---|
| Mean | **87.4** (range 79.5–91.5) |
| Grade A | 4 (`09b-mcp-utility-scripts` 91.5, `11-parallel-plugin` 91.5, `00-core-principles` 91.0, `15-shell-scripts` 90.2) |
| Below 80 needing work | **0** |
| Below 80 as tombstone | 1 — `19-automation-cycle.mdc` (79.5, C, `QUARANTINE`) |
| Mean + declared format offset | ~90.9 |
| Version delta vs 0.3.0 | 87.3 → **87.4** (rubric effectively unchanged for this corpus) |

**The single sub-80 rule is the WAVE F tombstone** — 12 lines that exist
precisely to be short and redirect to `swarm/SWARM_OPS.md`. The scorer flags it
for *"very little content (15 lines)"*. That is a **false signal for the
tombstone class**: a well-formed tombstone is short on purpose, and no
structural gate can tell that apart from under-writing. This is the same
correctness gap as ρ = 0.14 in arXiv 2608.20614, observed directly in our own
corpus.

### Tombstones are now classified, not just penalized

The scorer discriminates on an **explicit self-declaration**: the `description:`
must *start* with `QUARANTINE|HISTORICAL|RETIRED|DEPRECATED|ARCHIVED|NO
LONGER`. That yields exactly five rules — `07-ai-agent-behavior` (RETIRED P4),
`08-project-context` (RETIRED P4), `19-automation-cycle` (QUARANTINE),
`ue57-editor-ui` and `ue57-sources` (HISTORICAL) — with **zero** false
positives.

Matching on *body* text instead would have been useless: **14 of 31 rules**
mention "deprecated"/"removed" somewhere, almost always describing a UE API or a
deleted tool (`unreal-cpp.mdc` on deprecated UE APIs, `19-automation-gaps.mdc`
on removed scripts). Those five are locked down by a test that asserts they stay
substantive.

Exempting never hides a number. Tombstone scores stay in every report and in the
table; they are only excluded from "needs work" and from `--strict`, which now
**passes** at 0 actionable rules below threshold.

### Declared adaptations (in the JSON report, not buried in prose)

| Adaptation | Effect |
|---|---|
| `name` slugified to satisfy `^[a-z0-9-]+$` | rule titles are not scored |
| `version` passed through from `.mdc` | so the SKILL_SPEC check measures the rule, not the adapter |
| `alwaysApply` / `globs` have no SKILL.md equivalent | **not scored** |
| `metadata.author` / `metadata.tags` have no `.mdc` equivalent | **constant 3.5-point composite offset**, reported as `formatOffsetComposite` |

Scores are **lower bounds**. The offset is declared rather than removed because
inventing an author or tags list would fabricate provenance.

### A bug in the adapter, caught and fixed

The first implementation dropped `version` from the materialized frontmatter.
SkillEvaluator deducts 5 correctness points when it is missing — so the adapter
was manufacturing a finding **against all 31 rules**. Effect: mean read 85.6
instead of 87.3, and **two** rules looked below threshold instead of one.
`unreal-gas.mdc` moved 79.0 → 80.8 once fixed, matching the predicted ~1.75
composite points. Recorded in
[KNOWN_ERRORS.md](../../docs/KNOWN_ERRORS.md) § Harness traps.

### Two more harness bugs the tests caught, both mine

1. **Scorer substitution.** `resolveTool` fell through from an explicit
   `--tool` to a bare PATH lookup, so requesting scorer X could silently run
   scorer Y while the report named X — one rubric's numbers attributed to
   another. An explicit `--tool` is now authoritative and is never substituted.
2. **A refusal became a crash.** `toolVersion(tool)` was called *before* the
   not-found guard, so a missing scorer produced an `ERR_INVALID_ARG_TYPE` stack
   trace and `exit 1` instead of the intended clean `exit 2`. Caught by the
   pre-existing fail-loud test. A refusal must be a message, never a trace.

### The version anchor exists because the version moved

Installing the Tier 3 extra silently took SkillEvaluator **0.3.0 → 0.4.0**. The
mean moved only 87.3 → 87.4, but adding one missing frontmatter `name:` moved
`16-feature-debug-instrumentation.mdc` **85.5 → 89.8** — scores drift with the
rubric *and* with the input. Every report therefore records `scorerVersion` and
`rubricComparable`; a run that cannot read the version sets
`rubricComparable: false` rather than emitting numbers that merely look
comparable.

### Real defect found and fixed

`16-feature-debug-instrumentation.mdc` was missing `name:`, `priority:` and
`version:` — the only rule of 31 without them, so it was unaddressable by name.
Added. Verified `priority` is decorative (nothing reads it; values mirror the
filename number), so adding it changes no load order. The `name:` alone was
worth **+4.3** to that rule's score.

## Finding 2 — the submodule gate verified a SHA but never the URL

`scripts/verify-userharness-submodule.sh` proved the gitlink SHA matched the
registry. It never compared the `.gitmodules` **URL text**. That is precisely
the rename-redirect trap: a renamed GitHub repo still clones successfully via
redirect, so a stale URL fails *silently* while the registry asserts the new
name. The three-name rule in `NAMING_CONTRACT.md` (repo URL / path /
productName) was unenforced at CI.

Now asserted: submodule URL, submodule path, and the `PIN_SYNC_POLICY` rule
that the registry may not document `main` while the gitlink is expected on
`master`. Cosmetic `.git`/trailing-slash differences are normalized so a real
rename still fails loudly.

**Mutation-tested, not just passing.** Three deliberate breakages, each
required to exit non-zero — and each did:

| Injected fault | Result |
|---|---|
| `.gitmodules` URL reverted to the pre-rename `DevEnvTemplate` | `exit 1`, "Submodule URL mismatch" |
| `.gitmodules` path renamed | `exit 1`, "Submodule path mismatch" |
| registry `branch` set to `main` | `exit 1`, cites `PIN_SYNC_POLICY` |

Real repo exits 0. Both mutated files restored byte-identical afterwards. CI is
unchanged — `.github/workflows/` was not touched.

## Finding 3 — machine-absolute paths in a tracked config

`.opencode/opencode.json` granted permissions on
`C:/dev/HomeWorld/.opencode/gsd-core/*`, written by the GSD installer on this
machine. Cloned anywhere else the grant matches nothing.

Replaced with `*/.opencode/gsd-core/*` (plus a native-backslash variant),
verified against 10 cases under the semantics OpenCode documents — `*` is
zero-or-more of any character, all other characters literal — including four
negatives that must **not** match (`gsd-core-extras/`, `gsd-coreX/`,
`.opencode/other/`, `Content/Python/`). No machine-absolute path remains in the
tracked config.

Two honest caveats: `read` already defaults to `allow` and `gsd-core/` lives
*inside* the workspace, so `external_directory` should never fire for it — both
entries are close to vestigial. I kept them rather than deleting, because
deleting changes behavior in the one case I cannot rule out (OpenCode started
from a directory *above* the project). Making them portable cannot be worse than
what shipped.

## Skill Lift — corrected characterization

HR4-A recorded Tier 3 as requiring Docker. **That was an over-generalization
from a single `health-check` line.** The Tier 3 extra installed cleanly and
`harbor==0.13.2` imports fine; the `harbor CLI not found` message was only a
`PATH` problem, since `uv tool install` puts `harbor.exe` in
`…\uv\tools\skillevaluator\Scripts\` without linking it. With `PATH` corrected,
`docker prerequisite` reports its actual reason: *"Docker Compose v2 is required
for Tier 3 — Docker mode: [WinError 2]"*.

Crucially, `harbor` ships **many** environment backends, not just Docker:
`docker/`, `modal`, `e2b`, `runloop`, `daytona`, `gke`, `singularity`,
`novita`, `wandb`, `langsmith`, `cwsandbox`, `islo`, `tensorlake`,
`apple_container`, `use_computer`, `tar_transfer`. Docker is only the **default
local** backend.

| Tier | Blocked on | Docker needed? |
|---|---|---|
| **1** static | nothing — **works** | no |
| **2** dedup / inter-skill similarity | **a paid LLM provider key only** | **no** |
| **3** live agent eval | **a key + *some* environment backend** | only if you choose the Docker backend |

So the real blocker for Tier 2 is a single credential, not a hypervisor. Tier 3
is reachable without Docker at all, via any of the cloud sandbox backends —
each of which needs its own account.

`skillevaluator health-check` at the time of writing confirmed there was **no
provider configured**: no `SKILL_EVAL_LLM_PROVIDER`, and no `NVIDIA_API_KEY` /
`OPENAI_API_KEY` / `ANTHROPIC_API_KEY` in the environment, so no LLM-judged
number could be produced. **That was a Lead action — a credential, not an
engineering task — and it has since been supplied.** `health-check` now reads
`Public LLM provider | pass | nv_build / nvidia/nemotron-3-super-120b-a12b`, and
the judged measurement follows under *Skill Lift — MEASURED* below. This
paragraph is kept only as the historical state that blocked it; it no longer
describes the tree.

## Two prior open items closed by measurement

**`UserHarness/docs/BEST-PRACTICES.md` — no action justified.** The retire/split
question assumed 25 KB of context bloat. Measured, it is 1016 lines / 25,576 B
/ 112 headings / 106 code fences — a dense reference, not filler. But a grep of
**535 live files** (`.agents/`, `.cursor/`, `docs/`, `AGENTS.md`) finds **zero**
path references, and `npm run sync` (dry run) reports *"No files were
modified"* — it belongs to neither live layer. It is never copied into agent
context, so it costs **zero** context budget. Retiring or splitting it would be
pure churn inside a submodule that also carries uncommitted work. **Premise
overturned by measurement; left untouched.**

**`scope-refinement` duplicate — removed (human authorised).** Both
`.cursor/skills/scope-refinement/SKILL.md` and
`.agents/skills-extras/scope-refinement/SKILL.md` were 1960 B,
SHA-256 `A8F965840527C1C9…`, each directory containing only that one file.
Resolution required deciding *which catalog is canonical*, not merely which file
is redundant — and the answer was not the one the file layout suggests:

- `UserHarness/.agents/README.md` lists `scope-refinement` among the **extras**,
  and `UserHarness/docs/human-use/README.md` calls it an **"opt-in skill"**.
- `.cursor/skills/README.md` enumerates exactly three live skills
  (`pcg-validate`, `ue58-api-check`, `automation-gap-solutions`) plus the
  `ue57-api-check` tombstone, and has a *"Not here (by design)"* section for
  skills deliberately kept off the scan path. `scope-refinement` appears in
  **neither** list.

So the canonical home is `.agents/skills-extras/scope-refinement/`, and the
`.cursor/skills/` copy was an unlisted duplicate sitting on a **Cursor scan
path** — where every `SKILL.md` `description` is read on every turn. Removing it
frees scan budget and matches the documented set. The removal is **lossless**:
the kept copy is byte-identical (verified by hash before and after), so there is
no orphaned content to recover.

**Observed consequence (not inferred):** the harness immediately reported
`scope-refinement` as *no longer available*. That is the honest edge of the
decision — `.cursor/skills/` was the only scan path surfacing it, so the skill is
now genuinely **opt-in** rather than auto-discoverable. That is the documented
intent, but it is a behaviour change, not a no-op: to make it discoverable again,
copy it onto a live scan path (`.agents/skills/`), **not** back to
`.cursor/skills/`:

```powershell
# opt back in on a LIVE scan path (not back to .cursor/skills/)
Copy-Item -Recurse .agents\skills-extras\scope-refinement .agents\skills\
```

## Tier 2 — semantic similarity, measured

Tier 2 was recorded as blocked on **"a paid LLM provider key only"**. With the
key present it runs — but **not the way the plan assumed**, and the difference is
the same schema mismatch as Tier 1.

**`--type rules` cannot see this corpus at all.** `similarity-check
.cursor/rules --type rules` exits 1 with `No rules content found to compare` and
`files_scanned: 0`, because its discovery reads the rule's name from a **`title`**
frontmatter field — and **0 of 31** rules have one. Cursor writes `name:`, so the
scanner finds nothing. This is not a broken tree or an empty folder; it is the
tool's "rules" support not matching Cursor's rule schema. The plan recorded Tier
2 as *"needs no materialization"*: **that was wrong.** The corpus must be
materialized into Agent Skills first — the skill discovery path reads `name:`,
which our rules do have.

```
# 1. materialize .cursor/rules/*.mdc -> <dir>/<slug>/SKILL.md  (shared materializer)
# 2. then, and only then:
skillevaluator similarity-check <materialized-dir> --type skill `
  --save-catalog Saved/rules_catalog.json -r cli
```

**Result:** `Similarity Check | PASS`, **31 entries indexed**, catalog saved to
`Saved/rules_catalog.json` (1,383,401 B; gitignored, machine-local). Exactly
**one** pair exceeds the default 0.75 threshold:

| pair | score |
|---|---|
| `ue57-sources.mdc` ⇄ `ue57-editor-ui.mdc` | **0.792** |

Both are the **UE 5.7 HISTORICAL tombstones** that point at their 5.8
replacements, so a near-identical pair is the expected state, not a defect — and
both are already classified as tombstones by the structural scorer. No live rule
duplicates another. (Descriptions are embedded, not bodies; `--full-body` was not
used.)

## Gates

| Gate | Result |
|---|---|
| `npm run rules:score:test` | **18/18 pass** |
| `npm run rules:score -- --strict` | exit 0 (0 actionable below 80) |
| `npm run lift:score:test` | **48/48 pass** (no key or network required) |
| `npm run lift:score` | exits **2** with no report when no credential is set (fail-loud) |
| `bash scripts/verify-userharness-submodule.sh` | exit 0 |
| `npm run preflight:ue:test` | 5/5 pass |
| `npm run preflight:ue -- --skip-mcp --assets-only` | repo + assets + JSON PASS |
| `npm run sync` (dry run) | no files to modify |
| `.github/workflows/` | **not modified** |

## Still open

- **Tier 3 not run.** Tier 1 (structural + judged) and **Tier 2 (semantic
  similarity, now measured — see the section above)** are both done. Tier 3 (live
  agent eval) remains unrun: it needs an environment backend beyond Docker —
  `health-check` reports `docker prerequisite: fail` while `Harbor agents: pass`,
  and `harbor` ships many non-Docker backends, each needing its own account.
- **Jitter dominates small deltas — quantified.** Pooled within-rule SD is
  **8.13** points (28 df), mean spread 7.22, max 35.5. At 80% power / 95%
  confidence, detecting a change on **one rule** needs ~**114 judged samples per
  side for 3 points**, ~41 for 5, ~16 for 8 — i.e. roughly **29 full-corpus
  passes at `--repeat 4`** to call a 3-point move real. `meanSpread` /
  `pooledWithinSd` / `standardErrorOfMean` are recorded so this stays visible.
- **Two of 31 rules are UNSCORED, and they are the two largest.** The judged mean
  covers 29 rules and is therefore *not* the corpus mean; `09-mcp-workflow.mdc`
  and `20-full-automation-no-manual-steps.mdc` fail deterministically (8/8
  attempts), unlike the 7 rules retries repaired. Bounding or splitting the
  largest rule is the plausible reduction, still unproven — see the Skill Lift
  section.
- **The judged score is a diagnostic, not a regression gate.** Because a single
  rule moves ±8 points between identical runs, no single-rule judged delta under
  ~8 points is evidence of anything. The deterministic structural gate
  (`rules:score --strict`) stays the regression gate; the judge is for triage —
  which criteria are weak, corpus-wide — not for gating an edit.
- **`scope-refinement` duplicate — CLOSED.** The `.cursor/skills/` copy was
  removed on the human's instruction; the canonical extras copy is intact. It is
  now opt-in (no longer auto-discoverable) — see the resolution note above for
  the observed consequence and the opt-in command.

## Skill Lift — MEASURED over 29 of 31 rules (Tier 1 LLM judge)

Unblocked once `SKILL_EVAL_LLM_PROVIDER` + a key were available. Judge:
**`nv_build` / `nvidia/nemotron-3-super-120b-a12b`**, scorer v0.4.0, at
`--repeat 2 --retries 3`.

```
$env:SKILL_EVAL_LLM_PROVIDER="nv_build"
$env:NVIDIA_API_KEY="<key>"
npm run lift:score -- --repeat 2 --retries 3 --json Saved/rules_lift.json
npm run lift:score:test          # 48 tests, no key required
```

| | structural (`quality-check`) | judged (`rubric-eval`) |
|---|---|---|
| rules measured | **31 / 31** | **29 / 31** |
| mean | **87.4** | **62.3** |
| median | — | **67.5** |
| range | — | 22.8 – 78.6 |
| against its own gate | 0 actionable below 80 | **19 / 29 below 70** |
| repeatability | exact (deterministic) | ±**8.1** pts (pooled within-rule SD) |

The corpus clears its structural gate and fails its judged one. Both numbers are
real, and they are not the same measurement
(`comparability.againstQualityCheck: false`).

**Read the corpus mean as 29 rules, not 31.** The two it cannot cover are the
**two largest** rules in the corpus, so the mean is not the corpus mean — see
"Two rules stay UNSCORED" below. The mean (62.3) also sits ~5 points under the
median (67.5): it is a low tail of retired and quarantined tombstones that drags
it down, not a mediocre typical rule.

### The judge is not deterministic — so a single run is not a measurement

The earlier text here rested on one rule scoring **57.7 / 58.6 / 60.5** (~6.4
points). The full corpus shows the jitter is worse: **mean spread 7.22**, **max
spread 35.5**, **pooled within-rule SD 8.13** (28 df). Identical bytes, identical
judge:

| rule | run 1 | run 2 | spread |
|---|---|---|---|
| `19-automation-cycle.mdc` | 5.0 | 40.5 | **35.5** |
| `07-ai-agent-behavior.mdc` | 52.7 | 22.3 | **30.4** |
| `22-unreal-editor-ui.mdc` | 35.9 | 64.5 | **28.6** |
| `08-project-context.mdc` | 53.6 | 40.0 | 13.6 |
| `unreal-cpp.mdc` | 66.8 | 67.3 | 0.5 |

A single-run score — or a sub-8-point delta presented as a regression — is false
precision. `--repeat N` measures the jitter and the report records `meanSpread` /
`maxSpread` / `withinRuleSd` / `standardErrorOfMean` beside the mean — on this
corpus **7.22 / 35.5 / 8.13 / 1.51**, the SD over the 28 rules that had two
samples. (The field is `withinRuleSd`; it is produced by the tool's
`pooledWithinSd()` helper, which was re-called directly on the saved report to
confirm the value.)
`19-automation-cycle.mdc` has been seen as low as **5.0** here and as high as
**60.5** in this harness earlier, so its spread is not a property of one bad run.

This is the reason `score-mdc-lift.js` refuses to run at all without a
credential: with no judge there is no measurement, and a missing measurement
must never be reported as a pass. Exit 2, no report file written. The key is read
from the environment only — the report stores the **variable name and character
count**, never the value, and a test asserts no key-shaped token can appear in
CLI output. The judge model is recorded too (`judge.modelPinned`,
`judge.modelSource`): this run used the provider's default
(`modelSource: health-check`), and `--judge-model NAME` pins it explicitly — a
verdict from a different judge is a different measurement, exactly as a verdict
from a different scorer version is.

### The cache makes a re-measurement nearly free

`scripts/score-mdc-lift.js` keys a content cache on `sha256(materialized
SKILL.md) | judgeModel | scorerVersion` and reuses stored samples up to
`--repeat` before judging anything new. Only *fresh* samples are stored, entries
cap at 8, a corrupt cache is treated as empty, and the flush happens **per rule**
— so a crash keeps whatever already completed instead of losing the run's work.

Measured on a second full pass over the identical corpus:

| | cold pass | cached pass |
|---|---|---|
| rules served from cache | 0 / 31 | **29 / 31** (57 samples) |
| judge calls (`attemptsTotal`) | 88 | **48** |
| rules needing a retry | 7 | **1** |
| mean | 62.32 | **62.32** |

Only `03-testing.mdc` (a missing second sample) and the two UNSCORED rules
needed new judge calls. The mean is **identical**, which is the point — the cache
returns the same measurement, not a new one. The two UNSCORED rules are the
exception *by construction*: they have no samples to cache, so every pass
re-attempts them — and in this second, independent pass they failed again,
**8 attempts each**, with the identical `LLM not configured` warning. That is the
difference between a deterministic miss and a flaky one, observed twice.

### What the corpus is actually weak at

Corpus criterion means (0–10, weakest first):

| criterion | mean /10 | n |
|---|---|---|
| Example Quality | **3.7** | 24 |
| Error Handling Quality | 4.8 | 22 |
| Workflow Completeness | 6.0 | 23 |
| Documentation Completeness | 6.3 | 24 |
| Trigger Simulation | 6.5 | 23 |
| Instruction Clarity | 7.2 | 29 |
| Description Clarity | 7.3 | 29 |
| Scope Definition | 7.5 | 24 |
| Professional Tone | 8.1 | 23 |

The ordering is consistent across rules and reduces to one line: **the corpus
tells agents what to do and how to talk, and is weakest exactly where it would
change behaviour — worked examples, failure modes, and end-to-end workflows.**
`Example Quality` at 3.7/10 is the largest deficit and is the criterion a
structural check cannot see at all. (`n` varies 22–29 because per-criterion
capture depends on the CLI's table shape; the criterion means cover a subset and
are not weighted to the whole corpus.)

### Two rules stay UNSCORED, and it is not flakiness

`09-mcp-workflow.mdc` (7,760 B) and `20-full-automation-no-manual-steps.mdc`
(4,732 B) — **the two largest rules in the corpus** — produced no score in **8
attempts each** (2 samples × 4 attempts) in the saved pass, and were the two
largest of the **6** rules the earlier pass lost (the other 4 recovered on retry —
`docs/KNOWN_ERRORS.md`). That makes these two deterministic, and it is a
different failure from the transient one retries do repair: **7 scored rules**
missed an attempt and then scored normally, while these two never did. (Note
`judge.retriedCount` counts only *scored* rules — 7 — against **9** rules that
actually retried, so it is a flakiness indicator, not a count of everything the
provider touched.)

The judge's own log makes this hard to diagnose, because the wording is
misleading. `inference/client.py` `process()` catches `LLMClientError` **first**
and prints **`LLM not configured - using fallback response`** — the handler at
line 343, the *first branch of a generic failure handler*, not a statement about
configuration. The provider was configured and judged 29 other rules in the same
process. `inference/types.py:15` shows `EmptyLLMResponseError` **subclasses**
`LLMClientError`, so an **empty completion** is reported as a configuration
fault.

That is now **proven**, not inferred. Wrapping
`openai.resources.chat.completions.Completions.create` and re-running the real
`rubric-eval` on `09-mcp-workflow.mdc` printed:

    RESPONSE finish_reason='length' content_len=0
             model='nvidia/nemotron-3-super-120b-a12b' max_tokens=4096
    USAGE    prompt=2587 completion=4096 reasoning=4096
    COMPLETIONS-RAISED EmptyLLMResponseError: LLM returned empty response content
    WARNING  LLM not configured - using fallback response

`RUBRIC_MAX_TOKENS = 4096` (`constants.py:392`) is the `default_max_tokens` of
`RubricEvalValidator` (`rubric_eval.py:194`) and has **no env or CLI override**
(`rubric-eval --help` exposes only `--min-score`, `-r`, `-o`). On this judge —
`nvidia/nemotron-3-super-120b-a12b`, a reasoning model — those 4096 tokens are
**shared between reasoning and content**. On the two largest rules the model
spent all 4096 on reasoning and returned `content=""`, so the judge raised
`EmptyLLMResponseError`, fell back, and printed "not configured".

A size sweep on throwaway copies (bodies truncated to 100 / 50 / 25 % of body
lines, never touching `.cursor/rules/`) shows the effect is **probabilistic, not
a byte cutoff**:

| rule | 100 % | 50 % | 25 % |
|---|---|---|---|
| `09-mcp-workflow.mdc` | UNSCORED | UNSCORED | 57.7 |
| `20-full-automation-no-manual-steps.mdc` | UNSCORED | 70.5 | 60.9 |

Halving the largest rule **still failed** (3,516 B) while `03-testing.mdc`
scored at 3,692 B — so size alone does not decide it, and a bounded rule is not
a reliable fix. **Not actioned, deliberately:** bounding `09-mcp-workflow.mdc`
would edit the agent behaviour spec (a content decision), and the sweep shows it
would not reliably work. The available remedies are all ask-first: pin a
non-reasoning `--judge-model`, take an upstream fix, or accept 2/31 UNSCORED.

### The two measurements disagree, and that is the finding

**These numbers must not be averaged, diffed, or read as a deficit.** They answer
different questions. The gap is not a quality regression; it is ρ = 0.14 made
concrete: rules can look structurally immaculate and still be judged mediocre,
because "has a `name:` and 5 sections" is not the same as "changes what an agent
does". `score-mdc-lift.js` records `comparability.againstQualityCheck: false` so
no future consumer merges them by accident.

The tombstoned rules are judged lowest, which is the expected direction: the
**WAVE F quarantine tombstone `19-automation-cycle.mdc` is the lowest rule in the
corpus at 22.8**, with `ue57-sources.mdc` (33.9, HISTORICAL),
`07-ai-agent-behavior.mdc` (37.5, RETIRED) and `08-project-context.mdc` (46.8,
RETIRED) filling four of the bottom five. The earlier text called the tombstone
"judged lowest of all (~57–63)": the direction was right, the number was
extrapolated from two rules and is wrong by ~35 points.

### Provider support (corrected earlier claim)

`skillevaluator` 0.4.0 accepts exactly five providers — `openai`, `anthropic`,
`nv_build`, `bedrock`, `openai-compatible`. **There is no xAI/Grok provider and
no `XAI_API_KEY`**, so a consumer Grok or X Premium subscription cannot serve as
the judge regardless of billing. `health-check` now passes on `nv_build`.

## Sources

- arXiv 2608.20614 — <https://arxiv.org/abs/2608.20614>
- NVIDIA SkillEvaluator — <https://github.com/NVIDIA/SkillEvaluator>
- OpenCode, *Permissions* (wildcards, home expansion, external directories) — <https://opencode.ai/docs/permissions/>
- [PIN_SYNC_POLICY.md](PIN_SYNC_POLICY.md) · [NAMING_CONTRACT.md](NAMING_CONTRACT.md)