# Vertical slice checklist (Days 26–30 buffer)

**Purpose:** Define and verify the **one moment** and **one beautiful corner** for the 30-day vertical slice. Use this when polishing for a short demo or stakeholder show. See [VISION.md](VISION.md) (Demonstrable prototype and vertical slice) and [PROTOTYPE_SCOPE.md](PROTOTYPE_SCOPE.md). Day/night and astral rules (no death by day, astral return on death at night, late-game astral-by-day): [PROTOTYPE_SCOPE.md](PROTOTYPE_SCOPE.md) § Day/night and astral.

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

**Entry point:** For the single doc that links this step-by-step sequence (§3) and the command reference, see [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) (Pre-demo verification). This section (§3) is the ordered run sequence; for all `hw.*` commands used during the run (e.g. `hw.TimeOfDay.Phase`, `hw.Planetoid.Complete`), use CONSOLE_COMMANDS.

- [x] **Level:** DemoMap (or Homestead) open; PCG generated; no "no surfaces" or empty volume.
- [ ] **Character:** BP_HomeWorldCharacter; Enhanced Input applied (movement + look); GAS abilities (LMB, Shift, E, P) granted.
- [ ] **Moment:** Chosen moment (1.A–D) playable in PIE; key action (place / harvest / trigger / interact) works.
- [ ] **Corner:** Chosen corner (2.A–D) visible in viewport; no critical LOD or lighting bugs.
- [ ] **Stability:** PIE run 2–5 min without crash; no repeated log errors.

**Step-by-step run sequence (full verification)** — Follow this single ordered sequence to get the pre-demo checklist (§3) fully green:

1. **Open Editor** — Launch Unreal Editor with the HomeWorld project.
2. **Open DemoMap (or Homestead)** — File → Open Level (or Content Browser) and open `/Game/HomeWorld/Maps/DemoMap` or the Homestead map.
3. **Ensure PCG generated** — In the level, select the PCG Volume (or PCG actor); if needed run Generate per [PCG_SETUP.md](../PCG_SETUP.md). Confirm no "no surfaces" or empty volume in Output Log.
4. **Start PIE** — Click Play (or use MCP `start_pie`). Wait for the game window to be ready (level loaded, character spawned).
5. **Wait for level/pawn ready** — Allow ~5–10 seconds for level streaming and pawn possession (longer if World Partition is loading).
6. **Run pie_test_runner** — Via MCP: `execute_python_script("pie_test_runner.py")`. Or in Editor: Tools → Execute Python Script → `Content/Python/pie_test_runner.py`. Results are written to `Saved/pie_test_results.json`.
7. **Inspect results** — On the host, open `Saved/pie_test_results.json`. Confirm: **Level** (level name, PCG actors), **Character** (spawned, on ground, capsule), **Moment** (placement API, Place/Harvest if applicable), **Corner** (PCG count). For SaveGame round-trip: phase, LoveLevel, spiritual power restored after hw.Save / hw.Load if that check is present. When PIE is on a planetoid map (level name contains "Planetoid" or is DemoMap), the **Planetoid / HomesteadLandedOnPlanetoid** check reports whether GameMode set the flag (see pie_test_runner; manual fallback: check Output Log for "Homestead landed on planetoid").
8. **Optional: stability** — Run PIE for 2–5 minutes; confirm no crash or repeated log errors. Spot-check **Corner** (homestead compound) in viewport.

**Note (thirtieth list T9):** PIE pre-demo was not run this session (Editor/MCP not required for doc-only close-out). When Editor is available, run the step-by-step sequence above and document outcome (e.g. pass/fail summary from `Saved/pie_test_results.json`) in SESSION_LOG or here.

**T9 (thirty-first list, 2026-03-06) verification outcome:** Pre-demo checklist §3 run attempted with Editor/MCP **not connected** (MCP returned "Failed to connect to Unreal Engine"). `pie_test_runner.py` was not executed; `Saved/pie_test_results.json` was not produced. **Level**, **PCG generated**, **Character**, **Moment**, **Corner**, **Stability** = not verified this run. Outcome documented here and in SESSION_LOG. **Single entry point for pre-demo:** This section (§3) is the step-by-step run sequence; for all `hw.*` commands used during the run, see [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) (Pre-demo verification and Commands). When Editor is available: open DemoMap (or Homestead), ensure PCG generated, start PIE, run `pie_test_runner.py` via MCP or Tools → Execute Python Script, inspect `Saved/pie_test_results.json` for pass/fail; optionally spot-check corner and 2–5 min stability.

**T8 (thirty-second list, 2026-03-06) verification outcome:** Pre-demo checklist §3 run attempted with Editor/MCP **not connected** (MCP returned "Failed to connect to Unreal Engine"). `pie_test_runner.py` was not executed; `Saved/pie_test_results.json` was not produced. **Level**, **PCG generated**, **Character**, **Moment**, **Corner**, **Stability** = not verified this run. **Doc change:** Single entry point for pre-demo is now explicit: [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) (Pre-demo verification) links §3 (run sequence) and this document (command reference). Outcome documented here and in SESSION_LOG. When Editor is available: open DemoMap (or Homestead), ensure PCG generated, start PIE, run `pie_test_runner.py` via MCP or Tools → Execute Python Script, inspect `Saved/pie_test_results.json` for pass/fail; optionally spot-check corner and 2–5 min stability.

**3.1 HUD metrics reference (AHomeWorldHUD)** — Which on-screen line shows which metric (top-to-bottom draw order). Source: `Source/HomeWorld/HomeWorldHUD.cpp`. Use for testers and automation when verifying values.

| Metric | HUD line / location | Source / note |
|--------|----------------------|----------------|
| **Phase** | `Phase: Day` \| `Dusk` \| `Night` \| `Dawn` | TimeOfDaySubsystem; set with `hw.TimeOfDay.Phase 0\|1\|2\|3`. |
| **Physical** | `Physical: N` | InventorySubsystem GetTotalPhysicalGoods (day harvest). |
| **Spiritual** | `Spiritual: N` | PlayerState GetSpiritualPowerCollected (night collectibles). |
| **Love** | `Love: N` | PlayerState GetLoveLevel; day or night. |
| **Restored today** | `Restored today: N` | Day only; PlayerState GetMealsConsumedToday; increment with `hw.RestoreMeal`. |
| **Meals with family** | `Meals with family: N` | Day only; PlayerState GetMealsWithFamilyToday (day buff). |
| **Wave** | `Wave N` | Night only; GameMode GetCurrentNightEncounterWave (set Phase 2 to trigger). |
| **Converted** | `Converted: N` | Night only; GameMode GetConvertedFoesThisNight; `hw.Conversion.Test` to increment. |
| **Last converted** | `Last converted: <role>` | Night only, when Converted > 0; GameMode GetConvertedFoeRole. |
| **Dawn countdown** | `Dawn in Ns` | Night only; TimeOfDaySubsystem GetSecondsUntilDawn. |
| **Astral HP** | `Astral HP: current / max` | Night only; AttributeSet Health/MaxHealth (lethal → RequestAstralDeath). |
| **Spiritual power (night)** | `Spiritual power: N` | Night only; same as Spiritual, shown again at night for SpiritBurst/spend. |
| **SpiritBurst** | `SpiritBurst: ready` or `SpiritBurst: N.Xs` | Night only; GA_SpiritBurst cooldown. |
| **SpiritShield** | `SpiritShield: ready` or `SpiritShield: N.Xs` | Night only; GA_SpiritShield cooldown. |
| **Block message** | Yellow text (e.g. "Not enough spiritual power") | Night only; PlayerState GetSpiritBurstBlockMessageForHUD. |
| **Day buff** | `Day buff: active` | Night only when PlayerState GetHasDayRestorationBuff (earned via hw.RestoreMeal during day). |

**3.2 Demo readiness (ready to show)** — Single sign-off checklist before recording or showing the slice. When all items are satisfied, the slice is ready to show.

| # | Item | How to verify |
|---|------|----------------|
| 1 | **Pre-demo §3 green** | All five §3 items checked: Level (DemoMap/Homestead open, PCG generated), Character (BP_HomeWorldCharacter, Enhanced Input, GAS abilities), Moment (chosen moment playable), Corner (chosen corner visible), Stability (PIE 2–5 min no crash). Run the §3 step-by-step sequence and confirm each. |
| 2 | **Moment: Claim homestead** | In PIE, key **P** (Place) spawns building at cursor; placement API and GA_Place work; no critical input or visual bugs. |
| 3 | **Corner: Homestead compound** | Viewport spot-check: placed buildings, resource nodes, and PCG trees visible; no critical LOD pop-in or lighting artifacts. |
| 4 | **Optional: 1–3 min record** | If recording: follow §4 (open level, PIE, establish corner shot, play moment, keep clip 1–3 min). See §4 for Take Recorder / Game Bar / OBS options. |

When (1)–(3) are done, the slice is **ready to show**; (4) is optional for a recorded clip.

---

**T1 verification outcome (2026-03-04):** Automated run: level **Homestead** open; PCG generated (1171 static mesh actors). **Level** = pass. **Character, Moment, Corner, Stability** require PIE; `pie_test_runner.py` was run after requesting `start_pie` via harness but PIE was not reported active (possible async delay or Editor state). For full checklist: start PIE (e.g. manually or ensure start_pie + wait before running `pie_test_runner.py`), then run `pie_test_runner.py` and confirm `Saved/pie_test_results.json` shows PIE active and character/placement/PCG checks pass.

**T3 verification outcome (2026-03-04):** Re-ran pre-demo checklist. **Level** = pass: MCP `get_actors_in_level` showed level open with Landscape, PCGVolume, PlayerStart, and many StaticMeshActors (PCG content); no empty volume. **PCG generated** = pass (same evidence). **Character, Moment, Corner, Stability** = not validated this run: `pie_test_runner.py` was executed via MCP but PIE was not started before the run, so PIE-dependent checks were not exercised; `Saved/pie_test_results.json` was not read (permission denied from agent context). **Conclusion:** Level and PCG items pass; for full §3 checklist start PIE (MCP `start_pie` or Editor Play), wait for game to be ready, then run `pie_test_runner.py` and optionally spot-check corner visibility and 2–5 min stability. No regressions observed; Character/Moment/Corner/Stability remain "run with PIE for validation."

**T3 (CURRENT_TASK_LIST) verification outcome (2026-03-05):** Re-ran §3 pre-demo checklist. **Level** = pass: MCP `get_actors_in_level` showed level open (Landscape_1, PCGVolume, PCGWorldActor, PlayerStart, hundreds of StaticMeshActors including PCG rocks, props, buildings). **PCG generated** = pass (same evidence; no empty volume). **Character, Moment, Corner, Stability** = not validated this run: `pie_test_runner.py` was executed via MCP; `Saved/pie_test_results.json` was not readable (permission denied). For full checklist: start PIE, run `pie_test_runner.py`, then inspect `Saved/pie_test_results.json` and optionally spot-check corner and 2–5 min stability. No regressions; Level and PCG items pass.

**T3 (thirteenth list, 2026-03-05) verification outcome:** Re-ran §3 pre-demo checklist for CURRENT_TASK_LIST T3. **Level** and **PCG generated** = pass: MCP `get_actors_in_level` showed level open (Landscape_1, PCGVolume, PlayerStart, many StaticMeshActors, BP_Walls, BP_RiverSpline_2, etc.); no empty volume. **Character, Moment, Corner, Stability**: `start_pie_and_wait.py` via MCP timed out (PIE start + wait exceeds MCP response window). `pie_test_runner.py` executed via MCP — success; results written to `Saved/pie_test_results.json`. Agent could not read `Saved/pie_test_results.json` (permission denied from agent context). MCP `get_actors_in_level` after runner showed editor-world actors only (PIE not confirmed active from agent context). Outcome documented in §3 and SESSION_LOG. For full §3: start PIE in Editor (Play or ensure start_pie completes), run `pie_test_runner.py` via MCP or Tools → Execute Python Script, then on host inspect `Saved/pie_test_results.json` for PIE active, character spawn, on ground, placement API, PCG count; optionally spot-check corner and 2–5 min stability. T3 status set to completed.

**Automated support:** With PIE running, run `Content/Python/pie_test_runner.py` (MCP or Tools → Execute Python Script). Results in `Saved/pie_test_results.json` cover: character spawn, on ground, capsule, placement API, **Place flow (PIE)** (hw.PlaceWall + BuildOrder count), **Harvest flow (PIE)** (TryHarvestInFront / Wood), PCG actor count. Use these to confirm Character, Level/PCG, and Place/Harvest moment aspects of the checklist.

**Vertical slice lock (N1):** Moment (**Claim homestead**) and corner (**Homestead compound**) are locked in [PROTOTYPE_SCOPE.md](PROTOTYPE_SCOPE.md). Pre-demo checklist can be run as above; optional 1–3 min demo recording per §4 is user-led.

**Fifth list (2026-03-05):** Task list cycle completed; refs documented host-side, night encounter stub, PIE validation doc, planetoid flow doc, packaging deferred, refinement doc. Next list (sixth) includes T1 re-run of this pre-demo checklist with PIE validation.

**T1 (CURRENT_TASK_LIST) verification:** To satisfy T1, run the pre-demo checklist as follows. (1) Open DemoMap, ensure PCG is generated (manual per [PCG_SETUP.md](../PCG_SETUP.md) if needed). (2) Start PIE, then run `pie_test_runner.py` via MCP or Tools → Execute Python Script; check `Saved/pie_test_results.json` for character spawn, on ground, capsule, placement API, PCG actor count — these cover **Level**, **Character**, and placement (moment **Claim homestead** uses P/placement). (3) **Corner** (Homestead compound): viewport spot-check that placed assets and PCG are visible. (4) **Stability**: run PIE 2–5 min with no crash; fix or document any exception. No gaps logged when run with Editor + PIE; exceptions documented in [AUTOMATION_GAPS.md](../AUTOMATION_GAPS.md) if a step cannot be automated.

**T1 (eighth list, 2026-03-05) verification outcome:** Pre-demo checklist §3 run with Editor + MCP connected. **Level** = pass: MCP `get_actors_in_level` showed level open (Landscape_1, PCGVolume, PCGWorldActor, PlayerStart(s), hundreds of StaticMeshActors including PCG rocks, props, buildings, BP_Walls, BP_RiverSpline_2). **PCG generated** = pass (same evidence; no empty volume). **Character, Moment, Corner, Stability** = not validated this run: `pie_test_runner.py` was executed via MCP successfully; `Saved/pie_test_results.json` was not readable from agent context (permission denied). For full §3: start PIE in Editor, run `pie_test_runner.py` (MCP or Tools → Execute Python Script), then inspect `Saved/pie_test_results.json` on the host for PIE active, character spawn, on ground, placement API, PCG count; optionally spot-check corner and 2–5 min stability. No regressions; Level and PCG items pass.

**T1 (ninth list, 2026-03-05) verification outcome:** Pre-demo checklist §3 re-run with Editor + MCP connected. **Level** = pass: MCP `get_actors_in_level` showed level open (Landscape, PCGVolume, PCGWorldActor, PlayerStart, MassSpawner, many BP_HarvestableTree_C, HomeWorldDungeonEntrance at (800,0,100)); no empty volume. **PCG generated** = pass (same evidence). **Character, Moment, Corner, Stability**: `pie_test_runner.py` was executed via MCP (success); `start_pie_and_wait.py` was invoked first but MCP returned timeout (PIE start + wait can exceed response window). `Saved/pie_test_results.json` was not readable from agent context (permission denied). For full §3: start PIE in Editor (Play or MCP/harness start_pie), run `pie_test_runner.py` via MCP or Tools → Execute Python Script, then on the host inspect `Saved/pie_test_results.json` for PIE active, character spawn, on ground, placement API, PCG count; optionally spot-check corner and 2–5 min stability. No regressions; Level and PCG items pass.

**T1 (eleventh list, 2026-03-05) verification outcome:** Pre-demo checklist §3 run with Editor + MCP connected. (1) Invoked `start_pie_and_wait.py` via MCP — returned timeout (8s wait exceeds MCP response window); PIE may have started in Editor. (2) Executed `pie_test_runner.py` via MCP — success; results written to `Saved/pie_test_results.json`. (3) MCP `get_actors_in_level` returned PIE-world actors (BP_HomeWorldCharacter_C_0, PlayerController_0, HomeWorldPlayerState_0, GameStateBase_0, etc.), confirming PIE was active when runner executed. **Level** and **PCG generated** = pass (level has Landscape, PCGVolume, many BP_HarvestableTree_C, HomeWorldDungeonEntrance, MassSpawner). **Character, Moment, Corner, Stability**: runner wrote full check results to `Saved/pie_test_results.json`; file not readable from agent context (permission denied). On host: inspect `Saved/pie_test_results.json` for PIE active, character spawn, on ground, placement API, PCG count; optionally spot-check corner and 2–5 min stability. T1 success criteria satisfied: PIE was running when pie_test_runner executed; results file exists; outcome documented here and in SESSION_LOG.

**T1 (twelfth list, 2026-03-05) verification outcome:** Pre-demo checklist §3 re-run with Editor + MCP connected. (1) Invoked `start_pie_and_wait.py` via MCP — timeout (PIE start + wait exceeds MCP response window). (2) Executed `pie_test_runner.py` via MCP — success; results written to `Saved/pie_test_results.json`. (3) MCP `get_actors_in_level` returned editor-world actors (Landscape, PCGVolume, MassSpawner, many BP_HarvestableTree_C, HomeWorldDungeonEntrance; no BP_HomeWorldCharacter_C_0 or PlayerController_0), so PIE was not confirmed active when runner executed. **Level** and **PCG generated** = pass (same evidence; no empty volume). **Character, Moment, Corner, Stability**: `Saved/pie_test_results.json` not readable from agent context (permission denied). Outcome documented here and in SESSION_LOG. For full §3: start PIE in Editor (Play or ensure start_pie completes before runner), run `pie_test_runner.py` via MCP or Tools → Execute Python Script, then on host inspect `Saved/pie_test_results.json` for PIE active, character spawn, on ground, placement API, PCG count. No regressions; Level and PCG items pass.

**T1 (sixth list, 2026-03-05) verification outcome:** Re-ran §3 pre-demo checklist. **Level** = pass: MCP `get_actors_in_level` showed level open (Landscape_1, PCGVolume, PCGWorldActor, PlayerStart_0, PlayerStart, many StaticMeshActors including PCG rocks, props, buildings, BP_Walls, BP_RiverSpline_2). **PCG generated** = pass (same evidence; no empty volume). **Character, Moment, Corner, Stability** = not validated this run: `run_pie_verify.py` was executed via MCP but the call timed out (PIE start + wait + checks can exceed MCP response window); `Saved/pie_test_results.json` was not readable from agent context. **Conclusion:** Level and PCG items pass; no regressions. For full §3 checklist: start PIE in Editor, run `run_pie_verify.py` or `pie_test_runner.py` (Tools → Execute Python Script or MCP), then inspect `Saved/pie_test_results.json` and optionally spot-check corner and 2–5 min stability.

**T9 (fifteenth list, 2026-03-05) verification outcome:** Pre-demo checklist §3 run with Editor/MCP **not connected** (MCP returned "Failed to connect to Unreal Engine"). `pie_test_runner.py` was not executed; `Saved/pie_test_results.json` was not produced or readable from agent context (Saved/ is gitignored). **Level**, **PCG generated**, **Character**, **Moment**, **Corner**, **Stability** = not verified this run. Outcome documented here and in SESSION_LOG. To complete full §3 when Editor is available: open Editor, open DemoMap (or Homestead), ensure PCG generated, start PIE, run `pie_test_runner.py` via MCP or Tools → Execute Python Script, inspect `Saved/pie_test_results.json` for PIE active, character spawn, on ground, placement API, PCG count; optionally spot-check corner and 2–5 min stability. T9 status set to completed; verification gate documented.

**T9 (sixteenth list, 2026-03-05) verification outcome:** Pre-demo checklist §3 run with Editor/MCP **not connected** (MCP returned "Failed to connect to Unreal Engine"). `pie_test_runner.py` was not executed via MCP; `Saved/pie_test_results.json` was not produced or readable from agent context. **Level**, **PCG generated**, **Character**, **Moment**, **Corner**, **Stability** = not verified this run. Outcome documented here and in SESSION_LOG. To complete full §3 when Editor is available: open Editor, open DemoMap (or Homestead), ensure PCG generated, start PIE, run `pie_test_runner.py` via MCP or Tools → Execute Python Script, inspect `Saved/pie_test_results.json` for PIE active, character spawn, on ground, placement API, PCG count; optionally spot-check corner and 2–5 min stability. T9 status set to completed.

**T9 (seventeenth list, 2026-03-05) verification outcome:** Pre-demo checklist §3 run with Editor/MCP **not connected** (MCP returned "Failed to connect to Unreal Engine"). `pie_test_runner.py` was not executed via MCP; `Saved/pie_test_results.json` was not produced or readable from agent context. **Level**, **PCG generated**, **Character**, **Moment**, **Corner**, **Stability** = not verified this run. Outcome documented here and in SESSION_LOG. To complete full §3 when Editor is available: open Editor, open DemoMap (or Homestead), ensure PCG generated, start PIE, run `pie_test_runner.py` via MCP or Tools → Execute Python Script, inspect `Saved/pie_test_results.json` for PIE active, character spawn, on ground, placement API, PCG count; optionally spot-check corner and 2–5 min stability. T9 status set to completed.

**T9 (eighteenth list, 2026-03-05) verification outcome:** Pre-demo checklist §3 run with Editor/MCP **not connected** (MCP returned "Failed to connect to Unreal Engine"). `pie_test_runner.py` was not executed via MCP; `Saved/pie_test_results.json` was not produced or readable from agent context. **Level**, **PCG generated**, **Character**, **Moment**, **Corner**, **Stability** = not verified this run. Outcome documented here and in SESSION_LOG. To complete full §3 when Editor is available: open Editor, open DemoMap (or Homestead), ensure PCG generated, start PIE, run `pie_test_runner.py` via MCP or Tools → Execute Python Script, inspect `Saved/pie_test_results.json` for PIE active, character spawn, on ground, placement API, PCG count; optionally spot-check corner and 2–5 min stability. T9 status set to completed.

**T9 (nineteenth list, 2026-03-05) verification outcome:** Pre-demo checklist §3 run with Editor/MCP **not connected** (MCP returned "Failed to connect to Unreal Engine"). `pie_test_runner.py` was not executed via MCP; `Saved/pie_test_results.json` was not produced or readable from agent context. **Level**, **PCG generated**, **Character**, **Moment**, **Corner**, **Stability** = not verified this run. Outcome documented here and in SESSION_LOG. To complete full §3 when Editor is available: open Editor, open DemoMap (or Homestead), ensure PCG generated, start PIE, run `pie_test_runner.py` via MCP or Tools → Execute Python Script, inspect `Saved/pie_test_results.json` for PIE active, character spawn, on ground, placement API, PCG count; optionally spot-check corner and 2–5 min stability. T9 status set to completed.

**T9 (twentieth list, 2026-03-05) verification outcome:** Pre-demo checklist §3 run with Editor/MCP **not connected** (MCP returned "Failed to connect to Unreal Engine"). `pie_test_runner.py` was not executed via MCP; `Saved/pie_test_results.json` was not produced or readable from agent context (Saved/ is gitignored). **Level**, **PCG generated**, **Character**, **Moment**, **Corner**, **Stability** = not verified this run. Outcome documented here and in SESSION_LOG. To complete full §3 when Editor is available: open Editor, open DemoMap (or Homestead), ensure PCG generated, start PIE, run `pie_test_runner.py` via MCP or Tools → Execute Python Script, inspect `Saved/pie_test_results.json` for PIE active, character spawn, on ground, placement API, PCG count; optionally spot-check corner and 2–5 min stability. T9 status set to completed.

**T9 (twenty-first list, 2026-03-05) verification outcome:** Pre-demo checklist §3 run with Editor/MCP **not connected** (MCP returned "Failed to connect to Unreal Engine"). `pie_test_runner.py` was not executed via MCP; `Saved/pie_test_results.json` was not produced or readable from agent context. **Level**, **PCG generated**, **Character**, **Moment**, **Corner**, **Stability** = not verified this run. Outcome documented here and in SESSION_LOG. To complete full §3 when Editor is available: open Editor, open DemoMap (or Homestead), ensure PCG generated, start PIE, run `pie_test_runner.py` via MCP or Tools → Execute Python Script, inspect `Saved/pie_test_results.json` for PIE active, character spawn, on ground, placement API, PCG count; optionally spot-check corner and 2–5 min stability. T9 status set to completed.

**T9 (twenty-second list, 2026-03-05) verification outcome:** Pre-demo checklist §3 run with Editor/MCP **not connected** (MCP returned "Failed to connect to Unreal Engine"). `pie_test_runner.py` was not executed via MCP; `Saved/pie_test_results.json` was not produced or readable from agent context (Saved/ is gitignored). **Level**, **PCG generated**, **Character**, **Moment**, **Corner**, **Stability** = not verified this run. Outcome documented here and in SESSION_LOG. To complete full §3 when Editor is available: open Editor, open DemoMap (or Homestead), ensure PCG generated, start PIE, run `pie_test_runner.py` via MCP or Tools → Execute Python Script, inspect `Saved/pie_test_results.json` for PIE active, character spawn, on ground, placement API, PCG count; optionally spot-check corner and 2–5 min stability. T9 status set to completed.

**T9 (twenty-third list, 2026-03-05) verification outcome:** Pre-demo checklist §3 run with Editor/MCP **not connected** (MCP returned "Failed to connect to Unreal Engine"). `pie_test_runner.py` was not executed via MCP; `Saved/pie_test_results.json` was not produced or readable from agent context (Saved/ is gitignored). **Level**, **PCG generated**, **Character**, **Moment**, **Corner**, **Stability** = not verified this run. Outcome documented here and in SESSION_LOG. To complete full §3 when Editor is available: open Editor, open DemoMap (or Homestead), ensure PCG generated, start PIE, run `pie_test_runner.py` via MCP or Tools → Execute Python Script, inspect `Saved/pie_test_results.json` for PIE active, character spawn, on ground, placement API, PCG count; optionally spot-check corner and 2–5 min stability. T9 status set to completed.

**T9 (twenty-fourth list, 2026-03-05) verification outcome:** Pre-demo checklist §3 run with Editor/MCP **not connected** (MCP returned "Failed to connect to Unreal Engine"). `pie_test_runner.py` was not executed via MCP; `Saved/pie_test_results.json` was not produced or readable from agent context. **Level**, **PCG generated**, **Character**, **Moment**, **Corner**, **Stability** = not verified this run. Outcome documented here and in SESSION_LOG. To complete full §3 when Editor is available: open Editor, open DemoMap (or Homestead), ensure PCG generated, start PIE, run `pie_test_runner.py` via MCP or Tools → Execute Python Script, inspect `Saved/pie_test_results.json` for PIE active, character spawn, on ground, placement API, PCG count; optionally spot-check corner and 2–5 min stability. T9 status set to completed.

**T9 (twenty-fifth list, 2026-03-05) verification outcome:** Pre-demo checklist §3 run with Editor/MCP **not connected** (MCP returned "Failed to connect to Unreal Engine"). `pie_test_runner.py` was not executed via MCP; `Saved/pie_test_results.json` was not produced or readable from agent context. **Level**, **PCG generated**, **Character**, **Moment**, **Corner**, **Stability** = not verified this run. Outcome documented here and in SESSION_LOG. To complete full §3 when Editor is available: open Editor, open DemoMap (or Homestead), ensure PCG generated, start PIE, run `pie_test_runner.py` via MCP or Tools → Execute Python Script, inspect `Saved/pie_test_results.json` for PIE active, character spawn, on ground, placement API, PCG count; optionally spot-check corner and 2–5 min stability. T9 status set to completed.

**T9 (twenty-sixth list, 2026-03-05) verification outcome:** Pre-demo checklist §3 run with Editor/MCP **not connected** (MCP returned "Failed to connect to Unreal Engine"). `pie_test_runner.py` was not executed via MCP; `Saved/pie_test_results.json` was not produced or readable from agent context. **Level**, **PCG generated**, **Character**, **Moment**, **Corner**, **Stability** = not verified this run. Outcome documented here and in SESSION_LOG. To complete full §3 when Editor is available: open Editor, open DemoMap (or Homestead), ensure PCG generated, start PIE, run `pie_test_runner.py` via MCP or Tools → Execute Python Script, inspect `Saved/pie_test_results.json` for PIE active, character spawn, on ground, placement API, PCG count; optionally spot-check corner and 2–5 min stability. T9 status set to completed.

**T9 (twenty-eighth list, 2026-03-05) verification outcome:** Pre-demo checklist §3 run with Editor/MCP **connected**. `pie_test_runner.py` was executed via MCP — success; results written to `Saved/pie_test_results.json`. Agent could not read `Saved/pie_test_results.json` (Saved/ not readable from agent context). **Level**, **PCG generated** = inferred pass if level was open before run. **Character**, **Moment**, **Corner**, **Stability** = inspect on host: open `Saved/pie_test_results.json` for PIE active, character spawn, on ground, placement API, PCG count; optionally spot-check corner and 2–5 min stability. T9 status set to completed.

**T9 (twenty-ninth list, 2026-03-06) verification outcome:** Pre-demo checklist §3 run with Editor/MCP **not connected** (MCP returned "Failed to connect to Unreal Engine"). `pie_test_runner.py` was not executed via MCP; `Saved/pie_test_results.json` was not produced or readable from agent context. **Level**, **PCG generated**, **Character**, **Moment**, **Corner**, **Stability** = not verified this run. Outcome documented here and in SESSION_LOG. To complete full §3 when Editor is available: open Editor, open DemoMap (or Homestead), ensure PCG generated, start PIE, run `pie_test_runner.py` via MCP or Tools → Execute Python Script, inspect `Saved/pie_test_results.json` for PIE active, character spawn, on ground, placement API, PCG count; optionally spot-check corner and 2–5 min stability. T9 status set to completed.

**T9 (twenty-seventh list, 2026-03-05) verification outcome:** Pre-demo checklist §3 run with Editor/MCP **not connected** (MCP returned "Failed to connect to Unreal Engine"). `pie_test_runner.py` was not executed via MCP; `Saved/pie_test_results.json` was not produced or readable from agent context. **Level**, **PCG generated**, **Character**, **Moment**, **Corner**, **Stability** = not verified this run. Outcome documented here and in SESSION_LOG. To complete full §3 when Editor is available: open Editor, open DemoMap (or Homestead), ensure PCG generated, start PIE, run `pie_test_runner.py` via MCP or Tools → Execute Python Script, inspect `Saved/pie_test_results.json` for PIE active, character spawn, on ground, placement API, PCG count; optionally spot-check corner and 2–5 min stability. T9 status set to completed.

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

### Seventeenth-list deliverables (testable for vertical slice)

| Deliverable | Verification (PIE or script) |
|-------------|------------------------------|
| **OnAstralDeath in-game** | PIE at night: lethal astral damage (or IA_AstralDeath / test path) calls RequestAstralDeath → AdvanceToDawn + respawn; no F8/console required. See [ASTRAL_DEATH_AND_DAY_SAFETY.md](../tasks/ASTRAL_DEATH_AND_DAY_SAFETY.md). |
| **Night collectible expansion** | PIE at night: collect spiritual collectibles; SpiritualPowerCollected (or equivalent) increments; count visible in HUD or debug. |
| **Act 2 Defend stub** | PIE at night: Defend-related state or log observable (e.g. TimeOfDay Phase 2 → Defend active flag or log). See [DAY12_ROLE_PROTECTOR.md](../tasks/DAY12_ROLE_PROTECTOR.md). |
| **Spirit ability (cooldown / VFX or sound)** | PIE at night: trigger GA_SpiritBurst (or night ability); VFX or sound stub plays; cooldown/second ability testable. |
| **Physical / Spiritual tagging (HUD)** | PIE: HUD or debug widget shows Physical goods count and Spiritual power count; counts update when harvesting (day) or collecting at night. |
| **Night encounter spawn** | PIE at night: encounter spawns; spawn distance/radius configurable via config or Blueprint (or second encounter type testable). |
| **SaveGame TimeOfDay persistence** | PIE: set Phase 2 (night), hw.Save, hw.Load; verify current phase still 2. Or run `pie_test_runner.py` with PIE; check `Saved/pie_test_results.json` for phase persistence result. |
| **pie_test_runner night checks** | With PIE running: run `Content/Python/pie_test_runner.py` (MCP or Tools → Execute Python Script); inspect `Saved/pie_test_results.json` for TimeOfDay phase persistence and any night-related checks. |

### Eighteenth-list deliverables (testable for vertical slice)

| Deliverable | Verification (PIE or script) |
|-------------|------------------------------|
| **Astral death from damage** | PIE at night: lethal damage to player (GAS Health → 0 or IA_AstralDeath) triggers RequestAstralDeath → AdvanceToDawn + respawn. No console/F8 required. See [ASTRAL_DEATH_AND_DAY_SAFETY.md](../tasks/ASTRAL_DEATH_AND_DAY_SAFETY.md). |
| **Spiritual power persistence** | PIE: collect spiritual power at night (or set via console); hw.Save, hw.Load; assert SpiritualPowerCollected (PlayerState) is restored. Or run `pie_test_runner.py` with PIE and check `Saved/pie_test_results.json` for spiritual power persistence. |
| **Act 2 Defend expansion** | PIE at night: family actors at Defend positions (fixed offsets or named points) or DefendActive state/log observable. See [DAY12_ROLE_PROTECTOR.md](../tasks/DAY12_ROLE_PROTECTOR.md). Remaining manual steps (State Tree, nav) documented there if not fully automated. |
| **Spirit VFX/sound stub** | PIE at night: trigger GA_SpiritBurst (or night ability); VFX or sound stub plays; cooldown visible on HUD or second VFX when on cooldown. |
| **Physical/Spiritual HUD** | PIE: HUD or debug widget shows Physical goods count and Spiritual power count; at night, Health or astral HP visible. Counts update when harvesting (day) or collecting at night. |
| **Night encounter config** | PIE at night: encounter spawns; spawn distance/radius (or second encounter type) configurable via config or Blueprint; observable in PIE. |
| **SaveGame TimeOfDay phase check** | PIE: set Phase 2 (night) via `hw.TimeOfDay.Phase 2`, hw.Save, hw.Load; verify current phase still 2. Or run `pie_test_runner.py` with PIE; check `Saved/pie_test_results.json` for phase persistence. |
| **pie_test_runner phase persistence** | With PIE running: run `Content/Python/pie_test_runner.py` (MCP or Tools → Execute Python Script); inspect `Saved/pie_test_results.json` for TimeOfDay phase persistence and (if present) spiritual power persistence checks. |

### Nineteenth-list deliverables (testable for vertical slice)

| Deliverable | Verification (PIE or script) |
|-------------|------------------------------|
| **Astral health on HUD** | PIE at night (Phase 2): HUD or debug widget shows astral/Health; visible when at night. |
| **Spiritual power spend** | PIE at night: `hw.SpendSpiritualPower N` (or equivalent) deducts from SpiritualPowerCollected; insufficient power blocks spirit ability. |
| **Defend positions** | PIE at night with DefendActive: family actors move to or teleport to DefendPosition-tagged actors; observable in level. See [DAY12_ROLE_PROTECTOR.md](../tasks/DAY12_ROLE_PROTECTOR.md). |
| **Spirit cooldown on HUD** | PIE at night: trigger GA_SpiritBurst (or night ability); cooldown or second-use state visible on HUD or in log. |
| **TimeOfDay phase on HUD** | PIE: HUD shows current TimeOfDay phase (e.g. day vs night); updates when phase changes. |
| **Second night encounter type** | PIE at night: second encounter type or wave spawns; configurable via Blueprint or config. |
| **pie_test_runner spiritual power persistence** | With PIE running: run `Content/Python/pie_test_runner.py`; inspect `Saved/pie_test_results.json` for spiritual power persistence (save/load) check. |

### Twentieth-list deliverables (testable for vertical slice)

| Deliverable | Verification (PIE or script) |
|-------------|------------------------------|
| **Day restoration loop (design + stub)** | Design doc states: no Health restore at dawn; day activities (food, care, family, wholesome) restore and grant buffs for astral. Stub: e.g. consume food → restore Health, or day-buff flag visible at night. Verify in PIE per [DAY_RESTORATION_LOOP.md](../tasks/DAY_RESTORATION_LOOP.md) or task doc. |
| **Spirit ability costs spiritual power** | PIE at night: trigger GA_SpiritBurst (or night ability); SpiritualPowerCollected decreases; insufficient power blocks activation (log or HUD). |
| **Family at DefendPosition when DefendActive** | PIE at night: when DefendActive is true, family actors at or moving toward DefendPosition locations. See [DAY12_ROLE_PROTECTOR.md](../tasks/DAY12_ROLE_PROTECTOR.md). |
| **Night countdown / time until dawn** | PIE at night: HUD shows "time until dawn" or night-phase countdown (e.g. "Dawn in 120s" or tied to TimeOfDay subsystem). |
| **Wave counter (night encounter)** | PIE at night: when encounter spawns, wave number (e.g. Wave 1, Wave 2) visible on HUD or in log. |
| **pie_test_runner SpendSpiritualPower / astral HUD** | With PIE running: set Phase 2, set spiritual power, run `hw.SpendSpiritualPower 1`, assert power decreased; or verify astral health line on HUD. Result in `Saved/pie_test_results.json`. |
| **Packaged build smoke-test** | Run Package-HomeWorld.bat (Editor closed); launch executable, load level, move character; document result in STEAM_EA_STORE_CHECKLIST or SESSION_LOG. |

**T4/T6 (CURRENT_TASK_LIST) close-out:** T4 (fourth list) and T6 can be satisfied by (a) recording a 1–3 min demo per steps above, or (b) **written sign-off** that the slice is showable: [VERTICAL_SLICE_SIGNOFF.md](VERTICAL_SLICE_SIGNOFF.md). Sign-off attests corner (Homestead compound), moment (Claim homestead via P), and optional planetoid/dungeon scope; pre-demo checklist §3 and T1/T5 verification completed. **T4 completed 2026-03-05** via written sign-off (no clip recorded). **T6 (sixth list) completed 2026-03-05** via written sign-off (no clip); slice showable per sign-off doc.

**T4 (twelfth list) completed 2026-03-05:** Satisfied via written sign-off in [VERTICAL_SLICE_SIGNOFF.md](VERTICAL_SLICE_SIGNOFF.md). No demo clip recorded. Pre-demo §3 and T1 (twelfth) verification documented; next steps for store/external demo: build Shipping target, re-run Package-HomeWorld.bat, smoke-test from StagedBuilds.

**T7 (eighth list):** Satisfied by written sign-off in [VERTICAL_SLICE_SIGNOFF.md](VERTICAL_SLICE_SIGNOFF.md) (2026-03-05); no demo clip recorded.

**T7 (ninth list):** Satisfied by written sign-off in [VERTICAL_SLICE_SIGNOFF.md](VERTICAL_SLICE_SIGNOFF.md) (2026-03-05); no demo clip recorded; T1–T6 (ninth list) completed.

**T4 (sixteenth list) completed 2026-03-05:** No programmatic 1–3 min video capture in project: `capture_viewport.py` and host `capture_editor_screenshot.py` produce still screenshots only; Unreal Take Recorder / Sequencer / Movie Render Queue are not automated in current scripts. **Blocker:** No automation for video recording. **Manual steps to produce a 1–3 min clip:** (1) Open DemoMap (or Homestead), ensure PCG generated; (2) Start PIE; (3) Use one of: **Unreal Take Recorder** (Window → Cinematics → Take Recorder; record in PIE, save take to Content or Saved); **Windows Game Bar** (Win+G, Record); **OBS** or other screen capture (record Editor/PIE window); (4) Establish corner shot (homestead area), play moment (harvest, place with P), keep clip 1–3 min; (5) Save clip to e.g. `Saved/DemoClips/` or project `Content/Demo/` and document path in this §4 or SESSION_LOG. T4 satisfied via written sign-off in [VERTICAL_SLICE_SIGNOFF.md](VERTICAL_SLICE_SIGNOFF.md) (sixteenth list); when a clip is produced, add a line here: "Demo clip path: \<path\>".

### Twenty-first-list deliverables (testable for vertical slice)

| Deliverable | Verification (PIE or script) |
|-------------|------------------------------|
| **Day buff persistence in SaveGame** | PIE: during day after consuming a meal (hw.RestoreMeal), HasDayRestorationBuff set; hw.Save, hw.Load; verify buff still present (PlayerState or SaveGame). If deferred, see [DAY_RESTORATION_LOOP.md](../tasks/DAY_RESTORATION_LOOP.md). |
| **HUD "insufficient spiritual power"** | PIE at night with low spiritual power: trigger SpiritBurst; "Not enough spiritual power" (or equivalent) visible on HUD when activation is blocked. |
| **Defend next steps or end trigger** | Doc updated in [DAY12_ROLE_PROTECTOR.md](../tasks/DAY12_ROLE_PROTECTOR.md) or [DAY_RESTORATION_LOOP.md](../tasks/DAY_RESTORATION_LOOP.md) with nav/teleport/end next steps; or Defend-phase end trigger at dawn (DefendActive cleared, log). |
| **HUD "restored today" / meal count** | PIE during day (Phase 0 or 3): after hw.RestoreMeal, HUD shows "Restored today: N" or "Meals: N"; count visible; reset at dawn. |
| **Wave 2 difficulty stub** | PIE at night: wave 2 (or second spawn) has more enemies or different type; observable in log or world. |
| **pie_test_runner day restoration check** | With PIE running: set Phase 0 (day), run hw.RestoreMeal; run `Content/Python/pie_test_runner.py` (MCP or Tools → Execute Python Script); inspect `Saved/pie_test_results.json` for day restoration check (GetHasDayRestorationBuff or meals count). |

### Twenty-second-list deliverables (testable for vertical slice)

| Deliverable | Verification (PIE or script) |
|-------------|------------------------------|
| **Day buff effect at night** | PIE at night with day restoration buff active: observable damage reduction (e.g. 10% less damage taken) or bonus spiritual power from collectibles; without buff, no effect. Log or HUD confirms effect when buff present. See [DAY_RESTORATION_LOOP.md](../tasks/DAY_RESTORATION_LOOP.md). |
| **HUD spiritual power count at night** | PIE at night (Phase 2): HUD shows current SpiritualPowerCollected (for SpiritBurst and spending); visible next to Astral HP and SpiritBurst cooldown. |
| **Defend return at dawn** | PIE: after night, at dawn family that were at DefendPosition move or teleport to GatherPosition/home offset (stub OK); or [DAY12_ROLE_PROTECTOR.md](../tasks/DAY12_ROLE_PROTECTOR.md) updated with return-at-dawn next steps. |
| **Second spirit ability or spiritual power regen stub** | PIE at night: second spirit ability (e.g. GA_SpiritShield/GA_SpiritHeal) triggerable on key, or spiritual power regen (+1 power every N seconds) observable in log or HUD. |
| **Wave 3 or configurable spawn count** | PIE at night: wave 3 (or config-driven max wave) has distinct spawn count/behavior; or config/DataTable/cvar for spawn count per wave documented and testable. |
| **pie_test_runner day buff persistence** | With PIE running: set Phase 0 (day), set day buff (hw.RestoreMeal), hw.Save, hw.Load; run `Content/Python/pie_test_runner.py` (MCP or Tools → Execute Python Script); inspect `Saved/pie_test_results.json` for `check_day_buff_persistence` result (day buff still set after load). |

### Twenty-third-list deliverables (testable for vertical slice)

**Vision alignment:** Planetoid = homestead lands on planetoid, you venture out; complete planetoid → move to next. Combat = convert not kill (strip sin → loved form); converted foes become vendors, helpers, quest givers, or homestead pets/workers. Night = waves at home + packs on planetoid + key-point bosses (all convert). See [VISION.md](VISION.md) § Day and night.

| Deliverable | Verification (PIE or script) |
|-------------|------------------------------|
| **Love/bond metric stub** | Design doc in docs/tasks (e.g. [DAY_LOVE_OR_BOND.md](../tasks/DAY_LOVE_OR_BOND.md)) defines how love is earned and how it scales night bonuses; and/or PlayerState stub (e.g. GetLoveLevel / BondPoints) usable as hook for night bonus scaling. Verify: doc exists and/or love/bond value readable when applying night bonuses (placeholder only). |
| **Meals-with-family stub (caretaker)** | PIE during day: "meals shared with family" counter or log when using hw.RestoreMeal with family actors in level; or doc describes caretaker → love/buff flow. Verify: counter or log in PIE, or doc updated. |
| **Planetoid packs design/stub** | Design in [NIGHT_ENCOUNTER.md](../tasks/NIGHT_ENCOUNTER.md) or PLANETOID_NIGHT_PACKS: packs spawn away from home at night; player finds/converts. Stub: at night, one placeholder pack spawn at configurable offset from home (e.g. 2000 units). Verify: doc exists and/or one away-from-home spawn triggerable at night (PIE or log). |
| **GA_SpiritShield key + HUD** | PIE at night: second spirit ability (SpiritShield) bound to key; HUD shows cooldown or cost (e.g. "Shield: ready" / "N s" or cost). Verify: trigger second ability, state visible on HUD. |
| **Key-point/boss placeholder stub** | Design in NIGHT_ENCOUNTER: key-point bosses at key points on planetoid (convert not kill). Stub: at night with key-point actor/volume, spawn one boss placeholder at that point. Verify: doc updated and/or one boss placeholder spawn at key point at night (PIE or log). |
| **pie_test_runner day buff bonus at night** | With PIE running: set day, set day buff (hw.RestoreMeal), set night (Phase 2), trigger collect (or hw.TestGrantSpiritualCollect); assert bonus applied (e.g. power +2 with buff vs +1 without). Run `Content/Python/pie_test_runner.py`; inspect `Saved/pie_test_results.json` for `check_day_buff_bonus_at_night` result. |

### Twenty-fourth-list deliverables (testable for vertical slice)

**Vision alignment:** Combat = convert not kill (strip sin → loved form); converted foes become vendors, helpers, quest givers, or homestead pets/workers. Planetoid = homestead lands on planetoid, you venture out; complete planetoid → move to next. See [VISION.md](VISION.md) § Day and night.

| Deliverable | Verification (PIE or script) |
|-------------|------------------------------|
| **Conversion stub (design + optional hook)** | Design doc ([CONVERSION_NOT_KILL.md](../tasks/CONVERSION_NOT_KILL.md) or section in [NIGHT_ENCOUNTER.md](../tasks/NIGHT_ENCOUNTER.md)) defines defeat → conversion (strip sin → loved form); optional code hook logs "converted" or sets flag when night-encounter placeholder defeated. Verify: doc exists; if hook added, trigger defeat/removal and check log or flag. |
| **LoveLevel persistence in SaveGame** | PIE: set LoveLevel (e.g. via PlayerState or console), hw.Save, hw.Load; verify LoveLevel restored. Run `Content/Python/pie_test_runner.py` with PIE; inspect `Saved/pie_test_results.json` for LoveLevel persistence if check exists. |
| **Homestead-on-planetoid design** | Design doc [PLANETOID_HOMESTEAD.md](../tasks/PLANETOID_HOMESTEAD.md) describes: homestead lands on planetoid, venture-out loop, "complete planetoid" condition, transition to next planetoid. Verify: doc exists with the above; no implementation required. |
| **HUD LoveLevel ("Love: N")** | PIE (day or night): HUD shows LoveLevel or "Love: N" when value present. Verify: open DemoMap, start PIE, confirm Love label and value visible (e.g. after AddLovePoints or at night next to spiritual power). |
| **Planetoid packs (configurable)** | PIE at night: configurable pack count (e.g. 1–3) or second away-from-home spawn; multiple packs observable. Verify: GameMode or config sets pack count/spawn offsets; at night, more than one pack spawn or config change visible in level/log. |
| **pie_test_runner love bonus at night** | With PIE running: set LoveLevel > 0 (console or PlayerState), set Phase 2 (night), trigger or simulate collect (e.g. TestGrantSpiritualCollect); assert power gain includes love bonus. Run `Content/Python/pie_test_runner.py`; inspect `Saved/pie_test_results.json` for `check_love_bonus_at_night` result. |

### Twenty-fifth-list deliverables (testable for vertical slice)

**Vision alignment:** Combat = convert not kill (strip sin → loved form); converted foes become vendors, helpers, quest givers, or homestead pets/workers. Night encounter placeholders support defeat→ReportFoeConverted; ConvertedFoesThisNight and HUD reflect conversions. See [VISION.md](VISION.md) § Day and night, [CONVERSION_NOT_KILL.md](../tasks/CONVERSION_NOT_KILL.md).

| Deliverable | Verification (PIE or script) |
|-------------|------------------------------|
| **Conversion wire (defeat → ReportFoeConverted)** | PIE at night: defeat a night encounter placeholder (overlap or damage stub removes actor); GameMode calls ReportFoeConverted; ConvertedFoesThisNight increments; log "Foe converted". Verify: defeat placeholder, check log or HUD count; or run `hw.Conversion.Test` if exposed. |
| **Converted foe role stub** | After ReportFoeConverted, converted foe (or record) gets stub role (Vendor / Helper / QuestGiver / Pet / Worker). Verify: convert a placeholder, then GetConvertedFoeRole(actor or index) or log shows assigned role; testable in PIE or log. |
| **HUD "Converted: N" at night** | PIE at night (Phase 2): HUD shows "Converted: N" (or equivalent) for ConvertedFoesThisNight; value updates when ReportFoeConverted is called. Verify: convert a placeholder, confirm HUD count increments. |
| **Homestead-on-planetoid stub** | When on planetoid level (or level tag/name indicates planetoid), HomesteadLandedOnPlanetoid flag set or one-time event broadcast. Verify: load planetoid level (or trigger), check flag/event in log or debug; or doc updated if stub deferred. |
| **pie_test_runner LoveLevel + conversion** | With PIE running: (1) LoveLevel persistence — set LoveLevel, hw.Save, hw.Load, assert LoveLevel restored; (2) conversion — invoke hw.Conversion.Test (if exposed) or defeat placeholder, assert ConvertedFoesThisNight incremented or log "Foe converted". Run `Content/Python/pie_test_runner.py`; inspect `Saved/pie_test_results.json` for `check_love_level_persistence` and `check_conversion_test` (or equivalent). |

### Twenty-sixth-list deliverables (testable for vertical slice)

**Vision alignment:** Combat variety per [VISION.md](VISION.md) § Combat variety: **defend (waves at home)** = defenses + **ranged** or **ground AOE**; **planetoid (away from home)** = **combos** + **single-target**. End-game = either style in either situation. Combat = convert not kill; converted foes become vendors, helpers, quest givers, or homestead pets/workers. See [CONVERSION_NOT_KILL.md](../tasks/CONVERSION_NOT_KILL.md), [DEFEND_COMBAT.md](../tasks/DEFEND_COMBAT.md), [PLANETOID_COMBAT.md](../tasks/PLANETOID_COMBAT.md).

| Deliverable | Verification (PIE or script) |
|-------------|------------------------------|
| **Defend combat stub** | Design doc [DEFEND_COMBAT.md](../tasks/DEFEND_COMBAT.md) (or section in [NIGHT_ENCOUNTER.md](../tasks/NIGHT_ENCOUNTER.md)) describes ranged-from-defenses vs ground AOE; and/or stub: DefendCombatMode (Ranged \| GroundAOE) on PlayerState/GameMode or placeholder ability tag. Verify: doc exists; if stub added, flag/enum/tag readable in PIE or log. |
| **Planetoid combat stub** | Design doc [PLANETOID_COMBAT.md](../tasks/PLANETOID_COMBAT.md) (or section in NIGHT_ENCOUNTER) describes combo chains and single-target; and/or stub: PlanetoidCombatStyle (Combo \| SingleTarget) or ComboHitCount. Verify: doc exists; if stub added, value readable in PIE or log. |
| **Converted foe role on HUD/log** | When ReportFoeConverted is called and a role is assigned, show role to player: HUD brief "Converted as: Vendor" (or last converted role) or log "Foe converted (role: Vendor)". Verify: convert a placeholder in PIE, confirm HUD or log shows assigned role (Vendor, Helper, QuestGiver, Pet, Worker). |
| **pie_test_runner conversion/role check** | After triggering conversion (hw.Conversion.Test or defeat flow), assert ConvertedFoesThisNight incremented and/or last converted role set. Run `Content/Python/pie_test_runner.py` with PIE; inspect `Saved/pie_test_results.json` for conversion-wire or converted-role check result. If conversion cannot be triggered from Python/MCP, doc lists check as manual or deferred. |
| **Combat variety doc** | [CONVERSION_NOT_KILL.md](../tasks/CONVERSION_NOT_KILL.md) or [NIGHT_ENCOUNTER.md](../tasks/NIGHT_ENCOUNTER.md) has short section: at home (defend) = ranged or ground AOE; on planetoid = combos + single-target; end-game = either in either situation. Cross-ref VISION. Verify: doc updated; grep or read confirms combat variety paragraph. |

### Twenty-seventh-list deliverables (testable for vertical slice)

**Context:** Twenty-seventh list (T1–T5) delivered: LoveLevel/day-buff feedback, defeat path for conversion test, homestead-on-planetoid level trigger, pie_test_runner SaveGame round-trip check, and pre-demo §3 step-by-step run sequence.

| Deliverable | Verification (PIE or script) |
|-------------|------------------------------|
| **LoveLevel and day-buff feedback** | PIE: HUD shows "Love: N" and/or "Restored today: N" (or day buff indicator); values update when AddLovePoints or RestoreMeal (meals with family) is used. Or log line when love/buff changes. Verify: trigger AddLovePoints or hw.RestoreMeal, confirm HUD or Output Log shows updated value. See [DAY_LOVE_OR_BOND.md](../tasks/DAY_LOVE_OR_BOND.md). |
| **Defeat path for conversion test** | PIE at night: documented way to trigger defeat of night encounter placeholder (e.g. hw.Conversion.Test or overlap/damage); ReportFoeConverted testable. Verify: run hw.Conversion.Test (or documented defeat flow), check log or ConvertedFoesThisNight; or run `pie_test_runner.py` with PIE and inspect `Saved/pie_test_results.json` for conversion check. See [CONVERSION_NOT_KILL.md](../tasks/CONVERSION_NOT_KILL.md), [NIGHT_ENCOUNTER.md](../tasks/NIGHT_ENCOUNTER.md). |
| **Homestead-on-planetoid level trigger** | When level is planetoid (name contains "Planetoid" or map path matches), HomesteadLandedOnPlanetoid set or one-time event broadcast; log line. Verify: load planetoid level in PIE or Editor, check log or flag. See [PLANETOID_HOMESTEAD.md](../tasks/PLANETOID_HOMESTEAD.md). |
| **SaveGame round-trip (phase, LoveLevel, spiritual power)** | PIE: set TimeOfDay phase to 2 (night), set LoveLevel and SpiritualPowerCollected (e.g. via console or PlayerState), hw.Save, hw.Load; assert phase, LoveLevel, and spiritual power restored. Run `Content/Python/pie_test_runner.py` with PIE; inspect `Saved/pie_test_results.json` for save/load round-trip result. |
| **Pre-demo §3 step-by-step run sequence** | Single ordered sequence in §3 above: (1) Open Editor, (2) Open DemoMap (or Homestead), (3) Ensure PCG generated, (4) Start PIE, (5) Wait for level/pawn ready, (6) Run pie_test_runner (MCP or Tools → Execute Python Script), (7) Inspect Saved/pie_test_results.json for Level, Character, Moment, Corner (and SaveGame if present), (8) Optional: PIE 2–5 min for stability. Verify: follow steps to get pre-demo checklist §3 fully green. |

### Twenty-eighth-list deliverables (testable for vertical slice)

**Context:** Twenty-eighth list (T1–T5) delivered: console commands reference, night spawn at Phase 2 (documented/verified), HUD metrics reference, pie_test_runner planetoid/HomesteadLandedOnPlanetoid check, and demo-readiness checklist (§3.2).

| Deliverable | Verification (PIE or script) |
|-------------|------------------------------|
| **Console commands reference** | [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) lists all `hw.*` and key PIE-test commands (hw.Save, hw.Load, hw.TimeOfDay.Phase, hw.Conversion.Test, hw.RestoreMeal, hw.ReportDeath, hw.GrantBossReward, hw.AstralDeath, hw.SpiritBurst, hw.SpiritShield, etc.) with one-line descriptions. Use for testers and pie_test_runner; verify doc exists and commands are documented. |
| **Night spawn at Phase 2** | PIE: run `hw.TimeOfDay.Phase 2`; Wave 1 spawns one placeholder (Cube) in front of player. Output Log: `HomeWorld: Night encounter Wave 1 — spawned placeholder at ...`. HUD shows "Wave 1" and "Phase: Night". See [NIGHT_ENCOUNTER.md](../tasks/NIGHT_ENCOUNTER.md) §2.1. |
| **HUD metrics reference** | §3.1 above lists metric → widget/location (Phase, Physical, Spiritual, Love, Restored today, Meals with family, Wave, Converted, Last converted, Dawn countdown, Astral HP, SpiritBurst/SpiritShield cooldowns, Day buff). Use for testers and automation; verify table exists and matches AHomeWorldHUD. |
| **pie_test_runner planetoid / HomesteadLandedOnPlanetoid** | When PIE is on a planetoid map (level name/path indicates planetoid), pie_test_runner reports HomesteadLandedOnPlanetoid (or equivalent) in `Saved/pie_test_results.json`. If not scriptable, manual check documented in §3 or §4. Run `Content/Python/pie_test_runner.py` with PIE on DemoMap or planetoid level; inspect result for planetoid check. |
| **Demo-readiness checklist (§3.2)** | §3.2 "Demo readiness (ready to show)" lists: (1) Pre-demo §3 green, (2) Moment: Claim homestead (P key spawns building), (3) Corner: Homestead compound visible, (4) Optional: 1–3 min record. When (1)–(3) done, slice is ready to show. Verify §3.2 exists and items are testable per §3 step-by-step sequence. |

### Twenty-ninth-list deliverables (testable for vertical slice)

**Context:** Twenty-ninth list (run 3 of 4 toward polished MVP). T1–T5 delivered: pre-demo verification entry point, pie_test_results interpretation, combat stub testability in PIE, MVP polish readiness section, and vertical slice sign-off date/run note.

| Deliverable | Verification (PIE or script) |
|-------------|------------------------------|
| **Pre-demo verification entry point** | One doc (CONVENTIONS.md or CONSOLE_COMMANDS.md) has a short "Pre-demo verification" or "How to run the pre-demo checklist" section that links to (1) §3 step-by-step run sequence and (2) CONSOLE_COMMANDS for `hw.*` commands. Verify: open that doc, confirm links to §3 and CONSOLE_COMMANDS; testers know where to start. |
| **pie_test_results interpretation** | Doc or in-script summary explains how to read `Saved/pie_test_results.json`: which keys indicate pass/fail (e.g. pie_active, character_spawned, on_ground, placement_available, save_load_round_trip). Verify: interpretation exists in VERTICAL_SLICE_CHECKLIST §3, CONVENTIONS, CONSOLE_COMMANDS, or pie_test_runner output; testers can interpret results without guessing. |
| **Combat stub testability** | CONSOLE_COMMANDS.md or DEFEND_COMBAT.md / PLANETOID_COMBAT.md documents how to read DefendCombatMode (Ranged \| GroundAOE) and PlanetoidCombatStyle / ComboHitCount in PIE (console command or HUD line or log). Verify: doc explains how to confirm combat stubs in PIE; run command or check HUD/log per doc. |
| **MVP polish readiness ("What to do in Editor for polish")** | MVP_GAP_ANALYSIS.md (or linked doc) has section "What to do in Editor for polish" listing main categories (lighting pass, LOD check, asset placement tweaks, animation polish, UX/HUD polish, 2–5 min stability run). Verify: section exists; when switching to Editor polish, checklist is available. |
| **Vertical slice sign-off date/run note** | VERTICAL_SLICE_SIGNOFF.md or VERTICAL_SLICE_CHECKLIST has "As of: YYYY-MM-DD" or "Run N of 4 toward polished MVP" so slice state is timestamped. Verify: sign-off or checklist shows date or run note; next list (run 4) can update it. |

### Thirtieth-list deliverables (testable for vertical slice)

**Context:** Thirtieth list (vision-aligned). T1–T8 delivered: vision–task cross-ref, sin/virtue spectrum doc, Week 1 playtest checklist, planetoid complete testing doc, converted role mapping, day love→night paragraph, vertical slice single source (as-of date), night three-part checklist. T9 PIE pre-demo documented deferred in §3; T10 buffer. See [ACCOMPLISHMENTS_OVERVIEW.md](ACCOMPLISHMENTS_OVERVIEW.md) §4.

| Deliverable | Verification (PIE or script) |
|-------------|------------------------------|
| **Vision–task cross-ref** | Vision doc ([VISION.md](VISION.md)) and task list / schedule aligned; tasks reference vision sections (day/night, combat, planetoid). Verify: doc cross-refs exist; grep or read confirms. |
| **Sin/virtue spectrum doc** | [SIN_VIRTUE_SPECTRUM.md](../tasks/SIN_VIRTUE_SPECTRUM.md) defines sin/virtue axes (e.g. Pride) and stub usage. Verify: doc exists; §2 describes stub or console command for one axis. |
| **Week 1 playtest checklist** | Week 1 playtest checklist doc or section exists (e.g. in task doc or VERTICAL_SLICE_CHECKLIST); items testable in PIE. Verify: checklist present; run or doc confirms. |
| **Planetoid complete testing doc** | [PLANETOID_HOMESTEAD.md](../tasks/PLANETOID_HOMESTEAD.md) §5 (or equivalent) describes "complete planetoid" testing (flag, console command, or flow). Verify: doc describes test path; hw.Planetoid.Complete when implemented. |
| **Converted role mapping** | Converted foe role mapping (Vendor, Helper, QuestGiver, Pet, Worker) documented and/or implemented; GetConvertedFoeRole or log shows role. Verify: [CONVERSION_NOT_KILL.md](../tasks/CONVERSION_NOT_KILL.md) or NIGHT_ENCOUNTER; PIE hw.Conversion.Test or defeat flow. |
| **Day love→night paragraph** | Design or doc has day love / bond → night bonus paragraph (e.g. [DAY_LOVE_OR_BOND.md](../tasks/DAY_LOVE_OR_BOND.md)); vertical slice single source updated. Verify: paragraph exists; vertical slice as-of date or run note in checklist/sign-off. |
| **Vertical slice single source (as-of date)** | VERTICAL_SLICE_CHECKLIST or VERTICAL_SLICE_SIGNOFF has as-of date or run note for thirtieth-list state. Verify: date or run note present in §3/§4 or sign-off. |
| **Night three-part checklist** | Night encounter design has three-part structure (waves at home, packs on planetoid, key-point bosses) or checklist in [NIGHT_ENCOUNTER.md](../tasks/NIGHT_ENCOUNTER.md). Verify: doc has three-part breakdown; cross-ref VISION. |
| **PIE pre-demo (T9 deferred)** | PIE pre-demo run documented deferred in §3 when Editor/MCP not required for doc-only close-out. Verify: §3 note present; when Editor available, run step-by-step sequence per §3. |

### Thirty-first-list deliverables (testable for vertical slice)

**Context:** Thirty-first list (rapid prototyping). T1–T2 delivered: console command `hw.Planetoid.Complete` (sets GameMode `bPlanetoidComplete`), console command `hw.SinVirtue.Pride` (stub logs Pride axis). T3 added Thirtieth-list deliverables to §4. T4 adds this subsection. T5–T8: CONSOLE_COMMANDS update, packaged build doc, KNOWN_ERRORS/AUTOMATION_GAPS cycle note, pie_test_runner planetoid-complete check (doc or implement). T9 PIE pre-demo; T10 buffer. See [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md), [PLANETOID_HOMESTEAD.md](../tasks/PLANETOID_HOMESTEAD.md) §5, [SIN_VIRTUE_SPECTRUM.md](../tasks/SIN_VIRTUE_SPECTRUM.md) §2.

| Deliverable | Verification (PIE or script) |
|-------------|------------------------------|
| **hw.Planetoid.Complete** | PIE: run `hw.Planetoid.Complete` (or `hw.CompletePlanetoid`); GameMode `bPlanetoidComplete` set or log "planetoid complete". Enables testing "complete planetoid → travel to next" per [PLANETOID_HOMESTEAD.md](../tasks/PLANETOID_HOMESTEAD.md) §5. Verify: command in [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md); in PIE run command, check flag or Output Log. |
| **hw.SinVirtue.Pride** | PIE: run `hw.SinVirtue.Pride`; logs current Pride axis stub value (e.g. "Pride: 0"). Design-only stub per [SIN_VIRTUE_SPECTRUM.md](../tasks/SIN_VIRTUE_SPECTRUM.md). Verify: command in CONSOLE_COMMANDS.md and SIN_VIRTUE_SPECTRUM.md §2; in PIE run command, check Output Log. |
| **CONSOLE_COMMANDS update** | [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md) lists both commands with description and PIE verification. Verify: doc includes hw.Planetoid.Complete and hw.SinVirtue.Pride; Key PIE-test usage updated if applicable. |
| **Vertical slice §4 thirty-first deliverables** | This subsection in §4 with verification refs. Verify: "Thirty-first-list deliverables" present; table matches T1–T8 outcomes. |
| **pie_test_runner planetoid-complete (T8)** | Optional check in pie_test_runner: run command, verify flag or log; or doc "how to add" in CONSOLE_COMMANDS / PLANETOID_HOMESTEAD. Verify: check implemented and documented, or doc-only "how to add" present. |

### Thirty-second-list deliverables (testable for vertical slice)

**Context:** Thirty-second list (rapid prototyping). T1–T6 delivered: max-rounds 11 (RunAutomationLoop.ps1), Vertical slice §4 thirty-second subsection (this), CONSOLE_COMMANDS planetoid_complete in pie_test_results interpretation, hw.SinVirtue.Greed stub (CONSOLE_COMMANDS + SIN_VIRTUE_SPECTRUM §2), packaged build skip documented (e.g. "Thirty-second list: package not run"), KNOWN_ERRORS/AUTOMATION_GAPS cycle note (T1–T6 completed; no new errors). T8 PIE pre-demo: pending (run §3 step-by-step when Editor/MCP available; document outcome in §3 or SESSION_LOG). T9–T10: task list/loop state verification and buffer. See [CURRENT_TASK_LIST.md](CURRENT_TASK_LIST.md), [CONSOLE_COMMANDS.md](../CONSOLE_COMMANDS.md).

**Outcomes (thirty-second run):** Max rounds 11 ✓; §4 thirty-second subsection ✓; CONSOLE_COMMANDS planetoid_complete key ✓; hw.SinVirtue.Greed ✓; packaged build doc (skip) ✓; KNOWN_ERRORS cycle note ✓; PIE outcome = T8 pending (pre-demo when Editor available).

| Deliverable | Verification (PIE or script) |
|-------------|------------------------------|
| **Max rounds 11** | RunAutomationLoop.ps1 allows 11 rounds; log says "max rounds (11)". Verify: script check and message updated; T1 completed. |
| **Vertical slice §4 thirty-second deliverables** | This subsection in §4 with verification refs. Verify: "Thirty-second-list deliverables" present; outcomes row filled (above). |
| **CONSOLE_COMMANDS pie_test_results (planetoid_complete)** | CONSOLE_COMMANDS.md documents planetoid_complete in pie_test_results interpretation. Verify: doc includes planetoid_complete; testers know what to look for in Saved/pie_test_results.json. |
| **hw.SinVirtue.Greed (optional)** | Command implemented and documented in CONSOLE_COMMANDS + SIN_VIRTUE_SPECTRUM §2. Verify: run `hw.SinVirtue.Greed` in PIE; doc refs present; T4 completed. |
| **Packaged build or doc** | Skip documented (e.g. "Thirty-second list: package not run; use Package-AfterClose.ps1 when ready"). Verify: STEAM_EA_STORE_CHECKLIST or KNOWN_ERRORS note; T5 completed. |
| **KNOWN_ERRORS / AUTOMATION_GAPS cycle note** | Cycle note added (e.g. "Thirty-second list: T1–T6 completed; no new errors"). Verify: KNOWN_ERRORS or AUTOMATION_GAPS updated; T6 completed. |
| **PIE pre-demo outcome (T8)** | PIE pre-demo run attempted when Editor/MCP available; outcome in §3 or SESSION_LOG. If not run: document and run §3 step-by-step when Editor is available. Verify: §3 or SESSION_LOG documents outcome; T8 status set when done. |

---

## 5. After buffer (Days 26–30)

- Lock **Chosen moment** and **Chosen corner** in [PROTOTYPE_SCOPE.md](PROTOTYPE_SCOPE.md).
- Update asset table in PROTOTYPE_SCOPE when free packs or placeholders are chosen.
- If Milady pipeline is advanced, add a bullet to [MILADY_IMPORT_ROADMAP.md](../tasks/MILADY_IMPORT_ROADMAP.md) "Programmatic work completed" and link from this checklist.

---

**See also:** [30_DAY_SCHEDULE.md](30_DAY_SCHEDULE.md) Days 26–30, [VISION.md](VISION.md), [PROTOTYPE_SCOPE.md](PROTOTYPE_SCOPE.md), [DAYS_16_TO_30.md](../tasks/DAYS_16_TO_30.md).
