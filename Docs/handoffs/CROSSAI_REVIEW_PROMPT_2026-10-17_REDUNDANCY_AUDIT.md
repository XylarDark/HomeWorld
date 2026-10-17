# Cross-AI review prompt — redundancy audit + OpenCode/Cursor parity (2026-10-17)

**Purpose:** an independent audit of everything one agent changed in a single session. Written for a fresh AI with no access to that session's reasoning.

**File protocol:** this is a **review** document, not research and not canon. Do not mine `Docs/handoffs/` for product truth. Product canon starts at `Docs/VISION_BOARD.md`, indexed by `Docs/CANON_MAP.md`.

**Paste the block below verbatim.** Everything after the block is context for you, the human, and is not part of the prompt.

---

## PASTE BLOCK START

You are auditing a completed work session in the HomeWorld repo (`C:\dev\HomeWorld`, UE 5.8, Windows, git). Another AI made the changes listed below. **Do not trust its conclusions, including the ones in this brief.** Verify each claim independently from the repo.

### Ground rules

1. **Verify, do not review.** For every claim, produce the command you ran and its actual output. A claim you did not execute is an unverified claim — label it as such.
2. **Do not fix anything.** Report only. If you believe a change is wrong, say so with evidence and stop. Do not edit, stage, commit, revert, or delete.
3. **Uncommitted work is the subject.** The tree is deliberately dirty. `git status` and `git diff` are your primary instruments. Do not clean, reset, stash, or checkout anything.
4. **Do not trust the numbers in this brief.** Several were wrong at least once during the session. Recompute them.
5. **The agent reported four mistakes in its own tooling.** Section 6 lists them. Check whether any shipped in the delivered files, and whether the register's own claims are accurate.

### What the session was for

Two tasks. (a) Audit and OpenCode/Cursor workflow parity. (b) A repo-wide redundancy audit, and fix what was ruled safe.

### Change 1 — C++: paradox-toy discovery (uncommitted, runtime-verified)

- `Source/HomeWorld/HomeWorldCharacter.h` — added `void DiscoverParadoxToy();`
- `Source/HomeWorld/HomeWorldCharacter.cpp` — implemented it (mirrors `DiscoverStrokePad()`: early-return if set, else `TActorIterator<AHomeWorldParadoxToy>`, take first); called it from `BeginStrokeFromInput()` right after `DiscoverStrokePad()`
- `Source/HomeWorld/HomeWorldStrokePawnTests.cpp` — added `FStrokeParadoxToyDiscovered`

**Claim:** test passes at runtime. **Verify independently** — do not take the automation runner's summary at face value:
```
git diff Source/HomeWorld/HomeWorldCharacter.cpp Source/HomeWorld/HomeWorldCharacter.h
git diff Source/HomeWorld/HomeWorldStrokePawnTests.cpp
.\Tools\Safe-Build.ps1
.\Tools\RunTests.ps1 -Filter "HomeWorld.Systems.Stroke"
```
Then open `Saved/AutomationReport/index.json` and confirm `HomeWorld.Systems.Stroke.ParadoxToyDiscovered` has `state=Success` yourself. The runner printed `passed 14` while listing 16 tests; the agent claims this is the runner's arithmetic and all 16 are `Success`. **Confirm or refute that.**

**Scrutinise the design.** `DiscoverParadoxToy` takes the *first* toy in the world. `DiscoverStrokePad` has the same first-match behaviour. Judge whether first-match is acceptable, or whether it is a latent bug when a level holds more than one toy. Also: `DiscoverStrokePad` early-returns if already set, so it never re-scans — check whether that interacts badly with level transitions.

### Change 2 — deletions (audit trail)

Deleted, as scaffolding that should never have shipped:
`Tools/Run-RiderDiagnostics.ps1` (it only called `Write-Host` — it never contacted Rider MCP, so running it produced a false pass), `PLAN_OPENCODE_PARITY.md`, `.opencode/AGENTS_OPENCODE.md`, `docs/Setup/OPENCODE_RULES_BOOTSTRAP.md`.

**Claim:** the AGENTS.md edit removed a `## OpenCode parity` section while preserving an unrelated concurrent edit to the same file. **Verify both halves** — that the parity block is gone AND that the `RESEARCH_PROMPT_CONTRACT.md` sentence is still present:
```
git diff AGENTS.md
```
**Claim:** no dangling references to the four deleted files remain anywhere. Sweep the repo yourself; do not trust the claim.

### Change 3 — AGENTS.md link casing (2 links)

`AGENTS.md` linked `docs/tools/Rider_MCP_for_UE_Games.md` (twice) and `docs/handoffs/MARKETPLACE_POLICY_V1.md`, but git records both as `Docs/…`. Changed to the recorded casing.

**Claim:** these 404 on a case-sensitive clone; they resolved only because Windows is case-insensitive. Verify the current paths match `git ls-tree` exactly, and that `AGENTS.md` is 18/18 links resolving. The repo has its own checker: `npm run docs:links`.

### Change 4 — skill dedupe (30 files removed)

`.agents/skills/` and `.cursor/skills/` held five skills as byte-identical full copies (SKILL.md + metadata.json + whole `reference/` subtrees). Four other skills already used pointer stubs saying *"Pointer. Read the other. Do not keep a second copy here."*

Converted to pointers with **`.agents/skills/` as content owner**: `navigating-code`, `refactoring-code`, `ue-code-authoring`, `ue-live-debugging`, `ue-test-authoring`. 30 files removed from `.cursor/skills/`; each `.cursor` skill is now a single `SKILL.md`.

**Claim:** `.agents` trees untouched and intact (5/12/5/7/6 files), every pointer target resolves, 0 byte-identical skill pairs remain.

**Scrutinise the justification**, which was: `.agents/skills/` is larger, owns `skills-extras/`, is where the session's own skill loader resolved, and the newest UE skill `ue58-api-check` already resolved `.agents` as owner. Is `.agents` genuinely the right owner, or is this a guess dressed as evidence? Would a Cursor-only user lose anything now that `.cursor/skills/` holds pointers into a tree Cursor may not read? **This is the highest-value question in the audit.**

Also verify the pointer stubs are well-formed: correct `name:`, resolvable relative link, and that deleting `reference/` from `.cursor` broke no other file that referenced those paths. Search for inbound references to the deleted `reference/` files.

### Change 5 — DOCS_LAYOUT.md amended

`AGENTS.md` (always loaded) says `Docs/` and `docs/` are one directory and forbids describing a split. `docs/DOCS_LAYOUT.md` said they were "intentionally separate" and "do not merge". Ruling received: DOCS_LAYOUT was stale. Four edits brought it in line with DEC-0029, keeping its casing guidance.

**Claim:** DOCS_LAYOUT was the only file asserting a split. Verify by searching canon for "intentionally separate", "do not merge", "second tree" — the agent cites `CANON_MAP.md:40` and `:243`, `AGENTS_REFERENCE.md:10`/`:12`, `README.md:5` as already saying "one directory". Confirm or find dissenters.

**Scrutinise the edit:** did it delete anything of value, or weaken a real constraint that was doing work? Check the retained case-collision guidance still stands.

### Change 6 — R1 casing repair (13 renames, STAGED)

13 case-only index changes for files in folders whose declared owner is the lowercase tree: 9 in `TaskLists/`, 2 in `guides/`, 1 in `human-use/`, 1 in `tasks/`. All landed as `R100`.
```
git diff --cached --name-status     # expect 13 R100 lines
```
**Claim:** nothing moves on disk (case-only). **Claim:** counts went `Docs/` 485→474, `docs/` 155→168.

**The agent found a defect in the repo's own documented method** and corrected it in place: `DOCS_LAYOUT.md` says use `git update-index --cacheinfo`, but that alone fails (`missing --add option?`), and adding the new path without removing the old leaves BOTH spellings in the index as duplicates. Correct sequence: `git rm --cached <old>` then `git update-index --add --cacheinfo <mode>,<hash>,<new>`. **Verify the index has no duplicate-spelling entries**, and confirm no file was lost or duplicated. Consider whether the docs should be corrected (the agent recorded it in the register but did NOT edit that line).

### Change 7 — Tools/AgentRoles.ps1 (new, calibrated after 4 failures)

`.cursor/agents/*.md` is now the declared source of truth; `swarm/agents/*.md` and `.codex/agents/*.toml` are derived. There was no generator and the copies had already drifted.
```
.\Tools\AgentRoles.ps1            # read-only, exit 1 on drift
.\Tools\AgentRoles.ps1 -Check
.\Tools\AgentRoles.ps1 -Sync      # NOT run by the agent; see below
```
**Claim:** currently reports exactly 4 problems — `swarm/agents/verifier.md` MISSING, `swarm/agents/integration.md` DIFFERS, `.codex/agents/integration.toml` DIFFERS, `.codex/agents/verifier.toml` DIFFERS.

**Audit the script hard.** It is new, untested-in-CI code that rewrites committed files. Check: does `-Check` genuinely write nothing? Does `-Sync` ever modify `.cursor/agents/` (it must not)? Is the TOML emitter correct for edge cases — bodies containing `"""`, or `"` in descriptions? Is the normalisation in `Get-Normalized` too lossy (could it mask a real content change)? Does it handle a source card whose frontmatter lacks `name:`? Does it write LF consistently with the committed files, and with or without a BOM?

**`swarm/agents/integration.md` is stale, not absent** — the agent's first survey missed this by only counting byte-identical copies. Check whether other agents are stale in ways both surveys missed, e.g. by diffing content rather than counting hashes.

### Change 8 — docs/audit/REDUNDANCY_REGISTER.md (new) + 2 index updates

New register plus entries in `docs/DOCS_LAYOUT.md` and `docs/README_ENGINEERING.md`, per the rule in `.cursor/rules/19-docs-directory-structure.mdc` that a new subdirectory requires updating both index files. Verify that rule was followed and that both index files were actually updated.

**The register is the session's main written deliverable. Scrutinise it hardest.** Every number and status in it should be independently reproducible. It claims R1, R4, R6 applied; R2, R3, R5-drift, R7 open; and lists three of the agent's own measurement errors. Check for claims that are wrong, unsupported, or quietly overstated.

### Deliberately NOT done — verify these are genuinely incomplete, not quietly skipped

- **`AgentRoles.ps1 -Sync` was not run.** It would overwrite 4 derived files from source, risking loss of hand-edits made directly in `swarm/` or `.codex/`. Judge whether that caution was correct or whether the drift should have been fixed.
- **R1 remainder:** ~142 paths elsewhere (`handoffs/`, `art/`, `context/`, `qa/`, `canon/`) still carry historical casing.
- **R3 fan-out:** the pointer of record (`Docs/context/PLAY_TASKS.md`) was designated centrally in `DOCS_LAYOUT.md`, but pointer lines were **not** added to the other twelve competing docs.
- **R2:** 122 broken + 85 ambiguous doc links, pre-existing. `npm run docs:links --fix` can repair 1324.
- **R7:** duplicate `.fbx` in `AssetCreation/AssetDump/` vs `AssetCreation/Exports/`. Ruled: leave open, no gitignore.

### Constraints you inherit

- Read `AGENTS.md` first. UE 5.8 only. Never run `Build-HomeWorld.bat` — use `.\Tools\Safe-Build.ps1`.
- The tree is intentionally dirty. **Do not reset, clean, stash, or checkout.** Other uncommitted work predates this session.
- Rider MCP (`127.0.0.1:64342`) was **not running** during the session and is not required for this audit — use native tools.
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

- **Uncommitted by design.** Nothing is committed. The 13 renames are staged because `git update-index` stages as a side effect; everything else is unstaged.
- **Strongest thing to challenge** is Change 4 — designating `.agents/skills/` as content owner makes every Cursor-side skill a pointer into a tree Cursor may not read. That is a behavioural bet, and it is the one decision here that could quietly degrade the Cursor flow the whole task was meant to improve.
- **Second** is Change 7 — `AgentRoles.ps1 -Sync` can rewrite committed files and has never been run. If Grok finds it correct, running `-Sync` on the two stale agents is the natural next step, but review `integration` by hand first.
- If you want the audit to be cheaper to run, cut section 3 (the deleted-scaffolding audit). It is the least load-bearing of the seven.