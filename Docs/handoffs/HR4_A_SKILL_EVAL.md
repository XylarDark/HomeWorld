# HR4-A — Skill evaluation baseline and harness measurement

| Field | Value |
|-------|-------|
| **Date** | 2026-09-30 |
| **Phase** | HR4-A · harness/bot (Lead lock 2026-09-27: horizon = harness only) |
| **Scope** | Measure whether the agent harness actually helps. Read-only measurement plus one new rule. |
| **Tool** | NVIDIA `skillevaluator` 0.3.0, Apache-2.0, installed via `uv tool install` (machine-local; **not** added to `package.json`) |

---

## Why this exists

The P0–P4 trim optimised the harness by **bytes**: always-on context
34,974 → 23,735 B (−32%), corpus 96,505 → 87,725 B (−9%), broken links 0. Those
are the wrong numbers.

> *"scan-only gates surface useful authoring issues but measure complementary
> facets (structural versus LLM-judge Spearman ρ = 0.14)"*
> — arXiv **2608.20614**, *Evaluating Skills, Not Just Agents* (Agent Skills '26
> / KDD 2026 Workshop), 947 scored paired cases across 4 harnesses

ρ = 0.14 means a structural measurement is close to uninformative about whether a
rule helps. The same paper reports mean **Skill Lift 0.2134** composite /
0.1799 outcome-only, positive in 72.8% of paired cases, with only **58 of 64**
production skills showing measurable value. A harness with 59 artifacts has not
been asked which of them earn their place.

---

## What was actually run

**Tier 1 `quality-check`, keyless, no LLM provider, no Docker.** Scored
correctness 35% / discoverability 25% / reliability 25% / efficiency 15%.

| Population | Count | Result |
|---|---|---|
| `SKILL.md` artifacts (`.agents/skills`, `.agents/skills-extras`, `.cursor/skills`) | 28 | 28 scored, **mean 84.5**, range 79.8–88.5 |
| `.cursor/rules/*.mdc` | 31 | **FAIL — not scoreable.** See below. |

Lowest scores: `architecture-trade-offs-design-depth` **79.8 (C)** — the vendored
DET blob, cite-only, not ours to edit; `taste-gate` / `taste-profiler` extras
pointers 80.2; `ue57-api-check` 80.2. None below 80 except the vendored blob.

### Tier 2 (deduplication) — run structurally, no embeddings

Tier 2 needs a provider key for embeddings, so the duplicate question was
answered by hashing instead. Result:

| Pair | Verdict |
|---|---|
| `.cursor/skills/scope-refinement` vs `.agents/skills-extras/scope-refinement` | **Byte-identical, 1,960 B, same SHA-256** — a true duplicate |
| `.agents/skills-extras/taste-gate` (389 B) vs `.agents/skills/taste-gate` (4,046 B) | Not a duplicate — deliberate pointer stub, cites canonical |
| `.agents/skills-extras/taste-profiler` (341 B) vs core (2,439 B) | Same — deliberate pointer stub |
| `architecture-tradeoffs` (2,223 B) vs `architecture-trade-offs-design-depth` (28,783 B) | Deliberate two-tier split, "do not load together" |

The pointer stubs carry the note *"prior extras copy had drifted"* — the dedup
class P4 fixed by hand is already handled correctly. **The single real duplicate
is the untracked `scope-refinement` pair, which is uncommitted user work. Left
untouched; reported to the Lead.**

### Tier 3 (Skill Lift) — NOT RUN

Requires Docker (not installed) and a paid provider key (none set). **No Skill
Lift number exists for this harness.** Recorded as an open item, not as a pass.

---

## Finding 1 — the `.mdc` corpus is unmeasurable by the leading tool

```
$ skillevaluator quality-check .cursor/rules
QUALITY | FAIL | 1 errors
```

An Agent Skill is a directory containing `SKILL.md`. A Cursor rule is a
`.mdc` file with different frontmatter. The 31 `.cursor/rules/*.mdc`
(83,464 B) therefore cannot be scored at all.

This is the uncomfortable one: the always-on surface is `AGENTS.md` (23,733 B),
which *is* covered by the harness's own discipline, but the **next-largest
instruction surface in the repo is outside the industry's evaluation tool.**
Closing that gap means either converting rules to Agent Skills or writing a
scorer for the `.mdc` format. Both are larger than this phase.

## Finding 2 — `alwaysApply` cardinality stays at 0

All 31 rules are `alwaysApply: false`. A naive grep returns **4 hits for
`alwaysApply: true`** — all four are prose inside tombstones reading *"This rule
**was** `alwaysApply: true`"*. The grep is wrong, not the repo.

Per [PIN_SYNC_POLICY.md](PIN_SYNC_POLICY.md) line 30, `alwaysApply` cardinality
is `NEVER_AUTO` and Lead-gated. **No rule was promoted or retired here.** P1 adds
a section to an existing rule; it does not create or remove one.

## Finding 3 — 22 of 259 KNOWN_ERRORS rows are one root cause

`docs/KNOWN_ERRORS.md` is 572 lines / **259 one-line entries** / 60 headers.
Clustered:

| Cluster | Rows | Status |
|---|---|---|
| Async / game-thread / yield race | **22** | **Now one rule** — see [`.cursor/rules/09-mcp-workflow.mdc`](../../.cursor/rules/09-mcp-workflow.mdc) § The game-thread rule |
| MCP tool-surface limits | 49 | Genuine, mostly irreducible (tool API gaps) |
| PCG no-access / graph limits | 37 | Genuine; matches external finding that agents cannot build PCG graphs unaided |
| UE 5.7-era entries under a 5.8-only lock | 28 | Historical; left as dated record, not rewritten |

The 22-row cluster carried **8 distinct acronyms** — `CAP001_SETTLE_AFTER_YIELD_V1`,
`CAP001_AL_AFTER_MCP_DISCONNECT_V1`, `CAP001_FIRE_ON_SLATE_TICK_V1`,
`CAP001_FIRE_ON_POST_TICK_AFTER_YIELD_V1`, `CAP001_FIRE_ONLY_AL_READY_WIRE_V1`,
`CAP001_DARK_STILL_LIT_AIM_V1`, `CAP001_DARK_STILL_NIGHT_STACK_V2`,
`CAP001_POST_NIGHT_AL_READY_V1` — for one race condition.

Epic documents the cause directly: *"executing Tool invocations on the game
thread serially, meaning clients should not issue overlapping Tool calls"* and
**Live Coding does not propagate new `UFUNCTION` declarations** (which is why
`Safe-Build` stays mandatory rather than stylistic). One rule now carries the
invariant; the 22 dated rows stay as the evidence trail, per the Lead's
2026-09-22 token-lean format decision.

---

## Explicitly not done

- **No Skill Lift measured.** Docker absent, no provider key. Tiers 1–2 only.
- **No `.mdc` → Agent Skills migration.** Larger than this phase, and it would
  change how rules are discovered.
- **No `alwaysApply` change** — Lead-gated by policy.
- **No user untracked work touched** (`scope-refinement` pair, 40 untracked
  files, dirty `UserHarness` submodule).

## Sources

- arXiv 2608.20614 — <https://arxiv.org/abs/2608.20614>
- NVIDIA SkillEvaluator — <https://github.com/NVIDIA/SkillEvaluator>
- Epic, *Unreal MCP in Unreal Editor* (UE 5.8, Experimental) — <https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-mcp-in-unreal-editor>
- Puget Systems, *Unreal Engine MCP Hands-On* (2026-07-09)
- NVIDIA, *Reliable AI Coding for Unreal Engine* (2026-03-10)

See [U58F_F_MCP_DECISION.md](U58F_F_MCP_DECISION.md) for the MCP server decision
this measurement did **not** overturn.
