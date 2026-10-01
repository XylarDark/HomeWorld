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

### DEC-0010 — Spending agent sessions requires `--run` (2026-10-01)

- **Area:** harness refactor
- **Decision:** The runner refuses to start agent sessions unless `--run` is passed.
  The old default was the opposite: agents ran unless `--dry` was passed.
- **Rationale:** Asking for a report cost eight real sessions, and I paid that twice
  before noticing. A default that spends money when the caller only wanted output is
  the wrong default for anything expensive. The alternative — keeping the permissive
  default and documenting it — was rejected because the documentation is what I
  failed to read the first time.
- **Evidence:** `main()` returns 2 with a message naming both flags; a test spawns the
  runner without `--run` and asserts exit 2, and another asserts every spending npm
  script passes `--run` explicitly.
- **Reverses if:** Never on the guard itself. If a wrapper genuinely needs a
  different default, give it its own flag rather than inverting this one.

### DEC-0011 — The taste beats are the benchmark; the chores are an instrument sanity set (2026-10-01)

- **Area:** code design
- **Decision:** Keep both manifests. `tasks.json` (chores) is a sanity set; the new
  `tasks-taste.json` (art master spec, shot brief, asset naming, T0 beat packet) is the
  benchmark. The decision rule is preregistered in
  `Docs/qa/TASK_LIFT_PREREGISTRATION.md` before any taste data exists.
- **Rationale:** The chore tasks are at ceiling — both arms already do those jobs — so
  they measure the instrument and nothing else, which is worth having but is not
  evidence about the harness. The alternative was to swap the chores out, which
  would have thrown away a validated sanity set. Stating the threshold (`d ≥ 0.25`)
  in advance matters: any non-null number can be called large if "large" is defined
  afterwards.
- **Evidence:** Both manifests' controls reach 100% (chores 8/8, 9/9, 6/6, 5/5;
  taste 10/10, 7/7, 4/4, 10/10). A test also scores a deliberately wrong art answer
  against the same checks and asserts it fails, so the checks are not merely
  satisfiable but discriminating.
- **Reverses if:** The taste benchmark turns out to be at ceiling too, or the checks
  prove sensitive to wording rather than to knowing the canon.

### DEC-0012 — Compare paired tasks only, and never retry a substantive failure (2026-10-01)

- **Area:** code design
- **Decision:** A task contributes to the lift only when **both** its arms have a
  valid run. Retries happen only for transport failures (429, 5xx, dropped socket,
  timeout) — never for a non-zero exit that is not transport noise.
- **Rationale:** Two failure modes found while implementing P0. First, a single void
  run discarded the whole experiment, which made the instrument too brittle to
  survive ordinary infrastructure noise. Second — and worse — excluding the void run
  but keeping its partner's task produced an *unpaired* comparison: averaging
  `a/with` against `a/without + b/without` while `b/with` is missing compares two
  groups built from different subjects. That is the same fallacy as comparing
  independent proportions, and my first implementation of the fix introduced it.
  On retries: retrying a run that failed substantively would silently replace a
  measurement with a more flattering one, which is worse than a void.
- **Evidence:** `summarize` reports `pairedTasks`, `droppedPairs` and `validByCell`;
  a dry run additionally withholds the lift, because scoring an untouched worktree
  produced a "0pp" that was an artifact of no agent running. Tests pin the pairing,
  the dropped-pair reporting, the dry-run withholding, and that a timeout is
  transient while "the model refused to continue" is not.
- **Reverses if:** Repeats per cell arrive and a mixed-effects model replaces the
  paired proportion. The pairing rule survives that; only the estimator changes.

### DEC-0013 — The pilot selects and records its model (2026-10-01)

- **Area:** code design
- **Decision:** `--model` is passed through to the driver and the model id is recorded
  in `meta` and printed in the report.
- **Rationale:** The runner never selected a model, so it inherited the client default
  — which sits on the OpenCode Console account returning `402 Insufficient account
  funds`. A harness experiment was therefore hostage to an unrelated billing state,
  and I had been treating "the pilot is blocked" as a fact when the paid model was
  only one of several. Free models (`space-bunny-free`, `nemotron-3-ultra-free`) were
  verified to complete real work. The alternative — leaving the model implicit —
  is rejected for a second reason: a result that does not name its model cannot be
  reproduced, and judge/model identity is part of the measurement (the same reason
  the scorer version is pinned).
- **Evidence:** Probe: both free models created a file, exit 0. Two real paired runs
  (`asset-naming`, `art-master-spec`) then completed with 0 void.
- **Reverses if:** Never on recording the model. Selecting it by default can change.

### DEC-0014 — Two taste checks were wrong; the harness arm "losing" was my bug, not its result (2026-10-01)

- **Area:** code design
- **Decision:** `noneMatch` gains an optional `unless` pattern so a banned term on a
  line that negates it is not a hit; the `NightMix` range pattern accepts the several
  ways a range is actually written. Both fixes are pinned by tests in both directions.
- **Rationale:** The first real taste run reported the with-harness arm at 0.78
  against the ablated arm's 1.0 — a −22pp lift, the preregistered "harness scored
  worse" verdict. It was an artifact. The arm that *read the canon* quoted the
  canon's prohibition ("not photoreal, no grimdark") and a bare banned-term regex
  failed it for being correct. The asymmetry matters more than the bug: the arm that
  consults the documentation is structurally more likely to name the banned words,
  so this check was biased against the harness by construction. I recorded the verdict
  before investigating it, which is why the preregistration mattered — it forced the
  number to be examined rather than believed.
- **Evidence:** Re-run after the fix: 1.0 in both arms. Two checks, two runs, four
  agent sessions on a free model.
- **Reverses if:** n/a — these are correctness fixes.
- **Note on the remaining result:** both tasks now score 1.0 in both arms, i.e. a
  **null**. Under the preregistered rule that is *inconclusive*, and the correct
  sentence is "this benchmark did not detect an effect", not "the harness does not
  help". n=1 task, n=1 trial. Do not upgrade that sentence.
---

### DEC-0015 — "Hunyuan3D and TRELLIS are on a do-not-use list; the pipeline fails closed on free tiers" (2026-10-01)

- **Area:** architecture / tooling
- **Decision:** Neither Hunyuan3D-2/2.1 nor TRELLIS/2 may be used to produce any asset
  that reaches `Content/`. Meshy and Tripo are usable **only on a paid tier**; free-tier
  output must cause a hard failure at generation time, not a warning. Tier is asserted
  at generation, recorded in the sidecar, and re-checked at promote.
- **Rationale:** Read from the license files, not vendor pages. Hunyuan3D's license
  opens by stating it *"DOES NOT APPLY IN THE EUROPEAN UNION, UNITED KINGDOM AND SOUTH
  KOREA"*, and §5.c forbids using outputs outside that Territory. We target PC + Steam
  Early Access, where EU distribution is the normal case. TRELLIS is MIT on the code
  while the project page states the materials are *"not intended for commercial
  exploitation or use"* — a real ambiguity I decline to resolve by guess. Meshy free is
  CC BY 4.0 (attribution mandatory in a shipped game); Tripo free retains all IP rights
  in outputs. No agent running unattended will notice a tier change underneath it, so
  the pipeline must fail closed rather than warn.
- **Evidence:** `Tencent-Hunyuan/Hunyuan3D-2.1` LICENSE §1.l and §5.c; `microsoft/TRELLIS`
  LICENSE + `trellis3d.github.io`; `docs.meshy.ai` terms; Tripo ToS 5.2.1.
  Full write-up in [Docs/34_ART_PIPELINE_RESEARCH.md](../../Docs/34_ART_PIPELINE_RESEARCH.md) §2.
- **Reverses if:** legal counsel clears a specific tool in writing. Hunyuan's clause is
  explicit enough that this would need a negotiated licence, not a reading.
- **Note:** this is the finding I would act on first if the reader acts on one thing.
  It is cheap to comply with now and expensive to unwind after assets ship.

---

### DEC-0016 — "The kit pipeline is deterministic batch variant generation, not AI mesh generation" (2026-10-01)

- **Area:** architecture
- **Decision:** Build the pipeline around a checked-in generator producing kit variants
  and instance sets from an authored master. AI mesh generation is an **experiment gated
  behind measurement**, not the pipeline. The existing 30-minute rule stands until it is
  replaced by real numbers.
- **Rationale:** The research recommended the opposite — native low-poly generation now
  exists and our 12–1,680 tri budgets sit inside its native range, which was not true
  when the 30-minute rule was written. I am not taking that recommendation. (1) The
  highest-leverage agent task here is thirty consistent cliff-module variants, which
  nobody hand-models and which code does deterministically under a seed. Generation
  gives a *different* rock, not a variant of *our* rock. (2) Everything in `HW_Hero`
  needs authored topology: the art bible says the face is built from planes that act and
  to spend triangles on the face — no generator produces deliberate deformation-zone
  edge flow, which is why Hunyuan's own PolyGen paper headlines that property as its
  contribution. (3) Compliance cost does not shrink with volume; every AI asset owes a
  sidecar, a log row and a licence note.
- **Rejected:** adopting generation as the pipeline on the strength of vendor marketing
  ("built low, not crushed"), which is explicitly unbenchmarked and, per the 2026 survey
  arXiv 2604.23629, unfalsifiable while no game-readiness benchmark exists.
- **Evidence:** arXiv 2604.23629 (assetization bottleneck); arXiv 2509.12815 (PolyGen);
  art bible §3 and §5. Test to run: one prop class, 10–35 assets, measured cleanup minutes
  vs the 30-minute rule, one paid Meshy Pro month (~$20 / 1,000 credits ≈ 35–50 assets).
- **Reverses if:** that measurement shows cleanup cost below 30 min at our poly budgets
  **and** the facet-read assertion passes. Both, not either.

---

### DEC-0017 — "The generator is reviewed code the agent invokes; the agent does not improvise Blender code" (2026-10-01)

- **Area:** code design
- **Decision:** Blender-side generation lives in a checked-in, human-reviewed script
  driven by a declarative spec. The agent runs it and reports deltas; it does not author
  fresh `bpy` per run.
- **Rationale:** LLM-authored `bpy` is improvised — different code each run, no grouped
  undo, no output schema. That makes runs non-reproducible and unreviewable, which is
  precisely the property that lets an unattended agent do useful work. Seeded
  determinism is the property worth buying. This converts the task from "agent writes
  Blender code" to "agent runs a parameterised generator and reports what changed".
- **Evidence:** architectural pattern corroborated by `mcp-blender-agent`'s stated
  problem (README only, not audited); determinism requirement corroborated by Ubisoft's
  procedural pipeline (GDC 2018, *"the generation needs to yield the same result given
  the same inputs"*).
- **Reverses if:** n/a — this is a correctness property for unattended operation.

---

### DEC-0018 — "The pre-import gate fails closed on name, scale, budget, facet read, master, and tier" (2026-10-01)

- **Area:** architecture
- **Decision:** No mesh reaches `Content/` without passing six assertions: name allocated
  from `MVP_EXPORT_MANIFEST.md` (never invented, one writer, serialized); measured bbox
  height within per-class tolerance with pivot Z == 0; per-class poly budget; **visible
  planar facets still present under a hard-shaded master**; one of the ten masters only,
  generated textures inadmissible; paid tier confirmed.
- **Rationale:** Each of the seven known batch failure modes from the research maps to
  exactly one of these. The facet-read check is the one that cannot be inferred from a
  file listing — it is the only assertion that catches the failure mode the art bible
  calls *"the wrong kind of beauty"* (§1), and it is the reason texture generation must
  be off for Layer A structure.
- **Evidence:** art bible §1, §7, §10; Docs/20 §4; research §3 and §6.
- **Reverses if:** n/a — these are correctness gates.

---

### DEC-0019 — "The spec reader measures and reports; it does not place primitives over authored geometry" (2026-10-01)

- **Area:** architecture
- **Decision:** `graybox_spec_reader.py` is read-only by default. `place_missing=True`
  is check-before-create and **never overwrites** an existing object. The reader
  verifies the live blend against `Lib/01_Homestead/*.json` and emits a report.
- **Rationale:** The handoff asked for a reader that "emits placed primitives into
  Blender". Taken literally that would overwrite authored work — the blend holds a
  1680-tri cabin, 864/648/540-tri cliff assemblies and 472-tri pines, all exported
  and in `MVP_EXPORT_MANIFEST.md`. Rejected because asset policy is
  create-if-missing / update-in-place, and because greyboxing is the *output* of the
  pipeline, not its input: replacing modelled geometry with cubes discards the
  refinement the spec is supposed to support (criterion 3).
- **Evidence:** `AssetCreation/Exports/MVP_EXPORT_MANIFEST.md` tris per asset;
  live measurement of `blender/floating_island_homestead_LIB.blend`;
  AGENTS.md "Automation preserves existing content".
- **Reverses if:** a future spec *is* the geometry — i.e. a greybox class that has
  no authored master at all. Then placement becomes the only way to build it, and
  should be a separate explicit mode rather than this script's default.

---

### DEC-0020 — "Two spec sources stay: the five JSON specs and the GRAYBOX_LAYOUT table, parsed not rewritten" (2026-10-01)

- **Area:** architecture
- **Decision:** Read layout data from both `Lib/01_Homestead/*.json` (5 specs, rich
  schema) and the `GRAYBOX_LAYOUT.md` table (39 volumes). Do **not** rewrite
  `GRAYBOX_LAYOUT.md` into a new JSON canon file.
- **Rationale:** The JSON specs are the better schema and already exist; converting
  them into markdown would lose `separate_from`, `rejects[]`, `sockets[]` and
  `graybox_map[]`. The 39-volume table is cited by `CAM_Hero.md`, the PA-C tranche
  handoffs and the taste gates, so forking it into a machine file creates a second
  source that must be kept in sync — the exact failure mode `place_vs_mvp_pa_d.py`
  already demonstrates. Rejected alternative: "generate the .md from a JSON canon".
- **Evidence:** `Lib/01_Homestead/KIT_README.md`; `Lib/00_Core/CAM_HERO.md`
  references; `Content/Python/place_vs_mvp_pa_d.py:23` (spec in a comment, values
  hardcoded).
- **Reverses if:** the layout grows a field that cannot survive a markdown table, or
  a third consumer needs the 39 volumes and the table stops being authoritative.

---

### DEC-0021 — "Family assignment is an explicit table with a reported-unassigned state, not keyword inference" (2026-10-01)

- **Area:** code design
- **Decision:** `VOLUME_FAMILY_MAP` maps volume name → family explicitly.
  Unmapped volumes get `family_status == "unassigned"` and are **excluded from the
  assertion while still being reported**. Never silently treated as passing.
- **Rationale:** First implementation inferred families by substring-matching the
  Role column. It returned `spine` for all 29 spec volumes, which zeroed the
  collision assertion's input — a check that passes because its input was empty is
  more dangerous than no check, because it reports a green result. An explicit
  table is also reviewable: the Lead can audit every assignment on one screen
  rather than trusting a regex.
- **Evidence:** measured first run — `volumes_assertable: 0` despite 29 volumes;
  4 of 7 families absent from the layout entirely (see the coverage gap in
  `TASTE_GATE_GRAYBOX_SILHOUETTE.md`).
- **Reverses if:** volume count grows past the point where a table is unmaintainable
  *and* family assignment becomes derivable from a canon field (i.e. the specs grow
  a `family` key — the handoff's suggestion). Then read the field instead.

---

### DEC-0022 — "Silhouette distinctness is measured by band + openness, not aspect ratio alone" (2026-10-01)

- **Area:** architecture
- **Decision:** The collision assertion compares **verticality band** first, then
  aspect within `ASPECT_TOLERANCE`, and uses estimated **openness** to downgrade a
  collision from `blocking` to `warn`. Aspect ratio is reported as a cheap input,
  never as the verdict.
- **Rationale:** The handoff proposed "two volumes from different families may not
  share an aspect ratio within the same scale band". Aspect ratio is a *proxy for*
  silhouette and fails in both directions: a 1:1:1 pyramid and a 1:1:1 cube both
  give 1.00 and are not the same shape (this is exactly the measured
  `SM_Cabin` vs `SM_PineValley_Block_A` defect), while two unmistakably different
  flat plates at 0.05 and 0.06 would false-positive. Band-first also encodes the
  locked signatures directly — spirit is tall, gather is flat — so a violation of
  the taste gate is caught rather than merely flagged. Openness exists because one
  locked signature is "tall thin vertical **with a see-through gap**", and no pure
  proportion metric can see a gap.
- **Evidence:** `homeworld_graybox_silhouette.py`; measured collision
  `SM_BeastPad_01` (nurture, aspect 0.05) vs `SM_SpiritWound_01` (spirit, aspect
  0.17), both flat band.
- **Reverses if:** a measured eye threshold replaces `ASPECT_TOLERANCE`. Until then
  this is a **house standard with no cited basis** — the report says so on its face,
  and a collision is a prompt to look, not proof of a defect.
