---
artifact_contract: "ce-handoff/v1"
created_at: "2026-10-14T19:09:42Z"
title: "HomeWorld 2026-10-14 commit audit - T1-T7 audited, T7 fixed; 21169765 audited"
summary: "Audited the six 2026-10-14 commits as concern-based tasks (T1-T7). T1, T2, T3, T4, T5, T6 and T7 are repaired; T2 found the recorded field pass is REAL (editor log 2026-10-14 16:53Z) but predates befdc171, so the scene is not done until a desktop re-run. T3 had no code defect. T4 fixed the T1-3 soft-bounds gate in HomeWorldCharacter.cpp (DEC-0045). T7's edits were correct where made, but two files it touched still contradicted the bed rule; fixed here (DEC-0046). The unassigned 21169765 stands alone as the size-test pocket-kit sheet; audited, its numbers match the checker and it needs no fix (DEC-0047, DEC-0048). The rune/dusk sweep realigned three hand-owned stale copies and stopped at two human-owned ones (DEC-0049)."
keywords: ["HomeWorld", "commit-audit", "field-greybox", "soft-bounds", "skill-catalog", "doc-links", "handoff"]
cwd: "C:\\dev\\HomeWorld"
resume_focus: "T1-T7 are audited and their residual contradictions are fixed (DEC-0046, DEC-0049). Next real work is the desktop sitting that re-runs the field placer and verifier and walks L_Field (T2, T4), which also owes the two pad-relative route-gap lines (DEC-0048). Open for the Lead: DAYNIGHT_BIBLE.md 'bed or campsite' and the stamped fourteen-MUST list (DEC-0049); open for an agent: a re-grep pass for COMMANDS_AND_LOG_TAGS.md's drifted HomeWorldCharacter.cpp line column."
repository: "XylarDark/HomeWorld"
branch: "main"
head: "c0a201f1b45d57b6ecd3d3446d2c484cdceb0c26"
---

# SESSION_HANDOFF 2026-10-14 - commit audit

Audit of the six commits authored on 2026-10-14. Work is grouped by concern (T1-T7), not per commit.
T1-T7 are audited and the defects this audit found are fixed. The field scene is not done.

## Resume focus

T1-T7 are audited. Do not re-audit T1/T2/T3/T4/T5/T6 - they are committed and pushed - or T7, which
is fixed in DEC-0046. Do not touch the foreign working-tree files listed at the bottom. The next
real work is the desktop sitting that re-runs the field placer and verifier and walks `L_Field` (see T2
and T4 below), which also owes the two pad-relative route-gap lines for the size-test sheet
(DEC-0048). Open for the Lead: the `DAYNIGHT_BIBLE.md` "bed or campsite" call and the stamped
fourteen-MUST list that still carries the rune (see the T7 sweep, DEC-0049). Open for an agent: a
re-grep pass for `COMMANDS_AND_LOG_TAGS.md`'s drifted line column.

## Commit map (verified with `git show --stat --name-status`)

| SHA | Task | Concern |
|-----|------|---------|
| `34500e3c` | T3 | cottage sheet PNG + `L_Field_CONTEXT.md` + `L_Field_METRICS.md` (1398 lines) |
| `dadc5cf7` | T1 + T2 + T4 | 16 files: `L_Field.umap` (new) + `L_SizeTest.umap` + `place_field_greybox.py` (new) + `verify_field_greybox.py` (new) + `scene_placement.py` + `HomeWorldCharacter.cpp` + 10 docs (`FIELD.json`, `SCENE_SETUP.md`, `PLAY_TASKS.md`, `PROVE_TASKS.md`, 3 art docs, both `L_SizeTest` sheets) |
| `8bc982c8` | T6 | skill files + catalogs + `instruction-budget` ceiling |
| `21169765` | audited | `Docs/level/L_SizeTest_ROOM_PLAN.md` (+11) only; numbers match `check_pocket_kit`, no fix needed |
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

## Fixed - T4 (the T1-3 blocker)

`Source/HomeWorld/HomeWorldCharacter.{h,cpp}`. **DEC-0045.**

- **T1-3 (High, fixed):** the Tick soft-bounds gate keyed on the level name and recognised only
  "SizeTest", so on `L_Field` it forced `bBoundsEnabled = true` every frame and overrode the `false`
  `BeginPlay` had just set. The hero-island cylinder then applied - centre (-400, -50, 100) cm,
  `BoundsRadiusXY` 1050 cm (clamp max 10000), MinZ -400, MaxZ 600, push strength 1.2 - so the meadow
  was a ~21 m playpen, and it also fought the cliff tops (+8 m > MaxZ) and the shelf (-2850 cm <
  MinZ). `SCENE_SETUP.md` rule 5 says the new scene turns bounds off or matches centre/radius/Z; the
  29700 cm half-diagonal is not expressible, so off is the only option.
  - **Fix:** `BeginPlay` now sets a member `bGreyboxBodyLevel` (SizeTest or L_Field), and `Tick`
    branches on it - `if (SoftBoundsComponent && !bGreyboxBodyLevel)` - instead of re-testing the
    level name. It is the same flag the rest of `BeginPlay` already used, so there is no third copy
    of the greybox-body test.
  - **Verified:** `.\Tools\Safe-Build.ps1` exit 0 (`HomeWorldCharacter.cpp` compiled);
    `py -3 -m pytest Content/Python/tests -q` 366 passed; `npm run verify:fast` 6/6 PASSED.
  - **Not verified:** the walk itself - no live editor. A desktop session on `L_Field` is owed; the
    T2 lighting re-run is the same sitting.
- `scene_placement.py` (+47 in `dadc5cf7`) refuses to save on a failed check; that is the model T1-4
  followed.

## Fixed - T7 (`54858b1b`)

Docs-only. Files: `Docs/01_GDD_MVP.md`, `Docs/03_GAMEPLAY_MVP.md`, `Docs/VISION_BOARD.md`,
`Docs/canon/LOOPS.md`. **DEC-0046.**

- **Correct where edited.** The rune model is gone from `01_GDD_MVP.md` (fantasy, mode table, cycle
  rules 3-4, tame transport "rune stone" -> "the shrine", first-run order) and from
  `03_GAMEPLAY_MVP.md` §4; `VISION_BOARD.md` line 30 now matches the "two kinds of spirit" principle
  (line 40), dropping the old "Some creatures are always spirit" contradiction; `canon/LOOPS.md` step 4
  and the Meet row are right. All agree with the board (39, 89, 94, 95, 108-110).
- **T7-1 (Med, fixed):** `03_GAMEPLAY_MVP.md` contradicted itself. T7 rewrote §4's end-rule to "Dawn
  does not end the form", but §7 still drove `Dawn (V8 success) ... body form on homestead` with a phase
  table that swapped form at dusk and dawn, and §8 walked the demo through a "dusk form swap". §7 and
  §8 line 4 now read the bed rule. `DAYNIGHT_BIBLE.md` forbids a timer form swap, so this is alignment.
- **T7-2 (Med, fixed):** `canon/LOOPS.md` line 4 said the list below "still names a dusk form change",
  but T7's own edit to step 4 removed the only dusk line - the sentence was false. Reworded, and step 6
  now says the bed ends the form rather than rest / dawn.
- **T7-3 (Low, left):** `01_GDD_MVP.md` §3 rule 1 and V8 still read dawn -> body; the file's new header
  disclaims it ("the board wins"), so it is a labelled earlier cut. Left as-is.
- **Swept (DEC-0049):** the three stale copies an agent owns now read the settled rules.
  `HOMEWORLD_ROUTE.md:44` "the rune stone transports you and the bull" -> "the shrine brings you and the
  bull"; `08d_CONTENT_CANON.md:278` "spirit/body swap at dusk" -> "at the bed";
  `COMMANDS_AND_LOG_TAGS.md:186` dropped the `rune gate` token, which no Source file emits.
  - **Held, not committed here:** `COMMANDS_AND_LOG_TAGS.md` and `CANON_MAP.md` are being edited by the
    live virtue workstream at the same time (a `hw.Virtue.Read` regeneration, a virtue row). This
    session's one-line edits in both are in the working tree and land with that session's commit, not
    this one.
- **Left for the Lead (not alignment):** `Docs/DAYNIGHT_BIBLE.md:14` "sleep (bed **or campsite**)" is
  LOCKED and its campsite entry is a *mechanics* difference from the board's "the bed alone", so removing
  it changes gameplay; `Docs/guides/T0_HUMAN_DESKTOP_PIPELINE.md:82/86` is a Lead-stamped fourteen-MUST
  list whose items 7/11 carry the superseded M7 rune milestone, so rewriting them re-stamps beats. Both
  stopped on and named, not edited.
- **Left as history:** legacy `TaskLists/` already carries "pre-lock, do not implement" disclaimers.
- **New finding, not the sweep:** `COMMANDS_AND_LOG_TAGS.md`'s `HomeWorldCharacter.cpp:NNN` column
  drifted after its last regeneration (`54718be9`). Only that file changed in `Source/` since
  (`dadc5cf7`, `eff7fe09`), so ~22 handler-line refs are stale. It needs one re-grep pass.
- **Verified:** `py -3 -m pytest Content/Python/tests -q` 366 passed; `npm run verify:fast` 6/6 PASSED;
  `npm run docs:links` still `gone ... (46)`, unchanged.

## Audited - 21169765

**Stands alone and needs no fix** (DEC-0047, DEC-0048). `Docs/level/L_SizeTest_ROOM_PLAN.md` (+11)
records the size-test pocket kit: path stones and a fence run. It is the `L_SizeTest` sheet, tied to
`Content/Python/check_pocket_kit.py`; T3 is the `L_Field` sheet. Different map, different checker -
do not fold.

- **Audit result (no defect):** the section's numbers match the checker's constants exactly - path
  `(-9.5,-6.8)` to `(14.0,-6.0)`, one stone every 1.5 m (16 stones), fence `Y -11.5` across
  `X -15.0..-4.0` (6 pieces), shrine `(-16.2,-8.3)` at 4 m. `check_pocket_kit.run_host_checks()`
  passes (points=16, fences=6).
- **The one gap, deferred not broken:** `stated_route_gaps()` keeps a value only from a line naming a
  "pad edge" or a "route gap"; the plan states its run as a table, so `path_pos_x` / `fence_neg_y`
  soft_fail with "room plan states no route gap". Confirmed `stated_route_gaps(plan) == {}`. Soft_fail
  is the checker's by-design nudge and does not fail the run (only `closed_fail` sets a non-zero exit).
  Both gaps are measured against the `SM_Size_Island` pad, which is read in-editor and is larger than
  the cottage shell the plan describes, so the plan cannot state them from its own text - adding guessed
  numbers would be worse. Owed to the same desktop sitting as T2/T4.
- Its working tree also carries an EOL-only change from another session; leave it (one of the four
  foreign files).

## Scene status - NOT done

The field scene cannot be called done for the current revision. The pass on record is real but dated:
the editor log holds it at 2026-10-14 16:53Z, before `befdc171`. The committed `L_Field.umap` still
carries the old upward sun and no sky light or atmosphere, so a desktop session must re-run the
placer (which re-poses the sun and adds the lighting set) and then the verifier, in the open editor,
and re-log the pass. The code walk blocker (T1-3) is now fixed (T4); the walk is still unverified until
that editor sitting.

## Foreign working-tree files - do not touch or stage

Never `git add -A`; stage by explicit path. Another session has been writing in this tree all day, and by
mid-afternoon it was adding a whole virtue workstream. Anything not authored by this session is foreign.

Four files first seen at 2:25-2:30 PM (Rider MCP scouting, the size-test plan):

- `.cursor/mcp.json.example`
- `.cursor/rules/unreal-cpp.mdc`
- `Docs/handoffs/MARKETPLACE_POLICY_V1.md`
- `Docs/level/L_SizeTest_ROOM_PLAN.md`

The sin/virtue move, seen later:

- `VisionBoard/Core/VISION.md` (a new "Virtue attributes" section holding the seven pairs)
- `docs/TaskLists/TaskSpecs/SIN_VIRTUE_SPECTRUM.md` (its copy of the table deleted; now a pointer)

Then a live virtue-system workstream, still landing. It also co-edits two files this session touched:

- new `Source/HomeWorld/HomeWorldVirtue*.{cpp,h}` (component, spawn table, types, tests)
- `docs/VIRTUE_ATTRIBUTE_BIBLE.md`
- edits to `Source/HomeWorld/HomeWorld.cpp`, `HomeWorldHUD.cpp`, `HomeWorldInventorySubsystem.{cpp,h}`,
  `docs/CONSOLE_COMMANDS.md`, `Docs/VISION_BOARD.md`
- **co-edited with this session:** `Docs/CANON_MAP.md` (its virtue row; this session's DEC-range line is
  held in the tree) and `Docs/COMMANDS_AND_LOG_TAGS.md` (its `hw.Virtue.Read` regeneration; this
  session's `FORM` row line is held)

This list is a snapshot - the rule at the top is the durable one.

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
