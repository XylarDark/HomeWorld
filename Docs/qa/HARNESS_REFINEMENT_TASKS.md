# Harness refinement tasks

Derived from the first full taste run (`6f88a7f`, 2026-10-01). Each task states the
finding that motivates it, what "done" means, and how it will be proven. Order is by
value per unit of cost, not by ease.

Status legend: **done** · **open** · **blocked** (needs something this repo does not have)

---

## R1 — Audit the taste checks for phrasing sensitivity — **DONE `b80bb41`**

Four checks measured wording, not canon. Three rewritten to accept the canon's real
vocabulary; the neon/tech-gate ban **deleted** because a banned-term check cannot live
in a document whose job is stating rejection criteria (markdown puts `Fail when` in
the header row). The verdict-vocabulary check had accepted the word `pass` and so
could not fail. Two new tests were passing **vacuously** (they seeded after writing,
so every check returned `void`) — both now seed first and assert `subjectPresent`.

## R2 — Add the `docs-only` third arm — **DONE**

`ARMS` in `scripts/task-lift.js`; `--arms with,docs-only,without`. `docs-only` keeps
`AGENTS.md` / `START_HERE.md` / `swarm/` and drops `.cursor/` + `.agents/` +
`UserHarness/`, so `with` vs `docs-only` isolates the rules corpus and `docs-only`
vs `without` isolates the entry points. Verified by three distinct tree fingerprints
(4264 / 4172 / 4143 files) and per-arm removal counts. **Not yet run with real
agents** — see R4.

## R3 — Paired significance test — **DONE**

`mcnemarExact()` — exact two-sided binomial on discordant per-check outcomes. Reports
`p = null` and an explicit note when there are **no discordant pairs**, because
reporting `p = 1` from an absence would be inventing a result from an absence. The
report now says *"Not significant — at this sample size, treat any delta above as
noise"* rather than presenting a bare delta. `summarize` also emits `byArm` so a third
arm is visible rather than invisible.

---

## R4 — Run `--trials 2` for real — **OPEN, now unblocked**

**Supersedes the original R4.** R1–R3 are done, so the instrument is worth spending
sessions on. Recommended run:

```
npm run tasklift:run:taste -- --model opencode/space-bunny-free --trials 2 --arms with,docs-only,without --min-valid 2
```

4 tasks × 3 arms × 2 trials = **24 sessions**, verified available on the free model.
Three-arm is now affordable *and* is the only run that answers the question the
two-arm design could not.

**Finding.** Run 1 produced `lift −7.4pp`, driven by three individual checks. Two of
them failed on *wording*, not on knowledge:
`pairs the shrine light against the cabin key` requires the literal string
`Cabin amber`, so "the cabin's warm window light" fails; and
`the shrine is a handmade spirit cue, not a tech gate` is a banned-term check that
still lacks the `unless` negation guard added to the *material* check in `e937c9a`.
This is the third occurrence of the same defect class — a check that measures the
author's phrasing rather than the canon.

**Done when** every taste check is classified as *canon-bearing* or *phrasing*, and
every phrasing check is either rewritten to accept the real vocabulary of the canon
(synonyms, the actual palette-chip names, the actual negative phrasings) or replaced
with a check that cannot be satisfied by word choice alone.

**Proven by** the same three checks failing on a hand-written "correct but worded
differently" fixture, exactly as `noneMatch` is proven in both directions today.

**Cost.** Zero agent sessions.

---

## R2 — Add the `docs-only` third arm — **OPEN**

**Finding.** The preregistration's own structural limit: `ABLATE_PATHS` removes the
harness but **not** `Docs/`, so the art bible is reachable from both arms. Run 1
therefore measures whether the harness *points an agent at* the canon, not whether the
canon was available. That is a real question but a narrower one than the results
imply, and it is stated in the manifest and the prereg rather than hidden.

**Done when** a third condition exists: `AGENTS.md` + `docs/` + `Docs/` retained, with
`.cursor/`, `.agents/`, `swarm/`, `UserHarness`, `START_HERE.md` removed. It isolates
the always-on rules layer from the documentation layer, which is the only way to tell
"the rules told it where to look" apart from "it would have found it anyway".

**Proven by** a dry run reporting three distinct worktree fingerprints, and by
`verifyAblation` asserting the expected surfaces per arm rather than one global list.

**Risk.** Triples the session count. Do not run it before R1, or the extra sessions
buy three times as many phrasing artefacts.

---

## R3 — Replace the proportion delta with a paired significance test — **OPEN**

**Finding.** The preregistered rule compares two proportions. `summarize` already
restricts to complete pairs (DEC-0012), but the statistic is still a difference of
means with no dispersion and no test. At 1 trial per cell nothing can be inferred
from it either way, which is precisely why R1 fired instead of a conclusion.

**Done when** lift is reported with a paired exact test (McNemar on per-check binary
outcomes within pairs) alongside the raw delta, and the report states the power it
does and does not have.

**Proven by** a fixture where the paired test and the naive proportion disagree, and
the report follows the paired test.

**Cost.** Zero agent sessions.

---

## R4 — Run `--trials 2` for real — **BLOCKED (pending R1, R3)**

**Finding.** Every taste result so far is 1 trial per cell. The runner supports
`--trials` and it has never been exercised against real agents.

**Done when** 16 sessions complete with no void run, or the voids are explained.

**Blocked by** R1 — running 16 sessions before the checks are phrasing-audited spends
real money measuring the instrument's wording.

**Cost.** 16 sessions; verified available on `opencode/space-bunny-free`.

---

## R5 — A competing-model adversarial pass — **OPEN, deliberately deferred**

**Finding.** The Week 1 harness guidance asks for a competing-LLM review; nothing in
`scripts/` implements it. After the 2026-10-01 ownership reset the agent owns
self-review, which is the one place a sycophantic model flatters its own work.

**Why deferred.** A same-model adversarial pass is close to worthless for this
purpose, and the PDF means a *different* provider. Rather than build something that
looks like the thing and is not, it is recorded as absent in
`docs/human-use/cursor-cannot/harness-engineering.md` where a reader will meet it.

**Revisit when** a second provider is actually available. Not before.

---

## R6 — Cost and token accounting per run — **OPEN, low value**

A line in the report so practicality is visible. Only worth doing if the pilot is run
often enough for it to matter. Not started.

---

## Ordering

**R1 → R2 → R3 → R4.** R1 is free and unblocks the interpretation of everything
measured so far. R2 triples cost and must not run on unaudited checks. R3 makes the
number mean something before R4 produces more numbers. R5 is deferred on purpose, R6
is optional.
