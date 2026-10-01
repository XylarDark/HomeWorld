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
npm run rules:score:test       # 12 unit tests, no scorer required
npm run rules:score -- --json Saved/rules_score.json --strict
```

### Result — 31/31 scored, 0 unscored

| Metric | Value |
|---|---|
| Mean | **87.3** (range 79.5–91.5) |
| Grade A | 4 (`09b-mcp-utility-scripts` 91.5, `11-parallel-plugin` 91.5, `00-core-principles` 91.0, `15-shell-scripts` 90.2) |
| Below 80 | **1** — `19-automation-cycle.mdc` (79.5, C) |
| Mean + declared format offset | ~90.8 |

**The single C-grade is the WAVE F tombstone** — 12 lines that exist precisely
to be short and redirect to `swarm/SWARM_OPS.md`. The scorer penalizes it for
having "very little content (15 lines)". That is a **false signal for the
tombstone class**: a well-formed tombstone is short on purpose, and no
structural gate can tell that apart from under-writing. This is the same
correctness gap as ρ = 0.14 in arXiv 2608.20614, observed directly in our own
corpus.

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

### Real defect found and fixed

`16-feature-debug-instrumentation.mdc` was missing `name:`, `priority:` and
`version:` — the only rule of 31 without them, so it was unaddressable by name.
Added. Verified `priority` is decorative (nothing reads it; values mirror the
filename number), so adding it changes no load order.

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

## Gates

| Gate | Result |
|---|---|
| `npm run rules:score:test` | **12/12 pass** |
| `bash scripts/verify-userharness-submodule.sh` | exit 0 |
| `npm run preflight:ue:test` | 5/5 pass |
| `npm run preflight:ue -- --skip-mcp --assets-only` | repo + assets + JSON PASS |
| `.github/workflows/` | **not modified** |

## Still open

- **No Skill Lift number.** Tier 3 needs Docker (absent) and a paid provider
  key (unset). Tiers 1–2 only. Unchanged from HR4-A.
- **Tombstones are structurally penalized.** A future gate should exempt rules
  whose description declares `QUARANTINE`/`HISTORICAL`/`RETIRED`, rather than
  leaving every future run to explain the same false signal.
- **Structural score is not value.** ρ = 0.14 still stands; this corpus is
  healthy on form, which says nothing about whether the rules help.

## Sources

- arXiv 2608.20614 — <https://arxiv.org/abs/2608.20614>
- NVIDIA SkillEvaluator — <https://github.com/NVIDIA/SkillEvaluator>
- OpenCode, *Permissions* (wildcards, home expansion, external directories) — <https://opencode.ai/docs/permissions/>
- [PIN_SYNC_POLICY.md](PIN_SYNC_POLICY.md) · [NAMING_CONTRACT.md](NAMING_CONTRACT.md)