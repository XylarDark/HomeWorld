---
artifact_contract: "ce-handoff/v1"
created_at: "2026-10-14T19:09:42Z"
title: "HomeWorld 2026-10-14 commit audit - T1/T2/T5/T6 fixed; T3/T4/T7 open"
summary: "Audited the six 2026-10-14 commits as concern-based tasks (T1-T7). T1, T2, T3, T5 and T6 are repaired; T2 found the recorded field pass is REAL (editor log 2026-10-14 16:53Z) but predates befdc171, so the scene is not done until a desktop re-run. T3 had no code defect. T4, T7 and the unassigned 21169765 are still to audit."
keywords: ["HomeWorld", "commit-audit", "field-greybox", "soft-bounds", "skill-catalog", "doc-links", "handoff"]
cwd: "C:\\dev\\HomeWorld"
resume_focus: "Audit T4 (HomeWorldCharacter.cpp, which owns the T1-3 soft-bounds blocker), then T7, and place 21169765. The field lighting re-run is owed to a desktop session."
repository: "XylarDark/HomeWorld"
branch: "main"
head: "c0a201f1b45d57b6ecd3d3446d2c484cdceb0c26"
---

# SESSION_HANDOFF 2026-10-14 - commit audit

Audit of the six commits authored on 2026-10-14. Work is grouped by concern (T1-T7), not per commit.
Three tasks are fixed and pushed. Three are open. The field scene is not done.

## Resume focus

Audit **T4** next, then **T7**, and decide where **21169765** belongs. Do not re-audit
T1/T2/T3/T5/T6 - they are committed and pushed. Do not touch the four foreign working-tree files listed
at the bottom. The field lighting re-run is owed to a desktop session (see T2 below).

## Commit map (verified with `git show --stat --name-status`)

| SHA | Task | Concern |
|-----|------|---------|
| `34500e3c` | T3 | cottage sheet PNG + `L_Field_CONTEXT.md` + `L_Field_METRICS.md` (1398 lines) |
| `dadc5cf7` | T1 + T2 + T4 | 16 files: `L_Field.umap` (new) + `L_SizeTest.umap` + `place_field_greybox.py` (new) + `verify_field_greybox.py` (new) + `scene_placement.py` + `HomeWorldCharacter.cpp` + 10 docs (`FIELD.json`, `SCENE_SETUP.md`, `PLAY_TASKS.md`, `PROVE_TASKS.md`, 3 art docs, both `L_SizeTest` sheets) |
| `8bc982c8` | T6 | skill files + catalogs + `instruction-budget` ceiling |
| `21169765` | unassigned | `Docs/level/L_SizeTest_ROOM_PLAN.md` (+11) only |
| `4e9cb4b8` | T5 | `check_doc_links.py` + `start_editor.py` + tests + `docs/KNOWN_ERRORS.md` |
| `54858b1b` | T7 | docs-only: `01_GDD_MVP.md`, `03_GAMEPLAY_MVP.md`, `VISION_BOARD.md`, `canon/LOOPS.md` |

`dadc5cf7`'s subject undersells it: it also changes `L_SizeTest.umap` and `scene_placement.py`.

## Done and pushed (do not re-open)

Pushed as `34500e3c..c0a201f1`. `git rev-list --left-right --count origin/main...HEAD` is `0 0`.

**T1 - `befdc171`** `place_field_greybox.py`, `verify_field_greybox.py`, new
`Content/Python/tests/test_place_field_greybox.py`.
- Sun was `Rotator(-45.0, 30.0, 0.0)` positionally. Positional order is `(roll, pitch, yaw)`, so
  the elevation landed in the inert roll slot and the sun lit upward. Now keyword args, re-posed
  every run, plus SkyLight and SkyAtmosphere (matching `place_size_test.py:185-194`).
- A missing mesh used to save the map and exit 0. Now fails closed: records the failure, does not
  save, exits non-zero.
- Verifier now checks one directional light, the sun's pitch/yaw, and mesh bottoms against z = 0
  (+/- 2 cm) for pine/tree/herb/bull. Mass cubes intentionally sit below zero and are excluded.

**T5 - `22b87116`** `check_doc_links.py`, `start_editor.py`, both test files,
`docs/KNOWN_ERRORS.md`, `package.json`.
- Directory links and `%20` links were reported dead; `start_editor` read a time-of-check result
  instead of `process.poll() is None`; two dead shared-path rows in `KNOWN_ERRORS.md` fixed; added
  non-gating `npm run editor:start` and `npm run docs:links`. Checker `gone` count 55 -> 46.
- **Deliberately not done, per agreed scope:** the remaining dead links are not repaired and no CI
  gate was added.

**T6 - `b8ae30e4`** swapped `ue-editor-ui` trees (body + `paths:` in `.cursor/skills`, pointer in
`.agents/skills`), rewrote the `instruction-budget.js` comment with gate-exact numbers, fixed both
catalogs, removed the empty `ue57-api-check` dir. Recorded as **DEC-0041**. T6-4 and T6-6 were
withdrawn (a `paths:` field is real; counting disabled descriptions is deliberate and asserted).

**T2 - `748216e6`** `verify_field_greybox.py`, new `Content/Python/tests/test_verify_field_greybox.py`,
`Docs/context/PLAY_TASKS.md`, `Docs/level/L_Field_CONTEXT.md`, `AGENT_DECISIONS.md`.
- **Correction to this handoff's first version:** it claimed the recorded `field_greybox: CHECK PASS`
  had no open-editor evidence. That was wrong. `Saved/Logs/HomeWorld.log` holds two passes on
  2026-10-14, and the 16:51:35-16:53:53Z run matches `dadc5cf7`'s script text exactly, two minutes
  before that commit at 16:56:01Z. The claim was honestly evidenced for `dadc5cf7`.
- But the evidence is **stale against main**: `befdc171` (18:31:52Z) changed both scripts after the
  log ends (17:49:18Z), and the saved map still has one `Field_Sun` (posed `Rotator(-45,30,0)`, so it
  lights upward) and zero `SkyLight`/`SkyAtmosphere`. So the current scripts have never run.
- **Fixed:** `sheet_spots()` states where every sheet-pinned mass belongs; `check()` compares each
  built actor to it within 10 cm. The verifier previously compared the sheet only with itself.
- The two docs that quote the pass now say which revision it covers and that a re-run is owed;
  **the scene is not read as done**. Test ownership of "done" is human (`docs/human-use/OWNERSHIP.md`
  line 28), so this was put to the owner as a numbered choice before any edit.
- Still open, not fixed here: `Saved/` is gitignored, so the proof is not re-checkable from the repo;
  the MCP response for a passing run is `success: true` regardless of the script's exit code, so the
  verdict lives only in log text; neither field script is wired to a gate; `FIELD.json`'s `measured`
  stays null. Decisions **DEC-0042**, **DEC-0043**.

## T2 - owed to a desktop session

Re-run the placer, then the verifier, in the open editor on `L_Field`, and re-log the pass. Only
then is the field greybox done for the current revision. A clean log is not evidence by itself; the
run has to be in the open editor on this tree.

## T3 - audited, no code defect (`c0a201f1`)

`34500e3c`. **No High or Med defect.** The committed map was built from exactly the committed sheet:
`L_Field.umap` holds 230 `SM_Field_` labels - 7 mass cubes/cliffs + 71 pines (`S_*` 35, `W_*` 35,
`Corner` 1) + 8 trees + 144 herb nodes - every sheet label present exactly once, no duplicate labels.
The prose is internally consistent: 104 centres = 70 single + 28 dual + 6 triple = 144 nodes, min
centre spacing 30.03 m, 52 bulls at exactly 2.50 m and 52 with min 8.03 m, 36 stations, 8 meadow
pines >= 42.9 m apart, river `sx` 7. The PNG is a real image (IHDR + 17 IDAT, ~1.03 MB payload),
linked from 4 art docs. `npm run docs:links` flags no field path.
- **Withdrawn, my error:** I first measured bull-to-herb distance to the nearest herb *node* and read
  a 7.77 m "violation" of the sheet's ">= 8 m" rule. Measured to the nearest herb **centre** - which
  is what "beside a herb" means - it is 8.03 m, and the prose is exactly right.
- **Fixed:** the seed line; a CANON_MAP row for the field scene; CANON_MAP's decision range
  (0036 -> 0044, stale since DEC-0037). DEC-0044.
- **T3-3, history-only, nothing to fix:** `dadc5cf7` referenced T3's files before they existed - its
  placer reads `L_Field_METRICS.md` (absent) and its art docs link `HS_Cottage_sheet_plan.png`
  (absent). `34500e3c` added both 27 s later.
- **Not done:** coordinates were not re-measured against the map - that needs the editor. Only the
  label set and the counts were checked.
- **Nit, not fixed:** the sheet's per-bull `beside` field is read by nothing, and the verifier
  recomputes "beside" with a 4 m cutoff against the sheet's stated 2.5 m rule.

## Open - T4 (owns the T1-3 blocker)

`Source/HomeWorld/HomeWorldCharacter.cpp`.

- **T1-3 (High, unfixed):** line 341 forces `bBoundsEnabled = true` every Tick on any level name
  lacking "SizeTest". `dadc5cf7` treated `L_Field` as a greybox body for mesh/walk (lines 237, 374)
  but left this gate alone. Defaults in `HomeWorldSoftBoundsComponent.h`: centre (-400, -50, 100) cm,
  `BoundsRadiusXY` 1050 cm (clamp max 10000), MinZ -400, MaxZ 600. The player is pushed back beyond
  ~10.5 m (strength 1.2 > input 1.0), so the meadow is a ~21 m playpen; it also fights the cliff tops
  (+8 m > MaxZ) and the shelf (-2850 cm < MinZ). `SCENE_SETUP.md` rule 5 requires the new scene to
  turn bounds off or match centre/radius/Z; the 29700 cm half-diagonal is not expressible, so bounds
  must be turned off. Cannot be fixed from the map or a BP - the Tick assignment overrides every
  frame. Suggested fix: branch on the greybox-body flag rather than the level name.
- `scene_placement.py` (+47 in `dadc5cf7`) refuses to save on a failed check; that is the model T1-4
  followed.

## Open - T7

`54858b1b`. Docs-only: "Make the bed the form change in the older design files, and match the shape
line to the spirit pair." Files: `Docs/01_GDD_MVP.md`, `Docs/03_GAMEPLAY_MVP.md`,
`Docs/VISION_BOARD.md`, `Docs/canon/LOOPS.md`. Check the edits against `VISION_BOARD.md` canon
(bed = the form change) and cross-file consistency. Docs only - no product code.

## Open - 21169765

`Docs/level/L_SizeTest_ROOM_PLAN.md` (+11) only. Subject: "Record the size-test path and fence run
that the pocket-kit check already measures." No task assigned yet. Decide whether it folds into T3
(the other docs/level sheet) or stands alone.

## Scene status - NOT done

The field scene cannot be called done for the current revision. The pass on record is real but dated:
the editor log holds it at 2026-10-14 16:53Z, before `befdc171`. The committed `L_Field.umap` still
carries the old upward sun and no sky light or atmosphere, so a desktop session must re-run the
placer (which re-poses the sun and adds the lighting set) and then the verifier, in the open editor,
and re-log the pass. The walk also stays blocked on T1-3.

## Foreign working-tree files - do not touch or stage

Four files were written by another session (2:25-2:30 PM), all Rider MCP scouting or the size-test
plan. Leave them alone; never `git add -A`:

- `.cursor/mcp.json.example`
- `.cursor/rules/unreal-cpp.mdc`
- `Docs/handoffs/MARKETPLACE_POLICY_V1.md`
- `Docs/level/L_SizeTest_ROOM_PLAN.md`

## Gates and tooling

- `py -3 -m pytest Content/Python/tests -q` (currently 366 passed)
- `npm run verify:fast` (6 stages, currently PASSED)
- No live editor: `unrealMCP.get_actors_in_level` returns `null`. The proof of a field run is the log
  at `Saved/Logs/HomeWorld.log`, which is gitignored - grep it for `field_greybox:`.
- `.umap` files are Git LFS pointers; working-tree copies are materialized and greppable. In
  PowerShell 5.1 read them with `[System.IO.File]::ReadAllBytes` + `[Text.Encoding]::ASCII`
  (`-Encoding Latin1` does not exist).
- Commit style: Conventional Commits (573 of 906 commits). Stage by explicit path.
- The `post-commit` / `pre-push` hooks are `git-lfs` only (no gate, no commit-msg check).
- PowerShell mangles `$`, quotes and backticks in inline `python -c` / `node -e` - write a script to
  `C:\Users\User\AppData\Local\Temp\opencode\` instead. Long reads truncate - re-read with offset.
