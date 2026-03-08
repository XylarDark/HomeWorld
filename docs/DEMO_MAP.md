# Demo Map (Primary Demo / MVP Build-out)

DemoMap is the **primary demo and playable map** for HomeWorld. It is created as an **Empty Open World** (World Partition from the start), so there is no duplicate-from-Main or convert step. You add a minimal landscape once, then scripts set up PCG, volume, and graph.

---

## Purpose

- **Clean base:** No dependency on Main or Homestead (no Provencal retrofit). World Partition is enabled by default (Empty Open World template).
- **MVP build-out:** Add StylizedProvencal or other assets gradually; reference them in PCG config and content. This map becomes the playable demo and MVP level.
- **Script target:** All demo automation (create_demo_from_scratch, setup_level when run_pcg=True, bootstrap next-steps) uses DemoMap.

---

## Creating the map

**Automatic (when template is configured):** Set **`template_level_path`** in [demo_map_config.json](../Content/Python/demo_map_config.json) to a project-owned Empty Open World level (e.g. create once: File → New Level → Empty Open World → Save As `/Game/HomeWorld/Maps/Templates/EmptyOpenWorld`). Then run **ensure_demo_map.py** or **create_demo_from_scratch.py**; when DemoMap is missing, the script creates it from that template via `NewLevelFromTemplate`. No manual "File → New Level" step.

**One-time manual (when no template):** If `template_level_path` is not set:
1. In the Editor: **File → New Level** → choose **Empty Open World** → **Create**.
2. **File → Save As** → save to **Content/HomeWorld/Maps/** as **DemoMap** (path `/Game/HomeWorld/Maps/DemoMap`).
3. Confirm **World Settings → World Partition** is enabled (it is, for Empty Open World).

---

## Adding a minimal landscape (one-time manual)

1. With DemoMap open: **Mode** panel → **Landscape** → **Create New**.
2. Create a small landscape (e.g. 1–2 sections for speed).
3. In Details set **Component Subsection** to **1 x 1** (required for PCG in UE 5.x).
4. Add tag **PCG_Landscape** to the Landscape actor (Details → Actor → Tags).

---

## Config and scripts

- **Config:** [Content/Python/demo_map_config.json](../Content/Python/demo_map_config.json) — `demo_level_path`, `template_level_path` (optional; when set, DemoMap is created from this template when missing), `volume_center_*`, `volume_extent_*`, `exclusion_zones`, `recreate_volume_and_graph`, `use_landscape_bounds`. No `source_level_path`; this map is never duplicated.
- **Scripts:**
  - **ensure_demo_map.py** — Checks that DemoMap exists; if not, creates it from `template_level_path` when set (via `NewLevelFromTemplate`), else logs manual steps. Run from Editor or MCP.
  - **create_demo_from_scratch.py** — Calls ensure_demo_map, opens DemoMap, tags landscape, creates/reuses PCG volume and ForestIsland_PCG graph, tries to assign graph and trigger Generate. Run with DemoMap open or let it open the level.
  - **setup_level.py** — Run with DemoMap open to add a **PlayerStart** (so the character spawns in PIE) and **Directional Light + Sky Light** (so the level is not black). Run after creating the map and landscape; then save and press Play.

**Homestead spawn (MVP tutorial List 2):** When run on DemoMap, setup_level.py places the PlayerStart at the **center of the homestead compound** (first exclusion zone in `demo_map_config.json`). That ensures the player spawns in or at the homestead for the "wake up in homestead" tutorial step. **Verify:** Open DemoMap, run setup_level.py (Tools → Execute Python Script, or MCP `execute_python_script("setup_level.py")`), start PIE, and confirm the character spawns at the compound (viewport or Output Log: "Spawned PlayerStart at …" / "Using homestead spawn (first exclusion zone center)").

**Build orders and family agents (List 60 / agentic building):** To give DemoMap **at least one incomplete build order** and **family agents** for the agentic-building test: (1) Run **create_bp_build_order_wall.py** (ensures BP_BuildOrder_Wall and PlaceActorClass on BP_HomeWorldCharacter). (2) Run **place_build_order_wall.py** (places one BP_BuildOrder_Wall at `demo_map_config.json` **build_order_wall_position**; idempotent). (3) Run **place_mass_spawner_demomap.py** (places Mass Spawner with MEC_FamilyGatherer per **mass_spawner_*** in config). After that, DemoMap has build order(s) and family agent(s); PIE can demonstrate "agent completes one build order" when the State Tree BUILD branch is set up (see [DAY10_AGENTIC_BUILDING.md](tasks/DAY10_AGENTIC_BUILDING.md) and [AGENTIC_BUILDING.md](tasks/AGENTIC_BUILDING.md)), or use console **hw.PlaceWall** / **hw.CompleteBuildOrder** / **hw.SimulateBuildOrderActivation** for Path 1 verification.

Volume bounds come from config; if `use_landscape_bounds` is true, the script tries landscape then World Partition bounds. For a small playable area, set `use_landscape_bounds: false` and set `volume_center_*` and `volume_extent_*` to match your landscape. See [PCG_QUICK_SETUP.md](PCG_QUICK_SETUP.md).

---

## PCG manual steps (after running the script)

After **create_demo_from_scratch.py**, complete these steps once (engine API limits in UE 5.7):

1. **Get Landscape Data:** Open ForestIsland_PCG → select Get Landscape Data → Details: Actor → **By Tag**, tag **PCG_Landscape**; Component → **By Class** → **Landscape Component**.
2. **Meshes:** Set mesh list on tree (and rocks) Static Mesh Spawner from [Content/Python/pcg_forest_config.json](../Content/Python/pcg_forest_config.json). Save the graph.
3. **Load World Partition region (required for Empty Open World):** In a World Partition level the root Landscape has 0 components (they live in LandscapeStreamingProxy). **Window → World Partition** → select the cell(s) that contain your landscape → **Load region from selection**. Then run **create_demo_from_scratch.py** again (or **pcg_generate_nothing_diagnostic.py** once); the script tags all loaded LandscapeStreamingProxy actors with **PCG_Landscape** so Get Landscape Data finds the full landscape surface. Without this, Generate produces nothing.
4. **Assign and Generate:** In the level, select PCG_Forest → Details → Graph → ForestIsland_PCG → **Generate** (or Ctrl+Click). Save the level.

See [PCG_QUICK_SETUP.md](PCG_QUICK_SETUP.md) Option B for the full flow.

---

## Default map (optional)

To open DemoMap by default when starting the Editor or PIE: set in **Config/DefaultEngine.ini**:

- `GameDefaultMap=/Game/HomeWorld/Maps/DemoMap.DemoMap`
- `EditorStartupMap=/Game/HomeWorld/Maps/DemoMap.DemoMap`

---

## Legacy maps

- **Main** and **Homestead** remain in the project. Homestead is used for narrative/campaign content when needed; scripts **ensure_homestead_map.py** and **create_homestead_from_scratch.py** still target Homestead. The **primary demo and MVP build-out** use **DemoMap** and **create_demo_from_scratch.py**.
