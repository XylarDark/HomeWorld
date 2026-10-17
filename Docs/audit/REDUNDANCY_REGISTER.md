# Redundancy register

**Purpose:** One place for measured redundancy in this repo, with evidence and a proposed fix per entry. Audit-only unless an entry says *Applied*. Scope: committed state at `HEAD` (`git ls-tree -r HEAD`), measured 2026-10-17.

**Not a delete list.** Every *Proposed* entry needs human sign-off before anything is removed. Deleting canon is a scope call, not an agent call.

**Baseline:** 3211 committed files. 1832 `Content/` (binary UE assets), 640 doc files, 197 `Source/`, 89 `.cursor/`, 64 `.agents/`, 34 `Tools/`, 16 `.codex/`, 2 `.opencode/`.

---

## R1 — doc-tree casing drift

**Status:** APPLIED 2026-10-17 (targeted)

640 doc files live in one directory; git records **485** as `Docs/…` and **155** as `docs/…`. The same folder names were split across both spellings:

| Folder | `Docs/` | `docs/` | Total |
|---|---|---|---|
| `TaskLists/` | 9 | 51 | 60 |
| `human-use/` | 1 | 20 | 21 |
| `guides/` | 2 | 3 | 5 |
| `tasks/` | 1 | 4 | 5 |

**Applied:** the 13 files sitting in folders whose declared owner is the lowercase tree were re-recorded as case-only index changes — 9 in `TaskLists/`, 2 in `guides/`, 1 in `human-use/`, 1 in `tasks/`. All landed as `R100` (100% similarity: pure case change, nothing moves on disk). Counts are now `Docs/` 474, `docs/` 168, with 0 capital-spelled files left in those four folders.

**Correction to the documented method:** `DOCS_LAYOUT.md` says to use `git update-index --cacheinfo` for a case-only change. That is not sufficient on its own — git rejects adding a path that is not already in the index (`missing --add option?`). The working sequence is `git rm --cached <old>` then `git update-index --add --cacheinfo <mode>,<hash>,<new>`. Doing only the second step leaves both spellings in the index as duplicate entries, which is worse than the original drift.

**Still open:** ~142 paths elsewhere in the tree (`handoffs/`, `art/`, `context/`, `qa/`, `canon/` and others) remain under either spelling by historical accident. Settling those is a larger diff and was deliberately not bundled here.

---

## R2 — broken and ambiguous doc links

**Status:** open (pre-existing; unrelated to R1)

`npm run docs:links` (`Content/Python/check_doc_links.py`) reports, at `HEAD`:

```
checked 549 files; repaired 0; still broken 122 (1324 more repairable with --fix)
ambiguous - several files share the name (85), not guessed
```

122 broken links and 85 basename-ambiguous links. `--fix` can repair 1324 more.

**Note:** two broken links in the always-on `AGENTS.md` were found and fixed during this audit (see R6). `AGENTS.md` is now clean under this checker. The remaining 122 are elsewhere.

**Proposed:** run `--fix`, then triage the remainder by owner. Ambiguous basename links matter most — they resolve to whatever the checker guesses.

---

## R3 — thirteen "what is next" surfaces, no pointer of record

**Status:** open

Thirteen committed docs present themselves as current or next work. Staleness by last commit:

| Tier | Files | Last commit |
|---|---|---|
| Stale (~4 weeks) | `Docs/11_NEXT_PHASE_STRATEGY.md`, `docs/workflow/MVP_AND_ROADMAP_STRATEGY.md` | 2026-09-17 |
| Stale | `Docs/26_TASTE_NEXT.md` | 2026-09-19 |
| Mid | `Docs/TaskLists/T0_ROADMAP.md` | 2026-10-01 |
| Mid | `Docs/TaskLists/T0_NEXT_QUEUE.md`, `Docs/TaskLists/T0_EXECUTION_QUEUE.md` | 2026-10-08 |
| Mid | `Docs/qa/POLISH_READINESS.md`, `docs/TaskLists/NEXT_SESSION_PROMPT.md` | 2026-10-06 |
| Fresh | `docs/TaskLists/CURRENT_TASK_LIST.md`, `docs/TaskLists/30_DAY_IMPLEMENTATION_STATUS.md`, `docs/Automation/AUTOMATION_READINESS.md` | 2026-10-13 |
| Fresh | `Docs/context/PLAY_TASKS.md` | 2026-10-14 |
| Fresh | `Docs/context/NEXT_BEATS_INTERVIEW.md` | 2026-10-15 |

No two are byte-identical, so this is **navigational** redundancy, not file duplication: an agent cannot tell which is authoritative.

**Proposed (ruled 2026-10-17):** `Docs/context/PLAY_TASKS.md` is the pointer of record — it is the freshest credible candidate, is already the doc root `AGENTS.md` names, and sits under `context/` beside `SCENE_SETUP.md` and `SESSION_START.md`. The other twelve should carry a pointer to it rather than be deleted. **Not yet fanned out** — the designation is recorded here and in `DOCS_LAYOUT.md`; adding the pointer line to all twelve files is still to do.

---

## R4 — duplicated skill trees

**Status:** APPLIED 2026-10-17

`.agents/skills/` and `.cursor/skills/` mirrored five skills as byte-identical full copies — 35 files including whole `reference/` subtrees and `metadata.json`. Four other skills already used pointer stubs ("Pointer. Read the other. Do not keep a second copy here."), so the convention existed and these five did not follow it.

**Applied:** `.agents/skills/` is the content owner. Justification: it is larger (50 skills vs 40), owns `skills-extras/`, is where this session's own skill loader resolves, and the newest UE skill (`ue58-api-check`) already resolved `.agents/` as owner.

Converted to pointers in `.cursor/skills/`: `navigating-code`, `refactoring-code`, `ue-code-authoring`, `ue-live-debugging`, `ue-test-authoring`.

**Result:** 30 files removed. Each `.cursor` skill is now a single `SKILL.md` pointer; all `.agents` trees intact; every pointer target resolves; **0 byte-identical skill pairs remain**.

**Rule now in force:** a skill's content lives in exactly one tree. The other holds an 8-line pointer. Never a second copy.

---

## R5 — agent roster maintained three times, already drifted

**Status:** tooling APPLIED 2026-10-17. Drift itself still open — see below.

The same 15-agent roster exists three ways:

| Path | Count | Form |
|---|---|---|
| `.cursor/agents/` | 15 + `README.md` | `.md` — **source of truth** |
| `swarm/agents/` | 14 | `.md` — derived, must stay byte-identical |
| `.codex/agents/` | 15 | `.toml` — derived, same content in Codex's shape |

**There was no generator.** No script under `scripts/`, `Tools/`, or `swarm/` wrote these directories, so the copies drifted silently.

**Applied:** `Tools/AgentRoles.ps1`. Read-only by default; `-Sync` regenerates the derived copies and never edits the source.

```
.\Tools\AgentRoles.ps1          # check only, exit 1 on drift
.\Tools\AgentRoles.ps1 -Sync    # regenerate derived copies
```

The check compares **normalized** content (line endings and trailing whitespace folded), so legacy formatting does not read as drift while a real edit still trips it.

**Remaining real drift — 4 files, 2 agents.** The check reported 17 problems before calibration and 4 after; the other 13 were formatting artifacts of the generator, not repo drift.

| Agent | Problem |
|---|---|
| `integration` | `swarm/agents/integration.md` and `.codex/agents/integration.toml` both differ from source — source was edited, copies never followed |
| `verifier` | `swarm/agents/verifier.md` **MISSING**; `.codex/agents/verifier.toml` differs — added to source, never propagated |

**Not yet synced, deliberately.** `-Sync` overwrites the derived copies from source, which would discard any hand-edit made directly in `swarm/` or `.codex/`. Review those two agents' diffs before running it:

```
git diff --no-index .cursor/agents/integration.md swarm/agents/integration.md
```

**Rule now in force:** `.cursor/agents/*.md` is the source of truth. `swarm/agents/*.md` and `.codex/agents/*.toml` are generated. Never hand-edit a derived copy; run `-Sync`.

---

## R6 — link casing in always-on context

**Status:** APPLIED 2026-10-17

`AGENTS.md` linked `docs/tools/Rider_MCP_for_UE_Games.md` (twice) and `docs/handoffs/MARKETPLACE_POLICY_V1.md`, but both files are recorded as `Docs/…`. They resolve on Windows and **404 on a case-sensitive clone or CI checkout** — including the doc that explains the Rider MCP tool trust matrix.

**Applied:** both links now use the casing git records. `AGENTS.md` is 18/18 links resolving, 0 defective, confirmed by the repo's own `npm run docs:links`.

---

## R7 — duplicate binary assets

**Status:** open — needs an ownership call

Byte-identical committed binaries:

- `AssetCreation/AssetDump/SM_Portal_Prototype.fbx` ≡ `AssetCreation/Exports/Gatherables/SM_Portal_Prototype.fbx`
- `AssetCreation/AssetDump/SM_Cabin_Prototype.fbx` ≡ `AssetCreation/Exports/Homestead/SM_Cabin_Prototype.fbx`
- `AssetCreation/AssetDump/SM_Flowers_Prototype.fbx` ≡ `AssetCreation/Exports/Gatherables/SM_Flowers_Prototype.fbx`
- Five identical `khronos_box_*.glb` placeholders across `AssetCreation/Exports/*/`

**Proposed:** decide whether `AssetDump/` is a staging area or an owned location. If staging, it should not be committed. The `khronos_box_*` files are intentional identical placeholders — de-duplicating them buys nothing.

---

## Not redundancy

- **25 `.gitkeep` files** are byte-identical by design — git cannot track an empty directory. Leave them.
- **Four skills that "diverged"** between `.agents/` and `.cursor/` are intentional pointer stubs, not conflicting copies. Verified by content: each names the other tree and says "Do not keep a second copy here." `ue58-api-check` points the opposite direction (`.cursor` → `.agents`), which is consistent with R4's ownership ruling.

---

## Verified negatives

Checked, not assumed — each of these was confirmed rather than inferred:

- `alwaysApply: false` in **all 17** `.cursor/rules/*.mdc`. The `AGENTS.md` "no `alwaysApply: true`" rule holds.
- `.cursor/rules/unreal-cpp.mdc` carries `globs: "**/*.cpp, **/*.h"`, so Cursor **does** auto-attach the C++ rules to every `.cpp`/`.h` edit. The OpenCode-vs-Cursor parity gap is real, not theoretical.
- `Docs/` and `docs/` are one directory: 4 other canon files (`CANON_MAP.md:40` and `:243`, `docs/AGENTS_REFERENCE.md:10` and `:12`, `Docs/README.md:5`) already say so. `DOCS_LAYOUT.md` was the only file still asserting a split; it was amended to match DEC-0029.

---

## Method notes

Two measurement errors were caught and corrected during this audit. Recording them so the numbers above are not trusted blindly:

1. **PowerShell `Group-Object` is case-insensitive.** The first pass collapsed `Docs/` and `docs/` into one row of 640, hiding R1 entirely. Only an explicit `StartsWith` comparison surfaced the 485/155 split.
2. **`git rev-parse` without `--verify` echoes its argument on failure** instead of erroring, so nonexistent paths compared as "different content". Separately, `if (git cat-file -e ...)` in PowerShell tests **stdout**, not the exit code, and `cat-file -e` prints nothing on success — so it always read false. R4's duplicate/pointer classification was redone using blob hashes from `git ls-tree`, which is unambiguous.