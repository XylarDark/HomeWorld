# Redundancy register

**Purpose:** One place for measured redundancy in this repo, with evidence and a proposed fix per entry. Audit-only unless an entry says *Applied*. Counts were rechecked with `git ls-tree -r` against `185853a5` and `7669dda4`.

**Not a delete list.** Every *Proposed* entry needs human sign-off before anything is removed. Deleting canon is a scope call, not an agent call.

**Before the chore (`185853a5`):** 3213 committed files. 1832 `Content/`, 642 files under the doc trees (487 `Docs/`, 155 `docs/`), 197 `Source/`, 89 `.cursor/`, 64 `.agents/`, 34 `Tools/`, 16 `.codex/`, 2 `.opencode/`. An earlier pass reported 3211 files and 485 `Docs/` entries. Those figures omit the only two PDFs, both under `Docs/harness-bible/`.

**After the chore (`7669dda4`):** 3193 committed files. `Docs/` 476, `docs/` 168, `.cursor/` 59, `.agents/` 71, `Tools/` 35. The seven extra `.agents` files arrived in `aeedc129`, between the two commits. `Content/`, `Source/`, `.codex/`, and `.opencode/` were unchanged.

---

## R1 — doc-tree casing drift

**Status:** APPLIED 2026-10-17 (targeted)

642 doc-tree files live in one directory; at `185853a5` git records **487** as `Docs/…` and **155** as `docs/…`. The same folder names were split across both spellings:

| Folder | `Docs/` | `docs/` | Total |
|---|---|---|---|
| `TaskLists/` | 9 | 51 | 60 |
| `human-use/` | 1 | 20 | 21 |
| `guides/` | 2 | 3 | 5 |
| `tasks/` | 1 | 4 | 5 |

**Applied:** the 13 files sitting in folders whose declared owner is the lowercase tree were re-recorded as case-only index changes — 9 in `TaskLists/`, 2 in `guides/`, 1 in `human-use/`, 1 in `tasks/`. All landed as `R100` (100% similarity: pure case change, nothing moves on disk). At `7669dda4` the counts are `Docs/` 476 and `docs/` 168 (487 − 13 renames + 2 new `Docs/` files, and 155 + 13). Those four folders have no `Docs/` entries left, and the index has 0 paths that differ only by case.

**Case-only index edit:** `git update-index --cacheinfo` alone fails with `missing --add option?`. Adding the new spelling without removing the old leaves both spellings in the index. The working sequence is `git rm --cached <old>` then `git update-index --add --cacheinfo <mode>,<hash>,<new>`. `docs/DOCS_LAYOUT.md` now says that.

**Still open:** the four folders above are settled. These `Docs/` folders were left on their recorded spelling: `handoffs/` 181, `art/` 90, `context/` 36, `qa/` 33, `canon/` 13, `level/` 8, `decisions/` 3, `harness-bible/` 3, `refs/` 3, `tools/` 1, `audit/` 1, plus 103 files at the `Docs/` root. An earlier "~142" did not match any of these totals. Settling them is a larger diff and was deliberately not bundled here.

---

## R2 — broken and ambiguous doc links

**Status:** open (pre-existing; unrelated to R1)

`npm run docs:links` (`Content/Python/check_doc_links.py`) at `7669dda4`:

```
checked 551 files; repaired 0; still broken 122 (1324 more repairable with --fix)
```

The 122 is the checker's blocking set: 37 links whose target exists nowhere, plus 85 basename-ambiguous links. The 1324 are a third bucket, resolvable by `--fix`, and are not inside the 122. An earlier "549 files" was the markdown count before this commit added two files. The checker uses `os.path.exists`, which on Windows does not prove the casing git records.

**Note:** two broken links in the always-on `AGENTS.md` were found and fixed during this audit (see R6). The remaining blocking links are elsewhere.

**Proposed:** run `--fix`, then triage the remainder by owner. The 85 ambiguous basename links matter most — they resolve to whatever the checker guesses.

---

## R3 — thirteen "what is next" surfaces, no pointer of record

**Status:** open

Thirteen committed docs present themselves as current or next work. Staleness by last commit:

| Tier | Files | Last commit |
|---|---|---|
| Stale (~4 weeks) | `Docs/11_NEXT_PHASE_STRATEGY.md`, `docs/workflow/MVP_AND_ROADMAP_STRATEGY.md` | 2026-09-17 |
| Stale | `Docs/26_TASTE_NEXT.md` | 2026-09-19 |
| Mid | `docs/TaskLists/T0_ROADMAP.md` | 2026-10-01 |
| Mid | `docs/TaskLists/T0_NEXT_QUEUE.md`, `docs/TaskLists/T0_EXECUTION_QUEUE.md` | 2026-10-08 |
| Mid | `Docs/qa/POLISH_READINESS.md`, `docs/TaskLists/NEXT_SESSION_PROMPT.md` | 2026-10-06 |
| Fresh | `docs/TaskLists/CURRENT_TASK_LIST.md`, `docs/TaskLists/30_DAY_IMPLEMENTATION_STATUS.md`, `docs/Automation/AUTOMATION_READINESS.md` | 2026-10-13 |
| Fresh | `Docs/context/PLAY_TASKS.md` | 2026-10-14 |
| Fresh | `Docs/context/NEXT_BEATS_INTERVIEW.md` | 2026-10-15 |

No two are byte-identical, so this is **navigational** redundancy, not file duplication: an agent cannot tell which is authoritative.

**Proposed (ruled 2026-10-17):** `Docs/context/PLAY_TASKS.md` is the pointer of record — it is the freshest credible candidate, is already the doc root `AGENTS.md` names, and sits under `context/` beside `SCENE_SETUP.md` and `SESSION_START.md`. The other twelve should carry a pointer to it rather than be deleted. **Not yet fanned out** — the designation is recorded here and in `DOCS_LAYOUT.md`; adding the pointer line to all twelve files is still to do. The three `TaskLists` dates above are the last content edit, taken at the parent of the case-only rename. `git log -1` on the new `docs/TaskLists/…` path reports 2026-10-17 because that rename is the latest commit.

---

## R4 — duplicated skill trees

**Status:** APPLIED 2026-10-17

`.agents/skills/` and `.cursor/skills/` mirrored five skills as byte-identical full copies — 35 files including whole `reference/` subtrees and `metadata.json`. Four other skills already used pointer stubs ("Pointer. Read the other. Do not keep a second copy here."), so a pointer convention existed and these five did not follow it.

**Applied:** `.agents/skills/` is the content owner for these five. At `185853a5` that directory held 50 files in 20 skill directories; `.cursor/skills/` held 40 files in 9 directories. `.agents` also owns `skills-extras/`. The pointer direction was already mixed: `automation-gap-solutions`, `pcg-validate`, and `ue-editor-ui` keep their content in `.cursor` and point from `.agents`. `ue58-api-check` already pointed from `.cursor` to `.agents`.

Converted to pointers in `.cursor/skills/`: `navigating-code`, `refactoring-code`, `ue-code-authoring`, `ue-live-debugging`, `ue-test-authoring`.

**Result:** 30 files removed. Each of those `.cursor` skills is now a single 8-line `SKILL.md` pointer; all `.agents` trees intact; every pointer target resolves; **0 byte-identical skill pairs remain**.

**Rule now in force:** a skill's content lives in exactly one tree. The other holds a pointer. Never a second copy. `.agents` is the owner for the five converted skills, not for every skill.

---

## R5 — agent roster maintained three times, already drifted

**Status:** APPLIED 2026-10-17. Derived copies were synced after the integration diff was reviewed.

The same 15-agent roster exists three ways:

| Path | Count | Form |
|---|---|---|
| `.cursor/agents/` | 15 + `README.md` | `.md` — **source of truth** |
| `swarm/agents/` | 15 | `.md` — derived, normalized content must match the source |
| `.codex/agents/` | 15 | `.toml` — derived, same content in Codex's shape |

**There was no generator.** No script under `scripts/`, `Tools/`, or `swarm/` wrote these directories, so the copies drifted silently.

**Applied:** `Tools/AgentRoles.ps1`. Read-only by default; `-Sync` regenerates the derived copies and never edits the source. Bodies are TOML literal strings (`'''`). A basic string (`"""`) treats `\b` as backspace and rejects `\P`, which corrupts a Windows path.

```
.\Tools\AgentRoles.ps1          # check only, exit 1 on drift
.\Tools\AgentRoles.ps1 -Sync    # regenerate derived copies
```

The check compares **normalized** content (line endings and trailing whitespace folded), so legacy formatting does not read as drift while a real edit still trips it. Trailing spaces that markdown treats as a hard line break are inside that fold.

**Drift that was open, then synced.** The check reported 17 problems before calibration and 4 after; the other 13 were formatting artifacts of the generator, not repo drift. The four were `swarm/agents/integration.md`, `.codex/agents/integration.toml`, a missing `swarm/agents/verifier.md`, and `.codex/agents/verifier.toml`.

The integration diff was the older card. Source says Mixar. The swarm copy still said Blender and omitted the Mixar paragraph. `-Sync` copied the source and added `swarm/agents/verifier.md`. Codex bodies now use literal strings, so `C:\Program Files\Mixar\mixar.exe` and `.\Tools\Safe-Build.ps1` stay character-for-character. `.\Tools\AgentRoles.ps1 -Check` exits 0: 15 cards, source `.cursor/agents`.

**Rule now in force:** `.cursor/agents/*.md` is the source of truth. `swarm/agents/*.md` and `.codex/agents/*.toml` are generated. Never hand-edit a derived copy; run `-Sync`.

---

## R6 — link casing in always-on context

**Status:** APPLIED 2026-10-17

`AGENTS.md` linked `docs/tools/Rider_MCP_for_UE_Games.md` (twice) and `docs/handoffs/MARKETPLACE_POLICY_V1.md`, but both files are recorded as `Docs/…`. They resolve on Windows and **404 on a case-sensitive clone or CI checkout** — including the doc that explains the Rider MCP tool trust matrix.

**Applied:** both links now use the casing git records. `AGENTS.md` has 20 markdown-link instances and 18 unique targets. Each unique target matches `git ls-tree` exactly. `npm run docs:links` also reports the file clean, and that checker cannot see case on Windows.

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
- **Four skills that "diverged"** between `.agents/` and `.cursor/` are intentional pointer stubs, not conflicting copies. Three point at content in `.cursor`: `automation-gap-solutions`, `pcg-validate`, `ue-editor-ui`. `ue58-api-check` points at content in `.agents`.

---

## Verified negatives

Checked, not assumed — each of these was confirmed rather than inferred:

- `alwaysApply: false` in **all 17** `.cursor/rules/*.mdc`. The `AGENTS.md` "no `alwaysApply: true`" rule holds.
- `.cursor/rules/unreal-cpp.mdc` carries `globs: "**/*.cpp, **/*.h"`, so Cursor **does** auto-attach the C++ rules to every `.cpp`/`.h` edit. The OpenCode-vs-Cursor parity gap is real, not theoretical.
- `Docs/` and `docs/` are one directory. `CANON_MAP.md:40` and `:243`, `docs/AGENTS_REFERENCE.md:10` and `:12`, and `Docs/README.md:5` say so. `docs/DOCS_LAYOUT.md` was amended to match those lines. Root `README.md` also had a "Docs split" section; that section now uses the one-directory wording. DEC-0029 is the vision-board decision. Its text does not state this casing rule.

---

## Method notes

Measurement errors caught while these numbers were produced:

1. **PowerShell `Group-Object` is case-insensitive.** The first pass collapsed `Docs/` and `docs/` into one row, hiding R1. Count the two spellings with a case-sensitive `StartsWith`.
2. **`git rev-parse` without `--verify` writes the missing name on stdout and still exits 128.** A caller that reads only stdout treats a missing path as real content. `if (git cat-file -e ...)` in PowerShell tests stdout, and `cat-file -e` prints nothing on success, so the true branch never runs. Blob hashes from `git ls-tree` are the check that does not depend on either.
3. **The first `Docs/` total dropped two PDFs** (`Docs/harness-bible/Slides - Agentic Engineering in Unreal.pdf` and `Week 1 - Agentic Engineering.pdf`). `git ls-tree -r --name-only` counts them. 487 and 476 are the totals that include them.