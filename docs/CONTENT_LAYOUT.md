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

- **Python scripts:** `Content/Python/` (e.g. `bootstrap_project.py`, `create_demo_map.py`).
- **Configs:** `Content/Python/*.json` (e.g. `demo_map_config.json`, `pcg_forest_config.json`, `character_blueprint_config.json`).

Paths in config files use `/Game/...` asset paths; file paths are relative to project root or `Content/Python/`.

---

**See also:** [SETUP.md](SETUP.md), [STACK_PLAN.md](STACK_PLAN.md), [CONVENTIONS.md](CONVENTIONS.md).
