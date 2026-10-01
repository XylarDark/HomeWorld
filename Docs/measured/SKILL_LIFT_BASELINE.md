# Skill Lift — tracked judged baseline

`Saved/` is gitignored, so the full `Saved/rules_lift.json` does not travel with a
clone. This file is the **small tracked summary** of that run: enough to tell
whether a later run is comparable, and to reproduce every headline figure without
the 21 KB-per-run judge reports.

**The raw artifact remains the authority.** If these numbers and
`Saved/rules_lift.json` ever disagree, the JSON is correct and this file is stale.

## Run identity — check this first

A judged score is only comparable to another judged score from the **same judge
and the same scorer version**. Changing either is a **re-baseline**, not a
completion.

| Field | Value |
|---|---|
| Tool | `scripts/score-mdc-lift.js` |
| Scorer | SkillEvaluator **0.4.0** (required; 0.3.0 → 0.4.0 already moved the mean once) |
| Judge provider | `nv_build` (NVIDIA Build) |
| Judge model | `nvidia/nemotron-3-super-120b-a12b` |
| Judge type | **reasoning** model with a shared reasoning+content budget — see below |
| Repeats | 2 per rule |
| Generated | see `Saved/rules_lift.json` → `generatedAt` |
| Corpus | `.cursor/rules/*.mdc` — **31 rules** |

## Headline figures

| Measure | Value |
|---|---|
| Rules | **31** |
| Judged | **29** |
| UNSCORED | **2** (accepted — see below) |
| **Mean (all judged)** | **62.32** |
| **Mean (live rules only)** | **66.25** over 24 rules |
| **Mean (tombstones only)** | **43.45** over 5 rules |
| Standard error of mean | ±1.51 (judge noise only) |
| **Pooled within-rule SD** | **8.1331** — the noise floor for every delta here |
| Range | 22.8 – 78.6 |
| Below 70 | 19 of 29 |
| Judge mean spread | 7.22 · max spread **35.5** |
| Judge calls | 88 (57 samples cache-served on the second pass) |

## Comparability rules

- **Never average or diff the judged mean against the structural mean.** The
  structural score (`rules:score`, mean **87.4**, 31/31, deterministic) is a
  *different measurement*; the report sets `comparability.againstQualityCheck:
  false`. Measured ρ between the two is 0.14.
- **Never quote a single judge's run as a rule's score.** Within-rule SD is
  **8.1331**. Accept a rule-level change only at **Δ > 8.13**.
- **Never re-judge the whole corpus to answer a per-rule question.** At 80 %
  power, moving one rule by 3 points costs ~232 calls — 4× a full corpus pass.
  Use `--only <rule> --repeat ≥8`.
- **A tombstone is not a quality signal.** The highest-scoring tombstone
  (`ue57-editor-ui.mdc`, **76.35**) outranks **23 of the 24** live rules. Judge
  score does not track rule status, so it must not decide keep/retire.

## The 2 UNSCORED rules — accepted, not a regression gate

Mechanism is proven, not guessed: `nvidia/nemotron-3-super-120b-a12b` is a
reasoning model with a **shared reasoning+content budget**, hardcoded at 4096
with no override. Control: `"say ok"` with `max_tokens=64` returns
`finish_reason='length'`, `content_len=0`, `reasoning=64` — the entire budget goes
to reasoning and no content is emitted, which surfaces as
`EmptyLLMResponseError` → the misleading `LLM not configured` message.

The credential reaches only that one function, so `--judge-model` cannot be
swapped with the key on hand. The Lead **adopted** accepting 2/31 UNSCORED as
final (29/31 judged), **refused** bounding the rules, and **deferred**
re-baselining. Do not treat this as a regression.

## Weakest signal (triage, not a gate)

Per-criterion means identify where the corpus is actually thin. Example Quality
and Error Handling Quality are the two lowest.

**A bounded content pass has since run on the weakest live rule**
(`14-json-yaml.mdc`): worked examples only, judged before and after with
`--only … --repeat 8`. Score **54.1 → 77.89** (Δ **+23.8**), Example Quality
**0 → 8.5**, Error Handling **1.5 → 8.0**. Two independent after-runs agreed to
**0.06 pts**. Full record:
[Docs/handoffs/SKILL_LIFT_CONSOLIDATION.md](../../Docs/handoffs/SKILL_LIFT_CONSOLIDATION.md) §10.

This does **not** move the corpus mean above, which stays the 29-rule cold
measurement. A single-rule change is a single-rule change.

## Reproducing

```powershell
# structural (deterministic, keyless) - the regression gate
npm run rules:score -- --strict

# judged (needs the judge credential in env; never commit it)
npm run lift:score -- --json Saved/rules_lift.json --repeat 2
```

Cache reuse cuts cost, not jitter, and mixes samples across days — use
`--no-cache` for a clean before/after.

Full analysis, cost model, decision record and the two fixed measurement defects:
[Docs/handoffs/SKILL_LIFT_CONSOLIDATION.md](../../Docs/handoffs/SKILL_LIFT_CONSOLIDATION.md).
