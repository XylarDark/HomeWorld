# HomeWorld – Content layout

Single source of truth for Content paths. Scripts, configs, and MCP assume these paths. Do not rename or move top-level folders without updating this doc and all references.

---

## Project-owned content: `/Game/HomeWorld/`

All project-specific assets live under `/Game/HomeWorld/`.

| Path | Purpose |
|------|--------|
| `/Game/HomeWorld/Maps/` | Levels. **MainMenu** is the main menu map (create via ensure_main_menu_map.py; set GameDefaultMap to start here). **DemoMap** is the primary demo/playable map for MVP (Empty Open World, no duplicate). **Planetoid_Pride** (Day 16+) is the first planetoid level; travel from DemoMap via portal. **Dungeon_Interior** (Day 24) optional dungeon sublevel; use **BP_DungeonEntrance** (C++ AHomeWorldDungeonEntrance) at entrance to open. **Main** and **Homestead** are legacy/narrative. See [DEMO_MAP.md](DEMO_MAP.md), [HOMESTEAD_MAP.md](HOMESTEAD_MAP.md), [CHARACTER_GENERATION_AND_CUSTOMIZATION.md](CHARACTER_GENERATION_AND_CUSTOMIZATION.md), [tasks/DAYS_16_TO_30.md](tasks/DAYS_16_TO_30.md). |
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
| `/Game/HomeWorld/Harvestables/` | Static meshes for harvestables (trees, rocks, flowers). Assigned to BP_HarvestableTree etc.; filled by batch import from `AssetCreation/Exports/Harvestables/`. See [AssetCreation/README.md](../AssetCreation/README.md). |
| `/Game/HomeWorld/Dungeon/` | Dungeon kit pieces (walls, pillars, doors, props). Filled by batch import from `AssetCreation/Exports/Dungeon/`. See [AssetCreation/README.md](../AssetCreation/README.md). |
| `/Game/HomeWorld/Biomes/` | Biome props (trees, rocks, plants for PCG or placement). Filled by batch import from `AssetCreation/Exports/Biomes/`. See [AssetCreation/README.md](../AssetCreation/README.md). |
| `/Game/HomeWorld/UI/` | Main menu and character UI: **WBP_MainMenu** (parent HomeWorldMainMenuWidget), **WBP_CharacterCreate** / **WBP_CharacterCustomize**. Create folder via ensure_ui_folders.py. See [CHARACTER_GENERATION_AND_CUSTOMIZATION.md](CHARACTER_GENERATION_AND_CUSTOMIZATION.md). |

Other subfolders under `/Game/HomeWorld/` (e.g. Blueprints, Materials) may be added as the project grows. New project content should go under `/Game/HomeWorld/` or a documented subfolder.

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

- **Python scripts:** `Content/Python/` (e.g. `bootstrap_project.py`, `create_demo_from_scratch.py`, `create_homestead_from_scratch.py`).
- **Source assets:** `AssetCreation/` at project root — Blender exports (FBX/GLB) go in `AssetCreation/Exports/<Category>/`; batch import script reads from there and imports into `/Game/HomeWorld/...`. See [AssetCreation/README.md](../AssetCreation/README.md) and [ASSET_WORKFLOW_AND_STEAM_DEMO.md](ASSET_WORKFLOW_AND_STEAM_DEMO.md) §1.
- **Configs:** `Content/Python/*.json` (e.g. `demo_map_config.json`, `planetoid_map_config.json` for Day 16 planetoid/portal, `dungeon_map_config.json` for Day 24 dungeon entrance, `pcg_forest_config.json`, `character_blueprint_config.json`; `homestead_map_config.json` for legacy Homestead map).

Paths in config files use `/Game/...` asset paths; file paths are relative to project root or `Content/Python/`.

### Script index

| Script | Purpose | Entry / called-by | Config |
|--------|---------|-------------------|--------|
| `bootstrap_project.py` | One-click project setup: Enhanced Input, AnimBP, character BP, project settings, level (optional PCG). | Entry | — |
| `create_demo_from_scratch.py` | Ensures DemoMap exists (manual create), opens it, creates/sizes PCG volume and graph (ForestIsland_PCG). Primary demo flow. | Entry | demo_map_config.json |
| `ensure_demo_map.py` | Idempotent: check DemoMap exists; if not, log manual steps (File -> New Level -> Empty Open World -> Save As). | Standalone (also used by create_demo_from_scratch) | demo_map_config.json |
| `create_homestead_from_scratch.py` | Ensures Homestead exists (duplicate from Main if missing), opens it, creates/sizes PCG volume and graph. Legacy/campaign. | Entry | homestead_map_config.json |
| `create_pcg_forest.py` | Creates PCG graph (Get Landscape Data, Surface Sampler, Density, Transform, Spawner), tags Landscape, places PCG volume. | Called by create_demo_from_scratch, create_homestead_from_scratch | pcg_forest_config.json |
| `level_loader.py` | Level open/load, landscape bounds, WP streaming helpers. | Library (used by create_demo, create_homestead, check_level_bounds, tests) | — |
| `ensure_homestead_map.py` | Idempotent: duplicate Main to Homestead if Homestead does not exist. | Standalone (also used by create_homestead_from_scratch) | homestead_map_config.json |
| `ensure_homestead_folders.py` | Idempotent: create `/Game/HomeWorld/Homestead/`, Structures, Placeholders. | Standalone | — |
| `ensure_milady_folders.py` | Idempotent: create Milady content folders (Meshes, Materials, Animations, Blueprints). | Standalone | — |
| `ensure_week2_folders.py` | Idempotent: create Mass, AI, ZoneGraph, SmartObjects, Building. | Standalone | — |
| `place_homestead_placeholders.py` | Spawn placeholders from config (house, outbuildings). | Standalone | homestead_map_config.json |
| `create_bp_harvestable_tree.py` | Creates BP_HarvestableTree (AHomeWorldResourcePile) with ResourceType=Wood, AmountPerHarvest=10. Idempotent. Run before place_resource_nodes. | Standalone | — |
| `place_resource_nodes.py` | Spawn BP_HarvestableTree at resource_node_positions on DemoMap (Day 7). Idempotent. | Standalone | demo_map_config.json |
| `setup_level.py` | PlayerStart, optional run of create_demo_from_scratch. | Called by bootstrap_project | — |
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
| `ensure_planetoid_level.py` | Idempotent: ensure planetoid level exists (Day 16); create from template when set or log manual steps. | Standalone | planetoid_map_config.json |
| `place_portal_placeholder.py` | With DemoMap open: place portal placeholder actor at config position; tag Portal_To_Planetoid (Day 16). | Standalone | planetoid_map_config.json |
| `create_bp_poi_placeholders.py` | Creates BP_Shrine_POI, BP_Treasure_POI (Actor) for Day 17 PCG POI. | Standalone | — |
| `create_planetoid_poi_pcg.py` | Creates Planetoid_POI_PCG graph (Actor Spawner) for planetoid level (Day 17). | Standalone | planetoid_map_config.json |
| `create_bp_yield_nodes.py` | Creates BP_Cultivation_POI, BP_Mining_POI (AHomeWorldYieldNode) with tags and yield defaults (Day 19). | Standalone | — |
| `place_dungeon_entrance.py` | With level open: place dungeon entrance placeholder at config position; tag Dungeon_POI (Day 24). | Standalone | dungeon_map_config.json |
| `place_mass_spawner_demomap.py` | Idempotent: ensure Mass Spawner on DemoMap with MEC_FamilyGatherer config and spawn count (Day 11). | Standalone | demo_map_config.json |
| `set_mec_representation_mesh.py` | Set Static Mesh (Cube) on MEC_FamilyGatherer representation trait. | Standalone | — |
| `batch_import_asset_creation.py` | Batch import FBX/GLB from `AssetCreation/Exports/` into `/Game/HomeWorld/` by category (Characters, Harvestables, Homestead, Dungeon, Biomes). Idempotent; run from Editor or MCP. | Standalone | — |

Tests live in `Content/Python/tests/` (e.g. `test_level_loader.py`, `test_pcg_forest.py`). Run via Editor: Tools > Test Automation.

---

**See also:** [SETUP.md](SETUP.md), [STACK_PLAN.md](STACK_PLAN.md), [CONVENTIONS.md](CONVENTIONS.md).
