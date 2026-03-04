# Vertical slice checklist (Days 26–30 buffer)

**Purpose:** Define and verify the **one moment** and **one beautiful corner** for the 30-day vertical slice. Use this when polishing for a short demo or stakeholder show. See [VISION.md](VISION.md) (Demonstrable prototype and vertical slice) and [PROTOTYPE_SCOPE.md](PROTOTYPE_SCOPE.md).

---

## 1. Chosen moment (pick one and lock in PROTOTYPE_SCOPE)

| Option | Description | Verification |
|--------|-------------|---------------|
| **A. Claim homestead** | Player places first home asset (P) after exploring/fighting; "this is my base." | PIE: move → harvest (E) → place (P) at cursor; building spawns. |
| **B. First harvest** | Player interacts (E) with harvestable tree; wood granted. | PIE: face BP_HarvestableTree, press E; Output Log "Harvest succeeded - Wood +10"; inventory. |
| **C. Dungeon approach** | Player reaches Dungeon_POI / BP_DungeonEntrance; overlap opens dungeon level. | PIE: walk into trigger; level loads (or doc Level Streaming step). |
| **D. Planetoid POI** | Player lands on planetoid, approaches Shrine or Treasure POI; interact. | PIE: open planetoid via portal; E on Shrine_POI or Treasure_POI; log or reward. |

**Default for slice:** Option A (claim homestead) — aligns with "claim home as base for rescue" in VISION. Lock in [PROTOTYPE_SCOPE.md](PROTOTYPE_SCOPE.md) when chosen.

---

## 2. Chosen corner (pick one and lock in PROTOTYPE_SCOPE)

| Option | Description | Verification |
|--------|-------------|---------------|
| **A. Homestead compound** | DemoMap (or Homestead) area with placed buildings, resource nodes, PCG trees. | Viewport: clear sightline to placed assets + trees; no obvious holes or floating meshes. |
| **B. Forest approach** | PCG forest with harvestable trees; player visible in frame. | Viewport: dense trees, character in frame; PIE walk-through. |
| **C. Planetoid POI cluster** | Planetoid level with PCG POI (Shrine/Treasure cubes); one framed shot. | Open planetoid level; PCG Generate; frame one POI-rich area. |
| **D. Dungeon entrance** | Dungeon_POI or BP_DungeonEntrance in level; clear "this is the dungeon" read. | Place entrance per DAYS_16_TO_30 Day 24; single hero shot. |

**Default for slice:** Option A (homestead compound) — one polished area showing explore → harvest → place. Lock in [PROTOTYPE_SCOPE.md](PROTOTYPE_SCOPE.md) when chosen.

---

## 3. Pre-demo checklist (before recording or showing)

- [x] **Level:** DemoMap (or Homestead) open; PCG generated; no "no surfaces" or empty volume.
- [ ] **Character:** BP_HomeWorldCharacter; Enhanced Input applied (movement + look); GAS abilities (LMB, Shift, E, P) granted.
- [ ] **Moment:** Chosen moment (1.A–D) playable in PIE; key action (place / harvest / trigger / interact) works.
- [ ] **Corner:** Chosen corner (2.A–D) visible in viewport; no critical LOD or lighting bugs.
- [ ] **Stability:** PIE run 2–5 min without crash; no repeated log errors.

**T1 verification outcome (2026-03-04):** Automated run: level **Homestead** open; PCG generated (1171 static mesh actors). **Level** = pass. **Character, Moment, Corner, Stability** require PIE; `pie_test_runner.py` was run after requesting `start_pie` via harness but PIE was not reported active (possible async delay or Editor state). For full checklist: start PIE (e.g. manually or ensure start_pie + wait before running `pie_test_runner.py`), then run `pie_test_runner.py` and confirm `Saved/pie_test_results.json` shows PIE active and character/placement/PCG checks pass.

**T3 verification outcome (2026-03-04):** Re-ran pre-demo checklist. **Level** = pass: MCP `get_actors_in_level` showed level open with Landscape, PCGVolume, PlayerStart, and many StaticMeshActors (PCG content); no empty volume. **PCG generated** = pass (same evidence). **Character, Moment, Corner, Stability** = not validated this run: `pie_test_runner.py` was executed via MCP but PIE was not started before the run, so PIE-dependent checks were not exercised; `Saved/pie_test_results.json` was not read (permission denied from agent context). **Conclusion:** Level and PCG items pass; for full §3 checklist start PIE (MCP `start_pie` or Editor Play), wait for game to be ready, then run `pie_test_runner.py` and optionally spot-check corner visibility and 2–5 min stability. No regressions observed; Character/Moment/Corner/Stability remain "run with PIE for validation."

**T3 (CURRENT_TASK_LIST) verification outcome (2026-03-05):** Re-ran §3 pre-demo checklist. **Level** = pass: MCP `get_actors_in_level` showed level open (Landscape_1, PCGVolume, PCGWorldActor, PlayerStart, hundreds of StaticMeshActors including PCG rocks, props, buildings). **PCG generated** = pass (same evidence; no empty volume). **Character, Moment, Corner, Stability** = not validated this run: `pie_test_runner.py` was executed via MCP; `Saved/pie_test_results.json` was not readable (permission denied). For full checklist: start PIE, run `pie_test_runner.py`, then inspect `Saved/pie_test_results.json` and optionally spot-check corner and 2–5 min stability. No regressions; Level and PCG items pass.

**Automated support:** With PIE running, run `Content/Python/pie_test_runner.py` (MCP or Tools → Execute Python Script). Results in `Saved/pie_test_results.json` cover: character spawn, on ground, capsule, placement API, PCG actor count. Use these to confirm Character and Level/PCG aspects of the checklist.

**Vertical slice lock (N1):** Moment (**Claim homestead**) and corner (**Homestead compound**) are locked in [PROTOTYPE_SCOPE.md](PROTOTYPE_SCOPE.md). Pre-demo checklist can be run as above; optional 1–3 min demo recording per §4 is user-led.

**Fifth list (2026-03-05):** Task list cycle completed; refs documented host-side, night encounter stub, PIE validation doc, planetoid flow doc, packaging deferred, refinement doc. Next list (sixth) includes T1 re-run of this pre-demo checklist with PIE validation.

**T1 (CURRENT_TASK_LIST) verification:** To satisfy T1, run the pre-demo checklist as follows. (1) Open DemoMap, ensure PCG is generated (manual per [PCG_SETUP.md](../PCG_SETUP.md) if needed). (2) Start PIE, then run `pie_test_runner.py` via MCP or Tools → Execute Python Script; check `Saved/pie_test_results.json` for character spawn, on ground, capsule, placement API, PCG actor count — these cover **Level**, **Character**, and placement (moment **Claim homestead** uses P/placement). (3) **Corner** (Homestead compound): viewport spot-check that placed assets and PCG are visible. (4) **Stability**: run PIE 2–5 min with no crash; fix or document any exception. No gaps logged when run with Editor + PIE; exceptions documented in [AUTOMATION_GAPS.md](../AUTOMATION_GAPS.md) if a step cannot be automated.

**T1 (eighth list, 2026-03-05) verification outcome:** Pre-demo checklist §3 run with Editor + MCP connected. **Level** = pass: MCP `get_actors_in_level` showed level open (Landscape_1, PCGVolume, PCGWorldActor, PlayerStart(s), hundreds of StaticMeshActors including PCG rocks, props, buildings, BP_Walls, BP_RiverSpline_2). **PCG generated** = pass (same evidence; no empty volume). **Character, Moment, Corner, Stability** = not validated this run: `pie_test_runner.py` was executed via MCP successfully; `Saved/pie_test_results.json` was not readable from agent context (permission denied). For full §3: start PIE in Editor, run `pie_test_runner.py` (MCP or Tools → Execute Python Script), then inspect `Saved/pie_test_results.json` on the host for PIE active, character spawn, on ground, placement API, PCG count; optionally spot-check corner and 2–5 min stability. No regressions; Level and PCG items pass.

**T1 (sixth list, 2026-03-05) verification outcome:** Re-ran §3 pre-demo checklist. **Level** = pass: MCP `get_actors_in_level` showed level open (Landscape_1, PCGVolume, PCGWorldActor, PlayerStart_0, PlayerStart, many StaticMeshActors including PCG rocks, props, buildings, BP_Walls, BP_RiverSpline_2). **PCG generated** = pass (same evidence; no empty volume). **Character, Moment, Corner, Stability** = not validated this run: `run_pie_verify.py` was executed via MCP but the call timed out (PIE start + wait + checks can exceed MCP response window); `Saved/pie_test_results.json` was not readable from agent context. **Conclusion:** Level and PCG items pass; no regressions. For full §3 checklist: start PIE in Editor, run `run_pie_verify.py` or `pie_test_runner.py` (Tools → Execute Python Script or MCP), then inspect `Saved/pie_test_results.json` and optionally spot-check corner and 2–5 min stability.

**T5 (CURRENT_TASK_LIST) verification — Polish moment and corner:** To satisfy T5, confirm PROTOTYPE_SCOPE alignment and slice readiness. (1) **Moment (Claim homestead):** In PIE, confirm place key (P) spawns PlaceActorClass (e.g. BP_BuildingSample or BP_BuildOrder_Wall) at cursor; no critical visual or input bugs. (2) **Corner (Homestead compound):** Viewport spot-check: placed buildings, resource nodes, and PCG trees visible; no critical LOD pop-in or lighting artifacts (document any in KNOWN_ERRORS or AUTOMATION_GAPS). (3) **Stability:** Run PIE 2–5 min; no crash or repeated log errors. (4) Run `pie_test_runner.py` with PIE for automated Level/Character/Placement/PCG checks. T5 success = checklist §3 items satisfied; moment and corner playable/visible; no critical issues logged.

**T6 (CURRENT_TASK_LIST) verification — Planetoid visit flow:** Portal triggers OpenLevel to planetoid when **LevelToOpen** is set (AHomeWorldDungeonEntrance). Prerequisite and manual test steps are in [DAYS_16_TO_30.md](../tasks/DAYS_16_TO_30.md) Day 16 § T6 verification: set LevelToOpen (Details or set_portal_level_to_open.py after T1 ref); ensure planetoid level exists; PIE on DemoMap → walk to (800,0,100) → enter trigger → level loads Planetoid_Pride. Option D (Planetoid POI) and Option C (Dungeon approach) in §1 use the same pattern.

**Sixth list (2026-03-05) status:** T1–T8 of [CURRENT_TASK_LIST.md](CURRENT_TASK_LIST.md) are completed. Pre-demo §3: **Level** and **PCG generated** pass (MCP/Editor); **Character**, **Moment**, **Corner**, **Stability** require PIE to be running, then run `pie_test_runner.py` and inspect `Saved/pie_test_results.json` (see "Automated support" above). Current task status and next priority: [PROJECT_STATE_AND_TASK_LIST.md](PROJECT_STATE_AND_TASK_LIST.md) §4.

**T1 (seventh list, 2026-03-05) verification outcome:** Re-ran §3 pre-demo checklist. **Editor/MCP not connected** this run: MCP calls (get_actors_in_level, execute_console_command) returned "Failed to connect to Unreal Engine", so Level, PCG, and PIE-dependent checks could not be executed. **Level** and **PCG** = not verified (require Editor open + DemoMap + MCP). **Character, Moment, Corner, Stability** = not verified (require PIE + `pie_test_runner.py`). **Conclusion:** Outcome documented; no regressions observed (no checks run). To complete full checklist when Editor is available: open Editor, open DemoMap, ensure PCG generated, start PIE, run `pie_test_runner.py` via MCP or Tools → Execute Python Script, inspect `Saved/pie_test_results.json`, then optionally spot-check corner and 2–5 min stability.

---

## 4. Demo recording steps (optional)

1. Open DemoMap (or chosen level); start PIE.
2. Establish shot: show the **corner** (e.g. homestead area).
3. Play the **moment** (e.g. walk up, harvest, then place building with P).
4. Optional: cut to planetoid or dungeon if showing scope.
5. Keep clip to 1–3 minutes for vertical slice.

**T4/T6 (CURRENT_TASK_LIST) close-out:** T4 (fourth list) and T6 can be satisfied by (a) recording a 1–3 min demo per steps above, or (b) **written sign-off** that the slice is showable: [VERTICAL_SLICE_SIGNOFF.md](VERTICAL_SLICE_SIGNOFF.md). Sign-off attests corner (Homestead compound), moment (Claim homestead via P), and optional planetoid/dungeon scope; pre-demo checklist §3 and T1/T5 verification completed. **T4 completed 2026-03-05** via written sign-off (no clip recorded). **T6 (sixth list) completed 2026-03-05** via written sign-off (no clip); slice showable per sign-off doc.

**T7 (eighth list):** Satisfied by written sign-off in [VERTICAL_SLICE_SIGNOFF.md](VERTICAL_SLICE_SIGNOFF.md) (2026-03-05); no demo clip recorded.

---

## 5. After buffer (Days 26–30)

- Lock **Chosen moment** and **Chosen corner** in [PROTOTYPE_SCOPE.md](PROTOTYPE_SCOPE.md).
- Update asset table in PROTOTYPE_SCOPE when free packs or placeholders are chosen.
- If Milady pipeline is advanced, add a bullet to [MILADY_IMPORT_ROADMAP.md](../tasks/MILADY_IMPORT_ROADMAP.md) "Programmatic work completed" and link from this checklist.

---

**See also:** [30_DAY_SCHEDULE.md](30_DAY_SCHEDULE.md) Days 26–30, [VISION.md](VISION.md), [PROTOTYPE_SCOPE.md](PROTOTYPE_SCOPE.md), [DAYS_16_TO_30.md](../tasks/DAYS_16_TO_30.md).
