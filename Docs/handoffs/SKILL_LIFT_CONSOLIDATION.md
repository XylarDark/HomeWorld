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

## 4. Measurement defects — both FIXED 2026-10-01 (code landed, not yet re-run)

**D1 · Criterion denominators varied.** `parseCriteria` read the judge's **CLI
text table**, and the merge averaged each criterion over only the samples whose
table listed it. So 7 of 29 rules contributed partial criteria (5 of them missing
7 of 9) and every criterion mean had an **unknown denominator**. *Effect was
bounded but real:* recomputing on the 22 rules carrying all nine shifted each
criterion mean by **≤0.16/10**, so the **ranking was safe** — Example Quality
~3.6–3.7 and Error Handling Quality 4.8 remain clearly weakest.

> **Root cause found, and it was not "a partial report".** The CLI prints a
> box-drawn table whose Criterion column **wraps across lines on a narrow
> terminal**, and its numbered "Failure Details" list is matched **by row index** —
> so a wrapped row silently loses its criterion. The scorer had emitted all nine
> every time. This is why the loss was intermittent and rule-dependent.
>
> **Fix (landed).** `runRubricOnce` now runs `-r cli,json -o <tmpdir>` and parses
> `rubric_eval.checks[]`, which is **always exactly nine** and is keyed by a
> stable `id` (e.g. `example_quality`). The stable key is `id`, **not**
> `criterion` — the latter is the full rubric question text. The CLI text is
> retained as fallback and `criteriaSource` records which one answered. Denominators
> are now explicit per rule as `fullCriteriaSamples`/`criteriaSamples`.
>
> **Verified bonus.** `rubric_eval.aggregation` names the roll-up, and
> `weightedOverall()` reproduces it: `10 · Σ(w·s)/Σ(w)` with high=3, medium=2,
> low=1. Confirmed exactly against two real runs (70.5 and 75.0). `rollupVerified`
> flags any run where that stops holding — an upstream shape change surfaces
> instead of passing silently.
>
> **Not re-run corpus-wide.** `Saved/rules_lift.json` predates D1 and stays the
> canonical artifact. D1 pays off on the next **targeted** run; whole-corpus
> re-judging remains retired (§5).
>
> **D1 proven end-to-end 2026-10-01**, not just by unit test — one live judge run
> (`--only 15-shell-scripts.mdc --repeat 1 --no-cache`, judge
> `nvidia/nemotron-3-super-120b-a12b`, scorer 0.4.0):
>
> | Field | Value | Meaning |
> |---|---|---|
> | `criteriaSource` | `json` | the JSON path answered, not the CLI table |
> | criteria present | **9 / 9** | fixed denominator; the old parser would drop rows here |
> | `fullCriteriaSamples` | `1/1` | the sample carried the full nine |
> | `rollupVerified` | `true` | `weightedOverall` reproduced the scorer's own composite |
> | `importance` | 9 criteria | per-criterion weights now captured |
> | `judge.retriedCount` | `0` (0 scored / 0 unscored) | D2 field present and correct |
> | `mean` / `meanLive` | `69.5` / `69.5` (1 live, 0 tomb) | P3 field present |
>
> That single run also **caught a defect the 64/64 unit tests could not**: the
> new console line called `.toFixed()` on a `null` `meanTombstone` and crashed,
> because a `--only` run on a live rule has no tombstones. The bad call sat in
> `main()`, which no keyless test can reach. Fixed by extracting `formatLiveSplit()`
> so the null-on-either-side shape is testable, plus 5 regression tests (69/69 now).
> *A green test suite is not evidence the tool runs; the run is.*

**D2 · `judge.retriedCount` undercounted.** It counted only *scored* rules — 7 in
the cold report, against **9** rules that actually retried. Reporting-side only;
needed no re-run. **Fix (landed):** `retriedSplit()` counts every rule that
retried and reports `retriedScored` / `retriedUnscored` separately, so retries
that ended UNSCORED — the most diagnostic ones — can no longer be filtered out.

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
| Wire `rules:score --strict` into CI | **Lead** | ask-first | **Lead answered 2026-10-01: no CI change yet.** Revisit after D1 is in practical use. |
| Pin `skillevaluator` in `package.json` | **Lead** | ask-first (dependency change) | **Lead answered 2026-10-01: no pin — record the required version (0.4.0) in docs only.** Done, §2a. |
| Tier 3 live agent eval | **Lead** | an environment backend — Docker locally, or a cloud sandbox account | **Lead answered 2026-10-01: defer.** Needs an account the agent cannot create. |
| D1 `-r json` parser | agent | **unblocked** | **DONE** — `checks[].id`, CLI fallback, root cause recorded, 64/64 tests |
| D2 `retriedCount` fix | agent | **unblocked** | **DONE** — `retriedSplit()`, scored/unscored split, tested |
| `meanLive` alongside `mean` | agent | **unblocked** | **DONE** — `liveSplit()`, tested against the recorded 24/5 split |
| Roll-up verification | agent | **unblocked** | **DONE** — `weightedOverall()` + `rollupVerified`, verified on two real runs |
| Repo-wide UE 5.7 sweep | **Lead/Conductor** | **resolved 2026-10-01** — census is **231 matches / 67 files** (not ~100), most legitimately historical. `08c` corrected. Remainder stays a Lead call, "correct live claims, keep history". |
| Is WAVE C still the right next thing? | — | **RESOLVED 2026-10-01** | **Not a question: WAVE C is COMPLETE and signed off** (PR #13, `APPROVE WAVE C`). The `t0_*.py` scripts are **gameplay** beat-prove harnesses, not boot-health. See §6. |
| Rule-content fixes from the judged signal (examples, error handling) | **Lead** | taste call, needs a taste gate | **Lead answered 2026-10-01: not now** — measurement was the ask. Remains open for a future taste-gated pass. |

⚠️ On Tier 3: **do not** take `health-check`'s own suggestion to reinstall
`"skillevaluator[all]"` from git HEAD. It moves the scorer off 0.4.0 and breaks
comparability with `Saved/rules_lift.json`. The real fault is only that
`harbor.exe` is unlinked from `PATH`.

---

## 2a) Lead interview decisions — 2026-10-01

Conducted as a structured interview; **all recommendations were accepted**, so
execution scope was the agent-unblocked work only.

| Question | Decision | Consequence |
|---|---|---|
| Execution scope | **Harness defects only** | D1, D2, `meanLive`, roll-up verification — no CI, no dependency, no product surface |
| CI gate for `rules:score --strict` | **No CI change yet** | Ask-first item stays open; wire after D1 is in practical use |
| Pin `skillevaluator` in `package.json`? | **Record version in docs, no pin** | Keeps a Python/uv CLI out of a Node manifest. **Required scorer version: `skillevaluator` 0.4.0** — comparability with `Saved/rules_lift.json` depends on it, and 0.3.0 → 0.4.0 already moved the corpus mean once |
| UE 5.7 sweep depth | **Correct live claims, keep history** | Policy for whenever the sweep is authorised — do not falsify the `KNOWN_ERRORS` 5.7 history or the literal `ue57-*` rule filenames |
| Tier 3 live agent eval | **Defer — needs an account** | Blocked on an environment backend only, not on the CLI |
| Judged-signal content work | **Not now** | Measurement was the ask; rule prose is a separate taste-gated job |
| WAVE C direction | **Conductor assesses first** | Assessment returned — §6 |

**Standing constraints reaffirmed:** the judge credential stays env-only and is
never committed; user untracked work and the dirty `UserHarness` submodule are
not touched; no product decisions are invented.

### 2b) Second interview decisions — 2026-10-01 (round two)

Every option was new — none of these existed as choices in round one, because
none of them had been reached yet.

| Question | Decision | Consequence |
|---|---|---|
| Make "green tests ≠ tool runs" a standing rule? | **KNOWN_ERRORS + register, no new `.cursor/rules` entry** | Recorded as a Harness trap. Deliberately *not* a rule: adding one would change the 31-rule corpus and move `meanLive` |
| Preserve the judged baseline, which is gitignored? | **Commit a small tracked baseline summary** | A fresh clone otherwise has no baseline at all. Full 21 KB-per-run judge reports stay uncommitted |
| Revisit the CI gate now D1 is proven? | **Wire as a non-blocking check** | Surfaces structural drift in the PR UI without blocking merges. Replaces "no change yet" |
| Guard the scorer version? | **Preflight check, not a `package.json` pin** | `npm run doctor` asserts the installed scorer is 0.4.0 and warns otherwise. Catches the 0.3.0 → 0.4.0 class of drift where it happens |
| Rule-content pass on the judged signal? | **One rule, examples only** | Weakest live rule, then one targeted `--only … --repeat 8` run accepting only Δ > 8.13 |
| PHASE_BOARD T0 gap + self-contradiction? | **Delegate to the Conductor** | It owns the board; it can separate documented status from inference |
| 5.7 sweep remainder? | **Just the three siblings** | `08b_HARNESS_GAP.md`, `08_AUDIT_UPGRADE_STRATEGY.md`, `08a_INVENTORY.md` — same audit family, same defect class as 08c. The other ~220 matches stay put |
| Branch policy | **Keep fast-forwarding `main`** | Agent stages by explicit path, runs gates, fast-forwards when the branch is a clean FF |

---

## 6. WAVE C — resolved: complete, not superseded

Referred to the Conductor as record owner. **Verdict: WAVE C is done and signed
off.** It is not next, and it is not superseded. Two findings killed the premise
of the referral.

| Finding | Evidence | Conclusion |
|---|---|---|
| WAVE C completed long ago | `Docs/08_AUDIT_UPGRADE_STRATEGY.md` **COMPLETE**; `Docs/08_AUDIT_SIGN_OFF.md` gate **CLOSED** with `APPROVE WAVE C`; `08d_CONTENT_CANON.md` WAVE C COMPLETE; `Docs/README.md`; `swarm/PHASE_BOARD.md` Docs/08–10 **CLOSED** (PR #13) | The "Next (after gate) → WAVE C" row is a historical pointer, not a live plan |
| The `t0_*.py` scripts are **not** boot-health | Zero matches for any 08c boot term (`SetCollisionProfileName`, `PostInitProperties`, `NewObject`, `FObjectInitializer`, BOOT-00x, C2084) across all 17. `t0_m10_planetside_boot_prove.py` is the **gameplay beat** "planetside night boot home"; `t0_m12/m13_map_probe.py` are world inspectors | The referral premise was **wrong**. "boot" in T0 is a gameplay verb. T0 *builds on* WAVE-C-fixed code — it is a consumer, not a replacement |
| The 5.7.4 anchor was a real, small defect | `Docs/08c_BOOT_HEALTH.md` asserted 5.7.x/5.7.4 against a 5.8 lock; substance already re-proved on 5.8 by `Docs/22_UE58_UPGRADE.md` **U58-C** (APPROVED, `5.8.2-56702186`, Safe-Build exit 0) | **Corrected** — 4 lines + a 5.8 re-validation evidence row, gate block untouched |
| Repo-wide 5.7 census is larger than assumed | **231 matches / 67 files** (not ~100). Heaviest: `docs/KNOWN_ERRORS.md` 46, `docs/SESSION_LOG.md` 27, `docs/PCG/PCG_VARIABLES_NO_ACCESS.md` 16 | Much is legitimate history. A mechanical 5.7→5.8 rewrite would falsify true records. Remainder is a Lead call under "correct live claims, keep history" |
| T0 governance is inconsistent (separate issue) | `swarm/PHASE_BOARD.md` has **zero** T0 rows, and L3 ("Harness / bot optimization — idle") contradicts L168 ("Current track: Docs/33 PS"). `APPROVE-T0-MECHANIC-INV` box is unchecked while M1–M14 merged (#255–#268) | **Not a boot-health issue.** Board/record consistency for a live track — flagged, not actioned |

**Correction applied.** `Docs/08c_BOOT_HEALTH.md` engine labels now read 5.8
(`5.8.2-56702186`), with an explicit provenance note that the WAVE was authored on
5.7.4 and superseded by Docs/22 U58-C, plus a §4 evidence row so §3's CLOSED
crash table has a 5.8-shaped anchor instead of only a 5.7 one. The BOOT-001 root
cause keeps its historical observation, relabelled as observed at authoring.

**Unanswerable from the tree** (recorded, not guessed): whether
`APPROVE-T0-MECHANIC-INV` was ever stamped outside the document, and whether any
T0 beat was proved green in a *tracked* sense — the `Saved/t0_*_gate.json` files
are gitignored local runtime state, and the sampled `t0_m14` is self-reported
`"provisional": true`.

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
