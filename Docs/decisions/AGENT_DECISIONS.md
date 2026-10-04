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

---

### DEC-0023 — "Zone type is one enum keyed to the seven families; the shipped biome/alignment enums are not deleted" (2026-10-01)

- **Area:** architecture
- **Decision:** Add a single zone-type enum keyed to the seven mechanic families
  (gather, nurture_tame, heal, spirit, stealth, build_place, combat) as the
  vocabulary for art and level design. **Do not delete or repurpose
  `EBiomeType` or `EPlanetoidAlignment`** — they stay, demoted to terrain
  dressing / weather inputs. `EPlanetoidAlignment` is explicitly not a zone type.
- **Rationale:** `TG-ZONE-VOCABULARY` Q2 (Lead, 2026-10-01) settled that the
  mechanic family is the zone type. `HomeWorldPlanetoidTypes.h` already ships a
  4-biome × 3-alignment pair that predates the taste decision by seven months and
  is referenced from `docs/CONSOLE_COMMANDS.md`, `HomeWorldGameMode.h` and
  `PLANETOID_BIOMES.md`. Deleting them would break working console commands and
  re-litigate a settled product fork; overloading them would make a biome look
  like a mechanic, which is the exact confusion the Lead's answer removed. A new
  enum keeps the two axes separable at the type level instead of by convention.
- **Rejected:** reusing `EBiomeType` as the zone type (re-opens fork A, breaks
  "one family per section" — the Lead rejected paired families twice in Round 4);
  modelling family as a tag/soft-reference (keeps the ambiguity the gate closed);
  deleting the old enums as "wrong" (they are still correct for terrain).
- **Evidence:** `HomeWorldPlanetoidTypes.h`; `HomeWorldGameMode.h:239-259`;
  `docs/CONSOLE_COMMANDS.md:217-218`; `TASTE_GATE_ZONE_VOCABULARY.md` § Settled.
- **Reverses if:** the Lead later decides biomes *are* sections, which re-opens
  fork A and would make this enum redundant rather than wrong.

---

### DEC-0024 — "The env-art prototype is a new Lib/02_Zones kit, not an edit to the homestead kit" (2026-10-01)

- **Area:** architecture
- **Decision:** The authorised env-art prototype lands in a **new
  `Lib/02_Zones/<FAMILY>/` kit** with its own spec JSON, reusing the loader in
  `homeworld_graybox_spec.py`. It does not add volumes to `Lib/01_Homestead/`.
- **Rationale:** `TG-ZONE-VOCABULARY` Q1 authorised exactly one zone for one
  mechanic family. Homestead is `build_place` and is already at its greybox
  ceiling — the report has 7 blocking findings there. Writing the new family's
  volumes into the homestead kit would mix two families in one directory, which
  is the vocabulary collision the gate just resolved, and would make the
  collision assertion unable to tell them apart. One directory per family makes
  "one family per section" a property of the file tree rather than a convention.
- **Evidence:** `docs/qa/GRAYBOX_SPEC_REPORT.md` (7 blocking, homestead);
  `homeworld_graybox_spec.py` resolves spec dirs by path and needs no change to
  accept a sibling.
- **Reverses if:** a family genuinely spans regions rather than sections — e.g.
  the spirit shrines exist on both homestead and planet-side, which is already
  true and is handled by `SM_Shrine_Homestead` / `SM_Shrine_Return` sharing one
  family across two kits rather than by merging directories.

---

### DEC-0025 — "A child part is placed at its assembly origin, never at world zero" (2026-10-02)

- **Area:** code design
- **Decision:** `place()` resolves a part's location from `origin_is_explicit`,
  else `assembly_origin`, else `volume.origin`. A part that inherits its assembly's
  origin is never placed at `(0,0,0)`.
- **Rationale:** The first version read `volume.origin` directly. For every module
  that inherits its assembly origin — which is most of them, because
  `CABIN_MODULES` and the zone props name sub-modules without restating positions —
  that value *is* the zero vector. Placing the kettle put its body and handle at
  world origin while the spec said `(-4.5, 3.2, 0)`.
- **Evidence:** the verifier caught it rather than the build. `place=True` reported
  `SM_Kettle_Body: child module sits outside assembly 'None' footprint (module at
  0.000, 0.000; assembly centre -4.500, 3.200)`. Three props, three false
  findings, one root cause.
- **Reverses if:** a spec gives a part its own offset relative to the assembly
  (e.g. a porch post 1.3 m forward of the cabin centre). Then the offset is
  meaningful and should be added to the assembly origin rather than replacing it.

---

### DEC-0026 — "A family signature is asserted against the assembly read, not against each part" (2026-10-02)

- **Area:** architecture
- **Decision:** Only synthesised **assembly reads** are assertable. Individual
  parts are still measured, budgeted and master-checked, but are not held to a
  zone-level proportion.
- **Rationale:** A locked signature is a statement about how a **place** reads at
  20 m — *narrow upright, single soft column*. Asserting it against a kettle
  handle produced three false findings, because a handle is not supposed to be a
  "flat square plate". The original collision check was measuring bolts and
  firing on them. The assembly bounding volume is the unit that actually faces
  the player.
- **Rejected:** (a) keep asserting parts and add a per-part exception list — that
  is an unbounded list of apologias for a wrong unit; (b) drop the assertion for
  props entirely — the props are exactly where the families first appear, so
  dropping them would leave `heal` and `stealth` with no check at all.
- **Evidence:** authoring `NODE_KETTLE`, `NODE_RUNE`, `NODE_PLANT_SLOT` — three
  parts across three families, three false `4_distinct` findings, one root cause.
  Pinned by `test_a_part_is_measured_but_not_held_to_a_zone_proportion`.
- **Reverses if:** a future family is defined by a *part* rather than a whole —
  e.g. a shrine defined by its lintel alone. Then part-level assertion returns for
  that family specifically.

---

### DEC-0033 "Re-point the harness at the game, not at the agent tooling" (2026-10-01)

- **Area:** harness architecture — the governing decision for all harness work
- **Context change:** The harness is now explicitly tuned for **one human developer running multiple
  agents, working on game design with C++ in Unreal Engine 5.8.** That reframe was not assumed when
  the harness was built.
- **Decision:** Harness effort goes to (1) proving the game compiles, (2) proving the game runs,
  (3) protecting taste boundaries, and (4) minimising one person's review cost. Self-measurement
  of the agent harness is frozen, not extended.

- **Evidence gathered 2026-10-01 (the audit that forced this):**
  - The JS harness is 7,517 LOC against 45,109 LOC of product C++/Python.
  - **All 11 npm test scripts test harness tooling. Not one tests the product.**
  - **Zero `IMPLEMENT_SIMPLE_AUTOMATION_TEST` macros exist in `Source/`.** There are no C++ tests
    to run, so "it compiles" is currently the only automated fact about the game.
  - `ci.yml` proves compilation only. `validate.yml` runs `npm run test:all`, which is
    self-referential.
  - The working build/test entry points (`Tools/Safe-Build.ps1`, `Tools/RunTests.ps1`) are
    PowerShell outside the npm harness, so the documented and the verified path are different paths.
  - 24 of 32 commits on the branch were harness work; the product did not move.
  - The evaluation harness (`task-lift.js`) has produced **zero** product decisions, and its
    readings change sign depending on which model runs it (R4: with-arm leads 0.75 vs 0.65;
    R5: with-arm trails 0.314 vs 0.556). It measures harness-x-model interaction, not the harness.
  - `decisions:check` was red for 14 commits and caught nothing.

- **Rationale:** For a one-person team the binding constraint is **review attention**, not agent
  throughput. A solo dev has a few hours of real review a day. Gates that cost attention are a tax
  on the scarcest resource in the company, and gates that cannot fail are worse than no gate. A
  harness that watches the watchers while never compiling the game is inverted relative to need.

- **Rejected:**
  - Extending `task-lift.js` (R6, more trials, cost accounting). It has answered its question:
    *this benchmark did not detect an effect.* More precision cannot rescue an instrument whose
    reading flips with the model.
  - Growing the rules/skills corpus for its own sake. Agent context is a commodity; a de-facto
    cross-tool standard exists and we over-invested in managing it locally.
  - Keeping `decisions:check` strict. Same-commit enforcement is an idealisation that penalises
    exactly the batching a solo dev already has to do. Recorded as a deliberate relaxation with
    the failure mode stated: a boundary change can now ship without its reasoning, and that is
    accepted because the alternative produced 100% friction and 0% findings.

- **Target harness shape (what to build, in priority order):**
  1. **One command that proves the game is real.** Wire `Tools/Safe-Build.ps1` and
     `Tools/RunTests.ps1` into `npm run verify`, so build truth lives where gates are read.
  2. **First C++ automation tests.** Until `Source/` contains at least one
     `IMPLEMENT_SIMPLE_AUTOMATION_TEST`, no harness can assert anything about behaviour.
     Start with things a solo dev would otherwise check by hand after every agent change.
  3. **UE Editor ownership lock.** With multiple agents, only one may drive the Editor at a time;
     this is a hazard with no web-dev equivalent and it is currently unguarded.
  4. **Assumption disclosure per change.** Each agent states what it invented. This is the cheapest
     possible protection for a single reviewer and it scales with agent count.
  5. **Taste-boundary enforcement stays as-is** (`docs/human-use/cursor-cannot/`, taste gates).
     It is the highest-value part of the existing harness because it is the only thing standing
     between agent initiative and unrequested game design.

- **Reverses if:** the team grows past a point where one person is no longer the integration
  bottleneck, or the evaluation harness produces a decision that changes what the team builds.
  The second is the real test of this decision and it has not happened yet.
- **Consequence:** `Docs/qa/HARNESS_REFINEMENT_TASKS.md` R5/R6 are superseded by this entry and
  should not be started.

---

### DEC-0034 "Correction to DEC-0033: the sign-flip is the EXPECTED result, not evidence of a broken harness" (2026-10-01)

- **Area:** harness — corrects the inference in DEC-0033
- **Why this entry exists:** DEC-0033 concluded that because `task-lift.js` readings flip sign
  depending on which model runs them, the instrument may be "measuring harness-x-model
  interaction" rather than the harness. **That inference was wrong, and it was mine.** It is
  corrected here rather than left standing, because a wrong decision left in the log is worse
  than no decision.

- **The evidence that corrects it (VERIFIED from the paper):**
  *"Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?"*
  Gloaugen, Muendler, Mueller, Raychev, Vechev. arXiv **2602.11988** (v3 2026-09-29),
  ICLR 2026 Workshop on Memory for LLM-Based Agentic Systems, ETH Zurich + LogicStar.ai.
  Code: `eth-sri/agentbench`, MIT.

  | Condition | Task success | Steps | Cost |
  |---|---|---|---|
  | LLM-generated context file | **-3%** (marginal negative) | +2.45 to +3.92 | **+20% / +23%** |
  | Developer-written context file | **+4%** (marginal positive) | +3.34 | up to +19% |

  **The mechanism is the part that matters:** instructions in context files **are followed**.
  Repo-specific tooling was used **1.6x/instance when mentioned vs <0.01x when not mentioned**;
  repo tools **2.5x vs <0.05x**. Context files reliably increase steps and cost, and reliably
  get followed. What they do **not** reliably do is move a binary task-success metric.
  Their own recommendation is to omit LLM-generated context files and include only minimal
  requirements (e.g. specific tooling to use).

- **Reinterpretation of our own data:** R4 (space-bunny-free) gave with-arm 0.75 vs without 0.65.
  R5 (nemotron) gave with-arm 0.314 vs without 0.556. A sign flip between models is the
  **expected** outcome at 4 tasks x 2 conditions, not evidence the harness is broken or harmful.
  The likely cause of our instability is that **a single discordant pair flips McNemar** at
  this n — the fix is more tasks with fewer checks each, not a bigger instrument.

- **Consequence for DEC-0033:** the *cuts* stand. The *diagnosis* is corrected. DEC-0033's
  evidence list should be read with the following removed: any inference that the sign-flip
  indicates the harness measures harness-x-model interaction rather than the harness.

- **Cuts ADOPTED on this evidence (each is a deletion, not a build):**
  1. **`score-mdc-lift.js` (1,006 LOC) + `score-mdc-rules.js` (462 LOC) + their tests — DELETE.**
     Structural lint-scoring of markdown. Our own `task-lift.js` header already states these
     "measure the inputs - how good the rule text is. Neither can answer the only question that
     matters." The paper makes the general point concrete: score the behaviour, not the text.
  2. **The `decisions:check` boundary gate — DELETE the gate, keep the log file as prose.**
     An enterprise compliance control applied to a team with no auditors. It was red for 14
     commits and caught nothing.
  3. **The tombstone-retirement apparatus — DELETE.** Tombstones exist to avoid dangling
     references and accumulate only because nothing ever deletes. Let the refresh script fail
     loudly on a dangling ref instead.
  4. **`.cursor/rules/` 25 files -> 6-8.** `AGENTS.md` is now a **Linux Foundation standard**
     (Agentic AI Foundation, announced 2025-12-09; `agentsmd/agents.md`, 24.7k stars, MIT,
     60k+ projects, read by opencode/Cursor/Codex/Aider/goose and others). Keep only what is
     genuinely UE-5.8-and-HomeWorld-specific; the tech-agnostic ones belong in `AGENTS.md` or
     nowhere.
  5. **promptfoo replaces the evaluation *mechanism*; McNemar stays.** promptfoo (25.6k stars,
     MIT, ~3M npm downloads/month, now part of OpenAI) already supports `copy_working_dir: 'git'`
     (a clone of the current commit, no remote), templated `working_dir` so two rows can point
     at two pre-built worktrees, the `opencode:sdk` provider, `trajectory:*` assertions that read
     what the agent DID rather than what it says it did, and a `skill-used` assertion. That
     replaces our worktree builder, process-spawn plumbing and glob->RegExp compiler. **We keep
     McNemar and the three-arm design - promptfoo has NO statistical significance testing.**
  6. **`eth-sri/agentbench` already ran our experiment** at proper scale (3-arm true file-removal
     ablation, 4 agents, 438 instances, MIT). We do not need to re-derive their finding; we should
     cite it.

- **UE C++ testing — corrected by this research:** for pure C++ unit tests, the intended tool is
  the **Catch2-based Low-Level Test (LLT)** framework in UE5, not Automation Test Framework.
  Epic's own ATF documentation states ATF is "not ideal for pure unit testing." **Gauntlet is
  AAA-scale, requires a source build of the engine, and is overbuilt for 1-3 people** - gate it
  behind real multiplayer need. `Source/` currently contains **zero** automation tests.

- **Reverses if:** a future run at adequate n shows context files move conformance reliably in
  the positive direction. That would justify keeping the eval harness - but not the deleted
  pieces, whose arguments were never about statistical power.

---

### DEC-0035 "Not finished: the instruction corpus is 10.8x the published ceiling, and .agents/ was never audited" (2026-10-01)

- **Area:** harness — **overturns the implicit "Phase 4 is done" conclusion**
- **Trigger:** Lead asked whether this matches what solo devs actually do and whether the
  harness can now be considered complete. Research was commissioned specifically because the
  prior work had **never investigated solo-dev practice** - it inferred it from tool pricing and
  team-size reasoning. That was an argument from plausibility, not evidence.

- **Finding 1 — our instruction corpus is an order of magnitude over budget.**
  Measured on disk 2026-10-01:

  | Surface | Files | Lines |
  |---|---|---|
  | `.cursor/rules/*.mdc` | 25 | 1,088 |
  | `.agents/**` | 25 | 2,166 |
  | **Total agent instructions** | **50** | **3,254** |

  Against published ceilings: HumanLayer's root `CLAUDE.md` is **under 60 lines** with a
  consensus ceiling of **under 300**; OpenAI's `AGENTS.md` is **~100 lines** because it is a
  *table of contents* with `docs/` as the system of record; frontier models follow roughly
  **150-200 instructions**, and instruction-following **decays uniformly as count rises**, not
  only at the tail. Claude Code's own system prompt already spends ~50 of that budget.

  **We are ~10.8x the consensus ceiling.** Phase 4 stopped at 25 rules and called it done.
  It was not done. Worse, **`.agents/` (2,166 lines) was never audited at all** - the entire
  Phase 4 exercise looked only at `.cursor/rules`, which is the *smaller* of the two surfaces.

- **Finding 2 — the strongest published evidence says added instruction can be NET NEGATIVE.**
  Dan Luu, 160 runs per condition, Sept 2026: **Default (no instructions) scored above
  average**; TDD underperformed; large third-party test skills **underperformed while costing
  26-41% more**. Henry Pan, independently: harness complexity grew **55% LOC with solve count
  flat**, and rule-based harnesses trap the task model in "a policy maze". Ronacher: *"if you
  stop using it, it's a failed automation, delete it"* - and 95% of his workflow is talking to
  the machine. Boris Cherny deletes his `CLAUDE.md` every six months.

  This *supports* the Phase 1-2 deletions and it also says **we did not go far enough.**
  R5's dose-response (with 0.311 / docs-only 0.563 / without 0.667) is consistent with these
  findings rather than an anomaly.

- **Finding 3 — OpenAI tried the thing we have and published why it failed.**
  One big `AGENTS.md` failed four named ways: context crowding, **"too much guidance becomes
  non-guidance"**, instant rot, and no mechanical verifiability. Their fix is the shape we
  should adopt: `AGENTS.md` as a ~100-line index, `docs/` as the system of record, guidance
  **enforced by linters**, plus a doc-gardening agent.

- **Finding 4 — our multi-agent model may be wrong.** Cognition: writes should stay
  **single-threaded**. Simon Willison: **one significant change under review at a time**;
  parallelism is for research, PoCs and low-stakes maintenance. Christopher Meiklejohn
  documents **real data loss from migration collisions across agent worktrees**. We have been
  treating parallel agent writes as the goal; the evidence says writes serialise and only
  *research* parallelises.

- **Decision:** the harness is **NOT complete**. Continue. Three specific reductions remain,
  each evidence-backed rather than taste-led:
  1. **`.agents/` audit** - 2,166 lines, never examined, larger than the corpus we trimmed.
  2. **Fold `.cursor/rules/` toward the ceiling** - target `AGENTS.md` ~100 lines and a total
     always-reachable instruction surface under 300 lines. Move detail into `docs/` (already
     the canon) and enforce the invariants that matter with deterministic checks instead of
     prose. "Claude is not a linter": style and formatting rules belong in tools, not prompts.
  3. **Adopt the six-month deletion rhythm** Cherny uses, promoted from my kill rule to a
     scheduled event.

- **Rejected:** declaring the harness complete. Four of the five completion criteria in
  Docs/36 are met, but criterion 1 - "every category solo devs report using is present" -
  cannot be asserted while a whole instruction surface is unaudited, and criterion 2 -
  "nothing we have is doing nothing" - fails for 3,254 lines of instructions against a 300-line
  ceiling.

- **Honest caveat:** no published harness-to-product-code ratio from solo developers exists.
  I searched and did not find one, so our 4,250 LOC cannot be benchmarked against a number. The
  instruction-budget findings above are the strongest available proxy and they are unambiguous.

- **Reverses if:** measurement at adequate n shows the corpus size is not the constraint. That
  is testable, and Dan Luu's result is the strongest prior against us being right - but it is a
  prior from *other* tasks, not from HomeWorld.

---

## DEC-0027 - The camp is at a FIXED position, hidden by the treeline, not randomly placed

**Date:** 2026-10-02
**Decided by:** agent
**Surface:** level design / quest flow

**Decision.** The camp sits at one authored location at the forest edge. The treeline blocks the
sightline until the player is roughly 15 m out, so it is discovered on approach rather than
revealed by luck. A rune prerequisite gates the day-take event.

**Rejected:**
- *Random placement at the treeline* - maximum surprise, and it produces an **unwinnable
  save**. The day event (companion taken, ejected) is scripted and not reversible. A player who
  finds the camp at minute two, before knowing the rune exists or that spirit form needs bed
  AND rune, has lost the loved one with no route to recovering them. It is also ungateable: with
  no authored position there is nothing to gate against.
- *Pre-placed and plainly visible* - kills the discovery the Lead asked for and makes the camp a
  waypoint from minute one.

**Why this is agent-owned rather than a taste gate.** Level design and placement are normally the
human's, and `docs/human-use/OWNERSHIP.md` says so. This one is decided here because the
constraint that settles it is engineering, not preference: an irreversible scripted event at an
authored location can be made safe, and at a random location it cannot. Recording it here with
the reasoning attached so it can be vetoed on the record rather than absorbed silently.

**Does not decide:** the treeline's exact density, how far back the sightline is cut, and
whether the camp is visible from the field at night. Those remain `2B-1` and taste.

**Reverses if:** the world gains a save-scumming or fast-travel system that lets the player
recover a missed camp, which would remove the dead-save argument entirely.
---

## DEC-0028 - The camp forest is CHOSEN by the player, not fixed, not random

**Date:** 2026-10-02
**Decided by:** agent, from a Lead instruction
**Surface:** level design / quest flow
**Supersedes:** DEC-0027's placement method only. Its reasoning survives - see below.

**Decision.** The field has four edges: a cliff (boundary, scenic), a river (future path), and
two pine forests. **Entering either forest commits to it and the camp generates there.** The
forest not chosen becomes a future path, eventually leading to an area like the river.

**What survives from DEC-0027.** The whole argument was that a random climax cannot be gated,
because the day event (companion taken, ejected) is scripted and irreversible. **That still
holds** - and this answer satisfies it rather than avoiding it: the moment of choice is the
player walking into a treeline, which is an authored, deterministic moment. It is gateable
because the player makes it, not because the map did.

**Why this is better than both things I originally offered:**

- It keeps **player agency**. DEC-0027 had the player discovering a fixed place. Here they pick,
  and the picking is the discovery.
- It keeps **determinism after the choice**, so the rune can gate the day event and the dead-save
  problem stays solved.
- It adds a **second future** the player can see they gave up. The unchosen forest is a road they
  did not take, which makes the choice feel like it cost something rather than being a formality.

**THE HARD CONSTRAINT, and the reason this is not the lead's to answer casually:** both forest
edges must look **identical** from inside the field - same density, height, opacity, silhouette.
If one looks fuller, darker or more inviting, the choice stops being a choice and becomes a
puzzle with a correct answer. Players will optimise instead of choose, and the whole thing
becomes a test - which is the opposite of what V2b ("gather by day, tend by night") is for.

**Rejected:** *cliff as a candidate edge* - it is a boundary and has no forest on it.

**Does not decide:** forest density, how far back the sightline is cut, whether the cliff reads
as safe or dangerous. Those stay in the image prompts and are the Lead's.
---

## DEC-0029 - The operative vision is `VISION_BOARD.md`; `00_CANON.md` + `canon/` are superseded FOR PROTOTYPE SCOPE

**This records a decision the Lead already made on 2026-10-02. It does not take a new one.**

Asked "do we have a single source of truth for the canon", the honest finding was that the
*substance* is singular but nothing says so, so it reads as three. Three documents declare
themselves authoritative over the same question, and the newest one never names the ones it
replaces:

| Document | Declares | Last touched |
| --- | --- | --- |
| `Docs/00_CANON.md` | `Status: LOCKED (P0)` | pre-T0 |
| `Docs/canon/*.md` (12 files) | `Status: LOCKED` | 2026-09-21 |
| `Docs/VISION_BOARD.md` | `CANON for product work` | 2026-10-02 |

`Docs/canon/README.md:3` names `00_CANON.md` and `01_GDD_MVP.md` as the "long sources of truth"
and `canon/` points at nothing else. `VISION_BOARD.md` never once mentions `00_CANON.md` or
`canon/`. So the supersession is real but **unrecorded**, which means every new reader has to
rediscover it - and a reader who starts at `canon/README.md` lands on the September vision and
never learns it is stale.

**The decision:** for prototype scope, `VISION_BOARD.md` (V2b, gather by day / tend by night) is
the operative vision. `00_CANON.md`, `canon/*` and `01_GDD_MVP.md` remain valid as **Act 2+
background** - they are not wrong, they are simply describing a different, earlier cut, and
VISION_BOARD §2 already defers the family/rescue/ruin text there on purpose.

**Substantively the two agree on the axis**, which is why this was survivable rather than
loudly broken: both put gathering in the day and tending/nurturing in the night, both forbid
kill-combat and require convert-not-kill, both keep the homestead non-combat. What changed is
*who you are* - and there the old set is wrong in one specific, load-bearing line:

> `Docs/canon/FANTASY.md:14` - `| Player | Family co-op caretaker (body by day, spirit by night) |`

VISION_BOARD §1 (Lead, 2026-10-02) says *"You are **alone** and you have **lost something**"*, and
V1b adds **one** companion who is rescued - Q16/Q18/Q19/Q20 settled on one NPC. So `FANTASY.md` is
the only sentence in the set that names the protagonist, and it names the wrong one. It also
contradicts its own sibling `canon/DO_NOT.md:30`, which drops co-op for "NPC family".

**Not decided here, and deliberately so:** I did not edit `FANTASY.md`, `canon/*` or
`00_CANON.md`. All three are Lead-LOCKED, and "who the player is" is product framing, which the
ownership map above puts on the **human**. The one-line contradiction is escalated instead. What
the agent can own - and does - is that the supersession is now written down, plus
`Docs/CANON_MAP.md` as the entry point that names it.

**Why this is a doc problem and not a taste problem:** the vision was never ambiguous. It was
invisible from two of its three doors.

## DEC-0030 - A blocked gate row must name an executable next action

**Decision:** every non-PASS check in `polish_readiness.py` now carries a `next_action`
field, separate from its `note`, and a test (`BlockedRowsMustNameAnAction`) fails if any
substantive blocked row leaves it empty. The rendered markdown gains a **"What to do"**
table per gate.

**Why.** On 2026-10-04, 6 of the 8 substantive blocked rows stated a finding and no next
step. Reading them told you what was wrong and nothing about what to do about it. A gate
that only ever complains is a mood, not a work list.

**Why a separate field and not better prose.** `note` answers *why is this row the state it
is*, and "the manifest disagrees with disk" is a complete diagnosis - the action is a
different sentence. Keeping them in one blob is how the action got lost in the first place,
and a structural field with a test on it cannot drift back.

**Deliberately not required of:** PASS rows (there is nothing to do) and `dep.` rollups (a
gate-level summary naming its own actions would duplicate its children). A PASS carrying an
action is noise, and there is a test for that direction too.

**This is the "never idle" commitment made checkable.** `docs/human-use/OWNERSHIP.md`
already says the agent is always working, asking, or pointing at the next step. This makes
the third of those three measurable on every gate run instead of a property of how the
agent happens to be feeling that day.

**Not decided here:** the `ALLOWED_EMPTY` escape hatch is an empty set. It exists so that
"agent-owned and unfinished" can be declared deliberately later, and it is deliberately
empty today - nothing is exempt.

## DEC-0031 - Close the fail-opens in the export chain; do NOT add a severity ladder

**Decision, part 1.** An adversarial review of the two gate rows added on 2026-10-04 found
**six ways to turn them green without measuring anything**. All six are closed, each with a
test that fails if the hole reopens (178 -> 200 tests). The two that mattered most:

- `max(off_x, off_y)` discarded a NaN in the Y slot and reported **PASS**, with "off by nan"
  in its own note. `max` returns its first argument whenever the second is not greater, and
  `NaN > x` is always False - so the verdict depended on argument order.
- The check compared Blender's **object-space** box against Unreal's **world-space** AABB.
  Those disagree on any rotated actor, so it would have reported FAIL on a correctly placed
  island. Wrong by construction, not by tolerance; widening the tolerance would have hidden
  it rather than fixed it.

**Decision, part 2 - the restraint, which is the point.** The same research that prompted
this review says mature content-validation tooling ships a new rule as a **warning** and
promotes it to an error only once it has been clean (`Docs/38_AI_AGENT_PRACTICE.md` §11.3).
We have a binary gate. Adding a WARN tier and marking `master_binding` and `family_distinct`
WARN would have made all three gates readable and **would have quietly undone the Lead's
2026-10-04 ruling** that those two rows stay RED, by another name.

**So the capability is recorded and not applied.** The Lead's decision was made knowing the
gate could not go green; a change that makes the gate go green *while appearing to honour*
that decision is exactly the "widen the ask to allow it" failure. It needs a decision of its
own, on its own merits, stated as such.

**Already satisfied, no work needed:** separating "the check failed" from "the check could not
run at all" is the substance of a severity ladder, and we have it - MISSING never passes and
`--selftest` drives the fail-open paths directly.

**Scope note.** This was agent-owned under the ownership map ("refactoring the harness - rules,
skills, scripts, scorers, CI | Agent | Decide, then log"). No gameplay number, no art
decision, and no taste call was touched. `env.traversal_measured` remains deferred to the
polish pass by the Lead, and the traversal instrument research says should be telemetry
rather than a stopwatch is recorded in `Docs/38_AI_AGENT_PRACTICE.md` §11.5 for when that
unblocks.