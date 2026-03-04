# Day 17 [3.2] PCG POI placement — implementation plan

**Goal:** PCG graph on the planetoid level that places POI actors (Shrine, Treasure, and optionally Cultivation/Mining placeholders).

**Task doc:** [docs/tasks/DAYS_16_TO_30.md](../docs/tasks/DAYS_16_TO_30.md) (Day 17), [docs/PLANETOID_DESIGN.md](../docs/PLANETOID_DESIGN.md).

## Key steps

1. **Ensure planetoid level exists and open it.** Run `ensure_planetoid_level.py` if needed; open Planetoid_Pride (or level from `planetoid_map_config.json`).
2. **Create or extend PCG graph for planetoid.** Either:
   - **Option A:** New PCG graph (e.g. `Planetoid_POI_PCG`) with Get Landscape Data (By Tag `PCG_Landscape`), Surface Sampler, and **Actor Spawner** nodes for POI Blueprints. Use placeholder Blueprint classes (e.g. BP_Shrine_POI, BP_Treasure_POI) or engine defaults (e.g. StaticMeshActor with cube) if Blueprints don't exist yet.
   - **Option B:** Reuse/create script similar to `create_pcg_forest.py` but for planetoid: config-driven POI density and actor class paths; place PCG Volume on planetoid level; create graph with Actor Spawner(s).
3. **Create placeholder POI Blueprints if missing.** Minimal Blueprints (e.g. BP_Shrine_POI, BP_Treasure_POI) derived from Actor or StaticMeshActor so the PCG Actor Spawner has a class to spawn. Can be cubes with tags; Day 18 will add interaction.
4. **Validation:** Open planetoid level, run script or manual PCG setup, Generate; confirm POI actors appear (or document manual steps in task doc).

## Success criteria

- Planetoid level has a PCG graph that spawns at least one POI type (e.g. Shrine or Treasure placeholder).
- POI placement is configurable (density/points) or documented for manual tuning.
- Task doc DAYS_16_TO_30 Day 17 updated with implementation notes and any manual steps (graph assignment, mesh/Blueprint assignment per PCG_VARIABLES_NO_ACCESS).

## Notes

- Follow [docs/PCG_BEST_PRACTICES.md](../docs/PCG_BEST_PRACTICES.md) and [docs/PCG_VARIABLES_NO_ACCESS.md](../docs/PCG_VARIABLES_NO_ACCESS.md). Actor Spawner template/class may require manual assignment in Editor.
- Planetoid level must have a Landscape with tag `PCG_Landscape` (or equivalent) for Get Landscape Data to work; add minimal landscape if Empty Open World has none.
