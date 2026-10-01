# Skill Lift — consolidation and forward strategy

**Date:** 2026-10-01 · **Status:** measurement track answered and closed; two
defect fixes and one correctness sweep remain open.
**Purpose:** the single place to read what is settled, what is still open and who
owns it, and what the numbers do and do not support. It **links** to the owning
records rather than restating them, so there is one source of truth per claim.

Owning records: [HR4_B_MDC_SCORE_AND_GATES.md](HR4_B_MDC_SCORE_AND_GATES.md)
(measurements, gates, the UNSCORED decision record) ·
[HR4_A_SKILL_EVAL.md](HR4_A_SKILL_EVAL.md) (prior baseline) ·
[`docs/KNOWN_ERRORS.md`](../../docs/KNOWN_ERRORS.md) (mechanism and traps) ·
[`Saved/rules_lift.json`](../../Saved/rules_lift.json) (the artifact).

---

## 1. What is settled

| Question | Answer | Where |
|---|---|---|
| Are the rules structurally sound? | **Yes.** 87.4 mean, **31/31 pass**, deterministic | HR4_B |
| What is the judged quality? | **62.32** all-29 / **66.25** live-24 — *triage only*, see §4 | HR4_B |
| Why are 2 rules UNSCORED? | **Proven**: shared reasoning/content budget, not size | HR4_B, KNOWN_ERRORS |
| What to do about those 2? | **A adopted, B refused** (2026-10-01) | HR4_B decision record |
| Do judged and structural agree? | **No** — Spearman ρ = 0.14. That gap *is* the finding | HR4_B |
| Is Tier 3 blocked? | On **one** thing: an environment backend | HR4_B |
| Is the corpus worth re-measuring? | **No** — see §6 | this doc |

---

## 2. Two SDs that must never be confused

| Quantity | Value | What it means |
|---|---|---|
| **Within-rule SD** | **8.13** | Same rule, different judge samples → the **noise floor** for detecting change |
| Between-rule SD (all 29) | 14.38 | Real quality spread across the whole corpus |
| Between-rule SD (live 24) | 9.30 | Real spread among live rules only |

8.13 is *not* "how spread out the corpus is". Mixing the two is the easiest way
to misread this track: 8.13 governs "did it change?", 14.38/9.30 govern "do the
rules differ from each other?".

---

## 3. Tombstone split — a policy choice, and *not* a quality finding

| Set | n | Mean |
|---|---|---|
| All judged | 29 | **62.32** |
| Live (not self-declared dead) | 24 | **66.25** |
| Tombstone | 5 | 43.45 |

Excluding tombstones moves the mean by **+3.93**. Report both; keep `mean` as
all-29 so it stays comparable with the saved artifact, and add a `meanLive` for
interpretation.

**Do not read this as "tombstones are bad."** It is not true and the data says
so plainly: the *highest*-scoring tombstone, `ue57-editor-ui.mdc` at **76.35**,
outranks **23 of the 24 live rules**. Only 4 of 5 tombstones are low.

That is the most useful single fact in this document. **Judge scores do not track
rule status.** A rule that has been retired can out-score the entire live corpus,
so the score cannot be used to decide what to keep, retire or delete — which is
exactly the use one would be tempted to put it to. It is a writing-quality
signal, nothing more.

---

## 4. Measurement defects — found, unfixed. Fix before spending more calls

**D1 · Criterion denominators vary.** `parseCriteria` reads the judge's **CLI
text table** (`scripts/score-mdc-lift.js:165`), and the merge at `:564` averages
each criterion over only the samples whose table listed it. So 7 of 29 rules
contribute partial criteria (5 of them miss 7 of 9), and each criterion mean has
an **unknown denominator**.
*Effect is bounded but real:* recomputing on the 22 rules carrying all nine
criteria shifts every criterion mean by **≤0.16/10**, so the **ranking is safe**
— Example Quality ~3.6–3.7 and Error Handling Quality 4.8 remain clearly
weakest. But do not quote the absolute means to two decimals as if exact.
**Fix:** switch the parser to `-r json` (`overall_score` / `judge_score` /
`checks[]`) for a deterministic nine criteria per sample. This is a defect fix,
not a nice-to-have.

**D2 · `judge.retriedCount` undercounts.** It counts only *scored* rules — 7 in
the cold report, against **9** rules that actually retried. Reporting-side only;
needs no re-run.

---

## 5. Cost model — why whole-corpus re-judging is the wrong unit

Measured with the tool's own `pooledWithinSd` on the saved report
(**8.1331**), at 80 % power / two-sided 5 %, so samples per side =
`2·(2.8·σ/δ)²`. A full-corpus `--repeat 2` pass costs **58 samples / 88 calls**;
the cached second pass **48 calls** (45 % cheaper).

| Δ to detect | Samples/side | Total calls | × a full pass |
|---|---|---|---|
| 2 | 260 | 520 | 9.0× |
| 3 | 116 | 232 | 4.0× |
| 5 | 42 | 84 | 1.4× |
| **8** | **17** | **34** | **0.6×** |
| 10 | 11 | 22 | 0.4× |
| 15 | 5 | 10 | 0.2× |

**Read this before proposing any judged run.** A 3-point change to one rule costs
**4× a full corpus pass** and still answers only about that one rule. The
instrument's cheapest useful question is *"did this one rule get ≥8 points
better?"* at 34 calls.

**Adopt as policy:** one named question, one named rule, `--only`, `--repeat 8`
or more, and **accept only Δ > 8.13**. Never re-judge the corpus "to see" — at
2/31 unmeasurable and a partially-lossy criteria table, a full pass mostly buys
noise.

---

## 6. Strategy — the actual plan

**The recommendation is to stop measuring.** The question the track asked — *are
these rules good?* — is answered and the answer is stable. Structural quality is
maxed and needs nothing; judged quality's one actionable signal (weak examples,
weak error-handling guidance) is a **content** change, which is Lead taste, not
a measurement question. And per §3 the judged score cannot even rank live against
dead rules. No pending decision needs another judged run.

| # | Action | Owner | Cost |
|---|---|---|---|
| **S1** | Close the measured track at 29/31; stop whole-corpus judged passes | agent | done by this doc |
| **S2** | Fix D1 (`-r json`) and D2 before any next judged run | agent | code + tests; D2 needs no re-run |
| **S3** | Adopt §5 as the judging policy; retire ad-hoc corpus passes | agent | policy, free |
| **S4** | **Correctness before measurement:** triage the repo-wide UE 5.7 sweep | Lead/Conductor | ~100 matches; `Docs/08c_BOOT_HEALTH.md` first |
| **S5** | Keep the gate boundary: structural = gate, judged = triage | agent | standing rule |

**S4 outranks everything else here.** It is unrelated to the harness track, it
gates WAVE C, and boot-health evidence collected against the wrong Engine is
worthless — `Docs/08c_BOOT_HEALTH.md` still states a validated-on-5.7.4 baseline
while the project is locked to 5.8. No amount of further rule measurement
competes with fixing that.

**Do not promote the judged score into a gate.** Three independent reasons: the
8.13 noise floor, a permanent 2/31 blind spot, and the D1 denominator defect.

---

## 7. Open register

| Item | Owner | Blocked on | Closes when |
|---|---|---|---|
| Wire `rules:score --strict` into CI | **Lead** | ask-first | Lead rules yes/no |
| Pin `skillevaluator` in `package.json` | **Lead** | ask-first (dependency change) | Lead decides |
| Tier 3 live agent eval | **Lead** | an environment backend — Docker locally, or a cloud sandbox account | account exists |
| D1 `-r json` parser | agent | **unblocked** | implemented + tested |
| D2 `retriedCount` fix | agent | **unblocked** | one line + test |
| `meanLive` alongside `mean` | agent | **unblocked** | report shows both |
| Repo-wide UE 5.7 sweep | **Lead/Conductor** | ownership of ~100 matches | triaged; `08c` first |
| Is WAVE C still the right next thing? | **Lead** | Lead call — the untracked `t0_m*_*.py` boot probes suggest later boot-health work exists | confirmed or replaced |
| Rule-content fixes from the judged signal (examples, error handling) | **Lead** | taste call, needs a taste gate | Lead decides what to change |

⚠️ On Tier 3: **do not** take `health-check`'s own suggestion to reinstall
`"skillevaluator[all]"` from git HEAD. It moves the scorer off 0.4.0 and breaks
comparability with `Saved/rules_lift.json`. The real fault is only that
`harbor.exe` is unlinked from `PATH`.

---

## 8. What would change this strategy

- **A non-reasoning judge credential** → re-baseline (not a completion), after
  which per-criterion work becomes trustworthy and the 2/31 gap closes.
- **A scorer that separates reasoning from content budget** → fixes the 2/31 and
  makes retries meaningful. Out of our control.
- **A real Δ target.** If the Lead wants "did this rule improve by 3 points", the
  honest answer is that the instrument cannot say — §5 puts that at 232 calls for
  one rule. Take the content review instead; it is cheaper and more reliable.

---

## 9. Reproducing every number here

```
node -e "const{pooledWithinSd}=require('./scripts/score-mdc-lift.js');const r=require('./Saved/rules_lift.json');console.log(pooledWithinSd(r.results.filter(x=>x.score!==null).map(x=>x.runs)))"
```

Yields **8.1331**. Criterion means, the live/tombstone split and the power table
are all derived from [`Saved/rules_lift.json`](../../Saved/rules_lift.json), which
is the only artifact — every figure in this document is re-derivable from it.
