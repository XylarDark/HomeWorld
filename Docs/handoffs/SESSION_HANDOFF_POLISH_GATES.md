# Session handoff — polish entry gates and the island plate

**Written 2026-10-04. Branch `main`, HEAD `a701b15`, tree clean, `polish` untouched.**

Fresh chat should read this file plus `docs/SESSION_SUMMARY.md`. Do not carry the transcript.

## What this slice is

Make the human polish pass *safe to start* by making it impossible to start blind. That means
two things, both now built: an honest gate that refuses to call the build ready while it is not,
and a measurement instrument that reports the island's real size in the engine rather than the
size Blender wrote down.

## State

| | |
|---|---|
| `main` | `a701b15`, clean, verified an ancestor of `origin/main` |
| `polish` / `origin/polish` | untouched — reserved for the Lead |
| Tests | 114 pass + 69 subtests (`Content/Python/tests/test_polish_readiness.py`) |
| Gate | `NOT_READY`. G-ENV `FAIL 2 MISSING 2 PASS 6` · G-ASSET `FAIL 1 MISSING 1 PASS 2` · G-FEEL `FAIL 1 MISSING 3 PASS 1` |

Regenerate the gate with `python Content/Python/polish_readiness.py` from the repo root. Exit
code 1 is correct while RED.

## The one thing that needs the editor

`env.ue_island_measured` reads `MISSING` because `Docs/qa/UE_ISLAND_MEASUREMENT.json` is still
the seeded skeleton. When the Lead opens the editor, in this order:

1. Re-import `AssetCreation/Exports/**/SM_IslandTop.fbx` over the existing asset.
2. Re-place the actor if its transform moved.
3. Open **`Content/HomeWorld/Maps/VS_MVP/L_VS_MVP_Markers.umap`** — not `MainMenu`.
4. Run `Content/Python/measure_ue_island.py` (read-only; writes only the JSON).
5. Commit `Docs/qa/UE_ISLAND_MEASUREMENT.json` **and** the re-imported `SM_IslandTop.uasset`.
6. Re-run the gate chain.

Step 5 has no rule problem. `Config/uasset-allowlist.json` already allowlists
`Content/HomeWorld/Meshes`, the asset is already tracked and LFS-backed, and the object is
present. An earlier message to the Lead claimed otherwise and was wrong — see
`docs/KNOWN_ERRORS.md`, *"Asserting a repo rule from memory instead of reading the machine config."*

## The two RED failures in G-ENV that are on purpose

`master_binding` and `family_distinct` FAIL. The Lead ruled on 2026-10-04 that they stay RED.
Do not "fix" them, do not soften them, and do not add a WARN tier that would demote them — that
would undo the ruling by another name. Recorded as DEC-0031.

## Human-only rows — nobody has played this build

- `asset.board` — 0/10 declared
- `feel.human_playtest` — `feel.verb_script` 0/8 run — `feel.tunable_baselines` 0/6

`Docs/qa/POLISH_BASELINE.json` is an all-null skeleton with a `_deferrals` block. The Lead
deferred the two traversal numbers (`cabin_to_lookout_s`, `island_circuit_s`) until the engine
gap closes. Do not fill them in early; the deferral is recorded on purpose.

## Open decisions for the Lead — none of these are agent-owned

1. **Build the idea → Steam Early Access pipeline map**, one owner per step, indexed on
   `Docs/CANON_MAP.md`. Largest remaining gap against the Lead's stated vision. Asked twice, not
   yet answered.
2. **Does the gate get a severity ladder?** The research (`Docs/38_AI_AGENT_PRACTICE.md` §11.3)
   says mature gates ship a rule as WARN and promote it to error once clean. Our gate is binary.
   The capability is recorded; deliberately not applied.
3. **Is "polish" the right name for this stage?** Industry usage means alpha→beta; we have no
   human playtest, so we are at a vertical slice. Renaming touches every gate row id, both
   `Docs/qa/POLISH_*` files and four canon docs. Recorded, not decided.
4. **Tutor mode does not exist.** No row, clause or skill anywhere in the repo. Audited and
   confirmed absent. If it is wanted, it needs a decision first.

## If the island silhouette is wrong

Edit `RIM` / `SPEC_X` / `SPEC_Y` in `AssetCreation/Blender/apply_island_plate.py`, re-run, and
the abort gate reports if the walk oval escapes. `RIM` is the hand-tunable round-number
silhouette. `Lib/01_Homestead/SM_IslandTop.md` is Lead canon: 180×100, top Z=0, 0.3–0.6 thick.

## Traps that will cost the next chat time

- **`Docs/` and `docs/` are both tracked as separate trees** and `core.ignorecase = true`.
  `git status` displays `docs/qa/...` for files that must be staged as `Docs/qa/...`. Confirm
  every new file with `git diff --cached --name-status`.
- **A batched `git add` silently skips the whole command** if one pathspec is lowercase `docs/`
  and another is a new file. Exit 0, no output, nothing staged. Cause and repro are in
  `docs/KNOWN_ERRORS.md`. **Add one path at a time**, capital `Docs`, then confirm with
  `git diff --cached --name-status`.
- **`git push` writes stderr noise on success.** Verify with `git fetch` then
  `git merge-base --is-ancestor HEAD origin/main`.
- **`docs/SESSION_SUMMARY.md` is not valid UTF-8** (cp1252 `0xa7` at 84213). Append as bytes.
  Never `write_text(read_text(...))`.
- **LFS objects live under `.git/lfs/objects`**, not `%LOCALAPPDATA%\lfs\objects`. Ask
  `git lfs env`.
- **`unrealMCP` returns `null` rather than an error when the editor is down** — itself a
  fail-open. Do not read `null` as "checked and fine".
- **`Docs/decisions/AGENT_DECISIONS.md` uses two heading levels.** `##` for 0027–0031, `###` for
  the rest. Searching `^### DEC-` sees only part of the file and will report ids as missing.
  Use `^#{1,6}`.
- Builds only via `.\Tools\Safe-Build.ps1` from the repo root.
