# Level Testing Plan: Smart Level Loader and Reliable Level Tests

This document outlines a plan to make level loading and level-based testing reliable for HomeWorld, incorporating research findings and lessons from recent work (Homestead/PCG, World Partition, landscape bounds).

---

## 1. Problem statement

Level loading in an open-world, World Partition project causes several testing and automation issues:

- **Scripts run synchronously** — Python in the Editor does not tick during script execution. A call to `load_level()` starts loading but does not wait for completion; any code that immediately queries the level (e.g. landscape bounds, actors) may see an incomplete or empty world.
- **World Partition streaming** — Landscape and other actors live in streaming cells. Until cells are loaded, `get_all_actors_of_class(Landscape)` can return a Landscape actor with **zero bounds** and **zero LandscapeComponents**, so bounds-based logic (e.g. PCG volume sizing) fails unless we use a fallback (config or World Partition runtime bounds).
- **No single “level ready” signal** — There is no single Python/Blueprint API that means “level is fully loaded and World Partition has streamed what we need.” Tests and scripts either poll with timeouts or depend on manual steps (e.g. “Window → World Partition → Load All”).
- **PIE vs Editor** — PIE tests (`pie_test_runner.py`) assume a level is already open and PIE is started; they do not load a level or wait for streaming. So “test the level” requires a human to open the right map and start PIE first, or scripts must orchestrate load + optional “Load All” + PIE.

A **smart level loader** would provide a predictable way to get a level into a “ready for testing” state (optionally with World Partition fully loaded) so that automation and tests can rely on it.

---

## 2. Research summary

### 2.1 Epic documentation

- **Editor does not tick during Python** — Non-blocking operations (e.g. level load) need the engine to tick. The **AutomationScheduler** and **latent commands** are the intended mechanism: register a generator that `yield`s each frame (or each N frames) so the Editor can tick and the load can progress. See [Write Editor Tests with Python](https://dev.epicgames.com/documentation/en-us/unreal-engine/write-editor-tests-with-python-in-unreal-engine).
- **Level loading in tests** — Example pattern: `@unreal.AutomationScheduler.add_latent_command` then `unreal.EditorLevelLibrary.load_level("/Game/mymap")`. The doc does not show an explicit “wait until level load complete” idiom; typically you would `yield` in a loop until some condition (e.g. current level path matches, or a specific actor exists with non-zero bounds).
- **Python automation** — `PythonAutomationTest` discovers `test_*.py` under `Content/Python` (including subfolders like `tests/`). Tests can use `unreal.AutomationScheduler.add_latent_command` for multi-frame steps. Timeouts: `SetPyLatentCommandTimeout` / `set_latent_command_timeout(seconds)` (see `UPyAutomationTestLibrary`).
- **World Partition** — Single persistent level split into grid cells; distance-based streaming. There is no documented Python “Load All” or “flush streaming” API; editor UI uses **Window → World Partition → Load All**. Runtime bounds can be obtained via World Partition’s **Get Runtime World Bounds** (Blueprint library or `UWorldPartition::GetRuntimeWorldBounds()`); we use this in `create_homestead_from_scratch.py` when landscape geometry is not loaded.

### 2.2 Community and ecosystem

- **Andrew Fray – Unreal Test Automation 2025** ([link](https://andrewfray.wordpress.com/2025/04/09/the-topography-of-unreal-test-automation-in-2025/)):
  - **Map Check** — Edit/build-time validation per map; good for setup errors (e.g. one player start, no missing materials). Does not run on save by default; output in Message Log.
  - **Asset Data Validation** — Broader than Map Check; runs on save, popups and Asset Check tab. Good for data/assets.
  - **Automation Framework** — C++ `IMPLEMENT_SIMPLE_AUTOMATION_TEST`, latent commands for multi-frame tests. Python tests sit on top of this.
  - **Functional Tests (Blueprint)** — Actor-based tests in Blueprint; can drive editor tests.
  - **Spec** — BDD-style C++ tests with BeforeEach/AfterEach; no BeforeAll/AfterAll.
  - **CQTest** — Newer C++ framework (Rare/Lyra lineage); good for gameplay and latent commands; docs thin, Lyra samples are the reference.
- **Takeaway** — For “load level then test,” we need either latent Python (AutomationScheduler + yield until ready) or a C++ latent test. A shared “level loader” that runs as a latent command and yields until “ready” would standardize this.

### 2.3 HomeWorld-specific findings (recent work)

- **Landscape bounds when World Partition is used** — With WP, the Landscape actor can be present but have **actor extent (0,0,0)** and **0 LandscapeComponents** until the landscape cell is streamed in. So:
  - Bounds from `land.get_actor_bounds(False)` can be zero.
  - Bounds from LandscapeComponent aggregation are only available when components are loaded (often after “Load All” or after streaming).
- **Mitigations already in place** — In `create_homestead_from_scratch.py` we:
  1. Prefer **LevelEditorSubsystem.load_level()** then fallback to **EditorLevelLibrary.load_level()**.
  2. **Wait for landscape** with a retry loop (e.g. 20 × 2 s) so that if the user has run “Load All,” bounds may become available.
  3. Use **World Partition runtime bounds** when landscape bounds are zero and component aggregation returns nothing — so the PCG volume can be sized even when geometry is not streamed.
  4. Fall back to **config volume bounds** when all of the above fail.
- **Manual step** — We document: “To fit volume to landscape: Window → World Partition → Load All, then run this script again with Homestead still open.” So “smart” loading for tests could include: load level (latent) → optionally trigger or wait for “Load All” equivalent → then run assertions.
- **Configurable timeouts** — `create_homestead_from_scratch.py` reads wait attempts and delays from `homestead_map_config.json` (phase1/phase2, `use_landscape_bounds`, `recreate_volume_and_graph`). For fast iteration or test runs, reduce phase1 attempts/delay or set `use_landscape_bounds: false`. See [PCG_SETUP.md](PCG_SETUP.md) (Fast iteration).

---

## 3. Goals for a smart level loader and testing enhancements

1. **Deterministic “level ready” for scripts** — A single entry point (e.g. `ensure_level_loaded(level_path, options)`) that:
   - Opens the level (using latent commands if run from automation so the Editor can tick).
   - Optionally waits until a “ready” condition (e.g. landscape bounds non-zero, or World Partition runtime bounds available, or a timeout).
   - Can be used from both one-off scripts (e.g. `create_homestead_from_scratch.py`) and from Python automation tests.
2. **Use latent commands where it matters** — Any test or script that **loads a level and then immediately asserts** should run inside the AutomationScheduler with `yield` until the level is ready (or timeout). This avoids “level not loaded yet” flakes.
3. **World Partition awareness** — When the level uses World Partition:
   - Prefer **World Partition runtime bounds** when actor/component bounds are zero (already done for Homestead).
   - Document that “Load All” (or future scripted equivalent) may be required for full geometry; otherwise tests that depend on specific streamed actors should either run after “Load All” or assert on what is actually available (e.g. runtime bounds vs. landscape mesh).
4. **PIE testing** — For PIE-based tests (e.g. `pie_test_runner.py`):
   - Option A: Keep current contract (“user opens level and starts PIE; script only runs checks”). Document this clearly.
   - Option B: Add an optional “full flow” test that uses latent commands to load a chosen level, optionally wait for ready, start PIE, then run existing checks. This would be a new test or harness, not a replacement for the current lightweight runner.
5. **Reuse and document** — A small, shared Python module (e.g. `level_loader.py` or `content/Python/level_loader.py`) could provide:
   - `open_level(level_path)` — current behavior (synchronous open; no wait).
   - `wait_for_level_ready(level_path, max_wait_sec, condition)` — poll until condition or timeout (for use inside a latent generator: `while not condition(): yield`).
   - Helpers for “landscape has non-zero bounds” or “world partition runtime bounds available” as ready conditions.
   - All of this documented in this plan and in [PCG_SETUP.md](PCG_SETUP.md) / [HOMESTEAD_MAP.md](HOMESTEAD_MAP.md) where relevant.

---

## 4. Proposed implementation plan

### Phase 1: Shared level-load and “ready” helpers (no AutomationScheduler yet)

- Add **`Content/Python/level_loader.py`** (or equivalent name under `Content/Python/`):
  - `open_level(level_path)` — Call LevelEditorSubsystem.load_level or EditorLevelLibrary.load_level (mirror current logic in `create_homestead_from_scratch._open_level`), return success/failure.
  - `get_current_level_path()` — Return current editor level path (mirror `_get_current_level_path`).
  - `is_level_loaded(level_path)` — True if current level path matches (with normalization).
  - `wait_for_condition(condition_fn, max_attempts, delay_sec)` — Synchronous poll loop: call `condition_fn()` each time, sleep `delay_sec` between attempts, return True if condition met, False after max_attempts. (Used by scripts that are OK blocking.)
  - Ready conditions (for use with `wait_for_condition` or future latent):
    - `landscape_has_bounds()` — At least one Landscape with non-zero actor bounds or non-zero component-derived bounds, or World Partition runtime bounds available (reuse logic from `create_homestead_from_scratch`).
    - Optional: `level_has_actor_of_class(actor_class)` — At least one actor of that class in the editor world.
- Refactor **`create_homestead_from_scratch.py`** to call into this module for open + wait for landscape/ready, so we don’t duplicate “wait for landscape” and “World Partition bounds” logic.
- **Document** in this plan and in [HOMESTEAD_MAP.md](HOMESTEAD_MAP.md): “For reliable Homestead setup, run after opening Homestead; if using World Partition, run Window → World Partition → Load All first for full landscape bounds, or rely on config/World Partition runtime bounds.”

**Implemented:** Phase 1 implemented: [Content/Python/level_loader.py](../Content/Python/level_loader.py) provides `open_level`, `get_current_level_path`, `is_level_loaded`, `wait_for_condition`, `get_landscape_bounds`, `landscape_has_bounds`, `level_has_actor_of_class`; [create_homestead_from_scratch.py](../Content/Python/create_homestead_from_scratch.py) refactored to use it.

### Phase 2: Latent “smart level loader” for Python automation tests

- In **`level_loader.py`** (or a dedicated test helper):
  - `latent_load_level_and_wait(level_path, ready_condition, max_wait_sec)` — Intended to be used as a **generator** registered with `unreal.AutomationScheduler.add_latent_command`: each iteration calls the ready condition; if not met, `yield` and let the Editor tick; if met or timeout, finish. This gives tests a single “load level and wait until ready” step.
  - Set **latent command timeout** (e.g. `set_latent_command_timeout(max_wait_sec + buffer)`) so the test does not hang indefinitely.
- Add (or extend) a **Python automation test** that:
  1. Registers a latent command that calls `latent_load_level_and_wait("/Game/HomeWorld/Maps/Homestead", landscape_has_bounds, 30)` (or similar).
  2. After the command completes, runs assertions (e.g. “Landscape exists and has non-zero extent” or “PCG volume exists”). This validates that the smart level loader plus ready condition works in the test framework.
- **Document** in this plan and in [SETUP.md](SETUP.md) / AGENTS.md: “Level tests that load a map should use the latent level loader so the Editor can tick during load and optional streaming.”

**Implemented:** Phase 2 implemented: [level_loader.py](../Content/Python/level_loader.py) has `latent_load_level_and_wait`; [test_level_loader.py](../Content/Python/tests/test_level_loader.py) loads Homestead and asserts level ready (landscape or WP bounds).

### Phase 3: Optional PIE “full flow” test

- If we want a single “load level → wait ready → start PIE → run PIE checks” test:
  - Add a **latent** test that: (1) latent load level + wait for ready, (2) start PIE (via LevelEditorSubsystem), (3) wait a few frames (yield), (4) run the same checks as `pie_test_runner.run_checks()`, (5) stop PIE. Results can be written to `Saved/pie_test_results.json` or reported via the automation framework.
  - This is optional and can live in `Content/Python/tests/` with a name like `test_level_pie_flow.py` (or similar), so that “run Test Automation” can cover level load + PIE in one go.
- **Document** that this test requires the Editor and may take 30–60 seconds; CI may run it only on a schedule or on demand.

**Implemented:** Phase 3 implemented: [test_level_pie_flow.py](../Content/Python/tests/test_level_pie_flow.py) runs load → ready → start PIE → run checks → stop PIE; takes ~30–60 s, run on demand or in scheduled CI.

### Phase 4: Map Check and validation (optional)

- Consider a **custom Map Check** or **Asset Data Validation** rule that, for World Partition maps, warns if “Landscape has zero bounds when opened” (e.g. “Run Load All for full bounds”) — so designers get a reminder. This is optional and can be a later iteration.
- Keep **Asset Data Validation** and **Map Check** in mind for “level setup” checks (e.g. “exactly one PlayerStart,” “PCG volume has graph assigned”) as in Andrew Fray’s overview; the smart level loader does not replace those.

**Phase 4 (partial):** [check_level_bounds.py](../Content/Python/check_level_bounds.py) — runnable check: run from Tools > Execute Python Script or MCP; warns if the current level has a Landscape but zero bounds (suggests Window > World Partition > Load All). Use before running create_homestead_from_scratch when the volume must match landscape size.

**Future work:** Full integration: register a Python `EditorValidatorBase` (or C++ Map Check) so validation runs automatically on level save or via Tools > Validate Data; same warning when Landscape has zero bounds. Python validators must register with `EditorValidatorSubsystem`. See Epic docs: Data Validation, EditorValidatorBase.

---

## 5. Summary of findings applied

| Finding | Application in plan |
|--------|----------------------|
| Editor doesn’t tick during Python | Use AutomationScheduler + latent commands (generators with `yield`) for any test that loads a level and must wait for load/streaming. |
| World Partition streams cells | Ready condition can be “landscape bounds or WP runtime bounds”; document “Load All” for full geometry. |
| Landscape 0 components / 0 bounds | Already handled in create_homestead_from_scratch via component aggregation + WP runtime bounds + config fallback; centralize in level_loader. |
| No Python “Load All” API | Document manual step; optional future: explore C++ or Editor subsystem to trigger “Load All” from Python. |
| PIE tests assume level open | Keep current contract; add optional latent test that loads level then PIE then runs checks. |
| Epic latent command timeout | Use `set_latent_command_timeout()` for level-load tests to avoid hangs. |

---

## 6. References

- [Write Editor Tests with Python in Unreal Engine](https://dev.epicgames.com/documentation/en-us/unreal-engine/write-editor-tests-with-python-in-unreal-engine) — Latent commands, AutomationScheduler, level load example.
- [UPyAutomationTestLibrary](https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Plugins/PythonAutomationTest/UPyAutomationTestLibrary) — Latent command timeout.
- [World Partition](https://dev.epicgames.com/documentation/en-us/unreal-engine/world-partition-in-unreal-engine) — Overview.
- [Get Runtime World Bounds](https://dev.epicgames.com/documentation/en-us/unreal-engine/BlueprintAPI/WorldPartition/GetRuntimeWorldBounds) — World Partition bounds when geometry not streamed.
- [The Topography of Unreal Test Automation in 2025 (Andrew Fray)](https://andrewfray.wordpress.com/2025/04/09/the-topography-of-unreal-test-automation-in-2025/) — Map Check, Asset Validation, Spec, CQTest.
- HomeWorld: [PCG_SETUP.md](PCG_SETUP.md), [HOMESTEAD_MAP.md](HOMESTEAD_MAP.md), [PCG_VARIABLES_NO_ACCESS.md](PCG_VARIABLES_NO_ACCESS.md), [create_homestead_from_scratch.py](../Content/Python/create_homestead_from_scratch.py), [pie_test_runner.py](../Content/Python/pie_test_runner.py).
