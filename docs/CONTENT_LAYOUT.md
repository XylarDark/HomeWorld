# HomeWorld – Content layout

Single source of truth for Content paths. Scripts, configs, and MCP assume these paths. Do not rename or move top-level folders without updating this doc and all references.

---

## Project-owned content: `/Game/HomeWorld/`

All project-specific assets live under `/Game/HomeWorld/`.

| Path | Purpose |
|------|--------|
| `/Game/HomeWorld/Maps/` | Levels (e.g. Main, Homestead). **Main** is primary demo/overworld; **Homestead** is the homestead-focused map (tutorial home, compound, surrounding zones). See [HOMESTEAD_MAP.md](HOMESTEAD_MAP.md). |
| `/Game/HomeWorld/Characters/` | Character Blueprints, Animation Blueprints (e.g. BP_HomeWorldCharacter, ABP_HomeWorldCharacter). |
| `/Game/HomeWorld/GameMode/` | GameMode Blueprints (e.g. BP_GameMode). |
| `/Game/HomeWorld/PCG/` | PCG graphs and related assets (e.g. ForestIsland_PCG). |
| `/Game/HomeWorld/Mass/` | Mass Entity configs (e.g. MEC_FamilyGatherer), spawner presets. Week 2+ family agents. |
| `/Game/HomeWorld/AI/` | State Trees (e.g. ST_FamilyGatherer), shared AI assets. |
| `/Game/HomeWorld/ZoneGraph/` | ZoneGraph data / lanes for home/forest (optional; may live under Maps). |
| `/Game/HomeWorld/SmartObjects/` | Smart Object definitions (e.g. Harvestable, Bed). |
| `/Game/HomeWorld/Building/` | Build order Blueprints (BP_BuildOrder_Wall, etc.), building-related assets. Smart Object definitions for building (e.g. SO_WallBuilder) can live here or under SmartObjects. |
| `/Game/HomeWorld/Milady/` | Milady character import pipeline: imported VRM/GLB meshes (Meshes, Generated), materials (Materials), retargeted animations (Animations), Blueprints (e.g. BP_MiladyCharacter). See [MILADY_IMPORT_ROADMAP.md](tasks/MILADY_IMPORT_ROADMAP.md). |
| `/Game/HomeWorld/Homestead/` | Homestead map assets: Structures, Placeholders (central house, outbuildings, walls). See [HOMESTEAD_MAP.md](HOMESTEAD_MAP.md). PCG graphs for Homestead can live here or under `/Game/HomeWorld/PCG/`. |

Other subfolders under `/Game/HomeWorld/` (e.g. Blueprints, UI, Materials) may be added as the project grows. New project content should go under `/Game/HomeWorld/` or a documented subfolder.

---

## Character/skeleton assets: `/Game/Man/`

Character mesh, skeleton, and animation sequences (e.g. FAB survival character or equivalent).

- Skeletal mesh: e.g. `/Game/Man/Mesh/Full/SK_Man_Full_01`
- Animations: e.g. `/Game/Man/Demo/Animations/` (ThirdPersonIdle, ThirdPersonWalk, etc.)

Referenced by [character_blueprint_config.json](../Content/Python/character_blueprint_config.json) and setup scripts.

---

## Third-party / shared content

Top-level content folders not under `/Game/HomeWorld/` or `/Game/Man/` are third-party or shared (e.g. marketplace packs). Do not rename these; reference them by their existing paths.

- Example: `StylizedProvencal` — environment/biome assets, used by PCG and demo map.

---

## Python and config paths

- **Python scripts:** `Content/Python/` (e.g. `bootstrap_project.py`, `create_homestead_from_scratch.py`).
- **Configs:** `Content/Python/*.json` (e.g. `homestead_map_config.json`, `pcg_forest_config.json`, `character_blueprint_config.json`).

Paths in config files use `/Game/...` asset paths; file paths are relative to project root or `Content/Python/`.

### Script index

| Script | Purpose | Entry / called-by | Config |
|--------|---------|-------------------|--------|
| `bootstrap_project.py` | One-click project setup: Enhanced Input, AnimBP, character BP, project settings, level (optional PCG). | Entry | — |
| `create_homestead_from_scratch.py` | Ensures Homestead exists, opens it, creates/sizes PCG volume and graph (ForestIsland_PCG). | Entry | homestead_map_config.json |
| `create_pcg_forest.py` | Creates PCG graph (Get Landscape Data, Surface Sampler, Density, Transform, Spawner), tags Landscape, places PCG volume. | Called by create_homestead_from_scratch | pcg_forest_config.json |
| `level_loader.py` | Level open/load, landscape bounds, WP streaming helpers. | Library (used by create_homestead, check_level_bounds, tests) | — |
| `ensure_homestead_map.py` | Idempotent: duplicate Main to Homestead if Homestead does not exist. | Standalone (also used by create_homestead_from_scratch) | homestead_map_config.json |
| `ensure_homestead_folders.py` | Idempotent: create `/Game/HomeWorld/Homestead/`, Structures, Placeholders. | Standalone | — |
| `ensure_milady_folders.py` | Idempotent: create Milady content folders (Meshes, Materials, Animations, Blueprints). | Standalone | — |
| `ensure_week2_folders.py` | Idempotent: create Mass, AI, ZoneGraph, SmartObjects, Building. | Standalone | — |
| `place_homestead_placeholders.py` | Spawn placeholders from config (house, outbuildings). | Standalone | homestead_map_config.json |
| `setup_level.py` | PlayerStart, optional run of create_homestead_from_scratch. | Called by bootstrap_project | — |
| `setup_enhanced_input.py` | IA_Move, IA_Look, IMC_Default. | Called by bootstrap; also init_unreal.py on Editor load | — |
| `setup_animation_blueprint.py` | ABP_HomeWorldCharacter. | Called by bootstrap_project | character_blueprint_config.json |
| `setup_character_blueprint.py` | BP_HomeWorldCharacter. | Called by bootstrap_project | character_blueprint_config.json |
| `setup_project_settings.py` | Game mode, default map, pawn class. | Called by bootstrap_project | — |
| `init_unreal.py` | Runs on Editor load; applies Enhanced Input. | Editor startup | — |
| `check_level_bounds.py` | Report landscape bounds (for scripts that depend on landscape size). | Standalone | — |
| `mcp_harness.py` | Structured command-response bridge for agents (Saved/mcp_request.json → mcp_response.json). | Agent tool | — |
| `pie_test_runner.py` | PIE validation (character, ground, PCG); writes Saved/pie_test_results.json. | Agent tool | — |
| `blueprint_inspector.py` | Read Blueprint structure as JSON (Saved/blueprint_inspect_request.json → result). | Agent tool | — |
| `capture_viewport.py` | Screenshot capture; writes Saved/screenshot_result.json. | Agent tool | — |
| `layout_blueprint_nodes.py` | Space Blueprint graph nodes in a grid. | Agent tool | — |
| `create_milady_pastel_material.py` | Creates M_MiladyPastel material. | Standalone | — |
| `run_pie_verify.py` | Run PIE and run pie_test_runner. | Standalone | — |

Tests live in `Content/Python/tests/` (e.g. `test_level_loader.py`, `test_pcg_forest.py`). Run via Editor: Tools > Test Automation.

---

**See also:** [SETUP.md](SETUP.md), [STACK_PLAN.md](STACK_PLAN.md), [CONVENTIONS.md](CONVENTIONS.md).
