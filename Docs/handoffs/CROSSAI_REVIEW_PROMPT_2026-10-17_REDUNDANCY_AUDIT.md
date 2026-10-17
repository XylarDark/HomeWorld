# Cross-AI review prompt — redundancy audit + OpenCode/Cursor parity (2026-10-17)

**Purpose:** an independent audit of work that is now **committed and pushed**, so every claim can be checked against an immutable SHA rather than a dirty working tree.

**File protocol:** this is a **review** document, not research and not canon. Do not mine `Docs/handoffs/` for product truth. Product canon starts at `Docs/VISION_BOARD.md`, indexed by `Docs/CANON_MAP.md`.

**Paste the block below verbatim.** Everything after the block is context for you, the human, and is not part of the prompt.

---

## PASTE BLOCK START

You are auditing a completed work session in the HomeWorld repo (`C:\dev\HomeWorld`, UE 5.8, Windows, git). Another AI made the changes below and committed them. **Do not trust its conclusions, including the ones in this brief.** Verify each claim independently from the repo.

### Ground rules

1. **Verify, do not review.** For every claim, produce the command you ran and its actual output. A claim you did not execute is an unverified claim — label it as such.
2. **Do not fix anything.** Report only. If you believe a change is wrong, say so with evidence and stop. Do not edit, stage, commit, revert, or delete.
3. **The audit target is immutable.** The work is committed and pushed. Inspect it with `git show` and `git diff` between SHAs — never by reading the working tree, which has drifted since.
4. **One unrelated file is dirty.** `Docs/level/L_SizeTest_ROOM_PLAN.md` was already modified before this session and is explicitly **out of scope**. Do not touch it, and do not treat it as part of the audit. Do not run `git checkout .`, `git reset`, `git stash`, or `git clean` — they would destroy it.
5. **Do not trust the numbers in this brief.** Several were wrong at least once during the session. Recompute them.
6. **The agent reported four mistakes in its own tooling.** Section 7 lists them. Check whether any shipped in the delivered files, and whether the register's own claims are accurate.

### The commits under audit

| SHA | Subject | Scope |
|---|---|---|
| `185853a5` | `feat: discover the paradox toy when a stroke begins` | C++ change + its test |
| `7669dda4` | `chore: dedupe agent skill trees and settle doc-tree casing` | 54 files: skill dedupe, doc casing, tooling, register, this prompt's first draft |

Start here:
```
git show 185853a5 --stat
git show 7669dda4 --stat
git log --oneline -5
```

Confirm the commits contain **only** what is claimed. If `7669dda4` contains anything unexpected, that is your first finding.

---

### Change 1 — C++: paradox-toy discovery (`185853a5`)

- `Source/HomeWorld/HomeWorldCharacter.h` — added `void DiscoverParadoxToy();`
- `Source/HomeWorld/HomeWorldCharacter.cpp` — implemented it (mirrors `DiscoverStrokePad()`: early-return if set, else `TActorIterator<AHomeWorldParadoxToy>`, take first); called it from `BeginStrokeFromInput()` right after `DiscoverStrokePad()`
- `Source/HomeWorld/HomeWorldStrokePawnTests.cpp` — added `FStrokeParadoxToyDiscovered`

**Claim:** `Safe-Build.ps1` exits 0 and the test passes at runtime (`passed 14, failed 0`). **Verify independently** — do not take the automation runner's summary at face value:
```
git show 185853a5 -- Source/HomeWorld/HomeWorldCharacter.cpp Source/HomeWorld/HomeWorldCharacter.h
git show 185853a5 -- Source/HomeWorld/HomeWorldStrokePawnTests.cpp
.\Tools\Safe-Build.ps1
.\Tools\RunTests.ps1 -Filter "HomeWorld.Systems.Stroke"
```
Then open `Saved/AutomationReport/index.json` and confirm `HomeWorld.Systems.Stroke.ParadoxToyDiscovered` has `state=Success` yourself. The runner printed `passed 14` while listing 16 tests; the agent claims this is the runner's own arithmetic and all 16 are `Success`. **Confirm or refute that.**

**Scrutinise the design.** `DiscoverParadoxToy` takes the *first* toy in the world, mirroring `DiscoverStrokePad`. Judge whether first-match is acceptable or a latent bug when a level holds more than one toy. Also: `DiscoverStrokePad` early-returns if already set and never re-scans — check whether that interacts badly with level transitions.

### Change 2 — deletions of scaffolding (pre-`7669dda4`, not in either SHA)

These were deleted as scaffolding that should never have shipped: `Tools/Run-RiderDiagnostics.ps1` (it only called `Write-Host` — it never contacted Rider MCP, so running it produced a **false pass**), `PLAN_OPENCODE_PARITY.md`, `.opencode/AGENTS_OPENCODE.md`, `docs/Setup/OPENCODE_RULES_BOOTSTRAP.md`. Recover them with `git show 185853a5:<path>`.

**Claim:** the `AGENTS.md` edit removed a `## OpenCode parity` section while preserving an unrelated concurrent edit to the same file. **Verify both halves** — the parity block is gone AND the `RESEARCH_PROMPT_CONTRACT.md` sentence survived:
```
git show 185853a5:AGENTS.md | Select-String "RESEARCH_PROMPT_CONTRACT"
git show 185853a5:AGENTS.md | Select-String "OpenCode parity"
```
**Claim:** no dangling references to the four deleted files remain. Sweep the repo yourself; do not trust the claim.

### Change 3 — AGENTS.md link casing (`7669dda4`)

`AGENTS.md` linked `docs/tools/Rider_MCP_for_UE_Games.md` (twice) and `docs/handoffs/MARKETPLACE_POLICY_V1.md`, but git records both as `Docs/…`. Changed to the recorded casing.

**Claim:** these 404 on a case-sensitive clone and resolved only because Windows is case-insensitive. Verify the paths match `git ls-tree` exactly and that `AGENTS.md` is 18/18 links resolving. The repo has its own checker: `npm run docs:links`.

### Change 4 — skill dedupe, 30 files removed (`7669dda4`)

`.agents/skills/` and `.cursor/skills/` held five skills as byte-identical full copies (SKILL.md + metadata.json + whole `reference/` subtrees). Four other skills already used pointer stubs saying *"Pointer. Read the other. Do not keep a second copy here."*

Converted to pointers with **`.agents/skills/` as content owner**: `navigating-code`, `refactoring-code`, `ue-code-authoring`, `ue-live-debugging`, `ue-test-authoring`. Each `.cursor` skill is now a single `SKILL.md`.

**Claim:** `.agents` trees untouched and intact (5/12/5/7/6 files), every pointer target resolves, 0 byte-identical skill pairs remain.

**Scrutinise the justification**, which was: `.agents/skills/` is larger, owns `skills-extras/`, is where the session's own skill loader resolved, and the newest UE skill `ue58-api-check` already resolved `.agents` as owner. Is `.agents` genuinely the right owner, or is this a guess dressed as evidence? **Would a Cursor-only user lose anything now that `.cursor/skills/` holds pointers into a tree Cursor may not read?** This is the highest-value question in the audit.

Also verify the stubs are well-formed (correct `name:`, resolvable relative link) and that deleting `reference/` from `.cursor` broke no inbound reference. Search for pointers to the deleted paths.

### Change 5 — DOCS_LAYOUT.md amended (`7669dda4`)

`AGENTS.md` (always loaded) says `Docs/` and `docs/` are one directory and forbids describing a split. `docs/DOCS_LAYOUT.md` said they were "intentionally separate" and "do not merge". Ruling received: DOCS_LAYOUT was stale. Four edits brought it in line with DEC-0029, keeping its casing guidance.

**Claim:** DOCS_LAYOUT was the only file asserting a split. Verify by searching canon for "intentionally separate", "do not merge", "second tree" — the agent cites `CANON_MAP.md:40` and `:243`, `AGENTS_REFERENCE.md:10`/`:12`, `README.md:5`. Confirm or find dissenters.

**Scrutinise the edit:** did it delete anything of value, or weaken a real constraint that was doing work? Check the retained case-collision guidance still stands.

### Change 6 — R1 casing repair, 13 renames (`7669dda4`)

13 case-only index changes for files in folders whose declared owner is the lowercase tree: 9 in `TaskLists/`, 2 in `guides/`, 1 in `human-use/`, 1 in `tasks/`. All landed as `R100`.
```
git show 7669dda4 --name-status | Select-String "^R"
```
**Claim:** nothing moves on disk (case-only), and counts went `Docs/` 485→474, `docs/` 155→168.

**The agent found a defect in the repo's own documented method:** `DOCS_LAYOUT.md` says use `git update-index --cacheinfo`, but that alone fails (`missing --add option?`), and adding the new path without removing the old leaves BOTH spellings in the index as duplicates — worse than the original drift. Correct sequence: `git rm --cached <old>` then `git update-index --add --cacheinfo <mode>,<hash>,<new>`. **Verify the index has no duplicate-spelling entries** and that no file was lost or duplicated. Note the agent recorded this in the register but did **not** correct the line in `DOCS_LAYOUT.md` — judge whether that follow-up is owed.

### Change 7 — `Tools/AgentRoles.ps1`, new (`7669dda4`)

`.cursor/agents/*.md` is the declared source of truth; `swarm/agents/*.md` and `.codex/agents/*.toml` are derived. There was no generator and the copies had already drifted.
```
.\Tools\AgentRoles.ps1            # read-only, exit 1 on drift
.\Tools\AgentRoles.ps1 -Check
.\Tools\AgentRoles.ps1 -Sync      # deliberately NOT run; see below
```
**Claim:** reports exactly 4 problems — `swarm/agents/verifier.md` MISSING, `swarm/agents/integration.md` DIFFERS, `.codex/agents/integration.toml` DIFFERS, `.codex/agents/verifier.toml` DIFFERS.

**Audit the script hard.** It is new, untested-in-CI code that can rewrite committed files. Check: does `-Check` genuinely write nothing? Does `-Sync` ever modify `.cursor/agents/` (it must not)? Is the TOML emitter correct for edge cases — bodies containing `"""`, or `"` in descriptions? Is `Get-Normalized` too lossy (could it mask a real content change)? Does it handle a source card whose frontmatter lacks `name:`? Does it write LF consistently, with or without a BOM?

**`swarm/agents/integration.md` is stale, not absent** — the agent's first survey missed this by counting only byte-identical copies. Check whether other agents are stale in ways both surveys missed, e.g. by diffing content rather than counting hashes.

### Change 8 — `docs/audit/REDUNDANCY_REGISTER.md`, new (`7669dda4`)

New register plus entries in `docs/DOCS_LAYOUT.md` and `docs/README_ENGINEERING.md`, per `.cursor/rules/19-docs-directory-structure.mdc`, which requires a new subdirectory to update both index files. Verify that rule was followed and both files were actually updated.

**The register is the session's main written deliverable. Scrutinise it hardest.** Every number and status should be independently reproducible. It claims R1, R4, R6 applied; R2, R3, R5-drift, R7 open; and lists three of the agent's own measurement errors. Check for claims that are wrong, unsupported, or quietly overstated.

### Deliberately NOT done — verify these are genuinely incomplete, not quietly skipped

- **`AgentRoles.ps1 -Sync` was not run.** It would overwrite 4 derived files from source, risking loss of hand-edits made directly in `swarm/` or `.codex/`. Judge whether that caution was correct or whether the drift should have been fixed.
- **R1 remainder:** ~142 paths elsewhere (`handoffs/`, `art/`, `context/`, `qa/`, `canon/`) still carry historical casing. Note the commit's two new files landed as `Docs/audit/` and `Docs/handoffs/` (capital D), so the remainder is 142+, not 142.
- **R3 fan-out:** the pointer of record (`Docs/context/PLAY_TASKS.md`) was designated centrally in `DOCS_LAYOUT.md`, but pointer lines were **not** added to the other twelve competing docs.
- **R2:** 122 broken + 85 ambiguous doc links, pre-existing and unchanged by this work. `npm run docs:links --fix` can repair 1324.
- **R7:** duplicate `.fbx` in `AssetCreation/AssetDump/` vs `AssetCreation/Exports/`. Ruled: leave open, no gitignore.

### Constraints you inherit

- Read `AGENTS.md` at the audited SHA first. UE 5.8 only. Never run `Build-HomeWorld.bat` — use `.\Tools\Safe-Build.ps1`.
- Rider MCP (`127.0.0.1:64342`) was **not running** during the session and is not required here — use native tools.
- `Docs/handoffs/research/` was off-limits under `AGENTS.md` during the session. Respect that unless you have reason to enter it.
- `Docs/canon/DESIGN_ETHOS.md` is gated: open it only when auditing a mechanic, environment, or progression step. This audit is neither.

### Report format

1. **Verdict per change** — correct / correct-with-concerns / wrong, each with the command you ran and its output.
2. **Defects found**, ranked by severity, each with reproduction.
3. **Claims that did not survive checking** — quote the claim, show the contradicting evidence.
4. **Anything the agent missed entirely.**
5. **What you would change**, if you were fixing it. Do not fix it.

## PASTE BLOCK END

---

## Notes for the human (not part of the prompt)

- **Why this rewrite matters:** the first version told the auditor to inspect a dirty working tree. Now that the work is pinned to two SHAs, the audit target is immutable — the auditor can reproduce exactly what was committed, and cannot accidentally measure a half-written state. That was the single biggest weakness in the original.
- **Strongest thing to challenge** is Change 4 — designating `.agents/skills/` as content owner makes every Cursor-side skill a pointer into a tree Cursor may not read. That is a behavioural bet, and it is the one decision here that could quietly degrade the Cursor flow the task was meant to improve.
- **Second** is Change 7 — `AgentRoles.ps1 -Sync` can rewrite committed files and has never been run. If Grok finds it correct, syncing the two stale agents is the natural next step, but review `integration` by hand first.
- **Owed follow-up** if the audit agrees: the `git update-index --cacheinfo` line in `DOCS_LAYOUT.md` is still wrong (Change 6). It is documented in the register but not fixed at source.
- To run a cheaper audit, cut Change 2 (the deleted-scaffolding review). It is the least load-bearing.