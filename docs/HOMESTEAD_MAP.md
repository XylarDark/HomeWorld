# Homestead Map

Homestead-focused level for the tutorial home, compound (house, outbuildings, walls), and surrounding zones. Used for Day 1 layout and Phase 1 of the [Homestead & Planetoid roadmap](tasks/HOMESTEAD_PLANETOID_ROADMAP.md).

---

## Purpose

- **Tutorial and campaign:** Player starts at the homestead with family; after the attack they spend 7 levels getting the family back; later they return to a ruined homestead for the day/night loop ([CAMPAIGN_VISION.md](CAMPAIGN_VISION.md)).
- **Single map for “home”:** Keeps Main as demo/overworld; Homestead is where we develop resource collection, home building, family, and defenses.
- **Travel later:** Portal or sublevel from Homestead to sin-themed planetoids fits the campaign.

---

## Layout summary

| Zone | Contents |
|------|----------|
| **Central house** | One main building with six room areas: **bedroom**, **dining room**, **kitchen**, **bathroom**, **attic**, **basement**. Implement as blockout volumes, named triggers, or subdivided floor plan with placeholder walls. |
| **Outbuildings (around house)** | Magical stone mill, lumber mill, water mill, well, loom, forge, garbage portal. Each is a placeholder (Engine primitive or Blueprint) until final art. |
| **Walls and defenses** | Walls enclosing the compound; defense points (turrets or placeholders) at intervals. |
| **Surrounding** | **Rock quarry**, **forest** (PCG), **animals** (placeholder), **garden**, **field**. |

---

## Content paths

- **Map:** `/Game/HomeWorld/Maps/Homestead` — create by duplicating Main, or run `Content/Python/ensure_homestead_map.py` (duplicates Main if Homestead does not exist). After converting to World Partition you may see **Homestead** and **Homestead_WP**; see below for which to use and how to keep only one.

### Why two maps (Homestead vs Homestead_WP)?

**Tools → Convert Level** creates a **new** World Partition level (e.g. **Homestead_WP**) and leaves the original (**Homestead**) in place. So you get:

- **Homestead** — the original duplicated level (no World Partition, or outdated).
- **Homestead_WP** — the converted level with World Partition and streaming; **this is the one to use**.

**To have only one map:** (1) In Content Browser, **delete** the old **Homestead** (the non–World Partition one; confirm in World Settings which is which). (2) **Rename** **Homestead_WP** to **Homestead** (right‑click → Rename). You then have a single map at `/Game/HomeWorld/Maps/Homestead` and all scripts/config that reference that path still work. If you prefer to keep the name Homestead_WP, set `homestead_level_path` in `Content/Python/homestead_map_config.json` to `/Game/HomeWorld/Maps/Homestead_WP` and use that map for all Homestead work.

### World Partition on Homestead (duplicated level)

If you created Homestead by duplicating Main, **World Settings → World Partition** may show **None** and be uneditable. Duplicated levels are not converted to World Partition automatically. **Fix:** With Homestead open, use **Tools → Convert Level** from the main menu to convert the level to World Partition. Save the level afterward. See [KNOWN_ERRORS.md](KNOWN_ERRORS.md) (duplicated level: World Partition shows None).

**Conversion time:** Converting can take **several minutes to 30+ minutes** because Homestead was duplicated from Main (landscape, many actors, possibly PCG instances). This is normal. Let it finish; check Task Manager for UnrealEditor CPU/disk activity if it seems stuck.

**After conversion finishes:** (1) Save the level (Ctrl+S). (2) Run `Content/Python/ensure_homestead_folders.py` if you haven’t yet. (3) Run `Content/Python/place_homestead_placeholders.py` to spawn house/outbuilding placeholders, or place them manually. (4) Run `Content/Python/create_homestead_pcg.py` (with Homestead open) to add the PCG volume and tag the Landscape; then complete the manual PCG steps in [PCG_SETUP.md](PCG_SETUP.md). (5) If you see no ground (placeholders/PCG floating): the Landscape may be in an unloaded cell — see **No ground visible** below.

### No ground visible (placeholders / trees floating)

After World Partition conversion, the **Landscape** can end up in a **streaming cell** that isn’t loaded in the Editor, so you see no ground. **Fix:** (1) **Window → World Partition** to open the World Partition window. (2) Use **Load All** (or **Load All Streamed Levels** / **Load All Cells** depending on UE version) so every cell loads, including the one containing the Landscape. The ground should appear. (3) If you prefer to keep cells unloaded for performance, use **Streaming** or **Loading** options to load only the region around the origin (e.g. 0,0,0) where your placeholders are. (4) If there is still no Landscape in the Outliner, the conversion may have omitted it: add a new one via **Landscape** mode (**Mode** panel → **Landscape**) → **Create New** and create a new landscape in the level. See [KNOWN_ERRORS.md](KNOWN_ERRORS.md) (Homestead: no ground visible).
- **Homestead assets:** `/Game/HomeWorld/Homestead/` with subfolders **Structures**, **Placeholders** (ensure via `Content/Python/ensure_homestead_folders.py`).
- **PCG:** Reuse `/Game/HomeWorld/PCG/ForestIsland_PCG` or add a dedicated graph (e.g. Homestead_PCG) under `/Game/HomeWorld/PCG/` or `/Game/HomeWorld/Homestead/`. Config: `Content/Python/homestead_map_config.json` (volume bounds, exclusion_zones for compound).

See [CONTENT_LAYOUT.md](CONTENT_LAYOUT.md) for the full path table.

---

## PCG summary

- **Forest (and optionally quarry/garden/field):** Use the same approach as Main ([PCG_SETUP.md](PCG_SETUP.md)): Landscape tagged **PCG_Landscape**, Component Subsection **1x1**, one PCG Volume covering the level with **exclusion zone(s)** for the compound so trees do not spawn inside the walls.
- **Config:** `homestead_map_config.json` defines `volume_extent_*` and `exclusion_zones` (compound center + half-extents in cm). Script `create_homestead_pcg.py` (or equivalent) can create/size the PCG Volume and feed exclusion zones when the Homestead level is open.
- **Manual steps:** After running the script, set Get Landscape Data (By Tag `PCG_Landscape`), mesh list on Static Mesh Spawner(s), assign graph to volume, and click **Generate** from the volume’s Details panel. See [PCG_SETUP.md](PCG_SETUP.md) and [PCG_VARIABLES_NO_ACCESS.md](PCG_VARIABLES_NO_ACCESS.md).

---

## Asset strategy

| Element | Source | Notes |
|---------|--------|------|
| **Central house** | StylizedProvencal building, or grouped **Cube/Plane** blockout | Rooms: blockout volumes or named subvolumes. |
| **Outbuildings** (mill, well, loom, forge, garbage portal) | **Placeholders:** Engine primitives (Cube, Cylinder) or simple Blueprints | Replace with final art later. |
| **Walls and defenses** | StylizedProvencal walls if available; else **Cube/Plane** segments; defenses = placeholder cubes | |
| **Forest** | Existing PCG tree meshes (e.g. from StylizedProvencal or pcg_forest_config.json) | Same as Main. |
| **Quarry** | StylizedProvencal rocks or PCG rock branch; or placed placeholder rocks | |
| **Garden / field** | Planes with materials, or low-density PCG grass/crop meshes | |
| **Animals** | Placeholder **Capsule** or simple mesh; later replace with animal Blueprints | |
| **Building system** | [Building](CONTENT_LAYOUT.md) folder: BP_WoodPile, build orders | For resource and placement (Phase 1). |

---

## Task linkage

- **Day 1 (1.1):** Homestead layout — the Homestead map and this doc implement the “authored map + placeholders + PCG” option. See [HOMESTEAD_DAILY_ROADMAP.md](tasks/HOMESTEAD_DAILY_ROADMAP.md).
- **Phase 1:** Homestead generation, resources, home placement. See [HOMESTEAD_PLANETOID_ROADMAP.md](tasks/HOMESTEAD_PLANETOID_ROADMAP.md).

---

## Scripts and config

| Item | Purpose |
|------|---------|
| `Content/Python/homestead_map_config.json` | `homestead_level_path`, `source_level_path`, PCG `volume_extent_*`, `exclusion_zones`. |
| `Content/Python/ensure_homestead_map.py` | Idempotent: duplicate Main to Homestead if Homestead does not exist. |
| `Content/Python/ensure_homestead_folders.py` | Idempotent: create `/Game/HomeWorld/Homestead/`, Structures, Placeholders. |
| `Content/Python/create_homestead_pcg.py` | (Optional) Create/size PCG Volume in Homestead, apply exclusion from config; manual steps still required for graph assignment and Generate. |
| `Content/Python/place_homestead_placeholders.py` | (Optional) Spawn Cube placeholders for house and outbuildings from `homestead_map_config.json` → `placeholder_actors`. Idempotent: re-run replaces placeholders. |
